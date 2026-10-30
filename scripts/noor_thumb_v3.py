"""Noor-e-Raah thumbnail v3 (user 2026-10-30): surah name in Arabic calligraphy (Aref Ruqaa, gold, glow) + Hindi name +
one honest hook line + a small chip, over a dark Islamic landscape wallpaper. Three layouts to choose from:
  A  text column on the left, wallpaper on the right
  B  everything centred
  C  the hook line is the hero (curiosity first), Arabic name above it, Hindi name as a ribbon
Hindi/hook/chip are drawn by libass (sizes measured through libass itself, no per-font constants). The ARABIC name is
drawn with Pillow + libraqm (HarfBuzz: correct joining and harakat, same shaping engine as libass) in Aref Ruqaa because
this ffmpeg's libass cannot shape Aref Ruqaa / Reem Kufi / Scheherazade (tofu boxes, tested 2026-10-30). Never ffmpeg
drawtext, never AI-drawn letters (RULES 1c). `--arabic amiri` = the old libass + Amiri path. Video text stays libass + Amiri.
Wallpaper: an existing image is free; --generate is FREE FIRST (Cloudflare flux, Rs0, scripts/cf_image.py) and only falls back to
one paid Gemini image (~Rs4-5, story budget check) in --engine auto. No people (RULES 2/2a); no studio/film/artist name (name_guard).

Spec: <story>/thumbnail.json
  {"arabic": "آيَةُ ٱلْكُرْسِيِّ", "hindi": "आयतुल कुर्सी", "chip": "1 आयत • आसान मतलब",
   "hook": "क्या आप इसका *असली मतलब* जानते हैं?", "image": "images/thumb_scene.png", "scene": "<prompt, for --generate>"}
  "*word*" in the hook is drawn in yellow. Keep the hook short (<= ~30 characters per line), true and respectful:
  curiosity, never fear, never a false promise (Munshi checks).

Usage: .venv/Scripts/python -X utf8 scripts/noor_thumb_v3.py channels/noor-e-raah/stories/<story> [--spec file]
         [--image wallpaper.png] [--generate [--engine auto|free|paid]] [--hindi-font "Yatra One"] [--layouts ABC] [--out-dir dir]
Output: <story>/long/output/<story>_thumbnail_v3A/B/C.jpg (1280x720, < 2 MB). YouTube's time stamp covers the bottom-right
corner: no text is placed there.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
import text_pil as TP  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FF = next((str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists()),
          None) or shutil.which("ffmpeg")
FONTS = ROOT / "shared/fonts"
W, H = 1280, 720
GOLD_DEEP, GOLD_PALE, YELLOW = "&H003CAAF0", "&H00AAF0FF", "&H003CE1FF"  # ASS colours are BGR
AR_FONT = "Amiri"  # libass path only (--arabic amiri)


def esc(p: Path) -> str:
    return Path(p).resolve().as_posix().replace(":", "\\:")


def head(styles: str) -> str:
    return (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
            "MarginR, MarginV, Encoding\n" + styles + "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, "
            "MarginV, Effect, Text\n")


def style(name, font, size, colour="&H00FFFFFF", outline="&H00101010", back="&H90000000", bold=-1, bs=1, ol=0, sh=0, an=5):
    return (f"Style: {name},{font},{size},{colour},&H00FFFFFF,{outline},{back},{bold},0,0,0,100,100,0,0,{bs},{ol},{sh},"
            f"{an},0,0,0,1\n")


_probe_cache = {}


def probe(text, font, size, pos, an=5, bold=-1):
    """Bounding box (x0, y0, x1, y1) of the text as libass really draws it (outline 0), or None."""
    key = (text, font, size, pos, an, bold)
    if key in _probe_cache:
        return _probe_cache[key]
    with tempfile.TemporaryDirectory() as td:
        a, png = Path(td) / "p.ass", Path(td) / "p.png"
        a.write_text(head(style("P", font, size, bold=bold, an=an)) +
                     f"Dialogue: 0,0:00:00.00,0:00:05.00,P,,0,0,0,,{{\\pos({pos[0]},{pos[1]})}}{text}\n", encoding="utf-8")
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}",
                        "-vf", f"subtitles=filename='{esc(a)}':fontsdir='{esc(FONTS)}'", "-frames:v", "1", str(png)],
                       check=True)
        im = cv2.imread(str(png))
    ys, xs = np.where(im.max(axis=2) > 60)
    box = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None
    _probe_cache[key] = box
    return box


def fit(text, font, target_w, max_h, pos, an=5, bold=-1):
    """Largest ASS font size whose drawn text is <= target_w wide and <= max_h high (measured through libass)."""
    size = 100
    for _ in range(3):
        box = probe(text, font, size, pos, an, bold)
        if not box:
            sys.exit(f"libass drew nothing for {text!r} in font {font!r} (font file missing in shared/fonts?)")
        w, h = box[2] - box[0] + 1, box[3] - box[1] + 1
        k = min(target_w / w, max_h / h)
        if abs(k - 1) < 0.02:
            break
        size = max(10, int(size * k))
    return size, probe(text, font, size, pos, an, bold)


def hook_markup(hook):
    """'a *b* c' -> libass text with b in yellow."""
    out, on = "", False
    for part in hook.split("*"):
        out += (f"{{\\1c{YELLOW}}}" if on else "{\\1c&H00FFFFFF&}") + part
        on = not on
    return out


def arabic_events(text, cx, cy, tw, mh, glow_rgb="&H0030A0F0", layer=1):
    """Gold calligraphy: blurred glow + deep gold + a paler top half (two-tone gold) + soft shadow."""
    size, box = fit(text, AR_FONT, tw, mh, (cx, cy))
    x0, y0, x1, y1 = box
    mid = y0 + int((y1 - y0) * 0.50)
    pos = f"\\an5\\pos({cx},{cy})"
    ev = [f"Dialogue: {layer},0:00:00.00,0:00:05.00,Ar,,0,0,0,,{{{pos}\\fs{size}\\bord{max(6, size // 10)}\\blur{max(10, size // 7)}"
          f"\\1c{glow_rgb}\\3c{glow_rgb}\\alpha&H60&}}{text}",
          f"Dialogue: {layer + 1},0:00:00.00,0:00:05.00,Ar,,0,0,0,,{{{pos}\\fs{size}\\bord2\\shad{max(3, size // 30)}"
          f"\\1c{GOLD_DEEP}\\3c&H00143050&}}{text}",
          f"Dialogue: {layer + 2},0:00:00.00,0:00:05.00,Ar,,0,0,0,,{{{pos}\\fs{size}\\bord0\\shad0\\1c{GOLD_PALE}"
          f"\\clip({x0 - 30},{y0 - 30},{x1 + 30},{mid})}}{text}"]
    return ev, box


ARABIC_BOX = {"A": (385, 215, 600, 240), "B": (640, 205, 780, 250), "C": (330, 110, 520, 150)}  # cx, cy, max w, max h
AR_FILE = FONTS / "ArefRuqaa-Bold.ttf"


def arabic_pil(bg, text, box, glow=(240, 160, 48)):
    """Gold calligraphy on bg (uint8 BGR) with Pillow + raqm: glow, soft shadow, dark edge, two-tone gold."""
    cx, cy, tw, mh = box
    size = 200
    for _ in range(4):  # fit the drawn ink to tw x mh
        f = ImageFont.truetype(str(AR_FILE), size, layout_engine=ImageFont.Layout.RAQM)
        x0, y0, x1, y1 = f.getbbox(text, direction="rtl")
        k = min(tw / (x1 - x0), mh / (y1 - y0))
        if abs(k - 1) < 0.02:
            break
        size = max(20, int(size * k))
    f = ImageFont.truetype(str(AR_FILE), size, layout_engine=ImageFont.Layout.RAQM)
    x0, y0, x1, y1 = f.getbbox(text, direction="rtl")
    w, h = x1 - x0, y1 - y0
    pad = size // 2
    mask = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    ImageDraw.Draw(mask).text((pad - x0, pad - y0), text, font=f, fill=255, direction="rtl")
    m = np.asarray(mask).astype(np.float32) / 255
    # layer colours (RGB): vertical two-tone gold inside the letters
    gh = m.shape[0]
    t = np.clip((np.arange(gh) - pad) / max(1, h), 0, 1)[:, None, None]
    pale, deep = np.array([255, 240, 170], np.float32), np.array([232, 160, 52], np.float32)
    fill = pale * (1 - t) + deep * t
    edge = np.asarray(mask.filter(ImageFilter.MaxFilter(2 * max(2, size // 40) + 1))).astype(np.float32) / 255
    glow_m = np.asarray(mask.filter(ImageFilter.GaussianBlur(max(8, size // 6)))).astype(np.float32) / 255
    shadow = np.asarray(mask.filter(ImageFilter.GaussianBlur(max(3, size // 25)))).astype(np.float32) / 255
    out = bg.astype(np.float32)
    ox, oy = int(cx - w / 2 - pad), int(cy - h / 2 - pad)

    def comp(layer_rgb, alpha, dx=0, dy=0):
        ax0, ay0 = max(0, ox + dx), max(0, oy + dy)
        ax1, ay1 = min(W, ox + dx + m.shape[1]), min(H, oy + dy + m.shape[0])
        if ax1 <= ax0 or ay1 <= ay0:
            return
        sx, sy = ax0 - (ox + dx), ay0 - (oy + dy)
        a = alpha[sy:sy + ay1 - ay0, sx:sx + ax1 - ax0][..., None]
        col = layer_rgb[sy:sy + ay1 - ay0, sx:sx + ax1 - ax0] if layer_rgb.ndim == 3 else layer_rgb
        out[ay0:ay1, ax0:ax1] = out[ay0:ay1, ax0:ax1] * (1 - a) + col[..., ::-1] * a if col.ndim == 3 else \
            out[ay0:ay1, ax0:ax1] * (1 - a) + np.array(col[::-1], np.float32) * a

    comp(np.array(glow, np.float32), np.clip(glow_m * 0.95, 0, 1))            # soft golden glow
    comp(np.array((10, 14, 30), np.float32), np.clip(shadow * 0.75, 0, 1), dx=size // 40, dy=size // 28)  # drop shadow
    comp(np.array((20, 44, 78), np.float32), edge)                              # dark edge for contrast
    comp(fill, m)                                                               # gold letters
    return np.clip(out, 0, 255).astype(np.uint8)


YELLOW_RGB, DARK, GOLD_RGB = (255, 225, 60), (16, 16, 16), (240, 170, 60)


def _fit_px(text_lines, font_name, tw, mh):
    """Largest Mukta/Yatra pixel size whose widest line's ink fits tw x mh (Pillow+raqm, same engine that draws it)."""
    longest = max(text_lines, key=len)
    size = 100.0
    for _ in range(4):
        f = TP._font(font_name, size)
        x0, y0, x1, y1 = f.getbbox(longest)
        k = min(tw / max(1, x1 - x0), mh / max(1, y1 - y0))
        if abs(k - 1) < 0.02:
            break
        size = max(10.0, size * k)
    return size


