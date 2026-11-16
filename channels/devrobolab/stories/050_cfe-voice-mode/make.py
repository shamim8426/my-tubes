"""050 Claude Feature 06 (Voice mode) Short. Light sketch look (mint paper), accent TEAL, Roman Hinglish captions, real official-page crops.
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
TEAL = (0, 150, 136); TEALL = (150, 236, 222); INKD = (30, 30, 36); OR = (217, 119, 87); GREEN = (22, 163, 74); RED = (225, 45, 57)
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
    im = Image.new("RGB", (W, H), (244, 251, 247)); d = ImageDraw.Draw(im)
    for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(224, 240, 233), width=2)
    for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(224, 240, 233), width=1)
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
    "hook": [(0, "Typing nahi karni?"), (3, "Claude se bol kar baat karo!"), (8, "Ye hai VOICE MODE")],
    "start": [(0, "Chat box me SOUND WAVE icon"), (6, "par click karo"), (9, "Ek voice chuno"), (12, "Aur bolna shuru karo"), (16, "Phone me icon mic ke paas hai")],
    "modes": [(0, "HANDS-FREE me ruko,"), (3, "Claude jawab deta hai"), (9, "Shor wali jagah?"), (14, "PUSH-TO-TALK button dabao, bolo")],
    "extra": [(0, "TEXT aur VOICE ek hi chat me"), (10, "Baat aage chalti hai"), (14, "LANGUAGE Settings se chuno"), (18, "Dusri languages BETA me")],
    "caution": [(0, "Dhyan rakho!"), (2, "Voice bhi USAGE LIMIT me ginti hai"), (12, "AUDIO save nahi hota,"), (16, "TRANSCRIPT chat me rehta hai")],
    "cta": [(0, "Voice mode try kiya?"), (4, "DevRoboLab ko FOLLOW karo"), (8, "Kal naya feature")],
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


# ---- official-page crops (own Playwright capture) ----
SL = Image.open(HERE / "raw/shot_limits.png").convert("RGB")
def crop_w(img, box, w):
    c = img.crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)
UI_BAR = crop_w(SL, (696, 124, 1768, 462), 940)          # input box: plus, settings, mic, white sound-wave button
NOTE = crop_w(SL, (648, 944, 1768, 1112), 900)           # 'Voice conversations count toward your regular usage limits'
def with_border(img, r=20):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=5); return o


# ---- scenes ----
def s_hook(base, t, b):
    base.alpha_composite(BGP)
    card = sk_card(940, 1000, (255, 255, 255)); d = ImageDraw.Draw(card); tape(card, 60, -14, -5); tape(card, 760, -14, 5)
    d.text((60, 40), "Talk to Claude", font=PF(76, True), fill=INKD + (255,))
    if t >= 0.25:
        kp = ease_back((t - 0.25) / 0.3); sub = Image.new("RGBA", (400, 220), (0, 0, 0, 0)); keyboard(ImageDraw.Draw(sub), 10, 20, 380, 180)
        card.alpha_composite(scaled(sub, kp), (60, 190))
        if t >= T("hook", 1) + 0.3: cp = ease_back((t - T("hook", 1) - 0.3) / 0.28); cross(d, 190, 260, int(150 * min(1, cp)))
    if t >= T("hook", 3):
        mp = ease_back((t - T("hook", 3)) / 0.35); r = int(210 * min(1, mp)); cx, cy = 470, 700
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL + (255,), outline=INKD + (255,), width=6)
        if mp > 0.7: mic(d, cx, cy - 10, 220, (255, 255, 255))
    if t >= T("hook", 5):
        act = min(1, (t - T("hook", 5)) / 0.4); bars(d, 800, 700, 3, 44, 240, t, TEAL, act, 22); bars(d, 140, 700, 3, 44, 240, t + 1.3, TEAL, act, 22)
    card_enter(base, card, 540, 800, t, b["t0"], rot=-0.8, dur=0.01)
    if t >= T("hook", 10): pp = pop(t, T("hook", 10)); place(base, chip("VOICE MODE", 84, TEAL, (255, 255, 255), pad=(44, 12), r=34), 540, 1290, 0.7 + 0.3 * pp, min(1, pp * 1.4), -1.5)


def phone(t, S):
    w, h = 520, 700; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 46, fill=(18, 18, 18, 255), outline=(70, 70, 70, 255), width=4)
    if t < S["picker"]:
        d.text((60, 120), "Hi, how can I help?", font=PF(40, True), fill=(150, 150, 150, 255))
        d.rounded_rectangle([30, 560, w - 30, 670], 36, fill=(40, 40, 40, 255)); d.text((60, 592), "Reply to Claude", font=PF(32), fill=(150, 150, 150, 255))
        mic(d, w - 190, 615, 56, (225, 225, 225)); d.ellipse([w - 130, 575, w - 56, 649], fill=(255, 255, 255, 255)); bars(d, w - 93, 612, 5, 13, 38, 0.7, INKD, 1.0, 6)
    elif t < S["listen"]:
        d.text((60, 50), "Choose a voice", font=PF(40, True), fill=(240, 240, 240, 255))
        for k, nm in enumerate(("Voice 1", "Voice 2", "Voice 3")):
            sel = t >= S["pick"] and k == 1; y = 150 + 130 * k
            d.rounded_rectangle([40, y, w - 40, y + 104], 26, fill=OR + (255,) if sel else (36, 36, 36, 255)); d.text((80, y + 28), nm, font=PF(38, True), fill=(17, 17, 17, 255) if sel else (230, 230, 230, 255))
            d.ellipse([w - 120, y + 30, w - 72, y + 78], outline=(17, 17, 17, 255) if sel else (110, 110, 110, 255), width=5)
    else:
        lp = ease_out(min(1, (t - S["listen"]) / 0.4)); pr = (150 + 12 * math.sin(t * 5)) * lp
        d.ellipse([w / 2 - pr, 270 - pr, w / 2 + pr, 270 + pr], fill=(60, 40, 32, 255), outline=OR + (255,), width=5)
        bars(d, w / 2, 270, 7, 34, 150, t, OR, lp, 16); d.text((w / 2 - 110, 470), "Listening...", font=PF(40, True), fill=(240, 240, 240, 255))
        d.rounded_rectangle([60, 570, w - 60, 650], 30, fill=(32, 32, 32, 255)); d.text((w / 2 - 80, 590), "Speak now", font=PF(32), fill=(140, 140, 140, 255))
    return im


def s_start(base, t, b):
    base.alpha_composite(BGP)
    S = dict(picker=T("start", 8), pick=T("start", 11) - 0.1, listen=T("start", 13) + 0.1)
    banner(base, t, [("STEP 1  TAP SOUND WAVE", b["t0"], T("start", 9)), ("STEP 2  PICK A VOICE", T("start", 9), T("start", 12)), ("STEP 3  START TALKING", T("start", 12), T("start", 16)), ("ON PHONE  NEXT TO MIC", T("start", 16), b["t1"])])
    bar = with_border(UI_BAR, 22); card_enter(base, bar, 540, 540, t, b["t0"], rot=0.0, dur=0.01)
    sx, sy = 540 - 470 + 998 * 940 / 1072, 540 - bar.height / 2 + 243 * 940 / 1072
    c0 = T("start", 3)
    if c0 <= t < c0 + 2.2:
        ph = (t - c0) % 0.8 / 0.8; r = 46 + 30 * ph; dr = ImageDraw.Draw(base)
        dr.ellipse([sx - r, sy - r, sx + r, sy + r], outline=TEAL + (255,), width=8); dr.ellipse([sx - 50, sy - 50, sx + 50, sy + 50], outline=TEAL + (255,), width=8)
    if t >= c0 - 0.2 and t < c0 + 2.2:
        k = max(0, 1 - ease_out((t - c0 + 0.2) / 0.5)); place(base, CUR, sx + 22 + 40 * k, sy + 30 + 60 * k)
    ph = phone(t, S)
    if t < T("start", 16):
        card_enter(base, ph, 540, 1090, t, b["t0"] + 0.1, rot=0.0, dur=0.35)
    else:  # phone input bar: mic + sound wave icons, wave icon ringed
        pb = Image.new("RGBA", (940, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(pb); d.rounded_rectangle([0, 0, 939, 329], 40, fill=(40, 40, 40, 255), outline=INKD + (255,), width=5)
        d.text((50, 50), "Reply to Claude", font=PF(54), fill=(170, 170, 170, 255)); d.ellipse([46, 190, 130, 274], outline=(130, 130, 130, 255), width=4)
        d.line([(88, 208), (88, 256)], fill=(220, 220, 220, 255), width=6); d.line([(64, 232), (112, 232)], fill=(220, 220, 220, 255), width=6)
        mic(d, 700, 230, 120, (225, 225, 225)); d.ellipse([780, 180, 900, 300], fill=(255, 255, 255, 255)); bars(d, 840, 240, 5, 20, 60, 0.7, INKD, 1.0, 9)
        pp = ease_back((t - T("start", 16)) / 0.3); place(base, pb, 540, 1090, 0.8 + 0.2 * min(1, pp), min(1, pp * 1.4))
        rr = 62 + 14 * math.sin(t * 6); ex, ey = 540 - 470 + 840, 1090 - 165 + 240; ImageDraw.Draw(base).ellipse([ex - rr, ey - rr, ex + rr, ey + rr], outline=TEAL + (255,), width=8)
    place(base, chip("Illustration (app screens)", 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, 1595)


def s_modes(base, t, b):
    base.alpha_composite(BGP)
    a = sk_card(940, 520, (255, 255, 255)); d = ImageDraw.Draw(a); tape(a, 70, -14, -5)
    d.text((50, 30), "HANDS-FREE", font=PF(64, True), fill=INKD + (255,)); d.rounded_rectangle([620, 38, 890, 100], 24, fill=TEAL + (255,)); d.text((646, 44), "DEFAULT", font=PF(40, True), fill=(255, 255, 255, 255))
    talk = T("modes", 0) <= t < T("modes", 4)
    mic(d, 110, 270, 150); bars(d, 330, 270, 7, 46, 200, t, TEAL, 1.0 if talk else 0.12, 20)
    if t >= T("modes", 4) + 0.1:
        pp = ease_back((t - T("modes", 4) - 0.1) / 0.3); bub = Image.new("RGBA", (330, 150), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
        bd.rounded_rectangle([0, 0, 329, 149], 34, fill=PEACH + (255,), outline=INKD + (255,), width=5); bd.text((30, 36), "Claude:", font=PF(38, True), fill=INKD + (255,)); bd.text((30, 88), "reply...", font=PF(30), fill=GREY + (255,))
        a.alpha_composite(scaled(bub, pp), (560, 250))
    card_enter(base, a, 540, 590, t, b["t0"], rot=-0.7, dur=0.01)
    p = sk_card(940, 520, (255, 255, 255)); d = ImageDraw.Draw(p); tape(p, 700, -14, 5)
    d.text((50, 30), "PUSH-TO-TALK", font=PF(64, True), fill=INKD + (255,))
    if t >= T("modes", 10): d.rounded_rectangle([600, 120, 890, 190], 24, fill=(255, 170, 60, 255)); d.text((624, 128), "NOISY", font=PF(46, True), fill=INKD + (255,))
    hold = t >= T("modes", 16) - 0.3; rr = 108 if hold else 120
    d.ellipse([140 - rr, 330 - rr, 140 + rr, 330 + rr], fill=TEAL + (255,) if hold else (200, 205, 207, 255), outline=INKD + (255,), width=6); mic(d, 140, 322, 130, (255, 255, 255))
    if hold: bars(d, 600, 330, 7, 46, 200, t, TEAL, 1.0, 20); d.text((330, 450), "HOLD and speak", font=PF(36, True), fill=TEAL + (255,))
    else: d.text((330, 300), "hold a button", font=PF(40), fill=(120, 120, 126, 255))
    card_enter(base, p, 540, 1160, t, T("modes", 8), rot=0.7, side=1)


def s_extra(base, t, b):
    base.alpha_composite(BGP)
    a = sk_card(940, 560, (255, 255, 255)); d = ImageDraw.Draw(a); tape(a, 70, -14, -5); d.text((50, 26), "One chat", font=PF(60, True), fill=INKD + (255,))

    def bubble(y, kind, ts, right=False):
        if t < ts: return
        pp = ease_back((t - ts) / 0.28); w_, h_ = (560, 110); sub = Image.new("RGBA", (w_, h_), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub)
        sd.rounded_rectangle([0, 0, w_ - 1, h_ - 1], 30, fill=(SKY if kind == "text" else TEALL) + (255,), outline=INKD + (255,), width=5)
        if kind == "text": sd.text((28, 28), "Typed message", font=PF(38, True), fill=INKD + (255,))
        else: mic(sd, 70, 56, 60); bars(sd, 330, 56, 12, 30, 60, t, INKD, 1.0, 10)
        a.alpha_composite(scaled(sub, pp), (340 if right else 40, y))
    bubble(130, "text", T("extra", 0)); bubble(270, "voice", T("extra", 2), True); bubble(410, "text", T("extra", 6))
    if t >= T("extra", 10):
        pp = min(1, (t - T("extra", 10)) / 0.4); ImageDraw.Draw(a).line([(910, 150), (910, 150 + int(330 * pp))], fill=TEAL + (255,), width=10)
    card_enter(base, a, 540, 640, t, b["t0"], rot=-0.7, dur=0.01)
    l = sk_card(940, 520, (255, 255, 255)); d = ImageDraw.Draw(l); tape(l, 700, -14, 5); d.text((50, 26), "Settings  >  Voice", font=PF(56, True), fill=INKD + (255,))
    d.text((50, 130), "Spoken language", font=PF(38), fill=(110, 110, 116, 255)); d.rounded_rectangle([50, 190, 890, 290], 24, fill=(244, 246, 247, 255), outline=INKD + (255,), width=4); d.text((80, 214), "English", font=PF(44, True), fill=INKD + (255,))
    if t >= T("extra", 18):
        d.rounded_rectangle([50, 320, 890, 420], 24, fill=(255, 244, 214, 255), outline=INKD + (255,), width=4); d.text((80, 344), "Other languages", font=PF(44, True), fill=INKD + (255,))
        d.rounded_rectangle([660, 338, 860, 402], 24, fill=TEAL + (255,)); d.text((690, 346), "BETA", font=PF(44, True), fill=(255, 255, 255, 255))
    card_enter(base, l, 540, 1190, t, T("extra", 7), rot=0.7, side=1)


def s_caution(base, t, b):
    base.alpha_composite(BGP)
    a = sk_card(940, 360, (255, 255, 255)); d = ImageDraw.Draw(a); tape(a, 70, -14, -5); d.text((50, 26), "Usage limit", font=PF(60, True), fill=INKD + (255,))
    fill_p = ease_io(min(1, max(0, (t - T("caution", 2)) / 2.2))); d.rounded_rectangle([50, 150, 890, 230], 38, fill=(228, 232, 233, 255), outline=INKD + (255,), width=4)
    if fill_p > 0.02: d.rounded_rectangle([54, 154, 54 + int(832 * 0.62 * fill_p), 226], 34, fill=TEAL + (255,))
    mic(d, 90, 300, 70); d.text((150, 270), "voice chats use the same limit", font=PF(34), fill=GREY + (255,))
    card_enter(base, a, 540, 520, t, b["t0"], rot=-0.7, dur=0.01)
    if t >= T("caution", 4):
        note = with_border(NOTE, 14); card_enter(base, note, 540, 850, t, T("caution", 4), rot=0.8, side=0)
        place(base, chip("Official page: support.claude.com / Use voice mode", 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, 965)
    c = sk_card(940, 330, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 700, -14, 5)
    if t >= T("caution", 12):
        pp = ease_back((t - T("caution", 12)) / 0.3); sub = Image.new("RGBA", (330, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub); bars(sd, 150, 100, 9, 30, 120, 0.4, (120, 120, 126), 1.0, 14)
        c.alpha_composite(scaled(sub, pp), (30, 40)); d.text((60, 250), "AUDIO", font=PF(44, True), fill=INKD + (255,))
        if t >= T("caution", 14) + 0.2: cross(d, 230, 80, int(110 * min(1, ease_back((t - T("caution", 14) - 0.2) / 0.28))))
    if t >= T("caution", 17):
        pp = ease_back((t - T("caution", 17)) / 0.3); sub = Image.new("RGBA", (340, 220), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub); sd.rounded_rectangle([20, 10, 250, 200], 16, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
        for k in range(5): sd.line([(44, 50 + 30 * k), (226 - (40 if k % 2 else 0), 50 + 30 * k)], fill=(150, 150, 156, 255), width=7)
        c.alpha_composite(scaled(sub, pp), (520, 30)); d.text((520, 250), "TRANSCRIPT", font=PF(44, True), fill=INKD + (255,)); tick(d, 780, 40, int(100 * min(1, pp)))
    card_enter(base, c, 540, 1240, t, T("caution", 11), rot=0.7, side=-1)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, robot("wave", 760), 540, 700 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill) in enumerate((("+ FOLLOW", T("cta", 4), TEAL), ("NEW FEATURE TOMORROW", T("cta", 8), INKD))):
        pp = pop(t, ts); place(base, chip(txt, 70 if n == 0 else 52, fill, (255, 255, 255), pad=(44, 10), r=30), 540, 1180 + 125 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("start", 0)), dict(k="start", t0=T("start", 0), t1=T("modes", 0)), dict(k="modes", t0=T("modes", 0), t1=T("extra", 0)),
     dict(k="extra", t0=T("extra", 0), t1=T("caution", 0)), dict(k="caution", t0=T("caution", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, start=s_start, modes=s_modes, extra=s_extra, caution=s_caution, cta=s_cta)
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
