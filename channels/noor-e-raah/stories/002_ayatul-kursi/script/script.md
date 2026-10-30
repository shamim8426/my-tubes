# 002 — आयतुल कुर्सी (सूरह अल-बक़रह 2:255) | नूर-ए-राह — script (SURAH MODE, do awaazein)


> **Trim 2026-10-30 (first version, 6:25 -> ~5:30):** lines 6, 14, 28, 36, 46, 50, 55 were removed (numbers NOT renumbered; their cached audio stays unused). The U1/U4/U6/U9 matlab and the K5 summary come back below as NEW lines 81-86 (new text, new numbers).

> **FORMAT DECISION (user 2026-10-30, valid for every Noor video from now on):** pronunciation + fuller meaning. Every
> `[AYAH 2..11]` jumla has a `UCHARAN` line right after the Arabic (the same Arabic words in Devanagari, read plainly by the
> Ustaad - NOT tilawat - and shown under the Arabic on screen), then the saral BHAAVARTH, then 2-3 short sentences of
> meaning in all (BHAAVARTH + MATLAB). One honest note once in the intro (line 70). Length **~7-8 min accepted for this
> video** (the old "4-6 min" note is gone). Devanagari table + source: `research/ucharan.md`, `research/sources.json` (T3).
> **Renumbering:** old line numbers 1-64 and 67-cues are unchanged (cached TTS stays); NEW lines are 70-86; the last two lines
> (old 65, 66) are now **87, 88** and the last cue (old 67) is **89**, because `noor_render.py` treats every line with
> `n >= end_from` (default: the second-to-last line's number) as an end-card line. Old numbers now UNUSED: 65, 66 (cached wav
> ignored - lines 87/88 get new TTS), and the already-unused 6, 14, 28, 36, 46, 50, 55. No existing text was rewritten, so no other old number is
> unused. Order of lines follows the file, not the number.

## HEADER
- **Channel / format:** noor-e-raah, surah explainer (channel `RULES.md` 1, 1a, 1b, 1c). Story 002 of the daily series
  (`series_queue.json` order 1). Kharcha ₹0 (sirf script). Ye ek AAYAT ka video hai: "surah parichay" = Al-Baqarah ke andar is
  aayat ka parichay (naam, jagah, madani, shan-e-nuzul ki sachchi halat); aayat ke 10 jumle = 10 "units".
