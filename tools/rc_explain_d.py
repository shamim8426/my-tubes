"""rc_explain scenes, part D: lines 97-124 (the push explained: sticky ball vs debris, beta, ejecta, unknowns, summary)."""
import math

import cv2
import numpy as np

import rc_build_long as B
from rc_explain import (scene, smooth, lin, seg, col, lerp, txt, txtw, blit, rock_spr, craft_spr, earth, sun, arrow, dotted, ring, flash, whiten,
                        particles, stars_bg, dial, put, text_spr, W, H, K, real, bar, view_seq)
from rc_explain_scenes import smooth_int, mixview, hm, place_rock
from rc_explain_b import at, until, inset, _ball_view

PUSH = "orange"   # 'ek dhakka' (craft) = strong orange; 'extra dhakka' (debris) = amber (lighter)
EXTRA = "gold"
L1 = 230.0


def _views(c, lines, fns, pre=0.0):
    """Hard-cut views starting at the given lines; fn(v, tt) with tt = seconds since the view began."""
    starts = [K(c, n, 0.0, -0.05) for n in lines[1:]]
    edges = [-1] + starts + [1e9]
    out = []
    for i, fn in enumerate(fns):
        a, b = edges[i], edges[i + 1]
        out.append((a, b, (lambda v, fn=fn, a=a: fn(v, c.T - max(a, 0.0)))))
    base = c.im.copy()
    view_seq(c, base, out)


