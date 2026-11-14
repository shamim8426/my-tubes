"""Pick a single beatless dark ambient bed by measured features (generic).
python tools/rc_music_pick.py <files or dirs...>  -> table sorted by 'score' (higher = more beatless / steady / dark)
Columns: tempo_conf (autocorr peak of onset flux at 60-180 bpm / lag 0; low = no beat) | ons/s | centroid Hz | dyn dB (p95-p05 of 2 s RMS, low = steady) | sim (mean cosine similarity of 1 s spectra >10 s apart, uncentred; ~0.8-0.95 = same all through) | pitched (stability of the strongest spectral peak = melody proxy, low = no melody)"""
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
SR = 22050


def feats(p, maxsec=240):
    raw = subprocess.run([FF, "-v", "error", "-i", str(p), "-t", str(maxsec), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    if len(x) < SR * 40:
        return None
    n, h = 2048, 512
    win = np.hanning(n)
    nf = (len(x) - n) // h
    idx = np.arange(n)[None, :] + h * np.arange(nf)[:, None]
    S = np.abs(np.fft.rfft(x[idx] * win, axis=1)) + 1e-9
    fr = np.fft.rfftfreq(n, 1 / SR)
    flux = np.maximum(np.diff(np.log1p(S * 50), axis=0), 0).sum(1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    pk = (flux[1:-1] > flux[:-2]) & (flux[1:-1] > flux[2:]) & (flux[1:-1] > 1.0)
    dens = pk.sum() / (len(x) / SR)
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    fps = SR / h
    lo, hi = int(fps * 60 / 180), int(fps * 60 / 60)
    tconf = float(ac[lo:hi].max() / (ac[0] + 1e-9))
    cen = float((S * fr[None, :]).sum() / S.sum())
    w = SR * 2
    r = np.array([np.sqrt((x[i:i + w] ** 2).mean()) + 1e-9 for i in range(0, len(x) - w, w)])
    rdb = 20 * np.log10(r)
    dyn = float(np.percentile(rdb, 95) - np.percentile(rdb, 5))
    bands = np.geomspace(50, 8000, 29)
    vecs = []
    for i in range(0, len(x) - SR, SR):
        Sp = np.abs(np.fft.rfft(x[i:i + SR] * np.hanning(SR))) ** 2
        f2 = np.fft.rfftfreq(SR, 1 / SR)
        vecs.append([np.log10(Sp[(f2 >= bands[b]) & (f2 < bands[b + 1])].sum() + 1e-9) for b in range(28)])
    V = np.array(vecs)
    V = V - V.min()
    V /= (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
    Sim = V @ V.T
    m = len(V)
    far = np.abs(np.arange(m)[:, None] - np.arange(m)[None, :]) > 10
    sim = float(Sim[far].mean())
    band = (fr > 80) & (fr < 1000)
    top = fr[band][np.argmax(S[:, band], axis=1)]
    pitched = float(np.mean(np.abs(np.diff(np.log2(top + 1))) < 0.03))   # fraction of frames whose strongest partial stays put
    return dict(tconf=tconf, dens=dens, cen=cen, dyn=dyn, sim=sim, pitched=pitched)


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
            f["score"] = (1 - min(f["tconf"], 1)) * 2 + max(0, 2.5 - f["dens"]) * 0.8 + max(0, 1000 - f["cen"]) / 500 + max(0, 12 - f["dyn"]) / 6 + f["sim"] * 2
            rows.append(f)
    rows.sort(key=lambda r: -r["score"])
    print(f"{'track':30s} {'tconf':>5s} {'ons/s':>5s} {'cent':>5s} {'dyn':>5s} {'sim':>5s} {'pitch':>5s} {'score':>5s}")
    for r in rows:
        print(f"{r['name'][:30]:30s} {r['tconf']:5.2f} {r['dens']:5.2f} {r['cen']:5.0f} {r['dyn']:5.1f} {r['sim']:5.2f} {r['pitched']:5.2f} {r['score']:5.2f}")


if __name__ == "__main__":
    main()
