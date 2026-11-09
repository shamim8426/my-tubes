r"""047 news Short: Gemini Omni 1.2 Flash. Engine = stories/047_clean_proto (make_clean3), style techniques from a study on 2026-11-08 (principles only):
pale grey rotating ghost bursts, popping pill stack, phone mock-up, count-up numbers, CAPS name chip. Accent colour this video: violet.
User 2026-11-08: real pictures (official-page screenshots with the key phrase marked, money shown, the edit really shown), fewer and slower changes,
no "comment" ask in the ending. Run (ffmpeg on PATH):  python make_omni.py [frames t1 t2 ...]"""
import os, sys, base64, io
from pathlib import Path
ODIR = Path(__file__).parent
os.environ["CLEAN_SRC"] = str(ODIR)
sys.path.insert(0, str(ODIR.parent / "047_clean_proto"))
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_clean as mc
import make_clean2 as m2
import make_clean3 as m3
from make_clean3 import *
HERE = ODIR

VIO = "#7B5CF6"
m2.ORANGE = VIO; m3.ORANGE = VIO
RAW = ODIR / "raw"
MUKTA = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf")


def gburst(size, rot, col="#dcdce0"):
    import math
    c = size / 2; lines = ""
    for i in range(8):
        a = math.radians(i * 45 + rot); l = size * (0.34 + 0.12 * ((i * 5) % 3) / 2)
        lines += f'<line x1="{c}" y1="{c}" x2="{c + l * math.cos(a)}" y2="{c + l * math.sin(a)}" stroke="{col}" stroke-width="{size * 0.1}" stroke-linecap="round"/>'
    return sprite(f'<svg width="{size}" height="{size}" style="display:block">{lines}</svg>')

def decor_grey(base, t, sid):
    i = IDS.index(sid); k = 0.6 + 0.4 * ease_out((t - SC[sid]) / 0.8)
    left = i % 2 == 0
    place(base, gburst(640, t * 5 * (1 if left else -1)), 90 if left else 990, 1300 if left else 1450, k, 0.9)
    place(base, gburst(380, -t * 6), 960 if left else 120, 190, k, 0.8)
m3.decor3 = decor_grey


def count_card(v, unit, sub, w=800, size=210):
    return sprite(card(w, f'<div style="text-align:center;font:800 {size}px MK;color:#111;line-height:1.05">{v}<span style="font-size:{size * .5}px;color:{VIO}"> {unit}</span></div><div style="text-align:center;font:700 54px MK;color:#777;margin-top:8px">{sub}</div>', pad=50, r=44))

def phone(inner_html, w=420, h=680):
    return sprite(f'<div style="width:{w}px;height:{h}px;border-radius:70px;background:#111;padding:20px;{SH}"><div style="width:100%;height:100%;border-radius:52px;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px">{inner_html}</div></div>')


def shot(key, y_css=540, h_px=250, w=1000, tag="Official website: blog.google", top=False):
    """own Playwright screenshot of Google's official announcement page, key phrase marked yellow (DAILY_COMMON rule 3)"""
    im = Image.open(RAW / f"shot_{key}.png").convert("RGB")
    crop = im.crop((0, 100, 1800, 1000)) if top else im.crop((0, max(0, int(y_css * 2) - h_px), 1800, min(im.height, int(y_css * 2) + h_px)))
    crop = crop.resize((w, int(crop.height * w / crop.width)), Image.LANCZOS)
    bio = io.BytesIO(); crop.save(bio, "JPEG", quality=90)
    src = "data:image/jpeg;base64," + base64.b64encode(bio.getvalue()).decode()
    return sprite(f'<div style="width:{w}px"><div style="display:inline-block;background:#fff;border-radius:16px;padding:6px 22px 10px;font:800 40px MK;color:#222;{SH};margin-bottom:18px">{tag}</div>'
                  f'<div style="width:{w}px;border-radius:30px;overflow:hidden;{SH};background:#fff;line-height:0"><img src="{src}" style="width:{w}px"></div></div>')