# =============================================================================== lines 97-98: back to the question
@scene
def recap_dials(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    a1 = smooth(seg(T, 0.2, 0.8))
    dial(im, 520, 520, 230, 7.0 * smooth(seg(T, 0.4, 2.2)), "teal", a1, full=60.0)
    txt(im, "7 min ka hisaab", 520, 830, 56, "teal", "c", a1)
    a2 = at(c, 98, 0.0, 0.5, 0.6)
    dial(im, 1400, 520, 230, 33.0 * smooth(seg(T, K(c, 98, 0.45), K(c, 98, 0.45) + 2.0)), "orange", a2, full=60.0)
    txt(im, "33 min ka nateeja", 1400, 830, 56, "orange", "c", a2)
    txt(im, "wapas wahi sawaal", 960, 120, 56, "ink", "c", smooth(seg(T, 0.3, 1.0)))


# =============================================================================== lines 99-110: the push
def _pile(im, cx, cy, R, seed, T, jig=0.0, a=1.0, hole=None):
    rng = np.random.default_rng(seed)
    for i in range(160):
        ang, rr = rng.uniform(0, 6.283), math.sqrt(rng.uniform(0, 1)) * R * 0.92
        r = rng.uniform(R * 0.07, R * 0.16)
        x = cx + rr * math.cos(ang) + jig * math.sin(T * 9 + i)
        y = cy + rr * math.sin(ang) + jig * math.cos(T * 8 + i * 1.3)
        g = int(rng.uniform(95, 170))
        B.circ(im, x, y, r, B.mix((g - 10, g, g + 10), a), -1)
        B.circ(im, x, y, r, B.mix((g - 60, g - 50, g - 40), a * 0.8), 2)


def _sphere(im, x, y, r, T, tag=None):
    B.circ(im, x, y, r, (120, 112, 100), -1)
    B.circ(im, x, y, r, B.mix("teal", 0.9), 5)


def _v99(im, T):
    _ball_view(im, T, None)


def _v100(im, T):
    _ball_view(im, 3.6 + 0.0 * T, None)
    k = 0.6 + 0.4 * math.sin(T * 5)
    txt(im, "7 min ka hisaab: bilkul isi tarah", 960, 150, 56, "amber", "c", smooth(seg(T, 0.3, 0.9)))


def _v101(im, T):
    _pile(im, 960, 520, 300, 101, T, 2.0 * smooth(seg(T, 1.0, 1.4)) * 0.0 + 1.5)
    B.circ(im, 960, 520, 306, B.mix("teal", 0.9), 5)
    txt(im, "Dimorphos: patthron ka dheela dher", 960, 150, 54, "ink", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "chipakne wali gend nahi", 960, 930, 46, "red", "c", smooth(seg(T, 2.0, 2.8)))


def _v102(im, T):
    cx, cy = 1100, 540
    ti = 1.4
    d = max(T - ti, 0.0)
    _pile(im, cx + 12 * (1 - math.exp(-d * 2)), cy, 280, 101, T, 3.0 * (T > ti) * math.exp(-d))
    B.circ(im, cx + 12 * (1 - math.exp(-d * 2)), cy, 286, B.mix("teal", 0.9), 5)
    if T < ti:
        blit(im, craft_spr(), lerp(100, cx - 330, smooth(T / ti)), cy, 0.34, 0.0)
    else:
        flash(im, cx - 280, cy, d / 0.8, 260)
        particles(im, cx - 280, cy, d, 150, 5, (120, 620), (math.pi * 0.62, math.pi * 1.38), (3, 9), 0.8, 3.0, (170, 172, 180))
    txt(im, "takkar se bahut saari chattaan aur dhool uchhli", 960, 130, 48, "ink", "c", smooth(seg(T, 1.2, 2.0)))


def _v103(im, T):
    cx, cy = 1150, 560
    off = 70 * (1 - math.exp(-T * 0.8))
    _pile(im, cx + off, cy, 240, 101, T, 1.0)
    B.circ(im, cx + off, cy, 246, B.mix("teal", 0.9), 5)
    particles(im, cx + off - 240, cy, (T % 3.0) + 0.1, 70, 7, (150, 520), (math.pi * 0.7, math.pi * 1.3), (3, 7), 0.7, 3.0, (170, 172, 180))
    k = smooth(seg(T, 1.0, 1.8))
    arrow(im, cx - 260, 230, cx - 560, 230, "grey", 7, k, 28, k)
    txt(im, "malba is taraf", cx - 410, 180, 38, "grey", "c", k)
    arrow(im, cx - 40, 230, cx + 330, 230, EXTRA, 11, k, 34, k)
    txt(im, "peeche dhakka: extra dhakka", cx + 150, 180, 42, EXTRA, "c", k)
    # rocket analogy inset
    a = smooth(seg(T, 3.0, 3.8))
    B.rrect(im, 140, 600, 700, 900, 24, (10, 12, 26), 0.8 * a)
    rx = 330 + 160 * ((T * 0.5) % 1.0)
    B.polyf(im, [(rx, 740), (rx + 130, 740), (rx + 170, 770), (rx + 130, 800), (rx, 800)], B.mix("ink", a))
    for i in range(14):
        ph = (T * 2 + i * 0.07) % 1.0
        B.circ(im, rx - ph * 140, 770 + 8 * math.sin(i * 3 + T * 8), 6 + 12 * ph, B.mix((60, 150, 255), a * (1 - ph)), -1)
    txt(im, "jaise rocket ka dhuaan rocket ko aage dhakelta hai", 420, 850, 28, "ink", "c", a, panel=False)


def _arrows(im, y, n_first, n_extra, T, k=1.0, lab=True, x0=300):
    a1 = min(n_first, 1.0) * L1
    kk = smooth(seg(T, 0.2, 0.9)) * k
    arrow(im, x0, y, x0 + a1, y, PUSH, 16, kk, 38, kk)
    if lab:
        txt(im, "ek dhakka", x0 + a1 / 2, y - 55, 36, PUSH, "c", kk)
    if n_extra > 0:
        k2 = smooth(seg(T, 1.0, 1.8)) * k
        x1 = x0 + a1
        arrow(im, x1 + 6, y, x1 + 6 + n_extra * L1, y, EXTRA, 16, k2, 38, k2)
        txt(im, "+ extra dhakka", x1 + n_extra * L1 / 2, y - 55, 36, EXTRA, "c", k2)


def _v104(im, T):
    _arrows(im, 460, 1, 1.4, T)
    k = smooth(seg(T, 2.2, 3.0))
    x0, x1 = 300, 300 + L1 * 2.4
    B.line(im, x0, 540, x1 * k + x0 * (1 - k), 540, B.mix("ink", k), 4)
    txt(im, "kul dhakka = yaan ka + malbe ka", (x0 + x1) / 2, 600, 46, "ink", "c", k)
    txt(im, "yahi hai 33 min ka raaz", 960, 880, 60, "amber", "c", smooth(seg(T, 4.5, 5.3)))
    _ball_small(im, 1500, 360, T)


def _ball_small(im, x, y, T):
    B.circ(im, x, y, 90, (120, 112, 100), -1)
    B.circ(im, x, y, 90, B.mix("teal", 0.9), 4)
    d = (T * 0.8) % 1.0
    for i in range(10):
        ph = (d + i * 0.1) % 1.0
        B.circ(im, x - 90 - ph * 120, y + 30 * math.sin(i * 2), 4, B.mix((170, 175, 185), 1 - ph), -1)
    arrow(im, x + 10, y - 120, x + 190, y - 120, PUSH, 8, 1.0, 22, 1.0)
    arrow(im, x + 190, y - 120, x + 330, y - 120, EXTRA, 8, 1.0, 22, 1.0)


def _v105(im, T):
    txt(im, "is extra dhakke ko naapne wali sankhya: BETA", 960, 130, 52, "amber", "c", smooth(seg(T, 0.2, 0.9)))
    txt(im, "beta = kul dhakka / yaan ka dhakka", 960, 230, 44, "ink", "c", smooth(seg(T, 1.0, 1.7)))
    _arrows(im, 520, 1, 0.0, T - 1.5)
    k = smooth(seg(T, 3.4, 4.2))
    txt(im, "beta = 1  (sirf yaan ka dhakka)", 960, 780, 66, "orange", "c", k)


def _v106(im, T):
    _arrows(im, 520, 1, 2.6, T)
    txt(im, "beta ~ 3.6", 960, 250, 100, "gold", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "agar dono pindon ka ghanatva barabar maanein", 960, 800, 44, "ink", "c", smooth(seg(T, 2.0, 2.8)))
    B.line(im, 300, 610, 300 + L1 * 3.6 * smooth(seg(T, 2.0, 3.2)), 610, "ink", 4)
    txt(im, "3.6 guna", 300 + L1 * 1.8, 660, 38, "ink", "c", smooth(seg(T, 2.8, 3.4)), panel=False)


def _v107(im, T):
    x0 = 300
    B.line(im, x0, 560, x0 + L1 * 5, 560, B.mix("dim", 0.9), 5)
    for b in range(0, 6):
        B.line(im, x0 + b * L1, 540, x0 + b * L1, 580, "ink", 4)
        txt(im, str(b), x0 + b * L1, 625, 30, "ink", "c", 1.0, panel=False)
    k = smooth(seg(T, 0.5, 2.0))
    xa, xb = x0 + 2.2 * L1, x0 + 4.9 * L1
    B.rrect(im, xa, 520, xa + (xb - xa) * k, 600, 16, EXTRA, 0.45)
    B.rrect(im, xa, 520, xa + (xb - xa) * k, 600, 16, EXTRA, 0.95, False, 4)
    txt(im, "ghanatva tay nahi: beta ek range", 960, 200, 56, "amber", "c", smooth(seg(T, 0.2, 0.8)))
    txt(im, "2.2 se 4.9", (xa + xb) / 2, 460, 70, "gold", "c", k)


def _v108(im, T):
    _arrows(im, 480, 1, 1.2, T)
    _arrows(im, 700, 1, 4.0, T - 0.6)
    txt(im, "kul dhakka: yaan ke dhakke ka lagbhag 2 se 5 guna", 960, 900, 52, "amber", "c", smooth(seg(T, 3.0, 3.8)))
    txt(im, "malbe ka dhakka khud yaan se bada tha", 960, 150, 48, "ink", "c", smooth(seg(T, 0.4, 1.2)))


def _v109(im, T):
    x0 = 260
    B.line(im, x0, 540, x0 + 1400, 540, B.mix("dim", 0.9), 4)
    for i in range(0, 15):
        B.line(im, x0 + i * 100, 525, x0 + i * 100, 555, "ink", 3)
    txt(im, "1 second mein badlav: ~2.7 millimetre", 960, 200, 52, "amber", "c", smooth(seg(T, 0.3, 1.0)))
    k = smooth(seg(T, 1.0, 5.0))
    B.circ(im, x0 + 27 * k * 1.0, 540, 12, "orange", -1)
    txt(im, "2.7 mm/s", 960, 760, 100, "orange", "c", smooth(seg(T, 0.8, 1.5)))
    txt(im, "(rafataar 22,000 km/h ke saamne ek zarra)", 960, 880, 36, "grey", "c", smooth(seg(T, 2.5, 3.2)))


def _v110(im, T):
    cx, cy = 600, 560
    place_rock(im, cx, cy, 120, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    r = 330
    B.ell(im, cx, cy, r, r * 0.85, B.mix("dim", 0.6), 2)
    w0 = 2 * math.pi / 4.0
    lap = T / 4.0
    ga = w0 * T
    ra = w0 * T * 1.045
    gx, gy = cx + r * math.cos(ga), cy + r * 0.85 * math.sin(ga)
    rx_, ry_ = cx + r * math.cos(ra), cy + r * 0.85 * math.sin(ra)
    place_rock(im, gx, gy, 24, 5, ga, 0.45)
    place_rock(im, rx_, ry_, 26, 5, ra)
    B.line(im, gx, gy, rx_, ry_, B.mix("red", 0.9), 3)
    txt(im, "bina dhakke ke", gx, gy + 54, 24, "grey", "c", 0.9, panel=False)
    gap = (ra - ga) / (2 * math.pi) * 715
    txt(im, "chhota dhakka, chakkar-dar-chakkar judta jaata hai", 1360, 250, 40, "ink", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, f"chakkar: {int(lap) + 1}", 1360, 420, 54, "amber", "c", 1.0)
    txt(im, f"farq: {int(min(gap * 0.36, 33))} min" if lap < 4.0 else "farq: 33 min", 1360, 540, 70, "red", "c", 1.0)


@scene
def push_full(c, **p):
    stars_bg(c)
    _views(c, [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
           [_v99, _v100, _v101, _v102, _v103, _v104, _v105, _v106, _v107, _v108, _v109, _v110])


# =============================================================================== lines 111-114: the ejecta
def _e111(im, T):
    cx, cy = 560, 560
    place_rock(im, cx, cy, 110, 2, 0.0)
    k = smooth(seg(T, 0.4, 5.0))
    ov = im.copy()
    cv2.fillPoly(ov, [np.array([[cx + 40, cy - 20], [cx + 40 + 1100 * k, cy - 120 - 330 * k], [cx + 40 + 1250 * k, cy + 150 + 120 * k * 0 + 80 * k]], np.int32)], (170, 190, 215))
    cv2.addWeighted(ov, 0.28, im, 0.72, 0, dst=im)
    rng = np.random.default_rng(111)
    for i in range(110):
        u = rng.random() * k
        ang = rng.uniform(-0.6, 0.45)
        B.circ(im, cx + 60 + 1100 * u * math.cos(ang), cy - 60 + 1000 * u * math.sin(ang) * 0.6, 3, B.mix((200, 205, 215), 0.7 * (1 - u)), -1)
    txt(im, "Hubble ne ye sab hote dekha", 960, 130, 52, "ink", "c", smooth(seg(T, 0.2, 0.9)))
    txt(im, "2 ghante ke andar: dhool ka shankhu", 960, 940, 46, "amber", "c", smooth(seg(T, 1.0, 1.8)))


def _e112(im, T):
    cx, cy = 600, 600
    place_rock(im, cx, cy, 70, 2, 0.0)
    txt(im, "17 ghante baad: ghoomta pinwheel", 960, 130, 48, "ink", "c", smooth(seg(T, 0.2, 0.8)))
    for arm in range(2):
        for i in range(120):
            u = i / 120
            ang = arm * math.pi + u * 5.0 + T * 0.35
            rr = 30 + u * 380 * smooth(seg(T, 0.3, 3.0))
            B.circ(im, cx + rr * math.cos(ang) * 1.0, cy + rr * math.sin(ang) * 0.9, 3 + 3 * (1 - u), B.mix((200, 210, 225), 0.7 * (1 - u * 0.7)), -1)
    k = smooth(seg(T, 3.6, 5.0))
    if k > 0.01:
        ov = im.copy()
        cv2.fillPoly(ov, [np.array([[cx + 60, cy - 30], [1780, cy - 380], [1780, cy - 160]], np.int32)], (180, 195, 220))
        cv2.addWeighted(ov, 0.3 * k, im, 1 - 0.3 * k, 0, dst=im)
        txt(im, "phir hafton tak dhoomketu jaisi poonchh", 1300, 900, 44, "amber", "c", k)


def _e113(im, T):
    txt(im, "kitna malba uchhla?", 960, 130, 52, "ink", "c", smooth(seg(T, 0.2, 0.8)))
    k = smooth(seg(T, 0.6, 3.0))
    n = int(40 * k)
    for i in range(n):
        x, y = 300 + (i % 10) * 90, 640 - (i // 10) * 90
        B.rrect(im, x, y, x + 74, y + 74, 8, (120, 130, 150), 0.95)
    txt(im, f"NASA: 1,000 ton se zyada", 960, 820, 66, "amber", "c", smooth(seg(T, 2.0, 2.8)))
    txt(im, "(har dibba = 25 ton, sirf paimaana)", 960, 930, 30, "grey", "c", smooth(seg(T, 2.6, 3.2)), panel=False)


def _e114(im, T):
    x0, x1 = 260, 1660
    B.line(im, x0, 560, x1, 560, B.mix("dim", 0.9), 5)
    marks = [(1000, "1,000"), (6000, "6,000+"), (11000, "11,000"), (55000, "55,000 ton")]
    def X(v):
        return lerp(x0, x1, math.log10(v / 500.0) / math.log10(120))
    for v, lab in marks:
        B.line(im, X(v), 540, X(v), 580, "ink", 4)
        txt(im, lab, X(v), 630, 30, "ink", "c", 1.0, panel=False)
    k = smooth(seg(T, 0.6, 2.2))
    B.rrect(im, X(11000), 520, X(11000) + (X(55000) - X(11000)) * k, 600, 14, "red", 0.4)
    B.rrect(im, X(11000), 520, X(11000) + (X(55000) - X(11000)) * k, 600, 14, "red", 0.95, False, 4)
    B.circ(im, X(1000), 560, 14, "amber", -1)
    B.circ(im, X(6000), 560, 14, "orange", -1)
    txt(im, "doosre adhyayan: 6,000 ton se upar, kuch 11,000 se 55,000 ton tak", 960, 330, 42, "ink", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "ek sankhya nahi, ek range", 960, 860, 60, "red", "c", smooth(seg(T, 2.4, 3.2)))


@scene
def ejecta(c, **p):
    stars_bg(c)
    _views(c, [111, 112, 113, 114], [_e111, _e112, _e113, _e114])


# =============================================================================== lines 115-118: why the range is wide / unknown mass
def _m115(im, T):
    txt(im, "beta ki range itni chaudi kyon?", 960, 150, 60, "amber", "c", smooth(seg(T, 0.2, 0.9)))
    x0 = 300
    B.line(im, x0, 560, x0 + L1 * 5, 560, B.mix("dim", 0.9), 5)
    k = 0.5 + 0.5 * math.sin(T * 2)
    xa, xb = x0 + (2.2 + 0.4 * k) * L1, x0 + (4.9 - 0.4 * k) * L1
    B.rrect(im, xa, 520, xb, 600, 16, EXTRA, 0.4)
    txt(im, "?", (xa + xb) / 2, 560, 90, "red", "c", 0.9, panel=False)


def _m116(im, T):
    cx, cy = 960, 560
    place_rock(im, cx, cy, 190, 2, T * 0.03, 1.0, 1.0, (1.0, 0.9))
    sc_x = cx + 450
    tilt = 0.12 * math.sin(T * 1.2)
    B.line(im, sc_x - 150, 440 - tilt * 150, sc_x + 150, 440 + tilt * 150, "ink", 5)
    B.line(im, sc_x, 440, sc_x, 700, "ink", 5)
    B.circ(im, sc_x - 150, 460 - tilt * 150, 34, B.mix("dim", 0.8), 3)
    txt(im, "?", sc_x - 150, 460 - tilt * 150, 50, "red", "c", 1.0, panel=False)
    txt(im, "Dimorphos ka asli dravyaman (kitna bhaari)? anjaan", 960, 150, 50, "red", "c", smooth(seg(T, 0.2, 0.9)))


def _m117(im, T):
    txt(im, "andar se kitna thos hai? abhi pata nahi", 960, 150, 52, "ink", "c", smooth(seg(T, 0.2, 0.9)))
    for x, lab, pile in ((520, "thos pind?", False), (1400, "patthron ka dher?", True)):
        B.circ(im, x, 560, 240, (60, 70, 90), -1)
        if pile:
            _pile(im, x, 560, 235, 117, T, 1.5)
        else:
            B.circ(im, x, 560, 235, (130, 122, 110), -1)
        B.circ(im, x, 560, 240, B.mix("teal", 0.9), 5)
        txt(im, "?", x, 560, 130, "red", "c", 0.6 + 0.4 * math.sin(T * 4 + x), panel=False)
        txt(im, lab, x, 860, 42, "ink", "c", smooth(seg(T, 0.8, 1.5)))


def _m118(im, T):
    B.rrect(im, 260, 300, 940, 700, 28, (12, 20, 30), 0.85)
    txt(im, "33 min", 600, 430, 110, "green", "c", 1.0, panel=False)
    txt(im, "naapa hua nateeja", 600, 560, 42, "ink", "c", 1.0, panel=False)
    B.circ(im, 600, 630, 24, "green", -1)
    k = smooth(seg(T, 1.0, 2.0))
    B.rrect(im, 980, 300, 1660, 700, 28, (24, 20, 20), 0.85)
    for i in range(24):
        a_ = i / 24 * 6.283
        B.line(im, 1320 + 300 * math.cos(a_), 500 + 190 * math.sin(a_), 1320 + 300 * math.cos(a_ + 0.15), 500 + 190 * math.sin(a_ + 0.15), B.mix("grey", 0.7), 3)
    txt(im, "peeche ka hisaab", 1320, 460, 46, "grey", "c", k, panel=False)
    txt(im, "abhi poora band nahi hua", 1320, 540, 42, "amber", "c", k, panel=False)


@scene
def mass_unknown(c, **p):
    stars_bg(c)
    _views(c, [115, 116, 117, 118], [_m115, _m116, _m117, _m118])


# =============================================================================== lines 119-121: orbit round the Sun
@scene
def solar_orbit(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    sun(im, 540, 560, 60, T, 1.0)
    for rr, cc_ in ((160, "dim"), (260, "dim"), (380, "teal")):
        B.ell(im, 540, 560, rr, rr * 0.92, B.mix(cc_, 0.6), 2)
    ang = T * 0.5 + 1.0
    px, py = 540 + 380 * math.cos(ang), 560 + 380 * 0.92 * math.sin(ang)
    place_rock(im, px, py, 14, 2, ang)
    place_rock(im, px + 22, py - 8, 7, 5, ang)
    txt(im, "poori jodi ka suraj ke charon taraf chakkar", 960, 120, 48, "ink", "c", at(c, 119, 0.2, 0, 0.6))
    k = at(c, 120, 0.3, 0, 0.8)
    if k > 0.01:
        mx, my, mr = 1450, 560, 270
        B.circ(im, mx, my, mr, (14, 18, 34), -1)
        B.circ(im, mx, my, mr, B.mix("ink", 0.9 * k), 4)
        B.line(im, px + 30, py, mx - mr * 0.7, my - 120, B.mix("dim", 0.5 * k), 2)
        B.line(im, mx - mr + 30, my + 60, mx + mr - 30, my + 60 - 0, B.mix("grey", k), 5)
        dd = 22 * smooth(seg(T, K(c, 120, 0.4), K(c, 120, 0.4) + 2.0))
        B.line(im, mx - mr + 30, my + 60 - dd, mx + mr - 30, my + 60 - dd - 4, B.mix("amber", k), 5)
        txt(im, "badlav ~0.15 s", mx, my - 80, 58, "amber", "c", k)
        txt(im, "(seconds ka dasva hissa)", mx, my + 190, 30, "grey", "c", k, panel=False)
    k2 = at(c, 121, 0.45, 0, 0.7)
    txt(im, "itna chhota ki khatre par koi asar nahi", 960, 960, 46, "green", "c", k2)


# =============================================================================== lines 122-124: so far, in short
@scene
def summary3(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    items = [("1", "7 min ki jagah 33: malbe ne bhi dhakka diya", 122, 0.15), ("2", "Dimorphos ka dravyaman anjaan", 123, 0.05), ("3", "dhundhna baaki, rokne ke tareeke bhi", 123, 0.5)]
    txt(im, "ab tak ka hisaab, chhote mein", 960, 130, 56, "amber", "c", at(c, 122, 0.0, 0, 0.6))
    for i, (n, t, ln, fr) in enumerate(items):
        a = at(c, ln, fr, 0, 0.6)
        y = 330 + i * 190
        B.rrect(im, 260, y - 70, 1660, y + 70, 28, (14, 18, 36), 0.85 * a)
        B.circ(im, 360, y, 42, B.mix("amber", a), -1)
        txt(im, n, 360, y, 54, "dark", "c", a, panel=False)
        txt(im, t, 450, y, 46, "ink", "l", a, panel=False)
        # tiny moving icon on the right
        ix = 1560
        if i == 0:
            arrow(im, ix - 70, y, ix - 10, y, PUSH, 8, a, 20, a)
            arrow(im, ix - 10, y, ix + 50, y, EXTRA, 8, a, 20, a)
        elif i == 1:
            B.circ(im, ix, y, 38, B.mix("teal", a), 4)
            txt(im, "?", ix, y, 48, "red", "c", a * (0.6 + 0.4 * math.sin(T * 4)), panel=False)
        else:
            B.ell(im, ix, y + 10, 40, 20, B.mix("ink", a), 4, -30)
    k = at(c, 124, 0.0, 0, 0.6)
    if k > 0.01:
        ov = im.copy()
        cv2.rectangle(ov, (0, 0), (W, H), (8, 10, 22), -1)
        cv2.addWeighted(ov, 0.92 * k, im, 1 - 0.92 * k, 0, dst=im)
        txt(im, "ab aakhri hissa", 960, 420, 80, "amber", "c", k)
        txt(im, "agar sach mein koi pind aata mile, to hamare paas kya tareeke hain?", 960, 560, 40, "ink", "c", at(c, 124, 0.3, 0, 0.6))
