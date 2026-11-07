"""Claude Feature 05 (Memory) LONG video, 16:9 1920x1080. Look: STYLE_LIBRARY sections 0, 9, 10 (no face, no robot box, whole screen shows what is said,
normal-size text, chapter badge, dark-neon theme with SKY BLUE highlight, dark Claude walkthrough). Voice + Funkorama only, no whoosh.
Run: python make_long.py [frames t1 t2 ...]   (needs audio/tts/s_*.wav, wt.json, raw/photos/*.png, raw/article*.png, raw/rects.json)"""
import json, math, re, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import ease_out, ease_back, ease_io, wav_dur
import subprocess

W, H, FPS = 1920, 1080, 30
LEAD, AFTER = 0.05, 0.05
SKY = (91, 200, 255); WHITE = (255, 255, 255); RED = (255, 96, 106); AMB = (255, 190, 80); DIM = (150, 160, 182)
BG0 = (7, 9, 15); CARD = (19, 23, 33); OUT = (58, 68, 94); INK = (10, 12, 18)
FMUK = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf"); FPOP = str(ROOT / "shared/fonts/Poppins-Medium.ttf"); FPOPB = str(ROOT / "shared/fonts/Poppins-Bold.ttf")
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; D[-1] += 3.0; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START)); DUR = dict(zip(IDS, D))


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]
def S(scene, off): return SC[scene] + off
def E(scene): return SC[scene] + DUR[scene]


_f = {}
def F(sz, kind="m"):
    k = (sz, kind)
    if k not in _f: _f[k] = ImageFont.truetype({"m": FMUK, "p": FPOP, "b": FPOPB}[kind], sz)
    return _f[k]


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def pop(t, t0, dur=0.28): return ease_back((t - t0) / dur) if t >= t0 else 0.0
def fade(t, t0, dur=0.25): return min(1.0, max(0.0, (t - t0) / dur))


def pill(text, size=34, fill=(20, 24, 34), color=WHITE, pad=(24, 9), r=None, hl=(), hlc=SKY, outline=None, kind="m", glow=False):
    f = F(size, kind); words = text.split(" "); sp = f.getlength(" "); wl = [f.getlength(w) for w in words]; tw = int(sum(wl) + sp * (len(words) - 1)); a, d_ = f.getmetrics()
    w_, h_ = tw + 2 * pad[0], a + d_ + 2 * pad[1]; r = r or h_ // 2
    im = Image.new("RGBA", (w_ + 24, h_ + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle([12, 12, w_ + 11, h_ + 11], r, outline=SKY + (255,), width=4); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(7)))
    d.rounded_rectangle([12, 12, w_ + 11, h_ + 11], r, fill=fill + (255,), outline=(outline + (255,)) if outline else None, width=3)
    x = 12 + pad[0]
    for w, l in zip(words, wl):
        d.text((x, 12 + pad[1]), w, font=f, fill=(hlc if w.strip(",.?!:") in hl else color) + (255,)); x += l + sp
    return im


def card(w, h, r=30, fill=CARD, outline=OUT, ow=3, glow=False):
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle([20, 20, w + 19, h + 19], r, outline=SKY + (255,), width=5); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(im).rounded_rectangle([20, 20, w + 19, h + 19], r, fill=fill + (255,), outline=outline + (255,), width=ow); return im


def rounded(img, r):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255); o = img.convert("RGBA"); o.putalpha(m); return o


def enter(base, spr, cx, cy, t, t0, side=0, dur=0.32, rot=0):
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur)); dx = side * (1 - q) * 360; dy = (1 - q) * (80 if side == 0 else 0)
    place(base, spr, cx + dx, cy + dy, 0.94 + 0.06 * e, min(1, q * 1.5), rot)


def txt(base, xy, s, size, fill=WHITE, kind="m", anchor="la", alpha=1.0):
    d = ImageDraw.Draw(base); d.text(xy, s, font=F(size, kind), fill=fill + (int(255 * alpha),), anchor=anchor)


def typed(s, t, a0, a1): n = int(len(s) * min(1, max(0, (t - a0) / max(0.1, a1 - a0)))); return s[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(s) else "")


# ---------- background / badge / caption ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None, None]; x = np.linspace(-1, 1, W)[None, :, None]
    base = np.array(BG0, dtype=np.float32)[None, None, :] + 14 * (1 - y) * np.exp(-x ** 2 * 1.5)
    base = np.clip(base + 0 * x, 0, 255).astype(np.uint8); im = Image.fromarray(np.broadcast_to(base, (H, W, 3)).copy()).convert("RGBA")
    d = ImageDraw.Draw(im)
    for gx in range(0, W, 96): d.line([(gx, 0), (gx, H)], fill=(14, 18, 27, 255), width=1)
    for gy in range(0, H, 96): d.line([(0, gy), (W, gy)], fill=(14, 18, 27, 255), width=1)
    return im
BG = make_bg()
CHAP = {"hook": None, "what": (1, "what it is"), "who": (2, "who gets it"), "switch": (3, "on / off"), "see": (4, "see and delete"), "never": (5, "never saved"),
        "private": (6, "private chats"), "projects": (7, "projects"), "caution": (8, "caution"), "cta": (9, "recap")}


def badge(base, sid, t):
    c = CHAP[sid]
    if not c: return
    sq = Image.new("RGBA", (54, 54), (0, 0, 0, 0)); d = ImageDraw.Draw(sq); d.rounded_rectangle([0, 0, 53, 53], 12, fill=SKY + (255,)); d.text((27, 27), str(c[0]), font=F(34, "b"), fill=INK + (255,), anchor="mm")
    place(base, sq, 86, 70); place(base, pill(c[1].upper(), 26, (20, 24, 34), WHITE, pad=(18, 6), outline=OUT, kind="p"), 86 + 36 + 100, 70)