def money(tl):
    v = round(1.05 * clamp((tl - 1.2) / 1.6), 2)
    return sprite(card(880, f'<div style="display:flex;align-items:center;justify-content:center;gap:30px"><div style="font:800 80px MK;color:#aaa;text-decoration:line-through">$0.10</div><div style="font:800 70px MK;color:{VIO}">&rarr;</div><div style="font:800 120px MK;color:#111">$0.07</div></div>'
                       f'<div style="text-align:center;font:700 50px MK;color:#777;margin:6px 0 24px">har second ka daam</div>'
                       f'<div style="background:#f2f2f5;border-radius:26px;padding:20px 30px;text-align:center;font:800 62px MK;color:#111">15 sec clip &asymp; <span style="color:{VIO}">${v:.2f}</span></div>', pad=46, r=44))

def len_bar(tl):
    p = clamp((tl - 0.6) / 1.2)
    return sprite(card(880, f'<div style="font:800 56px MK;color:#111;margin-bottom:18px">Clip length</div><div style="display:flex;width:788px;height:80px;border-radius:40px;overflow:hidden;background:#e6e6ea">'
                       f'<div style="width:{int(788 * 10 / 15)}px;background:#9aa0ad;color:#fff;font:800 44px MK;display:flex;align-items:center;justify-content:center">10 sec</div>'
                       f'<div style="width:{int(788 * 5 / 15 * p)}px;background:{VIO};color:#fff;font:800 44px MK;display:flex;align-items:center;justify-content:center;white-space:nowrap">{"+5" if p > .6 else ""}</div></div>'
                       f'<div style="display:flex;justify-content:space-between;font:700 42px MK;color:#777;margin-top:14px"><span>pehle</span><span>ab: 15 sec tak</span></div>', pad=46, r=44))

def lerp(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))

def edit_scene(tl, tb, tl2, tw, W_=880, H_=520):
    """PIL-drawn clip that really changes: sunset background, then night light, then rain"""
    k1 = clamp((tl - tb) / 0.8); k2 = clamp((tl - tl2) / 0.8); k3 = clamp((tl - tw) / 0.6)
    day_t, day_b = (110, 185, 250), (215, 238, 255); sun_t, sun_b = (255, 120, 90), (255, 205, 140); ng_t, ng_b = (22, 28, 66), (80, 76, 135)
    top = lerp(lerp(day_t, sun_t, k1), ng_t, k2); bot = lerp(lerp(day_b, sun_b, k1), ng_b, k2)
    im = Image.new("RGB", (W_, H_)); d = ImageDraw.Draw(im)
    for y in range(H_): d.line([(0, y), (W_, y)], fill=lerp(top, bot, y / H_))
    if k2 > 0.3:
        rng = np.random.RandomState(3)
        for _ in range(30):
            x, y = rng.randint(0, W_), rng.randint(0, 260); d.ellipse((x, y, x + 5, y + 5), fill=(255, 255, 255))
    if k2 < 0.5: sx, sy = 640, 150 + 150 * k1; d.ellipse((sx - 55, sy - 55, sx + 55, sy + 55), fill=lerp((255, 240, 150), (255, 150, 80), k1))
    else: d.ellipse((640 - 45, 120 - 45, 640 + 45, 120 + 45), fill=(240, 240, 255))
    hills = lerp(lerp((70, 170, 90), (200, 160, 100), k1), (40, 50, 70), k2 * 0.8)
    d.polygon([(0, 400), (200, 330), (420, 395), (640, 320), (W_, 390), (W_, H_), (0, H_)], fill=hills)
    d.rectangle((330, 330, 470, 440), fill=lerp((250, 245, 235), (60, 60, 80), k2)); d.polygon([(310, 335), (400, 270), (490, 335)], fill=(200, 80, 70))
    d.rectangle((385, 370, 415, 440), fill=(255, 210, 90) if k2 > 0.3 else (130, 90, 60))
    if k3 > 0:
        ov = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); rng = np.random.RandomState(int(tl * 15) % 7)
        od.rectangle((0, 0, W_, H_), fill=(40, 60, 90, int(90 * k3)))
        for _ in range(int(160 * k3)):
            x = rng.randint(0, W_); y = rng.randint(0, H_); od.line([(x, y), (x - 8, y + 30)], fill=(200, 220, 255, 190), width=3)
        for cx, cy in ((180, 90), (420, 60), (700, 100)): od.ellipse((cx - 90, cy - 35, cx + 90, cy + 35), fill=(90, 100, 120, int(230 * k3)))
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im); f = ImageFont.truetype(MUKTA, 44)
    lab = "Prompt: sunset background" if (k1 > 0 and k2 == 0) else ("Prompt: raat ki light" if k2 > 0 and k3 == 0 else ("Prompt: baarish ka mausam" if k3 > 0 else "Original clip"))
    wlab = d.textlength(lab, font=f); d.rounded_rectangle((24, 22, 24 + wlab + 44, 22 + 70), radius=22, fill=(255, 255, 255)); d.text((46, 22), lab, font=f, fill=(20, 20, 24))
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, W_, H_), radius=40, fill=255)
    out = Image.new("RGBA", (W_ + 120, H_ + 160), (0, 0, 0, 0)); sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 90, 60 + W_, 90 + H_), radius=40, fill=(0, 0, 0, 80)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    im = im.convert("RGBA"); im.putalpha(mask); out.alpha_composite(im, (60, 60)); return out


