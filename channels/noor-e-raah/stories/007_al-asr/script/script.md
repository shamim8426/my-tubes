# 007 — सूरह अल-अस्र (103) | नूर-ए-राह — script (SURAH MODE, RULES 1d: EK narrator, koi sawaal nahi)

> **Format (006 ka dhaancha, RULES 1d se):** har jumla = Arabic (Tanzil, bytes unchanged, code se copy) + `USTAAD — UCHARAN` (wahi Arabic Devanagari me, saada Hindi andaaz me) + `BHAAVARTH` + 2-3 chhote vaakya ka MATLAB.
> Line numbers file ke kram me 1..51 (koi gap nahi); UCHARAN hamesha apne BHAAVARTH se pehle; **aakhri bolne wali line 50, aakhri cue 51 -> `long/render.json` me `end_from: 50`.**

## HEADER
- **Channel / format:** noor-e-raah, surah explainer, RULES 1d (user 2026-11-09): sirf **USTAAD (Algieba)**; koi doosri awaaz nahi, koi sawaal nahi (hook me bhi, ant me bhi), koi intro-note nahi, koi tilawat-disclaimer nahi. Kram: parichay -> shan-e-nuzul -> aayat-dar-aayat -> seekh. Story 007, `series_queue` order 6. Kharcha script ke liye Rs0.
  Sirf 3 ayat par 103:3 lambi (9 shabd, 4 jumle): 1 poori-surah block (AYAH 1, usme UCHARAN nahi) + 6 jumla-blocks (AYAH 2 = 103:1, AYAH 3 = 103:2, AYAH 4-7 = 103:3 ke 4 jumle).
