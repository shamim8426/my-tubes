"""Possibilities channel art: 4 different options (colour + structure + logo). Output channels/reality-check/brand/options/."""
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "channels/reality-check/brand/options"
OUT.mkdir(parents=True, exist_ok=True)
FB = str(ROOT / "shared/fonts/Poppins-Bold.ttf")


def F(n):
    return ImageFont.truetype(FB, n)


def grad(w, h, c1, c2):
    yy, xx = np.mgrid[0:h, 0:w]
    t = ((xx / w + yy / h) / 2)[..., None]
    a = np.array(c1, np.float32) * (1 - t) + np.array(c2, np.float32) * t
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")


def over(im, fn):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(ov))
    return Image.alpha_composite(im, ov)


def glow(im, cx, cy, r, col, a):
    g = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (int(255 * a),))
    return Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(r * .55)))


def bez(p0, p1, p2, p3, n=60):
    return [tuple((1 - t) ** 3 * np.array(p0) + 3 * (1 - t) ** 2 * t * np.array(p1) + 3 * (1 - t) * t ** 2 * np.array(p2) + t ** 3 * np.array(p3)) for t in np.linspace(0, 1, n)]


def arrow(d, pts, col, w, L):
    d.line(pts, fill=col, width=w, joint="curve")
    for x, y in pts[::2]:
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)
    a = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
    tip = pts[-1]
    d.polygon([(tip[0] + L * .5 * math.cos(a), tip[1] + L * .5 * math.sin(a)), (tip[0] - L * math.cos(a - .5), tip[1] - L * math.sin(a - .5)),
               (tip[0] - L * math.cos(a + .5), tip[1] - L * math.sin(a + .5))], fill=col)


def dot(d, x, y, r, c):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)


# ---------------- marks / logos ----------------
def mark_fan(d, cx, cy, S, cm, cd, cdot):          # A: rays from one point, one bright
    sx, sy = cx - .42 * S, cy
    for ang in [-48, -24, 0, 24, 48]:
        r = .84 * S
        a = math.radians(ang)
        ex, ey = sx + r * math.cos(a), sy + r * math.sin(a)
        pts = bez((sx, sy), (sx + .3 * S, sy), (ex - .25 * S * math.cos(a), ey - .25 * S * math.sin(a)), (ex, ey))
        if ang == -24:
            arrow(d, pts, cm, int(S * .05), S * .14)
        else:
            d.line(pts, fill=cd, width=max(3, int(S * .02)), joint="curve")
            dot(d, ex, ey, S * .025, cd)
    dot(d, sx, sy, S * .06, cdot)


def mark_tree(d, cx, cy, S, cm, cd, cdot):         # B: decision tree
    root = (cx - .42 * S, cy)
    l1 = [(cx - .05 * S, cy - .32 * S), (cx - .05 * S, cy + .32 * S)]
    l2 = [(cx + .38 * S, cy - .5 * S), (cx + .38 * S, cy - .14 * S), (cx + .38 * S, cy + .14 * S), (cx + .38 * S, cy + .5 * S)]

    def link(p, q, c, w):
        d.line(bez(p, (p[0] + .22 * S, p[1]), (q[0] - .22 * S, q[1]), q), fill=c, width=w, joint="curve")
    thin = max(3, int(S * .02))
    for i, p in enumerate(l1):
        for q in l2[i * 2:i * 2 + 2]:
            link(p, q, cd, thin)
        link(root, p, cd, thin)
    link(root, l1[0], cm, int(S * .05))
    link(l1[0], l2[1], cm, int(S * .05))
    for q in l2:
        dot(d, q[0], q[1], S * .03, cd)
    for p in l1:
        dot(d, p[0], p[1], S * .035, cd)
    dot(d, l2[1][0], l2[1][1], S * .06, cm)
    dot(d, l1[0][0], l1[0][1], S * .045, cm)
    dot(d, root[0], root[1], S * .065, cdot)


def mark_q(d, cx, cy, S, cm, cd, cdot):            # C: big question mark with branching dots
    f = F(int(S * 1.25))
    bb = d.textbbox((0, 0), "?", font=f)
    d.text((cx - (bb[0] + bb[2]) / 2 - S * .1, cy - (bb[1] + bb[3]) / 2 - S * .05), "?", font=f, fill=cm)
    for dx, dy in [(.5, -.4), (.6, -.12), (.54, .2)]:
        d.line([(cx + .2 * S, cy - .05 * S), (cx + dx * S, cy + dy * S)], fill=cd, width=max(3, int(S * .02)))
        dot(d, cx + dx * S, cy + dy * S, S * .035, cdot)


