"""010 Ad-Duha — surah Long script (RULES 2i/2j/2k/2l/2m/2n: one narrator Charon, phrase lines, ayah read once with
Arabic on screen, story-style Hindi, no questions, no lesson line, no next-video teaser, short summary at the end).
Arabic = exact Tanzil bytes from research/tanzil_93.json (code-extracted from the Tanzil v1.1 file, never typed by hand).
Facts: research/dossier.md [P#]/[N#]/[U#]/[K#]. Ayat 3-8 speak to the Prophet (pbuh): their images are places/symbols only.
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/010_ad-duha/make_script.py
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent
AY = {a["ayah"]: a["text"] for a in json.loads((S / "research/tanzil_93.json").read_text(encoding="utf-8"))["ayat"]}

SRC = "सूरह अद-दुहा 93:{}"
# (image, text, gold keywords, ayah number or None)
L = [
    # hook [N1 N2 N5 P5]
    ("02_still_night", "कुछ रातें ऐसी आईं, जब आसमान से कोई पैग़ाम नहीं आया।", ["कुछ रातें"], None),               # N1 N5
    ("05_dawn_breaks", "तब अल्लाह ने ये सूरह उतारी, तसल्ली बनकर।", ["तसल्ली"], None),                             # P5
    # parichay [P1 P2 K1]
    ("01_morning_sun", "ये है सूरह अद-दुहा, क़ुरआन की तिरानवेवीं सूरह, ग्यारह छोटी आयतें।", ["अद-दुहा"], None),       # P1
    ("01_morning_sun", "ये मक्का में उतरी, नुबुव्वत के शुरुआती दौर में।", ["मक्का"], None),                          # P2
    ("01_morning_sun", "दुहा यानी दिन चढ़े की रौशनी, जब धूप चारों तरफ़ फैल जाती है।", ["दिन चढ़े"], None),           # P1 K1
    # halaat [N1 N2 N5]
    ("02_still_night", "सहीह बुख़ारी और सहीह मुस्लिम में आता है,", ["सहीह बुख़ारी"], None),                          # N1
    ("03_empty_roof_dusk", "एक बार नबी ﷺ बीमार हुए, और दो-तीन रात, रात की नमाज़ के लिए नहीं उठ सके।", ["बीमार"], None),  # N1
    ("03_empty_roof_dusk", "उन्हीं दिनों, कुछ रातों तक वह्य भी नहीं आई।", ["वह्य"], None),                          # N2 N5
    ("04_dark_clouds_town", "तब एक औरत ने ताना दिया, कि लगता है तुम्हें छोड़ दिया गया।", ["छोड़ दिया"], None),        # N1 N4
    ("04_dark_clouds_town", "और मक्का के बुत पूजने वाले भी यही बात कहने लगे।", ["बुत पूजने वाले"], None),                          # N2
    ("05_dawn_breaks", "इसी के जवाब में ये सूरह उतरी।", ["जवाब"], None),                                         # N1
    # ayah 1 [U1 K1]
    ("01_morning_sun", "वज़्ज़ुहा।", [], 1),
    ("01_morning_sun_c", "क़सम है दिन चढ़े की रौशनी की।", ["रौशनी"], None),                                       # U1
    # ayah 2 [U2 K2 K3]
    ("02_still_night", "वल्लैलि इज़ा सजा।", [], 2),
    ("02_still_night", "और क़सम है रात की, जब वो ठहर कर सब पर छा जाए।", ["रात"], None),                         # U2 K2
    ("02_still_night", "हर चीज़ पर सन्नाटा, हर तरफ़ सुकून।", ["सुकून"], None),                                    # K2
    ("05_dawn_breaks", "क़ुरआन समझाने वाले आलिम लिखते हैं: जैसे दिन के बाद रात का आना नाराज़गी नहीं,", ["नाराज़गी नहीं"], None),  # K3
    ("05_dawn_breaks", "वैसे ही वह्य का कुछ रातें रुक जाना भी नाराज़गी नहीं था।", ["रुक जाना"], None),             # K3
    # ayah 3 [U3 K4]
    ("r_04b_light_sky", "मा वद्दअका रब्बुका व मा क़ला।", [], 3),
    ("r_04b_light_sky", "तुम्हारे रब ने न तुम्हें छोड़ा, और न वो तुमसे नाराज़ हुआ।", ["न तुम्हें छोड़ा"], None),     # U3
    ("05_dawn_breaks", "एक तफ़्सीर के लफ़्ज़ों में: जब से तुमसे मुहब्बत की, तब से कभी नाराज़ नहीं हुआ।", ["मुहब्बत"], None),  # K4 (Qurtubi)
    # ayah 4 [U4 K5]
    ("06_path_to_light", "व लल आख़िरतु ख़ैरुल लका मिनल ऊला।", [], 4),
    ("06_path_to_light", "और आगे आने वाला वक़्त, तुम्हारे लिए पिछले से बेहतर है।", ["बेहतर"], None),              # U4
    ("06_path_to_light_c", "उलमा कहते हैं: आख़िरत दुनिया से कहीं बेहतर है, और हर आने वाला दौर पिछले से बेहतर होगा।", ["हर आने वाला दौर"], None),  # K5a K5b
    # ayah 5 [U5 K6]
    ("07_blooming_oasis", "व लसौफ़ा युअतीका रब्बुका फ़तरज़ा।", [], 5),
    ("07_blooming_oasis", "और तुम्हारा रब तुम्हें इतना देगा, कि तुम राज़ी हो जाओगे।", ["राज़ी"], None),            # U5
    ("r_10b_stars_sky", "दुनिया में दीन की कामयाबी, और आख़िरत में शफ़ाअत और हौज़े कौसर।", ["शफ़ाअत"], None),      # K6
    ("r_10b_stars_sky", "सहीह मुस्लिम में है, कि एक बार नबी ﷺ ने हाथ उठाए, और रोते हुए कहा: ऐ अल्लाह, मेरी उम्मत, मेरी उम्मत।", ["मेरी उम्मत"], None),  # K6 Muslim 202
    ("r_10b_stars_sky", "तो अल्लाह ने पैग़ाम भेजा: हम तुम्हें तुम्हारी उम्मत के बारे में राज़ी करेंगे, और दुखी नहीं करेंगे।", ["राज़ी करेंगे"], None),  # K6 Muslim 202
    # ayah 6 [U6 K7]
    ("08_shelter_lamp", "अलम यजिद्का यतीमन फ़आवा।", [], 6),
    ("08_shelter_lamp_c", "उसने तुम्हें यतीम पाया, तो ठिकाना दिया।", ["ठिकाना"], None),                            # U6
    ("08_shelter_lamp", "वालिद पैदाइश से पहले चल बसे, माँ छह साल की उम्र में, और फिर पालने वाले दादा आठ साल की उम्र में।", ["छह साल"], None),               # K7
    ("08_shelter_lamp", "फिर चाचा अबू तालिब ने पाला, और नुबुव्वत के बाद भी हिफ़ाज़त की।", ["हिफ़ाज़त"], None),        # K7
    # ayah 7 [U7 K8] (never "gumraah": C10)
    ("09_star_path", "व वजदका ज़ाल्लन फ़हदा।", [], 7),
    ("09_star_path", "और तुम्हें राह की तफ़्सील से अनजान पाया, तो राह दिखाई।", ["राह दिखाई"], None),              # U7
    ("09_star_path_c", "यानी नुबुव्वत से पहले, किताब और शरीअत की तफ़्सील मालूम न थी।", ["तफ़्सील"], None),           # K8
    ("09_star_path", "अल्लाह ने वह्य भेजी, और उसी को रौशनी बनाकर राह दिखाई।", ["रौशनी"], None),                   # K8 (42:52)
    # ayah 8 [U8 K9]
    ("10_full_well", "व वजदका आइलन फ़अग़ना।", [], 8),
    ("10_full_well", "और तुम्हें तंगी में पाया, तो ख़ुशहाल कर दिया।", ["ख़ुशहाल"], None),                                 # U8
    ("10_full_well", "हज़रत ख़दीजा के साथ तिजारत में, अल्लाह ने बरकत दी।", ["बरकत"], None),                       # K9
    ("07_blooming_oasis", "और सहीह हदीस में है: असली अमीरी माल की ज़्यादती नहीं, दिल की अमीरी है।", ["दिल की अमीरी"], None),  # K9 Bukhari 6446
    # ayah 9 [U9 K10]
    ("11_orphan_care", "फ़अम्मल यतीमा फ़ला तक़हर।", [], 9),
    ("11_orphan_care", "तो यतीम पर सख़्ती मत करना।", ["यतीम"], None),                                           # U9
    ("11_orphan_care_c", "उसका हक़ न दबाओ, उसके लिए मेहरबान बाप जैसे बनो।", ["मेहरबान बाप"], None),                 # K10
    ("11_orphan_care", "सहीह बुख़ारी में है, नबी ﷺ ने बताया: यतीम की परवरिश करने वाला, जन्नत में उनके इतना क़रीब होगा, जैसे हाथ की दो मिली हुई उंगलियाँ।", ["दो मिली हुई उंगलियाँ"], None),  # K10 Bukhari 5304
    # ayah 10 [U10 K11]
    ("12_door_giving", "व अम्मस साइला फ़ला तनहर।", [], 10),
    ("12_door_giving", "और माँगने वाले को मत झिड़को।", ["मत झिड़को"], None),                                     # U10
    ("12_door_giving_c", "दे सको तो कुछ दे दो, वरना नरमी से, अच्छे लफ़्ज़ों में मना करो।", ["नरमी"], None),           # K11a
    ("12_door_giving", "और जो कुछ पूछने आए, उसे भी नरमी से जवाब दो।", ["पूछने"], None),                           # K11b
    # ayah 11 [U11 K12]
    ("13_family_meal", "व अम्मा बिनिअमति रब्बिका फ़हद्दिस।", [], 11),
    ("13_family_meal", "और अपने रब की नेमत का चर्चा करते रहो।", ["नेमत"], None),                                 # U11
    ("13_family_meal_c", "यही शुक्र है, घमंड नहीं: ज़बान से शुक्र, और दूसरों तक भलाई पहुँचाना।", ["शुक्र"], None),    # K12
    ("13_family_meal", "अबू दाऊद की हदीस में है: जो लोगों का शुक्रिया अदा नहीं करता, वो अल्लाह का शुक्र भी अदा नहीं करता।", ["शुक्रिया"], None),  # K12 Abu Dawud 4811
    # summary [P5 K3 K13]
    ("02_still_night", "तो पूरी सूरह का मतलब बस इतना है:", [], None),
    ("05_dawn_breaks", "अंधेरी रात के बाद सुबह आती है, अल्लाह अपने बंदे को छोड़ता नहीं।", ["छोड़ता नहीं"], None),    # P5 K3
    ("01_morning_sun", "और जैसे सहारा मिला, वैसे ही दूसरों का सहारा बनो, और हर नेमत पर शुक्र करो।", ["हर नेमत पर शुक्र"], None),  # K13
]
P = ["push_in", "pan_right", "pull_out", "pan_left"]
M = "shared/music/noor/Soaring.mp3"
lines = []
for i, (im, t, g, ay) in enumerate(L):
    d = {"n": i + 1, "text": t, "img": im, "motion": True, "preset": "push_in" if ay else P[i % 4],
         "overlay": [["dust", 0.08]], "sfx": [], "amb": [], "music": M, "ayah": bool(ay), "gold": g}
    if ay:
        d.update({"ar": AY[ay], "src": SRC.format(ay), "ayah_y": 90, "tr_y": 870, "src_y": 300})
    lines.append(d)
cfg = {"title": "Surah Ad-Duha 93", "voice": "Charon",
       "style": "Calm, warm, clear Hindi storyteller. Simple spoken Hindi, gentle, steady, normal conversational pace, correct Urdu sounds. "
                "Read the Arabic-sound lines plainly and clearly, not as recitation, no tune.",
       "tempo": 1.1, "ambience": "", "music": M, "music_vol": 0.12, "amp": 0.08, "amb_db": -6, "sfx_db": -3,
       "duck": True, "ayah_fs": 165, "ayah_outline": 6, "ayah_src": "", "lines": lines}
(S / "script.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
(S / "audio").mkdir(exist_ok=True)
(S / "output").mkdir(exist_ok=True)
print(len(lines), "lines,", sum(len(x["text"].split()) for x in lines), "words")
