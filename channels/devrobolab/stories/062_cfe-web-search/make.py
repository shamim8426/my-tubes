"""062 How-to Short: Claude me web search kaise on karein. Lilac grid paper, accent MAGENTA, own Playwright captures of the official pages, drawn chat UI (illustration).
Run: python make.py frames t1 t2 ...  |  python make.py (render)"""
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
ACC = (214, 36, 120); ACCL = (251, 182, 214); INKD = (30, 30, 36); GREEN = (22, 163, 74); RED = (225, 45, 57)


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(str(ROOT / "shared/fonts/Poppins-Bold.ttf"), sz)
    return _fc[sz]


def chip(text, size, fill, color=(255, 255, 255), pad=(34, 14), r=26, hl=None, hlcolor=ACCL):
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


def card_enter(base, spr, cx, cy, t, t0, rot=0.0, side=0, dur=0.38, shad=True):
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur))
    dx = side * (1 - q) * 520; dy = (1 - q) * (140 if side == 0 else 0); sc = 0.9 + 0.1 * e; w, h = spr.size
    if shad: place(base, shadow(w, h), cx + dx, cy + dy, sc, min(1, q * 1.5), rot)
    place(base, spr, cx + dx, cy + dy, sc, min(1, q * 1.5), rot)


MASC = Image.open(ROOT / "channels/devrobolab/mascot/cut/wave.png").convert("RGBA")
def robot(h): return MASC.resize((int(MASC.width * h / MASC.height), h), Image.LANCZOS)


def bg_paper():
    im = Image.new("RGB", (W, H), (247, 245, 252)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(247 - 6 * k), int(245 - 8 * k), 252))
    d.ellipse([200, 300, 1300, 1300], fill=(252, 215, 234)); im = im.filter(ImageFilter.GaussianBlur(150)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(234, 230, 245), width=1)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(234, 230, 245), width=1)
    return im.convert("RGBA")
BGP = bg_paper()


def with_border(img, r=18, bw=5):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=bw); return o


def crop_w(name, box, w):
    c = Image.open(HERE / f"raw/{name}.png").convert("RGB").crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)


STEPS = with_border(crop_w("m_ws_check", (20, 790, 1060, 1415), 940))
CITE = with_border(crop_w("m_ws_cite", (25, 850, 1065, 1265), 940))
CAP = with_border(crop_w("m_ws_plus", (25, 630, 1065, 940), 960))
NEWX = with_border(crop_w("m_ws_newexp", (30, 1085, 1050, 1375), 960))
TIP = with_border(crop_w("m_ws_tip", (25, 855, 1075, 1510), 900))
LIM = with_border(crop_w("m_ws_limits", (25, 880, 1065, 1285), 960))
SRC1 = "Official: support.claude.com / Enable and use web search"


