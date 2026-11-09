"""Reality Check - Asli: orbit animation look-test (Didymos / Dimorphos, period before -> after DART).

    python tools/rc_orbit_anim.py <out.mp4> [--seconds 12] [--fps 30]

Free (Pillow + numpy + ffmpeg). Look: navy-black space, one amber accent, no faces. Illustrative, NOT to scale
(said on screen). Facts: period 11 h 55 min before, 11 h 23 min after (script v2, dossier F-tags).
Pass 1: Pillow draws the shapes (no text). Pass 2: ffmpeg/libass burns ALL on-screen text (Roman/Hinglish, user 2026-11-08: no Devanagari on screen, plain digits) from a generated .ass file,
because Pillow on the PC has no raqm and mis-shapes Devanagari (matras in the wrong order, broken conjuncts).
"""
import argparse
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
W, H, SS = 1920, 1080, 2
BG, INK, AMBER, DIM = (7, 11, 24), (232, 238, 250), (255, 176, 32), (88, 104, 140)
CX, CY, RAD = 780, 560, 330
P1, P2 = 4.0, 3.55  # seconds per orbit before / after impact (difference exaggerated so the eye sees it)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


_r = np.random.default_rng(7)
STARS = [(_r.uniform(0, W), _r.uniform(0, H), _r.uniform(0.8, 2.2), _r.uniform(0, 6.28)) for _ in range(140)]


def orbit_angle(t, t_hit):
    a0 = -math.pi / 2
    return a0 + 2 * math.pi * (t / P1 if t < t_hit else t_hit / P1 + (t - t_hit) / P2)


def frame(t, total):
    img = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img, "RGBA")
    S = SS
    for x, y, r, ph in STARS:
        a = int(110 + 60 * math.sin(t * 1.3 + ph))
        d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=(200, 215, 255, a))
    fade = ease(t / 1.0)
    d.ellipse([(CX - RAD) * S, (CY - RAD) * S, (CX + RAD) * S, (CY + RAD) * S], outline=(120, 140, 190, int(150 * fade)), width=2 * S)
    R = 92
    d.ellipse([(CX - R) * S, (CY - R) * S, (CX + R) * S, (CY + R) * S], fill=(150, 156, 170, int(255 * fade)), outline=(205, 210, 225, int(255 * fade)), width=3 * S)
    for ox, oy, rr in [(-30, -20, 22), (35, 25, 16), (10, -50, 11), (-45, 40, 13)]:
        d.ellipse([(CX + ox - rr) * S, (CY + oy - rr) * S, (CX + ox + rr) * S, (CY + oy + rr) * S], fill=(118, 124, 138, int(255 * fade)))
    t_hit = total * 0.55
    ang = orbit_angle(t, t_hit)
    for k in range(40, 0, -1):
        tt = t - k * 0.02
        if tt < 0:
            continue
        a_k = orbit_angle(tt, t_hit)
        px, py = CX + RAD * math.cos(a_k), CY + RAD * math.sin(a_k)
        rr = 9 * (1 - k / 45)
        d.ellipse([(px - rr) * S, (py - rr) * S, (px + rr) * S, (py + rr) * S], fill=(255, 176, 32, int(70 * (1 - k / 40))))
    mx, my = CX + RAD * math.cos(ang), CY + RAD * math.sin(ang)
    mr = 24
    d.ellipse([(mx - mr) * S, (my - mr) * S, (mx + mr) * S, (my + mr) * S], fill=(188, 190, 198, int(255 * fade)), outline=(235, 238, 245, 255), width=2 * S)
    if t_hit <= t < t_hit + 0.7:
        a = int(200 * (1 - (t - t_hit) / 0.7))
        d.rectangle([0, 0, W * S, H * S], fill=(255, 240, 210, a // 3))
        ir = 40 + 260 * ((t - t_hit) / 0.7)
        d.ellipse([(mx - ir) * S, (my - ir) * S, (mx + ir) * S, (my + ir) * S], outline=(255, 214, 120, a), width=4 * S)
    return img.resize((W, H), Image.LANCZOS)


def hms(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ass(total):
    t_hit = total * 0.55
    ang = orbit_angle(t_hit, t_hit)
    mx, my = CX + RAD * math.cos(ang), CY + RAD * math.sin(ang)

    def col(rgb):
        return "&H%02X%02X%02X&" % (rgb[2], rgb[1], rgb[0])

    def ev(a, b, x, y, txt, px, rgb, an=7, fi=300, fo=0):
        fs = int(px * 1.662)  # ASS size = line height; Mukta px = size / 1.662
        tag = "{\\an%d\\pos(%d,%d)\\fs%d\\1c%s\\fad(%d,%d)}" % (an, x, y, fs, col(rgb), fi, fo)
        return f"Dialogue: 0,{hms(a)},{hms(b)},T,,0,0,0,,{tag}{txt}"

    events = [
        ev(0, total, 1290, 160, "Didymos", 46, INK, fi=1000),
        ev(0, total, 1290, 225, "approx. 780 m", 34, DIM, fi=1000),
        ev(0.8, total, 1290, 290, "Dimorphos ka ek chakkar", 46, INK, fi=800),
        ev(0.8, t_hit + 0.5, 1290, 350, "11 ghante 55 min", 70, AMBER, fi=800, fo=500),
        ev(t_hit, total, 1290, 350, "11 ghante 23 min", 70, AMBER, fi=500),
        ev(t_hit + 0.4, total, 1290, 500, "33 min chhota", 46, INK, fi=600),
        ev(t_hit, t_hit + 0.8, int(mx), int(my) - 100, "DART", 40, AMBER, an=8, fi=100, fo=500),
        ev(0, total, 60, 1005, "Illustrative, not to scale", 34, DIM, fi=0),
        ev(0, total, 1860, 1005, "Source: NASA / Thomas et al., Nature 2023", 34, DIM, an=9, fi=0),
    ]
    head = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 2", "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        "Style: T,Mukta,60,&HFFFFFF&,&HFFFFFF&,&H000000&,&H000000&,-1,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1", "",
        "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]
    return "\n".join(head + events) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=12.0)
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    cands = [ROOT / "tools/ffmpeg/ffmpeg.exe", Path("D:/my-tubes/tools/ffmpeg/ffmpeg.exe")]
    ff = next((str(c) for c in cands if c.exists()), "ffmpeg")
    out = Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    base = out.with_suffix(".base.mp4")
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(base)], stdin=subprocess.PIPE)
    for i in range(int(a.seconds * a.fps)):
        p.stdin.write(frame(i / a.fps, a.seconds).tobytes())
    p.stdin.close()
    if p.wait():
        sys.exit(1)
    assf = out.with_suffix(".ass")
    assf.write_text(ass(a.seconds), encoding="utf-8")
    fonts = (ROOT / "shared/fonts").as_posix().replace(":", "\\:")
    rc = subprocess.run([ff, "-y", "-loglevel", "error", "-i", base.name, "-vf", f"subtitles=filename={assf.name}:fontsdir='{fonts}'",
                         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out.name], cwd=str(out.parent)).returncode
    base.unlink(missing_ok=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
