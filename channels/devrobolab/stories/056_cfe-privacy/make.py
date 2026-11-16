"""056 Claude Feature 08 (Privacy) Short. Warm cream paper, accent AMBER, own Playwright captures of the official pages, dark incognito beat.
Run: python make.py frames t1 t2 ...  |  python make.py (render)"""
import json, math, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import W, H, FPS, ease_out, ease_back, ease_io, wav_dur, encode

LEAD, AFTER = 0.05, 0.05
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START))
ACC = (217, 119, 6); ACCL = (253, 186, 116); INKD = (30, 30, 36); GREEN = (22, 163, 74); RED = (225, 45, 57)


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(str(ROOT / "shared/fonts/Poppins-Bold.ttf"), sz)
    return _fc[sz]


def chip(text, size, fill, color=(255, 255, 255), pad=(34, 14), r=26, hl=None, hlcolor=ACCL):
    f = font(size); words = text.split(" "); sp = f.getlength(" ")
    wl = [f.getlength(w) for w in words]; tw = int(sum(wl) + sp * (len(words) - 1)); asc, desc = f.getmetrics()
    im = Image.new("RGBA", (tw + 2 * pad[0], asc + desc + 2 * pad[1]), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=fill + (255,)); x = pad[0]
    for w, l in zip(words, wl):
        d.text((x, pad[1]), w, font=f, fill=(hlcolor if hl and w.strip(",.?!:") in hl else color) + (255,)); x += l + sp
    return im


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def pop(t, t0, dur=0.28): return ease_back((t - t0) / dur) if t >= t0 else 0.0


def shadow(w, h, r=30, off=30, blur=24, a=100):
    sh = Image.new("RGBA", (w + 160, h + 160), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([80, 80 + off, 80 + w, 80 + h + off], r, fill=(0, 0, 0, a))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def card_enter(base, spr, cx, cy, t, t0, rot=0.0, side=0, dur=0.38):
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur))
    dx = side * (1 - q) * 520; dy = (1 - q) * (140 if side == 0 else 0); sc = 0.9 + 0.1 * e; w, h = spr.size
    place(base, shadow(w, h), cx + dx, cy + dy, sc, min(1, q * 1.5), rot); place(base, spr, cx + dx, cy + dy, sc, min(1, q * 1.5), rot)


MASC = Image.open(ROOT / "channels/devrobolab/mascot/cut/wave.png").convert("RGBA")
def robot(h): return MASC.resize((int(MASC.width * h / MASC.height), h), Image.LANCZOS)


def bg_paper():
    im = Image.new("RGB", (W, H), (255, 250, 240)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(255, int(250 - 10 * k), int(240 - 14 * k)))
    d.ellipse([-200, 500, 900, 1500], fill=(255, 224, 178)); im = im.filter(ImageFilter.GaussianBlur(140)); d = ImageDraw.Draw(im)
    for x in range(0, W, 72): d.line([(x, 0), (x, H)], fill=(246, 236, 220), width=1)
    for y in range(0, H, 72): d.line([(0, y), (W, y)], fill=(246, 236, 220), width=1)
    return im.convert("RGBA")
BGP = bg_paper()
BGK = Image.new("RGBA", (W, H), (10, 10, 14, 255))


def with_border(img, r=18, bw=5):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=bw); return o


def crop_w(name, box, w):
    c = Image.open(HERE / f"raw/{name}.png").convert("RGB").crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)


TOG = with_border(crop_w("shot_priv_toggle", (80, 825, 1250, 1040), 1040))
TOGL = with_border(crop_w("shot_priv_toggle", (80, 930, 1165, 1040), 1040))
UNDO = with_border(crop_w("shot_priv_toggle", (80, 278, 1915, 428), 1040))
GHOSTC = with_border(crop_w("shot_inc_ghost", (647, 1128, 1560, 1348), 1040))
NOSAVE = with_border(crop_w("shot_inc_nosave", (647, 826, 1967, 935), 1000))
SRC1 = "Official: privacy.claude.com / model improvement settings"
SRC2 = "Official: support.claude.com / Use incognito chats"


