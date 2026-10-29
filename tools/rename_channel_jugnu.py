"""One-time rename (user 2026-10-29): channel Kissago (key dadi-ki-kahaniyan) -> Jugnu Stories (key jugnu-stories).

    python tools/rename_channel_jugnu.py           # dry run: what would change
    python tools/rename_channel_jugnu.py --apply   # do it (git mv + text replace + local secrets/cache rename)

Rules from the user: all English ("Jugnu Stories" name, suffix and label); old published videos' titles stay as they
are (published story files keep their history text); internal names become Jugnu (style "Jugnu Painted", agents
kaarigar-jugnu / nigraan-jugnu); logo/banner untouched.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD, NEW = "dadi-ki-kahaniyan", "jugnu-stories"
APPLY = "--apply" in sys.argv

KEY_SKIP = {"shared/sync.log"}                       # history log: keep as written
# "Kissago" brand words are changed only in living docs/code and the unpublished story 006 — never in the records
# of already published stories, logs, analytics or research (they show what was really published).
BRAND_PREFIXES = ("CLAUDE.md", "shared/RULES.md", ".claude/", "scripts/", "tools/", "channels/_template/",
                  f"channels/{NEW}/RULES.md", f"channels/{NEW}/channel_bible.md", f"channels/{NEW}/channel.json",
                  f"channels/{NEW}/brand/STYLE_PAINTED.md", f"channels/{NEW}/brand/STYLE_LEARNINGS.md",
                  f"channels/{NEW}/channel_brief.md", f"channels/{NEW}/idea_bank.md",
                  f"channels/{NEW}/festival_calendar.md", f"channels/{NEW}/stories/006_", "docs/", "deploy.ps1",
                  "README", "PREVIEW.md", "shared/stage_contracts.md")
BRAND_SKIP = {"tools/rename_channel_jugnu.py", "tools/name_guard.py"}
BRAND = [("किस्सागो | Kissago", "Jugnu Stories"), ("Kissago | किस्सागो", "Jugnu Stories"), ("किस्सागो जासूस", "Jugnu Stories"),
         ("#किस्सागो", "#JugnuStories"), ("| किस्सागो", "| Jugnu Stories"), ("Kissago Painted", "Jugnu Painted"),
         ("kissago_painted", "jugnu_painted"), ("किस्सागो", "Jugnu Stories"), ("Kissago", "Jugnu Stories")]
ALWAYS = [(OLD, NEW), ("kaarigar-kissago", "kaarigar-jugnu"), ("nigraan-kissago", "nigraan-jugnu"),
          ("nigraan kissago", "nigraan jugnu"), ("kissago_painted", "jugnu_painted")]


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True).stdout


def text_files():
    for rel in git("ls-files").splitlines():
        p = ROOT / rel
        if not p.is_file() or p.stat().st_size > 20_000_000:
            continue
        b = p.read_bytes()
        if b"\0" in b[:4096]:
            continue
        try:
            yield rel, b.decode("utf-8")
        except UnicodeDecodeError:
            continue


def main():
    # 1. moves (git mv keeps history)
    moves = [(f"channels/{OLD}", f"channels/{NEW}"),
             (".claude/agents/kaarigar-kissago.md", ".claude/agents/kaarigar-jugnu.md"),
             (".claude/agents/nigraan-kissago.md", ".claude/agents/nigraan-jugnu.md")]
    for a, b in moves:
        if (ROOT / a).exists():
            print("git mv", a, "->", b)
            if APPLY:
                git("mv", a, b)
    # 2. text replacements
    changed = 0
    for rel, t in text_files():
        new_rel = rel.replace(f"channels/{OLD}/", f"channels/{NEW}/")
        rel_now = new_rel if APPLY else rel
        s = t
        if rel_now not in KEY_SKIP:
            for a, b in ALWAYS:
                s = s.replace(a, b)
        if rel_now.replace(f"channels/{OLD}/", f"channels/{NEW}/").startswith(BRAND_PREFIXES) and rel_now not in BRAND_SKIP:
            for a, b in BRAND:
                s = s.replace(a, b)
        if s != t:
            changed += 1
            print("edit", rel_now)
            if APPLY:
                (ROOT / rel_now).write_text(s, encoding="utf-8", newline="")
    # 3. channel.json: names (all English) + keep the old name in former_names
    cfg_path = ROOT / f"channels/{NEW}/channel.json"
    if APPLY and cfg_path.exists():
        c = json.loads(cfg_path.read_text(encoding="utf-8"))
        c.update({"channel_key": NEW, "display_name": "Jugnu Stories", "title_suffix": "| Jugnu Stories",
                  "brand_label": "Jugnu Stories"})
        fn = c.get("former_names", [])
        for n in ("किस्सागो | Kissago", "Kissago (key dadi-ki-kahaniyan)"):
            if n not in fn:
                fn.append(n)
        c["former_names"] = fn
        c["image_style"] = "jugnu_painted"
        cfg_path.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 4. local (untracked) secrets and cache follow the key
    local = [(ROOT / "secrets" / OLD, ROOT / "secrets" / NEW),
             (ROOT / "secrets" / f"youtube_token_{OLD}.json", ROOT / "secrets" / f"youtube_token_{NEW}.json"),
             (ROOT / "cache" / OLD, ROOT / "cache" / NEW)]
    for a, b in local:
        if a.exists() and not b.exists():
            print("rename local", a.relative_to(ROOT).as_posix(), "->", b.relative_to(ROOT).as_posix())
            if APPLY:
                a.rename(b)
    print(("APPLIED" if APPLY else "DRY RUN"), f"- {changed} text files")


if __name__ == "__main__":
    main()
