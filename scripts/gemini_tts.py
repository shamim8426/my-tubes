"""Gemini TTS helper. Key from .env (never printed). Every call is logged to cost_log.csv."""
import base64
import os
import wave
from pathlib import Path

from dotenv import load_dotenv

import cost_log
import gemini_keys
import pricing

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-3.8-flash-tts")  # opt-in override (own daily quota per model); default unchanged
# prices: shared/pricing.json (scripts/pricing.py); kept as names for older callers
PRICE_IN = pricing.rates(MODEL)["input_per_1m"]
PRICE_OUT = pricing.rates(MODEL)["output_audio_per_1m"]
AUDIO_TOKENS_PER_SEC = pricing.rates(MODEL)["audio_tokens_per_sec"]
SR = 24000


def _find(obj, pred):
    if isinstance(obj, dict):
        if pred(obj):
            return obj
        for v in obj.values():
            if (hit := _find(v, pred)) is not None:
                return hit
    elif isinstance(obj, list):
        for v in obj:
            if (hit := _find(v, pred)) is not None:
                return hit
    return None


def _usage_tokens(js):
    """(input_tokens, output_tokens) if the response reports usage, else (None, None)."""
    u = _find(js, lambda d: any("token" in k.lower() for k in d) and not d.get("data"))
    if not u:
        return None, None
    get = lambda *names: next((u[k] for k in u for n in names if k.lower() == n), None)
    return get("input_tokens", "total_input_tokens", "prompttokencount"), \
        get("output_tokens", "total_output_tokens", "candidatestokencount")


def speak(text: str, voice: str, style: str, out: Path, free_only=False) -> dict:
    body = {
        "model": MODEL,
        "input": [{"type": "user_input", "content": [{
            "type": "text", "text": text,
            "annotations": [{"type": "speech_metadata", "style": style}]}]}],
        "response_format": {"type": "audio", "mime_type": "audio/l16", "sample_rate": SR},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }
    r, tier = gemini_keys.post(ENDPOINT, body, out, timeout=90, label="Gemini TTS",
                               free_only=free_only)  # free key first for free channels
    if not r.ok:
        raise RuntimeError(f"Gemini TTS {r.status_code}: {r.text[:500]}")
    js = r.json()
    blob = _find(js, lambda d: d.get("data") and "audio" in str(d.get("type", "")) + str(d.get("mime_type", "")))
    if not blob:
        raise RuntimeError(f"No audio in response: {str(js)[:500]}")
    pcm = base64.b64decode(blob["data"])
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR), w.writeframes(pcm)
    secs = len(pcm) / 2 / SR

    cost = pricing.tts_cost(MODEL, js, text_chars=len(text) + len(style), seconds=secs)
    if tier == "free":
        cost["actual_usd"] = 0.0
    estimated = cost["actual_usd"] is None
    usd = cost["estimated_usd"] if estimated else cost["actual_usd"]
    row = cost_log.record_call(out, MODEL, f"tts {secs:.1f}s{' est' if estimated else ''}{' free' if tier == 'free' else ''}", cost,
                               usage=pricing.read_usage(js))
    return {"seconds": secs, "usd": usd, "row": row, "usage_reported": not estimated}
