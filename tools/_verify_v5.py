import json
import sys
import wave
from collections import defaultdict

import numpy as np

sys.path.insert(0, "tools")
import rc_sound as RS

SR = RS.SR
st = "channels/reality-check/stories/002_great-dying/"
w = wave.open("cache/reality-check/002/music/music_stem.wav")
m = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, 2).mean(1) / 32768
v = RS.load_audio(st + "audio/voiceover_full.wav", 1)[:, 0][: len(m)]
v = np.pad(v, (0, len(m) - len(v)))
vpk = 20 * np.log10(np.abs(v).max())
log = json.load(open("cache/reality-check/002/music/fx_log.json"))
by = defaultdict(list)
for t, k, rel, note in log:
    if k == "AMB":
        continue
    s = m[int(t * SR): int((t + 0.3) * SR)] if k != "RISE" else m[int((t + 1.4) * SR): int((t + 1.8) * SR)]
    by[k].append(20 * np.log10(np.abs(s).max() + 1e-9) - vpk)
print("PEAK vs voice peak per type (stem, dB): " + "; ".join(f"{k} n={len(x)} median {np.median(x):.1f} range {min(x):.1f}..{max(x):.1f}" for k, x in by.items()))


def spec(x):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return X, f


# sweep check: AIR spectral centroid in 3 consecutive 80 ms slices (flat = no sweep); RISE energy above 350 Hz
cs = []
for t, k, rel, note in log:
    if k == "AIR":
        sl = []
        for j in range(3):
            x = m[int((t + 0.02 + 0.08 * j) * SR): int((t + 0.1 + 0.08 * j) * SR)]
            X, f = spec(x)
            sl.append(float((X * f).sum() / (X.sum() + 1e-12)))
        cs.append(sl)
cs = np.array(cs)
print("AIR centroid Hz per 80 ms slice (median over %d events): %s  (a whoosh would move by >1 kHz)" % (len(cs), np.round(np.median(cs, 0))))
import rc_fx_v5 as FX
a_ = FX.air()
sl = []
for j in range(3):
    X, f = spec(a_[int((0.01 + 0.07 * j) * SR): int((0.08 + 0.07 * j) * SR)])
    sl.append(float((X * f).sum() / X.sum()))
print("isolated AIR: centroid per 70 ms slice", np.round(sl), "Hz; band share 1.5-6k %.0f%%" % (100 * spec(a_)[0][(spec(a_)[1] > 1500) & (spec(a_)[1] < 6000)].sum() / spec(a_)[0].sum()))
r_ = FX.rise(1.8)
X, f = spec(r_)
print("isolated RISE: energy above 350 Hz %.1f dB below total; peak sub 30-58 Hz glide" % (-10 * np.log10(X[f > 350].sum() / X.sum() + 1e-12) ))
for nm in ["BOOM", "BOOM-soft", "THUD"]:
    X, f = spec(FX.render({"type": nm, "text": "", "t": 0}))
    print(nm, "isolated: %.1f%% of energy below 100 Hz, %.2f%% above 400 Hz" % (100 * X[f < 100].sum() / X.sum(), 100 * X[f > 400].sum() / X.sum()))
# ambience: spectral centroid drift across the bed (fixed filters => stable)
for t, k, rel, note in log:
    if k == "AMB":
        x = m[int(t * SR): int((t + 4) * SR)]
        X, f = spec(x)
        print(f"AMB {t:6.1f} {note[:28]:28s} peak {20*np.log10(np.abs(x).max()+1e-9)-vpk:5.1f} dB  centroid {float((X*f).sum()/(X.sum()+1e-12)):6.0f} Hz")
sp = np.zeros(len(m), bool)
for l in json.load(open(st + "audio/voiceover_timing.json", encoding="utf-8")):
    sp[int(l["start"] * SR): int(l["end"] * SR)] = 1
row = []
for t in range(0, 750, 30):
    a, b = t * SR, min((t + 30) * SR, len(m))
    mk = sp[a:b]
    if mk.sum() > SR:
        row.append(f"{t}:{RS.lufs(m[a:b][mk]) - RS.lufs(v[a:b][mk]):.0f}")
print("stem(music+fx) vs voice LU per 30 s window in speech:", " ".join(row))
for a, b in json.load(open(st + "long/music_cues.json"))["off_windows"]:
    s = m[int((a + 0.4) * SR): int((b - 0.3) * SR)]
    print(f"OFF {a:.1f}-{b:.1f}: stem peak {20*np.log10(np.abs(s).max()+1e-9):.0f} dBFS (voice peak {vpk:.0f})")
