"""rc_explain scenes, part E: lines 125-159 (the four methods, caveats, film vs plan, Hera, unknowns, verdict, three takeaways)."""
import math

import cv2
import numpy as np

import rc_build_long as B
from rc_explain import (scene, smooth, lin, seg, col, lerp, txt, txtw, blit, rock_spr, craft_spr, earth, sun, arrow, dotted, ring, flash, whiten,
                        particles, stars_bg, dial, put, text_spr, W, H, K, real, bar, view_seq)
from rc_explain_scenes import smooth_int, mixview, hm, place_rock
from rc_explain_b import at, until, inset
from rc_explain_d import _views, _pile, PUSH, EXTRA


def _lane(im, y, T, kind, a=1.0, ti=2.0, small=False):
    """craft | rock | result path, one shared layout. kind: kinetic, tractor, laser, nuke."""
    s = 0.6 if small else 1.0
    rx, ry = 1000, y
    R = 70 * s
    dv = 0.0
    if kind == "kinetic":
        dv = 90 * smooth(seg(T, ti, ti + 2.5)) * s
    elif kind == "tractor":
        dv = 70 * smooth(seg(T, 0.8, 7.0)) * s
    elif kind == "laser":
        dv = 40 * smooth(seg(T, 1.0, 7.0)) * s
    elif kind == "nuke":
        dv = 110 * smooth(seg(T, ti, ti + 1.5)) * s
    place_rock(im, rx, ry - dv, R, 4, T * 0.2, a)
    dotted(im, [(rx - 400 * s, ry), (rx + 500 * s, ry)], "dim", 3, 0.6 * a, 12, 12)
    if dv > 1:
        B.polyl(im, [(rx, ry), (rx + 220 * s, ry - dv * 1.2)], B.mix(PUSH, a), 5)
    if kind == "kinetic":
        cx = lerp(rx - 520 * s, rx - R * 1.05, smooth(seg(T, 0.3, ti))) if T < ti else rx - R * 1.05
        if T < ti + 0.3:
            blit(im, craft_spr(), cx, ry, 0.22 * s, 0.0, a)
        if T > ti:
            flash(im, rx - R, ry - dv * 0.2, (T - ti) / 0.8, 150 * s, a)
            particles(im, rx - R, ry, T - ti, 30, 8, (60, 260), (math.pi * 0.6, math.pi * 1.4), (2, 4), 1.5, 1.5, (190, 195, 205))
    elif kind == "tractor":
        cx, cy_ = rx - R - 130 * s, ry - dv * 0.0
        blit(im, craft_spr(), cx, cy_, 0.2 * s, 0.0, a)
        for i in range(5):
            ph = (T * 0.8 + i * 0.2) % 1.0
            B.circ(im, lerp(rx - R - 10, cx + 40, ph), ry - dv * (1 - ph) * 0.0 + (i - 2) * 9 * (1 - ph), 3.5, B.mix("blue", 0.9 * a * (1 - ph)), -1)
        ring(im, rx, ry - dv, R + 20 + 5 * math.sin(T * 3), "blue", 2, 0.5 * a)
    elif kind == "laser":
        cx = rx - R - 260 * s
        blit(im, craft_spr(), cx, ry - 60 * s, 0.2 * s, 0.0, a)
        B.line(im, cx + 30 * s, ry - 60 * s, rx - R * 0.5, ry - dv - R * 0.55, B.mix("red", a), 5)
        B.glow(im, rx - R * 0.5, ry - dv - R * 0.55, 60 * s, (60, 60, 255), 0.7 * a)
        for i in range(10):
            ph = (T * 1.4 + i * 0.1) % 1.0
            B.circ(im, rx - R * 0.5 - ph * 90 * s, ry - dv - R * 0.55 - ph * 120 * s, 4, B.mix((200, 200, 230), a * (1 - ph)), -1)
    elif kind == "nuke":
        bx = rx - R - 40 * s
        if T < ti:
            B.circ(im, bx - 160 * s * (1 - smooth(seg(T, 0.2, ti))), ry, 10 * s, B.mix("white", a), -1)
        else:
            flash(im, bx, ry, (T - ti) / 1.6, 260 * s, a)
        # surface vapour pushes the rock
    return rx, ry


def _success(im, x, y, a, ok=True):
    if ok:
        B.polyl(im, [(x - 22, y), (x - 6, y + 18), (x + 26, y - 20)], B.mix("green", a), 7)


