"""rc_explain scenes, part A: first 5 minutes (lines 14-60). Shared pieces (sky, skyline, bus, trees, fireball)."""
import math

import cv2
import numpy as np

import rc_build_long as B
from rc_explain import (scene, smooth, lin, seg, col, lerp, txt, txtw, blit, rock_spr, craft_spr, earth, sun, arrow, dotted, ring, flash, whiten,
                        particles, stars_bg, dial, put, text_spr, W, H)
from rc_explain_scenes import smooth_int, mixview, hm, place_rock

_CACHE = {}


def sky_fill(im, top, bottom, a=1.0):
    k = ("sky", top, bottom)
    if k not in _CACHE:
        g = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        arr = np.array(top, np.float32)[None, None, :] * (1 - g[..., None]) + np.array(bottom, np.float32)[None, None, :] * g[..., None]
        _CACHE[k] = np.repeat(arr, W, axis=1).astype(np.uint8)
    if a >= 0.999:
        im[:] = _CACHE[k]
    else:
        cv2.addWeighted(im, 1 - a, _CACHE[k], a, 0, dst=im)


def skyline_spr(seed=3, lit=0.35, hmax=330, dark=(34, 26, 24)):
    k = ("skyl", seed, lit, hmax, dark)
    if k in _CACHE:
        return _CACHE[k]
    rng = np.random.default_rng(seed)
    spr = np.zeros((hmax + 60, W, 4), np.uint8)
    x = -20
    while x < W:
        w = int(rng.uniform(80, 190))
        h = int(rng.uniform(70, hmax))
        y0 = spr.shape[0] - h
        shade = rng.uniform(0.85, 1.25)
        c = tuple(int(min(255, v * shade)) for v in dark) + (255,)
        cv2.rectangle(spr, (x, y0), (x + w, spr.shape[0]), c, -1)
        for wy in range(y0 + 16, spr.shape[0] - 18, 26):
            for wx in range(x + 12, x + w - 14, 22):
                if rng.random() < lit:
                    cv2.rectangle(spr, (wx, wy), (wx + 9, wy + 13), (110, 200, 245, 255), -1)
        x += w + int(rng.uniform(0, 20))
    spr[-60:, :, :3] = (np.array(dark, np.float32) * 0.9).astype(np.uint8)
    spr[-60:, :, 3] = 255
    _CACHE[k] = spr
    return spr


def bus_spr():
    if "bus" in _CACHE:
        return _CACHE["bus"]
    s = np.zeros((170, 440, 4), np.uint8)
    cv2.rectangle(s, (6, 30), (430, 132), (40, 175, 235, 255), -1, cv2.LINE_AA)
    cv2.rectangle(s, (6, 30), (430, 132), (20, 120, 190, 255), 4, cv2.LINE_AA)
    for k in range(7):
        cv2.rectangle(s, (30 + k * 56, 46), (70 + k * 56, 84), (235, 215, 160, 255), -1, cv2.LINE_AA)
    cv2.rectangle(s, (400, 46), (424, 100), (235, 215, 160, 255), -1, cv2.LINE_AA)
    for wx in (80, 340):
        cv2.circle(s, (wx, 134), 24, (30, 30, 34, 255), -1, cv2.LINE_AA)
        cv2.circle(s, (wx, 134), 10, (170, 170, 175, 255), -1, cv2.LINE_AA)
    _CACHE["bus"] = s
    return s


def fireball(im, pos_fn, T, T0, n=34, step=0.09, size=1.0, c1=(210, 245, 255), c2=(40, 140, 255), grow=14.0):
    for j in range(n, -1, -1):
        tt = T - j * step
        if tt < T0:
            continue
        x, y = pos_fn(tt)
        f = (1 - j / n)
        r = (10 + 38 * lin((tt - T0) / grow)) * size * (0.35 + 0.65 * f)
        B.glow(im, x, y, r * 2.3, c2, 0.5 * f)
        if j % 2 == 0:
            B.circ(im, x, y, r * 0.55, B.mix(c1, 0.35 + 0.65 * f), -1)
    x, y = pos_fn(T)
    r = (10 + 38 * lin((T - T0) / grow)) * size
    B.glow(im, x, y, r * 4.2, c2, 0.8)
    B.glow(im, x, y, r * 2.2, c1, 0.9)
    B.circ(im, x, y, r * 0.8, (255, 255, 255), -1)


