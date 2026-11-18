"""Re-time one scene whose Whisper pass skipped words (clear: 60 of 127 words, 17 s gap). Tries beam 5 without previous-text conditioning,
then falls back to a syllable-proportional split inside the speech regions. Run: python wt_fix.py <scene>"""
import json, re, sys, wave
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
H = Path(__file__).parent; sid = sys.argv[1]
deck = json.load(open(H / "deck.json", encoding="utf-8")); i = [s["id"] for s in deck["scenes"]].index(sid)
w = wave.open(str(H / "audio/tts" / f"s_{i:02d}.wav")); sr = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
n = int(len(a) * 16000 / sr); a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language="hi", beam_size=5, word_timestamps=True, condition_on_previous_text=False)
ws = [x for s in segs for x in s.words]
toks = re.sub(r"\s+", " ", deck["scenes"][i]["voice"]).strip().split(" ")
pts = [[tk, round(float(ws[min(len(ws) - 1, int(round(k * len(ws) / len(toks))))].start), 2)] for k, tk in enumerate(toks)]
gaps = max(pts[k + 1][1] - pts[k][1] for k in range(len(pts) - 1))
print("whisper small words", len(ws), "tokens", len(toks), "max gap", round(gaps, 2))
if len(ws) < 0.8 * len(toks) or gaps > 2.5:
    # fallback: speech frames (energy) mapped to cumulative syllable weight of the tokens
    fr = 160; e = np.array([np.sqrt(np.mean(a[j:j + fr] ** 2)) for j in range(0, len(a) - fr, fr)]); sp = e > 0.02
    tsp = np.cumsum(sp) / max(1, sp.sum()); wt = np.array([max(1, len(re.sub(r"[,.?!।]", "", tk))) for tk in toks], dtype=float)
    cw = np.concatenate([[0], np.cumsum(wt)[:-1]]) / wt.sum()
    pts = [[tk, round(float(np.searchsorted(tsp, c) * fr / 16000), 2)] for tk, c in zip(toks, cw)]
    print("fallback: syllable-proportional over speech frames")
W = json.load(open(H / "wt.json", encoding="utf-8")); W[sid] = {"tokens": pts, "voice_s": round(len(a) / 16000, 2), "n_whisper": len(ws), "n_tokens": len(toks)}
json.dump(W, open(H / "wt.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k in range(0, len(pts), 12): print(pts[k])