def hindi_pil(bg, layout, spec, hindi_font):
    """Hindi name / hook / chip with Pillow+raqm (the cloud's libass cannot shape Devanagari), same look and places as the
    libass path of build_ass. bg: uint8 BGR; returns it with the text drawn."""
    hi, chip, hook = spec["hindi"], spec.get("chip", ""), spec["hook"]
    hfont = hindi_font.replace(" ", "-") if hindi_font != "Yatra One" else "YatraOne-Regular"
    xb = "Mukta-ExtraBold"
    hook_lines = hook.replace("\\N", "\n").replace("*", "").split("\n")
    out = bg.copy()

    def put(text, font, px, anchor, x, y, hl=YELLOW_RGB, **st):
        style = dict(font=font, size=px * (TP.MUKTA_ASC + TP.MUKTA_DESC), fill=(255, 255, 255))
        style.update(st)
        spr = TP.render(text, style, hl=hl)
        h, w = spr.shape[:2]
        pad = int(round(style.get("outline", 0) + style.get("shadow", 0) + 6))
        sx = {"c": x - w // 2, "l": x - pad}[anchor[1]]
        sy = {"c": y - h // 2, "b": y - h + pad, "t": y - pad}[anchor[0]]
        TP.blend(out, spr, int(sx), int(sy))

    def multi(text, font, px, anchor, x, y, **st):  # hook may have several lines: one sprite per line, same size
        lines = text.replace("\\N", "\n").split("\n")
        lh = px * 1.4  # tighter than the font line height: the two hook lines read as one block
        if anchor[0] == "b":
            y0 = y - lh * (len(lines) - 1)
        elif anchor[0] == "c":
            y0 = y - lh * (len(lines) - 1) / 2
        else:
            y0 = y + lh / 2 - lh / 2
        shift = {"t": lh / 2, "c": 0, "b": -lh / 2}[anchor[0]]
        for i, ln in enumerate(lines):
            put(ln, font, px, "c" + anchor[1], x, int(y0 + i * lh + shift), **st)

    ribbon = dict(box=(8, 12, 20, 0.18), outline=16)
    chipst = dict(fill=(8, 24, 40), box=(*GOLD_RGB, 1.0), outline=10)
    hi_st = dict(outline=7, outline_rgba=(*DARK, 1.0), shadow=5, shadow_rgba=(0, 0, 0, 0.56))
    if layout == "A":
        multi(hi, hfont, _fit_px([hi], hfont, 560, 120), "cc", 385, 410, **hi_st)
        ks = min(_fit_px(hook_lines, xb, 680, 70), 64 * 0.6)
        multi(hook, xb, ks, "bl", 40, 662, **ribbon)
        if chip:
            multi(chip, "Mukta-Bold", 40 / 1.662, "tl", 40, 34, **chipst)
    elif layout == "B":
        multi(hi, hfont, _fit_px([hi], hfont, 640, 120), "cc", 640, 425, **hi_st)
        ks = min(_fit_px(hook_lines, xb, 880, 70), 66 / 1.662)
        multi(hook, xb, ks, "bc", 640, 655, **ribbon)
        if chip:
            multi(chip, "Mukta-Bold", 42 / 1.662, "tc", 640, 30, **chipst)
    else:
        ks = min(_fit_px(hook_lines, xb, 700, 110), 118 / 1.662)
        n = len(hook_lines)
        multi(hook, xb, ks, "tl", 50, 235, outline=8, outline_rgba=(*DARK, 1.0), shadow=5, shadow_rgba=(0, 0, 0, 0.56))
        multi(hi, hfont, min(_fit_px([hi], hfont, 420, 70), 66 / 1.662), "bl", 40, 676, **ribbon)
        if chip:
            multi(chip, "Mukta-Bold", 40 / 1.662, "tl", 40, 520 if n < 3 else 560, **chipst)
    return out


def build_ass(layout, spec, hindi_font, arabic):
    ar, hi, chip, hook = spec["arabic"], spec["hindi"], spec.get("chip", ""), spec["hook"]
    styles = (style("Ar", AR_FONT, 100, bold=-1) + style("Hi", hindi_font, 100, ol=7, sh=5, an=5) +
              style("Hook", "Mukta ExtraBold", 100, colour="&H00FFFFFF", outline="&H00101010", ol=6, sh=4, an=5) +
              style("Ribbon", "Mukta ExtraBold", 100, colour="&H00FFFFFF", outline="&HD0140C08", back="&HD0140C08", bs=3,
                    ol=16, an=1) +
              style("Chip", "Mukta Bold", 100, colour="&H00281808", outline=GOLD_DEEP, back=GOLD_DEEP, bs=3, ol=10, an=7))
    ev = []

    def add(style_name, x, y, size, text, an=5, extra=""):
        ev.append(f"Dialogue: 5,0:00:00.00,0:00:05.00,{style_name},,0,0,0,,{{\\an{an}\\pos({x},{y})\\fs{size}{extra}}}{text}")

    hook = hook.replace("\n", "\\N")  # a real newline in the JSON = a line break; ASS events are one line
    hook_lines = hook.replace("*", "").split("\\N")
    hook_marked = hook_markup(hook)
    if layout == "A":
        cx = 385
        if arabic == "amiri":
            ev += arabic_events(ar, cx, 215, 600, 240)[0]
        hs, _ = fit(hi, hindi_font, 560, 120, (cx, 410))
        add("Hi", cx, 410, hs, hi)
        ks, _ = fit(max(hook_lines, key=len), "Mukta ExtraBold", 680, 70, (50, 600), an=1)
        ks = min(ks, 64)
        add("Ribbon", 40, 662, ks, hook_marked, an=1)
        if chip:
            add("Chip", 40, 34, 40, chip, an=7)
    elif layout == "B":
        if arabic == "amiri":
            ev += arabic_events(ar, 640, 205, 780, 250)[0]
        hs, _ = fit(hi, hindi_font, 640, 120, (640, 425))
        add("Hi", 640, 425, hs, hi)
        ks, _ = fit(max(hook_lines, key=len), "Mukta ExtraBold", 880, 70, (640, 610))
        ks = min(ks, 66)
        ev.append(f"Dialogue: 5,0:00:00.00,0:00:05.00,Ribbon,,0,0,0,,{{\\an2\\pos(640,655)\\fs{ks}}}{hook_marked}")
        if chip:
            ev.append(f"Dialogue: 5,0:00:00.00,0:00:05.00,Chip,,0,0,0,,{{\\an8\\pos(640,30)\\fs42}}{chip}")
    else:  # C: hook first
        n_lines = max(1, len(hook_lines))
        ks, _ = fit(max(hook_lines, key=len), "Mukta ExtraBold", 700, 110, (50, 330), an=7)
        ks = min(ks, 118)
        add("Hook", 50, 235, ks, hook_marked, an=7, extra="\\bord8\\shad5")
        if arabic == "amiri":
            ev += arabic_events(ar, 330, 110, 520, 150)[0]
        hs, _ = fit(hi, hindi_font, 420, 70, (50, 640), an=1)
        add("Ribbon", 40, 676, min(hs, 66), hi, an=1)
        if chip:
            add("Chip", 40, 520 if n_lines < 3 else 560, 40, chip, an=7)
    return head(styles) + "\n".join(ev) + "\n"


def grade_bg(img, layout):
    bg = cv2.resize(img, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    bg *= (1 - 0.30 * np.clip(d - 0.5, 0, 1) ** 1.3)[..., None]  # vignette
    gray = bg.mean(axis=2, keepdims=True)
    bg = gray + (bg - gray) * 1.12  # a little more colour
    if layout == "A":
        bg *= (1 - 0.62 * np.clip(1 - xx / (W * 0.66), 0, 1) ** 0.8)[..., None]
    elif layout == "B":
        gy = np.clip(1 - np.abs(yy - H / 2) / (H / 2), 0, 1)
        bg *= (0.50 + 0.50 * gy ** 0.7)[..., None]
    else:
        bg *= (1 - 0.66 * np.clip(1 - xx / (W * 0.74), 0, 1) ** 0.8)[..., None]
        bg *= (1 - 0.25 * np.clip((yy - H * 0.7) / (H * 0.3), 0, 1))[..., None]
    return np.clip(bg, 0, 255).astype(np.uint8)


def render(spec, image: Path, layout, hindi_font, out: Path, arabic="aref"):
    bg = grade_bg(cv2.imread(str(image)), layout)
    if arabic == "aref":
        bg = arabic_pil(bg, spec["arabic"], ARABIC_BOX[layout])
    if arabic == "aref" and TP.available() and spec.get("hindi_engine", "auto") != "libass":
        bg = hindi_pil(bg, layout, spec, hindi_font)  # Pillow+raqm for Hindi too: no ffmpeg/libass in this path
        Image.fromarray(bg[..., ::-1]).save(out, quality=93)
        kb = out.stat().st_size // 1024
        if kb > 2000:
            sys.exit(f"{out.name} is {kb} KB (> 2 MB YouTube limit)")
        return kb
    with tempfile.TemporaryDirectory() as td:
        base, a = Path(td) / "bg.png", Path(td) / "t.ass"
        cv2.imwrite(str(base), bg)
        a.write_text(build_ass(layout, spec, hindi_font, arabic), encoding="utf-8")
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(base), "-vf",
                        f"subtitles=filename='{esc(a)}':fontsdir='{esc(FONTS)}'", "-frames:v", "1", "-q:v", "2", str(out)],
                       check=True)
    kb = out.stat().st_size // 1024
    if kb > 2000:
        sys.exit(f"{out.name} is {kb} KB (> 2 MB YouTube limit)")
    return kb


def generate(story: Path, spec, img: Path, engine="auto"):
    """Wallpaper. FREE FIRST (user 2026-10-30): Cloudflare flux (Rs0); the paid Gemini image only as the fallback in
    `auto` (story budget check first) or when asked (`--engine paid`). `--engine free` never spends."""
    from noor_look_test import STYLES
    from name_guard import find_names
    style_block = STYLES["a_cinematic_painted"]
    scene = spec.get("scene")
    if not scene:
        sys.exit('thumbnail.json needs a "scene" prompt for --generate (no people, empty dark area on the text side)')
    if find_names(scene + " " + style_block):
        sys.exit("BLOCK (RULES 12a): a name in the prompt")
    if engine in ("auto", "free"):
        import cf_image
        try:
            cf_image.generate(f"{scene} {style_block}", img)
            print(f"wallpaper: free engine (Cloudflare flux), Rs0 -> {img.name}")
            return
        except cf_image.FreeImageError as e:
            print(f"free engine unavailable: {e}")
            if engine == "free":
                sys.exit("--engine free: stopped, nothing was spent")
            print("falling back to the paid Gemini image (story budget check first)")
    import gemini_image
    import pricing
    import story_budget
    est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(scene) + len(style_block), 0) * pricing.usd_to_inr()
    story_budget.check(story.name, est)
    gemini_image.generate(scene, img, aspect_ratio="16:9", size="1K", style=style_block)
    print(story_budget.summary_line(story.name))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--spec")
    ap.add_argument("--image")
    ap.add_argument("--generate", action="store_true", help="make the wallpaper from spec['scene']")
    ap.add_argument("--engine", choices=["auto", "free", "paid"], default="auto",
                    help="auto = free Cloudflare flux first, paid Gemini only as fallback; free = never spend; paid = Gemini only")
    ap.add_argument("--hindi-font", default="Mukta ExtraBold")
    ap.add_argument("--arabic", choices=["aref", "amiri"], default="aref", help="aref = Pillow+raqm calligraphy (default); amiri = libass")
    ap.add_argument("--layouts", default="ABC")
    ap.add_argument("--out-dir")
    a = ap.parse_args()
    story = (ROOT / a.story).resolve() if not Path(a.story).is_absolute() else Path(a.story)
    spec_file = Path(a.spec) if a.spec else story / "thumbnail.json"
    spec = json.loads(spec_file.read_text(encoding="utf-8"))
    for k in ("arabic", "hindi", "hook"):
        if not spec.get(k):
            sys.exit(f"thumbnail spec has no '{k}'")
    img = Path(a.image) if a.image else story / spec.get("image", "images/thumb_scene.png")
    if a.generate and not img.exists():
        generate(story, spec, img, a.engine)
    if not img.exists():
        sys.exit(f"wallpaper missing: {img} (pass --image, or --generate for one paid image)")
    out_dir = Path(a.out_dir) if a.out_dir else story / "long/output"
    out_dir.mkdir(parents=True, exist_ok=True)
    for layout in a.layouts.upper():
        out = out_dir / f"{story.name}_thumbnail_v3{layout}.jpg"
        print(out.name, f"{render(spec, img, layout, a.hindi_font, out, a.arabic)} KB")


if __name__ == "__main__":
    main()
