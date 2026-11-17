"""Claude Roz Ke Kaam (Claude for everyone) LONG: 'Claude usage limit jaldi khatam? 7 tareeke' 16:9 1920x1080.
Copied from stories/044_cfe-memory/make_final.py (same look: dark neon, chapter badge, Chromium Hindi captions, cursor demos, every action at its
spoken word via T(scene, token)). New highlight colour: LIME. Official-page crops are our own Playwright captures (raw/capture.py) with the key
phrase marked yellow. Run: python make_final.py [frames t1 t2 ... | range t0 t1 out.mp4]"""
import hashlib, json, math, re, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import ease_out, ease_back, ease_io, wav_dur
import subprocess

W, H, FPS = 1920, 1080, 30
LEAD, AFTER = 0.15, 0.45
ACC = (170, 236, 90); WHITE = (255, 255, 255); RED = (255, 96, 106); AMB = (255, 190, 80); DIM = (150, 160, 182); BLUE = (110, 180, 255)
BG0 = (7, 9, 15); CARD = (19, 23, 33); OUT = (58, 68, 94); INK = (10, 12, 18); SOFT = (32, 44, 30)
FMUK = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf"); FPOP = str(ROOT / "shared/fonts/Poppins-Medium.ttf"); FPOPB = str(ROOT / "shared/fonts/Poppins-Bold.ttf")
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; D[-1] += 3.0; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START)); DUR = dict(zip(IDS, D))


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]
def S(scene, off): return SC[scene] + off
def E(scene): return SC[scene] + DUR[scene]
def I(scene, sub, nth=1, after=0):
    """index of the nth token (from index `after`) that contains `sub`"""
    c = 0
    for k, (tk, _) in enumerate(WT[scene]["tokens"]):
        if k >= after and sub in tk:
            c += 1
            if c == nth: return k
    raise KeyError(f"{scene}: '{sub}' #{nth} not found")
def A(scene, sub, nth=1, after=0): return T(scene, I(scene, sub, nth, after))


K = 1.0
CX0, CY0 = 960, 540
_f = {}
def F(sz, kind="m"):
    k = (int(round(sz * K)), kind)
    if k not in _f: _f[k] = ImageFont.truetype({"m": FMUK, "p": FPOP, "b": FPOPB}[kind], k[0])
    return _f[k]


class SD:
    def __init__(self, img): self.d = ImageDraw.Draw(img)
    def text(self, xy, s, font=None, fill=None, anchor=None): self.d.text(xy, s, font=font, fill=fill, anchor=anchor)
    def rounded_rectangle(self, box, radius=0, fill=None, outline=None, width=1): self.d.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)
    def rectangle(self, box, fill=None, outline=None, width=1): self.d.rectangle(box, fill=fill, outline=outline, width=width)
    def ellipse(self, box, fill=None, outline=None, width=1): self.d.ellipse(box, fill=fill, outline=outline, width=width)
    def arc(self, box, a0, a1, fill=None, width=1): self.d.arc(box, a0, a1, fill=fill, width=width)
    def line(self, pts, fill=None, width=1): self.d.line(pts, fill=fill, width=width)
    def polygon(self, pts, fill=None, outline=None): self.d.polygon(pts, fill=fill, outline=outline)


def NI(w, h): return Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def pop(t, t0, dur=0.28): return ease_back((t - t0) / dur) if t >= t0 else 0.0
def fade(t, t0, dur=0.25): return min(1.0, max(0.0, (t - t0) / dur))


def pill(text, size=34, fill=(20, 24, 34), color=WHITE, pad=(24, 9), r=None, hl=(), hlc=ACC, outline=None, kind="m", glow=False):
    f = F(size, kind); words = text.split(" "); sp = f.getlength(" "); wl = [f.getlength(w) for w in words]; tw = int(sum(wl) + sp * (len(words) - 1)); a, d_ = f.getmetrics()
    px_, py_ = pad; w_, h_ = tw + 2 * px_, a + d_ + 2 * py_; r = r or h_ // 2; m = 12
    im = Image.new("RGBA", (w_ + 2 * m, h_ + 2 * m), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle([m, m, w_ + m - 1, h_ + m - 1], r, outline=ACC + (255,), width=4); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(7)))
    d.rounded_rectangle([m, m, w_ + m - 1, h_ + m - 1], r, fill=fill + (255,), outline=(outline + (255,)) if outline else None, width=3)
    x = m + px_
    for w, l in zip(words, wl):
        d.text((x, m + py_), w, font=f, fill=(hlc if w.strip(",.?!:") in hl else color) + (255,)); x += l + sp
    return im


def card(w, h, r=30, fill=CARD, outline=OUT, ow=3, glow=False, gc=None):
    m = 20; im = Image.new("RGBA", (int(w) + 2 * m, int(h) + 2 * m), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle([m, m, w + m - 1, h + m - 1], r, outline=(gc or ACC) + (255,), width=5); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(im).rounded_rectangle([m, m, w + m - 1, h + m - 1], r, fill=fill + (255,), outline=outline + (255,), width=ow); return im


def enter(base, spr, cx, cy, t, t0, side=0, dur=0.32, rot=0):
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur)); dx = side * (1 - q) * 360; dy = (1 - q) * (80 if side == 0 else 0)
    place(base, spr, cx + dx, cy + dy, 0.94 + 0.06 * e, min(1, q * 1.5), rot)


def txt(base, xy, s, size, fill=WHITE, kind="m", anchor="la", alpha=1.0):
    SD(base).text(xy, s, font=F(size, kind), fill=fill + (int(255 * alpha),), anchor=anchor)


def typed(s, t, a0, a1): n = int(len(s) * min(1, max(0, (t - a0) / max(0.1, a1 - a0)))); return s[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(s) else "")


# ---------- background / badge / caption ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None, None]; x = np.linspace(-1, 1, W)[None, :, None]
    base = np.array(BG0, dtype=np.float32)[None, None, :] + 14 * (1 - y) * np.exp(-x ** 2 * 1.5)
    im = Image.fromarray(np.broadcast_to(np.clip(base, 0, 255).astype(np.uint8), (H, W, 3)).copy()).convert("RGBA"); d = ImageDraw.Draw(im)
    for gx in range(0, W, 96): d.line([(gx, 0), (gx, H)], fill=(14, 18, 27, 255), width=1)
    for gy in range(0, H, 96): d.line([(0, gy), (W, gy)], fill=(14, 18, 27, 255), width=1)
    return im
BG = make_bg()
CHAP = {"hook": None, "how": (1, "how limits work"), "eats": (2, "what uses more"), "batch": (3, "plan + one message"), "clear": (4, "clear prompt"),
        "projects": (5, "projects cache"), "settings": (6, "effort + tools"), "newchat": (7, "long chats"), "limit": (8, "limit hit?"), "cta": (9, "recap")}


def badge(base, sid, t):
    c = CHAP[sid]
    if not c: return
    sq = Image.new("RGBA", (54, 54), (0, 0, 0, 0)); d = ImageDraw.Draw(sq); d.rounded_rectangle([0, 0, 53, 53], 12, fill=ACC + (255,)); d.text((27, 27), str(c[0]), font=F(34, "b"), fill=INK + (255,), anchor="mm")
    place(base, sq, 86, 70); p = pill(c[1].upper(), 26, (20, 24, 34), WHITE, pad=(18, 6), outline=OUT, kind="p"); place(base, p, 86 + 36 + p.width / 2 - 10, 70)


