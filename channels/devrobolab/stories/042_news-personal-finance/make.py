"""AI News Short: Personal Finance in Claude, STYLE V5 (brand/STYLE_V5.md). Real official-page screenshots (raw/article.png, own Playwright capture,
key sentences marked) on dark grid cards with scroll + cursor, robot beats on white, number card, opaque caption chips, stacked CTA lock-up.
Run: python make.py [render]   (needs audio/tts/s_*.wav, wt.json, raw/article.png, raw/rects.json)"""
import json, math, re, sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import W, H, FPS, ease_out, ease_back, ease_io, wav_dur, encode

LEAD, AFTER = 0.05, 0.05
FONT = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf")
YEL = (255, 214, 10); INK = (17, 17, 20); VIO = (79, 70, 229); RED = (225, 45, 57); BLUE = (37, 99, 235)
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START))


def T(scene, k):  # absolute time of token k of a scene
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]


def chip(text, size, fill, color=(255, 255, 255), pad=(34, 14), r=26, hl=None, hlcolor=YEL):
    """opaque rounded chip -> RGBA PIL image; hl = set of words tinted"""
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


# ---------- backgrounds ----------
def bg_dark():
    im = Image.new("RGB", (W, H), (14, 15, 20)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(24, 26, 34), width=2)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(24, 26, 34), width=2)
    return im.convert("RGBA")


def bg_light():
    im = Image.new("RGB", (W, H), (250, 248, 242)); d = ImageDraw.Draw(im)
    for y in range(0, H, 96): d.line([(0, y), (W, y)], fill=(238, 235, 226), width=2)
    return im.convert("RGBA")


BGD, BGL = bg_dark(), bg_light()
MASC = {k: Image.open(ROOT / f"channels/devrobolab/mascot/cut/{k}.png").convert("RGBA") for k in ("wave", "think", "work", "stop")}


def robot(name, h):
    m = MASC[name]; return m.resize((int(m.width * h / m.height), h), Image.LANCZOS)


# ---------- article ----------
ART = Image.open(HERE / "raw/article.png").convert("RGB"); RJ = json.load(open(HERE / "raw/rects.json"))
CW, CH, CX, CY = 920, 860, 540, 800          # card size + centre
SCALE = CW / ART.width; ARTS = ART.resize((CW, int(ART.height * SCALE)), Image.LANCZOS)
SRC = "Official page: claude.com / Introducing Personal Finance in Claude"


def rect(k):  # rect of highlight in card pixels
    x, y, w, h = RJ["rects"][k]; s = 2 * SCALE; return x * s, y * s, w * s, h * s


def card_img(focus_y, drift):
    """CW x CH window of the article centred at focus_y (+ small scroll drift) with rounded corners -> RGBA, plus top-y offset"""
    y0 = int(max(0, min(ARTS.height - CH, focus_y - CH * 0.42 + drift)))
    win = ARTS.crop((0, y0, CW, y0 + CH)).convert("RGBA"); m = Image.new("L", win.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, CW - 1, CH - 1], 34, fill=255); win.putalpha(m); return win, y0


def cursor_spr():
    im = Image.new("RGBA", (70, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(6, 4), (6, 62), (22, 48), (34, 76), (46, 70), (34, 44), (56, 44)]
    d.polygon([(x + 3, y + 3) for x, y in pts], fill=(0, 0, 0, 90)); d.polygon(pts, fill=(255, 255, 255, 255), outline=(10, 10, 10, 255)); return im


CUR = cursor_spr()


def persp(img, tilt):
    """simple 3D tilt (page-flip feel) of an RGBA image about the vertical axis; tilt in 0..1 (1 = strongest)"""
    if tilt <= 0.01: return img
    a = np.array(img); h, w = a.shape[:2]; k = 0.14 * tilt * h
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]]); dst = np.float32([[0, k], [w, 0], [w, h], [0, h - k]])
    return Image.fromarray(cv2.warpPerspective(a, cv2.getPerspectiveTransform(src, dst), (w, h), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0)))


def src_line(base, y=1275, text=SRC):
    place(base, chip(text, 34, (40, 44, 58), (235, 235, 240), pad=(26, 8), r=18), W / 2, y)


