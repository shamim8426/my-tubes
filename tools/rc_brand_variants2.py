"""Possibilities channel art, options E-H (more colours, structures, logos). Output channels/reality-check/brand/options/."""
import math
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from rc_brand_variants import OUT, F, grad, over, glow, bez, arrow, dot   # noqa: E402


# ---------------- logos ----------------
def mark_ring(d, cx, cy, S, cm, cd, cdot):          # E: bold ring, a path breaks out of it with an arrow
    R = .42 * S
    d.arc([cx - R, cy - R, cx + R, cy + R], 40, 320, fill=cd, width=int(S * .09))
    pts = bez((cx - .1 * S, cy + .12 * S), (cx + .12 * S, cy + .1 * S), (cx + .3 * S, cy - .1 * S), (cx + .62 * S, cy - .42 * S))
    arrow(d, pts, cm, int(S * .1), S * .24)
    dot(d, cx - .1 * S, cy + .12 * S, S * .07, cdot)


def mark_compass(d, cx, cy, S, cm, cd, cdot):       # F: four-way arrows, one highlighted
    for k, ang in enumerate([-90, 0, 90, 180]):
        a = math.radians(ang)
        p0 = (cx + .12 * S * math.cos(a), cy + .12 * S * math.sin(a))
        p1 = (cx + .56 * S * math.cos(a), cy + .56 * S * math.sin(a))
        arrow(d, [p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2), p1, (p1[0] + 1e-3 * math.cos(a), p1[1] + 1e-3 * math.sin(a))], cm if k == 1 else cd, int(S * .075), S * .2)
    R = .64 * S
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=cd, width=max(3, int(S * .02)))
    dot(d, cx, cy, S * .07, cdot)


def mark_sign(d, cx, cy, S, cm, cd, cdot):          # G: signpost with arrows pointing different ways
    d.rounded_rectangle([cx - S * .04, cy - .55 * S, cx + S * .04, cy + .6 * S], int(S * .03), fill=cd)
    for i, (dy, dx, c, flip) in enumerate([(-.38, .46, cm, 1), (-.08, .38, cd, -1), (.22, .50, cd, 1)]):
        y = cy + dy * S
        x0, x1 = (cx - S * .04, cx + dx * S) if flip == 1 else (cx + S * .04, cx - dx * S)
        s = 1 if flip == 1 else -1
        d.polygon([(x0, y - .09 * S), (x1 - s * .1 * S, y - .09 * S), (x1, y), (x1 - s * .1 * S, y + .09 * S), (x0, y + .09 * S)], fill=c)
    dot(d, cx, cy + .6 * S, S * .06, cdot)


def mark_bulb(d, cx, cy, S, cm, cd, cdot):          # H: idea bulb, filament branches like paths
    R = .38 * S
    d.ellipse([cx - R, cy - .5 * S, cx + R, cy - .5 * S + 2 * R], outline=cm, width=int(S * .07))
    d.rounded_rectangle([cx - .17 * S, cy + .3 * S, cx + .17 * S, cy + .46 * S], int(S * .04), fill=cm)
    d.rounded_rectangle([cx - .11 * S, cy + .49 * S, cx + .11 * S, cy + .58 * S], int(S * .04), fill=cm)
    base = (cx, cy + .3 * S)
    for ex, ey, c in [(cx - .2 * S, cy - .22 * S, cd), (cx, cy - .34 * S, cdot), (cx + .2 * S, cy - .22 * S, cd)]:
        d.line(bez(base, (base[0], base[1] - .2 * S), (ex, ey + .18 * S), (ex, ey)), fill=c, width=max(4, int(S * .03)), joint="curve")
        dot(d, ex, ey, S * .04, c)


def deco(im, kind, p, W, H):
    def f(d):
        if kind == "split":      # diagonal two-colour split
            d.polygon([(W * .90, 0), (W, 0), (W, H), (W * .78, H)], fill=p["main"] + (255,))
        elif kind == "stripes":
            for i in range(0, W, 70):
                d.line([(i, 0), (i - 400, H)], fill=p["main"] + (24,), width=2)
        elif kind == "waves":
            for k in range(6):
                pts = [(x, H * .72 + k * 46 + 28 * math.sin(x / 160 + k)) for x in range(0, W + 20, 20)]
                d.line(pts, fill=p["main"] + (44,), width=3)
        elif kind == "leaves":
            for gx in range(0, W, 150):
                for gy in range(0, H, 150):
                    d.ellipse([gx + 60, gy + 60, gx + 74, gy + 74], fill=p["main"] + (40,))
            d.ellipse([W - 460, H - 460, W + 140, H + 140], fill=p["dim"] + (34,))
    return over(im, f)


D = {
    "E_blackyellow": dict(bg=((10, 10, 12), (28, 28, 34)), main=(255, 214, 10), dim=(235, 235, 240), dot=(255, 255, 255), title=(255, 255, 255), sub=(255, 214, 10), mark=mark_ring, deco="stripes", dx=0),
    "F_oceanlight": dict(bg=((242, 249, 255), (206, 230, 250)), main=(0, 110, 230), dim=(30, 60, 110), dot=(0, 110, 230), title=(14, 32, 66), sub=(0, 110, 230), mark=mark_compass, deco="waves", dx=0),
    "G_signpost": dict(bg=((11, 25, 58), (22, 54, 120)), main=(255, 140, 40), dim=(250, 244, 232), dot=(255, 255, 255), title=(255, 255, 255), sub=(255, 150, 60), mark=mark_sign, deco="split", dx=0),
    "H_mintbulb": dict(bg=((236, 250, 242), (214, 240, 226)), main=(18, 120, 80), dim=(255, 112, 90), dot=(255, 176, 30), title=(10, 56, 40), sub=(255, 112, 90), mark=mark_bulb, deco="leaves", dx=0),
}


def banner(name, p):
    W, H = 2048, 1152
    im = deco(grad(W, H, *p["bg"]), p["deco"], p, W, H)
    mx, tx = 560, 780 + p["dx"]
    im = glow(im, mx, H // 2, 200, p["main"], .14)
    im = over(im, lambda d: p["mark"](d, mx, H // 2, 260, p["main"], p["dim"], p["dot"]))
    d = ImageDraw.Draw(im)
    y1 = H // 2 - 95
    tcol = p["title"]
    d.text((tx, y1), "POSSIBILITIES", font=F(96), fill=tcol)
    d.text((tx + 4, y1 + 122), "Kya ho sakta hai?", font=F(52), fill=p["sub"])
    im.convert("RGB").save(OUT / f"banner_{name}.png")
    return im.convert("RGB")


def logo(name, p):
    S = 800
    im = deco(grad(S, S, *p["bg"]), p["deco"], p, S, S)
    im = glow(im, 400, 400, 230, p["main"], .14)
    im = over(im, lambda d: p["mark"](d, 400, 400, 460, p["main"], p["dim"], p["dot"]))
    im.convert("RGB").save(OUT / f"logo_{name}.png")
    return im.convert("RGB")


if __name__ == "__main__":
    sheet = Image.new("RGB", (1500, 4 * 470), (30, 30, 30))
    dd = ImageDraw.Draw(sheet)
    for i, (name, p) in enumerate(D.items()):
        b = banner(name, p)
        lg = logo(name, p)
        sheet.paste(b.resize((960, 540)).crop((0, 45, 960, 495)), (10, i * 470 + 10))
        sheet.paste(lg.resize((450, 450)), (1000, i * 470 + 10))
        dd.text((1465, i * 470 + 10), name[0], font=F(36), fill=(255, 255, 255))
    sheet.save(OUT / "options_sheet2.png")
    print(OUT)
