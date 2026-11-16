"""054 Claude in daily life 01 (Zomato connector) Short. Warm cream paper, accent CORAL, Roman Hinglish captions, real official-page crops.
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
TEAL = (214, 64, 52); TEALL = (255, 205, 196); INKD = (30, 30, 36); OR = (217, 119, 87); GREEN = (22, 163, 74); RED = (225, 45, 57)
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
    im = Image.new("RGB", (W, H), (255, 247, 238)); d = ImageDraw.Draw(im)
    for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(243, 228, 214), width=2)
    for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(243, 228, 214), width=1)
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




def meter(d, x, y, w, h, p, col):
    pass


CAPTXT = {
    "hook": [(0, "Khana order karna hai?"), (8, "CLAUDE se ho sakta hai"), (13, "Dekho EXAMPLE")],
    "connect": [(0, "Pehle CONNECT karo"), (4, "CONNECTORS > Add custom"), (11, "Zomato ka server URL"), (17, "SIGN IN karo")],
    "use": [(0, "Ab CHAT me bolo"), (4, "Rs 300, VEG restaurant"), (15, "Menu se CART me daalo")],
    "pay": [(0, "PAYMENT QR se"), (4, "Tum khud karte ho"), (8, "Claude PAISE nahi deta")],
    "caution": [(0, "CAUTION"), (5, "Zomato: sirf TESTING"), (22, "Sirf BHAROSE ke server")],
    "cta": [(0, "Roz ke kaam me Claude"), (7, "DevRoboLab ko FOLLOW karo")],
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


def s_hook(base, t, b):
    base.alpha_composite(BGP)
    card = sk_card(940, 760, (255, 255, 255)); d = ImageDraw.Draw(card); tape(card, 60, -14, -5); tape(card, 760, -14, 5)
    d.text((60, 36), "Claude chat", font=PF(64, True), fill=INKD + (255,))
    d.text((60, 640), "(example screen, no real order)", font=PF(32), fill=GREY + (255,))
    if t >= 0.3: card.alpha_composite(scaled(bubble("Dinner order karna hai", "u", 560), ease_back((t - 0.3) / 0.3)), (320, 150))
    if t >= T("hook", 8): card.alpha_composite(scaled(bubble("Zomato connector se ho jayega", "c", 800, 96, 34), ease_back((t - T("hook", 8)) / 0.3)), (60, 290))
    card_enter(base, card, 540, 760, t, b["t0"], rot=-0.8, dur=0.01)
    if t >= T("hook", 13): pp = pop(t, T("hook", 13)); place(base, chip("FOOD + CLAUDE", 80, TEAL, (255, 255, 255), pad=(44, 12), r=34), 540, 1260, 0.7 + 0.3 * pp, min(1, pp * 1.4), -1.5)
    illus(base)


def s_connect(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("CONNECT IN 5 STEPS", b["t0"], b["t1"])], 260)
    for i, (txt, k) in enumerate((("1  Customize", 2), ("2  Connectors", 4), ("3  Add custom connector", 7), ("4  Paste server URL", 11), ("5  Sign in", 17))):
        slide(base, row(txt), 540, 450 + 120 * i, t, T("connect", k) - 0.1)
    if t >= T("connect", 12) - 0.1:
        c = sk_card(900, 150, (255, 255, 255)); d = ImageDraw.Draw(c); d.text((30, 40), "Server URL (Zomato, third-party)", font=PF(28), fill=GREY + (255,)); d.text((30, 85), "mcp-server.zomato.com/mcp", font=PF(44, True), fill=TEAL + (255,))
        card_enter(base, c, 540, 1190, t, T("connect", 12) - 0.1, rot=0.4, side=1)
    tag(base, "Steps: support.claude.com (official help page)", 1595)


def s_use(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("TYPE IT IN CHAT", b["t0"], b["t1"])], 260)
    c = sk_card(940, 900, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 70, -14, -5)
    d.text((50, 30), "Claude chat (example)", font=PF(46, True), fill=INKD + (255,))
    if t >= T("use", 4): c.alpha_composite(scaled(bubble("Rs 300, paas ke veg restaurant dikhao", "u", 860, 100, 34), ease_back((t - T("use", 4)) / 0.3)), (50, 130))
    for i, txt in enumerate(("Restaurant A  (example)", "Restaurant B  (example)", "Restaurant C  (example)")):
        ts = T("use", 14) + 0.3 + 0.25 * i
        if t >= ts: c.alpha_composite(scaled(bubble(txt, "c", 700, 80, 32), ease_back((t - ts) / 0.3)), (50, 260 + 100 * i))
    if t >= T("use", 17): c.alpha_composite(scaled(bubble("Menu se 2 item cart me daalo", "u", 760, 100, 34), ease_back((t - T("use", 17)) / 0.3)), (150, 600))
    if t >= T("use", 23): c.alpha_composite(scaled(bubble("Cart ready (example)", "c", 600, 100, 36), ease_back((t - T("use", 23)) / 0.3)), (50, 740))
    card_enter(base, c, 540, 830, t, b["t0"] + 0.1, rot=0.5, side=1)
    illus(base)


def qr(d, x, y, s):
    rnd = np.random.RandomState(7); n = 15; cs = s / n
    for i in range(n):
        for j in range(n):
            if rnd.rand() > 0.5: d.rectangle([x + i * cs, y + j * cs, x + (i + 1) * cs, y + (j + 1) * cs], fill=INKD + (255,))
    for (a, bb) in ((0, 0), (n - 4, 0), (0, n - 4)):
        d.rectangle([x + a * cs, y + bb * cs, x + (a + 4) * cs, y + (bb + 4) * cs], fill=(255, 255, 255, 255), outline=INKD + (255,), width=6); d.rectangle([x + (a + 1) * cs, y + (bb + 1) * cs, x + (a + 3) * cs, y + (bb + 3) * cs], fill=INKD + (255,))


def s_pay(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, [("PAYMENT BY QR", b["t0"], b["t1"])], 260)
    c = sk_card(700, 700, (255, 255, 255)); d = ImageDraw.Draw(c); tape(c, 60, -14, -5); qr(d, 80, 80, 540)
    d.text((350, 650), "example QR, not real", font=PF(30), fill=GREY + (255,), anchor="mm")
    card_enter(base, c, 540, 720, t, b["t0"] + 0.1, rot=-0.6, dur=0.3)
    if t >= T("pay", 4): pp = pop(t, T("pay", 4)); place(base, chip("YOU SCAN + PAY", 56, GREEN, (255, 255, 255), pad=(36, 10), r=28), 540, 1180, 0.7 + 0.3 * pp, min(1, pp * 1.4), 1.2)
    if t >= T("pay", 8):
        pp = pop(t, T("pay", 8)); sub = Image.new("RGBA", (860, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub); sd.rounded_rectangle([0, 0, 859, 119], 30, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
        sd.text((130, 60), "Claude does NOT pay", font=PF(44, True), fill=INKD + (255,), anchor="lm"); cross(sd, 26, 26, 68); place(base, sub, 540, 1340, 0.7 + 0.3 * pp, min(1, pp * 1.4))
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
    card_enter(base, note("Zomato: ONLY FOR TESTING", "Their page says so, can change", "Source: github.com/Zomato (third-party)"), 540, 760, t, b["t0"] + 0.1, rot=-0.5, side=-1)
    card_enter(base, note("Trust only servers you know", "Check permissions at sign-in", "Source: support.claude.com (official)"), 540, 1130, t, T("caution", 22) - 0.1, rot=0.5, side=1)
    illus(base)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, robot("wave", 760), 540, 700 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill) in enumerate((("+ FOLLOW", T("cta", 7), TEAL), ("CLAUDE IN DAILY LIFE", T("cta", 4), INKD))):
        pp = pop(t, ts); place(base, chip(txt, 70 if n == 0 else 48, fill, (255, 255, 255), pad=(44, 10), r=30), 540, (1180 if n == 0 else 1305), 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("connect", 0)), dict(k="connect", t0=T("connect", 0), t1=T("use", 0)), dict(k="use", t0=T("use", 0), t1=T("pay", 0)),
     dict(k="pay", t0=T("pay", 0), t1=T("caution", 0)), dict(k="caution", t0=T("caution", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, connect=s_connect, use=s_use, pay=s_pay, caution=s_caution, cta=s_cta)
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

