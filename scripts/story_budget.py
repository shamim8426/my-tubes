"""Budget guard for auto mode (shared/RULES.md section 14).

    from story_budget import check
    check("003_mitthu-ne-sab-bata-diya", next_cost_inr=3.24)   # exits (STOP) if the cap or the floor would be crossed

Story cost = cost_log rows whose file is inside the story folder, plus channel-level files made for it
(listed in EXTRA_FILES, e.g. a new recurring character sheet or voice samples).
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "cost_log.csv"
CAP_INR = 130.0
FLOOR_INR = 50.0
EXTRA_FILES = {
    "003_mitthu-ne-sab-bata-diya": ["channels/dadi-ki-kahaniyan/characters/sharma_sheet.png",
                                    "channels/dadi-ki-kahaniyan/characters/voices/raghu_",
                                    "channels/dadi-ki-kahaniyan/characters/voices/gupta_"],
}


def _rows():
    with LOG.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def story_cost(story: str) -> float:
    extra = EXTRA_FILES.get(story, [])
    return sum(float(r["cost_inr"]) for r in _rows()
               if f"/stories/{story}/" in r["file"] or any(r["file"].startswith(e) for e in extra))


def remaining() -> float:
    rows = _rows()
    return float(rows[-1]["remaining_inr"]) if rows else 500.0


def check(story: str, next_cost_inr: float):
    spent, left = story_cost(story), remaining()
    if spent + next_cost_inr > CAP_INR:
        sys.exit(f"STOP (RULES 14): story {story} has spent ₹{spent:.2f}; +₹{next_cost_inr:.2f} would cross the ₹{CAP_INR:.0f} cap. ASK the user.")
    if left - next_cost_inr < FLOOR_INR:
        sys.exit(f"STOP (RULES 14): balance ₹{left:.2f} would drop below ₹{FLOOR_INR:.0f}. ASK the user.")
    return spent, left


if __name__ == "__main__":
    s = sys.argv[1]
    print(f"story {s}: spent ₹{story_cost(s):.2f} of ₹{CAP_INR:.0f} | account remaining ₹{remaining():.2f}")