def phrase2(base, t, sid, words, k0, k1, t_end, top=CAP_TOP, maxw=960):
    """whole phrase fades in at once (no word-by-word flicker) and stays until the next phrase"""
    ts = T(sid, k0) - 0.1
    if t < ts: return
    a = fade(t, ts, 0.25) * (1 - fade(t, t_end - 0.2, 0.2))
    sprs = [wspr(words[k][0], words[k][1], True) for k in range(k0, k1 + 1)]
    lines = [[]]; widths = [0]; gap = 22
    for sp in sprs:
        wd = sp.width - 140
        if widths[-1] + wd > maxw and lines[-1]: lines.append([]); widths.append(0)
        lines[-1].append((sp, wd)); widths[-1] += wd + gap
    y = top
    for ln, wd in zip(lines, widths):
        x = W / 2 - (wd - gap) / 2
        for sp, w_ in ln:
            place(base, sp, x + w_ / 2, y + (1 - a) * 16, 1.0, a); x += w_ + gap
        y += FS + 26

def scene2(sid, label, chip_name, chip_icon, words, pics, caps, intro=0.95):
    def f(base, t):
        t0 = SC[sid]; decor_grey(base, t, sid)
        if label and t < t0 + intro:
            q = pop(t, t0 + 0.02); out = 1 - fade(t, t0 + intro - 0.2, 0.2)
            place(base, big_label(label), 540, 520, 0.8 + 0.2 * q, fade(t, t0, 0.15) * out)
            place(base, chip(chip_name, chip_icon), 540, 700, pop(t, t0 + 0.25), fade(t, t0 + 0.25, 0.15) * out)
        else: place(base, chip(chip_name, chip_icon), 540, 150, 1.25, fade(t, t0 + intro, 0.2))
        st = [max(T(sid, p[0]) - 0.12, t0 + intro) if i == 0 else T(sid, p[0]) - 0.12 for i, p in enumerate(pics)]; en = st[1:] + [E(sid) - 0.05]
        for i, (k0, k1, fn, style) in enumerate(pics):
            if st[i] <= t < en[i]:
                spr = fn(t - st[i], st[i]) if fn.__code__.co_argcount == 2 else fn(t - st[i])
                show(base, t, spr, st[i], en[i], style)
        ce = [T(sid, c[0]) for c in caps[1:]] + [E(sid) - 0.05]
        for (k0, k1), te in zip(caps, ce): phrase2(base, t, sid, words, k0, k1, te)
    return f

def WD(s, bold=()):
    return [(w, i in bold) for i, w in enumerate(s.split())]


S_hook = scene2("hook", None, "GEMINI OMNI", "star",
    WD("Google ne AI video ki limit 15 second kar di, aur daam 30 percent kam!", (2, 3, 6, 7, 12, 13)),
    [(0, 9, lambda tl: shot("top", top=True), "zoomin"),
     (10, 14, lambda tl: count_card("-30%", "", "daam kam", size=230), "right")], [(0, 9), (10, 14)])

