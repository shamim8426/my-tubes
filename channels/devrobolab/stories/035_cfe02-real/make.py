"""Claude Feature 02 (Projects) - REAL-PHOTO version (user 2026-11-06: 'sab kuch real photos'). Photo-first, no HTML, scripts/photo_video.py.
Photos: CC0 / public domain, found via the Openverse API (raw/meta.json has source + licence). Screenshots of the official help pages = small proof insets only.
Voice = story 034 (copied)."""
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
CUT, SH, RAW = HERE / "cut", HERE / "shots", HERE / "raw"
waves = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(7)]
D = [LEAD + wav_dur(w) + AFTER for w in waves]
START = [sum(D[:i]) for i in range(7)]
TOTAL = sum(D)
voice = HERE / "build/voice.wav"
with wave.open(str(voice), "wb") as o:
    o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    for w in waves:
        with wave.open(str(w)) as r:
            o.writeframes(b"\x00\x00" * int(SR * LEAD) + r.readframes(r.getnframes()) + b"\x00\x00" * int(SR * AFTER))

PH = {k: load(RAW / f"{k}.jpg") for k in ["workspace_0", "workspace_1", "workspace_2", "checklist_0", "binders_0", "pencils_0", "pencils_2"]}
BL = {k: blurred_fill(v, 0.5) for k, v in PH.items()}
for n in ["intro", "create", "knowledge", "instr", "ctx", "free"]:
    if not (CUT / f"shot_{n}.png").exists():
        paper_rect(Image.open(SH / f"{n}.png").convert("RGB"), border=26, seed=sum(map(ord, n)) % 97).save(CUT / f"shot_{n}.png")
INW = {"intro": 760, "create": 620, "knowledge": 760, "instr": 640, "ctx": 760, "free": 760}
SP = {n: sprite_w(CUT / f"shot_{n}.png", w) for n, w in INW.items()}
CH = sprite_w(CUT / "char_3.png", 420)
paper = cover(load(CUT / "paper_bg.jpg"))
F = lambda s: ImageFont.truetype(FONT, s)
title = lambda fr, t, txt, t1=1.4: words_reveal(txt, 92, t, 0.3, t1, 250, fr)
P = lambda fr, s, x, y, t, t0, a=1.0: paste_rgba(fr, s, x, y, alpha=min(1, max(0, (t - t0) / 0.18)) * a, scale=0.6 + 0.4 * ease_back((t - t0) / 0.45))


def band(fr, key, t, dur, y=420, z1=1.08, pan=(0, 0)):
    fr[:] = BL[key]; paste(fr, kenburns(PH[key], t, dur, 1080, 1.0, z1, pan), 0, y)
    return round(PH[key].shape[0] * 1080 / PH[key].shape[1])


