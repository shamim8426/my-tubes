"""Reality Check - Asli: own animated EXPLAINER scenes for the Long (called by rc_real_look.render_real when a shot override has "scene").

footage_overrides.json:  "<line>": {"scene": {"type": "<name>", "sync": <master line>, ...params}}
  sync = line number where the continuous animation starts; T (master time) = shot-local t + (start of this line - start of the sync line),
  so one animation can run across several shots (lines) without a visible restart. Scene functions: SCENES[name](c, **params).
Look: dark space bg (B.draw_bg), amber accent, small overlay text only (Poppins Bold, Roman/Hinglish, plain digits). Everything moves every frame.
All frames are 1920x1080 BGR; finishing (grade, grain, vignette) is the same ffmpeg grade as the other real-look shots (RL.VF_GRADE).
"""
import hashlib
import inspect
import json
import math
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import rc_build_long as B

W, H, FPS = B.W, B.H, B.FPS
TK_VER = "e1"   # bump when a toolkit visual changes on purpose (scene functions are hashed by their own source)
SCENES = {}
ROOT = B.ROOT


def scene(f):
    SCENES[f.__name__] = f
    return f


def smooth(x):
    return B.ease(x)


def lin(x):
    return max(0.0, min(1.0, x))


def seg(T, a, b):
    """0..1 progress of T inside [a, b]."""
    return lin((T - a) / max(b - a, 1e-6))


def col(c):
    return B.C(c)


def lerp(a, b, k):
    return a + (b - a) * k


def lerp_t(a, b, k):
    return tuple(lerp(a[i], b[i], k) for i in range(len(a)))


# ------------------------------------------------------------------ text
_FONTS = {}
_TXT = {}


def font(px, weight="Bold"):
    k = (int(px), weight)
    if k not in _FONTS:
        _FONTS[k] = ImageFont.truetype(str(ROOT / f"shared/fonts/Poppins-{weight}.ttf"), int(px))
    return _FONTS[k]