S_what = scene2("what", "Naya", "NAME", "bolt",
    WD("Naam hai Gemini Omni 1.2 Flash. Pehle clip das second ki thi, ab teen se 15 second tak.", (2, 3, 4, 5, 8, 15)),
    [(0, 5, lambda tl: shot("len"), "left"), (6, 17, len_bar, "bottom")], [(0, 5), (6, 17)])

S_price = scene2("price", "Price", "PRICE", "clock",
    WD("Price bhi gira hai. Google ke mutabik 7 cent prati second, 720p video ke liye.", (0, 2, 7, 8, 11)),
    [(0, 3, lambda tl: shot("price"), "right"), (4, 14, money, "bottom")], [(0, 3), (4, 14)])

def _edit_fn(tl, start):
    return edit_scene(tl, T("edit", 8) - start, T("edit", 9) - start, T("edit", 11) - start)
S_edit = scene2("edit", "Edit", "REMIX", "star",
    WD("Ek clip ko baar-baar badal bhi sakte ho. Background, light ya mausam, bina shuru se banaye.", (1, 3, 4, 8, 9, 11, 12, 13)),
    [(0, 15, _edit_fn, "zoomin")], [(0, 7), (8, 15)])

S_where = scene2("where", "Kahan", "WHERE", "term",
    WD("Gemini API, AI Studio aur Google Vids mein hai. Gemini app mein sirf Ultra walon ko.", (0, 1, 2, 3, 5, 6, 9, 10, 13)),
    [(0, 8, lambda tl: shot("where"), "left"),
     (9, 15, lambda tl: phone(f'<div style="font:800 56px MK;color:#111">Gemini app</div>{ic("star", 130)}<div style="background:{VIO};color:#fff;font:800 50px MK;border-radius:24px;padding:10px 30px">ULTRA only</div>'), "right")], [(0, 8), (9, 15)])

S_caution = scene2("caution", "Dhyan", "CAUTION", "warn",
    WD("Dhyan rakho! Tez sports action aur complex physics par Google khud kehta hai, kaam jaari hai.", (0, 1, 3, 4, 6, 7, 13, 14)),
    [(0, 8, lambda tl: shot("caution"), "zoomin"),
     (9, 15, lambda tl: big_card("Work in progress", "Google ka kehna", None, size=96), "right")], [(0, 8), (9, 15)])

def S_cta(base, t):
    sid = "cta"; decor_grey(base, t, sid)
    place(base, sprite(robot_circle(480, "thumbs")), 540, 470, pop(t, SC[sid] + 0.05), fade(t, SC[sid], 0.2))
    t0 = T(sid, 5)
    place(base, sprite(card(760, f'<div style="font:800 84px MK;color:#fff;background:{VIO};border-radius:30px;padding:18px 20px;text-align:center">+ Follow</div><div style="text-align:center;font:700 44px MK;color:#777;margin-top:14px">DevRoboLab</div>', pad=26, r=40)), 540, 880, pop(t, t0), fade(t, t0, 0.2))
    words = WD("Aisi AI news roz chahiye? DevRoboLab ko follow karo.", (1, 2, 5, 7))
    phrase2(base, t, sid, words, 0, 4, T(sid, 5)); phrase2(base, t, sid, words, 5, 8, E(sid))

mc.SCENES.update({"hook": S_hook, "what": S_what, "price": S_price, "edit": S_edit, "where": S_where, "caution": S_caution, "cta": S_cta})

if __name__ == "__main__":
    (HERE / "review").mkdir(exist_ok=True); (HERE / "output").mkdir(exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        ims = [Image.fromarray(mc.frame(float(v))).resize((360, 640)) for v in sys.argv[2:]]
        s = Image.new("RGB", (360 * 6, 640 * ((len(ims) + 5) // 6)), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 360, (i // 6) * 640))
        s.save(HERE / "review/sheet.png"); print("total", round(TOTAL, 1), {k: round(v, 1) for k, v in SC.items()})
    else:
        mc.build_audio(HERE / "audio/voice.wav"); n = int(TOTAL * FPS)
        mc.encode((mc.frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / "shared/music/clean/Local_Forecast_Elevator.mp3", HERE / "output/short.mp4")
