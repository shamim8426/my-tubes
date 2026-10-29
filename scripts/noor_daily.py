"""Noor-e-Raah daily series helper (user 2026-10-30: one surah video per day, private upload, the user makes it public).

    python scripts/noor_daily.py status              table of channels/noor-e-raah/series_queue.json
    python scripts/noor_daily.py next                the next item that is not uploaded + what it still needs
    python scripts/noor_daily.py preflight [--story 002_ayatul-kursi]   safe to run today's paid/upload stages?
    python scripts/noor_daily.py mark <key> <status> [--note "..."]     update an item (planned/dossier_ok/script_ok/
                                                    assets_ok/built/thumbnail_ok/uploaded/public/blocked)
Read-only except `mark`. Exit code 1 from preflight = do NOT start today's run (reasons printed). Never prints secrets.
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "channels" / "noor-e-raah"
QUEUE = CH / "series_queue.json"
ORDER = ["planned", "dossier_ok", "script_ok", "assets_ok", "built", "thumbnail_ok", "uploaded", "public"]
NEEDS = {"planned": "Khoji dossier (+ sources.json)", "dossier_ok": "Kalam script + Munshi PASS",
         "script_ok": "images + TTS (paid, story budget)", "assets_ok": "build_long (noor_render) + Sampadak look",
         "built": "thumbnail (noor_thumb_v3) + Munshi final", "thumbnail_ok": "upload (private) + first comment",
         "uploaded": "the user makes it public in Studio", "public": "-"}
STORY_EST_INR = 120  # hard cap per story (shared RULES 15); preflight wants the account to cover it + the floor


def load():
    return json.loads(QUEUE.read_text(encoding="utf-8"))


def save(q):
    QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def rank(status):
    return ORDER.index(status) if status in ORDER else -1


def cmd_status(q):
    print(f"{'#':>2} {'story':24s} {'status':13s} {'ayat':>4s}  hindi")
    for it in q["items"]:
        print(f"{it['order']:>2} {it['story']:24s} {it['status']:13s} {it['ayat']:>4}  {it['hindi']}" +
              (f"  [{it['note']}]" if it.get("note") else ""))


def next_item(q):
    return next((it for it in q["items"] if rank(it["status"]) < rank("uploaded") and it["status"] != "blocked"), None)


def cmd_next(q):
    it = next_item(q)
    if not it:
        print("nothing left: every item is uploaded or blocked")
        return
    print(f"NEXT: {it['order']}. {it['story']} ({it['hindi']}) status={it['status']}\n  needs: {NEEDS.get(it['status'], '?')}\n"
          f"  search title: {it['search_title']}")


def cmd_preflight(q, story):
    it = next((i for i in q["items"] if i["story"] == story), None) if story else next_item(q)
    bad, ok = [], []

    def chk(cond, good, problem):
        (ok if cond else bad).append(good if cond else problem)

    chk(it is not None, f"item {it['story'] if it else '-'}", "no item to run (all uploaded/blocked or unknown story)")
    chk(bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY_FREE")), "Gemini key present",
        "GEMINI_API_KEY / GEMINI_API_KEY_FREE missing (environment variables)")
    sd = ROOT / "secrets" / "noor-e-raah"
    for f in ("client_secret.json", "token.json"):
        chk((sd / f).exists(), f"secrets/noor-e-raah/{f}", f"secrets/noor-e-raah/{f} missing (STORY_SECRETS_B64?)")
    chk(bool(shutil.which("ffmpeg")) or any((ROOT / p).exists() for p in ("tools/ffmpeg/ffmpeg.exe", "tools/ffmpeg/bin/ffmpeg.exe")),
        "ffmpeg", "ffmpeg missing")
    free_gb = shutil.disk_usage(ROOT).free / 1e9
    chk(free_gb >= 6, f"disk {free_gb:.0f} GB free", f"disk only {free_gb:.1f} GB free (need >= 6 GB for a render)")
    for f in ("ArefRuqaa-Bold.ttf", "Amiri-Regular.ttf", "Mukta-ExtraBold.ttf"):
        chk((ROOT / "shared/fonts" / f).exists(), f"font {f}", f"font {f} missing in shared/fonts")
    try:
        import pricing
        import story_budget
        left, floor = story_budget.remaining(), pricing.config()["budget"]["floor_inr"]
        chk(left - STORY_EST_INR >= floor, f"balance Rs{left:.0f} covers Rs{STORY_EST_INR} + floor Rs{floor:.0f}",
            f"balance Rs{left:.0f} < Rs{STORY_EST_INR} + floor Rs{floor:.0f}: the user must top up AI Studio credit, then "
            "`scripts/reconcile_balance.py <balance> --topup`")
    except Exception as e:  # noqa: BLE001
        bad.append(f"budget check failed: {e}")
    if it and rank(it["status"]) < rank("script_ok"):
        bad.append(f"{it['story']} is at '{it['status']}': script not yet Munshi-PASSed (daily run only builds ready items)")
    for line in ok:
        print("  OK   ", line)
    for line in bad:
        print("  STOP ", line)
    print("PREFLIGHT " + ("OK" if not bad else "FAILED"))
    return not bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "next", "preflight", "mark"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--story")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    q = load()
    if a.cmd == "status":
        cmd_status(q)
    elif a.cmd == "next":
        cmd_next(q)
    elif a.cmd == "preflight":
        sys.exit(0 if cmd_preflight(q, a.story) else 1)
    else:
        if len(a.args) != 2:
            ap.error("mark <key> <status>")
        key, status = a.args
        if status not in ORDER + ["blocked"]:
            ap.error(f"status must be one of {ORDER + ['blocked']}")
        it = next((i for i in q["items"] if i["key"] == key), None)
        if not it:
            sys.exit(f"unknown key {key}")
        it["status"], it["note"] = status, a.note
        save(q)
        print(f"{it['story']} -> {status}")


if __name__ == "__main__":
    main()
