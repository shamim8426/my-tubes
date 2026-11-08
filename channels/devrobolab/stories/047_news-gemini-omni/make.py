"""047 AI news Short: Gemini Omni 1.2 Flash. Engine/look family of 045 (PIL+OpenCV frames -> photo_video.encode), NEW style variants:
ICE-BLUE background with diagonal stripes + teal glow, accent = TEAL (chips ink-on-teal, key words teal), polaroid photo cards (white border, tilt),
6-frame horizontal slide transitions, tinting photo for the edit demo, robot only in CTA. Official blog crops = small taped notes with a LIVE yellow marker.
Run: python make.py [frames t1 t2 ...]   (needs audio/tts/s_*.wav, wt.json, raw/blocks, raw/photos)"""
import json, math, re, sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import W, H, FPS, ease_out, ease_back, ease_io, wav_dur, encode

LEAD, AFTER, TAIL = 0.10, 0.35, 2.2
FONT = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf")
YEL = (255, 214, 10); INK = (14, 24, 38); TEAL = (0, 196, 170); TEALD = (0, 128, 114); RED = (225, 45, 57); NAVY = (24, 44, 78); WHITE = (255, 255, 255)
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; D[-1] += TAIL; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START))


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]
def PF(sz, bold=False): return ImageFont.truetype(str(ROOT / ("shared/fonts/Poppins-Bold.ttf" if bold else "shared/fonts/Poppins-Medium.ttf")), sz)


def chip(text, size, fill, color=WHITE, pad=(34, 14), r=26, hl=None, hlcolor=TEAL, outline=None):
    f = font(size); words = text.split(" "); sp = f.getlength(" ")
    wl = [f.getlength(w) for w in words]; tw = int(sum(wl) + sp * (len(words) - 1)); asc, desc = f.getmetrics()
    im = Image.new("RGBA", (tw + 2 * pad[0], asc + desc + 2 * pad[1]), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=fill + (255,), outline=(outline + (255,)) if outline else None, width=5); x = pad[0]
    for w, l in zip(words, wl):
        d.text((x, pad[1]), w, font=f, fill=(hlcolor if hl and w.strip(",.?!।") in hl else color) + (255,)); x += l + sp
    return im


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def pop(t, t0, dur=0.28): return ease_back((t - t0) / dur) if t >= t0 else 0.0
def rounded(img, r):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); return o
def shadow(w, h, r=36, off=30, blur=24, a=95):
    sh = Image.new("RGBA", (w + 160, h + 160), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([80, 80 + off, 80 + w, 80 + h + off], r, fill=(0, 0, 0, a)); return sh.filter(ImageFilter.GaussianBlur(blur))


def card_enter(base, spr, cx, cy, t, t0, rot=0.0, side=0, dur=0.34):
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur))
    dx = side * (1 - q) * 520; dy = (1 - q) * (140 if side == 0 else 0); sc = 0.9 + 0.1 * e; w, h = spr.size
    place(base, shadow(w, h), cx + dx, cy + dy, sc, min(1, q * 1.5), rot); place(base, spr, cx + dx, cy + dy, sc, min(1, q * 1.5), rot)


# ---------- NEW look: ice-blue bg, diagonal stripes, teal glow ----------
def bg_ice():
    im = Image.new("RGB", (W, H), (232, 243, 250)); d = ImageDraw.Draw(im)
    for k in range(-H, W + H, 90): d.line([(k, 0), (k + H, H)], fill=(222, 236, 246), width=3)
    g = Image.new("RGB", (W, H), (0, 0, 0)); ImageDraw.Draw(g).ellipse([520, -300, 1500, 700], fill=(120, 232, 214)); g = g.filter(ImageFilter.GaussianBlur(160))
    return ImageChops.screen(im, ImageChops.multiply(g, Image.new("RGB", (W, H), (150, 150, 150)))).convert("RGBA")
BG = bg_ice()
MASC = {k: Image.open(ROOT / f"channels/devrobolab/mascot/cut/{k}.png").convert("RGBA") for k in ("wave", "think", "stop")}
def robot(name, h): m = MASC[name]; return m.resize((int(m.width * h / m.height), h), Image.LANCZOS)

PHOTO = {k: Image.open(HERE / f"raw/photos/{k}.png").convert("RGB") for k in ("hook", "sport", "devices")}
_cov = {}


