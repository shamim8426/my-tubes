"""Old flat-cartoon look vs Kissago Painted, both with 2.5D parallax (6 s each). Output: style_tests/painted/compare.mp4"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import parallax as P  # noqa: E402

OUT = ROOT / "style_tests/painted"
FONT = (ROOT / "shared/fonts/Mukta-Bold.ttf").as_posix().replace(":", r"\:")
PAIRS = [  # (label, old image, new image, preset, overlays)
    ("A - shaam ka aangan", ROOT / "channels/dadi-ki-kahaniyan/brand/_work/banner_art.png", OUT / "scene_A.png",
     "pull_out", [("dust", 0.18, (0.5, 0.6))]),
    ("B - raat ki chhat", ROOT / "channels/dadi-ki-kahaniyan/stories/004_chhat-par-bhoot/images/scene_16.png",
     OUT / "scene_B.png", "push_in", [("fireflies", 0.22, (0.5, 0.6))]),
]
report, parts = [], []
for i, (label, old, new, preset, ovs) in enumerate(PAIRS):
    a = P.render_clip(old, OUT / f"old_{i}.mp4", 6, preset, "long", overlays=ovs)
    b = P.render_clip(new, OUT / f"new_{i}.mp4", 6, preset, "long", overlays=ovs)
    report += [a, b]
    lab = lambda t: (f"drawtext=fontfile='{FONT}':text='{t}':x=18:y=18:fontsize=34:fontcolor=white:"
                     f"box=1:boxcolor=black@0.55:boxborderw=8")
    fc = (f"[0:v]scale=960:540,{lab('PURANA LOOK')}[l];[1:v]scale=960:540,{lab('KISSAGO PAINTED')}[r];"
          f"[l][r]hstack=inputs=2,drawtext=fontfile='{FONT}':text='{label}':x=(w-tw)/2:y=h-46:fontsize=26:"
          f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=6,format=yuv420p[out]")
    part = OUT / f"compare_{i}.mp4"
    subprocess.run([str(P.FFMPEG), "-v", "error", "-y", "-i", str(OUT / f"old_{i}.mp4"), "-i", str(OUT / f"new_{i}.mp4"),
                    "-filter_complex", fc, "-map", "[out]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    str(part)], check=True)
    parts.append(part)
    print(label, "| old:", a["mode"], a["amp"], a["reason"], "| new:", b["mode"], b["amp"], b["reason"],
          f"| new clip wall {b['wall_s']}s")
(OUT / "list.txt").write_text("\n".join(f"file '{p.as_posix()}'" for p in parts), encoding="utf-8")
subprocess.run([str(P.FFMPEG), "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(OUT / "list.txt"), "-c", "copy",
                str(OUT / "compare.mp4")], check=True)
(OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
