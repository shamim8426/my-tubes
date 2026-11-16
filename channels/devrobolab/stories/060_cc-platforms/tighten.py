import wave, numpy as np, shutil
from pathlib import Path
H = Path(__file__).parent; src = H / "audio/tts_orig"
if not src.exists(): shutil.copytree(H / "audio/tts", src)
tot = 0
for f in sorted(src.glob("s_*.wav")):
    w = wave.open(str(f)); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).copy(); w.close()
    fr = int(sr * 0.02); n = len(a) // fr
    rms = np.array([np.abs(a[i * fr:(i + 1) * fr].astype(np.int32)).mean() for i in range(n)]); sil = rms < 250
    out = []; i = 0; keep = 6
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if (j - i) > keep + 3 and i > 0 and j < n: out.append(a[i * fr:(i + keep) * fr])
            else: out.append(a[i * fr:j * fr])
            i = j
        else:
            out.append(a[i * fr:(i + 1) * fr]); i += 1
    o = np.concatenate(out + [a[n * fr:]]); tot += len(o) / sr
    w = wave.open(str(H / "audio/tts" / f.name), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(o.tobytes()); w.close()
    print(f.name, len(a) / sr, len(o) / sr)
print(tot)
