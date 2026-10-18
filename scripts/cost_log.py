"""Track Gemini image spend against the prepaid budget in cost_log.csv."""
import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "cost_log.csv"

BUDGET_INR = 500.0
USD_TO_INR = 96.5  # mid-market rate checked 2026-10-17; update if it drifts

# USD per output image (ai.google.dev/gemini-api/docs/pricing, checked 2026-10-17)
RATES_USD = {
    ("gemini-nano-banana-2.1", "1K"): 0.0336,
    ("gemini-nano-banana-2.1", "2K"): 0.0504,
    ("gemini-nano-banana-2.1", "4K"): 0.113,
}

FIELDS = ["timestamp", "file", "model", "size", "cost_usd", "cost_inr", "today_total_inr", "remaining_inr"]


def _rows():
    if not LOG.exists():
        return []
    with LOG.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def record(file: Path, model: str, size: str, when: datetime | None = None) -> dict:
    """Image: priced from the per-image rate table."""
    return record_usd(file, model, size, RATES_USD[(model, size)], when)


def record_usd(file: Path, model: str, size: str, usd: float, when: datetime | None = None) -> dict:
    """Anything with a computed USD cost (e.g. TTS priced by tokens)."""
    when = when or datetime.now()
    inr = usd * USD_TO_INR
    rows = _rows()
    today = when.strftime("%Y-%m-%d")
    today_total = inr + sum(float(r["cost_inr"]) for r in rows if r["timestamp"].startswith(today))
    spent = inr + sum(float(r["cost_inr"]) for r in rows)
    row = {
        "timestamp": when.strftime("%Y-%m-%d %H:%M:%S"),
        "file": Path(file).resolve().relative_to(ROOT).as_posix(),
        "model": model,
        "size": size,
        "cost_usd": f"{usd:.5f}",
        "cost_inr": f"{inr:.2f}",
        "today_total_inr": f"{today_total:.2f}",
        "remaining_inr": f"{BUDGET_INR - spent:.2f}",
    }
    new = not LOG.exists()
    with LOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    return row


def summary(row: dict, what="image") -> str:
    return (f"Is {what} ka cost: ₹{row['cost_inr']}  |  Aaj ka total: ₹{row['today_total_inr']}  |  "
            f"₹{BUDGET_INR:.0f} me se bacha: ₹{row['remaining_inr']}")
