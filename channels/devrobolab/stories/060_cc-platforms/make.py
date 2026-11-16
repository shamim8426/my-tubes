"""060 Claude Code 07 (Platforms) Short. Dark terminal demo + official-page crops (own Playwright capture), accent SKY, light-blue paper for doc beats.
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
PINK = (2, 132, 199); PINKL = (125, 211, 252); INKD = (30, 30, 36); GREEN = (22, 163, 74); RED = (225, 45, 57); YEL = (255, 214, 10); OR = (217, 119, 87)


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
    im = Image.new("RGB", (W, H), (245, 250, 255)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(245 - 10 * k), int(250 - 8 * k), 255))
    d.ellipse([-200, 500, 900, 1500], fill=(190, 225, 250)); im = im.filter(ImageFilter.GaussianBlur(140)); d = ImageDraw.Draw(im)
    for x in range(0, W, 72): d.line([(x, 0), (x, H)], fill=(228, 238, 250), width=1)
    for y in range(0, H, 72): d.line([(0, y), (W, y)], fill=(228, 238, 250), width=1)
    return im.convert("RGBA")
BGP = bg_paper()
BGK = Image.new("RGBA", (W, H), (8, 8, 12, 255))


def with_border(img, r=18, bw=5):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=bw); return o


def crop_w(name, box, w):
    c = Image.open(HERE / f"raw/{name}.png").convert("RGB").crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)


def crop_b(name, box, w): return with_border(crop_w(name, box, w))
HEAD = crop_b("shot_top", (30, 820, 720, 925), 800)
CLIR = crop_b("shot_cli", (30, 925, 1000, 1090), 980)
IDER = crop_b("shot_cli", (30, 1085, 1040, 1415), 980)
WEBR = crop_b("shot_web", (1070, 944, 1985, 1060), 940)
NOTE = crop_b("shot_web", (30, 1285, 1190, 1345), 980)
NOTE2 = crop_b("shot_web", (970, 1285, 1606, 1345), 740)
TOOLR = crop_b("shot_tools", (30, 960, 1150, 1415), 980)
SRC = "Official docs: code.claude.com / Platforms"


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
    "hook": [(0, "Claude Code KAHAN chalayein?"), (5, "TERMINAL"), (7, "VS CODE"), (10, "Ya FONE se?"), (13, "OFFICIAL DOCS me jawab")],
    "cli": [(0, "Pehla: CLI"), (2, "Yani TERMINAL window"), (14, "Sabse COMPLETE"), (18, "SCRIPTING + AGENT SDK"), (22, "Sirf yahin")],
    "ide": [(0, "Terminal pasand nahi?"), (3, "VS CODE ya JETBRAINS"), (10, "Badlav seedha EDITOR me"), (17, "DESKTOP app: visual review")],
    "web": [(0, "WEB: Claude CLOUD me chalta hai"), (7, "DISCONNECT ho jao"), (11, "Task chalta rahega"), (18, "FONE se shuru karo")],
    "tools": [(0, "Aur TOOLS jodna hai?"), (4, "CHROME: browser chalao"), (8, "GITHUB ACTIONS: CI me review"), (15, "SLACK me @Claude")],
    "caution": [(0, "Dhyan rakho!"), (2, "Har surface par har FEATURE nahi"), (9, "Kuch cheezein sirf CLI me"), (15, "Apne KAAM ke hisaab se chuno")],
    "cta": [(0, "Claude Code ke aur TIPS?"), (6, "Channel ko FOLLOW kijiye")],
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
            if k == 0: d.text((36, y), ">", font=f, fill=(150, 150, 150, 255))
            x = 36 + cw * 2; seg = p["text"][s:e]
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


def pc(base, txt, size, fill, color, cx, cy, t, ts, rot=0, pad=(36, 10), r=26, hl=None):
    if t >= ts - 0.02:
        pp = pop(t, ts); place(base, chip(txt, size, fill, color, pad=pad, r=r, hl=hl), cx, cy, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)


def note(base, txt, y): place(base, chip(txt, 24, (40, 40, 40), (200, 200, 200), pad=(20, 5), r=12), 540, y)
DK = (30, 30, 36); WH = (255, 255, 255)


def s_hook(base, t, b):
    base.alpha_composite(BGP)
    card_enter(base, HEAD, 540, 330, t, b["t0"], rot=-0.8, dur=0.01)
    pc(base, "WHERE TO RUN IT?", 86, PINK, WH, 540, 570, t, b["t0"] + 0.2, -1.5, pad=(46, 14), r=34)
    pc(base, "TERMINAL", 74, DK, WH, 300, 800, t, T("hook", 5), -2, pad=(44, 12), r=30)
    pc(base, "VS CODE", 74, WH, DK, 760, 950, t, T("hook", 7), 2, pad=(44, 12), r=30)
    pc(base, "PHONE", 74, PINK, WH, 340, 1100, t, T("hook", 11), -1.5, pad=(44, 12), r=30)
    pc(base, "OFFICIAL DOCS", 58, (70, 70, 80), (235, 235, 240), 540, 1250, t, T("hook", 13), 1, pad=(40, 12), r=30)
    srcline(base, 1420)


def s_cli(base, t, b):
    base.alpha_composite(BGK)
    p1, p2 = T("cli", 3), T("cli", 18)
    pr = [dict(text="claude", hl="claude", a=p1, b=p1 + 0.7),
          dict(text="claude -p \"list todo comments\"", hl="-p", a=p2, b=p2 + 1.8)]
    win = term(t, 980, 640, pr, extra={1: (p2 + 2.2, "prints answer, then exits")})
    lt = t - b["t0"]; sc = 0.94 + 0.06 * ease_out(min(1, lt / 0.3))
    place(base, shadow(980, 640, 24, 40, 40, 150), 540, 600, sc); place(base, win, 540, 600, sc)
    banner(base, t, [("CLI = TERMINAL", b["t0"], T("cli", 18)), ("SCRIPTING + AGENT SDK", T("cli", 18), b["t1"])], y=215)
    if t >= T("cli", 14): card_enter(base, NOTE, 540, 1060, t, T("cli", 14), rot=0.5, side=1)
    if t >= T("cli", 14): pc(base, "MOST COMPLETE", 66, PINK, WH, 540, 1200, t, T("cli", 15), -1.2, pad=(40, 12), r=30)
    note(base, "Example commands (illustration)", 1345)
    place(base, chip(SRC, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, 1410)


def diffcard(t, t0):
    w, h = 940, 330; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=(13, 13, 13, 255), outline=(60, 60, 60, 255), width=2)
    d.rounded_rectangle([0, 0, w - 1, 56], 24, fill=(30, 30, 30, 255)); d.rectangle([0, 28, w, 56], fill=(30, 30, 30, 255))
    d.text((30, 12), "editor  -  auth.ts   (illustration)", font=PM(24), fill=(150, 150, 150, 255))
    d.rectangle([20, 100, w - 20, 170], fill=(90, 30, 36, 255)); d.text((40, 110), "- if (user = admin)", font=PM(40), fill=(255, 150, 150, 255))
    if t >= t0 + 0.5: d.rectangle([20, 190, w - 20, 260], fill=(24, 80, 44, 255)); d.text((40, 200), "+ if (user === admin)", font=PM(40), fill=(150, 255, 180, 255))
    return im


def s_ide(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "VS CODE", 70, DK, WH, 290, 215, t, T("ide", 4), -2, pad=(44, 12), r=30)
    pc(base, "JETBRAINS", 70, WH, DK, 770, 215, t, T("ide", 7), 2, pad=(44, 12), r=30)
    card_enter(base, IDER, 540, 520, t, b["t0"] + 0.05, rot=0.5, side=1)
    if t >= T("ide", 10): card_enter(base, diffcard(t, T("ide", 10)), 540, 940, t, T("ide", 10), rot=-0.6, side=0)
    pc(base, "DESKTOP APP", 62, PINK, WH, 540, 1190, t, T("ide", 17), -1.2, pad=(40, 12), r=30)
    pc(base, "VISUAL REVIEW", 50, DK, WH, 300, 1290, t, T("ide", 20), -1.5, pad=(30, 10), r=26)
    pc(base, "PARALLEL SESSIONS", 50, DK, WH, 740, 1370, t, T("ide", 23), 1.5, pad=(30, 10), r=26)
    srcline(base, 1450)


def s_web(base, t, b):
    base.alpha_composite(BGK)
    pc(base, "WEB = CLOUD", 86, PINK, WH, 540, 260, t, b["t0"] + 0.2, -1.2, pad=(46, 14), r=34)
    card_enter(base, WEBR, 540, 470, t, b["t0"] + 0.3, rot=0.5, side=1)
    pc(base, "YOU: OFFLINE", 66, RED, WH, 300, 760, t, T("web", 8), -2, pad=(40, 12), r=30)
    pc(base, "TASK: RUNNING", 66, GREEN, WH, 760, 910, t, T("web", 12), 2, pad=(40, 12), r=30)
    if t >= T("web", 12):
        pp = (t * 1.5) % 1; bw = 760; d = ImageDraw.Draw(base); x0 = 160
        d.rounded_rectangle([x0, 1060, x0 + bw, 1090], 15, fill=(60, 60, 70, 255)); d.rounded_rectangle([x0, 1060, x0 + int(bw * (0.15 + 0.85 * pp)), 1090], 15, fill=GREEN + (255,))
    pc(base, "START FROM PHONE", 60, WH, DK, 540, 1220, t, T("web", 18), -1, pad=(40, 12), r=30)
    note(base, "Progress bar is an illustration", 1300)
    place(base, chip(SRC, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, 1410)


def s_tools(base, t, b):
    base.alpha_composite(BGP)
    card_enter(base, TOOLR, 540, 450, t, b["t0"] + 0.2, rot=-0.5, side=1)
    pc(base, "CHROME", 66, PINK, WH, 280, 830, t, T("tools", 4), -2, pad=(40, 12), r=30)
    pc(base, "GITHUB ACTIONS", 62, DK, WH, 640, 960, t, T("tools", 8), 1.5, pad=(40, 12), r=30)
    pc(base, "SLACK  @Claude", 66, WH, DK, 480, 1090, t, T("tools", 16), -1.5, pad=(40, 12), r=30)
    pc(base, "BROWSER  -  CI  -  CHAT", 48, (70, 70, 80), (235, 235, 240), 540, 1230, t, T("tools", 18), 1, pad=(34, 10), r=26)
    srcline(base, 1420)


def s_caution(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "NOT EVERYTHING EVERYWHERE", 62, RED, WH, 540, 260, t, b["t0"] + 0.2, -1.2, pad=(40, 14), r=32)
    card_enter(base, NOTE, 540, 480, t, T("caution", 2), rot=-0.4, side=1)
    card_enter(base, NOTE2, 540, 620, t, T("caution", 9), rot=0.5, side=1)
    pc(base, "CLI ONLY", 90, DK, WH, 300, 900, t, T("caution", 12), -2, pad=(50, 14), r=34)
    pc(base, "SCRIPTING", 58, WH, DK, 780, 860, t, T("caution", 12) + 0.15, 2, pad=(36, 10), r=26)
    pc(base, "AGENT SDK", 58, WH, DK, 740, 980, t, T("caution", 12) + 0.3, -1, pad=(36, 10), r=26)
    pc(base, "PICK BY YOUR WORK", 70, PINK, WH, 540, 1200, t, T("caution", 16), 1.5, pad=(44, 14), r=32)
    srcline(base, 1420)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, ImageOps.mirror(robot(720)), 540, 640 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill, sz) in enumerate((("+ FOLLOW", T("cta", 6), PINK, 78), ("MORE CLAUDE CODE TIPS", T("cta", 4), INKD, 50))):
        pp = pop(t, ts); place(base, chip(txt, sz, fill, WH, pad=(44, 10), r=30), 540, 1170 + 130 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


def banner(base, t, items, y=250, dark=False):
    for txt, ts, te in items:
        if ts <= t < te: pp = pop(t, ts + 0.03); place(base, chip(txt, 46, PINK, WH, pad=(30, 9), r=26), 540, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


SEQ = ["hook", "cli", "ide", "web", "tools", "caution", "cta"]
B = [dict(k=k, t0=(0.0 if i == 0 else T(SEQ[i], 0)), t1=(T(SEQ[i + 1], 0) if i + 1 < len(SEQ) else TOTAL + 1)) for i, k in enumerate(SEQ)]
FN = dict(hook=s_hook, cli=s_cli, ide=s_ide, web=s_web, tools=s_tools, caution=s_caution, cta=s_cta)
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