def srcline(base, txt, y=1425):
    place(base, chip(txt, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, y)


def banner(base, t, txt, ts, y=215, fill=ACC):
    if t >= ts:
        pp = pop(t, ts + 0.03); place(base, chip(txt, 46, fill, (255, 255, 255), pad=(30, 9), r=26), 540, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def pc(base, txt, size, fill, color, cx, cy, t, ts, rot=0, pad=(36, 10), r=26, hl=None):
    if t >= ts - 0.02:
        pp = pop(t, ts); place(base, chip(txt, size, fill, color, pad=pad, r=r, hl=hl), cx, cy, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)


def toggle(t, t_off, label_on=True):
    w, h = 900, 190; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 36, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    d.text((36, 28), "Help Improve our", font=font(40), fill=INKD + (255,)); d.text((36, 90), "AI models", font=font(40), fill=INKD + (255,))
    q = ease_io(min(1, max(0, (t - t_off) / 0.35))); sw, sh_ = 220, 110; sx, sy = w - sw - 40, (h - sh_) // 2
    col = tuple(int(GREEN[i] * (1 - q) + (150, 150, 156)[i] * q) for i in range(3))
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh_], 55, fill=col + (255,))
    kx = sx + 8 + (sw - sh_ - 0) * (1 - q); d.ellipse([kx, sy + 8, kx + sh_ - 16, sy + sh_ - 8], fill=(255, 255, 255, 255))
    d.text((sx + 30 if q < 0.5 else sx + sw - 90, sy + 28), "ON" if q < 0.5 else "OFF", font=font(40), fill=(255, 255, 255, 255) if q < 0.5 else (255, 255, 255, 255))
    return im


def ghost(size=300, eye=(30, 30, 36)):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = size
    d.pieslice([s * .12, s * .06, s * .88, s * .82], 180, 360, fill=(255, 255, 255, 255)); d.rectangle([s * .12, s * .44, s * .88, s * .80], fill=(255, 255, 255, 255))
    n = 4; bw = (s * .76) / n
    for i in range(n): d.ellipse([s * .12 + i * bw, s * .70, s * .12 + (i + 1) * bw, s * .92], fill=(255, 255, 255, 255) if i % 2 == 0 else (0, 0, 0, 0))
    for i in range(n):
        if i % 2 == 1: d.ellipse([s * .12 + i * bw, s * .70, s * .12 + (i + 1) * bw, s * .92], fill=(0, 0, 0, 0))
    d.ellipse([s * .33, s * .38, s * .43, s * .52], fill=eye + (255,)); d.ellipse([s * .57, s * .38, s * .67, s * .52], fill=eye + (255,))
    return im


# ---- captions ----
CAPTXT = {
    "hook": [(0, "Claude se PRIVATE baatein?"), (8, "Ye DO settings jaan lo"), (16, "Chat rahe aapke CONTROL me")],
    "train": [(0, "SETTING 1: Model training"), (8, "Name > Settings > Privacy"), (19, "TOGGLE ko OFF karo"), (26, "Nayi chats training me nahi")],
    "caution1": [(0, "Dhyan rakho!"), (2, "PURANI training WAPAS nahi"), (8, "Jo data ja chuka, wahi rahega"), (20, "Free, Pro, Max plans ke liye")],
    "incog": [(0, "SETTING 2: INCOGNITO chat"), (5, "GHOST icon, upar DAYE kone me"), (14, "Kala BORDER + label"), (23, "Na HISTORY, MEMORY, TRAINING")],
    "caution2": [(0, "Dhyan rakho!"), (2, "Band kiya to DOBARA nahi khulegi"), (10, "ZAROORI baat pehle COPY karo"), (17, "PROJECTS me kaam nahi karta")],
    "cta": [(0, "Aur USEFUL jaankari ke liye"), (6, "Hamein FOLLOW kijiye")],
}
CAPS = []
for sid in IDS:
    items = CAPTXT[sid]; end = SC[sid] + D[IDS.index(sid)]
    for j, (k, txt) in enumerate(items): CAPS.append((T(sid, k) - 0.04, (T(sid, items[j + 1][0]) - 0.04) if j + 1 < len(items) else end, txt))
