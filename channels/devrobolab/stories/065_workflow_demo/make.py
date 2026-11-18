"""064 How-to Short: Claude Code me apna slash command kaise banayein. Warm cream grid paper + dark terminal cards, accent TANGERINE,
own Playwright captures of the official docs (code.claude.com/docs/en/skills, /commands), drawn terminal / folder tree / SKILL.md editor (illustration).
Run: python make.py frames t1 t2 ...  |  python make.py range t0 t1 out.mp4  |  python make.py (render)"""
import json, math, sys, wave
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
ACC = (234, 88, 12); ACCL = (254, 215, 170); INKD = (30, 30, 36); GREEN = (22, 163, 74); RED = (225, 45, 57)
TERM = (24, 26, 33); TGREY = (150, 156, 170); TGREEN = (74, 222, 128); TYEL = (253, 224, 71)


def T(scene, k):
    toks = WT[scene]["tokens"]; return SC[scene] + LEAD + toks[min(k, len(toks) - 1)][1]


_fc = {}
def font(sz, mono=False):
    key = (sz, mono)
    if key not in _fc: _fc[key] = ImageFont.truetype(str(ROOT / ("shared/fonts/IBMPlexMono-Bold.ttf" if mono else "shared/fonts/Poppins-Bold.ttf")), sz)
    return _fc[key]


def chip(text, size, fill, color=(255, 255, 255), pad=(34, 14), r=26, hl=None, hlcolor=ACCL, mono=False):
    f = font(size, mono); words = text.split(" "); sp = f.getlength(" ")
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
    im = Image.new("RGB", (W, H), (252, 248, 238)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(252, int(248 - 8 * k), int(238 - 10 * k)))
    d.ellipse([150, 250, 1250, 1350], fill=(255, 222, 190)); im = im.filter(ImageFilter.GaussianBlur(150)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(240, 232, 216), width=1)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(240, 232, 216), width=1)
    return im.convert("RGBA")
BGP = bg_paper()


def with_border(img, r=18, bw=5):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    o = img.convert("RGBA"); o.putalpha(m); ImageDraw.Draw(o).rounded_rectangle([0, 0, o.width - 1, o.height - 1], r, outline=INKD + (255,), width=bw); return o


def crop_w(name, box, w):
    c = Image.open(HERE / f"raw/{name}.png").convert("RGB").crop(box); return c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)


SRC1 = "Official: code.claude.com/docs / Extend Claude with skills"


def srcline(base, txt=SRC1, y=1425):
    return
    place(base, chip(txt, 24, (40, 44, 58), (235, 235, 240), pad=(20, 5), r=12), 540, y)


def banner(base, t, txt, ts, y=200, fill=ACC, size=46):
    if t >= ts:
        pp = pop(t, ts + 0.03); place(base, chip(txt, size, fill, (255, 255, 255), pad=(30, 9), r=26), 540, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


def pc(base, txt, size, fill, color, cx, cy, t, ts, rot=0, pad=(36, 10), r=26, hl=None, mono=False):
    if t >= ts - 0.02:
        pp = pop(t, ts); place(base, chip(txt, size, fill, color, pad=pad, r=r, hl=hl, mono=mono), cx, cy, 0.6 + 0.4 * pp, min(1, pp * 1.4), rot)


def term_frame(w, h, title="terminal"):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 28, fill=TERM + (255,), outline=INKD + (255,), width=5)
    d.rounded_rectangle([0, 0, w - 1, 64], 28, fill=(44, 47, 58, 255)); d.rectangle([0, 40, w - 1, 64], fill=(44, 47, 58, 255))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))): d.ellipse([24 + 40 * i, 20, 48 + 40 * i, 44], fill=c + (255,))
    d.text((150, 14), title, font=font(30, True), fill=TGREY + (255,))
    return im, d


def typed(txt, t, t0, cps=22):
    if t < t0: return ""
    return txt[:int((t - t0) * cps) + 1]


