"""014 Ashab-e-Kahf — history story Long (RULES 2e/2f/2i/2j/2k/2l/2n; template 013 + ayah cards like 009).
One narrator Charon, short phrase lines, simple Hindi, no teaser/question/lesson, last line = source line.
Arabic = exact bytes from research/quran-uthmani.txt (Tanzil Uthmani 1.1), jumla = word-bounded substring.
Facts: research/dossier.md [F#] (Quran 18:9-26 first; tafseer only where tagged and hedged).
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/014_ashab-e-kahf/make_script.py
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent
TZ = {}
for row in (S / "research/quran-uthmani.txt").read_text(encoding="utf-8").splitlines():
    p = row.split("|")
    if len(p) == 3 and p[0] == "18":
        TZ[int(p[1])] = p[2]


def ar(n, wi=0):
    """Exact Tanzil bytes of 18:n; wi = index of the first word of a jumla (word-bounded tail of the ayah, split on ' ')."""
    return " ".join(TZ[n].split(" ")[wi:])


# (image, text, gold keywords, ayah card or None)  -- [F#] = dossier fact
L = [
    # hook + intro [F1 F2]
    ("06_cave_mouth", "कुछ नौजवान थे, जो अपना ईमान बचाने के लिए एक गुफा में जा छिपे।", ["ईमान"], None),            # F1 F6
    ("06_cave_mouth", "वो सो गए। और जब जागे, तो बरसों बीत चुके थे।", ["बरसों"], None),                       # F8 F12
    ("15_stars_cave", "ये वाक़िआ अल्लाह ने ख़ुद क़ुरआन की सूरह अल-कह्फ़ में बताया है।", ["सूरह अल-कह्फ़"], None),      # F1
    ("16_dawn_cave", "कह्फ़ का मतलब है गुफा। इसलिए इन्हें अस्हाब-ए-कह्फ़, यानी गुफा वाले कहा जाता है।", ["गुफा वाले"], None),  # F1
    # the town [F3 F4]
    ("02_town_idols", "बहुत पुराने ज़माने की बात है। एक शहर के लोगों ने, अल्लाह के सिवा दूसरे ख़ुदा बना रखे थे।", ["दूसरे ख़ुदा"], None),  # F4
    ("03_youths_together", "उसी शहर में कुछ नौजवान थे, जो एक अल्लाह पर ईमान ले आए।", ["एक अल्लाह"], None),            # F3
    ("03_youths_together", "इन्नहुम फ़ित्यतुन आमनू बिरब्बिहिम व ज़िदनाहुम हुदा।", [], (13, 5)),              # F3
    ("03_youths_together", "अल्लाह फ़रमाता है: वो कुछ नौजवान थे, जो अपने रब पर ईमान लाए, और हमने उन्हें सही राह में और आगे बढ़ा दिया।", ["सही राह"], None),  # F3
    # they stand firm [F5]
    ("04_youths_stand", "अल्लाह ने उनके दिल मज़बूत कर दिए।", ["दिल मज़बूत"], None),                                     # F5
    ("04_youths_stand", "वो खड़े हुए, और साफ़ कहा: हमारा रब वही है, जो आसमानों और ज़मीन का रब है।", ["आसमानों और ज़मीन"], None),  # F5
    ("04_youths_stand", "हम उसके सिवा किसी और को कभी नहीं पुकारेंगे। ऐसा करें, तो ये बहुत ग़लत बात होगी।", ["कभी नहीं"], None),  # F5
    ("02_town_idols", "उन्होंने कहा: हमारे लोगों ने अल्लाह के सिवा दूसरे ख़ुदा बना लिए हैं।", ["हमारे लोगों"], None),     # F4
    ("02_town_idols", "पर इसकी कोई साफ़ दलील नहीं लाते। और जो अल्लाह पर झूठ बाँधे, उससे बड़ा ज़ालिम कोई नहीं।", ["झूठ"], None),  # F4
    # leaving for the cave [F6 F7]
    ("05_leave_town", "फिर उन्होंने आपस में कहा: जब तुमने इन लोगों से, और इनके झूठे ख़ुदाओं से किनारा कर लिया है,", ["किनारा"], None),  # F6
    ("05_leave_town", "तो चलो, गुफा में पनाह लो।", ["गुफा"], None),                                                  # F6
    ("05_leave_town", "तुम्हारा रब तुम पर अपनी रहमत फैला देगा, और तुम्हारा काम आसान कर देगा।", ["रहमत"], None),      # F6
    ("06_cave_mouth", "वो शहर छोड़कर निकले, और पहाड़ की एक गुफा में जा पहुँचे।", ["गुफा"], None),                      # F6
    ("05_leave_town", "उनके साथ उनका एक कुत्ता भी था।", ["कुत्ता"], None),                                           # F10
    # the dua [F7]
    ("07_dua_cave", "गुफा में पहुँचकर, उन्होंने अल्लाह से ये दुआ की।", ["दुआ"], None),                                 # F7
    ("07_dua_cave", "रब्बना आतिना मिल्लदुन्का रह्मतंव्व हय्यिअ लना मिन अम्रिना रशदा।", [], (10, 6)),         # F7
    ("07_dua_cave", "ऐ हमारे रब, हमें अपने पास से रहमत दे, और हमारे इस काम में हमारे लिए सही रास्ता बना दे।", ["रहमत"], None),  # F7
    # the long sleep [F8 F9 F10]
    ("08_sleep_cave", "फिर अल्लाह ने उनके कानों पर पर्दा डाल दिया, और वो गहरी नींद सो गए।", ["गहरी नींद"], None),        # F8
    ("08_sleep_cave", "एक दिन नहीं, एक साल नहीं, बरसों-बरस तक।", ["बरसों-बरस"], None),                                  # F8
    ("09_sun_cave", "सूरज निकलता, तो उनकी गुफा से दाईं तरफ़ हटकर निकल जाता।", ["दाईं"], None),                          # F9
    ("09_sun_cave", "और डूबता, तो बाईं तरफ़ से कतराकर निकल जाता। और वो गुफा के अंदर एक खुली जगह में थे।", ["बाईं"], None),  # F9
    ("09_sun_cave", "ये अल्लाह की निशानियों में से एक निशानी थी।", ["निशानी"], None),                                   # F9
    ("08_sleep_cave", "कोई उन्हें देखता, तो समझता कि वो जाग रहे हैं, जबकि वो सो रहे थे।", ["सो रहे"], None),             # F10
    ("08_sleep_cave", "अल्लाह उन्हें कभी दाईं, कभी बाईं करवट बदलवाता रहा।", ["करवट"], None),                            # F10
    ("10_dog_entrance", "और उनका कुत्ता गुफा के मुँह पर, अपने दोनों अगले पैर फैलाए पड़ा था।", ["कुत्ता"], None),           # F10
    ("10_dog_entrance", "उन पर ऐसा रौब था, कि कोई झाँककर देखता, तो डरकर उल्टे पाँव भाग जाता।", ["डरकर"], None),         # F10
    # waking up [F11 F12]
    ("11_wake_talk", "फिर एक दिन, अल्लाह ने उन्हें जगा दिया।", ["जगा"], None),                                           # F11
    ("11_wake_talk", "एक ने पूछा: हम यहाँ कितनी देर रहे?", ["कितनी देर"], None),                                        # F11
    ("11_wake_talk", "दूसरों ने कहा: एक दिन, या दिन का कुछ हिस्सा।", ["एक दिन"], None),                                  # F11
    ("11_wake_talk", "फिर बोले: तुम्हारा रब ही बेहतर जानता है, कि हम कितना रहे।", ["रब ही"], None),                     # F11
    ("12_coins", "अब अपने में से किसी एक को, ये चाँदी के सिक्के देकर शहर भेजो।", ["चाँदी के सिक्के"], None),            # F11
    ("12_coins", "वो देखे कि सबसे पाक-साफ़ खाना कहाँ मिलता है, और वहाँ से कुछ ले आए।", ["पाक-साफ़"], None),            # F11
    ("12_coins", "पर बहुत होशियारी और नरमी से जाए, और किसी को हमारी ख़बर न होने दे।", ["होशियारी"], None),             # F11
    ("04_youths_stand", "क्योंकि अगर उन्हें पता चल गया, तो वो हमें पत्थर मारेंगे, या ज़बरदस्ती अपने धर्म में लौटा लेंगे।", ["पत्थर"], None),  # F11
    # the town finds out [F12 F13]
    ("13_market", "वो नौजवान शहर पहुँचा।", ["शहर"], None),                          # F12 (tafseer, hedged next line)
    ("13_market", "क़ुरआन समझाने वाले पुराने आलिम लिखते हैं, कि वहाँ सब बदल चुका था, और उसके बहुत पुराने सिक्के देखकर लोग हैरान रह गए।", ["पुराने सिक्के"], None),  # F12
    ("14_people_cave", "फिर अल्लाह ने लोगों को उनकी ख़बर दे दी।", ["ख़बर"], None),                                    # F13
    ("14_people_cave", "ताकि लोग जान लें, कि अल्लाह का वादा सच्चा है, और क़ियामत के आने में कोई शक नहीं।", ["वादा सच्चा"], None),  # F13
    # how many were they [F14]
    ("14_people_cave", "बाद में लोग उनकी गिनती पर भी बहस करने लगे।", ["गिनती"], None),                                   # F14
    ("14_people_cave", "कोई कहता: तीन थे, चौथा उनका कुत्ता। कोई कहता: पाँच थे, छठा उनका कुत्ता। ये सब अंदाज़े थे।", ["तीन", "पाँच"], None),  # F14
    ("14_people_cave", "और कोई कहता: सात थे, आठवाँ उनका कुत्ता।", ["सात"], None),                                        # F14
    ("15_stars_cave", "क़ुरआन में आया है: कहो, मेरा रब ही उनकी गिनती सबसे अच्छी तरह जानता है। उन्हें बहुत थोड़े लोग ही जानते हैं।", ["मेरा रब ही"], None),  # F14
    # how long [F15 F16]
    ("16_dawn_cave", "व लबिसू फ़ी कह्फ़िहिम सलासा मिअतिन सिनीना वज़्दादू तिस्आ।", [], (25, 0)),                   # F15
    ("16_dawn_cave", "और वो अपनी गुफा में तीन सौ साल रहे, और नौ साल और।", ["तीन सौ साल"], None),                       # F15
    ("16_dawn_cave", "और साथ ही फ़रमाया: अल्लाह ही ख़ूब जानता है, कि वो कितना रहे। आसमानों और ज़मीन की हर छिपी बात, बस वही जानता है।", ["अल्लाह ही"], None),  # F16
    # close [F1]
    ("06_cave_mouth", "कुछ नौजवान, जिन्होंने पूरे शहर के ख़िलाफ़, अपने रब को चुना।", ["अपने रब"], None),                  # F3 F5
    ("06_cave_mouth", "और अल्लाह ने उन्हें अपनी रहमत में ऐसे छिपा लिया, कि सदियाँ गुज़र गईं।", ["रहमत"], None),           # F8 F15
    ("16_dawn_cave", "ये वाक़िआ क़ुरआन की सूरह अल-कह्फ़, आयत नौ से छब्बीस में आया है।", [], None),                     # F1
]
P = ["push_in", "pan_right", "pull_out", "pan_left"]
M = "shared/music/noor/Quietude_Sections_Merged.mp3"  # 2j/2k: night/sukoon story (sleep in the cave)
lines = []
for i, (im, t, g, ay) in enumerate(L):
    d = {"n": i + 1, "text": t, "img": im, "motion": True, "preset": "push_in" if ay else P[i % 4],
         "overlay": [["dust", 0.08]], "sfx": [], "amb": [], "music": M, "ayah": bool(ay), "gold": g}
    if ay:
        d.update({"ar": ar(*ay), "src": f"सूरह अल-कह्फ़ 18:{ay[0]}", "ayah_y": 90, "tr_y": 870, "src_y": 330})
    lines.append(d)
cfg = {"title": "Ashab-e-Kahf (Surah al-Kahf 18:9-26)", "voice": "Charon",
       "style": "Calm, warm, clear Hindi storyteller telling a true story to a family. Simple spoken Hindi, gentle emotion, steady, "
                "normal conversational pace, correct Urdu sounds. Read the Arabic-sound lines plainly and clearly, not as recitation, no tune.",
       "tempo": 1.02, "ambience": "", "music": M, "music_vol": 0.5, "amp": 0.08, "amb_db": -6, "sfx_db": -3,
       "duck": True, "ayah_fs": 120, "ayah_outline": 6, "ayah_src": "", "lines": lines}
(S / "script.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
txt = "\n".join(f"{x['n']:2d}. [{x['img']}] {'(AYAH ' + x['src'] + ') ' + x['ar'] + ' | ' if x['ayah'] else ''}{x['text']}" for x in lines)
(S / "script.md").write_text("# 014 Ashab-e-Kahf script (generated by make_script.py)\n\n" + txt + "\n", encoding="utf-8")
print(len(lines), "lines,", sum(len(x["text"].split()) for x in lines), "words")
