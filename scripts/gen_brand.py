"""Kissago brand kit (BRAND.md). Paid steps only with the user's OK.

Usage: python scripts/gen_brand.py icons [1 2 3 4]   -> brand/_work/icon_v<N>.png (Gemini 1K, ₹3.24 each)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402
from paths import channel_dir  # noqa: E402

BRAND = channel_dir() / "brand"
WORK = BRAND / "_work"
CHAR = channel_dir() / "characters"

ICON_BASE = """Flat vector logo icon, NO text, letters or numbers anywhere. {scene}
Mitthu is EXACTLY the parrot in the attached reference sheet: green body, RED beak, thin RED neck ring, friendly eyes.
Simple bold shapes, thick clean dark outlines (dark indigo #1F1B4D), flat colours only from: night indigo #1F1B4D,
marigold #F4A300, cream #FFF4DC, parrot green #2FA84F, plus the red of the beak and neck ring. No gradients, no
shadows, no texture, no scenery. The icon is centred and fills about 70% of the square. Plain flat PURE WHITE
background (#FFFFFF) all around, nothing else in the image."""

VARIANTS = {
    1: "Mitthu the green parrot sits on top of an open book seen straight from the front; the book is cream with "
       "marigold covers.",
    2: "CLOSE-UP: Mitthu the green parrot is big (about 60% of the frame, head and upper body clearly readable at a tiny "
       "size), and a small open book sits below him, partly visible.",
    3: "Mitthu the green parrot sits on top of an open book, wings slightly open as if starting a story; cream pages, "
       "marigold covers.",
    4: "Mitthu the green parrot sits on top of an open book; a few small marigold sparkles rise from the open pages.",
}


def icons(ids):
    WORK.mkdir(parents=True, exist_ok=True)
    for n in ids:
        generate(ICON_BASE.format(scene=VARIANTS[n]), WORK / f"icon_v{n}.png", refs=[CHAR / "mitthu_sheet.png"],
                 aspect_ratio="1:1", size="1K")




# ---------------- free steps (no Gemini) ----------------
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

CHOSEN = WORK / "icon_v2.png"  # user picked option 2 (close-up Mitthu) on 2026-10-18
INDIGO, MARIGOLD, CREAM, GREEN = (0x1F, 0x1B, 0x4D), (0xF4, 0xA3, 0x00), (0xFF, 0xF4, 0xDC), (0x2F, 0xA8, 0x4F)


def cutout(src: Path, size=2048, margin=0.06) -> Image.Image:
    """White background -> transparent. Only white connected to the image border is removed (pages inside the thick
    outline stay); the light fringe next to the outline gets partial alpha so edges stay smooth."""
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    light = (a.min(axis=2) > 225)
    # flood fill from the border over light pixels
    bg = np.zeros(light.shape, bool)
    h, w = light.shape
    stack = [(y, x) for x in range(w) for y in (0, h - 1)] + [(y, x) for y in range(h) for x in (0, w - 1)]
    while stack:
        y, x = stack.pop()
        if 0 <= y < h and 0 <= x < w and light[y, x] and not bg[y, x]:
            bg[y, x] = True
            stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    alpha = np.where(bg, 0, 255).astype(np.float32)
    # soft edge: pixels next to the background get alpha from how dark they are
    near = np.asarray(Image.fromarray((bg * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
    fringe = near & ~bg
    lum = a.mean(axis=2)
    alpha[fringe] = np.clip((255 - lum[fringe]) / (255 - 60) * 255, 0, 255)
    rgba = np.dstack([a.astype(np.uint8), alpha.astype(np.uint8)])
    out = Image.fromarray(rgba, "RGBA")
    out = out.crop(out.getbbox())
    side = int(max(out.size) * (1 + 2 * margin))
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(out, ((side - out.width) // 2, (side - out.height) // 2), out)
    return sq.resize((size, size), Image.LANCZOS)


def icon():
    ic = cutout(CHOSEN)
    ic.save(BRAND / "icon.png")
    print("saved", BRAND / "icon.png", ic.size)


import shutil  # noqa: E402
import subprocess  # noqa: E402

from paths import FONTS_DIR, ROOT  # noqa: E402

FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
if not FFMPEG.exists():
    FFMPEG = Path(shutil.which("ffmpeg") or FFMPEG)
TAGLINE = "हर शाम एक नया किस्सा"


def text_layer(text, family, size, rgb, bold=False, spacing=0) -> Image.Image:
    """Text rendered by libass (HarfBuzz shaping) white-on-black, turned into a coloured RGBA layer cropped to the ink.
    Spacing must stay 0 for Devanagari (any spacing breaks the matras); Latin may use spacing."""
    tmp = WORK / "txt"
    (tmp / "fonts").mkdir(parents=True, exist_ok=True)
    for f in ("RozhaOne-Regular.ttf", "Mukta-Bold.ttf", "Mukta-ExtraBold.ttf"):
        shutil.copy(FONTS_DIR / f, tmp / "fonts" / f)
    W, H = int(size * max(len(text), 4) * 0.9) + 200, int(size * 2.2)
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: A,{family},{size},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,{-1 if bold else 0},0,0,0,100,100,{spacing},0,1,0,0,5,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,A,,0,0,0,,{{\\pos({W // 2},{H // 2})}}{text}
"""
    (tmp / "t.ass").write_text(ass, encoding="utf-8")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}",
                    "-vf", "subtitles=filename=t.ass:fontsdir=fonts", "-frames:v", "1", "t.png"], cwd=tmp, check=True)
    mask = Image.open(tmp / "t.png").convert("L")
    layer = Image.new("RGBA", mask.size, rgb + (0,))
    layer.putalpha(mask)
    return layer.crop(mask.getbbox())


def wordmark() -> Image.Image:
    """'किस्सागो' (Rozha One, marigold) over a small 'KISSAGO' (Mukta Bold, cream, letter-spaced)."""
    name = text_layer("किस्सागो", "Rozha One", 420, MARIGOLD)
    sub = text_layer("KISSAGO", "Mukta", 120, CREAM, bold=True, spacing=28)
    sub = sub.resize((int(name.width * 0.62), int(sub.height * name.width * 0.62 / sub.width)), Image.LANCZOS)
    gap = int(name.height * 0.10)
    wm = Image.new("RGBA", (name.width, name.height + gap + sub.height), (0, 0, 0, 0))
    wm.alpha_composite(name, (0, 0))
    wm.alpha_composite(sub, ((name.width - sub.width) // 2, name.height + gap))
    return wm


def pad(img, frac=0.06):
    m = int(max(img.size) * frac)
    out = Image.new("RGBA", (img.width + 2 * m, img.height + 2 * m), (0, 0, 0, 0))
    out.alpha_composite(img, (m, m))
    return out


def lockups():
    ic, wm = Image.open(BRAND / "icon.png").convert("RGBA"), wordmark()
    wm.save(BRAND / "wordmark.png")
    # horizontal: icon left, name right, both vertically centred
    ih = int(wm.height * 1.35)
    ich = ic.resize((ih, ih), Image.LANCZOS)
    gap = int(ih * 0.10)
    hz = Image.new("RGBA", (ih + gap + wm.width, ih), (0, 0, 0, 0))
    hz.alpha_composite(ich, (0, 0))
    hz.alpha_composite(wm, (ih + gap, (ih - wm.height) // 2))
    pad(hz).save(BRAND / "logo_horizontal.png")
    # stacked: icon on top, name below
    iw = int(wm.width * 0.85)
    ics = ic.resize((iw, iw), Image.LANCZOS)
    gap = int(iw * 0.04)
    st = Image.new("RGBA", (max(iw, wm.width), iw + gap + wm.height), (0, 0, 0, 0))
    st.alpha_composite(ics, ((st.width - iw) // 2, 0))
    st.alpha_composite(wm, ((st.width - wm.width) // 2, iw + gap))
    pad(st).save(BRAND / "logo_stacked.png")
    for f in ("wordmark.png", "logo_horizontal.png", "logo_stacked.png"):
        print("saved", BRAND / f, Image.open(BRAND / f).size)


def dp():
    """800x800 indigo, icon in the middle 70% (survives the circle crop)."""
    ic = Image.open(BRAND / "icon.png").convert("RGBA").resize((560, 560), Image.LANCZOS)
    d = Image.new("RGBA", (800, 800), INDIGO + (255,))
    d.alpha_composite(ic, (120, 120))
    d.convert("RGB").save(BRAND / "kissago_dp.png")
    print("saved", BRAND / "kissago_dp.png")


def watermark():
    Image.open(BRAND / "icon.png").convert("RGBA").resize((150, 150), Image.LANCZOS).save(BRAND / "watermark.png")
    print("saved", BRAND / "watermark.png")


def brand_corner(path, where="bl", width_frac=0.19):
    """Thumbnail brand: small logo_horizontal on a soft indigo patch (BRAND.md). bl = bottom-left, tc = top-centre."""
    im = Image.open(path).convert("RGBA")
    lg = Image.open(BRAND / "logo_horizontal.png").convert("RGBA")
    w = int(im.width * width_frac)
    lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)
    m = int(im.width * 0.015)
    patch = Image.new("RGBA", (lg.width + 2 * m, lg.height + 2 * m), (0, 0, 0, 0))
    ImageDraw.Draw(patch).rounded_rectangle((0, 0, patch.width - 1, patch.height - 1), radius=m * 2,
                                           fill=INDIGO + (190,))
    patch.alpha_composite(lg, (m, m))
    edge = int(im.width * 0.02)
    xy = (edge, im.height - patch.height - edge) if where == "bl" else ((im.width - patch.width) // 2, edge)
    im.alpha_composite(patch, xy)
    im.convert("RGB").save(path)


BANNER_PROMPT = """Wide 16:9 YouTube channel banner background illustration, NO text, letters, numbers or signs anywhere.
Scene: a cosy Indian mohalla lane at night (Gulmohar Mohalla): deep night-indigo sky (#1F1B4D) with a few soft stars,
small houses with warm marigold (#F4A300) lamp-lit windows, a gulmohar tree with soft orange-red flowers, warm and
peaceful, family-friendly, not scary.
On the RIGHT side only (between 68% and 92% of the width, between 35% and 70% of the height), a gentle glimpse of
Dadi sitting on a low charpai telling a story, Golu sitting beside her listening, and Mitthu the parrot perched on the
charpai — Dadi and Golu exactly as in their reference sheets, Mitthu exactly like the attached parrot logo (big round
green head, red beak, thin red neck ring), all fairly small.
COMPOSITION IS CRITICAL: the whole CENTRE and LEFT-CENTRE of the image (from 20% to 65% of the width, from 30% to 70%
of the height) must be calm and plain: dark night sky and a softly lit plain wall, no objects, no people, for a logo.
Keep important details away from the top and bottom edges. Flat 2D cartoon style, thick clean outlines, flat colours
in the brand palette: night indigo, marigold, cream (#FFF4DC), parrot green (#2FA84F)."""

BW, BH = 2560, 1440
SAFE = (507, 508, 2053, 931)  # 1546x423 visible on every device


def banner_bg():
    """PAID (2K, ~₹4.86): banner background, no text."""
    raw = WORK / "banner_v2_raw.png"
    generate(BANNER_PROMPT, raw, refs=[CHAR / "dadi_sheet.png", CHAR / "golu_sheet.png", CHOSEN],
             aspect_ratio="16:9", size="2K")
    reframe()


def reframe(zoom=1.28, ax=0.78, ay=1.0):
    """Free: re-crop the generated background. zoom > 1 and ay=1 (keep the bottom) lift the characters into the
    desktop band (y 508-931); ax=1 keeps the right edge, where Dadi, Golu and Mitthu sit."""
    im = Image.open(WORK / "banner_v2_raw.png").convert("RGB")
    s = max(BW / im.width, BH / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = int((im.width - BW) * ax), int((im.height - BH) * ay)
    im.crop((x, y, x + BW, y + BH)).save(WORK / "banner_v2_art.png")
    banner()


def banner():
    """Free: logo_horizontal + tagline inside the safe area on the background; plus device crop previews."""
    bg = Image.open(WORK / "banner_v2_art.png").convert("RGBA")
    lg = Image.open(BRAND / "logo_horizontal.png").convert("RGBA")
    sx0, sy0, sx1, sy1 = SAFE
    lw = int((sx1 - sx0) * 0.50)
    lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    tag = text_layer(TAGLINE, "Mukta", 70, CREAM, bold=True)
    gap = 18
    block_h = lg.height + gap + tag.height
    x = sx0 + 80
    y = sy0 + (sy1 - sy0 - block_h) // 2
    # BRAND.md: on a busy/light picture the logo sits on a soft indigo panel (cream text needs a dark ground)
    m = 34
    panel = Image.new("RGBA", (lg.width + 2 * m, block_h + 2 * m), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle((0, 0, panel.width - 1, panel.height - 1), radius=40, fill=INDIGO + (225,))
    bg.alpha_composite(panel, (x - m, y - m))
    bg.alpha_composite(lg, (x, y))
    bg.alpha_composite(tag, (x + (lg.width - tag.width) // 2, y + lg.height + gap))
    out = BRAND / "kissago_banner_v2.png"
    bg.convert("RGB").save(out)
    print("saved", out, bg.size, "| logo+tagline box:", (x, y, x + lg.width, y + block_h), "inside safe", SAFE)
    # device previews: TV = full, desktop = full-width middle band, mobile = safe area
    full = bg.convert("RGB")
    tv = full.resize((960, 540))
    desk = full.crop((0, sy0, BW, sy1)).resize((1280, 212))
    mob = full.crop(SAFE).resize((773, 212))
    sheet = Image.new("RGB", (1280, 540 + 212 + 212 + 60), (240, 240, 240))
    d = ImageDraw.Draw(sheet)
    sheet.paste(tv, (0, 20)); d.text((5, 3), "TV (full 2560x1440)", fill=(0, 0, 0))
    sheet.paste(desk, (0, 580)); d.text((5, 563), "Desktop (2560x423 band)", fill=(0, 0, 0))
    sheet.paste(mob, (0, 812)); d.text((5, 795), "Mobile (1546x423 safe area)", fill=(0, 0, 0))
    sheet.save(WORK / "banner_v2_devices.jpg", quality=90)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "icons":
        icons([int(x) for x in sys.argv[2:]] or [1, 2, 3, 4])
    else:
        globals()[cmd]()
