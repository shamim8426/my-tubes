"""Beat helper (idea from librosa, ISC licence; own code). Use: beats = beat_times(mp3, start, dur); t2 = snap(t, beats, tol=0.14).
Rule: snap only VISUAL events (card pops, banners, chips) to the nearest beat within tol seconds; never move voice."""
import json, sys
from pathlib import Path
import numpy as np


def beat_times(mp3, start=0.0, dur=70.0, out_json=None):
    import librosa
    y, sr = librosa.load(str(mp3), sr=22050, mono=True, offset=start, duration=dur)
    tempo, bf = librosa.beat.beat_track(y=y, sr=sr, units="frames", tightness=120)
    bt = librosa.frames_to_time(bf, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    res = {"tempo": round(tempo, 2), "beats": [round(float(b), 3) for b in bt]}
    if out_json: Path(out_json).write_text(json.dumps(res), encoding="utf-8")
    return res


def snap(t, beats, tol=0.14):
    b = np.asarray(beats, dtype=float)
    if not len(b): return t
    i = int(np.argmin(np.abs(b - t)))
    return float(b[i]) if abs(b[i] - t) <= tol else t


def pulse(t, beats, width=0.16):
    """0..1 spike right after each beat (for a tiny scale pulse)."""
    b = np.asarray(beats, dtype=float); d = t - b; d = d[(d >= 0) & (d < width)]
    return float(1 - d[0] / width) if len(d) else 0.0


if __name__ == "__main__":
    r = beat_times(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]); print(r["tempo"], len(r["beats"]), r["beats"][:12])
