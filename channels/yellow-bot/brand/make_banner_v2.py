"""DevRoboLab banner options (free). Safe area for all devices = centre 1235x338 (x 406-1641, y 407-745).
    .venv\Scripts\python -X utf8 channels\yellow-bot\brand\make_banner_v2.py
Writes brand/banner_v2_a.png (white, calm) and brand/banner_v2_b.png (yellow, bold)."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_art import M, OUT, YEL, INK, WHITE, cutout, fit, font  # noqa: E402

W, H = 2048, 1152
TAG = "AI ko seedhi bhasha me samjho"
PILLS = ["AI News", "Claude Code", "Shorts + Long"]


def pills(d, x, y, fill, ink, outline):
    f = font("Poppins-Bold.ttf", 30)
    for p in PILLS:
        w = int(d.textlength(p, font=f)) + 52
        d.rounded_rectangle((x, y, x + w, y + 62), radius=31, fill=fill, outline=outline, width=4)
        d.text((x + 26, y + 9), p, font=f, fill=ink)
        x += w + 18


def name(d, x, y, ink, box, box_ink):
    t1 = font("Poppins-ExtraBold.ttf", 118)
    d.text((x, y), "DevRobo", font=t1, fill=ink)
    w1 = d.textlength("DevRobo", font=t1)
    wl = d.textlength("Lab", font=t1)
    d.rounded_rectangle((x + w1 + 4, y + 30, x + w1 + wl + 24, y + 150), radius=28, fill=box)
    d.text((x + w1 + 10, y), "Lab", font=t1, fill=box_ink)


def a():
    c = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 40), fill=YEL)
    d.rectangle((0, H - 40, W, H), fill=YEL)
    for crop, right in (((0.045, 0.27), False), ((0.73, 0.955), True)):  # robots outside the safe area
        r = fit(cutout(M / "team.png", crop), 600)
        if right:
            r = r.transpose(Image.FLIP_LEFT_RIGHT)
        c.paste(r, (W - 40 - r.width if right else 40, (H - r.height) // 2 + 10), r)
    wave = fit(cutout(M / "wave.png"), 290)
    c.paste(wave, (440, 440), wave)
    name(d, 760, 410, INK, YEL, INK)
    d.text((762, 565), TAG, font=font("Poppins-Bold.ttf", 42), fill=INK)
    pills(d, 762, 650, WHITE, INK, INK)
    c.save(OUT / "banner_v2_a.png")


def b():
    c = Image.new("RGB", (W, H), YEL)
    d = ImageDraw.Draw(c)
    # soft diagonal block + dots for depth (own look)
    d.polygon([(1180, 0), (W, 0), (W, H), (880, H)], fill=(255, 224, 70))
    for gx in range(70, 380, 52):
        for gy in range(120, 1040, 52):
            d.ellipse((gx, gy, gx + 9, gy + 9), fill=(240, 196, 0))
    r1 = fit(cutout(M / "work.png"), 520)
    c.paste(r1, (30, (H - r1.height) // 2 + 20), r1)
    r2 = fit(cutout(M / "thumbs.png"), 520).transpose(Image.FLIP_LEFT_RIGHT)
    c.paste(r2, (W - 30 - r2.width, (H - r2.height) // 2 + 20), r2)
    name(d, 620, 410, INK, WHITE, INK)
    d.text((622, 565), TAG, font=font("Poppins-Bold.ttf", 42), fill=INK)
    pills(d, 622, 650, INK, YEL, INK)
    c.save(OUT / "banner_v2_b.png")


if __name__ == "__main__":
    a()
    b()
    print("ok")