def terminal(t, t_cmd, t_run, cmd="/fix-issue 123", steps=("Read the issue", "Implement the fix", "Write tests"), t_steps=None, hl=True):
    """Drawn Claude Code terminal (illustration): typed slash command, then Claude follows the SKILL.md steps."""
    w, h = 940, 560; im, d = term_frame(w, h, "Claude Code  (illustration)")
    s = typed(cmd, t, t_cmd); f = font(48, True)
    d.text((40, 100), ">", font=f, fill=TGREEN + (255,))
    if s:
        x0 = 90; tw = f.getlength(s)
        if hl and t >= t_run: d.rounded_rectangle([x0 - 10, 96, x0 + tw + 12, 160], 12, fill=ACC + (255,))
        d.text((x0, 100), s, font=f, fill=(255, 255, 255, 255))
        if int(t * 2.5) % 2 == 0 and len(s) < len(cmd): d.rectangle([x0 + tw + 4, 104, x0 + tw + 28, 156], fill=(255, 255, 255, 255))
    if t >= t_run:
        d.text((40, 196), "Claude: SKILL.md ke steps follow kar raha hai", font=font(30, True), fill=TYEL + (255,))
        ts = t_steps or [t_run + 0.4 + 0.5 * i for i in range(len(steps))]
        for i, (stp, tt) in enumerate(zip(steps, ts)):
            if t >= tt:
                y = 268 + 82 * i; q = ease_out(min(1, (t - tt) / 0.25))
                cx = 44 + int(30 * (1 - q)); d.line([(cx, y + 28), (cx + 16, y + 46), (cx + 44, y + 10)], fill=TGREEN + (int(255 * q),), width=8)
                d.text((100 + int(30 * (1 - q)), y + 4), stp, font=font(40, True), fill=(235, 238, 245, int(255 * q)))
    return im


TREE = [("my-project/", 0, None), (".claude/", 1, None), ("skills/", 2, None), ("fix-issue/", 3, "folder"), ("SKILL.md", 4, "file")]
def tree(t, times, t_arrow=None, root="my-project/"):
    """Folder tree card that grows line by line (illustration)."""
    w, h = 940, 520; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    for i, (name, lvl, kind) in enumerate(TREE):
        tt = times[i]
        if t < tt: continue
        q = ease_out(min(1, (t - tt) / 0.25)); y = 34 + 92 * i; x = 40 + 66 * lvl + int(40 * (1 - q))
        if i == 0: name = root
        if lvl:
            d.line([(40 + 66 * (lvl - 1) + 22, y - 40), (40 + 66 * (lvl - 1) + 22, y + 30), (x - 10, y + 30)], fill=(190, 190, 200, 255), width=4)
        isfile = kind == "file"
        col = ACC if kind == "folder" else (INKD if not isfile else (37, 99, 235))
        if kind == "folder" and t_arrow and t >= t_arrow:
            tw = font(50, True).getlength(name); d.rounded_rectangle([x - 12, y - 4, x + tw + 14, y + 68], 14, fill=ACCL + (255,))
        if isfile:
            d.rounded_rectangle([x, y + 8, x + 40, y + 60], 6, outline=col + (255,), width=5); d.line([(x + 9, y + 26), (x + 31, y + 26)], fill=col + (255,), width=4)
        else:
            d.rounded_rectangle([x, y + 16, x + 48, y + 58], 6, fill=(253, 186, 116, 255)); d.rounded_rectangle([x, y + 8, x + 22, y + 22], 4, fill=(253, 186, 116, 255))
        d.text((x + 66, y), name, font=font(50, True), fill=col + (int(255 * q),))
    d.text((w - 210, h - 44), "illustration", font=font(24), fill=(140, 140, 150, 255))
    return im


EDIT = [("---", "dash"), ("description: Fix a GitHub issue", "desc"), ("---", "dash"), ("Fix GitHub issue $ARGUMENTS", "body"),
        ("1. Read the issue", "step"), ("2. Implement the fix", "step"), ("3. Write tests", "step")]
