import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/"scripts"))
import gemini_tts
D=ROOT/"channels/noor-e-raah/stories/006_imaan-shorts"
for l in json.load(open(D/"short/lines_v2.json",encoding="utf-8")):
    out=D/f"audio/v2_l{l['n']:02d}.wav"
    if out.exists(): continue
    for fo in (True,False):
        try: r=gemini_tts.speak(l["text"],l["voice"],l["style"],out,free_only=fo); print(l["n"],"free" if fo else "paid",round(r["seconds"],1)); break
        except Exception as e: print(l["n"],"fail",fo,str(e)[:60])
