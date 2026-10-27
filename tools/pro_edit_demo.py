"""Pro-edit demo on an existing final (free, local): re-edits the first N seconds of a built long video using its own
work files (video, voice and music stems) — no new image or TTS.

    python tools/pro_edit_demo.py            # story 005 (khazana), 0-120 s
Output: style_tests/pro_edit/khazana_pro_demo.mp4 and khazana_before_after.mp4 (old | new)

What it adds (all ours / CC0): colour grade + vignette + light grain + soft light leak, punch-in zooms on story beats,
a comic shake, whip transitions at scene cuts, an animated title card, the riddle as on-screen text, a counting pop-up,
name tags on first appearance; sound design (village ambience bed, paper, whooshes, chimes, running, comedy sting).
"""
import math
import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
S = ROOT / "channels/dadi-ki-kahaniyan/stories/005_gulmohar-ka-khazana/long/output"
WORK = S / "long_04_work"
SFX = ROOT / "shared/sfx"
OUT = ROOT / "style_tests/pro_edit"
DUR = 120.0
FPS = 30
W, H = 1920, 1080

CUTS = [15.533, 19.7, 32.1, 41.5, 53.167, 58.234, 68.367, 76.5, 79.333, 86.5, 94.1, 116.3]          # scene changes in the final
# punch-ins: (start, ramp s, zoom, end, centre x, centre y)
PUNCH = [(0.45, 0.25, 1.10, 3.1, 0.5, 0.45), (3.15, 0.2, 1.16, 4.2, 0.5, 0.45), (32.15, 0.2, 1.12, 34.4, 0.55, 0.45),
         (36.95, 0.15, 1.15, 38.9, 0.6, 0.35), (50.6, 0.12, 1.18, 52.4, 0.45, 0.5), (53.25, 0.12, 1.14, 54.9, 0.6, 0.4),
         (57.1, 0.12, 1.12, 58.2, 0.5, 0.5), (76.55, 0.15, 1.15, 78.4, 0.53, 0.28), (83.3, 0.12, 1.12, 84.3, 0.62, 0.45),
         (88.4, 0.15, 1.12, 90.0, 0.4, 0.5), (106.4, 1.2, 1.15, 108.6, 0.77, 0.55), (108.65, 0.12, 1.12, 110.2, 0.79, 0.5),
         (116.4, 0.25, 1.10, 118.6, 0.45, 0.5)]
SHAKE = (53.25, 0.55)                                        # "मेरी गोभी!!"
DAY = (9.0, 120.0)                                            # golden-light scenes get a soft light leak


def ease(x):
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, x)))


def zoom_at(t):
    z, cx, cy = 1.0, 0.5, 0.5
    for s, r, zz, e, x, y in PUNCH:
        if s <= t < e:
            k = ease((t - s) / r) if t - s < r else (1 - ease((t - (e - 0.2)) / 0.2) if t > e - 0.2 else 1.0)
            z, cx, cy = 1 + (zz - 1) * k, x, y
    return z, cx, cy


def grade_tables():
    x = np.arange(256, dtype=np.float32) / 255
    s = x + 0.06 * np.sin(2 * math.pi * (x - 0.25)) * (x * (1 - x)) * 4    # gentle S-curve
    b = np.clip(s * 0.97 + 0.01, 0, 1)
    r = np.clip(s * 1.04, 0, 1)
    return [(np.clip(c, 0, 1) * 255).astype(np.uint8) for c in (b, s, r)]   # BGR


def vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    return (1 - 0.22 * np.clip(d - 0.55, 0, 1) ** 1.5)[..., None].astype(np.float32)


