"""058 Claude in daily life 03 (Google Calendar) Short. Mint paper, accent TEAL, Roman Hinglish captions, own illustrations (labelled).
Run: python make.py frames t1 t2 ...  |  python make.py   (render)  |  python make.py range t0 t1 out.mp4"""
import json, math, os, random, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "shared/style_library"))
os.environ["PATH"] += ";" + str(ROOT / "tools/ffmpeg")
from beat_sync import pulse as _pulse
from photo_video import W, H, FPS, ease_out, ease_back, ease_io, wav_dur, encode

LEAD, AFTER = 0.05, 0.05
FONT = str(ROOT / "shared/fonts/Poppins-Bold.ttf")
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START))
TEAL = (16, 140, 150); TEALL = (208, 240, 242); INKD = (30, 30, 36); OR = (217, 119, 87); GREEN = (22, 163, 74); RED = (225, 45, 57)
PEACH = (255, 228, 210); SKY = (208, 232, 250)
GREY = (90, 90, 96)


BEATS = json.load(open(HERE / "audio/beats.json"))["beats"]   # librosa beat times on the video clock (music starts at t=0)


def Tr(scene, k):   # raw spoken time of token k (captions + audio never move)
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


def T(scene, k):    # VISUAL event time: spoken time snapped to the nearest beat if the beat is -0.07..+0.15 s from the word, so pictures land on the beat
    r = Tr(scene, k); b = min(BEATS, key=lambda x: abs(x - (r + 0.04)))
    return b if -0.07 <= b - r <= 0.15 else r


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
    im = Image.new("RGB", (W, H), (239, 250, 245)); d = ImageDraw.Draw(im)
    for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(213, 237, 227), width=2)
    for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(213, 237, 227), width=1)
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



CAPTXT = {
    "hook": [(0, "Kal ki meetings yaad?"), (6, "Kab khali ho?"), (15, "CLAUDE bata sakta hai")],
    "connect": [(0, "Pehle CALENDAR connect"), (4, "CUSTOMIZE > Connectors"), (11, "Calendar ke aage CONNECT"), (18, "Google se SIGN IN"), (29, "Bas EK baar")],
    "use": [(0, "Chat me CALENDAR on karo"), (13, "Seedha SAWAAL poocho"), (21, "Claude calendar PADHTA hai"), (27, "Events ke LINKS bhi")],
    "more": [(0, "Aur bhi POOCHO"), (7, "Meeting TAKRA rahi?"), (14, "Budget review me KAUN?"), (22, "Time aur NAAM")],
    "caution": [(0, "CAUTION"), (2, "Official pages ALAG likhte"), (24, "APPROVAL padho, phir HAAN")],
    "cta": [(0, "Aur AASAN tips"), (7, "FOLLOW karo")],
}
CAPS = []
for sid in IDS:
    items = CAPTXT[sid]; end = SC[sid] + D[IDS.index(sid)]
    for j, (k, txt) in enumerate(items): CAPS.append((Tr(sid, k) - 0.04, (Tr(sid, items[j + 1][0]) - 0.04) if j + 1 < len(items) else end, txt))
_capc = {}
def caption(base, t):
    for a, b, txt in CAPS:
        if a <= t < b:
            if txt not in _capc: _capc[txt] = chip(txt, 50, (28, 28, 34), (255, 255, 255), pad=(32, 12), r=28, hl={w.strip(",.?!") for w in txt.split() if w.isupper() and len(w) > 2})
            place(base, _capc[txt], 540, 1500, (0.94 + 0.06 * ease_out((t - a) / 0.12)) * (1 + 0.022 * _pulse(t, BEATS))); return


PIX_COL = [(16, 140, 150), (255, 214, 10), (30, 30, 36), (255, 255, 255), (217, 119, 87)]


