# 008 — सूरह अल-फ़ील (105) | नूर-ए-राह — script (SURAH MODE, RULES 1d: EK narrator, koi sawaal nahi)

> **Format (007 ka dhaancha, RULES 1d se):** har jumla = Arabic (Tanzil, bytes unchanged, `research/sources.json` se code se copy) + `USTAAD — UCHARAN` (wahi Arabic Devanagari me, `research/ucharan.md` se hu-ba-hu) + `BHAAVARTH` + 1-2 chhote vaakya ka MATLAB (kul 2-3 vaakya per jumla).
> Line numbers file ke kram me 1..N (koi gap nahi); UCHARAN hamesha apne BHAAVARTH se pehle; aakhri bolne wali line aur aakhri cue ka number CHECKS me; `long/render.json` me `end_from` = aakhri bolti line.

## HEADER
- **Channel / format:** noor-e-raah, surah explainer, RULES 1d: **EK narrator** (script me role-label `USTAAD` rakha hai kyunki `scripts/noor_build.py` ka parser wahi label padhta hai; awaaz = Gemini **Charon**, user 2026-11-13, RULES 1d; 007 ne Algieba use kiya tha, runbook `DAILY_LONG.md` me abhi purana Algieba likha hai — RULES 1d ka Charon lagu). Koi doosri awaaz nahi, koi sawaal nahi (hook me bhi, ant me bhi), koi intro-note, koi tilawat-disclaimer, koi [NOTE] nahi. Kram: parichay -> shan-e-nuzul -> aayat-dar-aayat -> seekh. Story 008, `series_queue` order 7. Kharcha script ke liye Rs0.
  5 ayat, har ayat 2 jumle: 1 poori-surah block (AYAH 1, usme UCHARAN nahi) + 10 jumla-blocks (AYAH 2-3 = 105:1, AYAH 4-5 = 105:2, AYAH 6-7 = 105:3, AYAH 8-9 = 105:4, AYAH 10-11 = 105:5).
