"""Claude Code 04 (prompt caching) LONG video build (adapted from 044 make_final.py), 16:9 1920x1080.
v3 (2026-11-07, after the user's review): per-beat zoom K (cards fill the screen), no blank frames, Hindi captions rendered by Chromium
(Pillow here has no raqm), every action tied to word times T(scene, token). Look: STYLE_LIBRARY sections 0, 9, 10 (no face / robot, dark neon, sky blue).
Run: python make_final.py [frames t1 t2 ...]"""
import hashlib, json, math, re, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = Path(__file__).parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import ease_out, ease_back, ease_io, wav_dur
import subprocess

W, H, FPS = 1920, 1080, 30
LEAD, AFTER = 0.05, 0.05
SKY = (172, 146, 255); WHITE = (255, 255, 255); RED = (255, 96, 106); AMB = (255, 190, 80); DIM = (150, 160, 182)
BG0 = (6, 11, 13); CARD = (19, 23, 33); OUT = (58, 68, 94); INK = (10, 12, 18)
FMUK = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf"); FPOP = str(ROOT / "shared/fonts/Poppins-Medium.ttf"); FPOPB = str(ROOT / "shared/fonts/Poppins-Bold.ttf"); FMONO = str(ROOT / "shared/fonts/IBMPlexMono-Bold.ttf")
deck = json.load(open(HERE / "deck.json", encoding="utf-8")); WT = json.load(open(HERE / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; D[-1] += 3.0; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START)); DUR = dict(zip(IDS, D))


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]
def S(scene, off): return SC[scene] + off
def E(scene): return SC[scene] + DUR[scene]


# ---------- zoom K: design coordinates (1920x1080) are scaled about the screen centre, sprites are built at K size ----------
K = 1.0
CX0, CY0 = 960, 540
_f = {}
def F(sz, kind="m"):
    k = (int(round(sz * K)), kind)
    if k not in _f: _f[k] = ImageFont.truetype({"m": FMUK, "p": FPOP, "b": FPOPB, "t": FMONO}[kind], k[0])
    return _f[k]


class SD:
    """ImageDraw in design units: sprite mode scales by K; screen mode (the full 1920x1080 base) also maps positions about the centre"""
    def __init__(self, img): self.d = ImageDraw.Draw(img); self.scr = (img.size == (W, H))
    def _p(self, x, y): return (CX0 + (x - CX0) * K, CY0 + (y - CY0) * K) if self.scr else (x * K, y * K)
    def _b(self, b): a = self._p(b[0], b[1]); c = self._p(b[2], b[3]); return [a[0], a[1], c[0], c[1]]
    def _w(self, w): return max(1, int(round(w * K)))
    def text(self, xy, s, font=None, fill=None, anchor=None): self.d.text(self._p(*xy), s, font=font, fill=fill, anchor=anchor)
    def rounded_rectangle(self, box, radius=0, fill=None, outline=None, width=1): self.d.rounded_rectangle(self._b(box), radius * K, fill=fill, outline=outline, width=self._w(width))
    def rectangle(self, box, fill=None, outline=None, width=1): self.d.rectangle(self._b(box), fill=fill, outline=outline, width=self._w(width))
    def ellipse(self, box, fill=None, outline=None, width=1): self.d.ellipse(self._b(box), fill=fill, outline=outline, width=self._w(width))
    def pieslice(self, box, start, end, fill=None, outline=None, width=1): self.d.pieslice(self._b(box), start, end, fill=fill, outline=outline, width=self._w(width))
    def line(self, pts, fill=None, width=1): self.d.line([self._p(*p) for p in pts], fill=fill, width=self._w(width))
    def polygon(self, pts, fill=None, outline=None): self.d.polygon([self._p(*p) for p in pts], fill=fill, outline=outline)


def NI(w, h): return Image.new("RGBA", (max(1, int(round(w * K))), max(1, int(round(h * K)))), (0, 0, 0, 0))


def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0, absolute=False):
    if scale <= 0.01 or alpha <= 0.01: return
    if not absolute: cx = CX0 + (cx - CX0) * K; cy = CY0 + (cy - CY0) * K
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def pop(t, t0, dur=0.28): return ease_back((t - t0) / dur) if t >= t0 else 0.0
def fade(t, t0, dur=0.25): return min(1.0, max(0.0, (t - t0) / dur))


def pill(text, size=34, fill=(20, 24, 34), color=WHITE, pad=(24, 9), r=None, hl=(), hlc=SKY, outline=None, kind="m", glow=False):
    f = F(size, kind); words = text.split(" "); sp = f.getlength(" "); wl = [f.getlength(w) for w in words]; tw = int(sum(wl) + sp * (len(words) - 1)); a, d_ = f.getmetrics()
    px_, py_ = int(pad[0] * K), int(pad[1] * K); w_, h_ = tw + 2 * px_, a + d_ + 2 * py_; r = r or h_ // 2; m = int(12 * K)
    im = Image.new("RGBA", (w_ + 2 * m, h_ + 2 * m), (0, 0, 0, 0)); d = ImageDraw.Draw(im); ow = max(1, int(3 * K))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle([m, m, w_ + m - 1, h_ + m - 1], r, outline=SKY + (255,), width=max(2, int(4 * K))); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(7 * K)))
    d.rounded_rectangle([m, m, w_ + m - 1, h_ + m - 1], r, fill=fill + (255,), outline=(outline + (255,)) if outline else None, width=ow)
    x = m + px_
    for w, l in zip(words, wl):
        d.text((x, m + py_), w, font=f, fill=(hlc if w.strip(",.?!:") in hl else color) + (255,)); x += l + sp
    return im


def card(w, h, r=30, fill=CARD, outline=OUT, ow=3, glow=False):
    m = int(20 * K); wk, hk = int(w * K), int(h * K); im = Image.new("RGBA", (wk + 2 * m, hk + 2 * m), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle([m, m, wk + m - 1, hk + m - 1], int(r * K), outline=SKY + (255,), width=max(2, int(5 * K))); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(9 * K)))
    ImageDraw.Draw(im).rounded_rectangle([m, m, wk + m - 1, hk + m - 1], int(r * K), fill=fill + (255,), outline=outline + (255,), width=max(1, int(ow * K))); return im


