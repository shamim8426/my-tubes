"""067 Short: Claude Code website live link (AweShell). Light InsiderForce-style presentation (brand/INSIDERFORCE_STYLE.md): flat light background,
word-by-word mixed-weight text, soft-shadow white cards with moving content (UI mock-ups + free Pixabay clips), icon on a string, collage pop-ins.
Run: python make.py frames t1 t2 ...  |  python make.py (render)"""
import json, math, sys, wave, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import W, H, FPS, ease_out, ease_back, ease_io, wav_dur, encode

LEAD, AFTER = 0.05, 0.05
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START))
BG = (243, 243, 244); INK = (24, 24, 30); GREY = (118, 118, 126); ACC = (37, 99, 235); GREEN = (22, 163, 74); RED = (225, 45, 57); TERM = (22, 24, 30)
TGREEN = (74, 222, 128); TGREY = (150, 156, 170); WHITE = (255, 255, 255)


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz, kind="bold"):
    key = (sz, kind)
    if key not in _fc:
        f = {"bold": "Poppins-Bold.ttf", "med": "Poppins-Medium.ttf", "mono": "IBMPlexMono-Bold.ttf"}[kind]
        _fc[key] = ImageFont.truetype(str(ROOT / "shared/fonts" / f), sz)
    return _fc[key]


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def shadow(w, h, r=26):
    sh = Image.new("RGBA", (w + 240, h + 240), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([120 + 24, 120 + 44, 120 + 24 + w, 120 + 44 + h], r, fill=(0, 0, 0, 62))
    return sh.filter(ImageFilter.GaussianBlur(34))


_sh = {}
def card(w, h, content=None, r=26, fill=(255, 255, 255)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, w - 1, h - 1], r, fill=fill + (255,))
    if content is not None:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
        c = content.convert("RGBA").resize((w, h)); c.putalpha(m); im.alpha_composite(c)
    return im


def enter(base, spr, cx, cy, t, t0, side=0, dur=0.42, float_amp=7, rot=0.0, shad=True, t_out=None, sway=1.6):
    lt = t - t0
    if lt < 0: return
    fade = 1.0; xo = 0
    if t_out is not None and t > t_out:
        q = ease_io((t - t_out) / 0.35)
        if q >= 1: return
        fade = 1 - q; xo = (-1 if side <= 0 else 1) * q * 380
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur))
    dx = side * (1 - q) * 640 + xo; dy = (1 - q) * (170 if side == 0 else 0); sc = (0.86 + 0.14 * e) * (1 - 0.12 * (1 - fade))
    fl = float_amp * math.sin(lt * 2.2 + cx * 0.01) if lt > dur else 0
    rr = rot + (sway * math.sin(lt * 1.4 + cy * 0.01) if lt > dur else 0)
    w, h = spr.size
    if shad:
        key = (w, h)
        if key not in _sh: _sh[key] = shadow(w, h)
        place(base, _sh[key], cx + dx, cy + dy + fl, sc, min(1, q * 1.4) * fade, rr)
    place(base, spr, cx + dx, cy + dy + fl, sc, min(1, q * 1.4) * fade, rr)


def starburst(base, cx, cy, t, t0, col=ACC):
    lt = t - t0
    if lt < 0 or lt > 0.9: return
    q = ease_out(lt / 0.5); a = 1 - ease_io(lt / 0.9); d = ImageDraw.Draw(base)
    for i in range(7):
        ang = math.radians(-100 + i * 26); r0 = 14 + 40 * q; r1 = r0 + 30 * (1 - lt / 0.9)
        d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))], fill=col + (int(255 * a),), width=7)


