# 003 — सूरह अल-इख़लास (112) | नूर-ए-राह — script (SURAH MODE, do awaazein, UCHARAN format)

> **Format (user 2026-10-30, 002 ka dhaancha):** har jumla = Arabic (Tanzil, bytes unchanged) + `USTAAD — UCHARAN` (wahi Arabic Devanagari me, saada Hindi
> andaaz me, tilawat nahi, screen par Arabic ke neeche) + `BHAAVARTH` + 2-3 chhote vaakya ka matlab. Honest note ek baar intro me (line 5).
> Line numbers file ke kram me 1..52 (koi gap/renumber nahi); UCHARAN hamesha apne BHAAVARTH se pehle; aakhri do lines (50, 51) ke number sabse bade
> (`noor_render.py` end_from = doosri-aakhri line = 50), aakhri cue 52.

## HEADER
- **Channel / format:** noor-e-raah, surah explainer (channel `RULES.md` 1, 1a, 1b, 1c, 2, 2a + 2026-10-30 sections: ucharan, bade screen text). Story 003 of the daily
  series (`series_queue.json` order 2). Kharcha ₹0 (sirf script). Ek chhoti poori SURAH (4 ayat): "units" = 4 jumle (har ayah ek jumla).
- **Content source:** sirf `research/dossier.md` + `sources.json` (Khoji MODE 3, 2026-10-30). Tags dossier ke IDs: parichay **[P#]**, shan-e-nuzul **[N#]**,
  fazilat/hadith **[Z#]**, matlab **[M#]**, tarjuma **[T2]**, ucharan **[T3]**, aaj ki misaal **[MISAAL]**, agli video **[NEXT]**, honest note **[NOTE]**.
  Production me tags spoken text aur captions se hata diye jaayenge (tags quote ke BAAD likhe hain).
- **Awaazein (channel.json "voices"):**
  - `USTAAD` = Algieba — UCHARAN (Arabic ke shabd Devanagari me, saada Hindi andaaz me — tilawat/lai nahi), BHAAVARTH, MATLAB, parichay, shan-e-nuzul,
    hadith, seekh. **Deeni baat sirf Ustaad kehta hai**, hamesha [tag] ke saath.
  - `SAWAAL` = Sulafat — sirf **2 asli sawaal** (line 3 hook ~0:01 aur line 46 seekh ~5:05; gap > 4 min), ek [MISAAL] (line 23: har dar band hone par dil ka
    pukarna — insaani tajurba, koi deeni daava nahi), ek chhota saar (line 38, Ustaad ki hi baat dohrata hai) aur aakhri line 51 (darshakon se comment ki guzarish).
    Khud koi hukm, fazilat, hadith ya tafseer ki baat nahi.
- **Audio:** KOI tilawat nahi. UCHARAN = Ustaad Devanagari me likhe Arabic shabd saade Hindi andaaz me padhta hai; Arabic text khud screen par. Music continuous
  (RULES 1c, ~19 LU neeche), har Arabic block par ek halka swoosh (`[SWOOSH — ARABIC ON SCREEN]`; music chalta rehta hai). Tracks: Soaring (intro + parichay)
  -> River Flute (shan-e-nuzul se ant tak). Ambience: gentle breeze (Freesound CC0).
- **UCHARAN:** har jumle ke Arabic ke theek wahi shabd Devanagari me (nuqta jahan zaroori; koi bracket/tag/maane nahi), Tanzil ke Arabic aur Tanzil ki Latin
  transliteration (`ara-quran-la`, `sources.json` TRANSLIT_TANZIL) se shabd-ba-shabd milaye; jumle ke ant par waqf (aakhri harkat nahi: "अहद", "समद", "यूलद").
  Table + source: `research/ucharan.md`. Ye "padhne ki madad" hai — sahi tilawat ke liye qaari.
- **Tarjuma = SARAL BHAAVARTH (RULES 1a).** Teen maane hue tarjume (al-Umari/QuranEnc, Mahmud Hasan (PD), Tanzil hi.hindi) ke saanjhe matlab par, apne
  shabdon me (`research/translation_options.md`); koi 5+ shabd ka hu-ba-hu tukda nahi. "समद" = "बेनियाज़/सबका सहारा" (al-Umari ka "ab-ran" footnote NAHI — dossier C5).
  Screen label har BHAAVARTH par: **"सरल भावार्थ — माने हुए तर्जुमों के आधार पर"**.
- **Arabic:** Tanzil Uthmani (CC BY 3.0), `research/sources.json` -> `ayat[].text`, **code se copy kiya** (retype nahi, koi NFC/NFKC nahi); AYAH 1 = chaaron ayat
  ek space se joda hua (code se verify). 112:4 ke aakhri `ٌۢ` ka Amiri render Munshi zoom se dekhega. PC par ek baar tanzil.net `quran-uthmani` 112:1-4 se byte-milaan baaki.
- **AYAH blocks:** `[AYAH 1]` = poori surah (4 ayat) ek saath, ~0:30 par (Nigraan LAGU KARO: hook ka vaada 30-40 s me); `[AYAH 2..5]` = ayah 1..4 (Arabic ->
  UCHARAN (screen par Arabic ke neeche) -> BHAAVARTH -> MATLAB). [AYAH 1] par UCHARAN nahi. Map: AYAH 2 = 112:1 · 3 = 112:2 · 4 = 112:3 · 5 = 112:4.
- **Visuals:** sirf jagah, aasmaan, roshni, diye, ret/pahaad, kamra (images.json). **Koi Nabi, Sahabi, farishta, koi insaan nahi** — na aakaar, na parchhai, na haath.
  **Na Allah ka koi roop**. "Na aulad" ke liye koi bachcha/parivaar ka drishya NAHI (sirf khaali samandar-ufaq). Koi likha harf image me nahi; Arabic aur Hindi text hum
  libass/Pillow se lagayenge. Pehle 60 s me har image/crop <= ~8 s.
- **Nigraan LAGU KARO lagu:** (1) hook + pehli Arabic ~0:30 (parichay sirf ek line; makki/madani + shan-e-nuzul ISKE BAAD, Arabic ke baad); koi ginti/naamon ki list
  nahi, nuzool-kramank/doosre naam nahi (P4/P5 "pata nahi"); (2) title me search shabd pehle; thumbnail <= 3-4 bade shabd; pehla frame bina awaaz samajh aaye
  (Arabic title + Hindi caption "सिर्फ़ 4 आयतें").
- **Niyam:** koi fiqh ruling (kab/kitni baar padhna) nahi, koi firqa/maslak nahi, "chhoda gaya" (C1-C11, N1 ko fact ki tarah, P2/P4/P5) ki koi baat nahi;
  "tihai" ke baare me "khatm ka badal/sawab" nahi (Z6). Sirf Bukhari/Muslim ki sahih riwayat (Z1, Z3, Z4; Z6 ikhtilaaf ki tarah). "guarantee/100%/jaadu/taweez" jaise shabd nahi.
- **Spoken honorific:** "नबी सल्लल्लाहु अलैहि वसल्लम" poora; sahaba ke naam ke saath "रज़ियल्लाहु अन्हु" ("अन्हा" Aisha ke liye).

---

## INTRO (`part: intro`, hook)
[SCREEN: raat ka khula aasmaan, ek akela chamakta taara, door tak khaali ret; upar Arabic title سُورَةُ ٱلْإِخْلَاصِ (font se) aur neeche chhota caption "सिर्फ़ 4 आयतें". Pehla frame bina awaaz ke bhi samajh aaye.]
1. [MUSIC soft: Soaring — intro + parichay]
2. [AMBIENCE: gentle breeze (Freesound CC0)]
3. SAWAAL: "उस्ताद जी, सूरह इख़लास तो बचपन से सुनते आए हैं — पर क्या इसका मतलब जानते हैं?"
4. USTAAD: "सिर्फ़ चार आयतें — और हदीस के मुताबिक़ क़ुरआन के तिहाई के बराबर। आज इन्हें एक-एक करके समझते हैं।" [Z1][Z2]
5. USTAAD: "ये पढ़ने की मदद है, तिलावत नहीं — सही तिलावत किसी क़ारी से सुनें।" [NOTE]
## 1. SURAH KA PARICHAY
[SCREEN: wahi akela taara, ret ka shaant ufaq; font se do chhote cards: "सूरह अल-इख़लास · क़ुरआन की 112वीं सूरह", "4 आयतें"]
6. USTAAD: "सूरह अल-इख़लास क़ुरआन की एक सौ बारहवीं सूरह है, और 'इख़लास' यानी सच्चाई, ख़ालिसपन।" [P1]
### [AYAH 1]
[SCREEN: taaron bhara shaant aasmaan; poori surah Arabic me (4 ayat) — swoosh ke saath aati hai]
7. [SWOOSH — ARABIC ON SCREEN]
ARABIC: قُلْ هُوَ ٱللَّهُ أَحَدٌ ٱللَّهُ ٱلصَّمَدُ لَمْ يَلِدْ وَلَمْ يُولَدْ وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ
8. USTAAD: "ये रही पूरी सूरह — चार छोटी आयतें, और एक ही पैग़ाम: अल्लाह एक है।" [P6]
9. [MUSIC continue: River Flute — matlab]
## 2. SHAN-E-NUZUL
[SCREEN: Makka ki tarah ki sookhi ghaati, kaale-bhoore granite pahaad, raat ki chaandni, khaali raasta; koi insaan nahi, koi gumbad/minar nahi]
10. USTAAD: "ज़्यादातर उलमा के मुताबिक़ ये सूरह मक्की है — कुछ उलमा इसे मदनी भी कहते हैं।" [P3]
11. USTAAD: "इसके उतरने का कोई सहीह-दर्जे का ख़ास वाक़िया नहीं मिलता।" [N1][N2]
12. USTAAD: "तफ़्सीरों में एक रिवायत आती है कि लोगों ने अल्लाह के बारे में सवाल किए और जवाब में ये सूरह उतरी — पर इस रिवायत की सनद पर उलमा में इख़्तिलाफ़ है।" [N1][N2]
## 3. AAYAT-DAR-AAYAT
[SCREEN (har Arabic block): Arabic bade Amiri font me (Tanzil Uthmani, bytes unchanged), uske neeche UCHARAN (Devanagari), upar chhota label "सरल भावार्थ — माने हुए तर्जुमों के आधार पर" (sirf BHAAVARTH line par), neeche Hindi caption. Har ayah alag Arabic block.]
### [AYAH 2]
[SCREEN: andhere me ek akela diya, ek hi shaant lau — "ek" ka ishaara; baaki andhera]
13. [SWOOSH — ARABIC ON SCREEN]
ARABIC: قُلْ هُوَ ٱللَّهُ أَحَدٌ
14. USTAAD — UCHARAN: "क़ुल हुवल्लाहु अहद"
15. USTAAD — BHAAVARTH: "पहली आयत: कह दो — वो अल्लाह अकेला है, एक है।" [T2]
16. [MUSIC continue: River Flute — matlab]
17. USTAAD — MATLAB: "'क़ुल' यानी 'कहो' — नबी सल्लल्लाहु अलैहि वसल्लम को हुक्म कि ये बात लोगों तक पहुँचा दें।" [M1]
18. USTAAD — MATLAB: "'अहद' यानी ऐसा एक, जिसका कोई साझी नहीं, कोई जोड़ीदार नहीं — उसके बारे में हिस्सों या जोड़ का ख़याल भी नहीं।" [M1]
### [AYAH 3]
[SCREEN: रेगिस्तान में कई पगडंडियाँ, सब एक ही हरे चश्मे की तरफ़ जाती हुईं (ऊपर से) — "सब उसी की तरफ़"; koi insaan nahi]
19. [SWOOSH — ARABIC ON SCREEN]
ARABIC: ٱللَّهُ ٱلصَّمَدُ
20. USTAAD — UCHARAN: "अल्लाहुस्समद"
21. USTAAD — BHAAVARTH: "दूसरी आयत: अल्लाह बेनियाज़ है — उसे किसी की ज़रूरत नहीं, और सब उसी के मोहताज हैं।" [T2]
22. [MUSIC continue: River Flute — matlab]
23. SAWAAL — MISAAL: "जब हर दरवाज़ा बंद लगे और कोई सहारा न दिखे, तो दिल अपने आप किसी बड़े सहारे को पुकारने लगता है।" [MISAAL]
24. USTAAD — MATLAB: "'समद' यानी वो, जिसकी तरफ़ सब अपनी ज़रूरतों में लौटते हैं, और जिसे ख़ुद किसी की ज़रूरत नहीं।" [M2]
25. USTAAD — MATLAB: "तफ़्सीरों में ये भी आता है कि वो ऐसा सरदार है जिसके ऊपर कोई नहीं।" [M2]
### [AYAH 4]
[SCREEN: शाम का शांत समंदर, सामने बस एक साफ़ ख़ाली ufaq — kuch bhi nahi, na koi bachcha, na parivaar]
26. [SWOOSH — ARABIC ON SCREEN]
ARABIC: لَمْ يَلِدْ وَلَمْ يُولَدْ
27. USTAAD — UCHARAN: "लम यलिद वलम यूलद"
28. USTAAD — BHAAVARTH: "तीसरी आयत: न उसकी कोई औलाद है, और न वो किसी की औलाद है।" [T2]
29. [MUSIC continue: River Flute — matlab]
30. USTAAD — MATLAB: "यानी न उसकी कोई औलाद, न माँ-बाप, न जीवनसाथी।" [M3]
31. USTAAD — MATLAB: "तफ़्सीर में एक दलील आती है: जो पैदा होता है वो मरता है और उसका वारिस होता है — पर अल्लाह न मरता है, न उसका कोई वारिस।" [M3]
### [AYAH 5]
[SCREEN: bahut chauda taaron bhara aasmaan, khaali registaan ke upar — "bade se bada bhi uski barabari nahi"]
32. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ
33. USTAAD — UCHARAN: "वलम यकुल लहू कुफ़ुवन अहद"
34. USTAAD — BHAAVARTH: "चौथी आयत: और कोई भी उसके बराबर, उसके जैसा नहीं।" [T2]
35. [MUSIC continue: River Flute — matlab]
36. USTAAD — MATLAB: "'कुफ़ुव' यानी बराबरी का, जोड़ का।" [M4]
37. USTAAD — MATLAB: "ज़ात में, सिफ़तों में, काम में, ताक़त में — कहीं भी, कभी भी कोई उसके जैसा नहीं।" [M4]
38. SAWAAL: "तो यानी — अल्लाह एक है, सब उसके मोहताज हैं, न उसकी औलाद, न वो किसी की औलाद, और कोई उसके बराबर नहीं।"
## 4. HADITH ME SURAH AL-IKHLAS
[SCREEN: saada mitti ka kamra, chatai, subah ki roshni khidki se; phir khajoor ke beech subah ka raasta, khaali. Hadith ke alfaaz chhote caption me; koi insaan nahi.]
39. [MUSIC soft: River Flute — hadith + seekh]
40. USTAAD: "बुख़ारी की हदीस में अबू सईद ख़ुदरी रज़ियल्लाहु अन्हु बताते हैं: एक आदमी ने किसी को बार-बार 'क़ुल हुवल्लाहु अहद' पढ़ते सुना। सुबह उसने नबी सल्लल्लाहु अलैहि वसल्लम से इसका ज़िक्र किया, जैसे उसे कम समझ रहा हो।" [Z1]
41. USTAAD: "नबी सल्लल्लाहु अलैहि वसल्लम ने फ़रमाया: 'उसकी क़सम जिसके हाथ में मेरी जान है, ये ज़रूर क़ुरआन के तिहाई के बराबर है।'" [Z1]
42. USTAAD: "मुस्लिम की हदीस में अबू हुरैरा रज़ियल्लाहु अन्हु की रिवायत है: नबी सल्लल्लाहु अलैहि वसल्लम ने लोगों को इकट्ठा करके ये सूरह पढ़ी, और फ़रमाया कि ये क़ुरआन के तिहाई के बराबर है।" [Z3]
43. USTAAD: "'तिहाई' का मतलब क्या है, इस पर उलमा के क़ौल अलग हैं; एक क़ौल ये है कि क़ुरआन की बातें तीन हिस्सों में हैं, और अल्लाह के नामों-सिफ़तों का हिस्सा इस सूरह में है।" [Z6]
44. USTAAD: "आइशा रज़ियल्लाहु अन्हा बताती हैं, और बुख़ारी व मुस्लिम दोनों में है: एक आदमी, जो एक दस्ते के सरदार थे, नमाज़ में अपनी क़िरात हर बार 'क़ुल हुवल्लाहु अहद' पर ख़त्म करते थे।" [Z4]
45. USTAAD: "वजह पूछी गई, तो उन्होंने कहा: 'ये रहमान की सिफ़त है, और मुझे इसे पढ़ना पसंद है।' नबी सल्लल्लाहु अलैहि वसल्लम ने फ़रमाया: 'उसे बता दो कि अल्लाह उससे मुहब्बत करता है।'" [Z4]
## 5. SEEKH
[SCREEN: subah ka sunehra ujala registaan par; seekh ke teen chhote cards font se]
46. SAWAAL: "उस्ताद जी, इस सूरह से हमें क्या सीख मिलती है?"
47. USTAAD: "पहली: अल्लाह एक है, अकेला — उसका कोई साझी नहीं। भरोसा और उम्मीद उसी से जुड़ी रहे।" [M1]
48. USTAAD: "दूसरी: सब उसके मोहताज हैं, और वो किसी का मोहताज नहीं — तो मदद की उम्मीद उसी से।" [M2]
49. USTAAD: "तीसरी: तफ़्सीर के मुताबिक़ ये चार आयतें हर ग़लत ख़याल को एक-एक करके हटाती हैं — इसे मतलब समझ कर पढ़ें।" [M5]
[SCREEN (end, aakhri ~15 s end-screen area khaali): tagline card "क़ुरआन, आसान ज़बान में।" + chhota card "Arabic text: Tanzil Project, tanzil.net" + "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"]
50. USTAAD: "अगली बार, नूर-ए-राह में: सूरह अल-फ़लक़ — सुबह के रब की पनाह।" [NEXT]
51. SAWAAL: "और आप कमेंट में बताइए — इन चार आयतों में से कौन-सी बात आपके दिल को सबसे ज़्यादा छू गई, और क्यों।"
52. [MUSIC: River Flute dheere fade-out; aakhri ~3 s sirf gentle breeze]

## SOURCES (description ke liye)
- Arabic Quran text: Tanzil Project (https://tanzil.net) — Tanzil Quran Text, Copyright (C) 2007-2021 Tanzil Project, License: Creative Commons Attribution 3.0. Text unchanged; check https://tanzil.net/updates/ for changes.
- सरल भावार्थ: माने हुए तर्जुमों (Azizul Haq al-Umari / QuranEnc.com; Shaikh-ul-Hind Mahmud Hasan; Suhel Farooq Khan & Saifur Rahman Nadwi / Tanzil hi.hindi) के आधार पर — शब्दशः तर्जुमा नहीं।
- Tafseer: Tafsir Ibn Kathir (112); Ma'ariful Qur'an (Mufti Muhammad Shafi); al-Qurtubi, al-Jami' li-Ahkam al-Qur'an; al-Tabari, Jami' al-Bayan.
- Hadith: Sahih al-Bukhari 5013, 7375; Sahih Muslim 811-813 (numbering sunnah.com par PC se confirm baaki).
- उच्चारण (Arabic की हिंदी लिपि): टंज़ील ट्रांसलिटरेशन से मिलाकर — पढ़ने की मदद, तिलावत नहीं।
- Surah data: Tanzil Quran Metadata (CC BY 3.0, https://tanzil.net).
- Music: "Soaring" Kevin MacLeod (incompetech.com) · "River Flute" Kevin MacLeod (incompetech.com) — both CC BY 4.0, http://creativecommons.org/licenses/by/4.0/
- Ambience: freesound.org (CC0)

## SOURCE MAP — har tag dossier me kahan (Munshi ke liye)
| Tag | Dossier | Grade | Lines |
|---|---|---|---|
| P1 | section 2 P1 (naam, 112vi, 4 ayat; "Sincerity") | maana hua | 6 |
| P3 | P3 (makki zyadatar, madani doosri raay; Ibn Kathir, Qurtubi, MQ, Tanzil) | ikhtilaaf, "ज़्यादातर उलमा ... कुछ उलमा" | 10 |
| P6 | P6 (mukhya sandesh tauheed) | maana hua | 8 |
| N1/N2 | N1 + N2 (surakshit line, shabd-ba-shabd; Tirmidhi riwayat ko fact nahi banaya) | ikhtilaaf, ikhtilaaf ki tarah bola | 11, 12 |
| T2 | translation_options.md (saral bhaavarth) | decision 001 | 15, 21, 28, 34 |
| UCHARAN | research/ucharan.md + sources.json T3 (Tanzil Latin, own Devanagari; plain reading) | decision 2026-10-30 | 14, 20, 27, 33 |
| NOTE | intro honest note, koi deeni daava nahi | decision | 5 |
| M1 | M1 (Qul = hukm; ahad) | maana hua | 17, 18, 47 |
| M2 | M2 (samad: sab lautte hain / sayyid) | maana hua | 24, 25, 48 |
| M3 | M3 (na aulad/waalid/biwi; daleel Ubayy/Ibn Abbas) | maana hua | 30, 31 |
| M4 | M4 (kufuwan) | maana hua | 36, 37 |
| M5 | M5 (Ma'ariful Qur'an: har ghalat khayal ka radd; "Ikrima wala hissa chhoda) | maana hua | 49 |
| Z1 | Z1 (Bukhari 5013/7374, Abu Sa'id) | sahih | 4, 40, 41 |
| Z2 | Z2 (Bukhari 5015 / Muslim 811a "tihai") | sahih | 4 |
| Z3 | Z3 (Muslim 812a/b, Abu Hurairah) | sahih | 42 |
| Z4 | Z4 (Bukhari 7375, Muslim 813, Aisha) | sahih | 44, 45 |
| Z6 | Z6 (Qurtubi: "tihai" ka explanation, ikhtilaaf; "khatm ka badal/sawab" nahi kaha) | ikhtilaaf, "एक क़ौल" | 43 |
Line 3, 38, 46, 51: bina tag (sawaal / Ustaad ki hi baat ka saar / comment ki guzarish — koi deeni daava nahi). Line 23: [MISAAL], insaani tajurba, koi deeni daava nahi.
Line 4 ka "हदीस के मुताबिक़ ... तिहाई के बराबर" = Z1/Z2 ke sahih alfaaz (khatm ka badal nahi kaha). Z5 (sone se pehle), Anas/Quba hadith, C1-C11 SHAMIL NAHI.
Shan-e-nuzul ke bayan sirf: lines 10 (makki/madani, P3), 11-12 (N2).

## SAWAAL ke sawaal — ginti (RULES 1b: max 3-4, beech me >= 3-3.5 min; is chhoti video me user ne max 2 tay kiye)
| Line | Time ~ | Text | Sawaal? |
|---|---|---|---|
| 3 | 0:01 | hook: "क्या इसका मतलब जानते हैं?" | haan (1) |
| 23 | ~1:55 | [MISAAL] dil ka pukarna | nahi |
| 38 | ~3:15 | chhota saar (Ustaad ki baat dohraya) | nahi |
| 46 | ~5:05 | "इस सूरह से हमें क्या सीख मिलती है?" | haan (2) |
| 51 | end | darshakon se comment ki guzarish, `?` nahi | nahi |
Gap pehle-doosre sawaal me ~5:00 (>= 3.5 min). Line 40-45 ke andar hadith ke alfaaz me koi sawaal nahi.

## MISAAL — 1 rakhi (max 2)
- Line 23 (M2): insaani tajurba; Ustaad ka MATLAB (24-25) uske baad "deeni baat" karta hai. Koi doosri misaal nahi.

## IMAGES (long/images.json; 9 nayi + 7 crop entries = 16 entries, free-first, ~₹0 agar Cloudflare chale)
Mapping: 01 akela taara (line 3; crop line 6; crop ant line 50) · 02 diya (line 4; crop AYAH 2) · 04 subah ka ret-tila (line 5; crop line 46 seekh) · 06 milky-way registaan (AYAH 1; crop AYAH 5) ·
03 sookhi ghaati raat (line 10; crop line 12) · 05 pagdandiyan -> chashma (AYAH 3, samad) · 07 shaam ka samandar-ufaq (AYAH 4) · 08 khaali kamra (line 40; crop line 44) · 09 khajoor ka subah raasta (line 42).
Pehle ~60 s (anuman): 01 (0-7) · 02 (7-14) · 04 (14-21) · 01 crop (21-29) · 06 (29-40, builder 2 shots) · 03 (40-48) · 03 crop (48-62, 2 shots) — koi image/crop ~8 s se lambi nahi (MAX_SHOT 8 s).

## LENGTH ESTIMATE (measured TTS of story 002: USTAAD ~0.48 s/shabd at TEMPO 1.08, SAWAAL ~0.35, UCHARAN ~0.78; renderer gaps: speaker badle +0.6 s, wahi +0.35 s, section +0.8 s, har Arabic block +0.6 lead +2.0 Arabic akeli +0.3 hold +0.5 fade)
| Hissa | Shabd | Anuman |
|---|---|---|
| USTAAD (UCHARAN chhod kar) | 559 | ~268 s |
| UCHARAN (4 lines, Arabic ke shabd, dheere) | 13 | ~10 s |
| SAWAAL | 91 | ~32 s |
| Gaps + 5 Arabic blocks (0.6 + 2.0 alone + 0.8 hold/fade) + 5 sections + ant ~3.5 s | | baaki |
| **Kul** | | **~351 s ≈ 5:50** (band 5:30-6:15) |
Pehla poora Arabic (AYAH 1) ~0:31 (swoosh ~31 s; target 30-40 s: PURA). Pehle jumle (AYAH 2) ka Arabic ~1:12, uska BHAAVARTH ~1:17. Target 4:30-6:00 (user): andaza us band me.
Agar asli TTS 6:00 paar kare to pehle ye trim: line 25, line 31 ka dusra hissa, line 43. Kuch pad nahi kiya.

## THUMBNAIL (thumbnail.json, v3 ka dhaancha)
- Arabic: سُورَةُ ٱلْإِخْلَاصِ (surah_titles.json) · Hindi: सूरह अल-इख़लास · **chip: "हदीस में: क़ुरआन के तिहाई के बराबर"** (Z1/Z2 ka sahih wording; "khatm ka badal" nahi) ·
  **hook: "सिर्फ़ *4 आयतें* —\nइनमें है क्या?"** (sawaal, jhoota vaada nahi, title ke shabd nahi dohrata; <= 3-4 bade shabd). Scene: khaali andhera hissa (left 45%), akela taara + ek diya; koi insaan nahi.

## TITLE options (search-phrase pehle; title_suffix "| Noor-e-Raah" jaisa 001/002)
1. **Surah Al-Ikhlas ka Matlab Hindi Mein | 4 Ayat, Padhne ki Madad aur Hadith | Noor-e-Raah** (recommended)
2. Surah Al-Ikhlas Hindi Mein | Har Ayat ka Saral Matlab | Noor-e-Raah
3. Surah Ikhlas ka Matlab | Sirf 4 Ayat, Poora Paigham | Noor-e-Raah

## CONTINUITY / CHECKS
- Sahaba ka naam sirf bola jaata hai (Abu Sa'id al-Khudri, Abu Hurairah, Aisha — lines 40, 42, 44), screen par koi aakaar nahi. Hadith sirf Z1/Z3/Z4 (Bukhari/Muslim); Z5, C1-C11 nahi.
- Tihai (line 4, 41, 42, 43): "barabar" kaha gaya, "khatm ka badal/sawab" kahin nahi (Z6).
- 002 se alag: poori chhoti surah (4 jumle), makki/madani ikhtilaaf + hedged shan-e-nuzul, hadith section me teen sahih riwayat, 2 sawaal, Arabic ~0:30 par. Agli video: Al-Falaq (series_queue order 3, line 50).
- Line numbers 1..52 file ke kram me; UCHARAN (14, 20, 27, 33) apne BHAAVARTH (15, 21, 28, 34) se pehle; aakhri do lines 50, 51; aakhri cue 52.
