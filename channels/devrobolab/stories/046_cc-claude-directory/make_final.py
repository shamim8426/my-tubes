"""Claude Code 03 (.claude directory) LONG video build (adapted from 044 make_final.py), 16:9 1920x1080.
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
SKY = (80, 224, 170); WHITE = (255, 255, 255); RED = (255, 96, 106); AMB = (255, 190, 80); DIM = (150, 160, 182)
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
           ".k{color:#50E0AA}") % font_url
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
PH = {k: Image.open(HERE / f"raw/photos/{k}.png").convert("RGB") for k in ("hook", "team", "home", "shield")}
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


# ---------- Claude Code 03 (.claude directory): theme MINT on dark neon; scenes ----------
KB = {"hook_a": 1.0, "hook_b": 1.2, "what_a": 1.12, "what_b": 1.12, "two_a": 1.2, "demo": 1.08, "choose": 1.2, "extras": 1.12, "mine_a": 1.1, "mine_b": 1.25,
      "data_a": 1.05, "data_b": 1.1, "purge_a": 1.15, "purge_b": 1.25, "cta_a": 1.3, "cta_b": 1.0}
CHAP = {"hook": None, "what": (1, "two places"), "two": (2, "two key files"), "demo": (3, "terminal demo"), "choose": (4, "which file"), "extras": (5, "optional extras"),
        "mine": (6, "private + org"), "data": (7, "app data"), "purge": (8, "clean up"), "cta": (9, "recap")}
KEYW = {w.strip(",.?!:।") for w in ["Claude", "Code", ".claude", "CLAUDE.md", "settings.json", "settings.local.json", ".mcp.json", "CLAUDE.local.md", "AGENTS.md", "tests", "transcripts",
                                    "plain", "text", "encrypted", "purge", "dry-run", "delete", "folder", "files", "skills", "agents", "rules", "output-styles", "team", "home", "सिर्फ", "कभी", "मत",
                                    "तीस", "cleanupPeriodDays", "hooks", "permissions", "DIRECTORY", "secrets", "managed"]}
MONO = "t"
GREEN = (110, 230, 150)


def bubble(w, h, text, side="user", size=34):
    im = NI(w + 8, h + 8); d = SD(im)
    d.rounded_rectangle([4, 4, w + 3, h + 3], 26, fill=((30, 60, 56, 255) if side == "user" else (26, 31, 45, 255)), outline=(SKY if side == "user" else OUT) + (255,), width=2)
    d.text((34, h // 2 + 4), text, font=F(size, "p"), fill=WHITE + (255,), anchor="lm"); return im


def termwin(w, h, title="Terminal"):
    im = card(w, h, 26, fill=(9, 12, 18), outline=OUT, ow=3); d = SD(im); ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + w - 1, oy + 64], 26, fill=(20, 25, 36, 255)); d.rectangle([ox, oy + 40, ox + w - 1, oy + 64], fill=(20, 25, 36, 255))
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([ox + 28 + 34 * i, oy + 22, ox + 46 + 34 * i, oy + 40], fill=c + (255,))
    d.text((ox + w / 2, oy + 32), title, font=F(26, "p"), fill=DIM + (255,), anchor="mm")
    return im, d, ox, oy


def tl(d, x, y, s, fill=(214, 222, 238), size=30): d.text((x, y), s, font=F(size, MONO), fill=fill + (255,))


def prompt_line(d, x, y, cmd, t, a0, a1, path="my-project"):
    tl(d, x, y, path + " $ ", GREEN); w0 = len(path + " $ ") * 18.0
    s = typed(cmd, t, a0, a1)
    if t >= a0: tl(d, x + w0, y, s, WHITE)
    elif int(t * 3) % 2 == 0: tl(d, x + w0, y, "|", WHITE)


def key_flash(base, t, t0, x, y, s="Enter"):
    if 0 <= t - t0 <= 0.7: place(base, pill(s, 26, (36, 44, 62), SKY, pad=(18, 5), kind="b", outline=SKY), x, y, 1.0, min(1, (0.7 - (t - t0)) * 4))


def fcard(name, sub, col=SKY, w=520, h=190, size=40):
    spr = card(w, h, 26, outline=col); d = SD(spr); d.text((40, 36), name, font=F(size, MONO), fill=col + (255,)); d.text((40, 36 + size + 26), sub, font=F(34, "p"), fill=(214, 222, 238, 255))
    return spr


# ---------- hook ----------
def b_hook_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("hook", 700, 480, lt, b["t1"] - o + 4), 470, 520, t, o + 0.02, side=-1)
    im, d, ox, oy = termwin(860, 480, "Claude Code"); enter(base, im, 1400, 520, t, o + 0.2, side=1)
    tl(d, ox + 30, oy + 100, "> ", GREEN); t_a = T("hook", 3); t_b = T("hook", 11)
    tl(d, ox + 66, oy + 100, typed("Always run tests first", t, o + 0.5, t_b), WHITE, 28)
    if t >= T("hook", 12): tl(d, ox + 30, oy + 160, "Got it.", SKY, 28)
    if t >= T("hook", 12) + 0.3: pass
    t_n = T("hook", 13)
    if t >= t_n:
        d.line([(ox + 30, oy + 235), (ox + 830, oy + 235)], fill=OUT + (255,), width=2); tl(d, ox + 30, oy + 255, "-- next session --", DIM, 24)
    if t >= T("hook", 16): tl(d, ox + 30, oy + 320, "How do I run the tests?", AMB, 28)
    # redraw sprite content: window was already placed, so re-place with content when it changes
    base2 = None


def _hook_term(t, o):
    im, d, ox, oy = termwin(880, 600, "Claude Code")
    tl(d, ox + 30, oy + 110, "> ", GREEN); t_b = T("hook", 11)
    tl(d, ox + 70, oy + 110, typed("Always run tests first", t, o + 0.5, t_b), WHITE, 32)
    if t >= T("hook", 12): tl(d, ox + 30, oy + 190, "Got it.", SKY, 32)
    if t >= T("hook", 13): d.line([(ox + 30, oy + 290), (ox + 850, oy + 290)], fill=OUT + (255,), width=2); tl(d, ox + 30, oy + 320, "-- next session --", DIM, 26)
    if t >= T("hook", 16): tl(d, ox + 30, oy + 410, "How do I run the tests?", AMB, 32)
    return im


def b_hook_a(base, t, b):  # noqa: F811
    o = b["t0"]; lt = t - o
    enter(base, photo("hook", 780, 600, lt, b["t1"] - o + 4), 450, 560, t, o + 0.02, side=-1)
    enter(base, _hook_term(t, o), 1410, 560, t, o + 0.2, side=1)
    place(base, pill("Claude Code forgets?", 36, (30, 44, 62), WHITE, pad=(30, 10), kind="b", outline=SKY, hl=("forgets?",)), 960, 190, 1.0, fade(t, o + 0.1, 0.3))


def b_hook_b(base, t, b):
    o = b["t0"]
    place(base, pill(".claude", 120, (20, 24, 34), SKY, pad=(70, 24), outline=SKY, kind=MONO if False else "b", glow=True), W / 2, 400, 0.85 + 0.15 * pop(t, o), min(1, fade(t, o, 0.2)))
    for i, (s, tt) in enumerate([("which files", T("hook", 39)), ("what to change", T("hook", 44)), ("what to watch out for", T("hook", 51))]):
        x = (420, 960, 1500)[i]
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 36, (20, 24, 34), WHITE, pad=(30, 10), outline=OUT, kind="b"), x, 640, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t < T("hook", 39): place(base, pill("the folder where Claude Code keeps its rules", 34, (30, 44, 62), WHITE, pad=(30, 10), kind="p", outline=OUT), 960, 640, 1.0, fade(t, o + 0.3))


# ---------- what: two places ----------
TREE_P = [("my-project/", 0, WHITE), ("CLAUDE.md", 1, SKY), (".claude/", 1, WHITE), ("settings.json", 2, SKY), ("skills/", 2, (200, 208, 224)), ("agents/", 2, (200, 208, 224)), ("rules/", 2, (200, 208, 224))]
TREE_H = [("home folder/", 0, WHITE), (".claude/", 1, WHITE), ("settings.json", 2, SKY), ("skills/", 2, (200, 208, 224)), ("agents/", 2, (200, 208, 224)), ("projects/", 2, (200, 208, 224))]


def tree_card(w, h, tree, t, t0, times, col):
    im, d, ox, oy = termwin(w, h, "files")
    for i, ((s, lv, c), tt) in enumerate(zip(tree, times)):
        if t >= tt:
            a = fade(t, tt, 0.2); y = oy + 100 + i * 56; x = ox + 40 + lv * 46
            tl(d, x, y, ("+- " if lv else "") + s, tuple(int(v * a) for v in c), 32)
    return im


def b_what_a(base, t, b):
    o = b["t0"]; lt = t - o
    place(base, pill("1   THIS PROJECT", 38, SKY, INK, pad=(32, 10), kind="b"), 500, 205, 1.0, fade(t, o, 0.25))
    enter(base, photo("team", 700, 460, lt, b["t1"] - o + 4), 500, 490, t, o + 0.05, side=-1)
    tt = [T("what", 17), T("what", 19), T("what", 19) + 0.3, T("what", 19) + 0.6, T("what", 19) + 0.9, T("what", 19) + 1.2, T("what", 19) + 1.5]
    enter(base, tree_card(640, 560, TREE_P, t, o, tt, SKY), 1400, 530, t, o + 0.15, side=1)
    if t >= T("what", 23): pp = pop(t, T("what", 23)); place(base, pill("git commit  >  whole team gets it", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=SKY, hl=("team",)), 560, 790, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= T("what", 14) - 0.2 and t < T("what", 23): place(base, pill("pehli jagah: project ka .claude", 30, (20, 24, 34), DIM, pad=(24, 8), kind="p", outline=OUT), 560, 790, 1.0, fade(t, T("what", 14) - 0.2))


def b_what_b(base, t, b):
    o = b["t0"]; lt = t - o
    place(base, pill("2   YOUR HOME FOLDER", 38, AMB, INK, pad=(32, 10), kind="b"), 500, 205, 1.0, fade(t, o, 0.25))
    enter(base, photo("home", 700, 460, lt, b["t1"] - o + 4), 500, 490, t, o + 0.05, side=-1)
    tt = [T("what", 38), T("what", 41), T("what", 41) + 0.3, T("what", 41) + 0.6, T("what", 41) + 0.9, T("what", 41) + 1.2]
    enter(base, tree_card(640, 560, TREE_H, t, o, tt, AMB), 1400, 530, t, o + 0.15, side=1)
    if t >= T("what", 43): pp = pop(t, T("what", 43)); place(base, pill("personal  -  all your projects", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=AMB), 560, 790, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= T("what", 55): pp = pop(t, T("what", 55)); place(base, pill("Windows:  %USERPROFILE%\\.claude", 30, (20, 24, 34), WHITE, pad=(26, 9), kind="p", outline=SKY), 1400, 850, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- two key files ----------
def b_two_a(base, t, b):
    o = b["t0"]
    place(base, pill("Most people edit only 2 files", 44, (30, 44, 62), WHITE, pad=(36, 12), kind="b", outline=SKY, hl=("2",)), W / 2, 200, 1.0, fade(t, o, 0.3))
    for (name, lines, ta, x, col, tl_) in [("CLAUDE.md", ["instructions for Claude", "loaded every session"], 0.6, 520, SKY, T("two", 17)),
                                           ("settings.json", ["permissions  -  hooks", "env variables  -  model"], 0.9, 1400, AMB, T("two", 31))]:
        enter(base, fcard(name, "", col, 600, 360, 50), x, 520, t, o + ta - 0.3, side=0)
        spr = NI(600, 360); d = SD(spr)
        for j, s in enumerate(lines):
            if t >= tl_ + 0.5 * j: a = fade(t, tl_ + 0.5 * j); d.rounded_rectangle([40, 130 + 90 * j, 560, 130 + 90 * j + 70], 16, fill=(26, 32, 46, int(255 * a)), outline=col + (int(255 * a),), width=2); d.text((300, 165 + 90 * j), s, font=F(30, "p"), fill=WHITE + (int(255 * a),), anchor="mm")
        enter(base, spr, x, 520, t, o + ta - 0.3)
    if False: place(base, pill("1   CLAUDE.md      2   settings.json", 40, (20, 24, 34), DIM, pad=(34, 12), kind="p", outline=OUT), W / 2, 520, 1.0, fade(t, o + 0.2))
    if t >= T("two", 41): pp = pop(t, T("two", 41)); place(base, pill("the rest is optional", 40, SKY, INK, pad=(34, 10), kind="b"), W / 2, 820, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- terminal demo ----------
def b_demo(base, t, b):
    o = b["t0"]; sid = "demo"
    t_p1 = T(sid, 5); t_p2 = T(sid, 20); t_p3 = T(sid, 35)
    page = 3 if t >= t_p3 else (2 if t >= t_p2 else 1)
    title = "CLAUDE.md" if page == 3 else "Terminal"
    im, d, ox, oy = termwin(1560, 700, title); x0, y0 = ox + 50, oy + 110; lh = 52
    if page == 1:
        a0, a1 = T(sid, 8), T(sid, 10) + 0.4
        prompt_line(d, x0, y0, "ls .claude", t, a0, a1)
        names = [("settings.json", T(sid, 12)), ("settings.local.json", T(sid, 12) + 0.25), ("rules/", T(sid, 13)), ("skills/", T(sid, 14)), ("agents/", T(sid, 16)), ("CLAUDE.md", T(sid, 16) + 0.3)]
        for i, (s, tt) in enumerate(names):
            if t >= tt:
                a = fade(t, tt, 0.2); col = SKY if s in ("settings.json", "CLAUDE.md") else (214, 222, 238); tl(d, x0 + (i % 2) * 520, y0 + lh * 1.6 + (i // 2) * lh, s, tuple(int(c * a) for c in col), 34)
        st = "STEP 1   list the folder:  ls .claude"
    elif page == 2:
        a0, a1 = T(sid, 21), T(sid, 22) + 0.5
        prompt_line(d, x0, y0, "cat .claude/settings.json", t, a0, a1)
        js = [(T(sid, 24), '{', WHITE), (T(sid, 25), '  "permissions": {', WHITE), (T(sid, 28), '    "allow": [', WHITE), (T(sid, 30), '      "Bash(npm test)"', SKY), (T(sid, 33), '    ]', WHITE), (T(sid, 33) + 0.2, '  }', WHITE), (T(sid, 33) + 0.4, '}', WHITE)]
        for i, (tt, s, c) in enumerate(js):
            if t >= tt: tl(d, x0, y0 + lh * 1.5 + i * 46, s, c, 32)
        st = "STEP 2   open settings.json  >  permissions"
    else:
        tl(d, x0, y0 - 6, "CLAUDE.md", SKY, 30); d.line([(x0, y0 + 40), (x0 + 1000, y0 + 40)], fill=OUT + (255,), width=2)
        if t >= T(sid, 36): tl(d, x0, y0 + 70, "# My project", (214, 222, 238), 34)
        a0, a1 = T(sid, 40), T(sid, 48)
        if t >= a0: tl(d, x0, y0 + 70 + lh * 1.3, typed("Run tests with:  npm test", t, a0, a1), WHITE, 34)
        st = "STEP 3   write it in plain words in CLAUDE.md"
    enter(base, im, 960, 565, t, o, dur=0.3)
    step(base, t, t_p1 - 0.3, st)
    if page == 1: key_flash(base, t, T(sid, 10) + 0.5, 1560, 880)
    if page == 2: key_flash(base, t, T(sid, 22) + 0.6, 1560, 880)
    if t >= T(sid, 51): pp = pop(t, T(sid, 51)); place(base, pill("next session: Claude reads it", 34, SKY, INK, pad=(30, 10), kind="b"), 960, 800, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if page == 2 and t >= T(sid, 30): place(base, pill("example", 24, (20, 24, 34), AMB, pad=(16, 4), kind="p", outline=AMB), 1590, 300)
    illu(base)


# ---------- choose the file ----------
ROWS = [("Project context + rules", "CLAUDE.md", SKY, 9, 19), ("Allow / block tools, hooks, env", "settings.json", AMB, 20, 36), ("Share MCP servers with the team", ".mcp.json", GREEN, 37, 46), ("Personal overrides, out of git", "settings.local.json", (255, 130, 200), 47, 57)]


def b_choose(base, t, b):
    o = b["t0"]; sid = "choose"
    place(base, pill("What do you want to do?   >   which file?", 40, (30, 44, 62), WHITE, pad=(36, 12), kind="b", outline=OUT), W / 2, 210, 1.0, fade(t, o, 0.3))
    for i, (s, fn, col, ta, tb) in enumerate(ROWS):
        y = 340 + 150 * i; tt = T(sid, ta); act = (t >= tt and (i == 3 or t < T(sid, ROWS[i + 1][3])))
        enter(base, card(1500, 110, 26, outline=col if t >= tt else OUT, glow=act), 960, y, t, o + 0.1 + 0.12 * i, side=0)
        spr = NI(1500, 110); d = SD(spr); d.text((50, 55), s, font=F(38, "p"), fill=(WHITE if t >= tt - 0.2 else DIM) + (255,), anchor="lm")
        enter(base, spr, 960, y, t, o + 0.1 + 0.12 * i)
        tf = T(sid, tb)
        if t >= tf - 0.1: pp = pop(t, tf - 0.1); place(base, pill(fn, 38, col, INK, pad=(28, 8), kind=MONO), 1330, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- extras ----------
EX = [("skills/", "SKILL.md  >  run with /name", 6, SKY), ("agents/", "subagent: own prompt + tools", 24, AMB), ("rules/", "topic rules, can be path-gated", 39, GREEN), ("output-styles/", "changes how Claude answers", 60, (255, 130, 200))]


def b_extras(base, t, b):
    o = b["t0"]
    place(base, pill("optional extras", 44, (30, 44, 62), WHITE, pad=(36, 12), kind="b", outline=OUT), W / 2, 200, 1.0, fade(t, o, 0.3))
    for i, (name, sub, tk, col) in enumerate(EX):
        x = 560 + 800 * (i % 2); y = 440 + 330 * (i // 2); tt = T("extras", tk) - 0.3
        enter(base, fcard(name, sub, col, 640, 270, 46), x, y, t, tt, side=0)


# ---------- mine ----------
def b_mine_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("home", 700, 470, lt, b["t1"] - o + 4), 470, 520, t, o + 0.02, side=-1)
    place(base, fcard("CLAUDE.local.md", "your private notes", AMB, 700, 190, 40), 1400, 360, 1.0, fade(t, T("mine", 5) - 0.3))
    for i, (s, tt) in enumerate([("you create it yourself", T("mine", 9)), ("add it to .gitignore", T("mine", 15))]):
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 34, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=AMB), 1400, 540 + 100 * i, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t < T("mine", 5) - 0.3: place(base, pill("your own preferences", 40, (30, 44, 62), WHITE, pad=(32, 10), kind="b", outline=AMB), 1400, 360, 1.0, fade(t, o + 0.1))


def b_mine_b(base, t, b):
    o = b["t0"]
    place(base, fcard("AGENTS.md", "already in your repo?", SKY, 560, 190, 40), 560, 400, 1.0, fade(t, T("mine", 27) - 0.3))
    if t >= T("mine", 33) - 0.2: pp = pop(t, T("mine", 33) - 0.2); place(base, pill("=", 70, (20, 24, 34), WHITE, pad=(30, 4), kind="b"), 960, 400, 1.0, min(1, pp * 1.4)); place(base, fcard("CLAUDE.md", "can be read instead", SKY, 560, 190, 40), 1360, 400, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    if t < T("mine", 27) - 0.3: place(base, pill("already have AGENTS.md?", 40, (30, 44, 62), WHITE, pad=(34, 12), kind="b", outline=SKY), 960, 400, 1.0, fade(t, o))
    tt = T("mine", 42)
    if t >= tt:
        pp = pop(t, tt); place(base, pill("ORGANIZATION  managed settings", 36, RED, INK, pad=(32, 10), kind="b"), 960, 620, 0.8 + 0.2 * pp, min(1, pp * 1.4))
        if t >= tt + 0.7: place(base, pill("your settings.json", 34, (30, 44, 62), WHITE, pad=(30, 10), kind=MONO, outline=OUT), 960, 740, 1.0, fade(t, tt + 0.7))
        if t >= tt + 0.7: SD(base).polygon([(930, 670), (990, 670), (960, 700)], fill=RED + (255,))
        if t >= T("mine", 49): place(base, pill("managed settings win", 34, (70, 28, 36), RED, pad=(28, 9), kind="p", outline=RED), 960, 815, 1.0, fade(t, T("mine", 49)))


# ---------- app data ----------
def b_data_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("shield", 700, 440, lt, b["t1"] - o + 4), 470, 500, t, o + 0.02, side=-1)
    im, d, ox, oy = termwin(760, 440, "inside .claude")
    tl(d, ox + 40, oy + 100, "projects/", WHITE, 30)
    for i, (s, tt) in enumerate([("session.jsonl   transcript", T("data", 17)), ("history.jsonl   prompts", T("data", 19))]):
        if t >= tt: a = fade(t, tt, 0.2); tl(d, ox + 80, oy + 160 + 60 * i, s, tuple(int(c * a) for c in SKY), 28)
    enter(base, im, 1400, 500, t, o + 0.2, side=1)
    place(base, pill("Claude Code also WRITES data here", 36, (30, 44, 62), WHITE, pad=(30, 10), kind="b", outline=AMB, hl=("WRITES",), hlc=AMB), 960, 190, 1.0, fade(t, o, 0.3))
    if t >= T("data", 23): pp = pop(t, T("data", 23)); place(base, pill("PLAIN TEXT  -  not encrypted", 40, RED, INK, pad=(34, 10), kind="b"), 960, 790, 0.75 + 0.25 * pp, min(1, pp * 1.4))


def b_data_b(base, t, b):
    o = b["t0"]
    place(base, pill("a tool reads your .env file...", 38, (30, 44, 62), WHITE, pad=(32, 10), kind="b", outline=OUT), W / 2, 190, 1.0, fade(t, o, 0.3))
    ta = T("data", 34) - 0.3
    enter(base, fcard(".env", "API_KEY=sk-demo-1234", AMB, 560, 190, 44), 520, 420, t, o + 0.1, side=-1)
    if t >= T("data", 36): a = ease_out((t - T("data", 36)) / 0.5); SD(base).line([(820, 420), (820 + 240 * a, 420)], fill=RED + (255,), width=6); SD(base).polygon([(1060, 420), (1030, 402), (1030, 438)], fill=RED + (int(255 * a),))
    if t >= T("data", 38) - 0.2: enter(base, fcard("transcript", "API_KEY=sk-demo-1234", RED, 560, 190, 44), 1400, 420, t, T("data", 38) - 0.2, side=1)
    if t >= T("data", 41): pp = pop(t, T("data", 41)); place(base, pill("the value is saved in the transcript", 34, (70, 28, 36), RED, pad=(28, 10), kind="p", outline=RED), 960, 590, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    tt = T("data", 50)
    if t >= tt - 0.3:
        enter(base, card(560, 220, 28, glow=True), 520, 790, t, tt - 0.3, side=0)
        spr = NI(560, 220); d = SD(spr); d.text((280, 85), "30", font=F(110, "b"), fill=SKY + (255,), anchor="mm"); d.text((280, 175), "days  -  auto delete (default)", font=F(28, "p"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 520, 790, t, tt - 0.3)
    if t >= T("data", 59): pp = pop(t, T("data", 59)); place(base, pill("change it:  cleanupPeriodDays", 34, (20, 24, 34), SKY, pad=(28, 10), kind=MONO, outline=SKY), 1360, 790, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- purge ----------
def b_purge_a(base, t, b):
    o = b["t0"]; sid = "purge"
    im, d, ox, oy = termwin(1560, 640, "Terminal"); x0, y0 = ox + 40, oy + 100; lh = 44
    prompt_line(d, x0, y0, "claude purge ~/work/my-repo --dry-run", t, T(sid, 4), T(sid, 9), "~")
    L = [(T(sid, 13), "Purge plan for /home/user/work/my-repo:", WHITE), (T(sid, 19), "  dir:    projects/...  transcripts and memory/", SKY),
         (T(sid, 22), "  config: project entry in ~/.claude.json", SKY), (T(sid, 25), "  filter: history.jsonl  12 prompt(s)", SKY), (T(sid, 26) + 0.6, "Dry run: 3 item(s) would be deleted.", AMB)]
    for i, (tt, s, c) in enumerate(L):
        if t >= tt: tl(d, x0, y0 + 80 + i * lh * 1.25, s, c, 28)
    enter(base, im, 960, 560, t, o, dur=0.3)
    step(base, t, T(sid, 3), "STEP   claude purge <project> --dry-run  =  only a preview")
    key_flash(base, t, T(sid, 9) + 0.6, 1560, 880)
    if t >= T(sid, 27): pass
    illu(base)


def b_purge_b(base, t, b):
    o = b["t0"]; sid = "purge"
    place(base, pill("NEVER DELETE", 64, RED, INK, pad=(50, 14), kind="b", glow=False), W / 2, 230, 0.85 + 0.15 * pop(t, o), fade(t, o, 0.2))
    for i, (s, why, tt) in enumerate([("~/.claude.json", "account", T(sid, 29)), ("~/.claude/settings.json", "preferences", T(sid, 30)), ("~/.claude/plugins/", "plugins", T(sid, 32))]):
        y = 420 + 140 * i; enter(base, card(1300, 110, 26, outline=RED), 960, y, t, tt - 0.3, side=0)
        spr = NI(1300, 110); d = SD(spr); d.text((50, 55), s, font=F(42, MONO), fill=WHITE + (255,), anchor="lm")
        if t >= T(sid, 40 + i): d.text((1250, 55), "= " + why, font=F(36, "b"), fill=AMB + (255,), anchor="rm")
        enter(base, spr, 960, y, t, tt - 0.3)
    if t < T(sid, 29) - 0.3: place(base, pill("careful with these three", 40, (30, 44, 62), WHITE, pad=(34, 12), kind="p", outline=RED), 960, 520, 1.0, fade(t, o))


# ---------- recap + CTA ----------
def b_cta_a(base, t, b):
    sid = "cta"
    place(base, pill("3 THINGS TO REMEMBER", 52, (20, 24, 34), WHITE, pad=(50, 14), kind="b", outline=SKY, glow=True), W / 2, 230, 1.0, fade(t, b["t0"], 0.25))
    for i, (n, s, tt) in enumerate([("1", "project .claude = team  |  home .claude = you", T(sid, 5)), ("2", "most work: CLAUDE.md + settings.json", T(sid, 19)), ("3", "transcripts are plain text: guard secrets", T(sid, 29))]):
        y = 430 + 150 * i; enter(base, card(1300, 110, 26), 960, y, t, tt - 0.2, side=0)
        spr = NI(1300, 110); d = SD(spr); d.rounded_rectangle([24, 22, 90, 88], 14, fill=SKY + (255,)); d.text((57, 55), n, font=F(40, "b"), fill=INK + (255,), anchor="mm"); d.text((130, 55), s, font=F(36, "p"), fill=WHITE + (255,), anchor="lm"); enter(base, spr, 960, y, t, tt - 0.2)


def b_cta_b(base, t, b):
    sid = "cta"; t1, t2, t3 = T(sid, 45), T(sid, 47), T(sid, 49)
    place(base, pill("Was it useful?  Send it to a friend", 44, (30, 44, 62), WHITE, pad=(34, 12), kind="b", outline=SKY), 960, 195, 1.0, fade(t, b["t0"], 0.3))
    if t >= t1 - 0.2: place(base, pill("Comment", 60, (20, 24, 34), WHITE, pad=(40, 12), kind="b", outline=OUT), 960, 335, 0.8 + 0.2 * pop(t, t1 - 0.2), min(1, fade(t, t1 - 0.2, 0.2)))
    if t >= t2: place(base, pill("DIRECTORY", 120, SKY, INK, pad=(60, 14), kind="b", glow=True), 960, 510, 0.8 + 0.2 * pop(t, t2), min(1, fade(t, t2, 0.2)))
    if t >= t3: place(base, pill("Follow DevRoboLab", 54, (20, 24, 34), SKY, pad=(40, 12), kind="b", outline=OUT), 960, 690, 0.8 + 0.2 * pop(t, t3), min(1, fade(t, t3, 0.2)))
    tt = t3 + 0.9
    if t >= tt:
        for i, s in enumerate(["Watch next", "Subscribe"]):
            enter(base, card(640, 150, 28, glow=True), 560 + 800 * i, 860, t, tt + 0.3 * i, side=0)
            spr = NI(640, 150); SD(spr).text((320, 75), s, font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 560 + 800 * i, 860, t, tt + 0.3 * i)


def _mk():
    B = []
    def add(i, sid, a, b): B.append(dict(id=i, sid=sid, t0=a, t1=b))
    add("hook_a", "hook", 0.0, T("hook", 26) - 0.2); add("hook_b", "hook", T("hook", 26) - 0.2, E("hook"))
    add("what_a", "what", S("what", 0), T("what", 35) - 0.2); add("what_b", "what", T("what", 35) - 0.2, E("what"))
    add("two_a", "two", S("two", 0), E("two")); add("demo", "demo", S("demo", 0), E("demo")); add("choose", "choose", S("choose", 0), E("choose")); add("extras", "extras", S("extras", 0), E("extras"))
    add("mine_a", "mine", S("mine", 0), T("mine", 21) - 0.2); add("mine_b", "mine", T("mine", 21) - 0.2, E("mine"))
    add("data_a", "data", S("data", 0), T("data", 30) - 0.2); add("data_b", "data", T("data", 30) - 0.2, E("data"))
    add("purge_a", "purge", S("purge", 0), T("purge", 28) - 0.2); add("purge_b", "purge", T("purge", 28) - 0.2, E("purge"))
    add("cta_a", "cta", S("cta", 0), T("cta", 38) - 0.2); add("cta_b", "cta", T("cta", 38) - 0.2, TOTAL + 1)
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
