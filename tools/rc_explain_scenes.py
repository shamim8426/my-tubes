"""Scene functions for rc_explain (registered into rc_explain.SCENES). One idea per scene, constant motion, small overlay text only."""
import math

import cv2
import numpy as np

import rc_build_long as B
import rc_explain as E
from rc_explain import (SCENES, scene, smooth, lin, seg, col, lerp, txt, txtw, blit, rock_spr, craft_spr, earth, sun, arrow, dotted, ring, flash, whiten,
                        particles, stars_bg, dial, put, text_spr, W, H)


def smooth_int(x):
    """Integral of smoothstep over 0..x (x may exceed 1)."""
    x = max(x, 0.0)
    if x <= 1:
        return x ** 3 - x ** 4 / 2
    return 0.5 + (x - 1)


def mixview(c, base, fn, a):
    if a <= 0.003:
        return
    v = base.copy()
    fn(v)
    if a >= 0.997:
        c.im[:] = v
    else:
        cv2.addWeighted(c.im, 1 - a, v, a, 0, dst=c.im)


def hm(minutes):
    m = int(round(minutes))
    return f"{m // 60} h {m % 60:02d} min"


def place_rock(im, x, y, R, seed=2, rot=0.0, a=1.0, tone=1.0, elong=(1, 1), warm=0.0):
    spr = rock_spr(seed, 460, tone, elong, warm)
    blit(im, spr, x, y, R / 200.0, rot, a)


# =============================================================================== DHAKKA (lines 4-8): push explained as motion
DM_TI = 2.3           # impact time in the hit view
DM_HIT = (1150, 560)  # rock centre at impact
DM_V0 = (190.0, -65.0)
DM_V1 = (330.0, -22.0)
DM_R = 150.0


def _dm_rock_pos(T):
    if T < DM_TI:
        return DM_HIT[0] + DM_V0[0] * (T - DM_TI), DM_HIT[1] + DM_V0[1] * (T - DM_TI)
    d = T - DM_TI
    return DM_HIT[0] + DM_V1[0] * d, DM_HIT[1] + DM_V1[1] * d


def _hit_view(im, T, c):
    rx, ry = _dm_rock_pos(T)
    p0 = _dm_rock_pos(0.0)
    # original path (dotted grey) through the hit point, ahead of the rock
    far = (DM_HIT[0] + DM_V0[0] * 8, DM_HIT[1] + DM_V0[1] * 8)
    dotted(im, [p0, far], "grey", 3, 0.8 * smooth(seg(T, 0.2, 0.8)), 14, 14)
    if T > DM_TI + 0.2:
        txt(im, "pehle ka raasta", 1720, DM_HIT[1] + DM_V0[1] * 6 - 50, 32, "grey", "r", smooth(seg(T, DM_TI + 0.6, DM_TI + 1.2)))
    # new path: amber trail behind the rock + dotted ahead
    if T > DM_TI:
        pts = [(DM_HIT[0], DM_HIT[1]), (rx, ry)]
        B.polyl(im, pts, B.mix("amber", 0.95), 6)
        ahead = (rx + DM_V1[0] * 3, ry + DM_V1[1] * 3)
        dotted(im, [(rx, ry), ahead], "amber", 4, 0.8, 16, 12)
    place_rock(im, rx, ry, DM_R, 2, T * 0.05)
    # craft flying in
    cx = DM_HIT[0] - DM_R * 0.9 - 20 + 640 * (T - DM_TI)
    if T < DM_TI:
        for k in range(10):
            yy = DM_HIT[1] - 30 + k * 7
            B.line(im, cx - 40 - 200 - k * 30, yy, cx - 40, yy, B.mix("white", 0.10 + 0.01 * k), 2)
        blit(im, craft_spr(), cx, DM_HIT[1], 0.42, 0.0)
        a = smooth(seg(T, 0.3, 0.9)) * (1 - smooth(seg(T, DM_TI - 0.4, DM_TI - 0.05)))
        txt(im, "DART yaan", cx, DM_HIT[1] - 150, 36, "ink", "c", a)
        txt(im, "22,000 km/h", cx, DM_HIT[1] + 150, 34, "amber", "c", a)
    else:
        d = T - DM_TI
        if d < 0.35:
            blit(im, craft_spr(), DM_HIT[0] - DM_R * 0.9 - 20 + 20 * d, DM_HIT[1], 0.42 * (1 - 0.5 * d / 0.35), 0.0, 1 - d / 0.35)
        flash(im, DM_HIT[0] - DM_R * 0.85, DM_HIT[1], d / 0.9, 260)
        particles(im, DM_HIT[0] - DM_R * 0.85, DM_HIT[1], d, 40, 11, (80, 330), (math.pi * 0.62, math.pi * 1.38), (2, 5), 1.6, 1.8, (190, 195, 205))
        # push arrow on the rock
        k = smooth(seg(T, DM_TI + 0.3, DM_TI + 0.9))
        arrow(im, rx - 20, ry - DM_R - 40, rx + 190, ry - DM_R - 40, "amber", 8, k, 30, k)
        txt(im, "yaan ka dhakka", rx + 90, ry - DM_R - 95, 38, "amber", "c", k)
        txt(im, "raasta thoda mud gaya", rx, ry + DM_R + 70, 34, "ink", "c", smooth(seg(T, DM_TI + 1.2, DM_TI + 1.8)))


