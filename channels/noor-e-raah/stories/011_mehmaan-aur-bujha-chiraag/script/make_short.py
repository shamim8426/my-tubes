"""Short (9:16) cut from this story's Long (SHORT_FROM_LONG.md). Rs0: reuses the Long's clips (work/cNN_*.mp4, no subs)
and the Long's final mixed audio (output/video.mp4), new 9:16 subtitles. Usage: python -X utf8 make_short.py [n n n ...]"""
import json, subprocess, sys, wave
from pathlib import Path
S = Path(__file__).resolve().parent.parent
ROOT = S.parents[3]
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
FONTS = ROOT / "shared/fonts"
PAD = 0.45
cfg = json.loads((S / "script.json").read_text(encoding="utf-8"))
L = cfg["lines"]
PICK = [int(x) for x in sys.argv[1:]] or [1, 15, 17, 21, 25, 28, 29, 30]
tempo = float(cfg.get("tempo", 1.0))
# Long timeline (same as history_build.py)
tl, t = {}, 0.0
for i, l in enumerate(L):
    with wave.open(str(S / f"audio/l{l['n']:02d}.wav")) as w:
        d = w.getnframes() / w.getframerate() / tempo + PAD + (0.8 if i == len(L) - 1 else 0)
    tl[l["n"]] = (l, t, d)
    t += d
W = S / "work_short"; W.mkdir(exist_ok=True)
out = S / "shorts"; out.mkdir(exist_ok=True)


def ts(x):
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


def esc(p):
    return Path(p).resolve().as_posix().replace(":", "\\:")


segs, T = [], 0.0
for n in PICK:
    l, st, d = tl[n]
    clip = next((S / "work").glob(f"c{n:02d}_*.mp4"))
    v = W / f"s{n:02d}.mp4"
    # 9:16: blurred full frame behind, the picture zoomed to 1200 px height in the middle (sides trimmed a little)
    vf = ("[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.12[bg];"
          "[b]scale=-2:1200,crop=1080:1200[fg];[bg][fg]overlay=0:330,fps=30,format=yuv420p")
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(clip), "-t", f"{d:.3f}", "-filter_complex", vf, "-an",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", str(v)], check=True)
    a = W / f"s{n:02d}.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{st:.3f}", "-t", f"{d:.3f}", "-i", str(S / "output/video.mp4"),
                    "-vn", "-af", f"afade=t=in:d=0.08,afade=t=out:st={max(0, d - 0.15):.3f}:d=0.15", "-ar", "48000", "-ac", "2", str(a)], check=True)
    segs.append((l, T, d, v, a))
    T += d
print("short length", round(T, 1), "s")
assert T < 59.5, "too long"
head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Sub,Mukta Bold,64,&H00FFFFFF,&H00FFFFFF,&H8C0A0C14,&H8C0A0C14,0,0,0,0,100,100,0,0,3,14,0,2,70,70,330,1\n"
        "Style: Ayah,Amiri,84,&H0078C8F0,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,3,3,8,60,60,0,0\n"
        "Style: Src,Mukta Bold,44,&H006EAAC8,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,8,0,0,0,1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
ev = []
for l, st, d, v, a in segs:
    s0, e = max(st, 1.0 if st == 0 else st), st + d - 0.05  # first 1 s without caption (cover frame = hook visual)
    txt = l["text"]
    for g in l.get("gold", []):
        txt = txt.replace(g, r"{\1c&H0078C8F0&}" + g + r"{\1c&HFFFFFF&}")
    if l.get("ayah"):
        ev.append(r"Dialogue: 0,%s,%s,Ayah,,0,0,0,,{\pos(540,420)\fad(300,200)}%s" % (ts(st), ts(e), cfg["ayah_ar"]))
        ev.append(r"Dialogue: 0,%s,%s,Src,,0,0,0,,{\pos(540,600)\fad(300,200)}%s" % (ts(st), ts(e), cfg.get("ayah_src", "")))
    if l.get("src") and not l.get("ayah"):
        ev.append(r"Dialogue: 0,%s,%s,Src,,0,0,0,,{\pos(540,1560)\fad(200,150)}%s" % (ts(s0), ts(e), l["src"]))
    ev.append(f"Dialogue: 0,{ts(s0)},{ts(e)},Sub,,0,0,0,,{txt}")
ev.append(r"Dialogue: 0,%s,%s,Src,,0,0,0,,{\pos(540,300)\fad(300,0)}पूरी कहानी: चैनल पर लंबी वीडियो" % (ts(T - 3.5), ts(T)))
(W / "subs.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
(W / "v.txt").write_text("".join(f"file '{x[3].as_posix()}'\n" for x in segs))
(W / "a.txt").write_text("".join(f"file '{x[4].as_posix()}'\n" for x in segs))
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(W / "a.txt"), "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000", str(W / "a.wav")], check=True)
r = subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(W / "v.txt"), "-i", str(W / "a.wav"),
                    "-filter_complex", f"[0:v]subtitles=filename='{esc(W / 'subs.ass')}':fontsdir='{esc(FONTS)}'[v]", "-map", "[v]", "-map", "1:a",
                    "-t", f"{T:.2f}", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(out / "short.mp4")], capture_output=True, text=True)
print("OK" if r.returncode == 0 else r.stderr[-800:], out / "short.mp4")
srt = []
for k, (l, st, d, v, a) in enumerate(segs, 1):
    srt.append(f"{k}\n{ts(st).replace('.', ',')} --> {ts(st + d - 0.05).replace('.', ',')}\n{l['text']}\n")
(out / "short.srt").write_text("\n".join(srt), encoding="utf-8")
