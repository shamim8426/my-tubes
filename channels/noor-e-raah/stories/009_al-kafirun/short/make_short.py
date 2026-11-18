"""Short cut from the 009 Long (SHORT_FROM_LONG.md, surah rule: consecutive ayat 1-3 = lines 12-21, Rs0).
9:16: the Long frame's upper part (Arabic + ucharan, no Long subtitle band) scaled into the middle over a blurred copy;
own Hindi captions (non-ayah lines only; ayah lines already show Arabic + ucharan) inside 15-85% height; Long's own mix.
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/009_al-kafirun/short/make_short.py
"""
import json
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
S = Path(__file__).resolve().parents[1]
cfg = json.loads((S / "script.json").read_text(encoding="utf-8"))
PAD = 0.45
A, B = 12, 21
t, T = 0.0, {}
for i, l in enumerate(cfg["lines"]):
    with wave.open(str(S / f"audio/l{l['n']:02d}.wav")) as w:
        d = w.getnframes() / w.getframerate() / cfg["tempo"] + PAD + (0.8 if i == len(cfg["lines"]) - 1 else 0)
    T[l["n"]] = (t, t + d, l)
    t += d
t0, t1 = T[A][0], T[B][1] - 0.02  # last word ends ~0.35 s before T[B][1]; next line's voice starts +0.1 s


def ts(x):
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


ev, srt = [], []
for k, n in enumerate(range(A, B + 1), 1):
    s, e, l = T[n]
    s, e = s - t0, min(e, t1) - t0 - 0.05
    if not l.get("ayah"):
        txt = l["text"]
        for g in l.get("gold", []):
            txt = txt.replace(g, r"{\1c&H0078C8F0&}" + g + r"{\1c&HFFFFFF&}")
        ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{txt}")
    ms = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x * 1000)) % 1000:03d}"  # noqa: E731
    srt.append(f"{k}\n{ms(s)} --> {ms(e)}\n{l['text']}\n")
ev.append(r"Dialogue: 0,0:00:00.00,%s,Tag,,0,0,0,,सूरह अल-काफ़िरून 109:1-3" % ts(t1 - t0))
ass = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
       "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
       "Style: Cap,Mukta Bold,66,&H00FFFFFF,&H00FFFFFF,&H8C0A0C14,&H8C0A0C14,0,0,0,0,100,100,0,0,3,14,0,2,170,170,400,1\n"
       "Style: Tag,Mukta Bold,52,&H0078C8F0,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,3,1,8,60,60,330,1\n\n"
       "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n" + "\n".join(ev) + "\n")
O = S / "short/output"
O.mkdir(parents=True, exist_ok=True)
(S / "short/subs.ass").write_text(ass, encoding="utf-8")
(O / "short.srt").write_text("\n".join(srt), encoding="utf-8")
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
fd = str(ROOT / "shared/fonts").replace("\\", "/").replace(":", r"\:")
sub = str(S / "short/subs.ass").replace("\\", "/").replace(":", r"\:")
dur = t1 - t0
fc = ("[0:v]split[a][b];[a]crop=1920:560:0:330,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=45,eq=brightness=-0.18[bg];"
      "[b]crop=1240:930:340:0,scale=1080:810[fg];[bg][fg]overlay=0:470[v1];"
      f"[v1]subtitles=filename='{sub}':fontsdir='{fd}'[v]")
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", str(S / "output/video.mp4"),
                "-filter_complex", fc + f";[0:a]afade=t=in:d=0.3,afade=t=out:st={dur - 0.3:.2f}:d=0.3,loudnorm=I=-14:TP=-1.5:LRA=9[aa]",
                "-map", "[v]", "-map", "[aa]", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-r", "30", "-movflags", "+faststart", str(O / "short.mp4")], check=True)
print("ok", round(dur, 1), "s", t0, t1)
subprocess.run([FF, "-loglevel", "error", "-y", "-ss", "1.0", "-i", str(O / "short.mp4"), "-frames:v", "1", "-q:v", "2", str(O / "cover.jpg")], check=True)
