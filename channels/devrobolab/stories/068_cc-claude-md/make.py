"""068 LONG (16:9): Claude Code CLAUDE.md kaise likhein. Light InsiderForce-style (brand/INSIDERFORCE_STYLE.md, RUN_COMMON 14-18):
flat light bg, word-by-word mixed-weight Roman text, soft-shadow cards with animated UI mock-ups, icon on a string, hub diagram,
big-numeral chapter openers, chooser row, sparkle bullets, corner ray bursts. Every visual is anchored to the spoken word (wt.json).
Run: python make.py frames t1 t2 ...  |  python make.py chunk i N  |  python make.py mux N  |  python make.py info"""
import json, math, sys, wave, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import photo_video as pv
from photo_video import ease_out, ease_back, ease_io, wav_dur
W, H, FPS = 1920, 1080, 30
pv.W, pv.H = W, H

LEAD, AFTER = 0.10, 0.30
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]; CH = {s["id"]: s.get("chapter", "") for s in deck["scenes"]}
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START)); SE = {k: SC[k] + D[i] for i, k in enumerate(IDS)}
BG = (244, 244, 246); INK = (22, 22, 28); GREY = (120, 120, 130); LGREY = (214, 215, 222); ACC = (8, 145, 178); ACC2 = (207, 250, 254)
GREEN = (22, 163, 74); RED = (220, 38, 38); TERM = (22, 24, 30); TGREEN = (74, 222, 128); TGREY = (150, 156, 170); WHITE = (255, 255, 255); AMBER = (217, 119, 6)
CX = W // 2; TEXT_Y = 905


# ---------------- word timing ----------------
def toks(s): return WT[s]["tokens"]
def ix(s, sub, n=1):
    c = 0
    for i, (tk, _) in enumerate(toks(s)):
        if sub in tk:
            c += 1
            if c == n: return i
    raise KeyError(f"{s}: '{sub}' #{n} not found")
def T(s, k): tk = toks(s); return SC[s] + LEAD + tk[min(k, len(tk) - 1)][1]
def at(s, sub, n=1): return T(s, ix(s, sub, n))


_fc = {}
def font(sz, kind="bold"):
    key = (sz, kind)
    if key not in _fc:
        f = {"bold": "Poppins-Bold.ttf", "xb": "Poppins-ExtraBold.ttf", "med": "Poppins-Medium.ttf", "mono": "IBMPlexMono-Bold.ttf"}[kind]
        _fc[key] = ImageFont.truetype(str(ROOT / "shared/fonts" / f), sz)
    return _fc[key]


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BILINEAR)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


_sh = {}
def shadow(w, h, r=24):
    k = (w, h, r)
    if k not in _sh:
        sh = Image.new("RGBA", (w + 200, h + 200), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([100 + 18, 100 + 34, 100 + 18 + w, 100 + 34 + h], r, fill=(0, 0, 0, 58))
        _sh[k] = sh.filter(ImageFilter.GaussianBlur(28))
    return _sh[k]


def enter(base, spr, cx, cy, t, t0, side=0, dur=0.42, float_amp=5, rot=0.0, shad=True, t_out=None, sway=0.8, out_side=None):
    lt = t - t0
    if lt < 0: return
    fade = 1.0; xo = 0
    if t_out is not None and t > t_out:
        q = ease_io((t - t_out) / 0.35)
        if q >= 1: return
        fade = 1 - q; os_ = out_side if out_side is not None else (-1 if side <= 0 else 1); xo = os_ * q * 520
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur))
    dx = side * (1 - q) * 900 + xo; dy = (1 - q) * (150 if side == 0 else 0); sc = (0.84 + 0.16 * e) * (1 - 0.1 * (1 - fade))
    fl = float_amp * math.sin(lt * 2.0 + cx * 0.01) if lt > dur else 0
    rr = rot + (sway * math.sin(lt * 1.3 + cy * 0.01) if lt > dur else 0)
    w, h = spr.size
    if shad: place(base, shadow(w, h), cx + dx, cy + dy + fl, sc, min(1, q * 1.4) * fade, rr)
    place(base, spr, cx + dx, cy + dy + fl, sc, min(1, q * 1.4) * fade, rr)


def rays(base, cx, cy, t, t0, ang0=-100, n=7, col=ACC, big=1.0):
    lt = t - t0
    if lt < 0 or lt > 0.9: return
    q = ease_out(lt / 0.5); a = 1 - ease_io(lt / 0.9); d = ImageDraw.Draw(base)
    for i in range(n):
        ang = math.radians(ang0 + i * 26); r0 = (16 + 46 * q) * big; r1 = r0 + 34 * big * (1 - lt / 0.9)
        d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))], fill=col + (int(255 * a),), width=int(8 * big))


def corner_bursts(base, t, t0):
    """Big soft accent ray bursts half outside two opposite corners (hook / giant-number beats)."""
    lt = t - t0
    if lt < 0 or lt > 1.6: return
    a = min(1, lt / 0.2) * (1 - max(0, (lt - 1.1) / 0.5)); sc = ease_back(min(1, lt / 0.45))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (cx, cy, a0) in ((40, 30, 10), (W - 40, H - 30, 190)):
        for i in range(6):
            ang = math.radians(a0 + i * 14); r0, r1 = 40 * sc, 210 * sc
            d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))], fill=ACC + (int(200 * a),), width=30)
    base.alpha_composite(lay)


# ---------------- icons ----------------
_ic = {}
def file_icon(label="CLAUDE.md", col=ACC):
    k = ("file", label)
    if k not in _ic:
        ic = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(ic); d.ellipse([8, 8, 192, 192], fill=WHITE + (255,))
        d.rounded_rectangle([62, 40, 138, 140], 10, fill=col + (255,)); d.polygon([(112, 40), (138, 66), (112, 66)], fill=(255, 255, 255, 150))
        for i in range(3): d.rounded_rectangle([74, 80 + 16 * i, 126 - 14 * (i == 2), 88 + 16 * i], 3, fill=(255, 255, 255, 220))
        f = font(22, "bold"); d.text((100 - f.getlength(label) / 2, 148), label, font=f, fill=INK + (255,)); _ic[k] = ic
    return _ic[k]


def circle_icon(label, col, size=44):
    k = ("c", label, col)
    if k not in _ic:
        ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(ic); d.ellipse([10, 10, 170, 170], fill=WHITE + (255,)); d.ellipse([34, 34, 146, 146], fill=col + (255,))
        d.ellipse([46, 40, 96, 76], fill=(255, 255, 255, 70)); f = font(size, "bold"); w = f.getlength(label); d.text((90 - w / 2, 90 - size * 0.72), label, font=f, fill=WHITE + (255,)); _ic[k] = ic
    return _ic[k]


def gear_icon(angle, col=INK):
    ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(ic); d.ellipse([10, 10, 170, 170], fill=WHITE + (255,))
    g = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); dg = ImageDraw.Draw(g); dg.ellipse([50, 50, 130, 130], fill=col + (255,))
    for i in range(8):
        a = math.radians(i * 45); x, y = 90 + 52 * math.cos(a), 90 + 52 * math.sin(a); dg.ellipse([x - 14, y - 14, x + 14, y + 14], fill=col + (255,))
    dg.ellipse([72, 72, 108, 108], fill=WHITE + (255,)); ic.alpha_composite(g.rotate(angle, resample=Image.BICUBIC)); return ic


