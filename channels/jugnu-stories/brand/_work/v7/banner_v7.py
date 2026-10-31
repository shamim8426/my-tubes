"""Banner v7 (₹0, local): same Gemini scene, kids removed from the background and placed in front of a big bold
title; the dot of the "i" is a glowing firefly. Two samples: A = "Jugnu Stories", B = "JUGNU STORIES"."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"D:\Story-Channel")
V6 = ROOT / "channels/jugnu-stories/brand/_work/v6"
OUT = ROOT / "channels/jugnu-stories/brand/_work/v7"
OUT.mkdir(exist_ok=True)
W, H = 2560, 1440
SAFE = ((W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2)
art = Image.open(V6 / "art_2560.png").convert("RGB")
S, OX, OY = 0.68, 170, 83

# ---------- 1. kids mask (GrabCut on the full-res art) ----------
KX0, KY0, KX1, KY1 = 440, 600, 1680, 1250
img = cv2.cvtColor(np.asarray(art), cv2.COLOR_RGB2BGR)
sub = img[KY0:KY1, KX0:KX1].copy()
hsv = cv2.cvtColor(sub, cv2.COLOR_BGR2HSV)
b, g, r = [sub[..., i].astype(int) for i in range(3)]
mask = np.full(sub.shape[:2], cv2.GC_PR_FGD, np.uint8)
sky = (b > r + 25) & (b > g + 10) & (hsv[..., 2] < 140)
grass = (g > r + 30) & (g > b + 20)
mask[sky | grass] = cv2.GC_PR_BGD
mask[:6, :] = mask[-6:, :] = cv2.GC_BGD
mask[:, :6] = mask[:, -6:] = cv2.GC_BGD
bgd, fgd = np.zeros((1, 65)), np.zeros((1, 65))
cv2.grabCut(sub, mask, None, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)
fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
fg[0:135, 300:385] = 0                     # Tinku's firefly (redrawn below); his head ends left of x=300
fg[0:260, 150:520][sky[0:260, 150:520]] = 0  # leftover dark sky near the firefly
for foot in ((slice(430, 560), slice(540, 690)), (slice(470, 600), slice(415, 525))):  # Bholu's two feet
    fg[foot] = np.where(grass[foot] | sky[foot], fg[foot], 255)
n, lab, st, _ = cv2.connectedComponentsWithStats(fg, 8)
keep = np.zeros_like(fg)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] > 400:
        keep[lab == i] = 255
keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
keep = cv2.GaussianBlur(keep, (3, 3), 0)
kids = Image.fromarray(cv2.cvtColor(sub, cv2.COLOR_BGR2RGB))
kids_a = Image.fromarray(keep)
kids_a.save(OUT / "_kids_mask_final.png")

# ---------- 2. clean background (same layout as v6, kids area refilled with clean sky/grass columns) ----------
c = art.crop((0, 0, 1950, 1440)).resize((round(1950 * S), round(1440 * S)), Image.LANCZOS)
ca = np.asarray(c).copy()
cw, ch = c.size
strip = ca[:, round(1665 * S):round(1945 * S)].copy()


def tile(width, x_start_flip=True):
    out, flip = [], x_start_flip
    while sum(t.shape[1] for t in out) < width:
        out.append(strip[:, ::-1] if flip else strip)
        flip = not flip
    return np.concatenate(out, axis=1)[:, :width]


# erase the kids inside the scaled crop: rows of the kids box, columns of the kids box, feathered edges
ex0, ex1 = round((KX0 - 10) * S), round((KX1 + 10) * S)
ey0, ey1 = round((KY0 - 30) * S), round((KY1 + 10) * S)
fill = tile(ex1 - ex0)[ey0:ey1].astype(np.float32)
a = np.ones((ey1 - ey0, ex1 - ex0), np.float32)
fx = 40
a[:, :fx] *= np.linspace(0, 1, fx)[None, :]
a[:, -fx:] *= np.linspace(1, 0, fx)[None, :]
a[:fx, :] *= np.linspace(0, 1, fx)[:, None]
reg = ca[ey0:ey1, ex0:ex1].astype(np.float32)
ca[ey0:ey1, ex0:ex1] = (reg * (1 - a[..., None]) + fill * a[..., None]).astype(np.uint8)

L = np.zeros((ch, W, 3), np.uint8)
L[:, OX:OX + cw] = ca
L[:, :OX] = ca[:, :OX][:, ::-1]
L[:, OX + cw:] = tile(W - OX - cw)
tw = round(470 * S)
tree = ca[:, :tw][:, ::-1].astype(np.float32)
al = np.ones(tw, np.float32)
ramp = np.linspace(0, 1, 230)
al[:230] = ramp * ramp * (3 - 2 * ramp)  # wide smooth blend, no visible edge
seg = L[:, W - tw:].astype(np.float32)
L[:, W - tw:] = (seg * (1 - al[None, :, None]) + tree * al[None, :, None]).astype(np.uint8)
top = L[:OY][::-1]
need = H - OY - ch
gr = np.asarray(art.crop((0, 1235, W, 1440)).resize((W, need + 60), Image.LANCZOS)).astype(np.float32)
mid = np.concatenate([top, L]).astype(np.float32)
bl = np.linspace(0, 1, 60)[:, None, None]
mid[-60:] = mid[-60:] * (1 - bl) + gr[:60] * bl
bg = Image.fromarray(np.concatenate([mid, gr[60:]]).clip(0, 255).astype(np.uint8)).convert("RGBA")
rng = np.random.default_rng(7)
ff = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(ff)
for _ in range(46):
    x, y, rr = int(rng.uniform(300, 2500)), int(rng.uniform(120, 880)), rng.uniform(2.5, 5)
    fd.ellipse((x - rr * 3, y - rr * 3, x + rr * 3, y + rr * 3), fill=(220, 255, 120, 40))
    fd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(250, 255, 170, 230))
bg = Image.alpha_composite(bg, ff.filter(ImageFilter.GaussianBlur(1.6)))
bg.convert("RGB").save(OUT / "_bg_clean.png")


# ---------- 3. firefly sprite (glowing dot with tiny wings) ----------
def firefly(d):
    """d = glowing belly diameter in px; RGBA sprite with a soft glow, no hard edges."""
    k = 4
    size = int(d * 9) * k
    cx = cy = size // 2
    glow = Image.new("RGBA", (size, size), (200, 255, 90, 0))
    gd = ImageDraw.Draw(glow)
    for rad, a_ in ((d * 1.9, 70), (d * 1.3, 110), (d * 0.9, 170)):
        rr = rad * k
        gd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(200, 255, 90, a_))
    im = glow.filter(ImageFilter.GaussianBlur(d * 0.55 * k))
    dr = ImageDraw.Draw(im)
    rb = d * 0.5 * k
    w = d * 0.62 * k
    for sx in (-1, 1):  # translucent wings, angled up and out
        x0 = cx + sx * rb * 0.35
        box = (x0 - w * 0.45 + sx * w * 0.45, cy - rb * 2.6, x0 + w * 0.45 + sx * w * 0.45, cy - rb * 1.0)
        dr.ellipse(box, fill=(235, 245, 255, 120), outline=(255, 255, 255, 190), width=k)
    dr.ellipse((cx - rb * 0.7, cy - rb * 2.0, cx + rb * 0.7, cy - rb * 0.4), fill=(70, 40, 25, 255))
    dr.ellipse((cx - rb * 0.45, cy - rb * 2.5, cx + rb * 0.45, cy - rb * 1.65), fill=(205, 85, 40, 255))
    dr.ellipse((cx - rb, cy - rb, cx + rb, cy + rb), fill=(248, 255, 160, 255))
    dr.ellipse((cx - rb * 0.55, cy - rb * 0.55, cx + rb * 0.55, cy + rb * 0.55), fill=(255, 255, 232, 255))
    return im.resize((size // k, size // k), Image.LANCZOS)


def paste_center(base, sprite, x, y):
    base.alpha_composite(sprite, (int(x - sprite.width / 2), int(y - sprite.height / 2)))


def font(px):
    f = ImageFont.truetype(str(ROOT / "shared/fonts/Baloo2-Variable.ttf"), px)
    f.set_variation_by_name(b"ExtraBold")
    return f


# ---------- 4. kids, one by one (columns in the full-res kids box), spread under the title ----------
KS = 0.62
SPLITS = [(0, 312), (312, 693), (693, 898), (898, KX1 - KX0)]   # Tinku, Bholu+ball, Ira, Titli
sprites = []
for x0, x1 in SPLITS:
    a_ = np.asarray(kids_a)[:, x0:x1].copy()
    # keep only real parts: big components (child, Bholu's ball); drop blossom bits and dark sky leftovers
    sub_rgb = np.asarray(kids)[:, x0:x1].astype(int)
    darkblue = (sub_rgb[..., 2] > sub_rgb[..., 0] + 15) & (sub_rgb.max(axis=2) < 90)
    a_[darkblue & (np.arange(a_.shape[0])[:, None] < 260)] = 0
    pinkish = (sub_rgb[..., 0] > 120) & (sub_rgb[..., 2] > sub_rgb[..., 1] + 30)   # lavender blossom, not skin
    yy, xx = np.arange(a_.shape[0])[:, None], np.arange(a_.shape[1])[None, :] + x0
    purple = ((sub_rgb[..., 2] > sub_rgb[..., 1] + 25) & (sub_rgb[..., 0] > 80)) | (sub_rgb[..., 2] > sub_rgb[..., 0] + 40)
    a_[purple & (((yy < 230) & (xx < 120)) | ((yy < 130) & (xx < 240)))] = 0   # blossom bits around Tinku's hair
    skin = (sub_rgb[..., 0] > 150) & (sub_rgb[..., 0] > sub_rgb[..., 1]) & (sub_rgb[..., 1] > sub_rgb[..., 2])
    head = ((xx - 124) / 106.0) ** 2 + ((yy - 152) / 110.0) ** 2 <= 1.0
    if x0 == 0:
        a_[~(head | skin) & (yy < 200) & (xx > 150)] = 0  # sky/glow patch around the old firefly
    if x0 == 312:
        a_[((yy < 140) & (xx < 392)) | ((yy < 100) & (xx < 412))] = 0  # glow of Tinku's firefly left of Bholu's hair
    if x0 == 0:  # Tinku's raised hand + index finger: keep skin and its dark outline (sky is bluer)
        hand = (yy >= 136) & (yy < 265) & (xx >= 250) & (xx < 310)
        outline = (sub_rgb[..., 0] >= sub_rgb[..., 2]) & (sub_rgb.max(axis=2) < 130)
        near_skin = cv2.dilate((hand & skin).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        a_[hand & (skin | (outline & near_skin))] = 255
        a_[hand & ~(skin | (outline & near_skin))] = 0
    nn, lb, stt, _ = cv2.connectedComponentsWithStats((a_ > 20).astype(np.uint8), 8)
    big = [i for i in range(1, nn) if stt[i, cv2.CC_STAT_AREA] > 3500]
    a_ = np.where(np.isin(lb, big), a_, 0).astype(np.uint8)
    kids_a.paste(Image.fromarray(a_), (x0, 0))
    ys, xs = np.where(a_ > 20)
    bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    rgb = kids.crop((x0 + bx0, by0, x0 + bx1, by1))
    al_ = kids_a.crop((x0 + bx0, by0, x0 + bx1, by1))
    w_, h_ = round(rgb.width * KS), round(rgb.height * KS)
    sp = rgb.resize((w_, h_), Image.LANCZOS).convert("RGBA")
    sp.putalpha(al_.resize((w_, h_), Image.LANCZOS))
    sprites.append((sp, x0 + bx0, by0))
FINGER = (282, 165)   # Tinku's fingertip in full-res kids-box coords


def build(text, dot_char, name, title_px, baseline, centers, ground=926):
    im = bg.copy()
    f = font(title_px)
    d = ImageDraw.Draw(im)
    tl = d.textlength(text, font=f)
    x0 = W / 2 - tl / 2
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((x0, baseline), text, font=f, anchor="ls", fill=(255, 190, 50, 200))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(im)
    d.text((x0, baseline + 8), text, font=f, anchor="ls", fill=(10, 12, 40, 200))
    d.text((x0, baseline), text, font=f, anchor="ls", fill=(255, 214, 72, 255),
           stroke_width=max(6, title_px // 22), stroke_fill=(18, 20, 60, 255))
    bbox = d.textbbox((x0, baseline), text, font=f, anchor="ls")
    idx = text.index(dot_char)
    xi = x0 + d.textlength(text[:idx], font=f)
    if dot_char == "ı":   # where the real dot of "i" would be
        bi = d.textbbox((xi, baseline), "i", font=f, anchor="ls")
        bd = d.textbbox((xi, baseline), "ı", font=f, anchor="ls")
        dot_x, dot_y = (bi[0] + bi[2]) / 2, (bi[1] + bd[1]) / 2 + title_px * 0.08
        size = (bd[1] - bi[1]) * 1.25
    else:                 # capital I: the firefly floats just above it
        bi = d.textbbox((xi, baseline), dot_char, font=f, anchor="ls")
        size = title_px * 0.22
        dot_x, dot_y = (bi[0] + bi[2]) / 2, bi[1] - size * 1.1
    spr = firefly(size)
    top_px = int(dot_y - spr.height / 2) + int(np.argmax((np.asarray(spr)[..., 3] > 120).any(axis=1)))
    print('i-dot firefly top', top_px, 'safe top', SAFE[1])
    paste_center(im, spr, dot_x, dot_y)
    # kids stand fully BELOW the letters (like Titli): one common scale so no head touches the title
    tm = Image.new("L", (W, H), 0)
    ImageDraw.Draw(tm).text((x0, baseline), text, font=f, anchor="ls", fill=255,
                             stroke_width=max(6, title_px // 22), stroke_fill=255)
    tma = np.asarray(tm) > 40
    rows = np.arange(H)[:, None]
    bottom = np.where(tma, rows, -1).max(axis=0)          # lowest text pixel per column (-1 = none)
    gap = 14
    r = 1.0
    for _ in range(3):
        lim = []
        for (sp, bx, by), cx in zip(sprites, centers):
            w_, h_ = sp.width * r, sp.height * r
            tb = bottom[int(cx - w_ / 2):int(cx + w_ / 2)].max()
            if tb >= 0:
                lim.append((ground - tb - gap) / sp.height)
        r = min([1.0] + lim)
    tinku_pos = None
    for (sp, bx, by), cx in zip(sprites, centers):
        sp2 = sp.resize((round(sp.width * r), round(sp.height * r)), Image.LANCZOS)
        px, py = int(cx - sp2.width / 2), ground - sp2.height
        im.alpha_composite(sp2, (px, py))
        if tinku_pos is None:
            tinku_pos = (px + (FINGER[0] - bx) * KS * r, py + (FINGER[1] - by) * KS * r)
    print("kids scale", round(KS * r, 3))
    # Tinku's own firefly from the art (clear and a bit bigger), soft round edge so it sits on the sky
    fc, fr = (305, 88), 58
    patch = kids.crop((fc[0] - fr, fc[1] - fr, fc[0] + fr, fc[1] + fr)).convert('RGBA')
    yy_, xx_ = np.mgrid[0:2 * fr, 0:2 * fr]
    rad = np.hypot(xx_ - fr, yy_ - fr)
    patch.putalpha(Image.fromarray((np.clip((fr - rad) / (fr * 0.45), 0, 1) * 255).astype(np.uint8)))
    k = KS * r * 1.35
    patch = patch.resize((round(patch.width * k), round(patch.height * k)), Image.LANCZOS)
    tx, ty = tinku_pos[0] - (FINGER[0] - fc[0]) * KS * r, tinku_pos[1] - (FINGER[1] - fc[1]) * KS * r + 4
    paste_center(im, patch, tx, ty)
    out = im.convert("RGB")
    out.save(OUT / f"{name}_2560.png")
    return out, bbox


samples = [
    ("Jugnu Storıes", "ı", "banner_A", 150, 640, (860, 1120, 1420, 1660)),
    ("JUGNU STORIES", "I", "banner_B", 180, 692, (690, 1020, 1430, 1830)),
]
prev = []
for text, dot, name, px, base, centers in samples:
    out, bb = build(text, dot, name, px, base, centers)
    print(name, "title bbox", bb)
    g = out.copy()
    gd = ImageDraw.Draw(g)
    gd.rectangle(SAFE, outline=(255, 60, 60), width=6)
    gd.rectangle((0, SAFE[1], W - 1, SAFE[3]), outline=(60, 200, 255), width=4)
    prev.append((name, g, out))
F = ImageFont.truetype(str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf"), 26)
sheet = Image.new("RGB", (1280, (40 + 720 + 40 + 246 + 20) * len(prev)), "white")
q = ImageDraw.Draw(sheet)
y = 0
for name, g, out in prev:
    q.text((8, y + 6), f"{name}: poora (TV) - laal = mobile, neela = desktop", fill="black", font=F)
    sheet.paste(g.resize((1280, 720), Image.LANCZOS), (0, y + 40))
    y += 760
    q.text((8, y + 6), "mobile", fill="black", font=F)
    sheet.paste(out.crop(SAFE).resize((900, 246), Image.LANCZOS), (0, y + 40))
    y += 306
sheet.save(OUT / "_preview.jpg", quality=88)

# zoom crops for checking
z=Image.open(OUT/"banner_A_2560.png").crop((560,480,2000,940)); z.resize((1200,383)).save(OUT/"_zoom_A.jpg",quality=90)
Image.open(OUT/"banner_A_2560.png").crop((SAFE[0],SAFE[1],SAFE[2],SAFE[3])).save(OUT/"_mobile_A.jpg",quality=90)
Image.open(OUT/"banner_A_2560.png").crop((760,640,980,935)).resize((440,590)).save(OUT/"_zoom_tinku.jpg",quality=92)
