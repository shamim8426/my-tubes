"""Reality Check - Asli: Long builder (16:9, 1920x1080, 30 fps), all own graphics (cv2 + numpy, text via ffmpeg/libass).

    python tools/rc_build_long.py 001 [--seconds 60] [--shots 5,12] [--workers 10] [--final-name NAME] [--no-music] [--tail 20]

Reads  stories/<NNN>_*/long/shot_specs.json  (one spec per shot = per voiceover line, from the script CUT cues; see
       long/_gen_shot_specs.py) and audio/voiceover_timing.json (else voiceover_draft_timing.json).
Writes cache/reality-check/<NNN>/shot_<n>_<hash>.mp4 (only changed shots are re-rendered), then concatenates, muxes
       audio/voiceover_full.wav (else voiceover_draft_mixed.wav) + a quiet music bed (shared/music/mystery_bed.wav, own, no credit)
       into long/output/<NNN>_long_preview.mp4.
Look: navy-black bg (7,11,24), amber accent, red = ANJAAN (unknown), green/teal = status. ON-SCREEN TEXT IS ROMAN/HINGLISH, plain digits
(Pillow has no raqm and libass mis-shapes Devanagari). Every shot keeps moving (star drift, motes, slow text zoom, animated graphic).
NASA media shots: put long/footage/<shot>.mp4|jpg (shot = 001, 1, shot_001) and it is used with the credit label; else a placeholder card.
"""
import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H, FPS = 1920, 1080, 30
VERSION = "v3"


def find_ff(name="ffmpeg"):
    for c in (ROOT / f"tools/ffmpeg/{name}.exe", Path(f"D:/my-tubes/tools/ffmpeg/{name}.exe")):
        if c.exists():
            return str(c)
    return name


def rgb(r, g, b):
    return (b, g, r)


COL = dict(amber=rgb(255, 176, 32), red=rgb(255, 82, 82), green=rgb(60, 200, 140), blue=rgb(90, 170, 255), teal=rgb(50, 190, 190),
           ink=rgb(232, 238, 250), dim=rgb(120, 136, 172), grey=rgb(150, 156, 170), white=rgb(255, 255, 255), orange=rgb(255, 130, 40),
           dark=rgb(60, 70, 96), gold=rgb(255, 214, 10), brown=rgb(150, 100, 60), forest=rgb(40, 120, 70))
BGC = rgb(7, 11, 24)


def C(x):
    return COL[x] if isinstance(x, str) else tuple(x)


def mix(c, a):
    c = C(c)
    return tuple(int(c[i] * a + BGC[i] * (1 - a)) for i in range(3))


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


# ---------------------------------------------------------------- fonts / text measuring
FONT_FILE = {"M": "Mukta-Bold.ttf", "N": "Poppins-Bold.ttf"}
FONT_NAME = {"M": "Mukta", "N": "Poppins"}
_F, _RATIO = {}, {}


def fnt(font, px):
    k = (font, int(px))
    if k not in _F:
        _F[k] = ImageFont.truetype(str(ROOT / "shared/fonts" / FONT_FILE[font]), int(px))
    return _F[k]


def ratio(font):
    if font not in _RATIO:
        a, d = ImageFont.truetype(str(ROOT / "shared/fonts" / FONT_FILE[font]), 1000).getmetrics()
        _RATIO[font] = (a + d) / 1000.0
    return _RATIO[font]


def tw(text, font, px):
    return max(fnt(font, px).getlength(l) for l in text.split("\n")) * 1.04


# ---------------------------------------------------------------- cv2 helpers (subpixel AA)
def circ(im, x, y, r, c, th=-1):
    cv2.circle(im, (int(x * 16), int(y * 16)), int(max(r, 0.2) * 16), C(c), th, cv2.LINE_AA, 4)


def line(im, x0, y0, x1, y1, c, th=2):
    cv2.line(im, (int(x0 * 16), int(y0 * 16)), (int(x1 * 16), int(y1 * 16)), C(c), th, cv2.LINE_AA, 4)


def polyl(im, pts, c, th=2, closed=False):
    p = np.array([[int(x * 16), int(y * 16)] for x, y in pts], np.int32)
    cv2.polylines(im, [p], closed, C(c), th, cv2.LINE_AA, 4)


def polyf(im, pts, c):
    p = np.array([[int(x * 16), int(y * 16)] for x, y in pts], np.int32)
    cv2.fillPoly(im, [p], C(c), cv2.LINE_AA, 4)


def ell(im, x, y, a, b, c, th=2, ang=0, a0=0, a1=360):
    cv2.ellipse(im, (int(x * 16), int(y * 16)), (int(max(a, 0.2) * 16), int(max(b, 0.2) * 16)), ang, a0, a1, C(c), th, cv2.LINE_AA, 4)


def rect_alpha(im, x0, y0, x1, y1, c, a):
    x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(W, int(x1)), min(H, int(y1))
    if x1 <= x0 or y1 <= y0 or a <= 0:
        return
    roi = im[y0:y1, x0:x1]
    roi[:] = (roi * (1 - a) + np.array(C(c), np.float32) * a).astype(np.uint8)


def rrect(im, x0, y0, x1, y1, r, c, a=1.0, fill=True, th=2):
    """Rounded rect, alpha-blended inside its own ROI (cheap)."""
    X0, Y0, X1, Y1 = max(0, int(x0 - 3)), max(0, int(y0 - 3)), min(W, int(x1 + 3)), min(H, int(y1 + 3))
    if X1 <= X0 or Y1 <= Y0 or a <= 0:
        return
    m = np.zeros((Y1 - Y0, X1 - X0), np.uint8)
    ox, oy = X0, Y0
    r = int(min(r, (y1 - y0) / 2, (x1 - x0) / 2))
    pts = []
    for cx, cy, a0 in ((x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90)):
        for k in range(0, 91, 9):
            ang = math.radians(a0 + k)
            pts.append([(cx + r * math.cos(ang) - ox) * 16, (cy + r * math.sin(ang) - oy) * 16])
    p = np.array(pts, np.int32)
    if fill:
        cv2.fillPoly(m, [p], 255, cv2.LINE_AA, 4)
    else:
        cv2.polylines(m, [p], True, 255, th, cv2.LINE_AA, 4)
    roi = im[Y0:Y1, X0:X1]
    al = (m.astype(np.float32) / 255.0 * a)[..., None]
    roi[:] = (roi * (1 - al) + np.array(C(c), np.float32) * al).astype(np.uint8)


_GLOW = {}