def rounded(img, r):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255); o = img.convert("RGBA"); o.putalpha(m); return o


def enter(base, spr, cx, cy, t, t0, side=0, dur=0.32, rot=0):
    lt = t - t0
    if lt < 0: return
    e = ease_back(lt / dur) if lt < dur else 1.0; q = ease_out(min(1, lt / dur)); dx = side * (1 - q) * 360; dy = (1 - q) * (80 if side == 0 else 0)
    place(base, spr, cx + dx, cy + dy, 0.94 + 0.06 * e, min(1, q * 1.5), rot)


def txt(base, xy, s, size, fill=WHITE, kind="m", anchor="la", alpha=1.0):
    SD(base).text(xy, s, font=F(size, kind), fill=fill + (int(255 * alpha),), anchor=anchor)


def typed(s, t, a0, a1): n = int(len(s) * min(1, max(0, (t - a0) / max(0.1, a1 - a0)))); return s[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(s) else "")


def with_k1(fn):
    def wrap(*a, **k):
        global K
        k0 = K; K = 1.0
        try: return fn(*a, **k)
        finally: K = k0
    return wrap


# ---------- background / badge / caption (always K = 1) ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None, None]; x = np.linspace(-1, 1, W)[None, :, None]
    base = np.array(BG0, dtype=np.float32)[None, None, :] + 14 * (1 - y) * np.exp(-x ** 2 * 1.5)
    im = Image.fromarray(np.broadcast_to(np.clip(base, 0, 255).astype(np.uint8), (H, W, 3)).copy()).convert("RGBA"); d = ImageDraw.Draw(im)
    for gx in range(0, W, 96): d.line([(gx, 0), (gx, H)], fill=(14, 18, 27, 255), width=1)
    for gy in range(0, H, 96): d.line([(0, gy), (W, gy)], fill=(14, 18, 27, 255), width=1)
    return im
BG = make_bg()
CHAP = {"hook": None, "what": (1, "what it is"), "who": (2, "who gets it"), "switch": (3, "on / off"), "see": (4, "see and delete"), "never": (5, "never saved"),
        "private": (6, "private chats"), "projects": (7, "projects"), "caution": (8, "caution"), "cta": (9, "recap")}


@with_k1
def badge(base, sid, t):
    c = CHAP[sid]
    if not c: return
    sq = Image.new("RGBA", (54, 54), (0, 0, 0, 0)); d = ImageDraw.Draw(sq); d.rounded_rectangle([0, 0, 53, 53], 12, fill=SKY + (255,)); d.text((27, 27), str(c[0]), font=F(34, "b"), fill=INK + (255,), anchor="mm")
    place(base, sq, 86, 70, absolute=True); _pb = pill(c[1].upper(), 26, (20, 24, 34), WHITE, pad=(18, 6), outline=OUT, kind="p"); place(base, _pb, 86 + 36 + _pb.width / 2 + 2, 70, absolute=True)


def caption_chunks():
    out = []
    for sid in IDS:
        toks = WT[sid]["tokens"]; segs = []; cur = []
        for k, (tk, _) in enumerate(toks):
            cur.append(k)
            if re.search(r"[,।?!]$", tk): segs.append(cur); cur = []
        if cur: segs.append(cur)
        for sg in segs:
            n = len(sg); k = -(-n // 4); sizes = [n // k + (1 if j < n % k else 0) for j in range(k)]; i = 0
            for z in sizes: idx = sg[i:i + z]; out.append((SC[sid] + LEAD + toks[idx[0]][1], " ".join(toks[q][0] for q in idx))); i += z
    ends = [c[0] for c in out[1:]] + [TOTAL]
    return [(a, min(b, a + 2.2), txt_) for (a, txt_), b in zip(out, ends)]
CAPS = caption_chunks()
KEYW = {w.strip(",.?!:।") for w in ["Memory", "memory", "Pause", "Reset", "Manage", "Delete", "Incognito", "Settings", "toggle", "ID", "bank", "delete", "Projects", "project", "Topics", "plans", "Free,", "Pro,", "Max", "Ultra,", "ghost", "plus", "भूल", "नहीं", "हमेशा"]}
CAPDIR = HERE / "raw/caps"; CAPDIR.mkdir(parents=True, exist_ok=True)


def cap_path(s): return CAPDIR / (hashlib.md5(s.encode("utf-8")).hexdigest()[:16] + ".png")


def build_caps():
    """Hindi shaping: Pillow here has no raqm, so each caption chunk is rendered by Chromium (HarfBuzz) to a transparent PNG"""
    todo = [s for _, _, s in CAPS if not cap_path(s).exists()]
    if not todo: return
    from playwright.sync_api import sync_playwright
    font_url = (ROOT / "shared/fonts/Mukta-ExtraBold.ttf").as_uri()
    css = ("@font-face{font-family:MK;src:url('%s');font-weight:800}body{margin:0;background:transparent}"
           "#c{display:inline-block;font-family:MK,sans-serif;font-weight:800;font-size:40px;line-height:1.35;color:#fff;background:#080a10;border:3px solid #28344c;border-radius:999px;padding:6px 32px;white-space:nowrap}"
           ".k{color:#AC92FF}") % font_url
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1700, "height": 200}, device_scale_factor=1)
        for s in sorted(set(todo)):
            html = "".join(f'<span class="k">{w}</span> ' if w.strip(",.?!:।") in KEYW else f"{w} " for w in s.split(" ")).strip()
            html = html.replace("&", "&amp;") if "<" not in html else html
            pg.set_content(f"<style>{css}</style><div id='c'>{html}</div>"); pg.wait_for_timeout(60)
            pg.evaluate("document.fonts.ready"); pg.locator("#c").screenshot(path=str(cap_path(s)), omit_background=True)
        b.close()


_cap = {}
def caption(base, t):
    for a, b, s in CAPS:
        if a - 0.04 <= t < b:
            if s not in _cap: _cap[s] = Image.open(cap_path(s)).convert("RGBA")
            place(base, _cap[s], W / 2, 1010, 0.95 + 0.05 * ease_out((t - a) / 0.1), absolute=True); return


