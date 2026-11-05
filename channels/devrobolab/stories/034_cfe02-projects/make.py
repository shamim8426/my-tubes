"""Claude Feature 02 (series Claude for Everyone): Projects. Photo-first style (no HTML engine), scripts/photo_video.py.
Source (official): https://support.claude.com/en/articles/9517075-what-are-projects and /9519177-how-can-i-create-and-manage-projects (read 2026-11-06)
Real assets: own screenshots of those articles (shoot.py), real library photo (Wikimedia Commons, see CREDITS in log), AI-drawn robot sticker, drawn diagrams."""
import sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import *
from papercut import paper_rect

LEAD, AFTER, SR = 0.30, 0.28, 24000
CUT, SH = HERE / "cut", HERE / "shots"
waves = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(7)]
D = [LEAD + wav_dur(w) + AFTER for w in waves]
START = [sum(D[:i]) for i in range(7)]
TOTAL = sum(D)
(HERE / "build").mkdir(exist_ok=True)
voice = HERE / "build/voice.wav"
with wave.open(str(voice), "wb") as o:
    o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    for w in waves:
        with wave.open(str(w)) as r:
            o.writeframes(b"\x00\x00" * int(SR * LEAD) + r.readframes(r.getnframes()) + b"\x00\x00" * int(SR * AFTER))

lib = load(HERE / "raw/library_photo.jpg")
blur = blurred_fill(lib, 0.45)
paper = cover(load(CUT / "paper_bg.jpg"))
for n in ["intro", "create", "knowledge", "instr", "ctx", "free"]:
    if not (CUT / f"shot_{n}.png").exists():
        paper_rect(Image.open(SH / f"{n}.png").convert("RGB"), border=26, seed=sum(map(ord, n)) % 97).save(CUT / f"shot_{n}.png")
SP = {n: sprite_w(CUT / f"shot_{n}.png", 940) for n in ["intro", "create", "knowledge", "instr", "ctx", "free"]}
CH = sprite_w(CUT / "char_3.png", 420)
F = lambda s: ImageFont.truetype(FONT, s)