_capc = {}
def caption(base, t):
    for a, b, txt in CAPS:
        if a <= t < b:
            if txt not in _capc: _capc[txt] = chip(txt, 50, (28, 28, 34), (255, 255, 255), pad=(32, 12), r=28, hl={w.strip(",.?!:") for w in txt.split() if w.isupper() and len(w) > 2})
            place(base, _capc[txt], 540, 1530, 0.94 + 0.06 * ease_out((t - a) / 0.12)); return


# ---- scenes ----
def s_hook(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "PRIVATE CHATS?", 90, (255, 255, 255), INKD, 540, 330, t, b["t0"] + 0.1, -1.5, pad=(50, 12), r=36)
    card_enter(base, TOGL, 540, 600, t, b["t0"] + 0.15, rot=0.8, side=1)
    pc(base, "2 PRIVACY SETTINGS", 70, ACC, (255, 255, 255), 540, 880, t, T("hook", 11), -1, pad=(44, 12), r=30)
    if t >= T("hook", 15): card_enter(base, toggle(t, T("hook", 20)), 540, 1130, t, T("hook", 15))
    pc(base, "YOUR CONTROL", 84, (30, 30, 36), (255, 255, 255), 540, 1340, t, T("hook", 19), 1.5, pad=(44, 12), r=32)
    srcline(base, SRC1, 1445)


def s_train(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, "SETTING 1  MODEL TRAINING", b["t0"] + 0.1, 215)
    card_enter(base, TOG, 540, 470, t, b["t0"] + 0.2, rot=-0.5, side=1)
    for txt, k, x in (("YOUR NAME", 9, 190), ("SETTINGS", 13, 540), ("PRIVACY", 17, 890)):
        pc(base, txt, 38, (30, 30, 36), (255, 255, 255), x, 780, t, T("train", k), 0, pad=(22, 9), r=22)
    for x in (365, 715):
        if t >= T("train", 13) - 0.05 and x == 365 or t >= T("train", 17) - 0.05 and x == 715:
            place(base, chip(">", 52, ACC, (255, 255, 255), pad=(14, 2), r=14), x, 780)
    if t >= T("train", 19) - 0.1: card_enter(base, toggle(t, T("train", 23)), 540, 1080, t, T("train", 19) - 0.1)
    pc(base, "NEW CHATS: NOT USED", 62, GREEN, (255, 255, 255), 540, 1310, t, T("train", 28), -1, pad=(40, 12), r=30)
    srcline(base, SRC1, 1425)


def s_c1(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "CAUTION", 76, RED, (255, 255, 255), 540, 230, t, b["t0"] + 0.1, -1.5, pad=(46, 12), r=32)
    pc(base, "PAST TRAINING = NOT UNDONE", 56, INKD, (255, 255, 255), 540, 480, t, T("caution1", 4), 1, pad=(40, 12), r=28)
    if t >= T("caution1", 8) - 0.05: card_enter(base, UNDO, 540, 740, t, T("caution1", 8), rot=-0.6, side=1)
    pc(base, "OLD DATA STAYS", 84, RED, (255, 255, 255), 540, 990, t, T("caution1", 14), 1.5, pad=(44, 12), r=30)
    for txt, k, x in (("FREE", 22, 230), ("PRO", 23, 540), ("MAX", 25, 850)):
        pc(base, txt, 76, ACC, (255, 255, 255), x, 1250, t, T("caution1", k), (-1.5, 1, -1)[(22, 23, 25).index(k)], pad=(40, 12), r=30)
    srcline(base, SRC1, 1425)