def text_spr(s, px, c, weight="Bold"):
    k = (s, int(px), tuple(col(c)), weight)
    if k in _TXT:
        return _TXT[k]
    f = font(px, weight)
    lines = s.split("\n")
    wd = max(int(f.getlength(l)) for l in lines) + 12
    lh = int(px * 1.32)
    img = Image.new("RGBA", (wd, lh * len(lines) + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cc = col(c)
    rgb = (cc[2], cc[1], cc[0])
    for i, l in enumerate(lines):
        d.text((6, 4 + i * lh), l, font=f, fill=rgb + (255,), stroke_width=max(1, int(px / 22)), stroke_fill=(6, 8, 16, 255))
    arr = np.array(img)
    spr = np.dstack([arr[..., 2], arr[..., 1], arr[..., 0], arr[..., 3]])
    _TXT[k] = spr
    return spr


def put(im, spr, x0, y0, a=1.0):
    h, w = spr.shape[:2]
    X0, Y0 = int(x0), int(y0)
    sx0, sy0 = max(0, -X0), max(0, -Y0)
    X1, Y1 = min(W, X0 + w), min(H, Y0 + h)
    if X1 <= X0 + sx0 or Y1 <= Y0 + sy0 or a <= 0:
        return
    s = spr[sy0:sy0 + (Y1 - max(Y0, 0)), sx0:sx0 + (X1 - max(X0, 0))]
    roi = im[max(Y0, 0):Y1, max(X0, 0):X1]
    al = (s[..., 3:4].astype(np.float32) / 255.0) * a
    roi[:] = (roi * (1 - al) + s[..., :3].astype(np.float32) * al).astype(np.uint8)


def txt(im, s, x, y, px=40, c="ink", an="c", a=1.0, panel=True, pad=14, weight="Bold"):
    """Small overlay text with a dark rounded panel. an: c (centre), l (left x), r (right x)."""
    if a <= 0.01:
        return
    spr = text_spr(s, px, c, weight)
    h, w = spr.shape[:2]
    x0 = x - w / 2 if an == "c" else (x if an == "l" else x - w)
    y0 = y - h / 2
    if panel:
        B.rrect(im, x0 + 6 - pad, y0 + 6 - pad * 0.4, x0 + w - 6 + pad, y0 + h - 6 + pad * 0.4, 14, (10, 10, 18), 0.62 * a)
    put(im, spr, x0, y0, a)


def txtw(s, px, weight="Bold"):
    return font(px, weight).getlength(s.split("\n")[0]) + 12


# ------------------------------------------------------------------ sprites
_SPR = {}


def blit(im, spr, x, y, s=1.0, rot=0.0, a=1.0):
    """Blit BGRA sprite centred at (x, y), scale s, rotation rot (radians, clockwise on screen)."""
    h, w = spr.shape[:2]
    hd = 0.5 * math.hypot(w, h) * s + 2
    if x + hd < 0 or x - hd > W or y + hd < 0 or y - hd > H or a <= 0:
        return
    n = int(2 * hd)
    c, sn = math.cos(rot) * s, math.sin(rot) * s
    M = np.float32([[c, -sn, n / 2 - (c * w / 2 - sn * h / 2)], [sn, c, n / 2 - (sn * w / 2 + c * h / 2)]])
    patch = cv2.warpAffine(spr, M, (n, n), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    ox, oy = int(x - n / 2), int(y - n / 2)
    X0, Y0 = max(0, ox), max(0, oy)
    X1, Y1 = min(W, ox + n), min(H, oy + n)
    if X1 <= X0 or Y1 <= Y0:
        return
    p = patch[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]
    al = (p[..., 3:4].astype(np.float32) / 255.0) * a
    roi = im[Y0:Y1, X0:X1]
    roi[:] = (roi * (1 - al) + p[..., :3].astype(np.float32) * al).astype(np.uint8)


def _noise(sz, rng, octaves=((4, 1.0), (9, 0.5), (20, 0.25), (45, 0.12))):
    out = np.zeros((sz, sz), np.float32)
    for g, amp in octaves:
        out += cv2.resize(rng.random((g, g)).astype(np.float32), (sz, sz), interpolation=cv2.INTER_CUBIC) * amp
    out -= out.min()
    return out / out.max()


def rock_spr(seed=1, size=460, tone=1.0, elong=(1.0, 1.0), warm=0.0, craters=9):
    """Lumpy asteroid, BGRA, lit from the upper left."""
    k = ("rock", seed, size, tone, elong, warm, craters)
    if k in _SPR:
        return _SPR[k]
    rng = np.random.default_rng(seed)
    m = size
    th = np.linspace(0, 2 * np.pi, 160, endpoint=False)
    r = np.ones_like(th)
    for kk, amp in ((2, 0.07), (3, 0.06), (4, 0.045), (5, 0.03), (7, 0.018)):
        r += amp * np.cos(kk * th + rng.uniform(0, 6.28))
    r = r / r.max() * 0.46
    pts = np.stack([m / 2 + r * np.cos(th) * m * elong[0], m / 2 + r * np.sin(th) * m * elong[1]], 1)
    mask = np.zeros((m, m), np.uint8)
    cv2.fillPoly(mask, [(pts * 16).astype(np.int32)], 255, cv2.LINE_AA, 4)
    dt = cv2.distanceTransform((mask > 128).astype(np.uint8), cv2.DIST_L2, 5)
    dt = dt / max(dt.max(), 1)
    hgt = np.sqrt(np.clip(dt * 1.15, 0, 1)) * 0.9 + (_noise(m, rng) - 0.5) * 0.28 * np.clip(dt * 3, 0, 1)
    for _ in range(craters):
        cx, cy, cr = rng.uniform(0.25, 0.75) * m, rng.uniform(0.25, 0.75) * m, rng.uniform(0.04, 0.11) * m
        yy, xx = np.ogrid[:m, :m]
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / cr
        hgt -= 0.16 * np.exp(-(d ** 2) * 1.6) * (dt > 0.12)
        hgt += 0.07 * np.exp(-((d - 1.05) ** 2) * 14) * (dt > 0.12)
    hgt = cv2.GaussianBlur(hgt, (0, 0), 1.5)
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3) * 6
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3) * 6
    L = np.array([-0.55, -0.6, 0.58])
    L /= np.linalg.norm(L)
    nz = 1.0 / np.sqrt(gx * gx + gy * gy + 1)
    lum = np.clip((-gx * nz * L[0]) + (-gy * nz * L[1]) + nz * L[2], 0, 1)
    lum = 0.16 + 0.86 * lum
    grain = (_noise(m, rng, ((60, 1.0), (120, 0.6))) - 0.5) * 0.25
    lum = np.clip((lum + grain) * tone, 0, 1.2)
    base = np.array([138 - 12 * warm, 148 - 4 * warm, 158 + 4 * warm], np.float32)   # BGR, warm grey
    bgr = np.clip(lum[..., None] * base[None, None, :] * 1.1, 0, 255).astype(np.uint8)
    alpha = cv2.GaussianBlur(mask, (0, 0), 0.8)
    spr = np.dstack([bgr, alpha])
    _SPR[k] = spr
    return spr


def craft_spr(size=420):
    k = ("craft", size)
    if k in _SPR:
        return _SPR[k]
    s = size
    im = np.zeros((s, s, 4), np.uint8)
    cx, cy = s // 2, s // 2
    def poly(pts, c):
        cv2.fillPoly(im, [np.array(pts, np.int32) * 4], c + (255,), cv2.LINE_AA, 2)
    def P(a):
        return [(int(x * s / 420), int(y * s / 420)) for x, y in a]
    # solar panels (up and down), blue-black with grid
    for sgn in (-1, 1):
        y0, y1 = (cy - 20, cy - 190) if sgn < 0 else (cy + 20, cy + 190)
        cv2.rectangle(im, (cx - 62, min(y0, y1)), (cx + 62, max(y0, y1)), (74, 52, 26, 255), -1, cv2.LINE_AA)
        for gx in range(cx - 62, cx + 63, 21):
            cv2.line(im, (gx, min(y0, y1)), (gx, max(y0, y1)), (140, 120, 80, 255), 1, cv2.LINE_AA)
        for gy in range(min(y0, y1), max(y0, y1) + 1, 22):
            cv2.line(im, (cx - 62, gy), (cx + 62, gy), (140, 120, 80, 255), 1, cv2.LINE_AA)
        cv2.rectangle(im, (cx - 62, min(y0, y1)), (cx + 62, max(y0, y1)), (190, 170, 130, 255), 2, cv2.LINE_AA)
    cv2.rectangle(im, (cx - 52, cy - 40), (cx + 52, cy + 40), (40, 150, 215, 255), -1, cv2.LINE_AA)
    cv2.rectangle(im, (cx - 52, cy - 40), (cx + 52, cy + 40), (90, 205, 250, 255), 3, cv2.LINE_AA)
    cv2.circle(im, (cx + 8, cy), 22, (225, 230, 235, 255), -1, cv2.LINE_AA)
    cv2.circle(im, (cx + 8, cy), 22, (140, 150, 160, 255), 3, cv2.LINE_AA)
    cv2.rectangle(im, (cx - 70, cy - 12), (cx - 52, cy + 12), (120, 120, 130, 255), -1, cv2.LINE_AA)
    _SPR[k] = im
    return im


def _earth_tex():
    if "earth" in _SPR:
        return _SPR["earth"]
    rng = np.random.default_rng(3)
    sz = 512
    land = _noise(sz, rng, ((3, 1.0), (7, 0.6), (16, 0.3), (40, 0.15)))
    tex = np.zeros((sz, sz * 2, 3), np.uint8)
    land2 = cv2.resize(land, (sz * 2, sz))
    ocean = np.array([120, 70, 22], np.float32)
    grass = np.array([70, 120, 80], np.float32)
    desert = np.array([100, 150, 175], np.float32)
    mland = (land2 > 0.55).astype(np.float32)[..., None]
    mdes = ((land2 > 0.68)).astype(np.float32)[..., None]
    tex = ocean * (1 - mland) + (grass * (1 - mdes) + desert * mdes) * mland
    cl = cv2.resize(_noise(sz, rng, ((5, 1.0), (12, 0.6), (30, 0.3))), (sz * 2, sz))
    cl = np.clip((cl - 0.52) * 4, 0, 1)[..., None]
    tex = tex * (1 - cl * 0.8) + 245 * cl * 0.8
    _SPR["earth"] = tex.astype(np.uint8)
    return _SPR["earth"]


def earth(im, x, y, r, rot=0.0, a=1.0, glow_a=0.5):
    r = int(r)
    k = ("emap", r)
    if k not in _SPR:
        yy, xx = np.mgrid[-r:r, -r:r].astype(np.float32)
        d2 = (xx * xx + yy * yy) / (r * r)
        z = np.sqrt(np.clip(1 - d2, 0, 1))
        lat = np.arcsin(np.clip(yy / r, -1, 1))
        lon = np.arctan2(xx / r, z)
        shade = np.clip(0.18 + 1.0 * (-0.55 * xx / r - 0.25 * yy / r + 0.8 * z), 0, 1.1)
        _SPR[k] = (lat, lon, d2 < 1, shade[..., None], d2)
    lat, lon, inside, shade, d2 = _SPR[k]
    tex = _earth_tex()
    th, tw_ = tex.shape[:2]
    mx = (((lon + rot) / (2 * np.pi)) % 1.0 * tw_).astype(np.float32)
    my = ((lat / np.pi + 0.5) * th).astype(np.float32)
    samp = cv2.remap(tex, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP).astype(np.float32)
    rim = np.clip(d2, 0, 1) ** 4 * 0.5
    samp = samp * shade + np.array([255, 190, 110], np.float32) * rim[..., None] * 0.5
    B.glow(im, x, y, r * 1.35, (255, 170, 80), glow_a * 0.55 * a)
    X0, Y0 = int(x - r), int(y - r)
    ys0, xs0 = max(0, -Y0), max(0, -X0)
    ye, xe = min(2 * r, H - Y0), min(2 * r, W - X0)
    if ye <= ys0 or xe <= xs0:
        return
    roi = im[Y0 + ys0:Y0 + ye, X0 + xs0:X0 + xe]
    m = inside[ys0:ye, xs0:xe, None].astype(np.float32) * a
    roi[:] = (roi * (1 - m) + np.clip(samp[ys0:ye, xs0:xe], 0, 255) * m).astype(np.uint8)


def sun(im, x, y, r, t=0.0, a=1.0):
    B.glow(im, x, y, r * 5 * (1 + 0.03 * math.sin(t * 1.3)), (60, 170, 255), 0.55 * a)
    B.glow(im, x, y, r * 2.2, (150, 220, 255), 0.7 * a)
    B.circ(im, x, y, r, (205, 245, 255), -1)


# ------------------------------------------------------------------ drawing helpers
def arrow(im, x0, y0, x1, y1, c="amber", th=6, a=1.0, head=26, prog=1.0):
    if prog <= 0 or a <= 0:
        return
    x1p, y1p = x0 + (x1 - x0) * prog, y0 + (y1 - y0) * prog
    cc = B.mix(c, a)
    B.line(im, x0, y0, x1p, y1p, cc, th)
    if prog > 0.15:
        ang = math.atan2(y1p - y0, x1p - x0)
        for s_ in (-0.5, 0.5):
            B.line(im, x1p, y1p, x1p - head * math.cos(ang + s_), y1p - head * math.sin(ang + s_), cc, th)


def dotted(im, pts, c="dim", th=3, a=1.0, dash=16, gap=14, prog=1.0):
    """Dotted polyline, drawn up to fraction prog of its length."""
    cc = B.mix(c, a)
    tot = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
    lim = tot * prog
    acc = 0.0
    for i in range(len(pts) - 1):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        L = math.hypot(xb - xa, yb - ya)
        if L < 1e-6:
            continue
        ux, uy = (xb - xa) / L, (yb - ya) / L
        d = 0.0
        while d < L:
            s0, s1 = acc + d, acc + min(d + dash, L)
            if s0 >= lim:
                return
            s1 = min(s1, lim)
            B.line(im, xa + ux * (s0 - acc), ya + uy * (s0 - acc), xa + ux * (s1 - acc), ya + uy * (s1 - acc), cc, th)
            d += dash + gap
        acc += L


def ring(im, x, y, r, c="dim", th=3, a=1.0, dash=0):
    if dash:
        n = int(2 * math.pi * r / (dash * 2))
        for k in range(max(n, 8)):
            B.ell(im, x, y, r, r, B.mix(c, a), th, 0, k * 360 / n, k * 360 / n + 180 / n)
    else:
        B.circ(im, x, y, r, B.mix(c, a), th)


def flash(im, x, y, k, r=300, a=1.0):
    """k: 0..1 age of a flash burst (white core, expanding ring)."""
    if k < 0 or k > 1:
        return
    f = 1 - k
    B.glow(im, x, y, r * (0.5 + 0.8 * k), (230, 245, 255), min(1.0, 1.4 * f) * a)
    B.glow(im, x, y, r * (0.9 + 1.2 * k), (60, 160, 255), 0.7 * f * a)
    B.circ(im, x, y, r * 0.25 + r * 1.1 * smooth(k), B.mix((200, 230, 255), 0.9 * f * a), max(2, int(8 * f)))


def whiten(im, k):
    if k > 0:
        cv2.addWeighted(im, 1 - k, np.full_like(im, 255), k, 0, dst=im)


def particles(im, ox, oy, T, n=60, seed=1, v=(200, 500), ang=(0, 6.28), size=(2, 6), drag=1.2, life=2.5, c=(170, 180, 190), gravity=0.0, a=1.0, glowc=None):
    """Deterministic debris burst starting at T=0."""
    if T <= 0:
        return
    rng = np.random.default_rng(seed)
    vs = rng.uniform(v[0], v[1], n)
    an = rng.uniform(ang[0], ang[1], n)
    sz = rng.uniform(size[0], size[1], n)
    lf = rng.uniform(0.5, 1.0, n) * life
    for i in range(n):
        if T > lf[i]:
            continue
        k = (1 - math.exp(-drag * T)) / drag
        px = ox + math.cos(an[i]) * vs[i] * k
        py = oy + math.sin(an[i]) * vs[i] * k + gravity * T * T
        al = (1 - (T / lf[i]) ** 2) * a
        if glowc is not None and T < 0.6:
            B.glow(im, px, py, sz[i] * 5, glowc, 0.5 * al)
        B.circ(im, px, py, sz[i], B.mix(c, 0.3 + 0.7 * al), -1)


def stars_bg(c, tint=None):
    B.draw_bg(c.im, c.t + c.boff, c.seed, tint)


def dial(im, cx, cy, r, minutes, c="amber", a=1.0, label=None, hand=True, ticks=True, lab_px=34, full=60.0):
    """Clock face with `minutes` (of `full`) filled as a coloured wedge from 12 o'clock + a hand."""
    B.circ(im, cx, cy, r, B.mix((30, 36, 60), a), -1)
    ov = im.copy()
    frac = max(minutes, 0) / full
    if frac > 0:
        cv2.ellipse(ov, (int(cx), int(cy)), (int(r - 6), int(r - 6)), -90, 0, 360 * min(frac, 1.0), col(c), -1, cv2.LINE_AA)
    cv2.addWeighted(ov, 0.55 * a, im, 1 - 0.55 * a, 0, dst=im)
    B.circ(im, cx, cy, r, B.mix((200, 210, 240), a * 0.9), 4)
    if ticks:
        for k in range(60):
            ang = math.radians(k * 6 - 90)
            r0 = r - (22 if k % 5 == 0 else 11)
            B.line(im, cx + r0 * math.cos(ang), cy + r0 * math.sin(ang), cx + (r - 4) * math.cos(ang), cy + (r - 4) * math.sin(ang),
                   B.mix((220, 226, 245), a * (0.95 if k % 5 == 0 else 0.5)), 3 if k % 5 == 0 else 1)
    if hand:
        ang = math.radians(360 * frac - 90)
        B.line(im, cx, cy, cx + (r - 14) * math.cos(ang), cy + (r - 14) * math.sin(ang), B.mix("white", a), 6)
        B.circ(im, cx, cy, 11, B.mix("white", a), -1)


# ------------------------------------------------------------------ context + render
class Ctx:
    pass


def load_starts(ld):
    f = ld.parent / "audio/voiceover_timing.json"
    lines = json.loads(f.read_text(encoding="utf-8"))
    st = {l["line"]: l["start"] for l in lines}
    st[lines[0]["line"]] = 0.0
    return st, {l["line"]: l for l in lines}


def K(c, line, frac=0.0, off=0.0):
    """Master-scene time (T) at which `line` starts (+ frac of its spoken length + off s)."""
    s0 = c.st[line]
    e0 = c.en.get(line, s0)
    return s0 + frac * (e0 - s0) + off - c.st[c.sync]


_REAL = {}


def real(c, rel, tin=0.0, z0=1.0, z1=1.06, crop=None, dark=0.0, speed=1.0, fx=0.5, fy=0.5, loop=True):
    """Fill c.im with real footage/still (path under long/), slow push z0->z1 over the shot, optional darkening."""
    key = str(rel)
    if key not in _REAL:
        _REAL[key] = B.Footage(c.ld / rel)
    f = _REAL[key]
    if f.is_img:
        fr = f.img
    else:
        cd = f.nfr / f.fps
        tt = tin + c.t * speed
        if loop:
            tt = tin + ((c.t * speed) % max(cd - tin - 0.1, 0.5))
        fr = f.raw(min(tt, cd - 0.1))
    if crop:
        h, w = fr.shape[:2]
        fr = fr[int(crop[1] * h):int(crop[3] * h), int(crop[0] * w):int(crop[2] * w)]
    z = z0 + (z1 - z0) * lin(c.t / max(c.dur, 0.5))
    h, w = fr.shape[:2]
    sc = max(W / w, H / h) * z
    M = np.float32([[sc, 0, W / 2 - fx * w * sc], [0, sc, H / 2 - fy * h * sc]])
    out = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_AREA if sc < 1 else cv2.INTER_LINEAR)
    if dark > 0:
        out = cv2.convertScaleAbs(out, alpha=1 - dark)
    c.im[:] = out