def date_chip(im, s, a=1.0, x=80, y=80):
    txt(im, s, x, y, 36, "amber", "l", a)


def stars_dim(c, a):
    """Stars only (no motes) at reduced brightness, added onto the current frame."""
    Bg = B.bg_layers()
    t = c.T
    def pp(v, rng):
        v = v % (2 * rng)
        return int(v if v <= rng else 2 * rng - v)
    o1x, o1y = pp(230 + t * 5, 460), pp(130 + t * 2, 260)
    star = Bg["L1"][o1y:o1y + H, o1x:o1x + W]
    mask = (star.max(axis=2) > 90)[..., None]
    c.im[:] = np.where(mask, np.clip(c.im.astype(np.float32) + star * a, 0, 255), c.im).astype(np.uint8)


def trees_row(im, y, x0, x1, seed=1, h=(40, 80), c=(36, 74, 40), T=0.0, sway=1.5, fall=None):
    """Row of conifers. fall(x) -> 0..1 how far the tree has fallen over (0 = upright)."""
    rng = np.random.default_rng(seed)
    x = x0
    while x < x1:
        hh = rng.uniform(*h)
        w = hh * 0.36
        f = fall(x) if fall else 0.0
        sw = sway * math.sin(T * 1.3 + x * 0.05) * (1 - f)
        ang = f * 1.45
        tip = (x + math.sin(ang) * hh + sw, y - math.cos(ang) * hh)
        B.polyf(im, [(x - w, y), tip, (x + w, y)], c)
        x += rng.uniform(w * 0.9, w * 1.5)


# =============================================================================== lines 14-15: how big is the danger / yearly bursts
@scene
def earth_incoming(c, **p):
    """Rocks of very different sizes stream toward Earth (the question: how big is the danger?)."""
    stars_bg(c)
    im, T = c.im, c.T
    earth(im, 1480, 620, 330, T * 0.12)
    rng = np.random.default_rng(14)
    sizes = [10, 16, 26, 42, 70, 110]
    for i, s_ in enumerate(sizes):
        per = 5.0
        ph = ((T * (0.5 + 0.08 * i) / per + i / len(sizes)) % 1.0)
        x = lerp(-150, 1200, ph)
        y = lerp(160 + i * 110, 560 + (i - 3) * 30, ph)
        a = lin(ph * 8) * (1 - lin((ph - 0.9) * 10))
        place_rock(im, x, y, s_, 20 + i, T * (0.3 + 0.1 * i), a)
    txt(im, "khatra kitna bada?", 400, 940, 56, "amber", "c", smooth(seg(T, 0.4, 1.2)))


@scene
def airburst_years(c, **p):
    """Earth turning; about once a year a small flash high in the atmosphere. A year counter ticks."""
    stars_bg(c)
    im, T = c.im, c.T
    ex, ey, er = 1180, 540, 380
    earth(im, ex, ey, er, T * 0.1 + 0.5)
    yrs = 7
    per = (c.dur + 0.5) / yrs
    cur = int(T / per)
    for i in range(min(cur + 1, yrs)):
        age = T - i * per
        if age < 0 or age > 1.6:
            continue
        rng = np.random.default_rng(100 + i)
        ang, rr = rng.uniform(0, 6.28), math.sqrt(rng.uniform(0.05, 0.8)) * er
        px, py = ex + rr * math.cos(ang), ey + rr * math.sin(ang) * 0.9
        k = age / 1.6
        B.glow(im, px, py, 60 * (1 - 0.3 * k) + 20, (210, 240, 255), 0.95 * (1 - k))
        B.circ(im, px, py, 14 + 70 * k, B.mix((210, 240, 255), 0.9 * (1 - k)), 3)
    # year counter + ticks
    txt(im, f"saal {min(cur + 1, yrs)}", 330, 420, 84, "amber", "c", 1.0)
    txt(im, "har saal ek chhota dhamaka", 330, 520, 38, "ink", "c", smooth(seg(T, 0.5, 1.2)))
    for i in range(yrs):
        done = i <= cur
        B.circ(im, 130 + i * 70, 640, 18, B.mix("amber" if done else "dim", 1.0 if done else 0.5), -1 if done else 3)
    txt(im, "satellite record", 330, 760, 32, "grey", "c", smooth(seg(T, 1.0, 1.8)))