def polaroid(key, w, h, lt, dur, z0=1.0, z1=1.15, fx=0.5, fy=0.5, tint=None, bt=26, bb=84):
    """photo with slow push-in inside a white polaroid frame (w x h = photo area); tint=(r,g,b,amount)"""
    src = PHOTO[key]; ck = (key, w, h)
    if ck not in _cov:
        s = max(1.5 * w / src.width, 1.5 * h / src.height); _cov[ck] = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    cov = _cov[ck]; p = ease_io(min(1, max(0, lt / dur))); z = z0 + (z1 - z0) * p; ww, wh = w * 1.5 / z, h * 1.5 / z
    cx = min(max(cov.width * fx, ww / 2), cov.width - ww / 2); cy = min(max(cov.height * fy, wh / 2), cov.height - wh / 2)
    im = cov.crop((int(cx - ww / 2), int(cy - wh / 2), int(cx + ww / 2), int(cy + wh / 2))).resize((w, h), Image.BILINEAR)
    if tint:
        a = np.array(im).astype(np.float32); c = np.array(tint[:3], np.float32)
        im = Image.fromarray(np.clip(a * (1 - tint[3]) + (a * c / 255.0) * tint[3] + c * 0.12 * tint[3], 0, 255).astype(np.uint8))
    fr = Image.new("RGBA", (w + 2 * bt, h + bt + bb), (0, 0, 0, 0)); d = ImageDraw.Draw(fr); d.rounded_rectangle([0, 0, fr.width - 1, fr.height - 1], 18, fill=(255, 255, 255, 255), outline=(205, 215, 226, 255), width=3)
    fr.alpha_composite(rounded(im, 8), (bt, bt)); return fr


def tape(im, x, y, rot=-6):
    t = Image.new("RGBA", (130, 44), TEAL + (190,)); im.alpha_composite(t.rotate(rot, expand=True), (x, y))


# ---- small official-page note with LIVE marker ----
BLK = json.load(open(HERE / "raw/blocks.json", encoding="utf-8")); _blk = {}
def note(key, w, hp, maxh=330):
    if key not in _blk: _blk[key] = Image.open(HERE / f"raw/blocks/{key}.png").convert("RGB")
    a0 = _blk[key]; s = (w - 60) / a0.width; a = a0.resize((int(a0.width * s), int(a0.height * s)), Image.LANCZOS); k = 2 * s
    lines = BLK[key]["lines"]
    if lines and hp > 0:
        tot = sum(l[2] for l in lines); done = 0.0; layer = Image.new("RGB", a.size, (255, 255, 255)); d = ImageDraw.Draw(layer)
        for x, y, lw, lh in lines:
            f0 = done / tot; f1 = (done + lw) / tot; done += lw; q = min(1, max(0, (hp - f0) / (f1 - f0)))
            if q > 0: d.rounded_rectangle([x * k - 4, y * k - 2, (x + lw * q) * k + 4, (y + lh) * k + 2], 5, fill=YEL)
        a = ImageChops.multiply(a, layer)
    cy = float(np.mean([l[1] + l[3] / 2 for l in lines])) * k if lines else a.height / 2; h = min(maxh, a.height + 50)
    y0 = int(max(0, min(a.height - (h - 50), cy - (h - 50) * 0.5)))
    pg = a.crop((0, y0, a.width, y0 + h - 50)).convert("RGBA"); sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(sheet)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 14, fill=(255, 254, 250, 255), outline=(200, 212, 224, 255), width=3); sheet.alpha_composite(pg, (30, 30)); tape(sheet, 40, -18, 6); tape(sheet, w - 170, -18, -6)
    return sheet


def src_tag(base, t, t0, y=1290, text="Official page: blog.google"):
    if t >= t0: place(base, chip(text, 30, NAVY, (225, 236, 248), pad=(24, 6), r=16), 540, y)


# ---- captions (single strip, white on ink, key words teal) ----
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
KEY = {"पंद्रह", "तीस", "percent", "15", "30", "seven", "सेंट", "Price", "दाम", "बदल", "मौसम", "Background", "light", "Ultra", "Vids", "API", "Studio", "sports", "physics", "ध्यान", "OMNI", "Follow", "दस", "तीन"}
_cap = {}
def caption(base, t):
    for a, b, txt in CAPS:
        if a - 0.04 <= t < b:
            if txt not in _cap: _cap[txt] = chip(txt, 54, INK, WHITE, pad=(34, 12), r=28, hl=KEY, hlcolor=TEAL)
            place(base, _cap[txt], 540, 1470, 0.94 + 0.06 * ease_out((t - a) / 0.12)); return


def key_chip(txt, size=104, fill=TEAL, color=INK, pad=(40, 4), r=34): return chip(txt, size, fill, color, pad=pad, r=r)
def pc(base, txt, cx, cy, t, t0, size=90, fill=TEAL, color=INK, rot=0, pad=(40, 4)):
    if t >= t0 - 0.02: pp = pop(t, t0); place(base, key_chip(txt, size, fill, color, pad), cx, cy, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)


