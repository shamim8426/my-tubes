"""YouTube channel art: banner (2560x1440) + profile picture (800x800).

Usage: python scripts/gen_channel_assets.py banner|dp|text
  banner -> generate the art (no text), then add the title
  dp     -> generate the profile picture
  text   -> only re-draw the banner title on the existing art (free)
Images come from Gemini with the approved character sheets as references; the Hindi title is drawn with
Mukta Bold through libass (correct Devanagari shaping), never by the image model.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "channel_assets"
WORK = OUT / "_work"
CHAR = ROOT / "characters"
FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
if not FFMPEG.exists():  # new system: ffmpeg from winget on PATH (tools/ffmpeg is not in git)
    FFMPEG = Path(shutil.which("ffmpeg") or FFMPEG)
TITLE = "दादी की कहानियाँ"

BW, BH = 2560, 1440
SAFE_W, SAFE_H = 1546, 423  # YouTube: area visible on every device
SAFE_TOP = (BH - SAFE_H) // 2  # 508

LOOKS = ("Keep Dadi, Golu and Mitthu EXACTLY as in the attached reference sheets (faces, outfits, colours) "
         "and match their flat 2D cartoon style: thick bold outlines, warm colours, flat cel shading.")

BANNER_PROMPT = f"""Wide 16:9 YouTube channel banner illustration, NO text or letters anywhere.
Scene: warm, cozy Indian village at golden sunset - green fields in the distance, a mud house with a tiled roof,
the swept courtyard (aangan) in front, warm golden light, a few birds in the sky. Family-friendly, welcoming, not scary.
Exactly in the horizontal CENTER of the image: Dadi sits on a low wooden charpai, thoughtful, with a peaceful smile,
as if telling a story. Golu sits on the ground right beside her, looking up at her, listening happily.
Mitthu the green parrot sits on a low tree branch just to the side of them.
COMPOSITION IS CRITICAL: the characters must be fairly small and fit inside the middle horizontal band of the image
(between 36% and 58% of the image height, and within the central 55% of the width). Directly below them, from 58% to
66% of the height across the centre, keep a plain, smooth, slightly darker courtyard floor with no objects, for a title.
Fill the left and right sides with scenery only (fields, house, trees), no important details near the top and bottom edges.
{LOOKS}"""

DP_PROMPT = f"""Square profile picture, NO text. Close-up portrait of Dadi (head and shoulders), centred, with a gentle
warm smile, looking slightly towards the viewer. Golden round glasses, white hair bun clearly visible, light green saree
with yellow border visible on the shoulders, small red bindi. Soft warm lighting. Plain softly blurred cream / light warm
background. Her face fills about 60% of the frame and sits in the centre, with margin all around so it survives a circle
crop. Simple, bold, very clear at small sizes.
{LOOKS}"""


def cover(src: Path, w: int, h: int, dst: Path):
    """Resize to cover w x h and centre-crop."""
    im = Image.open(src).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    im.crop((x, y, x + w, y + h)).save(dst)


TITLE_POS = (805, 720)  # centre of the empty house wall, left part of the safe area (x 507-1100)


def draw_title(art: Path, out: Path):
    """Title in two lines inside the YouTube safe area (left of the characters), warm gold with dark outline.
    Letter spacing must stay 0: any spacing makes libass drop Devanagari shaping (broken matras)."""
    fonts = WORK / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets" / "fonts" / "Mukta-Bold.ttf", fonts / "Mukta-Bold.ttf")
    first, second = TITLE.rsplit(" ", 1)
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {BW}
PlayResY: {BH}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,Mukta,150,&H0030C8FF,&H000000FF,&H00102040,&H96000000,-1,0,0,0,100,100,0,0,1,10,6,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,T,,0,0,0,,{{\\an5\\pos({TITLE_POS[0]},{TITLE_POS[1]})\\q2}}{first}\\N{second}
"""
    (WORK / "title.ass").write_text(ass, encoding="utf-8")
    shutil.copy(art, WORK / "art.png")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-i", "art.png", "-vf",
                    "subtitles=filename=title.ass:fontsdir=fonts", "-frames:v", "1", "titled.png"],
                   cwd=WORK, check=True)
    shutil.copy(WORK / "titled.png", out)


def banner():
    raw = WORK / "banner_raw.png"
    generate(BANNER_PROMPT, raw, refs=[CHAR / "dadi_sheet.png", CHAR / "golu_sheet.png", CHAR / "mitthu_sheet.png"],
             aspect_ratio="16:9", size="2K")
    cover(raw, BW, BH, WORK / "banner_art.png")
    text()


def text():
    out = OUT / "dadi_ki_kahaniyan_banner.png"
    draw_title(WORK / "banner_art.png", out)
    print("saved", out, Image.open(out).size)


def dp():
    raw = WORK / "dp_raw.png"
    generate(DP_PROMPT, raw, refs=[CHAR / "dadi_sheet.png"], aspect_ratio="1:1", size="1K")
    out = OUT / "dadi_ki_kahaniyan_dp.png"
    cover(raw, 800, 800, out)
    print("saved", out, Image.open(out).size)