# ---------- photos ----------
PH = {k: Image.open(HERE / f"raw/photos/{k}.png").convert("RGB") for k in ("hook", "what", "clock")}
_cov = {}
def photo(key, w, h, lt, dur, z0=1.0, z1=1.15, r=30):
    src = PH[key]; wk, hk = int(w * K), int(h * K); ck = (key, wk, hk)
    if ck not in _cov: s = max(1.4 * wk / src.width, 1.4 * hk / src.height); _cov[ck] = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    cov = _cov[ck]; p = ease_io(min(1, max(0, lt / dur))); z = z0 + (z1 - z0) * p; ww, wh = wk * 1.2 / z, hk * 1.2 / z; cx, cy = cov.width / 2, cov.height / 2
    im = cov.crop((int(cx - ww / 2), int(cy - wh / 2), int(cx + ww / 2), int(cy + wh / 2))).resize((wk, hk), Image.BILINEAR)
    m = int(20 * K); out = card(w, h, r, fill=(0, 0, 0), outline=OUT); out.alpha_composite(rounded(im, int(r * K)), (m, m)); return out


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
    d = SD(base)
    for ck in clicks:
        if 0 <= t - ck <= 0.45: rr = 18 + 55 * (t - ck) / 0.45; d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=SKY + (255,), width=5)


@with_k1
def step(base, t, t0, text, y=110):
    if t >= t0: pp = pop(t, t0); place(base, pill(text, 34, SKY, INK, pad=(30, 9), kind="b"), W / 2, y, 0.7 + 0.3 * pp, min(1, pp * 1.4), absolute=True)


@with_k1
def illu(base, x=1730, y=1050): place(base, pill("Illustration, not a recording", 22, (20, 24, 34), DIM, pad=(14, 4), kind="p"), x, y, absolute=True)