def lock_icon(open_=False):
    k = ("lock", open_)
    if k not in _ic:
        ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(ic); d.ellipse([10, 10, 170, 170], fill=WHITE + (255,))
        d.rounded_rectangle([52, 84, 128, 140], 12, fill=AMBER + (255,))
        if open_: d.arc([62, 38, 118, 100], 180, 330, fill=AMBER + (255,), width=12)
        else: d.arc([62, 44, 118, 104], 180, 360, fill=AMBER + (255,), width=12)
        d.ellipse([82, 102, 98, 118], fill=WHITE + (255,)); _ic[k] = ic
    return _ic[k]


def hang(base, t, t0, cx, y, spr, t_out=None):
    lt = t - t0
    if lt < 0: return
    al = 1.0
    if t_out is not None and t > t_out:
        al = 1 - min(1, (t - t_out) / 0.3)
        if al <= 0: return
    q = ease_out(min(1, lt / 0.45)); yy = -120 + (y + 120) * q + (14 * math.sin(lt * 9) * math.exp(-lt * 4) if lt > 0.4 else 0)
    xx = cx + (7 * math.sin(lt * 1.6) if lt > 0.5 else 0)
    ImageDraw.Draw(base).line([(xx, 0), (xx, yy - spr.height * 0.4)], fill=(170, 170, 176, int(255 * al)), width=3)
    place(base, shadow(spr.width, spr.height, spr.width // 2), xx, yy, 0.62, al); place(base, spr, xx, yy, 1.0, al)


def tick(d, x, y, s=1.0, col=GREEN):
    d.ellipse([x, y, x + 56 * s, y + 56 * s], fill=col + (255,)); d.line([(x + 15 * s, y + 29 * s), (x + 25 * s, y + 39 * s), (x + 42 * s, y + 18 * s)], fill=WHITE + (255,), width=int(7 * s))
def cross(d, x, y, s=1.0, col=RED):
    d.ellipse([x, y, x + 56 * s, y + 56 * s], fill=col + (255,)); d.line([(x + 18 * s, y + 18 * s), (x + 38 * s, y + 38 * s)], fill=WHITE + (255,), width=int(7 * s)); d.line([(x + 38 * s, y + 18 * s), (x + 18 * s, y + 38 * s)], fill=WHITE + (255,), width=int(7 * s))


def pill(text, size, fill, color=WHITE, pad=(30, 12), r=28, kind="bold", icon=None):
    f = font(size, kind); tw = int(f.getlength(text)); asc, desc = f.getmetrics(); ih = asc + desc + 2 * pad[1]; iw = (ih - 10) if icon else 0
    im = Image.new("RGBA", (tw + 2 * pad[0] + iw, ih), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=fill + (255,))
    if icon == "tick": tick(d, pad[0] - 8, (ih - 56 * (ih - 20) / 56) / 2, (ih - 20) / 56)
    if icon == "cross": cross(d, pad[0] - 8, (ih - 56 * (ih - 20) / 56) / 2, (ih - 20) / 56)
    d.text((pad[0] + iw, pad[1]), text, font=f, fill=color + (255,)); return im


def cursor(base, x, y, click_t=None, t=0):
    d = ImageDraw.Draw(base)
    if click_t is not None and 0 <= t - click_t < 0.5:
        r = int(14 + 60 * (t - click_t) / 0.5); d.ellipse([x - r, y - r, x + r, y + r], outline=ACC + (int(255 * (1 - (t - click_t) / 0.5)),), width=5)
    d.polygon([(x, y), (x, y + 50), (x + 14, y + 38), (x + 27, y + 63), (x + 38, y + 57), (x + 25, y + 34), (x + 43, y + 32)], fill=WHITE + (255,), outline=INK + (255,))


def arrow(base, x0, y0, x1, y1, t, t0, col=ACC, w=6, dur=0.45):
    if t < t0: return
    q = ease_out(min(1, (t - t0) / dur)); xe, ye = x0 + (x1 - x0) * q, y0 + (y1 - y0) * q; d = ImageDraw.Draw(base)
    d.line([(x0, y0), (xe, ye)], fill=col + (255,), width=w)
    if q > 0.6:
        a = math.atan2(y1 - y0, x1 - x0); L = 22
        d.polygon([(xe, ye), (xe - L * math.cos(a - 0.45), ye - L * math.sin(a - 0.45)), (xe - L * math.cos(a + 0.45), ye - L * math.sin(a + 0.45))], fill=col + (255,))


def dotted(base, x0, y0, x1, y1, t, t0, col=ACC):
    if t < t0: return
    d = ImageDraw.Draw(base); L = math.hypot(x1 - x0, y1 - y0); q = ease_out(min(1, (t - t0) / 0.5)); n = max(2, int(L / 26))
    for i in range(n):
        f = i / n
        if f > q: break
        ph = (f * 8 - t * 3) % 1; r = 5 + 3 * max(0, 1 - ph * 2)
        d.ellipse([x0 + (x1 - x0) * f - r, y0 + (y1 - y0) * f - r, x0 + (x1 - x0) * f + r, y0 + (y1 - y0) * f + r], fill=col + (255,))


# ---------------- word-by-word text ----------------
_wc = {}
_TXT = [None]
TS = 56
def wsprite(word, bold, mono=False):
    k = (word, bold, mono)
    if k not in _wc:
        f = font(TS - 4 if mono else TS, "mono" if mono else ("bold" if bold else "med")); col = (ACC if mono else INK) if bold else GREY
        w = int(f.getlength(word)) + 6; im = Image.new("RGBA", (w, 92), (0, 0, 0, 0)); ImageDraw.Draw(im).text((3, 6), word, font=f, fill=col + (255,)); _wc[k] = im
    return _wc[k]


def run_text(base, t, s, phrases, y=TEXT_Y, maxw=1560, t_from=None):
    """phrases = [(anchor_substring_or_None, 'text with *bold* `mono` words'), ...] resolved in spoken order."""
    if t_from is not None and t < t_from: return
    seq = []; k0 = 0
    for j, (sub, txt) in enumerate(phrases):
        if j == 0 and sub is None: a = SC[s]
        else:
            k = next((i for i in range(k0, len(toks(s))) if sub in toks(s)[i][0]), None)
            if k is None: raise KeyError(f"{s}: text anchor '{sub}'")
            k0 = k; a = T(s, k) - 0.08
        seq.append((max(a, t_from or 0), txt))
    cur = None
    for j, (a, txt) in enumerate(seq):
        b = seq[j + 1][0] if j + 1 < len(seq) else SE[s]
        if a <= t < b: cur = (a, b, txt)
    if not cur: return
    a, b, txt = cur; items = []
    for w in txt.split(" "):
        mono = "`" in w; w2 = w.replace("`", ""); bold = "*" in w2; items.append((w2.replace("*", ""), bold or mono, mono))
    span = min(1.3, max(0.45, (b - a) * 0.6)); n = len(items)
    lines = [[]]; cw = 0; sp = font(TS, "med").getlength(" ")
    for it in items:
        wl = wsprite(*it).width
        if cw + wl > maxw and lines[-1]: lines.append([]); cw = 0
        lines[-1].append(it); cw += wl + sp
    idx = 0; y0 = y - 38 * (len(lines) - 1); base = _TXT[0] if _TXT[0] is not None else base
    for li, ln in enumerate(lines):
        tw = sum(wsprite(*it).width for it in ln) + sp * (len(ln) - 1); x = CX - tw / 2
        for it in ln:
            ts = a + span * idx / max(1, n); idx += 1; spr = wsprite(*it)
            q = ease_out(min(1, (t - ts) / 0.2)) if t >= ts else 0; sp2 = ease_back(min(1, (t - ts) / 0.32)) if t >= ts else 0
            xa = 1.0 if (b - t) > 0.1 else max(0, (b - t) / 0.1)
            if q > 0: place(base, spr, x + spr.width / 2, y0 + 76 * li + 26 * (1 - sp2) + spr.height / 2 - 46, (0.72 + 0.28 * sp2) if it[1] else 1.0, q * xa)
            x += spr.width + sp


def watermark(base):
    f = font(26, "med"); ImageDraw.Draw(base).text((CX - f.getlength("DevRoboLab") / 2, 1032), "DevRoboLab", font=f, fill=(196, 196, 204, 255))


def chapter_badge(base, s, t):
    if s == "hook": return
    n = IDS.index(s); lab = f"{n}/{len(IDS) - 1}  {CH[s]}"; f = font(26, "bold"); w = int(f.getlength(lab)) + 64
    lt = t - SC[s] - 1.2
    if lt < 0: return
    a = min(1, lt / 0.3); d = ImageDraw.Draw(base); x = 40 - (1 - ease_out(min(1, lt / 0.3))) * 60
    d.rounded_rectangle([x, 34, x + w, 84], 25, fill=WHITE + (int(255 * a),)); d.ellipse([x + 20, 51, x + 36, 67], fill=ACC + (int(255 * a),))
    d.text((x + 46, 41), lab, font=f, fill=INK + (int(255 * a),))


_num = {}
def numeral(base, t, t0, num, label, dur=1.25):
    """Chapter opener: giant numeral fading out at its bottom + bold name (InsiderForce item opener)."""
    lt = t - t0
    if lt < 0 or lt > dur + 0.3: return
    if num not in _num:
        f = font(330, "xb"); w = int(f.getlength(num)) + 40; im = Image.new("RGBA", (w, 400), (0, 0, 0, 0)); ImageDraw.Draw(im).text((20, -40), num, font=f, fill=INK + (255,))
        g = np.ones((400, w), dtype=np.float32); g[220:, :] = np.linspace(1, 0, 180)[:, None]
        im.putalpha(Image.fromarray((np.asarray(im.getchannel("A")) * g).astype(np.uint8))); _num[num] = im
    sc = 0.82 + 0.18 * ease_back(min(1, lt / 0.35)); out = max(0, (lt - dur) / 0.3); a = min(1, lt / 0.12) * (1 - out)
    place(base, _num[num], CX, 380 - 120 * ease_io(out), sc, a)
    lab = wsprite(label, True); place(base, lab, CX, 640 - 120 * ease_io(out), 1.15 * sc, a)


def opener_on(s, t): return t < SC[s] + 1.25 + 0.3


# ---------------- card builders ----------------
def white_card(w, h, r=24):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=WHITE + (255,)); return im


def term_card(w, h, t, lines, title="Terminal", cps=22, fs=34):
    """lines: (text, t_show, kind) kind: 'cmd' typed with prompt, 'out' grey, 'ok' green, 'acc' accent, 'warn' amber, 'red'."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=TERM + (255,)); d.rounded_rectangle([0, 0, w - 1, 52], 22, fill=(44, 47, 58, 255)); d.rectangle([0, 30, w - 1, 52], fill=(44, 47, 58, 255))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))): d.ellipse([20 + 32 * i, 17, 38 + 32 * i, 35], fill=c + (255,))
    d.text((130, 10), title, font=font(24, "med"), fill=TGREY + (255,))
    vis = [ln for ln in lines if t >= ln[1]]; lh = int(fs * 1.55); maxl = (h - 80) // lh; vis = vis[-maxl:]; y = 74
    cols = {"out": TGREY, "ok": TGREEN, "acc": (103, 232, 249), "warn": (251, 191, 36), "red": (248, 113, 113)}
    for txt, tt, kind in vis:
        if kind == "cmd":
            d.text((26, y), "$", font=font(fs, "mono"), fill=TGREEN + (255,)); s = txt[:int((t - tt) * cps) + 1]
            d.text((26 + fs * 0.9, y), s, font=font(fs, "mono"), fill=WHITE + (255,))
            if len(s) < len(txt) or (t * 2) % 1 < 0.5: d.rectangle([26 + fs * 0.9 + font(fs, "mono").getlength(s) + 4, y + 4, 26 + fs * 0.9 + font(fs, "mono").getlength(s) + 4 + fs * 0.5, y + fs + 4], fill=(200, 200, 210, 255))
        else: d.text((26, y), txt, font=font(fs - 4, "mono"), fill=cols.get(kind, TGREY) + (255,))
        y += lh
    return im


def editor(w, h, t, lines, title="CLAUDE.md", cps=40, fs=30, tag=None):
    """Light editor card. lines: (text, t_show, kind) kind 'h' heading, 'l' text, 'c' comment, 'hl' highlighted, 'x' struck."""
    im = white_card(w, h, 22); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 58], 22, fill=(236, 237, 242, 255)); d.rectangle([0, 34, w - 1, 58], fill=(236, 237, 242, 255))
    d.rounded_rectangle([20, 12, 20 + font(24, "bold").getlength(title) + 60, 50], 12, fill=WHITE + (255,)); d.rounded_rectangle([32, 22, 48, 40], 3, fill=ACC + (255,))
    d.text((58, 14), title, font=font(24, "bold"), fill=INK + (255,))
    if tag: f = font(20, "bold"); tw = f.getlength(tag); d.rounded_rectangle([w - tw - 50, 14, w - 20, 46], 14, fill=ACC2 + (255,)); d.text((w - tw - 35, 16), tag, font=f, fill=ACC + (255,))
    y = 80; lh = int(fs * 1.5); n = 0
    for txt, tt, kind in lines:
        if t < tt: continue
        n += 1; s = txt[:int((t - tt) * cps) + 1]; col = {"h": ACC, "c": GREY, "x": GREY}.get(kind, INK)
        if kind == "hl":
            q = ease_out(min(1, (t - tt) / 0.4)); d.rounded_rectangle([18, y - 4, 18 + (font(fs, "mono").getlength(txt) + 24) * q, y + fs + 10], 8, fill=(254, 240, 138, 255))
        d.text((30, y), s, font=font(fs, "mono"), fill=col + (255,))
        if kind == "x": d.line([(26, y + fs * 0.62), (34 + font(fs, "mono").getlength(s), y + fs * 0.62)], fill=RED + (255,), width=4)
        y += lh
    return im


def session_card(t, t_fill=None, label="Naya session", fill_txt="CLAUDE.md"):
    im = white_card(560, 300); d = ImageDraw.Draw(im)
    d.text((34, 26), label, font=font(36, "bold"), fill=INK + (255,)); d.text((34, 84), "context window", font=font(24, "med"), fill=GREY + (255,))
    d.rounded_rectangle([34, 130, 526, 180], 14, fill=(236, 237, 242, 255))
    if t_fill is not None and t >= t_fill:
        q = ease_out(min(1, (t - t_fill) / 0.6)); d.rounded_rectangle([34, 130, 34 + 150 * q, 180], 14, fill=ACC + (255,))
        if q > 0.7: d.text((48, 138), fill_txt, font=font(20, "bold"), fill=WHITE + (255,))
    else: d.text((200, 136), "khaali", font=font(26, "med"), fill=GREY + (255,))
    d.rounded_rectangle([34, 210, 360, 254], 16, fill=(245, 245, 248, 255)); d.text((52, 214), "Claude: kya karna hai?", font=font(22, "med"), fill=GREY + (255,))
    return im


def bubble(text, col=WHITE, tcol=INK, fs=30):
    f = font(fs, "bold"); w = int(f.getlength(text)) + 56; im = Image.new("RGBA", (w, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 72], 26, fill=col + (255,)); d.polygon([(34, 70), (60, 70), (36, 94)], fill=col + (255,)); d.text((28, 12), text, font=f, fill=tcol + (255,)); return im


def node_card(title, sub, mono=True, w=440, col=ACC):
    im = white_card(w, 150, 22); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, 12, 149], 6, fill=col + (255,))
    f = font(30 if mono else 34, "mono" if mono else "bold"); d.text((34, 26), title, font=f, fill=INK + (255,)); d.text((34, 86), sub, font=font(28, "med"), fill=GREY + (255,)); return im


def big_num(text, sub, col=INK):
    f = font(210, "xb"); w = int(max(f.getlength(text), font(44, "bold").getlength(sub))) + 40; im = Image.new("RGBA", (w, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text(((w - f.getlength(text)) / 2, -30), text, font=f, fill=col + (255,)); fs = font(44, "bold"); d.text(((w - fs.getlength(sub)) / 2, 250), sub, font=fs, fill=GREY + (255,)); return im


def sparkle_list(base, t, items, x, y, gap=78, fs=44):
    """items: (text, t_show, done) - 4-point star bullets (or ticks) appearing one per spoken word."""
    d = ImageDraw.Draw(base)
    for i, (txt, ts, done) in enumerate(items):
        if t < ts: continue
        q = ease_out(min(1, (t - ts) / 0.3)); yy = y + gap * i; xo = (1 - q) * 40; a = int(255 * q)
        if done: tick(d, x + xo - 6, yy - 2, 0.85)
        else:
            cx, cy, r = x + xo + 20, yy + 26, 20
            d.polygon([(cx, cy - r), (cx + 5, cy - 5), (cx + r, cy), (cx + 5, cy + 5), (cx, cy + r), (cx - 5, cy + 5), (cx - r, cy), (cx - 5, cy - 5)], fill=INK + (a,))
        d.text((x + xo + 66, yy), txt, font=font(fs, "bold"), fill=INK + (a,))


def chooser(base, t, labels, sel_times, cx, cy, t0, gap=300):
    """Row of small cards; selected one scales 1.25x with stronger shadow (InsiderForce chooser row)."""
    if t < t0: return
    sel = -1
    for i, ts in enumerate(sel_times):
        if t >= ts: sel = i
    for i, lab in enumerate(labels):
        c = white_card(250, 120, 20); d = ImageDraw.Draw(c); f = font(30, "bold"); col = ACC if i == sel else GREY
        d.text((125 - f.getlength(lab) / 2, 40), lab, font=f, fill=col + (255,))
        if i == sel: d.rounded_rectangle([0, 0, 249, 119], 20, outline=ACC + (255,), width=4)
        ts = sel_times[i] if i == sel else 0; k = ease_back(min(1, (t - ts) / 0.3)) if i == sel else 0
        sc = 1.0 + 0.25 * k; x = cx + (i - (len(labels) - 1) / 2) * gap
        enter(base, c, x, cy, t, t0 + 0.12 * i, side=0, dur=0.35, float_amp=0 if i == sel else 3)
        if i == sel: place(base, shadow(250, 120), x, cy, sc); place(base, c, x, cy, sc)


# ---------------- beats ----------------
def b_hook(base, t, s):
    t0 = SC[s]; corner_bursts(base, t, t0 + 0.05)
    tc = at(s, "CLAUDE", 1)
    ta = at(s, "आज")
    lines = [("claude", t0 + 0.1, "cmd"), ("Naya session shuru...", t0 + 0.6, "out"), ("Test command kya hai?", at(s, "भूल") - 0.2, "warn"), ("Kaunsa folder safe hai?", at(s, "folder") - 0.1, "warn")]
    enter(base, term_card(820, 380, t, lines, title="my-app"), 700, 390, t, t0 + 0.05, side=0, rot=-1.5, t_out=tc - 0.2)
    enter(base, bubble("Phir se samjhao?", INK, WHITE), 1330, 260, t, at(s, "दोबारा") - 0.2, side=1, t_out=tc - 0.2)
    if t >= at(s, "भूल"):
        lt = t - at(s, "भूल"); d = ImageDraw.Draw(base)
        for i in range(3):
            q = ease_back(min(1, (lt - 0.12 * i) / 0.3)) if lt > 0.12 * i else 0
            if q > 0 and t < tc - 0.2: d.text((1180 + 70 * i, 470 - 40 * i - 20 * q), "?", font=font(int(80 * q) + 1, "xb"), fill=AMBER + (255,))
    hang(base, t, tc - 0.15, 560 if t >= ta else CX, 330, file_icon(), t_out=None)
    rays(base, CX if t < ta else 560, 330, t, tc)
    items = [("Kya hai", at(s, "क्या", 1)), ("Kahan rakhein", at(s, "कहाँ")), ("/init se banana", at(s, "init")), ("Kya likhein", at(s, "लिखें")), ("3 galtiyan", at(s, "तीन"))]
    sparkle_list(base, t, [(a, b, False) for a, b in items], 860, 120, gap=92, fs=50)
    run_text(base, t, s, [(None, "Har *naya session*: project *bhool* jata hai"), ("दोबारा", "Wahi baatein *dobara* samjhao"), ("इसका", "Hal: ek chhoti file *CLAUDE.md*"), ("आज", "Aaj *step by step*"), ("तीन", "Aur *3 galtiyan* jo isse bekaar karti hain")])


def b_what(base, t, s):
    t0 = SC[s]; numeral(base, t, t0, "1", "CLAUDE.md kya hai")
    if opener_on(s, t) and t < t0 + 1.25: return
    tf = at(s, "शुरुआत"); tn = at(s, "नियम"); tl = at(s, "बस")
    enter(base, session_card(t, tf), 520, 400, t, max(t0 + 1.3, at(s, "Claude", 1) - 0.1), side=-1, t_out=tn - 0.25)
    if t >= at(s, "पिछली") and t < tf:
        q = min(1, (t - at(s, "पिछली")) / 1.2); g = bubble("Kal: npm test chalana", (230, 231, 236), GREY, 26); place(base, g, 560, 160 - 30 * q, 1.0, 1 - 0.75 * q)
        if q > 0.4: cross(ImageDraw.Draw(base), 820, 120 - 30 * q, 0.8)
    ed = [("# Project rules", at(s, "markdown") + 0.1, "h"), ("- Test: npm test", at(s, "instructions") - 0.1, "l"), ("- src/legacy mat chhedo", at(s, "instructions") + 0.3, "l")]
    enter(base, editor(560, 300, t, ed, tag="example"), 1360, 400, t, at(s, "markdown") - 0.15, side=1, t_out=tn - 0.25)
    if tf - 0.1 <= t < tn - 0.25:
        arrow(base, 1075, 400, 815, 400, t, tf - 0.1); place(base, pill("har session ki shuruaat me", 26, ACC, WHITE), 945, 330, 1, min(1, (t - tf) * 4))
    if tn - 0.1 <= t < tl - 0.2:
        enter(base, bubble("Har baar samjhana...", (230, 231, 236), GREY, 36), 560, 380, t, tn - 0.1, side=-1, shad=False)
        arrow(base, 860, 400, 1080, 400, t, at(s, "लिख", 1) - 0.4)
        enter(base, pill("CLAUDE.md me likh do", 40, WHITE, INK, icon="tick", pad=(40, 16)), 1370, 400, t, at(s, "लिख", 1) - 0.15, side=1)
    if t >= tl - 0.2:
        hang(base, t, tl - 0.2, 760, 330, lock_icon(open_=t >= at(s, "lock") - 0.1))
        enter(base, pill("Context hai", 44, ACC, WHITE, pad=(36, 16)), 1150, 290, t, at(s, "context", 1) - 0.1, side=1)
        enter(base, pill("pakka lock nahi", 44, WHITE, INK, icon="cross", pad=(36, 16)), 1150, 420, t, at(s, "lock") - 0.1, side=1)
    run_text(base, t, s, [(None, ""), ("Claude", "Har session: *khaali* context window"), ("पिछली", "Pichhli baat *yaad nahi*"), ("CLAUDE", "*CLAUDE.md* = markdown file, *aapke instructions*"),
                          ("शुरुआत", "Har session ki *shuruaat* me padhta hai"), ("नियम", "Jo *baar baar* samjhate ho, *likh do*"), ("बस", "Ye *context* hai, *pakka lock* nahi")], t_from=t0 + 1.3)


HUB = [(-560, -150), (560, -150), (-560, 170), (560, 170)]
def b_where(base, t, s):
    t0 = SC[s]; numeral(base, t, t0, "2", "Kahan rakhein")
    if opener_on(s, t) and t < t0 + 1.25: return
    tc = at(s, "current"); hx, hy = CX, 400
    if t < tc - 0.2:
        nodes = [("./CLAUDE.md", "Project folder · team + git", "पहली"), ("~/.claude/CLAUDE.md", "Home · sab projects", "दूसरी"), ("CLAUDE.local.md", "Sirf aap · isi project me", "तीसरी"), ("Company file", "Managed · IT team", "चौथी")]
        for (dx, dy), (ti, sub, w) in zip(HUB, nodes):
            ts = at(s, w); dotted(base, hx, hy, hx + dx * 0.62, hy + dy * 0.72, t, ts - 0.2)
        hang(base, t, t0 + 1.3, hx, hy, file_icon())
        for (dx, dy), (ti, sub, w) in zip(HUB, nodes):
            ts = at(s, w); enter(base, node_card(ti, sub, mono=ti != "Company file"), hx + dx, hy + dy, t, ts + 0.1, side=0, dur=0.35)
            rays(base, hx + dx + 200, hy + dy - 60, t, ts + 0.15, n=5)
        if t >= at(s, "gitignore") - 0.1: enter(base, pill(".gitignore", 30, INK, WHITE), hx - 560 + 130, hy + 170 + 105, t, at(s, "gitignore") - 0.1, side=0, dur=0.3)
    else:
        # folder tree: loads current folder + every folder above; sub-folder on demand
        tw = at(s, "जोड़"); tsub = at(s, "Sub"); tk = at(s, "काम")
        tree = white_card(860, 520, 24); d = ImageDraw.Draw(tree)
        rows = [("projects/", 0, "CLAUDE.md", "up"), ("my-app/", 1, "CLAUDE.md", "here"), ("api/", 2, "CLAUDE.md", "sub")]
        for i, (fold, lvl, f, kind) in enumerate(rows):
            y = 60 + 150 * i; x = 50 + 90 * lvl
            d.rounded_rectangle([x, y, x + 54, y + 40], 8, fill=(251, 146, 60, 255)); d.text((x + 70, y - 4), fold, font=font(36, "bold"), fill=INK + (255,))
            on = (kind in ("up", "here") and t >= at(s, "पढ़ता") - 0.1) or (kind == "sub" and t >= tk + 0.2)
            fc = ACC if on else LGREY; d.rounded_rectangle([x + 70, y + 54, x + 330, y + 100], 12, fill=fc + (255,)); d.text((x + 88, y + 58), f, font=font(28, "mono"), fill=WHITE + (255,))
            if kind == "here": d.text((x + 350, y + 56), "<- yahan claude chala", font=font(26, "med"), fill=GREY + (255,))
            if kind == "sub" and t >= tsub - 0.1 and not on: d.text((x + 350, y + 56), "jab zaroorat ho", font=font(26, "med"), fill=AMBER + (255,))
            if kind == "sub" and on: d.text((x + 350, y + 56), "ab load", font=font(26, "bold"), fill=GREEN + (255,))
        enter(base, tree, 660, 400, t, tc - 0.15, side=-1, float_amp=2)
        if t >= tw - 0.1:
            blk = white_card(520, 300, 22); db = ImageDraw.Draw(blk); db.text((30, 24), "Claude ka context", font=font(30, "bold"), fill=INK + (255,))
            q = ease_out(min(1, (t - tw) / 0.6))
            for i, lab in enumerate(("projects/CLAUDE.md", "my-app/CLAUDE.md")):
                db.rounded_rectangle([30, 90 + 70 * i, 30 + 460 * q, 140 + 70 * i], 12, fill=ACC + (255,)); db.text((46, 98 + 70 * i), lab, font=font(24, "mono"), fill=WHITE + (255,))
            if t >= tk + 0.3: qq = ease_out(min(1, (t - tk - 0.3) / 0.5)); db.rounded_rectangle([30, 230, 30 + 460 * qq, 280], 12, fill=GREEN + (255,)); db.text((46, 238), "api/CLAUDE.md", font=font(24, "mono"), fill=WHITE + (255,))
            enter(base, blk, 1460, 400, t, tw - 0.1, side=1)
            arrow(base, 1060, 400, 1190, 400, t, tw)
        if t >= tk - 0.3:
            q = ease_io(min(1, (t - tk + 0.3) / 0.5)); cursor(base, 760 - 120 * q, 760 - 120 * q + 0, tk + 0.2, t)
            if t >= tk: enter(base, pill("api/users.ts edit", 26, INK, WHITE), 640, 700, t, tk, side=0, dur=0.3, shad=False)
    run_text(base, t, s, [(None, ""), ("चार", "*4 jagah*"), ("पहली", "1. *Project folder*: team ke liye, git me"), ("दूसरी", "2. *Home* `~/.claude`: sab projects"), ("तीसरी", "3. *CLAUDE.local.md*: sirf aap"),
                          ("gitignore", "Ise *.gitignore* me daalo"), ("चौथी", "4. Company ki *managed* file"), ("current", "Current folder + *upar ke sab* folders"), ("जोड़", "Sab *jud* jaati hain"), ("Sub", "Sub folder: *jab wahan kaam* ho")], t_from=t0 + 1.3)


def b_init(base, t, s):
    t0 = SC[s]; numeral(base, t, t0, "3", "/init se banayein")
    if opener_on(s, t) and t < t0 + 1.25: return
    ti = at(s, "init."); tr = at(s, "पढ़ता"); tm = at(s, "memory"); tcx = at(s, "context"); tch = at(s, "चुनिए"); te = at(s, "editor")
    lines = [("cd my-app", at(s, "folder") - 0.2, "cmd"), ("claude", at(s, "claude", 1) - 0.1, "cmd"), ("/init", ti - 0.3, "cmd"),
             ("Reading codebase...", tr, "out"), ("Wrote CLAUDE.md", at(s, "starting"), "ok"),
             ("/memory", tm - 0.3, "cmd"), ("/context all", tcx - 0.3, "cmd"), ("Memory files:", at(s, "Memory") - 0.1, "acc"), ("  ./CLAUDE.md", at(s, "list") - 0.3, "ok")]
    enter(base, term_card(760, 560, t, lines, title="Terminal · my-app", fs=32), 600, 400, t, max(t0 + 1.3, at(s, "Terminal") - 0.1), side=-1, rot=-1.2, float_amp=3)
    if tr <= t < at(s, "starting"):
        d = ImageDraw.Draw(base); q = (t - tr) / max(0.5, at(s, "starting") - tr)
        d.rounded_rectangle([240, 700, 960, 720], 10, fill=LGREY + (255,)); d.rounded_rectangle([240, 700, 240 + 720 * min(1, q), 720], 10, fill=ACC + (255,))
    if at(s, "starting") - 0.1 <= t < tm - 0.3:
        ed = [("# Build", at(s, "build") - 0.1, "h"), ("npm run build", at(s, "build") + 0.2, "l"), ("# Test", at(s, "test") - 0.1, "h"), ("npm test", at(s, "test") + 0.2, "l"),
              ("# Conventions", at(s, "conventions") - 0.1, "h"), ("2-space indent", at(s, "conventions") + 0.3, "l")]
        enter(base, editor(640, 520, t, ed, tag="example"), 1400, 400, t, at(s, "starting") - 0.1, side=1)
        rays(base, 1690, 160, t, at(s, "starting"))
        if t >= at(s, "overwrite") - 0.2:
            enter(base, pill("overwrite nahi", 32, WHITE, INK, icon="cross"), 1400, 160, t, at(s, "overwrite") - 0.2, side=0, dur=0.3)
            enter(base, pill("sirf sujhaav", 32, GREEN, WHITE, icon="tick"), 1400, 250, t, at(s, "सुधार") - 0.1, side=0, dur=0.3)
    if tm - 0.3 <= t < tcx - 0.4:
        menu = white_card(600, 320, 22); d = ImageDraw.Draw(menu); d.text((30, 22), "Memory files", font=font(32, "bold"), fill=INK + (255,))
        sel = t >= tch
        for i, (a, b) in enumerate((("Project", "./CLAUDE.md"), ("User", "~/.claude/CLAUDE.md"))):
            y = 90 + 100 * i
            if i == 0 and sel: d.rounded_rectangle([20, y - 8, 580, y + 76], 16, fill=ACC2 + (255,))
            d.text((40, y), a, font=font(30, "bold"), fill=INK + (255,)); d.text((40, y + 38), b, font=font(24, "mono"), fill=GREY + (255,))
        enter(base, menu, 1380, 330, t, tm - 0.1, side=1, t_out=te - 0.1)
        if t >= tch - 0.6: q = ease_io(min(1, (t - tch + 0.6) / 0.5)); cursor(base, 1700 - 180 * q, 640 - 330 * q, tch, t)
        if t >= te - 0.1:
            ed = [("# Project rules", te, "h"), ("npm test", te, "l"), ("_", te, "c")]
            enter(base, editor(620, 360, t, ed, title="CLAUDE.md  (editor)", cps=200), 1380, 380, t, te - 0.1, side=0, dur=0.35)
    if t >= tcx - 0.4:
        c = white_card(560, 260, 22); d = ImageDraw.Draw(c); d.text((30, 24), "/context all", font=font(32, "mono"), fill=ACC + (255,)); d.text((30, 90), "Memory files", font=font(32, "bold"), fill=INK + (255,))
        if t >= at(s, "list") - 0.3: tick(d, 30, 160, 0.9); d.text((100, 164), "./CLAUDE.md loaded", font=font(30, "bold"), fill=INK + (255,))
        enter(base, c, 1400, 400, t, tcx - 0.3, side=1)
    run_text(base, t, s, [(None, ""), ("Terminal", "Terminal me *project folder*"), ("claude", "`claude` chalao, phir `/init`"), ("पढ़ता", "Claude *codebase padhta* hai"), ("starting", "Ban gayi *starting file*"),
                          ("अगर", "Pehle se hai? *Overwrite nahi*, sirf *sujhaav*"), ("इसके", "Edit: `/memory` chalao"), ("चुनिए", "File chuno, *editor me khulegi*"), ("Check", "Check: `/context all`"), ("Memory", "*Memory files* list dekho")], t_from=t0 + 1.3)


def b_write(base, t, s):
    t0 = SC[s]; numeral(base, t, t0, "4", "Kya likhein")
    if opener_on(s, t) and t < t0 + 1.25: return
    tc = at(s, "check", 2); tk = at(s, "कब")
    if t < tc - 0.2:
        e1, e2, e3 = at(s, "commands."), at(s, "conventions."), at(s, "gotchas.")
        ed = [("# Commands", e1 - 0.05, "h"), ("- Install: pnpm install", at(s, "Install"), "l"), ("- Ek test: pnpm vitest run a.test.ts", at(s, "test", 1), "l"), ("- Typecheck: pnpm tsc --noEmit", at(s, "typecheck"), "l"),
              ("# Conventions", e2 - 0.05, "h"), ("- Errors: src/lib/errors.ts helpers", at(s, "helper"), "l"), ("- src/legacy: pattern copy mat karo", at(s, "legacy"), "l"),
              ("# Gotchas", e3 - 0.05, "h"), ("- Integration tests: DATABASE_URL", at(s, "DATABASE_URL"), "hl")]
        enter(base, editor(860, 600, t, ed, tag="example", fs=28), 620, 440, t, max(t0 + 1.3, at(s, "सिर्फ़") - 0.1), side=-1, float_amp=2)
        for i, (lab, ts) in enumerate((("Commands", e1), ("Conventions", e2), ("Gotchas", e3))):
            sel = (t >= ts - 0.1) and (i == 2 or t < [e2, e3][i] - 0.1)
            c = white_card(330, 120, 20); d = ImageDraw.Draw(c); d.text((165 - font(34, "bold").getlength(lab) / 2, 36), lab, font=font(34, "bold"), fill=(ACC if sel else GREY) + (255,))
            if sel: d.rounded_rectangle([0, 0, 329, 119], 20, outline=ACC + (255,), width=4)
            y = 210 + 190 * i
            k = ease_back(min(1, (t - ts + 0.1) / 0.3)) if sel else 0
            if t >= ts - 0.1: place(base, shadow(330, 120), 1440, y, 1 + 0.22 * k, 1); place(base, c, 1440, y, 1 + 0.22 * k)
            else: place(base, c, 1440, y, 1.0, 0.45)
            ImageDraw.Draw(base).text((1165, y - 30), str(i + 1), font=font(56, "xb"), fill=((ACC if sel else LGREY) + (255,)))
    elif t < tk - 0.2:
        t1, t2 = at(s, "Format"), at(s, "Test", 2) if sum("Test" in x[0] for x in toks(s)) > 1 else at(s, "Test")
        first = t < t2 - 0.2
        bad, good, tb, tg = (("Format code properly", "Use 2-space indentation", t1, at(s, "two")) if first else ("Test your changes", "Commit se pehle: npm test", t2, at(s, "npm")))
        tin = tc - 0.1 if first else t2 - 0.2
        cb = white_card(640, 220); d = ImageDraw.Draw(cb); cross(d, 30, 30); d.text((110, 34), "Bekaar", font=font(30, "bold"), fill=RED + (255,)); d.text((40, 120), bad, font=font(36, "mono"), fill=GREY + (255,))
        enter(base, cb, 580, 400, t, tin if first else max(tin, tb - 0.15), side=-1, t_out=(t2 - 0.3) if first else None)
        cg = white_card(640, 220); d = ImageDraw.Draw(cg); tick(d, 30, 30); d.text((110, 34), "Check ho sake", font=font(30, "bold"), fill=GREEN + (255,)); d.text((40, 120), good, font=font(36, "mono"), fill=INK + (255,))
        enter(base, cg, 1340, 400, t, tg - 0.15, side=1, t_out=(t2 - 0.3) if first else None)
        arrow(base, 915, 400, 1005, 400, t, tg - 0.15)
    else:
        hang(base, t, tk - 0.1, 520, 360, circle_icon("+", ACC, 90))
        sparkle_list(base, t, [("Claude ne same galti 2nd baar ki", at(s, "गलती") - 0.2, False), ("Wahi correction dobara type kiya", at(s, "correction") - 0.2, False)], 760, 260, gap=120, fs=48)
    run_text(base, t, s, [(None, ""), ("सिर्फ़", "Sirf wo jo Claude *code se nahi* jaan sakta"), ("Example", "Example 1: *Commands*"), ("conventions.", "Example 2: *Conventions*"), ("gotchas.", "Example 3: *Gotchas*"),
                          ("check", "Aisa likho jo *check* ho sake"), ("कब", "*Kab* jodein?"), ("गलती", "Same *galti* 2nd baar"), ("correction", "Wahi *correction* dobara")], t_from=t0 + 1.3)


def b_size(base, t, s):
    t0 = SC[s]; numeral(base, t, t0, "5", "Size aur imports")
    if opener_on(s, t) and t < t0 + 1.25: return
    t200 = at(s, "सौ"); tl = at(s, "लंबी"); tat = at(s, "at", 1); t4 = at(s, "चार"); tr = at(s, "rules"); tcost = at(s, "खर्च", 2)
    if t < tat - 0.2:
        enter(base, big_num("200", "lines se kam"), 560, 390, t, max(t0 + 1.3, t200 - 0.3), side=0, dur=0.4, shad=False)
        corner_bursts(base, t, t200 - 0.2)
        if t >= tl - 0.1:
            c = white_card(640, 400); d = ImageDraw.Draw(c); q = ease_io(min(1, (t - tl + 0.1) / 1.6))
            d.text((34, 24), "File ki lambai", font=font(32, "bold"), fill=INK + (255,)); d.rounded_rectangle([34, 80, 606, 120], 14, fill=(236, 237, 242, 255)); d.rounded_rectangle([34, 80, 34 + 572 * (0.3 + 0.7 * q), 120], 14, fill=(AMBER if q > 0.5 else ACC) + (255,))
            d.text((34, 160), "Context kharch", font=font(30, "bold"), fill=INK + (255,)); d.rounded_rectangle([34, 210, 34 + 572 * (0.25 + 0.7 * q), 246], 14, fill=RED + (255,))
            d.text((34, 280), "Follow karna", font=font(30, "bold"), fill=INK + (255,)); d.rounded_rectangle([34, 330, 34 + 572 * (0.95 - 0.6 * q), 366], 14, fill=GREEN + (255,))
            enter(base, c, 1380, 400, t, tl - 0.1, side=1)
    elif t < tr - 0.2:
        ed = [("# Notes", tat - 0.2, "h"), ("See @README", at(s, "README") - 0.2, "hl")]
        enter(base, editor(520, 260, t, ed), 520, 260, t, tat - 0.2, side=-1)
        if t >= at(s, "README") - 0.1:
            arrow(base, 790, 260, 950, 260, t, at(s, "README") - 0.1)
            enter(base, editor(360, 200, t, [("# My app", at(s, "README"), "h")], title="README.md"), 1150, 260, t, at(s, "README"), side=0, dur=0.3)
        if t >= t4 - 0.2:
            d = ImageDraw.Draw(base)
            for i in range(5):
                ts = t4 - 0.2 + 0.18 * i
                if t < ts: continue
                x = 420 + 300 * i; enter(base, circle_icon("md" if i else "C", ACC if i else INK, 40), x, 600, t, ts, side=0, dur=0.3, shad=True, float_amp=2)
                if i: arrow(base, x - 300 + 95, 600, x - 95, 600, t, ts - 0.05, w=5); d.text((x - 150 - 12, 530), str(i), font=font(40, "xb"), fill=ACC + (255,))
        if t >= tcost - 0.6: enter(base, pill("Import bhi poora load: kharch same", 36, INK, WHITE, pad=(36, 14)), 1420, 380, t, tcost - 0.6, side=1, dur=0.35)
    else:
        tm = at(s, "matching")
        rf = [("---", tr, "c"), ("paths:", at(s, "paths") - 0.2, "h"), ('  - "src/api/**"', at(s, "paths"), "hl"), ("---", at(s, "paths") + 0.2, "c"), ("API: input validate karo", at(s, "paths") + 0.4, "l")]
        enter(base, editor(700, 420, t, rf, title=".claude/rules/api.md", fs=30), 600, 390, t, tr - 0.15, side=-1)
        files = [("src/api/users.ts", True), ("src/ui/Button.tsx", False)]
        for i, (fn, match) in enumerate(files):
            on = match and t >= tm + 0.3
            c = white_card(560, 110, 18); d = ImageDraw.Draw(c); d.text((30, 30), fn, font=font(32, "mono"), fill=INK + (255,))
            if t >= tm + 0.3: (tick if match else cross)(d, 480, 26, 1.0, GREEN if match else LGREY)
            enter(base, c, 1400, 280 + 190 * i, t, tm - 0.6 + 0.15 * i, side=1)
        if t >= tm - 0.3: q = ease_io(min(1, (t - tm + 0.3) / 0.5)); cursor(base, 1700 - 150 * q, 560 - 260 * q, tm, t)
        if t >= tm + 0.4: enter(base, pill("rule load hua", 30, GREEN, WHITE, icon="tick"), 900, 700, t, tm + 0.4, side=0, dur=0.3)
    run_text(base, t, s, [(None, ""), ("सौ", "Har file *200 lines* se kam"), ("लंबी", "Lambi file = *zyada kharch*, *kam follow*"), ("at", "*@* se import, jaise `@README`"), ("चार", "*4 level* tak"),
                          ("पर", "Par *kharch kam nahi* hota"), ("rules", "Kuch files ke rules: `.claude/rules`"), ("paths", "Upar *paths* likho"), ("तभी", "Sirf *matching files* par load")], t_from=t0 + 1.3)


def b_mistakes(base, t, s):
    t0 = SC[s]; numeral(base, t, t0, "6", "3 aam galtiyan")
    if opener_on(s, t) and t < t0 + 1.25: return
    t1, t2, t3 = at(s, "पहली"), at(s, "दूसरी"), at(s, "तीसरी")
    d = ImageDraw.Draw(base)
    if t < t2 - 0.2:
        place(base, big_num("1", ""), 270, 360, 0.8, min(1, (t - t1 + 0.1) * 5) if t >= t1 - 0.1 else 0)
        ed = [("# Architecture", t1, "h"), ("src/ me 40 folders hain...", t1 + 0.2, "x" if t >= at(s, "repo") else "l"), ("har folder ka poora haal...", t1 + 0.4, "x" if t >= at(s, "repo") else "l"), ("components/ me buttons...", t1 + 0.6, "x" if t >= at(s, "repo") else "l")]
        enter(base, editor(760, 360, t, ed, fs=30), 860, 400, t, max(t0 + 1.3, t1 - 0.1), side=0)
        if t >= at(s, "repo") - 0.1:
            enter(base, pill("Claude repo khud padhta hai", 30, INK, WHITE), 1500, 300, t, at(s, "repo") - 0.1, side=1, dur=0.3)
            enter(base, pill("Sirf jo repo me nahi", 30, GREEN, WHITE, icon="tick"), 1500, 420, t, at(s, "सिर्फ़") - 0.1, side=1, dur=0.3)
    elif t < t3 - 0.2:
        place(base, big_num("2", ""), 270, 360, 0.8)
        th = at(s, "hook"); sh = 6 * math.sin(t * 40) if at(s, "IMPORTANT") <= t < at(s, "फ़र्क") else 0
        ln = editor(760, 200, t, [("IMPORTANT!!! .env kabhi mat padho", t2, "hl")], fs=30)
        enter(base, ln, 860 + sh, 300, t, t2 - 0.1, side=0)
        if t >= at(s, "फ़र्क") - 0.1: cross(d, 1200, 190, 1.0)
        if t >= at(s, "लंबी") - 0.1: enter(base, pill("File bahut lambi?", 30, WHITE, INK), 660, 520, t, at(s, "लंबी") - 0.1, side=0, dur=0.3)
        if t >= at(s, "छूट") - 0.2: enter(base, pill("Koi chhoot nahi?", 30, WHITE, INK), 1080, 520, t, at(s, "छूट") - 0.2, side=0, dur=0.3)
        if t >= th - 0.3:
            hang(base, t, th - 0.3, 1600, 300, gear_icon((t - th) * 120, ACC))
            enter(base, term_card(560, 200, t, [("read .env", th + 0.2, "cmd"), ("BLOCKED by hook", th + 0.9, "red")], title="hook"), 1520, 600, t, th, side=1)
    else:
        place(base, big_num("3", ""), 270, 360, 0.8)
        tc = at(s, "टकराने")
        if t >= t3 - 0.1:
            enter(base, pill("Tabs use karo", 40, WHITE, INK, pad=(34, 16)), 580, 250, t, t3 - 0.1, side=-1, dur=0.35, shad=False)
            enter(base, pill("2 spaces use karo", 40, WHITE, INK, pad=(34, 16)), 1360, 250, t, t3 + 0.1, side=1, dur=0.35, shad=False)
        if t >= tc - 0.2:
            q = ease_io(min(1, (t - tc + 0.2) / 0.6))
            if q > 0: rays(base, 900, 250, t, tc + 0.3, ang0=0, n=14)
            d.line([(750 + 60 * q, 250), (1145 - 60 * q, 250)], fill=RED + (255,), width=5)
        if t >= at(s, "चुन") - 0.2:
            enter(base, pill("Claude koi bhi ek chun sakta hai", 34, AMBER, WHITE, pad=(34, 14)), 900, 360, t, at(s, "चुन") - 0.2, side=0, dur=0.3)
        tp = at(s, "Slash")
        if t >= tp - 0.2:
            lines = [("/doctor prompt-audit", tp - 0.1, "cmd"), ("! 2 instructions takra rahi hain", at(s, "टक्कर"), "warn"), ("! 1 purani baat", at(s, "पुरानी"), "warn")]
            enter(base, term_card(820, 250, t, lines, title="Claude Code"), 900, 590, t, tp - 0.2, side=0, dur=0.35)
    run_text(base, t, s, [(None, ""), ("पहली", "1. Poora *architecture* likh dena"), ("Claude", "Claude *repo khud* padhta hai"), ("दूसरी", "2. Line par *IMPORTANT* likhna"), ("फ़र्क", "Aksar *farq nahi* padta"),
                          ("ऐसे", "Pakke rule ke liye *hook*"), ("तीसरी", "3. *Takraate* instructions"), ("Slash", "`/doctor prompt-audit` dhoondh deta hai")], t_from=t0 + 1.3)


def b_recap(base, t, s):
    t0 = SC[s]; ta = at(s, "अगला"); tf = at(s, "follow")
    if t < ta - 0.2:
        items = [("/init se file banao", at(s, "init"), True), ("Commands, conventions, gotchas", at(s, "commands"), True), ("200 lines se kam", at(s, "सौ"), True), ("Pakke rule = hook", at(s, "hook"), True)]
        sparkle_list(base, t, items, 560, 140, gap=110, fs=54)
        hang(base, t, t0 + 0.05, 330, 330, file_icon())
    else:
        c = white_card(820, 300); d = ImageDraw.Draw(c); d.text((40, 30), "Agla video", font=font(34, "bold"), fill=GREY + (255,)); d.text((40, 90), "Claude Code: Plan mode", font=font(54, "xb"), fill=INK + (255,))
        d.text((40, 190), "pehle plan, phir code", font=font(36, "med"), fill=ACC + (255,))
        enter(base, c, 700, 380, t, ta - 0.15, side=-1)
        enter(base, pill("+ Follow", 64, INK, WHITE, pad=(70, 26), r=50), 1450, 380, t, tf - 0.8, side=1, dur=0.4)
        if t >= tf - 0.5: q = ease_io(min(1, (t - tf + 0.5) / 0.5)); cursor(base, 1760 - 250 * q, 640 - 230 * q, tf, t)
    run_text(base, t, s, [(None, "Yaad rakhiye"), ("init", "`/init` se *banao*"), ("commands", "Sirf *zaroori* baatein"), ("सौ", "*200 lines* se kam"), ("hook", "Pakka rule = *hook*"), ("अगला", "Agla: *Plan mode*"), ("follow", "Miss na ho: *follow* kijiye")])


FN = dict(hook=b_hook, what=b_what, where=b_where, init=b_init, write=b_write, size=b_size, mistakes=b_mistakes, recap=b_recap)
BGIM = Image.new("RGBA", (W, H), BG + (255,))


def scene_at(t):
    for k in reversed(IDS):
        if t >= SC[k]: return k
    return IDS[0]


VS, VCX, VCY = 1.12, 960, 400
def frame(t):
    s = scene_at(t); base = BGIM.copy(); vis = Image.new("RGBA", (W, H), (0, 0, 0, 0)); _TXT[0] = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    FN[s](vis, t, s)
    sw, sh = int(W * VS), int(H * VS); vs = vis.resize((sw, sh), Image.BILINEAR); ox, oy = int(VCX - VCX * VS), int(VCY - VCY * VS)
    base.alpha_composite(vs.crop((-ox, -oy, -ox + W, -oy + H))); base.alpha_composite(_TXT[0]); _TXT[0] = None
    chapter_badge(base, s, t); watermark(base)
    p = min(1, max(0, (t - SC[s]) / max(1.0, D[IDS.index(s)]))); z = 1.0 + 0.035 * p; im = base.convert("RGB")
    if z > 1.001:
        cw, ch = int(W / z), int(H / z); cx0 = int((W - cw) * (0.35 + 0.3 * p)); cy0 = int((H - ch) * 0.4)
        im = im.crop((cx0, cy0, cx0 + cw, cy0 + ch)).resize((W, H), Image.BILINEAR)
    return np.array(im)


SR = 24000
def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "info"
    if cmd == "info":
        print(f"total {TOTAL:.1f}s"); [print(f"  {k:9s} {SC[k]:6.1f} {D[i]:5.1f}") for i, k in enumerate(IDS)]; return
    if cmd == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/frames/f_{tt:06.1f}.png")
        return
    if cmd == "chunk":
        i, N = int(sys.argv[2]), int(sys.argv[3]); n = int(TOTAL * FPS); a, b = n * i // N, n * (i + 1) // N
        out = HERE / f"output/c_{i:02d}.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                              "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(out)], stdin=subprocess.PIPE)
        for f in range(a, b):
            p.stdin.write(frame(f / FPS).tobytes())
            if (f - a) % 300 == 0: print(f"chunk {i}: {f - a}/{b - a}", flush=True)
        p.stdin.close(); p.wait(); print(f"chunk {i} done", flush=True); return
    if cmd == "mux":
        N = int(sys.argv[2]); build_audio(HERE / "audio/voice.wav")
        lst = HERE / "output/chunks.txt"; lst.write_text("".join(f"file 'c_{i:02d}.mp4'\n" for i in range(N)), encoding="utf-8")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(HERE / "output/video_only.mp4")], check=True)
        mu = ROOT / deck["music"]["file"]
        fc = ("[2:a]volume=-22dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];"
              "[v][m]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=%.2f:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=7[a]" % (TOTAL - 1.6))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(HERE / "output/video_only.mp4"), "-i", str(HERE / "audio/voice.wav"), "-stream_loop", "-1", "-ss", str(deck["music"]["start"]), "-i", str(mu),
                        "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(HERE / "output/long_final.mp4")], check=True)
        print("muxed output/long_final.mp4"); return


if __name__ == "__main__":
    main()