THUMB_PROMPT = f"""16:9 YouTube thumbnail illustration for a kids' mystery cartoon, NO text or letters anywhere.
Background: dramatic dark blue-to-purple gradient night sky with a soft spotlight glow behind the centre; mystery
detective vibe, still family-friendly and not scary.
CENTRE: big close-up of Dadi (head, shoulders and one hand) holding a large magnifying glass up near her face like a
detective, one eye enlarged through the lens, clever knowing smile.
Around her, smaller head-and-hands portraits of the three suspects (each about 1/4 of Dadi's size), with their HANDS
held up and clearly visible:
- left of Dadi: Pappu the milkman (white kurta, red gamchha) - CLEAN hands, confused face
- right of Dadi, upper: Raju the tea seller (brown shirt, apron, small moustache) - fingers BLACK with soot, guilty look
- right of Dadi, lower: Bunty (17, spiky hair, sky-blue shirt) - fingertips with bright RED paint, caught-red-handed look
COMPOSITION: keep the TOP 24% of the image as empty dark sky (for a title) and the bottom-left corner empty and dark
(for a small logo). Everything important between 26% and 92% of the height. Bold, high contrast, readable when small.
Keep every character EXACTLY as in the attached references (faces, outfits, colours) and match the flat 2D cartoon
style: thick bold outlines, warm colours on the characters, flat cel shading."""

TW, TH = 1280, 720


def draw_thumb_text(art: Path, out: Path):
    fonts = WORK / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets" / "fonts" / "Mukta-Bold.ttf", fonts / "Mukta-Bold.ttf")
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {TW}
PlayResY: {TH}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Q,Mukta,120,&H0000E5FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,9,5,8,20,20,8,1
Style: L,Mukta,40,&H00FFFFFF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,4,2,1,26,20,18,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,Q,,0,0,0,,बताओ, दोषी कौन?
Dialogue: 0,0:00:00.00,0:00:01.00,L,,0,0,0,,{{\\c&H0030C8FF&}}दादी की कहानियाँ
"""
    (WORK / "thumb.ass").write_text(ass, encoding="utf-8")
    shutil.copy(art, WORK / "thumb_art.png")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-i", "thumb_art.png", "-vf",
                    "subtitles=filename=thumb.ass:fontsdir=fonts", "-frames:v", "1", "thumb_titled.png"],
                   cwd=WORK, check=True)
    shutil.copy(WORK / "thumb_titled.png", out)


def thumb():
    raw = WORK / "thumb_raw.png"
    refs = [CHAR / "dadi_sheet.png"] + [ROOT / "images" / "case01_cycle_chori" / f"scene_0{n}.png" for n in (3, 4, 5)]
    generate(THUMB_PROMPT, raw, refs=refs, aspect_ratio="16:9", size="1K")
    cover(raw, TW, TH, WORK / "thumb_art_sized.png")
    thumb_text()


def thumb_text():
    out = OUT / "case01_thumbnail.png"
    draw_thumb_text(WORK / "thumb_art_sized.png", out)
    print("saved", out, Image.open(out).size)


THUMB_V_PROMPT = f"""Vertical 9:16 cover image for a kids' mystery cartoon Short, NO text or letters anywhere.
Background: dramatic dark blue-to-purple gradient night sky with a soft spotlight glow behind Dadi; mystery detective
vibe, still family-friendly and not scary.
Upper-middle (from 17% to 57% of the height): big close-up of Dadi (head, shoulders and one hand) holding a large
magnifying glass near her face like a detective, one eye enlarged through the lens, clever knowing smile.
Below her (from 57% to 79% of the height), a row of the three suspects side by side, head and hands only, each holding
BOTH hands up toward the viewer so the hands are clearly visible:
- left: Pappu the milkman (white kurta, red gamchha) - CLEAN hands, confused face
- middle: Raju the tea seller (brown shirt, apron, small moustache) - fingers BLACK with soot, nervous face
- right: Bunty (17, spiky hair, sky-blue shirt) - small bright RED paint marks on his fingertips, calm innocent
  everyday face (NOT scared, NOT guilty - he must look just as innocent as the others)
