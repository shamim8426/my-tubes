"""003 sample (lines 1-8, 60 s): stills with slow eased camera moves (sub-pixel PIL crops), 0.3 s dissolves, mid-tone grade,
side/bottom panels (Roman text), 'AI reconstruction' label; audio = cache/reality-check/003/sample60/mix_norm.wav.
python build_sample.py  -> output/003_sample_60s.mp4 (1080p) + output/003_sample_60s_360p.mp4"""
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
ROOT = HERE.parents[4]
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
FONT_B = str(ROOT / "shared/fonts/Mukta-ExtraBold.ttf")
FONT = str(ROOT / "shared/fonts/Mukta-Bold.ttf")
W, H, FPS, DUR = 1920, 1080, 30, 60.0
T = {l["line"]: l for l in json.loads((HERE.parent / "audio/voiceover_timing.json").read_text(encoding="utf-8"))}
AMBER = (242, 179, 61, 255)

# shot table: (t0, t1, image, (cx, cy, wfrac) start, end)   all times from voiceover_timing.json
s = lambda n: T[n]["start"]  # noqa: E731
SHOTS = [
    (0.0, s(2), "a01_bedroom_night", (0.5, 0.5, 1.0), (0.52, 0.5, 0.88)),
    (s(2), s(2) + 3.3, "a02a_clock_3am", (0.46, 0.52, 0.68), (0.50, 0.52, 0.60)),
    (s(2) + 3.3, s(2) + 6.5, "a02b_notebook", (0.5, 0.5, 1.0), (0.55, 0.55, 0.85)),
    (s(2) + 6.5, s(3), "a02c_hallway_shadow", (0.5, 0.5, 1.0), (0.5, 0.48, 0.82)),
    (s(3), s(4), "a03_pinball", (0.64, 0.62, 0.62), (0.62, 0.64, 0.54)),   # crop right: keeps the blurred arcade visitors out of frame
    (s(4), s(4) + 3.6, "a04a_street_night", (0.45, 0.5, 0.92), (0.55, 0.5, 0.92)),
    (s(4) + 3.6, s(5), "a04b_traffic_light", (0.5, 0.5, 1.0), (0.5, 0.5, 0.88)),
    (s(5), s(6), "a05_moon_rooftops", (0.5, 0.48, 0.88), (0.5, 0.5, 1.0)),
    (s(6), s(6) + 4.8, "a06_phone_bed", (0.45, 0.55, 1.0), (0.42, 0.58, 0.85)),
    (s(6) + 4.8, s(7), "a12_pillow_moon", (0.5, 0.5, 1.0), (0.5, 0.55, 0.9)),
    (s(7), s(8), "a07_school", (0.5, 0.5, 1.0), (0.55, 0.5, 0.88)),
    (s(8), s(8) + 4.9, "a08_science_fair", (0.62, 0.6, 0.70), (0.60, 0.62, 0.60)),
    (s(8) + 4.9, DUR, "a09_hourglass", (0.5, 0.55, 1.0), (0.5, 0.6, 0.85)),
]


def clause_time(line, frac):
    l = T[line]
    return l["start"] + frac * (l["end"] - l["start"])