def proof(fr, name, t, t0):
    s = SP[name]; P(fr, s, (W - s.shape[1]) // 2, 1880 - s.shape[0], t, t0)


def lines(fr, t, dur, items, y0=1180, size=72, gap=140, start=0.25, step=0.25):
    for k, (ln, c) in enumerate(items):
        t0 = dur * (start + step * k)
        if t >= t0:
            s = text_sprite(ln, size, c); a = ease_out((t - t0) / 0.3)
            paste_rgba(fr, s, (W - s.shape[1]) // 2, y0 + k * gap + int((1 - a) * 30), alpha=a)


def scene(i, t, dur):
    fr = np.zeros((H, W, 3), np.uint8)
    if i == 0:
        h = band(fr, "workspace_0", t, dur, 420, 1.10, (0.2, 0)); title(fr, t, "Projects banao", 1.2)
        lines(fr, t, dur, [("har project = alag workspace", YEL)], 1230, 62, 0, 0.35)
        proof(fr, "intro", t, dur * 0.5)
    elif i == 1:
        h = band(fr, "workspace_1", t, dur, 420, 1.08, (-0.2, 0)); title(fr, t, "Project kaise banao", 1.4)
        lines(fr, t, dur, [("Projects  >  + New Project", YEL), ("naam + description", (255, 255, 255)), ("Claude ko ye nahi dikhta", YEL)], 1180, 62, 125, 0.22, 0.24)
        proof(fr, "create", t, dur * 0.55)
    elif i == 2:
        h = band(fr, "binders_0", t, dur, 420, 1.08); title(fr, t, "Knowledge daalo", 1.2)
        lines(fr, t, dur, [("documents  ·  text  ·  code", YEL), ("sab chats me kaam aayega", (255, 255, 255))], 1190, 66, 140, 0.25, 0.35)
        proof(fr, "knowledge", t, dur * 0.55)
    elif i == 3:
        h = band(fr, "checklist_0", t, dur, 420, 1.08, (0.3, 0)); title(fr, t, "Instructions do", 1.2)
        lines(fr, t, dur, [("Set project instructions", YEL), ("Save  ->  har chat me lagu", (255, 255, 255))], 1190, 66, 140, 0.25, 0.3)
        proof(fr, "instr", t, dur * 0.55)
    elif i == 4:
        fr[:] = BL["workspace_1"]; title(fr, t, "Ek baat yaad rakho", 1.3)
        paste(fr, kenburns(PH["workspace_1"], t, dur, 1080, 1.0, 1.05), 0, 360)
        paste(fr, kenburns(PH["workspace_2"], t, dur, 1080, 1.0, 1.05), 0, 360 + 740)
        for k, (nm, y) in enumerate([("Chat 1", 380), ("Chat 2", 380 + 740)]):
            s = text_sprite(nm, 70, YEL); paste_rgba(fr, s, 50, y)
        a = ease_back((t - dur * 0.25) / 0.4)
        x = np.zeros((300, 300, 4), np.uint8); cv2.line(x, (40, 40), (260, 260), (214, 40, 40, 255), 40); cv2.line(x, (260, 40), (40, 260), (214, 40, 40, 255), 40)
        paste_rgba(fr, x, 390, 1010, alpha=min(1, a), scale=max(0.01, a))
        if t > dur * 0.62:
            s = text_sprite("jo chahiye, knowledge me daalo", 58, YEL); paste_rgba(fr, s, (W - s.shape[1]) // 2, 1690, alpha=ease_out((t - dur * 0.62) / 0.4))
        proof(fr, "ctx", t, dur * 0.35) if False else None
    elif i == 5:
        h = band(fr, "pencils_0", t, dur, 420, 1.06); title(fr, t, "Free me bhi milta hai", 1.4)
        if t > dur * 0.35:
            a = ease_out((t - dur * 0.35) / 0.4)
            s = text_sprite("5", 340, YEL); paste_rgba(fr, s, (W - s.shape[1]) // 2, 1160, alpha=a, scale=0.7 + 0.3 * a)
            s = text_sprite("projects (free users)", 74); paste_rgba(fr, s, (W - s.shape[1]) // 2, 1580, alpha=a)
        proof(fr, "free", t, dur * 0.6) if False else None
    else:
        fr[:] = BL["pencils_2"]; paste(fr, kenburns(PH["pencils_2"], t, dur, 1080, 1.0, 1.06), 0, 900)
        words_reveal("DevRoboLab\nko follow karo", 110, t, 0.3, 1.8, 330, fr)
        a = ease_back((t - 1.6) / 0.5)
        btn = Image.new("RGBA", (520, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(btn)
        d.rounded_rectangle((0, 0, 519, 189), 95, fill=YEL + (255,)); f = F(100)
        d.text((260 - f.getlength("Follow") / 2, 36), "Follow", font=f, fill=(20, 20, 20, 255))
        paste_rgba(fr, np.array(btn), 280, 560, alpha=min(1, a), scale=max(0.01, a))
        P(fr, CH, 330, 1500, t, 0.8)
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
    encode(frames(), int(TOTAL * FPS), voice, ROOT / "shared/music/presentation/Funkorama.mp3", HERE / "output/short_real.mp4")
    print("done")
