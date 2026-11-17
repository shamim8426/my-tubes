import json
from pathlib import Path
S = Path(__file__).resolve().parent
A1 = "أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَٰبِ ٱلْفِيلِ"
A2 = "أَلَمْ يَجْعَلْ كَيْدَهُمْ فِى تَضْلِيلٍ"
A3 = "وَأَرْسَلَ عَلَيْهِمْ طَيْرًا أَبَابِيلَ"
L = [
 ("1_army", "ये उस साल की बात है, जब यमन का हाकिम अबरहा हाथियों का लश्कर लेकर चला। उसका इरादा था, काबा को गिराना।", None, "pan_right"),
 ("2_kaaba", "अलम तरा कैफ़ा फ़अला रब्बुका बि अस्हाबिल फ़ील।", (A1, "सूरह अल-फ़ील 105:1"), "push_in"),
 ("2_kaaba", "अल्लाह पूछता है: क्या तुमने नहीं देखा, तुम्हारे रब ने हाथी वालों के साथ क्या किया? ये बात उन लोगों से कही गई, जिन्होंने ये वाक़िआ ख़ुद देखा या सुना था।", None, "pull_out"),
 ("3_elephant_sits", "अलम यज्अल कैदहुम फ़ी तज़्लील।", (A2, "सूरह अल-फ़ील 105:2"), "push_in"),
 ("3_elephant_sits", "क्या उसने उनकी सारी चाल बेकार नहीं कर दी? रिवायतों में आता है कि हाथी आगे बढ़ा ही नहीं, वहीं बैठ गया।", None, "pan_left"),
 ("4_birds", "व अर्सला अलैहिम तैरन अबाबील।", (A3, "सूरह अल-फ़ील 105:3"), "push_in"),
 ("4_birds", "और अल्लाह ने उन पर झुंड के झुंड परिंदे भेज दिए।", None, "pan_right"),
 ("5_night_valley", "यानी जो ताक़त के घमंड में अल्लाह का घर गिराने आया, उसकी चाल अल्लाह ने ख़ुद बेकार कर दी।", None, "pull_out"),
]
M = "shared/music/noor/Quietude_Sections_Merged.mp3"
lines = []
for i, (im, t, ay, p) in enumerate(L):
    d = {"n": i + 1, "text": t, "img": im, "motion": True, "preset": p, "overlay": [["dust", 0.10]],
         "sfx": [], "amb": [], "music": M, "ayah": bool(ay)}
    if ay:
        d.update({"ar": ay[0], "src": ay[1], "ayah_y": 60, "tr_y": 870, "src_y": 280})
    lines.append(d)
cfg = {"title": "Al-Fil 105:1-3 toon demo", "voice": "Charon",
       "style": "Calm, warm, clear Hindi storyteller. Simple spoken Hindi, gentle, normal conversational pace, correct Urdu sounds.",
       "tempo": 1.0, "ambience": "shared/sfx/history/wind_desert_675710.mp3", "music": M, "music_vol": 0.5,
       "amp": 0.08, "amb_db": -6, "sfx_db": -3, "duck": True, "ayah_fs": 150, "ayah_src": "", "lines": lines}
(S / "script.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
(S / "audio").mkdir(exist_ok=True); (S / "output").mkdir(exist_ok=True)
