"""How much a channel has spent today against its per-day cap, and the account balance against the floor.
    python scripts/daily_spend.py devrobolab        (exit code 1 when no room is left for another paid call)
Spending day = 05:00 to 04:59 local time (shared/pricing.json budget.channel_daily_cap_inr). User 2026-11-07: DevRoboLab Rs 30 per day, floor Rs 50."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cost_log, pricing

key = sys.argv[1] if len(sys.argv) > 1 else "devrobolab"
b = pricing.config()["budget"]; cfg = b.get("channel_daily_cap_inr") or {}
cap, margin = cfg.get(key), cfg.get("margin_inr", 1.0)
spent = cost_log.channel_spent_day(key); left_balance = cost_log.remaining(); floor = b["floor_inr"]
print(f"channel {key} | today (day 05:00-04:59) spent Rs {spent:.2f}" + (f" | daily cap Rs {cap} | room Rs {max(0.0, cap - spent):.2f}" if cap is not None else " | no daily cap")
      + f" | account balance Rs {left_balance:.2f} (floor Rs {floor:.0f})")
ok = (cap is None or spent + margin <= cap) and left_balance - margin >= floor
print("PAID CALLS ALLOWED" if ok else "STOP: no paid calls (daily cap or floor)")
sys.exit(0 if ok else 1)
