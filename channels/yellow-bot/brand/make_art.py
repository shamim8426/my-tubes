"""DevRoboLab channel art (free): profile picture 800x800 and banner 2048x1152 from the mascot PNGs + Poppins.
    .venv\Scripts\python -X utf8 channels\yellow-bot\brand\make_art.py
Outputs: brand/dp.png, brand/banner.png. Banner safe area for all devices = centre 1235x338 (x 406-1641, y 407-745)."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
M = ROOT / "channels/yellow-bot/mascot"
OUT = ROOT / "channels/yellow-bot/brand"
F = ROOT / "shared/fonts"
YEL, INK, WHITE = (255, 214, 10), (17, 17, 17), (255, 255, 255)


def cutout(path, crop=None):
    """White background -> transparent (only the white connected to the image border, so the white body stays)."""
    im = Image.open(path).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), 0, int(crop[1] * w), h))
    work = im.copy()
    key = (255, 0, 255)
    for seed in ((0, 0), (work.width - 1, 0), (0, work.height - 1), (work.width - 1, work.height - 1)):
        if work.getpixel(seed) != key:
            ImageDraw.floodfill(work, seed, key, thresh=26)
    a = np.asarray(work)
    bg = (a[:, :, 0] == 255) & (a[:, :, 1] == 0) & (a[:, :, 2] == 255)
    mask = Image.fromarray(np.where(bg, 0, 255).astype("uint8"))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out.crop(out.getbbox())


def fit(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def font(name, size):
    return ImageFont.truetype(str(F / name), size)


def dp():
    S = 800
    c = Image.new("RGB", (S, S), YEL)
    d = ImageDraw.Draw(c)
    d.ellipse((60, 60, S - 60, S - 60), fill=WHITE, outline=INK, width=14)  # YouTube crops to a circle
    r = fit(cutout(M / "wave.png"), 560)
    c.paste(r, ((S - r.width) // 2, (S - r.height) // 2 + 20), r)
    c.save(OUT / "dp.png")


def banner():
    W, H = 2048, 1152
    c = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 40), fill=YEL)
    d.rectangle((0, H - 40, W, H), fill=YEL)
    # one big robot per side (tight crops of the lineup), outside the safe area (x < 406, x > 1641)
    for crop, right in (((0.045, 0.27), False), ((0.73, 0.955), True)):
        r = fit(cutout(M / "team.png", crop), 600)
        if right:
            r = r.transpose(Image.FLIP_LEFT_RIGHT)
        x = W - 40 - r.width if right else 40
        c.paste(r, (x, (H - r.height) // 2 + 10), r)
    # centre block inside the safe area (x 406-1641, y 407-745)
    wave = fit(cutout(M / "wave.png"), 290)
    c.paste(wave, (440, 430), wave)
    t1, t2 = font("Poppins-ExtraBold.ttf", 112), font("Poppins-Bold.ttf", 38)
    x0 = 760
    # channel renamed 2026-11-05: yellow Bot -> DevRoboLab (same layout, yellow highlight on "Lab")
    d.text((x0, 420), "DevRobo", font=t1, fill=INK)
    w1 = d.textlength("DevRobo", font=t1)
    d.rounded_rectangle((x0 + w1 + 4, 450, x0 + w1 + d.textlength("Lab", font=t1) + 22, 566), radius=26, fill=YEL)
    d.text((x0 + w1, 420), "Lab", font=t1, fill=INK)
    d.text((x0 + 2, 585), "Claude Code features, Hinglish me", font=t2, fill=INK)
    d.text((x0 + 2, 640), "Robot ke saath, step by step.", font=font("Poppins-Medium.ttf", 32), fill=(90, 90, 90))
    c.save(OUT / "banner.png")


if __name__ == "__main__":
    dp()
    banner()
    print("ok")