_ic = {}
def icon_string(base, t, t0, cx, y, kind, col=ACC):
    """Glossy icon in a white circle hanging from a thin line (drops in, swings)."""
    lt = t - t0
    if lt < 0: return
    q = ease_out(min(1, lt / 0.45)); yy = -120 + (y + 120) * q + (14 * math.sin(lt * 9) * math.exp(-lt * 4) if lt > 0.4 else 0)
    d = ImageDraw.Draw(base); d.line([(cx, 0), (cx, yy - 70)], fill=(170, 170, 176, 255), width=3)
    if kind not in _ic:
        ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); di = ImageDraw.Draw(ic); di.ellipse([10, 10, 170, 170], fill=(255, 255, 255, 255))
        di.ellipse([40, 40, 140, 140], fill=col + (255,)); di.ellipse([52, 48, 98, 84], fill=(255, 255, 255, 70))
        if kind == "term": di.text((52, 62), ">_", font=font(44, "mono"), fill=(255, 255, 255, 255))
        elif kind == "plus": di.rectangle([84, 56, 96, 124], fill=(255, 255, 255, 255)); di.rectangle([56, 84, 124, 96], fill=(255, 255, 255, 255))
        elif kind == "phone": di.rounded_rectangle([64, 50, 116, 130], 10, outline=(255, 255, 255, 255), width=6)
        _ic[kind] = ic
    if "sh" not in _ic: _ic["sh"] = shadow(180, 180, 90)
    place(base, _ic["sh"], cx, yy, 0.6); place(base, _ic[kind], cx, yy, 1.0)


# ---- word-by-word text: phrases = [(token_index, "text with *bold* words"), ...] ----
_wc = {}
def wsprite(word, bold, mono=False):
    k = (word, bold, mono)
    if k not in _wc:
        f = font(66, "mono" if mono else ("bold" if bold else "med")); col = INK if bold else GREY
        w = int(f.getlength(word)) + 6; im = Image.new("RGBA", (w, 100), (0, 0, 0, 0)); ImageDraw.Draw(im).text((3, 6), word, font=f, fill=col + (255,)); _wc[k] = im
    return _wc[k]


def run_text(base, t, scene, phrases, y=1330, maxw=940):
    end = SC[scene] + D[IDS.index(scene)]
    cur = None
    for j, (k, txt) in enumerate(phrases):
        a = T(scene, k) - 0.05 if j else SC[scene]; b = (T(scene, phrases[j + 1][0]) - 0.05) if j + 1 < len(phrases) else end
        if a <= t < b: cur = (a, b, txt)
    if not cur: return
    a, b, txt = cur; items = []
    for w in txt.split(" "):
        mono = "`" in w; w = w.replace("`", "")
        bold = "*" in w; items.append((w.replace("*", ""), bold or mono, mono))
    span = min(1.5, max(0.5, (b - a) * 0.75)); n = len(items)
    lines = [[]]; cw = 0; sp = font(66, "med").getlength(" ")
    for it in items:
        wl = wsprite(*it).width
        if cw + wl > maxw and lines[-1]: lines.append([]); cw = 0
        lines[-1].append(it); cw += wl + sp
    idx = 0; y0 = y - 42 * (len(lines) - 1)
    for li, ln in enumerate(lines):
        tw = sum(wsprite(*it).width for it in ln) + sp * (len(ln) - 1); x = 540 - tw / 2
        for it in ln:
            ts = a + span * idx / max(1, n); idx += 1; spr = wsprite(*it)
            q = ease_out(min(1, (t - ts) / 0.22)) if t >= ts else 0; sp2 = ease_back(min(1, (t - ts) / 0.34)) if t >= ts else 0
            xa = 1.0 if (b - t) > 0.12 else max(0, (b - t) / 0.12)
            if q > 0: place(base, spr, x + spr.width / 2, y0 + 84 * li + 34 * (1 - sp2) + spr.height / 2 - 50, (0.7 + 0.3 * sp2) if it[1] else 1.0, q * xa)
            x += spr.width + sp


def watermark(base):
    ImageDraw.Draw(base).text((540 - font(34, "med").getlength("DevRoboLab") / 2, 1748), "DevRoboLab", font=font(34, "med"), fill=(196, 196, 202, 255))


