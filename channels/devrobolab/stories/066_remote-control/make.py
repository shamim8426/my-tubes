"""066 How-to Short: Claude Code Remote Control. Light InsiderForce-style presentation (brand/INSIDERFORCE_STYLE.md): flat light background,
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
        mono = w.startswith("`"); w = w.strip("`")
        bold = w.startswith("*"); items.append((w.strip("*"), bold or mono, mono))
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


def clip_card(kind, t, w, h, speed=1.0, r=26):
    """Drawn mock that matches the script (no stock footage): laptop = Claude Code terminal, phone = Claude app chat, photo = picture attachment."""
    if kind == "laptop":
        return term_card(w, h, t, [("claude", 0, WHITE, True), ("Fixing login bug...", 0.8, TGREEN, False), ("3 files changed", 1.8, (125, 211, 252), False)], title="Claude Code")
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "photo":
        d.rounded_rectangle([0, 0, w - 1, h - 1], r, fill=(219, 234, 254, 255)); d.ellipse([w * 0.62, h * 0.16, w * 0.62 + h * 0.2, h * 0.16 + h * 0.2], fill=(250, 204, 21, 255))
        d.polygon([(0, h), (w * 0.35, h * 0.45), (w * 0.62, h * 0.75), (w * 0.8, h * 0.58), (w, h)], fill=(59, 130, 246, 255)); return card(w, h, im, r)
    d.rounded_rectangle([0, 0, w - 1, h - 1], int(w * 0.14), fill=(28, 28, 34, 255)); d.rounded_rectangle([8, 8, w - 9, h - 9], int(w * 0.12), fill=(250, 250, 252, 255))
    d.text((w * 0.1, h * 0.05), "Claude", font=font(int(w * 0.09), "bold"), fill=INK + (255,))
    for i, (txt, mine) in enumerate((("Fix login bug", True), ("Done!", False), ("Tests pass", False))):
        q = ease_out(min(1, max(0, (t * speed - 0.4 * i) / 0.3))); f = font(int(w * 0.075), "med"); tw = int(f.getlength(txt)) + 28; x = (w - tw - 22 if mine else 22) + int((1 - q) * 50); y = h * (0.2 + 0.14 * i)
        d.rounded_rectangle([x, y, x + tw, y + w * 0.17], 16, fill=(ACC if mine else (232, 232, 238)) + (int(255 * q),)); d.text((x + 14, y + w * 0.04), txt, font=f, fill=((255, 255, 255) if mine else INK) + (int(255 * q),))
    return im


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


def b_hook(base, t, b):
    icon_string(base, t, 0.05, 540, 150, "term")
    enter(base, clip_card("laptop", t, 760, 520), 500, 640, t, 0.05, side=0, dur=0.4, t_out=T("hook", 12) - 0.1)
    starburst(base, 130, 400, t, 0.3)
    enter(base, term_card(680, 200, t, [("claude remote-control", T("hook", 8) - 0.2, WHITE, True)]), 420, 940, t, T("hook", 8) - 0.5, side=-1)
    dotted(base, 640, 800, 760, 780, t, T("hook", 11))
    enter(base, clip_card("laptop", t + 2, 420, 300), 300, 640, t, T("hook", 12), side=-1)
    enter(base, clip_card("phone", t, 300, 540, 1.0), 880, 820, t, T("hook", 11) - 0.2, side=1)
    starburst(base, 1010, 560, t, T("hook", 11))
    run_text(base, t, "hook", [(0, "Apna *Claude Code* session"), (4, "*phone* se chalana hai?"), (8, "Bas *ek command*"), (12, "Computer ka session, *phone* me")], y=1250)


def b_steps(base, t, b):
    icon_string(base, t, b["t0"] + 0.05, 540, 150, "term")
    lines = [("claude remote-control", T("steps", 3), WHITE, True), ("Remote Control active", T("steps", 7), TGREEN, False), ("claude.ai/code/...  (link)", T("steps", 8), (125, 211, 252), False)]
    enter(base, term_card(900, 300, t, lines), 540, 440, t, b["t0"] + 0.1, side=0, dur=0.4, t_out=T("steps", 14) - 0.2)
    if t >= T("steps", 11) - 0.1:
        press = 8 * math.exp(-(t - T("steps", 11)) * 6)
        enter(base, pill("SPACEBAR", 44, WHITE, INK, pad=(40, 16), r=18), 540, 690 + press, t, T("steps", 11) - 0.1, side=0, dur=0.3, t_out=T("steps", 14) - 0.2)
    if t >= T("steps", 14) - 0.1:
        enter(base, card(430, 430, QR.resize((430, 430)), 30), 540, 1000, t, T("steps", 14) - 0.1, side=0, dur=0.45)
        starburst(base, 800, 800, t, T("steps", 14))
        if t >= T("steps", 19):
            q = ((t - T("steps", 19)) * 0.9) % 1; yy = 800 + 400 * q; ImageDraw.Draw(base).rectangle([335, yy - 4, 745, yy + 4], fill=ACC + (255,))
            enter(base, clip_card("phone", t, 240, 420, 1.2), 900, 1150, t, T("steps", 19) - 0.2, side=1)
    run_text(base, t, "steps", [(0, "Terminal me likho"), (3, "`claude remote-control`"), (8, "Aayega ek *link*"), (11, "*Spacebar* = *QR code*"), (16, "Phone se *scan* karo")], y=1340)


def b_phone(base, t, b):
    icon_string(base, t, b["t0"] + 0.05, 300, 150, "phone")
    pw, ph = 470, 880; im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], 56, fill=(28, 28, 34, 255)); d.rounded_rectangle([14, 14, pw - 15, ph - 15], 44, fill=(250, 250, 252, 255))
    d.text((40, 52), "Claude", font=font(36, "bold"), fill=INK + (255,))
    if t >= T("phone", 8):
        d.rounded_rectangle([34, 120, pw - 34, 210], 20, fill=(235, 241, 255, 255)); d.ellipse([56, 150, 76, 170], fill=GREEN + (255,)); d.text((92, 142), "my-project  online", font=font(28, "bold"), fill=INK + (255,))
    for txt, tt, mine, yy in (("Fix the login bug", T("phone", 13), True, 260), ("Done. 3 files changed", T("phone", 13) + 0.9, False, 360)):
        if t < tt: continue
        q = ease_out(min(1, (t - tt) / 0.3)); f = font(26, "med"); w = int(f.getlength(txt)) + 44
        x = pw - 40 - w + int(60 * (1 - q)) if mine else 40 - int(60 * (1 - q))
        d.rounded_rectangle([x, yy, x + w, yy + 70], 24, fill=(ACC if mine else (232, 232, 238)) + (int(255 * q),)); d.text((x + 22, yy + 17), txt, font=f, fill=(WHITE if mine else INK) + (int(255 * q),))
    enter(base, im, 330, 880, t, b["t0"] + 0.05, side=-1, dur=0.45)
    if t >= T("phone", 15):
        enter(base, clip_card("photo", t, 300, 220), 790, 520, t, T("phone", 15), side=1)
        starburst(base, 930, 410, t, T("phone", 15))
    if t >= T("phone", 17): enter(base, pill("notes.pdf", 36, WHITE, INK, pad=(30, 16), r=22), 790, 700, t, T("phone", 17), side=1)
    if t >= T("phone", 23):
        enter(base, clip_card("laptop", t, 360, 250), 800, 960, t, T("phone", 23) - 0.1, side=1)
        dotted(base, 580, 960, 610, 960, t, T("phone", 23))
        enter(base, pill("Code yahin chalta hai", 30, ACC, pad=(26, 12), r=24), 800, 1120, t, T("phone", 25), side=0)
    run_text(base, t, "phone", [(0, "Claude *app* ya *claude.ai/code* me"), (8, "Dikhega aapka *session*"), (13, "*Message* bhejo"), (15, "*Photo* ya *file* attach karo"), (23, "Code chalta hai *computer* par")], y=1440)


def check_card(title, sub, mark, col):
    im = Image.new("RGBA", (440, 270), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, 439, 269], 28, fill=(255, 255, 255, 255))
    d.ellipse([30, 34, 106, 110], fill=col + (255,))
    if mark == "ok": d.line([(50, 74), (64, 90), (88, 54)], fill=WHITE + (255,), width=9)
    elif mark == "no": d.line([(52, 56), (84, 88)], fill=WHITE + (255,), width=9); d.line([(84, 56), (52, 88)], fill=WHITE + (255,), width=9)
    else: d.arc([48, 52, 88, 92], -60, 240, fill=WHITE + (255,), width=8); d.line([(68, 46), (68, 70)], fill=WHITE + (255,), width=8)
    d.text((30, 140), title, font=font(44, "bold"), fill=INK + (255,)); d.text((30, 200), sub, font=font(30, "med"), fill=GREY + (255,)); return im


def b_note(base, t, b):
    icon_string(base, t, b["t0"] + 0.05, 540, 120, "term")
    enter(base, check_card("Pro / Max plan", "paid plan chahiye", "ok", GREEN), 300, 470, t, T("note", 2), side=-1)
    starburst(base, 500, 340, t, T("note", 2), GREEN)
    enter(base, check_card("API key", "nahi chalegi", "no", RED), 780, 520, t, T("note", 9), side=1)
    enter(base, check_card("Computer ON", "chalu rehna chahiye", "pw", ACC), 300, 790, t, T("note", 14), side=-1)
    if t >= T("note", 18):
        sn = Image.new("RGBA", (440, 270), (0, 0, 0, 0)); d = ImageDraw.Draw(sn); d.rounded_rectangle([0, 0, 439, 269], 10, fill=(255, 244, 168, 255))
        d.text((28, 36), "Laptop sleep?", font=font(40, "bold"), fill=INK + (255,)); d.text((28, 104), "Wapas aate hi", font=font(36, "med"), fill=INK + (255,)); d.text((28, 160), "auto RECONNECT", font=font(40, "bold"), fill=ACC + (255,))
        enter(base, sn, 780, 830, t, T("note", 18), side=1, rot=-3)
    run_text(base, t, "note", [(0, "Dhyan *rakho*"), (2, "*Pro* ya *Max* plan"), (9, "*API key* se nahi"), (14, "*Computer* chalu rakho"), (18, "Sleep ke baad *auto reconnect*")], y=1230)


def b_cta(base, t, b):
    icon_string(base, t, b["t0"] + 0.05, 540, 260, "plus")
    lt = t - T("cta", 7)
    enter(base, pill("Follow", 80, INK, WHITE, pad=(90, 30), r=60), 540, 760, t, b["t0"] + 0.3, side=0, dur=0.4)
    if t >= T("cta", 6):
        q = ease_io(min(1, (t - T("cta", 6)) / 0.5)); cx = 900 - 300 * q; cy = 1000 - 200 * q
        d = ImageDraw.Draw(base); d.polygon([(cx, cy), (cx, cy + 56), (cx + 16, cy + 42), (cx + 30, cy + 70), (cx + 42, cy + 64), (cx + 28, cy + 38), (cx + 48, cy + 36)], fill=WHITE + (255,), outline=INK + (255,))
        if 0 < lt < 0.6:
            r = int(20 + 90 * lt / 0.6); d.ellipse([640 - r, 800 - r, 640 + r, 800 + r], outline=ACC + (int(255 * (1 - lt / 0.6)),), width=6)
    run_text(base, t, "cta", [(0, "Aur *Claude Code* tricks ke liye"), (6, "*Follow* karo")], y=1250)


B = [dict(k="hook", t0=0.0, t1=SC["steps"]), dict(k="steps", t0=SC["steps"], t1=SC["phone"]), dict(k="phone", t0=SC["phone"], t1=SC["note"]),
     dict(k="note", t0=SC["note"], t1=SC["cta"]), dict(k="cta", t0=SC["cta"], t1=TOTAL + 1)]
FN = dict(hook=b_hook, steps=b_steps, phone=b_phone, note=b_note, cta=b_cta)
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
