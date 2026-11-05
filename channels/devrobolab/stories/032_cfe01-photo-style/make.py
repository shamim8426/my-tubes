"""Claude Feature 01 (photo upload) rebuilt WITHOUT the HTML engine: real photo + real screenshots (paper-cut) + plain captions,
rendered by scripts/photo_video.py. Same voice as story 031. Run: python -X utf8 make.py"""
import sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import *

LEAD, AFTER, SR = 0.30, 0.28, 24000
CUT = HERE / "cut"
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

shoe = load(HERE / "assets_raw/shoe_0.jpg")
blur = blurred_fill(shoe, 0.5)
low = cv2.resize(cv2.resize(shoe, (54, 37), interpolation=cv2.INTER_AREA), (shoe.shape[1], shoe.shape[0]), interpolation=cv2.INTER_NEAREST)
SP = {n: sprite_w(CUT / f"shot_{n}.png", 940) for n in ["intro", "how", "formats", "limits", "tips", "project"]}
CH = sprite_w(CUT / "char_3.png", 460)
paper = cover(load(CUT / "paper_bg.jpg"))


def stamp(txt, rot):
    f = ImageFont.truetype(FONT, 78); w = int(f.getlength(txt)) + 90
    im = Image.new("RGBA", (w, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w - 5, 145), 28, outline=YEL + (255,), width=10, fill=(20, 20, 20, 235))
    d.text((45, 22), txt, font=f, fill=YEL + (255,))
    return np.array(im.rotate(rot, expand=True, resample=Image.BICUBIC))


STAMPS = [(stamp("JPEG", 4), 80, 1380), (stamp("PNG", -5), 560, 1400), (stamp("GIF", -4), 100, 1560), (stamp("WebP", 5), 520, 1580)]
title = lambda fr, t, txt, t1=1.4: words_reveal(txt, 92, t, 0.3, t1, 250, fr)
P = lambda fr, s, x, y, t, t0, a=1.0: paste_rgba(fr, s, x, y, alpha=min(1, max(0, (t - t0) / 0.18)) * a, scale=0.6 + 0.4 * ease_back((t - t0) / 0.45))


def scene(i, t, dur):
    fr = np.zeros((H, W, 3), np.uint8)
    if i == 0:
        fr[:] = blur; paste(fr, kenburns(shoe, t, dur, 1080, 1.0, 1.10, (0.3, 0)), 0, 560)
        title(fr, t, "Photo dikhao,\nClaude ko", 1.6)
        t0 = dur * 0.42; p = ease_out((t - t0) / 0.6)
        paste_rgba(fr, SP["intro"], 70, int(H + 20 - p * (H - 1300)), alpha=1.0)
    elif i == 1:
        fr[:] = blur; title(fr, t, "Photo kaise daalo", 1.2)
        P(fr, SP["how"], 70, 340, t, 0.3)
        for k, ln in enumerate(["+  button", "drag & drop", "clipboard paste"]):
            t0 = dur * (0.30 + 0.22 * k)
            if t >= t0:
                s = text_sprite(ln, 84, YEL if k != 1 else (255, 255, 255)); a = ease_out((t - t0) / 0.3)
                paste_rgba(fr, s, (W - s.shape[1]) // 2, 1100 + k * 150 + int((1 - a) * 30), alpha=a)
    elif i == 2:
        fr[:] = blur; paste(fr, kenburns(shoe, t, dur, 1080, 1.0, 1.06, (-0.3, 0)), 0, 560)
        title(fr, t, "Kaunse formats\nchalte hain", 1.5)
        for k, (s, x, y) in enumerate(STAMPS):
            t0 = dur * 0.30 + k * 0.42
            P(fr, s, x, y, t, t0)
    elif i == 3:
        fr[:] = blur; title(fr, t, "Limits yaad rakho", 1.2)
        P(fr, SP["limits"], 70, 360, t, 0.3)
        if t > dur * 0.30:
            a = ease_out((t - dur * 0.30) / 0.4)
            s = text_sprite("20", 380, YEL); paste_rgba(fr, s, (W - s.shape[1]) // 2, 780, alpha=a, scale=0.7 + 0.3 * a)
            s = text_sprite("files per chat", 78); paste_rgba(fr, s, (W - s.shape[1]) // 2, 1190, alpha=a)
        if t > dur * 0.62:
            a = ease_out((t - dur * 0.62) / 0.4)
            s = text_sprite("8000 x 8000", 150, YEL); paste_rgba(fr, s, (W - s.shape[1]) // 2, 1340, alpha=a, scale=0.7 + 0.3 * a)
            s = text_sprite("pixels tak (image)", 70); paste_rgba(fr, s, (W - s.shape[1]) // 2, 1520, alpha=a)
    elif i == 4:
        fr[:] = blur; title(fr, t, "Behtar nateeja", 1.0)
        P(fr, SP["tips"], 70, 340, t, 0.3)
        y0, h = 760, round(shoe.shape[0] * 1080 / shoe.shape[1])
        a_ = cv2.resize(low, (1080, h), interpolation=cv2.INTER_NEAREST); b_ = cv2.resize(shoe, (1080, h), interpolation=cv2.INTER_CUBIC)
        div = int(1080 * ease_io((t - dur * 0.28) / (dur * 0.45)))
        img = a_.copy(); img[:, :div] = b_[:, :div]; paste(fr, img, 0, y0)
        cv2.rectangle(fr, (div - 4, y0), (div + 4, y0 + h), YEL[::-1][::-1], -1)
        s = text_sprite("1000 x 1000+", 62, YEL); paste_rgba(fr, s, 60, y0 + h + 40)
        s = text_sprite("chhoti, blurry", 62); paste_rgba(fr, s, W - s.shape[1] - 60, y0 + h + 40)
    elif i == 5:
        fr[:] = paper; title(fr, t, "Project me bhi rakho", 1.2)
        P(fr, SP["project"], 70, 380, t, 0.3)
        P(fr, CH, 560, 800, t, dur * 0.35)
        if t > dur * 0.5:
            s = text_sprite("Project > Files", 90, YEL); a = ease_out((t - dur * 0.5) / 0.4)
            paste_rgba(fr, s, 60, 1250, alpha=a)
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
        if i > 0 and lt < 0.3:
            a = ease_io(lt / 0.3); fr = (prev.astype(np.float32) * (1 - a) + fr.astype(np.float32) * a).astype(np.uint8)
        elif i > 0 and prev is None:
            pass
        if lt > D[i] - 0.05: prev = fr
        elif k == 0 or lt < 0.01: prev = prev
        last_scene_frame[0] = fr
        if lt >= D[i] - 1 / FPS - 1e-6: prev = fr
        yield fr


last_scene_frame = [None]
if __name__ == "__main__":
    print("scenes", [round(x, 1) for x in START], "total", round(TOTAL, 1), flush=True)
    encode(frames(), int(TOTAL * FPS), voice, ROOT / "shared/music/presentation/Funkorama.mp3", HERE / "output/short_photo.mp4")
    print("done")