def caption_chunks():
    out = []
    for sid in IDS:
        toks = WT[sid]["tokens"]; segs = []; cur = []
        for k, (tk, _) in enumerate(toks):
            cur.append(k)
            if re.search(r"[,।?!]$", tk): segs.append(cur); cur = []
        if cur: segs.append(cur)
        for sg in segs:
            n = len(sg); k = -(-n // 4); sizes = [n // k + (1 if j < n % k else 0) for j in range(k)]; i = 0
            for z in sizes: idx = sg[i:i + z]; out.append((SC[sid] + LEAD + toks[idx[0]][1], " ".join(toks[q][0] for q in idx))); i += z
    ends = [c[0] for c in out[1:]] + [TOTAL]
    return [(a, min(b, a + 2.2), txt_) for (a, txt_), b in zip(out, ends)]
CAPS = caption_chunks()
KEYW = {"Memory", "memory", "Pause", "Reset", "Manage", "Delete", "Incognito", "Settings", "toggle", "ID", "bank", "delete", "Projects", "project", "Topics", "plans", "Free,", "Pro,", "Max", "Ultra,", "ghost", "plus", "भूल", "नहीं", "हमेशा"}
_cap = {}
def caption(base, t):
    for a, b, s in CAPS:
        if a - 0.04 <= t < b:
            if s not in _cap: _cap[s] = pill(s, 40, (8, 10, 16), WHITE, pad=(30, 8), hl=KEYW, hlc=SKY, outline=(40, 48, 68))
            place(base, _cap[s], W / 2, 1010, 0.95 + 0.05 * ease_out((t - a) / 0.1)); return


# ---------- photos ----------
PH = {k: Image.open(HERE / f"raw/photos/{k}.png").convert("RGB") for k in ("hook", "notebook", "laptop", "folders", "trash")}
_cov = {}
def photo(key, w, h, lt, dur, z0=1.0, z1=1.15, r=30):
    src = PH[key]; ck = (key, w, h)
    if ck not in _cov: s = max(1.4 * w / src.width, 1.4 * h / src.height); _cov[ck] = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    cov = _cov[ck]; p = ease_io(min(1, max(0, lt / dur))); z = z0 + (z1 - z0) * p; ww, wh = w * 1.2 / z, h * 1.2 / z
    cx, cy = cov.width / 2, cov.height / 2
    im = cov.crop((int(cx - ww / 2), int(cy - wh / 2), int(cx + ww / 2), int(cy + wh / 2))).resize((w, h), Image.BILINEAR)
    sp = rounded(im, r); out = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); out.alpha_composite(card(w, h, r, fill=(0, 0, 0), outline=OUT)); out.alpha_composite(sp, (20, 20)); return out


# ---------- cursor ----------
def cursor_spr():
    im = Image.new("RGBA", (56, 76), (0, 0, 0, 0)); d = ImageDraw.Draw(im); pts = [(4, 3), (4, 52), (17, 41), (27, 64), (37, 59), (27, 37), (46, 37)]
    d.polygon([(x + 3, y + 3) for x, y in pts], fill=(0, 0, 0, 120)); d.polygon(pts, fill=(255, 255, 255, 255), outline=(10, 10, 10, 255)); return im
CUR = cursor_spr()


def cursor_path(base, t, pts, clicks=()):
    """pts = [(time, x, y)] eased; draws cursor + click ripple at clicks times"""
    if t < pts[0][0]: return (pts[0][1], pts[0][2])
    x, y = pts[-1][1], pts[-1][2]
    for (ta, xa, ya), (tb, xb, yb) in zip(pts, pts[1:]):
        if ta <= t < tb: q = ease_io((t - ta) / (tb - ta)); x, y = xa + (xb - xa) * q, ya + (yb - ya) * q; break
    place(base, CUR, x + 22, y + 30)
    d = ImageDraw.Draw(base)
    for ck in clicks:
        if 0 <= t - ck <= 0.45: rr = int(18 + 55 * (t - ck) / 0.45); d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=SKY + (255,), width=5)
    return (x, y)