All three suspects must look equally suspicious/innocent so the picture does not give away the answer.
COMPOSITION: TOP 16% = empty dark sky (title goes there). BOTTOM 20% = plain dark ground/gradient, nothing important
(the app overlays text there). Bold, high contrast, readable when small.
Keep every character EXACTLY as in the attached references (faces, outfits, colours) and match the flat 2D cartoon
style: thick bold outlines, warm colours on the characters, flat cel shading."""

VW, VH = 1080, 1920


def thumb_v():
    raw = WORK / "thumb_v_raw.png"
    refs = [CHAR / "dadi_sheet.png"] + [ROOT / "images" / "case01_cycle_chori" / f"scene_0{n}.png" for n in (3, 4, 5)]
    generate(THUMB_V_PROMPT, raw, refs=refs, aspect_ratio="9:16", size="1K")
    cover(raw, VW, VH, WORK / "thumb_v_art.png")
    thumb_v_text()


def thumb_v_text():
    """Title + small logo in the top 16%; bottom 20% left clear for the Shorts overlay."""
    fonts = WORK / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets" / "fonts" / "Mukta-Bold.ttf", fonts / "Mukta-Bold.ttf")
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VW}
PlayResY: {VH}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Q,Mukta,150,&H0000E5FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,11,6,8,30,30,70,1
Style: L,Mukta,52,&H0030C8FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,5,3,8,30,30,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,L,,0,0,0,,दादी की कहानियाँ
Dialogue: 0,0:00:00.00,0:00:01.00,Q,,0,0,0,,बताओ, दोषी कौन?
"""
    (WORK / "thumb_v.ass").write_text(ass, encoding="utf-8")
    shutil.copy(WORK / "thumb_v_art.png", WORK / "thumb_v_in.png")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-i", "thumb_v_in.png", "-vf",
                    "subtitles=filename=thumb_v.ass:fontsdir=fonts", "-frames:v", "1", "thumb_v_titled.png"],
                   cwd=WORK, check=True)
    out = OUT / "case01_thumbnail_vertical.png"
    shutil.copy(WORK / "thumb_v_titled.png", out)
    print("saved", out, Image.open(out).size)


LONG01 = ROOT / "long-videos" / "long_01"

L01_THUMB_PROMPT = """16:9 YouTube thumbnail illustration for a kids' Hindi moral-story cartoon, NO text or letters
anywhere. Setting: a small Indian village sweet shop at evening, warm and family-friendly, not scary.
RIGHT HALF of the image: the big magic iron kadhai (exactly as in the prop reference) sits on a clay chulha, glowing
with bright golden magical light and sparkles, and it is OVERFLOWING - orange jalebis and yellow laddoos bubbling up
and spilling over its rim. Right behind it, a big close-up of Ghasita the sweet-shop owner (exactly as in his reference
sheet: face, moustache, outfit) leaning over the kadhai with both hands raised, eyes wide and shining with GREED,
huge greedy grin, the golden glow lighting his face. Behind him, smaller, Chhotu (exactly as in his reference sheet)
peeks in, amazed, mouth open.
Mood: magic + greed at the START of the story - the kadhai is still magical and working (no mud, nothing broken).
COMPOSITION IS CRITICAL: keep the LEFT 42% of the image as a plain, darker, softly blurred warm brown/purple background
with NO characters or objects (a big title goes there). Keep the BOTTOM-RIGHT corner (last 20% of width, bottom 18% of
height) plain and unimportant (YouTube puts the video length there). Faces big, bold, high contrast, readable when small.
Match the flat 2D cartoon style of the references: thick bold outlines, warm colours, flat cel shading."""


def long01_thumb():
    raw = WORK / "long01_thumb_raw.png"
    c = LONG01 / "characters"
    generate(L01_THUMB_PROMPT, raw, refs=[c / "ghasita_sheet.png", c / "chhotu_sheet.png", c / "cadhai_prop.png"],
             aspect_ratio="16:9", size="1K")
    cover(raw, TW, TH, WORK / "long01_thumb_art.png")
    long01_thumb_text()


def long01_thumb_text():
    """Hook in two big lines in the empty left part; channel name small at bottom-left (bottom-right = timestamp)."""
    fonts = WORK / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets" / "fonts" / "Mukta-Bold.ttf", fonts / "Mukta-Bold.ttf")
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {TW}
PlayResY: {TH}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Q,Mukta,130,&H0000E5FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,10,6,5,0,0,0,1
Style: L,Mukta,40,&H0030C8FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,4,2,1,26,20,18,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,Q,,0,0,0,,{{\\an5\\pos(275,320)\\q2}}जो डालो,\\N{{\\c&H0030FFFF&}}दुगना!
Dialogue: 0,0:00:00.00,0:00:01.00,L,,0,0,0,,दादी की कहानियाँ
"""
    (WORK / "long01_thumb.ass").write_text(ass, encoding="utf-8")
    shutil.copy(WORK / "long01_thumb_art.png", WORK / "long01_thumb_in.png")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-i", "long01_thumb_in.png", "-vf",
                    "subtitles=filename=long01_thumb.ass:fontsdir=fonts", "-frames:v", "1", "long01_thumb_titled.png"],
                   cwd=WORK, check=True)
    out = LONG01 / "output" / "long_01_thumbnail.png"
    shutil.copy(WORK / "long01_thumb_titled.png", out)
    print("saved", out, Image.open(out).size)


if __name__ == "__main__":
    WORK.mkdir(parents=True, exist_ok=True)
    {"banner": banner, "dp": dp, "text": text, "thumb": thumb, "thumb_text": thumb_text,
     "thumb_v": thumb_v, "thumb_v_text": thumb_v_text,
     "long01_thumb": long01_thumb, "long01_thumb_text": long01_thumb_text}[sys.argv[1]]()
