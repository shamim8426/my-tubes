"""Track Gemini spend (images + TTS) against the prepaid balance in cost_log.csv (shared/RULES.md section 15).

Each row has the estimate made before the call and the ACTUAL cost from the response's usage numbers (blank when
the API did not report usage; then the estimate counts). GST is shown separately. Prices and limits live in
shared/pricing.json (scripts/pricing.py).
"""
import csv
import json
import os
from datetime import datetime
from pathlib import Path

import pricing
from paths import DEFAULT_CHANNEL, channel_of

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "cost_log.csv"
USAGE_LOG = ROOT / "usage_log.jsonl"  # raw usage numbers per call (no media data), for audits and tests

USD_TO_INR = pricing.usd_to_inr()
BUDGET_INR = pricing.config()["budget"]["prepaid_inr"]

FIELDS = ["timestamp", "file", "model", "size", "cost_usd", "cost_inr", "today_total_inr", "remaining_inr", "channel",
          "estimated_inr", "actual_inr", "gst_inr", "input_tokens", "output_tokens"]


def _rows():
    if not LOG.exists():
        return []
    with LOG.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _migrate():
    """Old logs (before the actual/GST columns): rewrite once with the new header; old rows keep cost_inr as the
    estimate and a blank actual."""
    if not LOG.exists():
        return
    with LOG.open(encoding="utf-8", newline="") as f:
        header = next(csv.reader(f), [])
    if header == FIELDS:
        return
    rows = _rows()
    for r in rows:
        r.setdefault("estimated_inr", r.get("cost_inr", ""))
        # old TTS rows were already priced from the API's token counts (size without "est") -> actual
        if pricing.config()["models"].get(r.get("model"), {}).get("kind") == "tts" and "est" not in r.get("size", ""):
            r["actual_inr"] = r.get("cost_inr", "")
    with LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def base_inr(r: dict) -> float:
    """Pre-GST cost of a row: actual if the API reported usage, else the estimate."""
    v = r.get("actual_inr") or r.get("cost_inr") or r.get("estimated_inr") or 0
    return float(v)


def charge_inr(r: dict) -> float:
    """What a row takes from the budget: base cost, plus GST when pricing.json budget_includes_gst."""
    b = base_inr(r)
    return b * (1 + pricing.gst_rate()) if pricing.config()["budget_includes_gst"] else b


def remaining(rows=None) -> float:
    rows = _rows() if rows is None else rows
    cp = pricing.config()["budget"]["balance_checkpoint"]
    if cp.get("timestamp") and cp.get("inr") is not None:
        return cp["inr"] - sum(charge_inr(r) for r in rows if r["timestamp"] > cp["timestamp"])
    return BUDGET_INR - sum(charge_inr(r) for r in rows)


def channel_spent(key: str, rows=None) -> float:
    """What one channel has taken from the shared balance (the "channel" column; GST as charge_inr)."""
    rows = _rows() if rows is None else rows
    return sum(charge_inr(r) for r in rows if (r.get("channel") or DEFAULT_CHANNEL) == key)


def record_call(file: Path, model: str, size: str, cost: dict, when: datetime | None = None,
                usage: dict | None = None) -> dict:
    """Log one paid call. cost = pricing.image_cost()/tts_cost() result (estimated_usd, actual_usd, tokens)."""
    _migrate()
    when = when or datetime.now()
    usd = cost["actual_usd"] if cost.get("actual_usd") is not None else cost["estimated_usd"]
    inr = usd * USD_TO_INR
    gst = inr * pricing.gst_rate()
    row = {
        "timestamp": when.strftime("%Y-%m-%d %H:%M:%S"),
        "file": Path(file).resolve().relative_to(ROOT).as_posix(),
        "model": model,
        "size": size,
        "cost_usd": f"{usd:.5f}",
        "cost_inr": f"{inr:.2f}",
        # the file's own channel folder, else the channel of the running build (make_short sets STORY_CHANNEL)
        "channel": (channel_of(file) if "channels" in Path(file).resolve().parts
                    else os.environ.get("STORY_CHANNEL", DEFAULT_CHANNEL)),
        "estimated_inr": f"{cost['estimated_usd'] * USD_TO_INR:.2f}",
        "actual_inr": "" if cost.get("actual_usd") is None else f"{cost['actual_usd'] * USD_TO_INR:.4f}",
        "gst_inr": f"{gst:.2f}",
        "input_tokens": "" if cost.get("input_tokens") is None else cost["input_tokens"],
        "output_tokens": "" if cost.get("output_tokens") is None else cost["output_tokens"],
    }
    rows = _rows()
    today = row["timestamp"][:10]
    row["today_total_inr"] = f"{sum(charge_inr(r) for r in rows if r['timestamp'].startswith(today)) + charge_inr(row):.2f}"
    row["remaining_inr"] = f"{remaining(rows + [row]):.2f}"
    new = not LOG.exists()
    with LOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    if usage is not None:
        with USAGE_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"timestamp": row["timestamp"], "file": row["file"], "model": model, "size": size,
                                "usage": usage}, ensure_ascii=False) + "\n")
    return row


def record(file: Path, model: str, size: str, when: datetime | None = None) -> dict:
    """Old API: image priced from the table only (no usage). Prefer record_call()."""
    r = pricing.rates(model)
    usd = r["image_tokens"][size] / 1e6 * r["output_image_per_1m"]
    return record_call(file, model, size, {"estimated_usd": usd, "actual_usd": None}, when)


def record_usd(file: Path, model: str, size: str, usd: float, when: datetime | None = None) -> dict:
    """Old API: a computed USD cost without usage numbers. Prefer record_call()."""
    return record_call(file, model, size, {"estimated_usd": usd, "actual_usd": None}, when)


def summary(row: dict, what="image") -> str:
    kind = "asli" if row.get("actual_inr") else "andaza"
    return (f"Is {what} ka cost: ₹{float(row['cost_inr']):.2f} ({kind}; andaza tha ₹{row['estimated_inr']}) + GST ₹{row['gst_inr']}"
            f"  |  Aaj ka total (GST samet): ₹{row['today_total_inr']}  |  Bacha: ₹{row['remaining_inr']}")
