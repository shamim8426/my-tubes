import json
from pathlib import Path
S = Path(__file__).resolve().parent
L = [
    ("A_door", "मदीना की एक सुबह। ख़ौला के घर के दरवाज़े पर, उनके पति औस ग़ुस्से में खड़े थे।", "pan_right"),
    ("A_door", "ग़ुस्से में उन्होंने एक ऐसी बात कह दी, जो उस ज़माने में रिश्ता तोड़ने जैसी मानी जाती थी।", "push_in"),
    ("A_door", "ख़ौला के पीछे उनके छोटे बच्चे सहमे हुए देख रहे थे। अब इनका क्या होगा?", "pan_left"),
    ("B_dua", "ख़ौला कुछ देर चुप रहीं। फिर वो अकेले बैठीं, और दोनों हाथ उठाकर अल्लाह से अपना दुख कह दिया।", "push_in"),
    ("B_dua", "और फिर, अल्लाह ने उनकी बात सुन ली।", "pull_out"),
]
M = "shared/music/seekh/Peaceful_Desolation.mp3"
lines = [{"n": i + 1, "text": t, "img": im, "motion": True, "preset": p, "overlay": [["dust", 0.12]],
          "sfx": [], "amb": [], "music": M, "ayah": False} for i, (im, t, p) in enumerate(L)]
cfg = {"title": "toon style test", "voice": "Charon", "style": "calm", "tempo": 1.0,
       "ambience": "shared/sfx/history/wind_desert_675710.mp3", "music": M, "music_vol": 0.5, "amp": 0.08,
       "amb_db": -6, "sfx_db": -3, "duck": True, "lines": lines}
(S / "script.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
(S / "audio").mkdir(exist_ok=True)
(S / "output").mkdir(exist_ok=True)
print("ok")
