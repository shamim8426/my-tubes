import json, wave, glob, sys, os
from faster_whisper import WhisperModel
try:
    m = WhisperModel("small", device="cpu", compute_type="int8", local_files_only=True)
except Exception as e:
    try:
        m = WhisperModel("base", device="cpu", compute_type="int8", local_files_only=True)
    except Exception as e2:
        print("no local whisper model", str(e2)[:200]); sys.exit()


def run(p):
    import numpy as np
    ww = wave.open(p); a = np.frombuffer(ww.readframes(ww.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    n = int(len(a) * 16000 / ww.getframerate()); a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
    segs, _ = m.transcribe(a, language="hi", beam_size=1)
    t = " ".join(s.text for s in segs)
    w = wave.open(p); d = w.getnframes() / w.getframerate()
    print(os.path.basename(p), round(d, 1), "s", len(t.split()), "words ->", round(len(t.split()) / d, 2), "w/s")
    print("  ", t[:220])


d = json.load(open(r"D:\my-tubes\channels\yellow-bot\stories\020_quickstart\deck.json", encoding="utf-8"))
print("REF:", d["scenes"][3]["voice"], len(d["scenes"][3]["voice"].split()), "ref words")
run(r"D:\my-tubes\channels\yellow-bot\stories\020_quickstart\_ttstest\3.8_flash_lite_tts.wav")
for f in sorted(glob.glob(r"D:\my-tubes\channels\yellow-bot\stories\019_overview\audio\tts\s_0[13].wav")):
    run(f)