# ---------- UI window ----------
WW, WH = 1500, 700
SIDE = ["General", "Privacy", "Your Claude", "Connectors", "Billing"]
def ui_window(sel_side=2, pane=None):
    im = card(WW, WH, 26, fill=(14, 17, 25), outline=OUT, ow=3); d = SD(im); ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + 330, oy + WH - 1], 26, fill=(10, 12, 18, 255)); d.rectangle([ox + 300, oy, ox + 330, oy + WH - 1], fill=(10, 12, 18, 255))
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([ox + 28 + 34 * i, oy + 26, ox + 46 + 34 * i, oy + 44], fill=c + (255,))
    d.text((ox + 34, oy + 80), "Settings", font=F(40, "b"), fill=WHITE + (255,))
    for i, s in enumerate(SIDE):
        y = oy + 150 + i * 78
        if i == sel_side: d.rounded_rectangle([ox + 20, y - 8, ox + 310, y + 52], 16, fill=(28, 48, 66, 255), outline=SKY + (255,), width=2)
        d.text((ox + 50, y), s, font=F(32, "p"), fill=(SKY if i == sel_side else (200, 208, 224)) + (255,))
    if pane: pane(im, ox + 330, oy, WW - 330, WH)
    else:
        d.text((ox + 380, oy + 70), SIDE[sel_side], font=F(46, "b"), fill=WHITE + (255,))
        for i in range(3): d.rounded_rectangle([ox + 380, oy + 170 + 110 * i, ox + WW - 80, oy + 260 + 110 * i], 20, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
    return im


def toggle(d, x, y, on, w=96, h=50):
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=(SKY if on else (70, 78, 98)) + (255,)); kx = x + w - h // 2 - 3 if on else x + h // 2 + 3
    d.ellipse([kx - h // 2 + 6, y + 6, kx + h // 2 - 6, y + h - 6], fill=(255, 255, 255, 255))


def pane_your_claude(on=True, manage_hot=False, menu=0.0, pick=None):
    def f(im, ox, oy, w, h):
        d = SD(im); d.text((ox + 50, oy + 70), "Your Claude", font=F(46, "b"), fill=WHITE + (255,))
        d.rounded_rectangle([ox + 50, oy + 170, ox + w - 50, oy + 280], 20, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
        d.text((ox + 80, oy + 200), "Generate memory from chats", font=F(34, "p"), fill=WHITE + (255,)); toggle(d, ox + w - 190, oy + 200, on)
        d.rounded_rectangle([ox + 50, oy + 310, ox + w - 50, oy + 420], 20, fill=(22, 27, 39, 255), outline=(SKY if manage_hot else OUT) + (255,), width=3 if manage_hot else 2)
        d.text((ox + 80, oy + 340), "Your memory", font=F(34, "p"), fill=WHITE + (255,)); d.rounded_rectangle([ox + w - 250, oy + 335, ox + w - 80, oy + 395], 16, fill=(40, 52, 76, 255)); d.text((ox + w - 165, oy + 365), "Manage", font=F(30, "b"), fill=SKY + (255,), anchor="mm")
        if menu > 0.02:
            mw, mh = 520, 250; m = card(mw, mh, 22, fill=(24, 30, 44), outline=SKY, ow=3); md = SD(m)
            md.rounded_rectangle([40, 44, mw, 44 + 90], 16, fill=((34, 60, 84, 255) if pick == "pause" else (30, 36, 52, 255)), outline=(SKY + (255,)) if pick == "pause" else None, width=2)
            md.text((70, 62), "Pause memory", font=F(34, "b"), fill=WHITE + (255,))
            md.rounded_rectangle([40, 150, mw, 150 + 90], 16, fill=((70, 28, 36, 255) if pick == "reset" else (30, 36, 52, 255)), outline=(RED + (255,)) if pick == "reset" else None, width=2)
            md.text((70, 168), "Reset memory", font=F(34, "b"), fill=RED + (255,))
            sc = 0.85 + 0.15 * min(1, menu); mm = m.resize((int(m.width * sc), int(m.height * sc))); im.alpha_composite(mm, (int((ox + w - 640) * K), int((oy + 420) * K)))
    return f


TOPICS = [("Role", "student, 3rd year"), ("Project", "thesis on solar energy"), ("Style", "short answers please"), ("College", "St. Mary's, Pune")]
def pane_topics(sel=None, edit=False, deleted=False, hot_del=False, t=0.0):
    def f(im, ox, oy, w, h):
        d = SD(im); d.text((ox + 50, oy + 60), "Your memory  ·  Topics", font=F(42, "b"), fill=WHITE + (255,))
        rows = [r for r in TOPICS if not (deleted and r[0] == "College")]
        for i, (a, b) in enumerate(rows):
            y = oy + 150 + i * 105; on = (sel == a)
            d.rounded_rectangle([ox + 50, y, ox + w - 50, y + 88], 18, fill=((28, 48, 66, 255) if on else (22, 27, 39, 255)), outline=(SKY if on else OUT) + (255,), width=3 if on else 2)
            val = (b + ("|" if (edit and a == "College" and int(t * 3) % 2 == 0) else "")) if (edit and a == "College") else b
            d.text((ox + 82, y + 24), a, font=F(32, "b"), fill=SKY + (255,)); d.text((ox + 300, y + 24), val, font=F(32, "p"), fill=((255, 255, 255) if (edit and a == "College") else (220, 226, 238)) + (255,))
            if edit and a == "College": d.rectangle([ox + 296, y + 70, ox + 296 + 420, y + 73], fill=SKY + (255,))
        if deleted: d.rounded_rectangle([ox + w - 470, oy + 560, ox + w - 70, oy + 625], 16, fill=(70, 28, 36, 255), outline=RED + (255,), width=2); d.text((ox + w - 270, oy + 592), "College deleted", font=F(30, "b"), fill=RED + (255,), anchor="mm")
        if sel == "College" and not deleted:
            d.rounded_rectangle([ox + w - 560, oy + 575, ox + w - 70, oy + 660], 16, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
            d.rounded_rectangle([ox + w - 540, oy + 590, ox + w - 400, oy + 645], 12, fill=((40, 52, 76, 255) if not edit else (34, 60, 84, 255)), outline=(SKY + (255,)) if edit else None, width=2); d.text((ox + w - 470, oy + 618), "Edit", font=F(28, "b"), fill=SKY + (255,), anchor="mm")
            d.rounded_rectangle([ox + w - 380, oy + 590, ox + w - 90, oy + 645], 12, fill=((90, 30, 40, 255) if hot_del else (60, 30, 36, 255))); d.text((ox + w - 235, oy + 618), "Delete", font=F(28, "b"), fill=RED + (255,), anchor="mm")
    return f


# ---------- Claude Code 04 (prompt caching): theme VIOLET on dark neon; scenes ----------
KB = {"hook_a": 1.05, "hook_b": 1.15, "what_a": 1.1, "what_b": 1.1, "prefix_a": 1.1, "prefix_b": 1.1, "breaks": 1.1, "demo": 1.08, "keep_a": 1.1, "keep_b": 1.15,
      "compact_a": 1.1, "compact_b": 1.1, "ttl": 1.1, "check_a": 1.1, "check_b": 1.1, "cta_a": 1.25, "cta_b": 1.0}
CHAP = {"hook": None, "what": (1, "what is caching"), "prefix": (2, "prefix rule"), "breaks": (3, "what breaks it"), "demo": (4, "terminal demo"), "keep": (5, "safe actions"),
        "compact": (6, "compact"), "ttl": (7, "cache lifetime"), "check": (8, "check it"), "cta": (9, "recap")}
KEYW = {w.strip(",.?!:।") for w in ["Claude", "Code", "cache", "Cache", "caching", "prompt", "prefix", "model", "compact", "usage", "TTL", "CLAUDE.md", "tokens", "read", "creation", "uncached",
                                    "exact", "fast", "mode", "promptCacheTtl", "hit", "rate", "ratio", "सस्ते", "महँगा", "धीमा", "नहीं", "सिर्फ", "CACHE", "एक", "घंटे", "पाँच", "मिनट"]}
MONO = "t"
GREEN = (110, 230, 150)


def termwin(w, h, title="Terminal"):
    im = card(w, h, 26, fill=(9, 12, 18), outline=OUT, ow=3); d = SD(im); ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + w - 1, oy + 64], 26, fill=(20, 25, 36, 255)); d.rectangle([ox, oy + 40, ox + w - 1, oy + 64], fill=(20, 25, 36, 255))
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([ox + 28 + 34 * i, oy + 22, ox + 46 + 34 * i, oy + 40], fill=c + (255,))
    d.text((ox + w / 2, oy + 32), title, font=F(26, "p"), fill=DIM + (255,), anchor="mm")
    return im, d, ox, oy


def tl(d, x, y, s, fill=(214, 222, 238), size=30): d.text((x, y), s, font=F(size, MONO), fill=fill + (255,))


def prompt_line(d, x, y, cmd, t, a0, a1, path=">"):
    tl(d, x, y, path + " ", GREEN); w0 = len(path + " ") * 18.0
    s = typed(cmd, t, a0, a1)
    if t >= a0: tl(d, x + w0, y, s, WHITE)
    elif int(t * 3) % 2 == 0: tl(d, x + w0, y, "|", WHITE)


def key_flash(base, t, t0, x, y, s="Enter"):
    if 0 <= t - t0 <= 0.7: place(base, pill(s, 26, (36, 44, 62), SKY, pad=(18, 5), kind="b", outline=SKY), x, y, 1.0, min(1, (0.7 - (t - t0)) * 4))


def fcard(name, sub, col=SKY, w=520, h=190, size=40):
    spr = card(w, h, 26, outline=col); d = SD(spr); d.text((40, 36), name, font=F(size, MONO), fill=col + (255,)); d.text((40, 36 + size + 26), sub, font=F(34, "p"), fill=(214, 222, 238, 255))
    return spr


def lbl(w, h, text, col, size=34, fill=CARD, tc=WHITE, kind="b", glow=False):
    spr = card(w, h, 22, fill=fill, outline=col, glow=glow); d = SD(spr); d.text((w / 2 + 20, h / 2 + 20), text, font=F(size, kind), fill=tc + (255,), anchor="mm"); return spr


def P(base, text, x, y, t, t0, size=36, fill=(30, 44, 62), color=WHITE, outline=OUT, kind="b", pad=(30, 10), hl=(), hlc=SKY, glow=False):
    if t >= t0: pp = pop(t, t0); place(base, pill(text, size, fill, color, pad=pad, kind=kind, outline=outline, hl=hl, hlc=hlc, glow=glow), x, y, 0.75 + 0.25 * pp, min(1, pp * 1.4))


def C(base, spr, x, y, t, t0, side=0): enter(base, spr, x, y, t, t0, side=side)


# ---------- hook ----------
def _hook_term(t, o):
    im, d, ox, oy = termwin(840, 600, "Claude Code")
    tl(d, ox + 30, oy + 110, "> ", GREEN); tl(d, ox + 70, oy + 110, typed("/model", t, T("hook", 6) - 0.3, T("hook", 7)), WHITE, 32)
    if t >= T("hook", 8): tl(d, ox + 30, oy + 190, "Model switched.", SKY, 30)
    if t >= T("hook", 11): tl(d, ox + 30, oy + 290, "... slow turn (cache rebuilt)", AMB, 30)
    if t >= T("hook", 17): tl(d, ox + 30, oy + 380, "usage went up a lot", RED, 30)
    return im


def b_hook_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("hook", 740, 600, lt, b["t1"] - o + 4), 490, 560, t, o + 0.02, side=-1)
    enter(base, _hook_term(t, o), 1400, 560, t, o + 0.2, side=1)
    place(base, pill("Suddenly slow after a model switch?", 38, (30, 44, 62), WHITE, pad=(30, 10), kind="b", outline=SKY, hl=("slow",)), 960, 190, 1.0, fade(t, o + 0.1, 0.3))


def b_hook_b(base, t, b):
    o = b["t0"]
    place(base, pill("prompt caching", 110, (20, 24, 34), SKY, pad=(70, 24), outline=SKY, kind="b", glow=True), W / 2, 400, 0.85 + 0.15 * pop(t, o), min(1, fade(t, o, 0.2)))
    for i, (s, tt) in enumerate([("what is the cache", T("hook", 32)), ("what breaks it", T("hook", 39)), ("check your hit rate", T("hook", 44))]):
        x = (420, 960, 1500)[i]
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 36, (20, 24, 34), WHITE, pad=(30, 10), outline=OUT, kind="b"), x, 640, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t < T("hook", 32): place(base, pill("why Claude Code feels faster (and cheaper)", 34, (30, 44, 62), WHITE, pad=(30, 10), kind="p", outline=OUT), 960, 640, 1.0, fade(t, o + 0.3))


