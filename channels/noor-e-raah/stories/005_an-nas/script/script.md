# 005 — सूरह अन-नास (114) | नूर-ए-राह — script (SURAH MODE, do awaazein, UCHARAN format)

> **Format (004 ka dhaancha):** har jumla = Arabic (Tanzil, bytes unchanged) + `USTAAD — UCHARAN` (wahi Arabic Devanagari me, saada Hindi andaaz me, tilawat nahi, screen par Arabic ke
> neeche) + `BHAAVARTH` + 1-2 line ka MATLAB (2-3 chhote vaakya). Honest note ek baar intro me (line 5). Line numbers file ke kram me 1..56 (koi gap/renumber nahi); UCHARAN hamesha apne BHAAVARTH
> se pehle; **aakhri do bolne wali lines 54, 55 (sabse bade bolte numbers), aakhri cue 56 -> `long/render.json` me `end_from: 54`.**

## HEADER
- **Channel / format:** noor-e-raah, surah explainer (channel `RULES.md` 1, 1a, 1b, 1c, 2, 2a + ucharan, bade screen text, Image reuse first). Story 005 of the daily series (`series_queue.json` order 4).
  Kharcha script ke liye Rs0. Chhoti SURAH (6 ayat): 6 ayah-blocks + 1 poori-surah block (AYAH 1 = poori surah, usme UCHARAN nahi).