def pixel_burst(base, cx, cy, t, t0, n=34, life=0.75, seed=1):
    """Own tiny pixel-art burst (idea: patch-gg/pixelfx, MIT; no code copied): square pixels on an 8 px grid, stepped at 14 fps, shrinking."""
    age = t - t0
    if age < 0 or age > life: return
    a = math.floor(age * 14) / 14; rnd = random.Random(seed); d = ImageDraw.Draw(base)
    for i in range(n):
        ang = rnd.uniform(0, 2 * math.pi); sp = rnd.uniform(260, 760); sz = rnd.choice((12, 16, 20, 24)); col = rnd.choice(PIX_COL)
        x = cx + math.cos(ang) * sp * a; y = cy + math.sin(ang) * sp * a + 650 * a * a
        s = int(sz * max(0.0, 1 - a / life)) // 4 * 4
        if s < 4: continue
        x = round(x / 8) * 8; y = round(y / 8) * 8
        d.rectangle([x - s // 2 - 3, y - s // 2 - 3, x + s // 2 + 3, y + s // 2 + 3], fill=INKD + (255,)); d.rectangle([x - s // 2, y - s // 2, x + s // 2, y + s // 2], fill=col + (255,))


def banner(base, t, items, y=300):
    for txt, ts, te in items:
        if ts <= t < te: pp = pop(t, ts + 0.03); place(base, chip(txt, 46, TEAL, (255, 255, 255), pad=(30, 9), r=26), 540, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def tag(base, text, y): place(base, chip(text, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, y)
def illus(base, y=1595): tag(base, "Illustration (own drawing), example only", y)


def bubble(txt, who, w=780, h=96, size=36):
    col = SKY if who == "u" else TEALL
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=col + (255,), outline=INKD + (255,), width=5); d.text((26, h // 2), txt, font=PF(size, True), fill=INKD + (255,), anchor="lm"); return im


def row(txt, w=860):
    sub = Image.new("RGBA", (w, 100), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub); sd.rounded_rectangle([0, 0, w - 1, 99], 26, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    sd.text((130, 50), txt, font=PF(38, True), fill=INKD + (255,), anchor="lm"); tick(sd, 24, 18, 64); return sub


def slide(base, spr, x, y, t, t0, dur=0.32):
    if t < t0: return
    pp = min(1, (t - t0) / dur); q = ease_out(pp); place(base, spr, x + (1 - q) * 420, y, 0.92 + 0.08 * ease_back(pp), min(1, pp * 1.5))


def toggle(d, x, y, on):
    d.rounded_rectangle([x, y, x + 120, y + 60], 30, fill=(GREEN if on else (190, 190, 198)) + (255,), outline=INKD + (255,), width=4)
    cx = x + (90 if on else 30); d.ellipse([cx - 24, y + 6, cx + 24, y + 54], fill=(255, 255, 255, 255), outline=INKD + (255,), width=3)


def s_hook(base, t, b):
    base.alpha_composite(BGP)
    card = sk_card(940, 900, (255, 255, 255)); d = ImageDraw.Draw(card); tape(card, 60, -14, -5); tape(card, 760, -14, 5)
    d.text((50, 30), "My Calendar (example)", font=PF(58, True), fill=INKD + (255,))
    imp = T("hook", 1)
    for c, nm in enumerate(("M", "T", "W", "T", "F")): d.text((120 + 172 * c, 140), nm, font=PF(36, True), fill=GREY + (255,), anchor="mm")
    for r in range(4):
        for c in range(5):
            x = 40 + 172 * c; y = 170 + 168 * r; hot = (r == 1 and c == 2 and t >= imp)
            d.rounded_rectangle([x, y, x + 160, y + 156], 18, fill=((TEALL if hot else (244, 248, 250)) + (255,)), outline=INKD + (255,), width=4)
            d.text((x + 16, y + 10), str(4 + r * 7 + c), font=PF(26, True), fill=GREY + (255,))
            if (r, c) in ((0, 1), (1, 2), (1, 4), (2, 0), (2, 3), (3, 2)):
                d.rounded_rectangle([x + 14, y + 80, x + 146, y + 106], 10, fill=((TEAL if hot else (170, 180, 196)) + (255,)))
                if (r + c) % 2: d.rounded_rectangle([x + 14, y + 114, x + 110, y + 136], 8, fill=(205, 212, 222, 255))
    card_enter(base, card, 540, 800, t, b["t0"], rot=-0.6, dur=0.01)
    if t >= T("hook", 15): pp = pop(t, T("hook", 15)); place(base, chip("CALENDAR + CLAUDE", 74, TEAL, (255, 255, 255), pad=(44, 12), r=34), 540, 1345, 0.7 + 0.3 * pp, min(1, pp * 1.4), -1.5)
    pixel_burst(base, 528, 762, t, imp, seed=3); pixel_burst(base, 540, 1300, t, T("hook", 15), n=16, life=0.5, seed=4)
    illus(base)


def s_connect(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("CONNECT CALENDAR, 5 STEPS", b["t0"], b["t1"])], 260)
    for i, (txt, k) in enumerate((("1  Open Customize", 1), ("2  Go to Connectors", 8), ("3  Google Calendar", 12), ("4  Sign in to Google", 18), ("5  Allow permissions", 26))):
        slide(base, row(txt), 540, 420 + 110 * i, t, T("connect", k) - 0.1)
    if t >= T("connect", 16) - 0.1:
        c = sk_card(900, 150, (255, 255, 255)); d = ImageDraw.Draw(c); on = t >= T("connect", 29)
        d.text((30, 28), "Google Calendar", font=PF(48, True), fill=INKD + (255,)); d.text((30, 92), "claude.ai > Customize > Connectors", font=PF(28), fill=GREY + (255,))
        lab = "Disconnect" if on else "Connect"; d.rounded_rectangle([600, 38, 870, 112], 20, fill=((GREEN if on else TEAL) + (255,)), outline=INKD + (255,), width=4); d.text((735, 76), lab, font=PF(36, True), fill=(255, 255, 255, 255), anchor="mm")
        card_enter(base, c, 540, 1130, t, T("connect", 16) - 0.1, rot=0.4, side=1)
    if t >= T("connect", 30): pp = pop(t, T("connect", 30)); place(base, chip("ONLY ONCE", 52, INKD, (255, 255, 255), pad=(34, 10), r=26), 540, 1300, 0.7 + 0.3 * pp, min(1, pp * 1.4), 1.2)
    tag(base, "Steps: claude.com/docs (official page)", 1595)


def s_use(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("ASK ABOUT YOUR SCHEDULE", b["t0"], b["t1"])], 260)
    c = sk_card(940, 820, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 70, -14, -5)
    d.text((50, 30), "Claude chat (example)", font=PF(46, True), fill=INKD + (255,))
    d.rounded_rectangle([50, 110, 890, 200], 20, fill=(244, 248, 250, 255), outline=INKD + (255,), width=4); d.text((80, 155), "+  Connectors > Google Calendar", font=PF(32, True), fill=INKD + (255,), anchor="lm"); toggle(d, 740, 125, t >= T("use", 10))
    if t >= T("use", 15): c.alpha_composite(scaled(bubble("Kal meri kaun si meetings hain?", "u", 860, 100, 32), ease_back((t - T("use", 15)) / 0.3)), (50, 240))
    if t >= T("use", 24): c.alpha_composite(scaled(bubble("Kal: 11:00 Team call, 4:30 Review (example)", "c", 860, 100, 28), ease_back((t - T("use", 24)) / 0.3)), (50, 390))
    if t >= T("use", 30):
        for i, txt in enumerate(("Event 1  (link)", "Event 2  (link)")):
            ts = T("use", 30) + 0.25 * i
            if t >= ts: c.alpha_composite(scaled(bubble(txt, "c", 520, 84, 32), ease_back((t - ts) / 0.3)), (50, 540 + 110 * i))
    card_enter(base, c, 540, 830, t, b["t0"] + 0.1, rot=0.5, side=1)
    illus(base)


def s_more(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("ASK MORE", b["t0"], b["t1"])], 260)
    c = sk_card(940, 780, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 70, -14, -5)
    d.text((50, 30), "Claude chat (example)", font=PF(46, True), fill=INKD + (255,))
    for ts, y, txt, who, sz in ((7, 110, "Next week meeting takra rahi?", "u", 32), (11, 230, "1 clash: Tue 3 PM (example)", "c", 32), (14, 380, "Budget review me kaun aa raha?", "u", 32), (18, 500, "Sam, Priya, Ravi (example)", "c", 32)):
        if t >= T("more", ts): c.alpha_composite(scaled(bubble(txt, who, 860, 100, sz), ease_back((t - T("more", ts)) / 0.3)), (50, y))
    card_enter(base, c, 540, 790, t, b["t0"] + 0.1, rot=-0.5, side=-1)
    for n, (txt, k, fill) in enumerate((("TIME", 23, INKD), ("PEOPLE", 25, TEAL))):
        if t >= T("more", k): pp = pop(t, T("more", k)); place(base, chip(txt, 56, fill, (255, 255, 255), pad=(36, 10), r=28), 330 + 400 * n, 1310, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.2)[n])
    illus(base)


def warn(d, x, y, s):
    d.polygon([(x + s / 2, y), (x + s, y + s * 0.9), (x, y + s * 0.9)], fill=(255, 214, 10, 255), outline=INKD + (255,)); d.text((x + s / 2, y + s * 0.62), "!", font=PF(int(s * 0.5), True), fill=INKD + (255,), anchor="mm")


def note(txt1, txt2, src):
    c = sk_card(900, 300, (255, 255, 255)); d = ImageDraw.Draw(c); warn(d, 30, 30, 90)
    d.text((150, 60), txt1, font=PF(44, True), fill=INKD + (255,)); d.text((150, 130), txt2, font=PF(34), fill=GREY + (255,))
    d.rounded_rectangle([30, 220, 870, 270], 14, fill=(40, 44, 58, 255)); d.text((450, 245), src, font=PF(26, True), fill=(235, 235, 240, 255), anchor="mm"); return c


def s_caution(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("CAUTION", b["t0"], b["t1"])], 260)
    card_enter(base, note("Official pages DIFFER", "Read-only vs create / edit", "Source: claude.com/docs + support.claude.com"), 540, 700, t, b["t0"] + 0.1, rot=-0.5, side=-1)
    card_enter(base, note("Read the approval first", "Say yes only if you agree", "Source: support.claude.com (official)"), 540, 1070, t, T("caution", 24) - 0.1, rot=0.5, side=1)
    for n, (txt, k, fill) in enumerate((("ONLY READ?", 15, INKD), ("OR EDIT?", 21, TEAL))):
        if t >= T("caution", k): pp = pop(t, T("caution", k)); place(base, chip(txt, 56, fill, (255, 255, 255), pad=(36, 10), r=28), 330 + 420 * n, 1310, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.2)[n])
    illus(base)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, robot("wave", 760), 540, 700 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill) in enumerate((("+ FOLLOW", T("cta", 8), TEAL), ("CLAUDE IN DAILY LIFE", T("cta", 3), INKD))):
        pp = pop(t, ts); (pixel_burst(base, 540, 1180, t, ts, n=36, seed=9) if n == 0 else None); place(base, chip(txt, 70 if n == 0 else 48, fill, (255, 255, 255), pad=(44, 10), r=30), 540, (1180 if n == 0 else 1305), 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("connect", 0)), dict(k="connect", t0=T("connect", 0), t1=T("use", 0)), dict(k="use", t0=T("use", 0), t1=T("more", 0)),
     dict(k="more", t0=T("more", 0), t1=T("caution", 0)), dict(k="caution", t0=T("caution", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, connect=s_connect, use=s_use, more=s_more, caution=s_caution, cta=s_cta)
SR = 24000

def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = Image.new("RGBA", (W, H)); FN[b["k"]](base, t, b); caption(base, t)
    im = base.convert("RGB"); lt = t - b["t0"]
    if b["k"] != "hook" and 0 <= lt < 0.26:   # shot recipe "impact settle" (principle from video-shotcraft): each beat-cut lands 3.5% big and settles
        s = 1 + 0.035 * (1 - ease_out(lt / 0.26)); w2, h2 = int(W * s), int(H * s)
        im = im.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
    return np.array(im)


def load_audio(path, sr=SR, ss=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(ss)] + (["-t", str(dur)] if dur else []) + ["-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).copy()


def sfx_track():
    n = int(TOTAL * SR) + SR; out = np.zeros(n, dtype=np.float32); whoosh = load_audio(ROOT / "shared/sfx/whoosh_142348.mp3", dur=0.6); magic = load_audio(ROOT / "shared/sfx/magic_376745.mp3", dur=0.9)
    for clip in (whoosh, magic):
        clip *= np.linspace(1, 0, len(clip)) ** 1.5; clip /= max(1e-6, float(np.abs(clip).max()))
    hits = [(x["t0"] - 0.05, whoosh, 0.20) for x in B[1:]] + [(T("hook", 1), magic, 0.16), (T("hook", 15), magic, 0.13), (T("cta", 8), magic, 0.2)]
    for t0, clip, g in hits:
        s0 = max(0, int(t0 * SR)); seg = clip[: n - s0] * g; out[s0:s0 + len(seg)] += seg
    return out, [round(h[0], 2) for h in hits]


def mix_and_norm(out_wav):
    voice = load_audio(HERE / "audio/voice.wav"); n = int(TOTAL * SR) + SR; v = np.zeros(n, dtype=np.float32); v[:len(voice)] = voice[:n]
    mus = load_audio(ROOT / deck["music"]["file"], ss=deck["music"]["start"], dur=TOTAL + 2) * (10 ** (-22 / 20)); m = np.zeros(n, dtype=np.float32); m[:len(mus)] = mus[:n]
    sfx, hits = sfx_track(); mix = v + m + sfx
    raw = HERE / "audio/mix_raw.wav"
    with wave.open(str(raw), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    af = f"loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", af, "-ar", "48000", str(out_wav)], check=True); print("sfx at", hits); return hits


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['k'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/v2_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice.wav"); mix_and_norm(HERE / "audio/final_mix.wav"); n = int(TOTAL * FPS); out = HERE / "output/short_v2_beat.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(HERE / "audio/final_mix.wav"),
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 150 == 0: print(f"  frame {i}/{n}", flush=True)
    p.stdin.close(); p.wait()


main()
