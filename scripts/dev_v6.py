"""DevRoboLab STYLE v6 helpers: show the source page inside a device (phone / TV / paper sheet / chat window) instead of a scrolling full-page card.
Used by stories/04x make.py:  import dev_v6; dev_v6.install(globals())  -> replaces ui_beat(), frame() and blur_push() of that make.py.
Rules: one crop of the highlighted block (never a scrolling page), different device from the previous UI beat, no blur-push, no progress bar."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageChops


def install(g):
    chip, place, pop, font = g["chip"], g["place"], g["pop"], g["font"]
    ease_out, ease_back, ease_io = g["ease_out"], g["ease_back"], g["ease_io"]
    W, H, YEL, INK, RED, BLUE = g["W"], g["H"], g["YEL"], g["INK"], g["RED"], g["BLUE"]
    ARTS, CW, rect, persp = g["ARTS"], g["CW"], g["rect"], g["persp"]

    def bg_soft():
        im = Image.new("RGB", (W, H), (252, 250, 244)); d = ImageDraw.Draw(im)
        for y in range(H):
            k = y / H; d.line([(0, y), (W, y)], fill=(int(252 - 14 * k), int(250 - 18 * k), int(244 - 40 * k)))
        d.ellipse([-300, 380, 700, 1380], fill=(255, 236, 140)); im = im.filter(ImageFilter.GaussianBlur(120))
        return im.convert("RGBA")
    BGS = bg_soft()

    PLAIN = Image.open(g["HERE"] / "raw/article_plain.png").convert("RGB"); LINES = g["RJ"].get("lines", {})
    PLAIN = PLAIN.resize((CW, int(PLAIN.height * CW / PLAIN.width)), Image.LANCZOS)

    def crop(key, w, h, zoom=1.0, drift=0.0, hp=1.0):
        """w x h window of the PLAIN article around highlight `key`; marker highlight wipes in line by line, progress hp 0..1"""
        rx, ry, rw, rh = rect(key); s = (w * zoom) / CW
        a = PLAIN.resize((int(PLAIN.width * s), int(PLAIN.height * s)), Image.LANCZOS); k = 2 * g["SCALE"] * s   # css px -> a px
        lines = LINES.get(key) or []
        if lines and hp > 0:
            tot = sum(l[2] for l in lines); done = 0.0; layer = Image.new("RGB", a.size, (255, 255, 255)); d = ImageDraw.Draw(layer)
            for x, y, lw, lh in lines:
                f0 = done / tot; f1 = (done + lw) / tot; done += lw; q = min(1, max(0, (hp - f0) / (f1 - f0)))
                if q > 0: d.rounded_rectangle([x * k - 4, y * k - 2, (x + lw * q) * k + 4, (y + lh) * k + 2], 5, fill=(255, 214, 10))
            a = ImageChops.multiply(a, layer)
        cy = (ry + rh / 2) * s + drift; y0 = int(max(0, min(a.height - h, cy - h * 0.45))); x0 = int(max(0, (a.width - w) / 2))
        return a.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")

    def rounded(img, r):
        m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
        o = img.copy(); o.putalpha(m); return o

    def shadow(w, h, r, off=40, blur=30, a=110):
        sh = Image.new("RGBA", (w + 160, h + 160), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([80, 80 + off, 80 + w, 80 + h + off], r, fill=(0, 0, 0, a))
        return sh.filter(ImageFilter.GaussianBlur(blur))

    def phone(key, lt, p, hp):
        w, h = 640, 940; scr = rounded(crop(key, w - 56, h - 120, 1.0, 0, hp), 38)
        dev = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(dev)
        d.rounded_rectangle([0, 0, w - 1, h - 1], 74, fill=(18, 18, 22, 255)); d.rounded_rectangle([6, 6, w - 7, h - 7], 68, outline=(70, 70, 80, 255), width=3)
        dev.alpha_composite(scr, (28, 76)); d.rounded_rectangle([w // 2 - 70, 24, w // 2 + 70, 52], 14, fill=(0, 0, 0, 255))
        return dev, -4

    def paper(key, lt, p, hp):
        w, h = 900, 470; pg = crop(key, w - 60, h - 70, 1.0, 0, hp)
        sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(sheet)
        d.rounded_rectangle([0, 0, w - 1, h - 1], 14, fill=(255, 254, 250, 255), outline=(220, 214, 196, 255), width=3); sheet.alpha_composite(pg, (30, 40))
        for x in (70, w - 220):
            tape = Image.new("RGBA", (150, 52), (255, 214, 10, 190)); sheet.alpha_composite(tape.rotate(6 if x < 300 else -6, expand=True), (x, -18))
        return sheet, 3

    def tv(key, lt, p, hp):
        w, h = 980, 640; scr = rounded(crop(key, w - 60, h - 190, 1.0, 0, hp), 14)
        dev = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(dev)
        d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(18, 18, 22, 255)); d.rectangle([30, 22, w - 31, 92], fill=RED + (255,))
        d.text((54, 28), "AI NEWS  •  LIVE", font=font(52), fill=(255, 255, 255, 255)); dev.alpha_composite(scr, (30, 108))
        d.rectangle([30, h - 74, w - 31, h - 24], fill=YEL + (255,)); d.text((50, h - 76), "DevRoboLab  •  Claude update", font=font(44), fill=INK + (255,))
        return dev, 0

    DEV = {"phone": phone, "paper": paper, "tv": tv}

    def ui_beat(base, t, b):
        base.alpha_composite(BGS)
        lt = t - b["t0"]; p = min(1, max(0, lt / max(0.1, b["t1"] - b["t0"])))
        key = [k for ts, k in b["keys"] if t >= ts][-1] if b.get("keys") else b["key"]
        ks = b.get("keys") or [(b["t0"], b["key"])]; i = [n for n, (ts, k) in enumerate(ks) if t >= ts][-1]
        seg0 = max(ks[i][0], b["t0"]); seg1 = ks[i + 1][0] if i + 1 < len(ks) else b["t1"]
        h0 = seg0 + 0.55; h1 = min(seg1 - 0.35, h0 + 2.6); hp = min(1, max(0, (t - h0) / max(0.3, h1 - h0)))
        hp = hp * hp * (3 - 2 * hp)   # ease in-out so the marker speeds up and settles like a hand
        dev, rot = DEV[b.get("dev", "phone")](key, lt, p, hp)
        e = ease_back(lt / 0.4) if lt < 0.4 else 1.0; sc = 0.92 + 0.08 * e
        cy = 790 + (1 - ease_out(min(1, lt / 0.4))) * 70 + 10 * math.sin(lt * 1.6)
        w, h = dev.size; place(base, shadow(w, h, 60), 540, cy, sc, min(1, e), rot)
        place(base, dev, 540, cy, sc, min(1, e), rot)
        if b.get("dev") == "paper" and b.get("stamp"):
            place(base, chip(b["stamp"], 78, (255, 255, 255), RED, pad=(26, 6), r=14).rotate(-12, expand=True, resample=Image.BICUBIC), 800, cy - 290, pop(t, b["t0"] + 0.4))
        place(base, chip(g["SRC"], 34, (40, 44, 58), (235, 235, 240), pad=(26, 8), r=18), 540, 1275)

    def frame(t):
        B = g["B"]; b = next((x for x in B if x["t0"] <= t < x["t1"]), B[-1]); base = Image.new("RGBA", (W, H))
        if b["k"] == "ui": ui_beat(base, t, b); g["overlays"](base, t, b)
        elif b["k"] == "robot": g["robot_beat"](base, t, b)
        elif b["k"] == "num": g["num_beat"](base, t, b)
        else: g["cta_beat"](base, t, b)
        g["caption"](base, t, b["k"])
        return g["np"].array(base.convert("RGB"))

    g["ui_beat"], g["frame"] = ui_beat, frame