# =============================================================================== 125 kinetic, 126-127 tractor, 128 laser
@scene
def method_demo(c, kind="kinetic", ttl="", need="", **p):
    stars_bg(c)
    im, T = c.im, c.T
    _lane(im, 520, T, kind, 1.0)
    txt(im, ttl, 960, 120, 62, "amber", "c", smooth(seg(T, 0.2, 0.8)))
    if need:
        for i, line_ in enumerate(need.split("|")):
            txt(im, line_, 960, 880 + i * 62, 40, "ink" if i == 0 else "grey", "c", smooth(seg(T, 1.5 + 1.2 * i, 2.2 + 1.2 * i)))


@scene
def tractor_demo(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    _lane(im, 520, T, "tractor", 1.0)
    txt(im, "tareeka 2: gravity tractor", 960, 120, 62, "amber", "c", at(c, 126, 0.0, 0.2, 0.6))
    txt(im, "yaan pind ke paas mandrata hai, gurutwaakarshan se dheere-dheere kheenchta hai", 960, 860, 38, "ink", "c", at(c, 126, 0.25, 0, 0.6))
    k = at(c, 127, 0.0, 0, 0.6)
    if k > 0.01:
        txt(im, "saalon, kai dashakon ki chetavani chahiye", 960, 940, 46, "orange", "c", k)
        n = int(10 * smooth(seg(T, K(c, 127, 0.0), K(c, 127, 0.0) + 3.5)))
        for i in range(11):
            B.circ(im, 560 + i * 80, 780, 10, B.mix("orange" if i <= n else "dim", 0.95), -1)
        txt(im, f"{n * 5} saal", 1400, 720, 40, "orange", "c", k, panel=False)


@scene
def laser_demo(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    _lane(im, 520, T, "laser", 1.0)
    txt(im, "tareeka 3: laser se satah ko bhaap banana", 960, 120, 58, "amber", "c", smooth(seg(T, 0.2, 0.8)))
    txt(im, "nikalti dhaar dhakka deti hai", 960, 840, 42, "ink", "c", at(c, 128, 0.25, 0, 0.6))
    txt(im, "abhi sirf ek vichaar, aur dheema bhi", 960, 930, 44, "red", "c", at(c, 128, 0.6, 0, 0.6))


# =============================================================================== 129-130: the 2023 exercise
@scene
def exercise(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    txt(im, "2023 ka kalpanik-pind abhyaas", 960, 90, 52, "amber", "c", at(c, 129, 0.0, 0.1, 0.6))
    kinds = [("kinetic", "kai kinetic dhakke"), ("tractor", "kai gravity tractor"), ("laser", "laser"), ("nuke", "parmanu")]
    for i, (k_, lab) in enumerate(kinds):
        y = 270 + i * 205
        a = smooth(seg(T, 0.4 + 0.25 * i, 1.0 + 0.25 * i))
        B.rrect(im, 90, y - 90, 1830, y + 90, 22, (12, 14, 30), 0.5 * a)
        txt(im, lab, 120, y, 36, "ink", "l", a, panel=False)
        # shift lane left via drawing at offset: reuse by temp translate
        sub = im.copy()
        _lane(sub, y, T, k_, 1.0, ti=1.5, small=True)
        M = np.float32([[1, 0, -150], [0, 1, 0]])
        sub = cv2.warpAffine(sub, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
        roi = (slice(y - 90, y + 90), slice(520, 1500))
        im[roi] = (im[roi] * (1 - a) + sub[roi] * a).astype(np.uint8)
        t_ok = K(c, 130, 0.12 + 0.18 * i)
        ok = at(c, 130, 0.12 + 0.18 * i, 0, 0.4)
        if ok > 0.01:
            _success(im, 1620, y, ok)
            txt(im, "pind mud sakta tha", 1700, y + 44, 24, "green", "c", ok, panel=False)


# =============================================================================== 131-133: nuclear standoff
@scene
def nuclear(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    rx, ry = 1000, 540
    ti = 3.0
    d = max(T - ti, 0.0)
    kick = 120 * smooth(seg(T, ti, ti + 2.0))
    place_rock(im, rx + kick, ry, 90, 4, T * 0.1)
    bx = rx - 90 - 50
    if T < ti:
        B.circ(im, bx - 420 * (1 - smooth(seg(T, 0.4, ti))), ry, 8, "white", -1)
    else:
        flash(im, bx, ry, d / 1.6, 340)
        particles(im, rx + kick - 80, ry, d, 90, 41, (80, 420), (math.pi * 0.6, math.pi * 1.4), (2, 6), 1.0, 3.0, (200, 205, 215), glowc=(60, 160, 255))
    dotted(im, [(rx - 500, ry), (rx + 700, ry)], "dim", 3, 0.5, 12, 12)
    txt(im, "tareeka 4: parmanu dhamaka (aakhri upaay)", 960, 100, 54, "amber", "c", at(c, 131, 0.0, 0.2, 0.6))
    txt(im, "dhamaka satah par nahi, pind ke paas", 960, 960, 44, "ink", "c", at(c, 131, 0.5, 0, 0.6) * until(c, 132, 0.0, 0, 0.3))
    k = at(c, 132, 0.0, 0, 0.6)
    if k > 0.01:
        for i, t_ in enumerate(("100 m ka pind", "~1 megaton, kuch metre door", "takkar se ~2 mahine pehle")):
            txt(im, t_, 380, 330 + i * 80, 38, "ink", "l", at(c, 132, 0.12 + 0.28 * i, 0, 0.5))
    k2 = at(c, 133, 0.0, 0, 0.6)
    if k2 > 0.01:
        ex, ey = 1640, 760
        earth(im, ex, ey, 120, T * 0.1, k2)
        for i in range(24):
            ph = (T * 0.5 + i * 0.07) % 1.0
            yy = ey - 190 - (i % 5) * 36
            B.circ(im, lerp(1100, 1860, ph), yy + 0.0, 4, B.mix((200, 205, 215), 0.9 * k2), -1)
        txt(im, "99.9% se zyaada hissa dharti se chook gaya", 960, 960, 46, "green", "c", k2)


# =============================================================================== 134-137: caveats
def _n134(im, T):
    B.rrect(im, 460, 220, 1460, 760, 30, (12, 16, 32), 0.9)
    B.rrect(im, 460, 220, 1460, 760, 30, "ink", 0.8, False, 5)
    rng = np.random.default_rng(134)
    for i in range(200):
        B.circ(im, 500 + rng.random() * 920, 260 + rng.random() * 460, 2, B.mix("blue", 0.4), -1)
    place_rock(im, 960, 490, 90, 4, T * 0.2)
    flash(im, 840, 490, ((T * 0.6) % 1.0), 240)
    txt(im, "SIRF COMPUTER SIMULATION", 960, 860, 64, "red", "c", smooth(seg(T, 0.4, 1.0)))
    txt(im, "asal mein ise antariksh mein kabhi aazmaya nahi gaya", 960, 950, 38, "ink", "c", smooth(seg(T, 1.6, 2.4)))


def _n135(im, T):
    cx, cy = 600, 540
    k = smooth(seg(T, 1.2, 3.0))
    for i, (dx, dy) in enumerate(((-60, -30), (50, -70), (70, 50), (-40, 60), (0, 0))):
        place_rock(im, cx + dx * (1 + 3 * k), cy + dy * (1 + 3 * k), 55 - 4 * i, 4 + i, T * 0.3 + i)
    txt(im, "dhamaka pind ko kai tukdon mein tod sakta hai", 960, 130, 46, "red", "c", smooth(seg(T, 0.3, 1.0)))
    B.circ(im, 1400, 540, 210, (60, 70, 90), -1)
    _pile(im, 1400, 540, 205, 135, T, 1.0)
    B.circ(im, 1400, 540, 210, B.mix("teal", 0.9), 4)
    txt(im, "?", 1400, 540, 120, "red", "c", 0.7, panel=False)
    txt(im, "andar ki banaawat aksar pata nahi", 1400, 830, 38, "ink", "c", smooth(seg(T, 3.0, 3.7)))


def _n136(im, T):
    cx, cy = 960, 560
    tilt = 0.10 * math.sin(T * 1.3)
    B.line(im, cx - 340, cy - 120 - tilt * 340, cx + 340, cy - 120 + tilt * 340, "ink", 7)
    B.line(im, cx, cy - 120, cx, cy + 220, "ink", 7)
    B.line(im, cx - 120, cy + 230, cx + 120, cy + 230, "ink", 7)
    for sgn, lab, cc_ in ((-1, "vigyan", "teal"), (1, "qanoon", "amber")):
        x = cx + sgn * 340
        y = cy - 120 + sgn * tilt * 340
        B.line(im, x, y, x, y + 100, "ink", 3)
        B.rrect(im, x - 120, y + 100, x + 120, y + 190, 16, cc_, 0.45)
        txt(im, lab, x, y + 145, 44, cc_, "c", 1.0, panel=False)
    txt(im, "antariksh mein parmanu hathiyaaron par qanooni sawaal bhi hain", 960, 130, 44, "ink", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "sawaal sirf vigyan ka nahi hai", 960, 960, 50, "amber", "c", smooth(seg(T, 2.0, 2.8)))


def _n137(im, T):
    for x, lab, cc_ in ((520, "\"ye pakka chalega\"", "green"), (1400, "\"ye pakka nahi chalega\"", "red")):
        B.rrect(im, x - 380, 330, x + 380, 560, 28, (12, 14, 30), 0.85)
        txt(im, lab, x, 440, 46, cc_, "c", 1.0, panel=False)
        a = smooth(seg(T, 1.0 if x < 900 else 1.6, 1.8 if x < 900 else 2.4))
        B.line(im, x - 340, 520, x - 340 + 680 * a, 520, B.mix("amber", a), 6)
        txt(im, "saboot nahi", x, 640, 42, "amber", "c", a)
    txt(im, "dono daave bina saboot ke hain", 960, 880, 56, "ink", "c", smooth(seg(T, 2.8, 3.6)))


@scene
def nuclear_caveats(c, **p):
    stars_bg(c)
    _views(c, [134, 135, 136, 137], [_n134, _n135, _n136, _n137])


# =============================================================================== 138-140: films vs the real plan
def _f138(im, T):
    x0, x1 = 260, 1660
    txt(im, "filmon mein", x0, 300, 40, "grey", "l", 1.0)
    B.line(im, x0, 360, x1, 360, B.mix("dim", 0.8), 4)
    k = smooth(seg(T, 0.6, 1.6))
    B.rrect(im, x1 - 90, 330, x1 - 90 + 90 * k, 390, 10, "red", 0.7)
    txt(im, "aakhri minute: drill karo, udaa do", x1 - 90, 440, 34, "red", "r", k, panel=False)
    txt(im, "asli yojana", x0, 600, 40, "amber", "l", smooth(seg(T, 2.0, 2.6)))
    B.line(im, x0, 660, x1, 660, B.mix("dim", 0.8), 4)
    k2 = smooth(seg(T, 2.4, 5.0))
    B.rrect(im, x0, 630, x0 + (x1 - x0) * 0.82 * k2, 690, 10, "green", 0.55)
    txt(im, "dashakon pehle dhoondho, phir halka dhakka", x0, 740, 40, "green", "l", smooth(seg(T, 3.4, 4.2)), panel=False)
    txt(im, "time ->", x1, 780, 28, "grey", "r", 1.0, panel=False)


def _f139(im, T):
    ex, ey = 1560, 540
    earth(im, ex, ey, 150, T * 0.1)
    sx, sy = 160, 540
    k = smooth(seg(T, 0.6, 5.0))
    # path hits Earth (grey dotted); early nudge diverges a lot, late nudge little
    dotted(im, [(sx, sy), (ex - 150, ey)], "dim", 3, 0.7, 12, 12)
    px, py = lerp(sx, ex - 160, k), lerp(sy, ey, k)
    B.polyl(im, [(sx, sy), (lerp(sx, ex - 160, 0.1), lerp(sy, ey, 0.1))], B.mix(PUSH, 0.9), 6)
    pts = [(lerp(sx, ex - 160, u), lerp(sy, ey, u) - 420 * max(u - 0.1, 0) ** 1.0 * 0.0 - 400 * max(u - 0.1, 0) * (u - 0.1) / 0.81) for u in np.linspace(0.1, k, 30)] if k > 0.1 else []
    if len(pts) > 2:
        B.polyl(im, pts, B.mix("green", 1.0), 6)
    place_rock(im, pts[-1][0] if pts else sx, pts[-1][1] if pts else sy, 22, 4, T)
    txt(im, "shuru ka chhota dhakka", 400, 340, 44, "green", "c", smooth(seg(T, 0.8, 1.5)))
    txt(im, "samay ke saath bahut bada farq", 960, 920, 54, "amber", "c", smooth(seg(T, 3.0, 3.8)))


def _f140(im, T):
    B.rrect(im, 360, 360, 1560, 640, 30, (10, 18, 20), 0.85)
    txt(im, "in sab ke baad bhi", 960, 440, 46, "ink", "c", smooth(seg(T, 0.2, 0.8)), panel=False)
    txt(im, "jaana-pehchaana bada khatra aaj koi nahi", 960, 540, 56, "green", "c", smooth(seg(T, 0.8, 1.6)), panel=False)


@scene
def film_plan(c, **p):
    stars_bg(c)
    _views(c, [138, 139, 140], [_f138, _f139, _f140])


# =============================================================================== 141-148: Hera
def _h141(im, T):
    place_rock(im, 1400, 560, 300, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    blit(im, craft_spr(), 640, 540, 0.62, 0.15 * math.sin(T), 1.0)
    txt(im, "Hera: ESA ka yaan", 640, 280, 54, "blue", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "DART ka adhoora sawaal ab Hera suljhayega", 960, 960, 46, "ink", "c", smooth(seg(T, 0.8, 1.6)))


def _h142(im, T):
    cx, cy = 960, 560
    sun(im, cx, cy, 36, T, 1.0)
    B.ell(im, cx, cy, 200, 200, B.mix("blue", 0.6), 2)
    B.ell(im, cx, cy, 300, 300, B.mix("red", 0.6), 2)
    txt(im, "Dharti", cx + 200 * 0.7 + 40, cy + 200 * 0.7 + 30, 28, "blue", "l", 1.0, panel=False)
    txt(im, "Mangal", cx + 300 * 0.7 + 40, cy - 300 * 0.7 - 30, 28, "red", "l", 1.0, panel=False)
    ea = 0.4 + T * 0.5
    B.circ(im, cx + 200 * math.cos(ea), cy + 200 * math.sin(ea), 12, "blue", -1)
    ma = -2.2 + T * 0.25
    B.circ(im, cx + 300 * math.cos(ma), cy + 300 * math.sin(ma), 10, "red", -1)
    pts = []
    k = smooth(seg(T, 0.5, 6.0))
    for i in range(0, 61):
        u = i / 60 * k
        r_ = 200 + 270 * u
        a_ = 0.4 + 4.2 * u
        pts.append((cx + r_ * math.cos(a_), cy + r_ * math.sin(a_)))
    if len(pts) > 2:
        dotted(im, pts, "amber", 5, 1.0, 14, 8)
        B.circ(im, pts[-1][0], pts[-1][1], 9, "white", -1)
    txt(im, "7 Oct 2024: udaan", 320, 160, 44, "amber", "c", smooth(seg(T, 0.3, 0.9)))
    txt(im, "Mar 2025: Mangal ke paas se guzra", 1500, 920, 40, "ink", "c", smooth(seg(T, 3.8, 4.6)))


def _h143(im, T):
    cx, cy = 760, 560
    place_rock(im, cx, cy, 190, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    ang = T * 0.5
    mx, my = cx + 480 * math.cos(ang), cy + 330 * math.sin(ang)
    B.ell(im, cx, cy, 480, 330, B.mix("dim", 0.4), 2)
    place_rock(im, mx, my, 45, 5, ang)
    ha = -ang * 0.8 + 2
    hx, hy = mx + 110 * math.cos(ha), my + 110 * math.sin(ha)
    blit(im, craft_spr(), hx, hy, 0.15, 0.0)
    for i, (t_, y) in enumerate((("dravyaman naapna", 300), ("banaawat naapna", 390), ("takkar ka gaddha dekhna", 480))):
        a = smooth(seg(T, 0.6 + 0.9 * i, 1.3 + 0.9 * i))
        B.circ(im, 1400, y, 12, B.mix("blue", a), -1)
        txt(im, t_, 1440, y, 40, "ink", "l", a, panel=False)
    txt(im, "Hera ka kaam", 1440, 215, 54, "blue", "l", smooth(seg(T, 0.2, 0.8)), panel=False)


def _h144(im, T):
    x0 = 300
    txt(im, "simulation ne bataya", x0, 330, 40, "grey", "l", 1.0)
    bar(im, x0, 370, 700, 40, 0.45 * smooth(seg(T, 0.4, 1.4)), "grey", 1.0)
    txt(im, "asal mein", x0, 560, 40, "amber", "l", smooth(seg(T, 1.2, 1.8)))
    bar(im, x0, 600, 1300, 40, 0.97 * smooth(seg(T, 1.6, 3.4)), "orange", 1.0)
    txt(im, "wo simulation ki bhavishyavani se itna zyaada kyon hila?", 960, 880, 46, "amber", "c", smooth(seg(T, 2.6, 3.4)))


def _h145(im, T):
    blit(im, craft_spr(), 960, 540, 0.5, 0.0)
    for sgn, nm in ((-1, "Milani"), (1, "Juventas")):
        k = smooth(seg(T, 0.8 + (0.6 if sgn > 0 else 0), 3.0 + (0.6 if sgn > 0 else 0)))
        x = 960 + sgn * (60 + 520 * k)
        y = 540 - 30 * k * sgn * 0
        B.rrect(im, x - 28, y - 28, x + 28, y + 28, 6, (200, 210, 230), 1.0)
        B.rrect(im, x - 28, y - 28, x + 28, y + 28, 6, "amber", 1.0, False, 3)
        txt(im, nm, x, y - 70, 38, "ink", "c", smooth(seg(T, 1.4, 2.0)))
    txt(im, "do chhote CubeSat saath mein", 960, 130, 52, "ink", "c", smooth(seg(T, 0.2, 0.8)))
    txt(im, "Hera apne aap raasta khojne ki takneek bhi parkhega", 960, 940, 42, "blue", "c", smooth(seg(T, 3.6, 4.4)))


def _h146(im, T):
    B.rrect(im, 360, 230, 1560, 790, 26, (8, 10, 20), 0.95)
    B.rrect(im, 360, 230, 1560, 790, 26, "ink", 0.7, False, 4)
    place_rock(im, 800 - 20 * smooth(seg(T, 0.5, 3.0)), 520, 70, 2, T * 0.05)
    place_rock(im, 1050 + 30 * smooth(seg(T, 0.5, 3.0)), 560, 22, 5, T * 0.1)
    txt(im, "27 Oct 2026: ESA ki jaari tasveer", 960, 150, 46, "amber", "c", smooth(seg(T, 0.2, 0.8)))
    txt(im, "dono asteroid alag-alag dikhte hain", 960, 880, 46, "ink", "c", smooth(seg(T, 1.6, 2.4)))


def _h147(im, T):
    x0, x1 = 300, 1620
    B.line(im, x0, 540, x1, 540, B.mix("dim", 0.9), 5)
    for i, m in enumerate(("Oct 2026", "Nov 2026", "Dec 2026")):
        B.line(im, x0 + i * 660, 520, x0 + i * 660, 560, "ink", 4)
        txt(im, m, x0 + i * 660, 610, 32, "ink", "c", 1.0, panel=False)
    k = smooth(seg(T, 0.5, 2.5))
    blit(im, craft_spr(), lerp(x0, x0 + 660 + 20, k), 470, 0.14, 0.0)
    txt(im, "pahunchne ki yojana: Nov 2026", 960, 250, 54, "amber", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "?", x0 + 700, 540, 80, "red", "c", smooth(seg(T, 2.0, 2.6)), panel=False)


def _h148(im, T):
    B.rrect(im, 340, 330, 1580, 650, 30, (12, 16, 32), 0.9)
    txt(im, "pahunchne ki pakki khabar hamne nahi dekhi", 960, 430, 50, "ink", "c", smooth(seg(T, 0.2, 0.9)), panel=False)
    txt(im, "taaza haal agency ke page par dekhiye", 960, 540, 44, "amber", "c", smooth(seg(T, 1.4, 2.2)), panel=False)


@scene
def hera(c, **p):
    stars_bg(c)
    _views(c, [141, 142, 143, 144, 145, 146, 147, 148], [_h141, _h142, _h143, _h144, _h145, _h146, _h147, _h148])


# =============================================================================== 149-151: what we do not know yet
@scene
def unknowns(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    txt(im, "abhi kya nahi pata?", 960, 100, 60, "amber", "c", at(c, 149, 0.0, 0.1, 0.6))
    cols = [(380, 149, 0.2, "1", "Dimorphos ka dravyaman aur banaawat"), (960, 150, 0.0, "2", "kya har asteroid par chalega?"), (1540, 151, 0.0, "3", "jo abhi dhundhe hi nahi gaye")]
    for x, ln, fr, n, lab in cols:
        a = at(c, ln, fr, 0, 0.6)
        B.rrect(im, x - 270, 230, x + 270, 880, 28, (12, 14, 30), 0.85 * a)
        B.circ(im, x, 300, 36, B.mix("amber", a), -1)
        txt(im, n, x, 300, 46, "dark", "c", a, panel=False)
        txt(im, lab, x, 800, 30, "ink", "c", a, panel=False)
    a = at(c, 149, 0.2, 0, 0.6)
    place_rock(im, 380, 520, 120, 2, T * 0.04, a)
    txt(im, "?", 380, 520, 100, "red", "c", a * (0.6 + 0.4 * math.sin(T * 4)), panel=False)
    a = at(c, 150, 0.0, 0, 0.6)
    _pile(im, 960, 440, 90, 150, T, 1.0, a)
    B.circ(im, 960, 440, 94, B.mix("teal", a), 3)
    B.circ(im, 960, 640, 90, B.mix((130, 122, 110), a), -1)
    B.circ(im, 960, 640, 94, B.mix("teal", a), 3)
    txt(im, "patthron ka dher: chala", 960, 540, 24, "green", "c", a, panel=False)
    txt(im, "thos pind: asar alag ho sakta hai", 960, 740, 24, "orange", "c", at(c, 150, 0.45, 0, 0.5), panel=False)
    a = at(c, 151, 0.0, 0, 0.6)
    ov = im.copy()
    cv2.circle(ov, (1540, 520), 190, (4, 6, 14), -1, cv2.LINE_AA)
    cv2.addWeighted(ov, 0.9 * a, im, 1 - 0.9 * a, 0, dst=im)
    txt(im, "?", 1540, 520, 140, "red", "c", a * (0.6 + 0.4 * math.sin(T * 3)), panel=False)


# =============================================================================== 152-156: the verdict
@scene
def verdict(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    txt(im, "chaar daave, chaar nishaan", 960, 90, 56, "amber", "c", at(c, 152, 0.0, 0.1, 0.6))
    claims = [("kya hum asteroid ki chaal badal sakte hain?", "SACH", "green", 153, "chhote, bekhatar nishane par, ek baar"),
              ("kya hum kisi bhi asteroid ko rok lenge?", "ANJAAN", "amber", 154, "ek tareeka, ek baar chala"),
              ("kya aaj koi jaana-pehchaana bada khatra hai?", "NAHI", "red", 155, "par anjaan hisse ka jawab: pata nahi"),
              ("kya filmon wala aakhri-minute ka hal asli yojana hai?", "AADHA SACH", "orange", 156, "asli yojana: waqt rehte dhundhna")]
    for i, (q, st, cc_, ln, note) in enumerate(claims):
        y = 250 + i * 215
        a = at(c, ln, 0.0, 0.0, 0.5)
        B.rrect(im, 140, y - 90, 1780, y + 90, 26, (12, 14, 30), 0.85 * a)
        B.circ(im, 220, y, 36, B.mix(cc_, a), -1)
        txt(im, str(i + 1), 220, y, 44, "dark", "c", a, panel=False)
        txt(im, q, 290, y - 22, 36, "ink", "l", a, panel=False)
        txt(im, note, 290, y + 38, 28, "grey", "l", at(c, ln, 0.5, 0, 0.5), panel=False)
        k = smooth(seg(T, K(c, ln, 0.55), K(c, ln, 0.55) + 0.25))
        if k > 0.01:
            sc_ = 1.0 + 0.5 * (1 - k)
            B.rrect(im, 1330, y - 52, 1730, y + 52, 18, cc_, 0.25 * k)
            B.rrect(im, 1330, y - 52, 1730, y + 52, 18, cc_, 1.0 * k, False, 5)
            txt(im, st, 1530, y, int(52 * sc_), cc_, "c", k, panel=False)


# =============================================================================== 157-159: remember three things, then the question
@scene
def final3(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    t159 = K(c, 159, 0.0, -0.05)
    if T < t159:
        txt(im, "yaad rakhne layak teen baatein", 960, 110, 56, "amber", "c", at(c, 157, 0.0, 0.1, 0.6))
        items = [("1", "DART ne 7 ki jagah 33 min diye: malbe ne bhi dhakka diya", 157, 0.3), ("2", "dhoondhna sabse bada kaam: anjaana hissa hi sawaal hai", 158, 0.0),
                 ("3", "koi ek tareeka pakka nahi: har tareeke ki seema hai", 158, 0.55)]
        for i, (n, t, ln, fr) in enumerate(items):
            a = at(c, ln, fr, 0, 0.6)
            y = 340 + i * 210
            B.rrect(im, 200, y - 80, 1720, y + 80, 28, (14, 18, 36), 0.85 * a)
            B.circ(im, 300, y, 44, B.mix("amber", a), -1)
            txt(im, n, 300, y, 56, "dark", "c", a, panel=False)
            txt(im, t, 380, y, 40, "ink", "l", a, panel=False)
    else:
        tt = T - t159
        cx, cy = 960, 540
        place_rock(im, cx, cy, 90, 2, tt * 0.05)
        for i, (rr, sp) in enumerate(((220, 0.5), (330, 0.33), (440, 0.22))):
            B.ell(im, cx, cy, rr, rr * 0.7, B.mix("dim", 0.5), 2)
            a_ = tt * sp + i * 2
            place_rock(im, cx + rr * math.cos(a_), cy + rr * 0.7 * math.sin(a_), 16, 5 + i, a_)
        txt(im, "ab aapse ek sawaal", 960, 110, 56, "amber", "c", smooth(seg(tt, 0.2, 0.8)))
        txt(im, "seemit paisa ho, to pehle kis par lagna chahiye?", 960, 940, 52, "ink", "c", smooth(seg(tt, 0.6, 1.4)))


# =============================================================================== lines 24 and 26 (Tunguska date, flattened forest from above)
@scene
def tunguska_date(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    ex, ey, er = 1100, 540, 380
    earth(im, ex, ey, er, 0.6 + T * 0.04)
    px, py = ex - 60, ey - 250
    k = smooth(seg(T, 0.8, 1.6))
    B.circ(im, px, py, 14, B.mix("red", k), -1)
    ring(im, px, py, 20 + 30 * ((T * 0.8) % 1.0), "red", 3, 0.9 * k * (1 - (T * 0.8) % 1.0))
    B.line(im, px, py, 520, 300, B.mix("amber", 0.8 * k), 3)
    txt(im, "Siberia: Tunguska", 520, 260, 50, "amber", "c", k)
    txt(im, "30 Jun 1908", 520, 760, 90, "amber", "c", smooth(seg(T, 0.3, 1.0)))
    txt(im, "isse bhi purani ghatna", 520, 860, 40, "ink", "c", smooth(seg(T, 0.6, 1.3)))


@scene
def trees_top(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    B.rrect(im, 140, 120, 1780, 930, 30, (22, 44, 30), 1.0)
    cx, cy = 960, 520
    rng = np.random.default_rng(26)
    wave = seg(T, 0.8, 5.0) * 760
    for i in range(1500):
        ang, rr = rng.uniform(0, 6.283), math.sqrt(rng.uniform(0, 1)) * 760
        x, y = cx + rr * math.cos(ang) * 1.05, cy + rr * math.sin(ang) * 0.52 * 1.4
        if not (160 < x < 1760 and 140 < y < 910):
            continue
        if rr < wave:
            f = min(1.0, (wave - rr) / 60)
            L = 14 * f
            B.line(im, x, y, x + L * math.cos(ang), y + L * math.sin(ang), B.mix((40, 100, 70), 0.9), 2)
        else:
            B.circ(im, x, y, 3.5, B.mix((40, 140, 70), 0.95), -1)
    if wave > 0:
        ring(im, cx, cy, wave, "white", 3, 0.4 * (1 - wave / 800))
    k = at(c, 26, 0.0, 0.4, 0.6)
    txt(im, "koi gaddha nahi", 960, 190, 44, "ink", "c", k)
    n = 80 * smooth(seg(T, K(c, 26, 0.35), K(c, 26, 0.35) + 2.5))
    txt(im, f"~{int(n)} million ped gire", 960, 860, 56, "amber", "c", at(c, 26, 0.35, 0, 0.5))
    txt(im, "~2,000 km2 mein", 1500, 190, 40, "orange", "c", at(c, 26, 0.55, 0, 0.5))