def step(base, t, t0, text, y=150):
    if t >= t0: pp = pop(t, t0); place(base, pill(text, 34, SKY, INK, pad=(30, 9), kind="b"), W / 2, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def illu(base, x=1700, y=905): place(base, pill("Illustration, not a recording", 22, (20, 24, 34), DIM, pad=(14, 4), kind="p"), x, y)


# ---------- UI window ----------
WX, WY, WW, WH = 210, 215, 1500, 700   # window area (centre 960, 565)
SIDE = ["General", "Privacy", "Your Claude", "Connectors", "Billing"]
def ui_window(sel_side=2, pane=None, hot=None):
    """pane: callable(im, ox, oy, w, h) draws main pane; returns RGBA sprite"""
    im = card(WW, WH, 26, fill=(14, 17, 25), outline=OUT, ow=3); d = ImageDraw.Draw(im)
    ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + 330, oy + WH - 1], 26, fill=(10, 12, 18, 255)); d.rectangle([ox + 300, oy, ox + 330, oy + WH - 1], fill=(10, 12, 18, 255))
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([ox + 28 + 34 * i, oy + 26, ox + 46 + 34 * i, oy + 44], fill=c + (255,))
    d.text((ox + 34, oy + 80), "Settings", font=F(40, "b"), fill=WHITE + (255,))
    for i, s in enumerate(SIDE):
        y = oy + 150 + i * 78
        if i == sel_side: d.rounded_rectangle([ox + 20, y - 8, ox + 310, y + 52], 16, fill=(28, 48, 66, 255), outline=SKY + (255,), width=2)
        d.text((ox + 50, y), s, font=F(32, "p"), fill=(SKY if i == sel_side else (200, 208, 224)) + (255,))
    if pane: pane(im, ox + 330, oy, WW - 330, WH)
    else:
        d.text((ox + 380, oy + 70), SIDE[sel_side], font=F(46, 'b'), fill=WHITE + (255,))
        for i in range(3): d.rounded_rectangle([ox + 380, oy + 170 + 110 * i, ox + WW - 80, oy + 260 + 110 * i], 20, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
    return im


def toggle(d, x, y, on, w=96, h=50):
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=(SKY if on else (70, 78, 98)) + (255,)); kx = x + w - h // 2 - 3 if on else x + h // 2 + 3
    d.ellipse([kx - h // 2 + 6, y + 6, kx + h // 2 - 6, y + h - 6], fill=(255, 255, 255, 255))


def pane_your_claude(on=True, manage_hot=False, menu=0.0, pick=None):
    def f(im, ox, oy, w, h):
        d = ImageDraw.Draw(im); d.text((ox + 50, oy + 70), "Your Claude", font=F(46, "b"), fill=WHITE + (255,))
        d.rounded_rectangle([ox + 50, oy + 170, ox + w - 50, oy + 280], 20, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
        d.text((ox + 80, oy + 200), "Generate memory from chats", font=F(34, "p"), fill=WHITE + (255,)); toggle(d, ox + w - 190, oy + 200, on)
        d.rounded_rectangle([ox + 50, oy + 310, ox + w - 50, oy + 420], 20, fill=(22, 27, 39, 255), outline=(SKY if manage_hot else OUT) + (255,), width=3 if manage_hot else 2)
        d.text((ox + 80, oy + 340), "Your memory", font=F(34, "p"), fill=WHITE + (255,)); d.rounded_rectangle([ox + w - 250, oy + 335, ox + w - 80, oy + 395], 16, fill=(40, 52, 76, 255)); d.text((ox + w - 165, oy + 365), "Manage", font=F(30, "b"), fill=SKY + (255,), anchor="mm")
        if menu > 0.02:
            mw, mh = 520, 250; m = card(mw, mh, 22, fill=(24, 30, 44), outline=SKY, ow=3); md = ImageDraw.Draw(m)
            md.rounded_rectangle([40, 44, mw, 44 + 90], 16, fill=((34, 60, 84, 255) if pick == "pause" else (30, 36, 52, 255)), outline=(SKY + (255,)) if pick == "pause" else None, width=2)
            md.text((70, 62), "Pause memory", font=F(34, "b"), fill=WHITE + (255,))
            md.rounded_rectangle([40, 150, mw, 150 + 90], 16, fill=((70, 28, 36, 255) if pick == "reset" else (30, 36, 52, 255)), outline=(RED + (255,)) if pick == "reset" else None, width=2)
            md.text((70, 168), "Reset memory", font=F(34, "b"), fill=RED + (255,))
            sc = 0.85 + 0.15 * min(1, menu); im.alpha_composite(m.resize((int(m.width * sc), int(m.height * sc))), (ox + w - 640, oy + 290))
    return f


TOPICS = [("Role", "student, 3rd year"), ("Project", "thesis on solar energy"), ("Style", "short answers please"), ("College", "St. Mary's, Pune")]
def pane_topics(sel=None, edit=False, deleted=False, hot_del=False):
    def f(im, ox, oy, w, h):
        d = ImageDraw.Draw(im); d.text((ox + 50, oy + 60), "Your memory  ·  Topics", font=F(42, "b"), fill=WHITE + (255,))
        rows = [r for r in TOPICS if not (deleted and r[0] == "College")]
        for i, (a, b) in enumerate(rows):
            y = oy + 150 + i * 105; on = (sel == a)
            d.rounded_rectangle([ox + 50, y, ox + w - 50, y + 88], 18, fill=((28, 48, 66, 255) if on else (22, 27, 39, 255)), outline=(SKY if on else OUT) + (255,), width=3 if on else 2)
            d.text((ox + 82, y + 24), a, font=F(32, "b"), fill=SKY + (255,)); d.text((ox + 300, y + 24), b, font=F(32, "p"), fill=(220, 226, 238, 255))
        if sel == "College" and not deleted:
            d.rounded_rectangle([ox + w - 560, oy + 575, ox + w - 70, oy + 660], 16, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
            d.rounded_rectangle([ox + w - 540, oy + 590, ox + w - 400, oy + 645], 12, fill=((40, 52, 76, 255) if not edit else (34, 60, 84, 255)), outline=(SKY + (255,)) if edit else None, width=2); d.text((ox + w - 470, oy + 618), "Edit", font=F(28, "b"), fill=SKY + (255,), anchor="mm")
            d.rounded_rectangle([ox + w - 380, oy + 590, ox + w - 90, oy + 645], 12, fill=((90, 30, 40, 255) if hot_del else (60, 30, 36, 255))); d.text((ox + w - 235, oy + 618), "Delete", font=F(28, "b"), fill=RED + (255,), anchor="mm")
    return f


# ---------- beats (v2: every action tied to the real word times T(scene, token)) ----------
def _mk():
    B = []
    def add(i, sid, a, b): B.append(dict(id=i, sid=sid, t0=a, t1=b))
    add("hook_a", "hook", 0.0, T("hook", 9) - 0.4); add("hook_b", "hook", T("hook", 9) - 0.4, T("hook", 26) - 0.1); add("hook_c", "hook", T("hook", 26) - 0.1, E("hook"))
    add("what_a", "what", S("what", 0), T("what", 34) - 0.3); add("what_b", "what", T("what", 34) - 0.3, E("what"))
    add("who_a", "who", S("who", 0), T("who", 18) - 0.3); add("who_b", "who", T("who", 18) - 0.3, E("who"))
    add("switch", "switch", S("switch", 0), E("switch")); add("see", "see", S("see", 0), E("see")); add("never", "never", S("never", 0), E("never"))
    add("private_a", "private", S("private", 0), T("private", 36) - 0.3); add("private_b", "private", T("private", 36) - 0.3, E("private"))
    add("projects", "projects", S("projects", 0), E("projects"))
    add("caution_a", "caution", S("caution", 0), T("caution", 19) - 0.2); add("caution_b", "caution", T("caution", 19) - 0.2, E("caution"))
    add("cta_a", "cta", S("cta", 0), T("cta", 30) - 0.3); add("cta_b", "cta", T("cta", 30) - 0.3, TOTAL + 1)
    return B
B = _mk()


def bubble(w, h, text, side="user", size=34):
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w + 3, h + 3], 26, fill=((34, 60, 84, 255) if side == "user" else (26, 31, 45, 255)), outline=(SKY if side == "user" else OUT) + (255,), width=2)
    d.text((34, h // 2 + 4), text, font=F(size, "p"), fill=WHITE + (255,), anchor="lm"); return im


def b_hook_a(base, t, b):
    lt = t - b["t0"]; dur = b["t1"] - b["t0"]
    enter(base, photo("hook", 760, 520, lt, dur + 4), 520, 520, t, b["t0"] + 0.02, side=-1)
    c = card(860, 520, 30); d = ImageDraw.Draw(c); d.text((50, 40), "Day 1", font=F(30, "b"), fill=SKY + (255,)); d.text((50, 330), "Day 2", font=F(30, "b"), fill=SKY + (255,))
    enter(base, c, 1400, 520, t, b["t0"] + 0.2, side=1)
    place(base, bubble(740, 84, typed("My name is Rahul. I'm a student.", t, 0.5, 2.2)), 1400, 420, 1.0, fade(t, 0.4))
    t2 = T("hook", 9)
    if t > t2: place(base, bubble(740, 84, typed("Hi! Who are you again?", t, t2 + 0.1, t2 + 1.0), "claude"), 1400, 640, 1.0, fade(t, t2))


def b_hook_b(base, t, b):
    marks = [(T("hook", 13), "NAME", "naam", T("hook", 19)), (T("hook", 15), "WORK", "kaam", T("hook", 19) + 0.3), (T("hook", 18), "LIKES", "pasand", T("hook", 19) + 0.6)]
    for i, (ta, a, c, tg) in enumerate(marks):
        x = 480 + 480 * i; y = 520
        enter(base, card(400, 300, 30), x, y, t, ta - 0.3, side=0)
        spr = Image.new("RGBA", (400, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(spr)
        d.text((200, 110), a, font=F(54, "b"), fill=WHITE + (255,), anchor="mm"); d.text((200, 180), c, font=F(34, "p"), fill=DIM + (255,), anchor="mm")
        enter(base, spr, x, y, t, ta - 0.3)
        if t >= tg: pp = pop(t, tg); place(base, pill("again?", 30, RED, INK, pad=(20, 6), kind="b"), x + 110, y - 160, 0.6 + 0.4 * pp, min(1, pp * 1.4), -6)
    if t >= T("hook", 23): pp = pop(t, T("hook", 23)); place(base, pill("tired of repeating?", 34, (30, 30, 40), DIM, pad=(28, 10), kind="p", outline=OUT), 960, 780, 0.8 + 0.2 * pp, min(1, pp * 1.4))


def b_hook_c(base, t, b):
    t0 = T("hook", 28) - 0.1
    if t >= t0: place(base, pill("CLAUDE MEMORY", 84, (20, 24, 34), WHITE, pad=(60, 22), outline=SKY, kind="b", glow=True), W / 2, 430, 0.85 + 0.15 * pop(t, t0), min(1, fade(t, t0, 0.2)))
    for i, (s, tt) in enumerate([("what it is", T("hook", 41)), ("on / off", T("hook", 44)), ("see and delete", T("hook", 53))]):
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 36, (20, 24, 34), SKY, pad=(30, 10), outline=OUT, kind="b"), 560 + 400 * i, 640, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_what_a(base, t, b):
    enter(base, card(520, 360, 28), 440, 500, t, b["t0"], side=-1); txt(base, (230, 360), "your chat", 28, DIM, "p")
    ev = [(T("what", 16) - 0.2, "I'm a student", "ROLE", "student"), (T("what", 22) - 0.2, "working on a thesis", "PROJECT", "thesis"), (T("what", 30) - 0.2, "keep answers short", "STYLE", "short answers")]
    for i, (tt, s, a, c) in enumerate(ev):
        if t >= tt: place(base, bubble(430, 64, s, "user", 28), 440, 440 + 80 * i, 1.0, fade(t, tt))
    d = ImageDraw.Draw(base); ta = T("what", 9)
    if t >= ta:
        q = ease_out((t - ta) / 0.6); d.line([(720, 500), (720 + 130 * q, 500)], fill=SKY + (255,), width=5); d.polygon([(850, 500), (830, 484), (830, 516)], fill=SKY + (int(255 * q),))
    enter(base, card(520, 440, 28, glow=True), 1330, 500, t, ta, side=1)
    place(base, pill("MEMORY", 40, (19, 23, 33), SKY, pad=(10, 2), kind="b"), 1330, 340, 1.0, fade(t, ta))
    for i, (tt, s, a, c) in enumerate(ev):
        if t >= tt + 0.5: pp = pop(t, tt + 0.5); place(base, pill(f"{a}: {c}", 32, (30, 44, 62), WHITE, pad=(26, 9), hl=(a + ":",), kind="p", outline=SKY), 1330, 440 + 84 * i, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_what_b(base, t, b):
    enter(base, card(1100, 360, 28), 960, 470, t, b["t0"], side=0)
    ta = T("what", 41)
    place(base, bubble(900, 90, typed("Remember this: I prefer short answers.", t, ta, T("what", 46)), "user", 36), 960, 420, 1.0, fade(t, ta - 0.1))
    tb = T("what", 47)
    if t > tb: place(base, bubble(900, 90, "Saved. I'll keep it in mind.", "claude", 36), 960, 540, 1.0, fade(t, tb))
    tc = T("what", 50)
    if t > tc: pp = pop(t, tc); place(base, pill("saved to memory", 30, SKY, INK, pad=(22, 7), kind="b"), 960, 700, 0.6 + 0.4 * pp, min(1, pp * 1.4))


def b_who_a(base, t, b):
    for i, (s, tt) in enumerate([("Free", T("who", 5)), ("Pro", T("who", 6)), ("Max", T("who", 7)), ("Ultra", T("who", 9))]):
        x = 390 + 380 * i; enter(base, card(300, 200, 28, glow=t >= tt + 0.3), x, 560, t, tt - 0.2, side=0)
        spr = Image.new("RGBA", (300, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(spr); d.text((150, 85), s, font=F(54, "b"), fill=WHITE + (255,), anchor="mm")
        if t >= tt + 0.3: d.ellipse([200, 125, 260, 185], fill=SKY + (255,)); d.line([(214, 156), (228, 170), (250, 138)], fill=INK + (255,), width=7)
        enter(base, spr, x, 560, t, tt - 0.2)
    tt = T("who", 14) - 0.1
    if t >= tt: place(base, pill("ON BY DEFAULT", 64, (20, 24, 34), SKY, pad=(50, 16), outline=SKY, kind="b", glow=True), W / 2, 270, 0.85 + 0.15 * pop(t, tt), fade(t, tt, 0.2))


def b_who_b(base, t, b):
    for i, (s, c, tt) in enumerate([("WEB", "claude.ai", T("who", 18)), ("DESKTOP", "Claude Desktop", T("who", 19) + 0.5), ("MOBILE", "latest app version", T("who", 21))]):
        x = 440 + 520 * i; enter(base, card(420, 260, 28), x, 460, t, tt - 0.2, side=0)
        spr = Image.new("RGBA", (420, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(spr); d.text((210, 100), s, font=F(48, "b"), fill=SKY + (255,), anchor="mm"); d.text((210, 170), c, font=F(28, "p"), fill=DIM + (255,), anchor="mm"); enter(base, spr, x, 460, t, tt - 0.2)
    tt = T("who", 32)
    if t >= tt: pp = pop(t, tt); place(base, pill("Team / Enterprise: the owner decides", 34, (30, 30, 40), DIM, pad=(30, 12), outline=OUT, kind="p"), W / 2, 740, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_switch(base, t, b):
    sid = "switch"
    t_s1 = T(sid, 10); t_side = T(sid, 15) + 0.1; t_s2 = T(sid, 19); t_toggle = T(sid, 28); t_s3 = T(sid, 30); t_pause = T(sid, 33); t_reset_pick = T(sid, 55); t_reset = T(sid, 57)
    sel = 2 if t >= t_side else 0
    menu = ease_out((t - t_toggle) / 0.3) if t >= t_toggle else 0.0
    pick = "reset" if t >= t_reset_pick else ("pause" if t >= t_pause else None)
    win = ui_window(sel, pane_your_claude(on=True, menu=menu, pick=pick) if sel == 2 else None)
    enter(base, win, 960, 565, t, b["t0"], dur=0.3)
    st = "STEP 3   Pause  or  Reset" if t >= t_s3 else ("STEP 2   toggle: Generate memory from chats" if t >= t_s2 else "STEP 1   Settings  >  Your Claude")
    step(base, t, t_s1 - 0.2, st)
    if t >= t_pause and t < t_reset_pick: place(base, pill("keeps old memory, stops using it", 28, (30, 44, 62), SKY, pad=(22, 7), kind="p", outline=SKY), 1180, 830, 1.0, fade(t, t_pause))
    if t >= t_reset_pick: pp = pop(t, t_reset_pick); place(base, pill("deletes ALL memory. cannot be undone", 28, (70, 28, 36), RED, pad=(22, 7), kind="p", outline=RED), 1180, 830, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    pts = sorted([(b["t0"], 1200, 300), (t_side - 0.8, 1200, 300), (t_side, 400, 545), (t_toggle - 1.0, 400, 545), (t_toggle - 0.1, 1568, 440), (t_pause - 0.6, 1568, 440), (t_pause, 1350, 594), (t_reset_pick - 0.5, 1350, 594), (t_reset_pick, 1350, 700)])
    cursor_path(base, t, pts, clicks=(t_side, t_toggle, t_reset)); illu(base)


def b_see(base, t, b):
    sid = "see"
    t_s1 = T(sid, 13); t_man = T(sid, 24); t_row = T(sid, 31) + 0.2; t_edit = T(sid, 38); t_del = T(sid, 46); t_chat = T(sid, 50)
    if t < t_chat:
        if t < t_man: pane = pane_your_claude(on=True, manage_hot=t >= t_man - 0.6)
        else:
            sel = "College" if t >= t_row else None
            pane = pane_topics(sel, edit=(t_edit <= t < t_del), deleted=(t >= t_del), hot_del=(t >= t_del - 0.3))
        win = ui_window(2, pane); enter(base, win, 960, 565, t, b["t0"], dur=0.3)
        st = "STEP 2   open a topic: read, Edit or Delete" if t >= T(sid, 26) else "STEP 1   Manage  (next to Your memory)"
        step(base, t, t_s1, st)
        pts = sorted([(b["t0"], 1100, 300), (t_man - 0.7, 1100, 300), (t_man, 1545, 580), (t_man + 0.6, 1545, 580), (t_row - 0.5, 1000, 724), (t_edit - 0.8, 1000, 724), (t_edit, 1070, 832), (t_del - 0.6, 1070, 832), (t_del, 1305, 832), (t_chat, 1305, 832)])
        cursor_path(base, t, pts, clicks=(t_man, t_row, t_edit, t_del)); illu(base)
    else:
        c = card(1300, 620, 30); enter(base, c, 960, 520, t, t_chat, dur=0.3)
        step(base, t, t_chat + 0.2, "or just tell Claude in chat")
        place(base, bubble(1000, 90, typed("Forget my college name.", t, T(sid, 54), T(sid, 59)), "user", 38), 960, 440, 1.0, fade(t, t_chat + 0.4))
        tr = T(sid, 64)
        if t > tr: place(base, bubble(1000, 90, "Done. From the next chat I won't remember it.", "claude", 34), 960, 570, 1.0, fade(t, tr))
        illu(base)


def b_never(base, t, b):
    sid = "never"
    cols = [("SAVED", SKY, ["your role", "your projects", "how you like answers"], [0.3, 0.8, 1.3]),
            ("NOT BY DEFAULT", AMB, ["health", "religion", "politics"], [T(sid, 9), T(sid, 10), T(sid, 12)]),
            ("NEVER SAVED", RED, ["government ID numbers", "bank account numbers", "even if you ask"], [T(sid, 34), T(sid, 39), T(sid, 29)])]
    for i, (title, col, rows, rts) in enumerate(cols):
        x = 360 + 600 * i; tt = (b["t0"] + 0.1) if i == 0 else (T(sid, 9) - 0.3 if i == 1 else T(sid, 25) - 0.3)
        enter(base, card(520, 520, 30, outline=col), x, 540, t, tt, side=0)
        spr = Image.new("RGBA", (520, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(spr); d.text((260, 60), title, font=F(38, "b"), fill=col + (255,), anchor="mm")
        for j, r in enumerate(rows):
            rt = rts[j]
            if t >= rt: a = fade(t, rt); d.rounded_rectangle([30, 120 + 120 * j, 490, 120 + 120 * j + 90], 18, fill=(24, 30, 42, int(255 * a)), outline=col + (int(255 * a),), width=2); d.text((260, 165 + 120 * j), r, font=F(30, "p"), fill=WHITE + (int(255 * a),), anchor="mm")
        enter(base, spr, x, 540, t, tt)


def b_private_a(base, t, b):
    sid = "private"; o = b["t0"]
    t_two = T(sid, 11); t_new = T(sid, 15); t_plus = T(sid, 18) + 0.05; t_msg = T(sid, 21); t_mem = T(sid, 26); t_off = T(sid, 27) + 0.1; t_later = T(sid, 30)
    c = card(1300, 560, 30); enter(base, c, 960, 560, t, o, dur=0.3)
    if t >= t_two: place(base, pill("2 ways to keep a chat private", 34, SKY, INK, pad=(30, 9), kind="b"), W / 2, 150, 1.0, fade(t, t_two))
    if t >= t_new: place(base, pill("New chat", 30, (30, 44, 62), WHITE, pad=(24, 8), kind="b", outline=SKY), 410, 330, 1.0, fade(t, t_new - 0.1))
    place(base, pill("Message Claude...", 32, (26, 31, 45), DIM, pad=(40, 14), outline=OUT, kind="p"), 1120, 760, 1.0, fade(t, o))
    place(base, pill("+", 46, (36, 44, 62), SKY, pad=(26, 4), outline=(SKY if t >= t_plus - 0.2 else OUT), kind="b"), 480, 760)
    if t >= t_plus:
        pp = ease_out((t - t_plus) / 0.3); m = card(520, 190, 22, fill=(24, 30, 44), outline=SKY); md = ImageDraw.Draw(m); md.text((50, 50), "Add files or photos", font=F(30, "p"), fill=DIM + (255,)); md.text((50, 112), "Memory", font=F(34, "b"), fill=WHITE + (255,))
        toggle(md, 400, 112, t < t_off, 90, 46); place(base, m, 700, 600, 0.85 + 0.15 * pp, min(1, pp * 1.5))
    if t >= t_msg: place(base, pill("BEFORE the first message", 30, (30, 44, 62), SKY, pad=(24, 8), kind="p", outline=SKY), 1250, 440, 1.0, fade(t, t_msg))
    if t >= t_off: place(base, pill("Memory OFF for this chat", 30, SKY, INK, pad=(24, 8), kind="b"), 1250, 510, 1.0, fade(t, t_off))
    if t >= t_later: place(base, pill("cannot be changed later", 28, (70, 28, 36), RED, pad=(22, 7), kind="p", outline=RED), 1250, 580, 1.0, fade(t, t_later))
    pts = sorted([(o, 1500, 300), (t_new, 1500, 300), (t_plus - 0.6, 760, 560), (t_plus, 485, 770), (t_mem - 0.5, 485, 770), (t_off - 0.1, 885, 640)])
    cursor_path(base, t, pts, clicks=(t_plus, t_off)); illu(base)


def b_private_b(base, t, b):
    sid = "private"; o = b["t0"]; t_click = T(sid, 42); t_m = T(sid, 48); t_h = T(sid, 53)
    place(base, pill("2   INCOGNITO CHAT", 34, SKY, INK, pad=(30, 9), kind="b"), W / 2, 150, 1.0, fade(t, o))
    c = card(1300, 560, 30); enter(base, c, 960, 560, t, o, dur=0.3)
    gx, gy = 1560, 330; d = ImageDraw.Draw(base)
    d.ellipse([gx - 40, gy - 40, gx + 40, gy + 40], outline=SKY + (255,), width=4); d.pieslice([gx - 18, gy - 24, gx + 18, gy + 12], 180, 360, fill=SKY + (255,)); d.rectangle([gx - 18, gy - 6, gx + 18, gy + 22], fill=SKY + (255,))
    for i in range(3): d.ellipse([gx - 18 + 12 * i, gy + 14, gx - 6 + 12 * i, gy + 28], fill=SKY + (255,))
    d.ellipse([gx - 9, gy - 10, gx - 3, gy - 2], fill=INK + (255,)); d.ellipse([gx + 3, gy - 10, gx + 9, gy - 2], fill=INK + (255,))
    if 0 <= (t - t_click) <= 0.45: rr = int(20 + 50 * (t - t_click) / 0.45); d.ellipse([gx - rr, gy - rr, gx + rr, gy + rr], outline=SKY + (255,), width=4)
    if t >= T(sid, 37): place(base, pill("ghost icon, top right", 28, (20, 24, 34), DIM, pad=(20, 6), kind="p", outline=OUT), 1380, 410, 1.0, fade(t, T(sid, 37)))
    for i, (s, tt) in enumerate([("not saved to memory", t_m), ("not saved to chat history", t_h)]):
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 34, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=SKY, hl=("not",), hlc=SKY), 960, 540 + 100 * i, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    cursor_path(base, t, [(o, 1200, 800), (t_click - 0.9, 1200, 800), (t_click, gx, gy)], clicks=(t_click,)); illu(base)


def b_projects(base, t, b):
    sid = "projects"; o = b["t0"]; t_b = T(sid, 23); t_sw = T(sid, 35); t_off = T(sid, 38) + 0.2
    enter(base, card(900, 120, 28, outline=SKY, glow=True), 960, 250, t, T(sid, 17) - 0.3, side=0)
    if t >= T(sid, 17) - 0.3: txt(base, (960, 250), "your normal account memory", 34, SKY, "b", "mm", fade(t, T(sid, 17) - 0.2))
    for i, (n, col, tt) in enumerate([("PROJECT A", SKY, T(sid, 1)), ("PROJECT B", AMB, T(sid, 3) + 0.5)]):
        x = 520 + 880 * i; enter(base, card(560, 300, 28, outline=col), x, 560, t, tt, side=0)
        spr = Image.new("RGBA", (560, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(spr); d.text((280, 60), n, font=F(40, "b"), fill=col + (255,), anchor="mm"); d.rounded_rectangle([60, 120, 500, 220], 18, fill=(26, 32, 46, 255), outline=col + (255,), width=2); d.text((280, 170), "its own memory", font=F(30, "p"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, x, 560, t, tt)
    dd = ImageDraw.Draw(base)
    if t >= T(sid, 15): dd.line([(520, 310), (520, 410)], fill=SKY + (255,), width=4)
    if t >= t_b: dd.line([(1400, 310), (1400, 410)], fill=RED + (255,), width=4); place(base, pill("X  never project B", 28, (70, 28, 36), RED, pad=(22, 7), kind="p", outline=RED), 1400, 330, 1.0, fade(t, t_b))
    if t >= T(sid, 15): place(base, pill("A uses A + account memory", 30, (20, 24, 34), WHITE, pad=(26, 9), kind="p", outline=OUT), 1340, 800, 1.0, fade(t, T(sid, 15)))
    if t >= t_sw:
        pp = pop(t, t_sw); sw = card(560, 110, 26, fill=(24, 30, 44), outline=SKY); d = ImageDraw.Draw(sw); d.text((50, 30), "Use account memory", font=F(32, "b"), fill=WHITE + (255,)); toggle(d, 420, 28, t < t_off, 90, 46); place(base, sw, 520, 800, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    if t >= t_off: step(base, t, t_off, "OFF = this project is fully separate", y=150)


def b_caution_a(base, t, b):
    sid = "caution"; o = b["t0"]; t_del = T(sid, 10); t_mem = T(sid, 16)
    enter(base, photo("trash", 700, 470, t - o, b["t1"] - o + 3), 560, 500, t, o, side=-1)
    c = card(780, 470, 28); enter(base, c, 1360, 500, t, o + 0.2, side=1)
    if t >= T(sid, 8): place(base, pill("Chat: Trip plan", 32, (26, 31, 45), WHITE, pad=(26, 10), kind="p", outline=OUT), 1360, 400, 1.0, fade(t, T(sid, 8)))
    if t >= t_del:
        a = fade(t, t_del, 0.3); ImageDraw.Draw(base).line([(1170, 400), (1550, 400)], fill=RED + (int(255 * a),), width=6)
        place(base, pill("chat deleted", 26, RED, INK, pad=(18, 5), kind="b"), 1630, 355, 1.0, a, 5)
    if t >= t_mem: pp = pop(t, t_mem); place(base, pill("memory from it: still there", 34, (30, 44, 62), SKY, pad=(28, 10), kind="b", outline=SKY), 1360, 580, 0.7 + 0.3 * pp, min(1, pp * 1.4))


ART = Image.open(HERE / "raw/article_plain.png").convert("RGB"); RJ = json.load(open(HERE / "raw/rects.json"))
def note(hp, w=1300, h=420):
    rx, ry, rw, rh = RJ["rects"]["delete"]; s = (w - 80) / ART.width; a = ART.resize((int(ART.width * s), int(ART.height * s)), Image.LANCZOS)
    lines = RJ.get("lines", {}).get("delete") or []
    if lines and hp > 0:
        tot = sum(l[2] for l in lines); done = 0.0; layer = Image.new("RGB", a.size, (255, 255, 255)); d = ImageDraw.Draw(layer)
        for x, y, lw, lh in lines:
            f0 = done / tot; f1 = (done + lw) / tot; done += lw; q = min(1, max(0, (hp - f0) / (f1 - f0)))
            if q > 0: d.rounded_rectangle([x * 2 * s - 4, y * 2 * s - 2, (x + lw * q) * 2 * s + 4, (y + lh) * 2 * s + 2], 5, fill=(91, 200, 255))
        a = ImageChops.multiply(a, layer)
    cy = (ry + rh / 2) * 2 * s; y0 = int(max(0, min(a.height - (h - 70), cy - (h - 70) * 0.5))); pg = a.crop((0, y0, w - 80, y0 + h - 70)).convert("RGBA")
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(sh); d.rounded_rectangle([0, 0, w - 1, h - 1], 16, fill=(255, 255, 255, 255), outline=(200, 204, 214, 255), width=3); sh.alpha_composite(pg, (40, 36))
    return sh


def b_caution_b(base, t, b):
    sid = "caution"; o = b["t0"]; hp = min(1, max(0, (t - T(sid, 19)) / max(0.3, T(sid, 28) - T(sid, 19))))
    enter(base, note(hp), 960, 470, t, o, side=0)
    place(base, pill("Official page: support.claude.com  /  Claude's chat search and memory", 26, (20, 24, 34), (200, 208, 224), pad=(22, 6), kind="p", outline=OUT), 960, 740, 1.0, fade(t, o + 0.3))
    t1 = T(sid, 22)
    if t >= t1: pp = pop(t, t1); place(base, pill("delete the memory separately", 36, SKY, INK, pad=(30, 10), kind="b"), 960, 830, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    t2 = T(sid, 33)
    if t >= t2: pp = pop(t, t2); place(base, pill("memory is part of data exports", 30, (30, 44, 62), WHITE, pad=(26, 9), kind="p", outline=SKY), 960, 900, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_cta_a(base, t, b):
    sid = "cta"
    place(base, pill("3 THINGS TO REMEMBER", 52, (20, 24, 34), WHITE, pad=(50, 14), kind="b", outline=SKY, glow=True), W / 2, 230, 1.0, fade(t, T(sid, 3) - 0.2, 0.2))
    for i, (n, s, tt) in enumerate([("1", "Settings > Your Claude: the toggle", T(sid, 5)), ("2", "Manage: see, edit, delete topics", T(sid, 13)), ("3", "Incognito chat for private things", T(sid, 23))]):
        y = 430 + 150 * i; enter(base, card(1100, 110, 26), 960, y, t, tt - 0.2, side=0)
        spr = Image.new("RGBA", (1100, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(spr); d.rounded_rectangle([24, 22, 90, 88], 14, fill=SKY + (255,)); d.text((57, 55), n, font=F(40, "b"), fill=INK + (255,), anchor="mm"); d.text((130, 55), s, font=F(38, "p"), fill=WHITE + (255,), anchor="lm"); enter(base, spr, 960, y, t, tt - 0.2)


def b_cta_b(base, t, b):
    sid = "cta"; t1, t2, t3 = T(sid, 35), T(sid, 37), T(sid, 40)
    if t >= t1: place(base, pill("Comment", 60, (20, 24, 34), WHITE, pad=(40, 12), kind="b", outline=OUT), 960, 300, 0.8 + 0.2 * pop(t, t1), min(1, fade(t, t1, 0.2)))
    if t >= t2: place(base, pill("MEMORY", 120, SKY, INK, pad=(60, 14), kind="b", glow=True), 960, 450, 0.8 + 0.2 * pop(t, t2), min(1, fade(t, t2, 0.2)))
    if t >= t3: place(base, pill("Follow DevRoboLab", 54, (20, 24, 34), SKY, pad=(40, 12), kind="b", outline=OUT), 960, 600, 0.8 + 0.2 * pop(t, t3), min(1, fade(t, t3, 0.2)))
    tt = t3 + 0.9
    if t >= tt:
        for i, s in enumerate(["Watch next", "Subscribe"]):
            enter(base, card(640, 150, 28, glow=True), 560 + 800 * i, 830, t, tt + 0.3 * i, side=0)
            spr = Image.new("RGBA", (640, 150), (0, 0, 0, 0)); ImageDraw.Draw(spr).text((320, 75), s, font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 560 + 800 * i, 830, t, tt + 0.3 * i)


FN = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}
def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = BG.copy()
    FN[b["id"]](base, t, b); badge(base, b["sid"], t); caption(base, t)
    return np.array(base.convert("RGB"))


SR = 24000
def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def encode(frames_iter, n_frames, voice_wav, music, out, music_start=6, music_gain_db=-22):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice_wav), "-ss", str(music_start), "-i", str(music)]
    fc = f"[2:a]volume={music_gain_db}dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, fr in enumerate(frames_iter):
        p.stdin.write(fr.tobytes())
        if i % 300 == 0: print(f"  frame {i}/{n_frames}", flush=True)
    p.stdin.close(); p.wait()


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['id'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/L_{tt:06.1f}.png")
        return
    build_audio(HERE / "audio/voice_long.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_long.wav", ROOT / deck["music"]["file"], HERE / "output/long.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