def bar(im, x, y, w, h, frac, c="amber", a=1.0, back=(40, 48, 78)):
    B.rrect(im, x, y, x + w, y + h, h / 2, back, 0.8 * a)
    if frac > 0.002:
        B.rrect(im, x, y, x + max(h, w * min(frac, 1.0)), y + h, h / 2, B.C(c), a)


def view_seq(c, base, views):
    """views: [(t_from, t_to, fn(v))]: hard cut with a 0.12 s blend; fn draws onto a copy of base."""
    T = c.T
    for i, (a, b, fn) in enumerate(views):
        k_in = lin((T - a) / 0.12) if i > 0 else 1.0
        if T < a - 0.001 or T >= b:
            continue
        v = base.copy()
        fn(v)
        if k_in >= 0.999:
            c.im[:] = v
        else:
            cv2.addWeighted(c.im, 1 - k_in, v, k_in, 0, dst=c.im)
        return
    # past the last view: hold last
    a, b, fn = views[-1]
    v = base.copy()
    fn(v)
    c.im[:] = v


def scene_sig(sc):
    f = SCENES.get(sc["type"])
    src = inspect.getsource(f) if f else ""
    return hashlib.sha1((TK_VER + json.dumps(sc, sort_keys=True) + src).encode()).hexdigest()[:8]


