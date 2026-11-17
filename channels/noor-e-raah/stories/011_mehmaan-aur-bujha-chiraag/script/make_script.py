import json
from pathlib import Path
S = Path(__file__).resolve().parent.parent
ROOT = S.parents[3]
QU = "shared/music/noor/Quietude_Sections_Merged.mp3"; RF = "shared/music/noor/River_Flute.mp3"
PD = "shared/music/seekh/Peaceful_Desolation.mp3"; TM = "shared/music/seekh/Touching_Moments_Two_Higher.mp3"
LD = "shared/music/clean/Lightless_Dawn.mp3"; SO = "shared/music/noor/Soaring.mp3"
ONE = RF  # RULES 2i (user 2026-11-17): one soft track for the whole video
H = "shared/sfx/history/"
CR = [H + "night_crickets_268962.mp3", -4]; FI = [H + "fire_crackle_508110.mp3", -6]; WI = [H + "wind_desert_675710.mp3", -6]
PL = [H + "palm_leaves_378725.mp3", -6]; CF = [H + "crowd_far_675054.mp3", -8]; MK = [H + "market_crowd_139981.mp3", -10]
# (img, text, music, amb, sfx, src, gold)
L = [
("01_night_house", "उस रात एक घर में सिर्फ़ बच्चों का थोड़ा सा खाना बचा था। और उसी रात, उस घर में एक भूखा मेहमान आया।", QU, [CR], [], None, ["भूखा मेहमान"]),
("02_lamp_glow", "फिर उस घर के पति-पत्नी ने जो किया, उसकी तारीफ़ ख़ुद क़ुरआन में आई।", QU, [CR], [], None, ["क़ुरआन"]),
("03_madinah_morning", "ये बात मदीना शहर की है, इस्लाम के शुरू के दिनों की।", RF, [PL], [], None, ["मदीना"]),
("04_travelers", "उन दिनों मक्का से बहुत से मुसलमान, अपना घर-बार छोड़ कर मदीना आए थे।", RF, [WI], [], None, []),
("05_welcome_house", "मदीना के जिन लोगों ने इनकी मदद की, उन्हें अंसार कहा जाता है। अंसार का मतलब है, मदद करने वाले।", RF, [PL], [], None, ["अंसार"]),
("06_palm_share", "अंसार ने इन लोगों को अपने घरों में जगह दी, और अपने खजूर के बाग़ों के फल में भी हिस्सेदार बनाया।", RF, [PL], [], "सहीह बुख़ारी 2325", []),
("07_tired_man", "एक दिन एक आदमी नबी ﷺ के पास आया। उसने बताया कि वो बहुत भूखा और थका हुआ है।", PD, [WI], [], "सहीह बुख़ारी 4889", []),
("08_messenger_walk", "नबी ﷺ ने अपनी पत्नियों के घर संदेसा भेजा, कि मेहमान के लिए कुछ खाना हो तो दे दें।", PD, [WI], [[H + "steps_sand_414310.mp3", 0.3, -8]], None, []),
("09_water_pot", "एक-एक करके हर घर से एक ही जवाब आया। हमारे पास पानी के सिवा कुछ नहीं है।", PD, [WI], [], "सहीह मुस्लिम 2054", ["पानी"]),
("10_empty_bowl", "यानी उस दिन नबी ﷺ के अपने घर में भी, सिर्फ़ पानी था।", PD, [WI], [], None, []),
("11_courtyard", "तब नबी ﷺ ने वहाँ बैठे लोगों से पूछा, आज रात इस मेहमान को अपने घर कौन ले जाएगा?", PD, [CF], [], "सहीह बुख़ारी 3798", []),
("12_man_stands", "अंसार में से एक आदमी खड़ा हुआ, और बोला, मैं ले जाऊँगा।", PD, [CF], [[H + "cloth_rustle_493264.mp3", 0.2, -8]], None, ["मैं ले जाऊँगा"]),
("13_two_walk", "सहीह मुस्लिम की एक रिवायत में, उनका नाम अबू तल्हा आता है।", PD, [WI], [[H + "steps_sand_560950.mp3", 0.2, -8]], "सहीह मुस्लिम 2054", ["अबू तल्हा"]),
("14_door_arrive", "वो मेहमान को साथ लेकर अपने घर पहुँचे, और पत्नी से कहा, ये अल्लाह के रसूल ﷺ का मेहमान है। इसकी अच्छी ख़ातिर करो।", PD, [CR], [[H + "wood_door_390123.mp3", 0.3, -6]], None, []),
("15_wife_hearth", "पत्नी ने बताया, घर में बच्चों के खाने के सिवा कुछ नहीं है।", PD, [FI], [], None, ["बच्चों के खाने"]),
("16_small_pot", "अब हालत ये थी, कि अगर मेहमान को खिलाएँ, तो बच्चे भूखे रहें। और घर वालों के अपने लिए तो कुछ था ही नहीं।", PD, [FI], [], None, []),
("17_couple_talk", "पति ने कहा, खाना तैयार करो, और चिराग़ जलाओ। बच्चे खाना माँगें, तो उन्हें किसी तरह बहला कर सुला देना।", PD, [FI], [], "सहीह बुख़ारी 3798", []),
("18_lamp_light", "पत्नी ने वैसा ही किया। उसने खाना तैयार किया, और चिराग़ जलाया।", QU, [FI], [], None, ["चिराग़"]),
("19_kids_sleep", "फिर माँ ने बच्चों को बहला कर सुला दिया।", QU, [CR], [], None, []),
("20_three_sit", "फिर तीनों खाने के लिए बैठे। मेहमान, और घर के पति-पत्नी।", QU, [CR], [], None, []),
("21_lamp_out", "तभी पत्नी उठी, जैसे चिराग़ ठीक करने जा रही हो। और उसने चिराग़ बुझा दिया।", QU, [CR], [[H + "cloth_rustle_493462.mp3", 0.4, -8]], "सहीह बुख़ारी 3798", ["चिराग़ बुझा दिया"]),
("22_dark_room", "कमरे में अँधेरा हो गया।", QU, [CR], [], None, []),
("23_pretend", "अँधेरे में पति-पत्नी ऐसे दिखाते रहे, जैसे वो भी साथ में खा रहे हों।", QU, [CR], [], "सहीह मुस्लिम 2054", []),
("24_guest_eats", "मेहमान ने आराम से खाना खाया।", QU, [CR], [], None, []),
("25_sleep_hungry", "और वो दोनों, उस रात भूखे ही सो गए।", QU, [CR], [], "सहीह बुख़ारी 3798", ["भूखे ही सो गए"]),
("26_dawn", "रात बीती, और सुबह हुई।", LD, [PL], [], None, []),
("27_walk_morning", "फिर वो अंसारी, नबी ﷺ के पास गए।", LD, [PL], [[H + "steps_sand_414310.mp3", 0.3, -8]], None, []),
("28_light_door", "नबी ﷺ ने उनसे कहा, कि रात को तुम दोनों ने जो किया, वो अल्लाह को बहुत पसंद आया।", TM, [], [], "सहीह बुख़ारी 3798", ["अल्लाह को बहुत पसंद आया"]),
("29_light_ray", "और उन्हीं के बारे में, क़ुरआन की ये आयत उतरी।", TM, [], [], "सहीह बुख़ारी 3798", []),
("30_ayah_card", "वो दूसरों को अपने से पहले रखते हैं, चाहे ख़ुद तंगी में हों।", TM, [], [], None, []),
("31_sharing_bread", "यानी अपनी ज़रूरत होते हुए भी, दूसरे की ज़रूरत पहले पूरी करना। क़ुरआन ने इसी बात की तारीफ़ की।", TM, [], [], None, []),
("32_open_hand", "उसी आयत में आगे आता है, कि जो अपने दिल की कंजूसी से बच गया, वही असल में कामयाब है।", TM, [], [], "क़ुरआन 59:9", ["कामयाब"]),
("33_market_give", "इस कहानी से हम क्या सीखते हैं? पहली बात, देने के लिए अमीर होना ज़रूरी नहीं। उस घर में बस बच्चों का खाना था, फिर भी उन्होंने दिया।", SO, [MK], [], None, ["अमीर होना ज़रूरी नहीं"]),
("34_dark_lamp", "दूसरी बात, उन्होंने मेहमान को पता ही नहीं चलने दिया। चिराग़ इसलिए बुझाया, ताकि उसे लगे कि घर वाले भी साथ खा रहे हैं।", SO, [CR], [], None, ["पता ही नहीं चलने दिया"]),
("35_night_stars", "तीसरी बात, अच्छा काम चुपचाप भी हो, तो अल्लाह उसे देखता है। उस अँधेरे कमरे की बात, अल्लाह ने क़ुरआन में हमेशा के लिए रख दी।", SO, [CR], [], None, ["अल्लाह उसे देखता है"]),
("36_lamp_end", "अगली बार जब आपके पास कम हो, और कोई ज़रूरतमंद सामने आए, तो उस बुझे हुए चिराग़ को याद करना।", SO, [CR], [], None, ["बुझे हुए चिराग़"]),
]
P = ["push_in", "pan_right", "pull_out", "pan_left"]
PUSH = {"01_night_house", "21_lamp_out", "22_dark_room", "28_light_door", "36_lamp_end"}
lines = []
for i, (img, t, m, amb, sfx, src, gold) in enumerate(L):
    l = {"n": i + 1, "text": t, "img": img, "motion": img != "30_ayah_card", "preset": "push_in" if img in PUSH else P[i % 4],
         "overlay": [["dust", 0.12]], "sfx": sfx, "amb": amb, "music": ONE, "ayah": img == "30_ayah_card", "gold": gold}
    if src:
        l["src"] = src
    lines.append(l)
tz = ROOT / ".claude/worktrees/hi-30f55e/channels/noor-e-raah/stories/006_imaan-shorts/research/quran-uthmani.txt"
a = [x for x in tz.read_text(encoding="utf-8").splitlines() if x.startswith("59|9|")][0].split("|", 2)[2]
i0 = a.index("وَيُؤْثِرُونَ"); i1 = a.index("خَصَاصَةٌ") + len("خَصَاصَةٌ")
cfg = {"title": "मेहमान और बुझा हुआ चिराग़", "voice": "Charon",
       "style": "Calm, warm, clear Hindi storyteller for an Islamic history video. Simple everyday spoken Hindi, gentle emotion, normal conversational pace, correct Urdu sounds (ज़, फ़, क़, ख़, ग़).",
       "tempo": 1.0, "music": ONE, "music_vol": 0.5, "amp": 0.08, "amb_db": -6, "sfx_db": -3, "duck": True,
       "ayah_ar": a[i0:i1], "ayah_src": "सूरह अल-हश्र 59:9", "ayah_fs": 120, "lines": lines}
(S / "script.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(lines), "lines", sum(len(l["text"].split()) for l in lines), "words")
print(cfg["ayah_ar"])
