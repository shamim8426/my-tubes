"""Make 1-line Gemini TTS samples per character for casting.

Usage: python scripts/voice_samples.py [character ...]
Output: audio/voice_samples/<character>_<Voice>.wav  (cost logged per sample)
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cost_log  # noqa: E402
from gemini_tts import speak  # noqa: E402
from voices import CAST  # noqa: E402

from paths import ROOT, channel_dir  # noqa: E402

OUT = channel_dir() / "characters" / "voices"

SAMPLE_LINES = {
    "narrator": "शर्मा जी की नई साइकिल... रातों-रात गायब!",
    "sharma": "कल ही ख़रीदी थी! रात को गेट से बाँधी थी... और गेट पर कल शाम ही लाल पेंट करवाया था!",
    "dadi": "बेटा, चोर कितना भी चालाक हो... दादी से नहीं बच सकता!",
    "golu": "दादी, मुझे पता है चोर कौन है! पप्पू! देखो, उसका गमछा लाल है!",
    "mitthu": "गीला! गीला!",
    "pandey": "पकड़ो इसे!",
    "pappu": "मैं तो रोज़ सुबह दूध देने निकलता हूँ, मैंने कुछ नहीं देखा!",
    "raju": "हाँ, मैंने कहा था ऐसी साइकिल मुझे भी चाहिए... पर चोरी? कभी नहीं!",
    "bunty": "मैं तो रात भर घर पर पढ़ाई कर रहा था!",
    "ghasita": "एक सिक्का भी कम, तो जलेबी नहीं! भागो यहाँ से!",
    "chhotu": "बाबा, मेरे पास बस यही है। आप खा लीजिए।",
    "sadhu": "पर याद रखना — ये सिर्फ़ भूखों के लिए है। लालच के लिए नहीं।",
    "woman": "भैया, आधा किलो जलेबी देना।",
    "kid": "चाचा, एक जलेबी... बस एक सिक्का कम है।",
    "villager": "छोटू की जलेबी! इसमें ईमानदारी का स्वाद है!",
    "kids": "छोटू भैया ज़िंदाबाद!",
}

if __name__ == "__main__":
    total = 0.0
    for name in sys.argv[1:] or list(CAST):
        voice, style, _ = CAST[name]
        line = SAMPLE_LINES[name]
        out = OUT / f"{name}_{voice}.wav"
        t0 = time.time()
        try:
            res = speak(line, voice, style, out)
        except Exception as e:
            print(f"SKIPPED {name}: {e}", flush=True)
            continue
        total += res["usd"]
        print(f"{name:9s} {voice:14s} {res['seconds']:4.1f}s audio, {time.time() - t0:4.1f}s wait  "
              f"usage={'reported' if res['usage_reported'] else 'estimated'}  "
              + cost_log.summary(res["row"], "sample"), flush=True)
    print(f"TOTAL ${total:.4f} = ₹{total * cost_log.USD_TO_INR:.2f}")
