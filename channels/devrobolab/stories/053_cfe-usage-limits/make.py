"""053 Claude Feature 07 (Usage limits) Short. Light sketch look (lavender paper), accent INDIGO, Roman Hinglish captions, real official-page crops.
Run: python make.py frames t1 t2 ...  |  python make.py   (render)  |  python make.py range t0 t1 out.mp4"""
import json, math, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import W, H, FPS, ease_out, ease_back, ease_io, wav_dur, encode

LEAD, AFTER = 0.05, 0.05
FONT = str(ROOT / "shared/fonts/Poppins-Bold.ttf")
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START))
TEAL = (79, 70, 229); TEALL = (196, 192, 255); INKD = (30, 30, 36); OR = (217, 119, 87); GREEN = (22, 163, 74); RED = (225, 45, 57)
PEACH = (255, 228, 210); SKY = (208, 232, 250)
GREY = (90, 90, 96)


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]


PF = lambda sz, bold=False: ImageFont.truetype(str(ROOT / ("shared/fonts/Poppins-Bold.ttf" if bold else "shared/fonts/Poppins-Medium.ttf")), sz)


def chip(text, size, fill, color=(255, 255, 255), pad=(34, 14), r=26, hl=None, hlcolor=TEALL):
    f = font(size); words = text.split(" "); sp = f.getlength(" ")
    wl = [f.getlength(w) for w in words]; tw = int(sum(wl) + sp * (len(words) - 1)); asc, desc = f.getmetrics()
    im = Image.new("RGBA", (tw + 2 * pad[0], asc + desc + 2 * pad[1]), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=fill + (255,)); x = pad[0]
    for w, l in zip(words, wl):
        d.text((x, pad[1]), w, font=f, fill=(hlcolor if hl and w.strip(",.?!") in hl else color) + (255,)); x += l + sp
    return im


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def pop(t, t0, dur=0.28): return ease_back((t - t0) / dur) if t >= t0 else 0.0


def scaled(spr, p):
    p = max(0.01, min(1, p)); return spr.resize((max(1, int(spr.width * p)), max(1, int(spr.height * p))))


def shadow(w, h, r=40, off=34, blur=26, a=105):
    sh = Image.new("RGBA", (w + 160, h + 160), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([80, 80 + off, 80 + w, 80 + h + off], r, fill=(0, 0, 0, a))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def card_enter(base, spr, cx, cy, t, t0, rot=0.0, side=0, dur=0.38):
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur))
    dx = side * (1 - q) * 520; dy = (1 - q) * (140 if side == 0 else 0); sc = 0.9 + 0.1 * e; w, h = spr.size
    place(base, shadow(w, h), cx + dx, cy + dy, sc, min(1, q * 1.5), rot); place(base, spr, cx + dx, cy + dy, sc, min(1, q * 1.5), rot)


MASC = {k: Image.open(ROOT / f"channels/devrobolab/mascot/cut/{k}.png").convert("RGBA") for k in ("wave",)}
def robot(name, h): m = MASC[name]; return m.resize((int(m.width * h / m.height), h), Image.LANCZOS)


def cursor_spr():
    im = Image.new("RGBA", (70, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(im); pts = [(6, 4), (6, 62), (22, 48), (34, 76), (46, 70), (34, 44), (56, 44)]
    d.polygon([(x + 3, y + 3) for x, y in pts], fill=(0, 0, 0, 90)); d.polygon(pts, fill=(255, 255, 255, 255), outline=(10, 10, 10, 255)); return im
CUR = cursor_spr()


def bg_paper():
    im = Image.new("RGB", (W, H), (246, 245, 255)); d = ImageDraw.Draw(im)
    for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(228, 226, 246), width=2)
    for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(228, 226, 246), width=1)
    return im.convert("RGBA")
BGP = bg_paper()


