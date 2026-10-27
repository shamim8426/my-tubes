"""Kissago Painted helpers shared by gen_short_cover.py and gen_thumb_painted.py (gen_scenes.py has its own copy
of the rules). A story uses the painted style when channel.json "image_style" is "kissago_painted" and its number is
>= gen_scenes.PAINTED_FROM (5)."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gen_scenes import CHAR_NOTES, MITTHU_NOTE, PAINTED_FROM  # noqa: E402
from paths import ROOT  # noqa: E402

sys.path.insert(0, str(ROOT / "tools"))
from name_guard import find_names  # noqa: E402


def is_painted(story_dir: Path, chan: Path) -> bool:
    cfg = json.loads((chan / "channel.json").read_text(encoding="utf-8"))
    num = int("".join(c for c in story_dir.name.split("_")[0] if c.isdigit()) or 0)
    return cfg.get("image_style") == "kissago_painted" and num >= PAINTED_FROM


def style_block(chan: Path) -> str:
    guide = (chan / "brand" / "STYLE_PAINTED.md").read_text(encoding="utf-8")
    return re.search(r"## 1\..*?```\n(.*?)\n```", guide, re.S).group(1).strip()


def sheet(chan: Path, name: str) -> Path:
    p = chan / "characters" / name / "sheet_painted.png"
    if not p.exists():
        sys.exit(f"painted sheet missing: {p} (make it first, ~₹6 from the story budget)")
    return p


def notes(refs) -> str:
    out = [MITTHU_NOTE] if "mitthu" in refs else []
    out += [CHAR_NOTES[r] for r in refs if r in CHAR_NOTES]
    return "\n".join(out)


def guard(prompt: str):
    """Prompts are no longer name-blocked (RULES 12a 2026-10-27: only public metadata is); kept as a no-op hook."""
    return None