def ui_beat(base, t, b):
    """real screenshot card on the dark grid: slow scroll, push-in, cursor to the highlighted line, optional tilt entry"""
    p = (t - b["t0"]) / (b["t1"] - b["t0"]); lt = t - b["t0"]
    rx, ry, rw, rh = rect(b["key"]); focus = ry + rh / 2
    img, y0 = card_img(focus, (p - 0.5) * 70)
    scale = (0.94 + 0.06 * ease_out(lt / 0.3)) * (1 + 0.04 * p)
    tilt = max(0, 1 - lt / 0.38) if b.get("tilt") else 0
    c = persp(img, tilt)
    sh = Image.new("RGBA", (CW + 80, CH + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([40, 56, CW + 40, CH + 56], 38, fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(22))
    place(base, sh, CX, CY, scale); place(base, c, CX, CY, scale)
    # cursor: from below-right to the start of the highlighted line, then drifts along it
    tx, ty = CX - CW / 2 + rx + min(rw, 380) * 0.85, CY - CH / 2 + (ry + rh / 2 - y0)
    sx, sy = CX + CW * 0.45, CY + CH * 0.55; q = ease_io((lt - 0.15) / 0.7)
    cx = sx + (tx - sx) * q + 40 * math.sin(lt * 2.0) * q; cy = sy + (ty - sy) * q
    if 0 <= ty - (CY - CH / 2) <= CH:
        place(base, CUR, cx + 24, cy + 32, scale)
        ck = b["t0"] + 0.95
        if 0 <= t - ck <= 0.5:
            rr = int(24 + 60 * (t - ck) / 0.5); d = ImageDraw.Draw(base); d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=YEL + (255,), width=5)
    src_line(base)


# ---------- beats ----------
QUERIES = ["Where did my money go?", "Left before payday?", "Any odd charges?"]
B = [
    dict(k="robot", t0=0.0, t1=T("hook", 8) - 0.1, pose="think", claim="CLAUDE BATAYEGA\nPAISE KAHAN\nGAYE", hl={"KAHAN"}),
    dict(k="ui", t0=T("hook", 8) - 0.1, t1=T("avail", 0), key="intro", dev="tv", over="queries", hl=(T("hook", 8), T("avail", 0) - 0.1)),
    dict(k="num", t0=T("avail", 0), t1=T("avail", 12) - 0.1, lines=("BETA", "THIS WEEK", "US ONLY")),
    dict(k="ui", t0=T("avail", 12) - 0.1, t1=T("how", 0), key="avail", dev="phone", hl=(T("avail", 12), T("how", 0) - 0.1), pill=("PRO / MAX / ULTRA", T("avail", 12))),
    dict(k="ui", t0=T("how", 0), t1=T("how", 12) - 0.1, key="plaid", dev="paper", stamp="PLAID", hl=(T("how", 0) + 0.2, T("how", 11)), pill=("SIGN IN VIA PLAID", T("how", 1))),
    dict(k="robot", t0=T("how", 12) - 0.1, t1=T("ask", 0), pose="work", dark=True, chips=[("NO PASSWORD", T("how", 15)), ("READ-ONLY", T("how", 21))]),
    dict(k="robot", t0=T("ask", 0), t1=T("ask", 7) - 0.1, pose="work", prompt=("Where did my money go?", T("ask", 2), T("ask", 6))),
    dict(k="ui", t0=T("ask", 7) - 0.1, t1=T("caution", 0), key="img1", dev="tv", pill=("SORTS BY CATEGORY", T("ask", 8))),
    dict(k="robot", t0=T("caution", 0), t1=T("caution", 10) - 0.1, pose="stop", claim="INVESTMENT\nADVICE NAHI", hl={"NAHI"}),
    dict(k="ui", t0=T("caution", 10) - 0.1, t1=T("cta", 0), key="mistakes", dev="paper", stamp="CHECK!", hl=(T("caution", 10), T("cta", 0) - 0.2), tag=("CHECK WITH YOUR BANK", T("caution", 16))),
    dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1),
]
EXACT_UI = sum(b["t1"] - b["t0"] for b in B if b["k"] in ("ui",)) + 0.0


