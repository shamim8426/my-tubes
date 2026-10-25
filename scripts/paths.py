"""Project layout (multi-channel). Every script takes its paths from here.

channels/<channel_key>/
    channel.json, RULES.md, channel_bible.md, log.md, carry_over.md, brand/, characters/
    stories/<NNN>_<slug>/
        story.md, scene_prompts.json, script/, characters/, images/, audio/
        long/                     project.json, lines.json, shots.json, meta.json, review/, output/
        shorts/short_<NN>_<slug>/ project.json, lines.json, shots.json, meta.json, review/, output/
shared/  music/, sfx/, fonts/, assets_license.csv, RULES.md, sync.log
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared"
MUSIC_DIR = SHARED / "music"
SFX_DIR = SHARED / "sfx"
FONTS_DIR = SHARED / "fonts"
REGISTER = SHARED / "assets_license.csv"
CHANNELS = ROOT / "channels"
DEFAULT_CHANNEL = "dadi-ki-kahaniyan"


def channel_dir(key: str = DEFAULT_CHANNEL) -> Path:
    return CHANNELS / key


def channel_config(key: str = DEFAULT_CHANNEL) -> dict:
    return json.loads((channel_dir(key) / "channel.json").read_text(encoding="utf-8"))


def channel_of(path) -> str:
    """channel_key of any path inside channels/<key>/ (DEFAULT_CHANNEL if it is not inside one)."""
    p = Path(path).resolve()
    try:
        return p.relative_to(CHANNELS).parts[0]
    except (ValueError, IndexError):
        return DEFAULT_CHANNEL


def learnings_brief(key: str) -> str:
    """The "LAGU KARO" part of channels/<key>/learnings.md (Nigraan): builders print it before every build."""
    f = channel_dir(key) / "learnings.md"
    if not f.exists():
        return ""
    s = f.read_text(encoding="utf-8")
    part = s.split("## LAGU KARO", 1)[1].split("\n## ", 1)[0] if "## LAGU KARO" in s else ""
    lines = [l for l in part.splitlines()[1:] if l.strip()]
    return "\n".join(lines)


def story_of(variant: Path) -> Path:
    """Story folder of a long/ or shorts/short_XX/ folder."""
    variant = Path(variant).resolve()
    return variant.parent if variant.name == "long" else variant.parent.parent
