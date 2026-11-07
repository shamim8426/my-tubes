"""v7 (real photos): Claude Feature 03 (Research) Short, STYLE V5 (brand/STYLE_V5.md). Real official-page screenshots (raw/article.png, own Playwright capture,
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
SRC = "Official page: support.claude.com / Use research on Claude"


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




def robot_beat(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGL)
    if "claim" in b:
        lines = b["claim"].split("\n"); ch = 150 * len(lines) + 70
        card = Image.new("RGBA", (940, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle([0, 0, 939, ch - 1], 48, fill=INK + (255,))
        for i, l in enumerate(lines):
            f = font(138 if len(l) < 12 else 112); w = f.getlength(l); x = 470 - w / 2
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
        d.text((46, 20), "Example prompt (illustration)", font=font(34), fill=(120, 120, 130, 255)); d.text((46, 80), shown, font=font(76), fill=INK + (255,))
        place(base, box, 590, 1130, 0.9 + 0.1 * ease_out(lt / 0.3))
        place(base, chip("Research ON", 54, BLUE, pad=(30, 12), r=26), 300, 1290, 0.8 + 0.2 * pop(t, a0 - 0.5))




def num_beat(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGD)
    place(base, chip("5+", 330, (14, 15, 20), YEL, pad=(10, 0), r=1), 540, 620, 0.7 + 0.3 * ease_back(lt / 0.35))
    place(base, chip("SEARCHES", 130, (255, 255, 255), INK, pad=(54, 18), r=40), 540, 920, pop(t, b["t0"] + 0.25))
    place(base, chip("IN 1-3 MINUTES", 86, YEL, INK, pad=(44, 14), r=34), 540, 1090, pop(t, b["t0"] + 0.55))
    src_line(base, 1275, "Source: support.claude.com / web search, extended thinking, research")


def cta_beat(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGL)
    place(base, robot("wave", 620), 210, 1000 + 8 * math.sin(lt * 3.5))
    t4 = T("cta", 4) - 0.1
    if t >= t4:
        s = pop(t, t4, 0.3)
        place(base, chip("COMMENT", 100, INK, (255, 255, 255), pad=(44, 10), r=32), 680, 780, s)
        kw = chip("RESEARCH", 138, YEL, INK, pad=(44, 4), r=38); place(base, kw, 680, 930, pop(t, t4 + 0.12, 0.3))
        place(base, chip("FOR LINK", 100, INK, (255, 255, 255), pad=(44, 10), r=32), 680, 1080, pop(t, t4 + 0.24, 0.3))
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
KEY = {"Research", "RESEARCH", "web", "Mobile", "paid", "plans", "connectors", "usage", "limit", "searches", "Gmail", "Calendar", "Docs", "indicator", "plus", "खुद", "रिसर्च"}
_cap = {}


def caption(base, t, kind):
    for a, b, txt in CAPS:
        if a - 0.04 <= t < b:
            if txt not in _cap: _cap[txt] = chip(txt.upper() if txt.isascii() else txt, 70, VIO, pad=(40, 14), r=34, hl={w.upper() for w in KEY} | KEY, hlcolor=YEL)
            y = 1385 if kind in ("ui", "num") else (1420 if kind == "robot" else 1500)
            place(base, _cap[txt], 540, y, 0.92 + 0.08 * ease_out((t - a) / 0.12)); return



# =====================  STYLE v7: real photos with motion, small cards, document only once  =====================
from PIL import ImageChops
PHOTO = {k: Image.open(HERE / f"raw/photos/{k}.png").convert("RGB") for k in ("hook", "web", "desktop", "mobile", "team", "plan")}
_cov = {}


def bg_soft():
    im = Image.new("RGB", (W, H), (252, 250, 244)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(252 - 14 * k), int(250 - 18 * k), int(244 - 40 * k)))
    d.ellipse([-300, 380, 700, 1380], fill=(255, 236, 140)); return im.filter(ImageFilter.GaussianBlur(120)).convert("RGBA")


BGS = bg_soft()


def rounded(img, r):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); return o


def shadow(w, h, r=40, off=34, blur=26, a=105):
    sh = Image.new("RGBA", (w + 160, h + 160), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([80, 80 + off, 80 + w, 80 + h + off], r, fill=(0, 0, 0, a))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def photo(key, w, h, lt, dur, z0=1.0, z1=1.14, pan=(0.0, 0.0), r=40):
    """real photo with slow camera move (zoom + pan) inside a rounded w x h card -> RGBA"""
    src = PHOTO[key]; ck = (key, w, h)
    if ck not in _cov:
        s = max(1.5 * w / src.width, 1.5 * h / src.height); _cov[ck] = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    cov = _cov[ck]; p = ease_io(min(1, max(0, lt / dur))); z = z0 + (z1 - z0) * p
    ww, wh = w * 1.25 / z, h * 1.25 / z
    cx = cov.width / 2 + pan[0] * (cov.width - ww) / 2 * (p - 0.5) * 2; cy = cov.height / 2 + pan[1] * (cov.height - wh) / 2 * (p - 0.5) * 2
    im = cov.crop((int(cx - ww / 2), int(cy - wh / 2), int(cx + ww / 2), int(cy + wh / 2))).resize((w, h), Image.BILINEAR)
    return rounded(im, r)


def card_enter(base, spr, cx, cy, t, t0, rot=0.0, side=0, dur=0.38):
    """slide + overshoot entry of a card with its shadow (side: -1 from left, 1 from right, 0 from below)"""
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur))
    dx = side * (1 - q) * 520; dy = (1 - q) * (140 if side == 0 else 0)
    sc = 0.9 + 0.1 * e; w, h = spr.size
    place(base, shadow(w, h), cx + dx, cy + dy, sc, min(1, q * 1.5), rot); place(base, spr, cx + dx, cy + dy, sc, min(1, q * 1.5), rot)


def label(base, text, cx, cy, t, t0, color=YEL, tc=INK, size=64, rot=0):
    if t >= t0 - 0.02: pp = pop(t, t0); place(base, chip(text, size, color, tc, pad=(34, 10), r=26), cx, cy, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)


def typed(txt, t, a0, a1): n = int(len(txt) * min(1, max(0, (t - a0) / max(0.1, a1 - a0)))); return txt[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(txt) else "")


# ---- one-and-only document moment: small paper note, marker follows the voice live ----
PLAIN = Image.open(HERE / "raw/article_plain.png").convert("RGB"); PLAIN = PLAIN.resize((CW, int(PLAIN.height * CW / PLAIN.width)), Image.LANCZOS); LINES = RJ.get("lines", {})


def note(key, w, h, hp):
    rx, ry, rw, rh = rect(key); s = (w - 60) / CW; a = PLAIN.resize((int(PLAIN.width * s), int(PLAIN.height * s)), Image.LANCZOS); k = 2 * SCALE * s
    lines = LINES.get(key) or []
    if lines and hp > 0:
        tot = sum(l[2] for l in lines); done = 0.0; layer = Image.new("RGB", a.size, (255, 255, 255)); d = ImageDraw.Draw(layer)
        for x, y, lw, lh in lines:
            f0 = done / tot; f1 = (done + lw) / tot; done += lw; q = min(1, max(0, (hp - f0) / (f1 - f0)))
            if q > 0: d.rounded_rectangle([x * k - 4, y * k - 2, (x + lw * q) * k + 4, (y + lh) * k + 2], 5, fill=YEL)
        a = ImageChops.multiply(a, layer)
    cy = (ry + rh / 2) * s; y0 = int(max(0, min(a.height - (h - 70), cy - (h - 70) * 0.45))); x0 = int(max(0, (a.width - (w - 60)) / 2))
    pg = a.crop((x0, y0, x0 + w - 60, y0 + h - 70)).convert("RGBA")
    sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(sheet)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 14, fill=(255, 254, 250, 255), outline=(220, 214, 196, 255), width=3); sheet.alpha_composite(pg, (30, 40))
    for x in (60, w - 210): sheet.alpha_composite(Image.new("RGBA", (150, 50), (255, 214, 10, 190)).rotate(6 if x < 300 else -6, expand=True), (x, -16))
    return sheet


# ---- HTML-style mock of the chat box for the 'how to switch it on' steps (labelled illustration) ----
def mock_chat(t, b):
    w, h = 940, 860; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 46, fill=(255, 255, 255, 255), outline=(30, 30, 36, 255), width=6)
    # header: web search toggle
    on = ease_out((t - b["on"]) / 0.3) if t >= b["on"] else 0.0
    d.text((48, 36), "Web search", font=font(58), fill=INK + (255,))
    d.rounded_rectangle([w - 250, 44, w - 70, 114], 35, fill=(int(205 + (37 - 205) * on), int(205 + (99 - 205) * on), int(210 + (235 - 210) * on), 255))
    kx = w - 250 + 35 + on * 110; d.ellipse([kx - 29, 50, kx + 29, 108], fill=(255, 255, 255, 255))
    d.line([(48, 150), (w - 48, 150)], fill=(225, 225, 230, 255), width=3)
    d.text((48, 190), "How can I help you today?", font=font(54), fill=(150, 150, 160, 255))
    # menu
    mt = b["menu"]; mp = ease_back((t - mt) / 0.3) if t >= mt else 0.0
    if mp > 0.02:
        mw, mh_ = 600, 270; menu = Image.new("RGBA", (mw, mh_), (0, 0, 0, 0)); md = ImageDraw.Draw(menu)
        md.rounded_rectangle([0, 0, mw - 1, mh_ - 1], 34, fill=(250, 250, 252, 255), outline=(30, 30, 36, 255), width=5)
        sel = t >= b["pick"]
        md.text((40, 30), "Add files or photos", font=font(52), fill=(110, 110, 120, 255))
        md.rounded_rectangle([18, 130, mw - 18, 240], 26, fill=(YEL + (255,)) if sel else (235, 235, 240, 255)); md.text((40, 146), "Research", font=font(62), fill=INK + (255,))
        place(im, menu, 40 + mw / 2, 470 - mh_ / 2 + 30, 0.85 + 0.15 * min(1, mp), min(1, mp * 1.5))
    # input pill with plus button
    d.rounded_rectangle([40, 640, w - 40, 800], 80, fill=(245, 245, 248, 255), outline=(30, 30, 36, 255), width=5)
    pr = (t - b["menu"]) if t >= b["menu"] else -1
    d.ellipse([70, 670, 170, 770], fill=INK + (255,)); d.line([(120, 690), (120, 750)], fill=(255, 255, 255, 255), width=9); d.line([(90, 720), (150, 720)], fill=(255, 255, 255, 255), width=9)
    if 0 <= pr <= 0.5: rr = int(52 + 70 * pr / 0.5); d.ellipse([120 - rr, 720 - rr, 120 + rr, 720 + rr], outline=YEL + (255,), width=7)
    if t >= b["ind"]:
        pp = ease_back((t - b["ind"]) / 0.3); ch = chip("Research", 56, BLUE, pad=(34, 8), r=30); sc = 0.5 + 0.5 * pp
        place(im, ch, 330, 720, sc, min(1, pp * 1.4))
    else: d.text((210, 686), "Message Claude...", font=font(50), fill=(160, 160, 170, 255))
    return im


def meter_beat(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGL)
    place(base, robot("stop", 520), 300, 760 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    card = Image.new("RGBA", (520, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle([0, 0, 519, 329], 44, fill=INK + (255,))
    d.text((40, 24), "USAGE LIMIT", font=font(70), fill=(255, 255, 255, 255)); p = ease_io(min(1, lt / 2.2))
    d.rounded_rectangle([40, 150, 480, 220], 35, fill=(60, 62, 72, 255)); col = (int(255), int(214 - 160 * p), int(10 + 20 * p))
    d.rounded_rectangle([40, 150, 40 + int(440 * (0.15 + 0.85 * p)), 220], 35, fill=col + (255,)); d.text((40, 235), "jaldi kharch!" if p > 0.6 else "...", font=font(64), fill=YEL + (255,))
    card_enter(base, card, 760, 640, t, b["t0"] + 0.1, side=1)



# =====================  v8: the screens in the photos PLAY a demo (typing question -> searches -> report)  =====================
import cv2
PF = lambda sz, bold=False: ImageFont.truetype(str(ROOT / ("shared/fonts/Poppins-Bold.ttf" if bold else "shared/fonts/Poppins-Medium.ttf")), sz)
PNP = {k: np.array(PHOTO[k]) for k in ("web", "desktop", "mobile")}
QUAD = {"web": [(628, 150), (1068, 150), (1024, 497), (576, 445)], "desktop": [(371, 149), (979, 149), (981, 470), (369, 472)], "mobile": [(502, 104), (778, 100), (867, 598), (556, 651)]}
UISIZE = {"web": (960, 620), "desktop": (960, 620), "mobile": (540, 980)}
GREEN = (22, 163, 74)


def demo_ui(kind, t, s):
    """animated chat UI (PIL RGBA) at local time t. s: q (question), ty=(a0,a1) typing window, rows=[(label,t0)], done=t_report, extra rows allowed"""
    w, h = UISIZE[kind]; m = kind == "mobile"; im = Image.new("RGBA", (w, h), (250, 249, 245, 255)); d = ImageDraw.Draw(im)
    fs = (50 if m else 46); sb = 0 if m else (210 if kind == "desktop" else 0)
    if kind == "desktop":
        d.rectangle([0, 0, sb, h], fill=(32, 32, 38, 255))
        for k in range(5): d.rounded_rectangle([20, 110 + 60 * k, sb - 20, 140 + 60 * k], 10, fill=(70, 72, 82, 255))
        d.text((24, 36), "Claude", font=PF(34, True), fill=(255, 255, 255, 255))
    top = 90 if m else 70; d.rectangle([sb, 0, w, top], fill=(255, 255, 255, 255)); d.line([(sb, top), (w, top)], fill=(225, 225, 230, 255), width=2)
    if kind != "desktop": d.text((28, 16 if m else 14), "Claude", font=PF(40 if m else 34, True), fill=INK + (255,))
    d.rounded_rectangle([w - (210 if m else 190), 18, w - 24, top - 18], 24, fill=(37, 99, 235, 255) if s.get("web", True) else (200, 200, 205, 255))
    d.text((w - (190 if m else 170), 22 if m else 20), "Web ON", font=PF(30 if m else 26, True), fill=(255, 255, 255, 255))
    x0 = sb + 30; y = top + 40
    q = s["q"]; a0, a1 = s["ty"]; sent = a1 + 0.35
    # input pill
    ih = 120 if m else 96; iy = h - ih - 36
    d.rounded_rectangle([x0 - 6, iy, w - 28, iy + ih], ih // 2, fill=(255, 255, 255, 255), outline=(190, 190, 198, 255), width=3)
    if t < sent:
        n = int(len(q) * min(1, max(0, (t - a0) / max(0.1, a1 - a0)))); txt = q[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(q) else "")
        d.text((x0 + 30, iy + (ih - fs) // 2 - 6), txt if n else "Message Claude...", font=PF(fs), fill=INK + (255,) if n else (160, 160, 170, 255))
        if t < a0: d.text((x0 + 4, top + 50), "How can I help you today?", font=PF(fs + 4, True), fill=(150, 150, 160, 255))
        if s.get("chip") and t >= s["chip"]:
            d.rounded_rectangle([x0 + 6, iy - 70, x0 + 250, iy - 14], 26, fill=(37, 99, 235, 255)); d.text((x0 + 28, iy - 68), "Research", font=PF(32, True), fill=(255, 255, 255, 255))
    else:
        # user bubble
        bw = int(PF(fs).getlength(q)) + 60; bx1 = w - 30; bx0 = max(x0, bx1 - bw); by = y
        d.rounded_rectangle([bx0, by, bx1, by + fs + 44], 30, fill=(255, 214, 10, 255)); d.text((bx0 + 30, by + 14), q, font=PF(fs), fill=INK + (255,))
        ry = by + fs + 90
        for k, (label, rt0) in enumerate(s.get("rows", [])):
            if t < rt0: continue
            rr = ry + k * (fs + 52); p = ease_out((t - rt0) / 0.3); xo = int(40 * (1 - p)); done = t >= rt0 + s.get("dur", 0.9)
            if done: d.ellipse([x0 + xo, rr, x0 + xo + 46, rr + 46], fill=GREEN + (255,)); d.line([(x0 + xo + 11, rr + 24), (x0 + xo + 20, rr + 33), (x0 + xo + 35, rr + 14)], fill=(255, 255, 255, 255), width=6)
            else:
                ang = (t * 400) % 360; d.ellipse([x0 + xo, rr, x0 + xo + 46, rr + 46], outline=(210, 210, 216, 255), width=6); d.arc([x0 + xo, rr, x0 + xo + 46, rr + 46], ang, ang + 100, fill=(37, 99, 235, 255), width=6)
            col = (60, 60, 70, 255) if not label.startswith("!") else (200, 40, 50, 255)
            d.text((x0 + xo + 66, rr - 4), label.lstrip("!"), font=PF(fs - 6, label.startswith("!")), fill=col)
        if s.get("done") and t >= s["done"]:
            p = ease_back((t - s["done"]) / 0.35); cy = ry + len(s.get("rows", [])) * (fs + 52) + 20
            if cy + 220 < iy:
                d.rounded_rectangle([x0, cy, w - 30, cy + 200], 28, fill=(255, 255, 255, 255), outline=(30, 30, 36, 255), width=4)
                d.text((x0 + 30, cy + 16), "Report ready", font=PF(fs, True), fill=INK + (255,))
                for k, wd in enumerate((0.9, 0.7, 0.5)): d.rounded_rectangle([x0 + 30, cy + 80 + 36 * k, x0 + 30 + int((w - sb - 120) * wd * min(1, p)), cy + 98 + 36 * k], 9, fill=(215, 215, 222, 255))
    return im


def screen_comp(key, ui):
    """warp the animated UI onto the screen of the photo (perspective), blend -> PIL RGB 1344x768"""
    base = PNP[key].astype(np.float32); w, h = ui.size; src = np.float32([[0, 0], [w, 0], [w, h], [0, h]]); dst = np.float32(QUAD[key])
    M = cv2.getPerspectiveTransform(src, dst); u = np.array(ui).astype(np.float32)
    if key == "mobile":  # rounded screen corners
        mk = Image.new("L", ui.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, w - 1, h - 1], 60, fill=255); u[..., 3] = np.array(mk)
    wp = cv2.warpPerspective(u, M, (base.shape[1], base.shape[0]), flags=cv2.INTER_AREA if False else cv2.INTER_LINEAR); a = wp[..., 3:4] / 255.0
    out = base * (1 - a) + (wp[..., :3] * 0.96) * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


FOCUS = {"web": (820, 330), "desktop": (675, 310), "mobile": (690, 380)}


def photo_dyn(img, key, w, h, lt, dur, z0=1.0, z1=1.3, r=40):
    p = ease_io(min(1, max(0, lt / dur))); z = z0 + (z1 - z0) * p
    zw, zh = min(1344.0, 768.0 * w / h), min(768.0, 1344.0 * h / w); ww, wh = zw / z, zh / z
    fx, fy = FOCUS[key]; cx = min(max(fx, ww / 2), 1344 - ww / 2); cy = min(max(fy, wh / 2), 768 - wh / 2)
    return rounded(img.crop((int(cx - ww / 2), int(cy - wh / 2), int(cx + ww / 2), int(cy + wh / 2))).resize((w, h), Image.BILINEAR), r)


def demo_card(key, w, h, t, t0, spec, dur, z0=1.0, z1=1.3, r=40):
    lt = max(0.0, t - t0); return photo_dyn(screen_comp(key, demo_ui(key, lt, spec)), key, w, h, lt, dur, z0, z1, r)


# ---- dark UI walkthrough (Claude Feature 01/02 look). Rule (user 2026-11-07): every moment where something is DONE inside Claude
# (switch on, ask, searches, sources) is shown in this dark UI with cursor + click; photos are only for 'which device' and mood. ----
OR = (217, 119, 87)


def walk_win(t, S):
    w, h = 980, 860; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); iy = h - 160
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(18, 18, 18, 255), outline=(42, 42, 42, 255), width=2)
    d.rounded_rectangle([0, 0, 210, h - 1], 30, fill=(12, 12, 12, 255)); d.rectangle([180, 0, 210, h], fill=(12, 12, 12, 255)); d.line([(210, 0), (210, h)], fill=(38, 38, 38, 255), width=2)
    d.text((26, 28), "Assistant", font=PF(32, True), fill=(255, 255, 255, 255))
    for k, nm in enumerate(["New chat", "Projects", "Artifacts", "Chats"]):
        if k == 0: d.rounded_rectangle([16, 100, 194, 148], 12, fill=(30, 30, 30, 255))
        d.text((34, 108 + 62 * k), nm, font=PF(24), fill=(235, 235, 235, 255) if k == 0 else (150, 150, 150, 255))
    on = 1.0 if S["on"] < -50 else (ease_out((t - S["on"]) / 0.2) if t >= S["on"] else 0.0)
    d.text((w - 440, 24), "Web search", font=PF(30, True), fill=(235, 235, 235, 255))
    d.rounded_rectangle([w - 200, 22, w - 40, 76], 27, fill=(int(58 + (OR[0] - 58) * on), int(58 + (OR[1] - 58) * on), int(58 + (OR[2] - 58) * on), 255))
    kx = w - 200 + 27 + on * 106; d.ellipse([kx - 22, 27, kx + 22, 71], fill=(255, 255, 255, 255)); d.line([(210, 98), (w, 98)], fill=(38, 38, 38, 255), width=2)
    sent = t >= S["sent"]; ty0, ty1 = S["ty"]
    if not sent: d.text((250, 160), "How can I help you today?", font=PF(40, True), fill=(120, 120, 120, 255))
    d.rounded_rectangle([240, iy, w - 36, iy + 100], 30, fill=(22, 22, 22, 255), outline=OR + (255,) if (t >= S["menu"] or t >= S["ty"][0]) else (60, 60, 60, 255), width=3)
    d.ellipse([262, iy + 20, 322, iy + 80], fill=(48, 48, 48, 255)); d.line([(292, iy + 34), (292, iy + 66)], fill=(255, 255, 255, 255), width=6); d.line([(276, iy + 50), (308, iy + 50)], fill=(255, 255, 255, 255), width=6)
    tx = 345
    if t >= S["ind"]:
        pp = ease_back((t - S["ind"]) / 0.25); c = chip("Research", 40, BLUE, pad=(26, 4), r=22); c = c.resize((max(1, int(c.width * min(1, pp))), max(1, int(c.height * min(1, pp)))))
        im.alpha_composite(c, (tx, iy + 50 - c.height // 2)); tx += c.width + 18
    if not sent:
        q = S["q"]; n = int(len(q) * min(1, max(0, (t - ty0) / max(0.1, ty1 - ty0))))
        d.text((tx, iy + 28), q[:n] + ("|" if int(t * 4) % 2 == 0 and 0 < n < len(q) else "") if n else ("Message..." if t < S["ind"] else ""), font=PF(32), fill=(240, 240, 240, 255) if n else (110, 110, 110, 255))
    mt = S["menu"]
    if mt <= t < S["pick"] + 0.45:
        mp = min(1, ease_back((t - mt) / 0.22)); mw, mh = 520, 230; my = iy - 20 - mh; sel = t >= S["pick"]
        menu = Image.new("RGBA", (mw, mh), (0, 0, 0, 0)); md = ImageDraw.Draw(menu); md.rounded_rectangle([0, 0, mw - 1, mh - 1], 22, fill=(27, 27, 27, 255), outline=(58, 58, 58, 255), width=2)
        md.text((30, 26), "Add files or photos", font=PF(30), fill=(190, 190, 190, 255)); md.rounded_rectangle([14, 100, mw - 14, 208], 16, fill=OR + (255,) if sel else (40, 40, 40, 255))
        md.text((34, 124), "Research", font=PF(36, True), fill=(17, 17, 17, 255) if sel else (235, 235, 235, 255))
        im.alpha_composite(menu.resize((max(1, int(mw * (0.9 + 0.1 * mp))), max(1, int(mh * (0.9 + 0.1 * mp))))), (240, int(my + (1 - mp) * 20)))
    if sent:  # chat: user bubble, step rows with spinner -> tick, report card
        q = S["q"]; f = PF(32); bw = int(f.getlength(q)) + 56; bx1 = w - 40; bx0 = bx1 - bw; p = ease_out((t - S["sent"]) / 0.2)
        d.rounded_rectangle([bx0, 126 + int(20 * (1 - p)), bx1, 190 + int(20 * (1 - p))], 24, fill=(38, 38, 38, 255)); d.text((bx0 + 28, 136 + int(20 * (1 - p))), q, font=f, fill=(240, 240, 240, 255))
        ry = 226
        for k, (label, rt0) in enumerate(S["rows"]):
            if t < rt0: continue
            rr = ry + k * 62; pp = ease_out((t - rt0) / 0.2); xo = int(36 * (1 - pp)); done = t >= rt0 + S.get("dur", 0.5); x0 = 250
            if done: d.ellipse([x0 + xo, rr, x0 + xo + 40, rr + 40], fill=GREEN + (255,)); d.line([(x0 + xo + 9, rr + 21), (x0 + xo + 17, rr + 29), (x0 + xo + 31, rr + 11)], fill=(255, 255, 255, 255), width=5)
            else: ang = (t * 520) % 360; d.ellipse([x0 + xo, rr, x0 + xo + 40, rr + 40], outline=(70, 70, 70, 255), width=5); d.arc([x0 + xo, rr, x0 + xo + 40, rr + 40], ang, ang + 100, fill=OR + (255,), width=5)
            d.text((x0 + xo + 58, rr - 4), label, font=PF(30), fill=(225, 225, 225, 255))
        if S.get("report") and t >= S["report"]:
            pp = ease_back((t - S["report"]) / 0.3); cy = ry + len(S["rows"]) * 62 + 24
            card = Image.new("RGBA", (w - 290, 190), (0, 0, 0, 0)); cd = ImageDraw.Draw(card); cd.rounded_rectangle([0, 0, card.width - 1, 189], 22, fill=(26, 26, 26, 255), outline=OR + (255,), width=3)
            cd.text((26, 14), "Research report ready", font=PF(32, True), fill=(255, 255, 255, 255))
            for k, wd in enumerate((0.92, 0.74, 0.5)): cd.rounded_rectangle([26, 78 + 34 * k, 26 + int((card.width - 52) * wd * min(1, pp)), 96 + 34 * k], 8, fill=(70, 70, 70, 255))
            im.alpha_composite(card, (250, cy))
    return im


def walk_cursor(S, t):
    pts = S["cur"]
    for (ta, xa, ya), (tb, xb, yb) in zip(pts, pts[1:]):
        if ta <= t <= tb: q = ease_io((t - ta) / max(0.05, tb - ta)); return xa + (xb - xa) * q, ya + (yb - ya) * q
    return (pts[0][1], pts[0][2]) if t < pts[0][0] else (pts[-1][1], pts[-1][2])


def walk_scene(base, t, b, S):
    lt = t - b["t0"]; base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)))
    punch = max([0.035 * max(0, 1 - (t - c) / 0.25) for c in S["clicks"] if t >= c] or [0.0])
    sc = 0.93 + 0.07 * ease_out(min(1, lt / 0.3)) + 0.06 * min(1, lt / max(3.0, b["t1"] - b["t0"])) + punch
    win = walk_win(t, S); cx, cy = walk_cursor(S, t)
    place(base, shadow(980, 860, 30, 40, 40, 150), 540, 720, sc)
    layer = Image.new("RGBA", win.size, (0, 0, 0, 0)); layer.alpha_composite(win); place(layer, CUR, cx + 24, cy + 32)
    for c in S["clicks"]:
        if 0 <= t - c <= 0.4: rr = int(20 + 70 * (t - c) / 0.4); ImageDraw.Draw(layer).ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=OR + (255,), width=6)
    place(base, layer, 540, 720, sc)
    bn = [x for x in S["banners"] if x[1] <= t < x[2]]
    if bn:
        txt, ts, te = bn[-1]; pp = pop(t, ts + 0.03); place(base, chip(txt, 60 if len(txt) < 28 else 46, OR, (17, 17, 17), pad=(34, 8), r=26), 540, 215, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    place(base, chip("Illustration", 28, (40, 40, 40), (200, 200, 200), pad=(20, 5), r=12), 540, 1280)


IY = 860 - 160


def S_hook(b):
    t0 = b["t0"]; ty = (T("hook", 6), T("hook", 9)); sent = ty[1] + 0.2
    return dict(on=-99, menu=-9, pick=-9, ind=-9, ty=ty, sent=sent, q="Plan a team offsite", dur=0.45, report=T("hook", 14) + 0.2,
                rows=[("Searching venues", T("hook", 11)), ("Checking travel prices", T("hook", 12) + 0.15), ("Reading reviews", T("hook", 13) + 0.1), ("Building the report", T("hook", 14) - 0.1)],
                cur=[(t0, 720, 420), (ty[0] - 0.05, 560, IY + 50), (b["t1"] + 2, 640, 420)], clicks=[ty[0] - 0.05],
                banners=[("1  ASK A QUESTION", t0, T("hook", 11)), ("2  CLAUDE SEARCHES", T("hook", 11), b["t1"] + 1)])


def S_main(b):
    t0 = b["t0"]; on, menu, pick, ind = T("enable", 2) - 0.15, T("enable", 8) - 0.1, T("enable", 12) - 0.1, T("enable", 13) + 0.15
    ty = (T("use", 3), T("use", 7)); sent = ty[1] + 0.2; ask = T("use", 2); my = IY - 20 - 230 + 154
    return dict(on=on, menu=menu, pick=pick, ind=ind, ty=ty, sent=sent, q="Plan a team offsite", dur=0.45, report=T("use", 17) + 0.5,
                rows=[("Web search", T("use", 9)), ("Gmail", T("use", 13)), ("Google Calendar", T("use", 14)), ("Google Docs", T("use", 16))],
                cur=[(t0, 720, 430), (on - 0.25, 790, 49), (menu - 0.3, 292, IY + 50), (pick - 0.25, 480, my), (ask - 0.1, 560, IY + 50), (b["t1"], 640, 430)], clicks=[on, menu, pick, ask],
                banners=[("STEP 1  WEB SEARCH ON", t0, T("enable", 5)), ("STEP 2  PLUS BUTTON", T("enable", 5), T("enable", 11)), ("STEP 3  CHOOSE RESEARCH", T("enable", 11), T("use", 0)),
                         ("STEP 4  ASK YOUR QUESTION", T("use", 0), T("use", 8)), ("SOURCES  WEB, GMAIL, CALENDAR, DOCS", T("use", 8), b["t1"])])


# ---------- beats (voice-synced) ----------
def beats():
    B = []
    B.append(dict(k="photo", id="hook1", t0=0.0, t1=T("hook", 6) - 0.1))
    B.append(dict(k="photo", id="hook2", t0=T("hook", 6) - 0.1, t1=T("hook", 15)))
    B.append(dict(k="num", t0=T("hook", 15), t1=T("avail", 3) - 0.1))
    B.append(dict(k="plans", t0=T("avail", 3) - 0.1, t1=T("avail", 13) - 0.1))
    B.append(dict(k="photo", id="stack", t0=T("avail", 13) - 0.1, t1=T("enable", 0)))
    B.append(dict(k="photo", id="walkmain", t0=T("enable", 0), t1=T("caution", 0)))
    B.append(dict(k="photo", id="mobnote", t0=T("caution", 0), t1=T("caution", 11) - 0.1, hl=(T("caution", 2), T("caution", 10))))
    B.append(dict(k="meter", t0=T("caution", 11) - 0.1, t1=T("cta", 0)))
    B.append(dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1))
    return B


B = beats()
H2 = None


def photo_beat(base, t, b):
    lt = t - b["t0"]; i = b["id"]; base.alpha_composite(BGS)
    if i == "hook1":
        card_enter(base, photo("hook", 960, 700, lt, b["t1"] - b["t0"], 1.0, 1.16, (0.5, 0)), 540, 560, t, 0.0, dur=0.01)
        for n, (txt, col, tc) in enumerate([("CLAUDE KHUD", INK, (255, 255, 255)), ("KARTA HAI", INK, (255, 255, 255)), ("RESEARCH", YEL, INK)]):
            pp = pop(t, 0.15 + 0.14 * n); place(base, chip(txt, 74, col, tc, pad=(40, 2), r=26), 540, 985 + 128 * n, 0.6 + 0.4 * pp, min(1, pp * 1.4), (-1.5, 1.5, -1)[n])
    elif i == "hook2":
        walk_scene(base, t, b, S_hook(b))
    elif i == "stack":
        S = {"web": dict(q="Plan a team offsite", ty=(0.05, 0.55), chip=0.0, rows=[("Searching venues", 0.7), ("Checking prices", 1.1)], dur=0.4),
             "desktop": dict(q="Best laptop under 60k?", ty=(0.05, 0.55), chip=0.0, rows=[("Searching reviews", 0.7), ("Comparing prices", 1.1)], dur=0.4),
             "mobile": dict(q="Trip plan for Goa", ty=(0.05, 0.55), chip=0.0, rows=[("Searching hotels", 0.7), ("Checking flights", 1.1)], dur=0.4)}
        for k, (key, txt, tt, side, rot) in enumerate([("web", "WEB", T("avail", 13), -1, -1.2), ("desktop", "DESKTOP", T("avail", 14), 1, 1.0), ("mobile", "MOBILE", T("avail", 16), -1, -0.8)]):
            cy = 375 + 350 * k; spr = demo_card(key, 900, 330, t, tt, S[key], 3.0, 1.45 + 0.1 * (key == "mobile"), 1.75 + 0.1 * (key == "mobile"))
            card_enter(base, spr, 540, cy, t, tt - 0.05, rot=rot, side=side)
            label(base, txt, 250 if k % 2 == 0 else 830, cy + 120, t, tt + 0.1, size=60)
    elif i == "walkmain":
        walk_scene(base, t, b, S_main(b))
    elif i == "mobnote":
        o = b["t0"]; sp = dict(q="Plan a team offsite", ty=(-2.0, -1.0), rows=[("Searching the web", 0.3), ("!Connectors skipped", T("caution", 8) - o)], dur=0.7)
        card_enter(base, demo_card("mobile", 620, 700, t, o, sp, b["t1"] - o, 1.15, 1.4), 540, 560, t, b["t0"], rot=-1.0)
        label(base, "CONNECTORS ✕", 800, 300, t, T("caution", 9), color=RED, tc=(255, 255, 255), size=58, rot=-3)
        h0, h1 = b["hl"]; hp = min(1, max(0, (t - h0) / max(0.3, h1 - h0))); card_enter(base, note("mobile", 880, 360, hp), 540, 1070, t, b["t0"] + 0.25, rot=1.2, side=0)
        place(base, chip(SRC, 30, (40, 44, 58), (235, 235, 240), pad=(24, 6), r=14), 540, 1292)


SR = 24000


def build_audio(out):
    """voice only (no whoosh / swipe sounds; user 2026-11-07); the music is mixed in by encode()"""
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = Image.new("RGBA", (W, H)); kind = "ui"
    if b["k"] == "photo": photo_beat(base, t, b)
    elif b["k"] == "plans":
        base.alpha_composite(BGS)
        for k, (txt, tt) in enumerate([("PRO", T("avail", 3)), ("MAX", T("avail", 4)), ("TEAM", T("avail", 6))]):
            pp = pop(t, tt - 0.05); place(base, chip(txt, 190, INK if k != 1 else YEL, (255, 255, 255) if k != 1 else INK, pad=(70, 8), r=50), 540, 520 + 230 * k, 0.6 + 0.4 * pp, min(1, pp * 1.4), (-2, 2, -1)[k])
        label(base, "PAID PLANS", 540, 300, t, b["t0"] + 0.1, size=74)
    elif b["k"] == "num": num_beat(base, t, b)
    elif b["k"] == "meter": meter_beat(base, t, b); kind = "robot"
    else: cta_beat(base, t, b); kind = "cta"
    caption(base, t, kind)
    return np.array(base.convert("RGB"))


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['k'], x.get('id'), round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/k_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice_v10.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_v10.wav", ROOT / deck["music"]["file"], HERE / "output/short_v10.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