def _orbit_view(im, T, c):
    cx, cy, RD = 600, 560, 165
    t0 = 4.7
    place_rock(im, cx, cy, RD, 5, T * 0.04, 1.0, 1.0, (1.0, 0.88))
    R0 = 365
    ring(im, cx, cy, R0, "grey", 2, 0.6, 14)
    rr = R0 - 30 * smooth(seg(T, t0, 11.0))
    ring(im, cx, cy, rr, "amber", 3, 0.9 * smooth(seg(T, t0 + 0.2, t0 + 1.0)))
    w0 = 2 * math.pi / 7.0
    th = w0 * T + w0 * 0.35 * (smooth_int(seg(T, t0, 11.0) ) * 6.3)
    mx, my = cx + rr * math.cos(th), cy + rr * math.sin(th) * 0.92
    # moon trail
    for k in range(1, 26):
        tt = T - k * 0.03
        thk = w0 * tt + w0 * 0.35 * (smooth_int(seg(tt, t0, 11.0)) * 6.3)
        B.circ(im, cx + rr * math.cos(thk), cy + rr * math.sin(thk) * 0.92, 11 * (1 - k / 28), B.mix("amber", 0.35 * (1 - k / 26)), -1)
    place_rock(im, mx, my, 44, 9, th * 2)
    txt(im, "Didymos", cx, cy + RD + 55, 32, "grey", "c", 0.9)
    txt(im, "Dimorphos", mx, my - 80, 32, "ink", "c", 0.95)
    # right panel: orbit time counter + dial
    M = 715 - 7 * smooth(seg(T, 4.9, 8.0)) - 26 * smooth(seg(T, 8.2, 10.9))
    px = 1470
    txt(im, "Dimorphos ka ek chakkar", px, 250, 36, "ink", "c", smooth(seg(T, 4.6, 5.2)))
    txt(im, hm(M), px, 330, 64, "amber", "c", smooth(seg(T, 4.6, 5.2)), panel=True)
    ddmin = 7 * smooth(seg(T, 4.9, 8.0)) + 26 * smooth(seg(T, 8.2, 10.9))
    a = smooth(seg(T, 5.0, 5.8))
    dcol = "amber" if T < 8.2 else "orange"
    dial(im, px, 700, 170, ddmin, dcol, a, hand=True)
    txt(im, f"{int(round(ddmin))} min kam", px, 930, 44, dcol, "c", a)
    if T > 10.9:
        txt(im, "7 + ? = 33", px, 995, 38, "red", "c", smooth(seg(T, 11.4, 12.0)))
    if T > 11.6:
        k = 0.5 + 0.5 * math.sin(T * 6)
        ring(im, mx, my, 68 + 6 * k, "red", 4, 0.9 * smooth(seg(T, 11.6, 12.2)))