def _prep_mix(mix, ld, dur):
    """Real-footage cuts inside a scene shot. Each cut: a, b (seconds in the shot, b null = to end), mode real|under, file (rel to long/),
    tin/tout (video window), crop, credit, cap (small caption), dim (under only), speed, z0, z1."""
    import rc_real_look as RL
    out = []
    for k, m in enumerate(mix or []):
        m = dict(m)
        m["a"] = float(m.get("a", 0))
        m["b"] = dur + 1 if m.get("b") is None else float(m["b"])
        path = Path(ld) / m["file"]
        d = max(min(m["b"], dur) - m["a"], 0.1)
        if path.suffix.lower() in (".mp4", ".mov", ".webm"):
            tin = float(m.get("tin", 0))
            tout = float(m.get("tout", tin + d))
            m["src"] = RL.VidSrc(path, tin, tout, float(m.get("speed", 1.0)), float(m.get("z0", 1.0)), float(m.get("z1", 1.06)), 0.0, d, m.get("crop"), True)
        else:
            m["src"] = RL.StillSrc(RL.cropped_still(path, m.get("crop"), ld), int(m.get("k", k)), d)
        out.append(m)
    return out


def _mix_real(m, t, dim=1.0):
    import rc_real_look as RL
    fr = m["src"].get(t - m["a"])
    if dim < 1.0:
        fr = RL.soft(fr)
        fr = cv2.convertScaleAbs(fr, alpha=dim / 0.66)
    return fr


