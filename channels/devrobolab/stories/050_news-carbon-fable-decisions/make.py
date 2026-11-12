"""048 AI news Short: Phonon TTS (Hugging Face / Gradium). Engine of 047; NEW variants: LAVENDER dotted bg + violet glow, accent=VIOLET; ORIGINAL 047 docstring: Engine/look family of 045 (PIL+OpenCV frames -> photo_video.encode), NEW style variants:
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

LEAD, AFTER, TAIL = 0.05, 0.10, 0.6
FONT = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf")
YEL = (255, 214, 10); INK = (14, 24, 38); TEAL = (176, 140, 255); TEALD = (110, 70, 210); RED = (225, 45, 57); NAVY = (24, 44, 78); WHITE = (255, 255, 255)
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
    im = Image.new("RGB", (W, H), (241, 236, 252)); d = ImageDraw.Draw(im)
    for yy in range(30, H, 70):
        for xx in range(30 + (35 if (yy // 70) % 2 else 0), W, 70): d.ellipse([xx - 4, yy - 4, xx + 4, yy + 4], fill=(222, 212, 245))
    g = Image.new("RGB", (W, H), (0, 0, 0)); ImageDraw.Draw(g).ellipse([520, -300, 1500, 700], fill=(200, 175, 255)); g = g.filter(ImageFilter.GaussianBlur(160))
    return ImageChops.screen(im, ImageChops.multiply(g, Image.new("RGB", (W, H), (150, 150, 150)))).convert("RGBA")
BG = bg_ice()
MASC = {k: Image.open(ROOT / f"channels/devrobolab/mascot/cut/{k}.png").convert("RGBA") for k in ("wave", "think", "stop")}
def robot(name, h): m = MASC[name]; return m.resize((int(m.width * h / m.height), h), Image.LANCZOS)

PHOTO = {k: Image.open(HERE / f"raw/photos/{k}.png").convert("RGB") for k in ("hook", "globe", "mic")}
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


def src_tag(base, t, t0, y=1290, text="Source: huggingface.co/blog/phonon-tts"):
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
KEY = {"पैंसठ", "पचहत्तर", "MB", "MB।", "सौ", "दो", "लाख", "Hindi", "free", "commercial", "ध्यान", "PHONON", "Follow", "internet", "device", "download", "इकतीस", "voices", "Phonon", "Phonon।"}
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
    card_enter(base, polaroid("hook", 860, 640, lt, 7.5, fx=0.5, fy=0.55), 540, 640, t, b["t0"], rot=-1.8, dur=0.01)
    pc(base, "ONLY 65 MB", 340, 1130, t, T("hook", 1) - 0.05, 104, rot=-3)
    pc(base, "NO INTERNET", 690, 1290, t, T("hook", 9) - 0.05, 84, INK, TEAL, rot=2)
    place(base, chip("AI VOICE NEWS", 52, INK, WHITE, pad=(32, 6), r=24), 540, 250, 1.0)


def s_what(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    pc(base, "PHONON", 540, 250, t, T("what", 2) - 0.1, 90, INK, WHITE, pad=(40, 6))
    card_enter(base, polaroid("mic", 800, 440, lt, 8, z0=1.0, z1=1.12), 540, 640, t, b["t0"] + 0.1, rot=-1.2, dur=0.01)
    pc(base, "TEXT TO SPEECH", 340, 960, t, T("what", 6) - 0.1, 62, TEAL, INK, rot=-2, pad=(30, 4))
    pc(base, "BY GRADIUM", 720, 1040, t, T("what", 9) - 0.05, 62, INK, WHITE, rot=2, pad=(30, 4))
    hp = (t - T("what", 15)) / max(0.3, T("what", 20) - T("what", 15))
    card_enter(base, note("device", 900, min(1, max(0, hp)), 300), 540, 1245, t, T("what", 14) - 0.2, rot=0.8, side=1)
    src_tag(base, t, T("what", 14), 1412)


def s_size(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    card = Image.new("RGBA", (900, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle([0, 0, 899, 469], 44, fill=INK + (255,)); tape(card, 60, -16, -5)
    d.text((50, 30), "MODEL SIZE", font=PF(44, True), fill=(180, 170, 215, 255))
    if t >= T("size", 2): d.text((50, 110), "65 - 75", font=PF(165, True), fill=TEAL + (255,)); d.text((660, 262), "MB", font=PF(84, True), fill=WHITE + (255,))
    if t >= T("size", 5): d.text((50, 370), "small enough for a phone", font=PF(46, True), fill=(205, 200, 235, 255))
    card_enter(base, card, 540, 450, t, b["t0"] + 0.1, rot=-0.8, dur=0.01)
    pc(base, "100+ VOICES", 340, 800, t, T("size", 6) - 0.05, 84, YEL, INK, rot=-2)
    pc(base, "MAKE YOUR OWN", 690, 930, t, T("size", 13) - 0.05, 66, INK, WHITE, rot=2, pad=(30, 4))
    sw = T("size", 6)
    if t < sw:
        hp = (t - T("size", 1)) / max(0.3, T("size", 5) - T("size", 1))
        card_enter(base, note("size", 800, min(1, max(0, hp)), 320), 540, 1190, t, T("size", 1) - 0.2, rot=0.8, side=1)
    else:
        hp = (t - sw) / max(0.3, T("size", 11) - sw)
        card_enter(base, note("voices", 800, min(1, max(0, hp)), 320), 540, 1190, t, sw - 0.1, rot=-0.8, side=-1, dur=0.2)
    src_tag(base, t, T("size", 1), 1385)


def s_langs(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    card_enter(base, polaroid("globe", 800, 400, lt, 8, z0=1.0, z1=1.12), 540, 380, t, b["t0"], rot=1.2, dur=0.01)
    items = (("ENGLISH", T("langs", 0), 330, 780), ("FRENCH", T("langs", 1), 740, 780), ("GERMAN", T("langs", 2), 330, 890),
             ("SPANISH", T("langs", 3) + 0.15, 740, 890), ("PORTUGUESE", T("langs", 5), 540, 1000))
    for txt, ts, x, y in items:
        if t >= ts - 0.02:
            pp = pop(t, ts); place(base, chip(txt, 56, WHITE, INK, pad=(32, 4), r=30, outline=TEAL), x, y, 0.8 + 0.2 * min(1, pp), min(1, pp * 1.4), rot=0)
    pc(base, "200,000+ DOWNLOADS", 540, 1130, t, T("langs", 12) - 0.05, 66, INK, TEAL, rot=-1.5, pad=(34, 4))
    hp = (t - T("langs", 12)) / max(0.3, T("langs", 17) - T("langs", 12))
    card_enter(base, note("dl", 780, min(1, max(0, hp)), 140), 540, 1290, t, T("langs", 11) - 0.2, rot=0.8, side=1)


def s_caution(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    pc(base, "CAUTION", 540, 280, t, b["t0"] + 0.1, 100, YEL, INK, rot=-2)
    pc(base, "HINDI: NOT LISTED", 540, 440, t, T("caution", 2) - 0.1, 76, RED, WHITE, rot=1.5, pad=(36, 6))
    pc(base, "ONLY 31m EN = FREE FOR BUSINESS", 540, 590, t, T("caution", 14) - 0.1, 50, INK, WHITE, rot=-1, pad=(30, 6))
    pc(base, "OTHERS = NON-COMMERCIAL", 540, 700, t, T("caution", 14) + 1.0, 54, INK, TEAL, rot=1, pad=(30, 6))
    hp = (t - T("caution", 14)) / max(0.3, T("caution", 22) - T("caution", 14))
    card_enter(base, note("lic", 880, min(1, max(0, hp)), 520), 540, 1090, t, T("caution", 3) - 0.2, rot=-0.8, side=-1)
    src_tag(base, t, T("caution", 3), 1385)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BG)
    place(base, robot("wave", 780), 540, 620 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    pc(base, "FOLLOW", 540, 1090, t, T("cta", 4) - 0.1, 84, INK, WHITE, rot=-1.5, pad=(46, 6))
    pc(base, "COMMENT  PHONON", 540, 1250, t, T("cta", 8) - 0.1, 84, TEAL, INK, rot=1.5, pad=(46, 6))


def beats():
    return [dict(k=k, t0=SC[k], t1=(SC[IDS[i + 1]] if i + 1 < len(IDS) else TOTAL + 1)) for i, k in enumerate(IDS)]
B = beats(); FN = dict(hook=s_hook, what=s_what, size=s_size, langs=s_langs, caution=s_caution, cta=s_cta)
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
    build_audio(HERE / "audio/voice_048.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_048.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