def caption_chunks():
    out = []
    for sid in IDS:
        toks = WT[sid]["tokens"]; segs = []; cur = []
        for k, (tk, _) in enumerate(toks):
            cur.append(k)
            if re.search(r"[,।?!]$", tk): segs.append(cur); cur = []
        if cur: segs.append(cur)
        for sg in segs:
            n = len(sg); k = -(-n // 6); sizes = [n // k + (1 if j < n % k else 0) for j in range(k)]; i = 0
            for z in sizes: idx = sg[i:i + z]; out.append((SC[sid] + LEAD + toks[idx[0]][1], " ".join(toks[q][0] for q in idx))); i += z
    ends = [c[0] for c in out[1:]] + [TOTAL]
    return [(a, min(b, a + 3.2), txt_) for (a, txt_), b in zip(out, ends)]
CAPS = caption_chunks()
KEYW = {"usage", "limit", "limit,", "Settings", "Usage", "Project", "Projects", "cache", "effort", "thinking", "tools", "message", "chat", "reset", "credits", "upgrade",
        "पाँच", "सात", "तीन", "एक", "नई", "weekly", "session", "search", "memory"}
CAPDIR = HERE / "raw/caps"; CAPDIR.mkdir(parents=True, exist_ok=True)


def cap_path(s): return CAPDIR / (hashlib.md5(s.encode("utf-8")).hexdigest()[:16] + ".png")


def build_caps():
    todo = [s for _, _, s in CAPS if not cap_path(s).exists()]
    if not todo: return
    from playwright.sync_api import sync_playwright
    font_url = (ROOT / "shared/fonts/Mukta-ExtraBold.ttf").as_uri()
    css = ("@font-face{font-family:MK;src:url('%s');font-weight:800}body{margin:0;background:transparent}"
           "#c{display:inline-block;font-family:MK,sans-serif;font-weight:800;font-size:40px;line-height:1.35;color:#fff;background:#080a10;border:3px solid #2c3a24;border-radius:999px;padding:6px 32px;white-space:nowrap}"
           ".k{color:#AAEC5A}") % font_url
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1880, "height": 200}, device_scale_factor=1)
        for s in sorted(set(todo)):
            html = "".join(f'<span class="k">{w}</span> ' if w.strip(",.?!:।") in KEYW else f"{w} " for w in s.replace("&", "&amp;").split(" ")).strip()
            pg.set_content(f"<style>{css}</style><div id='c'>{html}</div>"); pg.wait_for_timeout(60)
            pg.evaluate("document.fonts.ready"); pg.locator("#c").screenshot(path=str(cap_path(s)), omit_background=True)
        b.close()


_cap = {}
def caption(base, t):
    for a, b, s in CAPS:
        if a - 0.04 <= t < b:
            if s not in _cap:
                im = Image.open(cap_path(s)).convert("RGBA")
                if im.width > 1820: im = im.resize((1820, int(im.height * 1820 / im.width)), Image.LANCZOS)
                _cap[s] = im
            place(base, _cap[s], W / 2, 1012, 1.0, fade(t, a - 0.04, 0.12)); return


# ---------- cursor ----------
def cursor_spr():
    im = Image.new("RGBA", (56, 76), (0, 0, 0, 0)); d = ImageDraw.Draw(im); pts = [(4, 3), (4, 52), (17, 41), (27, 64), (37, 59), (27, 37), (46, 37)]
    d.polygon([(x + 3, y + 3) for x, y in pts], fill=(0, 0, 0, 120)); d.polygon(pts, fill=(255, 255, 255, 255), outline=(10, 10, 10, 255)); return im.resize((int(56 * 1.35), int(76 * 1.35)), Image.LANCZOS)
CUR = cursor_spr()


def cursor_path(base, t, pts, clicks=()):
    if t < pts[0][0]: x, y = pts[0][1], pts[0][2]
    else:
        x, y = pts[-1][1], pts[-1][2]
        for (ta, xa, ya), (tb, xb, yb) in zip(pts, pts[1:]):
            if ta <= t < tb: q = ease_io((t - ta) / (tb - ta)); x, y = xa + (xb - xa) * q, ya + (yb - ya) * q; break
    place(base, CUR, x + 18, y + 26)
    for ck in clicks:
        if 0 <= t - ck <= 0.45: rr = 18 + 55 * (t - ck) / 0.45; SD(base).ellipse([x - rr, y - rr, x + rr, y + rr], outline=ACC + (255,), width=5)