- **Length target:** `series_queue.json length_target_min` = 4-6 min (short surahs) -> ~6:00 (estimate neeche; 004 ke ~7:07 se chhota, isliye matlab 1-2 line/jumla, hadith 2 riwayat compact).
- **Content source:** sirf `research/dossier.md` + `sources.json` (Khoji MODE 3, 2026-11-03). Tags = dossier IDs: parichay **[P#]**, shan-e-nuzul **[N#]**, fazilat/hadith **[Z#]**, matlab **[M#]**,
  tarjuma **[T2]**, ucharan **[T3]**, aaj ki misaal **[MISAAL]**, agli video **[NEXT]**, honest note **[NOTE]**. Production me tags spoken text aur captions se hata diye jaayenge.
- **HOOK (naya, IMAANDAAR):** series_queue ka `hook_hint` ("जीत मिले तो क्या करें?") An-Nasr surah ka hai, An-Nas ka nahi — NAHI liya. Naya hook (line 3): "कभी-कभी मन में बिना बुलाए बुरा ख़याल आ जाता है। क़ुरआन की आख़िरी सूरह इसी बारे में क्या सिखाती है?" —
  surah ka asli mukhya vishay (vasvasa, P6/M2/M3) hai; vaada line 4 + Arabic (line 7) me ~0:30 tak pura. Search title wahi: "Surah Nas ka Matlab Hindi Mein".
- **Sanchalak ke faisle jo lagu hue (004 ki tarah):** (1) shan-e-nuzul = "koi sahih-दर्जे ki khaas wajah nahi" (line 12); **jaadu/Labid/girah/11-ayat waqia POORA CHHODA** (C1); koi "isliye utri" daava nahi;
  (2) Makki/Madani = "उलमा में इख़्तिलाफ़ है" (line 11, "zyadatar" nahi); (3) fazilat sirf Muslim 814 (Z1, line 47) aur Bukhari 5017/5748 (Z2, line 48), riwayat ke taur par, "badal/gaarantee/hukm" nahi;
  Bukhari 5016 (Z3) aur C1-C8 SHAMIL NAHI; (4) SAWAAL ke max 2 asli sawaal (lines 3 aur 50; gap ~5 min).
- **Awaazein (channel.json "voices"):** `USTAAD` = Algieba (UCHARAN, BHAAVARTH, MATLAB, parichay, hadith, seekh — deeni baat sirf Ustaad, hamesha [tag] ke saath). `SAWAAL` = Sulafat — 2 asli sawaal (line 3 ~0:01, line 50 ~5:15),
  ek [MISAAL] (line 35: raat ka andar ka khayaal, insaani tajurba, koi deeni daava nahi) aur aakhri line 55 (comment ki guzarish, `?` nahi). Khud koi hukm/fazilat/hadith/tafseer nahi.
- **Audio:** KOI tilawat nahi. UCHARAN = Devanagari me likhe Arabic shabd saade andaaz me. Music continuous (RULES 1c, ~19 LU neeche), har Arabic block par ek halka swoosh. Tracks: Soaring (intro + parichay)
  -> River Flute (shan-e-nuzul se ant). Ambience: night wind + crickets, phir subah ki chidiyaan (CC0, `shared/sfx/noor/`).
- **UCHARAN:** har jumle ke Arabic ke theek wahi shabd Devanagari me, `research/ucharan.md` ki "Line:" se (Tanzil Latin se shabd-ba-shabd; assimilated lam: बिरब्बिन नास, मलिकिन नास, इलाहिन नास, शर्रिल वसवासिल ख़न्नास, सुदूरिन नास, वन नास);
  "ye padhne ki madad hai" (line 5).
- **Tarjuma = SARAL BHAAVARTH (RULES 1a)** — teen tarjume (Tanzil hi.hindi, Muhammad Farooq Khan, Mahmud Hasan PD) ke saanjhe matlab par, apne shabdon me (`research/translation_options.md`); Tanzil ke bracket-izafe
  "(शैतानी)", "(ख़ुदा के नाम से)" NAHI liye. Label: **"सरल भावार्थ — माने हुए तर्जुमों के आधार पर"**.
- **Arabic:** Tanzil Uthmani (CC BY 3.0), `research/sources.json` -> `ayat[].text`, **code se copy** (retype nahi, koi NFC/NFKC); AYAH 1 = chhah ayat ek space se joda (code se). Bismillah 114:1 ka hissa nahi (nahi lagayi). Sanchalak ne 2026-11-03 ko PC par Tanzil se byte-milaan bataya; sources.json/dossier ka PC-check note abhi purana (update baaki).
  Amiri render zoom (shadda wali jagah, 114:3 ka khanjari alif إِلَٰهِ) Munshi ke build review me.
- **Visuals:** sirf jagah, aasmaan, roshni, diye, darwaza, ret, kamra. **Koi Nabi, Sahabi, farishta, shaitan/jinn ka roop, insaan nahi** — na aakaar, na parchhai, na haath. Vasvase ke liye sirf andhera, band khidki/darwaza, khaali raasta.
  Koi likha harf image me nahi. **Images: poori reuse (0 nayi)**, Google balance kam; thumbnail wallpaper nayi (free Cloudflare pehle).
- **Nigraan LAGU KARO lagu:** (1) hook ke baad ~0:36 par pehla poora Arabic (line 7); parichay sirf EK line (6), ginti/naamon ki list nahi, "114vi/6 ayat" sirf screen card par, bolne me nahi; shan-e-nuzul Arabic ke baad;
  (2) title me search shabd pehle; thumbnail <= 3-4 bade shabd; pehla frame bina awaaz samajh aaye; (3) pehle 60 s me ek image/crop max ~8 s (IMAGES section).
- **Niyam:** koi fiqh hukm (kab/kitni baar), koi firqa/maslak, koi "chhoda gaya" baat (C1-C8) nahi. "guarantee/100%/nazar/taweez/jaadu" jaise shabd nahi.
- **Spoken honorific:** "नबी सल्लल्लाहु अलैहि वसल्लम" poora; sahaba ke saath "रज़ियल्लाहु अन्हु" ("अन्हा" Aisha ke liye).

---

## INTRO (`part: intro`, hook)
[SCREEN: गहरी रात, ख़ाली रेत के टीले, एक तारा; ऊपर Arabic title سُورَةُ ٱلنَّاسِ (font se) aur neeche chhota caption "दिल में चुपके से आने वाली बात". Pehla frame bina awaaz ke bhi samajh aaye: raat, ek tara, akela dil.]
1. [MUSIC soft: Soaring — intro + parichay]
2. [AMBIENCE: night wind + crickets, dheere se subah ki chidiyaan (Freesound CC0)]
3. SAWAAL: "उस्ताद जी, कभी-कभी मन में बिना बुलाए बुरा ख़याल आ जाता है। क़ुरआन की आख़िरी सूरह इसी बारे में क्या सिखाती है?"
4. USTAAD: "ये सूरह ऐसे ही चुपके से आने वाले ख़याल की बुराई से पनाह माँगना सिखाती है। आज इसकी आयतें एक-एक करके समझते हैं।" [P6]
5. USTAAD: "ये पढ़ने की मदद है, तिलावत नहीं — सही तिलावत किसी क़ारी से सुनें।" [NOTE]
## 1. SURAH KA PARICHAY
[SCREEN: ek chhota card: "सूरह अन-नास · क़ुरआन की 114वीं सूरह"; peeche raat ka aasmaan]
6. USTAAD: "सूरह अन-नास में "नास" का मतलब है — लोग, इंसान। ये क़ुरआन की आख़िरी सूरह है।" [P1]
### [AYAH 1]
[SCREEN: taaron bhara aasmaan; poori surah Arabic me (6 ayat) — swoosh ke saath aati hai]
7. [SWOOSH — ARABIC ON SCREEN]
ARABIC: قُلْ أَعُوذُ بِرَبِّ ٱلنَّاسِ مَلِكِ ٱلنَّاسِ إِلَٰهِ ٱلنَّاسِ مِن شَرِّ ٱلْوَسْوَاسِ ٱلْخَنَّاسِ ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ
8. USTAAD: "ये रही पूरी सूरह — छोटी-छोटी आयतें, और एक ही बात: वसवसे की बुराई से पनाह सिर्फ़ अल्लाह की।" [P6]
9. [MUSIC continue: River Flute — matlab]
## 2. SHAN-E-NUZUL
[SCREEN: Makka ki tarah ki sookhi ghaati raat me, kaale-bhoore pahaad, khaali raasta; koi insaan nahi, koi gumbad/minar nahi]
10. USTAAD: "इस सूरह को "अल-फ़लक़" के साथ "मुअव्विज़तैन" कहा जाता है — यानी पनाह माँगने वाली दो सूरतें।" [P2]
11. USTAAD: "ये सूरह मक्की है या मदनी — इस पर उलमा में इख़्तिलाफ़ है। कुछ इसे मक्की कहते हैं, कुछ मदनी।" [P3]
12. USTAAD: "इसके उतरने की कोई सहीह-दर्जे की ख़ास वजह नहीं मिलती।" [N2]
## 3. AAYAT-DAR-AAYAT
[SCREEN (har Arabic block): Arabic bade Amiri font me (Tanzil Uthmani, bytes unchanged), uske neeche UCHARAN (Devanagari), upar chhota label "सरल भावार्थ — माने हुए तर्जुमों के आधार पर" (sirf BHAAVARTH line par), neeche Hindi caption. Har ayah alag Arabic block. Vasvase/shaitan/jinn ka koi roop nahi — sirf andhera, diya, darwaza, raasta.]
### [AYAH 2]  (= 114:1)
[SCREEN: raat ki ghaati, door ek diya — "sahara"; koi insaan nahi]
13. [SWOOSH — ARABIC ON SCREEN]
ARABIC: قُلْ أَعُوذُ بِرَبِّ ٱلنَّاسِ
14. USTAAD — UCHARAN: "क़ुल अऊज़ु बिरब्बिन नास"
15. USTAAD — BHAAVARTH: "पहली आयत: कहो — मैं लोगों के रब की पनाह माँगता हूँ।" [T2]
16. [MUSIC continue: River Flute — matlab]
17. USTAAD — MATLAB: ""क़ुल" यानी "कहो" — पनाह माँगने की ये बात कहने का हुक्म। "अऊज़ु" यानी मैं पनाह माँगता हूँ, सहारा लेता हूँ।" [M1]
18. USTAAD — MATLAB: ""रब" यानी मालिक, जो हर हाल में पालने वाला है। ये "लोगों के" रब के साथ आया है।" [M1]
### [AYAH 3]  (= 114:2)
[SCREEN: ek band bhaari darwaza, uske kinaron se sunehri roshni; koi insaan nahi]
19. [SWOOSH — ARABIC ON SCREEN]
ARABIC: مَلِكِ ٱلنَّاسِ
20. USTAAD — UCHARAN: "मलिकिन नास"
21. USTAAD — BHAAVARTH: "दूसरी आयत: लोगों के बादशाह की पनाह।" [T2]
22. [MUSIC continue: River Flute — matlab]
23. USTAAD — MATLAB: ""मलिक" यानी बादशाह। तफ़्सीर के मुताबिक़ कुछ लोग ख़ुद को बादशाह समझ बैठते हैं, मगर असली बादशाह अल्लाह है।" [M1]
### [AYAH 4]  (= 114:3)
[SCREEN: ek akela diya andheri kothri me, uski golai me roshni; koi insaan nahi]
24. [SWOOSH — ARABIC ON SCREEN]
ARABIC: إِلَٰهِ ٱلنَّاسِ
25. USTAAD — UCHARAN: "इलाहिन नास"
26. USTAAD — BHAAVARTH: "तीसरी आयत: लोगों के इलाह की पनाह — यानी उसकी, जिसकी इबादत की जाती है।" [T2]
27. [MUSIC continue: River Flute — matlab]
28. USTAAD — MATLAB: ""इलाह" यानी वो, जिसकी इबादत की जाए। तफ़्सीर में आता है कि कुछ लोग दूसरों को पूजते हैं, मगर इबादत सिर्फ़ उसी की है।" [M1]
### [AYAH 5]  (= 114:4)
[SCREEN: bahut gehri raat, ek band khidki ke bahar andhera; phir door diye ki halki lau; koi insaan nahi]
29. [SWOOSH — ARABIC ON SCREEN]
ARABIC: مِن شَرِّ ٱلْوَسْوَاسِ ٱلْخَنَّاسِ
30. USTAAD — UCHARAN: "मिन शर्रिल वसवासिल ख़न्नास"
31. USTAAD — BHAAVARTH: "चौथी आयत: उसकी बुराई से, जो दिल में बुरा ख़याल डालकर पीछे हट जाता है।" [T2]
32. [MUSIC continue: River Flute — matlab]
33. USTAAD — MATLAB: ""वसवास" यानी वसवसा डालने वाला — जो दिल में बुरा ख़याल डालता है। "ख़न्नास" यानी पीछे हट जाने वाला।" [M2]
34. USTAAD — MATLAB: "तफ़्सीर में आता है कि बंदा अल्लाह को याद करे, तो वो पीछे हट जाता है — और ग़फ़लत में फिर वसवसा डालता है।" [M2]
35. SAWAAL: "रात को अकेले में कोई ग़लत ख़याल चुपके से आए, और फिर दुआ याद आते ही दिल हल्का हो जाए — सोचिए, ऐसा पल कैसा लगता है।" [MISAAL]
### [AYAH 6]  (= 114:5)
[SCREEN: khaali raasta andhere me, door subah ki halki lakeer; koi insaan nahi]
36. [SWOOSH — ARABIC ON SCREEN]
ARABIC: ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ
37. USTAAD — UCHARAN: "अल्लज़ी युवस्विसु फ़ी सुदूरिन नास"
38. USTAAD — BHAAVARTH: "पाँचवीं आयत: वही, जो इंसानों के सीनों में बुरे ख़याल डालता रहता है।" [T2]
39. [MUSIC continue: River Flute — matlab]
40. USTAAD — MATLAB: ""सुदूर" यानी सीने, यानी दिल। यानी वसवसा दिलों में डाला जाता है।" [M3]
### [AYAH 7]  (= 114:6)
[SCREEN: subah ka ujala, khula raasta, aasmaan saaf; koi insaan nahi]
41. [SWOOSH — ARABIC ON SCREEN]
ARABIC: مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ
42. USTAAD — UCHARAN: "मिनल जिन्नति वन नास"
43. USTAAD — BHAAVARTH: "छठी आयत: चाहे वो जिन्नों में से हो, या इंसानों में से।" [T2]
44. [MUSIC continue: River Flute — matlab]
45. USTAAD — MATLAB: "यानी वसवसा डालने वाले जिन्नों में से भी हो सकते हैं और इंसानों में से भी। इब्ने कसीर के मुताबिक़ महफ़ूज़ वही है, जिसे अल्लाह बचाए।" [M4][M5]
## 4. HADITH ME SURAH AN-NAS
[SCREEN: saada kamra, bistar ke paas chhota diya, khidki se taare; hadith ke alfaaz chhote caption me; koi insaan nahi]
46. [MUSIC soft: River Flute — hadith + seekh]
47. USTAAD: "मुस्लिम की हदीस में उक़्बा बिन आमिर रज़ियल्लाहु अन्हु बताते हैं कि नबी सल्लल्लाहु अलैहि वसल्लम ने फ़रमाया: "क्या तुमने नहीं देखा, आज रात ऐसी आयतें उतारी गईं जैसी पहले कभी नहीं देखी गईं?" और फिर इन्हीं दो सूरतों का ज़िक्र किया।" [Z1]
48. USTAAD: "बुख़ारी की रिवायत में आइशा रज़ियल्लाहु अन्हा बताती हैं: नबी सल्लल्लाहु अलैहि वसल्लम हर रात बिस्तर पर जाते, तो हथेलियों में फूँककर "क़ुल हुवल्लाहु अहद" और ये दोनों सूरतें पढ़ते, फिर सिर, चेहरे और जिस्म पर हाथ फेरते — तीन बार।" [Z2]
49. USTAAD: "ये सिर्फ़ रिवायत है — यहाँ कोई हुक्म या वादा नहीं बताया जा रहा।" [NOTE]
## 5. SEEKH
[SCREEN: subah ka sunehra ujala; seekh ke teen chhote cards font se]
50. SAWAAL: "उस्ताद जी, इस सूरह से हमें क्या सीख मिलती है?"
51. USTAAD: "पहली: बुरे ख़याल या वसवसे से बचने के लिए पहला सहारा अल्लाह की पनाह है।" [P6]
52. USTAAD: "दूसरी: वसवसा आए तो अल्लाह को याद करें — तफ़्सीर के मुताबिक़ याद करने पर वो पीछे हट जाता है।" [M2]
53. USTAAD: "तीसरी: माआरिफ़ुल क़ुरआन के मुताबिक़ अल-फ़लक़ में दुनिया की मुसीबतों से पनाह है, और अन-नास में आख़िरत की आज़माइशों से — दोनों साथ, उसी एक रब की।" [M5]
[SCREEN (end, aakhri ~15 s end-screen area khaali): tagline card "क़ुरआन, आसान ज़बान में।" + chhota card "Arabic text: Tanzil Project, tanzil.net" + "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"]
54. USTAAD: "अगली बार, नूर-ए-राह में: सूरह अल-कौसर — क़ुरआन की सबसे छोटी सूरह।" [NEXT]
55. SAWAAL: "और आप कमेंट में बताइए — इन छह आयतों में से कौन-सी बात आपके दिल को सबसे ज़्यादा छू गई, और क्यों।"
56. [MUSIC: River Flute dheere fade-out; aakhri ~3 s sirf gentle breeze]

## SOURCES (description ke liye)
- Arabic Quran text: Tanzil Project (https://tanzil.net) — Tanzil Quran Text, Copyright (C) 2007-2021 Tanzil Project, License: Creative Commons Attribution 3.0. Text unchanged; check https://tanzil.net/updates/ for changes.
- सरल भावार्थ: माने हुए तर्जुमों (Suhel Farooq Khan / Tanzil hi.hindi; Muhammad Farooq Khan; Shaikh-ul-Hind Mahmud Hasan) के आधार पर — शब्दशः तर्जुमा नहीं।
- Tafseer: Tafsir Ibn Kathir (114); Ma'ariful Qur'an (Mufti Muhammad Shafi); al-Qurtubi, al-Jami' li-Ahkam al-Qur'an; al-Tabari, Jami' al-Bayan.
- Hadith: Sahih Muslim 814; Sahih al-Bukhari 5017, 5748 (numbering sunnah.com par PC se confirm baaki).
- उच्चारण (Arabic की हिंदी लिपि): टंज़ील ट्रांसलिटरेशन से मिलाकर — पढ़ने की मदद, तिलावत नहीं।
- Surah data: Tanzil Quran Metadata (CC BY 3.0, https://tanzil.net).
- Music: "Soaring" Kevin MacLeod (incompetech.com) · "River Flute" Kevin MacLeod (incompetech.com) — both CC BY 4.0, http://creativecommons.org/licenses/by/4.0/
- Ambience: freesound.org (CC0)

## SOURCE MAP — har tag dossier me kahan (Munshi ke liye)
| Tag | Dossier | Grade | Lines |
|---|---|---|---|
| P1 | P1 (naam, 114vi/aakhri, 6 ayat; "nas" = log) | maana hua | 6 |
| P2 | P2 (Mu'awwidhatayn) | maana hua | 10 |
| P3 | P3 (Makki/Madani IKHTILAAF, "zyadatar" nahi) | ikhtilaaf | 11 |
| P6 | P6 (mukhya sandesh: vasvase ki burai se panah Allah se) | maana hua | 4, 8, 51 |
| N2 | N1+N2 safe wording: sahih-दर्जे ki khaas wajah nahi; jaadu waqia POORA CHHODA | maana hua | 12 |
| T2 | translation_options.md (saral bhaavarth) | decision 001 | 15, 21, 26, 31, 38, 43 |
| UCHARAN | research/ucharan.md + sources.json T3 | decision 2026-10-30 | 14, 20, 25, 30, 37, 42 |
| NOTE | intro honest note (5); riwayat-only note (49) | decision | 5, 49 |
| M1 | M1 (qul=hukm; rab/malik/ilah; "logon ke" teen baar) | maana hua | 17, 18, 23, 28 |
| M2 | M2 (waswas/khannas; zikr par peeche; Tabari wali baat NAHI li) | maana hua | 33, 34, 52 |
| M3 | M3 (sudoor = seene/dil; andar ka khatra) | maana hua | 40 |
| M4 | M4 core (jinn aur insaan dono me se; ikhtilaaf nahi) | maana hua | 45 |
| M5 | M5 (Ibn Kathir "safe wahi jise Allah bachaye"; Ma'ariful: Falaq bahar, Nas andar) | maana hua | 45, 53 |
| Z1 | Z1 (Muslim 814, 'Uqba bin 'Amir) | sahih (PC check needed) | 47 |
| Z2 | Z2 (Bukhari 5017, 5748, Aisha; riwayat, hukm nahi) | sahih (PC check needed) | 48 |
| NEXT | series_queue order 5: al-kausar (3 ayat) | queue | 54 |
Line 3, 50, 55: bina tag (sawaal / comment ki guzarish — koi deeni daava nahi). Line 35: [MISAAL], insaani tajurba. Z3 (Bukhari 5016) aur C1-C8 SHAMIL NAHI.
Shan-e-nuzul ke bayan sirf lines 10 (P2), 11 (P3), 12 (N2). "ज़्यादातर" shabd Makki/Madani par kahin nahi.

## SAWAAL ke sawaal — ginti (RULES 1b: max 3-4, beech me >= 3-3.5 min)
| Line | Time ~ | Text | Sawaal? |
|---|---|---|---|
| 3 | 0:01 | hook: "आख़िरी सूरह इसी बारे में क्या सिखाती है?" | haan (1) |
| 35 | ~3:05 | [MISAAL] andar ka khayaal | nahi |
| 50 | ~5:15 | "इस सूरह से हमें क्या सीख मिलती है?" | haan (2) |
| 55 | end | comment ki guzarish, `?` nahi | nahi |
Gap ~5 min (>= 3.5 min). Hadith lines (47-49) me koi sawaal nahi.

## MISAAL — 1 rakhi (max 2): line 35 (M2 ke baad), deeni daava nahi, koi vyakti drishya nahi.

## IMAGES (long/images.json banana baad me; **0 NAYI image, sab library reuse + crop, Rs0**; thumbnail wallpaper alag nayi, free engine pehle)
Source paths (sab maujood, check kiye):
- A `channels/noor-e-raah/stories/003_al-ikhlas/images/01_one_star_night.png`  - B `.../003_al-ikhlas/images/06_milkyway_desert.png`  - C `.../003_al-ikhlas/images/04_dawn_sand_ridge.png`  - D `.../003_al-ikhlas/images/08_empty_room_morning.png`  - E `.../003_al-ikhlas/images/09_morning_palm_path.png`
- F `.../001_al-fatiha/images/09_single_lamp_dark.png`  - G `.../001_al-fatiha/images/05_night_lamp_path.png`  - H `.../001_al-fatiha/images/07_rocky_valley_moon.png`  - I `.../001_al-fatiha/images/06_makka_night_houses.png`  - J `.../001_al-fatiha/images/18_lamp_toward_light.png`  - K `.../001_al-fatiha/images/22_path_fading_tracks.png`  - L `.../001_al-fatiha/images/23_golden_valley_full_light.png`
- M `.../002_ayatul-kursi/images/09_lit_door.png`  - N `.../002_ayatul-kursi/images/02_lamp_on_stone.png`  - O `.../002_ayatul-kursi/images/07_moonlit_rooftops_lamp.png`  - P `.../002_ayatul-kursi/images/12_bedtime_room_lamp.png`
(16 alag base images; 004 ke ye kam-dohraye gaye: 001 ki 7 images 004 me nahi thi; A, B, C, D, E, P 004 me bhi the — alag crop rect.)
| Lines | Image | Shot | Lagbhag samay |
|---|---|---|---|
| 3 | A poori | raat + ek tara | 0-9 s |
| 4 | A crop 1 (neeche-baayen) 9-14 s, phir A crop 2 (upar-daayen, alag rect) 14-20 s | tara/rait ka tukda | 9-20 s |
| 5 | F poori | akela diya, andhera | 20-26 s |
| 6 | G poori | raat ka diye wala raasta | 26-32 s |
| 7-8 (AYAH 1) | B poori, phir B crop (Milky Way ka kendra) | taaron bhara aasmaan | 32-40, 40-47 s |
| 10 | H poori | Makka-jaisi ghaati raat | 46-54 s |
| 11 | H crop (ghaati ka raasta) | | 54-62 s |
| 12 | I poori | door ke ghar, raat | 62-70 s |
| 13-18 (114:1) | J poori (13-15), J crop (diye ki taraf, 16-18) | | |
| 19-23 (114:2) | M poori (19-21), M crop (darwaze ki daraar, 22-23) | | |
| 24-28 (114:3) | N poori (24-26), N crop (lau, 27-28) | | |
| 29-32, 33-35 (114:4) | O poori (29-31), O crop (khidki ki lau, 32-34), F crop alag rect (35, misaal) | | |
| 36-40 (114:5) | K poori (36-38), K crop khaali raasta (39-40) | | |
| 41-45 (114:6) | C poori (41-43), C crop (44-45) | | |
| 46-49 (hadith) | P poori (46-48), P crop (lamp, 49) | | |
| 50-53 (seekh) | D poori (50-51), D crop (52), L poori (53) | | |
| 54-56 (ant) | E poori (54-55), E crop / L crop (56) | | |
Pehle ~60 s: A (0-9) · A crop (9-17) · F (17-24) · G (24-31) · B (31-39) · B crop (39-46) · H (46-54) · H crop (54-62): koi image/crop ~8 s se lambi nahi (1 image / ~8 s). Same (image, rect) dobara nahi.
Kul: 29 clips, 16 base images (A-P), 0 nayi. Vasvase/shaitan/jinn ke liye koi aakaar nahi — sirf andhera, diya, darwaza, raasta.

## LENGTH ESTIMATE (measured TTS rates, story 003/004: USTAAD ~0.48 s/shabd at TEMPO 1.08, SAWAAL ~0.35, UCHARAN ~0.78; gaps: speaker badle +0.6 s, wahi +0.35 s, section +0.8 s, har Arabic block ~3.4 s)
| Hissa | Shabd | Anuman |
|---|---|---|
| USTAAD (UCHARAN chhod kar) | 539 | ~259 s |
| UCHARAN (6 lines) | 21 | ~16 s |
| SAWAAL | 82 | ~29 s |
| Gaps + 7 Arabic blocks + 5 sections + ant ~3.5 s | | ~53 s |
| **Kul** | | **~357 s ≈ 5:57** (band 5:30-6:20; target 4-6 min) |
**Pehla poora Arabic (AYAH 1, line 7) ~0:36** (target 30-40 s: PURA). Pehle jumle (114:1) ka Arabic ~1:15. Agar asli TTS 6:20 paar kare to pehle trim: line 18, line 34, line 49.

## THUMBNAIL (thumbnail.json, v3 ka dhaancha)
Arabic سُورَةُ ٱلنَّاسِ (surah_titles.json) · Hindi सूरह अन-नास · chip: "दिल की बात, रब की पनाह" · hook text: "*वो कौन* जो दिल में\nचुपके से बोलता है?" (<= 4 bade shabd; title ke shabd nahi dohrata; shaitan ka koi roop nahi). Scene: gehri raat, ek diya (left 45% shaant), koi insaan nahi.
Wallpaper NAYI, free engine (Cloudflare flux) pehle; paid Gemini sirf fallback aur sirf balance > Rs50 floor par.

## TITLE options (search-phrase pehle; suffix "| Noor-e-Raah")
1. **Surah Nas ka Matlab Hindi Mein | 6 Ayat, Padhne ki Madad aur Hadith | Noor-e-Raah** (recommended; queue search_title se match)
2. Surah An-Nas Hindi Mein | Har Ayat ka Saral Matlab | Noor-e-Raah
3. Surah Nas ka Matlab | Dil ke Vasvase se Panah, 6 Ayat | Noor-e-Raah

## CONTINUITY / CHECKS
- Sahaba ke naam sirf bole jaate hain (Uqba bin Amir line 47, Aisha line 48); screen par koi aakaar nahi. Hadith sirf Z1 (Muslim 814), Z2 (Bukhari 5017/5748). Z3, C1-C8 nahi.
- Nabi SAW par jaadu ka waqia: kahin nahi. Shaitan/jinn ka koi roop-varnan nahi (C3): "वसवसा डालने वाला", "पीछे हट जाने वाला" sirf M2 ka saral maana.
- 004 se alag: 6 ayat (3 chhoti "logon ke" sifaat + 3), hook = andar ka vasvasa (naya), hadith = Z1+Z2 compact, length ~6 min (queue target 4-6), images zyada 001 se reuse.
- Line numbers 1..56 file ke kram me; UCHARAN (14, 20, 25, 30, 37, 42) apne BHAAVARTH (15, 21, 26, 31, 38, 43) se pehle; aakhri bolti lines 54, 55; aakhri cue 56; render.json end_from = 54.
- PC check needed (Sanchalak/user): sunnah.com par Muslim 814, Bukhari 5017, 5748 ka number+text (aaj 403, dossier ke hisaab se likhe).