def editor(t, t_dash, t_desc, t_steps, t_arg):
    """Drawn SKILL.md editor (illustration)."""
    w, h = 940, 660; im, d = term_frame(w, h, ".claude/skills/fix-issue/SKILL.md")
    times = [t_dash, t_desc, t_dash + 0.15, t_steps, t_steps + 0.25, t_steps + 0.45, t_steps + 0.65]
    f = font(40, True)
    if t < t_dash: d.text((40, 110), "# khaali file ... upar se likhiye", font=f, fill=(110, 116, 130, 255))
    for i, ((txt, kind), tt) in enumerate(zip(EDIT, times)):
        if t < tt: continue
        y = 96 + 76 * i + (14 if i >= 3 else 0); q = ease_out(min(1, (t - tt) / 0.25)); a = int(255 * q)
        if kind == "dash":
            d.rounded_rectangle([30, y - 6, 140, y + 54], 10, fill=(ACC if t < t_desc + 1.5 else (60, 64, 78)) + (255,)); d.text((44, y), txt, font=f, fill=(255, 255, 255, a))
        elif kind == "desc":
            d.text((40, y), "description:", font=f, fill=(125, 211, 252, a)); d.text((40 + f.getlength("description: "), y), "Fix a GitHub issue", font=f, fill=(235, 238, 245, a))
        elif kind == "body":
            pre = "Fix GitHub issue "; d.text((40, y), pre, font=f, fill=(235, 238, 245, a)); x = 40 + f.getlength(pre)
            on = t >= t_arg
            if on: d.rounded_rectangle([x - 8, y - 6, x + f.getlength("$ARGUMENTS") + 8, y + 54], 10, fill=TYEL + (255,))
            d.text((x, y), "$ARGUMENTS", font=f, fill=(INKD if on else TYEL) + (a,))
        else:
            d.text((40, y), txt, font=f, fill=(200, 205, 215, a))
    return im


def result_card(t, t0, t_hl):
    w, h = 940, 230; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    d.text((36, 22), "Claude ko milta hai:", font=font(36), fill=(120, 120, 130, 255))
    f = font(54, True); pre = "Fix GitHub issue "; d.text((36, 100), pre, font=f, fill=INKD + (255,)); x = 36 + f.getlength(pre)
    if t >= t_hl: d.rounded_rectangle([x - 8, 94, x + f.getlength("123") + 10, 170], 12, fill=TYEL + (255,))
    d.text((x, 100), "123", font=f, fill=ACC + (255,)); d.text((x + f.getlength("123 "), 100), "...", font=f, fill=INKD + (255,))
    return im


def long_prompt(t, t_strike):
    w, h = 900, 330; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 28, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    d.text((30, 20), "Har baar type:", font=font(34), fill=(120, 120, 130, 255))
    for i, ln in enumerate(("Issue padho, requirement samjho,", "fix likho, tests likho,", "phir commit karo...")):
        d.text((30, 80 + 70 * i), ln, font=font(46, True), fill=INKD + (255,))
    if t >= t_strike:
        q = ease_out(min(1, (t - t_strike) / 0.35))
        for i in range(3): d.line([(24, 112 + 70 * i), (24 + int((w - 60) * q), 112 + 70 * i)], fill=RED + (255,), width=8)
    return im


def path_table(t, t0):
    w, h = 940, 330; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    rows = (("~/.claude/skills/", "SABHI projects", ACC), (".claude/skills/", "sirf IS project", (37, 99, 235)))
    for i, (p, lab, col) in enumerate(rows):
        tt = t0 + 0.3 + 0.6 * i
        if t < tt: continue
        q = ease_out(min(1, (t - tt) / 0.3)); y = 40 + 140 * i; a = int(255 * q); dx = int(60 * (1 - q))
        d.rounded_rectangle([30 + dx, y, 910, y + 120], 22, fill=(246, 244, 238, a))
        d.text((54 + dx, y + 16), p, font=font(46, True), fill=col + (a,)); d.text((54 + dx, y + 70), "= " + lab, font=font(38, True), fill=INKD + (a,))
    return im


