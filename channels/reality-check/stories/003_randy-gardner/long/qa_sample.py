"""QA of output/003_sample_60s.mp4: frames at every line midpoint (contact sheet), black frames, A/V sync vs voiceover_full.wav, durations."""
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
ROOT = HERE.parents[4]
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
V = HERE / "output/003_sample_60s.mp4"
T = json.loads((HERE.parent / "audio/voiceover_timing.json").read_text(encoding="utf-8"))


def grab(t):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.2f}", "-i", str(V), "-frames:v", "1", "-vf", "scale=480:270", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (480, 270), raw)


sheet = Image.new("RGB", (480 * 4, 270 * 2), "black")
d = ImageDraw.Draw(sheet)
for i, l in enumerate(T):
    m = (l["start"] + l["end"]) / 2
    sheet.paste(grab(m), ((i % 4) * 480, (i // 4) * 270))
    d.text(((i % 4) * 480 + 6, (i // 4) * 270 + 250), f"L{l['line']} {m:.1f}s", fill="yellow")
sheet.save(HERE / "review/sample_line_midpoints.jpg", quality=85)
e = subprocess.run([FF, "-hide_banner", "-i", str(V), "-vf", "blackdetect=d=0.1:pix_th=0.06", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
print("black frames:", [x for x in e.splitlines() if "black_start" in x] or "none")


def env(path, sr=8000):
    x = np.frombuffer(subprocess.run([FF, "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    n = len(x) // 80
    return np.sqrt((x[: n * 80].reshape(n, 80) ** 2).mean(1))


a, b = env(V), env(HERE.parent / "audio/voiceover_full.wav")
n = min(len(a), len(b))
a0, b0 = a[:n] - a[:n].mean(), b[:n] - b[:n].mean()
best = max(range(-50, 51), key=lambda k: float(np.dot(a0[max(k, 0): n + min(k, 0)], b0[max(-k, 0): n - max(k, 0)])))
print(f"A/V: voice offset in the video vs voiceover_full.wav = {best * 10} ms (100 Hz envelope xcorr)")
p = subprocess.run([FF, "-hide_banner", "-i", str(V)], capture_output=True, text=True).stderr
print([x.strip() for x in p.splitlines() if "Duration" in x or "Stream" in x])