def _mix_chip(im, m, t):
    tt = t - m["a"]
    a = lin(tt / 0.3) * lin((m["b"] - t) / 0.3 if m["b"] < 900 else 1.0)
    if m.get("credit"):
        txt(im, m["credit"], 84, 1048, px=24, c=(235, 235, 235), an="l", a=min(a, lin((4.2 - tt) / 0.4)) if tt > 3.5 else a)
    if m.get("cap"):
        txt(im, m["cap"], 960, 960, px=36, c="amber", an="c", a=a)


def render(n, nfr, out, sc, ld_s, vf_grade):
    out = Path(out)
    t_start = time.time()
    ld = Path(ld_s)
    starts, _ = load_starts(ld)
    c = Ctx()
    c.n, c.dur, c.seed = n, nfr / FPS, n
    c.boff = starts.get(n, 0.0) - starts.get(sc.get("sync", n), starts.get(n, 0.0))
    c.st = starts
    c.en = {k: v["end"] for k, v in _.items()}
    c.sync = sc.get("sync", n)
    c.ld = ld
    c.im = np.empty((H, W, 3), np.uint8)
    c.p = {k: v for k, v in sc.items() if k not in ("type", "sync", "mix", "punch")}
    f = SCENES[sc["type"]]
    mix = _prep_mix(sc.get("mix"), ld, c.dur)
    _real_bg = {"on": False}
    _orig_bg = B.draw_bg
    if any(m["mode"] == "under" for m in mix):
        def _bg(im, t, seed, tint):
            if _real_bg["on"]:
                im[:] = 0
            else:
                _orig_bg(im, t, seed, tint)
        B.draw_bg = _bg
    tmp = out.with_name(out.stem + ".part.mp4")
    ff = B.find_ff()
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", vf_grade, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-g", "30", "-r", str(FPS), "-an", str(tmp)],
                         stdin=subprocess.PIPE, cwd=str(out.parent))
    for fr in range(nfr):
        c.t = fr / FPS
        c.T = c.t + c.boff
        c.f = fr
        cut = next((m for m in mix if m["a"] <= c.t < m["b"]), None)
        if cut is not None and cut["mode"] == "real":
            c.im[:] = _mix_real(cut, c.t)
        elif cut is not None:
            _real_bg["on"] = True
            try:
                f(c, **c.p)
            finally:
                _real_bg["on"] = False
            real = _mix_real(cut, c.t, dim=cut.get("dim", 0.55))
            m = np.clip(c.im.max(axis=2, keepdims=True).astype(np.float32) / 40.0, 0, 1)
            c.im[:] = np.clip(real.astype(np.float32) * (1 - m) + c.im.astype(np.float32), 0, 255).astype(np.uint8)
            _mix_chip(c.im, cut, c.t)
        else:
            f(c, **c.p)
            if sc.get("punch"):   # slow camera push on long drawn shots (hold > 8 s)
                z = 1.0 + sc["punch"] * smooth(c.t / max(c.dur, 1.0))
                M = np.float32([[z, 0, W / 2 * (1 - z)], [0, z, H / 2 * (1 - z)]])
                c.im[:] = cv2.warpAffine(c.im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        if cut is not None and cut["mode"] == "real":
            _mix_chip(c.im, cut, c.t)
        # soft fade-in on the first 4 frames (hides the hard cut between unrelated scenes)
        if sc.get("fadein", False) and fr < 4:
            cv2.addWeighted(c.im, (fr + 1) / 5.0, np.zeros_like(c.im), 1 - (fr + 1) / 5.0, 0, dst=c.im)
        if sc.get("flash") and fr < 7:   # warm flash at block boundaries (5-7 frames)
            k_ = 0.55 * (1 - fr / 7.0)
            cv2.addWeighted(c.im, 1 - k_, np.full_like(c.im, (80, 170, 255)), k_, 0, dst=c.im)
        p.stdin.write(c.im.tobytes())
    p.stdin.close()
    B.draw_bg = _orig_bg
    if p.wait():
        return n, 0.0, "ffmpeg failed"
    tmp.replace(out)
    return n, time.time() - t_start, "ok"


import rc_explain_scenes  # noqa: E402,F401  (registers the scenes)
import rc_explain_a  # noqa: E402,F401
for _m in ("rc_explain_b", "rc_explain_c", "rc_explain_d", "rc_explain_e"):
    try:
        __import__(_m)
    except ModuleNotFoundError as _e:
        if _e.name != _m:
            raise
