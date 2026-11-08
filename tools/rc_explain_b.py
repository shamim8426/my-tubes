"""rc_explain scenes, part B: lines 28-62 (size ladder, extinction, rarity, status, DART set-up, push basics, result, two methods)."""
import math

import cv2
import numpy as np

import rc_build_long as B
from rc_explain import (scene, smooth, lin, seg, col, lerp, txt, txtw, blit, rock_spr, craft_spr, earth, sun, arrow, dotted, ring, flash, whiten,
                        particles, stars_bg, dial, put, text_spr, W, H, K, real, bar, view_seq)
from rc_explain_scenes import smooth_int, mixview, hm, place_rock
from rc_explain_a import sky_fill, stars_dim, trees_row


def at(c, line, frac=0.0, off=0.0, dur=0.35):
    t0 = K(c, line, frac, off)
    return smooth(seg(c.T, t0, t0 + dur))


def until(c, line, frac=0.0, off=0.0, dur=0.3):
    """1 before the moment, 0 after (fade out)."""
    t0 = K(c, line, frac, off)
    return 1 - smooth(seg(c.T, t0, t0 + dur))


def inset(im, c, rel, x, y, w, h, tin=0.0, a=1.0, label="", crop=None, z=(1.0, 1.08)):
    """Small real picture window (rounded border) with a tiny credit label."""
    if a <= 0.01:
        return
    save = c.im
    tmp = np.zeros_like(im)
    c.im = tmp
    real(c, rel, tin, z[0], z[1], crop)
    c.im = save
    win = cv2.resize(tmp, (int(w), int(h)), interpolation=cv2.INTER_AREA)
    x0, y0 = int(x - w / 2), int(y - h / 2)
    roi = im[y0:y0 + int(h), x0:x0 + int(w)]
    roi[:] = (roi * (1 - a) + win * a).astype(np.uint8)
    B.rrect(im, x0 - 3, y0 - 3, x0 + w + 3, y0 + h + 3, 8, (220, 226, 240), a * 0.9, False, 3)
    if label:
        txt(im, label, x0 + 12, y0 + h - 26, 22, "ink", "l", a, pad=8)


# =============================================================================== size ladder, lines 28-32
_LAD = [(20, "~20 m", "shehar mein kaanch tootte hain", 28, 0.0), (55, "50-60 m", "jungle gir jaata hai", 29, 0.0),
        (140, "140 m se bade", "NASA: kshetriya nuksaan", 30, 0.18), (1000, "1 km se bade", "poori duniya par asar", 31, 0.12),
        (10000, "~10 km", "Chicxulub, Mexico | 66 million saal pehle", 32, 0.0)]


def _ladder_scale(c):
    """metres per pixel at master time T (piecewise log-interpolated)."""
    T = c.T
    s = [D / 430.0 for D, *_ in _LAD]
    ls = math.log(s[0])
    for k in range(1, len(_LAD)):
        t0 = K(c, _LAD[k][3], 0.0, -0.85)
        if T < t0:
            break
        ls = lerp(math.log(s[k - 1]), math.log(s[k]), smooth(seg(T, t0, t0 + 1.5)))
    return math.exp(ls)


_BLD = None


def _buildings():
    global _BLD
    if _BLD is None:
        rng = np.random.default_rng(28)
        out, x = [], -9000.0
        while x < 9000:
            w = rng.uniform(14, 34)
            out.append((x, w, rng.uniform(8, 48), rng.uniform(0.8, 1.2), rng.random()))
            x += w + rng.uniform(2, 14)
        _BLD = out
    return _BLD


