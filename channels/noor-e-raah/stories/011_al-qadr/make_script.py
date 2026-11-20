"""011 Al-Qadr — surah Long script (RULES 1d/2i/2j/2k/2m/2n: one narrator Charon, phrase lines, ayah read once with
Arabic on screen, story-style simple Hindi, no questions, no lesson line, no next-video teaser, short summary at the end).
Arabic = exact Tanzil bytes from research/tanzil_97.json (code-extracted, never typed by hand).
Facts: research/dossier.md [P#]/[N#]/[U#]/[K#]. No sahih shan-e-nuzul exists (N1): the "halaat" part uses Quran 2:185/44:3 (N2).
Lines that speak about the Prophet (pbuh) or his family use places-only images (no person). Ayah 4 (angels, ar-Ruh): no light
beam / figure image, only the calm town / palms.
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/011_al-qadr/make_script.py
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent
AY = {a["ayah"]: a["text"] for a in json.loads((S / "research/tanzil_97.json").read_text(encoding="utf-8"))["ayat"]}

SRC = "सूरह अल-क़द्र 97:{}"
# (image, text, gold keywords, ayah number or None)
L = [
    # hook [U3 K5]
    ("01_qadr_night", "साल में एक रात ऐसी आती है, जो हज़ार महीनों से बेहतर है।", ["हज़ार महीनों"], None),          # U3
    ("06_old_man_years", "हज़ार महीने, यानी तिरासी साल से भी ज़्यादा, एक पूरी उम्र।", ["तिरासी साल"], None),         # K5
    ("04_sky_light_valley", "उसी रात के बारे में, अल्लाह ने ये छोटी सी सूरह उतारी।", ["छोटी सी सूरह"], None),      # P5
    # parichay [P1 P2 N2]
    ("01_qadr_night_c", "ये है सूरह अल-क़द्र, क़ुरआन की सत्तानवेवीं सूरह, पाँच छोटी आयतें।", ["अल-क़द्र"], None),   # P1
    ("02_mountain_night", "मशहूर राय ये है कि ये मक्का में उतरी, और कुछ उलमा इसे मदीना की सूरह मानते हैं।", ["मक्का"], None),  # P2
    ("03_ramadan_lamps", "क़ुरआन ख़ुद बताता है, कि वो रमज़ान के महीने में, एक बरकत वाली रात में उतरा।", ["रमज़ान"], None),  # N2 (2:185, 44:3)
    # ayah 1 [U1 K1 K2 K3]
    ("04_sky_light_valley", "इन्ना अनज़ल्नाहु फ़ी लैलतिल क़द्र।", [], 1),
    ("04_sky_light_valley_c", "हमने इसे, यानी क़ुरआन को, क़द्र की रात में उतारा।", ["यानी क़ुरआन को"], None),           # U1 K1
    ("01_qadr_night", "क़ुरआन समझाने वाले आलिम लिखते हैं, हज़रत इब्न अब्बास के मुताबिक़, पूरा क़ुरआन इस रात पहले आसमान पर उतारा गया।", ["पहले आसमान"], None),  # K2a
    ("02_mountain_night_c", "फिर कई सालों में, थोड़ा-थोड़ा करके, नबी ﷺ पर उतरता रहा।", ["थोड़ा-थोड़ा"], None),        # K2a
    ("02_mountain_night", "और इसी रात से, क़ुरआन का उतरना शुरू हुआ।", ["शुरू"], None),                                # K2b
    ("09_town_lamps_night", "क़द्र के दो मतलब हैं: इज़्ज़त और शान, और तक़दीर, यानी फ़ैसला।", ["इज़्ज़त और शान"], None),  # K3
    ("09_town_lamps_night_c", "और ये दोनों मतलब, इस एक रात में हैं।", ["दोनों मतलब"], None),                            # K3
    # ayah 2 [U2 K4]
    ("05_looking_up_stars", "व मा अदराका मा लैलतुल क़द्र।", [], 2),
    ("05_looking_up_stars_c", "और तुम क्या जानो, क़द्र की रात कितनी बड़ी है!", ["कितनी बड़ी"], None),                     # U2
    # ayah 3 [U3 K5]
    ("06_old_man_years", "लैलतुल क़द्रि ख़ैरुम मिन अल्फ़ि शह्र।", [], 3),
    ("06_old_man_years_c", "क़द्र की रात, हज़ार महीनों से बेहतर है।", ["हज़ार महीनों से बेहतर"], None),                  # U3
    ("06_old_man_years", "हज़ार महीने, यानी तिरासी साल और चार महीने।", ["चार महीने"], None),                             # K5
    ("06_old_man_years_c", "एक आदमी बचपन से बुढ़ापे तक जितना जीता है, उससे भी ज़्यादा।", ["उससे भी ज़्यादा"], None),       # K5
    ("07_night_prayer_far", "आलिम लिखते हैं: इस एक रात की इबादत, उन हज़ार महीनों की इबादत से बेहतर है, जिनमें ये रात न हो।", ["एक रात की इबादत"], None),  # K5
    # ayah 4 [U4 K6 K7 K8]
    ("09_town_lamps_night", "तनज़्ज़लुल मलाइकतु वर्रूहु फ़ीहा बिइज़्नि रब्बिहिम मिन कुल्लि अम्र।", [], 4),
    ("09_town_lamps_night_c", "उस रात फ़रिश्ते और रूह, अपने रब के हुक्म से, हर काम के लिए उतरते हैं।", ["अपने रब के हुक्म से"], None),  # U4
    ("01_qadr_night", "रूह, यानी जिबरील अलैहिस्सलाम। उनका नाम अलग से, उनकी शान के लिए आया है।", ["जिबरील"], None),        # K7
    ("10_still_palms", "फ़रिश्ते इस रात बहुत बड़ी तादाद में उतरते हैं, रहमत और बरकत के साथ।", ["रहमत और बरकत"], None),    # K6
    ("14_closed_door_calm", "हर वो काम, जो अल्लाह ने तय किया, उसे लेकर वो उतरते हैं।", ["तय किया"], None),               # K8
    ("14_closed_door_calm_c", "आलिम लिखते हैं: साल भर के फ़ैसले, रोज़ी और उम्र, इसी रात फ़रिश्तों को सौंपे जाते हैं।", ["साल भर के फ़ैसले"], None),  # K8
    # ayah 5 [U5 K9 K10]
    ("10_still_palms", "सलामुन हिया हत्ता मतलइल फ़ज्र।", [], 5),
    ("10_still_palms_c", "वो रात पूरी की पूरी सलामती है, फ़ज्र की रौशनी निकलने तक।", ["सलामती"], None),               # U5
    ("09_town_lamps_night", "शुरू से आख़िर तक ख़ैर ही ख़ैर, उसमें कोई बुराई नहीं।", ["ख़ैर ही ख़ैर"], None),            # K9
    # hadith [N6]
    ("03_ramadan_lamps", "सहीह बुख़ारी और सहीह मुस्लिम में है, नबी ﷺ ने फ़रमाया:", ["सहीह बुख़ारी"], None),             # N6
    ("07_night_prayer_far", "जो इस रात ईमान के साथ, और सवाब की उम्मीद में इबादत में खड़ा रहे, उसके पिछले गुनाह माफ़ कर दिए जाते हैं।", ["पिछले गुनाह माफ़"], None),  # N6
    # when [N7 N8 K11 N12]
    ("13_masjid_night_far", "ये रात, रमज़ान की आख़िरी दस रातों में आती है।", ["आख़िरी दस रातों"], None),                 # N7
    ("01_qadr_night_c", "नबी ﷺ ने फ़रमाया: इसे आख़िरी दस की ताक़ रातों में तलाश करो।", ["ताक़ रातों"], None),          # N7 Bukhari 2017
    ("13_masjid_night_far", "यानी इक्कीसवीं, तेईसवीं, पच्चीसवीं, सत्ताईसवीं और उनतीसवीं रात।", ["इक्कीसवीं"], None),        # N7 (odd nights, as example)
    ("14_closed_door_calm", "सहीह बुख़ारी में है, एक बार नबी ﷺ इस रात की ख़बर देने निकले।", ["ख़बर देने"], None),         # N8 Bukhari 2023
    ("14_closed_door_calm_c", "दो आदमी आपस में झगड़ रहे थे, और उस रात की पक्की ख़बर उठा ली गई।", ["पक्की ख़बर उठा ली गई"], None),  # N8
    ("01_qadr_night", "आप ﷺ ने फ़रमाया: शायद यही तुम्हारे लिए बेहतर हो।", ["बेहतर"], None),                            # N8
    ("09_town_lamps_night", "इसीलिए ठीक कौन सी रात है, ये छुपा कर रखा गया, ताकि लोग हर ताक़ रात में कोशिश करें।", ["छुपा कर रखा गया"], None),  # K11 N12
    # effort [N9]
    ("03_ramadan_lamps_c", "सहीह बुख़ारी में है, आख़िरी दस रातें आतीं, तो नबी ﷺ पूरी मेहनत से इबादत में लग जाते, रात भर जागते, और घर वालों को भी जगाते।", ["रात भर जागते"], None),  # N9 Bukhari 2024 ("kamar kas lete" = poori mehnat)
    # sign [N10]
    ("12_pale_sun", "सहीह मुस्लिम में, इस रात की एक निशानी आई है:", ["निशानी"], None),                                  # N10 Muslim 762
    ("12_pale_sun_c", "उसकी सुबह सूरज सफ़ेद-सा निकलता है, बिना तेज़ किरणों के।", ["बिना तेज़ किरणों"], None),                # N10
    # dua [N11]
    ("03_ramadan_lamps", "तिर्मिज़ी और इब्न माजा की हदीस में है, हज़रत आइशा को नबी ﷺ ने इस रात के लिए ये दुआ सिखाई:", ["ये दुआ"], None),  # N11
    ("09_town_lamps_night_c", "अल्लाहुम्मा इन्नका अफ़ुव्वुन तुहिब्बुल अफ़्वा फ़अफ़ु अन्नी।", ["अफ़ुव्वुन"], None),           # N11 (Ibn Majah 3850 words)
    ("15_family_night_dua", "ऐ अल्लाह, तू बहुत माफ़ करने वाला है, माफ़ करना पसंद करता है, तो मुझे माफ़ कर दे।", ["मुझे माफ़ कर दे"], None),  # N11
    # summary [P5 K5 K6 K9]
    ("01_qadr_night", "तो पूरी सूरह का मतलब बस इतना है:", [], None),
    ("04_sky_light_valley", "एक रात, जिसमें क़ुरआन उतरा, और जो हज़ार महीनों से बेहतर है।", ["हज़ार महीनों से बेहतर"], None),  # P5 K5
    ("09_town_lamps_night", "उस रात फ़रिश्ते, अल्लाह के हुक्म से उतरते हैं,", ["अल्लाह के हुक्म"], None),               # K6
    ("11_fajr_breaks", "और फ़ज्र तक, पूरी रात सलामती ही सलामती है।", ["सलामती ही सलामती"], None),                      # K9
]
P = ["push_in", "pan_right", "pull_out", "pan_left"]
M = "shared/music/noor/Quietude_Sections_Merged.mp3"
lines = []
for i, (im, t, g, ay) in enumerate(L):
    d = {"n": i + 1, "text": t, "img": im, "motion": True, "preset": "push_in" if ay else P[i % 4],
         "overlay": [["dust", 0.08]], "sfx": [], "amb": [], "music": M, "ayah": bool(ay), "gold": g}
    if ay:
        d.update({"ar": AY[ay], "src": SRC.format(ay), "ayah_y": 90, "tr_y": 870, "src_y": 300})
    lines.append(d)
cfg = {"title": "Surah Al-Qadr 97", "voice": "Charon",
       "style": "Calm, warm, clear Hindi storyteller. Simple spoken Hindi, gentle, steady, normal conversational pace, correct Urdu sounds. "
                "Read the Arabic-sound lines plainly and clearly, not as recitation, no tune.",
       "tempo": 1.1, "ambience": "", "music": M, "music_vol": 0.12, "amp": 0.08, "amb_db": -6, "sfx_db": -3,
       "duck": True, "ayah_fs": 165, "ayah_outline": 6, "ayah_src": "", "lines": lines}
(S / "script.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
(S / "audio").mkdir(exist_ok=True)
(S / "output").mkdir(exist_ok=True)
print(len(lines), "lines,", sum(len(x["text"].split()) for x in lines), "words")