# ---------- what ----------
def b_what_a(base, t, b):
    o = b["t0"]; lt = t - o
    P(base, "every message re-sends the whole context", 960, 200, t, o + 0.1, 40, hl=("re-sends",))
    enter(base, photo("what", 640, 470, lt, b["t1"] - o + 4), 480, 540, t, o + 0.05, side=-1)
    for i, (s, col, tk) in enumerate([("System prompt", SKY, 10), ("CLAUDE.md", AMB, 13), ("Old messages + results", GREEN, 15)]):
        C(base, lbl(760, 110, s, col, 38), 1330, 400 + 135 * i, t, T("what", tk) - 0.2, side=1)
    P(base, "mostly the SAME as last time", 1330, 830, t, T("what", 19) - 0.2, 36, SKY, INK, SKY, hl=())


def b_what_b(base, t, b):
    o = b["t0"]
    P(base, "with caching", 960, 200, t, o + 0.1, 46, SKY, INK, SKY)
    t_c = T("what", 39) - 0.2; cached = t >= t_c
    C(base, lbl(1400, 130, "old part:  cached rate (cheap)" if cached else "old part:  processed again = full price", GREEN if cached else RED, 40, glow=cached), 960, 430, t, o + 0.2)
    tn = T("what", 47) - 0.2
    if t >= tn: C(base, lbl(700, 120, "new part only: processed", AMB, 38), 1310, 640, t, tn)
    P(base, "automatic", 560, 830, t, T("what", 53) - 0.1, 40, (20, 24, 34), SKY, SKY)


# ---------- prefix ----------
def seg_row(items, w=1500, h=96):
    spr = NI(w, h); d = SD(spr); x = 0
    for (s, wi, col, ok) in items:
        d.rounded_rectangle([x, 0, x + wi - 8, h - 1], 18, fill=(26, 32, 46, 255) if ok else (70, 28, 36, 255), outline=col + (255,), width=3)
        d.text((x + (wi - 8) / 2, h / 2), s, font=F(30, "b"), fill=WHITE + (255,), anchor="mm"); x += wi
    return spr


def b_prefix_a(base, t, b):
    o = b["t0"]
    P(base, "match the START of the request, exactly", 960, 200, t, o + 0.1, 40, hl=("exact", "START"), hlc=SKY)
    if t >= T("prefix", 5) - 0.2:
        C(base, lbl(260, 70, "request 1", DIM, 30, kind="p"), 330, 400, t, T("prefix", 7) - 0.2)
        C(base, seg_row([("system", 260, SKY, True), ("CLAUDE.md", 300, AMB, True), ("chat", 480, GREEN, True)], 1040, 96), 1000, 400, t, T("prefix", 7) - 0.2)
    if t >= T("prefix", 11):
        C(base, lbl(260, 70, "request 2", DIM, 30, kind="p"), 330, 560, t, T("prefix", 11) - 0.2)
        C(base, seg_row([("system", 260, SKY, True), ("CLAUDE.md", 300, AMB, True), ("chat", 480, GREEN, True), ("new", 200, AMB, True)], 1240, 96), 1100, 560, t, T("prefix", 11) - 0.2)
    P(base, "same start = read from cache", 960, 740, t, T("prefix", 16), 36, SKY, INK, SKY)
    if t >= T("prefix", 18): P(base, "exact match", 960, 840, t, T("prefix", 18), 34, (20, 24, 34), WHITE, OUT, hl=("exact",))


def b_prefix_b(base, t, b):
    o = b["t0"]
    t_c = T("prefix", 25)
    place(base, pill("change at the start  =  everything after is rebuilt", 38, (70, 28, 36), RED, pad=(30, 10), kind="b", outline=RED), 960, 200, 1.0, fade(t, o + 0.1, 0.3))
    C(base, seg_row([("system", 300, RED, t < t_c), ("CLAUDE.md", 330, AMB, t < t_c), ("chat", 560, GREEN, t < t_c)], 1190, 96), 960, 330, t, o + 0.2)
    for i, (s, sub, col, tk) in enumerate([("1  System prompt", "rarely changes", SKY, 38), ("2  Project context", "CLAUDE.md, memory: set at session start", AMB, 44), ("3  Conversation", "changes every turn", GREEN, 51)]):
        spr = card(1500, 130, 22, outline=col); d = SD(spr); d.text((50, 85), s, font=F(38, "b"), fill=WHITE + (255,), anchor="lm"); d.text((1470, 85), sub, font=F(28, "p"), fill=col + (255,), anchor="rm")
        C(base, spr, 960, 500 + 150 * i, t, T("prefix", tk) - 0.3)