def diagram(label, color, k, cross=False, n=3):
    """Drawn diagram (Pillow, no HTML): a central box (Knowledge / Instructions) connected to k of n chat circles. cross=True: two chats with a red X between."""
    im = Image.new("RGBA", (940, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if cross:
        for x, nm in [(230, "Chat 1"), (710, "Chat 2")]:
            d.ellipse((x - 120, 250, x + 120, 490), fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=10)
            d.text((x - F(54).getlength(nm) / 2, 335), nm, font=F(54), fill=(20, 20, 20, 255))
        d.line((380, 370, 560, 370), fill=(20, 20, 20, 255), width=8)
        d.line((435, 320, 505, 420), fill=(214, 40, 40, 255), width=18); d.line((505, 320, 435, 420), fill=(214, 40, 40, 255), width=18)
        if k:
            d.rounded_rectangle((250, 20, 690, 150), 36, fill=color + (255,), outline=(20, 20, 20, 255), width=10)
            d.text((470 - F(60).getlength(label) / 2, 45), label, font=F(60), fill=(20, 20, 20, 255))
            for x in (230, 710): d.line((470, 150, x, 250), fill=(20, 20, 20, 255), width=10)
        return np.array(im)
    d.rounded_rectangle((250, 20, 690, 150), 36, fill=color + (255,), outline=(20, 20, 20, 255), width=10)
    d.text((470 - F(60).getlength(label) / 2, 45), label, font=F(60), fill=(20, 20, 20, 255))
    xs = [170, 470, 770]
    for i, x in enumerate(xs[:n]):
        on = i < k
        if on: d.line((470, 150, x, 300), fill=(20, 20, 20, 255), width=10)
        d.ellipse((x - 105, 300, x + 105, 510), fill=(YEL if on else (255, 255, 255)) + (255,), outline=(20, 20, 20, 255), width=10)
        nm = f"Chat {i + 1}"; d.text((x - F(46).getlength(nm) / 2, 378), nm, font=F(46), fill=(20, 20, 20, 255))
    return np.array(im)


DIA = {k: diagram("Knowledge", YEL, k) for k in range(4)}
DIA_I = {k: diagram("Instructions", (255, 255, 255), k) for k in range(4)}
DIA_X = {0: diagram("Knowledge", YEL, 0, True), 1: diagram("Knowledge", YEL, 1, True)}
title = lambda fr, t, txt, t1=1.4: words_reveal(txt, 92, t, 0.3, t1, 250, fr)
P = lambda fr, s, x, y, t, t0, a=1.0: paste_rgba(fr, s, x, y, alpha=min(1, max(0, (t - t0) / 0.18)) * a, scale=0.6 + 0.4 * ease_back((t - t0) / 0.45))


def scene(i, t, dur):
    fr = np.zeros((H, W, 3), np.uint8)
    if i == 0:
        fr[:] = blur; paste(fr, kenburns(lib, t, dur, 1080, 1.0, 1.10, (0.2, 0.0)), 0, 440)
        title(fr, t, "Projects banao", 1.2)
        p = ease_out((t - dur * 0.38) / 0.6)
        paste_rgba(fr, SP["intro"], 70, int(H + 20 - p * (H - 1260)))
    elif i == 1:
        fr[:] = blur; title(fr, t, "Project kaise banao", 1.4)
        P(fr, SP["create"], 70, 340, t, 0.3)
        for k, (ln, c) in enumerate([("Projects  >  + New Project", YEL), ("naam + description", (255, 255, 255)), ("Claude ko ye nahi dikhta", YEL)]):
            t0 = dur * (0.25 + 0.25 * k)
            if t >= t0:
                s = text_sprite(ln, 70, c); a = ease_out((t - t0) / 0.3)
                paste_rgba(fr, s, (W - s.shape[1]) // 2, 980 + k * 150 + int((1 - a) * 30), alpha=a)
    elif i == 2:
        fr[:] = blur; title(fr, t, "Knowledge daalo", 1.2)
        P(fr, SP["knowledge"], 70, 340, t, 0.3)
        k = 0 if t < dur * 0.45 else min(3, 1 + int((t - dur * 0.45) / 0.55))
        P(fr, DIA[k], 70, 760, t, 0.5)
    elif i == 3:
        fr[:] = paper; title(fr, t, "Instructions do", 1.2)
        P(fr, SP["instr"], 70, 340, t, 0.3)
        k = 0 if t < dur * 0.5 else min(3, 1 + int((t - dur * 0.5) / 0.55))
        P(fr, DIA_I[k], 70, 840, t, 0.5)
    elif i == 4:
        fr[:] = blur; title(fr, t, "Ek baat yaad rakho", 1.3)
        P(fr, SP["ctx"], 70, 340, t, 0.3)
        P(fr, DIA_X[1 if t > dur * 0.62 else 0], 70, 700, t, 0.6)
        if t > dur * 0.62:
            s = text_sprite("jo chahiye, knowledge me daalo", 62, YEL); a = ease_out((t - dur * 0.62) / 0.4)
            paste_rgba(fr, s, (W - s.shape[1]) // 2, 1380, alpha=a)
    elif i == 5:
        fr[:] = paper; title(fr, t, "Free me bhi milta hai", 1.4)
        P(fr, SP["free"], 70, 340, t, 0.3)
        if t > dur * 0.4:
            a = ease_out((t - dur * 0.4) / 0.4)
            s = text_sprite("5", 520, YEL); paste_rgba(fr, s, (W - s.shape[1]) // 2, 680, alpha=a, scale=0.7 + 0.3 * a)
            s = text_sprite("projects (free users)", 80); paste_rgba(fr, s, (W - s.shape[1]) // 2, 1360, alpha=a)
    else:
        fr[:] = paper
        words_reveal("DevRoboLab\nko follow karo", 110, t, 0.3, 1.8, 330, fr)
        a = ease_back((t - 1.6) / 0.5)
        btn = Image.new("RGBA", (520, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(btn)
        d.rounded_rectangle((0, 0, 519, 189), 95, fill=YEL + (255,)); f = ImageFont.truetype(FONT, 100)
        d.text((260 - f.getlength("Follow") / 2, 36), "Follow", font=f, fill=(20, 20, 20, 255))
        paste_rgba(fr, np.array(btn), 280, 760, alpha=min(1, a), scale=max(0.01, a))
        P(fr, CH, 300, 1100, t, 0.8)
    return fr


def frames():
    n = int(TOTAL * FPS); prev = None
    for k in range(n):
        t = k / FPS
        i = max(j for j in range(7) if START[j] <= t + 1e-6); lt = t - START[i]
        fr = scene(i, lt, D[i])
        if i > 0 and lt < 0.3 and prev is not None:
            a = ease_io(lt / 0.3); fr = (prev.astype(np.float32) * (1 - a) + fr.astype(np.float32) * a).astype(np.uint8)
        if lt >= D[i] - 1 / FPS - 1e-6: prev = fr
        yield fr


if __name__ == "__main__":
    print("scenes", [round(x, 1) for x in START], "total", round(TOTAL, 1), flush=True)
    encode(frames(), int(TOTAL * FPS), voice, ROOT / "shared/music/presentation/Funkorama.mp3", HERE / "output/short_photo.mp4")
    print("done")
