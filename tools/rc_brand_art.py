"""Possibilities GENERIC channel art (own render, not tied to any video): logo 800x800 + banner 2048x1152. Output channels/reality-check/brand/."""
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "channels/reality-check/brand"; OUT.mkdir(parents=True, exist_ok=True)
FB = str(ROOT / "shared/fonts/Poppins-Bold.ttf")
NAVY, ORANGE, YEL, ICE = (11, 14, 28), (255, 140, 40), (255, 214, 10), (150, 190, 255)

def bg(w, h, seed, glow_at=None, stars=0.0):
    yy, xx = np.mgrid[0:h, 0:w]
    gx, gy = glow_at or (w / 2, h / 2)
    d = np.hypot(xx - gx, yy - gy) / (max(w, h) * 0.65)
    t = (xx / w * 0.5 + yy / h * 0.5)[..., None]
    base = np.array(NAVY, np.float32) * (1 - t) + np.array((14, 30, 62), np.float32) * t
    base += (np.clip(1 - d, 0, 1) ** 2)[..., None] * np.array([14, 34, 78], np.float32)
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8)).convert("RGBA")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    step = max(40, w // 22)
    for x in range(0, w, step): dr.line([(x, 0), (x, h)], fill=(150, 190, 255, 14), width=1)
    for y in range(0, h, step): dr.line([(0, y), (w, y)], fill=(150, 190, 255, 14), width=1)
    return Image.alpha_composite(im, ov)

def glow(im, cx, cy, r, col, alpha):
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (int(255 * alpha),))
    return Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(r * 0.55)))

def orbit(dr, cx, cy, a, b, tilt, col, width, steps=240):
    pts = []
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps
        x, y = a * math.cos(t), b * math.sin(t)
        pts.append((cx + x * math.cos(tilt) - y * math.sin(tilt), cy + x * math.sin(tilt) + y * math.cos(tilt)))
    dr.line(pts, fill=col, width=width, joint="curve")

def check(dr, cx, cy, s, col, width):
    dr.line([(cx - 0.55 * s, cy + 0.02 * s), (cx - 0.12 * s, cy + 0.45 * s), (cx + 0.62 * s, cy - 0.48 * s)], fill=col, width=width, joint="curve")
    for p in [(cx - 0.55 * s, cy + 0.02 * s), (cx - 0.12 * s, cy + 0.45 * s), (cx + 0.62 * s, cy - 0.48 * s)]:
        dr.ellipse([p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2], fill=col)

def lens_mark(im, cx, cy, R, handle=True):
    im = glow(im, cx, cy, R * 0.95, (255, 140, 40), 0.20)
    im = glow(im, cx, cy, R * 0.6, (255, 214, 10), 0.14)
    dr = ImageDraw.Draw(im)
    for tilt, a, b in [(0.5, 0.82, 0.30), (-0.5, 0.82, 0.30), (1.571, 0.82, 0.30)]:   # atom orbits inside the lens
        orbit(dr, cx, cy, R * a, R * b, tilt, ICE + (110,), max(2, int(R * 0.018)))
    check(dr, cx, cy, R * 0.52, YEL + (255,), int(R * 0.12))
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], outline=ORANGE + (255,), width=int(R * 0.14))
    dr.ellipse([cx - R * 0.9, cy - R * 0.9, cx + R * 0.9, cy + R * 0.9], outline=(255, 214, 10, 80), width=3)
    if handle:
        a = math.radians(45); x0, y0 = cx + (R + R * 0.05) * math.cos(a), cy + (R + R * 0.05) * math.sin(a)
        L = R * 0.42
        dr.line([x0, y0, x0 + L, y0 + L], fill=ORANGE + (255,), width=int(R * 0.18))
    return im


def bez(p0, p1, p2, p3, n=60):
    return [tuple((1-t)**3*np.array(p0)+3*(1-t)**2*t*np.array(p1)+3*(1-t)*t**2*np.array(p2)+t**3*np.array(p3)) for t in np.linspace(0, 1, n)]