def mark_p(d, cx, cy, S, cm, cd, cdot):            # D: monogram P - stem + bowl that is a path ending in an arrow
    x0, y0, y1 = cx - .30 * S, cy - .5 * S, cy + .5 * S
    w = int(S * .13)
    d.line([(x0, y0 - w // 2), (x0, y1)], fill=cm, width=w)
    pts = bez((x0, y0), (x0 + .62 * S, y0 - .06 * S), (x0 + .74 * S, y0 + .52 * S), (x0 + .08 * S, y0 + .54 * S), 50)
    arrow(d, pts, cd, int(S * .11), S * .2)
    for k, (ex, ey) in enumerate([(cx + .5 * S, cy - .08 * S), (cx + .46 * S, cy + .2 * S)]):
        d.line([(x0, y1 - .18 * S), (ex, ey + .24 * S)], fill=cdot + (120,), width=max(3, int(S * .018)))
        dot(d, ex, ey + .24 * S, S * .03, cdot)
    dot(d, x0, y1, S * .06, cdot)


def deco(im, kind, p, W, H):
    def f(d):
        if kind == "arcs":
            for i in range(8):
                r = 260 + i * 120
                d.arc([W * .88 - r, H * .5 - r, W * .88 + r, H * .5 + r], 120, 240, fill=p["main"] + (40,), width=3)
        elif kind == "hex":
            for gx in range(0, W, 120):
                for gy in range(0, H, 104):
                    x = gx + (60 if (gy // 104) % 2 else 0)
                    d.polygon([(x + 40 * math.cos(math.radians(60 * k + 30)), gy + 40 * math.sin(math.radians(60 * k + 30))) for k in range(6)], outline=p["dim"] + (22,))
        elif kind == "dots":
            for gx in range(40, W, 56):
                for gy in range(40, H, 56):
                    d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(60, 60, 70, 40))
            d.ellipse([W - 520, -160, W + 160, 520], fill=p["main"] + (26,))
            d.ellipse([-200, H - 380, 360, H + 160], fill=p["dim"] + (18,))
        elif kind == "bars":
            for i in range(9):
                d.polygon([(W - 700 + i * 90, 0), (W - 640 + i * 90, 0), (W - 1000 + i * 90, H), (W - 1060 + i * 90, H)], fill=(p["dim"] if i % 2 else p["main"]) + (22,))
    return over(im, f)


D = {
    "A_sunrise": dict(bg=((38, 10, 28), (150, 48, 40)), main=(255, 196, 70), dim=(255, 215, 175), dot=(255, 255, 255), title=(255, 255, 255), sub=(255, 208, 120), mark=mark_fan, deco="arcs", dx=0),
    "B_teal": dict(bg=((6, 30, 36), (10, 80, 78)), main=(190, 255, 80), dim=(150, 225, 215), dot=(255, 255, 255), title=(255, 255, 255), sub=(190, 255, 80), mark=mark_tree, deco="hex", dx=60),
    "C_paper": dict(bg=((247, 241, 228), (236, 226, 205)), main=(226, 62, 40), dim=(60, 60, 70), dot=(226, 62, 40), title=(24, 24, 32), sub=(226, 62, 40), mark=mark_q, deco="dots", dx=0),
    "D_violet": dict(bg=((14, 8, 36), (62, 18, 96)), main=(255, 255, 255), dim=(255, 70, 160), dot=(60, 220, 255), title=(255, 255, 255), sub=(60, 220, 255), mark=mark_p, deco="bars", dx=60),
}


def banner(name, p):
    W, H = 2048, 1152
    im = deco(grad(W, H, *p["bg"]), p["deco"], p, W, H)
    mx, tx = 560, 780 + p["dx"]
    im = glow(im, mx, H // 2, 200, p["dim"] if name[0] == "D" else p["main"], .18)
    im = over(im, lambda d: p["mark"](d, mx, H // 2, 250, p["main"], p["dim"], p["dot"]))
    d = ImageDraw.Draw(im)
    y1 = H // 2 - 95
    d.text((tx, y1), "POSSIBILITIES", font=F(96), fill=p["title"])
    d.text((tx + 4, y1 + 122), "Kya ho sakta hai?", font=F(52), fill=p["sub"])
    im.convert("RGB").save(OUT / f"banner_{name}.png")
    return im.convert("RGB")


def logo(name, p):
    S = 800
    im = deco(grad(S, S, *p["bg"]), p["deco"], p, S, S)
    im = glow(im, 400, 400, 230, p["dim"] if name[0] == "D" else p["main"], .16)
    im = over(im, lambda d: p["mark"](d, 400, 400, 440, p["main"], p["dim"], p["dot"]))
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
    sheet.save(OUT / "options_sheet.png")
    print(OUT)
