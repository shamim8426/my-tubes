import json, re, subprocess, wave
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
S = Path(__file__).resolve().parents[1]
cfg = json.loads((S / "script.json").read_text(encoding="utf-8"))
PAD = 0.45
t = 0.0
T = {}
for l in cfg["lines"]:
    w = wave.open(str(S / f"audio/l{l['n']:02d}.wav"))
    d = w.getnframes() / w.getframerate() / cfg["tempo"] + PAD
    T[l["n"]] = (t, t + d, l)
    t += d
A, B = 10, 17  # consecutive lines for the Short
t0, t1 = T[A][0], T[B][1] - 0.2
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
ev = []
for n in range(A, B + 1):
    s, e, l = T[n]
    ev.append(f"Dialogue: 0,{ts(s - t0)},{ts(min(e, t1) - t0 - 0.05)},Cap,,0,0,0,,{l['text']}")
ass = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\n"
       "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
       "Style: Cap,Mukta Bold,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,2,2,70,70,330,1\n\n"
       "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n" + "\n".join(ev) + "\n")
(S / "short/subs.ass").write_text(ass, encoding="utf-8")
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
fd = str(ROOT / "shared/fonts").replace("\\", "/").replace(":", r"\:")
sub = str(S / "short/subs.ass").replace("\\", "/").replace(":", r"\:")
dur = t1 - t0
fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=45,eq=brightness=-0.15[bg];"
      "[b]crop=800:930:560:0,scale=1080:1256[fg];[bg][fg]overlay=0:150[v1];"
      f"[v1]subtitles=filename='{sub}':fontsdir='{fd}'[v]")
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", str(S / "output/video_pre.mp4"),
                "-filter_complex", fc + f";[0:a]volume=1.9dB,alimiter=limit=0.84:level=false,afade=t=in:d=0.3,afade=t=out:st={dur-0.7:.2f}:d=0.6[aa]",
                "-map", "[v]", "-map", "[aa]", "-c:v", "libx264", "-crf", "21", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-r", "30", str(S / "short/output/short.mp4")], check=True)
print("ok", round(dur, 1))