def process_video(src: Path, dst: Path):
    cap = cv2.VideoCapture(str(src))
    tabs, vig = grade_tables(), vignette()
    rng = np.random.default_rng(3)
    enc = subprocess.Popen([str(FFMPEG), "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                            "-pix_fmt", "yuv420p", str(dst)], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    glow = (np.exp(-(((xx - W * 0.85) / (W * 0.35)) ** 2 + ((yy + H * 0.1) / (H * 0.6)) ** 2))[..., None]
            * np.float32((40, 90, 140)) * 0.35).astype(np.float32)
    grains = [rng.normal(0, 3.0, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1).astype(np.float32) for _ in range(6)]
    for i in range(n):
        ok, f = cap.read()
        if not ok:
            break
        t = i / FPS
        # punch-in zoom (+ comic shake)
        z, cx, cy = zoom_at(t)
        dx = dy = 0.0
        if SHAKE[0] <= t < SHAKE[0] + SHAKE[1]:
            a = 14 * (1 - (t - SHAKE[0]) / SHAKE[1])
            dx, dy = a * math.sin(t * 90), a * math.cos(t * 73)
            z = max(z, 1.04)
        if z > 1.0001 or dx or dy:
            M = np.float32([[z, 0, (1 - z) * cx * W + dx], [0, z, (1 - z) * cy * H + dy]])
            f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        # whip transition: horizontal motion blur + slide around each cut (±4 frames)
        for c in CUTS:
            d = t - c
            if -4 / FPS <= d < 4 / FPS:
                k = 1 - abs(d) / (4 / FPS)
                ksz = int(9 + 70 * k) | 1
                f = cv2.blur(f, (ksz, 1))
                shift = int(np.sign(d or 1) * -90 * k)
                f = np.roll(f, shift, axis=1)
        # colour grade, vignette, soft light leak, grain
        f = cv2.merge([cv2.LUT(ch, tb) for ch, tb in zip(cv2.split(f), tabs)])
        f = f.astype(np.float32)
        gray = f.mean(axis=2, keepdims=True)
        f = (gray + (f - gray) * 1.08) * vig
        if DAY[0] <= t < DAY[1]:
            f += np.roll(glow, int(W * 0.05 * math.sin(t * 0.3)), axis=1)
        f += grains[i % 6]
        if t > DUR - 0.8:
            f *= max(0.0, (DUR - t) / 0.8)
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    cap.release()


ASS = r"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleS,Mukta ExtraBold,64,&H00F0F5FF,&H000000FF,&H00203048,&H96000000,-1,0,0,0,100,100,0,0,1,5,3,5,0,0,0,1
Style: TitleB,Mukta ExtraBold,150,&H0040D8FF,&H000000FF,&H00102030,&H96000000,-1,0,0,0,100,100,0,0,1,9,5,5,0,0,0,1
Style: Riddle,Mukta Bold,58,&H00203A5A,&H000000FF,&H0098D8F0,&HB0000000,-1,0,0,0,100,100,0,0,3,18,0,2,140,140,90,1
Style: Count,Mukta ExtraBold,200,&H0040E0FF,&H000000FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,12,6,5,0,0,0,1
Style: Tag,Mukta Bold,46,&H00FFFFFF,&H000000FF,&H00305A9A,&H00305A9A,-1,0,0,0,100,100,0,0,3,10,0,1,70,0,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 2,0:00:08.95,0:00:13.40,TitleS,,0,0,0,,{\an5\pos(960,430)\fad(300,400)\t(0,400,\fscx100\fscy100)}गुलमोहर मोहल्ले का
Dialogue: 2,0:00:09.20,0:00:13.40,TitleB,,0,0,0,,{\an5\pos(960,560)\fad(250,400)\fscx70\fscy70\t(0,350,\fscx104\fscy104)\t(350,500,\fscx100\fscy100)}खज़ाना
Dialogue: 1,0:00:19.75,0:00:24.90,Riddle,,0,0,0,,{\fad(250,200)}गुलमोहर से सात कदम, पूरब की ओर चलो।\Nजहाँ पानी गीत गाए, वहाँ रुककर सुनो।
Dialogue: 1,0:00:25.85,0:00:31.70,Riddle,,0,0,0,,{\fad(250,250)}दो दीवारों के बीच, जहाँ बड़ा हाथ न जाए...\Nवहीं छुपा है ख़ज़ाना, जो दोस्ती निभाए।
Dialogue: 2,0:00:47.50,0:00:48.40,Count,,0,0,0,,{\an5\pos(1500,330)\fscx40\fscy40\t(0,140,\fscx110\fscy110)\t(140,240,\fscx100\fscy100)\fad(0,150)}1
Dialogue: 2,0:00:48.45,0:00:49.40,Count,,0,0,0,,{\an5\pos(1560,330)\fscx40\fscy40\t(0,140,\fscx110\fscy110)\t(140,240,\fscx100\fscy100)\fad(0,150)}2
Dialogue: 2,0:00:49.45,0:00:50.50,Count,,0,0,0,,{\an5\pos(1620,330)\fscx40\fscy40\t(0,140,\fscx110\fscy110)\t(140,240,\fscx100\fscy100)\fad(0,150)}3
Dialogue: 2,0:00:50.60,0:00:52.20,Count,,0,0,0,,{\an5\pos(1650,330)\c&H0030A0FF&\fscx40\fscy40\t(0,120,\fscx125\fscy125)\t(120,260,\fscx110\fscy110)\fad(0,200)}7!
Dialogue: 2,0:00:15.60,0:00:18.20,Tag,,0,0,0,,{\fad(200,250)}तारा
Dialogue: 2,0:00:32.20,0:00:34.80,Tag,,0,0,0,,{\fad(200,250)}टिंकू
Dialogue: 2,0:00:53.30,0:00:55.90,Tag,,0,0,0,,{\fad(200,250)}पांडे जी
Dialogue: 1,0:01:30.90,0:01:33.60,Riddle,,0,0,0,,{\fad(250,250)}जहाँ पानी गीत गाए...
Dialogue: 1,0:01:42.20,0:01:44.40,Riddle,,0,0,0,,{\fad(250,250)}जहाँ बड़ा हाथ न जाए...
"""

# sound design: (file, start s, gain dB)
SFX_EVENTS = [("magic_376747.mp3", 8.85, -14), ("paper_353125.mp3", 12.6, -12), ("paper_353125.mp3", 19.55, -14),
              ("whoosh_803771.mp3", 15.40, -20), ("whoosh_803771.mp3", 19.55, -20), ("whoosh_803771.mp3", 31.95, -20),
              ("whoosh_803771.mp3", 41.35, -20), ("whoosh_142348.mp3", 52.95, -17), ("whoosh_803771.mp3", 58.10, -20),
              ("magic_376745.mp3", 47.45, -22), ("magic_376745.mp3", 48.40, -22), ("magic_376745.mp3", 49.40, -22),
              ("magic_376747.mp3", 50.55, -16), ("comedy_sting_731262.mp3", 53.20, -14), ("run_816792.mp3", 57.05, -12),
              ("whoosh_803771.mp3", 68.25, -20), ("whoosh_803771.mp3", 76.35, -20), ("whoosh_803771.mp3", 79.20, -20),
              ("pump_832465.mp3", 85.40, -10), ("pump_832465.mp3", 86.55, -12), ("pump_832465.mp3", 87.60, -14),
              ("magic_376747.mp3", 90.85, -18), ("whoosh_803771.mp3", 93.95, -20), ("tension_sting_578351.mp3", 106.40, -16),
              ("comedy_sting_731261.mp3", 115.45, -17), ("whoosh_803771.mp3", 116.15, -20)]


def process_audio(dst: Path):
    ins = ["-ss", "0", "-t", str(DUR), "-i", str(WORK / "voice.wav"), "-ss", "0", "-t", str(DUR), "-i", str(WORK / "music.wav"),
           "-stream_loop", "-1", "-t", str(DUR), "-i", str(SFX / "birds_841386.mp3")]
    fl = ["[0:a]aresample=48000[v]", "[1:a]aresample=48000[m]",
          f"[2:a]aresample=48000,volume=-30dB,afade=t=in:d=1.5,afade=t=out:st={DUR - 1.5}:d=1.5[amb]"]
    mixin = ["[v]", "[m]", "[amb]"]
    for k, (f, st, g) in enumerate(SFX_EVENTS):
        ins += ["-i", str(SFX / f)]
        idx = 3 + k
        fl.append(f"[{idx}:a]aresample=48000,volume={g}dB,adelay={int(st * 1000)}|{int(st * 1000)}[s{k}]")
        mixin.append(f"[s{k}]")
    fl.append("".join(mixin) + f"amix=inputs={len(mixin)}:normalize=0:duration=first,"
              f"afade=t=out:st={DUR - 1.0}:d=1.0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[a]",
                    "-ar", "48000", "-ac", "2", str(dst)], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / "_work"
    (work / "fonts").mkdir(parents=True, exist_ok=True)
    for fnt in ("Mukta-ExtraBold.ttf", "Mukta-Bold.ttf"):
        shutil.copy(ROOT / "shared/fonts" / fnt, work / "fonts" / fnt)
    process_video(S / "long_04.mp4", work / "graded.mp4")
    (work / "titles.ass").write_text(ASS, encoding="utf-8")
    process_audio(work / "audio.wav")
    demo = OUT / "khazana_pro_demo.mp4"
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-i", "graded.mp4", "-i", "audio.wav", "-vf",
                    "subtitles=filename=titles.ass:fontsdir=fonts,format=yuv420p", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(demo)],
                   cwd=work, check=True)
    font = (ROOT / "shared/fonts/Mukta-Bold.ttf").as_posix().replace(":", r"\:")
    lab = lambda txt: (f"drawtext=fontfile='{font}':text='{txt}':x=20:y=20:fontsize=34:fontcolor=white:"
                       f"box=1:boxcolor=black@0.55:boxborderw=8")
    subprocess.run([str(FFMPEG), "-v", "error", "-y", "-t", str(DUR), "-i", str(S / "long_04.mp4"), "-i", str(demo),
                    "-filter_complex", f"[0:v]scale=960:540,{lab('PEHLE (abhi wala)')}[l];[1:v]scale=960:540,{lab('PRO EDIT (demo)')}[r];"
                    "[l][r]hstack=inputs=2,format=yuv420p[v]", "-map", "[v]", "-map", "1:a", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "20", "-c:a", "aac", "-shortest", str(OUT / "khazana_before_after.mp4")],
                   check=True)
    print("saved", demo)


if __name__ == "__main__":
    main()
