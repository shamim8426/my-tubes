"""Long-video thumbnail in Kissago Painted (story 005+), 1280x720.

Usage: python scripts/gen_thumb_painted.py <story>/long [--text-only]
  reads long/meta.json "thumbnail": {"text": "किसका है ये खज़ाना?", "lines": ["किसका है", "ये खज़ाना?"],
                                    "prompt": "...", "refs": ["golu", ...]}
Paid: one Gemini image (16:9, 1K) inside the story budget. The left 42% stays plain for the title; Hindi text is drawn
here with libass (never by the image model); logo bottom-left (bottom-right = YouTube timestamp).
Output: long/output/<name>_thumbnail.png; work files in long/thumbnail_work/.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import painted  # noqa: E402
from gemini_image import generate  # noqa: E402
from gen_brand import brand_corner  # noqa: E402
from gen_channel_assets import cover  # noqa: E402
from paths import FONTS_DIR, ROOT, channel_dir, channel_of  # noqa: E402
from story_budget import check  # noqa: E402

TW, TH = 1280, 720
FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
if not FFMPEG.exists():
    FFMPEG = Path(shutil.which("ffmpeg") or FFMPEG)
LAYOUT = """16:9 YouTube thumbnail illustration for a Hindi family story, NO text or letters anywhere.
COMPOSITION IS CRITICAL: keep the LEFT 42% of the image as a plain, softly blurred background with NO characters or
objects (a big title goes there). Keep the BOTTOM-RIGHT corner (last 20% of width, bottom 18% of height) plain and
unimportant (YouTube puts the video length there). Faces big, bright and expressive, readable when small; strong
warm/cool contrast. Keep every character EXACTLY as in the attached reference sheets."""


def draw(art: Path, out: Path, work: Path, lines, size=128, all_yellow=False):
    fonts = work / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    shutil.copy(FONTS_DIR / "Mukta-Bold.ttf", fonts / "Mukta-Bold.ttf")
    white = "" if all_yellow else "{\\c&H00FFFFFF&}"
    txt = "\\N".join([lines[0]] + [f"{white}{l}" for l in lines[1:]])
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {TW}
PlayResY: {TH}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Q,Mukta,{size},&H0000E5FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,11,7,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,Q,,0,0,0,,{{\\an5\\pos(275,300)\\q2}}{txt}
"""
    (work / "thumb.ass").write_text(ass, encoding="utf-8")
    shutil.copy(art, work / "thumb_in.png")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-i", "thumb_in.png", "-vf",
                    "subtitles=filename=thumb.ass:fontsdir=fonts", "-frames:v", "1", "thumb_titled.png"],
                   cwd=work, check=True)
    shutil.copy(work / "thumb_titled.png", out)
    brand_corner(out, "bl")


def main():
    ldir = (ROOT / sys.argv[1]).resolve()
    story = ldir.parent
    chan = channel_dir(channel_of(ldir))
    if not painted.is_painted(story, chan):
        sys.exit("this story is not in Kissago Painted; use the older thumbnail functions")
    meta = json.loads((ldir / "meta.json").read_text(encoding="utf-8"))
    t = meta["thumbnail"]
    name = json.loads((ldir / "project.json").read_text(encoding="utf-8")).get("name", ldir.name)
    work = ldir / "thumbnail_work"
    work.mkdir(exist_ok=True)
    raw, art = work / "thumb_raw.png", work / "thumb_art.png"
    if "--text-only" not in sys.argv:
        prompt = f"{LAYOUT}\n\n{t['prompt']}\n{painted.notes(t.get('refs', []))}".strip()
        painted.guard(prompt + " " + t["text"])
        check(story.name, 5.0)
        generate(prompt, raw, refs=[painted.sheet(chan, r) for r in t.get("refs", [])], aspect_ratio="16:9",
                 size="1K", style=painted.style_block(chan))
        cover(raw, TW, TH, art)
    out = ldir / "output" / f"{name}_thumbnail.png"
    out.parent.mkdir(exist_ok=True)
    draw(art, out, work, t.get("lines") or [t["text"]], t.get("size", 128), t.get("all_yellow", False))
    print("saved", out, Image.open(out).size)


if __name__ == "__main__":
    main()
