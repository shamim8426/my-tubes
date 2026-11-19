"""Whisper completeness check of every TTS line (RULES 1b): missing words -> listed; ayah (ucharan) lines -> length sanity only.
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/009_al-kafirun/check_tts.py (report only; never deletes audio: Whisper mishears nuqta words, judge misses by hand)
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

S = Path(__file__).resolve().parent
ROOT = S.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from noor_build import missing  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

cfg = json.loads((S / "script.json").read_text(encoding="utf-8"))
model = WhisperModel("small", device="cpu", compute_type="int8", download_root=str(ROOT / "tools/whisper-models"))
bad, rows, tot = [], [], 0.0
for l in cfg["lines"]:
    f = S / "audio" / f"l{l['n']:02d}.wav"
    ok = f.with_suffix(".ok")
    with wave.open(str(f)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    sec = len(x) / sr
    tot += sec
    if ok.exists():
        continue
    if l.get("ayah"):
        miss = ["too long"] if sec > 1.0 * len(l["text"].split()) + 3.0 else []
        heard = "(ayah: length check)"
    else:
        x16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
        heard = " ".join(s.text.strip() for s in model.transcribe(x16, language="hi", beam_size=5)[0])
        miss = missing(l["text"], heard)
    print(f"{l['n']:2d} {sec:5.1f}s {'OK' if not miss else 'MISS ' + str(miss)}", flush=True)
    if miss:
        bad.append(l["n"])
        rows.append(f"| {l['n']} | {l['text']} | {', '.join(miss)} | {heard} |")
    else:
        ok.write_text(heard, encoding="utf-8")
print(f"voice total {tot:.1f}s; failed lines: {bad}")
(S / "review").mkdir(exist_ok=True)
(S / "review/tts_check.md").write_text("| n | text | missing | heard |\n|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
