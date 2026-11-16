"""052 Claude Code 05 (Prompt library) Short. Dark terminal demo + official-page crops (own Playwright capture), accent PINK, cream-pink paper for doc beats.
Run: python make.py frames t1 t2 ...  |  python make.py (render)  |  python make.py range t0 t1 out.mp4"""
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
PINK = (232, 62, 140); PINKL = (255, 150, 200); INKD = (30, 30, 36); GREEN = (22, 163, 74); RED = (225, 45, 57); YEL = (255, 214, 10); OR = (217, 119, 87)


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(str(ROOT / "shared/fonts/Poppins-Bold.ttf"), sz)
    return _fc[sz]
PM = lambda sz: ImageFont.truetype(str(ROOT / "shared/fonts/IBMPlexMono-Bold.ttf"), sz)
PF = lambda sz, bold=False: ImageFont.truetype(str(ROOT / ("shared/fonts/Poppins-Bold.ttf" if bold else "shared/fonts/Poppins-Medium.ttf")), sz)


def chip(text, size, fill, color=(255, 255, 255), pad=(34, 14), r=26, hl=None, hlcolor=PINKL):
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
    im = Image.new("RGB", (W, H), (255, 249, 246)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(255 - 6 * k), int(249 - 14 * k), int(246 - 10 * k)))
    d.ellipse([-200, 500, 900, 1500], fill=(255, 205, 228)); im = im.filter(ImageFilter.GaussianBlur(140)); d = ImageDraw.Draw(im)
    for x in range(0, W, 72): d.line([(x, 0), (x, H)], fill=(250, 236, 240), width=1)
    for y in range(0, H, 72): d.line([(0, y), (W, y)], fill=(250, 236, 240), width=1)
    return im.convert("RGBA")
BGP = bg_paper()
BGK = Image.new("RGBA", (W, H), (8, 8, 12, 255))


def with_border(img, r=18, bw=5):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=bw); return o


def crop_w(name, box, w):
    c = Image.open(HERE / f"raw/{name}.png").convert("RGB").crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)


TITLE = with_border(crop_w("shot_top", (30, 310, 1010, 545), 940))
PILLS = with_border(crop_w("shot_top", (60, 1095, 1160, 1285), 940))
CROPA = with_border(crop_w("shot_start", (395, 805, 1065, 870), 940))
CROPB = crop_w("shot_start", (1055, 805, 1955, 870), 940); WHYBOX = (99 * 940 / 900, 0, 337 * 940 / 900, CROPB.height)
CROPB = with_border(CROPB)
SRC = "Official docs: code.claude.com / Prompt library"


