"""055 Claude Code 06 (Best practices) Short. Dark terminal demo + official-page crops (own Playwright capture), accent INDIGO, lavender paper for doc beats.
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
PINK = (79, 70, 229); PINKL = (165, 180, 255); INKD = (30, 30, 36); GREEN = (22, 163, 74); RED = (225, 45, 57); YEL = (255, 214, 10); OR = (217, 119, 87)


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
    im = Image.new("RGB", (W, H), (247, 247, 255)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(247 - 10 * k), int(247 - 10 * k), int(255 - 4 * k)))
    d.ellipse([-200, 500, 900, 1500], fill=(205, 212, 255)); im = im.filter(ImageFilter.GaussianBlur(140)); d = ImageDraw.Draw(im)
    for x in range(0, W, 72): d.line([(x, 0), (x, H)], fill=(232, 234, 250), width=1)
    for y in range(0, H, 72): d.line([(0, y), (W, y)], fill=(232, 234, 250), width=1)
    return im.convert("RGBA")
BGP = bg_paper()
BGK = Image.new("RGBA", (W, H), (8, 8, 12, 255))


def with_border(img, r=18, bw=5):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=bw); return o


def crop_w(name, box, w):
    c = Image.open(HERE / f"raw/{name}.png").convert("RGB").crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)


TITLE = with_border(crop_w("shot_pass", (30, 715, 760, 800), 760))
PARA = with_border(crop_w("shot_pass", (30, 975, 1335, 1040), 1000))
TIP = with_border(crop_w("shot_hook", (30, 952, 1315, 1030), 1000))
SRC = "Official docs: code.claude.com / Best practices"


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
    "hook": [(0, "Claude Code ne kaha DONE?"), (5, "Par kaam ADHURA nikla?"), (9, "OFFICIAL BEST PRACTICES me"), (13, "iska HAL hai")],
    "what": [(0, "Baat seedhi hai"), (3, "Claude ko ek CHECK do"), (9, "Jo PASS ya FAIL bataye"), (14, "Jaise TEST, BUILD, LINTER")],
    "levels": [(0, "Teen TAREEKE hain"), (3, "1: PROMPT me likho"), (12, "2: SLASH GOAL se condition"), (19, "3: STOP HOOK lagao"), (23, "PASS hone tak rukne nahi dega")],
    "caution": [(0, "Dhyan rakho!"), (2, "Sirf DONE sunkar mat mano"), (7, "EVIDENCE mango"), (9, "Kaun sa COMMAND chala"), (14, "Aur uska OUTPUT")],
    "tip": [(0, "Jo RULE kabhi nahi tootna chahiye"), (6, "Use CLAUDE.md me nahi"), (9, "HOOK me daalo")],
    "cta": [(0, "Claude Code ke aur TIPS chahiye?"), (6, "DevRoboLab ko FOLLOW karo")],
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
def pc(base, txt, size, fill, color, cx, cy, t, ts, rot=0, pad=(36, 10), r=26, hl=None):
    if t >= ts - 0.02:
        pp = pop(t, ts); place(base, chip(txt, size, fill, color, pad=pad, r=r, hl=hl), cx, cy, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)


def s_hook(base, t, b):
    base.alpha_composite(BGP)
    card_enter(base, TITLE, 540, 400, t, b["t0"], rot=-1.0, dur=0.01)
    card_enter(base, PARA, 540, 600, t, b["t0"] + 0.15, rot=0.8, side=1)
    pc(base, "DONE?", 100, (255, 255, 255), INKD, 540, 880, t, T("hook", 4), -1.5, pad=(50, 12), r=36)
    pc(base, "BUT HALF-DONE", 78, RED, (255, 255, 255), 540, 1050, t, T("hook", 7), 1.5, pad=(44, 12), r=32)
    pc(base, "OFFICIAL  BEST PRACTICES", 58, PINK, (255, 255, 255), 540, 1220, t, T("hook", 9), -1, pad=(40, 12), r=30)
    pc(base, "FOR CLAUDE CODE", 64, (30, 30, 36), (255, 255, 255), 540, 1370, t, T("hook", 13), 1, pad=(40, 10), r=30)
    srcline(base, 1420)


def s_what(base, t, b):
    base.alpha_composite(BGP)
    card_enter(base, TITLE, 540, 330, t, b["t0"], rot=-0.8, dur=0.01)
    card_enter(base, PARA, 540, 520, t, b["t0"] + 0.1, rot=0.8, side=1)
    pc(base, "GIVE A CHECK", 88, PINK, (255, 255, 255), 540, 760, t, T("what", 3), -1.5, pad=(46, 14), r=34)
    pc(base, "PASS", 80, GREEN, (255, 255, 255), 300, 980, t, T("what", 10), -2, pad=(50, 12), r=32)
    pc(base, "FAIL", 80, RED, (255, 255, 255), 780, 980, t, T("what", 12), 2, pad=(50, 12), r=32)
    for txt, k, x, y in (("TEST", 15, 270, 1160), ("BUILD", 16, 790, 1160), ("LINTER", 18, 540, 1300)):
        pc(base, txt, 70, (30, 30, 36), (255, 255, 255), x, y, t, T("what", k), (-1.5, 1.5, -1)[(15, 16, 18).index(k)], pad=(44, 12), r=30)
    srcline(base, 1430)


def s_levels(base, t, b):
    base.alpha_composite(BGK)
    p1, p2, p3 = T("levels", 4), T("levels", 13), T("levels", 21)
    pr = [dict(text="fix auth.ts, run the auth tests after, and keep going until they pass", hl="keep going until they pass", a=p1, b=p1 + 2.2),
          dict(text="/goal all tests in tests/auth pass and lint is clean", hl="/goal", a=p2, b=p2 + 2.0),
          dict(text="Stop hook: tsc --noEmit || exit 2", hl="exit 2", a=p3, b=p3 + 1.6)]
    win = term(t, 980, 900, pr, extra={0: (T("levels", 11) + 0.3, "tests pass: done"), 1: (T("levels", 18) + 0.3, "goal met"), 2: (T("levels", 29), "tsc passes: turn ends")})
    lt = t - b["t0"]; sc = 0.94 + 0.06 * ease_out(min(1, lt / 0.3))
    place(base, shadow(980, 900, 24, 40, 40, 150), 540, 790, sc); place(base, win, 540, 790, sc)
    banner(base, t, [("WAY 1  IN THE PROMPT", b["t0"], T("levels", 12)), ("WAY 2  /GOAL", T("levels", 12), T("levels", 19)), ("WAY 3  STOP HOOK", T("levels", 19), b["t1"])], y=215)
    place(base, chip("Example commands (illustration)", 24, (40, 40, 40), (200, 200, 200), pad=(20, 5), r=12), 540, 1290)


def s_caution(base, t, b):
    base.alpha_composite(BGP)
    if t >= T("caution", 2) - 0.05:
        pp = pop(t, T("caution", 2) - 0.05); sub = chip("DONE", 96, (255, 255, 255), (120, 120, 126), pad=(54, 14), r=36)
        ImageDraw.Draw(sub).line([(20, sub.height // 2), (sub.width - 20, sub.height // 2)], fill=RED + (255,), width=10)
        place(base, sub, 540, 330, 0.6 + 0.4 * pp, min(1, pp * 1.4), -2)
    pc(base, "ASK FOR EVIDENCE", 82, PINK, (255, 255, 255), 540, 560, t, T("caution", 7), 1.5, pad=(44, 14), r=34)
    # fake terminal evidence card
    w, h = 940, 360; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=(13, 13, 13, 255), outline=(60, 60, 60, 255), width=2)
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))): d.ellipse([24 + 30 * i, 20, 44 + 30 * i, 40], fill=c + (255,))
    if t >= T("caution", 9): d.text((40, 100), "$ pnpm test auth", font=PM(44), fill=PINKL + (255,))
    if t >= T("caution", 14): d.text((40, 200), "24 passed, 0 failed", font=PM(46), fill=(74, 222, 128, 255))
    card_enter(base, im, 540, 900, t, T("caution", 8), rot=-0.6, side=0)
    pc(base, "COMMAND", 56, (30, 30, 36), (255, 255, 255), 300, 1160, t, T("caution", 10), -1.5, pad=(34, 10), r=26)
    pc(base, "OUTPUT", 56, GREEN, (255, 255, 255), 790, 1160, t, T("caution", 15), 1.5, pad=(34, 10), r=26)
    place(base, chip("Example output (illustration)", 24, (40, 40, 40), (200, 200, 200), pad=(20, 5), r=12), 540, 1290)
    srcline(base, 1400)


def s_tip(base, t, b):
    base.alpha_composite(BGK)
    pc(base, "NEVER READ .ENV", 70, (255, 255, 255), INKD, 540, 330, t, b["t0"] + 0.2, -1.5, pad=(46, 14), r=34)
    pc(base, "IN CLAUDE.md = ALMOST ALWAYS", 50, (70, 70, 80), (235, 235, 240), 540, 600, t, T("tip", 7), 1, pad=(36, 12), r=28)
    pc(base, "IN A HOOK = ALWAYS", 68, PINK, (255, 255, 255), 540, 870, t, T("tip", 10), -1.5, pad=(44, 14), r=32)
    if t >= T("tip", 9): card_enter(base, TIP, 540, 1200, t, T("tip", 9), rot=0.6, side=1)
    place(base, chip("Rule example from the official page", 24, (40, 40, 40), (200, 200, 200), pad=(20, 5), r=12), 540, 1370)
    place(base, chip(SRC, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, 1430)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, ImageOps.mirror(robot(720)), 540, 640 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill, sz) in enumerate((("+ FOLLOW", T("cta", 6), PINK, 78), ("MORE CLAUDE CODE TIPS", T("cta", 4), INKD, 50))):
        pp = pop(t, ts); place(base, chip(txt, sz, fill, (255, 255, 255), pad=(44, 10), r=30), 540, 1170 + 130 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=T("what", 0)), dict(k="what", t0=T("what", 0), t1=T("levels", 0)), dict(k="levels", t0=T("levels", 0), t1=T("caution", 0)),
     dict(k="caution", t0=T("caution", 0), t1=T("tip", 0)), dict(k="tip", t0=T("tip", 0), t1=T("cta", 0)), dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1)]
FN = dict(hook=s_hook, what=s_what, levels=s_levels, caution=s_caution, tip=s_tip, cta=s_cta)
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

