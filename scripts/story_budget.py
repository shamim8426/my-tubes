"""Budget guard for auto mode (shared/RULES.md sections 14/15), on ACTUAL cost.

    from story_budget import check
    check("004_some-story", next_cost_inr=3.24)   # exits (STOP) if the story cap or the account floor would be crossed

    python scripts/story_budget.py <story>          # one line: the story's actual total (+ GST)
    python scripts/story_budget.py <story> --log    # same line appended to the channel log.md (end of a story)
    python scripts/story_budget.py --channel <key>  # one channel's own total (cost_log "channel" column) + its cap

Story cost = cost_log rows whose file is inside the story folder, plus channel-level files made for it
(EXTRA_FILES, e.g. a new recurring character sheet or voice samples). A row counts its actual cost (API usage
numbers) or, when the API reported none, its estimate; GST is added when pricing.json budget_includes_gst.
Cap per story and floor: shared/pricing.json "budget". All channels share one Gemini key and balance; each
channel's spend is counted on its own (budget.channel_cap_inr, null = no cap, only shown).
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cost_log  # noqa: E402
import pricing  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXTRA_FILES = {
    "003_mitthu-ne-sab-bata-diya": ["channels/jugnu-stories/characters/sharma_sheet.png",
                                    "channels/jugnu-stories/characters/voices/raghu_",
                                    "channels/jugnu-stories/characters/voices/gupta_"],
    "004_chhat-par-bhoot": ["channels/jugnu-stories/characters/voices/mishra_"],
    # style migration "Jugnu Painted" (own budget ₹35, not in any story)
    "style_migration": ["channels/jugnu-stories/characters/dadi/sheet_painted", "channels/jugnu-stories/characters/golu/sheet_painted",
                        "channels/jugnu-stories/characters/mitthu/sheet_painted", "style_tests/painted/"],
    "005_gulmohar-ka-khazana": ["channels/jugnu-stories/characters/pandey/"],
    "007_bachchon-ki-adalat": ["channels/jugnu-stories/characters/sharma/"],
    # new permanent characters Tara + Tinku (own budget ₹20)
    "new_characters": ["channels/jugnu-stories/characters/tara/", "channels/jugnu-stories/characters/tinku/",
                       "channels/jugnu-stories/characters/_review/"],
    # character look refresh (Tinku's mummy + new finish tests; own budget ₹20, user 2026-10-22)
    "character_refresh": ["channels/jugnu-stories/characters/tinku_mummy/",
                          "channels/jugnu-stories/characters/_v2_look/"],
    # Noor-e-Raah samples: dialogue, look test, 30 s sync sample (own budget ₹45 incl. GST, user 2026-10-24)
    "noor_samples": ["channels/noor-e-raah/music_samples/", "channels/noor-e-raah/samples/look_test/",
                     "channels/noor-e-raah/samples/sync_sample/"],
    # style b test (user 2026-10-25, own budget ₹12)
    "noor_style_b": ["channels/noor-e-raah/samples/sync_sample_b/"],
    # "immersive" cinematic watercolor test (user 2026-10-25, own budget ₹25)
    "noor_immersive_test": ["channels/noor-e-raah/samples/immersive_test/"],
    # "Musafir" character sheet + 3 scenes x 2 cinematic styles (user 2026-10-25, own budget ₹40)
    "noor_musafir_test": ["channels/noor-e-raah/samples/musafir_test/"],
    # "Musafir" v2: young, beardless, kurta-pajama; style V2 only (user 2026-10-25, own budget ₹20)
    "noor_musafir_v2": ["channels/noor-e-raah/samples/musafir_v2/"],
    # "Musafir" v3: beige kurta-pajama, only from behind (user 2026-10-25, own budget ₹12)
    "noor_musafir_v3": ["channels/noor-e-raah/samples/musafir_v3/"],
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


def story_channel(story: str) -> str:
    """Channel key of a story folder (channels/<key>/stories/<story>), else the default channel."""
    hit = next(iter(sorted((ROOT / "channels").glob(f"*/stories/{story}"))), None)
    return hit.parent.parent.name if hit else cost_log.DEFAULT_CHANNEL


def channel_cap(key: str):
    return pricing.config()["budget"].get("channel_cap_inr", {}).get(key)


def channel_line(key: str) -> str:
    spent, limit = cost_log.channel_spent(key), channel_cap(key)
    return (f"{date.today().isoformat()} | channel {key} | KUL KHARCHA (GST samet) ₹{spent:.2f}"
            + (f" | cap ₹{limit:.0f}, bacha ₹{limit - spent:.2f}" if limit is not None else " | cap: none"))


def remaining() -> float:
    return cost_log.remaining()


def check(story: str, next_cost_inr: float):
    """next_cost_inr: the pre-GST estimate of the next call; GST is added here when the budget includes it."""
    cfg = pricing.config()
    nxt = next_cost_inr * (1 + pricing.gst_rate()) if cfg["budget_includes_gst"] else next_cost_inr
    spent, left, limit = story_cost(story), remaining(), cap(story)
    if limit is not None and spent + nxt > limit:
        sys.exit(f"OVER CAP (RULES 15): story {story} has spent ₹{spent:.2f} (actual); +₹{nxt:.2f} would cross the "
                 f"₹{limit:.0f} HARD limit (RULES 15, user 2026-10-26). Not a user stop: shrink the plan (fewer new images, more crop/zoom reuse), log it, continue.")
    key = story_channel(story)
    ch_limit = channel_cap(key)
    if ch_limit is not None and cost_log.channel_spent(key) + nxt > ch_limit:
        sys.exit(f"OVER CHANNEL CAP: channel {key} has spent ₹{cost_log.channel_spent(key):.2f}; +₹{nxt:.2f} would "
                 f"cross its ₹{ch_limit:.0f} cap (shared/pricing.json budget.channel_cap_inr). ASK the user.")
    dcfg = (cfg["budget"].get("channel_daily_cap_inr") or {})
    dcap = dcfg.get(key)
    if dcap is not None and cost_log.channel_spent_day(key) + nxt + dcfg.get("margin_inr", 1.0) > dcap:
        sys.exit(f"OVER DAILY CAP: channel {key} has spent Rs {cost_log.channel_spent_day(key):.2f} today; +Rs {nxt:.2f} would cross its Rs {dcap} per-day cap (shared/pricing.json budget.channel_daily_cap_inr). Stop paid work for today.")
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
            + (f" | target ₹{pricing.config()['budget'].get('story_target_inr', limit):.0f}, hard limit ₹{limit:.0f}"
               if limit is not None else ""))


if __name__ == "__main__":
    if sys.argv[1] == "--channel":
        print(channel_line(sys.argv[2]))
        print(f"account remaining (ledger, GST samet): ₹{remaining():.2f}")
        sys.exit(0)
    s = sys.argv[1]
    line = summary_line(s)
    print(line)
    print(f"account remaining (ledger, GST samet): ₹{remaining():.2f}")
    if "--log" in sys.argv:
        key = story_channel(s)
        with (ROOT / "channels" / key / "log.md").open("a", encoding="utf-8") as f:
            f.write(line + "\n")
