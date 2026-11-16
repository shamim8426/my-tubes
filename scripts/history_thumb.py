"""History thumbnail (1280x720) from a story image + Hindi hook text via libass.
    .venv\\Scripts\\python -X utf8 scripts\\history_thumb.py <story dir> <image id> "<line 1>" "<line 2>" "<small tag>"
Output: <story dir>/output/thumbnail.jpg"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = Path(sys.argv[1]).resolve()
img, l1, l2, tag = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
W = D / "work"
W.mkdir(exist_ok=True)
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Big,Mukta Bold,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,7,4,2,40,40,0,1
Style: Gold,Mukta Bold,128,&H0078C8F0,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,7,4,2,40,40,0,1
Style: Tag,Mukta Bold,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,3,10,0,8,40,40,36,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,Tag,,0,0,0,,{{\\pos(640,50)\\an8\\1c&H0078C8F0&\\3c&H10202A&}}{tag}
Dialogue: 0,0:00:00.00,0:00:05.00,Big,,0,0,0,,{{\\pos(640,520)\\an2}}{l1}
Dialogue: 0,0:00:00.00,0:00:05.00,Gold,,0,0,0,,{{\\pos(640,680)\\an2}}{l2}
"""
(W / "thumb.ass").write_text(ass, encoding="utf-8")


def esc(p):
    return Path(p).resolve().as_posix().replace(":", "\\:")


vf = ("scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=contrast=1.15:saturation=1.3:brightness=0.02,"
      "drawbox=x=0:y=430:w=1280:h=290:color=black@0.22:t=fill,"
      f"subtitles=filename='{esc(W / 'thumb.ass')}':fontsdir='{esc(ROOT / 'shared/fonts')}'")
out = D / "output/thumbnail.jpg"
r = subprocess.run([str(ROOT / "tools/ffmpeg/ffmpeg.exe"), "-y", "-loglevel", "error", "-loop", "1", "-t", "1", "-i",
                    str(D / f"images/{img}.png"), "-vf", vf, "-frames:v", "1", "-q:v", "2", str(out)], capture_output=True, text=True)
print("OK" if r.returncode == 0 else r.stderr[-500:], out)
