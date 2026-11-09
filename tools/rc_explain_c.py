"""rc_explain scenes, part C: lines 63-96 (find it first, survey numbers, goals, NEO Surveyor, 2024 YR4, Apophis)."""
import math

import cv2
import numpy as np

import rc_build_long as B
from rc_explain import (scene, smooth, lin, seg, col, lerp, txt, txtw, blit, rock_spr, craft_spr, earth, sun, arrow, dotted, ring, flash, whiten,
                        particles, stars_bg, dial, put, text_spr, W, H, K, real, bar, view_seq)
from rc_explain_scenes import smooth_int, mixview, hm, place_rock
from rc_explain_b import at, until, inset


def _sky_dots(im, T, n, seed, lit_frac, x0, y0, x1, y1, cols, rad, c_on="green", c_off="dim", reveal=1.0, pulse=True):
    rng = np.random.default_rng(seed)
    rows = int(math.ceil(n / cols))
    order = rng.permutation(n)
    dx, dy = (x1 - x0) / cols, (y1 - y0) / rows
    for i in range(n):
        x, y = x0 + (i % cols + 0.5) * dx, y0 + (i // cols + 0.5) * dy
        rank = np.where(order == i)[0][0] / n
        on = rank < lit_frac and rank < reveal
        if on:
            B.circ(im, x, y, rad, B.mix(c_on, 0.95), -1)
        else:
            B.circ(im, x, y, rad * 0.8, B.mix(c_off, 0.55), -1)


# =============================================================================== lines 63-66: finding comes first
def _v63(im, T, c):
    rng = np.random.default_rng(63)
    for i in range(90):
        x, y = rng.uniform(100, 1820), rng.uniform(160, 900)
        B.circ(im, x, y, 3, B.mix("ink", 0.5), -1)
    sx = lerp(100, 1820, (T * 0.2) % 1.0)
    B.line(im, sx, 150, sx, 920, B.mix("green", 0.7), 3)
    for q in range(12):
        B.line(im, sx - q * 6, 150, sx - q * 6, 920, B.mix("green", 0.06), 6)
    place_rock(im, lerp(300, 1600, seg(T, 0.5, 4.5)), 540, 24, 5, T)
    txt(im, "pehle dhundhna, phir dhakka", 960, 110, 56, "amber", "c", smooth(seg(T, 0.3, 1.0)))


def _v64(im, T, c):
    B.rrect(im, 560, 300, 1360, 700, 30, (14, 18, 34), 0.8)
    txt(im, "2016", 960, 420, 120, "amber", "c", 1.0, panel=False)
    txt(im, "NASA ka Planetary Defense Coordination Office", 960, 540, 38, "ink", "c", smooth(seg(T, 0.5, 1.1)), panel=False)
    txt(im, "kaam: aise khatron par nazar", 960, 610, 36, "grey", "c", smooth(seg(T, 1.2, 1.8)), panel=False)
    ex, ey = 960, 820
    B.ell(im, ex, ey, 70, 36, "ink", 4)
    B.circ(im, ex + 8 * math.sin(T * 1.5), ey, 18, "amber", -1)


def _v65(im, T, c):
    names = ["Catalina", "Pan-STARRS", "ATLAS"]
    for i, nm in enumerate(names):
        x = 420 + i * 540
        a = smooth(seg(T, 0.3 + 0.7 * i, 1.0 + 0.7 * i))
        B.polyf(im, [(x - 60, 760), (x + 60, 760), (x, 640)], B.mix("dim", a))
        B.ell(im, x, 636, 34, 14, B.mix("ink", a), 4, -35)
        sw = math.sin(T * 1.2 + i) * 0.3
        ang = math.radians(-90) + sw
        ov = im.copy()
        cv2.fillPoly(ov, [np.array([[x, 636], [x + 520 * math.cos(ang - 0.28), 636 + 520 * math.sin(ang - 0.28)], [x + 520 * math.cos(ang + 0.28), 636 + 520 * math.sin(ang + 0.28)]], np.int32)], (110, 160, 90))
        cv2.addWeighted(ov, 0.22 * a, im, 1 - 0.22 * a, 0, dst=im)
        txt(im, nm, x, 830, 38, "ink", "c", a)
    txt(im, "survey teleskope aasman chhaante hain", 960, 130, 50, "amber", "c", smooth(seg(T, 0.2, 0.9)))


def _frame(im, x, y, w, h, T, moved, lab, a=1.0):
    B.rrect(im, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 16, (10, 12, 26), 0.95 * a)
    rng = np.random.default_rng(66)
    for i in range(45):
        B.circ(im, x - w / 2 + 20 + rng.random() * (w - 40), y - h / 2 + 20 + rng.random() * (h - 40), 2.3, B.mix("ink", 0.75 * a), -1)
    px = x - w * 0.18 + moved * w * 0.3
    B.circ(im, px, y + 10 - moved * 20, 6, B.mix("amber", a), -1)
    B.rrect(im, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 16, (200, 210, 230), 0.8 * a, False, 3)
    txt(im, lab, x, y + h / 2 + 40, 32, "ink", "c", a, panel=False)


def _v66(im, T, c):
    _frame(im, 520, 520, 640, 400, T, 0.0, "tasveer 1", smooth(seg(T, 0.2, 0.8)))
    _frame(im, 1400, 520, 640, 400, T, 1.0, "tasveer 2", smooth(seg(T, 1.0, 1.6)))
    k = smooth(seg(T, 2.2, 3.0))
    ring(im, 1400 - 640 * 0.18 + 640 * 0.3, 510, 30 + 4 * math.sin(T * 6), "amber", 4, k)
    arrow(im, 600, 280, 1320, 280, "amber", 5, k, 22, k)
    txt(im, "ek bindu apni jagah se hil gaya: wahi pind ho sakta hai", 960, 880, 42, "amber", "c", k)


@scene
def survey_sky(c, **p):
    stars_bg(c)
    base = c.im.copy()
    t64, t65, t66 = K(c, 64, 0, -0.1), K(c, 65, 0, -0.1), K(c, 66, 0, -0.1)
    view_seq(c, base, [(-1, t64, lambda v: _v63(v, c.T, c)), (t64, t65, lambda v: _v64(v, c.T - t64, c)),
                       (t65, t66, lambda v: _v65(v, c.T - t65, c)), (t66, 1e9, lambda v: _v66(v, c.T - t66, c))])


# =============================================================================== lines 67-71: how many found
@scene
def dots_found(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    t69, t70, t71 = K(c, 69, 0, -0.05), K(c, 70, 0, -0.05), K(c, 71, 0, -0.05)
    if T < t69:
        k = smooth(seg(T, 0.5, 3.8))
        _sky_dots(im, T, 100, 67, 0.95, 560, 200, 1360, 760, 20, 14, reveal=k)
        txt(im, "1 km se bade: 100 mein se ~95 mil chuke", 960, 110, 48, "green", "c", at(c, 67, 0.0, 0, 0.5))
        bar(im, 560, 850, 800, 36, 0.9 * smooth(seg(T, K(c, 68, 0.1), K(c, 68, 0.1) + 1.5)), "amber", at(c, 68, 0.0, 0, 0.4))
        txt(im, "2010: 90% ka lakshya poora", 960, 940, 42, "amber", "c", at(c, 68, 0.0, 0, 0.5))
    else:
        n = 2000
        a69 = smooth(seg(T, t69, t69 + 0.8))
        found = 0.42 if T >= t70 else 0.0
        reveal = smooth(seg(T, t70 + 0.2, t70 + 4.5)) * found
        _sky_dots(im, T, n, 69, found, 360, 170, 1560, 800, 50, 7.5, c_on="amber", reveal=max(reveal, 0.0001) if T >= t70 else 0.0)
        txt(im, "140 m se bade: ~25,000", 960, 110, 56, "amber", "c", a69)
        if T >= t70:
            txt(im, "40-44% hi mile the", 960, 880, 54, "amber", "c", at(c, 70, 0.1, 0, 0.5))
        if T >= t71:
            k = at(c, 71, 0.0, 0, 0.6)
            ov = im.copy()
            cv2.rectangle(ov, (360, 170), (1560, 800), (30, 20, 70), -1)
            cv2.addWeighted(ov, 0.18 * k, im, 1 - 0.18 * k, 0, dst=im)
            txt(im, "aadhe se zyaada anjaan the", 960, 960, 56, "red", "c", k)


# =============================================================================== lines 72-75: the goal that was missed
@scene
def goals(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    x0, x1, y = 260, 1660, 540
    B.line(im, x0, y, x1, y, B.mix("dim", 0.9), 5)
    def X(yr):
        return lerp(x0, x1, (yr - 2005) / 35.0)
    for yr in (2005, 2020, 2040):
        B.line(im, X(yr), y - 18, X(yr), y + 18, "ink", 4)
        txt(im, str(yr), X(yr), y + 70, 40, "ink", "c", 1.0, panel=False)
    prog = lin((T - 0.3) / 6.0)
    now = 2005 + (2040 - 2005) * smooth(seg(T, 0.4, 24.0))
    B.circ(im, X(now), y, 14, "white", -1)
    k1 = at(c, 72, 0.0, 0.1, 0.5)
    txt(im, "2005: Congress ka lakshya", X(2005) + 20, y - 250, 40, "ink", "l", k1)
    bar(im, X(2005), y - 150, X(2020) - X(2005), 36, 0.9 * smooth(seg(T, 0.6, 2.4)), "amber", k1)
    txt(im, "2020 tak 90% dhundhna", (X(2005) + X(2020)) / 2, y - 190, 36, "amber", "c", k1, panel=False)
    k2 = at(c, 73, 0.2, 0, 0.5)
    if k2 > 0.01:
        txt(im, "lakshya chook gaya", X(2020), y - 330, 50, "red", "c", k2)
        B.line(im, X(2020) - 24, y - 290, X(2020) + 24, y - 242, B.mix("red", k2), 6)
        B.line(im, X(2020) + 24, y - 290, X(2020) - 24, y - 242, B.mix("red", k2), 6)
    k3 = at(c, 74, 0.0, 0.0, 0.6)
    if k3 > 0.01:
        bar(im, X(2020), y + 160, X(2040) - X(2020), 36, 0.59 * smooth(seg(T, K(c, 74, 0.2), K(c, 74, 0.2) + 2.0)) / 0.9 * 0.9, "orange", k3)
        txt(im, "NASA ka apna andaza: 2040 tak bhi ~59%", (X(2020) + X(2040)) / 2, y + 240, 40, "orange", "c", k3)
    k4 = at(c, 75, 0.0, 0.0, 0.6)
    if k4 > 0.01:
        B.rrect(im, 380, 130, 1540, 250, 24, (10, 10, 18), 0.7 * k4)
        txt(im, "abhi koi jaana-pehchaana bada khatra nahi", 960, 170, 44, "green", "c", k4, panel=False)
        txt(im, "sawaal anjaan hisse ka hai", 960, 224, 34, "ink", "c", k4, panel=False)


# =============================================================================== lines 76-80: NEO Surveyor
def _dark_rock(im, T, x, y, glow_a):
    B.glow(im, x, y, 260, (60, 120, 255), 0.55 * glow_a)
    place_rock(im, x, y, 80, 7, T * 0.1, 1.0, 0.18 + 0.82 * glow_a, warm=1.0 if False else 0.0)
    if glow_a > 0.01:
        B.glow(im, x, y, 120, (30, 90, 255), 0.5 * glow_a)


@scene
def neo_surveyor(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    t77, t78, t79, t80 = K(c, 77, 0, -0.05), K(c, 78, 0, -0.05), K(c, 79, 0, -0.05), K(c, 80, 0, -0.05)
    if T < t78:
        for x, ttl, ga in ((520, "chamak (roshni) se", 0.0), (1400, "garmi (infrared) se", 1.0)):
            B.rrect(im, x - 400, 230, x + 400, 800, 24, (6, 8, 16), 0.85)
            a = smooth(seg(T, 0.2, 0.8)) if ga == 0 else at(c, 77, 0.0, 0, 0.6)
            _dark_rock(im, T, x, 520, ga * a)
            txt(im, ttl, x, 190, 40, "ink" if ga == 0 else "orange", "c", a)
        txt(im, "kaale pind andhere aasman mein nahi dikhte", 520, 860, 34, "grey", "c", at(c, 76, 0.2, 0, 0.6), panel=False)
        txt(im, "NEO Surveyor: garmi pakadta hai", 1400, 860, 34, "orange", "c", at(c, 77, 0.3, 0, 0.6), panel=False)
        txt(im, "NEO Surveyor: antariksh teleskope", 960, 110, 54, "amber", "c", at(c, 76, 0.55, 0, 0.6))
    elif T < t80:
        B.rrect(im, 560, 300, 1360, 700, 30, (14, 18, 34), 0.8)
        txt(im, "launch: Sep 2027 se pehle nahi", 960, 420, 52, "amber", "c", smooth(seg(T - t78, 0.3, 0.9)), panel=False)
        k = at(c, 79, 0.0, 0.0, 0.6)
        txt(im, "pehle: ~2026", 960, 540, 44, "grey", "c", k, panel=False)
        arrow(im, 780, 610, 1140, 610, "amber", 6, smooth(seg(T, t79 + 0.5, t79 + 1.6)), 24, smooth(seg(T, t79 + 0.5, t79 + 1.6)))
        txt(im, "tareekh aage bhi khisak sakti hai", 960, 670, 38, "ink", "c", at(c, 79, 0.55, 0, 0.6), panel=False)
        # moving calendar bar
        bar(im, 560, 780, 800, 28, lin((T - t78) / 10.0), "amber", 0.9)
    else:
        a = at(c, 80, 0.0, 0, 0.6)
        cx, cy, r = 960, 520, 230
        dial(im, cx, cy, r, 54.0 * smooth(seg(T, t80 + 0.6, t80 + 6.0)), "amber", a, full=60.0, hand=False, ticks=False)
        txt(im, "90%", cx, cy, 100, "amber", "c", a, panel=False)
        txt(im, "140 m se bade pindon mein se", cx, 190, 44, "ink", "c", a)
        txt(im, "udne ke ~10 saal ke andar", cx, 880, 48, "amber", "c", a)


# =============================================================================== lines 81-87: 2024 YR4 risk chart
def _yr4_pts():
    # (t01 over chart, value %)
    return [(0.0, 0.3), (0.12, 1.2), (0.28, 2.3), (0.4, 3.0), (0.47, 3.0), (0.56, 0.9), (0.6, 0.004), (0.66, 0.004)]


@scene
def yr4_chart(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    gx0, gy0, gw, gh = 300, 220, 1320, 560
    B.rrect(im, gx0 - 70, gy0 - 70, gx0 + gw + 50, gy0 + gh + 110, 24, (10, 12, 26), 0.75)
    B.line(im, gx0, gy0 + gh, gx0 + gw, gy0 + gh, "dim", 3)
    B.line(im, gx0, gy0, gx0, gy0 + gh, "dim", 3)
    txt(im, "2024 YR4: dharti se takkar ki sambhavna", 960, 140, 46, "ink", "c", at(c, 81, 0.2, 0, 0.6))
    pts = _yr4_pts()
    t_a, t_b = K(c, 81, 0.2), K(c, 84, 0.9)
    prog = seg(T, t_a, t_b)
    def XY(u, v):
        return gx0 + gw * u / 1.0 * 0.62, gy0 + gh * (1 - min(v, 3.6) / 3.6)
    line_ = []
    for i in range(0, 121):
        u = 0.66 * i / 120
        if u / 0.66 > prog:
            break
        # interpolate value
        v = pts[-1][1]
        for j in range(len(pts) - 1):
            if pts[j][0] <= u <= pts[j + 1][0]:
                v = lerp(pts[j][1], pts[j + 1][1], (u - pts[j][0]) / (pts[j + 1][0] - pts[j][0]))
                break
        line_.append(XY(u * 1.0, v))
    if len(line_) > 2:
        B.polyl(im, line_, B.mix("amber", 1.0), 6)
        B.glow(im, line_[-1][0], line_[-1][1], 40, (40, 160, 255), 0.7)
        B.circ(im, line_[-1][0], line_[-1][1], 9, "white", -1)
    # value labels on their spoken lines
    if T > K(c, 82, 0.35):
        x, y = XY(0.4, 3.0)
        txt(im, "~3%  (Feb 2025)", x, y - 60, 40, "orange", "c", at(c, 82, 0.35, 0, 0.5))
    if T > K(c, 83, 0.0):
        txt(im, "30 m se bade pind ke liye sabse ooncha", 1060, 300, 32, "ink", "l", at(c, 83, 0.0, 0, 0.5))
    if T > K(c, 84, 0.6):
        x, y = XY(0.62, 0.004)
        txt(im, "0.004%  (24 Feb)", x + 40, y - 70, 40, "green", "l", at(c, 84, 0.6, 0, 0.5))
    # moon chart (line 85-86)
    k5 = at(c, 85, 0.0, 0, 0.6)
    if k5 > 0.01:
        mx0, my0 = 1150, 500
        B.rrect(im, 1100, 330, 1620, 720, 20, (16, 20, 40), 0.9 * k5)
        txt(im, "chaand se takkar ki sambhavna", 1360, 365, 32, "ink", "c", k5, panel=False)
        mp = [(1150, 650), (1330, 540), (1480, 430), (1560, 420)]
        pr = smooth(seg(T, K(c, 85, 0.15), K(c, 85, 0.15) + 3.2))
        sub = []
        for j in range(30):
            u = pr * j / 29
            f = u * 3
            i = min(int(f), 2)
            sub.append((lerp(mp[i][0], mp[i + 1][0], f - i), lerp(mp[i][1], mp[i + 1][1], f - i)))
        B.polyl(im, sub, B.mix("blue", k5), 5)
        txt(im, "1.7 -> 3.8 -> 4.3 %", 1360, 690, 36, "blue", "c", k5, panel=False)
    k6 = at(c, 86, 0.4, 0, 0.6)
    if k6 > 0.01:
        B.rrect(im, 520, 400, 1400, 600, 30, (10, 10, 18), 0.75 * k6)
        txt(im, "5 Mar 2026: KHARIJ", 960, 470, 72, "green", "c", k6, panel=False)
        txt(im, "NASA ne ise bhi khaarij kiya", 960, 550, 36, "ink", "c", k6, panel=False)
    k7 = at(c, 87, 0.0, 0, 0.6)
    if k7 > 0.01:
        ov = im.copy()
        cv2.rectangle(ov, (0, 0), (W, H), (8, 10, 22), -1)
        cv2.addWeighted(ov, 0.9 * k7, im, 1 - 0.9 * k7, 0, dst=im)
        cx, cy = 960, 520
        names = [("data aata hai", 520), ("sambhavna badalti hai", 1400)]
        ang = 0.0
        for nm, x in names:
            B.rrect(im, x - 300, cy - 70, x + 300, cy + 70, 30, (20, 26, 50), 0.95 * k7)
            txt(im, nm, x, cy, 44, "amber", "c", k7, panel=False)
        arrow(im, 840, cy, 1100, cy, "amber", 7, k7, 28, k7)
        arrow(im, 1100, cy + 120, 840, cy + 120, "grey", 5, k7 * 0.8, 24, k7)
        txt(im, "yahi vigyan ka tareeka hai", 960, 800, 52, "ink", "c", at(c, 87, 0.55, 0, 0.6))


# =============================================================================== line 88: films vs reality
@scene
def film_vs_real(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    for x, ttl, cc_ in ((520, "kai filmon mein", "grey"), (1400, "asal mein", "amber")):
        B.rrect(im, x - 400, 220, x + 400, 800, 24, (10, 12, 26), 0.85)
        txt(im, ttl, x, 180, 46, cc_, "c", smooth(seg(T, 0.2, 0.8)))
    k = smooth(seg(T, 0.8, 1.6))
    # left: one sure announcement (step)
    B.line(im, 180, 700, 520, 700, B.mix("grey", k), 5)
    B.line(im, 520, 700, 520, 340, B.mix("grey", k), 5)
    B.line(im, 520, 340, 860, 340, B.mix("grey", k), 5)
    txt(im, "ek din pakka ailaan", 520, 840, 38, "ink", "c", smooth(seg(T, 1.8, 2.4)), panel=False)
    # right: wiggling probability
    k2 = seg(T, 1.8, 7.0)
    pts = []
    for i in range(0, 101):
        u = i / 100
        if u > k2:
            break
        pts.append((1030 + 740 * u, 560 - 140 * math.sin(u * 7) * (1 - 0.5 * u) - 100 * u))
    if len(pts) > 2:
        B.polyl(im, pts, B.mix("amber", 1.0), 5)
        B.circ(im, pts[-1][0], pts[-1][1], 9, "white", -1)
    txt(im, "sambhavna chhoti shuru, har observation par badalti", 1400, 840, 34, "ink", "c", smooth(seg(T, 2.4, 3.0)), panel=False)


# =============================================================================== lines 89-96: Apophis
EC = (960, 760)
ER = 75.0
GEO = 510.0


def _apo_space(im, T, a_dist=None, show_geo=True):
    earth(im, EC[0], EC[1], ER, T * 0.1)
    if show_geo:
        rng = np.random.default_rng(29)
        for i in range(60):
            ang = i / 60 * 6.283 + T * 0.03
            B.circ(im, EC[0] + GEO * math.cos(ang), EC[1] + GEO * math.sin(ang), 3, B.mix("teal", 0.7), -1)
    return


def _apo_path(u):
    """u in 0..1: x from -80 to 2000, closest approach y = EC[1]-465 at x = EC[0]."""
    x = lerp(-80, 2000, u)
    y = EC[1] - 465 - 0.00022 * (x - EC[0]) ** 2 * 0.0 + 60 * math.sin((u - 0.5) * 2.2) ** 2 * 0.0
    d = x - EC[0]
    y = EC[1] - math.sqrt(465 ** 2 + 0 * d) + (d * d) / 4000.0 * 0.0
    return x, EC[1] - 465 + 0.00009 * d * d * 0.0 + (d * d) / 30000.0


def _av89(im, T, c):
    place_rock(im, 960, 520, 260, 11, T * 0.05, 1.0, 1.0, (1.0, 0.85))
    txt(im, "Apophis", 960, 130, 90, "amber", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "afwaahon mein sabse zyaada aane waala naam", 960, 940, 42, "ink", "c", smooth(seg(T, 1.0, 1.8)))


def _av90(im, T, c):
    place_rock(im, 960, 520, 240, 11, T * 0.05, 1.0, 1.0, (1.0, 0.85))
    k = smooth(seg(T, 0.3, 1.2))
    B.line(im, 720, 820, 720 + 480 * k, 820, "amber", 5)
    B.line(im, 720, 800, 720, 840, "amber", 5)
    B.line(im, 720 + 480 * k, 800, 720 + 480 * k, 840, "amber", 5)
    txt(im, "~340 m (NASA)", 960, 890, 54, "amber", "c", k)
    txt(im, "ESA ke mutabik 375 m", 960, 960, 42, "blue", "c", smooth(seg(T, 3.0, 3.7)))


def _av91(im, T, c):
    _apo_space(im, T)
    ak = smooth(seg(T, 0.3, 5.6))
    pts = [_apo_path(i / 60) for i in range(61)]
    dotted(im, pts, "dim", 3, 0.7, 14, 12)
    x, y = _apo_path(ak)
    place_rock(im, x, y, 16, 11, T * 2)
    B.glow(im, x, y, 60, (40, 140, 255), 0.4)
    ring(im, EC[0], EC[1], GEO, "teal", 2, 0.45, 10)
    txt(im, "satellite ring", EC[0] + GEO * 0.72, EC[1] - GEO * 0.72, 28, "teal", "c", 0.9, panel=False)
    d = math.hypot(x - EC[0], y - EC[1]) - ER
    km = 32000 * d / 390.0
    txt(im, "13 Apr 2029", 300, 160, 64, "amber", "c", smooth(seg(T, 0.3, 0.9)))
    txt(im, f"doori: ~{int(max(km, 32000)):,} km" if ak > 0.48 else f"doori: ~{int(km / 1000) * 1000:,} km", 300, 250, 44, "ink", "c", smooth(seg(T, 0.6, 1.2)))
    txt(im, "dharti ki satah se ~32,000 km", 1500, 960, 40, "amber", "c", smooth(seg(T, 3.4, 4.2)))


def _av92(im, T, c):
    x0, x1 = 300, 1620
    B.line(im, x0, 540, x1, 540, B.mix("dim", 0.9), 5)
    txt(im, "aaj", x0, 610, 36, "ink", "c", 1.0, panel=False)
    txt(im, "+100 saal", x1, 610, 36, "ink", "c", 1.0, panel=False)
    k = smooth(seg(T, 0.4, 3.0))
    B.rrect(im, x0, 500, x0 + (x1 - x0) * k, 580, 20, "green", 0.45)
    txt(im, "NASA: kam se kam agle 100 saal koi jokhim nahi", 960, 330, 48, "green", "c", smooth(seg(T, 0.8, 1.6)))


def _av93(im, T, c):
    gx0, gy0, gw, gh = 360, 260, 1200, 520
    B.line(im, gx0, gy0 + gh, gx0 + gw, gy0 + gh, "dim", 3)
    B.line(im, gx0, gy0, gx0, gy0 + gh, "dim", 3)
    pr = seg(T, 0.4, 5.0)
    pts = []
    for i in range(0, 61):
        u = i / 60
        if u > pr:
            break
        v = 2.7 * min(1.0, u / 0.35) if u < 0.7 else 2.7 * (1 - (u - 0.7) / 0.1) if u < 0.8 else 0.0
        pts.append((gx0 + gw * u, gy0 + gh * (1 - v / 3.2)))
    if len(pts) > 2:
        B.polyl(im, pts, "amber", 6)
        B.circ(im, pts[-1][0], pts[-1][1], 9, "white", -1)
    txt(im, "2004 (khoj ke waqt): 2.7%", 700, 210, 48, "orange", "c", smooth(seg(T, 0.8, 1.6)))
    txt(im, "baad ke observation ne hata diya", 1300, 840, 40, "green", "c", smooth(seg(T, 4.4, 5.2)))


def _av94(im, T, c):
    earth(im, 960, 520, 330, T * 0.12 + 1.5)
    ov = im.copy()
    cv2.ellipse(ov, (960 + 120, 520), (190, 320), 0, -90, 90, (60, 190, 255), -1, cv2.LINE_AA)
    cv2.addWeighted(ov, 0.22, im, 0.78, 0, dst=im)
    B.ell(im, 1460, 300, 60, 32, "ink", 5)
    B.circ(im, 1460, 300, 15, "amber", -1)
    txt(im, "poorvi golaardh se nangi aankh se dikh sakta hai", 960, 940, 44, "amber", "c", smooth(seg(T, 0.5, 1.3)))


def _av95(im, T, c):
    place_rock(im, 960, 500, 150, 11, T * 0.05, 1.0, 1.0, (1.0, 0.85))
    for k, (nm, ang0, cc_, ln) in enumerate((("RAMSES (Europe)", -2.5, "blue", 95), ("OSIRIS-APEX (America)", 0.5, "green", 95))):
        a = smooth(seg(T, 0.4 + 2.5 * k, 1.1 + 2.5 * k))
        ang = ang0 + T * 0.6
        x, y = 960 + 330 * math.cos(ang), 500 + 230 * math.sin(ang)
        blit(im, craft_spr(), x, y, 0.16, ang, a)
        txt(im, nm, x, y - 70, 32, cc_, "c", a)
    B.ell(im, 960, 500, 330, 230, B.mix("dim", 0.4), 2)
    txt(im, "saath-saath rahega", 520, 930, 40, "blue", "c", smooth(seg(T, 0.6, 1.2)))
    txt(im, "uske baad pahunchega", 1400, 930, 40, "green", "c", smooth(seg(T, 3.0, 3.6)))


def _av96(im, T, c):
    B.rrect(im, 260, 300, 1660, 520, 28, (12, 14, 28), 0.85)
    txt(im, "\"Apophis takkarayega\"", 960, 360, 64, "ink", "c", 1.0, panel=False)
    k = smooth(seg(T, 0.6, 1.2))
    B.line(im, 330, 420, 1590, 420, B.mix("red", k), 7)
    txt(im, "NASA ke hisaab se: sach nahi", 960, 600, 66, "green", "c", smooth(seg(T, 1.6, 2.4)))
    txt(im, "abhi koi jaana-pehchaana bada khatra nahi", 960, 760, 44, "ink", "c", smooth(seg(T, 3.6, 4.4)))


@scene
def apophis(c, **p):
    stars_bg(c)
    base = c.im.copy()
    ts = [K(c, n, 0, -0.05) for n in (90, 91, 92, 93, 94, 95, 96)]
    fns = [_av89, _av90, _av91, _av92, _av93, _av94, _av95, _av96]
    views = []
    edges = [-1] + ts + [1e9]
    for i, fn in enumerate(fns):
        a, b = edges[i], edges[i + 1]
        views.append((a, b, (lambda v, fn=fn, a=a: fn(v, c.T - max(a, 0.0), c))))
    view_seq(c, base, views)