_vc = {}
def clip_card(kind, t, w, h, speed=1.0, r=26):
    folder = HERE / "raw" / kind; n = len(list(folder.glob("*.jpg"))) if kind not in _vc else _vc[kind]; _vc[kind] = n; i = int(t * 30 * speed) % n + 1
    key = (kind, i)
    if key not in _vc: _vc[key] = Image.open(folder / f"{i:04d}.jpg").convert("RGB")
    im = _vc[key]; sc = max(w / im.width, h / im.height); im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.BILINEAR)
    l, tp = (im.width - w) // 2, (im.height - h) // 2
    return card(w, h, im.crop((l, tp, l + w, tp + h)), r)


def term_card(w, h, t, lines, title="Terminal", cps=20):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=TERM + (255,)); d.rounded_rectangle([0, 0, w - 1, 56], 24, fill=(44, 47, 58, 255)); d.rectangle([0, 34, w - 1, 56], fill=(44, 47, 58, 255))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))): d.ellipse([22 + 36 * i, 18, 42 + 36 * i, 38], fill=c + (255,))
    d.text((150, 10), title, font=font(26, "med"), fill=TGREY + (255,))
    y = 84
    for txt, tt, col, typed in lines:
        if t < tt: continue
        if typed: d.text((30, y), ">", font=font(38, "mono"), fill=TGREEN + (255,)); d.text((72, y), txt[:int((t - tt) * cps) + 1], font=font(38, "mono"), fill=(255, 255, 255, 255))
        else: d.text((30, y), txt, font=font(32, "mono"), fill=col + (255,))
        y += 62
    return im


def qr_img(size, seed=7):
    n = 21; random.seed(seed); im = Image.new("RGBA", (size, size), (255, 255, 255, 255)); d = ImageDraw.Draw(im); c = size / (n + 2)
    for y in range(n):
        for x in range(n):
            if (x < 8 and y < 8) or (x > 12 and y < 8) or (x < 8 and y > 12): continue
            if random.random() < 0.5: d.rectangle([(x + 1) * c, (y + 1) * c, (x + 2) * c, (y + 2) * c], fill=INK + (255,))
    for ox, oy in ((0, 0), (14, 0), (0, 14)):
        d.rectangle([(ox + 1) * c, (oy + 1) * c, (ox + 8) * c, (oy + 8) * c], fill=INK + (255,)); d.rectangle([(ox + 2) * c, (oy + 2) * c, (ox + 7) * c, (oy + 7) * c], fill=(255, 255, 255, 255))
        d.rectangle([(ox + 3) * c, (oy + 3) * c, (ox + 6) * c, (oy + 6) * c], fill=INK + (255,))
    return im
QR = qr_img(380)


def pill(text, size, fill, color=WHITE, pad=(34, 14), r=30, kind="bold"):
    f = font(size, kind); tw = int(f.getlength(text)); asc, desc = f.getmetrics()
    im = Image.new("RGBA", (tw + 2 * pad[0], asc + desc + 2 * pad[1]), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=fill + (255,)); d.text((pad[0], pad[1]), text, font=f, fill=color + (255,)); return im


def dotted(base, x0, y0, x1, y1, t, t0):
    if t < t0: return
    d = ImageDraw.Draw(base); L = math.hypot(x1 - x0, y1 - y0); q = ease_out(min(1, (t - t0) / 0.5)); n = max(2, int(L / 30))
    for i in range(n):
        f = i / n
        if f > q: break
        ph = (f * 8 - t * 3) % 1; r = 6 + 4 * max(0, 1 - ph * 2)
        d.ellipse([x0 + (x1 - x0) * f - r, y0 + (y1 - y0) * f - r, x0 + (x1 - x0) * f + r, y0 + (y1 - y0) * f + r], fill=ACC + (255,))


# ---------------- 067 helpers + beats ----------------
def cube_icon():
    if "cube" in _ic: return _ic["cube"]
    ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(ic); d.ellipse([10, 10, 170, 170], fill=(255, 255, 255, 255))
    cx, cy, r = 90, 90, 48
    top = [(cx, cy - r), (cx + r * .87, cy - r / 2), (cx, cy), (cx - r * .87, cy - r / 2)]
    left = [(cx - r * .87, cy - r / 2), (cx, cy), (cx, cy + r), (cx - r * .87, cy + r / 2)]
    right = [(cx + r * .87, cy - r / 2), (cx + r * .87, cy + r / 2), (cx, cy + r), (cx, cy)]
    d.polygon(top, fill=(125, 170, 255, 255)); d.polygon(left, fill=(37, 99, 235, 255)); d.polygon(right, fill=(24, 60, 160, 255)); _ic["cube"] = ic; return ic


