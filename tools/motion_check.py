"""Frame-to-frame smoothness check for camera moves (user 2026-10-25: no shake).

    python tools/motion_check.py <video.mp4> [--from S] [--frames N] [--patch X,Y]
    python tools/motion_check.py --compare <image>          # zoompan 2x / zoompan 4x / warpAffine linear / cubic

For each pair of consecutive frames the shift of a patch is measured with sub-pixel phase correlation. A smooth
eased move gives a smooth shift curve; integer-pixel stepping shows up as jerk (the shift jumping up and down).
Reported: jerk = RMS of the 2nd difference of the shift (px/frame²) and max |step change|. Lower is smoother;
a clean eased move is ~0.01-0.05, integer stepping is ~0.3-0.7.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FF = next(str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists())


def read_frames(video, start=0.0, n=60, w=1920, h=1080):
    raw = subprocess.run([FF, "-v", "error", "-ss", str(start), "-i", str(video), "-frames:v", str(n), "-f", "rawvideo",
                          "-pix_fmt", "gray", "-s", f"{w}x{h}", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w)


def shifts(frames, px=0.25, py=0.25, size=384):
    h, w = frames.shape[1:]
    x0, y0 = int(px * w - size / 2), int(py * h - size / 2)
    win = cv2.createHanningWindow((size, size), cv2.CV_64F)
    out = []
    for a, b in zip(frames[:-1], frames[1:]):
        pa = a[y0:y0 + size, x0:x0 + size].astype(np.float64)
        pb = b[y0:y0 + size, x0:x0 + size].astype(np.float64)
        (dx, dy), _ = cv2.phaseCorrelate(pa, pb, win)
        out.append((dx, dy))
    return np.array(out)


def score(frames, px=0.25, py=0.25):
    s = shifts(frames, px, py)
    mag = np.hypot(s[:, 0], s[:, 1])
    d2 = np.diff(s, n=2, axis=0)
    return {"frames": len(frames), "mean_shift_px": round(float(mag.mean()), 3),
            "jerk_rms": round(float(np.sqrt((d2 ** 2).sum(axis=1).mean())), 4),
            "max_step_change": round(float(np.abs(np.diff(mag)).max()), 3),
            "shift_x": [round(float(v), 3) for v in s[:12, 0]]}


def ease(p):
    return 0.5 - 0.5 * np.cos(np.pi * p)


def compare(image, out_dir, n=210, W=1920, H=1080):
    out_dir.mkdir(parents=True, exist_ok=True)
    res = {}
    zexpr = f"1+0.07*(0.5-0.5*cos(PI*on/{n - 1}))"
    for name, up in (("zoompan_2x", 2), ("zoompan_4x", 4)):
        f = out_dir / f"{name}.mp4"
        subprocess.run([FF, "-v", "error", "-y", "-loop", "1", "-i", str(image), "-vf",
                        f"scale={W * up}:{H * up}:force_original_aspect_ratio=increase:flags=lanczos,crop={W * up}:{H * up},"
                        f"zoompan=z='{zexpr}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={W}x{H}:fps=30",
                        "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", str(f)], check=True)
        res[name] = score(read_frames(f, 0, n))
    img = cv2.imread(str(image))
    ih, iw = img.shape[:2]
    s = max(W * 1.0 / iw, H * 1.0 / ih)
    for name, interp, sup in (("warp_linear", cv2.INTER_LINEAR, 1), ("warp_cubic", cv2.INTER_CUBIC, 1),
                              ("warp_cubic_ss2", cv2.INTER_CUBIC, 2)):
        src = cv2.resize(img, (int(round(iw * s * sup)), int(round(ih * s * sup))), interpolation=cv2.INTER_LANCZOS4)
        sh, sw = src.shape[:2]
        frames = []
        for i in range(n):
            z = 1 + 0.07 * ease(i / (n - 1))
            M = np.float32([[z, 0, (1 - z) * sw / 2 - (sw - W * sup) / 2], [0, z, (1 - z) * sh / 2 - (sh - H * sup) / 2]])
            fr = cv2.warpAffine(src, M, (W * sup, H * sup), flags=interp, borderMode=cv2.BORDER_REFLECT)
            if sup > 1:
                fr = cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA)
            frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY))
        res[name] = score(np.array(frames))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", nargs="?")
    ap.add_argument("--compare")
    ap.add_argument("--from", dest="start", type=float, default=0.0)
    ap.add_argument("--frames", type=int, default=60)
    ap.add_argument("--patch", default="0.25,0.25")
    a = ap.parse_args()
    if a.compare:
        out = Path(a.compare).parent / "_motion_compare"
        print(json.dumps(compare(Path(a.compare), out), indent=1))
        return
    px, py = (float(v) for v in a.patch.split(","))
    print(json.dumps(score(read_frames(a.video, a.start, a.frames), px, py)))


if __name__ == "__main__":
    sys.exit(main())
