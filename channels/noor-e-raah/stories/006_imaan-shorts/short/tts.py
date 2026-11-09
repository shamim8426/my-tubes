import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/"scripts"))
import gemini_tts
D=ROOT/"channels/noor-e-raah/stories/006_imaan-shorts"
for l in json.load(open(D/"short/lines.json",encoding="utf-8")):
    out=D/f"audio/l{l['n']:02d}.wav"
    if out.exists(): continue
    try: r=gemini_tts.speak(l["text"],l["voice"],l["style"],out,free_only=False); print(l["n"],"ok",r if not isinstance(r,dict) else {k:r[k] for k in list(r)[:4]})
    except Exception as e: print(l["n"],"FAIL",str(e)[:200])