def sk_card(w, h, fill, r=34, off=9):
    im = Image.new("RGBA", (w + off + 4, h + off + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([off, off, w + off, h + off], r, fill=INKD + (255,)); d.rounded_rectangle([0, 0, w, h], r, fill=fill + (255,), outline=INKD + (255,), width=5)
    return im


def tape(im, x, y, rot=-6):
    t = Image.new("RGBA", (130, 44), (255, 214, 10, 200)); im.alpha_composite(t.rotate(rot, expand=True), (x, y))


def tick(d, x, y, s, col=GREEN):
    d.ellipse([x, y, x + s, y + s], fill=col + (255,)); d.line([(x + 0.25 * s, y + 0.52 * s), (x + 0.43 * s, y + 0.7 * s), (x + 0.76 * s, y + 0.3 * s)], fill=(255, 255, 255, 255), width=max(4, int(s * 0.13)))


def cross(d, x, y, s, col=RED):
    d.ellipse([x, y, x + s, y + s], fill=col + (255,)); w = max(4, int(s * 0.13))
    d.line([(x + 0.3 * s, y + 0.3 * s), (x + 0.7 * s, y + 0.7 * s)], fill=(255, 255, 255, 255), width=w); d.line([(x + 0.7 * s, y + 0.3 * s), (x + 0.3 * s, y + 0.7 * s)], fill=(255, 255, 255, 255), width=w)


def bars(d, cx, cy, n, gap, hmax, t, col, act=1.0, w=14):
    for i in range(n):
        h = max(8, hmax * (0.25 + 0.75 * abs(math.sin(t * 7 + i * 0.95))) * act); x = cx + (i - (n - 1) / 2) * gap
        d.rounded_rectangle([x - w / 2, cy - h / 2, x + w / 2, cy + h / 2], w // 2, fill=col + (255,))


def mic(d, cx, cy, s, col=INKD):
    lw = max(4, int(0.07 * s))
    d.rounded_rectangle([cx - 0.22 * s, cy - 0.5 * s, cx + 0.22 * s, cy + 0.12 * s], int(0.22 * s), fill=col + (255,))
    d.arc([cx - 0.4 * s, cy - 0.3 * s, cx + 0.4 * s, cy + 0.36 * s], 0, 180, fill=col + (255,), width=lw)
    d.line([(cx, cy + 0.36 * s), (cx, cy + 0.56 * s)], fill=col + (255,), width=lw); d.line([(cx - 0.2 * s, cy + 0.56 * s), (cx + 0.2 * s, cy + 0.56 * s)], fill=col + (255,), width=lw)


def keyboard(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], 18, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    for r in range(3):
        for c in range(8):
            kx = x + 22 + c * (w - 44) / 8; ky = y + 22 + r * (h - 44) / 3
            d.rounded_rectangle([kx, ky, kx + (w - 44) / 8 - 8, ky + (h - 44) / 3 - 10], 6, fill=(225, 230, 232, 255))


# ---- caption: Roman Hinglish, one strip, whole phrase, UPPERCASE words in accent ----
CAPTXT = {
    "hook": [(0, "Claude par limit aa gayi?"), (5, "Samjho USAGE LIMIT")],
    "session": [(0, "Paid plans: SESSION limit"), (7, "Har 5 ghante me RESET"), (14, "Pehla message = CLOCK ON")],
    "weekly": [(0, "Upar se WEEKLY limit bhi"), (7, "claude.ai, Code, Desktop"), (13, "Sab ek hi limit me")],
    "tips": [(0, "Usage bachana hai?"), (3, "THINKING / EFFORT kam"), (8, "WEB SEARCH, apps band"), (18, "Lambi chat? NAYI chat")],
    "check": [(0, "Apna usage dekhna hai?"), (5, "Settings > USAGE"), (9, "Bacha time + WEEKLY reset")],
    "cta": [(0, "Kaam ki lagi?"), (3, "DevRoboLab ko FOLLOW karo"), (8, "Roz naya tip")],
}
CAPS = []
for sid in IDS:
    items = CAPTXT[sid]; end = SC[sid] + D[IDS.index(sid)]
    for j, (k, txt) in enumerate(items): CAPS.append((T(sid, k) - 0.04, (T(sid, items[j + 1][0]) - 0.04) if j + 1 < len(items) else end, txt))
_capc = {}
def caption(base, t):
    for a, b, txt in CAPS:
        if a <= t < b:
            if txt not in _capc: _capc[txt] = chip(txt, 50, (28, 28, 34), (255, 255, 255), pad=(32, 12), r=28, hl={w.strip(",.?!") for w in txt.split() if w.isupper() and len(w) > 2})
            place(base, _capc[txt], 540, 1500, 0.94 + 0.06 * ease_out((t - a) / 0.12)); return


def banner(base, t, items, y=300):
    for txt, ts, te in items:
        if ts <= t < te: pp = pop(t, ts + 0.03); place(base, chip(txt, 46, TEAL, (255, 255, 255), pad=(30, 9), r=26), 540, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---- official-page crops (own Playwright capture, key phrase marked yellow) ----
def load(n): return Image.open(HERE / f"raw/shot_{n}.png").convert("RGB")
def crop_w(img, box, w):
    c = img.crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)
def with_border(img, r=20):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=5); return o
SS, SK, ST = load("session"), load("check"), load("tips")
C_SESSION = with_border(crop_w(SS, (640, 880, 1740, 1030), 1000))
C_SURF = with_border(crop_w(SS, (640, 1290, 1740, 1395), 1000))
C_WEEKLY = with_border(crop_w(SK, (640, 1225, 1740, 1400), 1000))
C_TIPS = with_border(crop_w(ST, (690, 965, 1790, 1115), 1000))
C_CHECK = with_border(crop_w(SK, (1000, 950, 2100, 1035), 1000))
def src_tag(base, y): place(base, chip("Official page: support.claude.com", 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, y)
def illus(base, y=1595): place(base, chip("Illustration (own drawing)", 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, y)


def meter(d, x, y, w, h, p, col):
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=(228, 232, 233, 255), outline=INKD + (255,), width=4)
    if p > 0.02: d.rounded_rectangle([x + 4, y + 4, x + 4 + int((w - 8) * p), y + h - 4], (h - 8) // 2, fill=col + (255,))


# ---- scenes ----
def s_hook(base, t, b):
    base.alpha_composite(BGP)
    card = sk_card(940, 900, (255, 255, 255)); d = ImageDraw.Draw(card); tape(card, 60, -14, -5); tape(card, 760, -14, 5)
    d.text((60, 40), "Claude chat", font=PF(70, True), fill=INKD + (255,))
    for i, (y, txt) in enumerate(((170, "Message 1"), (290, "Message 2"), (410, "Message 3"))):
        ts = 0.2 + 0.5 * i
        if t >= ts:
            pp = ease_back((t - ts) / 0.28); sub = Image.new("RGBA", (360, 96), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub)
            sd.rounded_rectangle([0, 0, 359, 95], 28, fill=(SKY if i % 2 == 0 else TEALL) + (255,), outline=INKD + (255,), width=5); sd.text((28, 24), txt, font=PF(38, True), fill=INKD + (255,))
            card.alpha_composite(scaled(sub, pp), (60 + 480 * (i % 2), y))
    fillp = ease_io(min(1, max(0, (t - 0.4) / max(0.5, T("hook", 2) - 0.4))))
    meter(d, 60, 600, 820, 90, fillp, RED if fillp > 0.97 else TEAL)
    d.text((60, 710), "usage", font=PF(40), fill=GREY + (255,))
    if t >= T("hook", 2) + 0.2:
        pp = ease_back((t - T("hook", 2) - 0.2) / 0.3); sub = chip("LIMIT REACHED", 60, RED, (255, 255, 255), pad=(36, 12), r=30)
        card.alpha_composite(scaled(sub, pp), (110, 770))
    card_enter(base, card, 540, 800, t, b["t0"], rot=-0.8, dur=0.01)
    if t >= T("hook", 8): pp = pop(t, T("hook", 8)); place(base, chip("USAGE LIMIT", 84, TEAL, (255, 255, 255), pad=(44, 12), r=34), 540, 1350, 0.7 + 0.3 * pp, min(1, pp * 1.4), -1.5)


def clock(d, cx, cy, r, p, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255), outline=INKD + (255,), width=6)
    if p > 0.005: d.pieslice([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], -90, -90 + 360 * p, fill=col + (255,))
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=INKD + (255,))


def s_session(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("PAID PLANS", b["t0"], T("session", 8)), ("EVERY 5 HOURS", T("session", 8), T("session", 14)), ("STARTS AT 1ST MESSAGE", T("session", 14), b["t1"])])
    card_enter(base, C_SESSION, 540, 540, t, b["t0"] + 0.05, rot=0.0, dur=0.3)
    if t >= b["t0"] + 0.4: src_tag(base, 640)
    c = sk_card(940, 640, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 70, -14, -5)
    start = T("session", 14)
    if t >= start: pp = ease_back((t - start) / 0.3); sub = chip("Message 1", 44, SKY, INKD, pad=(30, 12), r=26); c.alpha_composite(scaled(sub, pp), (50, 70))
    p = 0.0 if t < start else min(1, (t - start) / max(1.0, b["t1"] - start - 0.6))
    clock(d, 640, 330, 210, p, TEAL)
    d.text((50, 190), "5 HOURS", font=PF(58, True), fill=INKD + (255,)); d.text((50, 270), "then full reset", font=PF(36), fill=GREY + (255,))
    if p >= 0.97: pp = ease_back((p - 0.97) / 0.03); sub = chip("RESET", 50, GREEN, (255, 255, 255), pad=(30, 8), r=24); c.alpha_composite(scaled(sub, pp), (50, 460))
    card_enter(base, c, 540, 1110, t, b["t0"] + 0.9, rot=0.7, side=1)
    illus(base)


def s_weekly(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("+ WEEKLY LIMIT", b["t0"], T("weekly", 7)), ("ALL APPS, SAME LIMIT", T("weekly", 7), b["t1"])])
    card_enter(base, C_WEEKLY, 540, 480, t, b["t0"] + 0.05, rot=-0.5, dur=0.3)
    if t >= b["t0"] + 0.4: src_tag(base, 620)
    cal = sk_card(940, 220, (255, 255, 255)); cd = ImageDraw.Draw(cal)
    for i, dn in enumerate(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")):
        hot = dn == "Fri"; cd.rounded_rectangle([30 + 128 * i, 40, 140 + 128 * i, 150], 18, fill=(RED if hot else (240, 242, 243)) + (255,), outline=INKD + (255,), width=4)
        cd.text((30 + 128 * i + 55, 95), dn, font=PF(30, True), fill=((255, 255, 255) if hot else INKD) + (255,), anchor="mm")
    cd.text((470, 185), "weekly reset: same day + time every week", font=PF(28), fill=GREY + (255,), anchor="mm")
    card_enter(base, cal, 540, 790, t, T("weekly", 2) - 0.1, rot=0.5, side=1)
    if t >= T("weekly", 7) - 0.1:
        card_enter(base, C_SURF, 540, 990, t, T("weekly", 7) - 0.1, rot=0.4, side=1)
    c = sk_card(940, 320, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 700, -14, 5)
    for i, (txt, col, ts) in enumerate((("claude.ai", SKY, T("weekly", 8)), ("Claude Code", PEACH, T("weekly", 9)), ("Desktop", TEALL, T("weekly", 12)))):
        if t >= ts: pp = ease_back((t - ts) / 0.3); c.alpha_composite(scaled(chip(txt, 40, col, INKD, pad=(24, 14), r=24), pp), (40 + 300 * i, 40 + 30 * (i % 2)))
    if t >= T("weekly", 13):
        pp = min(1, (t - T("weekly", 13)) / 0.5); meter(d, 60, 160, 820, 80, 0.72 * ease_out(pp), TEAL); d.text((60, 250), "ONE shared limit", font=PF(52, True), fill=INKD + (255,))
    card_enter(base, c, 540, 1270, t, T("weekly", 7) + 0.1, rot=0.6, side=-1)
    illus(base)


def row(txt):
    sub = Image.new("RGBA", (860, 100), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub); sd.rounded_rectangle([0, 0, 859, 99], 26, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    sd.text((130, 24), txt, font=PF(40, True), fill=INKD + (255,)); tick(sd, 24, 18, 64); return sub


def s_tips(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("SAVE USAGE: 3 TIPS", b["t0"], b["t1"])])
    card_enter(base, C_TIPS, 540, 520, t, b["t0"] + 0.05, rot=0.0, dur=0.3)
    if t >= b["t0"] + 0.4: src_tag(base, 610)
    for i, (txt, ts) in enumerate((("Thinking / effort kam", T("tips", 3)), ("Web search + apps band", T("tips", 8)), ("Lambi chat? Nayi chat", T("tips", 18)))):
        if t >= ts:
            pp = ease_back((t - ts) / 0.32); place(base, row(txt), 540 + (1 - min(1, pp)) * 400, 900 + 210 * i, 0.9 + 0.1 * min(1, pp), min(1, pp * 1.4))
    illus(base)


def s_check(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("CHECK YOUR USAGE", b["t0"], b["t1"])])
    card_enter(base, C_CHECK, 540, 520, t, b["t0"] + 0.05, rot=0.0, dur=0.3)
    if t >= b["t0"] + 0.4: src_tag(base, 580)
    c = sk_card(940, 620, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 70, -14, -5)
    d.text((50, 30), "Settings  >  Usage", font=PF(58, True), fill=INKD + (255,))
    pp = min(1, max(0, (t - T("check", 9)) / 0.5)); d.text((50, 150), "Current session", font=PF(38), fill=GREY + (255,)); meter(d, 50, 210, 840, 70, 0.45 * ease_out(pp), TEAL)
    if pp > 0: d.text((50, 300), "3 hr 10 min left", font=PF(44, True), fill=INKD + (255,))
    pp = min(1, max(0, (t - T("check", 14)) / 0.5)); d.text((50, 400), "Weekly limits", font=PF(38), fill=GREY + (255,)); meter(d, 50, 460, 840, 70, 0.3 * ease_out(pp), OR)
    if pp > 0: d.text((50, 545), "Next reset: Fri", font=PF(40, True), fill=INKD + (255,))
    card_enter(base, c, 540, 1000, t, b["t0"] + 0.6, rot=0.6, side=1)
    illus(base)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, robot("wave", 760), 540, 700 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill) in enumerate((("+ FOLLOW", T("cta", 3), TEAL), ("DAILY NEW TIP", T("cta", 7), INKD))):
        pp = pop(t, ts); place(base, chip(txt, 70 if n == 0 else 52, fill, (255, 255, 255), pad=(44, 10), r=30), 540, 1180 + 125 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("session", 0)), dict(k="session", t0=T("session", 0), t1=T("weekly", 0)), dict(k="weekly", t0=T("weekly", 0), t1=T("tips", 0)),
     dict(k="tips", t0=T("tips", 0), t1=T("check", 0)), dict(k="check", t0=T("check", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, session=s_session, weekly=s_weekly, tips=s_tips, check=s_check, cta=s_cta)
SR = 24000


def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = Image.new("RGBA", (W, H)); FN[b["k"]](base, t, b); caption(base, t)
    return np.array(base.convert("RGB"))


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['k'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/d_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()