# =============================================================================== line 16: energy of a small airburst
@scene
def airburst_city(c, kt=5, label="5 kt = 5,000 t TNT", sub="", **p):
    """Side view: small bright burst high above a city skyline, shock ring spreads. Used for the yearly 5 kt event."""
    im, T = c.im, c.T
    sky_fill(im, (60, 32, 18), (90, 120, 190), 1.0)
    stars_dim(c, 0.3)
    sk = skyline_spr(5, 0.25, 280)
    blit(im, sk, W / 2, 1080 - sk.shape[0] / 2 + 10, 1.0)
    bp = (960, 300)
    def pos(t_):
        k = lin(t_ / 2.2)
        return lerp(1700, bp[0], k), lerp(-60, bp[1], k)
    if T < 2.2:
        fireball(im, pos, T, 0.0, size=0.6, grow=3)
    else:
        age = T - 2.2
        flash(im, bp[0], bp[1], age / 2.0, 240)
        for q, d0 in enumerate((0.0, 0.6)):
            a = max(0.0, 1 - (age - d0) / 5.0) if age > d0 else 0
            if a > 0:
                B.circ(im, bp[0], bp[1], 30 + (age - d0) * 160, B.mix((225, 238, 255), 0.6 * a), max(2, int(6 * a)))
        particles(im, bp[0], bp[1], age, 40, 3, (40, 260), (0, 6.28), (2, 5), 1.2, 2.5, (210, 225, 240), 50.0, glowc=(60, 160, 255))
    txt(im, label, 960, 830, 52, "amber", "c", smooth(seg(T, 2.6, 3.4)))
    if sub:
        txt(im, sub, 960, 930, 34, "ink", "c", smooth(seg(T, 3.2, 4.0)))


# =============================================================================== CHELYABINSK master (lines 17-21)
CH_BURST = (930, 340)


def _ch_path(T):
    k = lin((T - 0.8) / 14.3) ** 0.9
    return lerp(1950, CH_BURST[0], k), lerp(-90, CH_BURST[1], k)


