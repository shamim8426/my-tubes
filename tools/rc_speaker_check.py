"""Speaker-simulated audibility check of a Long's music vs voice (150 Hz - 8 kHz band, like a phone/laptop speaker) next to the full-band numbers.
python tools/rc_speaker_check.py 002 [--win 30]
Reads cache/reality-check/<story>/music/music_only.wav (music without booms) + audio/voiceover_full.wav. Prints per-window: voice LUFS (band), music LUFS (band), difference, full-band difference, music in gaps."""
import argparse
import json
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import rc_sound as RS  # noqa: E402

SR = RS.SR


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--win", type=int, default=30)
    a = ap.parse_args()
    sd = next((ROOT / "channels/reality-check/stories").glob(a.story + "_*"))
    w = wave.open(str(ROOT / "cache/reality-check" / a.story / "music/music_only.wav"))
    m = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, 2).mean(1).astype(np.float32) / 32768
    v = RS.load_audio(sd / "audio/voiceover_full.wav", 1)[:, 0]
    v = np.pad(v, (0, max(0, len(m) - len(v))))[: len(m)]
    lines = json.loads((sd / "audio/voiceover_timing.json").read_text(encoding="utf-8"))
    sp = np.zeros(len(m), bool)
    for l in lines:
        sp[int(l["start"] * SR): int(l["end"] * SR)] = True
    gap = ~sp
    vb = RS.fft_filter(v, lo=150, hi=8000)
    mb = RS.fft_filter(m, lo=150, hi=8000)
    print(f"{'window':>9s} {'voice_band':>10s} {'music_band':>10s} {'diff_band':>9s} {'diff_full':>9s} {'gap_diff':>8s}  (LU/LUFS; diff = music - voice, speech frames; gap_diff = music in pauses vs speech voice)")
    diffs = []
    for t in range(0, len(m) // SR, a.win):
        i, j = t * SR, min((t + a.win) * SR, len(m))
        s, g = sp[i:j], gap[i:j]
        if s.sum() < SR:
            continue
        vbl, mbl = RS.lufs(vb[i:j][s]), RS.lufs(mb[i:j][s])
        full = RS.lufs(m[i:j][s]) - RS.lufs(v[i:j][s])
        gd = (RS.lufs(mb[i:j][g]) - vbl) if g.sum() > SR // 2 else float("nan")
        diffs.append(mbl - vbl)
        print(f"{t:4d}-{t + a.win:<4d} {vbl:10.1f} {mbl:10.1f} {mbl - vbl:9.1f} {full:9.1f} {gd:8.1f}")
    print(f"band diff: median {np.median(diffs):.1f} LU, range {min(diffs):.1f}..{max(diffs):.1f}")
    tot = np.abs(np.fft.rfft(m[: 2 ** 22])) ** 2
    f = np.fft.rfftfreq(2 ** 22, 1 / SR)
    print("music-only energy share: <150 Hz %.0f%%, 150-2k %.0f%%, 2-8k %.1f%%" % tuple(100 * tot[(f >= lo) & (f < hi)].sum() / tot.sum() for lo, hi in ((0, 150), (150, 2000), (2000, 8000))))


if __name__ == "__main__":
    main()