def s_incog(base, t, b):
    base.alpha_composite(BGK)
    d = ImageDraw.Draw(base); d.rectangle([0, 0, W - 1, H - 1], outline=(255, 255, 255, 255), width=10)
    banner(base, t, "SETTING 2  INCOGNITO", b["t0"] + 0.1, 150)
    card_enter(base, GHOSTC, 540, 440, t, b["t0"] + 0.2, rot=0.5, side=1)
    if t >= T("incog", 9) - 0.1:
        pp = pop(t, T("incog", 9) - 0.1); place(base, ghost(300), 540, 820 + 10 * math.sin((t - b["t0"]) * 3), 0.6 + 0.4 * pp, min(1, pp * 1.4))
    pc(base, "Incognito chat", 54, (255, 255, 255), INKD, 540, 1010, t, T("incog", 19), 0, pad=(34, 10), r=24)
    for txt, k, y in (("NO HISTORY", 25, 1130), ("NO MEMORY", 27, 1230), ("NO TRAINING", 33, 1330)):
        pc(base, txt, 60, RED, (255, 255, 255), 540, y, t, T("incog", k), (-1.5, 1, -1)[(25, 27, 33).index(k)], pad=(44, 10), r=28)
    srcline(base, SRC2, 1445)


def s_c2(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "CAUTION", 76, RED, (255, 255, 255), 540, 230, t, b["t0"] + 0.1, -1.5, pad=(46, 12), r=32)
    w, h = 800, 300; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=(10, 10, 14, 255), outline=(255, 255, 255, 255), width=6)
    d.text((40, 30), "Incognito chat", font=font(44), fill=(255, 255, 255, 255)); d.line([(w - 90, 40), (w - 50, 80)], fill=(255, 255, 255, 255), width=8); d.line([(w - 50, 40), (w - 90, 80)], fill=(255, 255, 255, 255), width=8)
    d.text((40, 150), "important notes...", font=font(40), fill=(170, 170, 176, 255))
    tc, tg = T("caution2", 7), T("caution2", 9)
    if t >= b["t0"] + 0.3:
        al = 1.0 - 0.75 * min(1, max(0, (t - tg) / 0.45));
        if al > 0.02:
            card_enter(base, im if al > 0.99 else Image.blend(Image.new("RGBA", im.size, (0, 0, 0, 0)), im, al), 540, 520, t, b["t0"] + 0.3)
    pc(base, "CLOSED = GONE", 84, RED, (255, 255, 255), 540, 800, t, T("caution2", 7), 1.5, pad=(44, 12), r=32)
    pc(base, "COPY FIRST", 76, GREEN, (255, 255, 255), 540, 1020, t, T("caution2", 14), -1.5, pad=(44, 12), r=32)
    pc(base, "NOT INSIDE PROJECTS", 56, INKD, (255, 255, 255), 540, 1230, t, T("caution2", 19), 1, pad=(40, 12), r=28)
    srcline(base, SRC2, 1425)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, ImageOps.mirror(robot(720)), 540, 640 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill, sz) in enumerate((("+ FOLLOW", T("cta", 6), ACC, 78), ("MORE USEFUL CLAUDE TIPS", T("cta", 2), INKD, 46))):
        pp = pop(t, ts); place(base, chip(txt, sz, fill, (255, 255, 255), pad=(44, 10), r=30), 540, 1170 + 130 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("train", 0)), dict(k="train", t0=T("train", 0), t1=T("caution1", 0)), dict(k="c1", t0=T("caution1", 0), t1=T("incog", 0)),
     dict(k="incog", t0=T("incog", 0), t1=T("caution2", 0)), dict(k="c2", t0=T("caution2", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, train=s_train, c1=s_c1, incog=s_incog, c2=s_c2, cta=s_cta)
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
    build_audio(HERE / "audio/voice.wav")
    n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()




