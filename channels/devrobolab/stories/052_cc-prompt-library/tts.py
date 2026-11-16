import json, sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import gemini_tts
d = json.load(open(H / "deck.json", encoding="utf-8"))
paid = "--paid" in sys.argv
for i, s in enumerate(d["scenes"]):
    f = H / "audio/tts" / f"s_{i:02d}.wav"
    if f.exists(): continue
    r = gemini_tts.speak(s["voice"], d["voice"]["id"], d["voice"]["style"], f, free_only=not paid)
    print(s["id"], r, flush=True)
