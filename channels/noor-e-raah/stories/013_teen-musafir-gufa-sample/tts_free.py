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
        gemini_tts.speak(l["text"], cfg["voice"], cfg["style"], out, free_only=True)
        print("tts", l["n"], "ok", flush=True)
    except Exception as e:
        print("STOP", l["n"], str(e)[:150]); break