def glow(im, x, y, r, c, a=1.0):
    r = int(r)
    if r < 2 or a <= 0:
        return
    if r not in _GLOW:
        yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
        d = np.sqrt(xx * xx + yy * yy) / r
        _GLOW[r] = np.clip(1 - d, 0, 1) ** 2.2
    g = _GLOW[r]
    x, y = int(x), int(y)
    x0, y0, x1, y1 = max(0, x - r), max(0, y - r), min(W, x + r + 1), min(H, y + r + 1)
    if x1 <= x0 or y1 <= y0:
        return
    gg = g[y0 - (y - r):y1 - (y - r), x0 - (x - r):x1 - (x - r)][..., None]
    roi = im[y0:y1, x0:x1].astype(np.float32)
    roi += gg * np.array(C(c), np.float32) * a
    im[y0:y1, x0:x1] = np.clip(roi, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- background
_BG = {}


def bg_layers():
    if "L1" in _BG:
        return _BG
    r = np.random.default_rng(11)
    L1 = np.zeros((H + 260, W + 460, 3), np.uint8)
    L2 = np.zeros_like(L1)
    for n, L, amp in ((520, L1, 1.0), (320, L2, 0.55)):
        xs, ys = r.uniform(0, L.shape[1], n), r.uniform(0, L.shape[0], n)
        for x, y in zip(xs, ys):
            rr = r.uniform(0.7, 1.9)
            b = r.uniform(80, 230) * amp
            cv2.circle(L, (int(x * 16), int(y * 16)), int(rr * 16), (b * 1.0, b * 0.93, b * 0.82), -1, cv2.LINE_AA, 4)
    yy = np.linspace(0, 1, L1.shape[0])[:, None, None]
    base = np.zeros_like(L1, np.float32)
    base[:] = np.array(BGC, np.float32)
    base += yy * np.array([8, 4, 0], np.float32)
    L1 = cv2.add(L1, base.astype(np.uint8))
    _BG["L1"], _BG["L2"] = L1, L2
    mr = np.random.default_rng(5)
    _BG["motes"] = [(mr.uniform(0, W), mr.uniform(0, H), mr.uniform(1.2, 3.2), mr.uniform(0, 6.28), mr.uniform(8, 26)) for _ in range(34)]
    return _BG


def draw_bg(im, t, seed, tint):
    B = bg_layers()
    sx, sy = (1 if seed % 2 else -1), (1 if (seed // 2) % 2 else -1)
    def pp(v, rng):  # ping-pong inside 0..rng
        v = v % (2 * rng)
        return int(v if v <= rng else 2 * rng - v)
    o1x, o1y = pp(230 + sx * t * 7, 460), pp(130 + sy * t * 3, 260)
    o2x, o2y = pp(230 + sx * t * 15, 460), pp(130 + sy * t * 6, 260)
    a = B["L1"][o1y:o1y + H, o1x:o1x + W]
    b = B["L2"][o2y:o2y + H, o2x:o2x + W]
    cv2.add(a, b, dst=im)
    if tint:
        glow(im, 960 + tint.get("dx", 0), 540, tint.get("r", 900), tint["c"], tint.get("a", 0.16))
    for x, y, r, ph, sp in B["motes"]:
        px = (x + t * sp * 0.6) % W
        py = (y - t * sp * 0.35 + 10 * math.sin(t * 0.7 + ph)) % H
        al = 0.35 + 0.25 * math.sin(t * 1.1 + ph)
        circ(im, px, py, r, mix("amber", al * 0.6), -1)


# ---------------------------------------------------------------- footage
def find_footage(story_dir, n, fname=None):
    d = story_dir / "long/footage"
    if fname and (d / fname).exists():
        return d / fname
    for stem in (f"{n:03d}", f"{n}", f"shot_{n:03d}"):
        for ext in (".mp4", ".mov", ".webm", ".jpg", ".jpeg", ".png"):
            p = d / (stem + ext)
            if p.exists():
                return p
    return None


class Footage:
    def __init__(self, path):
        self.path = path
        self.is_img = path.suffix.lower() in (".jpg", ".jpeg", ".png")
        if self.is_img:
            self.img = cv2.imread(str(path))
        else:
            self.cap = cv2.VideoCapture(str(path))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            self.nfr = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
            self.pos = -1
            self.last = None

    def raw(self, t):
        if self.is_img:
            return self.img
        idx = int(t * self.fps) % self.nfr
        if idx == self.pos and self.last is not None:
            return self.last
        if idx != self.pos + 1:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, fr = self.cap.read()
        if not ok:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, fr = self.cap.read()
        self.pos = idx
        self.last = fr if ok else self.last
        return self.last


def place_footage(img, mode, z, h_target, cx, cy):
    h, w = img.shape[:2]
    if mode == "contain":
        sc = h_target / h * z
        cxx, cyy = cx, cy
    else:
        sc = max(W / w, H / h) * z
        cxx, cyy = W / 2, H / 2
    M = np.float32([[sc, 0, cxx - w * sc / 2], [0, sc, cyy - h * sc / 2]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_AREA if sc < 1 else cv2.INTER_LINEAR)


# ---------------------------------------------------------------- elements (graphics). coords: x,y absolute px
def e_ring(im, t, dur, x, y, r, o):
    a = ease((t - o.get("at", 0)) / 0.8)
    if o.get("dash"):
        n = 48
        for k in range(n):
            if k % 2 == 0:
                ell(im, x, y, r, r, mix(o.get("c", "dim"), a), o.get("th", 2), 0, k * 360 / n, (k + 1) * 360 / n)
    else:
        circ(im, x, y, r, mix(o.get("c", "dim"), a), o.get("th", 2))


def e_rock(im, t, dur, x, y, r, o):
    at = o.get("at", 0)
    a = ease((t - at) / 0.7) * o.get("a", 1.0)
    if "fade" in o:
        a *= 1 - ease((t - o["fade"][0]) / (o["fade"][1] - o["fade"][0]))
    base = o.get("c", rgb(150, 156, 170))
    wob = 1 + 0.012 * math.sin(t * 0.9)
    r = r * wob
    circ(im, x, y, r, mix(base, a), -1)
    circ(im, x, y, r, mix(rgb(205, 210, 225), a), max(2, int(r / 40)))
    for ox, oy, rr in ((-.33, -.22, .24), (.38, .27, .17), (.1, -.55, .12), (-.5, .43, .14)):
        circ(im, x + ox * r, y + oy * r, rr * r, mix(rgb(118, 124, 138), a), -1)
    if o.get("shape") == "top":
        ell(im, x, y, r * 1.0, r * 0.22, mix(rgb(205, 210, 225), a), 2)
    if o.get("glow"):
        glow(im, x, y, r * 1.8, o["glow"], 0.35 * a)


def e_earth(im, t, dur, x, y, r, o):
    a = ease((t - o.get("at", 0)) / 0.7)
    glow(im, x, y, r * 1.6, rgb(60, 120, 255), 0.35 * a)
    circ(im, x, y, r, mix(rgb(40, 90, 170), a), -1)
    for k, (ox, oy, rr) in enumerate(((-.3, -.2, .3), (.35, .15, .25), (-.1, .45, .2))):
        circ(im, x + ox * r + 3 * math.sin(t * 0.3 + k), y + oy * r, rr * r * 0.7, mix(rgb(60, 140, 100), a * .8), -1)
    circ(im, x, y, r, mix(rgb(140, 190, 255), a), 2)


def e_sun(im, t, dur, x, y, r, o):
    a = ease((t - o.get("at", 0)) / 0.8)
    glow(im, x, y, r * 4 * (1 + 0.04 * math.sin(t * 1.3)), rgb(255, 190, 60), 0.8 * a * o.get("g", 1))
    circ(im, x, y, r, mix(rgb(255, 224, 120), a), -1)


def e_dot(im, t, dur, x, y, r, o):
    a = ease((t - o.get("at", 0)) / 0.5)
    circ(im, x, y, r, mix(o.get("c", "ink"), a), -1)


def _angle(t, dur, o):
    P, P2 = o.get("P", 4.0), o.get("P2", 3.55)
    hit = o.get("hit")
    if hit is not None and hit < 1:
        hit = dur * hit
    ph = o.get("ph", -math.pi / 2)
    if hit is None or t < hit:
        return ph + 2 * math.pi * t / P, hit
    return ph + 2 * math.pi * (hit / P + (t - hit) / P2), hit


def e_orbit(im, t, dur, x, y, R, o):
    a = ease((t - o.get("at", 0)) / 0.9)
    circ(im, x, y, R, mix(rgb(120, 140, 190), a * 0.7), 2)
    if o.get("rock", True):
        e_rock(im, t, dur, x, y, R * 0.28, {"at": o.get("at", 0)})
    ang, hit = _angle(t, dur, o)
    for k in range(34, 0, -1):
        tt = t - k * 0.025
        if tt < 0:
            continue
        a2, _ = _angle(tt, dur, o)
        circ(im, x + R * math.cos(a2), y + R * math.sin(a2), R * 0.03 * (1 - k / 40), mix("amber", 0.4 * (1 - k / 34) * a), -1)
    mx, my = x + R * math.cos(ang), y + R * math.sin(ang)
    mr = R * 0.075
    circ(im, mx, my, mr, mix(rgb(188, 190, 198), a), -1)
    circ(im, mx, my, mr, mix(rgb(235, 238, 245), a), 2)
    if hit is not None and hit <= t < hit + 0.8:
        k = (t - hit) / 0.8
        circ(im, mx, my, R * 0.12 + R * 0.8 * k, mix(rgb(255, 214, 120), 0.9 * (1 - k)), 4)
        rect_alpha(im, 0, 0, W, H, rgb(255, 240, 210), 0.12 * (1 - k))
    if o.get("q"):
        circ(im, mx, my, mr + 14 + 8 * math.sin(t * 5), mix("red", 0.9), 3)


def e_craft(im, t, dur, x, y, s, o):
    kind = o.get("kind", "dart")
    fly = o.get("fly", 0)
    xo = 0
    if fly:
        xo = -(1 - ease(t / fly)) * 1400
    x = x + xo + 6 * math.sin(t * 0.6)
    y = y + 5 * math.sin(t * 0.8)
    a = ease((t - o.get("at", 0)) / 0.5)
    body = mix(rgb(170, 176, 190), a)
    edge = mix(rgb(230, 235, 245), a)
    pan = mix(rgb(70, 110, 190), a)
    if kind == "surveyor":
        polyf(im, [(x - s * 1.2, y + s * .35), (x + s * 1.2, y + s * .05), (x + s * 1.2, y + s * .55), (x - s * 1.2, y + s * .85)], mix(rgb(210, 190, 120), a * .8))
        rr = (x - s * .35, y - s * .35, x + s * .35, y + s * .3)
    else:
        for sg in (-1, 1):
            x0 = x + sg * s * 0.55
            for k in range(3):
                bx = x0 + sg * k * s * 0.5
                polyf(im, [(bx, y - s * .35), (bx + sg * s * .46, y - s * .35), (bx + sg * s * .46, y + s * .35), (bx, y + s * .35)], pan)
                polyl(im, [(bx, y - s * .35), (bx + sg * s * .46, y - s * .35), (bx + sg * s * .46, y + s * .35), (bx, y + s * .35)], edge, 1, True)
        rr = (x - s * .5, y - s * .5, x + s * .5, y + s * .5)
    polyf(im, [(rr[0], rr[1]), (rr[2], rr[1]), (rr[2], rr[3]), (rr[0], rr[3])], body)
    polyl(im, [(rr[0], rr[1]), (rr[2], rr[1]), (rr[2], rr[3]), (rr[0], rr[3])], edge, 2, True)
    circ(im, x, y - s * .62, s * .2, edge, 2)
    if kind == "hera":
        circ(im, x, y, s * .17, mix("amber", a), -1)


def e_scope(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / 0.6)
    c = mix(rgb(200, 210, 230), a)
    ang = math.radians(-35 + 4 * math.sin(t * 0.5))
    dx, dy = math.cos(ang) * s, math.sin(ang) * s
    polyl(im, [(x - dx * .5, y - dy * .5 + s * .1), (x + dx * .6, y + dy * .6 + s * .1)], c, max(10, int(s / 7)))
    for sg in (-1, 0, 1):
        line(im, x, y + s * .15, x + sg * s * .45, y + s * 1.0, c, 3)


def e_dome(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / 0.8)
    c = mix(rgb(95, 110, 150), a)
    ell(im, x, y, s, s, c, 3, 0, 180, 360)
    line(im, x - s, y, x + s, y, c, 3)
    rect_alpha(im, x - s * 1.1, y, x + s * 1.1, y + s * .35, rgb(30, 38, 62), 0.9 * a)
    k = 0.5 + 0.5 * math.sin(t * 0.6)
    sx = x - s * .06 + (k - .5) * s * .5
    polyf(im, [(sx - s * .08, y - s * .98), (sx + s * .08, y - s * .98), (sx + s * .08, y - s * .1), (sx - s * .08, y - s * .1)], mix(rgb(10, 14, 30), a))
    glow(im, sx, y - s * .6, s * .6, rgb(150, 170, 255), 0.15 * a)


def e_clock(im, t, dur, x, y, r, o):
    a = ease((t - o.get("at", 0)) / 0.5)
    circ(im, x, y, r, mix("amber", a), 4)
    ang = t * 1.8
    line(im, x, y, x + r * .75 * math.sin(ang), y - r * .75 * math.cos(ang), mix("ink", a), 4)
    line(im, x, y, x + r * .45 * math.sin(ang / 12), y - r * .45 * math.cos(ang / 12), mix("ink", a), 5)


def e_bubble(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / 0.5) * (0.85 + 0.15 * math.sin(t * 2))
    rrect(im, x - s, y - s * .6, x + s, y + s * .5, s * .3, o.get("c", "amber"), a, False, 4)
    polyl(im, [(x - s * .4, y + s * .5), (x - s * .6, y + s * .9), (x - s * .1, y + s * .5)], mix(o.get("c", "amber"), a), 4)
    for k in (-1, 0, 1):
        circ(im, x + k * s * .4, y - s * .05, s * .08, mix(o.get("c", "amber"), a), -1)


def e_eye(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / 0.5)
    ell(im, x, y, s, s * .5, mix("ink", a), 4)
    circ(im, x + 6 * math.sin(t), y, s * .25, mix("amber", a), -1)


def e_cross(im, t, dur, x, y, s, o):
    k = ease((t - o.get("at", 0)) / 0.35)
    c = mix(o.get("c", "red"), 1.0)
    line(im, x - s, y - s, x - s + 2 * s * k, y - s + 2 * s * k, c, 9)
    k2 = ease((t - o.get("at", 0) - 0.2) / 0.35)
    line(im, x + s, y - s, x + s - 2 * s * k2, y - s + 2 * s * k2, c, 9)


def e_tick(im, t, dur, x, y, s, o):
    k = ease((t - o.get("at", 0)) / 0.6)
    pts = [(x - s, y), (x - s * .3, y + s * .7), (x + s, y - s * .8)]
    n = k * 2
    c = mix(o.get("c", "green"), 1.0)
    if n > 0:
        a = min(n, 1)
        line(im, pts[0][0], pts[0][1], pts[0][0] + (pts[1][0] - pts[0][0]) * a, pts[0][1] + (pts[1][1] - pts[0][1]) * a, c, 10)
    if n > 1:
        a = n - 1
        line(im, pts[1][0], pts[1][1], pts[1][0] + (pts[2][0] - pts[1][0]) * a, pts[1][1] + (pts[2][1] - pts[1][1]) * a, c, 10)


def e_flash(im, t, dur, x, y, r, o):
    at = o.get("at", 0)
    per = o.get("every", 0)
    tt = (t - at) % per if per else t - at
    if tt < 0 or tt > 0.9:
        return
    k = tt / 0.9
    circ(im, x, y, r * (0.2 + k), mix(o.get("c", rgb(255, 214, 120)), 0.9 * (1 - k)), 4)
    glow(im, x, y, r * 1.6 * (1 - 0.3 * k), o.get("c", rgb(255, 214, 120)), 0.8 * (1 - k))


def e_path(im, t, dur, x, y, s, o):
    pts = o["pts"]
    at, ln = o.get("at", 0), o.get("len", 1.5)
    p = ease((t - at) / ln) if ln else 1.0
    if p <= 0:
        return
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(seg)
    want = tot * p
    c = mix(o.get("c", "ink"), 0.9)
    th = o.get("th", 2)
    acc = 0
    last = pts[0]
    for i, sl in enumerate(seg):
        if acc >= want:
            break
        f = min(1.0, (want - acc) / sl) if sl else 1
        a, b = pts[i], (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
        if o.get("dash"):
            n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 22))
            for k in range(0, n, 2):
                line(im, a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n, a[0] + (b[0] - a[0]) * (k + 1) / n, a[1] + (b[1] - a[1]) * (k + 1) / n, c, th)
        else:
            line(im, a[0], a[1], b[0], b[1], c, th)
        acc += sl
        last = b
    if o.get("arrow") and p > 0.98:
        prev = pts[-2]
        ang = math.atan2(pts[-1][1] - prev[1], pts[-1][0] - prev[0])
        L = 26
        polyf(im, [pts[-1], (pts[-1][0] - L * math.cos(ang - .45), pts[-1][1] - L * math.sin(ang - .45)),
                   (pts[-1][0] - L * math.cos(ang + .45), pts[-1][1] - L * math.sin(ang + .45))], c)
    if o.get("dot"):
        q = (t * o.get("speed", 0.25)) % 1.0
        d = tot * q
        acc = 0
        for i, sl in enumerate(seg):
            if acc + sl >= d:
                f = (d - acc) / sl if sl else 0
                px, py = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
                glow(im, px, py, 30, o.get("dc", "amber"), 0.7)
                circ(im, px, py, 7, mix(o.get("dc", "amber"), 1.0), -1)
                break
            acc += sl


def e_bar(im, t, dur, x, y, w, o):
    h = o.get("h", 44)
    at, ln = o.get("at", 0.3), o.get("len", 1.2)
    a = ease((t - at + 0.3) / 0.4)
    x0 = x - w / 2
    rrect(im, x0, y - h / 2, x0 + w, y + h / 2, h / 2, rgb(30, 40, 66), a * 0.9)
    v = o.get("v", 1) * ease((t - at) / ln)
    if v > 0.001:
        wd = max(h, w * v) if o.get("v", 1) > 0.02 else max(8, w * v)
        rrect(im, x0, y - h / 2, x0 + wd, y + h / 2, h / 2 if wd > h else 3, o.get("c", "amber"), 0.95)
    if o.get("band"):
        b0, b1 = o["band"]
        rrect(im, x0 + w * b0, y - h / 2 - 8, x0 + w * b1, y + h / 2 + 8, 6, o.get("bc", "red"), 0.35 * ease((t - at - 0.5) / 0.6))
        rrect(im, x0 + w * b0, y - h / 2 - 8, x0 + w * b1, y + h / 2 + 8, 6, o.get("bc", "red"), 0.9 * ease((t - at - 0.5) / 0.6), False, 3)
    if o.get("mark") is not None:
        mx = x0 + w * o["mark"]
        line(im, mx, y - h / 2 - 16, mx, y + h / 2 + 16, mix("ink", ease((t - at - 0.4) / 0.4)), 4)


def e_panel(im, t, dur, x, y, w, o):
    h = o.get("h", 400)
    a = ease((t - o.get("at", 0)) / 0.5)
    rrect(im, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 22, o.get("c", rgb(30, 40, 66)), 0.35 * a)
    rrect(im, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 22, o.get("lc", "dim"), 0.9 * a, False, 2)


def e_dots(im, t, dur, x, y, w, o):
    cols, rows = o.get("cols", 40), o.get("rows", 20)
    sp = w / cols
    r = sp * 0.30
    rng = np.random.default_rng(3)
    order = rng.permutation(cols * rows)
    rank = np.empty_like(order)
    rank[order] = np.arange(cols * rows)
    lit = o.get("lit", 0.42)
    at, ln = o.get("at", 0.3), o.get("len", 2.0)
    prog = ease((t - at) / ln)
    x0 = x - w / 2 + sp / 2
    y0 = y - rows * sp / 2 + sp / 2
    for i in range(cols):
        for j in range(rows):
            k = rank[i * rows + j] / (cols * rows)
            on = k < lit * prog if not o.get("all") else True
            c = o.get("c", "amber") if on else rgb(60, 72, 104)
            al = 0.95 if on else 0.5
            if (not on) and o.get("pulse"):
                al = 0.35 + 0.4 * (0.5 + 0.5 * math.sin(t * 3 + k * 20))
                c = o.get("pc", "red")
            circ(im, x0 + i * sp, y0 + j * sp, r, mix(c, al), -1)


def e_chart(im, t, dur, x, y, w, o):
    h = o.get("h", 400)
    x0, y0 = x - w / 2, y + h / 2
    a = ease((t - o.get("at", 0)) / 0.5)
    line(im, x0, y0, x0 + w, y0, mix("dim", a), 3)
    line(im, x0, y0, x0, y0 - h, mix("dim", a), 3)
    for g in range(1, 4):
        line(im, x0, y0 - h * g / 4, x0 + w, y0 - h * g / 4, mix(rgb(40, 52, 84), a), 1)
    pts = o["pts"]
    p = ease((t - o.get("at", 0.3) - 0.3) / o.get("len", 2.0))
    n = 90
    xs = np.linspace(pts[0][0], pts[-1][0], n)
    ys = np.interp(xs, [q[0] for q in pts], [q[1] for q in pts])
    if o.get("band"):
        bb = o["band"]
        bx = np.linspace(bb[0][0], bb[-1][0], n)
        lo = np.interp(bx, [q[0] for q in bb], [q[1] for q in bb])
        hi = np.interp(bx, [q[0] for q in bb], [q[2] for q in bb])
        k = int(n * p)
        if k > 2:
            poly = [(x0 + bx[i] * w, y0 - hi[i] * h) for i in range(k)] + [(x0 + bx[i] * w, y0 - lo[i] * h) for i in range(k - 1, -1, -1)]
            P = [(int(a_ * 16), int(b_ * 16)) for a_, b_ in poly]
            X0, Y0, X1, Y1 = int(x0), int(y0 - h), int(x0 + w), int(y0)
            ov = im[Y0:Y1, X0:X1].copy()
            cv2.fillPoly(im, [np.array(P, np.int32)], C(o.get("bc", "red")), cv2.LINE_AA, 4)
            im[Y0:Y1, X0:X1] = cv2.addWeighted(ov, 0.7, im[Y0:Y1, X0:X1], 0.3, 0)
    k = max(2, int(n * p))
    polyl(im, [(x0 + xs[i] * w, y0 - ys[i] * h) for i in range(k)], mix(o.get("c", "amber"), 1.0), 5)
    ex, ey = x0 + xs[k - 1] * w, y0 - ys[k - 1] * h
    glow(im, ex, ey, 26, o.get("c", "amber"), 0.8)
    circ(im, ex, ey, 7, C(o.get("c", "amber")), -1)


def e_globe(im, t, dur, x, y, r, o):
    a = ease((t - o.get("at", 0)) / 0.8)
    glow(im, x, y, r * 1.5, rgb(60, 120, 255), 0.3 * a)
    circ(im, x, y, r, mix(rgb(22, 50, 100), a), -1)
    ph = t * 0.35
    for k in range(6):
        wd = abs(math.cos(ph + k * math.pi / 6)) * r
        ell(im, x, y, wd, r, mix(rgb(90, 130, 200), a * .6), 1)
    for k in (-2, -1, 0, 1, 2):
        yy = y + k * r * 0.32
        ww = math.sqrt(max(r * r - (k * r * .32) ** 2, 0))
        ell(im, x, yy, ww, ww * 0.12, mix(rgb(90, 130, 200), a * .6), 1)
    circ(im, x, y, r, mix(rgb(140, 190, 255), a), 3)
    rng = np.random.default_rng(9)
    ev = o.get("every", 0)
    if ev:
        for k in range(40):
            tt = t - 0.5 - k * ev
            if tt < 0:
                break
            ang, rr = rng.uniform(0, 6.28), math.sqrt(rng.uniform(0, 1)) * r * .85
            if tt < 0.9:
                kk = tt / 0.9
                px, py = x + rr * math.cos(ang), y + rr * math.sin(ang)
                circ(im, px, py, 10 + 40 * kk, mix("amber", .9 * (1 - kk)), 3)
                glow(im, px, py, 40 * (1 - kk * .4), "amber", .8 * (1 - kk))
    if o.get("hemi"):
        k = ease((t - o.get("at", 0) - 0.4) / 0.8)
        ov = im[int(y - r):int(y + r), int(x):int(x + r)].copy()
        ell(im, x, y, r, r, "amber", -1, 0, -90, 90)
        im[int(y - r):int(y + r), int(x):int(x + r)] = cv2.addWeighted(ov, 1 - 0.28 * k, im[int(y - r):int(y + r), int(x):int(x + r)], 0.28 * k, 0)
        circ(im, x, y, r, mix("amber", k), 4)


def e_collide(im, t, dur, x, y, s, o):
    hit = o.get("hit", 0.4) * min(dur, 8)
    a = ease(t / 0.5)
    rb = s * 0.32
    ra = s * 0.13
    v = 1.0
    start = x - s * 1.5
    contact = x - rb - ra
    if t < hit:
        ax = start + (contact - start) * ease(t / hit) ** 1.0
        sh = 0
    else:
        sh = (t - hit) * s * 0.035
        ax = contact + sh
    bx = x + sh
    circ(im, bx, y, rb, mix(rgb(150, 156, 170), a), -1)
    circ(im, bx, y, rb, mix(rgb(205, 210, 225), a), 3)
    if o.get("kind") == "craft":
        e_craft(im, 99, dur, ax - s * 0.12, y, s * 0.12, {"kind": "dart", "at": -9})
    else:
        circ(im, ax, y, ra, mix("amber", a), -1)
    if t < hit:
        for k in range(1, 7):
            circ(im, ax - k * ra * .9, y, ra * (1 - k / 8) * .8, mix("amber", .5 * (1 - k / 7)), -1)
    if hit <= t < hit + 0.7:
        e_flash(im, t - hit, 0, contact + ra * 0.2, y, s * .5, {})
    if t > hit + 0.3:
        k = ease((t - hit - 0.3) / 0.6)
        line(im, bx + rb + 16, y - rb - 30, bx + rb + 16 + 120 * k, y - rb - 30, mix("amber", k), 6)


def e_fountain(im, t, dur, x, y, s, o):
    cv2.ellipse(im, (int(x * 16), int((y + s * 3.1) * 16)), (int(s * 3.6 * 16), int(s * 3.1 * 16)), 0, 0, 360, C(rgb(150, 156, 170)), -1, cv2.LINE_AA, 4)
    cv2.ellipse(im, (int(x * 16), int((y + s * 3.1) * 16)), (int(s * 3.6 * 16), int(s * 3.1 * 16)), 0, 0, 360, C(rgb(205, 210, 225)), 3, cv2.LINE_AA, 4)
    rng = np.random.default_rng(21)
    t0 = o.get("at", 0.5)
    if t < t0:
        return
    tt = t - t0
    for k in range(140):
        ang = rng.uniform(-1.25, 1.25)
        sp = rng.uniform(160, 520) * s / 100
        r = rng.uniform(2, 7)
        d = rng.uniform(0, 0.6)
        u = tt - d
        if u < 0:
            continue
        px = x + math.sin(ang) * sp * u * 0.9
        py = y + s * 0.0 - math.cos(ang) * sp * u * 1.2 + 140 * u * u * s / 100
        al = clamp(1 - u / 3.8)
        if al > 0:
            circ(im, px, py, r, mix(rgb(215, 190, 150) if k % 3 else "amber", al * .9), -1)


def e_rubble(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / 0.7)
    circ(im, x, y, s, mix(rgb(120, 140, 190), a * .8), 3)
    rng = np.random.default_rng(4)
    for k in range(60):
        ang, rr = rng.uniform(0, 6.28), math.sqrt(rng.uniform(0, 1)) * s * 0.86
        r = rng.uniform(.06, .17) * s
        jit = 3 * math.sin(t * 1.3 + k)
        g = int(rng.uniform(95, 175))
        circ(im, x + rr * math.cos(ang) + jit * .4, y + rr * math.sin(ang) + jit, r, mix(rgb(g, g + 4, g + 14), a), -1)
        circ(im, x + rr * math.cos(ang) + jit * .4, y + rr * math.sin(ang) + jit, r, mix(rgb(215, 220, 235), a * .7), 1)


def e_trees(im, t, dur, x, y, s, o):
    rng = np.random.default_rng(6)
    p = ease((t - o.get("at", 0.3)) / o.get("len", 3.0))
    for k in range(110):
        ang = rng.uniform(0, 6.28)
        L = s * rng.uniform(.62, 1.0)
        r0 = s * 0.1
        c = mix(rgb(120, 90, 60) if k % 2 else rgb(70, 130, 80), 0.9)
        line(im, x + r0 * math.cos(ang), y + r0 * math.sin(ang), x + (r0 + (L - r0) * p) * math.cos(ang), y + (r0 + (L - r0) * p) * math.sin(ang), c, 3)
    glow(im, x, y, s * .5, "amber", 0.4 * (1 - p * .6))
    circ(im, x, y, s * 0.08, mix("amber", 1), -1)


def e_city(im, t, dur, x, y, w, o):
    """winter morning skyline, no people"""
    a = ease(t / 0.8)
    yy = np.linspace(0, 1, 420)[:, None, None]
    sky = (np.array(rgb(30, 40, 70), np.float32) * (1 - yy) + np.array(rgb(120, 110, 120), np.float32) * yy)
    X0, Y0 = int(x - w / 2), int(y - 300)
    X1, Y1 = int(x + w / 2), int(y + 120)
    sk = np.repeat(sky, X1 - X0, axis=1).astype(np.uint8)[: Y1 - Y0]
    im[Y0:Y1, X0:X1] = cv2.addWeighted(im[Y0:Y1, X0:X1], 1 - .85 * a, sk, .85 * a, 0)
    rng = np.random.default_rng(8)
    xx = X0
    while xx < X1:
        bw = int(rng.uniform(70, 150))
        bh = int(rng.uniform(80, 280))
        cv2.rectangle(im, (xx, Y1 - bh), (min(xx + bw, X1), Y1), C(mix(rgb(24, 30, 52), a)), -1)
        for wx in range(xx + 12, min(xx + bw, X1) - 12, 26):
            for wy in range(Y1 - bh + 14, Y1 - 14, 34):
                if rng.uniform() < .3:
                    cv2.rectangle(im, (wx, wy), (wx + 12, wy + 18), C(mix(rgb(255, 200, 110), a * .8)), -1)
        xx += bw + 4


def e_fire(im, t, dur, x, y, s, o):
    at, ln = o.get("at", 0.3), o.get("len", 2.5)
    p = ease((t - at) / ln)
    if p <= 0:
        return
    x1, y1 = x + o.get("dx", 700), y + o.get("dy", 330)
    hx, hy = x + (x1 - x) * p, y + (y1 - y) * p
    for k in range(40):
        q = max(0, p - k * 0.012)
        px, py = x + (x1 - x) * q, y + (y1 - y) * q
        circ(im, px, py, s * (0.14 - k * 0.003) + 1, mix(rgb(255, 255, 255), .6 * (1 - k / 40)), -1)
    glow(im, hx, hy, s * 1.6, rgb(255, 190, 90), 0.9)
    circ(im, hx, hy, s * .18, rgb(255, 255, 255), -1)
    if o.get("flash") and p >= 1:
        k = (t - at - ln)
        e_flash(im, k, 0, hx, hy, 260, {"c": rgb(255, 235, 190)})
        rect_alpha(im, 0, 0, W, H, rgb(255, 245, 225), 0.35 * clamp(1 - k / 0.5))


def e_crack(im, t, dur, x, y, s, o):
    cv2.rectangle(im, (int(x - s * 1.3), int(y - s)), (int(x + s * 1.3), int(y + s)), C(rgb(110, 130, 170)), 6, cv2.LINE_AA)
    line(im, x, y - s, x, y + s, rgb(110, 130, 170), 4)
    rect_alpha(im, x - s * 1.3, y - s, x + s * 1.3, y + s, rgb(60, 80, 130), .12)
    rng = np.random.default_rng(12)
    p = ease((t - o.get("at", 0.6)) / 2.2)
    cx, cy = x - s * .35, y - s * .1
    for k in range(14):
        ang = rng.uniform(0, 6.28)
        L = s * rng.uniform(.4, 1.1) * p
        pts = [(cx, cy)]
        for j in range(1, 5):
            ang += rng.uniform(-.3, .3)
            pts.append((cx + math.cos(ang) * L * j / 4, cy + math.sin(ang) * L * j / 4))
        polyl(im, pts, rgb(235, 240, 255), 2)


def e_blinkframe(im, t, dur, x, y, w, o):
    h = o.get("h", 380)
    e_panel(im, t, dur, x, y, w, {"h": h, "at": o.get("at", 0)})
    rng = np.random.default_rng(o.get("seed", 1))
    for k in range(34):
        sx, sy = x + rng.uniform(-.46, .46) * w, y + rng.uniform(-.44, .44) * h
        circ(im, sx, sy, rng.uniform(1.2, 2.8), mix(rgb(220, 225, 245), .9), -1)
    dx, dy = o.get("dot", (0.1, 0.0))
    circ(im, x + dx * w, y + dy * h, 5, mix("white", 1), -1)
    if o.get("circle"):
        circ(im, x + dx * w, y + dy * h, 26 + 3 * math.sin(t * 4), mix("amber", 1), 3)


def e_tl(im, t, dur, x, y, w, o):
    a = ease((t - o.get("at", 0)) / 0.5)
    x0 = x - w / 2
    line(im, x0, y, x0 + w, y, mix("dim", a), 4)
    for i, f in enumerate(o["marks"]):
        k = ease((t - o.get("at", 0) - 0.4 - i * 0.6) / 0.4)
        circ(im, x0 + w * f, y, 12, mix("amber", k), -1)
        glow(im, x0 + w * f, y, 40, "amber", .4 * k)


def e_streaks(im, t, dur, x, y, s, o):
    rng = np.random.default_rng(31)
    for k in range(46):
        yy = rng.uniform(80, 1000)
        L = rng.uniform(120, 520)
        v = rng.uniform(900, 2400)
        x0 = rng.uniform(0, 2600)
        px = (x0 + t * v) % 2700 - 400
        line(im, px - L, yy, px, yy, mix(rgb(200, 215, 255) if k % 3 else "amber", rng.uniform(.15, .5)), int(rng.uniform(1, 3.5)))


def e_split(im, t, dur, x, y, r, o):
    at = o.get("at", 0.8)
    k = ease((t - at) / 2.5)
    rng = np.random.default_rng(14)
    if k <= 0:
        e_rock(im, t, dur, x, y, r, {})
        return
    for i in range(8):
        ang = i * math.pi / 4 + rng.uniform(-.3, .3)
        rr = r * rng.uniform(.28, .5)
        d = k * r * rng.uniform(1.2, 2.4)
        circ(im, x + math.cos(ang) * d, y + math.sin(ang) * d * 0.7, rr, mix(rgb(150, 156, 170), 1), -1)
        circ(im, x + math.cos(ang) * d, y + math.sin(ang) * d * 0.7, rr, mix(rgb(205, 210, 225), 1), 2)
    glow(im, x, y, r * 1.5, "amber", 0.5 * clamp(1 - k * 1.5))


def e_field(im, t, dur, x, y, w, o):
    e_dots(im, t, dur, x, y, w, {"cols": 36, "rows": 14, "all": True, "c": o.get("c", "forest"), "at": 0})


def e_scale(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / .5)
    c = mix("ink", a)
    line(im, x - s, y - s * .6, x + s, y - s * .6, c, 4)
    line(im, x, y - s * .6, x, y + s * .8, c, 4)
    line(im, x - s * .5, y + s * .8, x + s * .5, y + s * .8, c, 4)
    for sg in (-1, 1):
        polyl(im, [(x + sg * s, y - s * .6), (x + sg * s * .75, y), (x + sg * s * 1.25, y)], c, 2, True)


def e_shoebox(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / .5)
    rr = (x - s, y - s * .5, x + s, y + s * .5)
    polyl(im, [(rr[0], rr[1]), (rr[2], rr[1]), (rr[2], rr[3]), (rr[0], rr[3])], mix(o.get("c", "ink"), a), 4, True)
    line(im, rr[0], y - s * .15, rr[2], y - s * .15, mix(o.get("c", "ink"), a), 3)
    circ(im, x, y + s * .15, s * .12, mix("amber", a), -1)


def e_laser(im, t, dur, x, y, s, o):
    a = ease((t - o.get("at", 0)) / .5)
    line(im, x - s * 1.4, y - s * .6, x - s * .1, y - s * .05, mix("red", a), 5)
    glow(im, x - s * .1, y - s * .05, s * .5, "red", .6 * a)
    for k in range(10):
        ph = (t * 0.7 + k * 0.1) % 1.0
        circ(im, x + s * .05 + ph * s * .8 * math.cos(1 + k * .3), y - s * .05 - ph * s * .9, 3 + 3 * ph, mix("ink", a * (1 - ph) * .8), -1)


def e_none(im, t, dur, x, y, s, o):
    pass


def e_media_frame(im, t, dur, x, y, w, o):
    h = o.get("h", 560)
    a = ease(t / .5)
    X0, Y0 = int(x - w / 2), int(y - h / 2)
    n = int(w / 28)
    for k in range(0, n, 2):
        line(im, X0 + k * 28, Y0, X0 + k * 28 + 18, Y0, mix("dim", a), 3)
        line(im, X0 + k * 28, Y0 + h, X0 + k * 28 + 18, Y0 + h, mix("dim", a), 3)
    for k in range(0, int(h / 28), 2):
        line(im, X0, Y0 + k * 28, X0, Y0 + k * 28 + 18, mix("dim", a), 3)
        line(im, X0 + w, Y0 + k * 28, X0 + w, Y0 + k * 28 + 18, mix("dim", a), 3)
    scan = (t * 90) % h
    rect_alpha(im, X0, Y0 + scan - 3, X0 + w, Y0 + scan + 3, "dim", .25)


EL = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("e_") and callable(v)}


# ---------------------------------------------------------------- text items / layout / ASS
KINDS = {
    "B": dict(px=150, font="N", c="amber"),
    "M": dict(px=66, font="M", c="ink"),
    "s": dict(px=42, font="M", c="dim"),
    "C": dict(px=40, font="M", c="amber", box="line"),
    "K": dict(px=62, font="M", c="ink", box="card"),
    "R": dict(px=46, font="M", c="red", box="tag"),
    "D": dict(px=40, font="M", c="amber", box="line", fixed="date"),
    "H": dict(px=44, font="M", c="ink", box="line", fixed="title"),
    "S": dict(px=30, font="M", c="dim", fixed="src"),
    "X": dict(px=30, font="M", c="dim", fixed="credit"),
    "T": dict(px=40, font="M", c="ink"),
}
REG = {"c": (960, 540, 1650), "l": (520, 560, 880), "r": (1400, 560, 880), "b": (960, 810, 1650), "L": (480, 560, 800), "R": (1440, 560, 800), "ll": (560, 860, 920)}
LAY_OFF = {}  # graphics use absolute px coords; lay only picks the text region


def parse_item(s):
    head, *rest = s.split("|")
    kind, text = head.split(":", 1)
    it = dict(kind=kind, text=text.replace("\\n", "\n"))
    for p in rest:
        if "=" in p:
            k, v = p.split("=", 1)
            it[k] = v
        elif p in COL:
            it["c"] = p
        else:
            try:
                it["at"] = float(p)
            except ValueError:
                it["c"] = p
    return it


def layout(spec, dur):
    lay = spec.get("lay", "c")
    items = [parse_item(s) for s in spec.get("T", [])]
    placed = []
    groups = {}
    nstack = sum(1 for it in items if not KINDS[it["kind"]].get("fixed") and "at" not in it and "xy" not in it)
    stag = min(spec.get("stag", 0.65), max(0.2, (dur * 0.55) / max(nstack, 1)))
    idx = 0
    for it in items:
        K = KINDS[it["kind"]]
        px = float(it.get("px", K["px"])) * spec.get("pscale", 1.0)
        font = K["font"]
        c = it.get("c", K["c"])
        box = K.get("box")
        text = it["text"]
        pad = 20 if box else 0
        reg = it.get("r", lay if lay in REG else "c")
        maxw = REG[reg][2]
        if K.get("fixed") in ("date", "title"):
            maxw = 880
        w = tw(text, font, px)
        while w + 2 * pad > maxw and px > 24:
            px -= 2
            w = tw(text, font, px)
        lines = text.count("\n") + 1
        h = px * 1.18 * lines + (2 * pad * 0.6 if box else 0)
        d = dict(it, px=px, font=font, c=c, box=box, w=w, h=h, pad=pad, lines=lines, fixed=K.get("fixed"), reg=reg)
        if "at" in it:
            d["at"] = float(it["at"])
        elif not K.get("fixed") and "xy" not in it:
            d["at"] = 0.25 + idx * stag
            idx += 1
        else:
            d["at"] = 0.3
        d["out"] = float(it.get("out", 3.6 if d["fixed"] == "src" else dur))
        if K.get("fixed") == "date":
            d["x"], d["y"], d["an"] = 1850 - w / 2 - pad, 100, 5
        elif K.get("fixed") == "title":
            d["x"], d["y"], d["an"] = 90 + w / 2 + pad, 100, 5
        elif K.get("fixed") == "src":
            d["x"], d["y"], d["an"] = 70, 1010, 4
        elif K.get("fixed") == "credit":
            d["x"], d["y"], d["an"] = 1850, 1010, 6
        elif "xy" in it:
            x_, y_ = it["xy"].split(",")
            d["x"], d["y"], d["an"] = float(x_), float(y_), 5
        else:
            groups.setdefault(reg, []).append(d)
        placed.append(d)
    for reg, ds in groups.items():
        cx, cy, _ = REG[reg]
        cy += spec.get("cy", 0)
        gap = 26
        tot = sum(d["h"] for d in ds) + gap * (len(ds) - 1)
        yy = cy - tot / 2
        for d in ds:
            d["x"], d["y"], d["an"] = cx, yy + d["h"] / 2, 5
            yy += d["h"] + gap
    return placed


def hms(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def bgr_ass(c):
    c = C(c)
    return "&H%02X%02X%02X&" % c


def ass_events(placed, labs, dur):
    ev = []
    allt = [(d, d["text"]) for d in placed] + [(l, l["text"]) for l in labs]
    for d, text in allt:
        a, b = max(d["at"], 0.0), min(d["out"], dur)
        if b <= a:
            continue
        fs = int(d["px"] * ratio(d["font"]))
        slam = d.get("kind") == "B" and d.get("slam", "1") != "0"
        zoom = 106
        fo = 300 if d.get("fixed") in ("src", "credit") else 0
        tags = "\\an%d\\pos(%d,%d)\\fs%d\\1c%s\\fad(%d,%d)" % (d["an"], d["x"], d["y"], fs, bgr_ass(d["c"]), 0 if d["at"] < 0 else 350, fo)
        if d.get("alpha"):
            tags += "\\1a&H%s&" % d["alpha"]
        if not d.get("fixed"):
            span = int((b - a) * 1000)
            if slam:
                tags += "\\fscx135\\fscy135\\t(0,220,\\fscx100\\fscy100)\\t(220,%d,\\fscx%d\\fscy%d)" % (max(span, 300), zoom, zoom)
            else:
                tags += "\\fscx100\\fscy100\\t(0,%d,\\fscx%d\\fscy%d)" % (max(span, 300), 104, 104)
        txt = text.replace("\n", "\\N")
        ev.append("Dialogue: 1,%s,%s,%s,,0,0,0,,{%s}%s" % (hms(a), hms(b), "N" if d["font"] == "N" else "M", tags, txt))
    return ev


def ass_file(events):
    head = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        "Style: M,Mukta,60,&HFFFFFF&,&HFFFFFF&,&H0A0705&,&H000000&,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1",
        "Style: N,Poppins,60,&HFFFFFF&,&HFFFFFF&,&H0A0705&,&H000000&,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1", "",
        "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]
    return "\n".join(head + events) + "\n"


def lab_to_item(e, ox, oy):
    return None


# ---------------------------------------------------------------- one shot
def draw_boxes(im, placed, t):
    for d in placed:
        if not d.get("box"):
            continue
        a = ease((t - d["at"]) / 0.35)
        if d["out"] < 1e5 and t > d["out"] - 0.3:
            a *= clamp((d["out"] - t) / 0.3)
        if a <= 0:
            continue
        x0, x1 = d["x"] - d["w"] / 2 - d["pad"], d["x"] + d["w"] / 2 + d["pad"]
        y0, y1 = d["y"] - d["h"] / 2, d["y"] + d["h"] / 2
        c = d["c"] if d["box"] != "line" else d["c"]
        if d["box"] == "card":
            rrect(im, x0, y0, x1, y1, 22, c, 0.30 * a)
            rrect(im, x0, y0, x1, y1, 22, c, 1.0 * a, False, 3)
        elif d["box"] == "tag":
            rrect(im, x0, y0, x1, y1, 12, c, 0.22 * a)
            rrect(im, x0, y0, x1, y1, 12, c, 1.0 * a, False, 3)
        else:
            rrect(im, x0, y0, x1, y1, 14, c, 0.08 * a)
            rrect(im, x0, y0, x1, y1, 14, c, 0.9 * a, False, 2)


def shot_hash(spec, nfr, extra):
    return hashlib.sha1((VERSION + json.dumps(spec, sort_keys=True) + str(nfr) + extra).encode()).hexdigest()[:10]


def render_shot(args):
    n, spec, nfr, out, story_dir = args
    out = Path(out)
    if out.exists():
        return n, 0.0, "cached"
    t_start = time.time()
    dur = nfr / FPS
    feet = []
    mspec = spec.get("media")
    if mspec:
        names = mspec.get("files") or ([mspec["file"]] if mspec.get("file") else [])
        for nm in names:
            fp = find_footage(Path(story_dir), n, nm)
            if fp and fp.name == nm:
                feet.append(Footage(fp))
        if not names:
            fp = find_footage(Path(story_dir), n)
            if fp:
                feet.append(Footage(fp))
    foot = feet[0] if feet else None
    T = list(spec.get("T", []))
    if mspec:
        if foot:
            T.append("X:Credit: %s|at=0.4" % mspec.get("credit", "NASA"))
        else:
            T.append("M:NASA footage here|amber|xy=960,455|at=0.2|px=72")
            T.append("s:%s|xy=960,560|at=0.5|px=34" % mspec.get("cue", ""))
            T.append("s:credit: %s|xy=960,620|at=0.8|px=30" % mspec.get("credit", "NASA"))
    spec = dict(spec, T=T)
    placed = layout(spec, dur)
    ox, oy = 0, 0
    els = spec.get("g", [])
    labs = []
    elist = []
    for e in els:
        kind, ex, ey, es, o = e
        ax, ay = ex, ey
        if kind == "path":
            pass
        if kind == "bar":
            if o.get("lab"):
                labs.append(dict(text=o["lab"], x=ax - es / 2, y=ay - o.get("h", 44) / 2 - 30, px=o.get("lpx", 38), font="M", c=o.get("lc", "ink"), an=4, at=o.get("at", .3), out=dur))
            if o.get("end"):
                labs.append(dict(text=o["end"], x=ax - es / 2 + es * o.get("v", 1) * 0 + es + 18, y=ay, px=o.get("epx", 40), font="M", c=o.get("c", "amber"), an=4, at=o.get("at", .3) + o.get("len", 1.2) * .6, out=dur))
        for lb in o.get("labs", []) if kind != "path" else []:
            txt, dx, dy = lb[0], lb[1], lb[2]
            col = lb[3] if len(lb) > 3 else "ink"
            px = lb[4] if len(lb) > 4 else 38
            at = lb[5] if len(lb) > 5 else o.get("at", 0.3) + 0.4
            an = lb[6] if len(lb) > 6 else 5
            wlab = tw(txt, "M", px)
            maxw = 1780
            while wlab > maxw and px > 22:
                px -= 2
                wlab = tw(txt, "M", px)
            labs.append(dict(text=txt, x=ax + dx, y=ay + dy, px=px, font="M", c=col, an=an, at=at, out=dur))
        if kind == "path" and o.get("labs"):
            for lb in o["labs"]:
                txt, dx, dy = lb[0], lb[1], lb[2]
                labs.append(dict(text=txt, x=dx, y=dy, px=lb[4] if len(lb) > 4 else 36, font="M", c=lb[3] if len(lb) > 3 else "ink",
                                 an=lb[6] if len(lb) > 6 else 5, at=lb[5] if len(lb) > 5 else o.get("at", 0) + 0.5, out=dur))
        if kind == "txt":
            continue
        elist.append((kind, ax, ay, es, o))
    for lb in labs:
        lb.setdefault("fixed", None)
        lb.setdefault("kind", "L")
    assf = out.with_suffix(".ass")
    assf.write_text(ass_file(ass_events(placed, labs, dur)), encoding="utf-8")
    ff = find_ff()
    fonts = (ROOT / "shared/fonts").as_posix().replace(":", "\\:")
    tmp = out.with_name(out.stem + ".part.mp4")
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", f"subtitles=filename={assf.name}:fontsdir='{fonts}'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-g", "30", "-r", str(FPS), "-an", tmp.name], stdin=subprocess.PIPE, cwd=str(out.parent))
    im = np.empty((H, W, 3), np.uint8)
    tint = spec.get("tint")
    if tint:
        tint = dict(tint, c=C(tint["c"]))
    for f in range(nfr):
        t = f / FPS
        if foot:
            mode = mspec.get("mode", "cover")
            if len(feet) > 1:
                seg = dur / len(feet)
                k = min(int(t / seg), len(feet) - 1)
                fr = place_footage(feet[k].raw(0), mode, 1.0 + 0.25 * ((t - k * seg) / seg), mspec.get("h", 800), mspec.get("cx", 960), mspec.get("cy", 540))
            else:
                z = 1.0 + mspec.get("zoom", 0.06) * (t / max(dur, 1))
                fr = place_footage(foot.raw(mspec.get("start", 0) + t * mspec.get("rate", 1.0)), mode, z, mspec.get("h", 800), mspec.get("cx", 960), mspec.get("cy", 540))
            if mode == "contain":
                draw_bg(im, t, n, tint)
                cv2.add(im, cv2.convertScaleAbs(fr, alpha=mspec.get("dim", 1.0)), dst=im)
            else:
                im[:] = cv2.convertScaleAbs(fr, alpha=mspec.get("dim", 0.62), beta=0)
        else:
            draw_bg(im, t, n, tint)
        if mspec and not foot:
            e_media_frame(im, t, dur, 960, 520, 1000, {"h": 520})
        for kind, ax, ay, es, o in elist:
            EL[kind](im, t, dur, ax, ay, es, o)
        draw_boxes(im, placed, t)
        blk = spec.get("black", 0)
        if blk and t < blk:
            rect_alpha(im, 0, 0, W, H, (0, 0, 0), 1 - ease((t - blk * 0.55) / (blk * 0.45)))
        p.stdin.write(im.tobytes())
    p.stdin.close()
    rc = p.wait()
    if rc:
        return n, 0.0, "ffmpeg failed"
    tmp.replace(out)
    assf.unlink(missing_ok=True)
    return n, time.time() - t_start, "ok"


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story", help="story number, e.g. 001")
    ap.add_argument("--seconds", type=float, default=0, help="test render of the first N seconds")
    ap.add_argument("--shots", default="", help="comma list: render only these shots (no concat)")
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--tail", type=float, default=20.0)
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--plx-all", action="store_true", help="real look: only pre-make the depth-parallax clips for every still in the map/overrides")
    ap.add_argument("--plx-workers", type=int, default=5)
    ap.add_argument("--name", default="")
    ap.add_argument("--look", default="real", choices=["real", "graphic"], help="real = real NASA footage look (default); graphic = old own-graphics look")
    a = ap.parse_args()
    sd = next((ROOT / "channels/reality-check/stories").glob(a.story + "_*"))
    ld = sd / "long"
    if a.look == "real":
        import rc_real_look
        return rc_real_look.main_real(a, sd, ld)
    specs = {s["n"]: s for s in json.loads((ld / "shot_specs.json").read_text(encoding="utf-8"))}
    tfile = sd / "audio/voiceover_timing.json"
    if not tfile.exists():
        tfile = sd / "audio/voiceover_draft_timing.json"
    lines = json.loads(tfile.read_text(encoding="utf-8"))
    audio = sd / "audio/voiceover_full.wav"
    if not audio.exists():
        audio = sd / "audio/voiceover_draft_mixed.wav"
    probe = subprocess.run([find_ff("ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)], capture_output=True, text=True)
    adur = float(probe.stdout.strip())
    starts = [0.0] + [l["start"] for l in lines[1:]]
    ends_voice = max(adur, lines[-1]["end"])
    fb = [int(round(s * FPS)) for s in starts] + [int(round(ends_voice * FPS))]
    shots = []
    for i, l in enumerate(lines):
        n = l["line"]
        shots.append(dict(n=n, f0=fb[i], f1=fb[i + 1]))
    tail_fr = int(round(a.tail * FPS))
    shots.append(dict(n=999, f0=fb[-1], f1=fb[-1] + tail_fr))
    specs.setdefault(999, dict(n=999, lay="e", T=[], g=[]))
    total = shots[-1]["f1"]
    limit = int(a.seconds * FPS) if a.seconds else None
    cache = ROOT / "cache/reality-check" / a.story
    cache.mkdir(parents=True, exist_ok=True)
    only = {int(x) for x in a.shots.split(",") if x}
    jobs, order = [], []
    for s in shots:
        if limit is not None and s["f0"] >= limit:
            continue
        f1 = s["f1"] if limit is None else min(s["f1"], limit)
        nfr = f1 - s["f0"]
        if nfr <= 0:
            continue
        sp = specs.get(s["n"])
        if sp is None:
            print("MISSING spec", s["n"])
            sys.exit(1)
        ex = ""
        md = sp.get('media') or {}
        for nm in (md.get('files') or [md.get('file')] or []):
            fp = find_footage(sd, s["n"], nm) if nm else None
            if fp:
                ex += fp.name + str(fp.stat().st_mtime_ns)
        if not ex:
            fp = find_footage(sd, s["n"])
            if fp:
                ex = fp.name + str(fp.stat().st_mtime_ns)
        out = cache / f"shot_{s['n']:03d}_{shot_hash(sp, nfr, ex)}.mp4"
        order.append(out)
        if not only or s["n"] in only:
            jobs.append((s["n"], sp, nfr, str(out), str(sd)))
    # remove stale clips of the same shot
    keep = {p.name for p in order}
    for p in cache.glob("shot_*.mp4"):
        if p.name not in keep and not p.name.endswith(".part.mp4") and (limit is None):
            p.unlink()
    t0 = time.time()
    todo = [j for j in jobs if not Path(j[3]).exists()]
    print(f"{len(jobs)} shots, {len(todo)} to render, {a.workers} workers", flush=True)
    res = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(render_shot, sorted(todo, key=lambda j: -j[2])):
            res.append(r)
            if r[2] != "ok":
                print("shot", r, flush=True)
            elif len(res) % 10 == 0:
                print(f"  {len(res)}/{len(todo)} done, {time.time() - t0:.0f}s", flush=True)
    bad = [r for r in res if r[2] != "ok"]
    if bad:
        print("FAILED", bad)
        sys.exit(1)
    rt = time.time() - t0
    vid_s = (limit if limit else total) / FPS
    print(f"render {rt:.0f}s for {len(todo)} shots; video {vid_s:.0f}s")
    if only:
        return
    lst = cache / ("list_test.txt" if limit else "list.txt")
    lst.write_text("".join(f"file '{p.name}'\n" for p in order), encoding="utf-8")
    out_dir = ld / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    name = a.name or (f"{a.story}_long_preview_test{int(a.seconds)}.mp4" if limit else f"{a.story}_long_preview.mp4")
    outp = out_dir / name
    T = vid_s
    music = ROOT / "shared/music/mystery_bed.wav"
    if not music.exists():
        music = Path("D:/my-tubes/shared/music/mystery_bed.wav")
    cmd = [find_ff(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(audio)]
    use_music = (not a.no_music) and music.exists()
    if use_music:
        cmd += ["-stream_loop", "-1", "-i", str(music)]
        fc = (f"[1:a]apad,atrim=0:{T:.3f},asetpts=N/SR/TB[v];[2:a]volume=0.6,afade=t=in:d=3,afade=t=out:st={max(T - 6, 0):.2f}:d=6,atrim=0:{T:.3f}[m];"
              f"[v][m]amix=inputs=2:duration=first:normalize=0[a]")
        cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-af", f"apad,atrim=0:{T:.3f}", "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{T:.3f}", "-movflags", "+faststart", str(outp)]
    subprocess.run(cmd, cwd=str(cache), check=True)
    print("OUT", outp, f"music={'yes' if use_music else 'no'} timing={tfile.name} audio={audio.name}")


if __name__ == "__main__":
    main()