def step(base, t, t0, text, y=110, col=ACC):
    if t >= t0: pp = pop(t, t0); place(base, pill(text, 34, col, INK, pad=(30, 9), kind="b"), W / 2, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def tip(base, t, t0, n, text):
    """TIP n banner at the top (shows the tip number + its name)"""
    if t < t0: return
    pp = pop(t, t0); im = pill(f"TIP {n}   {text}", 38, ACC, INK, pad=(34, 10), kind="b"); place(base, im, W / 2, 112, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def illu(base, x=1720, y=930, s="Illustration, example only"): place(base, pill(s, 22, (20, 24, 34), DIM, pad=(14, 4), kind="p"), x, y)


# ---------- official page crops (own capture, phrase marked yellow) ----------
SRC = {"best": "support.claude.com  /  Usage limit best practices", "lim": "support.claude.com  /  How do usage and length limits work?"}
NSRC = {"session": "lim", "same": "lim", "usage": "best", "factors": "best", "batch": "best", "vague": "best", "cache": "best", "expire": "best",
        "effort": "lim", "tools": "lim", "long": "lim", "earlier": "best", "credits": "lim", "adjust": "lim"}
_shot = {}
def note(key, w=1000, hh=440):
    """crop of raw/shot_<key>.png (article column, the marked phrase sits at the screenshot centre y=1080 px) on a white card"""
    ck = (key, w, hh)
    if ck in _shot: return _shot[ck]
    src = Image.open(HERE / f"raw/shot_{key}.png").convert("RGB"); cw = 1190; ch = int(cw * hh / w)
    pg = src.crop((600, 1080 - ch // 2, 600 + cw, 1080 + ch // 2)).resize((w - 60, hh - 60), Image.LANCZOS).convert("RGBA")
    g = np.ones(pg.height, dtype=np.float32); fl = 40; g[:fl] = np.linspace(0, 1, fl); g[-fl:] = np.minimum(g[-fl:], np.linspace(1, 0, fl))
    arr = np.array(pg).astype(np.float32); arr[:, :, :3] = 250 - (250 - arr[:, :, :3]) * g[:, None, None]; pg = Image.fromarray(arr.astype(np.uint8), "RGBA")
    sh = Image.new("RGBA", (w, hh + 56), (0, 0, 0, 0)); d = ImageDraw.Draw(sh); d.rounded_rectangle([0, 0, w - 1, hh - 1], 18, fill=(250, 249, 246, 255), outline=(200, 204, 214, 255), width=3)
    sh.alpha_composite(pg, (30, 30))
    tag = pill("Official: " + SRC[NSRC[key]], 20, (20, 24, 34), (200, 208, 224), pad=(16, 5), kind="p", outline=OUT)
    if tag.width > w: tag = tag.resize((w, int(tag.height * w / tag.width)), Image.LANCZOS)
    sh.alpha_composite(tag, ((w - tag.width) // 2, hh - 6)); _shot[ck] = sh; return sh


def bubble(w, h, text, side="user", size=34, col=None):
    im = NI(w + 8, h + 8); d = SD(im)
    d.rounded_rectangle([4, 4, w + 3, h + 3], 26, fill=((34, 52, 30, 255) if side == "user" else (26, 31, 45, 255)), outline=(col or (ACC if side == "user" else OUT)) + (255,), width=2)
    lines = text.split("\n"); f = F(size, "p"); lh = size * 1.35; y0 = h / 2 + 4 - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines): d.text((34, y0 + i * lh), ln, font=f, fill=WHITE + (255,), anchor="lm")
    return im


def bar(d, x, y, w, h, frac, col=ACC, bg=(40, 46, 60)):
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=bg + (255,))
    if frac > 0.01: d.rounded_rectangle([x, y, x + max(h, int(w * min(1, frac))), y + h], h // 2, fill=col + (255,))


def toggle(d, x, y, on, w=96, h=50):
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=(ACC if on else (70, 78, 98)) + (255,)); kx = x + w - h // 2 - 3 if on else x + h // 2 + 3
    d.ellipse([kx - h // 2 + 6, y + 6, kx + h // 2 - 6, y + h - 6], fill=(255, 255, 255, 255))


def chip_seq(base, t, items, x, y0, dy, size=34, side=0, w=None):
    """items: list of (time, text[, colour]) appearing one under the other"""
    for i, it in enumerate(items):
        tt, s = it[0], it[1]; col = it[2] if len(it) > 2 else ACC
        if t >= tt: pp = pop(t, tt); place(base, pill(s, size, (24, 30, 40), WHITE, pad=(28, 10), kind="b", outline=col), x, y0 + dy * i, 0.7 + 0.3 * pp, min(1, pp * 1.4))


MASC = Image.open(ROOT / "channels/devrobolab/mascot/cut/wave.png").convert("RGBA")
def robot(h): return MASC.resize((int(MASC.width * h / MASC.height), h), Image.LANCZOS)


# ---------- beats ----------
def _mk():
    B = []
    def add(i, sid, a, b): B.append(dict(id=i, sid=sid, t0=a, t1=b))
    add("hook_a", "hook", 0.0, A("hook", "अच्छी") - 0.25); add("hook_b", "hook", A("hook", "अच्छी") - 0.25, A("hook", "आज") - 0.2); add("hook_c", "hook", A("hook", "आज") - 0.2, E("hook"))
    add("how_a", "how", S("how", 0), A("how", "दूसरी") - 0.25); add("how_b", "how", A("how", "दूसरी") - 0.25, A("how", "ध्यान") - 0.45)
    add("how_c", "how", A("how", "ध्यान") - 0.45, A("how", "देखने") - 0.6); add("how_d", "how", A("how", "देखने") - 0.6, E("how"))
    add("eats_a", "eats", S("eats", 0), A("eats", "आपका") - 0.25); add("eats_b", "eats", A("eats", "आपका") - 0.25, A("eats", "मतलब") - 0.25); add("eats_c", "eats", A("eats", "मतलब") - 0.25, E("eats"))
    add("batch_a", "batch", S("batch", 0), A("batch", "दूसरा") - 0.25); add("batch_b", "batch", A("batch", "दूसरा") - 0.25, A("batch", "मान") - 0.25); add("batch_c", "batch", A("batch", "मान") - 0.25, E("batch"))
    add("clear_a", "clear", S("clear", 0), A("clear", "Example") - 0.25); add("clear_b", "clear", A("clear", "Example") - 0.25, A("clear", "इसकी") - 0.25)
    add("clear_c", "clear", A("clear", "इसकी") - 0.25, A("clear", "लंबा") - 1.0); add("clear_d", "clear", A("clear", "लंबा") - 1.0, E("clear"))
    add("proj_a", "projects", S("projects", 0), A("projects", "Example,") - 0.25); add("proj_b", "projects", A("projects", "Example,") - 0.25, A("projects", "याद") - 0.6); add("proj_c", "projects", A("projects", "याद") - 0.6, E("projects"))
    add("set_a", "settings", S("settings", 0), A("settings", "छठा") - 0.25); add("set_b", "settings", A("settings", "छठा") - 0.25, A("settings", "Official") - 0.25); add("set_c", "settings", A("settings", "Official") - 0.25, E("settings"))
    add("new_a", "newchat", S("newchat", 0), A("newchat", "उसी") - 0.25); add("new_b", "newchat", A("newchat", "उसी") - 0.25, A("newchat", "paid") - 0.5); add("new_c", "newchat", A("newchat", "paid") - 0.5, E("newchat"))
    add("limit_a", "limit", S("limit", 0), A("limit", "ज़रूरी") - 0.6); add("limit_b", "limit", A("limit", "ज़रूरी") - 0.6, E("limit"))
    add("cta_a", "cta", S("cta", 0), A("cta", "अगले") - 0.25); add("cta_b", "cta", A("cta", "अगले") - 0.25, TOTAL + 1)
    return B
B = _mk()


# hook
def chat_window(w, h, title="New chat"):
    im = card(w, h, 26, fill=(14, 17, 25)); d = SD(im)
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([48 + 30 * i, 44, 64 + 30 * i, 60], fill=c + (255,))
    d.text((160, 52), title, font=F(28, "p"), fill=DIM + (255,), anchor="lm"); return im


def b_hook_a(base, t, b):
    o = b["t0"]; t_msg = A("hook", "message"); t_full = A("hook", "पूरी"); t_wait = A("hook", "इंतज़ार"); t_many = A("hook", "बहुत")
    enter(base, chat_window(1180, 560, "Claude  ·  working on my report"), 760, 470, t, o, side=-1, dur=0.25)
    place(base, bubble(900, 84, "Make the summary table for chapter 3...", "user", 32), 760, 360, 1.0, fade(t, o + 0.05))
    # result first: the limit banner is on screen from the first second
    tb = o + 0.5
    if t >= tb:
        pp = pop(t, tb); bn = card(980, 150, 22, fill=(60, 24, 30), outline=RED); d = SD(bn)
        d.text((60, 62), "Usage limit reached", font=F(42, "b"), fill=WHITE + (255,), anchor="lm"); d.text((60, 118), "Your limit resets later", font=F(28, "p"), fill=(240, 200, 204, 255), anchor="lm")
        place(base, bn, 760, 560, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    m = card(420, 380, 28); d = SD(m); d.text((230, 80), "Current session", font=F(32, "b"), fill=WHITE + (255,), anchor="mm")
    fr = min(1, 0.55 + 0.45 * ease_out(max(0, t - o) / max(0.1, t_full - o))); bar(d, 60, 150, 340, 40, fr, RED if fr > 0.97 else AMB)
    d.text((230, 250), f"{int(fr * 100)}% used", font=F(52, "b"), fill=((RED if fr > 0.97 else AMB)) + (255,), anchor="mm")
    enter(base, m, 1590, 470, t, o + 0.15, side=1)
    if t >= t_wait: pp = pop(t, t_wait); place(base, pill("wait... hours", 36, (30, 30, 40), AMB, pad=(30, 10), kind="b", outline=AMB), 1590, 750, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= t_many: pp = pop(t, t_many); place(base, pill("happens to many users", 32, (20, 24, 34), DIM, pad=(26, 9), kind="p", outline=OUT), 760, 800, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    illu(base)


def b_hook_b(base, t, b):
    o = b["t0"]; place(base, pill("Claude's own help page explains it", 36, (24, 30, 40), WHITE, pad=(30, 10), kind="b", outline=ACC, hl=("own",)), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, note("factors", 1300, 560), W / 2, 560, t, o + 0.1)


def b_hook_c(base, t, b):
    o = b["t0"]
    place(base, pill("USAGE LIMIT: 7 SMART WAYS", 80, (20, 24, 34), WHITE, pad=(56, 20), outline=ACC, kind="b", glow=True, hl=("7",)), W / 2, 330, 0.85 + 0.15 * pop(t, o), min(1, fade(t, o, 0.2)))
    t3 = A("hook", "तीन");
    if t >= t3: pp = pop(t, t3); place(base, pill("+ 3 full examples", 40, ACC, INK, pad=(32, 10), kind="b"), W / 2, 480, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    for i, (s, tt) in enumerate([("how limits work", A("hook", "समझेंगे")), ("what uses more", A("hook", "चीज़ें")), ("limit hit? what next", A("hook", "आख़िर"))]):
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 36, (20, 24, 34), ACC, pad=(30, 10), outline=OUT, kind="b"), 430 + 530 * i, 650, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# how
def clock(w, h, frac, label):
    im = card(w, h, 28); d = SD(im); cx, cy, r = w / 2 + 20, h / 2 - 10, min(w, h) * 0.3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(50, 58, 80, 255), width=20)
    if frac > 0.005: d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=ACC + (255,), width=20)
    d.text((cx, cy - 10), "5h", font=F(80, "b"), fill=WHITE + (255,), anchor="mm"); d.text((cx, cy + 60), label, font=F(26, "p"), fill=DIM + (255,), anchor="mm")
    return im


def b_how_a(base, t, b):
    o = b["t0"]; t_two = A("how", "दो"); t_ses = A("how", "session"); t_first = A("how", "पहले", 2); t_back = A("how", "वापस")
    place(base, pill("Paid plans: 2 kinds of usage limit", 38, (24, 30, 40), WHITE, pad=(32, 10), kind="b", outline=ACC, hl=("2",)), W / 2, 150, 1.0, fade(t, o, 0.3))
    if t >= t_ses:
        fr = ease_io(min(1, max(0, (t - t_first) / 3.0))) if t >= t_first else 0.0
        enter(base, clock(560, 520, fr, "session limit"), 470, 540, t, t_ses - 0.2, side=-1)
        if t >= t_first: pp = pop(t, t_first); place(base, pill("starts at your FIRST message", 30, ACC, INK, pad=(24, 8), kind="b"), 470, 850, 0.7 + 0.3 * pp, min(1, pp * 1.4))
        if t >= t_back: pp = pop(t, t_back); place(base, pill("then resets in full", 28, (24, 30, 40), WHITE, pad=(22, 7), kind="p", outline=OUT), 470, 920, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    enter(base, note("session", 1060, 470), 1330, 560, t, max(o + 0.3, t_two - 0.2), side=1)


def b_how_b(base, t, b):
    o = b["t0"]; t_week = A("how", "weekly"); t_fix = A("how", "तय"); t_ultra = A("how", "verified")
    c = card(1300, 420, 30); d = SD(c); days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    d.text((70, 70), "WEEKLY LIMIT", font=F(44, "b"), fill=ACC + (255,), anchor="lm"); d.text((1250, 70), "example week", font=F(24, "p"), fill=DIM + (255,), anchor="rm")
    for i, dd in enumerate(days):
        x = 70 + i * 170; hot = (i == 3 and t >= t_fix)
        d.rounded_rectangle([x, 140, x + 150, 330], 20, fill=((44, 64, 34, 255) if hot else (26, 31, 45, 255)), outline=(ACC if hot else OUT) + (255,), width=3 if hot else 2)
        d.text((x + 75, 190), dd, font=F(34, "b"), fill=(WHITE if hot else DIM) + (255,), anchor="mm")
        if hot: d.text((x + 75, 270), "10:30", font=F(30, "b"), fill=ACC + (255,), anchor="mm"); d.text((x + 75, 305), "reset", font=F(22, "p"), fill=WHITE + (255,), anchor="mm")
    enter(base, c, W / 2, 440, t, o, side=0)
    if t >= t_fix: pp = pop(t, t_fix); place(base, pill("fixed day + time for YOUR account", 34, ACC, INK, pad=(28, 9), kind="b"), W / 2, 730, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= t_ultra: pp = pop(t, t_ultra); place(base, pill("Verified Ultra: no 5-hour limit", 30, (24, 30, 40), WHITE, pad=(26, 9), kind="p", outline=OUT, hl=("no",)), W / 2, 830, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_how_c(base, t, b):
    o = b["t0"]; tts = [A("how", "claude.ai"), A("how", "Code"), A("how", "Desktop,")]; t_one = A("how", "एक", 1, I("how", "Desktop,"))
    for i, (s, tt) in enumerate(zip(["claude.ai", "Claude Code", "Claude Desktop"], tts)):
        y = 330 + 190 * i; enter(base, card(460, 140, 26), 380, y, t, tt - 0.25, side=-1)
        if t >= tt - 0.25: place(base, pill(s, 40, (19, 23, 33), WHITE, pad=(10, 2), kind="b"), 380, y, 1.0, fade(t, tt - 0.1))
        if t >= t_one: SD(base).line([(630, y), (930, 520)], fill=ACC + (int(255 * fade(t, t_one, 0.4)),), width=6)
    if t >= t_one:
        pp = pop(t, t_one); c = card(560, 300, 30, glow=True); d = SD(c); d.text((300, 110), "ONE usage limit", font=F(46, "b"), fill=ACC + (255,), anchor="mm"); bar(d, 70, 190, 460, 36, 0.45)
        place(base, c, 1220, 520, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    if t < t_one: enter(base, note("same", 1000, 420), 1260, 500, t, o + 0.4, side=1)


SIDE = ["General", "Account", "Privacy", "Billing", "Usage", "Connectors"]
def settings_win(sel, pane_fn=None, w=1500, h=720):
    im = card(w, h, 26, fill=(14, 17, 25)); d = SD(im); ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + 330, oy + h - 1], 26, fill=(10, 12, 18, 255)); d.rectangle([ox + 300, oy, ox + 330, oy + h - 1], fill=(10, 12, 18, 255))
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([ox + 28 + 34 * i, oy + 26, ox + 46 + 34 * i, oy + 44], fill=c + (255,))
    d.text((ox + 34, oy + 80), "Settings", font=F(40, "b"), fill=WHITE + (255,))
    for i, s in enumerate(SIDE):
        y = oy + 160 + i * 78
        if i == sel: d.rounded_rectangle([ox + 20, y - 8, ox + 310, y + 52], 16, fill=(40, 60, 34, 255), outline=ACC + (255,), width=2)
        d.text((ox + 50, y), s, font=F(32, "p"), fill=(ACC if i == sel else (200, 208, 224)) + (255,))
    if pane_fn: pane_fn(d, ox + 330, oy, w - 330, h)
    else:
        for i in range(3): d.rounded_rectangle([ox + 380, oy + 170 + 130 * i, ox + w - 80, oy + 270 + 130 * i], 20, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
    return im


def usage_pane(fill_t):
    def f(d, ox, oy, w, h):
        d.text((ox + 50, oy + 60), "Plan usage limits", font=F(44, "b"), fill=WHITE + (255,))
        rows = [("Current session", "Resets in 2 hr 10 min", 0.62), ("Weekly: all models", "Resets Thu 10:30 AM", 0.35)]
        for i, (a, c, fr) in enumerate(rows):
            y = oy + 160 + i * 230; d.rounded_rectangle([ox + 50, y, ox + w - 50, y + 200], 20, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
            d.text((ox + 85, y + 30), a, font=F(34, "b"), fill=WHITE + (255,)); d.text((ox + 85, y + 140), c, font=F(28, "p"), fill=DIM + (255,))
            q = min(1, max(0, fill_t - 0.4 * i)); bar(d, ox + 85, y + 92, w - 300, 30, fr * ease_out(q)); d.text((ox + w - 90, y + 107), f"{int(fr * 100 * ease_out(q))}%", font=F(32, "b"), fill=ACC + (255,), anchor="rm")
    return f


def b_how_d(base, t, b):
    o = b["t0"]; t_set = A("how", "Settings"); t_use = A("how", "Usage"); t_cur = A("how", "Current"); t_wk = A("how", "weekly", 2)
    sel = 4 if t >= t_use else 0
    win = settings_win(sel, usage_pane((t - t_use) / 1.2) if sel == 4 else None); enter(base, win, 960, 560, t, o, dur=0.3)
    step(base, t, t_set - 0.2, "STEP 2   Usage" if t >= t_use else "STEP 1   open Settings")
    pts = [(o, 1300, 300), (t_use - 0.8, 1300, 300), (t_use, 330, 523), (t_cur - 0.3, 330, 523), (t_cur + 0.4, 1200, 450), (t_wk - 0.2, 1200, 450), (t_wk + 0.4, 1200, 680)]
    cursor_path(base, t, pts, clicks=(t_use,)); illu(base, s="Illustration, example numbers")


# eats
FACT = [("message length", "लंबा"), ("file size", "file"), ("chat length", "chat"), ("web search / Research", "Web"), ("model choice", "model"), ("effort level", "effort"),
        ("artifacts", "Artifacts"), ("multi-step tasks", "steps")]
def b_eats_a(base, t, b):
    o = b["t0"]; place(base, pill("Why does usage run out fast?", 42, (24, 30, 40), WHITE, pad=(34, 12), kind="b", outline=ACC), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, note("factors", 1300, 520), W / 2, 570, t, o + 0.2)


def b_eats_b(base, t, b):
    o = b["t0"]; place(base, pill("WHAT USES MORE", 44, (24, 30, 40), WHITE, pad=(34, 12), kind="b", outline=ACC, hl=("MORE",)), W / 2, 150, 1.0, fade(t, o, 0.3))
    for i, (s, key) in enumerate(FACT):
        tt = A("eats", key) - 0.15; col, row = i % 4, i // 4; x = 285 + 450 * col; y = 400 + 300 * row
        if t >= tt:
            pp = pop(t, tt); c = card(400, 240, 26, outline=ACC if t < tt + 1.2 else OUT); d = SD(c)
            d.rounded_rectangle([40, 40, 104, 104], 16, fill=ACC + (255,)); d.text((72, 72), str(i + 1), font=F(36, "b"), fill=INK + (255,), anchor="mm")
            words = s.split(" "); l1 = " ".join(words[:2]); l2 = " ".join(words[2:])
            d.text((40, 160), l1, font=F(36, "b"), fill=WHITE + (255,), anchor="lm")
            if l2: d.text((40, 210), l2, font=F(30, "p"), fill=DIM + (255,), anchor="lm")
            place(base, c, x, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_eats_c(base, t, b):
    o = b["t0"]; t7 = A("eats", "सात")
    place(base, pill("not every message costs the same", 40, (24, 30, 40), WHITE, pad=(32, 11), kind="b", outline=ACC, hl=("not",)), W / 2, 170, 1.0, fade(t, o, 0.3))
    for i, (s, fr, tt) in enumerate([("short question", 0.12, o + 0.2), ("long chat + big PDF", 0.55, o + 0.9), ("web search + high effort", 0.85, o + 1.6)]):
        y = 360 + 160 * i; c = card(1300, 120, 24); d = SD(c); d.text((60, 80), s, font=F(36, "b"), fill=WHITE + (255,), anchor="lm")
        q = ease_out(min(1, max(0, (t - tt) / 0.8))); bar(d, 640, 62, 560, 36, fr * q, [ACC, AMB, RED][i]); enter(base, c, W / 2, y, t, tt)
    illu(base, x=1640, y=820, s="Illustration, relative only")
    if t >= t7: pp = pop(t, t7); place(base, pill("now: 7 ways to save it", 40, ACC, INK, pad=(34, 10), kind="b"), W / 2, 900, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# batch (example 1)
def b_batch_a(base, t, b):
    o = b["t0"]; tip(base, t, o + 0.1, 1, "PLAN FIRST")
    c = card(1100, 470, 30); d = SD(c); d.text((70, 70), "Before you start a chat", font=F(42, "b"), fill=WHITE + (255,), anchor="lm")
    rows = [("What exactly do I need?", A("batch", "ठीक-ठीक")), ("Give background info up front", A("batch", "background"))]
    for i, (s, tt) in enumerate(rows):
        y = 170 + 130 * i; on = t >= tt
        d.rounded_rectangle([70, y, 1030, y + 100], 20, fill=((40, 60, 34, 255) if on else (26, 31, 45, 255)), outline=(ACC if on else OUT) + (255,), width=3 if on else 2)
        d.rounded_rectangle([100, y + 28, 144, y + 72], 10, outline=(ACC if on else DIM) + (255,), width=4)
        if on: d.line([(108, y + 50), (120, y + 63), (138, y + 36)], fill=ACC + (255,), width=6)
        d.text((180, y + 50), s, font=F(36, "p"), fill=WHITE + (255,), anchor="lm")
    enter(base, c, W / 2, 520, t, o + 0.2)


def b_batch_b(base, t, b):
    o = b["t0"]; tip(base, t, o + 0.05, 2, "ONE MESSAGE, MANY QUESTIONS"); t_ex = A("batch", "example")
    enter(base, note("batch", 1300, 500), W / 2, 540, t, o + 0.2)
    if t >= t_ex: pp = pop(t, t_ex); place(base, pill("the official example: math problems", 32, ACC, INK, pad=(28, 9), kind="b"), W / 2, 880, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_batch_c(base, t, b):
    o = b["t0"]; t_sep = A("batch", "अलग"); t_one = A("batch", "इसकी"); t_step = A("batch", "step"); t_res = A("batch", "सिर्फ़")
    place(base, pill("EXAMPLE 1   5 math questions", 36, (24, 30, 40), WHITE, pad=(30, 10), kind="b", outline=ACC, hl=("EXAMPLE", "1")), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, card(760, 640, 28, outline=RED if t >= t_sep else OUT), 500, 560, t, o + 0.1, side=-1)
    txt(base, (500, 290), "5 separate messages", 34, RED, "b", "mm", fade(t, o + 0.2))
    for i in range(5):
        tt = t_sep + 0.25 * i
        if t >= tt: place(base, bubble(560, 64, f"Q{i + 1}: 3x + {i + 2} = {[8, 15, 22, 29, 36][i]}", "user", 28, RED), 500, 360 + 92 * i, 1.0, fade(t, tt))
    if t >= t_sep + 1.4: place(base, pill("5 x back and forth", 30, (60, 24, 30), RED, pad=(22, 7), kind="b", outline=RED), 500, 850, 1.0, fade(t, t_sep + 1.4))
    if t >= t_one:
        enter(base, card(820, 640, 28, glow=t >= t_res, outline=ACC), 1400, 560, t, t_one, side=1)
        txt(base, (1400, 290), "1 message", 34, ACC, "b", "mm", fade(t, t_one + 0.1))
        lines = "Solve these 5 questions:\n1) 3x + 2 = 8\n2) 3x + 3 = 15\n3) 3x + 4 = 22\n4) 3x + 5 = 29\n5) 3x + 6 = 36"
        place(base, bubble(660, 360, lines, "user", 30), 1400, 510, 1.0, fade(t, t_one + 0.2))
        if t >= t_step: place(base, bubble(660, 80, typed("Explain each step by step.", t, t_step, t_step + 1.2), "user", 30), 1400, 760, 1.0, fade(t, t_step))
    if t >= t_res: pp = pop(t, t_res); place(base, pill("same work:  5  ->  1 message", 40, ACC, INK, pad=(34, 10), kind="b"), W / 2, 920, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# clear (example 2)
def b_clear_a(base, t, b):
    o = b["t0"]; tip(base, t, o + 0.1, 3, "CLEAR + FULL, READ BEFORE SEND"); t_q = A("clear", "अधूरा")
    enter(base, note("vague", 1200, 470), W / 2, 500, t, o + 0.2)
    if t >= t_q: pp = pop(t, t_q); place(base, pill("unclear question = extra messages", 34, (60, 24, 30), RED, pad=(28, 9), kind="b", outline=RED), W / 2, 860, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_clear_b(base, t, b):
    o = b["t0"]; t_u = A("clear", "email"); t_c = A("clear", "पूछेगा"); t_w = A("clear", "चले")
    place(base, pill("EXAMPLE 2   writing an email", 36, (24, 30, 40), WHITE, pad=(30, 10), kind="b", outline=ACC, hl=("EXAMPLE", "2")), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, chat_window(1300, 640, "Vague prompt"), W / 2, 560, t, o + 0.1)
    if t >= t_u: place(base, bubble(560, 80, typed("Write an email.", t, t_u, t_u + 0.8), "user", 34, RED), 1250, 380, 1.0, fade(t, t_u))
    if t >= t_c: place(base, bubble(800, 80, "To whom? About what? Which tone?", "claude", 34), 760, 500, 1.0, fade(t, t_c))
    if t >= t_c + 1.6: place(base, bubble(560, 80, "To my manager...", "user", 34, RED), 1250, 620, 1.0, fade(t, t_c + 1.6))
    if t >= t_c + 2.6: place(base, bubble(600, 80, "And the reason?", "claude", 34), 760, 740, 1.0, fade(t, t_c + 2.6))
    if t >= t_w: pp = pop(t, t_w); place(base, pill("3-4 messages gone", 36, (60, 24, 30), RED, pad=(28, 9), kind="b", outline=RED), 1500, 860, 0.7 + 0.3 * pp, min(1, pp * 1.4), -4)
    illu(base, x=1700, y=950)


def b_clear_c(base, t, b):
    o = b["t0"]; t_ans = A("clear", "पूरा", 1, I("clear", "lines"))
    place(base, pill("one complete prompt", 38, ACC, INK, pad=(32, 10), kind="b"), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, card(1400, 620, 30, outline=ACC, glow=t >= t_ans), W / 2, 540, t, o + 0.1)
    rows = [("To", "my manager", A("clear", "manager")), ("About", "leave on Friday", A("clear", "शुक्रवार")), ("Reason", "family function", A("clear", "वजह")),
            ("Tone", "polite and short", A("clear", "tone", 2)), ("Length", "5 lines", A("clear", "lines"))]
    for i, (a, c, tt) in enumerate(rows):
        y = 300 + 92 * i
        d = SD(base)
        if t < tt - 0.1:   # empty field rows are on screen from the start, the value fills in when it is spoken
            q = fade(t, o + 0.3 + 0.08 * i); d.rounded_rectangle([340, y - 38, 1580, y + 38], 18, fill=(22, 26, 36) + (int(255 * q),), outline=OUT + (int(255 * q),), width=2)
            txt(base, (380, y), a, 34, DIM, "b", "lm", q); continue
        if t >= tt - 0.1:
            q = fade(t, tt - 0.1); hot = t < tt + 1.0
            d.rounded_rectangle([340, y - 38, 1580, y + 38], 18, fill=((44, 64, 34) if hot else (26, 31, 45)) + (int(255 * q),), outline=(ACC if hot else OUT) + (int(255 * q),), width=2)
            txt(base, (380, y), a, 34, ACC, "b", "lm", q); txt(base, (640, y), c, 36, WHITE, "p", "lm", q)
    if t >= t_ans: pp = pop(t, t_ans); place(base, pill("1 message = full answer", 36, (24, 30, 40), ACC, pad=(28, 9), kind="b", outline=ACC), W / 2, 880, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    illu(base, x=1700, y=950)


def b_clear_d(base, t, b):
    o = b["t0"]; t_code = A("clear", "Coding")
    c = card(760, 520, 28); d = SD(c); d.text((60, 70), "Editing a long text?", font=F(38, "b"), fill=WHITE + (255,), anchor="lm")
    for i in range(7): d.rounded_rectangle([60, 150 + 46 * i, 60 + [620, 560, 640, 600, 520, 630, 420][i], 172 + 46 * i], 8, fill=(46, 54, 72, 255))
    d.text((60, 520 - 40), "send the WHOLE text at once", font=F(32, "b"), fill=ACC + (255,), anchor="lm")
    enter(base, c, 520, 520, t, o, side=-1)
    if t >= t_code - 0.3:
        c2 = card(800, 520, 28, fill=(10, 12, 16)); d2 = SD(c2); d2.text((60, 70), "Coding?", font=F(38, "b"), fill=WHITE + (255,), anchor="lm")
        lines = ["$ setup: Python 3.12, Flask, Windows", "$ error: 'KeyError: user_id' in app.py", "", "# full app.py pasted below", "def login(req): ..."]
        for i, ln in enumerate(lines): d2.text((60, 150 + 54 * i), ln, font=F(28, "p"), fill=((ACC if i < 2 else DIM)) + (255,), anchor="lm")
        d2.text((60, 480), "full setup + full code in message 1", font=F(30, "b"), fill=ACC + (255,), anchor="lm")
        enter(base, c2, 1390, 520, t, t_code - 0.3, side=1)
    illu(base, x=1700, y=850)


# projects (example 3)
def doc_icon(d, x, y, s=1.0, col=ACC, label="PDF"):
    w, h = 110 * s, 140 * s; d.rounded_rectangle([x, y, x + w, y + h], 12, fill=(240, 244, 236, 255)); d.polygon([(x + w - 34 * s, y), (x + w, y + 34 * s), (x + w - 34 * s, y + 34 * s)], fill=(200, 206, 196, 255))
    d.rounded_rectangle([x + 10 * s, y + h - 50 * s, x + w - 10 * s, y + h - 14 * s], 8, fill=col + (255,)); d.text((x + w / 2, y + h - 32 * s), label, font=F(int(24 * s), "b"), fill=INK + (255,), anchor="mm")


def b_proj_a(base, t, b):
    o = b["t0"]; tip(base, t, o + 0.1, 4, "PROJECTS FOR FILES YOU REUSE"); t_up = A("projects", "upload"); t_cache = A("projects", "cache"); t_less = A("projects", "कम")
    c = card(820, 560, 30); d = SD(c); d.text((60, 60), "Project", font=F(40, "b"), fill=WHITE + (255,), anchor="lm")
    if t >= t_up: doc_icon(d, 80, 140); doc_icon(d, 220, 140, label="DOC")
    if t >= t_cache:
        d.rounded_rectangle([430, 130, 780, 300], 22, fill=(40, 60, 34, 255), outline=ACC + (255,), width=3); d.text((605, 190), "cached", font=F(40, "b"), fill=ACC + (255,), anchor="mm"); d.text((605, 250), "for reuse", font=F(28, "p"), fill=WHITE + (255,), anchor="mm")
    if t >= t_less:
        d.text((60, 380), "new content", font=F(30, "p"), fill=DIM + (255,), anchor="lm"); bar(d, 300, 365, 440, 30, 0.9, AMB)
        d.text((60, 460), "cached part", font=F(30, "p"), fill=DIM + (255,), anchor="lm"); bar(d, 300, 445, 440, 30, 0.9 * (1 - 0.6 * ease_out(min(1, (t - t_less) / 0.8))), ACC)
    enter(base, c, 520, 560, t, o + 0.2, side=-1)
    enter(base, note("cache", 900, 470), 1420, 560, t, o + 0.5, side=1)
    illu(base, x=520, y=880, s="Illustration, relative bars")


def b_proj_b(base, t, b):
    o = b["t0"]; t_new = A("projects", "बनाओ,"); t_pdf = A("projects", "PDF"); t1 = A("projects", "points"); t2 = A("projects", "quiz"); t3 = A("projects", "गलत"); t_no = A("projects", "दोबारा")
    place(base, pill("EXAMPLE 3   exam prep with a Project", 36, (24, 30, 40), WHITE, pad=(30, 10), kind="b", outline=ACC, hl=("EXAMPLE", "3")), W / 2, 150, 1.0, fade(t, o, 0.3))
    c = card(560, 640, 28); d = SD(c); d.text((50, 60), "Exam prep: Biology", font=F(34, "b"), fill=WHITE + (255,), anchor="lm"); d.text((50, 120), "Project knowledge", font=F(26, "p"), fill=DIM + (255,), anchor="lm")
    if t >= t_pdf: doc_icon(d, 50, 170, 0.9); d.text((170, 230), "chapter5_notes.pdf", font=F(28, "p"), fill=WHITE + (255,), anchor="lm")
    if t >= t_no: d.rounded_rectangle([50, 480, 510, 580], 18, fill=(40, 60, 34, 255), outline=ACC + (255,), width=2); d.text((280, 530), "uploaded ONCE", font=F(34, "b"), fill=ACC + (255,), anchor="mm")
    enter(base, c, 400, 560, t, max(o, t_new - 0.3), side=-1)
    enter(base, chat_window(1120, 640, "Chat inside the project"), 1300, 560, t, max(o + 0.2, t1 - 1.2), side=1)
    for i, (s, tt) in enumerate([("List the key points of this chapter.", t1), ("Make a 10-question quiz.", t2), ("Explain my wrong answers.", t3)]):
        if t >= tt - 0.2: place(base, bubble(900, 84, typed(s, t, tt - 0.2, tt + 0.8), "user", 32), 1300, 380 + 140 * i, 1.0, fade(t, tt - 0.2))
    illu(base, x=1700, y=950)


def b_proj_c(base, t, b):
    o = b["t0"]; t_brk = A("projects", "break"); t_full = A("projects", "पूरा")
    place(base, pill("one thing to remember", 36, (40, 34, 20), AMB, pad=(30, 10), kind="b", outline=AMB), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, note("expire", 1200, 460), W / 2, 500, t, o + 0.1)
    if t >= t_brk: pp = pop(t, t_brk); place(base, pill("long break = first message counts in full again", 32, (60, 44, 20), AMB, pad=(26, 9), kind="b", outline=AMB), W / 2, 850, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# settings
def b_set_a(base, t, b):
    o = b["t0"]; tip(base, t, o + 0.1, 5, "LOWER EFFORT FOR EASY TASKS"); t_low = A("settings", "कम"); t_tok = A("settings", "tokens"); t_th = A("settings", "thinking", 2) if sum("thinking" in x[0] for x in WT["settings"]["tokens"]) > 1 else A("settings", "thinking")
    c = card(820, 600, 30); d = SD(c); d.text((60, 60), "Effort", font=F(40, "b"), fill=WHITE + (255,), anchor="lm")
    for i, (s, fr) in enumerate([("Low", 0.25), ("Medium", 0.55), ("High", 0.95)]):
        y = 130 + 105 * i; sel = (i == 0 and t >= t_low) or (i == 2 and t < t_low)
        d.rounded_rectangle([60, y, 760, y + 85], 18, fill=((40, 60, 34, 255) if sel else (26, 31, 45, 255)), outline=(ACC if sel else OUT) + (255,), width=3 if sel else 2)
        d.text((95, y + 42), s, font=F(32, "b"), fill=WHITE + (255,), anchor="lm"); bar(d, 320, y + 28, 400, 30, fr, [ACC, AMB, RED][i])
    d.text((60, 470), "Thinking", font=F(34, "b"), fill=WHITE + (255,), anchor="lm"); toggle(d, 640, 446, t < t_th + 0.3)
    d.text((60, 540), "bars = more tokens", font=F(24, "p"), fill=DIM + (255,), anchor="lm")
    enter(base, c, 520, 560, t, o + 0.2, side=-1)
    enter(base, note("effort", 900, 420), 1420, 520, t, max(o + 0.4, t_tok - 1.5), side=1)
    if t >= t_th: pp = pop(t, t_th); place(base, pill("thinking OFF when not needed", 30, ACC, INK, pad=(24, 8), kind="b"), 1420, 830, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    illu(base, x=520, y=900)


def b_set_b(base, t, b):
    o = b["t0"]; tip(base, t, o + 0.05, 6, "TURN OFF TOOLS YOU DON'T NEED"); t_g = A("settings", "Gmail"); t_off = A("settings", "बंद", 3) if sum("बंद" in x[0] for x in WT["settings"]["tokens"]) >= 3 else A("settings", "Gmail") + 2.5; t_ws = A("settings", "web")
    c = card(820, 520, 30); d = SD(c); d.text((60, 60), "Tools in this chat", font=F(38, "b"), fill=WHITE + (255,), anchor="lm")
    for i, (s, offt) in enumerate([("Gmail (connected app)", t_off), ("Calendar (connected app)", t_off + 0.4), ("Web search", t_ws + 0.6)]):
        y = 140 + 120 * i; on = t < offt
        d.rounded_rectangle([60, y, 760, y + 95], 18, fill=(26, 31, 45, 255), outline=OUT + (255,), width=2); d.text((95, y + 47), s, font=F(32, "p"), fill=(WHITE if on else DIM) + (255,), anchor="lm"); toggle(d, 640, y + 22, on)
    enter(base, c, 520, 540, t, o + 0.15, side=-1)
    if t >= t_ws - 0.2: place(base, bubble(820, 90, typed("Don't search the web for this.", t, t_ws - 0.2, t_ws + 1.0), "user", 34), 1400, 470, 1.0, fade(t, t_ws - 0.2))
    if t >= t_ws + 1.2: place(base, pill("no fresh info needed? no web search", 30, (24, 30, 40), ACC, pad=(24, 8), kind="b", outline=ACC), 1400, 620, 1.0, fade(t, t_ws + 1.2))
    illu(base, x=520, y=860)


def b_set_c(base, t, b):
    o = b["t0"]; place(base, pill("official: tools + connectors use many tokens", 36, (24, 30, 40), WHITE, pad=(30, 10), kind="b", outline=ACC, hl=("many",)), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, note("tools", 1300, 520), W / 2, 560, t, o + 0.1)


# newchat
def b_new_a(base, t, b):
    o = b["t0"]; tip(base, t, o + 0.1, 7, "HANDLE LONG CHATS SMARTLY"); t_new = A("newchat", "नई")
    c = chat_window(700, 600, "Very long chat"); d = SD(c)
    sc = (t - o) * 40
    for i in range(12):
        y = 120 + i * 70 - sc % 70
        if 100 < y < 560: d.rounded_rectangle([(80 if i % 2 else 260), y, (470 if i % 2 else 640), y + 46], 14, fill=((40, 60, 34, 255) if i % 2 == 0 else (30, 36, 52, 255)))
    enter(base, c, 480, 540, t, o + 0.15, side=-1)
    enter(base, note("long", 1000, 420), 1380, 470, t, o + 0.5, side=1)
    if t >= t_new: pp = pop(t, t_new); place(base, pill("+  New chat", 44, ACC, INK, pad=(40, 12), kind="b", glow=True), 1380, 820, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def b_new_b(base, t, b):
    o = b["t0"]; t_p = A("newchat", "paste"); t_as = A("newchat", "mentioned") - 0.3
    c = card(760, 380, 28, outline=RED); d = SD(c); d.text((380, 70), "pasting it all again", font=F(36, "b"), fill=RED + (255,), anchor="mm")
    for i in range(4): d.rounded_rectangle([60, 140 + 50 * i, 700, 170 + 50 * i], 8, fill=(70, 40, 46, 255))
    enter(base, c, 520, 420, t, o, side=-1)
    if t >= t_p + 0.3: a = fade(t, t_p + 0.3); SD(base).line([(170, 260), (870, 580)], fill=RED + (int(255 * a),), width=10); SD(base).line([(870, 260), (170, 580)], fill=RED + (int(255 * a),), width=10)
    if t >= t_as - 0.2: place(base, bubble(820, 90, typed("As mentioned earlier, use that table.", t, t_as - 0.2, t_as + 1.2), "user", 34), 1380, 420, 1.0, fade(t, t_as - 0.2))
    enter(base, note("earlier", 900, 300), 1380, 700, t, max(o + 0.3, t_as - 0.2), side=1)


def b_new_c(base, t, b):
    o = b["t0"]; t_s = A("newchat", "search"); t_m = A("newchat", "memory")
    place(base, pill("Paid plans (Pro, Max, Ultra, Team, Enterprise)", 34, (24, 30, 40), WHITE, pad=(30, 10), kind="b", outline=ACC), W / 2, 170, 1.0, fade(t, o, 0.3))
    for i, (s, c2, tt) in enumerate([("Search past chats", "Claude finds old info", t_s), ("Memory", "context across chats", t_m)]):
        x = 560 + 800 * i
        if t >= tt - 0.3:
            c = card(640, 360, 30, glow=True); d = SD(c); d.text((340, 150), s, font=F(46, "b"), fill=ACC + (255,), anchor="mm"); d.text((340, 230), c2, font=F(32, "p"), fill=WHITE + (255,), anchor="mm")
            enter(base, c, x, 520, t, tt - 0.3, side=-1 if i == 0 else 1)
    if t >= t_m + 1.0: pp = pop(t, t_m + 1.0); place(base, pill("no need to repeat everything", 36, ACC, INK, pad=(30, 10), kind="b"), W / 2, 820, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# limit
def b_limit_a(base, t, b):
    o = b["t0"]; tts = [A("limit", "पहला"), A("limit", "दूसरा"), A("limit", "तीसरा")]
    place(base, pill("limit still hit? 3 options", 42, (24, 30, 40), WHITE, pad=(34, 12), kind="b", outline=ACC, hl=("3",)), W / 2, 150, 1.0, fade(t, o, 0.3))
    for i, ((a, c, c3), tt) in enumerate(zip([("WAIT", "for the reset", "time: Settings > Usage"), ("UPGRADE", "your plan", "new limit applies right away"), ("USAGE CREDITS", "paid plans", "work continues on credits")], tts)):
        x = 380 + 580 * i
        t_in = min(tt - 0.2, o + 0.4 + 0.35 * i)
        if t >= t_in:
            cc = card(520, 440, 30, glow=(tt <= t < tt + 2.5), outline=(ACC if tt <= t < tt + 2.5 else OUT)); d = SD(cc); d.rounded_rectangle([40, 40, 110, 110], 18, fill=ACC + (255,)); d.text((75, 75), str(i + 1), font=F(40, "b"), fill=INK + (255,), anchor="mm")
            d.text((40, 190), a, font=F(46, "b"), fill=WHITE + (255,), anchor="lm"); d.text((40, 255), c, font=F(32, "p"), fill=DIM + (255,), anchor="lm"); d.text((40, 360), c3, font=F(26, "p"), fill=ACC + (255,), anchor="lm")
            enter(base, cc, x, 540, t, t_in)


def b_limit_b(base, t, b):
    o = b["t0"]; t_adj = A("limit", "मर्ज़ी"); t_cnt = A("limit", "count"); t_chk = A("limit", "हमेशा")
    place(base, pill("CAUTION", 44, (60, 44, 20), AMB, pad=(36, 10), kind="b", outline=AMB), W / 2, 150, 1.0, fade(t, o, 0.3))
    enter(base, note("adjust", 1200, 440), W / 2, 470, t, o + 0.15)
    if t >= t_cnt: pp = pop(t, t_cnt); place(base, pill("no fixed message count", 34, (60, 24, 30), RED, pad=(28, 9), kind="b", outline=RED), 620, 830, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= t_chk: pp = pop(t, t_chk); place(base, pill("check: Settings > Usage", 36, ACC, INK, pad=(30, 10), kind="b"), 1320, 830, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# cta
def b_cta_a(base, t, b):
    o = b["t0"]
    place(base, pill("7 WAYS, RECAP", 50, (20, 24, 34), WHITE, pad=(46, 14), kind="b", outline=ACC, glow=True), W / 2, 150, 1.0, fade(t, o, 0.25))
    rows = [("plan first", "plan"), ("many questions, 1 message", "मिलते-जुलते"), ("clear + full, read before send", "साफ़"), ("reused files in a Project", "Project"),
            ("lower effort for easy tasks", "effort"), ("turn off unused tools", "tools"), ("long chat? start a new one", "लंबी")]
    for i, (s, key) in enumerate(rows):
        tt = A("cta", key) - 0.2; col, r = (0, i) if i < 4 else (1, i - 4); x = 520 + 880 * col; y = 300 + 140 * r
        if t >= tt:
            c = NI(840, 116); d = SD(c); d.rounded_rectangle([2, 2, 836, 112], 24, fill=CARD + (255,), outline=OUT + (255,), width=3)
            d.rounded_rectangle([24, 24, 92, 92], 16, fill=ACC + (255,)); d.text((58, 58), str(i + 1), font=F(40, "b"), fill=INK + (255,), anchor="mm"); d.text((120, 58), s, font=F(34, "p"), fill=WHITE + (255,), anchor="lm")
            enter(base, c, x, y, t, tt)


def b_cta_b(base, t, b):
    o = b["t0"]; t_f = A("cta", "follow")
    c = card(1000, 300, 30, glow=True); d = SD(c); d.text((70, 70), "NEXT VIDEO", font=F(32, "b"), fill=ACC + (255,), anchor="lm")
    d.text((70, 150), "Claude Projects:", font=F(52, "b"), fill=WHITE + (255,), anchor="lm"); d.text((70, 220), "how to make and use them, step by step", font=F(34, "p"), fill=DIM + (255,), anchor="lm")
    enter(base, c, 760, 420, t, o + 0.05, side=-1)
    rb = robot(520); enter(base, rb, 1530, 520, t, o + 0.3, side=1)
    if t >= t_f - 0.4: pp = pop(t, t_f - 0.4); place(base, pill("+ Follow", 64, ACC, INK, pad=(54, 14), kind="b", glow=True), 760, 720, 0.7 + 0.3 * pp, min(1, pp * 1.4))


FN = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}
def frame(t):
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = BG.copy()
    FN[b["id"]](base, t, b)
    badge(base, b["sid"], t); caption(base, t)
    return np.array(base.convert("RGB"))


SR = 24000
def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def encode(frames_iter, n_frames, voice_wav, music, out, music_start=6, music_gain_db=-22, lufs=-14.0):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice_wav), "-stream_loop", "-1", "-ss", str(music_start), "-i", str(music)]
    fc = f"[2:a]volume={music_gain_db}dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I={lufs}:TP=-1.5:LRA=7[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, fr in enumerate(frames_iter):
        p.stdin.write(fr.tobytes())
        if i % 300 == 0: print(f"  frame {i}/{n_frames}", flush=True)
    p.stdin.close(); p.wait()


def main():
    print(f"total {TOTAL:.1f}s; chapters:", [(s, round(SC[s], 1)) for s in IDS])
    build_caps()
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/F_{tt:06.1f}.png")
        return
    if len(sys.argv) > 1 and sys.argv[1] == "sheet":   # python make_final.py sheet <step_s>: contact sheets of the timeline (pre-render check)
        stp = float(sys.argv[2]); ts = [round(x, 2) for x in np.arange(0.5, TOTAL, stp)]; n = 0
        for k in range(0, len(ts), 20):
            sh = Image.new("RGB", (5 * 480, 4 * 290), (0, 0, 0)); dd = ImageDraw.Draw(sh)
            for j, tt in enumerate(ts[k:k + 20]):
                im = Image.fromarray(frame(tt)).resize((480, 270)); sh.paste(im, ((j % 5) * 480, (j // 5) * 290)); dd.text(((j % 5) * 480 + 6, (j // 5) * 290 + 272), f"{tt:.1f}s", fill=(255, 255, 0))
            sh.save(HERE / f"review/sheet_{n:02d}.png"); n += 1
        print("sheets", n); return
    if len(sys.argv) > 4 and sys.argv[1] == "range":
        t0, t1, outp = float(sys.argv[2]), float(sys.argv[3]), Path(sys.argv[4]); n0, n1 = int(round(t0 * FPS)), int(round(t1 * FPS)); outp.parent.mkdir(parents=True, exist_ok=True)
        pr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(outp)], stdin=subprocess.PIPE)
        for i in range(n0, n1): pr.stdin.write(frame(i / FPS).tobytes())
        pr.stdin.close(); pr.wait(); print("range rendered", t0, t1, outp); return
    build_audio(HERE / "audio/voice_final.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice_final.wav", ROOT / deck["music"]["file"], HERE / "output/long_final.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