# ---------- breaks ----------
BR = [("/model switch", "each model has its own cache", SKY, 7), ("fast mode on / off", "separate cache per speed", AMB, 19), ("tool definitions", "MCP add / remove (no tool search)", GREEN, 31), ("many images", "oldest dropped in batches", (255, 130, 200), 44)]


def b_breaks(base, t, b):
    o = b["t0"]
    P(base, "what BREAKS the cache", 960, 190, t, o + 0.1, 44, (70, 28, 36), RED, RED, hl=("BREAKS",), hlc=RED)
    for i, (name, sub, col, tk) in enumerate(BR):
        x = 540 + 840 * (i % 2); y = 400 + 230 * (i // 2)
        C(base, fcard(name, sub, col, 740, 190, 40), x, y, t, T("breaks", tk) - 0.3)
    P(base, "next turn: slower + costlier, ONCE", 960, 800, t, T("breaks", 52) - 0.2, 38, AMB, INK, AMB)


# ---------- terminal demo ----------
def b_demo(base, t, b):
    o = b["t0"]; sid = "demo"
    t_p2 = T(sid, 17); t_p3 = T(sid, 41)
    page = 3 if t >= t_p3 else (2 if t >= t_p2 else 1)
    im, d, ox, oy = termwin(1560, 700, "Claude Code"); x0, y0 = ox + 50, oy + 110; lh = 52
    if page == 1:
        prompt_line(d, x0, y0, "/model", t, T(sid, 12) - 0.3, T(sid, 13) + 0.2)
        for i, (s, tt) in enumerate([("1. Default (recommended)", T(sid, 14)), ("2. Sonnet", T(sid, 14) + 0.2), ("3. Opus", T(sid, 14) + 0.4)]):
            if t >= tt:
                sel = (i == 1 and t >= T(sid, 16)); tl(d, x0 + 30, y0 + lh * 1.6 + i * lh, ("> " if sel else "  ") + s, SKY if sel else (214, 222, 238), 34)
        if t >= T(sid, 5): tl(d, x0, y0 + lh * 6.4, "# new session: choose model + effort first", DIM, 30)
        st = "STEP 1   pick the model FIRST, at session start"
        if t >= T(sid, 16): tl(d, x0, y0 + lh * 5.2, "Model set. Cache starts clean, nothing to lose.", GREEN, 30)
    elif page == 2:
        prompt_line(d, x0, y0, "/model", t, T(sid, 22) - 0.3, T(sid, 24))
        if t >= T(sid, 26):
            a = fade(t, T(sid, 26), 0.25); d.rounded_rectangle([x0, y0 + lh * 1.5, x0 + 1380, y0 + lh * 1.5 + 270], 20, fill=(50, 38, 20, int(255 * a)), outline=AMB + (int(255 * a),), width=3)
            tl(d, x0 + 30, y0 + lh * 1.5 + 30, "Cache is still warm.", tuple(int(c * a) for c in AMB), 34)
            if t >= T(sid, 31): tl(d, x0 + 30, y0 + lh * 1.5 + 90, "Switching model reads the whole chat uncached.", WHITE, 32)
            if t >= T(sid, 36): tl(d, x0 + 30, y0 + lh * 1.5 + 190, "Switch anyway?   [ Yes ]   [ No ]", SKY, 34)
        st = "STEP 2   switch later = Claude Code asks first"
    else:
        prompt_line(d, x0, y0, "/usage", t, T(sid, 42), T(sid, 44) + 0.3)
        if t >= T(sid, 46): tl(d, x0, y0 + lh * 1.6, "Session", WHITE, 36)
        if t >= T(sid, 48): tl(d, x0 + 30, y0 + lh * 2.6, "Prompt cache (main):  94% hit ratio  -  2 misses  -  warm", SKY, 30)
        if t >= T(sid, 55): d.line([(x0 + 30, y0 + lh * 3.4), (x0 + 1100, y0 + lh * 3.4)], fill=SKY + (255,), width=4)
        st = "STEP 3   /usage  >  Prompt cache line"
    enter(base, im, 960, 565, t, o, dur=0.3)
    step(base, t, T(sid, 5) - 0.3 if page == 1 else (t_p2 if page == 2 else t_p3) - 0.1, st)
    if page == 1: key_flash(base, t, T(sid, 13) + 0.5, 1560, 880)
    if page == 2: key_flash(base, t, T(sid, 24) + 0.3, 1560, 880)
    if page == 3: key_flash(base, t, T(sid, 44) + 0.5, 1560, 880)
    if page == 3 and t >= T(sid, 48): place(base, pill("example numbers", 24, (20, 24, 34), AMB, pad=(16, 4), kind="p", outline=AMB), 1500, 300)
    illu(base)


# ---------- keep ----------
KP = [("edit repo files", 10), ("permission mode", 13), ("output style", 16), ("skills + commands", 19), ("/recap", 22), ("/rewind", 25)]


def b_keep_a(base, t, b):
    o = b["t0"]
    P(base, "these KEEP the cache", 960, 200, t, o + 0.1, 46, GREEN, INK, GREEN)
    for i, (s, tk) in enumerate(KP):
        x = 480 + 480 * (i % 3); y = 440 + 210 * (i // 3)
        C(base, lbl(440, 150, "+ " + s, GREEN, 34, kind="b"), x, y, t, T("keep", tk) - 0.25)
    P(base, "cache safe", 960, 820, t, T("keep", 29) - 0.1, 36, (20, 24, 34), GREEN, GREEN)


def b_keep_b(base, t, b):
    o = b["t0"]
    P(base, "edit CLAUDE.md in the middle of a session", 960, 200, t, o + 0.1, 40, hl=("CLAUDE.md",))
    C(base, fcard("CLAUDE.md", "edited mid-session", AMB, 600, 200, 44), 520, 450, t, T("keep", 32) - 0.3, side=-1)
    P(base, "cache: kept", 1360, 380, t, T("keep", 41) - 0.1, 38, GREEN, INK, GREEN)
    P(base, "new text: NOT read yet", 1360, 520, t, T("keep", 47) - 0.1, 38, AMB, INK, AMB)
    if t >= T("keep", 55) - 0.2:
        P(base, "loads after", 480, 690, t, T("keep", 53) - 0.2, 34, (20, 24, 34), WHITE, OUT)
        for i, (s, tk) in enumerate([("/clear", 55), ("/compact", 56), ("restart", 58)]):
            P(base, s, 800 + 300 * i, 690, t, T("keep", tk) - 0.1, 40, (20, 24, 34), SKY, SKY, kind=MONO)


# ---------- compact ----------
def b_compact_a(base, t, b):
    o = b["t0"]
    P(base, "/compact  =  summary replaces history", 960, 200, t, o + 0.1, 40, hl=("summary",))
    spr = card(560, 460, 26, outline=OUT); d = SD(spr)
    for i in range(5): d.rounded_rectangle([40, 50 + 76 * i, 540, 50 + 76 * i + 56], 12, fill=(26, 32, 46, 255), outline=OUT + (255,), width=2)
    d.text((290, 20 + 2), "", font=F(10, "p"), fill=WHITE + (255,))
    C(base, spr, 520, 520, t, o + 0.2, side=-1)
    P(base, "old history", 520, 800, t, T("compact", 5) - 0.2, 32, (20, 24, 34), DIM, OUT, kind="p")
    if t >= T("compact", 9) - 0.2:
        SD(base).polygon([(800, 500), (900, 500), (900, 460), (990, 530), (900, 600), (900, 560), (800, 560)], fill=SKY + (255,))
        C(base, lbl(500, 150, "summary", SKY, 44, glow=True), 1380, 520, t, T("compact", 10) - 0.2, side=1)
    P(base, "cache warm  =  cheap", 960, 830, t, T("compact", 23) - 0.1, 40, GREEN, INK, GREEN)


def b_compact_b(base, t, b):
    o = b["t0"]; lt = t - o
    P(base, "long break  >  cache expired", 960, 200, t, o + 0.1, 40, hl=("expired",), hlc=AMB)
    enter(base, photo("clock", 600, 440, lt, b["t1"] - o + 4), 460, 520, t, o + 0.05, side=-1)
    P(base, "resume old session + /compact", 1330, 380, t, T("compact", 36) - 0.2, 34, (20, 24, 34), WHITE, OUT, kind="b")
    if t >= T("compact", 43) - 0.2: C(base, lbl(760, 130, "whole history read UNCACHED", RED, 36, fill=(70, 28, 36), tc=RED), 1330, 540, t, T("compact", 43) - 0.2)
    P(base, "most expensive case", 1330, 680, t, T("compact", 51) - 0.1, 36, RED, INK, RED)
    P(base, "better: /compact when a task is DONE", 960, 860, t, T("compact", 55) - 0.2, 38, GREEN, INK, GREEN)


# ---------- ttl ----------
def b_ttl(base, t, b):
    o = b["t0"]; lt = t - o
    P(base, "idle too long  >  cache expires", 960, 200, t, o + 0.1, 42, hl=("expires",), hlc=AMB)
    enter(base, photo("clock", 600, 520, lt, b["t1"] - o + 4), 460, 520, t, o + 0.05, side=-1)
    C(base, lbl(850, 130, "Claude subscription (in plan)", SKY, 36), 1330, 340, t, T("ttl", 15) - 0.2, side=1)
    if t >= T("ttl", 26) - 0.1: P(base, "1 hour", 1330, 490, t, T("ttl", 26) - 0.1, 70, SKY, INK, SKY)
    C(base, lbl(850, 130, "API key / credits", AMB, 36), 1330, 650, t, T("ttl", 32) - 0.2, side=1)
    if t >= T("ttl", 36) - 0.1: P(base, "5 minutes", 1330, 780, t, T("ttl", 36) - 0.1, 56, AMB, INK, AMB)
    P(base, "promptCacheTtl:  5m  or  1h", 960, 880, t, T("ttl", 42) - 0.1, 36, (20, 24, 34), SKY, SKY, kind=MONO)


# ---------- check ----------
def meter(label, col, frac, t, t0):
    spr = card(1300, 130, 26, outline=col); d = SD(spr); q = ease_out(min(1, max(0, (t - t0) / 0.9)))
    d.text((40, 40), label, font=F(30, MONO), fill=col + (255,)); d.rounded_rectangle([40, 90, 40 + 1200 * frac * q, 112], 8, fill=col + (255,)); return spr


def b_check_a(base, t, b):
    o = b["t0"]
    P(base, "2 numbers tell you", 960, 200, t, o + 0.1, 44)
    t1, t2 = T("check", 12), T("check", 21)
    C(base, meter("cache_read_input_tokens   (cheap)", GREEN, 0.85, t, t1), 960, 440, t, t1 - 0.3)
    C(base, meter("cache_creation_input_tokens   (new)", AMB, 0.25, t, t2), 960, 640, t, t2 - 0.3)
    P(base, "read HIGH + creation LOW  =  good", 960, 840, t, T("check", 28) - 0.2, 38, GREEN, INK, GREEN)


def b_check_b(base, t, b):
    o = b["t0"]
    C(base, lbl(1300, 140, "creation high every turn", RED, 42, fill=(70, 28, 36), tc=RED), 960, 340, t, T("check", 37) - 0.3)
    P(base, "something in the prefix keeps changing", 960, 500, t, T("check", 44) - 0.2, 38, (30, 44, 62), WHITE, RED, hl=("prefix",), hlc=SKY)
    P(base, "/usage  >  Prompt cache (main)", 960, 640, t, T("check", 8) + 0.0, 34, (20, 24, 34), SKY, SKY, kind=MONO) if False else None
    if t >= T("check", 51): P(base, "DISABLE_PROMPT_CACHING=1", 960, 700, t, T("check", 51) - 0.1, 44, (20, 24, 34), AMB, AMB, kind=MONO)
    if t >= T("check", 55): P(base, "only for debugging", 960, 810, t, T("check", 55) - 0.1, 36, AMB, INK, AMB)


# ---------- recap + CTA ----------
def b_cta_a(base, t, b):
    sid = "cta"
    place(base, pill("3 THINGS TO REMEMBER", 52, (20, 24, 34), WHITE, pad=(50, 14), kind="b", outline=SKY, glow=True), W / 2, 230, 1.0, fade(t, b["t0"], 0.25))
    for i, (n, s, tt) in enumerate([("1", "pick model + effort at the START", T(sid, 6)), ("2", "/compact after a task, not in the middle", T(sid, 15)), ("3", "/usage: watch your cache hit rate", T(sid, 27))]):
        y = 430 + 150 * i; enter(base, card(1300, 110, 26), 960, y, t, tt - 0.2, side=0)
        spr = NI(1300, 110); d = SD(spr); d.rounded_rectangle([24, 22, 90, 88], 14, fill=SKY + (255,)); d.text((57, 55), n, font=F(40, "b"), fill=INK + (255,), anchor="mm"); d.text((130, 55), s, font=F(36, "p"), fill=WHITE + (255,), anchor="lm"); enter(base, spr, 960, y, t, tt - 0.2)


def b_cta_b(base, t, b):
    sid = "cta"; t1, t2, t3 = T(sid, 41), T(sid, 43), T(sid, 45)
    place(base, pill("Was it useful?  Save it", 44, (30, 44, 62), WHITE, pad=(34, 12), kind="b", outline=SKY), 960, 195, 1.0, fade(t, b["t0"], 0.3))
    if t >= t1 - 0.2: place(base, pill("Comment", 60, (20, 24, 34), WHITE, pad=(40, 12), kind="b", outline=OUT), 960, 335, 0.8 + 0.2 * pop(t, t1 - 0.2), min(1, fade(t, t1 - 0.2, 0.2)))
    if t >= t2: place(base, pill("CACHE", 120, SKY, INK, pad=(60, 14), kind="b", glow=True), 960, 510, 0.8 + 0.2 * pop(t, t2), min(1, fade(t, t2, 0.2)))
    if t >= t3: place(base, pill("Follow DevRoboLab", 54, (20, 24, 34), SKY, pad=(40, 12), kind="b", outline=OUT), 960, 690, 0.8 + 0.2 * pop(t, t3), min(1, fade(t, t3, 0.2)))
    tt = t3 + 0.9
    if t >= tt:
        for i, s in enumerate(["Watch next", "Subscribe"]):
            enter(base, card(640, 150, 28, glow=True), 560 + 800 * i, 860, t, tt + 0.3 * i, side=0)
            spr = NI(640, 150); SD(spr).text((320, 75), s, font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 560 + 800 * i, 860, t, tt + 0.3 * i)


def _mk():
    B = []
    def add(i, sid, a, b): B.append(dict(id=i, sid=sid, t0=a, t1=b))
    add("hook_a", "hook", 0.0, T("hook", 23) - 0.2); add("hook_b", "hook", T("hook", 23) - 0.2, E("hook"))
    add("what_a", "what", S("what", 0), T("what", 27) - 0.2); add("what_b", "what", T("what", 27) - 0.2, E("what"))
    add("prefix_a", "prefix", S("prefix", 0), T("prefix", 21) - 0.2); add("prefix_b", "prefix", T("prefix", 21) - 0.2, E("prefix"))
    add("breaks", "breaks", S("breaks", 0), E("breaks")); add("demo", "demo", S("demo", 0), E("demo"))
    add("keep_a", "keep", S("keep", 0), T("keep", 32) - 0.2); add("keep_b", "keep", T("keep", 32) - 0.2, E("keep"))
    add("compact_a", "compact", S("compact", 0), T("compact", 31) - 0.2); add("compact_b", "compact", T("compact", 31) - 0.2, E("compact"))
    add("ttl", "ttl", S("ttl", 0), E("ttl"))
    add("check_a", "check", S("check", 0), T("check", 37) - 0.2); add("check_b", "check", T("check", 37) - 0.2, E("check"))
    add("cta_a", "cta", S("cta", 0), T("cta", 34) - 0.2); add("cta_b", "cta", T("cta", 34) - 0.2, TOTAL + 1)
    return B
B = _mk()

FN = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}
def frame(t):
    global K
    b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = BG.copy()
    K = KB.get(b["id"], 1.2)
    try: FN[b["id"]](base, t, b)
    finally: K = 1.0
    badge(base, b["sid"], t); caption(base, t)
    return np.array(base.convert("RGB"))


SR = 24000
def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def encode(frames_iter, n_frames, voice_wav, music, out, music_start=6, music_gain_db=-22, lufs=-12.8):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice_wav), "-ss", str(music_start), "-i", str(music)]
    fc = f"[2:a]volume={music_gain_db}dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I={lufs}:TP=-1.5:LRA=7[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, fr in enumerate(frames_iter):
        p.stdin.write(fr.tobytes())
        if i % 300 == 0: print(f"  frame {i}/{n_frames}", flush=True)
    p.stdin.close(); p.wait()


def main():
    print(f"total {TOTAL:.1f}s; beats:", [(x['id'], round(x['t0'], 1), round(x['t1'], 1)) for x in B])
    build_caps()
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/F_{tt:06.1f}.png")
        return
    if len(sys.argv) > 4 and sys.argv[1] == "range":   # python make_final.py range <t0> <t1> <out.mp4>: re-render ONLY this time range (video only) for tools/splice_video.py
        t0, t1, outp = float(sys.argv[2]), float(sys.argv[3]), Path(sys.argv[4]); n0, n1 = int(round(t0 * FPS)), int(round(t1 * FPS)); outp.parent.mkdir(parents=True, exist_ok=True)
        pr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(outp)], stdin=subprocess.PIPE)
        for i in range(n0, n1): pr.stdin.write(frame(i / FPS).tobytes())
        pr.stdin.close(); pr.wait(); print("range rendered", t0, t1, outp); return
    build_audio(HERE / "audio/voice.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / deck["music"]["file"], HERE / "output/long.mp4", music_start=deck["music"]["start"], music_gain_db=-22)


main()