def older_card(t, t0):
    w, h = 940, 330; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(255, 255, 255, 255), outline=INKD + (255,), width=5)
    d.text((40, 30), ".claude/commands/", font=font(44, True), fill=ACC + (255,))
    d.rounded_rectangle([60, 120, 440, 200], 16, fill=(219, 234, 254, 255)); d.text((84, 134), "deploy.md", font=font(42, True), fill=(37, 99, 235, 255))
    if t >= t0 + 0.5:
        q = ease_out(min(1, (t - t0 - 0.5) / 0.4)); x1 = 460 + int(150 * q)
        d.line([(460, 160), (x1, 160)], fill=INKD + (255,), width=10)
        if q > 0.7: d.polygon([(x1 - 4, 134), (x1 - 4, 186), (x1 + 30, 160)], fill=INKD + (255,))
    if t >= t0 + 1.1:
        q = ease_out(min(1, (t - t0 - 1.1) / 0.3)); d.rounded_rectangle([660, 120, 910, 200], 16, fill=ACC + (int(255 * q),)); d.text((682, 134), "/deploy", font=font(44, True), fill=(255, 255, 255, int(255 * q)))
    d.text((40, 250), "purani files bhi chalti hain", font=font(36), fill=(120, 120, 130, 255))
    return im


def arrow_down(base, cx, y0, y1, t, ts, col=ACC):
    if t < ts: return
    q = ease_out(min(1, (t - ts) / 0.3)); y = y0 + (y1 - y0) * q; d = ImageDraw.Draw(base)
    d.line([(cx, y0), (cx, y)], fill=col + (255,), width=12)
    if q > 0.6: d.polygon([(cx - 30, y - 6), (cx + 30, y - 6), (cx, y + 30)], fill=col + (255,))


