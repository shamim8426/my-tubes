"""Budget guard for auto mode (shared/RULES.md sections 14/15), on ACTUAL cost.

    from story_budget import check
    check("004_some-story", next_cost_inr=3.24)   # exits (STOP) if the story cap or the account floor would be crossed

    python scripts/story_budget.py <story>          # one line: the story's actual total (+ GST)
    python scripts/story_budget.py <story> --log    # same line appended to the channel log.md (end of a story)

Story cost = cost_log rows whose file is inside the story folder, plus channel-level files made for it
(EXTRA_FILES, e.g. a new recurring character sheet or voice samples). A row counts its actual cost (API usage
numbers) or, when the API reported none, its estimate; GST is added when pricing.json budget_includes_gst.
Cap per story and floor: shared/pricing.json "budget".
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cost_log  # noqa: E402
import pricing  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXTRA_FILES = {
    "003_mitthu-ne-sab-bata-diya": ["channels/dadi-ki-kahaniyan/characters/sharma_sheet.png",
                                    "channels/dadi-ki-kahaniyan/characters/voices/raghu_",
                                    "channels/dadi-ki-kahaniyan/characters/voices/gupta_"],
    "004_chhat-par-bhoot": ["channels/dadi-ki-kahaniyan/characters/voices/mishra_"],
    # style migration "Kissago Painted" (own budget ₹35, not in any story)
    "style_migration": ["channels/dadi-ki-kahaniyan/characters/dadi/sheet_painted", "channels/dadi-ki-kahaniyan/characters/golu/sheet_painted",
                        "channels/dadi-ki-kahaniyan/characters/mitthu/sheet_painted", "style_tests/painted/"],
}


def _story_rows(story: str):
    extra = EXTRA_FILES.get(story, [])
    return [r for r in cost_log._rows()
            if f"/stories/{story}/" in r["file"] or any(r["file"].startswith(e) for e in extra)]


def story_cost(story: str) -> float:
    """What the story has taken from the budget (actual, else estimate; + GST if configured)."""
    return sum(cost_log.charge_inr(r) for r in _story_rows(story))


def cap(story: str):
    caps = pricing.config()["budget"]["story_cap_inr"]
    return caps.get(story, caps["default"])


def remaining() -> float:
    return cost_log.remaining()


def check(story: str, next_cost_inr: float):
    """next_cost_inr: the pre-GST estimate of the next call; GST is added here when the budget includes it."""
    cfg = pricing.config()
    nxt = next_cost_inr * (1 + pricing.gst_rate()) if cfg["budget_includes_gst"] else next_cost_inr
    spent, left, limit = story_cost(story), remaining(), cap(story)
    if limit is not None and spent + nxt > limit:
        sys.exit(f"OVER CAP (RULES 15): story {story} has spent ₹{spent:.2f} (actual); +₹{nxt:.2f} would cross the "
                 f"₹{limit:.0f} cap. Not a user stop (RULES 15): shrink the plan (fewer new images, more crop/zoom reuse), log it, continue.")
    floor = cfg["budget"]["floor_inr"]
    if left - nxt < floor:
        sys.exit(f"STOP (RULES 14/15): balance ₹{left:.2f} would drop below ₹{floor:.0f}. ASK the user to recharge Google credits.")
    return spent, left


def summary_line(story: str) -> str:
    rows = _story_rows(story)
    base = sum(cost_log.base_inr(r) for r in rows)
    gst = base * pricing.gst_rate()
    est = sum(float(r.get("estimated_inr") or r.get("cost_inr") or 0) for r in rows)
    no_usage = sum(1 for r in rows if not r.get("actual_inr"))
    limit = cap(story)
    return (f"{date.today().isoformat()} | {story} | ASLI KUL KHARCHA | ₹{base:.2f} + GST ₹{gst:.2f} = ₹{base + gst:.2f}"
            f" (andaza tha ₹{est:.2f}; {len(rows)} paid calls, {no_usage} bina usage = andaza)"
            + (f" | cap ₹{limit:.0f}" if limit is not None else ""))


if __name__ == "__main__":
    s = sys.argv[1]
    line = summary_line(s)
    print(line)
    print(f"account remaining (ledger, GST samet): ₹{remaining():.2f}")
    if "--log" in sys.argv:
        key = next((r["channel"] for r in _story_rows(s)), None) or "dadi-ki-kahaniyan"
        with (ROOT / "channels" / key / "log.md").open("a", encoding="utf-8") as f:
            f.write(line + "\n")
