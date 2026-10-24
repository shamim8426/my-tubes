# 001 — सूरह अल-फ़ातिहा | नूर-ए-राह — script (SURAH MODE, do awaazein)

## HEADER
- **Channel / format:** noor-e-raah, surah explainer (channel `RULES.md` 1, 1a, 1b, 1c). Pilot story 001. Kharcha ₹0 (sirf script).
- **Version:** do awaaz ki baat-cheet (user faisla 2026-10-24, RULES 1b). Pichhla ek-narrator version (Munshi R2 PASS)
  ka saara deeni maadda wahi hai; sirf bolne wale, kram aur lambai badli.
- **Content source:** sirf `research/dossier.md` + `sources.json` (Khoji MODE 3, 2026-10-24). Har parichay / shan-e-nuzul
  line ke ant me [S#], har matlab line ke ant me [M#], aaj ki misaal [MISAAL] (koi naya deeni daava nahi).
  Production me tags spoken text aur captions se hata diye jaayenge.
- **Awaazein (channel.json "voices"):**
  - `USTAAD` = Gemini **Algieba** — aayat ka elaan (Arabic sirf screen par, kabhi padha nahi jaata), BHAAVARTH, MATLAB,
    parichay, shan-e-nuzul. **Deeni baat sirf Ustaad kehta hai**, hamesha [S#]/[M#] ke saath.
  - `SAWAAL` = Gemini **Sulafat** — aam insaan ke sawaal, dono [MISAAL] kisse, chhota saar / apni baat. Narm aur izzat
    bhari; **khud koi hukm, fazeelat, hadith ya tafseer ki baat nahi kehti** — zaroorat ho to poochhti hai, Ustaad
    jawab deta hai. (Har SAWAAL line ki jaanch: `long/review/script_sheet.md` (c).)
  - Lines chhoti (zyadatar ≤ 25 shabd; SAWAAL ki har line ≤ 25) — TTS completeness har line Whisper se (RULES 1b).
- **Audio (user update 2026-10-24, music rule badla):** KOI tilawat nahi (na insaani, na AI) — koi bhi awaaz Arabic
  aayat **nahi padhti**, na transliteration me; Arabic sirf screen par (font). Koi vocal / nasheed / hum / beat nahi.
  **Music:** bahut halka instrumental (ambient pad / halki ney-bansuri / narm piano / oud ke halke sur), bina beat,
  awaaz ke neeche. **Ambience:** scene ke mood se halki qudrati awaaz (hawa, parinde, baarish, paani, jhingur,
  registaan ki hawa). **Jab Arabic aayat screen par ho:** music 1 s me fade-out, sirf halki ambience; aayat ke baad
  music dheere lautta hai. Cue lines numbered hain: `[MUSIC soft: <mood>]`, `[AMBIENCE: <sound>]`,
  `[MUSIC fade-out 1s — ARABIC ON SCREEN]`, `[MUSIC back slowly]`. Har aayat block: fade-out cue (1 s) →
  **Arabic ka pehla frame tabhi aaye jab music ka fade poora ho kar chup ho jaye** → Arabic akeli ~2 s (sirf ambience)
  → USTAAD ka BHAAVARTH (Arabic upar bani rehti hai) → Arabic chhoti hokar hat-ti hai → **`[MUSIC back slowly]` tabhi
  shuru ho jab Arabic (chhoti hone wali animation samet) poori tarah screen se hat chuki ho.** Niyam: channel `RULES.md` 1c + channel.json "music" (awaaz se 20–24 LU neeche,
  ducking; tracks sirf `shared/music/noor/`, har track `shared/assets_license.csv` me). On-screen aayat ke neeche
  music = BLOCKER.
- **Tarjuma = SARAL BHAAVARTH (tay, RULES 1a).** Har BHAAVARTH apne shabdon me, teen maane hue tarjumon (QuranEnc
  al-Umari, Tanzil hi.farooq, Tanzil hi.hindi) ke saanjhe matlab par; kisi se 5+ shabd ka hu-ba-hu tukda nahi; [M#] se
  bahar koi matlab nahi. Saaton BHAAVARTH lines R2 PASS wali hi hain, shabd-ba-shabd.
  Screen label har bhaavarth par: **"सरल भावार्थ — माने हुए तर्जुमों के आधार पर"**.
  Review niyam: har BHAAVARTH teeno tarjumon ke saath milaya jaata hai — matlab alag = BLOCKER; ibaarat copy = MAJOR.
- **Arabic:** Tanzil Quran Text, Uthmani (Hafs, Kufi ginti; Bismillah = aayat 1). ARABIC lines official tanzil.net
  download (quran-uthmani) se **byte-by-byte** (pichhle R2 version se program se copy, koi NFC/normalization nahi).
- **Visuals:** sirf jagah aur mahaul (dossier section 4). **Kabhi koi Nabi, Sahabi, farishta — na tasveer, na parchhai,
  na silhouette, na peeth, na roshni ka aakaar.** Koi bheed, koi riwayat ka abhinay nahi. Dono bolne wale bhi screen par
  **nahi** dikhte (sirf awaaz). Koi AI-likha harf nahi; Arabic aur Hindi text hum font se lagayenge. Hadith-e-qudsi
  ke jawab sirf likhe caption ki tarah, koi drishya nahi.
- **Niyam:** koi fiqh ruling nahi, koi maslak/firqa ka naam ya behes nahi, 1:7 me kisi qaum ka naam nahi (C7),
  "chhoda gaya" (C1–C10) ki koi baat nahi, nuzool kram "5" pakka nahi (S13).
- **Spoken honorific:** "नबी सल्लल्लाहु अलैहि वसल्लम" poora bola jaata hai; caption me ﷺ.

---

## INTRO (`part: intro`, hook)
[SCREEN: subah ki pehli roshni me do pahadiyon ke beech khulti ghaati; beech me khaali, bina likhai ka sunehri
hashiye wala kaagaz-sa panna (koi akshar nahi). Caption: "सूरह अल-फ़ातिहा"]

1. [MUSIC soft: shaant subah — halka ambient pad, door se ney-bansuri ke do-teen lambe sur]
2. [AMBIENCE: subah ki halki hawa, door chidiyon ki chahchahat]
3. SAWAAL: "उस्ताद जी, जो सूरह हम बचपन से सुनते आए हैं — क्या हम उसका मतलब जानते हैं?"
4. USTAAD: "आज उसी को समझेंगे — सूरह अल-फ़ातिहा, जिसे नबी सल्लल्लाहु अलैहि वसल्लम ने क़ुरआन की सबसे अज़ीम सूरह बताया।" [S17]

## 1. SURAH KA PARICHAY
[SCREEN: wahi ghaati, roshni badhti hui; info cards font se: "मक्की (ज़्यादातर उलमा)", "आयतें: 7", "क़ुरआन में क्रम: 1"]

5. SAWAAL: "पहले नाम। 'फ़ातिहा' का मतलब क्या है?"
6. USTAAD: "'फ़ातिहा' यानी खोलने वाली। क़ुरआन इसी सूरह से खुलता है।" [S1]
7. USTAAD: "ये क़ुरआन की पहली सूरह है, और इसकी आयतें सात हैं — इस पर उलमा एक राय हैं।" [S12][S10]
8. USTAAD: "हम जो गिनती ले रहे हैं, उसमें बिस्मिल्लाह पहली आयत है।" [S11]

[SCREEN: naamon ke cards, ek-ek kar (font se, Arabic naam + Hindi matlab)]

9. SAWAAL: "और इसके नाम? मैंने एक से ज़्यादा सुने हैं।"
10. USTAAD: "हाँ, कई नाम हैं। 'उम्मुल-क़ुरआन' — यानी क़ुरआन की असल, उसकी जड़।" [S2]
11. USTAAD: "'अस-सब्उल-मसानी' — यानी बार-बार दोहराई जाने वाली सात आयतें।" [S3]
12. USTAAD: "और 'अस-सलात', 'अल-हम्द', 'अर-रुक़्या' और 'अश-शिफ़ा' — यानी नमाज़, तारीफ़, दम की दुआ और शिफ़ा।" [S4][S5][S6][S7]
13. SAWAAL: "इतने नाम! तो एक बात में — इस सूरह में है क्या?"
14. USTAAD: "पहले अल्लाह की तारीफ़, फिर सिर्फ़ उसी की इबादत और उसी से मदद, और आख़िर में सीधी राह की दुआ।" [S20]

## 2. SHAN-E-NUZUL
[SCREEN: saatvi sadi ka Makka — sookhi kaali-bhoori chattani pahadiyan, tang wadi, retili zameen, kuchh khajoor ke
ped; mitti/patthar ke chaukor, chapti chhat wale ghar, lakdi ke darwaze; raat me mitti ka chhota diya, taaron bhara
aasmaan; subah se pehle neela ujala. Koi insaan nahi, koi gumbad/minar/bijli/pakki sadak nahi, Ka'ba nahi.]

15. [MUSIC soft: purani ghaati, raat — gehra halka pad, oud ke ikke-dukke narm sur]
16. [AMBIENCE: registaan ki dheemi hawa, raat ke halke jhingur]
17. SAWAAL: "ये सूरह कब उतरी? कोई ख़ास वाक़िया?"
18. USTAAD: "पहले एक साफ़ बात: इसके उतरने के किसी ख़ास वाक़िये की कोई मज़बूत रिवायत नहीं मिलती।" [S15]
19. USTAAD: "ज़्यादातर उलमा के मुताबिक़ ये मक्की सूरह है — मक्का में, पैग़म्बरी के बिल्कुल शुरुआती दौर में उतरी।" [S15][S9]
20. SAWAAL: "और कोई दूसरी राय भी है?"
21. USTAAD: "कुछ उलमा ने इसे मदीना में उतरी सूरह माना।" [S9]
22. USTAAD: "और कुछ ने कहा कि ये दो बार उतरी — एक बार मक्का में, एक बार मदीना में।" [S9]
23. USTAAD: "इमाम इब्न कसीर के नज़दीक पहली राय — यानी इसका मक्की होना — ज़्यादा मुनासिब है।" [S9]

## 3. AAYAT-DAR-AAYAT
[SCREEN (har aayat): beech me Arabic aayat bade Arabic font me (Tanzil Uthmani), neeche Hindi BHAAVARTH caption,
caption ke upar chhota label: "सरल भावार्थ — माने हुए तर्जुमों के आधार पर". TIMING: Arabic ka pehla frame tabhi
aaye jab music ka 1 s fade poora ho kar chup ho jaye; Arabic BHAAVARTH line ke ant tak screen par, phir chhoti hokar
hat-ti hai; `[MUSIC back slowly]` tabhi shuru ho jab Arabic (chhoti hone wali animation samet) poori tarah screen se hat
chuki ho. Hadith-e-qudsi ka jawab alag rang ke chhote caption me, koi
drishya nahi.]
[SCREEN (shuru): andhere me ek akela mitti ka diya — shaant.]

24. [MUSIC soft: shaant, thehra hua — narm piano ke dheeme sur, halka pad]
25. [AMBIENCE: raat ka sannata, diye ki halki chatak]
26. SAWAAL: "अब आयतें। पढ़ते वक़्त किस बात पर ध्यान दें?"
27. USTAAD: "एक हदीस-ए-क़ुदसी में अल्लाह फ़रमाता है: 'मैंने नमाज़ को अपने और अपने बंदे के बीच आधा-आधा बाँट दिया है।'" [S16][S4]
28. USTAAD: "'और मेरे बंदे को वो मिलेगा जो उसने माँगा।' फिर हदीस बताती है कि फ़ातिहा के हिस्सों पर अल्लाह की तरफ़ से जवाब आता है।" [S16]
29. SAWAAL: "ये तो दिल को छूने वाली बात है।"

### [AYAH 1]
[SCREEN: baarish ke baad hari hoti zameen, subah ki dhoop]
30. [MUSIC fade-out 1s — ARABIC ON SCREEN]
31. [AMBIENCE: baarish ke baad pattiyon se tapakta paani, halki hawa]
ARABIC: بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ
32. USTAAD — BHAAVARTH: "पहली आयत: अल्लाह के नाम से शुरू — वो, जो बेहद मेहरबान है, और बहुत रहम करने वाला है।"
33. [MUSIC back slowly]
34. USTAAD — MATLAB: "यानी हर काम की शुरुआत अल्लाह के नाम से — उसकी मदद और बरकत के साथ।" [M1]
35. USTAAD — MATLAB: "'रहमान' और 'रहीम' — दोनों उसकी बहुत बड़ी और पूरी रहमत के नाम हैं।" [M1]

### [AYAH 2]
[SCREEN: alag-alag jahan — samandar, pahad, raat ki aakaash-ganga, door udta parindon ka jhund, khet]
36. [MUSIC fade-out 1s — ARABIC ON SCREEN]
37. [AMBIENCE: samandar ki dheemi lehar, door parindon ki awaaz]
ARABIC: ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ
38. USTAAD — BHAAVARTH: "दूसरी आयत: हर तारीफ़ असल में अल्लाह की है — वो सारे जहानों का पालने वाला मालिक है।"
39. [MUSIC back slowly]
40. SAWAAL: "'हम्द' — क्या ये बस शुक्रिया कहना है?"
41. USTAAD — MATLAB: "'हम्द' सिर्फ़ शुक्रिया नहीं — किसी की ख़ूबियों की तारीफ़ भी हम्द है।" [M2]
42. USTAAD — MATLAB: "'रब' वो मालिक है जो पालता है, सँभालता है। और 'आलमीन' यानी अल्लाह के सिवा सारी मख़लूक़ — हर जहान।" [M2]
43. SAWAAL — MISAAL: "कोई हमारा गिरा सामान उठा दे, तो हम झट से 'शुक्रिया' कहते हैं।" [MISAAL]
44. SAWAAL — MISAAL: "पर बारिश, साँस, सुबह का सूरज — ये तो बिना माँगे मिले। इन्हें देने वाले की ख़ूबियों को सराहना... क्या यही हम्द है?" [MISAAL]
45. USTAAD: "हाँ, यही। और इस आयत पर हदीस में अल्लाह का जवाब है: 'मेरे बंदे ने मेरी हम्द की।'" [M2][S16]

### [AYAH 3]
[SCREEN: pahadi chashma, saaf behta paani, subah ki dhoop]
46. [MUSIC fade-out 1s — ARABIC ON SCREEN]
47. [AMBIENCE: chashme ka behta paani]
ARABIC: ٱلرَّحْمَٰنِ ٱلرَّحِيمِ
48. USTAAD — BHAAVARTH: "तीसरी आयत: वो बेहद मेहरबान है, बहुत रहम करने वाला।"
49. [MUSIC back slowly]
50. USTAAD — MATLAB: "'रब' के ठीक बाद रहमत का ज़िक्र — यानी वो सारे जहान को किसी मजबूरी से नहीं, अपनी रहमत से पालता है।" [M3]
51. USTAAD: "वो रब भी है, और रहमत वाला भी। जवाब: 'मेरे बंदे ने मेरी तारीफ़ की।'" [M3][S16]

### [AYAH 4]
[SCREEN: khaali, shaant, vishaal maidan; dhalta sooraj, sunsaan ufaq — gambhir, darawna nahi]
52. [MUSIC fade-out 1s — ARABIC ON SCREEN]
53. [AMBIENCE: khule maidan ki dheemi hawa]
ARABIC: مَٰلِكِ يَوْمِ ٱلدِّينِ
54. USTAAD — BHAAVARTH: "चौथी आयत: जिस दिन हर किसी को बदला मिलेगा, उस दिन का मालिक वही है।"
55. [MUSIC back slowly]
56. SAWAAL: "उस्ताद जी, ख़ास 'उस दिन' का मालिक क्यों कहा गया?"
57. USTAAD — MATLAB: "मालिक तो वो हमेशा है; पर हिसाब और बदले के उस दिन कोई और, किसी चीज़ का नाम-भर का मालिक भी नहीं होगा।" [M4]
58. USTAAD — MATLAB: "दुनिया अमल की जगह है, और हर अमल का पूरा बदला उसी दिन मिलेगा।" [M4]
59. USTAAD: "जवाब: 'मेरे बंदे ने मेरी बुज़ुर्गी बयान की' — 'बुज़ुर्गी' यानी बड़ाई।" [S16]

### [AYAH 5]
[SCREEN: andhere me akela diya — ek hi roshni ki taraf]
60. [MUSIC fade-out 1s — ARABIC ON SCREEN]
61. [AMBIENCE: raat ka sannata, halke jhingur]
ARABIC: إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ
62. USTAAD — BHAAVARTH: "पाँचवीं आयत: ऐ अल्लाह, हम सिर्फ़ तेरी इबादत करते हैं, और मदद भी सिर्फ़ तुझसे ही माँगते हैं।"
63. [MUSIC back slowly]
64. USTAAD — MATLAB: "ध्यान दीजिए — यहाँ से बंदा 'वो' नहीं, सीधे 'तू' कह कर अल्लाह से बात करता है।" [M5]
65. USTAAD — MATLAB: "अरबी में 'तुझी को' पहले आया — यानी सिर्फ़ तू। इबादत यानी पूरी मोहब्बत से, ख़ुद को छोटा मान कर झुकना।" [M5]
66. SAWAAL — MISAAL: "पर उस्ताद जी, बुख़ार में हम डॉक्टर के पास जाते हैं, मुश्किल में दोस्त से मदद माँगते हैं।" [MISAAL]
67. SAWAAL: "तो इस आयत का इससे क्या रिश्ता है?"
68. USTAAD: "आयत दिल के भरोसे की बात करती है — इलाज और दोस्त की मदद अपनी जगह, पर आख़िरी भरोसा और उम्मीद सिर्फ़ अल्लाह पर।" [M5][MISAAL]
69. USTAAD: "जवाब: 'ये मेरे और मेरे बंदे के बीच है, और मेरे बंदे को वो मिलेगा जो उसने माँगा।'" [S16]

### [AYAH 6]
[SCREEN: registaan me ek seedha, saaf raasta ufaq tak; koi insaan nahi]
70. [MUSIC fade-out 1s — ARABIC ON SCREEN]
71. [AMBIENCE: registaan ki halki hawa, ret ki sarsarahat]
ARABIC: ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ
72. USTAAD — BHAAVARTH: "छठी आयत: हमें सीधी राह दिखा, और उस पर चला।"
73. [MUSIC back slowly]
74. SAWAAL: "जो पहले से सीधी राह पर है, वो भी रोज़ ये दुआ क्यों माँगे?"
75. USTAAD — MATLAB: "सीधी राह यानी साफ़ रास्ता, जिसमें भटकाव की कोई शाख़ न हो।" [M6]
76. USTAAD — MATLAB: "ईमान वाला भी रोज़ माँगता है कि अल्लाह उसे इसी राह पर जमाए रखे — क्योंकि हर क़दम पर रहनुमाई चाहिए।" [M6]

### [AYAH 7]
[SCREEN: wahi seedha raasta; dono taraf bhatakte, ret me mitte raaste (koi aadmi nahi); door pakka raasta roshni ki taraf]
77. [MUSIC fade-out 1s — ARABIC ON SCREEN]
78. [AMBIENCE: registaan ki hawa, thodi tez phir dheemi]
ARABIC: صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ
79. USTAAD — BHAAVARTH: "सातवीं आयत: उन लोगों की राह, जिन्हें तूने अपनी नेमतों से नवाज़ा; न उनकी राह, जिन पर तेरा ग़ुस्सा हुआ, और न उनकी, जो रास्ते से भटक गए।"
80. [MUSIC back slowly]
81. SAWAAL: "ये नेमत वाले लोग कौन हैं? और किनकी राह से बचने की दुआ है?"
82. USTAAD — MATLAB: "सूरह अन-निसा की आयत उनहत्तर बताती है — नबी, सिद्दीक़ीन यानी सच्चाई में सबसे पक्के लोग, शहीद, और नेक लोग।" [M7]
83. USTAAD — MATLAB: "और बचने की दुआ दो राहों से है: एक उनकी, जिन्होंने हक़ जान कर भी जान-बूझकर छोड़ दिया;" [M7]
84. USTAAD — MATLAB: "और दूसरी उनकी, जो इल्म के बिना या लापरवाही से भटक गए।" [M7]
85. USTAAD: "आख़िरी दुआ पर जवाब: 'ये मेरे बंदे के लिए है, और मेरे बंदे को वो मिलेगा जो उसने माँगा।'" [S16]

## 4. SEEKH
[SCREEN: subah ka sunehra ujala, khulti ghaati (intro wali jagah, ab poori roshni); seekh ke chhote cards font se]

86. [MUSIC soft: ummeed bhari subah — narm piano, halka pad, ney ka ek lamba sur]
87. [AMBIENCE: subah ki chidiyan, halki hawa]
88. SAWAAL: "तो उस्ताद जी, हमारी ज़िंदगी के लिए सीख क्या है?"
89. USTAAD: "पहली: माँगने से पहले तारीफ़ और शुक्र — तफ़सीर इसे माँगने का सबसे बेहतर तरीक़ा बताती है।" [S20][M2]
90. SAWAAL: "पहले शुक्र, फिर माँग — ये मैं आज से याद रखूँगी।"
91. USTAAD: "दूसरी: मेहनत भी, मदद भी — पर दिल का आख़िरी भरोसा अल्लाह पर।" [M5]
92. USTAAD: "तीसरी: सीधी राह की दुआ एक बार नहीं — हर दिन, हर फ़ैसले पर।" [M6]

[SCREEN (end, last ~20 s end-screen area khaali): chhota card "Arabic text: Tanzil Project, tanzil.net" + "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"]

93. USTAAD: "अगली बार, 'शुरू से क़ुरआन' में: सूरह अल-बक़रह की पहली पाँच आयतें।" [NEXT]
94. SAWAAL: "और आप कमेंट में बताइए — फ़ातिहा की कौन-सी आयत आपके दिल के सबसे क़रीब है, और क्यों?"
95. [MUSIC soft: dheere fade-out, aakhri 3 s sirf hawa]

---

## SOURCES (description ke liye)
- Arabic Quran text: Tanzil Project (https://tanzil.net) — Tanzil Quran Text, Copyright (C) 2007-2021 Tanzil Project, License: Creative Commons Attribution 3.0. Text unchanged; check https://tanzil.net/updates/ for changes.
- सरल भावार्थ: माने हुए तर्जुमों (al-Umari / QuranEnc, Farooq Khan, Suhel Farooq Khan) के आधार पर — शब्दशः तर्जुमा नहीं
  (Tarjume: Azizul Haq al-Umari (QuranEnc.com, hindi_omari); Muhammad Farooq Khan & Muhammad Ahmed (Tanzil hi.farooq); Suhel Farooq Khan & Saifur Rahman Nadwi (Tanzil hi.hindi).)
- Tafseer: Tafsir Ibn Kathir; Ma'ariful Qur'an (Mufti Muhammad Shafi); al-Qurtubi, al-Jami' li-Ahkam al-Qur'an; Tafheem-ul-Qur'an (introduction, Al-Fatiha); al-Wahidi, Asbab al-Nuzul.
- Hadith: Sahih al-Bukhari 4474, 4704, 5007; Sahih Muslim 395.
- Surah data: Tanzil Quran Metadata (CC BY 3.0, https://tanzil.net); quran.com.
- Music (sirf jo track asal me lage, unki line; text `shared/assets_license.csv` se hu-ba-hu):
  - "Earth Prelude" Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 License — http://creativecommons.org/licenses/by/4.0/
  - "Water Prelude" Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 License — http://creativecommons.org/licenses/by/4.0/
  - "Meditation Impromptu 02" Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 License — http://creativecommons.org/licenses/by/4.0/
- Ambience SFX: audio stage se pehle har file `shared/assets_license.csv` me (source + licence), zaroorat ho to credit yahan.

(Description ke liye extra line, optional: "Shan-e-nuzul: is surah ke utarne ke kisi khaas waqiye ki mazboot riwayat nahi milti; zyadatar ulama ke mutabiq Makki.")

## MISAAL — kaunsi rakhi, kaunsi hataayi (RULES 1b: max 2)
- **Rakhi:** (1) 1:2 "shukriya vs hamd" (lines 43–45) — sabse seedha rozmarra ka farq; SAWAAL sawaal ki shakl me
  poochhti hai, Ustaad [M2] se haan kehta hai. (2) 1:5 "doctor / dost se madad" (lines 66–68) — aam aadmi ka asli
  sawaal; seekh 2 (line 91) isi par tiki.
- **Hataayi:** 1:4 "imtihaan ka nateeja" (dossier khud chetaavni deta hai: dar na phaile; "hisaab ka din" ki tulna
  halki pad sakti hai) aur 1:6 "anjaan shehar me raasta" (line 76 "har qadam par rehnumai" wahi baat keh deti hai).
- **Lambai ke liye R2 version se hataaya (sab sirf chhota kiya, koi naya daava nahi):** parichay — S3 ka "अल-क़ुरआनुल-अज़ीम"
  aur Hijr 15:87 ka hawala, S8 (Qurtubi ke 12 naam), S12 ka "ek ruku", S11 ki doosri ginti ki tafseel (dossier ki
  ijaazat wali ek line rakhi: line 8), Tafheem ki "dua aur jawab" line (S20); shan-e-nuzul — S9 ki daleel (Hijr /
  namaz), S14 (pehli poori surah?), S13 (nuzool kram 5); 1:1 me "Rahman sirf Allah ke liye khaas" (M1 ka hissa).
  RULES 1 parichay "order of revelation" sirf "agar maani hui list de" — optional; user chahe to S13 wapas (line
  ~23 ke baad, ~10 s).

## LENGTH ESTIMATE (measured audition speeds: Algieba ~1.98 shabd/s, Sulafat ~2.00 shabd/s)
Ginti: sirf bolne wale shabd (tags, cue, screen notes nahi; "—" shabd nahi). Speaker badalne par +0.6 s. Har aayat par
Arabic akeli ~2 s (sirf ambience) = 7 × 2 = 14 s. Music/ambience cues ka apna samay nahi (awaaz ke neeche).

| Section | Lines | USTAAD shabd | SAWAAL shabd | Speaker badle | Arabic hold | ~sec |
|---|---|---|---|---|---|---|
| Intro | 2 | 18 | 16 | 1 | 0 | 18 |
| 1. Parichay | 10 | 91 | 27 | 6 | 0 | 63 |
| 2. Shan-e-nuzul | 7 | 73 | 13 | 4 | 0 | 46 |
| 3. Aayat-dar-aayat | 39 | 498 | 123 | 16 | 14 | 337 |
| 4. Seekh + agli video + sawaal | 7 | 53 | 37 | 5 | 0 | 48 |
| **Kul** | **65** | **733** (46 lines) | **216** (19 lines) | **32** | **14** | **~511 s ≈ 8:31** |

Hisaab: USTAAD 733 ÷ 1.98 = 370.2 s · SAWAAL 216 ÷ 2.00 = 108.0 s · 32 × 0.6 = 19.2 s · Arabic hold 14 s →
**511.4 s ≈ 8:31** (Munshi R1 ke fixes ke baad; sirf Algieba speed par: 949 ÷ 1.98 = 479.3 + 19.2 + 14 = 512.5 s ≈ 8:33).
Isme intro ka music lead, section transitions aur ant ka ~3 s fade nahi gine — asli ~8:40 ke aas-paas ho sakti hai.
~8:00 ke paas laana ho (user faisla): line 29 (SAWAAL "दिल को छूने वाली बात", ~5 s), line 12 (baaki 4 naam, ~8 s),
line 90 (~6 s), line 11 (~5 s). Ikhtilaaf ki lines (19–23) aur BHAAVARTH/MATLAB kabhi nahi.
Lambi line: sirf 79 (1:7 BHAAVARTH, 28 shabd, R2 PASS shabd-ba-shabd; USTAAD). Baaki har line ≤ 25 shabd; SAWAAL ki
sabse lambi line 44 (22 shabd).