# ---- captions (Roman Hinglish, whole phrase per sentence part) ----
CAPTXT = {
    "hook": [(0, "Wahi LAMBA prompt baar baar?"), (8, "Banao apna SLASH COMMAND"), (14, "Bas 1 FILE"), (18, "/fix-issue likho, Claude STEPS follow kare")],
    "steps": [(0, "1. Project me FOLDER banao"), (5, ".claude > skills > fix-issue"), (12, "2. Andar SKILL.md file"), (19, "FOLDER ka naam = COMMAND")],
    "file": [(0, "Upar --- lines ke beech"), (10, "DESCRIPTION = command kya karta hai"), (17, "Neeche aasaan STEPS"), (21, "$ARGUMENTS = jo aap TYPE karo"), (32, "Jaise /fix-issue 123"), (39, "Claude ko mila: ISSUE 123")],
    "note": [(0, "Dhyan rakho!"), (2, "Session CHAL raha + folder NAYA?"), (13, "To chalao /reload-skills"), (18, "HAR project ke liye"), (22, "HOME ke ~/.claude me banao"), (30, "PURANI commands files bhi CHALTI")],
    "cta": [(0, "Agla tip: PLAN MODE"), (7, "Aisi TRICKS ke liye FOLLOW kijiye")],
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
    t_cmd = T("hook", 18)
    if t < T("hook", 8) - 0.05:
        pc(base, "LAMBA PROMPT, BAAR BAAR?", 62, INKD, (255, 255, 255), 540, 200, t, -1.0, -1.5, pad=(40, 12), r=32)
    else:
        pc(base, "APNA /COMMAND", 92, ACC, (255, 255, 255), 540, 200, t, T("hook", 8), -1.5, pad=(50, 12), r=36)
    # frame 0 = the result: command typed and Claude following the steps
    card_enter(base, terminal(t, -2.0, -1.0, t_steps=[-1.0, -1.0, -1.0]), 540, 640, t, -1.0, side=0, dur=0.25, shad=False)
    if t >= t_cmd and t < t_cmd + 0.9:
        q = (t - t_cmd) / 0.9; d = ImageDraw.Draw(base); r = int(30 + 60 * q)
        d.rounded_rectangle([110 - r // 3, 445 - r // 3, 590 + r // 3, 525 + r // 3], 20, outline=ACC + (int(255 * (1 - q)),), width=8)
    if t < T("hook", 14) - 0.05:
        card_enter(base, long_prompt(t, T("hook", 8)), 540, 1170, t, -1.0, side=0, dur=0.25)
    else:
        pc(base, "1 FILE", 70, INKD, (255, 255, 255), 270, 1030, t, T("hook", 14), -2, pad=(40, 12), r=30)
        pc(base, "SKILL.md", 64, (255, 255, 255), (37, 99, 235), 700, 1030, t, T("hook", 15), 2, pad=(36, 12), r=30, mono=True)
        arrow_down(base, 540, 1100, 1210, t, T("hook", 18))
        pc(base, "/fix-issue", 76, ACC, (255, 255, 255), 540, 1290, t, T("hook", 19), 0, pad=(44, 12), r=30, mono=True)
    srcline(base, y=1425)


def s_steps(base, t, b):
    base.alpha_composite(BGP)
    banner(base, t, "KAISE BANAYEIN", b["t0"] + 0.05, 110)
    times = [b["t0"] + 0.15, T("steps", 5), T("steps", 8), T("steps", 10), T("steps", 14)]
    card_enter(base, tree(t, times, T("steps", 19)), 540, 460, t, b["t0"] + 0.1, side=-1)
    pc(base, "1  FOLDER", 46, INKD, (255, 255, 255), 300, 790, t, T("steps", 0) + 0.1, -1, pad=(28, 10), r=24)
    pc(base, "2  FILE", 46, (37, 99, 235), (255, 255, 255), 760, 790, t, T("steps", 12), 1, pad=(28, 10), r=24)
    if t >= T("steps", 19):
        pc(base, "fix-issue/", 56, (255, 255, 255), ACC, 300, 940, t, T("steps", 19), 0, pad=(26, 10), r=22, mono=True)
        pc(base, "=", 70, INKD, (255, 255, 255), 540, 940, t, T("steps", 21), 0, pad=(22, 2), r=22)
        pc(base, "/fix-issue", 56, ACC, (255, 255, 255), 790, 940, t, T("steps", 23), 0, pad=(26, 10), r=22, mono=True)
    card_enter(base, terminal(t, T("steps", 23), 1e9, cmd="/fix-issue", steps=()).crop((0, 0, 940, 200)), 540, 1230, t, b["t0"] + 0.3, side=1, shad=False)
    srcline(base, y=1425)


def s_file(base, t, b):
    base.alpha_composite(BGP)
    t2 = T("file", 32)
    if t < t2:
        card_enter(base, editor(t, T("file", 4), T("file", 10), T("file", 18), T("file", 22)), 540, 520, t, b["t0"] + 0.1, side=-1, shad=False)
        pc(base, "SKILL.md", 50, (255, 255, 255), (37, 99, 235), 230, 1250, t, b["t0"] + 0.2, -2, pad=(28, 10), r=22, mono=True)
        if t >= T("file", 10) and t < T("file", 17):
            pc(base, "KYA KARTA HAI", 52, ACC, (255, 255, 255), 700, 1170, t, T("file", 12), 1.5, pad=(30, 10), r=24)
        if t >= T("file", 22):
            pc(base, "= JO AAP TYPE KARO", 52, INKD, (255, 255, 255), 600, 1170, t, T("file", 25), -1, pad=(30, 10), r=24)
    else:
        card_enter(base, terminal(t, t2 + 0.05, T("file", 36), steps=(), hl=True).crop((0, 0, 940, 200)), 540, 520, t, t2, side=-1, shad=False)
        arrow_down(base, 540, 640, 760, t, T("file", 39))
        if t >= T("file", 36) - 0.05: card_enter(base, result_card(t, T("file", 36), T("file", 47)), 540, 900, t, T("file", 36) - 0.05, side=1)
        card_enter(base, chip("SKILL.md:  Fix GitHub issue $ARGUMENTS", 40, (255, 255, 255), INKD, pad=(28, 14), r=22, mono=True, hl={"$ARGUMENTS"}, hlcolor=ACC), 540, 1180, t, t2 + 0.15, side=1)
        pc(base, "$ARGUMENTS  =  123", 52, ACC, (255, 255, 255), 540, 1310, t, T("file", 44), -1, pad=(30, 10), r=24, mono=True)
    srcline(base, y=1425)


def s_note(base, t, b):
    base.alpha_composite(BGP)
    pc(base, "DHYAN RAKHO", 64, RED, (255, 255, 255), 540, 150, t, b["t0"] + 0.05, -1.5, pad=(40, 10), r=30)
    t2, t3 = T("note", 18), T("note", 30)
    if t < t2:
        card_enter(base, tree(t, [b["t0"] + 0.4 + 0.3 * i for i in range(5)], None, "my-project/"), 540, 520, t, b["t0"] + 0.1, side=1)
        pc(base, "SESSION CHAL RAHA + NAYA FOLDER", 44, INKD, (255, 255, 255), 540, 840, t, T("note", 2), 1, pad=(28, 10), r=24)
        tm = terminal(t, T("note", 14), 1e9, cmd="/reload-skills", steps=()).crop((0, 0, 940, 200))
        if t < T("note", 14): ImageDraw.Draw(tm).text((90, 100), "claude  (session chal raha)", font=font(40, True), fill=TGREY + (255,))
        card_enter(base, tm, 540, 1020, t, b["t0"] + 0.2, side=-1, shad=False)
        pc(base, "+ .claude/skills/  NAYA", 44, (255, 255, 255), ACC, 330, 1220, t, T("note", 11), -1.5, pad=(26, 10), r=22, mono=True)
        pc(base, "RESTART NAHI", 48, GREEN, (255, 255, 255), 820, 1220, t, T("note", 17), 2, pad=(28, 10), r=24)
    elif t < t3:
        card_enter(base, path_table(t, t2), 540, 430, t, t2 - 0.05, side=-1)
        pc(base, "HAR PROJECT KE LIYE", 54, INKD, (255, 255, 255), 540, 820, t, t2, 1, pad=(32, 10), r=26)
        pc(base, "~/.claude/skills/fix-issue/", 46, ACC, (255, 255, 255), 540, 960, t, T("note", 24), -1, pad=(28, 12), r=24, mono=True)
        pc(base, "sirf is project: .claude/skills/", 40, (255, 255, 255), INKD, 540, 1100, t, T("note", 26), 0.5, pad=(26, 10), r=22, mono=True)
        pc(base, "~ = HOME folder", 46, (37, 99, 235), (255, 255, 255), 540, 1240, t, T("note", 24) + 0.3, -1, pad=(28, 10), r=22)
    else:
        card_enter(base, older_card(t, t3), 540, 520, t, t3 - 0.05, side=1)
        pc(base, ".claude/commands/  bhi CHALTA", 48, INKD, (255, 255, 255), 540, 900, t, T("note", 30) + 0.05, 1, pad=(30, 10), r=24, hl={"CHALTA"})
        pc(base, "commands/deploy.md  =  /deploy", 44, (255, 255, 255), INKD, 540, 1040, t, T("note", 32), -1, pad=(28, 10), r=22, mono=True)
        pc(base, "NAYA KAAM: skills/", 54, GREEN, (255, 255, 255), 540, 1200, t, T("note", 34), 1.5, pad=(32, 10), r=26)
    srcline(base, y=1425)


def s_cta(base, t, b):
    lt = t - b["t0"]; base.alpha_composite(BGP)
    pc(base, "AGLA TIP: PLAN MODE", 58, INKD, (255, 255, 255), 540, 230, t, b["t0"] + 0.05, -1, pad=(36, 12), r=28)
    place(base, robot(700), 540, 700 + 8 * math.sin(lt * 3.5), 0.94 + 0.06 * ease_out(lt / 0.3))
    for n, (txt, ts, fill, sz) in enumerate((("+ FOLLOW", T("cta", 15), ACC, 80), ("CLAUDE CODE TRICKS", T("cta", 7), INKD, 48))):
        pp = pop(t, ts); place(base, chip(txt, sz, fill, (255, 255, 255), pad=(44, 10), r=30), 540, 1180 + 140 * n, 0.7 + 0.3 * pp, min(1, pp * 1.4), (-1.5, 1.5)[n])


B = [dict(k="hook", t0=0.0, t1=SC["steps"]), dict(k="steps", t0=SC["steps"], t1=SC["file"]), dict(k="file", t0=SC["file"], t1=SC["note"]),
     dict(k="note", t0=SC["note"], t1=SC["cta"]), dict(k="cta", t0=SC["cta"], t1=TOTAL + 1)]
FN = dict(hook=s_hook, steps=s_steps, file=s_file, note=s_note, cta=s_cta)
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
