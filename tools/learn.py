"""Write a learning into the COMMON style library and push it to GitHub in ONE step (user 2026-11-07: "learning turant sync, mujhe bar bar kehna na pade").
Use it the moment you learn something that other videos/channels/sessions can use: a mistake found, a fix, a tool/OS trap, a style rule, a study result.
    python tools/learn.py "<short title>" "<what was learned, what to do next time>" [--dry-run]
It appends one dated line under "## 13. Learning inbox" in shared/STYLE_LIBRARY.md (newest last), commits ONLY that file, and pushes to main.
Works from the main checkout, a worktree, or a cloud session. Never needed: asking the user to sync. If the push fails it says so (exit 1) and the line stays committed locally.
Do not put secrets, tokens, keys or other creators' words/frames into a learning (principles only, RULES 12c)."""
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "shared" / "STYLE_LIBRARY.md"
REL = "shared/STYLE_LIBRARY.md"
HEAD = "## 13. Learning inbox (added automatically the moment something is learned; newest last; move good ones into the sections above when tidying)"
SECRET = re.compile(r"(AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9]{20,}|ya29\.[0-9A-Za-z_-]+|-----BEGIN [A-Z ]*PRIVATE KEY|(?:api[_-]?key|token|secret|password)\s*[:=]\s*\S{8,})", re.I)


def git(*a, check=True):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(a)}: {(r.stderr or r.stdout).strip()[:300]}")
    return r


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) < 2:
        sys.exit(__doc__)
    title, text = " ".join(args[0].split()), " ".join(args[1].split())
    if SECRET.search(title + " " + text):
        sys.exit("REFUSED: the text looks like it contains a secret (key/token/password). Remove it and try again.")
    if git("diff", "--quiet", "--", REL, check=False).returncode != 0 or git("diff", "--cached", "--quiet", "--", REL, check=False).returncode != 0:
        sys.exit(f"STOP: {REL} has uncommitted edits in this checkout; commit or finish them first (so nothing of yours is lost).")
    who = os.environ.get("STORY_CHANNEL") or ""
    line = f"- {datetime.now().strftime('%Y-%m-%d %H:%M')} **{title}**{' [' + who + ']' if who else ''}: {text}"
    for attempt in range(1, 4):
        git("fetch", "-q", "origin", "main")
        behind = git("rev-list", "--count", "HEAD..origin/main").stdout.strip()
        if behind != "0":
            if git("merge", "--ff-only", "-q", "origin/main", check=False).returncode != 0:
                r = git("merge", "--no-edit", "-q", "origin/main", check=False)
                if r.returncode != 0:
                    git("merge", "--abort", check=False)
                    sys.exit("STOP: this branch and main have diverged and could not merge cleanly; merge origin/main by hand, then run again.")
        s = FILE.read_text(encoding="utf-8")
        if HEAD.split(" (")[0] not in s:
            s = s.rstrip("\n") + f"\n\n{HEAD}\n"
        if line in s:
            print("already in the library"); return
        s = s.rstrip("\n") + "\n" + line + "\n"
        if dry:
            print("DRY RUN, would add:\n" + line); return
        FILE.write_text(s, encoding="utf-8")
        git("add", "--", REL)
        git("commit", "-q", "-m", f"style library: learned: {title[:70]}", "--", REL)
        r = git("push", "-q", "origin", "HEAD:main", check=False)
        if r.returncode == 0:
            print(f"learned and synced to GitHub (main): {title}"); return
        # lost a race with another session: undo our commit, take the newest main, add the line again
        git("reset", "-q", "--soft", "HEAD~1"); git("restore", "-q", "--staged", "--worktree", "--", REL)
        print(f"push rejected (attempt {attempt}), retrying", flush=True)
    sys.exit("FAILED to push after 3 tries. The learning was NOT saved; run it again or tell the user.")


main()
