# Dossier - Surah Al-Falaq (113) (004_al-falaq) | Khoji MODE 3

> **STATUS:** Arabic = ALLOWED (Tanzil Uthmani, CC BY 3.0; **PC byte-milaan zaroori**, strings fetch-tool se aaye). Hindi = SARAL BHAAVARTH (001 ka faisla; `translation_options.md`). **Koi LICENCE SHAK nahi.**
> **"Not opened" (cloud se nahi khule):** tanzil.net, sunnah.com, quran.com, islamqa/islamweb, altafsir, archive.org. Tafseer/hadith/translit text GitHub ke public datasets se (003 jaisa); har "PC check" niche likha hai.
- Bana 2026-10-31, Khoji, Rs0. Koi audio/tilawat nahi. Facts [F#] = `sources.json` ke ids (T1..T3, P1..P6, N1..N2, Z1..Z3, M1..M6).
- Ek line: panah maangne wali surah - Allah subah ke rab se, uski banayi har cheez ki, raat ke andhere ki, girah par phoonkne wali jaadu ki aur jalne wale ki burai se.
- **003 se farq:** (a) Makki/Madani me saaf "zyadatar" nahi - dono raay barabar (P3); (b) shan-e-nuzul ka jadoo-wala waqia hai magar uska surah ke nuzool se rishta sahih nahi (N1); (c) Tabari me na Makki/Madani na koi shan-e-nuzul.

## 1. Text sources
### 1.1 Arabic (Tanzil Uthmani) [T1] - ALLOWED
- Licence: 001-003 dossier jaisa (CC BY 3.0; verbatim, koi badlav nahi; "Tanzil Project" + link tanzil.net; description me notice).
- Snapshot: `risan/quran-json data/tanzil/uthmani.json` (003 wali hi file, sha256 `adaebb377c60eba1bab6ef652959c7a0b4ccb4d0ca42145945c14ecdbeb4b761`; aaj file download/sha nahi chalaya - text WebFetch se). Keys: chapter/verse/text.
- **Dhyan:** 113:1 ke aage Bismillah laga hai (`بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ ` + ayah). Bismillah 113:1 ka hissa **nahi** - hata kar neeche wala string (003 jaisa).
- Ayat (NFC/NFKC KABHI nahi; sha256 = UTF-8 string ka, local gine):

| Ayah | Arabic (Tanzil) | shabd | sha256 |
|---|---|---|---|
| 113:1 | قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ | 4 | 75a64035932e6081c4320fdfb0ce915e0e52916bd43529e78de14c6e58018ada |
| 113:2 | مِن شَرِّ مَا خَلَقَ | 4 | d32e9c709ebc5af1e748de00998b7374522ebec9fe48b907a62c87cd951445d9 |
| 113:3 | وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ | 5 | 394467f255bf2e28dea9d9eaefcd433b356e6e262199baced055efd9f1b2358c |
| 113:4 | وَمِن شَرِّ ٱلنَّفَّٰثَٰتِ فِى ٱلْعُقَدِ | 5 | 84dd76ff082d11699ac26e5594a27d6e7fda29666c377ff0452d3ebd4f477efa |
| 113:5 | وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ | 5 | e5f17e625f6b71834b9763cb904de787efa5e3167b25e58f79cf27c6827c6725 |

- **PC par karo:** (a) tanzil.net `quran-uthmani` se in 5 ayat ka byte-milaan (BOM + Bismillah hatao) aur sha dobara chalao - ek bhi harf/harkat ka farq = ye table galat. (b) 113:4 `ٱلنَّفَّٰثَٰتِ` (shadda + khanjari alif) ka libass/Amiri render Munshi zoom se dekho.
### 1.2 Hindi [T2]
001 ka faisla: **SARAL BHAAVARTH** (on-screen "सरल भावार्थ - माने हुए तर्जुमों के आधार पर"). Teen tarjume: al-Umari (QuranEnc), Mahmud Hasan (Urdu, PD), Tanzil `hi.hindi`. Cross-check: Farooq, Maududi, Taqi Usmani. Poora comparison + kunji-shabd: `translation_options.md`.
### 1.3 Latin transliteration -> Devanagari ucharan [T3]
`sources.json` -> `source_keys.TRANSLIT_TANZIL` aur `TRANSLIT_Q411` ke `text_per_ayah` (aur `ayat[].translit_*`). Kalam Devanagari likhega, Latin sirf jaanch ke liye.

| Ayah | Tanzil (ara-quran-la) | Quran411 (waqf rup) |
|---|---|---|
| 1 | Qul aAAoothu birabbi alfalaqi | Qul a'uzoo bi rabbil-falaq |
| 2 | Min sharri ma khalaqa | Min sharri ma khalaq |
| 3 | Wamin sharri ghasiqin itha waqaba | Wa min sharri ghasiqin iza waqab |
| 4 | Wamin sharri alnnaffathati fee alAAuqadi | Wa min sharrin-naffaa-thaati fil 'uqad |
| 5 | Wamin sharri hasidin itha hasada | Wa min shar ri haasidin iza hasad |

Sujhaav (Kalam): jumle - 113:1 "क़ुल" + "अऊज़ु बिरब्बिल फ़लक़"; 113:2 ek jumla; 113:3 "व मिन शर्रि ग़ासिक़िन" + "इज़ा वक़ब"; 113:4 "व मिन शर्रिन नफ़्फ़ासाति" + "फ़िल उक़द"; 113:5 "व मिन शर्रि हासिदिन" + "इज़ा हसद" (jumla-end par aakhri harkat girao: फ़लक़, ख़लक़, वक़ब, उक़द, हसद). Quran411 ka "aAAoothu"=अऊज़ु, "aAAuqadi"=उक़दि; "ن + ٱل" ka idgham (शर्रिन नफ़्फ़ासाति: Quran411 `sharrin-naffaa-thaati`) - waqf/wasl check ke liye; Arabic ka har shabd rahe. Dataset ki Q411 5vi ayah me extra space ("shar ri") - ignore.

## 2. Surah parichay + Shan-e-Nuzul
Grade: **maana hua** / **ikhtilaaf** / **chhoda gaya** (VIDEO ME KABHI NAHI).

| ID | Baat | Source(s) | Grade |
|---|---|---|---|
| P1 | Naam **अल-फ़लक़** (الفلق): "subah/daybreak"; Quran ki **113vi** surah, **5 ayat**, parah 30. | Tanzil chapters.json; Qurtubi (5 ayat) | maana hua |
| P2 | An-Nas ke saath inhe **"मुअव्विज़तैन"** (panah maangne wali do surah) kehte hain. | Ibn Kathir (EN+AR), Qurtubi, Ma'ariful Qur'an | maana hua |
| P3 | **Makki ya Madani - IKHTILAAF, "zyadatar" nahi keh sakte.** Makki: Qurtubi pehla qaul (al-Hasan, 'Ikrima, 'Ata', Jabir), Tanzil metadata. Madani: Ibn Kathir (Arabic matan: "wa huma madaniyyatan"), Qurtubi doosra qaul (Ibn 'Abbas ka ek qaul, Qatada). Ma'ariful Qur'an/Tabari: koi faisla nahi. Video: "इस पर उलमा में इख़्तिलाफ़ है - कुछ मक्की, कुछ मदनी कहते हैं।" | Qurtubi; Ibn Kathir AR; Tanzil chapters | ikhtilaaf |
| P4 | **Nuzool ka kramank**: aaj khule kisi source me nahi. Video me number mat bolo. | - | pata nahi (PC par accepted list se) |
| P5 | **Doosre naam**: Mu'awwidhatayn (P2) ke siva koi alag naam nahi mila. (Qurtubi "al-Muqashqishatan" - ek source, video me nahi.) | Qurtubi, IK | pata nahi / chhoda |
| P6 | Mukhya sandesh: har buri cheez se - raat ka andhera, jaadu, hasad - panah sirf Allah se, "subah ke rab" se. Ma'ariful: ye surah duniyawi museebaton ki panah; An-Nas aakhirat/andar ki. | Ma'ariful Qur'an; Ibn Kathir; Qurtubi; Tabari | maana hua |
| N1 | **Shan-e-nuzul - sahih-grade KOI NAHI.** Jaadu ka waqia (Labid bin al-A'sam, Banu Zuraiq, kanghi/baal/khajoor ka khol, Dharwan ka kuan) **Bukhari 5763 (Aisha) me sahih** hai; Nabi SAW ne badla nahi liya ("मैं लोगों में बुराई फैलाना नहीं चाहता"). Magar **sahih riwayat me ye nahi likha ki yahi surah ussi wajah se utri**. "11 girah = 11 ayat (113+114), har ayah par ek girah khuli" - Ibn 'Abbas/Tha'labi ki riwayat, bina sahih sanad (Ibn Kathir: Tha'labi wale bayaan me "nakarah"; Qurtubi bhi Ibn 'Abbas ka bayaan deta hai; Ma'ariful Qur'an teen bayaan (Ahmad, Bukhari, Tha'labi) shan-e-nuzul ke taur par deta hai). Tabari: na Labid ka zikr na shan-e-nuzul. | Bukhari 5763; Ibn Kathir AR+EN; Qurtubi; Ma'ariful Qur'an; Tabari | ikhtilaaf, sahih nahi - **fact ke taur par video me NAHI** |
| N2 | Video ke liye surakshit line: "इस सूरह के उतरने की वजह के बारे में तफ़्सीरों में नबी ﷺ पर जादू वाले वाक़िए का ज़िक्र आता है, पर सहीह रिवायत में सिर्फ़ वो वाक़िया है - ये नहीं लिखा कि सूरह उसी की वजह से उतरी; इसलिए इस पर उलमा में इख़्तिलाफ़ है।" **Behtar/aasan:** jaadu ka waqia poora chhod kar sirf: "सूरह के उतरने का कोई सहीह-दर्जे का ख़ास वाक़िया नहीं मिलता" + P3 ki makki/madani line (003 jaisa). Waqia sunane ki zaroorat nahi; nazuk vishay (Nabi SAW + jaadu) - Kalam chhota rakhe, koi drishya nahi. | N1 + P3 | maana hua |

