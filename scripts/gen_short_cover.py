"""Poster-style Short cover (channels/<key>/RULES.md "Short cover"), 1080x1920.

Usage: python scripts/gen_short_cover.py <short folder> [--text-only]
  reads meta.json "cover": {"label": "किस्सागो जासूस", "title": "सोना चोरी?", "prompt": "...", "refs": ["pandey", ...]}
  refs: a character name (story characters/ then channel characters/ <name>_sheet.png) or a path from the project root.
  --text-only: redraw the text on the existing art (free).
Paid: one Gemini image (9:16, 1K). Checks the story budget (RULES 14) first. Hindi text is drawn here with libass,
never by the image model. Output: output/<short name>_cover.png; work files in thumbnail_work/.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402
from paths import FONTS_DIR, ROOT, channel_dir, channel_of  # noqa: E402
from story_budget import check  # noqa: E402
import painted  # noqa: E402

W, H = 1080, 1920
FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
if not FFMPEG.exists():
    FFMPEG = Path(shutil.which("ffmpeg") or FFMPEG)
STYLE_REF = "brand/reference/short_cover_style_ref.png"

LAYOUT = """Vertical 9:16 poster-style cover for a Hindi family cartoon Short, NO text or letters anywhere.
Look: dramatic poster, dark navy-blue sky at the top fading into a warm orange glow lower down, high contrast,
flat 2D cartoon with thick bold black outlines, warm colours, flat cel shading (match the attached character sheets).
COMPOSITION IS CRITICAL:
- top 33% of the height: only the dark background (a title is added there later); nothing important, no faces.
- 33%-63%: ONE big hero character as described below, large and expressive.
- 61%-82%: the key object and the other characters described below, faces clearly visible.
- bottom 18%: only bodies/ground, no faces.
The attached last image is a COMPOSITION and MOOD reference only: do not copy its characters or objects.
Keep every character EXACTLY as in the attached reference sheets (faces, outfits, colours)."""

# Kissago Painted (story 005+): same composition, painted look; no flat style reference image
LAYOUT_PAINTED = """Vertical 9:16 poster-style cover for a Hindi family Short, NO text or letters anywhere.
Look: warm painted poster with strong contrast: a deeper sky at the top fading into warm golden light lower down.
COMPOSITION IS CRITICAL:
- top 33% of the height: only sky/background (a title is added there later); nothing important, no faces.
- 33%-63%: ONE big hero character as described below, large and expressive.
- 61%-80%: the key object and the other characters described below, faces clearly visible.
- bottom 20%: only bodies/ground, no faces.
Keep every character EXACTLY as in the attached reference sheets (faces, outfits, colours)."""


def ref_path(name: str, story: Path, chan: Path) -> Path:
    for p in (story / "characters" / f"{name}_sheet.png", chan / "characters" / f"{name}_sheet.png", ROOT / name):
        if p.exists():
            return p
    sys.exit(f"cover ref not found: {name}")


def draw_text(art: Path, out: Path, work: Path, label: str, title: str, label_y=0.178, title_y=0.268):
    fonts = work / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    shutil.copy(FONTS_DIR / "Mukta-ExtraBold.ttf", fonts / "Mukta-ExtraBold.ttf")
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Mukta ExtraBold,95,&H0060C8F0,&H000000FF,&H00101010,&H96000000,-1,0,0,0,100,100,0,0,1,5,3,5,40,40,0,1
Style: T,Mukta ExtraBold,280,&H0000E5FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,14,8,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,L,,0,0,0,,{{\\an5\\pos({W // 2},{int(H * label_y)})}}{label}
Dialogue: 0,0:00:00.00,0:00:01.00,T,,0,0,0,,{{\\an5\\pos({W // 2},{int(H * title_y)})}}{title}
"""
    (work / "cover.ass").write_text(ass, encoding="utf-8")
    shutil.copy(art, work / "cover_in.png")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-i", "cover_in.png", "-vf",
                    "subtitles=filename=cover.ass:fontsdir=fonts", "-frames:v", "1", "cover_titled.png"],
                   cwd=work, check=True)
    shutil.copy(work / "cover_titled.png", out)


def main():
    sdir = (ROOT / sys.argv[1]).resolve()
    text_only = "--text-only" in sys.argv
    meta = json.loads((sdir / "meta.json").read_text(encoding="utf-8"))
    c = meta["cover"]
    name = json.loads((sdir / "project.json").read_text(encoding="utf-8")).get("name", sdir.name)
    story = sdir.parent.parent
    chan = channel_dir(channel_of(sdir))
    work = sdir / "thumbnail_work"
    work.mkdir(exist_ok=True)
    raw, art = work / "cover_raw.png", work / "cover_art.png"
    if not text_only:
        check(story.name, 3.24)  # RULES 14 budget guard (exits on STOP)
        if painted.is_painted(story, chan):
            prompt = f"{LAYOUT_PAINTED}\n\n{c['prompt']}\n{painted.notes(c.get('refs', []))}".strip()
            painted.guard(prompt)
            generate(prompt, raw, refs=[painted.sheet(chan, r) for r in c.get("refs", [])], aspect_ratio="9:16",
                     size="1K", style=painted.style_block(chan))
        else:
            refs = [ref_path(r, story, chan) for r in c.get("refs", [])] + [chan / STYLE_REF]
            generate(f"{LAYOUT}\n\n{c['prompt']}", raw, refs=refs, aspect_ratio="9:16", size="1K")
        im = Image.open(raw).convert("RGB")
        k = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        x, y = (im.width - W) // 2, (im.height - H) // 2
        im.crop((x, y, x + W, y + H)).save(art)
    out = sdir / "output" / f"{name}_cover.png"
    out.parent.mkdir(exist_ok=True)
    draw_text(art, out, work, c["label"], c["title"], c.get("label_y", 0.178), c.get("title_y", 0.268))
    print("saved", out, Image.open(out).size)


if __name__ == "__main__":
    main()
