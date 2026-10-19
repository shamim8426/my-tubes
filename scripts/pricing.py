"""Gemini cost from the API's own usage numbers (shared/RULES.md section 15). Prices: shared/pricing.json.

    from pricing import image_cost, tts_cost
    c = image_cost(model, "1K", response_json, prompt_chars=900, n_refs=3)
    c -> {"estimated_usd", "actual_usd" (None if the response has no usage), "input_tokens", "output_tokens",
          "thought_tokens", "image_tokens"}
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "shared" / "pricing.json"


def config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def rates(model: str, on: date | None = None) -> dict:
    """The model's rates, with any "from_YYYY-MM-DD" price change that is already in force."""
    m = dict(config()["models"][model])
    today = (on or date.today()).isoformat()
    for k in sorted(k for k in m if k.startswith("from_")):
        if today >= k[5:]:
            m.update(m[k])
    return m


def usd_to_inr() -> float:
    return config()["usd_to_inr"]


def gst_rate() -> float:
    return config()["gst_pct"] / 100


# ---------- reading usage from a response ----------
IN_KEYS = ("inputtokens", "totalinputtokens", "prompttokencount", "prompttokens")
OUT_KEYS = ("outputtokens", "totaloutputtokens", "candidatestokencount", "completiontokens")
THOUGHT_KEYS = ("thoughtstokencount", "thoughttokens", "totalthoughttokens", "reasoningtokens", "totalreasoningtokens")
DETAIL_KEYS = ("candidatestokensdetails", "outputtokensdetails", "outputtokensbymodality", "totaloutputtokensbymodality")


def _norm(k: str) -> str:
    return k.replace("_", "").lower()


def _usage_dict(obj):
    """The first dict that holds token counts (never inside media data)."""
    if isinstance(obj, dict):
        keys = {_norm(k) for k in obj}
        if not obj.get("data") and keys & set(IN_KEYS + OUT_KEYS):
            return obj
        for v in obj.values():
            if (hit := _usage_dict(v)) is not None:
                return hit
    elif isinstance(obj, list):
        for v in obj:
            if (hit := _usage_dict(v)) is not None:
                return hit
    return None


def read_usage(response: dict) -> dict | None:
    """{"input", "output", "thoughts", "output_image" (None if not split by modality)} or None."""
    u = _usage_dict(response)
    if u is None:
        return None
    n = {_norm(k): v for k, v in u.items()}
    pick = lambda keys: next((int(n[k]) for k in keys if isinstance(n.get(k), (int, float))), 0)
    img = None
    for k in DETAIL_KEYS:
        if isinstance(n.get(k), list):
            for d in n[k]:
                dn = {_norm(a): b for a, b in d.items()}
                if str(dn.get("modality", "")).upper() == "IMAGE":
                    img = int(dn.get("tokencount", dn.get("tokens", 0)))
    return {"input": pick(IN_KEYS), "output": pick(OUT_KEYS), "thoughts": pick(THOUGHT_KEYS), "output_image": img}


# ---------- costs ----------
def image_estimate_usd(model: str, size: str, prompt_chars: int, n_refs: int) -> float:
    r = rates(model)
    tin = prompt_chars / 4 + n_refs * r["ref_image_tokens_est"]
    return tin / 1e6 * r["input_per_1m"] + r["image_tokens"][size] / 1e6 * r["output_image_per_1m"]


def image_cost(model: str, size: str, response: dict, prompt_chars: int, n_refs: int) -> dict:
    """Estimated and actual USD for one image call. Output tokens that are not the image (text, thinking) are
    billed at the output-text rate; if the response does not split output by modality, the image part is the
    per-size token count from the price table."""
    r = rates(model)
    est = image_estimate_usd(model, size, prompt_chars, n_refs)
    u = read_usage(response)
    if u is None:
        return {"estimated_usd": est, "actual_usd": None, "input_tokens": None, "output_tokens": None,
                "thought_tokens": None, "image_tokens": None}
    img = u["output_image"] if u["output_image"] is not None else min(u["output"], r["image_tokens"][size])
    text_out = max(u["output"] - img, 0) + u["thoughts"]
    act = (u["input"] / 1e6 * r["input_per_1m"] + img / 1e6 * r["output_image_per_1m"]
           + text_out / 1e6 * r["output_text_per_1m"])
    return {"estimated_usd": est, "actual_usd": act, "input_tokens": u["input"],
            "output_tokens": u["output"] + u["thoughts"], "thought_tokens": u["thoughts"], "image_tokens": img}


def tts_estimate_usd(model: str, text_chars: int, seconds: float) -> float:
    r = rates(model)
    return text_chars / 2 / 1e6 * r["input_per_1m"] + seconds * r["audio_tokens_per_sec"] / 1e6 * r["output_audio_per_1m"]


def tts_cost(model: str, response: dict, text_chars: int, seconds: float) -> dict:
    r = rates(model)
    est = tts_estimate_usd(model, text_chars, seconds)
    u = read_usage(response)
    if u is None:
        return {"estimated_usd": est, "actual_usd": None, "input_tokens": None, "output_tokens": None}
    out = u["output"] + u["thoughts"]
    act = u["input"] / 1e6 * r["input_per_1m"] + out / 1e6 * r["output_audio_per_1m"]
    return {"estimated_usd": est, "actual_usd": act, "input_tokens": u["input"], "output_tokens": out}
