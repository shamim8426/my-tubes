"""057 Claude in daily life 02 (Gmail) Short. Cool paper, accent VIOLET, Roman Hinglish captions, real official-page crops.
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
TEAL = (110, 70, 214); TEALL = (226, 214, 252); INKD = (30, 30, 36); OR = (217, 119, 87); GREEN = (22, 163, 74); RED = (225, 45, 57)
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
    im = Image.new("RGB", (W, H), (243, 247, 255)); d = ImageDraw.Draw(im)
    for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(222, 232, 248), width=2)
    for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(222, 232, 248), width=1)
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
    "hook": [(0, "Mail dhoondhne me time?"), (13, "CLAUDE kar sakta hai"), (20, "Dekho EXAMPLE")],
    "connect": [(0, "Pehle GMAIL connect"), (4, "CUSTOMIZE > Connectors"), (11, "Gmail ke aage CONNECT"), (16, "Google se SIGN IN"), (27, "Bas EK baar")],
    "use": [(0, "Chat me GMAIL on karo"), (12, "Seedha SAWAAL poocho"), (24, "Claude mail me DHOONDHTA hai"), (31, "Links bhi dikhata hai")],
    "draft": [(0, "Ab REPLY likhwao"), (15, "Claude TEXT banata hai"), (21, "Padho, badlo, KHUD bhejo")],
    "caution": [(0, "CAUTION"), (2, "Official pages ALAG likhte"), (13, "SETTING dekho, mail JAANCHO")],
    "cta": [(0, "Madadgaar laga?"), (10, "FOLLOW karo")],
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
    d.text((50, 30), "Inbox (example)", font=PF(60, True), fill=INKD + (255,))
    imp = T("hook", 6) - 0.05
    for i in range(7):
        y = 150 + 100 * i; hot = (i == 3 and t >= imp)
        d.rounded_rectangle([40, y, 900, y + 84], 20, fill=((TEALL if hot else (244, 246, 250)) + (255,)), outline=INKD + (255,), width=4)
        d.ellipse([60, y + 20, 104, y + 64], fill=((TEAL if hot else (200, 206, 216)) + (255,)))
        d.rounded_rectangle([130, y + 20, 130 + (300 if i % 2 else 380), y + 40], 8, fill=(150, 156, 170, 255))
        d.rounded_rectangle([130, y + 50, 130 + (560 if i % 3 else 440), y + 64], 6, fill=(205, 210, 220, 255))
        if hot: d.text((850, y + 42), "!", font=PF(52, True), fill=TEAL + (255,), anchor="mm")
    card_enter(base, card, 540, 800, t, b["t0"], rot=-0.6, dur=0.01)
    if t >= T("hook", 13): pp = pop(t, T("hook", 13)); place(base, chip("EMAIL + CLAUDE", 80, TEAL, (255, 255, 255), pad=(44, 12), r=34), 540, 1345, 0.7 + 0.3 * pp, min(1, pp * 1.4), -1.5)
    illus(base)


def s_connect(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("CONNECT GMAIL, 5 STEPS", b["t0"], b["t1"])], 260)
    for i, (txt, k) in enumerate((("1  Open Customize", 2), ("2  Go to Connectors", 8), ("3  Gmail > Connect", 11), ("4  Sign in to Google", 18), ("5  Allow permissions", 24))):
        slide(base, row(txt), 540, 420 + 110 * i, t, T("connect", k) - 0.1)
    if t >= T("connect", 14) - 0.1:
        c = sk_card(900, 150, (255, 255, 255)); d = ImageDraw.Draw(c); on = t >= T("connect", 26)
        d.text((30, 28), "Gmail", font=PF(48, True), fill=INKD + (255,)); d.text((30, 92), "claude.ai > Customize > Connectors", font=PF(28), fill=GREY + (255,))
        lab = "Disconnect" if on else "Connect"; d.rounded_rectangle([600, 38, 870, 112], 20, fill=((GREEN if on else TEAL) + (255,)), outline=INKD + (255,), width=4); d.text((735, 76), lab, font=PF(36, True), fill=(255, 255, 255, 255), anchor="mm")
        card_enter(base, c, 540, 1130, t, T("connect", 14) - 0.1, rot=0.4, side=1)
    if t >= T("connect", 27): pp = pop(t, T("connect", 27)); place(base, chip("ONLY ONCE", 52, INKD, (255, 255, 255), pad=(34, 10), r=26), 540, 1300, 0.7 + 0.3 * pp, min(1, pp * 1.4), 1.2)
    tag(base, "Steps: claude.com/docs (official page)", 1595)


def s_use(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("ASK ABOUT YOUR MAILS", b["t0"], b["t1"])], 260)
    c = sk_card(940, 820, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 70, -14, -5)
    d.text((50, 30), "Claude chat (example)", font=PF(46, True), fill=INKD + (255,))
    d.rounded_rectangle([50, 110, 890, 200], 20, fill=(244, 246, 250, 255), outline=INKD + (255,), width=4); d.text((80, 155), "+  Connectors > Gmail", font=PF(34, True), fill=INKD + (255,), anchor="lm"); toggle(d, 740, 125, t >= T("use", 9))
    if t >= T("use", 13): c.alpha_composite(scaled(bubble("Sarah ne deadline ke baare me kya likha?", "u", 860, 100, 30), ease_back((t - T("use", 13)) / 0.3)), (50, 240))
    if t >= T("use", 26): c.alpha_composite(scaled(bubble("Sarah: report Friday tak chahiye (example)", "c", 860, 100, 30), ease_back((t - T("use", 26)) / 0.3)), (50, 390))
    if t >= T("use", 35):
        for i, txt in enumerate(("Mail 1  (link)", "Mail 2  (link)")):
            ts = T("use", 35) + 0.25 * i
            if t >= ts: c.alpha_composite(scaled(bubble(txt, "c", 520, 84, 32), ease_back((t - ts) / 0.3)), (50, 540 + 110 * i))
    card_enter(base, c, 540, 830, t, b["t0"] + 0.1, rot=0.5, side=1)
    illus(base)


def s_draft(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("REPLY DRAFT", b["t0"], b["t1"])], 260)
    c = sk_card(940, 780, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 70, -14, -5)
    d.text((50, 30), "Claude chat (example)", font=PF(46, True), fill=INKD + (255,))
    d.rounded_rectangle([50, 110, 890, 200], 20, fill=(244, 246, 250, 255), outline=INKD + (255,), width=4); d.text((80, 155), "Sarah (mail): Report kab tak milega?", font=PF(30, True), fill=GREY + (255,), anchor="lm")
    if t >= T("draft", 2): c.alpha_composite(scaled(bubble("Polite reply likho: Friday tak bhej dunga", "u", 860, 100, 30), ease_back((t - T("draft", 2)) / 0.3)), (50, 240))
    if t >= T("draft", 15):
        pp = ease_back((t - T("draft", 15)) / 0.35); dr = Image.new("RGBA", (860, 340), (0, 0, 0, 0)); dd = ImageDraw.Draw(dr)
        dd.rounded_rectangle([0, 0, 859, 339], 26, fill=TEALL + (255,), outline=INKD + (255,), width=5)
        for i, ln in enumerate(("Hi Sarah,", "Main report Friday tak", "bhej dunga. Thanks!", "(draft text, example)")): dd.text((34, 36 + 72 * i), ln, font=PF(38 if i < 3 else 30, i < 3), fill=(INKD if i < 3 else GREY) + (255,))
        c.alpha_composite(scaled(dr, pp), (50, 380))
    card_enter(base, c, 540, 790, t, b["t0"] + 0.1, rot=-0.5, side=-1)
    for n, (txt, k, fill) in enumerate((("READ", 21, INKD), ("EDIT", 24, TEAL), ("YOU SEND", 26, GREEN))):
        if t >= T("draft", k): pp = pop(t, T("draft", k)); place(base, chip(txt, 52, fill, (255, 255, 255), pad=(34, 10), r=28), 300 + 240 * n if n < 2 else 810, 1310, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.2, -1)[n])
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
    card_enter(base, note("Official pages DIFFER", "Read-only vs draft / send", "Source: claude.com/docs + support.claude.com"), 540, 700, t, b["t0"] + 0.1, rot=-0.5, side=-1)
    card_enter(base, note("Check before you send", "Open Connectors, see permissions", "Source: support.claude.com (official)"), 540, 1070, t, T("caution", 13) - 0.1, rot=0.5, side=1)
    illus(base)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, robot("wave", 760), 540, 700 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill) in enumerate((("+ FOLLOW", T("cta", 10), TEAL), ("CLAUDE IN DAILY LIFE", T("cta", 5), INKD))):
        pp = pop(t, ts); place(base, chip(txt, 70 if n == 0 else 48, fill, (255, 255, 255), pad=(44, 10), r=30), 540, (1180 if n == 0 else 1305), 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("connect", 0)), dict(k="connect", t0=T("connect", 0), t1=T("use", 0)), dict(k="use", t0=T("use", 0), t1=T("draft", 0)),
     dict(k="draft", t0=T("draft", 0), t1=T("caution", 0)), dict(k="caution", t0=T("caution", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, connect=s_connect, use=s_use, draft=s_draft, caution=s_caution, cta=s_cta)
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
    if len(sys.argv) > 1 and sys.argv[1] == "range":
        print("range not implemented; full render"); return
    build_audio(HERE / "audio/voice.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()


