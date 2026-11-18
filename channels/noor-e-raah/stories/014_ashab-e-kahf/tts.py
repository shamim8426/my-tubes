import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import gemini_tts
S = Path(__file__).resolve().parent
cfg = json.loads((S/"script.json").read_text(encoding="utf-8"))
for l in cfg["lines"]:
    out = S/"audio"/f"l{l['n']:02d}.wav"
    if out.exists(): continue
    try:
        r = gemini_tts.speak(l["text"], cfg["voice"], cfg["style"], out, free_only=False)
        print("tts", l["n"], r["row"]["size"], r["row"]["actual_inr"], flush=True)
    except Exception as e:
        print("STOP", l["n"], str(e)[:200], flush=True); break
print("TTS DONE")