def panel(kind, title, lines=(), big=False):
    """RGBA full-frame overlay: 'side' (right/left panel) or 'bottom' panel; dark translucent box, amber bar, white text."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ft = ImageFont.truetype(FONT_B, 92 if big else 54)
    fl = ImageFont.truetype(FONT, 40)
    if kind.startswith("side"):
        x0 = 1190 if kind == "side_r" else 90
        bw = 640
        hh = 70 + (110 if big else 70) + 58 * len(lines) + 30
        y0 = (H - hh) // 2
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + hh], 22, fill=(8, 10, 14, 175))
        d.rectangle([x0, y0 + 24, x0 + 8, y0 + hh - 24], fill=AMBER)
        d.text((x0 + 40, y0 + 34), title, font=ft, fill=(255, 255, 255, 255))
        y = y0 + 34 + (118 if big else 74)
        for t in lines:
            d.text((x0 + 40, y), t, font=fl, fill=(235, 235, 235, 255))
            y += 58
    else:
        tw = d.textlength(title, font=ft)
        bw = int(tw + 120)
        x0 = (W - bw) // 2
        y0 = H - 230
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + 120], 20, fill=(8, 10, 14, 175))
        d.rectangle([x0 + 24, y0 + 112, x0 + bw - 24, y0 + 117], fill=AMBER)
        d.text((x0 + 60, y0 + 22), title, font=ft, fill=(255, 255, 255, 255))
    return np.asarray(im).astype(np.float32) / 255.0


def label():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 30)
    t = "AI reconstruction"
    tw = d.textlength(t, font=f)
    d.rounded_rectangle([W - tw - 96, 50, W - 60, 98], 10, fill=(0, 0, 0, 110))
    d.text((W - tw - 78, 54), t, font=f, fill=(255, 255, 255, 200))
    return np.asarray(im).astype(np.float32) / 255.0


L2 = [(0.0, "Aankhen tik nahi rahi"), (0.22, "Yaaddasht dhokha de rahi"), (0.45, "Shak hone laga"), (0.62, "Jo tha hi nahi, wo dikha")]
OVER = [  # (t0, t1, overlay)
    (1.0, s(2) - 0.2, panel("side_r", "11 DIN", ["ek pal bhi neend nahi"], big=True)),
    (s(3) + 1.2, s(4) - 0.3, panel("bottom", "Din 10: pinball mein scientist ko haraya")),
    (s(4) + 2.1, s(5) - 0.3, panel("bottom", "San Diego, USA  |  1964")),
    (s(5) + 0.6, s(6) - 0.3, panel("bottom", "Sawal: dimaag ko kya hua?")),
    (s(7) + 0.6, s(8) - 0.3, panel("side_r", "RANDY GARDNER", ["17 saal", "Point Loma High School", "San Diego"])),
    (clause_time(8, 0.42), DUR - 0.6, panel("bottom", "Insaan bina soye kitne din jaag sakta hai?")),
]
for k, (fr, _) in enumerate(L2):   # rising list, one item at a time (side panel left)
    t0 = clause_time(2, fr)
    t1 = clause_time(2, L2[k + 1][0]) if k + 1 < len(L2) else T[2]["end"] + 0.3
    OVER.append((t0, t1, panel("side_l", "Kya hua?", [x for _, x in L2[: k + 1]])))
LABEL = label()
IMG = {}
LUT = np.clip(255 * (np.arange(256) / 255.0) ** 0.86 * 0.96 + 8, 0, 255).astype(np.uint8)   # mid-tone grade: lift shadows a little, soft highlights


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def frame_of(shot, t):
    t0, t1, name, a, b = shot
    if name not in IMG:
        IMG[name] = Image.open(HERE / "ai" / f"{name}.png").convert("RGB")
    im = IMG[name]
    iw, ih = im.size
    e = ease((t - t0) / max(t1 - t0, 0.01))
    cx, cy, wf = [a[i] + (b[i] - a[i]) * e for i in range(3)]
    bw = wf * iw
    bh = bw * 9 / 16
    bh = min(bh, ih)
    bw = bh * 16 / 9
    x0 = min(max(cx * iw - bw / 2, 0), iw - bw)
    y0 = min(max(cy * ih - bh / 2, 0), ih - bh)
    return np.asarray(im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))).astype(np.float32)


def main():
    out = HERE / "output/003_sample_60s.mp4"
    wav = ROOT / "cache/reality-check/003/sample60/mix_norm.wav"
    p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR}", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        t = i / FPS
        k = next(j for j, sh in enumerate(SHOTS) if sh[0] <= t < sh[1] or j == len(SHOTS) - 1)
        f = frame_of(SHOTS[k], t)
        if k and t - SHOTS[k][0] < 0.3:            # 0.3 s dissolve from the previous shot
            w = (t - SHOTS[k][0]) / 0.3
            f = f * w + frame_of(SHOTS[k - 1], t) * (1 - w)
        f = LUT[np.clip(f, 0, 255).astype(np.uint8)].astype(np.float32)
        for t0, t1, ov in OVER + [(0, DUR, LABEL)]:
            if t0 <= t < t1:
                al = min(1.0, (t - t0) / 0.4, (t1 - t) / 0.4)
                a_ = ov[..., 3:4] * al
                f = f * (1 - a_) + ov[..., :3] * 255 * a_
        p.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(out), "-vf", "scale=640:360", "-c:v", "libx264", "-crf", "26", "-preset", "fast",
                    "-c:a", "aac", "-b:a", "128k", str(HERE / "output/003_sample_60s_360p.mp4")], check=True)
    print("done", out)


if __name__ == "__main__":
    main()
