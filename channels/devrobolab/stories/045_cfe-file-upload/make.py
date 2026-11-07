"""044 Claude Feature 04 (upload files): Claude Feature 03 (Research) Short, STYLE V5 (brand/STYLE_V5.md). Real official-page screenshots (raw/article.png, own Playwright capture,
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
SRC = "Official page: support.claude.com / Upload files to Claude"


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
KEY = {"PDF", "Word", "CSV", "text", "photos", "photo", "plus", "Add", "files", "Drag", "drop", "page", "chart", "number", "Save", "FILES", "बीस", "सौ"}
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



# =====================  044 CLAUDE FEATURE 04 (upload files): approved framework + STYLE_LIBRARY 9/10 rules  =====================
# style variants of this video: LIGHT SKETCH theme (cream paper, thick dark outlines, pastel cards, tape), accent = CORAL (white text, coral key words), big showing area (75-85 % of height),
# one small caption strip at the bottom, normal-size text (about 52 px), robot only in the CTA (centre, big). Dark Claude app screen only for the real steps.
CORAL = (242, 107, 91); MINT = (206, 238, 224); PEACH = (255, 228, 210); LAV = (226, 222, 250); SKY = (208, 232, 250); INKD = (30, 30, 36)
OR = (217, 119, 87); GREEN = (22, 163, 74)
PF = lambda sz, bold=False: ImageFont.truetype(str(ROOT / ("shared/fonts/Poppins-Bold.ttf" if bold else "shared/fonts/Poppins-Medium.ttf")), sz)
BF = lambda sz: ImageFont.truetype(str(ROOT / "shared/fonts/Baloo2-Variable.ttf"), sz)


def bg_paper():
    im = Image.new("RGB", (W, H), (251, 248, 241)); d = ImageDraw.Draw(im)
    for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(238, 233, 222), width=2)
    for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(238, 233, 222), width=1)
    return im.convert("RGBA")


BGP = bg_paper()


def sk_card(w, h, fill, r=34, off=9):
    im = Image.new("RGBA", (w + off + 4, h + off + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([off, off, w + off, h + off], r, fill=INKD + (255,)); d.rounded_rectangle([0, 0, w, h], r, fill=fill + (255,), outline=INKD + (255,), width=5)
    return im


def tape(im, x, y, rot=-6):
    t = Image.new("RGBA", (130, 44), (255, 214, 10, 200)); im.alpha_composite(t.rotate(rot, expand=True), (x, y))


def icon_pdf(d, x, y, s, label="PDF"):
    d.polygon([(x, y), (x + 0.68 * s, y), (x + s * 0.9, y + 0.22 * s), (x + 0.9 * s, y + 1.15 * s), (x, y + 1.15 * s)], fill=(255, 255, 255, 255), outline=INKD + (255,))
    d.line([(x, y), (x + 0.68 * s, y), (x + 0.9 * s, y + 0.22 * s), (x + 0.9 * s, y + 1.15 * s), (x, y + 1.15 * s), (x, y)], fill=INKD + (255,), width=5)
    d.rectangle([x + 0.08 * s, y + 0.62 * s, x + 0.82 * s, y + 0.9 * s], fill=CORAL + (255,)); d.text((x + 0.14 * s, y + 0.6 * s), label, font=BF(int(0.3 * s)), fill=(255, 255, 255, 255))
    for k in range(2): d.line([(x + 0.14 * s, y + (0.2 + 0.14 * k) * s), (x + 0.6 * s, y + (0.2 + 0.14 * k) * s)], fill=(150, 150, 150, 255), width=4)


def icon_photo(d, x, y, s):
    d.rounded_rectangle([x, y, x + 1.2 * s, y + 0.95 * s], 10, fill=SKY + (255,), outline=INKD + (255,), width=5)
    d.ellipse([x + 0.8 * s, y + 0.12 * s, x + 1.02 * s, y + 0.34 * s], fill=(255, 214, 10, 255), outline=INKD + (255,), width=3)
    d.polygon([(x + 0.06 * s, y + 0.88 * s), (x + 0.42 * s, y + 0.42 * s), (x + 0.68 * s, y + 0.72 * s), (x + 0.84 * s, y + 0.55 * s), (x + 1.14 * s, y + 0.88 * s)], fill=(120, 190, 140, 255), outline=INKD + (255,))


def icon_chat(d, x, y, s):
    d.rounded_rectangle([x, y, x + 1.3 * s, y + 0.95 * s], 22, fill=PEACH + (255,), outline=INKD + (255,), width=5); d.polygon([(x + 0.2 * s, y + 0.9 * s), (x + 0.12 * s, y + 1.2 * s), (x + 0.5 * s, y + 0.92 * s)], fill=PEACH + (255,), outline=INKD + (255,))
    for k in range(3): d.ellipse([x + (0.32 + 0.3 * k) * s, y + 0.4 * s, x + (0.46 + 0.3 * k) * s, y + 0.54 * s], fill=INKD + (255,))


def tick(d, x, y, s, col=GREEN):
    d.ellipse([x, y, x + s, y + s], fill=col + (255,)); d.line([(x + 0.25 * s, y + 0.52 * s), (x + 0.43 * s, y + 0.7 * s), (x + 0.76 * s, y + 0.3 * s)], fill=(255, 255, 255, 255), width=max(4, int(s * 0.13)))


def cross(d, x, y, s, col=RED):
    d.ellipse([x, y, x + s, y + s], fill=col + (255,)); d.line([(x + 0.3 * s, y + 0.3 * s), (x + 0.7 * s, y + 0.7 * s)], fill=(255, 255, 255, 255), width=max(4, int(s * 0.13))); d.line([(x + 0.7 * s, y + 0.3 * s), (x + 0.3 * s, y + 0.7 * s)], fill=(255, 255, 255, 255), width=max(4, int(s * 0.13)))


def cchip(txt, size=52, fill=CORAL, color=(255, 255, 255), pad=(30, 8), r=24):
    return chip(txt, size, fill, color, pad=pad, r=r)


def clabel(base, txt, cx, cy, t, t0, size=52, fill=CORAL, color=(255, 255, 255), rot=0):
    if t >= t0 - 0.02: pp = pop(t, t0); place(base, cchip(txt, size, fill, color), cx, cy, 0.7 + 0.3 * pp, min(1, pp * 1.4), rot)


# ---- caption strip: ONE small strip, white text, key word in the video's accent colour (rule: normal size, colours vary per video) ----
_capc = {}


def caption(base, t, kind):
    for a, b, txt in CAPS:
        if a - 0.04 <= t < b:
            if txt not in _capc: _capc[txt] = chip(txt, 52, (28, 28, 34), (255, 255, 255), pad=(34, 12), r=28, hl={w.upper() for w in KEY} | KEY, hlcolor=(255, 168, 150))
            place(base, _capc[txt], 540, 1400, 0.94 + 0.06 * ease_out((t - a) / 0.12)); return


# ---- S1 hook: sketch flow  PDF + photo -> Claude, three steps ----
def s_hook(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    card = sk_card(960, 900, (255, 255, 255)); d = ImageDraw.Draw(card); tape(card, 60, -14, -5); tape(card, 760, -14, 5)
    d.text((60, 56), "Ask Claude about a file", font=BF(70), fill=INKD + (255,))
    # sources (left), arrow, chat (right)
    for txt, key, y, tt in (("PDF", "pdf", 220, T("hook", 0)), ("photo", "photo", 470, T("hook", 2))):
        if t >= tt - 0.05:
            pp = ease_back((t - tt) / 0.3); sub = Image.new("RGBA", (300, 250), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub)
            (icon_pdf if key == "pdf" else icon_photo)(sd, 40, 20, 150) if key == "pdf" else icon_photo(sd, 30, 40, 150)
            sd.text((30, 190), txt, font=BF(48), fill=INKD + (255,)); card.alpha_composite(sub.resize((max(1, int(300 * min(1, pp))), max(1, int(250 * min(1, pp))))), (70, y))
    if t >= T("hook", 3):  # dotted flow with moving dot
        p = ease_io(min(1, (t - T("hook", 3)) / 1.6)); x0, x1 = 380, 620
        for i in range(0, 12):
            if i / 12 <= p: d.ellipse([x0 + (x1 - x0) * i / 12 - 7, 450 - 7, x0 + (x1 - x0) * i / 12 + 7, 450 + 7], fill=INKD + (255,))
        if p > 0.95: d.polygon([(x1, 420), (x1 + 44, 450), (x1, 480)], fill=INKD + (255,))
    if t >= T("hook", 5):
        pp = ease_back((t - T("hook", 5)) / 0.3); sub = Image.new("RGBA", (330, 280), (0, 0, 0, 0)); icon_chat(ImageDraw.Draw(sub), 20, 30, 220); card.alpha_composite(sub.resize((max(1, int(330 * min(1, pp))), max(1, int(280 * min(1, pp))))), (640, 300))
        d.text((640, 600), "Claude", font=BF(56), fill=INKD + (255,))
    # three steps
    for k, ts in enumerate((T("hook", 10), T("hook", 11), T("hook", 12))):
        if t >= ts: pp = ease_back((t - ts) / 0.28); cx = 200 + 280 * k; cy = 790; r = int(70 * min(1, pp)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CORAL + (255,), outline=INKD + (255,), width=5); d.text((cx - 22, cy - 56), str(k + 1), font=BF(110), fill=(255, 255, 255, 255)) if pp > 0.6 else None
    card_enter(base, card, 540, 670, t, b["t0"], rot=-0.8, dur=0.01)


# ---- S2 how: dark Claude app screen (real steps) ----
def fwin(t, S):
    w, h = 980, 1040; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); iy = h - 190
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(18, 18, 18, 255), outline=(42, 42, 42, 255), width=2)
    d.rounded_rectangle([0, 0, 210, h - 1], 30, fill=(12, 12, 12, 255)); d.rectangle([180, 0, 210, h], fill=(12, 12, 12, 255)); d.line([(210, 0), (210, h)], fill=(38, 38, 38, 255), width=2)
    d.text((26, 28), "Assistant", font=PF(32, True), fill=(255, 255, 255, 255))
    for k, nm in enumerate(["New chat", "Projects", "Artifacts", "Chats"]):
        if k == 0: d.rounded_rectangle([16, 100, 194, 148], 12, fill=(30, 30, 30, 255))
        d.text((34, 108 + 62 * k), nm, font=PF(24), fill=(235, 235, 235, 255) if k == 0 else (150, 150, 150, 255))
    d.line([(210, 98), (w, 98)], fill=(38, 38, 38, 255), width=2); d.text((250, 28), "New chat", font=PF(34, True), fill=(235, 235, 235, 255))
    d.text((250, 190), "How can I help you today?", font=PF(42, True), fill=(120, 120, 120, 255))
    drop = S["drop"]
    if drop[0] <= t < drop[1]:  # drop zone
        d.rounded_rectangle([236, 150, w - 30, iy - 30], 28, outline=OR + (255,), width=5, fill=(40, 26, 20, 255)); d.text((330, 460), "Drop files here", font=PF(54, True), fill=OR + (255,))
    d.rounded_rectangle([240, iy, w - 36, iy + 120], 32, fill=(22, 22, 22, 255), outline=OR + (255,) if t >= S["plus"] else (60, 60, 60, 255), width=3)
    d.ellipse([264, iy + 28, 328, iy + 92], fill=(48, 48, 48, 255)); d.line([(296, iy + 44), (296, iy + 76)], fill=(255, 255, 255, 255), width=6); d.line([(280, iy + 60), (312, iy + 60)], fill=(255, 255, 255, 255), width=6)
    # attached files (chips above the input)
    files = [("report.pdf", S["f1"], CORAL), ("photo.jpg", S["f2"], (96, 165, 250))]
    x = 250
    for nm, ft, col in files:
        if t >= ft:
            pp = ease_back((t - ft) / 0.28); c = Image.new("RGBA", (300, 70), (0, 0, 0, 0)); cd = ImageDraw.Draw(c); cd.rounded_rectangle([0, 0, 299, 69], 20, fill=(34, 34, 34, 255), outline=col + (255,), width=3)
            cd.rounded_rectangle([14, 14, 58, 56], 8, fill=col + (255,)); cd.text((70, 12), nm, font=PF(30, True), fill=(240, 240, 240, 255)); im.alpha_composite(c.resize((max(1, int(300 * min(1, pp))), max(1, int(70 * min(1, pp))))), (x, iy - 92)); x += 316
    if not (t >= S["f1"]): d.text((354, iy + 38), "Message...", font=PF(34), fill=(110, 110, 110, 255))
    if S["plus"] <= t < S["pick"] + 0.5:
        mp = min(1, ease_back((t - S["plus"]) / 0.22)); mw, mh = 540, 230; my = iy - 20 - mh; sel = t >= S["pick"]
        menu = Image.new("RGBA", (mw, mh), (0, 0, 0, 0)); md = ImageDraw.Draw(menu); md.rounded_rectangle([0, 0, mw - 1, mh - 1], 22, fill=(27, 27, 27, 255), outline=(58, 58, 58, 255), width=2)
        md.rounded_rectangle([14, 22, mw - 14, 112], 16, fill=OR + (255,) if sel else (40, 40, 40, 255)); md.text((34, 44), "Add files or photos", font=PF(36, True), fill=(17, 17, 17, 255) if sel else (235, 235, 235, 255))
        md.text((34, 140), "Take a screenshot", font=PF(30), fill=(150, 150, 150, 255)); im.alpha_composite(menu.resize((max(1, int(mw * (0.9 + 0.1 * mp))), max(1, int(mh * (0.9 + 0.1 * mp))))), (240, int(my + (1 - mp) * 20)))
    return im


def S_how(b):
    t0 = b["t0"]; iy = 1040 - 190; plus = T("how", 6); pick = T("how", 11); d0 = T("how", 17)
    return dict(plus=plus, pick=pick, f1=T("how", 15) + 0.1, f2=T("how", 21) + 0.1, drop=(d0 + 0.4, T("how", 21)),
                cur=[(t0, 720, 500), (plus - 0.3, 296, iy + 60), (pick - 0.3, 480, iy - 20 - 230 + 66), (T("how", 15) + 0.4, 600, 520), (b["t1"], 640, 560)], clicks=[plus, pick])


def s_how(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 255))); S = S_how(b)
    punch = max([0.03 * max(0, 1 - (t - c) / 0.25) for c in S["clicks"] if t >= c] or [0.0]); sc = 0.94 + 0.06 * ease_out(min(1, lt / 0.3)) + 0.05 * min(1, lt / 8.0) + punch
    win = fwin(t, S); cx, cy = walk_cursor(S, t); layer = Image.new("RGBA", win.size, (0, 0, 0, 0)); layer.alpha_composite(win)
    # dragged file icon (drag and drop) from outside the window into the input
    d0 = T("how", 17); d1 = T("how", 21)
    if d0 <= t < d1 + 0.1:
        q = ease_io((t - d0) / max(0.2, d1 - d0)); dx = 1060 - (1060 - 560) * q; dy = 300 + (840 - 300) * q; ic = Image.new("RGBA", (130, 110), (0, 0, 0, 0)); icon_photo(ImageDraw.Draw(ic), 6, 8, 90); place(layer, ic, dx, dy, 1.0, 0.95)
    elif t < d0: place(layer, CUR, cx + 24, cy + 32)
    for c in S["clicks"]:
        if 0 <= t - c <= 0.4: rr = int(20 + 70 * (t - c) / 0.4); ImageDraw.Draw(layer).ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=OR + (255,), width=6)
    place(base, shadow(980, 1040, 30, 40, 40, 150), 540, 740, sc); place(base, layer, 540, 740, sc)
    for txt, ts, te in (("STEP 1  CLICK +", b["t0"], T("how", 8)), ("STEP 2  ADD FILES OR PHOTOS", T("how", 8), T("how", 14)), ("STEP 3  PICK THE FILE", T("how", 14), T("how", 17)), ("OR DRAG AND DROP", T("how", 17), b["t1"])):
        if ts <= t < te: pp = pop(t, ts + 0.03); place(base, chip(txt, 46, OR, (17, 17, 17), pad=(28, 8), r=24), 540, 160, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    place(base, chip("Illustration", 24, (40, 40, 40), (200, 200, 200), pad=(18, 4), r=12), 540, 1318)


# ---- S3 types: checklist + big number ----
def s_types(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    card = sk_card(940, 700, (255, 255, 255)); d = ImageDraw.Draw(card); tape(card, 70, -14, -5)
    d.text((50, 36), "Works with", font=BF(72), fill=INKD + (255,))
    rows = (("PDF", T("types", 0), CORAL), ("Word", T("types", 1), (96, 165, 250)), ("CSV", T("types", 2), (74, 190, 120)), ("Text", T("types", 3), (170, 120, 230)), ("Photos", T("types", 5), (255, 170, 60)))
    for k, (nm, ts, col) in enumerate(rows):
        y = 150 + 105 * k; on = t >= ts - 0.05; a = 255 if on else 70
        d.rounded_rectangle([50, y, 890, y + 86], 22, fill=(250, 246, 238, 255) if on else (245, 243, 238, 255), outline=INKD + (a,), width=4)
        d.rounded_rectangle([70, y + 14, 130, y + 72], 12, fill=col + (a,)); d.text((160, y + 8), nm, font=BF(60), fill=INKD + (a,))
        if on: pp = ease_back((t - ts) / 0.25); tick(d, 810, y + 14, int(58 * min(1, pp)))
    card_enter(base, card, 540, 490, t, b["t0"], rot=-0.8, dur=0.01)
    num = sk_card(900, 360, PEACH); nd = ImageDraw.Draw(num)
    nd.text((60, 6), "20", font=BF(300), fill=INKD + (255,)); nd.text((420, 70), "files", font=BF(110), fill=INKD + (255,)); nd.text((420, 190), "in one chat", font=BF(70), fill=CORAL + (255,))
    card_enter(base, num, 540, 1075, t, T("types", 9), rot=1.0, side=1)


# ---- S4 caution: PDF up to 100 pages vs more + the one doc note ----
def pdf_page(w, h, with_chart, chart_t, t):
    im = sk_card(w, h, (255, 255, 255), 24, 8); d = ImageDraw.Draw(im)
    for k in range(5): d.line([(40, 60 + 38 * k), (w - 40 - (60 if k % 2 else 0), 60 + 38 * k)], fill=(170, 170, 175, 255), width=6)
    cy0 = 270
    if with_chart:
        p = ease_out(min(1, max(0, (t - chart_t) / 0.7))); d.rectangle([40, cy0, w - 40, cy0 + 170], outline=INKD + (255,), width=4)
        for k, hh in enumerate((0.5, 0.9, 0.65, 0.4)): d.rectangle([70 + 80 * k, cy0 + 160 - int(130 * hh * p), 120 + 80 * k, cy0 + 160], fill=CORAL + (255,))
        icon_photo(d, w - 150, cy0 + 20, 70)
    else:
        for k in range(4): d.line([(40, cy0 + 20 + 38 * k), (w - 40 - (60 if k % 2 else 0), cy0 + 20 + 38 * k)], fill=(170, 170, 175, 255), width=6)
    return im


def s_caution(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    a = pdf_page(420, 470, True, T("caution", 9), t); card_enter(base, a, 290, 340, t, b["t0"], rot=-2, dur=0.01)
    c = pdf_page(420, 470, False, 0, t); card_enter(base, c, 790, 340, t, T("caution", 15) - 0.3, rot=2, side=1)
    clabel(base, "UP TO 100 PAGES", 290, 640, t, T("caution", 2), size=44); clabel(base, "TEXT + CHARTS", 290, 710, t, T("caution", 8), size=44, fill=(74, 190, 120))
    clabel(base, "OVER 100 PAGES", 790, 640, t, T("caution", 15), size=44, fill=INKD); clabel(base, "TEXT ONLY", 790, 710, t, T("caution", 19), size=44, fill=(150, 150, 160))
    h0, h1 = T("caution", 2), T("caution", 14); hp = min(1, max(0, (t - h0) / max(0.3, h1 - h0))); card_enter(base, note("pdf100", 900, 380, hp), 540, 1040, t, b["t0"] + 0.3, rot=0.8, side=0)
    place(base, chip(SRC, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, 1268)


# ---- S5 tip: PDF viewer page number vs printed page number ----
def s_tip(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    card = sk_card(940, 1010, (238, 240, 245)); d = ImageDraw.Draw(card); tape(card, 70, -14, -5)
    d.rounded_rectangle([0, 0, 940, 90], 34, fill=(60, 64, 78, 255)); d.rectangle([0, 50, 940, 90], fill=(60, 64, 78, 255)); d.text((36, 18), "PDF viewer", font=PF(34, True), fill=(255, 255, 255, 255))
    vp = pop(t, T("tip", 7) - 0.1); pill = Image.new("RGBA", (230, 64), (0, 0, 0, 0)); pd = ImageDraw.Draw(pill); pd.rounded_rectangle([0, 0, 229, 63], 30, fill=(255, 255, 255, 255), outline=GREEN + (255,), width=4); pd.text((22, 10), "12 / 40", font=PF(34, True), fill=INKD + (255,))
    if t >= T("tip", 7) - 0.1: card.alpha_composite(pill.resize((max(1, int(230 * min(1, vp))), max(1, int(64 * min(1, vp))))), (680, 12))
    page = sk_card(560, 760, (255, 255, 255), 14, 8); pd2 = ImageDraw.Draw(page)
    for k in range(7): pd2.line([(40, 60 + 46 * k), (520 - (70 if k % 3 == 0 else 0), 60 + 46 * k)], fill=(170, 170, 175, 255), width=7)
    pd2.text((250, 690), "5", font=BF(70), fill=INKD + (255,))
    card.alpha_composite(page, (70, 150))
    if t >= T("tip", 13):
        cp = ease_back((t - T("tip", 13)) / 0.28); cross(d, 700, 700, int(110 * min(1, cp))); d.text((660, 820), "printed no. 5", font=BF(54), fill=RED + (255,)) if cp > 0.8 else None
    if t >= T("tip", 10):
        tp = ease_back((t - T("tip", 10)) / 0.28); tick(d, 700, 300, int(110 * min(1, tp))); d.text((660, 424), "use this", font=BF(54), fill=GREEN + (255,)) if tp > 0.8 else None
    card_enter(base, card, 540, 740, t, b["t0"], rot=-0.6, dur=0.01)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    place(base, robot("wave", 760), 540, 640 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill, col) in enumerate((("SAVE THIS TIP", T("cta", 5), INKD, (255, 255, 255)), ("COMMENT  FILES", T("cta", 8), CORAL, (255, 255, 255)))):
        pp = pop(t, ts); place(base, chip(txt, 64, fill, col, pad=(40, 10), r=28), 540, 1110 + 120 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


def beats():
    B = []
    B.append(dict(k="hook", t0=0.0, t1=T("how", 0)))
    B.append(dict(k="how", t0=T("how", 0), t1=T("types", 0)))
    B.append(dict(k="types", t0=T("types", 0), t1=T("caution", 0)))
    B.append(dict(k="caution", t0=T("caution", 0), t1=T("tip", 0)))
    B.append(dict(k="tip", t0=T("tip", 0), t1=T("cta", 0)))
    B.append(dict(k="cta", t0=T("cta", 0), t1=TOTAL + 1))
    return B


B = beats()
FN = dict(hook=s_hook, how=s_how, types=s_types, caution=s_caution, tip=s_tip, cta=s_cta)
SR = 24000


def build_audio(out):
    """voice only; no whoosh / swipe sounds; music is mixed by encode()"""
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = Image.new("RGBA", (W, H)); FN[b["k"]](base, t, b); caption(base, t, "ui")
    return np.array(base.convert("RGB"))


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['k'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/d_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice_f4.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_f4.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