- **Length target:** 3:30-4:30 (estimate neeche), `render.json` tempo **1.11**, TTS style "clear, steady, slightly brisk, not slow".
- **Content source:** sirf `research/dossier.md` + `sources.json` + `ucharan.md` (Khoji MODE 3, 2026-11-13). Tags: parichay **[P#]**, shan-e-nuzul **[N#]**, matlab **[M#]/[K#]**, tarjuma **[T2]**, ucharan **[T3]**, agli video **[NEXT]**. Production me tags spoken text/captions se hata diye jaayenge.
- **HOOK (line 3, bina sawaal):** "तीन आयतें — वक़्त की क़सम, इंसान का घाटा, और घाटे से बचने का रास्ता।" Pehla poora Arabic (line 5) ~0:25-0:28.
- **Dossier ke faisle jo lagu hue:** (1) **koi sabab-e-nuzul nahi** (N1): ek line me saaf kehte hain, koi kahani/waqia nahi jodte (Musaylima/'Amr C1 chhoda); (2) Makki/Madani = "ज़्यादातर उलमा ... मक्की; क़तादा वग़ैरह मदनी" (P2); **nuzool ka kramank NAHI bola** (P3 sirf ek source); (3) Tabarani wala Sahaba-riwayat sirf "रिवायत में आता है", **koi naam nahi** (N3; number/darja PC par baaki); (4) "ज़माने/वक़्त की क़सम" = core (M1); "asr ki namaz" sirf ikhtilaaf ki ek line (K2, line 17), T1 ka "नमाज़े अस्र की क़सम" tarjuma nahi liya; (5) fazilat/sawab ka koi daava nahi (Z1); koi hadith section nahi, C1-C6 poora chhoda (Shafi'i ka kathan bhi nahi, wording ka jokhim); (6) "ताकीद/हुक्म/वसीयत" ki jagah "याद दिलाते रहे".
- **Arabic:** Tanzil Uthmani (CC BY 3.0), `research/sources.json` -> `ayat[].text`, **code se copy** (koi NFC/NFKC, retype nahi). **103:1: sources.json/Tanzil file me Bismillah-prefix hai (`بِسْمِ ... ٱلرَّحِيمِ وَٱلْعَصْرِ`); Bismillah surah ki ayat nahi, isliye (006 ki tarah) sirf aakhri shabd `وَٱلْعَصْرِ` liya, code se `text.split(' ')[4]`.** AYAH 1 = (103:1 bina Bismillah) + 103:2 + 103:3 ek-ek space se joda; 103:3 ke jumle = `text.split(' ')` ke shabd [0:3], [3:5], [5:7], [7:9] (joda hua == poori ayat). **PC par: sha256 (103:2, 103:3 ka sources.json se match; 103:1 ka bina-Bismillah hash naya) + Amiri render zoom (103:2 khanjari alif/alif maksura, 103:3 `ءَامَنُوا۟` / `وَعَمِلُوا۟` / `وَتَوَاصَوْا۟` ka chhota gol sukoon, do khanjari alif `ٱلصَّٰلِحَٰتِ`, shadda).**
- **Awaaz:** `USTAAD` = Algieba (sab kuch). **Audio:** koi tilawat nahi, is baare me video me kuch nahi kehte. UCHARAN = Devanagari me Arabic shabd, screen par Arabic ke neeche. Music continuous (RULES 1c, ~19 LU neeche), har Arabic block par halka swoosh. Tracks: Soaring (intro+parichay) -> River Flute. Ambience: halki hawa / lahrein (CC0).
- **Tarjuma = SARAL BHAAVARTH (RULES 1a):** teen tarjumon ke saanjhe matlab par apne shabdon me. Label (screen): **"सरल भावार्थ — माने हुए तर्जुमों के आधार पर"**.
- **Visuals:** sirf jagah, aasmaan, roshni, raaste, diya, darwaza. **Koi Nabi, Sahabi, farishta, insaan nahi — na aakaar, na parchhai, na haath.** Koi ghadi/hourglass nahi, koi likha harf image me nahi.
- **Images (RULES 1d):** poori reuse (`image_library.md` + earlier stories), 0 nayi, Rs0; thumbnail wallpaper nayi (free Cloudflare pehle).
- **Nigraan LAGU KARO (006 ki tarah):** (1) hook ke baad ~0:25-0:28 par pehla poora Arabic; parichay sirf EK line, "103vi / 3 ayat" sirf screen card par; (2) title me search shabd pehle; thumbnail <= 3-4 bade shabd; pehla frame bina awaaz samajh aaye; (3) pehle 60 s me ek image/crop max ~8-10 s.
- **Niyam:** koi fiqh hukm (qasam ke ahkaam), koi firqa, koi "chhoda gaya" baat nahi. "guarantee/100%/rizq/sawab" jaise shabd nahi.
- **Spoken honorific:** "नबी सल्लल्लाहु अलैहि वसल्लम" poora; koi Sahabi naam nahi.

---

## INTRO (`part: intro`, hook)
[SCREEN: dhalti shaam ka khaali samundar-kinara, door chamakta kshitij; ऊपर Arabic title سُورَةُ ٱلْعَصْرِ (font se) aur neeche chhota caption "वक़्त की क़सम". Pehla frame bina awaaz ke samajh aaye: dhalti roshni, khaali kshitij.]
1. [MUSIC soft: Soaring — intro + parichay]
2. [AMBIENCE: halki hawa, door lahron ki dheemi awaaz (Freesound CC0)]
3. USTAAD: "तीन आयतें — वक़्त की क़सम, इंसान का घाटा, और घाटे से बचने का रास्ता। ये है सूरह अल-अस्र।" [P5]
## 1. SURAH KA PARICHAY
[SCREEN: chhota card: "सूरह अल-अस्र · क़ुरआन की 103वीं सूरह · 3 आयतें"; peeche sunehri ghaati]
4. USTAAD: ""अस्र" का मतलब है ज़माना, वक़्त। पहली आयत के इसी शब्द से सूरह का नाम है।" [P1][M1]
### [AYAH 1]
[SCREEN: badlon se utarti sunehri kirnein; poori surah Arabic me (3 ayat) — swoosh ke saath aati hai]
5. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَٱلْعَصْرِ إِنَّ ٱلْإِنسَٰنَ لَفِى خُسْرٍ إِلَّا ٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّٰلِحَٰتِ وَتَوَاصَوْا۟ بِٱلْحَقِّ وَتَوَاصَوْا۟ بِٱلصَّبْرِ
6. USTAAD: "ये रही पूरी सूरह। इसमें घाटे से बचने की चार बातें आती हैं।" [P5][M4]
7. [MUSIC continue: River Flute — matlab]
## 2. SHAN-E-NUZUL
[SCREEN: Makka-jaisi ghaati ki raat, kaale pahaad, khaali raasta; koi insaan nahi, koi gumbad/minar nahi]
8. USTAAD: "इस सूरह के उतरने का कोई ख़ास वाक़िया माने हुए तफ़्सीरों में नहीं मिलता।" [N1]
9. USTAAD: "ज़्यादातर उलमा के मुताबिक़ ये मक्की सूरह है। क़तादा वग़ैरह कुछ ने इसे मदनी भी कहा है।" [P2]
## 3. AAYAT-DAR-AAYAT
[SCREEN (har Arabic block): Arabic bade Amiri font me (Tanzil Uthmani, bytes unchanged), uske neeche UCHARAN (Devanagari), upar chhota label "सरल भावार्थ — माने हुए तर्जुमों के आधार पर" (sirf BHAAVARTH line par), neeche Hindi caption. Har jumla alag Arabic block. Koi insaan/farishta ka roop nahi.]
### [AYAH 2]  (= 103:1)
[SCREEN: dhalti shaam ki roshni me khajoor ke beech ka raasta; koi insaan nahi]
10. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَٱلْعَصْرِ
11. USTAAD — UCHARAN: "वल अस्र"
12. USTAAD — BHAAVARTH: "पहली आयत: वक़्त की क़सम, ज़माने की क़सम।" [T2]
13. [MUSIC continue: River Flute — matlab]
14. USTAAD — MATLAB: "अल्लाह ने उस वक़्त की क़सम खाई जिसमें इंसान जीता है और अपने अच्छे-बुरे काम करता है।" [M1]
15. USTAAD — MATLAB: "तबरी के मुताबिक़ यहाँ "अस्र" का मतलब पूरा ज़माना है — शाम, दिन और रात, सब।" [M1]
16. USTAAD — MATLAB: "कुछ उलमा ने इसका मतलब दिन का आख़िरी हिस्सा या अस्र की नमाज़ भी लिया है।" [K2]
### [AYAH 3]  (= 103:2)
[SCREEN: shaam dhale ka bada khaali maidan, door ek chhota-sa nishaan; koi insaan nahi]
17. [SWOOSH — ARABIC ON SCREEN]
ARABIC: إِنَّ ٱلْإِنسَٰنَ لَفِى خُسْرٍ
18. USTAAD — UCHARAN: "इन्नल इन्साना लफ़ी ख़ुस्र"
19. USTAAD — BHAAVARTH: "दूसरी आयत: हर इंसान घाटे में पड़ा हुआ है।" [T2]
20. [MUSIC continue: River Flute — matlab]
21. USTAAD — MATLAB: "तबरी के मुताबिक़ यहाँ "इंसान" किसी एक आदमी के लिए नहीं, पूरी इंसानियत के लिए है।" [M2]
22. USTAAD — MATLAB: ""ख़ुस्र" यानी नुक़सान, घाटा, बर्बादी। इब्ने कसीर भी इसका यही मतलब बताते हैं।" [M2]
### [AYAH 4]  (= 103:3 — pehla hissa)
[SCREEN: andhere kamre me ek akeli diya ki lau; koi insaan nahi]
23. [SWOOSH — ARABIC ON SCREEN]
ARABIC: إِلَّا ٱلَّذِينَ ءَامَنُوا۟
24. USTAAD — UCHARAN: "इल्लल लज़ीना आमनू"
25. USTAAD — BHAAVARTH: "तीसरी आयत, पहला हिस्सा: मगर वो लोग, जो ईमान लाए।" [T2]
26. [MUSIC continue: River Flute — matlab]
27. USTAAD — MATLAB: ""मगर" यहाँ अपवाद है — घाटे से बचने वाले लोग। पहली बात ईमान है।" [M3]
28. USTAAD — MATLAB: "तबरी में मुजाहिद के हवाले से इसका मतलब तौहीद को मानना आया है, और इब्ने कसीर के मुताबिक़ ईमान दिल से।" [M3]
### [AYAH 5]  (= 103:3 — doosra hissa)
[SCREEN: subah ki roshni me purane gharon ki khali gali; koi insaan nahi]
29. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَعَمِلُوا۟ ٱلصَّٰلِحَٰتِ
30. USTAAD — UCHARAN: "व अमिलुस सालिहात"
31. USTAAD — BHAAVARTH: "और जिन्होंने अच्छे काम किए।" [T2]
32. [MUSIC continue: River Flute — matlab]
33. USTAAD — MATLAB: "यानी ईमान के साथ नेक अमल — अच्छे काम करना।" [K5]
34. USTAAD — MATLAB: "तबरी के मुताबिक़ इनमें फ़र्ज़ पूरे करना और गुनाह से बचना भी आता है।" [K5]
### [AYAH 6]  (= 103:3 — teesra hissa)
[SCREEN: registaan me alag-alag disha se aate raaste jo ek jagah milte hain; koi insaan nahi]
35. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَتَوَاصَوْا۟ بِٱلْحَقِّ
36. USTAAD — UCHARAN: "व तवासौ बिल हक़्क़"
37. USTAAD — BHAAVARTH: "और एक-दूसरे को हक़ की बात याद दिलाते रहे।" [T2]
38. [MUSIC continue: River Flute — matlab]
39. USTAAD — MATLAB: ""हक़" यानी वो सच, जो अल्लाह की किताब और दीन से साबित है। तबरी में क़तादा और हसन के हवाले से यही आता है।" [K6]
40. USTAAD — MATLAB: "इब्ने कसीर के मुताबिक़ इसमें भलाई की बात कहना और बुराई से रोकना भी शामिल है।" [K6]
### [AYAH 7]  (= 103:3 — chautha hissa)
[SCREEN: bandh darwaze ke kinaron se aati garm roshni; koi insaan nahi]
41. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَتَوَاصَوْا۟ بِٱلصَّبْرِ
42. USTAAD — UCHARAN: "व तवासौ बिस सब्र"
43. USTAAD — BHAAVARTH: "और एक-दूसरे को सब्र की बात याद दिलाते रहे।" [T2]
44. [MUSIC continue: River Flute — matlab]
45. USTAAD — MATLAB: ""सब्र" यानी अल्लाह की इताअत पर जमे रहना। तबरी में क़तादा और हसन से यही आता है।" [K7]
46. USTAAD — MATLAB: "इब्ने कसीर और माआरिफ़ुल क़ुरआन के मुताबिक़ पहली दो बातें अपने सुधार की हैं, और आख़िरी दो दूसरों के साथ मिलकर निभाने की।" [M4]
## 4. SEEKH
[SCREEN: subah ka sunehra ujala, khula raasta; seekh ke teen chhote cards font se]
47. USTAAD: "पहली सीख: वक़्त की क़ीमत पहचानिए। ये वही वक़्त है जिसमें हम जीते हैं और अपने काम करते हैं।" [M1]
48. USTAAD: "दूसरी: घाटे से बचने के लिए ईमान और अच्छे काम, दोनों चाहिए।" [M3][K5]
49. USTAAD: "तीसरी: अकेले नहीं — एक-दूसरे को हक़ और सब्र की बात याद दिलाते रहिए।" [M4][K6][K7]
[SCREEN (end, aakhri ~15 s end-screen area khaali): tagline card "क़ुरआन, आसान ज़बान में।" + chhota card "Arabic text: Tanzil Project, tanzil.net" + "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"]
50. USTAAD: "अगली बार, नूर-ए-राह में: सूरह अल-फ़ील।" [NEXT]
51. [MUSIC: River Flute dheere fade-out; aakhri ~3 s sirf gentle breeze]

## SOURCES (description ke liye)
- Arabic Quran text: Tanzil Project (https://tanzil.net) — Tanzil Quran Text, Copyright (C) 2007-2021 Tanzil Project, License: Creative Commons Attribution 3.0. Text unchanged; check https://tanzil.net/updates/ for changes.
- सरल भावार्थ: माने हुए तर्जुमों (Suhel Farooq Khan / Tanzil hi.hindi; Muhammad Farooq Khan; Shaikh-ul-Hind Mahmud Hasan) के आधार पर — शब्दशः तर्जुमा नहीं।
- Tafseer: al-Tabari, Jami' al-Bayan (103); Tafsir Ibn Kathir (103); al-Qurtubi, al-Jami' li-Ahkam al-Qur'an (103); Ma'ariful Qur'an (Mufti Muhammad Shafi); Alim / quran.com surah info (parichay).
- उच्चारण (Arabic की हिंदी लिपि): टंज़ील ट्रांसलिटरेशन से मिलाकर — पढ़ने की मदद।
- Surah data: Tanzil Quran Metadata (CC BY 3.0, https://tanzil.net).
- Music: "Soaring" Kevin MacLeod (incompetech.com) · "River Flute" Kevin MacLeod (incompetech.com) — both CC BY 4.0, http://creativecommons.org/licenses/by/4.0/
- Ambience: freesound.org (CC0)
(Tabarani-riwayat wali line hata di gayi - number/darja PC par confirm nahi hua; description me uska zikr nahi.)

## SOURCE MAP — har tag dossier me kahan (Munshi ke liye)
| Tag | Dossier | Grade | Lines |
|---|---|---|---|
| P1 | P1 (naam pehle ayat ke "wal-'asr" shabd se; 103vi/3 ayat sirf screen card) | maana hua | 4 |
| P2 | P2 (zyadatar makki; Qatada wagairah madani) | ikhtilaaf | 9 |
| P5 | P5 (qasam -> ghata -> 4 guN) | maana hua | 3, 6 |
| N1 | N1 (chaaron tafseer me koi sabab-e-nuzul nahi) | maana hua (negative) | 8 |
| T2 | dossier 1.2 (saral bhaavarth) | decision 001 | 12, 19, 25, 31, 37, 43 |
| UCHARAN | research/ucharan.md [U1-U6] + sources.json T3 | decision 2026-10-30 | 11, 18, 24, 30, 36, 42 |
| M1/K1 | M1 (asr = zamana; Tabari) | maana hua | 14, 15, 47 |
| K2 | K2 (asr ki namaz / din ka aakhri hissa; sirf ikhtilaaf ki line, bina tarjeeh) | ikhtilaaf | 16 |
| M2/K3 | M2 (insaan = poori insaaniyat; khusr = nuksaan; Tabari, IK) | maana hua | 21, 22 |
| M3/K4 | M3 (istithna; iman: Mujahid/Tabari, IK dil se) | maana hua | 27, 28, 48 |
| K5 | K5 (nek amal; Tabari: farz + gunaah se bachna) | maana hua | 33, 34, 48 |
| K6 | K6 (haq; Qatada/Hasan via Tabari; IK) | maana hua | 39, 40, 49 |
| K7 | K7 (sabr = ita'at par jame rehna; Qatada/Hasan via Tabari) | maana hua | 45, 49 |
| M4/K8 | M4 (tarteeb; pehle do khud ke liye, aakhri do doosron ke liye; IK, Ma'ariful) | maana hua | 6, 46, 49 |
| NEXT | series_queue order 7: al-fil | queue | 50 |
Koi hadith section / fazilat nahi (Z1). C1-C6 SHAMIL NAHI (Musaylima, Ali ki qira'at, asr ke saare maane, qasam ke fiqh ahkaam, "subah jaan bechta hai" hadith, Ibn Taymiyya). Ma'ariful ki "poonji" tashbeeh bhi nahi (ek source). Shan-e-nuzul ke bayan sirf lines 8 (N1), 9 (P2), 10 (N3). Koi sawaal / SAWAAL line / disclaimer script me nahi (RULES 1d).

## IMAGES (long/images.json; **0 NAYI image, sab reuse + crop, Rs0**; thumbnail wallpaper alag nayi, free engine pehle)
- A `003/07_sea_horizon_dusk`  - B `005/23_golden_valley_full_light`  - C `002/11_sunrays_clouds`  - D `003/03_makka_valley_night`  - E `003/05_paths_to_oasis`  - F `002/04_date_palm_path`  - G `002/10_ring_in_desert`  - H `003/02_lamp_single_flame`  - I `002/03_madina_dawn_houses`  - J `002/09_lit_door`  - K `003/04_dawn_sand_ridge`  - L `003/08_empty_room_morning`  - M `002/05_dawn_horizon`
| Lines | Image | Shot | Lagbhag samay |
|---|---|---|---|
| 3 | A poori | dhalti shaam ka khaali kshitij (hook) | 0-8 s |
| 4 | B poori | parichay card ke peeche | 8-15 s |
| 5-5 (AYAH 1) | C poori; line 6: C crop (kiran ka kendra) | poori surah Arabic | 15-20, 20-28 s |
| 8 | D poori | Makka-jaisi ghaati raat | 28-37 s |
| 9 | D crop (raasta) | | 37-44 s |
| 10-15 (102:1) | F poori; line 16: F crop | waqt | |
| 17-22 (102:2) | G poori; line 23: G crop | ghata / khaali maidan | |
| 23-28 (iman) | H poori | diya | |
| 29-34 (nek amal) | I poori | subah ke ghar | |
| 35-40 (haq ki talqeen) | E crop (alag rect, milte raaste) | | |
| 41-46 (sabr) | J poori | band darwaza, roshni | |
| 47 | K poori | seekh 1 | |
| 48 | L poori | seekh 2 | |
| 49 | M poori | seekh 3 | |
| 50-51 | B crop (rect fx 0.7, fy 0.5, zc 1.4) | ant | |
Pehle ~60 s: A (0-8) · B (8-15) · C (15-20) · C crop (20-28) · D (28-37) · D crop (37-44) · (line 10 hata di: D crop ayah 2 tak chalta hai). Same (image, rect) dobara nahi.
Kul: ~20 clips, 13 base images, 0 nayi. Ghadi/hourglass nahi; koi insaan nahi.

## LENGTH ESTIMATE (measured TTS rates 003-006: USTAAD ~0.48 s/shabd at tempo 1.08 -> ~0.45 s/shabd at 1.11; UCHARAN ~0.78 -> ~0.73; gaps: wahi speaker +0.35 s, section +0.8 s, har Arabic block ~3.4 s)
| Hissa | Shabd | Anuman |
|---|---|---|
| USTAAD (UCHARAN chhod kar, tags bina) | 434 | ~195 s |
| UCHARAN (6 lines) | 20 | ~15 s |
| Gaps (~40 x 0.35) + 4 sections + 7 Arabic blocks x ~3.4 s + ant ~3.5 s | | ~44 s |
| **Kul** | | **~254 s ≈ 4:14** (band +-0:25; target 3:30-4:30) |
**Pehla poora Arabic (line 5) ~0:25.** Agar asli TTS 4:45 paar kare to pehle trim: line 16, line 35, line 41.

## THUMBNAIL (thumbnail.json, v3 ka dhaancha)
Arabic سُورَةُ ٱلْعَصْرِ (surah_titles.json al-asr) · Hindi सूरह अल-अस्र · chip: "तीन आयतें" · hook text: "*वक़्त* की क़सम —\nघाटे में इंसान" (<= 4 bade shabd; koi sawaal nahi; title ke shabd nahi dohrata; koi chehra/aakaar/ghadi nahi). Scene: dhalti shaam ki sunehri roshni, khaali registani raasta, left 45% shaant dark-blue. Wallpaper NAYI, free engine (Cloudflare flux) pehle; paid sirf fallback aur balance > Rs50 floor par.

## TITLE options (search-phrase pehle; suffix "| Noor-e-Raah")
1. **Surah Asr ka Matlab Hindi Mein | 3 Ayat, Ghate se Bachne ki 4 Baatein aur Har Ayat ka Matlab | Noor-e-Raah** (recommended; queue search_title se match)
2. Surah Al-Asr Hindi Mein | Har Ayat ka Saral Matlab | Noor-e-Raah
3. Surah Asr ka Matlab | Waqt ki Qasam aur Insaan ka Ghata | Noor-e-Raah

## CONTINUITY / CHECKS
- Koi Sahabi/Nabi aakaar nahi; Tabarani-riwayat wali line DROP (2026-11-13: number/darja confirm nahi hua). Koi hadith-fazilat nahi. C1-C6 nahi.
- 006 se alag: 3 ayat par 4-jumle wali lambi akhiri ayat (7 Arabic blocks), hook = waqt ki qasam + ghata, "koi sabab-e-nuzul nahi" ek line me, mood subah->shaam (dhalti roshni).
- Line numbers 1..51 file ke kram me; UCHARAN (11, 18, 24, 30, 36, 42) apne BHAAVARTH (12, 19, 25, 31, 37, 43) se pehle; aakhri bolti line 50; aakhri cue 51; render.json end_from = 50.
- PC check needed (Sanchalak/user): sha256 + Amiri zoom (upar); Tabarani riwayat: DROPPED; Makki/Madani Tanzil metadata.
