"""009 Al-Kafirun — surah Long script (RULES 2i/2j/2k/2l/2m: one narrator Charon, phrase lines, ayah read once with
Arabic on screen, story-style Hindi, no questions, no lesson line, no next-video teaser, short summary at the end).
Arabic = exact Tanzil bytes from research/sources.json (never typed by hand). Facts: research/dossier.md [F#]/[U#].
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/009_al-kafirun/make_script.py
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent
src = json.loads((S / "research/sources.json").read_text(encoding="utf-8"))


def tanzil(n):
    """Exact Tanzil Uthmani bytes of 109:n from sources.json (structure written by Khoji)."""
    for key in ("arabic", "ayat", "tanzil", "arabic_text"):
        v = src.get(key)
        if isinstance(v, dict):
            for k in (str(n), f"109:{n}"):
                if k in v:
                    x = v[k]
                    return x["text"] if isinstance(x, dict) else x
            if "ayat" in v:
                v = v["ayat"]
        if isinstance(v, list):
            for x in v:
                if isinstance(x, dict) and int(x.get("ayah", x.get("n", 0))) == n:
                    return x.get("text") or x.get("arabic") or x.get("ar")
    raise KeyError(f"109:{n} not found in sources.json")


SRC = "सूरह अल-काफ़िरून 109:{}"
# (image, text, gold keywords, ayah number or None)
L = [
    # parichay [P1-P5]
    ("01_valley_evening", "क़ुरआन की एक छोटी सी सूरह है, जिसमें बस छह आयतें हैं।", ["छह आयतें"], None),                     # P1
    ("01_valley_evening", "इसका नाम है सूरह अल-काफ़िरून, यानी इनकार करने वाले।", ["अल-काफ़िरून"], None),                   # P1
    ("01_valley_evening", "ये क़ुरआन की एक सौ नौवीं सूरह है। ज़्यादातर उलमा के मुताबिक़ ये मक्का में उतरी, और कुछ उलमा से इसके मदीना में उतरने की राय भी नक़्ल है।", ["मक्का"], None),  # P1 P2
    ("04_light_valley", "इसे अल-मुक़श्क़िशा भी कहा गया, यानी शिर्क से पाक कर देने वाली।", ["अल-मुक़श्क़िशा"], None),        # P4
    ("04_light_valley", "और इसकी बात बिल्कुल साफ़ है: इबादत सिर्फ़ एक अल्लाह की, इसमें कोई मिलावट नहीं।", ["एक अल्लाह"], None),  # P5
    # halaat [N1 N2] (N3 "ek saal" riwayat = chhoda gaya, never)
    ("03_idols_shrine", "उस वक़्त मक्का में लोग बुतों की पूजा करते थे।", ["बुतों"], None),
    ("03_idols_shrine", "और क़ुरैश के सरदार अपने बुतों को छोड़ने को तैयार नहीं थे।", ["तैयार नहीं"], None),
    ("02_chiefs_offer", "क़ुरैश के सरदार चाहते थे, कि इबादत में कोई बीच का रास्ता निकल आए।", ["बीच का रास्ता"], None),  # N1
    ("03_idols_shrine", "कुछ तुम हमारी मानो, और कुछ हम तुम्हारी।", ["कुछ हम तुम्हारी"], None),                               # N1
    ("02_chiefs_offer", "ऐसी पेशकश एक बार नहीं, कई बार हुई।", ["कई बार"], None),                                             # N1
    ("04b_light_sky", "तब ये सूरह उतरी, उनकी इस उम्मीद का साफ़ और आख़िरी जवाब बनकर।", ["आख़िरी जवाब"], None),               # N1
    # ayah 1 [U1 K1 N2]
    ("04b_light_sky", "क़ुल या अय्युहल काफ़िरून।", [], 1),
    ("04b_light_sky", "कह दो, ऐ इनकार करने वालो।", ["कह दो"], None),                                                     # U1
    ("04b_light_sky", "ये जवाब अल्लाह के हुक्म से दिया गया, अपनी तरफ़ से नहीं।", ["अल्लाह के हुक्म"], None),        # K1
    ("02_chiefs_offer", "और ये बात उस वक़्त के उन ख़ास लोगों से कही गई, जो अपनी ज़िद पर अड़े हुए थे।", ["ज़िद"], None),            # N2
    # ayah 2 [U2]
    ("02_chiefs_offer", "ला अअबुदु मा तअबुदून।", [], 2),
    ("03_idols_shrine", "मैं उनकी इबादत नहीं करता, जिनकी तुम इबादत करते हो।", ["नहीं करता"], None),                        # U2
    ("03_idols_shrine", "वो बुत, जिनके आगे तुम झुकते हो, मैं उनके आगे नहीं झुकता।", ["नहीं झुकता"], None),       # U2
    # ayah 3 [U3]
    ("04b_light_sky", "व ला अन्तुम आबिदूना मा अअबुद।", [], 3),
    ("06_family_dua", "और न तुम उसकी इबादत करने वाले हो, जिसकी मैं इबादत करता हूँ।", ["उसकी"], None),                    # U3
    ("06_family_dua", "मैं सिर्फ़ एक अल्लाह की इबादत करता हूँ, उसके साथ किसी को साझी नहीं बनाता।", ["सिर्फ़ एक अल्लाह"], None),  # U3
    # ayah 4 [U4]
    ("03_idols_shrine", "व ला अना आबिदुम मा अबत्तुम।", [], 4),
    ("05_two_paths", "और न मैं कभी उनकी इबादत करने वाला हूँ, जिनकी तुमने इबादत की।", ["कभी"], None),                     # U4
    # ayah 5 [U5 K2]
    ("09_dawn_walk", "व ला अन्तुम आबिदूना मा अअबुद।", [], 5),
    ("09_dawn_walk", "और न तुम उसकी इबादत करने वाले हो, जिसकी मैं इबादत करता हूँ।", ["उसकी"], None),                    # U5
    ("05_two_paths", "ये बात सूरह में दो बार आई है।", ["दो बार"], None),                                                    # K2
    ("05_two_paths", "उलमा कहते हैं, ये दोहराना ज़ोर देने के लिए है, ताकि सौदे की हर उम्मीद ख़त्म हो जाए।", ["ज़ोर"], None),   # K2a
    ("05_two_paths", "कुछ कहते हैं: एक बार आज के लिए, और एक बार आगे के लिए। न आज, न कभी।", ["न आज, न कभी"], None),         # K2b
    ("09_dawn_walk", "और कुछ कहते हैं: फ़र्क़ सिर्फ़ इसमें नहीं कि किसकी इबादत, बल्कि इसमें भी कि कैसे इबादत।", ["कैसे"], None),  # K2c
    # ayah 6 [U6 K3 K4]
    ("10b_stars_sky", "लकुम दीनुकुम व लिया दीन।", [], 6),
    ("10b_stars_sky", "तुम्हारे लिए तुम्हारा दीन, और मेरे लिए मेरा दीन।", ["मेरा दीन"], None),                           # U6
    ("05_two_paths", "इसका मतलब ये नहीं, कि सब रास्ते एक जैसे हैं।", ["एक जैसे"], None),                                  # K3
    ("05_two_paths", "इसका मतलब है: इबादत और यक़ीन में साफ़ अलगाव। मेरा रास्ता अलग, तुम्हारा रास्ता अलग।", ["साफ़ अलगाव"], None),  # K3
    ("07_neighbors", "पर ये अलगाव इबादत में है, बर्ताव में नहीं।", ["बर्ताव में नहीं"], None),                               # K4
    ("07_neighbors", "क़ुरआन की सूरह मुम्तहिना में है: जो लोग दीन की वजह से तुमसे नहीं लड़े,", ["नहीं लड़े"], None),  # K4 60:8
    ("07_neighbors", "और जिन्होंने तुम्हें घरों से नहीं निकाला, अल्लाह तुम्हें उनके साथ भलाई और इंसाफ़ करने से नहीं रोकता।", ["भलाई और इंसाफ़"], None),  # K4 60:8
    ("01b_valley_hills", "और सहीह बुख़ारी में है, कि एक सहाबिया की माँ उनसे मिलने आईं, जो मुसलमान नहीं थीं।", ["माँ"], None),  # K4 Bukhari 2620
    ("01b_valley_hills", "उन्होंने नबी ﷺ से पूछा, तो आप ﷺ ने फ़रमाया: हाँ, अपनी माँ के साथ अच्छा रिश्ता रखो।", ["अच्छा रिश्ता"], None),  # K4 Bukhari 2620
    # fazilat [Z1 Z2 Z3]
    ("09b_dawn_sky", "सहीह मुस्लिम में आता है, कि नबी ﷺ ने फ़ज्र की दो सुन्नत रकअतों में,", ["फ़ज्र"], None),                      # Z1
    ("09b_dawn_sky", "ये सूरह और सूरह इख़लास पढ़ीं।", ["सूरह इख़लास"], None),                                         # Z1
    ("09b_dawn_sky", "और हज में, तवाफ़ के बाद की दो रकअतों में भी।", ["तवाफ़"], None),                                       # Z2
    ("08_sleep_lamp", "अबू दाऊद और तिर्मिज़ी की एक हदीस में है, कि सोने से पहले ये सूरह पढ़ो,", ["सोने से पहले"], None),                          # Z3
    ("08_sleep_lamp", "क्योंकि ये शिर्क से बरी होने का एलान है।", ["शिर्क से बरी"], None),                                    # Z3
    # summary [P5 K5]
    ("10b_stars_sky", "तो पूरी सूरह का मतलब, बस इतना है:", [], None),
    ("10b_stars_sky", "इबादत सिर्फ़ एक अल्लाह की, और इसमें कोई सौदा, कोई मिलावट नहीं।", ["कोई सौदा"], None),
    # (line "और लोगों के साथ बर्ताव, नरमी और इंसाफ़ का।" dropped 2026-11-18: TTS daily cap 100 hit on both keys)
]
P = ["push_in", "pan_right", "pull_out", "pan_left"]
M = "shared/music/noor/River_Flute.mp3"
lines = []
for i, (im, t, g, ay) in enumerate(L):
    d = {"n": i + 1, "text": t, "img": im, "motion": True, "preset": "push_in" if ay else P[i % 4],
         "overlay": [["dust", 0.08]], "sfx": [], "amb": [], "music": M, "ayah": bool(ay), "gold": g}
    if ay:
        d.update({"ar": tanzil(ay), "src": SRC.format(ay), "ayah_y": 90, "tr_y": 870, "src_y": 300})
    lines.append(d)
cfg = {"title": "Surah Al-Kafirun 109", "voice": "Charon",
       "style": "Calm, warm, clear Hindi storyteller. Simple spoken Hindi, gentle, steady, normal conversational pace, correct Urdu sounds. "
                "Read the Arabic-sound lines plainly and clearly, not as recitation, no tune.",
       "tempo": 1.0, "ambience": "", "music": M, "music_vol": 0.5, "amp": 0.08, "amb_db": -6, "sfx_db": -3,
       "duck": True, "ayah_fs": 165, "ayah_outline": 6, "ayah_src": "", "lines": lines}
(S / "script.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
(S / "audio").mkdir(exist_ok=True)
(S / "output").mkdir(exist_ok=True)
print(len(lines), "lines,", sum(len(x["text"].split()) for x in lines), "words")