def srcline(base, txt=SRC1, y=1425):
    place(base, chip(txt, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, y)


def banner(base, t, txt, ts, y=200, fill=ACC):
    if t >= ts:
        pp = pop(t, ts + 0.03); place(base, chip(txt, 46, fill, (255, 255, 255), pad=(30, 9), r=26), 540, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def pc(base, txt, size, fill, color, cx, cy, t, ts, rot=0, pad=(36, 10), r=26, hl=None):
    if t >= ts - 0.02:
        pp = pop(t, ts); place(base, chip(txt, size, fill, color, pad=pad, r=r, hl=hl), cx, cy, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)


def globe(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5); d.ellipse([cx - r * .45, cy - r, cx + r * .45, cy + r], outline=col, width=4)
    d.line([(cx - r, cy), (cx + r, cy)], fill=col, width=4)


def cursor(d, x, y, s=1.0):
    pts = [(x, y), (x, y + 62 * s), (x + 17 * s, y + 46 * s), (x + 30 * s, y + 74 * s), (x + 42 * s, y + 68 * s), (x + 29 * s, y + 41 * s), (x + 50 * s, y + 41 * s)]
    d.polygon(pts, fill=(255, 255, 255, 255)); d.line(pts + [pts[0]], fill=INKD + (255,), width=4)


def chatui(t, t_plus, t_menu, t_pick, t_tick, t_off=None):
    """Drawn chat box (illustration): + button lower-left, menu with a 'Web search' row, checkmark when on."""
    w, h = 940, 600; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    by = 380; d.rounded_rectangle([0, by, w - 1, h - 1], 36, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    d.text((40, by + 40), "Claude se kuch bhi poochho...", font=font(36), fill=(150, 150, 160, 255))
    px, py = 40, by + 120; hot = t >= t_plus
    d.ellipse([px, py, px + 76, py + 76], fill=(ACC if hot else (240, 240, 244)) + (255,), outline=INKD + (255,), width=4)
    d.text((px + 20, py + 2), "+", font=font(56), fill=((255, 255, 255) if hot else INKD) + (255,))
    on = t >= t_tick and (t_off is None or t < t_off)
    if on:
        globe(d, 170, py + 38, 24, ACC + (255,)); d.text((208, py + 16), "Web search", font=font(32), fill=ACC + (255,))
    if t >= t_menu and (t_off is None or t < t_off):
        q = ease_out(min(1, (t - t_menu) / 0.25)); mh = int(330 * q)
        if mh > 20:
            m = Image.new("RGBA", (600, 330), (0, 0, 0, 0)); md = ImageDraw.Draw(m)
            md.rounded_rectangle([0, 0, 599, 329], 26, fill=(255, 255, 255, 255), outline=INKD + (255,), width=4)
            md.rounded_rectangle([30, 34, 330, 64], 12, fill=(226, 226, 232, 255))
            ry = 112; sel = t >= t_pick
            if sel: md.rounded_rectangle([14, ry - 10, 585, ry + 90], 18, fill=ACCL + (255,))
            globe(md, 70, ry + 40, 28, INKD + (255,)); md.text((120, ry + 14), "Web search", font=font(44), fill=INKD + (255,))
            if on:
                md.line([(480, ry + 40), (505, ry + 66), (555, ry + 10)], fill=GREEN + (255,), width=12)
            md.rounded_rectangle([30, 262, 290, 292], 12, fill=(226, 226, 232, 255))
            im.alpha_composite(m.crop((0, 330 - mh, 600, 330)), (20, by - 20 - mh))
    if t >= t_plus - 0.5:
        if t < t_pick - 0.1: cx, cy = px + 50, py + 46
        else: cx, cy = 420, by - 20 - 330 + 160
        cursor(d, cx, cy)
    d.rounded_rectangle([w - 230, by + 140, w - 30, by + 186], 14, fill=(240, 240, 244, 255)); d.text((w - 215, by + 147), "illustration", font=font(26), fill=(120, 120, 130, 255))
    return im


def answer_card(t, t0, t_cite):
    w, h = 940, 420; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    d.text((36, 26), "Claude", font=font(36), fill=ACC + (255,)); globe(d, w - 70, 50, 22, ACC + (255,))
    for i, ln in enumerate((640, 760, 560, 700)):
        y = 100 + i * 66; d.rounded_rectangle([36, y, 36 + ln, y + 30], 12, fill=(222, 222, 230, 255))
        if t >= t_cite + 0.25 * i:
            x = 36 + ln + 18; d.rounded_rectangle([x, y - 6, x + 64, y + 38], 12, fill=ACC + (255,)); d.text((x + 18, y - 4), str(i + 1), font=font(34), fill=(255, 255, 255, 255))
    d.text((36, 366), "illustration", font=font(24), fill=(140, 140, 150, 255))
    return im


def question(t, t0, t_hl):
    txt1, txt2 = "Aaj ki sabse badi AI news kya hai?", "search the web"
    w, h = 940, 210; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=(30, 30, 36, 255))
    n = int(len(txt1) * min(1, max(0, (t - t0) / 1.0))); d.text((40, 34), txt1[:n], font=font(42), fill=(255, 255, 255, 255))
    if t >= t_hl:
        f = font(42); tw = int(f.getlength(txt2)); d.rounded_rectangle([34, 112, 34 + tw + 24, 172], 14, fill=(255, 214, 10, 255)); d.text((46, 114), txt2, font=f, fill=INKD + (255,))
    return im


def meter(t, t_ws):
    w, h = 900, 230; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    d.text((36, 24), "Usage limit (free plan)", font=font(38), fill=INKD + (255,))
    bx, by, bw, bh = 36, 100, w - 72, 70; d.rounded_rectangle([bx, by, bx + bw, by + bh], 35, fill=(232, 232, 238, 255))
    base_f = 0.35; ws = 0.35 * ease_io(min(1, max(0, (t - t_ws) / 0.8)))
    d.rounded_rectangle([bx, by, bx + int(bw * (base_f + ws)), by + bh], 35, fill=ACC + (255,))
    d.rounded_rectangle([bx, by, bx + int(bw * base_f), by + bh], 35, fill=(120, 120, 132, 255))
    d.text((bx + 24, by + 12), "chat", font=font(36), fill=(255, 255, 255, 255))
    if ws > 0.15: d.text((bx + int(bw * base_f) + 24, by + 12), "+ web search", font=font(36), fill=(255, 255, 255, 255))
    d.text((w - 210, 186), "illustration", font=font(24), fill=(140, 140, 150, 255))
    return im


# ---- captions ----
CAPTXT = {
    "hook": [(0, "Claude se TAAZA jaankari?"), (7, "2 CLICKS me WEB SEARCH on"), (14, "Jawab ke saath SOURCE links")],
    "steps": [(0, "1. Neeche BAAYEIN kone me PLUS"), (11, "2. List me WEB SEARCH click"), (19, "TICK dikha = search ON"), (28, "Band? Dobara CLICK karo")],
    "use": [(0, "Ab TAAZA sawaal poochho"), (11, "Pakka? Likho SEARCH THE WEB"), (22, "Jawab me CITATIONS"), (26, "Har baat ka SOURCE link"), (34, "Khud JAANCH lo")],
    "note": [(0, "Dhyan rakho!"), (2, "TEAM plan: pehle OWNER on kare"), (18, "FREE plan: USAGE LIMIT me ginta"), (30, "Option nahi dikha?"), (39, "Naye Claude me KHUD search")],
    "cta": [(0, "Agla tip: EXTENDED THINKING"), (6, "Aise tips ke liye FOLLOW kijiye")],
}
CAPS = []
for sid in IDS:
    items = CAPTXT[sid]; end = SC[sid] + D[IDS.index(sid)]
    for j, (k, txt) in enumerate(items): CAPS.append((T(sid, k) - 0.04 if k else SC[sid], (T(sid, items[j + 1][0]) - 0.04) if j + 1 < len(items) else end, txt))
_capc = {}
def caption(base, t):
    for a, b, txt in CAPS:
        if a <= t < b:
            if txt not in _capc:
                c = chip(txt, 50, (28, 28, 34), (255, 255, 255), pad=(32, 12), r=28, hl={w.strip(",.?!:") for w in txt.split() if w.isupper() and len(w) > 2})
                if c.width > 1010: c = c.resize((1010, int(c.height * 1010 / c.width)), Image.LANCZOS)
                _capc[txt] = c
            place(base, _capc[txt], 540, 1560, 0.94 + 0.06 * ease_out((t - a) / 0.12)); return


# ---- scenes ----
def s_hook(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "WEB SEARCH ON", 92, ACC, (255, 255, 255), 540, 210, t, -1.0, -1.5, pad=(50, 12), r=36)
    card_enter(base, chatui(t, 0.0, -1.0, 0.0, 0.0), 540, 640, t, -1.0, side=0, dur=0.25, shad=False)
    pc(base, "2 CLICKS", 80, INKD, (255, 255, 255), 280, 1010, t, T("hook", 7), -2, pad=(44, 12), r=32)
    if t >= T("hook", 10): card_enter(base, answer_card(t, T("hook", 10), T("hook", 18)).resize((620, 277), Image.LANCZOS), 660, 1255, t, T("hook", 10), side=1)
    pc(base, "+ SOURCE LINKS", 52, GREEN, (255, 255, 255), 690, 1060, t, T("hook", 18), 1.5, pad=(30, 10), r=26)
    srcline(base, y=1440)


def s_steps(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, "KAISE ON KAREIN", b["t0"] + 0.05, 140)
    card_enter(base, STEPS, 540, 485, t, b["t0"] + 0.1, rot=-0.5, side=1)
    card_enter(base, chatui(t, T("steps", 8), T("steps", 12), T("steps", 14), T("steps", 21), T("steps", 32)), 540, 1135, t, b["t0"] + 0.25, side=-1, shad=False)
    for txt, k, x, fill in (("1  PLUS", 8, 180, INKD), ("2  WEB SEARCH", 14, 520, INKD), ("3  TICK = ON", 21, 880, GREEN)):
        pc(base, txt, 40, fill, (255, 255, 255), x, 812, t, T("steps", k), 0, pad=(22, 9), r=22)
    if t >= T("steps", 32): pc(base, "OFF: CLICK AGAIN", 60, RED, (255, 255, 255), 540, 1020, t, T("steps", 32), -1, pad=(34, 10), r=26)


def s_use(base, t, b):
    base.alpha_composite(BGP)
    t_c = T("use", 22)
    if t < t_c:
        card_enter(base, TIP, 540, 440, t, b["t0"] + 0.1, rot=0.5, side=1)
        card_enter(base, question(t, b["t0"] + 0.2, T("use", 19)), 540, 990, t, b["t0"] + 0.15, side=-1)
        pc(base, "PAKKA SEARCH KE LIYE", 58, ACC, (255, 255, 255), 540, 1230, t, T("use", 11), -1, pad=(34, 10), r=26)
    else:
        card_enter(base, CITE, 540, 345, t, t_c, rot=-0.5, side=1)
        card_enter(base, answer_card(t, t_c, T("use", 24)), 540, 790, t, t_c + 0.05, side=-1)
        pc(base, "CITATION = SOURCE LINK", 56, ACC, (255, 255, 255), 540, 1105, t, T("use", 26), 1, pad=(34, 10), r=26)
        pc(base, "KHUD JAANCHO", 64, GREEN, (255, 255, 255), 540, 1260, t, T("use", 36), -1.5, pad=(40, 10), r=28)
    srcline(base, y=1425)


def s_note(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "DHYAN RAKHO", 72, RED, (255, 255, 255), 540, 200, t, b["t0"] + 0.05, -1.5, pad=(44, 12), r=32)
    t2, t3 = T("note", 18), T("note", 30)
    if t < t2:
        card_enter(base, CAP, 540, 500, t, b["t0"] + 0.1, rot=0.5, side=1)
        pc(base, "TEAM / ENTERPRISE", 58, INKD, (255, 255, 255), 540, 760, t, T("note", 2), 1, pad=(36, 10), r=26)
        pc(base, "PEHLE OWNER ON KARE", 54, ACC, (255, 255, 255), 540, 880, t, T("note", 7), -1, pad=(32, 10), r=26)
        if t < T("note", 10) - 0.05 and t >= T("note", 2):
            pp = pop(t, T("note", 2)); place(base, chip("Owner  >  sab members", 46, (255, 255, 255), INKD, pad=(30, 12), r=22), 540, 1110, 0.6 + 0.4 * pp, min(1, pp * 1.4))
        for n, (txt, k) in enumerate((("Organization settings", 10), ("Capabilities", 11), ("Web search  ON", 14))):
            pc(base, txt, 46, (255, 255, 255), INKD if n < 2 else GREEN, 540, 1030 + 125 * n, t, T("note", k), 0, pad=(30, 10), r=22)
            if n and t >= T("note", k) - 0.02: place(base, chip("v", 34, INKD, (255, 255, 255), pad=(12, 0), r=12), 540, 1030 + 125 * n - 64)
    elif t < t3:
        card_enter(base, LIM, 540, 470, t, t2 - 0.05, rot=-0.5, side=-1)
        pc(base, "FREE PLAN", 70, INKD, (255, 255, 255), 540, 760, t, t2, -1, pad=(40, 10), r=28)
        pc(base, "USAGE LIMIT ME GINTA", 58, ACC, (255, 255, 255), 540, 900, t, T("note", 24), 1, pad=(36, 10), r=26)
        if t >= t2 + 0.2: card_enter(base, meter(t, T("note", 21)), 540, 1170, t, t2 + 0.2, side=1)
    else:
        card_enter(base, NEWX, 540, 470, t, t3 - 0.05, rot=0.5, side=1)
        pc(base, "TOGGLE NAHI DIKHA?", 60, INKD, (255, 255, 255), 540, 720, t, T("note", 35), 1, pad=(36, 10), r=26)
        pc(base, "CLAUDE KHUD SEARCH", 64, GREEN, (255, 255, 255), 540, 860, t, T("note", 42), -1.5, pad=(40, 10), r=28)
        if t >= t3 + 0.2:
            g = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse([10, 10, 290, 290], fill=(255, 255, 255, 255), outline=INKD + (255,), width=6)
            globe(gd, 150, 150, 95, ACC + (255,)); pp = pop(t, t3 + 0.2)
            place(base, g, 540, 1170 + 8 * math.sin((t - t3) * 3), 0.6 + 0.4 * pp, min(1, pp * 1.4), 6 * math.sin((t - t3) * 2))
    srcline(base, y=1425)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    pc(base, "AGLA TIP: EXTENDED THINKING", 50, INKD, (255, 255, 255), 540, 230, t, b["t0"] + 0.05, -1, pad=(36, 12), r=28)
    place(base, robot(700), 540, 700 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill, sz) in enumerate((("+ FOLLOW", T("cta", 12), ACC, 80), ("AUR AASAAN CLAUDE TIPS", T("cta", 6), INKD, 46))):
        pp = pop(t, ts); place(base, chip(txt, sz, fill, (255, 255, 255), pad=(44, 10), r=30), 540, 1180 + 140 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=SC["steps"]), dict(k="steps", t0=SC["steps"], t1=SC["use"]), dict(k="use", t0=SC["use"], t1=SC["note"]),
     dict(k="note", t0=SC["note"], t1=SC["cta"]), dict(k="cta", t0=SC["cta"], t1=TOTAL + 1)]
FN = dict(hook=s_hook, steps=s_steps, use=s_use, note=s_note, cta=s_cta)
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
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/frames/d_{tt:05.1f}.png")
        return
    if len(sys.argv) > 1 and sys.argv[1] == "range":
        import subprocess
        n0, n1 = int(round(float(sys.argv[2]) * FPS)), int(round(float(sys.argv[3]) * FPS))
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                              "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", sys.argv[4]], stdin=subprocess.PIPE)
        for i in range(n0, n1): p.stdin.write(frame(i / FPS).tobytes())
        p.stdin.close(); p.wait(); print("range", n0, n1, sys.argv[4]); return
    build_audio(HERE / "audio/voice.wav")
    n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / deck["music"]["file"], HERE / "output/short.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()