def paths_mark(im, cx, cy, S):
    """one start dot, many possible paths, one bright orange path with an arrow = 'what could happen'"""
    sx, sy = cx - 0.46 * S, cy + 0.30 * S
    ends = [(cx + 0.46 * S, cy - 0.46 * S), (cx + 0.50 * S, cy - 0.20 * S), (cx + 0.50 * S, cy + 0.02 * S), (cx + 0.46 * S, cy + 0.26 * S), (cx + 0.36 * S, cy + 0.46 * S)]
    hi = 1
    ex, ey = ends[hi]
    im = glow(im, ex, ey, S * 0.26, (255, 140, 40), 0.30)
    im = glow(im, sx, sy, S * 0.16, (255, 214, 10), 0.35)
    dr = ImageDraw.Draw(im)
    for i, (x, y) in enumerate(ends):
        pts = bez((sx, sy), (sx + 0.38 * S, sy), (x - 0.34 * S, y), (x, y))
        if i == hi:
            continue
        dr.line(pts, fill=ICE + (130,), width=max(3, int(S * 0.016)), joint="curve")
        dr.ellipse([x - S * 0.022, y - S * 0.022, x + S * 0.022, y + S * 0.022], fill=ICE + (190,))
    pts = bez((sx, sy), (sx + 0.38 * S, sy), (ex - 0.34 * S, ey), (ex, ey))
    dr.line(pts, fill=ORANGE + (255,), width=int(S * 0.045), joint="curve")
    a = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0]); L = S * 0.13
    tip = (ex + S * 0.03 * math.cos(a), ey + S * 0.03 * math.sin(a))
    dr.polygon([tip, (tip[0] - L * math.cos(a - 0.5), tip[1] - L * math.sin(a - 0.5)), (tip[0] - L * math.cos(a + 0.5), tip[1] - L * math.sin(a + 0.5))], fill=ORANGE + (255,))
    dr.ellipse([sx - S * 0.05, sy - S * 0.05, sx + S * 0.05, sy + S * 0.05], fill=YEL + (255,), outline=(255, 255, 255, 255), width=3)
    return im

# ---------- logo 800x800 (circle-safe) ----------
S = 800
logo = bg(S, S, 3, (S / 2, S / 2))
logo = paths_mark(logo, 400, 400, 500)
logo.convert("RGB").save(OUT / "logo_800.png")

# ---------- banner 2048x1152; text inside the 1235x338 centre safe area ----------
W, H = 2048, 1152
bn = bg(W, H, 5, (W / 2, H / 2), stars=0.35)
dr = ImageDraw.Draw(bn)
# faint branching network across the banner (possibilities), drawn first so everything sits on top
rngn = np.random.default_rng(11)
_ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(_ov)
for k in range(7):
    y0 = 140 + k * 140; y1 = y0 + rngn.uniform(-260, 260)
    pts = bez((-20, y0), (W * 0.35, y0), (W * 0.55, y1), (W + 20, y1))
    dr.line(pts, fill=(150, 190, 255, 26), width=3, joint="curve")
    for i in (14, 30, 45):
        x, y = pts[i]; dr.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(150, 190, 255, 55))
bn = Image.alpha_composite(bn, _ov); dr = ImageDraw.Draw(bn)
# faint subject icons around the edges (outside the safe area): many fields of science, not only space
LC = (150, 190, 255, 150); OC = (255, 160, 70, 170); LW = 4
def flask(cx, cy, s):
    dr.line([(cx - .18*s, cy - .5*s), (cx - .18*s, cy - .1*s), (cx - .5*s, cy + .45*s), (cx + .5*s, cy + .45*s), (cx + .18*s, cy - .1*s), (cx + .18*s, cy - .5*s)], fill=LC, width=LW, joint="curve")
    dr.line([(cx - .26*s, cy - .5*s), (cx + .26*s, cy - .5*s)], fill=LC, width=LW)
    dr.polygon([(cx - .38*s, cy + .22*s), (cx + .38*s, cy + .22*s), (cx + .5*s, cy + .45*s), (cx - .5*s, cy + .45*s)], fill=OC)
    for bx, by, br in [(cx - .1*s, cy + .05*s, 5), (cx + .08*s, cy - .08*s, 4)]: dr.ellipse([bx-br, by-br, bx+br, by+br], outline=OC, width=3)
def gear(cx, cy, s):
    for i in range(8):
        t = i * math.pi / 4; x, y = cx + .5*s*math.cos(t), cy + .5*s*math.sin(t)
        dr.line([(cx + .38*s*math.cos(t), cy + .38*s*math.sin(t)), (x, y)], fill=LC, width=int(.2*s))
    dr.ellipse([cx - .42*s, cy - .42*s, cx + .42*s, cy + .42*s], outline=LC, width=LW)
    dr.ellipse([cx - .16*s, cy - .16*s, cx + .16*s, cy + .16*s], outline=OC, width=LW)
