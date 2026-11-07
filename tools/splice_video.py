"""Replace one time range of a finished video with a re-rendered part (frame accurate, audio untouched).
Use after a review finds a mistake: re-render ONLY the broken range with the builder's `range` mode, then splice.
    python tools/splice_video.py <orig.mp4> <part.mp4> <t0_seconds> <t1_seconds> <out.mp4> [--fps 30]
The part must be video only, same size/fps as the original, covering exactly t0..t1. The original audio (voice + music) is copied as is.
ffmpeg must be on PATH (PC: <root>\tools\ffmpeg)."""
import subprocess, sys
from pathlib import Path


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    fps = 30
    if "--fps" in sys.argv: fps = int(sys.argv[sys.argv.index("--fps") + 1]); a = [x for x in a if x != str(fps)]
    orig, part, t0, t1, out = a[0], a[1], float(a[2]), float(a[3]), a[4]
    n0, n1 = int(round(t0 * fps)), int(round(t1 * fps))
    fc = (f"[0:v]trim=start_frame=0:end_frame={n0},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];"
          f"[0:v]trim=start_frame={n1},setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", orig, "-i", part, "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-r", str(fps), "-c:a", "copy", out]
    subprocess.run(cmd, check=True); print("spliced", out)


main()