- **Content source:** sirf `research/dossier.md` + `sources.json` (Khoji MODE 3, 2026-10-29). Tags (001 jaisa, dossier ke
  apne IDs): parichay / shan-e-nuzul = **[P#] / [N#]**, matlab = **[U#] / [K#]**, fazilat = **[FZ-A] / [FZ-B]**, aaj ki misaal
  **[MISAAL]**, agli video **[NEXT]**. Production me tags spoken text aur captions se hata diye jaayenge.
- **Awaazein (channel.json "voices"):**
  - `USTAAD` = Algieba — UCHARAN (Arabic ke shabd Devanagari me, saada Hindi me padhe - tilawat/lai nahi), BHAAVARTH,
    MATLAB, parichay, shan-e-nuzul, hadith, seekh. **Deeni baat sirf Ustaad kehta hai**, hamesha [tag] ke saath.
  - `SAWAAL` = Sulafat — sirf **2 asli sawaal** (line 3 hook ~0:03 aur line 61 ~6:50; beech me ~6:40 ka gap), ek [MISAAL]
    (line 23: insaani thakaan/ooongh — koi deeni daava nahi) aur aakhri line 88 (darshakon se
    comment ki guzarish, Ustaad se sawaal nahi). Khud koi hukm, fazeelat, hadith ya tafseer ki baat nahi.
- **Audio:** KOI tilawat nahi (na insaani, na AI). UCHARAN = Ustaad Devanagari me likhe Arabic shabd saade Hindi andaaz me padhta hai (bina lai/tarz ke); Arabic text khud screen par. Music continuous (RULES 1c, ~19 LU neeche), har Arabic
  block par ek halka swoosh (cue `[SWOOSH — ARABIC ON SCREEN]` = wahi swoosh cue; **music chalta rehta hai**, band
  nahi hota). Tracks: Soaring (intro + parichay) -> River Flute (matlab, hadith, seekh, ant). Ambience: gentle breeze (Freesound CC0).
- **UCHARAN (user 2026-10-30):** har jumle ke Arabic ke theek wahi shabd Devanagari me (nuqta jahan zaroori; koi bracket/tag/maane nahi), Tanzil ke
  Arabic aur Tanzil ki Latin transliteration (`ara-quran-la`) se shabd-ba-shabd milaye; jumle ke ant par waqf (aakhri harkat nahi: "हुव", "नौम", "अर्ज़").
  Table + source: `research/ucharan.md`. Ye "padhne ki madad" hai - sahi tilawat ke liye qaari.
- **Tarjuma = SARAL BHAAVARTH (RULES 1a).** Teen maane hue tarjume (al-Umari/QuranEnc, Mahmud Hasan (PD), Tanzil hi.hindi) ke
  saanjhe matlab par, apne shabdon me (`research/translation_options.md`); koi 5+ shabd ka hu-ba-hu tukda nahi; brackets/footnotes
  kisi tarjume ke nahi. Screen label har BHAAVARTH par: **"सरल भावार्थ — माने हुए तर्जुमों के आधार पर"**.
  "कुर्सी" ke liye lafz "कुर्सी" hi (K6: kuch tarjume "prabhuta/hukumat" likhte hain) + dossier K1/K2/K3/K5 ki surakshit line.
- **Arabic:** Tanzil Uthmani (CC BY 3.0), `research/sources.json` -> `ayah.text`, aayat ka string **code se copy kiya** (retype nahi,
  koi NFC/NFKC nahi) aur code se mila liya: 10 jumlon ke tukde joda to poori aayat se barabar (50 shabd). Libass/Amiri me
  `يَـُٔودُهُۥ` (tatweel + hamza-above) ka render Munshi zoom karega. PC par ek baar tanzil.net `quran-uthmani` 2:255 se byte-milaan baaki.
- **AYAH blocks:** `[AYAH 1]` = poori aayat (50 shabd) ek saath, ~0:42 par (intro ka honest note ~6 s le leta hai); `[AYAH 2..11]` = jumla 1..10 (Arabic tukda -> UCHARAN
  (Devanagari, Arabic ke neeche screen par) -> BHAAVARTH -> MATLAB; BHAAVARTH + MATLAB = 2-3 chhote vaakya). [AYAH 1] par UCHARAN nahi. Map: AYAH 2=U1 · 3=U2 · 4=U3 · 5=U4 · 6=U5 · 7=U6 · 8=U7 · 9=U8 (Kursi) · 10=U9 · 11=U10.
- **Visuals:** sirf jagah, aasmaan, roshni, diye, darwaza, ret/pahaad (images.json). **Koi Nabi, Sahabi, farishta, koi insaan nahi** —
  na aakaar, na parchhai, na haath. **Na Allah ka koi roop, na takht/kursi-furniture**: "Kursi" ke liye sirf bada aasmaan aur ret ki
  chhoti angoothi-si cheez (K3 ka misaali bimb). Koi likha harf image me nahi; Arabic aur Hindi text hum libass se lagayenge.
  Pehle minute me har ~7-9 s par nayi image ya naya crop (Nigraan: kmYyRGdykjY retention).
- **Nigraan LAGU KARO lagu:** hook ka vaada ("10 lines, 10 baatein" + "sabse azeem aayat") ~0:35 tak pehli poori aayat, ~0:48 tak
  pehle jumle ka matlab; parichay+shan-e-nuzul ~19 s (koi ginti/naamon ki list nahi; 286 ayat ki ginti description me); pehle
  frame par Arabic title + Hindi caption (bina awaaz ke samajh aaye).
- **Niyam:** koi fiqh ruling (kab/kitni baar padhna) nahi, koi firqa/maslak nahi, "chhoda gaya" (C1-C15, N3, K4, FZ-C, FZ-D) ki
  koi baat nahi, "guarantee/100%/jaadu/taweez/jinn-bhoot-dar" jaise shabd nahi, U5 me kisi khaas shakhs/wali ki sifarish ki behes nahi.
- **Spoken honorific:** "नबी सल्लल्लाहु अलैहि वसल्लम" poora bola jaata hai; sahaba ke naam ke saath "रज़ियल्लाहु अन्हु".

---

## INTRO (`part: intro`, hook)
[SCREEN: raat ka khula aasmaan, taare, door tak khaali ret ke teele; upar Arabic title आयतुल कुर्सी (font se) aur neeche chhota caption "10 लाइनें, 10 बातें". Pehla frame bina awaaz ke bhi samajh aaye.]
1. [MUSIC soft: Soaring — intro + parichay]
2. [AMBIENCE: gentle breeze (Freesound CC0)]
3. SAWAAL: "उस्ताद जी, आयतुल कुर्सी तो रोज़ पढ़ते हैं — पर क्या हर लाइन का मतलब जानते हैं?"
4. USTAAD: "आज इसकी दस लाइनें, दस बातें। और हदीस के मुताबिक़ ये क़ुरआन की सबसे अज़ीम आयत है।" [FZ-A]
70. USTAAD: "ये पढ़ने की मदद है, तिलावत नहीं — सही तिलावत किसी क़ारी से सुनें।" [NOTE]
## 1. SURAH KA PARICHAY
[SCREEN: subah ki roshni me khajoor ke ped aur mitti ke ghar (saatvi sadi ka Madina), khaali; font se do chhote cards: "सूरह अल-बक़रह · आयत 255", "मदनी"]
5. USTAAD: "ये क़ुरआन की दूसरी सूरह अल-बक़रह की आयत नंबर दो सौ पचपन है; बक़रह पूरी मदनी है, यानी मदीना में उतरी।" [P1][P2]
## 2. SHAN-E-NUZUL
[SCREEN: wahi khaali khajoor ka raasta, subah ka ujala; koi insaan nahi, koi gumbad/minar nahi]
7. USTAAD: "इसके उतरने का कोई मज़बूत, ख़ास वाक़िया रिवायतों में नहीं मिलता।" [N1][N2]
## 3. AAYAT-DAR-AAYAT
[SCREEN (har Arabic block): Arabic bade Amiri font me (Tanzil Uthmani, bytes unchanged), upar chhota label "सरल भावार्थ — माने हुए तर्जुमों के आधार पर" (sirf BHAAVARTH line par), neeche Hindi caption. Poori aayat ke baad har jumla alag Arabic block hai.]
### [AYAH 1]
[SCREEN: raat ka taaron bhara aasmaan, shaant; poori aayat Arabic me (50 shabd) — swoosh ke saath aati hai]
8. [SWOOSH — ARABIC ON SCREEN]
ARABIC: ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلْحَىُّ ٱلْقَيُّومُ لَا تَأْخُذُهُۥ سِنَةٌ وَلَا نَوْمٌ لَّهُۥ مَا فِى ٱلسَّمَٰوَٰتِ وَمَا فِى ٱلْأَرْضِ مَن ذَا ٱلَّذِى يَشْفَعُ عِندَهُۥٓ إِلَّا بِإِذْنِهِۦ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ وَلَا يُحِيطُونَ بِشَىْءٍ مِّنْ عِلْمِهِۦٓ إِلَّا بِمَا شَآءَ وَسِعَ كُرْسِيُّهُ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضَ وَلَا يَـُٔودُهُۥ حِفْظُهُمَا وَهُوَ ٱلْعَلِىُّ ٱلْعَظِيمُ
9. USTAAD: "ये रही पूरी आयत। इसमें दस जुमले हैं — अब एक-एक करके।" [P4]
10. [MUSIC continue: River Flute — matlab]
### [AYAH 2]
[SCREEN: subah ka pehla ujala, khaali shaant registaan ka ufaq]
11. [SWOOSH — ARABIC ON SCREEN]
ARABIC: ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ
71. USTAAD — UCHARAN: "अल्लाहु ला इलाहा इल्ला हुव"
12. USTAAD — BHAAVARTH: "पहला जुमला: अल्लाह — उसके सिवा इबादत के लायक़ कोई नहीं।"
13. [MUSIC continue: River Flute — matlab]
81. USTAAD — MATLAB: "'अल्लाह' उस ज़ात का नाम है जो सारी मख़लूक़ का अकेला रब है। इसीलिए इबादत सिर्फ़ उसी की।" [U1]
### [AYAH 3]
[SCREEN: registaan ke beech hara chashma aur khajoor — zindagi aur sahaara]
15. [SWOOSH — ARABIC ON SCREEN]
ARABIC: ٱلْحَىُّ ٱلْقَيُّومُ
72. USTAAD — UCHARAN: "अल हय्युल क़य्यूम"
16. USTAAD — BHAAVARTH: "दूसरा जुमला: वो हमेशा ज़िंदा है, और सबको थामे-सँभाले हुए है।"
17. [MUSIC continue: River Flute — matlab]
18. USTAAD — MATLAB: "'हय्य' यानी हमेशा ज़िंदा — जिसे कभी मौत नहीं आती।" [U2]
19. USTAAD — MATLAB: "'क़य्यूम' यानी जो ख़ुद अपने दम पर क़ायम है और सबको क़ायम रखता है — सब उसके सहारे, वो किसी के सहारे नहीं।" [U2]
### [AYAH 4]
[SCREEN: chaandni me soye hue ghar ki chhatein (khaali), bas ek diya jaagta hua]
20. [SWOOSH — ARABIC ON SCREEN]
ARABIC: لَا تَأْخُذُهُۥ سِنَةٌ وَلَا نَوْمٌ
73. USTAAD — UCHARAN: "ला ताख़ुज़ुहू सिनतुन वला नौम"
21. USTAAD — BHAAVARTH: "तीसरा जुमला: न उसे ऊँघ आती है, न नींद।"
22. [MUSIC continue: River Flute — matlab]
23. SAWAAL — MISAAL: "हम तो थोड़ी देर जागें तो आँखें भारी हो जाती हैं, और ऊँघ आने लगती है।" [MISAAL]
24. USTAAD — MATLAB: "'सिनह' यानी ऊँघ, 'नौम' यानी गहरी नींद — दोनों नहीं। उसे कभी कोई कमी या बेख़बरी नहीं।" [U3]
### [AYAH 5]
[SCREEN: pahaad, samandar aur taaron bhara aasmaan ek hi nazar me]
25. [SWOOSH — ARABIC ON SCREEN]
ARABIC: لَّهُۥ مَا فِى ٱلسَّمَٰوَٰتِ وَمَا فِى ٱلْأَرْضِ
74. USTAAD — UCHARAN: "लहू मा फ़ी अस्समावाति वमा फ़ी अल अर्ज़"
26. USTAAD — BHAAVARTH: "चौथा जुमला: आसमानों में जो कुछ है और ज़मीन में जो कुछ है — सब उसी का है।"
27. [MUSIC continue: River Flute — matlab]
82. USTAAD — MATLAB: "यानी आसमानों और ज़मीन की हर चीज़ उसी की मिल्कियत है, सब उसके बंदे हैं। इख़्तियार भी उसी का है।" [U4]
### [AYAH 6]
[SCREEN: ek band naqqashidaar lakdi ka darwaza, kinaron se andar ki roshni chhanti hui; koi insaan nahi]
29. [SWOOSH — ARABIC ON SCREEN]
ARABIC: مَن ذَا ٱلَّذِى يَشْفَعُ عِندَهُۥٓ إِلَّا بِإِذْنِهِۦ
75. USTAAD — UCHARAN: "मन ज़ा अल्लज़ी यशफ़उ इंदहू इल्ला बि इज़्निह"
30. USTAAD — BHAAVARTH: "पाँचवाँ जुमला: कौन है जो उसकी इजाज़त के बिना, उसके सामने किसी की सिफ़ारिश कर सके?"
31. [MUSIC continue: River Flute — matlab]
32. USTAAD — MATLAB: "सिफ़ारिश यानी किसी के हक़ में बात करना — उसके सामने बिना इजाज़त कोई बोल तक नहीं सकता।" [U5]
83. USTAAD — MATLAB: "जिसे वो इजाज़त दे, वही बोल सकता है; उसकी इजाज़त के बिना कोई दम नहीं मार सकता।" [U5]
### [AYAH 7]
[SCREEN: dhundh me jaata ek raasta, aage bhi peeche bhi door tak (khaali)]
33. [SWOOSH — ARABIC ON SCREEN]
ARABIC: يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ
76. USTAAD — UCHARAN: "यअलमु मा बैना ऐदीहिम वमा ख़लफ़हुम"
34. USTAAD — BHAAVARTH: "छठा जुमला: वो जानता है जो उनके आगे है, और जो उनके पीछे है।"
35. [MUSIC continue: River Flute — matlab]
84. USTAAD — MATLAB: "यानी बीता कल, आज और आने वाला कल — हर बात उसे मालूम है। ज़ाहिर भी, और छुपी हुई भी।" [U6]
### [AYAH 8]
[SCREEN: bade andhere hall me ek chhota diya, uski roshni ka ek chhota ghera; baaki andhera]
37. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَلَا يُحِيطُونَ بِشَىْءٍ مِّنْ عِلْمِهِۦٓ إِلَّا بِمَا شَآءَ
77. USTAAD — UCHARAN: "वला युहीतूना बि शैइन मिन इल्मिही इल्ला बिमा शा"
38. USTAAD — BHAAVARTH: "सातवाँ जुमला: उसके इल्म का कोई हिस्सा कोई घेर नहीं सकता — बस उतना, जितना वो ख़ुद चाहे।"
39. [MUSIC continue: River Flute — matlab]
40. USTAAD — MATLAB: "यानी हम उतना ही जानते हैं जितना उसने जानने दिया। पूरा इल्म सिर्फ़ उसी का है।" [U7]
### [AYAH 9]
[SCREEN: khaali vishaal registaan, door ret par padi ek chhoti angoothi-si gol cheez, upar bahut bada aasmaan]
41. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَسِعَ كُرْسِيُّهُ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضَ
78. USTAAD — UCHARAN: "वसिअ कुर्सिय्युहु अस्समावाति वल अर्ज़"
42. USTAAD — BHAAVARTH: "आठवाँ जुमला: उसकी कुर्सी आसमानों और ज़मीन को समेटे हुए है।"
43. [MUSIC continue: River Flute — matlab]
44. USTAAD — MATLAB: "'कुर्सी' की हक़ीक़त पर उलमा के कई क़ौल हैं: इब्ने अब्बास रज़ियल्लाहु अन्हु का एक क़ौल है अल्लाह का इल्म, और ज़्यादातर रिवायतों के मुताबिक़ वो अर्श के सामने एक अज़ीम मख़लूक़ है।" [K1][K2]
45. USTAAD — MATLAB: "नबी सल्लल्लाहु अलैहि वसल्लम ने बताया कि सातों आसमान उसके मुक़ाबले में वीराने में पड़े एक छल्ले जैसे हैं।" [K3]
85. USTAAD — MATLAB: "हर क़ौल का सार एक ही है: अल्लाह की अज़मत इतनी बड़ी है कि आसमान और ज़मीन उसके सामने बहुत छोटे हैं — और वो किसी जगह या तख़्त का मोहताज नहीं।" [K5]
### [AYAH 10]
[SCREEN: ek ke baad ek khade pahaad aur shaant jheel, subah ki halki roshni]
47. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَلَا يَـُٔودُهُۥ حِفْظُهُمَا
79. USTAAD — UCHARAN: "वला यऊदुहू हिफ़्ज़ुहुमा"
48. USTAAD — BHAAVARTH: "नौवाँ जुमला: और उन दोनों की निगहबानी उसे ज़रा भी भारी नहीं पड़ती।"
49. [MUSIC continue: River Flute — matlab]
86. USTAAD — MATLAB: "यानी आसमानों और ज़मीन को सँभालना उसके लिए बिलकुल आसान है। न कोई बोझ, न कोई थकान।" [U9]
### [AYAH 11]
[SCREEN: badalon ke beech se utarti sunehri kirnein, khula aasmaan]
51. [SWOOSH — ARABIC ON SCREEN]
ARABIC: وَهُوَ ٱلْعَلِىُّ ٱلْعَظِيمُ
80. USTAAD — UCHARAN: "व हुवल अलिय्युल अज़ीम"
52. USTAAD — BHAAVARTH: "दसवाँ जुमला: और वही सबसे बुलंद है, सबसे अज़ीम है।"
53. [MUSIC continue: River Flute — matlab]
54. USTAAD — MATLAB: "'अलिय्य' यानी मर्तबे में सबसे ऊँचा, जगह की ऊँचाई के मानी में नहीं। 'अज़ीम' यानी अज़मत और ताक़त में सबसे बड़ा।" [U10]
## 4. HADITH ME AYATUL KURSI
[SCREEN: saada mitti ka kamra, chatai aur ek diya, khaali; phir raat ki khidki se taare, takiya aur bistar, koi insaan nahi. Hadith ke alfaaz chhote caption me.]
56. [MUSIC soft: River Flute — hadith + seekh]
57. USTAAD: "मुस्लिम की हदीस में है कि नबी सल्लल्लाहु अलैहि वसल्लम ने उबैय बिन काब रज़ियल्लाहु अन्हु से पूछा:" [FZ-A]
58. USTAAD: "'ऐ अबुल-मुन्ज़िर, अल्लाह की किताब की कौन-सी आयत तुम्हारे पास सबसे अज़ीम है?' उन्होंने आयतुल कुर्सी पढ़ी, तो नबी सल्लल्लाहु अलैहि वसल्लम ने उनका सीना थपथपाकर कहा: 'तुम्हें इल्म मुबारक हो!'" [FZ-A]
59. USTAAD: "बुख़ारी की हदीस में अबू हुरैरा रज़ियल्लाहु अन्हु की रिवायत है कि उन्हें बताया गया: सोने के लिए बिस्तर पर जाओ, तो आयतुल कुर्सी पढ़ लो — अल्लाह की तरफ़ से एक निगहबान तुम्हारे साथ रहेगा, और सुबह तक शैतान तुम्हारे क़रीब नहीं आएगा। और नबी सल्लल्लाहु अलैहि वसल्लम ने फ़रमाया कि उसने सच कहा।" [FZ-B]
60. USTAAD: "ये अल्लाह पर भरोसे और उससे दुआ की बात है; नतीजा उसी के हाथ में है।" [FZ-B]
## 5. SEEKH
[SCREEN: subah ka sunehra ujala registaan par; seekh ke teen chhote cards font se]
61. SAWAAL: "उस्ताद जी, इस आयत से हमें क्या सीख मिलती है?"
62. USTAAD: "पहली: अल्लाह हमेशा ज़िंदा है, सबको सँभालता है, उसे ऊँघ भी नहीं आती, नींद भी नहीं — भरोसा उसी पर।" [U2][U3]
63. USTAAD: "दूसरी: इख़्तियार, इजाज़त और इल्म सब उसके हाथ में हैं — उम्मीद और मदद उसी से।" [U4][U5][U7]
64. USTAAD: "तीसरी: इसे मतलब समझ कर पढ़ें — हर बार ये दस बातें याद आएँगी।" [P4]
[SCREEN (end, aakhri ~15 s end-screen area khaali): tagline card "क़ुरआन, आसान ज़बान में।" + chhota card "Arabic text: Tanzil Project, tanzil.net" + "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"]
87. USTAAD: "अगली बार, नूर-ए-राह में: सूरह अल-इख़लास — सिर्फ़ चार आयतें।" [NEXT]
88. SAWAAL: "और आप कमेंट में बताइए — इन दस बातों में से कौन-सी आपके दिल को सबसे ज़्यादा छू गई, और क्यों।"
89. [MUSIC: River Flute dheere fade-out; aakhri ~3 s sirf gentle breeze]

## SOURCES (description ke liye)
- Arabic Quran text: Tanzil Project (https://tanzil.net) — Tanzil Quran Text, Copyright (C) 2007-2021 Tanzil Project, License: Creative Commons Attribution 3.0. Text unchanged; check https://tanzil.net/updates/ for changes.
- सरल भावार्थ: माने हुए तर्जुमों (Azizul Haq al-Umari / QuranEnc.com; Shaikh-ul-Hind Mahmud Hasan; Suhel Farooq Khan & Saifur Rahman Nadwi / Tanzil hi.hindi) के आधार पर — शब्दशः तर्जुमा नहीं।
- Tafseer: Tafsir Ibn Kathir (2:255); Ma'ariful Qur'an (Mufti Muhammad Shafi); al-Qurtubi, al-Jami' li-Ahkam al-Qur'an; al-Tabari, Jami' al-Bayan.
- Hadith: Sahih Muslim 810; Sahih al-Bukhari 2311 (also 3275, 5010). (PC par sunnah.com se wording dobara dekhni baaki.)
- Surah data: Tanzil Quran Metadata (CC BY 3.0, https://tanzil.net).
- Music: "Soaring" Kevin MacLeod (incompetech.com) · "River Flute" Kevin MacLeod (incompetech.com) — both CC BY 4.0, http://creativecommons.org/licenses/by/4.0/
- Ambience: freesound.org (CC0)

## SOURCE MAP — har tag dossier me kahan (Munshi ke liye)
| Tag | Dossier | Grade | Lines |
|---|---|---|---|
| P1 | section 2 P1 (2:255, Baqarah doosri surah) | maana hua | 5 |
| P2 | P2 (Baqarah poori Madani, bila khilaf) | maana hua | 5 |
| P4 | P4 (10 mukammal jumle: IK, MQ) | maana hua | 9, 64 |
| UCHARAN | research/ucharan.md + sources.json T3 (Tanzil Latin transliteration, own Devanagari; plain reading) | decision 2026-10-30 | 71-80 |
| NOTE | intro honest note (user 2026-10-30), no deeni claim | decision | 70 |
| N1/N2 | N1/N2 (koi pakka khaas shan-e-nuzul nahi) | maana hua | 7 |
| U1-U10 | section 3 table | maana hua | 81 (U1), 18-19, 24, 82 (U4), 32, 83 (U5), 84 (U6), 40, 86 (U9), 54 |
| K1/K2 | section 4 K1, K2 (ikhtilaaf, "kai qaul", "zyadatar riwayat") | ikhtilaaf, ikhtilaaf ki tarah bola | 44 |
| K3 | K3 (Abu Dharr, anguthi/chhalla, Ibn Hibban/Bayhaqi sahih) | maana hua | 45 |
| K5 | K5 (Allah jagah/takht ka mohtaj nahi) + "Video ke liye surakshit line" | maana hua | 85 |
| FZ-A | section 5 FZ-A (Sahih Muslim 810) | maana hua | 4, 57-58 |
| FZ-B | FZ-B (Sahih Bukhari 2311), "bharosa aur dua, natija Allah ke haath" (section 6) | maana hua | 59-60 |
Line 4 ka "हदीस के मुताबिक़ ... सबसे अज़ीम" = FZ-A ka dossier-surakshit chip-wording. Line 9, 61, 88 bina tag (koi deeni daava nahi). Line 70 = [NOTE] (padhne ki madad, koi deeni daava nahi).
Shan-e-nuzul ke bayan sirf ek: line 7 (N1/N2) — sources: Wahidi dataset (2:255 ki entry nahi), Ibn Kathir, Ma'ariful Qur'an, Jalalayn, Baghawi.

## SAWAAL ke sawaal — ginti (RULES 1b, user: is video me max 2)
| Line | Time ~ | Text | Sawaal? |
|---|---|---|---|
| 3 | 0:00 | hook: "क्या हर लाइन का मतलब जानते हैं?" | haan (1) |
| 23 | ~2:50 | [MISAAL] insaani ooongh | nahi |
| 61 | ~6:50 | "इस आयत से हमें क्या सीख मिलती है?" | haan (2) |
| 88 | ~7:20 | darshakon se comment ki guzarish ("बताइए"), `?` nahi | nahi (Ustaad se sawaal nahi) |
Gap pehle-doosre sawaal me ~6:50 (>= 3.5 min). Ustaad ki line 58 ke andar hadith ka sawaal ("कौन-सी आयत ... सबसे अज़ीम है?") hadith ke alfaaz hain, SAWAAL ka sawaal nahi. Line 55 pehle hi hata di gayi thi.

## MISAAL — 1 rakhi (max 2)
- Line 23 (U3): insaani ooongh/thakaan ka rozmarra tajurba; koi deeni daava nahi, Ustaad ka MATLAB (line 24) uske baad "mazhab ki baat" karta hai. Koi doosri misaal nahi (U5/U6 ki misaal firqa/dar ki taraf ja sakti thi).

## IMAGES (long/images.json; 12 nayi + 8 reuse_id = 20 entries)
Free flux-class prompts (places/sky/light/lamps only). Mapping: 01 stars (line 3; reuse AYAH 1 aur ant) · 02 diya (line 4; reuse U7) · 03 Madina subah (line 5, line 57) · 04 khajoor raasta (line 6-7; reuse U6) ·
05 subah ka ufaq (U1; reuse seekh) · 06 chashma (U2) · 07 chaandni chhatein + ek diya (U3) · 08 panorama (U4; reuse U9) · 09 band darwaza + roshni (U5) ·
10 ret me chhoti angoothi (U8; line 45 par reuse zoom) · 11 badal ki kirnein (U10) · 12 khaali bistar + diya (hadith FZ-B). Pehle ~60 s: 01 (0-7 s) · 02 (7-15) · 03 (15-24) · 04 (24-34, 2 shots) · 01 reuse (34-46, 2 shots) · 05 (46-62).

## LENGTH ESTIMATE (measured TTS of this story: USTAAD ~0.48 s/shabd at TEMPO 1.08; renderer gaps: speaker badle +0.6 s, wahi +0.35 s, section +0.8 s, har Arabic block +0.6 lead +2.0 Arabic akeli +0.3 hold)
| Hissa | Shabd (USTAAD / SAWAAL) | Anuman |
|---|---|---|
| Purana asli render (34 lines, real TTS) | 529 / 64 | 332 s (5:32) |
| Naye lines 70-86 (note 14 shabd, 10 ucharan = 50 Arabic shabd, 6 matlab ~130 shabd) | +194 | +93 s speech |
| Ucharan Arabic shabd dheere padhe jaate hain (~0.6 s/shabd) + 17 naye gaps | | +~17 s |
| **Kul** | **723 / 64** | **~442 s ≈ 7:20** (7:00-7:45) |
Lines 87/88 (purani 65/66) ka TTS naya banega (chhoti lines). Pehla poora Arabic (AYAH 1) ~0:42 (note +~7 s; RULES ka ~35 s target se ~7 s upar — user ko batao); pehle jumle ka BHAAVARTH ~1:00.
Agar asli TTS 8:00 paar kare to pehle ye trim: line 82/84/86 ka dusra vaakya, line 83.

## THUMBNAIL (thumbnail.json, v3 ka dhaancha)
- Arabic: آيَةُ ٱلْكُرْسِيِّ · Hindi: आयतुल कुर्सी · **chip: "हदीस में: क़ुरआन की सबसे अज़ीम आयत"** (FZ-A ka surakshit shabd, "सबसे बड़ी" nahi) ·
  **hook: "रोज़ पढ़ते हैं —\nपर *10 बातें* जानते हैं?"** (sawaal, jhoota vaada nahi, title ke shabd nahi dohrata). Scene: maujooda `scene` (khaali mehrab-hall, diye, noor; koi insaan nahi).

## TITLE options (search-phrase pehle; title_suffix "| Noor-e-Raah" jaisa 001)
1. **Ayatul Kursi ka Matlab Hindi Mein | Saral Bhaavarth, Line by Line | Noor-e-Raah** (recommended)
2. Ayatul Kursi Hindi Mein | 10 Jumle, 10 Baatein aur Hadith | Noor-e-Raah
3. Ayatul Kursi ka Matlab | Roz Padhte Hain, Ab Samjhein | Noor-e-Raah

## CONTINUITY / CHECKS
- Sahaba ka naam sirf bola jaata hai (Ubayy bin Ka'b, line 57), screen par koi aakaar nahi. Dono hadith dossier ke "HAAN" waale (FZ-A, FZ-B); FZ-C/D (daif/ikhtilaaf) nahi.
- 001 se alag: ek aayat, 10 units (har ek par uccharan + fuller matlab), hadith section, 2 sawaal. Agli video: Surah Al-Ikhlas (series_queue order 2).