### 2a. Chhoda gaya (VIDEO ME KABHI NAHI)
| ID | Baat | Kyun |
|---|---|---|
| C1 | "Surah Labid ke jaadu ki wajah se utri; 11 girah = 11 ayat; har ayah par ek girah khuli" (Ibn 'Abbas/Tha'labi/Qushayri; "Yahudi bachcha baal le gaya") | Sanad nahi/gharib; Ibn Kathir: nakarah; sahih Bukhari 5763 me surah ka rishta nahi |
| C2 | "Falaq = Jahannam ki qaid/ghati/darakht/kuan" (Ibn 'Abbas, Ubayy, Ibn 'Umar, Sa'id bin Jubayr, Kalbi; Tabari/Qurtubi me) | Ibn Kathir: marfu' sabit nahi; ulama ka zyada mashhoor maana subah (M1) |
| C3 | Ibn Mas'ud ka Mu'awwidhatayn ko mushaf me na likhna / "dua hai Quran nahi" (Ahmad, Bukhari 4976-4977; Qurtubi) | Ijma' se radd (Qurtubi), sahabi par bahas, bina-wajah firqawari/ilmi bahas - video ke dayre se bahar |
| C4 | Tha'labi/Ibn 'Abbas ka "Jibril ki ruqya", "Ali, Zubair, Ammar ne kuan ka paani ulta" tafseeli waqia | Sanad nahi, Sahabi/Jibril ka drishya |
| C5 | "Jaadu ek saal/6 mahine raha" (Ahmad/Qurtubi) | Muddat par riwayatein alag-alag, sahih nahi |
| C6 | Nasai (Abu Hurayra) "jis ne girah lagakar phoonka usne jaadu kiya... shirk" | Isnad/grade khula nahi; fiqh-hukm wala vishay |
| C7 | Ghasiq = "saanp ka daat marna", "tara", "Surayya ka girna se bimari" (Abu Hurayra, Ibn Zayd) | Ibn Kathir: Abu Hurayra wali marfu' sabit nahi; sirf "raat" (M3) core hai; chaand wali hadith hasan sahih par ikhtilaafi tafseer |
| C8 | Ibn Zayd: hasid = Yahudi (Tabari) | Ek taabi'i qaul, ek qaum par ilzam - RULES (kisi dharm/qaum par faisla nahi) |
| C9 | Nasai (Uqba): "Allah ke yahan inse behtar kuch nahi padhoge"; "inhi jaisa koi panah nahi mangta" / Nasai (Ibn 'Abis) | Bukhari/Muslim nahi - channel ka sahih-source niyam; PC par agar user chahe to alag grade check |
| C10 | Abu Dawud 1462 / Tirmidhi 2903 (gharib): har namaz ke baad padho | Bukhari/Muslim nahi (Tirmidhi gharib) - hold |
| C11 | Tirmidhi 3575 / Nasai / Ahmad: subah-sham teen baar Ikhlas+Mu'awwidhatayn "har cheez ke liye kaafi"; Ahmad ('Abdullah bin Khubayb) | Hasan (Bukhari/Muslim nahi); user chahe to PC check |
| C12 | Tirmidhi (Abu Sa'id): Nabi SAW jinn/insaan ki nazar se panah maangte the, in surahon ke baad sirf inhi par aa gaye (hasan sahih) | Bukhari/Muslim nahi; nazar (evil eye) ka vishay - nazuk, hold |
| C13 | "Hasid ki dua kabool nahi" wali hadith (Qurtubi), "hasad pehla gunah (Iblis/Qabil)" riwayat | Grade nahi diya; sirf Qurtubi ka hawala |

## 3. Fazilat (sirf Bukhari/Muslim, sahih) - hadith ke alfaaz sahi hi bolna
| ID | Hadith | Source (sunnah.com number; text dataset se padha) |
|---|---|---|
| Z1 | 'Uqba bin 'Amir: Nabi SAW ne farmaya: "क्या तुमने नहीं देखा, आज रात ऐसी आयतें उतारी गईं जैसी पहले कभी नहीं देखी गईं?" - "क़ुल अऊज़ु बिरब्बिल फ़लक़" aur "क़ुल अऊज़ु बिरब्बिन्नास". | Muslim 814 (dataset hadithnumber 1891); Ibn Kathir AR bhi "Muslim no. 814" likhta hai; MQ me |
| Z2 | 'Aisha: Nabi SAW har raat bistar par jaate to dono hathelian jod kar, phoonk kar, Ikhlas+Falaq+Nas padhte, phir jahan tak haath pahunche jism par phirate - sir, chehra, aage ka hissa - teen baar. (Sirf riwayat, koi hukm mat do) | Bukhari 5017, 5748; Ibn Kathir, Qurtubi, MQ |
| Z3 | 'Aisha: bimari me Nabi SAW Mu'awwidhat padh kar apne upar phoonkte; aakhri bimari me 'Aisha padh kar unke haath se jism par haath phiratin. (Sirf riwayat) | Bukhari 5016; Muwatta Malik; Ibn Kathir, Qurtubi, MQ |

Z1 "yaad rakhne ki saadi baat": Z1+Z2 hi video ke liye kaafi; Z3 optional. **Ye mat kaho:** "jaadu/nazar utarne ki gaarantee", "ye padhne se jaadu nahi lagta", "hukm ki tarah": sirf "riwayat me aata hai".

## 4. Meaning per ayah [M#] (kam se kam 2 tafseer ka milaa hua)
| ID | Ayah | Saajhi baat (Hindi me saral) | Tafseer |
|---|---|---|---|
| M1 | 113:1 | "कहो" = kehne ka hukm; *a'udhu* = main panah maangta/sahara leta hoon; *falaq* = chirna/phaadna; zyadatar mufassirin ke mutabiq **subah/pau phatna** (jab roshni raat ko cheerti hai). Tabari/Qurtubi: lafz bada hai - har wo cheez jise Allah cheerkar nikalta hai (paida karna) - par mukhya maana subah. Ma'ariful: subah isliye ki raat aksar museebat laati hai aur din usse door karta hai. | Ibn Kathir (Ibn 'Abbas, Mujahid, Sa'id bin Jubayr, Hasan, Qatada, Jabir), Qurtubi, Tabari, Ma'ariful Qur'an |
| M2 | 113:2 | Uski banayi har makhlooq ki burai se (aam). Ma'ariful: nafa-nuksan ka asli sabab Allah hai, isliye panah usi ki. | Ibn Kathir, Qurtubi, Tabari, Ma'ariful Qur'an |
| M3 | 113:3 | *Ghasiq* = chha jaane wala andhera; *waqab* = daakhil ho/jab chha jaaye - **zyadatar: andheri raat jab chha jaaye**. Doosre qaul: chaand/tara/doobta suraj (ikhtilaaf; Tabari: ayat aam hai). Raat me (Zajjaj/Qurtubi) jaanwar, kharabi, shararat zyada. | Ibn Kathir (Mujahid, Ibn 'Abbas, Qatada, Hasan), Qurtubi, Tabari |
| M4 | 113:4 | *Naffathat* (stree-ling) = phoonkne wali; *'uqad* = girahen: jo dhaage me girah lagakar padhti aur phoonkti hain, yaani jaadu karne wali. Panah: jaadu ke nuksan se. (Jaadu kaise hota hai - detail nahi; hukm/fiqh nahi.) | Ibn Kathir (Mujahid, 'Ikrima, Hasan, Qatada, Dahhak), Tabari, Qurtubi |
| M5 | 113:5 | *Hasid* = jalne wala: dusre se neamat ke chale jaane ki chahat rakhne wala; *idha hasad* = jab wo apna hasad zaahir kare/kuch kare (Qurtubi: ghair-zaahir hasad nuksan nahi karta). Tabari: koi bhi hasid (aam). Hasad **ghibta** (waisi neamat ki chahat bina dusre ke nuksan ke) se alag. | Qurtubi, Tabari, Ibn Kathir (ruqyah-hadith) |
| M6 | poori surah | Pehle roshni ke rab ki panah, phir har burai ka zikr aam se khaas: har makhlooq -> raat -> jaadu -> hasad (Qurtubi: hasad sabse aakhir me, uski sakhti dikhane ke liye). | Qurtubi, Tabari, Ma'ariful Qur'an |

Kalam ke liye sujhaav (idea only): [MISAAL] raat ke andhere me dil ghabrana aur subah ki pehli roshni se tasalli - bina kisi vyakti ke, sirf "aap ki" nazar se (POV: khidki se bahar). [SEEKH] (1) darr/pareshani me pehla sahara Allah ki panah; (2) hasad dusre ke liye nahi, apne dil ke liye bhi bura - ghibta alag; (3) subah/roshni yaad dilati hai ki har andhere ke baad. Sab bina fiqh/hukm, bina jaadu ki vidhi ke.

## 5. Visual notes (shabdon me) + IMAGE REUSE (channels/noor-e-raah/image_library.md)
Surah ka mood: andhera -> pau phatna. Kisi insaan/Nabi/Sahabi/farishte/jaadugar ka koi roop NAHI (jaadu waali ayat par bhi: sirf girah wali dori/dhaaga ka close-up object ya andhera). Haath sirf close-up; Musafir sirf peeth se.
**Library se REUSE ke liye fit (id -> kis ayah/mood ke liye):**
- **113:1 subah/falaq:** `003/04_dawn_sand_ridge`, `002/05_dawn_horizon` (pau phatna - hero shots, alag crop/rect se 2-3 baar), `002/03_madina_dawn_houses`, `002/11_sunrays_clouds`, `003/09_morning_palm_path`, `002/04_date_palm_path` (subah ke baad).
- **113:3 gehri raat / andhera:** `003/01_one_star_night`, `002/01_night_stars_dunes`, `003/06_milkyway_desert`, `003/03_makka_valley_night`.
- **chandni chhatein (raat ki aabadi):** `002/07_moonlit_rooftops_lamp` (chaand wale qaul ke liye bhi, par sirf "kuch ne kaha" line par).
- **diya (panah/tasalli):** `002/02_lamp_on_stone`, `003/02_lamp_single_flame`; `002/12_bedtime_room_lamp` (sone se pehle - Z2), `003/08_empty_room_morning` (subah ka kamra).
- **khaali registaan / akelapan (hasad, darr):** `002/10_ring_in_desert`, `003/06_milkyway_desert`, `003/05_paths_to_oasis` (har raasta ek hi taraf - panah).
- **darwaza (band/khulna):** `002/09_lit_door` (panah ka darwaza).
- **samundar/chitij:** `003/07_sea_horizon_dusk` (doobta suraj wala qaul / shaam).
**Library me nahi (sirf agar zaroori ho to NAYI, kaaran log.md me):** girah lagi rassi/dhaage ka close-up (113:4 - koi haath/chehra nahi; object photo-look), tez hawa/toofani andhera (ghasiq ke liye, optional - warna 003/01 ya 003/03). Baaki sab library se ho sakta hai. Thumbnail wallpaper nayi (RULES: har video ki alag).
Camera/rhythm: surah chhoti hai (5 ayat), dhimi pace, har ayah par theher.

## 6. Ant: ginti aur jokhim
- **Pakka (maana hua):** P1, P2, P6, Z1-Z3, M1-M6, T1-T3 = 15; **ikhtilaaf:** P3, N1 = 2 (N2 inse bana); **pata nahi:** P4, P5 = 2; **chhodi gayi:** C1-C13.
- Licence: Arabic ALLOWED (PC milaan baaki); Hindi saral bhaavarth, koi licence shak nahi.
- **Bade jokhim:** (1) Shan-e-nuzul: jaadu ka waqia sahih hai par surah ke nuzool se rishta sahih nahi - "surah isi wajah se utri" fact ke taur par KABHI nahi, behtar hai poora waqia chhod do (N2 ka chhota rup). (2) Makki/Madani me "zyadatar" mat bolo (Ibn Kathir Madani, Qurtubi/Tanzil Makki) - dono raay. (3) Fazilat sirf riwayat ki tarah (Z2/Z3), "gaarantee/hukm" nahi; jaadu/nazar ki ruqya ka fiqh nahi. (4) Arabic strings fetch-tool ke raste aaye - byte-milaan PC par pehle. (5) Falaq ke Jahannam waale maane video me nahi (C2). (6) Nabi SAW ya Sahabi ka koi drishya nahi (jaadu waqia ho ya na ho).
- **PC par baaki:** Tanzil byte-milaan + sha dobara; sunnah.com par Bukhari 5016/5017/5748/5763 aur Muslim 814 ka number+text (eng-muslim dataset ka hadithnumber sunnah.com number nahi hai); nuzool-kramank (accepted list) aur Makki/Madani ke liye ek aur alag source (Tanzil metadata ke siva), Ma'ariful Qur'an ka poora Urdu/English matan (ayah 2-5 ki tafseer is dataset me nahi thi); Munshi ke liye 113:4 ka Amiri render.