def _eject_view(im, T, c):
    rx, ry, R = 1120, 560, 200
    d = T - 14.0
    push = 14 * smooth(seg(T, 14.1, 15.5))
    place_rock(im, rx + push, ry, R, 2, 0.1)
    ix, iy = rx - R * 0.93, ry
    flash(im, ix, iy, d / 0.8, 240)
    particles(im, ix + push, iy, d, 110, 21, (160, 640), (math.pi * 0.66, math.pi * 1.34), (2, 7), 0.9, 3.6, (180, 186, 196))
    k = smooth(seg(T, 14.8, 15.6))
    if k > 0:
        pulse = 0.5 + 0.5 * math.sin(T * 7)
        arrow(im, rx + push + R * 0.2, ry, rx + push + R * 1.25, ry, "red", 10, k, 34, k)
        txt(im, "extra dhakka?", rx + push + R * 0.2, ry - R - 50, 42, "red", "c", k * (0.75 + 0.25 * pulse))
    txt(im, "malba bhi dhakka deta hai?", 960, 940, 36, "ink", "c", smooth(seg(T, 14.5, 15.2)))


def _dials_view(im, T, c):
    r = 190
    cy = 520
    # dial 1: 73 s (1.217 min on a 60-min dial)
    k_move = smooth(seg(T, 20.0, 20.9))
    x1 = lerp(960, 420, k_move)
    r1 = lerp(250, r, k_move)
    a1 = smooth(seg(T, 16.7, 17.3))
    v1 = 73 / 60.0 * smooth(seg(T, 17.0, 19.4))
    dial(im, x1, cy, r1, v1, "amber", a1)
    txt(im, "73 s", x1, cy + r1 + 70, 56, "amber", "c", a1)
    txt(im, "NASA ka minimum target", x1, cy + r1 + 135, 30, "grey", "c", smooth(seg(T, 18.2, 18.8)))
    # dial 2: 7 min
    a2 = smooth(seg(T, 24.2, 24.8))
    v2 = 7 * smooth(seg(T, 24.4, 26.0))
    dial(im, 960, cy, r, v2, "teal", a2)
    txt(im, "7 min", 960, cy + r + 70, 56, "teal", "c", a2)
    txt(im, "sirf yaan ka dhakka", 960, cy + r + 135, 30, "grey", "c", smooth(seg(T, 25.0, 25.6)))
    a3 = smooth(seg(T, 25.9, 26.5))
    v3 = 33 * smooth(seg(T, 26.0, 28.3))
    dial(im, 1500, cy, r, v3, "orange", a3)
    txt(im, "33 min", 1500, cy + r + 70, 56, "orange", "c", a3)
    txt(im, "asli nateeja", 1500, cy + r + 135, 30, "grey", "c", smooth(seg(T, 27.0, 27.6)))
    txt(im, "ek dial = 60 min", 960, 110, 30, "grey", "c", smooth(seg(T, 17.0, 17.6)) * 0.9)


@scene
def dhakka_main(c, **p):
    stars_bg(c)
    base = c.im.copy()
    T = c.T
    mixview(c, base, lambda v: _hit_view(v, T, c), 1.0 - smooth(seg(T, 4.35, 4.95)))
    mixview(c, base, lambda v: _orbit_view(v, T, c), smooth(seg(T, 4.35, 4.95)) * (1 - smooth(seg(T, 13.5, 14.0))))
    mixview(c, base, lambda v: _eject_view(v, T, c), smooth(seg(T, 13.5, 14.0)) * (1 - smooth(seg(T, 16.2, 16.7))))
    mixview(c, base, lambda v: _dials_view(v, T, c), smooth(seg(T, 16.2, 16.7)))
