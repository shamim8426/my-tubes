"""Build PREVIEW.md (image gallery with costs) and open images inside VS Code.

Usage:  python scripts/preview.py            rebuild PREVIEW.md and open its Markdown preview
        python scripts/preview.py <image>    open one image in a VS Code tab
"""
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / "PREVIEW.md"
SECTIONS = [("Characters", "characters"), ("Scenes", "images")]  # folder name inside channels/**/


def _costs():
    log = ROOT / "cost_log.csv"
    if not log.exists():
        return {}, None
    with log.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return {r["file"]: r for r in rows}, (rows[-1] if rows else None)


def build() -> Path:
    costs, last = _costs()
    lines = ["# Preview — Jugnu Stories", ""]
    if last:
        lines += [f"**Budget bacha:** ₹{last['remaining_inr']}  ·  **Last image:** {last['timestamp']}", ""]
    for title, kind in SECTIONS:
        imgs = sorted(p for p in (ROOT / "channels").rglob(f"{kind}/*.png")
                      if not any(part.startswith("_") for part in p.relative_to(ROOT).parts))
        if not imgs:
            continue
        lines += [f"## {title}", ""]
        for img in imgs:
            rel = img.relative_to(ROOT).as_posix()
            c = costs.get(rel)
            meta = f" — ₹{c['cost_inr']} · {c['timestamp']}" if c else ""
            lines += [f"### {img.stem}{meta}", "", f"![{img.stem}]({rel})", ""]
    PREVIEW.write_text("\n".join(lines), encoding="utf-8")
    return PREVIEW


def open_in_vscode(path: Path):
    if os.environ.get("AUTO_PREVIEW", "0") != "1":  # off by default (user, 2026-10-20); AUTO_PREVIEW=1 turns it on
        return
    code = shutil.which("code")
    if code:
        subprocess.run([code, "--reuse-window", str(path)], check=False, shell=os.name == "nt")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        open_in_vscode(Path(sys.argv[1]).resolve())
    else:
        open_in_vscode(build())