def srcline(base, y=1425):
    place(base, chip(SRC, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, y)


def banner(base, t, items, y=250, dark=False):
    for txt, ts, te in items:
        if ts <= t < te: pp = pop(t, ts + 0.03); place(base, chip(txt, 46, PINK, (255, 255, 255), pad=(30, 9), r=26), 540, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def keycap(base, txt, cx, cy, t, t0):
    if t < t0 - 0.05: return
    lt = t - t0; press = 0.06 * max(0, 1 - lt / 0.25); pp = pop(t, t0 - 0.05)
    place(base, chip(txt, 52, (245, 245, 247), INKD, pad=(44, 12), r=20), cx, cy + 6, (0.7 + 0.3 * pp) - press, min(1, pp * 1.4))


# ---- captions ----
CAPTXT = {
    "hook": [(0, "Claude Code me kya likhein?"), (5, "Samajh nahi aata?"), (8, "OFFICIAL PROMPT LIBRARY me"), (12, "COPY-PASTE prompts milte hain")],
    "what": [(0, "Ye docs ka ek page hai"), (6, "Prompts TASK aur ROLE"), (12, "ke hisaab se tag hain"), (17, "COPY karo, PASTE karo")],
    "patterns": [(0, "Teen PATTERN seekho"), (3, "1: Steps nahi, OUTCOME batao"), (8, "2: Check ka tareeka do"), (13, "jaise RUN karke CONFIRM karo"), (18, "3: AT-SIGN se file dikhao")],
    "caution": [(0, "Dhyan rakho!"), (2, "Ye scripts nahi,"), (5, "STARTING POINTS hain"), (9, "WHY THIS WORKS kholo,"), (13, "PATTERN samjho"), (16, "Aur apna prompt likho")],
    "tip": [(0, "Kaam ka prompt mile to"), (6, "SKILL bana lo"), (9, "Phir SLASH command se chalega")],
    "cta": [(0, "Claude Code seekhte rehna hai?"), (5, "DevRoboLab ko FOLLOW karo"), (9, "Roz naya TIP aayega")],
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


# ---- terminal ----
def wrap_idx(text, n):
    lines = []; s = 0
    while s < len(text):
        e = min(len(text), s + n)
        if e < len(text):
            sp = text.rfind(" ", s, e + 1)
            if sp > s: e = sp
        lines.append((s, e)); s = e + (1 if e < len(text) and text[e] == " " else 0)
    return lines


def term(t, w, h, prompts, extra=None):
    """prompts: list of dict(text, hl, a, b) typed from a to b; older ones dimmed"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=(13, 13, 13, 255), outline=(60, 60, 60, 255), width=2)
    d.rounded_rectangle([0, 0, w - 1, 60], 24, fill=(30, 30, 30, 255)); d.rectangle([0, 30, w, 60], fill=(30, 30, 30, 255))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))): d.ellipse([24 + 30 * i, 20, 44 + 30 * i, 40], fill=c + (255,))
    d.text((130, 14), "claude  -  Terminal", font=PM(24), fill=(150, 150, 150, 255))
    d.text((36, 84), "* Claude Code", font=PM(40), fill=OR + (255,))
    f = PM(40); y = 170; cw = f.getlength("M"); n = int((w - 110) / cw)
    cur = max([i for i, p in enumerate(prompts) if t >= p["a"]] or [-1])
    for i, p in enumerate(prompts):
        if t < p["a"]: break
        frac = min(1, max(0, (t - p["a"]) / max(0.1, p["b"] - p["a"]))); nc = int(len(p["text"]) * frac)
        hs = p["text"].find(p["hl"]) if p.get("hl") else -1; he = hs + len(p["hl"]) if hs >= 0 else -1
        for k, (s, e) in enumerate(wrap_idx(p["text"], n)):
            x = 36 + (cw * 2 if k else 0)
            if k == 0: d.text((36, y), ">", font=f, fill=(150, 150, 150, 255))
            x = 36 + cw * 2
            seg = p["text"][s:e]
            for ci, ch in enumerate(seg):
                gi = s + ci
                if gi >= nc: break
                col = PINKL if hs <= gi < he else ((235, 235, 235) if i == cur else (120, 120, 126))
                d.text((x, y), ch, font=f, fill=col + (255,)); x += cw
            if i == cur and nc < len(p["text"]) and s <= nc < e + 1 and int(t * 3) % 2 == 0: d.rectangle([x + 2, y + 4, x + 16, y + 40], fill=(235, 235, 235, 255))
            y += 56
        y += 34
        if extra and extra.get(i) is not None and t >= extra[i][0]:
            d.ellipse([60, y - 8, 104, y + 36], fill=GREEN + (255,)); d.line([(70, y + 14), (79, y + 24), (95, y + 4)], fill=(255, 255, 255, 255), width=6)
            d.text((124, y - 6), extra[i][1], font=PM(34), fill=(74, 222, 128, 255)); y += 70
    return im


# ---- scenes ----
def s_hook(base, t, b):
    base.alpha_composite(BGP)
    card_enter(base, TITLE, 540, 400, t, b["t0"], rot=-1.0, dur=0.01)
    card_enter(base, PILLS, 540, 640, t, b["t0"] + 0.15, rot=1.0, side=1)
    if t >= T("hook", 8) - 0.1:
        pp = pop(t, T("hook", 8) - 0.1); place(base, chip("OFFICIAL  PROMPT LIBRARY", 62, PINK, (255, 255, 255), pad=(40, 12), r=30), 540, 900, 0.7 + 0.3 * pp, min(1, pp * 1.4), 1.2)
    card_enter(base, chip("COPY-PASTE PROMPTS", 84, (30, 30, 36), (255, 255, 255), hl={"PROMPTS"}, pad=(46, 14), r=34), 540, 1090, t, T("hook", 12) - 0.2, side=0)
    card_enter(base, chip("FOR CLAUDE CODE", 64, (255, 255, 255), INKD, pad=(40, 10), r=30), 540, 1260, t, T("hook", 13), side=1)
    srcline(base, 1390)


def s_what(base, t, b):
    base.alpha_composite(BGP)
    card_enter(base, PILLS, 540, 360, t, b["t0"], rot=0.8, dur=0.01)
    for txt, ts, y, rot in (("BY TASK", T("what", 7), 570, -1.5), ("BY ROLE", T("what", 10), 570, 1.5)):
        if t >= ts - 0.02:
            pp = pop(t, ts); place(base, chip(txt, 62, PINK if txt == "BY TASK" else (30, 30, 36), (255, 255, 255), pad=(36, 10), r=26), 300 if txt == "BY TASK" else 780, y, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)
    # copy -> paste
    tc = T("what", 17) - 0.1
    pr = [dict(text="give me an overview of this codebase", hl="overview", a=tc + 0.5, b=tc + 1.3)]
    card_enter(base, term(t, 940, 480, pr), 540, 950, t, b["t0"] + 0.3, side=0)
    keycap(base, "COPY", 300, 1270, t, tc); keycap(base, "PASTE", 780, 1270, t, tc + 0.35)
    srcline(base, 1410)


def s_patterns(base, t, b):
    base.alpha_composite(BGK)
    p1, p2, p3 = T("patterns", 3), T("patterns", 8), T("patterns", 18) - 0.3
    pr = [dict(text="add rate limiting to the public API and make sure existing tests still pass", hl="add rate limiting to the public API", a=p1, b=p1 + 1.5),
          dict(text="write the migration, run it against the dev database, and confirm the schema matches", hl="run it against the dev database, and confirm", a=p2 - 0.2, b=p2 + 2.0),
          dict(text="why is the build failing? @build.log", hl="@build.log", a=p3, b=p3 + 1.4)]
    win = term(t, 980, 800, pr, extra={1: (T("patterns", 17), "run + confirm: checked")})
    lt = t - b["t0"]; sc = 0.94 + 0.06 * ease_out(min(1, lt / 0.3))
    place(base, shadow(980, 800, 24, 40, 40, 150), 540, 740, sc); place(base, win, 540, 740, sc)
    banner(base, t, [("PATTERN 1  OUTCOME, NOT STEPS", b["t0"], p2 - 0.2), ("PATTERN 2  GIVE A WAY TO CHECK", p2 - 0.2, p3), ("PATTERN 3  POINT AT A FILE", p3, b["t1"])], y=215)
    keycap(base, "@", 540, 1290, t, T("patterns", 19) - 0.2)
    place(base, chip("Example prompts from the official page", 24, (40, 40, 40), (200, 200, 200), pad=(20, 5), r=12), 540, 1215)


def s_caution(base, t, b):
    base.alpha_composite(BGP)
    card_enter(base, CROPA, 540, 330, t, b["t0"], rot=-0.8, dur=0.01)
    if t >= T("caution", 2) + 0.1:
        pp = ease_back((t - T("caution", 2) - 0.1) / 0.3); sub = Image.new("RGBA", (300, 110), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub)
        sd.rounded_rectangle([0, 0, 299, 109], 24, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5); sd.text((26, 22), "SCRIPTS", font=PF(48, True), fill=GREY + (255,) if False else (120, 120, 126, 255))
        sd.line([(20, 56), (280, 56)], fill=RED + (255,), width=8); place(base, sub, 330, 580, 0.6 + 0.4 * min(1, pp), min(1, pp * 1.4), -2)
    if t >= T("caution", 5): pp = pop(t, T("caution", 5)); place(base, chip("STARTING POINTS", 58, PINK, (255, 255, 255), pad=(34, 10), r=26), 735, 590, 0.6 + 0.4 * pp, min(1, pp * 1.4), 2)
    if t >= T("caution", 9) - 0.15:
        card_enter(base, CROPB, 540, 860, t, T("caution", 9) - 0.15, rot=0.8, side=1)
        pp = ease_out((t - T("caution", 9)) / 0.3) if t >= T("caution", 9) else 0
        if pp > 0:
            x0 = 540 - CROPB.width / 2 + WHYBOX[0]; x1 = 540 - CROPB.width / 2 + WHYBOX[2]; y0 = 860 - CROPB.height / 2
            ImageDraw.Draw(base).rounded_rectangle([x0 - 6, y0 - 8, x0 + (x1 - x0 + 12) * pp, y0 + CROPB.height + 8], 12, outline=PINK + (255,), width=7)
    if t >= T("caution", 13):
        pp = pop(t, T("caution", 13)); place(base, chip("SPOT THE PATTERN", 58, (30, 30, 36), (255, 255, 255), pad=(36, 10), r=26), 540, 1050, 0.6 + 0.4 * pp, min(1, pp * 1.4), -1)
    if t >= T("caution", 16):
        pp = pop(t, T("caution", 16)); place(base, chip("WRITE YOUR OWN", 72, PINK, (255, 255, 255), pad=(40, 12), r=30), 540, 1200, 0.6 + 0.4 * pp, min(1, pp * 1.4), 1.5)
    srcline(base, 1400)


def s_tip(base, t, b):
    base.alpha_composite(BGK)
    lt = t - b["t0"]
    flow = [("GOOD PROMPT", T("tip", 2), (255, 255, 255), INKD), ("SKILL", T("tip", 6), PINK, (255, 255, 255)), ("/COMMAND", T("tip", 11), YEL, INKD)]
    for i, (txt, ts, fill, tc) in enumerate(flow):
        y = 400 + 230 * i
        if t >= ts - 0.05:
            pp = pop(t, ts); place(base, chip(txt, 92, fill, tc, pad=(54, 16), r=38), 540, y, 0.6 + 0.4 * pp, min(1, pp * 1.4), (-1.5, 1.5, -1)[i])
        if i < 2 and t >= flow[i + 1][1] - 0.1:
            d = ImageDraw.Draw(base); ax = 540; ay = y + 105; d.polygon([(ax - 28, ay), (ax + 28, ay), (ax, ay + 40)], fill=PINKL + (255,))
    ts = T("tip", 11) - 0.2
    pr = [dict(text="/explain-codebase", hl="/explain-codebase", a=ts, b=ts + 0.9)]
    if t >= ts - 0.3: card_enter(base, term(t, 940, 330, pr), 540, 1180, t, ts - 0.3, side=0)
    place(base, chip("Example command name (illustration)", 24, (40, 40, 40), (200, 200, 200), pad=(20, 5), r=12), 540, 1360)
    place(base, chip(SRC, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, 1410)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, ImageOps.mirror(robot(720)), 540, 640 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill, sz) in enumerate((("+ FOLLOW", T("cta", 5), PINK, 78), ("A NEW TIP EVERY DAY", T("cta", 9), INKD, 54))):
        pp = pop(t, ts); place(base, chip(txt, sz, fill, (255, 255, 255), pad=(44, 10), r=30), 540, 1170 + 130 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("what", 0)), dict(k="what", t0=T("what", 0), t1=T("patterns", 0)), dict(k="patterns", t0=T("patterns", 0), t1=T("caution", 0)),
     dict(k="caution", t0=T("caution", 0), t1=T("tip", 0)), dict(k="tip", t0=T("tip", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, what=s_what, patterns=s_patterns, caution=s_caution, tip=s_tip, cta=s_cta)
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
    if len(sys.argv) > 1 and sys.argv[1] == "range":
        t0, t1 = float(sys.argv[2]), float(sys.argv[3]); out = sys.argv[4]; i0, i1 = int(t0 * FPS), int(t1 * FPS)
        encode((frame(i / FPS) for i in range(i0, i1)), i1 - i0, None, None, Path(out), music_start=0, music_gain_db=-22) if False else None
        print("range mode unsupported in this build; re-render fully"); return
    n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()