def robot_beat(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGD if b.get("dark") else BGL)
    if "claim" in b:
        lines = b["claim"].split("\n"); ch = 150 * len(lines) + 70
        card = Image.new("RGBA", (940, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle([0, 0, 939, ch - 1], 48, fill=INK + (255,))
        for i, l in enumerate(lines):
            sz = 138
            while font(sz).getlength(l) > 860: sz -= 4
            f = font(sz); w = f.getlength(l); x = 470 - w / 2
            col = YEL if (b.get("hl") and l.split(" ")[-1] in b["hl"] or l in b.get("hl", ())) else (255, 255, 255)
            if b.get("hl") and any(h in l for h in b["hl"]): col = YEL
            d.text((x, 30 + i * 150), l, font=f, fill=col + (255,))
        place(base, card, 540, 360 + ch / 2 - 40, 0.9 + 0.1 * ease_back(lt / 0.3) if lt < 0.4 else 1.0)
    if "mini" in b:
        rx, ry, rw, rh = rect(b["mini"]); s2 = 2 * SCALE; y0 = max(0, ry - 40); crop = ARTS.crop((0, int(y0), CW, int(y0 + 330))).convert("RGBA")
        m = Image.new("L", crop.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, crop.width - 1, crop.height - 1], 26, fill=255); crop.putalpha(m)
        crop = crop.resize((520, int(520 * crop.height / crop.width)), Image.LANCZOS)
        place(base, crop, 770, 1115, 0.9 + 0.1 * ease_back((lt - 0.1) / 0.35) if lt < 0.5 else 1.0, rot=-5)
    if "pose" in b:
        rb = robot(b["pose"], 620 if "claim" in b else 560); bob = 10 * math.sin(lt * 4.0)
        place(base, rb, 300 if "claim" in b else (540 if "chips" in b else 300), (1300 if "claim" in b else (640 if "chips" in b else 700)) + bob, 0.94 + 0.06 * ease_out(lt / 0.3))
    for i, (txt, tt) in enumerate(b.get("chips", [])):
        pp = pop(t, tt); place(base, chip(txt, 100, INK, YEL, pad=(52, 16), r=40), 540, 960 + 140 * i, 0.5 + 0.5 * pp, min(1, pp))
    if "prompt" in b:
        txt, a0, a1 = b["prompt"]; n = int(len(txt) * min(1, max(0, (t - a0) / max(0.1, a1 - a0)))); shown = txt[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(txt) else "")
        box = Image.new("RGBA", (900, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(box); d.rounded_rectangle([0, 0, 899, 229], 46, fill=(255, 255, 255, 255), outline=(30, 30, 36, 255), width=6)
        d.text((46, 20), "Example question (from the article)", font=font(34), fill=(120, 120, 130, 255)); d.text((46, 80), shown, font=font(76), fill=INK + (255,))
        place(base, box, 590, 1130, 0.9 + 0.1 * ease_out(lt / 0.3))
        place(base, chip("Personal Finance", 54, BLUE, pad=(30, 12), r=26), 300, 1290, 0.8 + 0.2 * pop(t, a0 - 0.5))


def num_beat(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGD); l1, l2, l3 = b["lines"]
    place(base, chip(l1, 300, (14, 15, 20), YEL, pad=(10, 0), r=1), 540, 620, 0.7 + 0.3 * ease_back(lt / 0.35))
    place(base, chip(l2, 120, (255, 255, 255), INK, pad=(54, 16), r=40), 540, 920, pop(t, b["t0"] + 0.25))
    place(base, chip(l3, 96, YEL, INK, pad=(44, 14), r=34), 540, 1090, pop(t, b["t0"] + 0.55))
    src_line(base, 1275, SRC)


def cta_beat(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGL)
    place(base, robot("wave", 620), 210, 1000 + 8 * math.sin(lt * 3.5))
    t4 = T("cta", 6) - 0.1
    if t >= t4:
        s = pop(t, t4, 0.3)
        place(base, chip("COMMENT", 100, INK, (255, 255, 255), pad=(44, 10), r=32), 680, 690, s)
        kw = chip("NEWS", 170, YEL, INK, pad=(60, 4), r=38); place(base, kw, 680, 890, pop(t, t4 + 0.12, 0.3))
        place(base, chip("FOR LINK", 100, INK, (255, 255, 255), pad=(44, 10), r=32), 680, 1075, pop(t, t4 + 0.24, 0.3))
    place(base, chip("DevRoboLab", 64, (255, 255, 255), INK, pad=(40, 10), r=30), 540, 330, 1.0) if False else None


def caption_chunks():
    out = []
    for sid in IDS:
        toks = WT[sid]["tokens"]; segs = []; cur = []
        for k, (tk, _) in enumerate(toks):
            cur.append(k)
            if re.search(r"[,।?!]$", tk): segs.append(cur); cur = []
        if cur: segs.append(cur)
        for sg in segs:
            n = len(sg); k = -(-n // 3); sizes = [n // k + (1 if j < n % k else 0) for j in range(k)]; i = 0
            for z in sizes:
                idx = sg[i:i + z]; out.append((SC[sid] + LEAD + toks[idx[0]][1], " ".join(toks[k][0] for k in idx))); i += z
    ends = [c[0] for c in out[1:]] + [TOTAL]
    return [(a, min(b, a + 1.5), txt) for (a, txt), b in zip(out, ends)]


CAPS = caption_chunks()
KEY = {"NEWS", "Plaid", "password", "read-only", "investment", "advice", "bank", "Research", "web", "Mobile", "paid", "plans", "connectors", "usage", "limit", "searches", "Gmail", "Calendar", "Docs", "indicator", "plus", "खुद", "रिसर्च"}
_cap = {}


def caption(base, t, kind):
    for a, b, txt in CAPS:
        if a - 0.04 <= t < b:
            if txt not in _cap: _cap[txt] = chip(txt.upper() if txt.isascii() else txt, 70, VIO, pad=(40, 14), r=34, hl={w.upper() for w in KEY} | KEY, hlcolor=YEL)
            y = 1385 if kind in ("ui", "num") else (1420 if kind == "robot" else 1500)
            place(base, _cap[txt], 540, y, 0.92 + 0.08 * ease_out((t - a) / 0.12)); return


def overlays(base, t, b):
    lt = t - b["t0"]
    if b.get("over") == "queries":
        idx = [k for k in range(len(QUERIES)) if t >= b["t0"] + 0.35 + 0.8 * k]
        if idx:
            k = idx[-1]; tt = b["t0"] + 0.35 + 0.8 * k; pp = pop(t, tt, 0.3); place(base, chip(QUERIES[k], 52, (255, 255, 255), INK, pad=(30, 12), r=28), 540, 295, pp, min(1, pp))
    if b.get("pill"):
        txt, tt = b["pill"]
        if t >= tt - 0.1: pp = pop(t, tt - 0.1); place(base, chip(txt, 66, YEL, INK, pad=(36, 12), r=30), 540, 295, pp, min(1, pp))
    if b.get("pill2"):
        txt, tt = b["pill2"]; place(base, chip("+ > Research", 60, (255, 255, 255), INK, pad=(30, 10), r=28), 330, 295, pop(t, b["t0"] + 0.2))
        if t >= tt - 0.1: place(base, chip("Research", 60, BLUE, pad=(32, 10), r=28), 740, 295, pop(t, tt - 0.1))
    for i, (txt, tt) in enumerate(b.get("chips2", [])):
        if t >= tt - 0.15: pp = pop(t, tt - 0.15); place(base, chip(txt, 62, (255, 255, 255), INK, pad=(32, 10), r=28), 220 + 300 * i, 295, pp, min(1, pp))
    if b.get("tag"):
        txt, tt = b["tag"]
        if t >= tt - 0.1: pp = pop(t, tt - 0.1); place(base, chip(txt, 70, RED, pad=(40, 12), r=30), 540, 295, pp, min(1, pp))


# ---------- audio track (voice + soft SFX) ----------
SR = 24000


def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    rng = np.random.default_rng(3); pk = float(np.abs(a).max()) or 1.0
    def whoosh(t0, dur=0.22):
        m = int(dur * SR); nz = rng.standard_normal(m).astype(np.float32); env = np.sin(np.linspace(0, math.pi, m)) ** 2
        k = np.ones(40, dtype=np.float32) / 40; nz = nz - np.convolve(nz, k, "same"); return t0, nz * env * 10 ** (-23 / 20) * pk * 0.6
    def click(t0):
        m = int(0.05 * SR); tt = np.arange(m) / SR; return t0, np.sin(2 * math.pi * 900 * tt) * np.exp(-tt * 70) * 10 ** (-24 / 20) * pk * 0.6
    ev = []
    for b0, b1 in zip(B, B[1:]):
        if b0["k"] != b1["k"] and "ui" in (b0["k"], b1["k"]): ev.append(whoosh(b1["t0"] - 0.12))
        elif b1["k"] == "ui": ev.append(click(b1["t0"] + 0.02))
    for t0, x in ev:
        s = int(t0 * SR); a[s:s + len(x)] += x[: len(a) - s]
    with wave.open(str(out), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def blur_push(arr, t):
    """fast blur-push at robot<->UI/num boundaries (about 6 frames)"""
    for b0, b1 in zip(B, B[1:]):
        if b0["k"] != b1["k"] and "ui" in (b0["k"], b1["k"]):
            d = abs(t - b1["t0"])
            if d < 0.1:
                k = int(10 + 60 * (1 - d / 0.1)) | 1; arr = cv2.blur(arr, (k, 1)); M = np.float32([[1, 0, (40 if t < b1["t0"] else -40) * (1 - d / 0.1)], [0, 1, 0]])
                arr = cv2.warpAffine(arr, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
    return arr


def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = Image.new("RGBA", (W, H))
    if b["k"] == "ui": base.alpha_composite(BGD); ui_beat(base, t, b); overlays(base, t, b)
    elif b["k"] == "robot": robot_beat(base, t, b)
    elif b["k"] == "num": num_beat(base, t, b)
    else: cta_beat(base, t, b)
    caption(base, t, b["k"])
    # progress bar
    ImageDraw.Draw(base).rectangle([0, H - 12, int(W * t / TOTAL), H], fill=YEL + (255,))
    return blur_push(np.array(base.convert("RGB")), t)


import dev_v6; dev_v6.install(globals())


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['k'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    real = sum(min(x["t1"], TOTAL) - x["t0"] for x in B if x["k"] in ("ui", "num")); print(f"real/UI+number share {real / TOTAL:.0%}")
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/f_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice_sfx.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_sfx.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