# ---------------- scenes ----------------
def s_hook(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    card_enter(base, polaroid("hook", 860, 640, lt, 7.5, fx=0.3, fy=0.55), 540, 640, t, b["t0"], rot=-1.8, dur=0.01)
    pc(base, "15 SEC", 330, 1130, t, T("hook", 6) - 0.05, 110, rot=-3)
    pc(base, "-30% PRICE", 700, 1290, t, T("hook", 12) - 0.05, 90, INK, TEAL, rot=2)
    place(base, chip("AI VIDEO NEWS", 52, INK, WHITE, pad=(32, 6), r=24), 540, 250, 1.0)


def s_what(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    pc(base, "GEMINI OMNI 1.2 FLASH", 540, 270, t, T("what", 2) - 0.1, 66, INK, WHITE, pad=(34, 6))
    card = Image.new("RGBA", (940, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle([0, 0, 939, 559], 40, fill=WHITE + (255,), outline=(205, 215, 226, 255), width=4)
    d.text((44, 24), "Clip length", font=PF(46, True), fill=INK + (255,))
    maxw = 840

    def bar(y, lab, frac, col, lbl_col):
        d.rounded_rectangle([50, y, 50 + maxw, y + 96], 24, fill=(236, 241, 247, 255)); w_ = int(maxw * frac)
        if w_ > 30: d.rounded_rectangle([50, y, 50 + w_, y + 96], 24, fill=col + (255,))
        d.text((50, y - 50), lab, font=PF(36, True), fill=lbl_col + (255,))
    t_old, t_new = T("what", 8), T("what", 13)
    if t >= t_old - 0.05: bar(130, "Omni 1.1: 10 s", ease_out((t - t_old) / 0.7) * 10 / 15, (150, 160, 175), (90, 100, 115))
    if t >= t_new - 0.05:
        p = ease_out((t - t_new) / 1.0); bar(330, "Omni 1.2 Flash: 3 to 15 s", p, TEAL, TEALD)
        if p > 0.97: d.text((50, 436), "3 s", font=PF(34, True), fill=INK + (255,)); d.text((50 + maxw - 80, 436), "15 s", font=PF(34, True), fill=INK + (255,))
    card_enter(base, card, 540, 600, t, b["t0"] + 0.2, rot=-0.6)
    hp = (t - T("what", 8)) / max(0.3, T("what", 17) - T("what", 8))
    card_enter(base, note("len", 900, min(1, max(0, hp)), 400), 540, 1110, t, T("what", 6), rot=0.8, side=1)
    src_tag(base, t, T("what", 6), 1345)


def s_price(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    card = Image.new("RGBA", (900, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle([0, 0, 899, 519], 44, fill=INK + (255,)); tape(card, 60, -16, -5)
    d.text((50, 30), "PRICE", font=PF(46, True), fill=(160, 180, 205, 255))
    k = ease_out(min(1, max(0, (t - T("price", 7)) / 0.5))); amt = 0.07 * k if t >= T("price", 7) else 0.0
    d.text((50, 100), f"${amt:.2f}", font=PF(200, True), fill=TEAL + (255,)); d.text((590, 300), "/ second", font=PF(54, True), fill=WHITE + (255,))
    if t >= T("price", 11) - 0.1: d.text((50, 410), "for 720p video", font=PF(54, True), fill=(200, 215, 235, 255))
    card_enter(base, card, 540, 480, t, b["t0"] + 0.1, rot=-0.8, dur=0.01)
    pc(base, "30% CHEAPER", 540, 850, t, T("price", 0) + 0.2, 84, YEL, INK, rot=-2)
    hp = (t - T("price", 4)) / max(0.3, T("price", 14) - T("price", 4))
    card_enter(base, note("price", 780, min(1, max(0, hp)), 460), 540, 1150, t, T("price", 4) - 0.2, rot=0.8, side=1)
    src_tag(base, t, T("price", 4), 1385)


def s_edit(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG); tint = None
    if t >= T("edit", 11): tint = (140, 170, 230, 0.75)
    elif t >= T("edit", 9): tint = (255, 200, 140, 0.65)
    elif t >= T("edit", 8): tint = (150, 235, 200, 0.55)
    card_enter(base, polaroid("hook", 820, 560, lt, 8, z0=1.0, z1=1.1, fx=0.35, tint=tint), 540, 560, t, b["t0"], rot=1.2, dur=0.01)
    for txt, ts, y in (("Background badlo", T("edit", 8), 1000), ("Light badlo", T("edit", 9), 1130), ("Mausam badlo", T("edit", 11), 1260)):
        if t >= ts - 0.02:
            pp = pop(t, ts); place(base, chip(txt, 66, WHITE, INK, pad=(36, 8), r=34, outline=(160, 175, 195)), 600 + (1 - min(1, pp)) * 200, y, 0.8 + 0.2 * min(1, pp), min(1, pp * 1.4))
    pc(base, "EDIT IN CHAT", 330, 880, t, T("edit", 3) - 0.1, 66, INK, WHITE, rot=-3, pad=(30, 6))


def s_where(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    card_enter(base, polaroid("devices", 800, 470, lt, 8), 540, 440, t, b["t0"], rot=-1.2, dur=0.01)
    for i, (txt, ts) in enumerate((("GEMINI API", T("where", 0)), ("AI STUDIO", T("where", 2)), ("GOOGLE VIDS", T("where", 5)))):
        if t >= ts - 0.02:
            pp = pop(t, ts); y = 830 + 118 * i; c = chip(txt, 66, WHITE, INK, pad=(40, 4), r=34, outline=TEAL)
            ic = Image.new("RGBA", (84, 84), (0, 0, 0, 0)); di = ImageDraw.Draw(ic); di.ellipse([2, 2, 82, 82], fill=TEAL + (255,)); di.line([(22, 44), (37, 60), (63, 26)], fill=INK + (255,), width=10)
            row = Image.new("RGBA", (c.width + 110, c.height), (0, 0, 0, 0)); row.alpha_composite(ic, (0, (c.height - 84) // 2)); row.alpha_composite(c, (100, 0))
            place(base, row, 540 - (1 - min(1, pp)) * 300, y, 0.8 + 0.2 * min(1, pp), min(1, pp * 1.4))
    if t >= T("where", 9) - 0.02:
        pp = pop(t, T("where", 9)); c = chip("GEMINI APP", 66, WHITE, INK, pad=(40, 4), r=34, outline=(160, 175, 195)); u = chip("ULTRA ONLY", 56, INK, YEL, pad=(32, 4), r=28)
        place(base, c, 400, 1230, 0.8 + 0.2 * min(1, pp), min(1, pp * 1.4))
        if t >= T("where", 12) - 0.02: place(base, u, 730, 1330, 0.7 + 0.3 * pop(t, T("where", 12)), 1.0, rot=-3)


def s_caution(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    card_enter(base, polaroid("sport", 800, 450, lt, 8, z0=1.0, z1=1.18, fy=0.55), 540, 420, t, b["t0"], rot=1.4, dur=0.01)
    pc(base, "CAUTION", 540, 750, t, b["t0"] + 0.1, 80, YEL, INK, rot=-2)
    pc(base, "FAST SPORTS", 330, 860, t, T("caution", 3) - 0.05, 66, INK, WHITE, rot=-2, pad=(30, 4))
    pc(base, "COMPLEX PHYSICS", 640, 950, t, T("caution", 6) - 0.05, 66, INK, WHITE, rot=2, pad=(30, 4))
    hp = (t - T("caution", 9)) / max(0.3, T("caution", 15) - T("caution", 9))
    card_enter(base, note("limit", 780, min(1, max(0, hp)), 460), 540, 1200, t, T("caution", 9) - 0.2, rot=-0.8, side=-1)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    place(base, robot("wave", 780), 540, 620 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    pc(base, "FOLLOW", 540, 1090, t, T("cta", 3) - 0.1, 84, INK, WHITE, rot=-1.5, pad=(46, 6))
    pc(base, "COMMENT  OMNI", 540, 1250, t, T("cta", 6) - 0.1, 84, TEAL, INK, rot=1.5, pad=(46, 6))


def beats():
    return [dict(k=k, t0=SC[k], t1=(SC[IDS[i + 1]] if i + 1 < len(IDS) else TOTAL + 1)) for i, k in enumerate(IDS)]
B = beats(); FN = dict(hook=s_hook, what=s_what, price=s_price, edit=s_edit, where=s_where, caution=s_caution, cta=s_cta)
SR = 24000; TR = 0.2


def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def render_beat(t, bi):
    b = B[bi]; base = Image.new("RGBA", (W, H)); FN[b["k"]](base, t, b); return base


def frame(t):
    bi = next((i for i, x in enumerate(B) if x["t0"] <= t < x["t1"]), len(B) - 1)
    if bi > 0 and t - B[bi]["t0"] < TR:  # 6-frame horizontal slide
        q = ease_io((t - B[bi]["t0"]) / TR); old = render_beat(B[bi]["t0"] - 1e-3, bi - 1); new = render_beat(t, bi)
        base = Image.new("RGBA", (W, H)); base.alpha_composite(old, (-int(q * W), 0)); base.alpha_composite(new, (int((1 - q) * W), 0))
    else: base = render_beat(t, bi)
    caption(base, t); return np.array(base.convert("RGB"))


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['k'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/d_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice_047.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_047.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
