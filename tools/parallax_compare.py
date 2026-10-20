"""Side-by-side test: old make_short zoom vs new 2.5D parallax (tools/parallax.py), story 004 images.

    python tools/parallax_compare.py
Output: style_tests/parallax/compare_<scene>.mp4 (each 1920x540: left old zoom, right parallax),
        style_tests/parallax/compare_all.mp4, style_tests/parallax/short_<scene>.mp4 (9:16 check),
        style_tests/parallax/report.json (decisions + CPU time per clip)
"""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parallax as P  # noqa: E402

ROOT = P.ROOT
IMG = ROOT / "channels/dadi-ki-kahaniyan/stories/004_chhat-par-bhoot/images"
OUT = ROOT / "style_tests/parallax"
FONT = (ROOT / "shared/fonts/Mukta-Bold.ttf").as_posix().replace(":", r"\:")
SECS = 6.0
TESTS = [  # scene, kind of image, mood -> preset, overlays
    ("scene_02", "raat, wide, chhat + chaand", "tension", [("fireflies", 0.25, (0.5, 0.6))]),
    ("scene_04", "raat, andar, Dadi + Golu + Mitthu (pankh, baal)", "tension", [("dust", 0.18, (0.5, 0.6))]),
    ("scene_05", "din, gali, 3 kirdaar + ped", "comedy", []),
    ("scene_06", "din, Pandey lathi + Mitthu ude pankh", "khushi", []),
]


def old_zoom(img, out):
    """Exactly make_short's 'in' wide move (RENDER_VERSION 3): 2x scale, zoompan 1 -> 1.08 over the shot."""
    n = int(SECS * 30)
    fc = (f"[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
          f"zoompan=z='1+0.08*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s=1920x1080:fps=30,"
          f"scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[out]")
    subprocess.run([str(P.FFMPEG), "-v", "error", "-y", "-i", str(img), "-filter_complex", fc, "-map", "[out]",
                    "-frames:v", str(n), "-c:v", "libx264", "-preset", "slow", "-crf", "18", str(out)], check=True)


def side_by_side(a, b, out, label):
    lab = lambda t, x: (f"drawtext=fontfile='{FONT}':text='{t}':x={x}:y=18:fontsize=34:fontcolor=white:"
                        f"box=1:boxcolor=black@0.55:boxborderw=8")
    fc = (f"[0:v]scale=960:540,{lab('ZOOM (purana)', 18)}[l];[1:v]scale=960:540,{lab('PARALLAX (naya)', 18)}[r];"
          f"[l][r]hstack=inputs=2,drawtext=fontfile='{FONT}':text='{label}':x=(w-tw)/2:y=h-46:fontsize=26:"
          f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=6,format=yuv420p[out]")
    subprocess.run([str(P.FFMPEG), "-v", "error", "-y", "-i", str(a), "-i", str(b), "-filter_complex", fc,
                    "-map", "[out]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", str(out)], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report, prev, parts = [], None, []
    for sc, kind, mood, ovs in TESTS:
        img = IMG / f"{sc}.png"
        preset = P.choose_preset(mood, prev)
        prev = preset
        t = time.time()
        old_zoom(img, OUT / f"old_{sc}.mp4")
        t_old = time.time() - t
        res = P.render_clip(img, OUT / f"new_{sc}.mp4", SECS, preset, "long", overlays=ovs)
        res.update({"kind": kind, "mood": mood, "old_zoom_wall_s": round(t_old, 1)})
        report.append(res)
        side_by_side(OUT / f"old_{sc}.mp4", OUT / f"new_{sc}.mp4", OUT / f"compare_{sc}.mp4",
                     f"{sc} - {preset} - {res['mode']}")
        parts.append(OUT / f"compare_{sc}.mp4")
        print(f"{sc}: {preset:14s} {res['mode']:8s} amp {res['amp']}  cpu {res['cpu_s']}s  wall {res['wall_s']}s "
              f"(old zoom wall {t_old:.1f}s)  {res['reason']}", flush=True)
    (OUT / "list.txt").write_text("\n".join(f"file '{p.as_posix()}'" for p in parts), encoding="utf-8")
    subprocess.run([str(P.FFMPEG), "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(OUT / "list.txt"),
                    "-c", "copy", str(OUT / "compare_all.mp4")], check=True)
    # 9:16 check (Short format), Golu + Mitthu side of scene 04 (cx 0.64: finger out of the right 15%)
    res = P.render_clip(IMG / "scene_04.png", OUT / "short_scene_04.mp4", SECS, "push_in", "short", cx=0.64)
    res.update({"kind": "Short 9:16 crop", "mood": "tension"})
    report.append(res)
    print(f"short scene_04: {res['mode']} cpu {res['cpu_s']}s wall {res['wall_s']}s")
    (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
