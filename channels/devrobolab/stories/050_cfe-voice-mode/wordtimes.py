"""Real word times of each scene voice (Whisper base, local, free) -> wt.json: per scene a list of [token, seconds_in_voice] for MY voice tokens
(relative-index match, as scripts/yb_wordtimes.py). Run: python wordtimes.py"""
import json, re, sys, wave
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
H = Path(__file__).parent
deck = json.load(open(H / "deck.json", encoding="utf-8"))
m = WhisperModel("base", device="cpu", compute_type="int8")
out = {}
for i, sc in enumerate(deck["scenes"]):
    w = wave.open(str(H / "audio/tts" / f"s_{i:02d}.wav")); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    n = int(len(a) * 16000 / sr); a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
    segs, _ = m.transcribe(a, language="hi", beam_size=1, word_timestamps=True)
    ws = [x for s in segs for x in s.words]
    toks = re.sub(r"\s+", " ", sc["voice"]).strip().split(" ")
    pts = []
    for k, tk in enumerate(toks):
        j = min(len(ws) - 1, int(round(k * len(ws) / max(1, len(toks))))) if ws else 0
        pts.append([tk, round(float(ws[j].start), 2) if ws else 0.0])
    out[sc["id"]] = {"tokens": pts, "voice_s": round(len(a) / 16000, 2), "n_whisper": len(ws), "n_tokens": len(toks)}
    print(sc["id"], len(toks), len(ws), flush=True)
json.dump(out, open(H / "wt.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done")
