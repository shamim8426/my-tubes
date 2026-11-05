"""Photo-first video renderer (NO HTML): real photos + paper-cut screenshots + plain captions, composed frame by frame with
Pillow/OpenCV and piped to ffmpeg. Free, local, CPU.  Used by channels/devrobolab/stories/032_*/make.py.
Helpers: Frame canvas 1080x1920, sprites (RGBA), eased pops, Ken-Burns photo, blurred-fill, before/after slider, outlined captions.
"""
import subprocess
import wave
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
ROOT = Path(__file__).resolve().parent.parent
FONT = str(ROOT / "shared/fonts/Poppins-ExtraBold.ttf")
YEL = (255, 214, 10)


def ease_out(p): p = min(1, max(0, p)); return 1 - (1 - p) ** 3
def ease_back(p):
    p = min(1, max(0, p)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2
def ease_io(p): p = min(1, max(0, p)); return 0.5 - 0.5 * np.cos(np.pi * p)


def load(path, mode="RGB"): return np.array(Image.open(path).convert(mode))


def cover(img, w=W, h=H):
    """Scale + centre-crop an RGB array to w x h."""
    s = max(w / img.shape[1], h / img.shape[0])
    r = cv2.resize(img, (int(img.shape[1] * s) + 1, int(img.shape[0] * s) + 1), interpolation=cv2.INTER_CUBIC)
    y0, x0 = (r.shape[0] - h) // 2, (r.shape[1] - w) // 2
    return r[y0:y0 + h, x0:x0 + w]


def blurred_fill(img, dark=0.55):
    b = cv2.GaussianBlur(cover(img), (0, 0), 28)
    return (b * dark).astype(np.uint8)


def kenburns(img, t, dur, w, z0=1.0, z1=1.08, pan=(0, 0)):
    """Photo shown w px wide (height from aspect) with a slow push-in; returns an RGB array w x h' (cropped from a zoomed window)."""
    h = round(img.shape[0] * w / img.shape[1])
    base = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)
    z = z0 + (z1 - z0) * ease_io(t / max(dur, 1e-3))
    cw, ch = w / z, h / z
    cx = w / 2 + pan[0] * (1 - 1 / z) * w; cy = h / 2 + pan[1] * (1 - 1 / z) * h
    M = np.float32([[z, 0, -(cx - cw / 2) * z], [0, z, -(cy - ch / 2) * z]])
    return cv2.warpAffine(base, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def paste(frame, rgb, x, y):
    h, w = rgb.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 > x0 and y1 > y0: frame[y0:y1, x0:x1] = rgb[y0 - y:y1 - y, x0 - x:x1 - x]


def paste_rgba(frame, spr, x, y, alpha=1.0, scale=1.0, cx=None, cy=None):
    """Alpha-composite an RGBA sprite. (x,y) = top-left at scale 1; scaling is around the sprite centre."""
    if alpha <= 0.01 or scale <= 0.02: return
    h, w = spr.shape[:2]
    if abs(scale - 1) > 1e-3:
        spr = cv2.resize(spr, (max(1, int(w * scale)), max(1, int(h * scale))), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
        x += int((w - spr.shape[1]) / 2); y += int((h - spr.shape[0]) / 2); h, w = spr.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0: return
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32); a = s[..., 3:4] / 255.0 * alpha
    reg = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (reg * (1 - a) + s[..., :3] * a).astype(np.uint8)


def sprite_w(path, w):
    a = load(path, "RGBA"); return cv2.resize(a, (w, round(a.shape[0] * w / a.shape[1])), interpolation=cv2.INTER_AREA)


def text_sprite(text, size, color=(255, 255, 255), stroke=8, hl=None):
    """Outlined bold text -> RGBA sprite. Words wrapped by '\n'. hl = set of words to colour yellow."""
    f = ImageFont.truetype(FONT, size)
    lines = text.split("\n"); lh = int(size * 1.25)
    wmax = max(int(f.getlength(l)) for l in lines) + 2 * stroke + 8
    im = Image.new("RGBA", (wmax, lh * len(lines) + 2 * stroke), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (wmax - int(f.getlength(l))) // 2
        for wd in l.split(" "):
            c = YEL if hl and wd.strip(",.:?!") in hl else color
            d.text((x, i * lh + stroke), wd, font=f, fill=c + (255,), stroke_width=stroke, stroke_fill=(15, 15, 15, 255))
            x += int(f.getlength(wd + " "))
    return np.array(im)


def words_reveal(text, size, t, t0, t1, y, frame, hl=None, color=(255, 255, 255)):
    """Word-by-word caption (centred at y): words appear evenly between t0 and t1 (rise + fade)."""
    ws = text.replace("\n", " \n ").split(" "); ws = [w for w in ws if w != ""]
    # build lines first (use '\n' tokens), reveal count by time
    n_vis = 0
    flat = [w for w in ws if w != "\n"]
    for k in range(len(flat)):
        if t >= t0 + (t1 - t0) * k / max(1, len(flat)): n_vis = k + 1
    out, cnt = [], 0
    for ln in text.split("\n"):
        toks = ln.split(" "); vis = []
        for tk in toks:
            if cnt < n_vis: vis.append(tk)
            cnt += 1
        out.append(" ".join(vis))
    # keep the layout stable: render full text with invisible (transparent) future words by padding with spaces of same width is complex;
    # simple approach: render visible part centred per line.
    txt = "\n".join(out)
    if not txt.strip(): return
    spr = text_sprite(txt, size, color, hl=hl)
    paste_rgba(frame, spr, (W - spr.shape[1]) // 2, int(y - spr.shape[0] / 2))


def wav_dur(p):
    with wave.open(str(p)) as w: return w.getnframes() / w.getframerate()


def encode(frames_iter, n_frames, voice_wav, music, out, music_start=6.0, music_gain_db=-24):
    """Pipe RGB frames to ffmpeg; mix voice + music, loudnorm to -14 LUFS."""
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice_wav)]
    if music:
        cmd += ["-ss", str(music_start), "-i", str(music)]
        fc = f"[2:a]volume={music_gain_db}dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]"
        cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, fr in enumerate(frames_iter):
        p.stdin.write(fr.tobytes())
        if i % 150 == 0: print(f"  frame {i}/{n_frames}", flush=True)
    p.stdin.close(); p.wait()
