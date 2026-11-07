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


# ---------- beats (voice-synced) ----------
def beats():
    B = []
    B.append(dict(k="photo", id="hook1", t0=0.0, t1=T("hook", 6) - 0.1))
    B.append(dict(k="photo", id="hook2", t0=T("hook", 6) - 0.1, t1=T("hook", 15)))
    B.append(dict(k="num", t0=T("hook", 15), t1=T("avail", 3) - 0.1))
    B.append(dict(k="plans", t0=T("avail", 3) - 0.1, t1=T("avail", 13) - 0.1))
    B.append(dict(k="photo", id="stack", t0=T("avail", 13) - 0.1, t1=T("enable", 0)))
    B.append(dict(k="photo", id="mock", t0=T("enable", 0), t1=T("use", 0), on=T("enable", 2), menu=T("enable", 8), pick=T("enable", 12), ind=T("enable", 14)))
    B.append(dict(k="photo", id="team", t0=T("use", 0), t1=T("use", 8) - 0.1))
    B.append(dict(k="photo", id="sources", t0=T("use", 8) - 0.1, t1=T("caution", 0)))
    B.append(dict(k="photo", id="mobnote", t0=T("caution", 0), t1=T("caution", 11) - 0.1, hl=(T("caution", 2), T("caution", 10))))
    B.append(dict(k="meter", t0=T("caution", 11) - 0.1, t1=T("cta", 0)))
    B.append(dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1))
    return B


B = beats()


def photo_beat(base, t, b):
    lt = t - b["t0"]; i = b["id"]; base.alpha_composite(BGS)
    if i == "hook1":
        place_w, ph = 960, 700
        card_enter(base, photo("hook", place_w, ph, lt, b["t1"] - b["t0"], 1.0, 1.16, (0.5, 0)), 540, 560, t, 0.0, dur=0.01)
        for n, (txt, col, tc) in enumerate([("CLAUDE KHUD", INK, (255, 255, 255)), ("KARTA HAI", INK, (255, 255, 255)), ("RESEARCH", YEL, INK)]):
            pp = pop(t, 0.15 + 0.14 * n); place(base, chip(txt, 74, col, tc, pad=(40, 2), r=26), 540, 985 + 128 * n, 0.6 + 0.4 * pp, min(1, pp * 1.4), (-1.5, 1.5, -1)[n])
    elif i == "hook2":
        card_enter(base, photo("web", 960, 640, lt, b["t1"] - b["t0"], 1.0, 1.15, (-0.6, 0)), 540, 520, t, b["t0"], rot=-1.5)
        for k, q in enumerate(["offsite venues", "travel prices", "hotel reviews", "team calendar"]):
            label(base, q, (330, 760, 380, 700)[k] if False else (320 if k % 2 == 0 else 760), 880 + 130 * k, t, b["t0"] + 0.3 + 0.55 * k, color=(255, 255, 255), tc=INK, size=56, rot=(-2, 2)[k % 2])
    elif i == "stack":
        for k, (key, txt, tt, side, rot) in enumerate([("web", "WEB", T("avail", 13), -1, -1.2), ("desktop", "DESKTOP", T("avail", 14), 1, 1.0), ("mobile", "MOBILE", T("avail", 16), -1, -0.8)]):
            cy = 390 + 345 * k; spr = photo(key, 900, 300, t - tt, 2.5, 1.0, 1.15, ((-0.5, 0.2), (0.5, 0), (0, 0.3))[k])
            card_enter(base, spr, 540, cy, t, tt - 0.05, rot=rot, side=side)
            label(base, txt, 250 if k % 2 == 0 else 830, cy + 120, t, tt + 0.1, size=60)
    elif i == "mock":
        sc = 1.0 + 0.04 * min(1, lt / 4.0); spr = mock_chat(t, b)
        card_enter(base, spr, 540, 700, t, b["t0"], dur=0.35); place(base, chip("Illustration", 30, (40, 44, 58), (235, 235, 240), pad=(22, 6), r=14), 540, 1180)
    elif i == "team":
        card_enter(base, photo("team", 960, 700, lt, b["t1"] - b["t0"], 1.0, 1.15, (0.6, 0)), 540, 560, t, b["t0"], rot=1.2)
        box = chip(typed("Plan a team offsite", t, T("use", 3), T("use", 7)), 70, (255, 255, 255), INK, pad=(40, 16), r=36); card_enter(base, box, 540, 1060, t, T("use", 2), side=0)
    elif i == "sources":
        card_enter(base, photo("plan", 960, 520, lt, b["t1"] - b["t0"], 1.0, 1.16, (-0.5, 0.3)), 540, 460, t, b["t0"], rot=-1.0)
        for k, (txt, tt) in enumerate([("WEB", T("use", 9)), ("GMAIL", T("use", 13)), ("CALENDAR", T("use", 14)), ("DOCS", T("use", 16))]):
            label(base, txt, 300 if k % 2 == 0 else 780, 880 + 150 * (k // 2) + 20 * (k % 2), t, tt, color=YEL if k == 0 else (255, 255, 255), size=70, rot=(-2, 2)[k % 2])
    elif i == "mobnote":
        card_enter(base, photo("mobile", 880, 480, lt, b["t1"] - b["t0"], 1.0, 1.15, (0.0, 0.4)), 540, 440, t, b["t0"], rot=-1.0)
        label(base, "CONNECTORS ✕", 740, 640, t, T("caution", 9), color=RED, tc=(255, 255, 255), size=58, rot=-3)
        h0, h1 = b["hl"]; hp = min(1, max(0, (t - h0) / max(0.3, h1 - h0))); card_enter(base, note("mobile", 880, 420, hp), 540, 960, t, b["t0"] + 0.25, rot=1.2, side=0)
        place(base, chip(SRC, 30, (40, 44, 58), (235, 235, 240), pad=(24, 6), r=14), 540, 1230)


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
    ev = [whoosh(x["t0"] - 0.1) for x in B[1:-1]] + [whoosh(T("avail", 14) - 0.1), whoosh(T("avail", 16) - 0.1)]
    for t0, x in ev:
        s = max(0, int(t0 * SR)); a[s:s + len(x)] += x[: len(a) - s]
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
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/g_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice_sfx_v7.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_sfx_v7.wav", ROOT / deck["music"]["file"], HERE / "output/short_v7.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