- **Length target:** 3:20-3:50 (estimate neeche), `render.json` tempo **1.11**, TTS style "clear, steady, slightly brisk, not slow".
- **Content source:** sirf `research/dossier.md` + `sources.json` + `ucharan.md` (Khoji MODE 3, 2026-11-14). Tags: parichay **[P#]**, shan-e-nuzul **[N#]**, matlab **[M#]/[K#]**, tarjuma **[T2]**, ucharan **[U#]**, agli video **[NEXT]**. Production me tags spoken text/captions se hata diye jaayenge.
- **HOOK (line 3, bina sawaal):** "एक लश्कर हाथी के साथ काबा ढहाने निकला — और उसकी चाल बेकार हो गई।" Pehla poora Arabic (line 5) ~0:17.
- **Dossier ke faisle jo lagu hue:** (1) **koi alag sabab-e-nuzul nahi** (N1): ek line me saaf kehte hain; surah ek jaane-maane waqie ki taraf ishara hai; (2) Makki = P2 (Qurtubi ijma', quran.com, Alim) -> "ये मक्की सूरह है", koi ikhtilaaf nahi mila; (3) **DROP:** nuzool ka kramank (P3, ek source), doosra naam "अलम तरा" (P4, ek source), CE saal (570/571), lashkar ki ginti (C4), parindon ka rang/shakl (C2), patthar ki ginti/size aur gore vivaran (C3), girja jalane wala (C1), Yemen ka itihaas (C5), **Abdul-Muttalib ki rivayat (N4) poori drop** (Tabari ke editors ne kuch zanjeeren kamzor likhi; surakshit nahi), Nabi ﷺ ki paidaish ka koi zikr, Hudaybiyyah wala hadith (C8), fazilat (Z1); (4) waqia ka saal: sirf "अरब उस साल को आमुल फ़ील कहते थे" (N2), fasle/ankde nahi; (5) "अबाबील" = sirf "झुंड के झुंड" (K6); "सिज्जील" = "पकी हुई मिट्टी का कंकर" (K8); (6) T1 ka "ऐ रसूल" izafa nahi liya; "खरन्जों की कंकरियाँ" nahi liya.
- **Arabic:** Tanzil Uthmani (CC BY 3.0), `research/sources.json` -> `ayat[].text`, **code se copy** (koi NFC/NFKC, retype nahi). 105:1 ka Bismillah-prefix sources.json me pehle hi hata hua. AYAH 1 = 105:1..105:5 ek-ek space se joda; jumla-blocks = `text.split(' ')` ke shabd (105:1 [0:5],[5:7]; 105:2 [0:3],[3:5]; 105:3 [0:2],[2:4]; 105:4 [0:2],[2:4]; 105:5 [0:1],[1:3]); joda hua == poori ayat (generator me assert). **PC par: sha256 (sources.json me abhi null) + Amiri render zoom (105:1 `بِأَصْحَٰبِ` khanjari alif, `رَبُّكَ` shadda; 105:2 `فِى`; 105:4 `مِّن`, `سِجِّيلٍ`; 105:5 `مَّأْكُولٍۭ`, `كَعَصْفٍ`).**
- **Audio:** koi tilawat nahi, is baare me video me kuch nahi kehte. UCHARAN = Devanagari me Arabic shabd, screen par Arabic ke neeche. Music continuous (RULES 1c, ~19 LU neeche), har Arabic block par halka swoosh. Tracks: Soaring (intro+parichay) -> River Flute. Ambience: halki hawa (CC0).
- **Tarjuma = SARAL BHAAVARTH (RULES 1a):** teen tarjumon ke saanjhe matlab par apne shabdon me. Label (screen): **"सरल भावार्थ — माने हुए तर्जुमों के आधार पर"**. Dhyan: bhaavarth me "क्या तुमने नहीं देखा" Quran ke shabdon ka tarjuma hai, darshak se sawaal nahi.
- **Visuals:** sirf jagah, aasmaan, roshni, raaste, patthar-ghati, khaali kamra. **Koi Nabi, Sahabi, farishta, insaan nahi — na aakaar, na parchhai, na haath.** Haathi, lashkar, parinde, gira hua lashkar kisi image me nahi (library me hain nahi; RULES 1d: nayi image nahi) — sirf mood: lambe raaste, door kshitij, khaali aasman. Koi likha harf image me nahi.
- **Images (RULES 1d):** poori reuse (`image_library.md` + earlier stories), 0 nayi, Rs0; thumbnail wallpaper nayi (free Cloudflare pehle).
- **Niyam:** koi fiqh hukm, koi firqa, koi "chhoda gaya" baat nahi. Kisi qaum/shaks par ilzam nahi. "guarantee/100%/sawab/hifazat ki dua" jaise shabd nahi.
- **Spoken honorific:** "नबी सल्लल्लाहु अलैहि वसल्लम" poora; koi Sahabi naam nahi.

---

## INTRO (`part: intro`, hook)
[SCREEN: subah ki pehli roshni me registan ka lamba khaali raasta, door kshitij; ऊपर Arabic title سُورَةُ ٱلْفِيلِ (font se) aur neeche chhota caption "हाथी वालों का वाक़िया". Pehla frame bina awaaz ke samajh aaye: khaali lamba raasta.]
1. [MUSIC soft: Soaring — intro + parichay]
2. [AMBIENCE: halki registani hawa (Freesound CC0)]
3. USTAAD: "एक लश्कर हाथी के साथ काबा ढहाने निकला — और उसकी चाल बेकार हो गई। ये है सूरह अल-फ़ील।" [P5][N3]
## 1. SURAH KA PARICHAY
[SCREEN: chhota card: "सूरह अल-फ़ील · क़ुरआन की 105वीं सूरह" + "5 आयतें"; peeche sunehri ghaati]
4. USTAAD: "अल-फ़ील यानी हाथी। पहली आयत के "अस्हाबिल फ़ील", यानी हाथी वालों, से इसका नाम है। ये मक्की सूरह है।" [P1][P2]
### [AYAH 1]
[SCREEN: badlon se utarti sunehri kirnein; poori surah Arabic me (5 ayat) — swoosh ke saath aati hai]
5. [SWOOSH — ARABIC ON SCREEN]
ARABIC: أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَٰبِ ٱلْفِيلِ أَلَمْ يَجْعَلْ كَيْدَهُمْ فِى تَضْلِيلٍ وَأَرْسَلَ عَلَيْهِمْ طَيْرًا أَبَابِيلَ تَرْمِيهِم بِحِجَارَةٍ مِّن سِجِّيلٍ فَجَعَلَهُمْ كَعَصْفٍ مَّأْكُولٍۭ
6. USTAAD: "ये रही पूरी सूरह। पाँच छोटी आयतें, एक ही बहाव — याद दिलाना, चाल का बेकार होना, परिंदे, कंकर, और बर्बादी।" [P6]
7. [MUSIC continue: River Flute — matlab]
## 2. SHAN-E-NUZUL
[SCREEN: Makka-jaisi ghaati ki raat, kaale pahaad, khaali raasta; koi insaan nahi, koi gumbad/minar nahi]
8. USTAAD: "इस सूरह का कोई अलग सबब-ए-नुज़ूल माने हुए तफ़्सीर में नहीं मिलता। सूरह ख़ुद एक जाने-माने वाक़िये, अस्हाबिल फ़ील, की तरफ़ इशारा करती है।" [N1]
9. USTAAD: "रिवायतों के मुताबिक़ यमन का हाकिम अबरहा हाथी के साथ अपना लश्कर लेकर काबा ढहाने निकला।" [N3]
10. USTAAD: "रिवायत में आता है कि हाथी आगे बढ़ने से रुक गया और बैठ गया।" [N5]
11. USTAAD: "ये वाक़िया उस साल हुआ, जिसे अरब "आमुल फ़ील", यानी हाथी का साल, कहते थे।" [N2]
12. USTAAD: "इब्ने इसहाक़ की रिवायत के मुताबिक़, जो इब्ने कसीर ने दी है, नबी सल्लल्लाहु अलैहि वसल्लम ने ये एहसान क़ुरैश को याद दिलाया।" [N1][M7]
## 3. AAYAT-DAR-AAYAT
[SCREEN (har Arabic block): Arabic bade Amiri font me (Tanzil Uthmani, bytes unchanged), uske neeche UCHARAN (Devanagari), upar chhota label "सरल भावार्थ — माने हुए तर्जुमों के आधार पर" (sirf BHAAVARTH line par), neeche Hindi caption. Har jumla alag Arabic block. Koi insaan/farishta ka roop nahi.]
### [AYAH 2]  (= 105:1 pehla jumla)
[SCREEN: subah ka khaali raasta, door kshitij, dhoop; koi insaan nahi]
13. [SWOOSH — ARABIC ON SCREEN]
ARABIC: أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ
14. USTAAD — UCHARAN: "अलम तरा कैफ़ा फ़अला रब्बुक" [U1]
15. USTAAD — BHAAVARTH: "पहली आयत: क्या तुमने नहीं देखा, तुम्हारे रब ने क्या किया।" [T2]
16. [MUSIC continue: River Flute — matlab]
17. USTAAD — MATLAB: "ये वाक़िया इतना मशहूर था कि मानो सबने देखा हो। "रब" यानी अल्लाह।" [M1]
### [AYAH 3]  (= 105:1 doosra jumla)
[SCREEN: wahi raasta, doosra crop; koi insaan nahi]
18. [SWOOSH — ARABIC ON SCREEN]
ARABIC: بِأَصْحَٰبِ ٱلْفِيلِ
19. USTAAD — UCHARAN: "बि अस्हाबिल फ़ील" [U2]
20. USTAAD — BHAAVARTH: "हाथी वालों के साथ।" [T2]
21. [MUSIC continue: River Flute — matlab]
22. USTAAD — MATLAB: "हाथी वाले यानी अबरहा का लश्कर, जो यमन से काबा ढहाने आया था।" [K2]
### [AYAH 4]  (= 105:2 pehla jumla)
[SCREEN: khaali maidan me door ek chhota nishaan; koi insaan nahi]
23. [SWOOSH — ARABIC ON SCREEN]
ARABIC: أَلَمْ يَجْعَلْ كَيْدَهُمْ
24. USTAAD — UCHARAN: "अलम यज्अल कैदहुम" [U3]
25. USTAAD — BHAAVARTH: "दूसरी आयत, पहला हिस्सा: क्या उसने उनकी चाल को" [T2]
26. [MUSIC continue: River Flute — matlab]
27. USTAAD — MATLAB: ""कैद" यानी चाल, साज़िश — काबा ढहाने का मंसूबा।" [K3]
### [AYAH 5]  (= 105:2 doosra jumla)
[SCREEN: wahi maidan, doosra crop; koi insaan nahi]
28. [SWOOSH — ARABIC ON SCREEN]
ARABIC: فِى تَضْلِيلٍ
29. USTAAD — UCHARAN: "फ़ी तज़्लील" [U4]
30. USTAAD — BHAAVARTH: "दूसरा हिस्सा: बेकार नहीं कर दिया।" [T2]
31. [MUSIC continue: River Flute — matlab]
32. USTAAD — MATLAB: ""तज़्लील" यानी बेकार, ग़लत रास्ते पर। उनकी चाल अपने मक़सद तक पहुँची ही नहीं।" [K4]
### [AYAH 6]  (= 105:3 pehla jumla)
[SCREEN: dhalte aasman ka khula kshitij; koi insaan nahi, koi parinda ka chitra nahi]
33. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَأَرْسَلَ عَلَيْهِمْ
34. USTAAD — UCHARAN: "व अर्सला अलैहिम" [U5]
35. USTAAD — BHAAVARTH: "तीसरी आयत, पहला हिस्सा: और उन पर भेजे।" [T2]
36. [MUSIC continue: River Flute — matlab]
37. USTAAD — MATLAB: "यानी अल्लाह ने उन पर परिंदे भेजे।" [K5]
### [AYAH 7]  (= 105:3 doosra jumla)
[SCREEN: wahi aasman, doosra crop; koi insaan nahi]
38. [SWOOSH — ARABIC ON SCREEN]
ARABIC: طَيْرًا أَبَابِيلَ
39. USTAAD — UCHARAN: "तैरन अबाबील" [U6]
40. USTAAD — BHAAVARTH: "दूसरा हिस्सा: परिंदों के झुंड।" [T2]
41. [MUSIC continue: River Flute — matlab]
42. USTAAD — MATLAB: "तफ़्सीरों में "अबाबील" का मतलब झुंड के झुंड आया है, यानी एक के पीछे एक।" [K6]
### [AYAH 8]  (= 105:4 pehla jumla)
[SCREEN: patthar-ghati ke bade patthar; koi insaan nahi]
43. [SWOOSH — ARABIC ON SCREEN]
ARABIC: تَرْمِيهِم بِحِجَارَةٍ
44. USTAAD — UCHARAN: "तरमीहिम बि हिजारतिम" [U7]
45. USTAAD — BHAAVARTH: "चौथी आयत, पहला हिस्सा: जो उन पर कंकर-पत्थर फेंकते थे।" [T2]
46. [MUSIC continue: River Flute — matlab]
47. USTAAD — MATLAB: "यानी वो परिंदे उन पर कंकर फेंकते थे।" [K7]
### [AYAH 9]  (= 105:4 doosra jumla)
[SCREEN: sookhi zameen, khaali raasta; koi insaan nahi]
48. [SWOOSH — ARABIC ON SCREEN]
ARABIC: مِّن سِجِّيلٍ
49. USTAAD — UCHARAN: "मिन सिज्जील" [U8]
50. USTAAD — BHAAVARTH: "दूसरा हिस्सा: सिज्जील के।" [T2]
51. [MUSIC continue: River Flute — matlab]
52. USTAAD — MATLAB: "तफ़्सीरों में "सिज्जील" का मतलब पकी हुई मिट्टी का कंकर-पत्थर आया है।" [K8]
### [AYAH 10]  (= 105:5 pehla jumla)
[SCREEN: khaali kamra, subah ki roshni; koi insaan nahi]
53. [SWOOSH — ARABIC ON SCREEN]
ARABIC: فَجَعَلَهُمْ
54. USTAAD — UCHARAN: "फ़जअलहुम" [U9]
55. USTAAD — BHAAVARTH: "पाँचवीं आयत, पहला हिस्सा: फिर उन्हें कर दिया।" [T2]
56. [MUSIC continue: River Flute — matlab]
57. USTAAD — MATLAB: "यानी अल्लाह ने उन्हें एक अंजाम तक पहुँचा दिया।" [K9]
### [AYAH 11]  (= 105:5 doosra jumla)
[SCREEN: wahi khaali kamra, crop; koi insaan nahi]
58. [SWOOSH — ARABIC ON SCREEN]
ARABIC: كَعَصْفٍ مَّأْكُولٍۭ
59. USTAAD — UCHARAN: "कअस्फ़िम मअकूल" [U10]
60. USTAAD — BHAAVARTH: "दूसरा हिस्सा: खाए हुए भूसे जैसा।" [T2]
61. [MUSIC continue: River Flute — matlab]
62. USTAAD — MATLAB: ""खाया हुआ भूसा" यानी वो चीज़, जो पूरी तरह बर्बाद और कमज़ोर हो गई।" [K10]
## 4. SEEKH
[SCREEN: subah ka sunehra ujala, khula raasta; seekh ke teen chhote cards font se]
63. USTAAD: "पहली सीख: ताक़तवर की ताक़त अल्लाह के सामने कुछ नहीं।" [M6]
64. USTAAD: "दूसरी: किसी की चाल अल्लाह के फ़ैसले को नहीं रोक सकती।" [M6]
65. USTAAD: "तीसरी: अल्लाह अपने घर की हिफ़ाज़त ख़ुद करता है।" [M6][P5]
[SCREEN (end, aakhri ~15 s end-screen area khaali): tagline card "क़ुरआन, आसान ज़बान में।" + chhota card "Arabic text: Tanzil Project, tanzil.net" + "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"]
66. USTAAD: "अगली बार, नूर-ए-राह में: सूरह अल-काफ़िरून।" [NEXT]
67. [MUSIC: River Flute dheere fade-out; aakhri ~3 s sirf gentle breeze]

## SOURCES (description ke liye)
- Arabic Quran text: Tanzil Project (https://tanzil.net) — Tanzil Quran Text, Copyright (C) 2007-2021 Tanzil Project, License: Creative Commons Attribution 3.0. Text unchanged; check https://tanzil.net/updates/ for changes.
- सरल भावार्थ: माने हुए तर्जुमों (Suhel Farooq Khan / Tanzil hi.hindi; Muhammad Farooq Khan; Shaikh-ul-Hind Mahmud Hasan) के आधार पर — शब्दशः तर्जुमा नहीं।
- Tafseer: al-Tabari, Jami' al-Bayan (105); Tafsir Ibn Kathir (105); al-Qurtubi, al-Jami' li-Ahkam al-Qur'an (105); Ma'ariful Qur'an (Mufti Muhammad Shafi); quran.com / Alim surah info (parichay).
- उच्चारण (Arabic की हिंदी लिपि): टंज़ील ट्रांसलिटरेशन और quran411 से मिलाकर — पढ़ने की मदद।
- Surah data: Tanzil Quran Metadata (CC BY 3.0, https://tanzil.net).
- Music: "Soaring" Kevin MacLeod (incompetech.com) · "River Flute" Kevin MacLeod (incompetech.com) — both CC BY 4.0, http://creativecommons.org/licenses/by/4.0/
- Ambience: freesound.org (CC0)

## SOURCE MAP — har tag dossier me kahan (Munshi ke liye)
| Tag | Dossier | Grade | Lines |
|---|---|---|---|
| P1 | P1 (naam "ashab-il-feel" se; 105vi/5 ayat sirf screen card) | maana hua | 4 |
| P2 | P2 (makki; Qurtubi ijma', quran.com, Alim) | maana hua | 4 |
| P5 | P5 (Allah ne Ghar ki hifazat; chaal bekaar) | maana hua | 3, 65 |
| P6 | P6 (5 tukde, ek bahav: yaad dilana -> chaal -> parinde -> patthar -> bhoosa) | maana hua | 6 |
| N1 | N1 (koi alag sabab-e-nuzul nahi; surah waqie ki taraf ishara; IK/Ibn Ishaq: Nabi ﷺ ne ehsaan Quraysh ko yaad dilaya) | maana hua | 8, 12 |
| N2 | N2 (waqia "aamul feel" me; sirf saal ka naam, koi ankda/fasla nahi) | maana hua (saal ka sambandh) | 11 |
| N3 | N3 (Abraha, Yemen ka hakim, haathi ke saath lashkar le kar Ka'ba dhaane chala; girja/kaaran nahi) | maana hua | 3, 9 |
| N5 | N5 (haathi aage badhne se ruk gaya/baith gaya; naam Mahmud nahi liya) | maana hua | 10 |
| M7 | M7 (Quraysh ko yaad-dehaani; IK EN) | maana hua | 12 |
| T2 | dossier 1.2 (saral bhaavarth) | decision 001 | 15, 20, 25, 30, 35, 40, 45, 50, 55, 60 |
| U1-U10 | research/ucharan.md [U1-U10] + sources.json T3 | decision 2026-10-30 | 14, 19, 24, 29, 34, 39, 44, 49, 54, 59 |
| M1/K1 | M1 (alam tara = yaad dilana; waqia mash'hoor; Ma'ariful, IK, Tabari; "Rabb" = Allah) | maana hua | 17 |
| K2 | K2 (ashab-il-feel = Abraha ka lashkar jo Yemen se aaya; 4 tafseer) | maana hua | 22 |
| K3 | K3/M2 (kayd = chaal, saazish; Tabari, IK) | maana hua | 27 |
| K4 | K4 (tadleel = bekaar/ghalat raaste par; Tabari, IK, Qurtubi) | maana hua | 32 |
| K5 | K5/M3 (parinde bheje; Tabari, IK, Qurtubi) | maana hua | 37 |
| K6 | K6 (ababeel = jhund ke jhund, ek ke peeche ek; Tabari, IK) | maana hua | 42 |
| K7 | K7/M4 (parinde kankar phenkte the; Tabari, IK, Ma'ariful) | maana hua | 47 |
| K8 | K8 (sijjeel = pakki mitti ka kankar-patthar; Tabari, IK) | maana hua | 52 |
| K9 | K9/M5 (phir ek anjaam par pahuncha diya; Tabari, IK) | maana hua | 57 |
| K10 | K10 (asf ma'kool = khaaya hua bhoosa, barbaadi aur kamzori ki misaal; Tabari, IK) | maana hua | 62 |
| M6/K11 | M6 (taaqat Allah ke saamne kuch nahi; chaal Allah ke faisle ko nahi rok sakti; Allah apne Ghar ki hifazat; IK, Qurtubi, Ma'ariful) | maana hua | 63, 64, 65 |
| NEXT | series_queue order 8: al-kafirun | queue | 66 |
Koi hadith section / fazilat nahi (Z1). Chhodi gayi C1-C10 SHAMIL NAHI; P3 (kramank), P4 ("अलम तरा" naam), N4 (Abdul-Muttalib) drop (upar HEADER).

## IMAGES (long/images.json; **0 NAYI image, sab reuse + crop, Rs0**; thumbnail wallpaper alag nayi, free engine pehle)
- A `003/04_dawn_sand_ridge`  - B `005/23_golden_valley_full_light`  - C `002/11_sunrays_clouds`  - D `003/03_makka_valley_night`  - E `003/05_paths_to_oasis`  - F `002/05_dawn_horizon`  - G `002/10_ring_in_desert`  - H `003/07_sea_horizon_dusk`  - I `003/08_empty_room_morning`  - J `002/09_lit_door`  - K `003/02_lamp_single_flame`  - L `002/03_madina_dawn_houses`
| Lines | Image | Shot | Lagbhag samay |
|---|---|---|---|
| 3 | A poori | subah ka lamba khaali raasta (hook) | 0-9 s |
| 4 | B poori | parichay card ke peeche | 9-17 s |
| 5 (AYAH 1) | C poori; line 6: C crop (fx 0.5 fy 0.4 zc 1.5) | poori surah Arabic | 17-25, 25-33 s |
| 8 | D poori | Makka-jaisi ghaati raat | 33-43 s |
| 9 | D crop (0.5, 0.75, 1.5) | | 43-52 s |
| 10-11 | E poori; line 12: E crop (0.3, 0.6, 1.5) | lashkar ke raaste (sirf raaste) | 52-70 s |
| AYAH 2-3 (105:1) | F poori; AYAH 3: F crop (0.5, 0.6, 1.5) | | |
| AYAH 4-5 (105:2) | G poori; AYAH 5: G crop (0.5, 0.62, 1.6) | chaal ka bekaar hona, khaali maidan | |
| AYAH 6-7 (105:3) | H poori; AYAH 7: H crop (0.5, 0.3, 1.5) | khula aasman (koi parinda image me nahi) | |
| AYAH 8-9 (105:4) | D crop (0.2, 0.4, 1.6); AYAH 9: A crop (0.7, 0.7, 1.5) | patthar, sookhi zameen | |
| AYAH 10-11 (105:5) | I poori; AYAH 11: I crop (0.5, 0.7, 1.6) | khaali kamra | |
| 63 | J poori | seekh 1 | |
| 64 | K poori | seekh 2 | |
| 65 | L poori | seekh 3 | |
| 66-67 | B crop (rect fx 0.7, fy 0.5, zc 1.4) | ant | |
Pehle ~60 s: A (0-9) · B (9-17) · C (17-25) · C crop (25-33) · D (33-43) · D crop (43-52) · E (52-60+). Same (image, rect) dobara nahi; D ka teesra rect (ayah 8) alag. Koi insaan/haathi/lashkar/parinda image me nahi (library me hain nahi; nayi image nahi banti — RULES 1d).
Kul: 21 clips, 12 base images, 0 nayi.

## LENGTH ESTIMATE (calibrated to 007 FINAL: 34 lines, 434 shabd, voice 183.6 s ~ 0.42 s/shabd (UCHARAN shaamil), 7 Arabic blocks, kul 3:28.8 tempo 1.11 — my pehle ka 0.45/0.73 wala formula 007 ko 4:14 batata tha, asli 3:29, isliye 007 ke asli aankde se)
| Hissa | Shabd | Anuman |
|---|---|---|
| USTAAD (UCHARAN chhod kar, tags bina) | 367 | ~152 s |
| UCHARAN (10 lines) | 26 | ~19 s (0.73 s/shabd) |
| Arabic blocks 11 x ~3.3 s + sections + ant (007 ke overhead ~25 s / 7 blocks) | | ~40 s |
| **Kul** | **393** | **~211 s ≈ 3:31** (band ±0:20 = 3:11-3:51; target 3:20-3:50) |
**Pehla poora Arabic (line 5) ~0:17.** Agar asli TTS 3:55 paar kare to pehle trim: line 11 (N2 saal), line 12, line 6 (aakhri hissa).
Agar 3:15 se kam aaye: kuch nahi jodna (target se thoda neeche chalega).

## THUMBNAIL (thumbnail.json, v3 ka dhaancha)
Arabic سُورَةُ ٱلْفِيلِ · Hindi सूरह अल-फ़ील · chip: "पाँच आयतें" · hook text: "*हाथी* वाला लश्कर —\nकाबा ढहाने आया था" (<= 4 bade shabd wale do chhote misre; koi sawaal nahi; title ke shabd hu-ba-hu nahi; koi chehra/aakaar/parinda nahi). Scene: subah ki sunehri roshni me khaali lamba registani raasta, door dhool ki halki lakeer, left 45% shaant dark-blue. Wallpaper NAYI, free engine (Cloudflare flux) pehle; paid sirf fallback aur balance > Rs50 floor par. **Haathi/lashkar/insaan prompt me nahi** (no people, no figures, no animals, no text, no domes).

## TITLE options (search-phrase pehle; suffix "| Noor-e-Raah")
1. **Surah Fil ka Matlab Hindi Mein | 5 Ayat, Haathi Walon ka Waqia aur Har Ayat ka Matlab | Noor-e-Raah** (recommended; queue search_title "Surah Fil ka Matlab Hindi Mein" se match)
2. Surah Al-Fil Hindi Mein | Har Ayat ka Saral Matlab | Noor-e-Raah
3. Surah Fil ka Matlab | Haathi Walon ki Chaal Kaise Bekaar Hui | Noor-e-Raah

## CONTINUITY / CHECKS
- Koi Sahabi/Nabi aakaar nahi; Abdul-Muttalib, Hudaybiyyah-hadith, Nabi ﷺ ki paidaish ka zikr, CE saal, lashkar ki ginti, parindon ka rang/shakl, gore vivaran: sab DROP. Koi hadith-fazilat nahi.
- Ek narrator (Charon), koi SAWAAL line nahi, koi sawaal-vaakya spoken text me nahi (bhaavarth line 15 "क्या तुमने नहीं देखा..." aur 25 Quran ke shabdon ka tarjuma hai), koi [NOTE], koi tilawat-disclaimer.
- 007 se alag: 5 ayat x 2 jumle (10 Arabic blocks), hook = lashkar ki chaal bekaar, shan-e-nuzul me ek waqia (Abraha) + "koi alag sabab nahi", mood subah/dhool/khaali raaste.
- Line numbers 1..67 file ke kram me; UCHARAN (14, 19, 24, 29, 34, 39, 44, 49, 54, 59) apne BHAAVARTH (15, 20, 25, 30, 35, 40, 45, 50, 55, 60) se pehle; **aakhri bolti line 66; aakhri cue 67; render.json end_from = 66.**
- UCHARAN har line `research/ucharan.md` ke Devanagari column se hu-ba-hu (U1-U10); Arabic = sources.json `ayat[].text` se code se (assert joined == poori ayat).
- Open PC checks (Sanchalak/user): sha256 + Amiri zoom (HEADER); ucharan ke 4 open points (ض -> ज़ "तज़्लील"; "तैरन"; "कैफ़ा"; full-block vs jumla-block vowels) — jumla blocks me ucharan.md ka tay roop liya; Tanzil licence page dobara kholna (2026-11-03 ke baad).