def hang(base, t, t0, cx, y, spr, swing=True):
    lt = t - t0
    if lt < 0: return
    q = ease_out(min(1, lt / 0.45)); yy = -120 + (y + 120) * q + (14 * math.sin(lt * 9) * math.exp(-lt * 4) if lt > 0.4 else 0)
    xx = cx + (8 * math.sin(lt * 1.6) if swing and lt > 0.5 else 0)
    ImageDraw.Draw(base).line([(xx, 0), (xx, yy - 70)], fill=(170, 170, 176, 255), width=3)
    if "sh" not in _ic: _ic["sh"] = shadow(180, 180, 90)
    place(base, _ic["sh"], xx, yy, 0.6); place(base, spr, xx, yy, 1.0)


def circle_icon(label, col, size=44):
    k = ("c", label)
    if k not in _ic:
        ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(ic); d.ellipse([10, 10, 170, 170], fill=(255, 255, 255, 255)); d.ellipse([34, 34, 146, 146], fill=col + (255,))
        d.ellipse([46, 40, 96, 76], fill=(255, 255, 255, 70)); f = font(size, "bold"); w = f.getlength(label); d.text((90 - w / 2, 90 - size * 0.7), label, font=f, fill=WHITE + (255,)); _ic[k] = ic
    return _ic[k]


def gear_icon(angle):
    ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(ic); d.ellipse([10, 10, 170, 170], fill=(255, 255, 255, 255))
    g = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); dg = ImageDraw.Draw(g); dg.ellipse([50, 50, 130, 130], fill=INK + (255,))
    for i in range(8):
        a = math.radians(i * 45); x, y = 90 + 52 * math.cos(a), 90 + 52 * math.sin(a); dg.ellipse([x - 14, y - 14, x + 14, y + 14], fill=INK + (255,))
    dg.ellipse([72, 72, 108, 108], fill=(255, 255, 255, 255)); g = g.rotate(angle, resample=Image.BICUBIC); ic.alpha_composite(g); return ic


def site_mock(w, h, t, title="Mera Portfolio"):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=(14, 16, 24, 255))
    d.rectangle([0, 0, w, 46], fill=(30, 33, 44, 255))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))): d.ellipse([20 + 28 * i, 16, 34 + 28 * i, 30], fill=c + (255,))
    ox = w * 0.5 + w * 0.28 * math.sin(t * 1.1); oy = h * 0.62 + h * 0.12 * math.cos(t * 1.7)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dg = ImageDraw.Draw(glow); dg.ellipse([ox - 90, oy - 90, ox + 90, oy + 90], fill=(60, 110, 255, 150)); glow = glow.filter(ImageFilter.GaussianBlur(40)); im.alpha_composite(glow)
    d = ImageDraw.Draw(im); f = font(int(h * 0.12), "bold"); n = int(t * 14) % (len(title) + 14); d.text((w * 0.08, h * 0.26), title[:n], font=f, fill=WHITE + (255,))
    d.rounded_rectangle([w * 0.08, h * 0.5, w * 0.08 + w * 0.26, h * 0.5 + h * 0.13], 14, fill=(255, 255, 255, 255)); d.rounded_rectangle([w * 0.08, h * 0.74, w * 0.9, h * 0.76], 4, fill=(60, 64, 80, 255))
    d.rounded_rectangle([w * 0.08, h * 0.74, w * 0.08 + w * 0.82 * ((t * 0.35) % 1), h * 0.76], 4, fill=(60, 110, 255, 255))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=255); a = im.getchannel("A"); im.putalpha(Image.fromarray(np.minimum(np.asarray(a), np.asarray(m)))); return im