@scene
def chely(c, **p):
    im, T = c.im, c.T
    fl = seg(T, 15.1, 15.5) * (1 - seg(T, 15.5, 17.2))
    sky_fill(im, (62, 34, 18), (95, 130, 205), 1.0)
    stars_dim(c, 0.35)
    sk = skyline_spr(3, 0.3, 330)
    B.glow(im, 700, 980, 1200, (70, 140, 230), 0.12)
    blit(im, sk, W / 2, 1080 - sk.shape[0] / 2 + 10, 1.0)
    if T < 15.1:
        fireball(im, _ch_path, T, 0.8)
    else:
        age = T - 15.1
        for q, d0 in enumerate((0.0, 0.5, 1.0)):
            a = max(0.0, 1 - (age - d0) / 5.5) if age > d0 else 0
            if a > 0:
                B.circ(im, CH_BURST[0], CH_BURST[1], 40 + (age - d0) * 220, B.mix((220, 235, 255), 0.7 * a), max(2, int(8 * a)))
        flash(im, CH_BURST[0], CH_BURST[1], age / 2.4, 520)
        particles(im, CH_BURST[0], CH_BURST[1], age, 70, 5, (60, 420), (0, 6.28), (2, 6), 1.1, 3.0, (200, 220, 240), 70.0, glowc=(60, 160, 255))
    if fl > 0:
        whiten(im, 0.55 * fl)
    if T < 15.1:
        date_chip(im, "15 Feb 2013", smooth(seg(T, 0.3, 1.0)))
        txt(im, "Chelyabinsk, Russia", 80, 140, 34, "ink", "l", smooth(seg(T, 0.6, 1.3)) * (1 - seg(T, 6.5, 7.1)))
        txt(im, "subah ka aasmaan", 960, 940, 34, "ink", "c", smooth(seg(T, 2.0, 2.8)) * (1 - seg(T, 6.5, 7.1)))
    k = smooth(seg(T, 8.0, 8.9)) * (1 - smooth(seg(T, 14.6, 15.1)))
    if k > 0:
        sc = 15.0
        ox, oy = 230, 720
        B.rrect(im, ox - 150, oy - 330, ox + 560, oy + 130, 24, (10, 10, 18), 0.55 * k)
        place_rock(im, ox + 120, oy - 110, 20 * sc / 2 * 1.05, 4, T * 0.15, k)
        blit(im, bus_spr(), ox + 330, oy + 25, 12 * sc / 440.0 * 1.0, 0.0, k)
        txt(im, "patthar ~20 m", ox + 120, oy - 300, 36, "amber", "c", k, panel=False)
        txt(im, "bus ~12 m", ox + 330, oy + 92, 32, "ink", "c", k, panel=False)
    if 15.8 < T < 21:
        txt(im, "~500 kt", 960, 640, 76, "amber", "c", smooth(seg(T, 15.9, 16.6)) * (1 - seg(T, 20.2, 20.9)))
        txt(im, "dhamaka aasmaan me hi", 960, 735, 36, "ink", "c", smooth(seg(T, 16.4, 17.0)) * (1 - seg(T, 20.2, 20.9)))
    if 20.7 <= T < 26.6:
        a = smooth(seg(T, 20.9, 21.5)) * (1 - smooth(seg(T, 26.2, 26.6)))
        cv2.addWeighted(im, 1 - 0.6 * a, np.zeros_like(im), 0.6 * a, 0, dst=im)
        prog = smooth(seg(T, 21.4, 24.4))
        cols_ = 64
        for i in range(int(1600 * prog)):
            cx_, cy_ = 960 - 63 * 9 + (i % cols_) * 18, 400 + (i // cols_) * 18
            B.circ(im, cx_, cy_, 5.5, B.mix("amber", a), -1)
        txt(im, f"~{int(1600 * prog):,}", 960, 250, 84, "amber", "c", a)
        txt(im, "logon ne ilaaj maanga", 960, 900, 40, "ink", "c", a)
        txt(im, "kisi ki jaan nahi gayi", 960, 975, 36, "green", "c", a * smooth(seg(T, 23.0, 23.8)))
    if T >= 26.4:
        a = smooth(seg(T, 26.4, 27.0))
        sky_fill(im, (60, 32, 16), (90, 125, 200), a)
        stars_dim(c, 0.2)
        ff_ = 1 - seg(T, 26.5, 29.0)
        B.glow(im, 260, 600, int(420 * (0.6 + ff_ * 0.8)), (200, 235, 255), 0.55 + 0.4 * ff_)
        B.circ(im, 260, 600, 18 + 24 * ff_, (255, 255, 255), -1)
        blit(im, skyline_spr(8, 0.0, 120, (30, 24, 22)), W / 2, 1080 - 90 + 10, 1.0)
        bx0, by0, bx1, by1 = 1180, 300, 1780, 1000
        cv2.rectangle(im, (bx0, by0), (bx1, by1), (42, 36, 34), -1)
        cv2.rectangle(im, (bx0, by0), (bx1, by1), (90, 84, 80), 3)
        arrive = 33.0
        for r_ in range(4):
            for q in range(4):
                wx0, wy0 = bx0 + 40 + q * 142, by0 + 50 + r_ * 160
                cv2.rectangle(im, (wx0, wy0), (wx0 + 108, wy0 + 118), (150, 170, 120), -1)
                cv2.rectangle(im, (wx0, wy0), (wx0 + 108, wy0 + 118), (200, 205, 190), 3)
                t_c = arrive + 0.02 * (r_ * 4 + q)
                if T > t_c:
                    kk = smooth(seg(T, t_c, arrive + 0.45))
                    cx_, cy_ = wx0 + 54, wy0 + 59
                    rng = np.random.default_rng(r_ * 9 + q)
                    for ang in np.linspace(0, 6.28, 9)[:-1] + rng.uniform(0, 1):
                        L_ = (36 + 30 * rng.random()) * kk
                        B.line(im, cx_, cy_, cx_ + L_ * math.cos(ang), cy_ + L_ * math.sin(ang), (245, 250, 255), 2)
                    B.ell(im, cx_, cy_, 22 * kk, 22 * kk, (245, 250, 255), 2)
                    if T > arrive + 0.5:
                        d_ = T - arrive - 0.5
                        for sh in range(4):
                            yy_ = cy_ + 6 + 120 * d_ * d_ * (0.6 + 0.3 * sh)
                            B.rrect(im, cx_ - 30 + sh * 18, yy_, cx_ - 22 + sh * 18, yy_ + 14, 2, (235, 245, 255), 0.7 * (1 - lin(d_ / 1.3)))
        wv = lin((T - 26.9) / (arrive - 26.9))
        wx = 260 + (bx0 - 260) * wv
        if 0 < wv <= 1:
            for q in range(3):
                B.ell(im, wx - q * 26, 700, 150, 360, B.mix((225, 238, 255), 0.55 - q * 0.15), 5 - q, 0, -70, 70)
        tl0, tl1, ty = 300, 1620, 960
        B.line(im, tl0, ty, tl1, ty, B.mix("dim", a), 4)
        ph = lin((T - 26.8) / (arrive - 26.8 + 0.8))
        B.circ(im, tl0 + (tl1 - tl0) * ph, ty, 14, B.mix("amber", a), -1)
        txt(im, "chamak", tl0, ty - 46, 32, "amber", "c", a, panel=False)
        txt(im, "kuch minute baad", (tl0 + tl1) / 2, ty - 46, 32, "ink", "c", a, panel=False)
        txt(im, "shock wave", tl1, ty - 46, 32, "red", "c", a, panel=False)
        if T > arrive:
            txt(im, "tooti khidkiyan", bx0 + 300, 230, 40, "red", "c", smooth(seg(T, arrive + 0.2, arrive + 0.8)))


# =============================================================================== lines 22-23: a rock nobody saw, from the sun side
@scene
def unseen(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    sun(im, 60, 540, 90, T, 1.0)
    earth(im, 1560, 600, 200, T * 0.1)
    # telescope view cone pointing away from the sun (empty sky)
    ov = im.copy()
    pts = np.array([[1560, 400], [1000, 80], [1700, 40]], np.int32)
    cv2.fillPoly(ov, [pts], (110, 80, 40))
    cv2.addWeighted(ov, 0.25, im, 0.75, 0, dst=im)
    B.polyl(im, [(1560, 400), (1000, 80), (1700, 40)], B.mix("blue", 0.5), 2, True)
    txt(im, "telescope ka nazaara: khaali", 1320, 160, 32, "blue", "c", smooth(seg(T, 0.5, 1.2)))
    # the rock: invisible in the glare, faint near Earth
    k = lin((T - 0.4) / 7.0)
    x = lerp(130, 1380, k)
    y = lerp(540, 590, k)
    r = lerp(5, 30, k ** 1.4)
    vis = smooth(seg(x, 650, 1100))
    for j in range(24):
        kk = lin((T - 0.4 - j * 0.04) / 7.0)
        xx = lerp(130, 1380, kk)
        B.circ(im, xx, lerp(540, 590, kk), 2.5, B.mix("amber", 0.12 * vis * (1 - j / 24)), -1)
    place_rock(im, x, y, r, 7, T, 0.25 + 0.75 * vis, 0.55)
    if T < 4.5:
        txt(im, "kisi ne nahi dekha", 760, 880, 52, "red", "c", smooth(seg(T, 1.0, 1.8)) * (1 - seg(T, 4.2, 4.8)))
    else:
        arrow(im, 230, 700, 700, 700, "amber", 8, 1.0, 30, smooth(seg(T, 5.0, 5.8)))
        txt(im, "suraj ki taraf se aaya", 700, 790, 48, "amber", "c", smooth(seg(T, 5.0, 5.8)))


# =============================================================================== line 25: Tunguska airburst (no crater)
@scene
def airburst_side(c, **p):
    im, T = c.im, c.T
    sky_fill(im, (40, 30, 24), (110, 130, 150), 1.0)
    stars_dim(c, 0.25)
    gy = 900
    cv2.rectangle(im, (0, gy), (W, H), (24, 44, 30), -1)
    # trees: fall radially outward after the burst
    bx = 960
    t_hit = 4.3
    def fall(x):
        if T < t_hit + 0.6:
            return 0.0
        d = abs(x - bx)
        return smooth(seg(T - t_hit - 0.6, d / 900.0, d / 900.0 + 0.45))
    trees_row(im, gy, -20, W + 20, 5, (60, 120), (42, 88, 46), T, 1.5, fall)
    trees_row(im, gy + 40, -20, W + 20, 6, (90, 160), (30, 70, 38), T, 1.5, fall)
    by = 330
    if T < t_hit:
        k = lin(T / t_hit)
        x, y = lerp(220, bx, k), lerp(-40, by, k)
        fireball(im, lambda t_: (lerp(220, bx, lin(t_ / t_hit)), lerp(-40, by, lin(t_ / t_hit))), T, 0.0, size=0.55, grow=4)
    else:
        age = T - t_hit
        flash(im, bx, by, age / 2.2, 480)
        for q, d0 in enumerate((0.0, 0.7)):
            a = max(0.0, 1 - (age - d0) / 4.5) if age > d0 else 0
            if a > 0:
                B.circ(im, bx, by, 40 + (age - d0) * 260, B.mix((225, 238, 255), 0.5 * a), max(2, int(6 * a)))
        # downward pressure cone to the ground
        a = smooth(seg(age, 0.3, 1.0)) * (1 - seg(age, 3.0, 4.5))
        ov = im.copy()
        cv2.fillPoly(ov, [np.array([[bx, by], [bx - 520, gy], [bx + 520, gy]], np.int32)], (170, 210, 255))
        cv2.addWeighted(ov, 0.18 * a, im, 1 - 0.18 * a, 0, dst=im)
    # height marker
    ka = smooth(seg(T, 5.2, 6.0))
    B.line(im, 1560, gy, 1560, by, B.mix("amber", ka), 4)
    B.line(im, 1540, by, 1580, by, B.mix("amber", ka), 4)
    B.line(im, 1540, gy, 1580, gy, B.mix("amber", ka), 4)
    txt(im, "5-10 km", 1560, (by + gy) / 2, 44, "amber", "c", ka)
    txt(im, "patthar ~50-60 m", 300, 190, 40, "ink", "c", smooth(seg(T, 0.4, 1.2)) * (1 - seg(T, 4.0, 4.4)))
    txt(im, "zameen tak nahi pahuncha", 960, 1010, 38, "ink", "c", smooth(seg(T, 6.0, 6.8)))
    date_chip(im, "30 Jun 1908  |  Tunguska", smooth(seg(T, 0.2, 0.9)))


# =============================================================================== line 27: estimates differ (swarm of guesses)
@scene
def estimate_swarm(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    x0, x1, y = 260, 1660, 560
    B.line(im, x0, y, x1, y, B.mix("grey", 0.8), 5)
    a = smooth(seg(T, 0.2, 0.9))
    txt(im, "kam", x0, y + 70, 34, "grey", "c", a, panel=False)
    txt(im, "zyada", x1, y + 70, 34, "grey", "c", a, panel=False)
    txt(im, "dhamake ki taakat ka andaza", 960, 250, 48, "ink", "c", a)
    rng = np.random.default_rng(27)
    for i in range(16):
        base = rng.uniform(x0 + 60, x1 - 60)
        ph = rng.uniform(0, 6.28)
        sp = rng.uniform(0.5, 1.2)
        px = base + 90 * math.sin(T * sp + ph)
        py = y - 110 - (i % 4) * 46 + 12 * math.sin(T * 1.4 + ph)
        ap = smooth(seg(T, 0.6 + i * 0.12, 1.1 + i * 0.12))
        B.circ(im, px, py, 14, B.mix("amber", 0.9 * ap), -1)
        B.line(im, px, py + 18, px, y - 6, B.mix("amber", 0.35 * ap), 2)
    # band
    bnd = smooth(seg(T, 3.0, 4.2))
    B.rrect(im, x0 + 140, y - 40, x1 - 90, y + 8, 12, "red", 0.35 * bnd)
    B.rrect(im, x0 + 140, y - 40, x1 - 90, y + 8, 12, "red", 0.95 * bnd, False, 3)
    txt(im, "ANJAAN: andaze alag-alag", 960, 800, 44, "red", "c", smooth(seg(T, 3.6, 4.4)))
    txt(im, "isliye hum range me bolte hain", 960, 880, 34, "ink", "c", smooth(seg(T, 5.0, 5.8)))