def globe(cx, cy, s):
    r = .5*s; dr.ellipse([cx-r, cy-r, cx+r, cy+r], outline=LC, width=LW)
    dr.ellipse([cx - r*.45, cy - r, cx + r*.45, cy + r], outline=LC, width=3)
    dr.line([(cx - r, cy), (cx + r, cy)], fill=LC, width=3); dr.arc([cx-r, cy-r*.5, cx+r, cy+r*.5], 0, 180, fill=OC, width=3)
def bolt(cx, cy, s):
    dr.polygon([(cx + .1*s, cy - .55*s), (cx - .3*s, cy + .05*s), (cx - .02*s, cy + .05*s), (cx - .12*s, cy + .55*s), (cx + .32*s, cy - .1*s), (cx + .04*s, cy - .1*s)], outline=OC, fill=None, width=LW)
def leaf(cx, cy, s):
    up = [(cx - .5*s + t*s, cy + .35*s - t*.7*s - .38*s*math.sin(math.pi*t)) for t in np.linspace(0, 1, 40)]
    lo = [(cx - .5*s + t*s, cy + .35*s - t*.7*s + .38*s*math.sin(math.pi*t)) for t in np.linspace(1, 0, 40)]
    dr.line(up + lo + [up[0]], fill=LC, width=LW, joint="curve")
    dr.line([(cx - .5*s, cy + .35*s), (cx + .5*s, cy - .35*s)], fill=OC, width=3)
    dr.line([(cx - .55*s, cy + .42*s), (cx - .5*s, cy + .35*s)], fill=OC, width=3)
def heart(cx, cy, s):
    pts = [(cx + .5*s*16*math.sin(t)**3/16, cy - .5*s*(13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t))/16) for t in np.linspace(0, 2*math.pi, 80)]
    dr.line(pts + [pts[0]], fill=OC, width=LW)
    dr.line([(cx - .55*s, cy + .05*s), (cx - .25*s, cy + .05*s), (cx - .1*s, cy - .2*s), (cx + .08*s, cy + .3*s), (cx + .2*s, cy + .05*s), (cx + .55*s, cy + .05*s)], fill=LC, width=3, joint="curve")
def atom(cx, cy, s):
    for t in (0.5, -0.5, 1.571): orbit(dr, cx, cy, .5*s, .19*s, t, LC, 3)
    dr.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 214, 10, 220))
def planet(cx, cy, s):
    dr.ellipse([cx - .32*s, cy - .32*s, cx + .32*s, cy + .32*s], outline=LC, width=LW); orbit(dr, cx, cy, .62*s, .16*s, -0.35, OC, 3)
for fn, cx, cy, sz in [(atom, 190, 260, 200), (flask, 520, 150, 150), (gear, 1450, 150, 150), (planet, 1850, 250, 190),
                       (globe, 190, 900, 170), (leaf, 500, 960, 150), (heart, 1500, 990, 160), (bolt, 1840, 900, 160)]:
    fn(cx, cy, sz)
for i in range(46):                                   # DNA helix, middle bottom strip
    x = 700 + i * 12; y1 = 990 + 38 * math.sin(i * 0.38); y2 = 990 - 38 * math.sin(i * 0.38)
    dr.ellipse([x - 3, y1 - 3, x + 3, y1 + 3], fill=(255, 140, 40, 150)); dr.ellipse([x - 3, y2 - 3, x + 3, y2 + 3], fill=(150, 190, 255, 150))
    if i % 3 == 0: dr.line([x, y1, x, y2], fill=(200, 215, 240, 60), width=2)
# lens mark left of the text, fully inside the safe area
bn = paths_mark(bn, 590, H // 2, 250)
dr = ImageDraw.Draw(bn)
f1 = ImageFont.truetype(FB, 96); f2 = ImageFont.truetype(FB, 50); f3 = ImageFont.truetype(FB, 52)
x1, y1 = 760, H // 2 - 95
dr.text((x1, y1), "POSSIBILITIES", font=f1, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=NAVY + (255,))
dr.text((x1 + 4, y1 + 122), "Kya ho sakta hai?", font=f3, fill=(255, 190, 120, 255), stroke_width=4, stroke_fill=NAVY + (255,))
bn.convert("RGB").save(OUT / "banner_2048x1152.png")
pv = bn.convert("RGB").copy(); d2 = ImageDraw.Draw(pv)
d2.rectangle([(W - 1235) / 2, (H - 338) / 2, (W + 1235) / 2, (H + 338) / 2], outline=(0, 255, 0), width=3)
pv.resize((1024, 576)).save(OUT / "banner_safe_preview.png")
print(OUT)