def url_pill(t, t0, text="https://my-site-4f2a...", cps=24):
    s = text[:max(0, int((t - t0) * cps))] if t >= t0 else ""
    im = Image.new("RGBA", (760, 84), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, 759, 83], 42, fill=WHITE + (255,))
    d.ellipse([26, 24, 62, 60], outline=GREY + (255,), width=4); d.line([(26, 42), (62, 42)], fill=GREY + (255,), width=3)
    d.text((86, 20), s, font=font(32, "med"), fill=INK + (255,)); d.rounded_rectangle([700, 26, 724, 52], 5, outline=GREY + (255,), width=3); return im


def file_card(label, sub, col):
    im = Image.new("RGBA", (300, 340), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, 299, 339], 28, fill=WHITE + (255,))
    d.rounded_rectangle([90, 40, 210, 170], 14, fill=col + (255,)); d.polygon([(170, 40), (210, 80), (170, 80)], fill=(255, 255, 255, 140))
    d.text((150 - font(40, "bold").getlength(label) / 2, 200), label, font=font(40, "bold"), fill=INK + (255,)); d.text((150 - font(26, "med").getlength(sub) / 2, 262), sub, font=font(26, "med"), fill=GREY + (255,)); return im


def folder_card():
    im = Image.new("RGBA", (300, 340), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, 299, 339], 28, fill=WHITE + (255,))
    d.rounded_rectangle([80, 70, 150, 100], 8, fill=(253, 186, 116, 255)); d.rounded_rectangle([80, 88, 220, 170], 12, fill=(251, 146, 60, 255))
    d.text((150 - font(40, "bold").getlength("build/") / 2, 200), "build/", font=font(40, "bold"), fill=INK + (255,)); d.text((150 - font(26, "med").getlength("folder") / 2, 262), "folder", font=font(26, "med"), fill=GREY + (255,)); return im


def prompt_card(t, t0):
    im = Image.new("RGBA", (780, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, 779, 399], 30, fill=WHITE + (255,))
    for i, w in enumerate((640, 560, 600, 380)): d.rounded_rectangle([50, 56 + 42 * i, 50 + w, 74 + 42 * i], 9, fill=(225, 226, 232, 255))
    on = t >= t0; d.rounded_rectangle([50, 280, 730, 360], 24, fill=((22, 163, 74) if on else (99, 102, 241)) + (255,))
    lab = "Copied" if on else "Copy prompt"; d.text((390 - font(34, "bold").getlength(lab) / 2, 298), lab, font=font(34, "bold"), fill=WHITE + (255,)); return im


def cursor(base, x, y):
    ImageDraw.Draw(base).polygon([(x, y), (x, y + 56), (x + 16, y + 42), (x + 30, y + 70), (x + 42, y + 64), (x + 28, y + 38), (x + 48, y + 36)], fill=WHITE + (255,), outline=INK + (255,))


def b_hook(base, t, b):
    hang(base, t, 0.05, 540, 150, cube_icon())
    enter(base, site_mock(780, 500, t), 540, 560, t, 0.05, side=0, dur=0.4)
    starburst(base, 130, 360, t, 0.3)
    if t >= T("hook", 15): enter(base, url_pill(t, T("hook", 15) + 0.2), 540, 940, t, T("hook", 15), side=0, dur=0.35)
    run_text(base, t, "hook", [(0, "Claude Code ki *website*"), (5, "*sabke liye* live?"), (11, "Bas *ek tool*"), (15, "Milega *public link*")], y=1120)


def b_setup(base, t, b):
    hang(base, t, b["t0"] + 0.05, 300, 140, circle_icon("Awe", ACC, 40))
    enter(base, prompt_card(t, T("setup", 7)), 540, 600, t, T("setup", 5) - 0.2, side=1, dur=0.4)
    starburst(base, 880, 420, t, T("setup", 5))
    if t >= T("setup", 7) - 0.3:
        q = ease_io(min(1, (t - T("setup", 7) - 0.3) / 0.4)); cursor(base, 880 - 160 * q, 800 - 120 * q)
    if t >= T("setup", 13) - 0.1:
        hang(base, t, T("setup", 13) - 0.1, 800, 170, gear_icon((t - T("setup", 13)) * 140))
    run_text(base, t, "setup", [(0, "Tool: *AweShell*"), (5, "Ek *prompt* copy karo"), (9, "*Agent* ko do"), (13, "*Setup* agent khud karega")], y=1120)


