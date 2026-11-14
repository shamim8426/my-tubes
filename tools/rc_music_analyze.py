"""Objective features of music candidates (generic): tempo, onset density, spectral centroid, level + dynamics, repetitiveness (self-similarity), melodic/tonal proxy.
python tools/rc_music_analyze.py <folder or files...>   -> table sorted by 'energy'; CSV in cache.  Used to reject slow minimal loops / drones and to pick tracks with real dynamics.
Columns: dur s | bpm | onsets/s | centroid Hz | rms dBFS | dyn dB (p95-p05 of 2 s RMS) | rep (mean similarity of frames >10 s apart; 1.0 = same all through) | flat (spectral flatness; low = tonal) | low% (<150 Hz energy: drone risk)
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
SR = 22050


def feats(p):
    raw = subprocess.run([FF, "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    if len(x) < SR * 20:
        return None
    n, h = 2048, 512
    win = np.hanning(n)
    nf = (len(x) - n) // h
    idx = np.arange(n)[None, :] + h * np.arange(nf)[:, None]
    S = np.abs(np.fft.rfft(x[idx] * win, axis=1)) + 1e-9
    fr = np.fft.rfftfreq(n, 1 / SR)
    # onsets: positive spectral flux
    flux = np.maximum(np.diff(np.log1p(S * 50), axis=0), 0).sum(1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    pk = (flux[1:-1] > flux[:-2]) & (flux[1:-1] > flux[2:]) & (flux[1:-1] > 1.0)
    dens = pk.sum() / (len(x) / SR)
    # tempo from autocorrelation of flux (60-180 bpm)
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    fps = SR / h
    lo, hi = int(fps * 60 / 180), int(fps * 60 / 60)
    lag = lo + int(np.argmax(ac[lo:hi]))
    bpm = 60 * fps / lag
    cen = float((S * fr[None, :]).sum() / S.sum())
    # level and dynamics (2 s windows)
    w = SR * 2
    r = np.array([np.sqrt((x[i:i + w] ** 2).mean()) + 1e-9 for i in range(0, len(x) - w, w)])
    rdb = 20 * np.log10(r)
    dyn = float(np.percentile(rdb, 95) - np.percentile(rdb, 5))
    rms = float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9))
    # repetitiveness: 1 s band-energy vectors (28 log bands), cosine similarity of frames more than 10 s apart
    bands = np.geomspace(60, 8000, 29)
    seg = SR
    vecs = []
    for i in range(0, len(x) - seg, seg):
        Sp = np.abs(np.fft.rfft(x[i:i + seg] * np.hanning(seg))) ** 2
        f2 = np.fft.rfftfreq(seg, 1 / SR)
        vecs.append([np.log10(Sp[(f2 >= bands[b]) & (f2 < bands[b + 1])].sum() + 1e-9) for b in range(28)])
    V = np.array(vecs)
    V = V - V.mean(0)
    V /= (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
    Sim = V @ V.T
    m = len(V)
    far = np.abs(np.arange(m)[:, None] - np.arange(m)[None, :]) > 10
    rep = float(Sim[far].mean()) if far.any() else 1.0
    flat = float(np.median(np.exp(np.log(S[:, 5:700]).mean(1)) / S[:, 5:700].mean(1)))
    low = float(100 * (S[:, fr < 150] ** 2).sum() / (S ** 2).sum())
    return dict(dur=len(x) / SR, bpm=bpm, dens=dens, cen=cen, rms=rms, dyn=dyn, rep=rep, flat=flat, low=low)


def main():
    files = []
    for a in sys.argv[1:]:
        p = Path(a)
        files += sorted(p.glob("*.mp3")) if p.is_dir() else [p]
    rows = []
    for p in files:
        f = feats(p)
        if f:
            f["name"] = p.stem
            rows.append(f)
    rows.sort(key=lambda r: r["dens"] * 10 ** (r["rms"] / 20))
    print(f"{'track':28s} {'dur':>4s} {'bpm':>4s} {'ons/s':>5s} {'cent':>5s} {'rms':>5s} {'dyn':>4s} {'rep':>5s} {'flat':>5s} {'low%':>4s}")
    for r in rows:
        print(f"{r['name'][:28]:28s} {r['dur']:4.0f} {r['bpm']:4.0f} {r['dens']:5.2f} {r['cen']:5.0f} {r['rms']:5.1f} {r['dyn']:4.1f} {r['rep']:5.2f} {r['flat']:5.2f} {r['low']:4.0f}")


if __name__ == "__main__":
    main()
