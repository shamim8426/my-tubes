r"""Measure real word times of a DevRoboLab deck voice with Whisper (local, free) and write <story>/wt.json.

    .venv\Scripts\python -X utf8 scripts\yb_wordtimes.py <story_dir>

For each scene: my voice text is split on spaces; Whisper words are matched by relative index (counts differ a little), giving
[[char_index_of_token, seconds_in_voice], ...]. gen_deck.py attaches it as scene["wt"]; build_deck.phrase_time interpolates it."""
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

story = Path(sys.argv[1]).resolve()
deck = json.loads((story / "deck.json").read_text(encoding="utf-8-sig"))
m = WhisperModel("small", device="cpu", compute_type="int8", local_files_only=True)
out = {}
for i, sc in enumerate(deck["scenes"]):
    w = wave.open(str(story / "audio/tts" / f"s_{i:02d}.wav"))
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    n = int(len(a) * 16000 / sr)
    a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
    segs, _ = m.transcribe(a, language="hi", beam_size=1, word_timestamps=True)
    ws = [x for s in segs for x in s.words]
    text = re.sub(r"\s+", " ", sc["voice"]).strip()
    toks = [(mt.start(), mt.group()) for mt in re.finditer(r"\S+", text)]
    pts = []
    for k, (ci, _) in enumerate(toks):
        j = min(len(ws) - 1, int(round(k * (len(ws) - 1) / max(1, len(toks) - 1))))
        pts.append([ci, round(ws[j].start, 2)])
    pts.append([len(text), round(len(a) / 16000, 2)])
    out[sc["id"]] = pts
    print(sc["id"], f"{len(a)/16000:.1f}s", len(toks), "tokens", len(ws), "whisper words")
(story / "wt.json").write_text(json.dumps(out), encoding="utf-8")