def b_publish(base, t, b):
    hang(base, t, b["t0"] + 0.05, 540, 140, cube_icon())
    enter(base, pill("Site publish karo", 44, ACC, WHITE, pad=(40, 18), r=34), 700, 420, t, T("publish", 2) - 0.1, side=1, dur=0.35)
    for i, (lab, col) in enumerate((("HTML", (59, 130, 246)), ("CSS", (234, 88, 12)), ("JS", (234, 179, 8)))):
        tt = T("publish", 8) + 0.15 * i
        if t >= tt:
            q = (t - tt) / 1.4; x = 330 + 190 * i
            if q < 1: place(base, file_card(lab, "", col).resize((130, 148)), x, 960 - 480 * ease_io(q), 1, 1 - max(0, q - 0.7) / 0.3)
    if t >= T("publish", 13):
        enter(base, site_mock(640, 400, t, "Live site"), 540, 640, t, T("publish", 13) - 0.1, side=0)
        enter(base, pill("LIVE", 40, GREEN, WHITE, pad=(34, 12), r=28), 800, 440, t, T("publish", 14), side=0, dur=0.3)
        enter(base, url_pill(t, T("publish", 15)), 540, 940, t, T("publish", 15) - 0.1, side=0, dur=0.3)
    run_text(base, t, "publish", [(0, "Bas bolo"), (2, "*Site publish karo*"), (6, "Agent *files upload* karta hai"), (12, "Milta hai *live link*")], y=1120)


def b_types(base, t, b):
    hang(base, t, b["t0"] + 0.05, 540, 130, cube_icon())
    enter(base, file_card("HTML", "ek file", (59, 130, 246)), 250, 500, t, T("types", 1), side=-1, rot=-3)
    enter(base, file_card("ZIP", "zipped project", (124, 58, 237)), 540, 620, t, T("types", 4), side=0, rot=2)
    enter(base, folder_card(), 830, 500, t, T("types", 7), side=1, rot=-2)
    starburst(base, 540, 450, t, T("types", 4))
    if t >= T("types", 15):
        enter(base, pill("25 MB / file", 46, INK, WHITE, pad=(36, 16), r=30), 330, 940, t, T("types", 16), side=-1, dur=0.3)
        enter(base, pill("100 MB total", 46, ACC, WHITE, pad=(36, 16), r=30), 760, 1030, t, T("types", 23), side=1, dur=0.3)
    run_text(base, t, "types", [(0, "*HTML*, *zip* ya *folder*"), (10, "Sab *chalta* hai"), (13, "Par *limit* hai")], y=1160)


