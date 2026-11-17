"""008 Al-Fil Short (9:16), cut from the Long's final video (SHORT_FROM_LONG.md, Rs0): hook line 3 -> the complete
ayah 105:5 (both jumla blocks, RULES 2b: whole ayah, nothing cut) -> seekh line 63. The Long's picture (its own Arabic
= Tanzil bytes, drawn by the Long's renderer; the Long's bottom caption band cropped away) sits in the middle over a
blurred copy; big Hindi subtitles from the Long's own .srt in the 15-85% band; the Long's mix, -14 LUFS.
    .venv/Scripts/python -X utf8 channels/noor-e-raah/stories/008_al-fil/script/make_short.py
"""
import json
import re
import subprocess
from pathlib import Path

S = Path(__file__).resolve().parent.parent
ROOT = S.parents[3]
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
FONTS = ROOT / "shared/fonts"
LONG = S / "long/output/008_al-fil_final.mp4"
tl = json.loads((S / "long/output/timeline.json").read_text(encoding="utf-8"))
st = {l["n"]: (l["start"], l["end"]) for l in tl["lines"]}
fade = tl["fade_at"]
SEGS = [  # (from, to) in Long seconds
    (0.0, st[4][0] - 0.25),                 # title card + hook line 3
    (max(float(fade["10"] if "10" in fade else fade[10]) - 0.4, st[52][1] + 0.15), st[63][0] - 0.3),  # 105:5 complete (ayah blocks 10 + 11)
    (st[63][0] - 0.3, min(st[63][1] + 0.6, st[64][0] - 0.15)),  # first lesson, never into line 64
]
W = S / "work_short"
W.mkdir(exist_ok=True)
OUT = S / "shorts"
OUT.mkdir(exist_ok=True)


def ts(x):
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


def esc(p):
    return Path(p).resolve().as_posix().replace(":", "\\:")


def srt_cues(p):
    cues = []
    for blk in p.read_text(encoding="utf-8").strip().split("\n\n"):
        ln = blk.strip().splitlines()
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)", ln[1])
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append((a, b, " ".join(ln[2:])))
    return cues


cues = srt_cues(S / "long/output/008_al-fil.srt")
parts, events, T = [], [], 0.0
for k, (a, b) in enumerate(SEGS):
    d = b - a
    v = W / f"seg{k}.mp4"
    # Long frame: drop the bottom caption band (top 74 %, middle 80 %), scale to width 1080, centre over a blurred full-height copy
    cw = 1.0 if k == 2 else 0.8  # the seekh card sits top-left in the Long: keep the full width there
    vf = (f"[0:v]crop=iw*{cw}:ih*0.74:iw*{(1 - cw) / 2}:0,split[x][y];"
          "[x]scale=-2:1920,crop=1080:1920,boxblur=28:2,"
          "eq=brightness=-0.15[bg];[y]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2-120,fps=30,format=yuv420p")
    af = f"afade=t=in:d=0.12,afade=t=out:st={max(0, d - 0.25):.3f}:d=0.25"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(LONG),
                    "-filter_complex", vf, "-af", af, "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(v)], check=True)
    parts.append(v)
    for (ca, cb, txt) in cues:
        if min(cb, b) - max(ca, a) < 0.6:  # a cue that only grazes the cut = a neighbour line, not in this Short
            continue
        s0, s1 = max(ca, a) - a + T, min(cb, b) - a + T
        if T == 0 and s0 < 1.0:
            s0 = 1.0  # first 1 s without caption: the cover frame is the hook visual
        events.append((s0, s1, re.sub(r"\s+", " ", txt)))
    T += d
print("short length", round(T, 1), "s")
assert 35 <= T < 59.5, T
head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
        "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding\n"
        "Style: Sub,Mukta Bold,66,&H00FFFFFF,&H00FFFFFF,&H8C0A0C14,&H8C0A0C14,0,0,0,0,100,100,0,0,3,14,0,2,70,70,520,1\n"
        "Style: Top,Mukta Bold,58,&H0078C8F0,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,3,1,8,60,60,330,1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
ev = [f"Dialogue: 0,{ts(1.0)},{ts(T - 3.6)},Top,,0,0,0,,सूरह अल-फ़ील · 105"]
ev += [f"Dialogue: 0,{ts(a)},{ts(b - 0.05)},Sub,,0,0,0,,{t}" for a, b, t in events]
ev.append(r"Dialogue: 0,%s,%s,Top,,0,0,0,,{\fad(300,0)}पूरी सूरह का मतलब: चैनल पर लंबी वीडियो" % (ts(T - 3.5), ts(T)))
(W / "subs.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
(W / "list.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in parts))
r = subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(W / "list.txt"),
                    "-filter_complex", f"[0:v]subtitles=filename='{esc(W / 'subs.ass')}':fontsdir='{esc(FONTS)}'[v];"
                    "[0:a]loudnorm=I=-14:TP=-1.5:LRA=9[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", str(OUT / "short.mp4")], capture_output=True, text=True)
print("OK" if r.returncode == 0 else r.stderr[-800:], OUT / "short.mp4")


def f(m):
    m = int(round(m * 1000))
    return f"00:{m // 60000:02d}:{m // 1000 % 60:02d},{m % 1000:03d}"


(OUT / "short.srt").write_text("\n".join(f"{i}\n{f(a)} --> {f(b - 0.05)}\n{t}\n" for i, (a, b, t) in enumerate(events, 1)),
                               encoding="utf-8")