@scene
def size_ladder(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    s = _ladder_scale(c)
    gy = 860
    cx, cy = 960, 500
    # city strip (metres -> pixels)
    for x, w, h, sh, r in _buildings():
        px0, px1 = cx + x / s, cx + (x + w) / s
        if px1 < 0 or px0 > W:
            continue
        hp = h / s
        if hp < 1.5:
            continue
        cc_ = (int(40 * sh), int(33 * sh), int(30 * sh))
        cv2.rectangle(im, (int(px0), int(gy - hp)), (int(px1), gy), cc_, -1)
        if px1 - px0 > 26 and hp > 40:
            for wy in np.arange(gy - hp + 12, gy - 8, 22):
                for wx in np.arange(px0 + 7, px1 - 9, 17):
                    if (int(wx * 13 + wy * 7) % 7) < 3:
                        cv2.rectangle(im, (int(wx), int(wy)), (int(wx + 7), int(wy + 11)), (110, 200, 245), -1)
    cv2.rectangle(im, (0, gy), (W, H), (26, 22, 20), -1)
    # rocks, biggest first, each fades in when its rung begins
    order = list(range(len(_LAD)))[::-1]
    for k in order:
        D = _LAD[k][0]
        a = 1.0 if k == 0 else smooth(seg(T, K(c, _LAD[k][3], 0.0, -1.1), K(c, _LAD[k][3], 0.0, -0.45)))
        R = D / s / 2.0
        if a <= 0.01 or R < 1.2:
            continue
        if R < 1700:
            place_rock(im, cx, cy, R, 30 + k, T * 0.03 * (k + 1), a, 1.0 - 0.0 * k, (1.0, 0.92))
        if k < len(_LAD) - 1 or True:
            B.circ(im, cx, cy, R * 1.04, B.mix("amber", 0.35 * a), 2)
    # rung label
    for k, (D, lab, sub, ln, fr) in enumerate(_LAD):
        t0 = K(c, ln, fr, 0.0)
        t1 = K(c, _LAD[k + 1][3], _LAD[k + 1][4], 0.0) if k + 1 < len(_LAD) else 1e9
        a = smooth(seg(T, t0, t0 + 0.3)) * (1 - smooth(seg(T, t1 - 0.35, t1)))
        if a > 0.01:
            txt(im, lab, 110, 150, 78, "amber", "l", a)
            txt(im, sub, 110, 245, 38, "ink", "l", a * smooth(seg(T, t0 + 0.4, t0 + 0.9)))
    # scale bar
    for L in (5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000):
        if 140 <= L / s <= 420:
            xs0 = 110
            B.line(im, xs0, 960, xs0 + L / s, 960, "ink", 4)
            B.line(im, xs0, 948, xs0, 972, "ink", 4)
            B.line(im, xs0 + L / s, 948, xs0 + L / s, 972, "ink", 4)
            txt(im, f"{L:,} m" if L < 1000 else f"{L // 1000} km", xs0 + L / s + 24, 960, 30, "ink", "l", 0.95, pad=8)
            break
    # mini ladder on the right
    x_l = 1820
    ys = [880 - 135 * k for k in range(len(_LAD))]
    B.line(im, x_l, ys[0], x_l, ys[-1], B.mix("dim", 0.7), 3)
    for k, (D, lab, *_r) in enumerate(_LAD):
        act = smooth(seg(T, K(c, _LAD[k][3], 0.0, -0.2), K(c, _LAD[k][3], 0.0, 0.3)))
        B.circ(im, x_l, ys[k], 9 + 7 * act, B.mix("amber", 0.35 + 0.65 * act), -1)
        txt(im, f"{D:,} m" if D < 1000 else f"{D // 1000} km", x_l - 26, ys[k], 26, "ink", "r", 0.5 + 0.5 * act, panel=False)


# =============================================================================== extinction + volcano, lines 33-34
def _extinct_view(im, T, c):
    earth(im, 1320, 520, 330, T * 0.05 + 1.0)
    dust = smooth(seg(T, 1.2, 4.6))
    ov = im.copy()
    cv2.circle(ov, (1320, 520), int(330 * (1.0 + 0.12 * dust)), (22, 40, 70), -1, cv2.LINE_AA)
    cv2.addWeighted(ov, 0.78 * dust, im, 1 - 0.78 * dust, 0, dst=im)
    B.glow(im, 540, 520, 340, (60, 170, 255), 0.6 * (1 - 0.8 * dust))
    B.circ(im, 540, 520, 60, B.mix((205, 245, 255), 1 - 0.7 * dust), -1)
    for q in range(8):
        a_ = math.radians(-26 + q * 7.5)
        B.line(im, 620, 520 + 40 * math.sin(a_ * 2), 990 - 330 * dust * 0 if False else 1000, 520 + 40 * math.sin(a_ * 2), (0, 0, 0), 0) if False else None
    rng = np.random.default_rng(33)
    n = 28
    for i in range(n):
        x, y = 230 + (i % 14) * 62, 850 + (i // 14) * 70
        die = 1.6 + rng.random() * 3.2
        alive = 1 - smooth(seg(T, die, die + 0.5))
        cc_ = tuple(int(lerp(70, v, alive)) for v in B.C("green"))
        B.circ(im, x, y, 17, cc_, -1)
        B.circ(im, x, y - 26, 9, cc_, -1)
    txt(im, "dhool se dhoop ghati", 1320, 150, 40, "ink", "c", smooth(seg(T, 1.6, 2.4)))
    txt(im, "prajatiyan", 660, 790, 30, "grey", "c", 0.9, panel=False)
    txt(im, "zyaadatar vaigyanik: badi vilupti isi takkar se juda", 960, 985, 38, "amber", "c", smooth(seg(T, 0.3, 1.0)))


def _volcano_view(im, T, c):
    sky_fill(im, (40, 28, 30), (60, 70, 110), 1.0)
    gy = 900
    B.polyf(im, [(260, gy), (700, 360), (840, 330), (900, 366), (1340, gy)], (46, 56, 76))
    B.polyf(im, [(700, 360), (840, 330), (790, 400)], (60, 80, 110))
    for k in range(5):
        a = 0.55 + 0.25 * math.sin(T * 3 + k)
        B.line(im, 820 + k * 8, 336, 760 + k * 56 - 30, 700 + 20 * k, B.mix((60, 120, 255), a * 0.8), 5)
    B.glow(im, 820, 330, 300, (40, 110, 255), 0.7 + 0.1 * math.sin(T * 4))
    rng = np.random.default_rng(34)
    for i in range(70):
        ph = (T * 0.22 + i * 0.151) % 1.0
        x = 820 + (rng.random() - 0.5) * 80 + ph * (rng.random() - 0.3) * 600
        y = 330 - ph * 560
        r = 24 + 120 * ph
        g = int(110 - 50 * ph)
        ov = im.copy()
        cv2.circle(ov, (int(x), int(y)), int(r), (g, g, g + 8), -1, cv2.LINE_AA)
        cv2.addWeighted(ov, 0.22 * (1 - ph), im, 1 - 0.22 * (1 - ph), 0, dst=im)
    cv2.rectangle(im, (0, gy), (W, H), (22, 30, 22), -1)
    txt(im, "kuch shodhkarta: jwalamukhi ki bhi bhumika", 960, 985, 38, "amber", "c", smooth(seg(T, 0.3, 1.0)))


@scene
def extinction(c, **p):
    stars_bg(c)
    base = c.im.copy()
    t_cut = K(c, 34, 0.0)
    view_seq(c, base, [(-1, t_cut, lambda v: _extinct_view(v, c.T, c)), (t_cut, 1e9, lambda v: _volcano_view(v, c.T - t_cut, c))])


# =============================================================================== how rare: lines 35-36
@scene
def rare_ladder(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    x0, x1 = 400, 1780
    lanes = [("har saal: ~5 kt", 330, 1.0, 22, "amber"), ("Tunguska jaise: kai sau - hazaar saal", 560, 4.2, 48, "orange"), ("~10 km: karodon saal", 790, 13.0, 90, "red")]
    yr = 1000 * smooth(seg(T, 0.2, 6.3))
    for lab, y, per, fr, cc_ in lanes:
        B.line(im, x0, y, x1, y, B.mix("dim", 0.8), 4)
        txt(im, lab, x0, y - 62, 34, "ink", "l", smooth(seg(T, 0.2, 0.8)), panel=False)
        n_ev = int(6.2 / per) + (1 if per > 5 else 0)
        if per == 1.0:
            evs = [0.4 + 0.5 * i for i in range(12)]
        elif per == 4.2:
            evs = [1.6, 4.4]
        else:
            evs = [5.6]
        for te in evs:
            ex = lerp(x0, x1, te / 6.4)
            if T > te:
                B.circ(im, ex, y, 9, B.mix(cc_, 0.9), -1)
                age = (T - te) / 1.0
                if age < 1.0:
                    B.glow(im, ex, y, fr * (0.6 + age), (230, 245, 255), 0.9 * (1 - age))
                    B.circ(im, ex, y, 14 + fr * age, B.mix(cc_, 0.9 * (1 - age)), 3)
    px = lerp(x0, x1, seg(T, 0.2, 6.3))
    B.line(im, px, 250, px, 860, B.mix("white", 0.55), 2)
    txt(im, f"{int(yr)} saal", px, 215, 40, "white", "c", 1.0)
    # uncertainty: lane 2 band widens at line 36
    k = at(c, 36, 0.0, 0.0, 0.8)
    if k > 0.01:
        xa, xb = lerp(x0, x1, 0.15), lerp(x0, x1, 0.95)
        B.rrect(im, xa, 535, xb, 585, 16, "red", 0.30 * k)
        B.rrect(im, xa, 535, xb, 585, 16, "red", 0.95 * k, False, 3)
        arrow(im, 960, 640, xa, 640, "red", 5, k, 22, k)
        arrow(im, 960, 640, xb, 640, "red", 5, k, 22, k)
        txt(im, "andaze me kai guna ki anishchitta", 960, 700, 38, "red", "c", k)


# =============================================================================== known vs unknown, lines 37-38
@scene
def known_unknown(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    earth(im, 1500, 560, 130, T * 0.1)
    rng = np.random.default_rng(37)
    pts = [(rng.uniform(150, 1750), rng.uniform(140, 960)) for _ in range(70)]
    pts = [q for q in pts if math.hypot(q[0] - 1500, q[1] - 560) > 260]
    a37 = at(c, 37, 0.1, 0, 0.6)
    for i, (x, y) in enumerate(pts):
        ph = i * 0.7
        xx, yy = x + 14 * math.sin(T * 0.6 + ph), y + 10 * math.cos(T * 0.5 + ph)
        B.circ(im, xx, yy, 6, B.mix("green", 0.9 * a37), -1)
        B.ell(im, xx, yy, 14, 14, B.mix("green", 0.35 * a37), 1)
    txt(im, "jaane-pehchaane pind: koi bada khatra nahi", 960, 110, 44, "green", "c", a37)
    # unknown: dark patches sweep in at line 38
    k = at(c, 38, 0.15, 0, 1.2)
    if k > 0.01:
        ov = im.copy()
        for (x, y, r) in ((420, 380, 330), (1000, 760, 380), (780, 220, 260), (1250, 330, 230)):
            cv2.circle(ov, (x, y), int(r * k), (4, 6, 14), -1, cv2.LINE_AA)
        cv2.addWeighted(ov, 0.88, im, 0.12, 0, dst=im)
        for i, (x, y) in enumerate(((420, 380), (1000, 760), (780, 220), (1250, 330))):
            q = 0.5 + 0.5 * math.sin(T * 3 + i)
            txt(im, "?", x, y, 120, "red", "c", k * (0.55 + 0.4 * q), panel=False)
        txt(im, "jo abhi dhundha hi nahi gaya: wahi asli sawaal", 960, 985, 44, "red", "c", k)


# =============================================================================== line 39: can we push it away?
@scene
def can_we_push(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    earth(im, 1560, 620, 210, T * 0.1)
    # rock approaches along a straight dotted line toward Earth, craft hits at T=3.1
    hit = 3.1
    start = (140, 330)
    tgt = (1480, 620)
    def pos(t_):
        if t_ < hit:
            k = t_ / 7.0
            return lerp(start[0], tgt[0], k), lerp(start[1], tgt[1], k)
        k0 = hit / 7.0
        hx, hy = lerp(start[0], tgt[0], k0), lerp(start[1], tgt[1], k0)
        d = t_ - hit
        vx, vy = (tgt[0] - start[0]) / 7.0, (tgt[1] - start[1]) / 7.0
        return hx + (vx + 20) * d, hy + (vy - 130) * d
    dotted(im, [start, tgt], "red", 3, 0.7 * smooth(seg(T, 0.2, 0.8)), 14, 12)
    x, y = pos(T)
    if T > hit:
        hx, hy = pos(hit)
        B.polyl(im, [(hx, hy), (x, y)], B.mix("amber", 0.95), 6)
        dotted(im, [(x, y), (x + 900, y - 150)], "amber", 4, 0.8, 16, 12)
    place_rock(im, x, y, 70, 4, T * 0.4)
    if T < hit:
        cx_ = x - 640 + 640 * smooth(seg(T, 0.0, hit - 0.05)) * 0 + (T - hit) * 0
        cxx = lerp(x - 260 * 0, x, 0)
        pc = (x - 70 - 520 * (1 - lin(T / hit)) ** 2 * 1.2, y + 4)
        blit(im, craft_spr(), pc[0], pc[1], 0.28, 0.0)
    else:
        d = T - hit
        flash(im, x - 66, y, d / 0.8, 190)
        particles(im, x - 60, y, d, 30, 8, (60, 260), (math.pi * 0.6, math.pi * 1.4), (2, 4), 1.6, 1.6, (190, 195, 205))
        k = smooth(seg(T, hit + 0.3, hit + 0.9))
        arrow(im, x - 10, y - 130, x + 150, y - 130, "amber", 7, k, 26, k)
        txt(im, "ek dhakka", x + 70, y - 180, 38, "amber", "c", k)
    txt(im, "agar patthar aata dikhe...", 700, 960, 46, "ink", "c", smooth(seg(T, 0.3, 1.0)) * (1 - smooth(seg(T, 3.0, 3.4))))
    txt(im, "kya hum use dhakel sakte hain?", 700, 960, 46, "amber", "c", smooth(seg(T, 3.4, 4.0)) * (1 - smooth(seg(T, 5.6, 6.0))))
    txt(im, "ek baar ise sach mein aazmaya gaya", 700, 960, 46, "ink", "c", smooth(seg(T, 5.9, 6.5)))


# =============================================================================== line 40: the mission name
@scene
def acronym(c, **p):
    real(c, "footage/pia25329_dart_at_didymos_illustration.jpg", 0, 1.0, 1.1, dark=0.4, fx=0.55)
    im, T = c.im, c.T
    rows = [("D", "ouble", 0.5), ("A", "steroid", 1.4), ("R", "edirection", 2.3), ("T", "est", 3.2)]
    B.rrect(im, 90, 250, 840, 790, 30, (10, 10, 18), 0.58 * smooth(seg(T, 0.2, 0.7)))
    for i, (L, rest, t0) in enumerate(rows):
        a = smooth(seg(T, t0, t0 + 0.45))
        y = 340 + i * 125
        txt(im, L, 150 + (1 - a) * -40, y, 110, "amber", "l", a, panel=False)
        txt(im, rest, 250 + (1 - a) * 40, y + 12, 70, "ink", "l", a, panel=False)
    txt(im, "DART", 1480, 940, 80, "amber", "c", smooth(seg(T, 4.0, 4.6)))


# =============================================================================== lines 41-43: the pair: size, orbit
def _pair_view(im, T, c, which):
    cx, cy = 760, 560
    rd = 235
    place_rock(im, cx, cy, rd, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    ang = T * 0.55
    mr = 520
    mx, my = cx + mr * math.cos(ang), cy + mr * 0.62 * math.sin(ang)
    rm = 45
    ring(im, cx, cy, mr, "dim", 2, 0.5, 14) if False else B.ell(im, cx, cy, mr, mr * 0.62, B.mix("dim", 0.5), 2)
    if which == "didymos":
        k = smooth(seg(T, 0.3, 1.1))
        B.line(im, cx - rd, cy + rd + 50, cx + rd * k, cy + rd + 50, "amber", 4)
        B.line(im, cx - rd, cy + rd + 38, cx - rd, cy + rd + 62, "amber", 4)
        B.line(im, cx + rd * k, cy + rd + 38, cx + rd * k, cy + rd + 62, "amber", 4)
        txt(im, "Didymos ~780 m", cx, cy + rd + 115, 52, "amber", "c", k)
        txt(im, "bada pind", cx, cy - rd - 60, 34, "grey", "c", k)
    place_rock(im, mx, my, rm * (1.5 if which == "dimorphos" else 1.0), 5, ang * 2, 1.0, 1.0, (1.0, 0.85))
    if which == "dimorphos":
        k = smooth(seg(T, 0.3, 1.1))
        B.ell(im, mx, my, rm * 1.9, rm * 1.9, B.mix("amber", 0.9 * k), 3)
        txt(im, "Dimorphos ~150-160 m", mx, my - 130, 44, "amber", "c", k)
        txt(im, "chhota chaand", mx, my + 120, 32, "grey", "c", k)
        # relative size: 780 m vs 155 m, side by side bracket
        a = smooth(seg(T, 1.6, 2.4))
        B.rrect(im, 1240, 200, 1840, 520, 24, (10, 10, 18), 0.55 * a)
        place_rock(im, 1400, 360, 110, 2, 0.0, a, 1.0, (1.0, 0.9))
        place_rock(im, 1660, 400, 22, 5, 0.0, a, 1.0, (1.0, 0.85))
        txt(im, "780 m", 1400, 250, 30, "ink", "c", a, panel=False)
        txt(im, "155 m", 1660, 345, 30, "ink", "c", a, panel=False)
        txt(im, "lagbhag 5 guna chhota", 1540, 470, 30, "grey", "c", a, panel=False)


def _orbit_period_view(im, T, c):
    cx, cy = 600, 560
    place_rock(im, cx, cy, 190, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    rr = 430
    B.ell(im, cx, cy, rr, rr * 0.8, B.mix("amber", 0.8), 3)
    ang = 2 * math.pi * (T / 5.8)
    mx, my = cx + rr * math.cos(ang), cy + rr * 0.8 * math.sin(ang)
    place_rock(im, mx, my, 50, 5, ang * 2, 1.0, 1.0, (1.0, 0.82))
    txt(im, "thodi chapti gend jaisa", mx, my - 90, 32, "ink", "c", 0.95)
    txt(im, "ek chakkar", 1450, 220, 40, "ink", "c", smooth(seg(T, 0.5, 1.1)))
    mins = 715 * lin(T / 5.8)
    dial(im, 1450, 560, 190, mins, "amber", smooth(seg(T, 0.5, 1.1)), full=715.0, ticks=True)
    txt(im, "11 h 55 min", 1450, 850, 62, "amber", "c", smooth(seg(T, 0.8, 1.4)))


@scene
def pair_scale(c, **p):
    stars_bg(c)
    base = c.im.copy()
    t42, t43 = K(c, 42, 0.0), K(c, 43, 0.0)
    def v1(v):
        _pair_view(v, c.T, c, "didymos")
        inset(v, c, "footage/draco_didymos_northup.png", 1640, 250, 470, 264, a=smooth(seg(c.T, 1.4, 2.0)), label="asli tasveer: NASA DRACO")
    def v2(v):
        _pair_view(v, c.T - t42 + 0.0, c, "dimorphos")
        inset(v, c, "footage/draco_dimorphos_northup.png", 1640, 780, 470, 264, a=smooth(seg(c.T - t42, 3.4, 4.0)), label="asli tasveer: NASA DRACO")
    view_seq(c, base, [(-1, t42, v1), (t42, t43, v2), (t43, 1e9, lambda v: _orbit_period_view(v, c.T - t43, c))])


# =============================================================================== lines 44-45: a harmless target
@scene
def safe_target(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    ex, ey = 230, 600
    earth(im, ex, ey, 130, T * 0.1)
    px, py = 1550, 380
    place_rock(im, px, py, 60, 2, T * 0.05)
    mr = 110
    ang = T * 0.9
    place_rock(im, px + mr * math.cos(ang), py + mr * 0.7 * math.sin(ang), 14, 5, ang)
    B.ell(im, px, py, mr, mr * 0.7, B.mix("dim", 0.5), 2)
    k = at(c, 44, 0.05, 0, 0.8)
    dotted(im, [(ex + 150, ey - 10), (px - 130, py + 20)], "dim", 3, k * 0.9, 12, 14, prog=seg(T, 0.2, 1.5))
    txt(im, "bahut door", 880, 530, 36, "grey", "c", at(c, 44, 0.1, 0, 0.6))
    # telescope dish on Earth + light pulses toward the pair
    B.line(im, ex + 70, ey - 130, ex + 110, ey - 175, "ink", 4)
    B.ell(im, ex + 112, ey - 178, 28, 12, "ink", 4, -40)
    for i in range(5):
        ph = (T * 0.6 + i * 0.2) % 1.0
        B.circ(im, lerp(px - 130, ex + 150, ph), lerp(py + 20, ey - 10, ph), 5, B.mix("amber", 0.9 * (1 - 0.5 * ph)), -1)
    txt(im, "dharti ki dooribeen se badlav naapa ja sakta tha", 960, 130, 42, "ink", "c", at(c, 44, 0.45, 0, 0.6))
    # lightcurve
    gx0, gy0, gw, gh = 820, 700, 760, 180
    B.rrect(im, gx0 - 20, gy0 - 40, gx0 + gw + 20, gy0 + gh + 40, 18, (10, 10, 18), 0.5 * k)
    pts = []
    for i in range(0, 181):
        x = gx0 + gw * i / 180
        v = 0.5 + 0.35 * math.sin(i / 180 * 6 * 2 * math.pi + T * 0.0) * (1 if i / 180 < seg(T, 0.8, 5.0) else 0)
        pts.append((x, gy0 + gh * (1 - v)))
    visible = [q for q in pts if q[0] <= gx0 + gw * seg(T, 0.8, 5.0)]
    if len(visible) > 2:
        B.polyl(im, visible, B.mix("amber", k), 4)
    txt(im, "roshni ka utaar-chadhaav", gx0 + gw / 2, gy0 + gh + 70, 28, "grey", "c", k, panel=False)
    # line 45: the target stays on its way; test only
    k2 = at(c, 45, 0.0, 0, 0.6)
    if k2 > 0.01:
        txt(im, "dharti se door bhejna nahi: bekhatar nishane par parikshan", 960, 960, 44, "green", "c", k2)
        B.ell(im, px, py, 150, 150, B.mix("green", 0.9 * k2), 3)


# =============================================================================== line 47: ten months, 580 kg
@scene
def journey(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    ex, ey = 260, 700
    earth(im, ex, ey, 110, T * 0.1)
    px, py = 1560, 380
    place_rock(im, px, py, 38, 2, T * 0.05)
    pts = [(ex + 120, ey - 60), (600, 420), (1000, 250), (1400, 330), (px - 30, py)]
    # smooth curve through points
    def curve(k):
        n = len(pts) - 1
        f = k * n
        i = min(int(f), n - 1)
        u = f - i
        a, b = pts[i], pts[i + 1]
        return lerp(a[0], b[0], u), lerp(a[1], b[1], u)
    prog = smooth(seg(T, 0.3, 5.0))
    trail = [curve(prog * j / 40) for j in range(41)]
    dotted(im, trail, "amber", 4, 0.9, 14, 10)
    cxy = curve(prog)
    blit(im, craft_spr(), cxy[0], cxy[1], 0.2, 0.0)
    months = int(10 * prog)
    txt(im, f"mahina {months}", 960, 900, 80, "amber", "c", smooth(seg(T, 0.3, 0.9)))
    for m in range(11):
        B.circ(im, 460 + m * 100, 990, 10, B.mix("amber" if m <= months else "dim", 0.95 if m <= months else 0.5), -1)
    txt(im, "580 kg ka yaan", 960, 130, 54, "ink", "c", at(c, 47, 0.45, 0, 0.5))
    txt(im, "seedha takkar", px, py - 110, 36, "red", "c", at(c, 47, 0.7, 0, 0.5))


# =============================================================================== lines 49-50: the 'ek dhakka' basics
def _ball_view(im, T, c):
    fy = 700
    B.line(im, 80, fy + 150, 1840, fy + 150, B.mix("dim", 0.8), 4)
    ti = 2.6
    rb, ra = 150, 62
    bx0 = 1180
    def bpos(t_):
        return bx0 + (0 if t_ < ti else 85 * (1 - math.exp(-(t_ - ti) * 1.6)))
    def apos(t_):
        if t_ < ti:
            return 90 + (bx0 - rb - ra - 90) * smooth(seg(t_, 0.2, ti)) ** 1.0 + 0
        return bpos(t_) - rb - ra
    bx = bpos(T)
    ax = apos(T)
    # rock ball B
    B.glow(im, bx, fy, rb * 1.8, (200, 180, 120), 0.12)
    B.circ(im, bx, fy, rb, (120, 112, 100), -1)
    B.circ(im, bx, fy, rb, B.mix("teal", 0.9), 5)
    for q in range(5):
        a_ = q * 1.3 + 0.4
        B.circ(im, bx + 0.5 * rb * math.cos(a_), fy + 0.5 * rb * math.sin(a_), 16 - q * 2, (95, 88, 80), -1)
    # craft ball A
    B.circ(im, ax, fy, ra, (40, 150, 235), -1)
    B.circ(im, ax, fy, ra, (90, 205, 250), 4)
    txt(im, "yaan", ax, fy + 5, 30, "white", "c", 1.0, panel=False)
    txt(im, "patthar", bx, fy - rb - 40, 34, "teal", "c", smooth(seg(T, 0.3, 0.9)))
    if T < ti:
        for k in range(8):
            B.line(im, ax - ra - 30 - k * 36, fy - 18 + k * 5, ax - ra - 12, fy - 18 + k * 5, B.mix("white", 0.1 + 0.012 * k), 2)
    else:
        d = T - ti
        flash(im, bx - rb, fy, d / 0.6, 160)
        k = smooth(seg(T, ti + 0.25, ti + 0.9))
        arrow(im, bx - 20, fy - rb - 100, bx + 230, fy - rb - 100, "orange", 11, k, 34, k)
        txt(im, "ek dhakka", bx + 105, fy - rb - 170, 52, "orange", "c", k)
        txt(im, "yaan chipak gaya: bas itna hi dhakka", 960, 940, 40, "ink", "c", smooth(seg(T, ti + 1.0, ti + 1.7)))


def _seven_view(im, T, c):
    cx, cy = 700, 560
    place_rock(im, cx, cy, 170, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    rr = 400
    B.ell(im, cx, cy, rr, rr * 0.85, B.mix("grey", 0.45), 2)
    sh = smooth(seg(T, 1.0, 4.0))
    B.ell(im, cx, cy, rr - 16 * sh, (rr - 16 * sh) * 0.85, B.mix("orange", 0.95), 4)
    ang = T * 0.5
    r_ = rr - 16 * sh
    place_rock(im, cx + r_ * math.cos(ang), cy + r_ * 0.85 * math.sin(ang), 38, 5, ang)
    M = 715 - 7 * sh
    txt(im, "chakkar ka samay", 1500, 300, 42, "ink", "c", 1.0)
    txt(im, hm(M), 1500, 400, 70, "orange", "c", 1.0)
    txt(im, f"{int(round(7 * sh))} min kam", 1500, 520, 56, "orange", "c", smooth(seg(T, 0.8, 1.4)))
    arrow(im, 1500, 600, 1500, 600, "orange", 1, 0)
    txt(im, "yaan ke dhakke se ~7 min", 1500, 640, 38, "ink", "c", smooth(seg(T, 3.0, 3.6)))


@scene
def push_basic(c, **p):
    stars_bg(c)
    base = c.im.copy()
    t50 = K(c, 50, 0.0) - 0.15
    view_seq(c, base, [(-1, t50, lambda v: _ball_view(v, c.T, c)), (t50, 1e9, lambda v: _seven_view(v, c.T - t50, c))])


# =============================================================================== lines 51-52: the 73 s success bar
@scene
def crit73(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    cx, cy = 560, 560
    place_rock(im, cx, cy, 150, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    rr = 340
    B.ell(im, cx, cy, rr, rr * 0.88, B.mix("grey", 0.45), 2)
    sh = smooth(seg(T, 1.5, 4.0))
    B.ell(im, cx, cy, rr - 3 * sh, (rr - 3 * sh) * 0.88, B.mix("amber", 0.95), 4)
    ang = T * 0.55
    place_rock(im, cx + rr * math.cos(ang), cy + rr * 0.88 * math.sin(ang), 32, 5, ang)
    # stopwatch ring 73 s
    a = at(c, 51, 0.45, 0, 0.6)
    sx, sy, sr = 1400, 470, 190
    dial(im, sx, sy, sr, 73.0 * smooth(seg(T, K(c, 51, 0.5), K(c, 51, 0.5) + 2.6)), "amber", a, full=60.0)
    txt(im, "73 s", sx, sy + sr + 90, 84, "amber", "c", a)
    txt(im, "NASA ki kasauti: kam se kam 73 s", 960, 130, 46, "ink", "c", at(c, 51, 0.15, 0, 0.6))
    k = at(c, 52, 0.0, 0, 0.6)
    txt(im, "bas itna: sirf 73 s", 960, 960, 54, "amber", "c", k)
    if k > 0.01:
        ring(im, sx, sy, sr + 26 + 6 * math.sin(T * 6), "amber", 4, 0.8 * k)


# =============================================================================== lines 53-56: the result
def _res_orbit(im, T, c):
    cx, cy = 640, 560
    place_rock(im, cx, cy, 175, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    r0 = 400
    sh = smooth(seg(T, 1.0, 3.6))
    B.ell(im, cx, cy, r0, r0 * 0.85, B.mix("grey", 0.5), 2)
    r1 = r0 - 22 * sh
    B.ell(im, cx, cy, r1, r1 * 0.85, B.mix("red", 0.95), 4)
    ang = T * 0.6
    place_rock(im, cx + r1 * math.cos(ang), cy + r1 * 0.85 * math.sin(ang), 38, 5, ang)
    txt(im, "pehle 11 h 55 min", 1480, 270, 44, "grey", "c", 1.0)
    M = 715 - 32 * sh
    txt(im, hm(M), 1480, 380, 74, "red", "c", 1.0)
    txt(im, f"{int(round(32 * sh))} min chhota", 1480, 500, 54, "red", "c", smooth(seg(T, 0.9, 1.5)))
    bar(im, 1180, 640, 600, 38, 32 * sh / 60.0, "red", 1.0)
    txt(im, "11 Oct: pehla nateeja", 1480, 730, 34, "ink", "c", 0.9)


def _res_bars(im, T, c):
    x0, w = 360, 1200
    txt(im, "kasauti: 73 s", x0, 330, 40, "amber", "l", 1.0)
    bar(im, x0, 370, w, 44, 73.0 / 60.0 / 40.0 * smooth(seg(T, 0.2, 1.0)) * 1.0, "amber", 1.0)
    txt(im, "mila: 32 min", x0, 560, 40, "red", "l", smooth(seg(T, 0.5, 1.0)))
    bar(im, x0, 600, w, 44, 32.0 / 40.0 * smooth(seg(T, 0.8, 2.6)), "red", 1.0)
    k = smooth(seg(T, 2.6, 3.2))
    txt(im, "25 guna se zyada", 1480, 780, 66, "red", "c", k)


def _res_pm(im, T, c):
    k = smooth(seg(T, 0.2, 0.8))
    txt(im, "33 min", 960, 430, 150, "red", "c", k)
    x0, x1 = 760, 1160
    B.line(im, x0, 580, x1, 580, B.mix("red", k), 6)
    B.line(im, x0, 556, x0, 604, B.mix("red", k), 6)
    B.line(im, x1, 556, x1, 604, B.mix("red", k), 6)
    txt(im, "+/- 1 min", 960, 660, 62, "ink", "c", smooth(seg(T, 0.9, 1.5)))
    txt(im, "aage ki jaanch ke baad", 960, 800, 40, "grey", "c", smooth(seg(T, 1.3, 1.9)))


@scene
def result_orbit(c, **p):
    stars_bg(c)
    base = c.im.copy()
    t55, t56 = K(c, 55, 0.0), K(c, 56, 0.0)
    view_seq(c, base, [(-1, t55, lambda v: _res_orbit(v, c.T, c)), (t55, t56, lambda v: _res_bars(v, c.T - t55, c)),
                       (t56, 1e9, lambda v: _res_pm(v, c.T - t56, c))])


# =============================================================================== lines 57-58: two independent measurements
@scene
def two_methods(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    # left: brightness (light curve) panel, right: radar echo
    for x0, ttl in ((120, "roshni ka utaar-chadhaav"), (1000, "radar")):
        B.rrect(im, x0, 250, x0 + 800, 720, 24, (14, 18, 34), 0.75)
        txt(im, ttl, x0 + 400, 215, 40, "ink", "c", at(c, 57, 0.3, 0, 0.5))
    prog = seg(T, 0.6, 6.5)
    # light curve: dips every period, second set (after) shifted earlier
    pts_a, pts_b = [], []
    n = 220
    for i in range(int(n * prog) + 1):
        x = 150 + 740 * i / n
        u = i / n
        va = 0.55 + 0.22 * math.cos(u * 5.0 * 2 * math.pi)
        vb = 0.55 + 0.22 * math.cos((u * 5.0 * 2 * math.pi) * 1.03)
        pts_a.append((x, 470 - 160 * (va - 0.55) * 2.2 - 0))
        pts_b.append((x, 560 - 160 * (vb - 0.55) * 2.2 - 0))
    if len(pts_a) > 2:
        B.polyl(im, pts_a, B.mix("grey", 0.9), 3)
        B.polyl(im, pts_b, B.mix("amber", 1.0), 4)
    txt(im, "pehle", 190, 405, 28, "grey", "l", 0.9, panel=False)
    txt(im, "baad mein: chakkar chhota", 190, 640, 28, "amber", "l", at(c, 57, 0.5, 0, 0.5), panel=False)
    # radar: sweep + echo ring
    rcx, rcy = 1400, 520
    for rr in (60, 120, 180, 240):
        B.circ(im, rcx, rcy, rr, B.mix("dim", 0.5), 1)
    sw = T * 2.6
    for j in range(24):
        a_ = sw - j * 0.05
        B.line(im, rcx, rcy, rcx + 250 * math.cos(a_), rcy + 250 * math.sin(a_), B.mix("green", 0.5 * (1 - j / 24)), 3)
    place_rock(im, rcx, rcy, 20, 2, T)
    for q in range(2):
        ang = T * (0.9 + 0.03 * q) + q * 3.1
        ex, ey = rcx + 170 * math.cos(ang), rcy + 170 * 0.9 * math.sin(ang)
        place_rock(im, ex, ey, 14, 5, ang)
        B.circ(im, ex, ey, 20 + 4 * math.sin(T * 5 + q), B.mix("green", 0.8), 2)
    # both end at -33 min
    k = at(c, 57, 0.8, 0, 0.7)
    txt(im, "-33 min", 520, 800, 80, "amber", "c", k)
    txt(im, "-33 min", 1400, 800, 80, "green", "c", k)
    k2 = at(c, 58, 0.1, 0, 0.7)
    if k2 > 0.01:
        B.line(im, 760, 800, 1160, 800, B.mix("white", k2), 6)
        txt(im, "dono ka jawab ek", 960, 880, 48, "ink", "c", k2)
        txt(im, "kisi ek aujaar ki galti nahi", 960, 960, 42, "green", "c", at(c, 58, 0.45, 0, 0.6))


# =============================================================================== lines 59-60: still there, first time
@scene
def still_orbiting(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    cx, cy = 700, 560
    place_rock(im, cx, cy, 175, 2, T * 0.02, 1.0, 1.0, (1.0, 0.9))
    r1 = 378
    B.ell(im, cx, cy, 400, 340, B.mix("grey", 0.35), 2)
    B.ell(im, cx, cy, r1, r1 * 0.85, B.mix("amber", 0.9), 3)
    ang = T * 0.75
    mx, my = cx + r1 * math.cos(ang), cy + r1 * 0.85 * math.sin(ang)
    place_rock(im, mx, my, 40, 5, ang)
    k = at(c, 59, 0.38, 0, 0.5)
    txt(im, "toota nahi", mx, my - 90, 40, "green", "c", k)
    B.circ(im, mx, my, 60, B.mix("green", 0.9 * k), 3)
    txt(im, "aaj bhi chakkar laga raha hai", 700, 960, 44, "ink", "c", at(c, 59, 0.5, 0, 0.6))
    txt(im, "bas chakkar badla", 1480, 380, 46, "amber", "c", at(c, 59, 0.75, 0, 0.6))
    k2 = at(c, 60, 0.0, 0, 0.6)
    if k2 > 0.01:
        B.rrect(im, 1180, 540, 1800, 760, 28, (10, 10, 18), 0.6 * k2)
        txt(im, "PEHLI BAAR", 1490, 620, 70, "amber", "c", k2, panel=False)
        txt(im, "insaan ne ek prakritik pind ki chaal badli", 1490, 700, 32, "ink", "c", k2, panel=False)


# =============================================================================== lines 61-62: the clue, then 'find it first'
@scene
def clue(c, **p):
    stars_bg(c)
    im, T = c.im, c.T
    place_rock(im, 640, 560, 110, 2, T * 0.04, 1.0, 1.0, (1.0, 0.9))
    # dust tail grows to the right after the clock reaches 2 h
    tl = smooth(seg(T, 2.2, 5.4))
    rng = np.random.default_rng(61)
    for i in range(160):
        u = rng.random() ** 0.8
        xx = 700 + u * 900 * tl
        yy = 560 - u * 150 * tl + rng.normal(0, 8 + 36 * u * tl)
        a = (1 - u) * 0.5 * tl
        B.circ(im, xx, yy, 2 + 3 * (1 - u), B.mix((200, 210, 225), a), -1)
    # clock: 2 hours
    dial(im, 1550, 270, 130, 120.0 * smooth(seg(T, 0.4, 2.4)), "amber", at(c, 61, 0.0, 0.2, 0.5), full=120.0, ticks=True)
    txt(im, "2 ghante", 1550, 450, 48, "amber", "c", at(c, 61, 0.0, 0.2, 0.5))
    txt(im, "takkar ke 2 ghante baad aasmaan mein suraag", 960, 940, 44, "ink", "c", at(c, 61, 0.3, 0, 0.6))
    txt(im, "?", 1020, 480, 130, "red", "c", at(c, 61, 0.7, 0, 0.5) * (0.6 + 0.4 * math.sin(T * 5)), panel=False)
    # line 62: telescope sweep -> 'pehle dhundhna'
    k = at(c, 62, 0.0, 0, 0.5)
    if k > 0.01:
        ov = im.copy()
        cv2.rectangle(ov, (0, 0), (W, H), (8, 10, 22), -1)
        cv2.addWeighted(ov, 0.88 * k, im, 1 - 0.88 * k, 0, dst=im)
        sx = lerp(300, 1620, (T * 0.28) % 1.0)
        B.line(im, sx, 200, sx, 880, B.mix("green", 0.7 * k), 3)
        rng2 = np.random.default_rng(62)
        for i in range(40):
            x, y = rng2.uniform(200, 1720), rng2.uniform(220, 860)
            lit = 1.0 if x < sx else 0.25
            B.circ(im, x, y, 4, B.mix("ink", 0.7 * lit * k), -1)
        txt(im, "pehle: patthar ko dhundhna", 960, 110, 60, "amber", "c", k)