def b_manual(base, t, b):
    hang(base, t, b["t0"] + 0.05, 540, 130, circle_icon("UP", ACC, 46))
    zone = Image.new("RGBA", (780, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(zone); d.rounded_rectangle([0, 0, 779, 459], 30, fill=WHITE + (255,))
    for i in range(0, 700, 36): d.line([(40 + i, 40), (62 + i, 40)], fill=(190, 190, 200, 255), width=4); d.line([(40 + i, 420), (62 + i, 420)], fill=(190, 190, 200, 255), width=4)
    d.text((390 - font(40, "bold").getlength("Drop files here") / 2, 340), "Drop files here", font=font(40, "bold"), fill=GREY + (255,)); d.polygon([(390, 120), (350, 180), (430, 180)], fill=ACC + (255,)); d.rectangle([378, 180, 402, 250], fill=ACC + (255,))
    enter(base, zone, 540, 620, t, T("manual", 4) - 0.2, side=0)
    ta, tb = T("manual", 11), T("manual", 15)
    if ta <= t < tb + 0.3:
        q = ease_io(min(1, (t - ta) / (tb - ta))); x = 920 - 380 * q; y = 1000 - 460 * q
        place(base, file_card("site", "", (59, 130, 246)).resize((150, 170)), x, y, 1 - 0.2 * q, 1 - max(0, (t - tb) / 0.3)); cursor(base, x + 40, y + 30)
    if t >= T("manual", 16):
        enter(base, url_pill(t, T("manual", 16) + 0.15), 540, 960, t, T("manual", 16), side=0, dur=0.3)
        enter(base, pill("link ready", 40, GREEN, WHITE, pad=(30, 12), r=26), 540, 1060, t, T("manual", 17), side=0, dur=0.3)
    run_text(base, t, "manual", [(0, "Chaho to *khud* bhi"), (7, "File ya folder *drag & drop*"), (16, "*Link* taiyaar")], y=1170)


def b_agents(base, t, b):
    for xx, lab, col, k in ((250, "G", (66, 133, 244), 1), (540, "C", (22, 163, 74), 2), (830, "...", (24, 24, 30), 5)):
        hang(base, t, T("agents", k) - 0.1, xx, 220, circle_icon(lab, col, 56))
    for xx, nm, k in ((250, "Gemini", 1), (540, "Codex", 2), (830, "Any agent", 5)):
        if t >= T("agents", k) + 0.3: enter(base, pill(nm, 36, WHITE, INK, pad=(28, 10), r=24), xx, 430, t, T("agents", k) + 0.3, side=0, dur=0.3)
    if t >= T("agents", 11):
        enter(base, term_card(820, 200, t, [("publish my site", T("agents", 12) - 0.2, WHITE, True)], title="agent"), 540, 760, t, T("agents", 11) - 0.2, side=0)
    run_text(base, t, "agents", [(0, "Chalta hai *Gemini*"), (2, "*Codex*"), (4, "aur *har agent* ke saath"), (10, "Jo *commands* chala sake")], y=1120)


def b_cta(base, t, b):
    hang(base, t, b["t0"] + 0.05, 540, 260, cube_icon())
    lt = t - T("cta", 5)
    enter(base, pill("Follow", 80, INK, WHITE, pad=(90, 30), r=60), 540, 760, t, b["t0"] + 0.3, side=0, dur=0.4)
    if t >= T("cta", 4):
        q = ease_io(min(1, (t - T("cta", 4)) / 0.5)); cursor(base, 900 - 300 * q, 1000 - 200 * q)
        if 0 < lt < 0.6:
            r = int(20 + 90 * lt / 0.6); ImageDraw.Draw(base).ellipse([640 - r, 800 - r, 640 + r, 800 + r], outline=ACC + (int(255 * (1 - lt / 0.6)),), width=6)
    run_text(base, t, "cta", [(0, "Aur *AI tricks* ke liye"), (4, "*Follow* karo")], y=1120)


KS = ["hook", "setup", "publish", "types", "manual", "agents", "cta"]
B = [dict(k=k, t0=(0.0 if i == 0 else SC[k]), t1=(SC[KS[i + 1]] if i + 1 < len(KS) else TOTAL + 1)) for i, k in enumerate(KS)]
FN = dict(hook=b_hook, setup=b_setup, publish=b_publish, types=b_types, manual=b_manual, agents=b_agents, cta=b_cta)

SR = 24000


def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


BGIM = Image.new("RGBA", (W, H), BG + (255,))
def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = BGIM.copy(); FN[b["k"]](base, t, b); watermark(base)
    p = min(1, max(0, (t - b["t0"]) / max(1.0, b["t1"] - b["t0"]))); z = 1.0 + 0.05 * p; im = base.convert("RGB")
    cw, ch = int(W / z), int(H / z); cx0 = int((W - cw) * (0.3 + 0.4 * p)); cy0 = int((H - ch) * 0.35)
    return np.array(im.crop((cx0, cy0, cx0 + cw, cy0 + ch)).resize((W, H), Image.BILINEAR))


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['k'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/frames/d_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice.wav")
    n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
