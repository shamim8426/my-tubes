# Dossier - Ayatul Kursi = Al-Baqarah 2:255 (002_ayatul-kursi) | Khoji MODE 3

> **STATUS:** Arabic text = ALLOWED (Tanzil Uthmani, CC BY 3.0; ek baar tanzil.net se PC par milaan baaki - section 1.1).
> Hindi = SARAL BHAAVARTH (001 ka faisla, translation_options.md). **Koi LICENCE SHAK nahi** (kisi tarjume ka text copy nahi hota).
> **"Not opened" (is container se khule nahi):** sunnah.com, quran.com, tanzil.net, islamweb, islamqa, altafsir, archive.org.
> Hadith/tafseer text GitHub ke public datasets se padha (section 6) - har jagah "PC par confirm karo" likha hai.

- Bana: 2026-10-29, Khoji. Kharcha Rs0. Koi audio/tilawat nahi. Ek line: Quran ki sabse azeem batayi gayi aayat - Allah ki
  zindagi, nigehbani, malkiyat, ijaazat wali sifarish, ilm, azmat aur buland martabe ki 10 baatein.

## 1. Text sources

### 1.1 Arabic 2:255 (Tanzil Uthmani) - ALLOWED
- Licence/attribution: 001 dossier section 1.1 jaisa (CC BY 3.0, verbatim, "Tanzil Project" + link tanzil.net, notice description me).
- Snapshot: `risan/quran-json` (GitHub) file `data/tanzil/uthmani.json`; uska source URL
  `https://tanzil.net/pub/download/index.php?quranType=uthmani&outType=txt-2&agree=true` (pause-marks option OFF);
  file sha256 `adaebb377c60eba1bab6ef652959c7a0b4ccb4d0ca42145945c14ecdbeb4b761` (repo ke data/meta/sources.json se, humne khud
  `sha256sum` se match kiya); repo revision `e20bba6abe2cc37f77f5aae5266f39cc55b9ca77`. Isi snapshot se Al-Fatiha 7/7 byte-for-byte match.
- Ayah string (408 code points, 50 shabd, sha256 of UTF-8 string `cdf04bda6db38541c5d84d515be92968fc30e60051165a9aa14da016470ca4fe`):

> ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلْحَىُّ ٱلْقَيُّومُ لَا تَأْخُذُهُۥ سِنَةٌ وَلَا نَوْمٌ لَّهُۥ مَا فِى ٱلسَّمَٰوَٰتِ وَمَا فِى ٱلْأَرْضِ مَن ذَا ٱلَّذِى يَشْفَعُ عِندَهُۥٓ إِلَّا بِإِذْنِهِۦ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ وَلَا يُحِيطُونَ بِشَىْءٍ مِّنْ عِلْمِهِۦٓ إِلَّا بِمَا شَآءَ وَسِعَ كُرْسِيُّهُ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضَ وَلَا يَـُٔودُهُۥ حِفْظُهُمَا وَهُوَ ٱلْعَلِىُّ ٱلْعَظِيمُ

- Shaabd ginti 50 = Qurtubi ("khamsun kalima") se mel khati hai. Doosra, alag source (KFGQPC Hafs, `quranpedia qpc-hafs`):
  harf-dar skeleton **barabar** (sirf alamat/wasl ka farq) - yaani rasm ek hi.
- **Ehtiyat:** (a) NFC/NFKC se text badalta hai - kabhi normalise mat karo. (b) `يَـُٔودُهُۥ` me tatweel (U+0640) + hamza-above (U+0654):
  libass/Amiri me render check karo (Munshi zoom). (c) **PC par ek baar tanzil.net/download ki `quran-uthmani` file se is ek ayah ka byte-milaan** (BOM hatao).

### 1.2 Hindi
- 001 ka faisla lagu: **SARAL BHAAVARTH**, on-screen "सरल भावार्थ - माने हुए तर्जुमों के आधार पर". 3 tarjume: al-Umari (QuranEnc, Hindi),
  Shaikh-ul-Hind Mahmud Hasan (Urdu, PD), Tanzil `hi.hindi` (Suhel Farooq Khan/Saifur Rahman Nadwi). Cross-check: Tanzil `hi.farooq`,
  Maududi (Urdu), Taqi Usmani (Urdu), Sahih Intl (EN). Poora text + key-word table: `translation_options.md`.

## 2. Parichay + Shan-e-Nuzul

Grade: **maana hua** / **ikhtilaaf** (zyadatar + doosri raay) / **chhoda gaya** (kamzor/vivaadit/channel-niyam; VIDEO ME KABHI NAHI).

| ID | Baat | Source(s) | Grade |
|---|---|---|---|
| P1 | Ayah **Surah Al-Baqarah (Quran ki 2sri surah) 2:255** - Kufi/Madinah ginti me 255vi ayah; surah ki kul ayat **286** (Ibn Kathir "counters" 287 bhi kehte hain - ginti ka farq, video me 286). Parah 3 (juz 3 2:253 se shuru). | Tanzil chapters.json (id 2, 286, medinan); Tanzil juz index; Ibn Kathir 2:1 (AR: "ayatuha 287" ginti wale) | maana hua (ginti: ikhtilaaf) |
| P2 | **Al-Baqarah poori Madani** ("bila khilaf") - Madina ki shuruaati surahon me. Isliye 2:255 Madani. | Ibn Kathir 2:1 (EN "no disagreement ... entirety in Al-Madinah"; AR "madaniyya bila khilaf"); Tanzil chapters.json type=medinan | maana hua |
| P3 | **Naam "Ayat al-Kursi"** ayah ke lafz "Kursi" se; Nabi ﷺ ke zamane se yahi naam - hadith ke alfaaz me "آية الكرسي". "Sayyid ul-ayat" jaisa naam kamzor hadith par tiki hai (C5), isliye video me sirf "Ayat al-Kursi". | Bukhari 2311/3275/5010 (alfaaz "آية الكرسي"); Qurtubi 2:255 ("hadhihi ayat al-Kursi"); Ibn Kathir 2:255 | maana hua |
| P4 | Ayah ek hai, 10 mukammal jumle (Ibn Kathir "Ten Complete Arabic Sentences"; Ma'ariful Qur'an "ten sentences"). | Ibn Kathir 2:255 (EN+AR); Ma'ariful Qur'an 2:255; Jalalayn (same flow) | maana hua |
| P5 | Sandarbh: pichli ayah 2:254 (kharch karo us din se pehle jab na kharid-farokht, na dosti, na sifarish) aur agli 2:256 ("deen me zabardasti nahi"). 254 me "shafa'at" ka zikr aur 255 me "ijaazat ke bina sifarish nahi" - link ka koi tafseer-source mila nahi. | Tanzil Arabic 2:254; link = Khoji ka anumaan | anumaan (video me NA bolo) |
| N1 | **2:255 ka koi pukhta (sahih/muttasil) khaas shan-e-nuzul nahi mila.** Wahidi "Asbab al-Nuzul" (altafsir EN) ke dataset me 2:256 ki entry hai, **2:255 ki nahi**. Ibn Kathir, Ma'ariful Qur'an, Jalalayn, Baghawi (datasets) me bhi koi nuzool-waqiya nahi. | Wahidi dataset (`en-asbab-al-nuzul-by-al-wahidi`: 2:256 hai, 2:255 nahi); IK, MQ, JAL, Baghawi 2:255; WikiShia (infobox cause "-", web search; not opened) | maana hua ("koi pakka nahi") |
| N2 | Video me kehna: "आयतुल कुर्सी के उतरने का कोई मज़बूत, ख़ास वाक़िया रिवायतों में नहीं मिलता; इतना तय है कि ये सूरह-बक़रा का हिस्सा है जो मदीना में उतरी।" | N1 + P2 | maana hua |
| N3 | Sooni baat: "raat ko utri, Zayd ko bulakar likhwayi" (Qurtubi 2:255, bina sanad). | Qurtubi 2:255 | **chhoda** (sanad nahi; Nabi/Sahabi ka drishya bhi maangti hai) |

### 2a. Chhoda gaya (VIDEO ME KABHI NAHI)
| ID | Riwayat / baat | Kyun chhodi |
|---|---|---|
| C1 | Ibn Abi Hatim [2580] (Ibn Abbas se): Bani Israil ne poochha "kya Rabb sota hai?" - Musa AS ko do shishe, neend se toote - "isi par Ayat al-Kursi utri". | Isra'ili-tarz ki kahani; Qurtubi isi tarah ki Musa-shishe riwayat ke baare me: "ye hadith sahih nahi, Bayhaqi samet kai ne kamzor kaha"; ek Nabi ka drishya bhi. |
| C2 | Rabi' bin Anas (Ibn Abi Hatim [2604], Tabari 5793): "wasi'a kursiyyuhu" utri to sahaba ne poochha "Arsh kaisa?" to 39:67 utri. | Taabi'i ka mursal qaul; doosri ayah ke baare me; sahaba ka drishya. |
| C3 | Muhammad ibn al-Hanafiyya (Qurtubi): ayah utri to duniya ke sab but gir gaye, taaj gir gaye, shaitan bhaage... | Bina sanad, mursal, ghaib ka daava. |
| C4 | Tabari (apna ta'wil): "min dha alladhi yashfa'u" isliye kaha ki mushrik kehte the "ham but sirf nazdeeki ke liye pujte hain." | Tabari ki apni vyakhya, riwayat/sanad nahi - shan-e-nuzul na bolo. (Matlab-wali baat M5 alag, maana hua.) |
| C5 | Tirmidhi 2878 "Baqarah ki kohan, usme sayyid-ul-ayat" | Daif: Shakir, Albani, Bashar Awad Ma'ruf, Zubair Ali Za'i (dataset grades, sunnah.com se). |
| C6 | Tirmidhi 2879 (Ha-Mim al-Mu'min + Ayat al-Kursi subah/sham = hifazat) | Daif: Shakir, Albani, Zubair (dataset grades); Tirmidhi: "gharib". |
| C7 | Tirmidhi 2880 (Abu Ayyub, "ghoul" aur ghar me Ayat al-Kursi) | **Ikhtilaaf**: Shakir/Albani sahih, Zubair daif; Ibn Kathir: Tirmidhi "hasan gharib". Jinn/dar wala content bhi. |
| C8 | "Ayat al-Kursi + Ism al-A'zam" (Asma bint Yazid; Abu Dawud, Tirmidhi, Ibn Majah) | Ibn Kathir: Tirmidhi "hasan sahih"; magar ism-e-azam ki pehchaan ka masla - hamare paas aayat-wise grade check nahi, video ke dayre se bahar. |
| C9 | "Is ayah ki zubaan aur do honth hain, Arsh ke paaye ke paas tasbih karti hai" (Ahmad via IK; Muslim me ye hissa nahi) | Ahmad ki sanad ka darja confirm nahi; Muslim ne ye hissa nahi liya (IK khud likhta hai). |
| C10 | Qurtubi/Ibn Atiyya: "50 shabd, har shabd me 50 barakat", "ek tihaai Quran", "Ayat al-Kursi Torah me 'Wali-ullah'" (Nawf al-Bakali) | Bina pakke darje/sanad ke. |
| C11 | Musa AS ko Anas/Ubayy ke zariye hadith-e-qudsi "har namaz ke baad padhne par nabiyon ka sawab" (Qurtubi via al-Hakim at-Tirmidhi) | Darja nahi, Qurtubi ne sanad nahi dikhayi; fazilat-sirf-sahih niyam. |
| C12 | "Kursi ek moti hai, qalam ek moti" (Ali, Ibn Asakir via Qurtubi) | Sanad/darja nahi. |
| C13 | Umar RA aur jinn ki kushti, Ibn Mas'ud wali sahabi-jinn kushti (Darimi/Abu Nu'aym via Qurtubi) | Jinn-wali kahaniyan (darr; Sahabi ka drishya bhi); Qurtubi ne ek ko "sahih" kaha par sanad/doosra grader hamne nahi dekha. |
| C14 | Ali RA wali "har namaz ke baad ... sirf siddiq ya abid hi niyamit padhta hai", Anas wali | Kamzor (Nuhshal b. Sa'id "matruk" aadi - web-search summary, not opened). Dekho FZ-C. |
| C15 | Tirmidhi 2884 (Ibn Mas'ud: "Ayat al-Kursi se azeem koi cheez nahi ban'i") | Sirf Zubair Ali Za'i ka "isnad sahih" (ek grader, mauquf) - 2 grader nahi. |

## 3. Aayat-dar-aayat: 10 units (Ibn Kathir + Ma'ariful Qur'an ke 10 jumle) - saral bhaavarth + tafseer-point
Key-word table (kaun tarjuma kya kehta hai): `translation_options.md`. "IK" = Ibn Kathir, "MQ" = Ma'ariful Qur'an, "QT" = Qurtubi, "TB" = Tabari.
Bhaavarth hamare shabdon me hai (draft); Munshi har line teeno tarjumon se milaye.

| U | Arabic (Tanzil, tukda) | Saral bhaavarth (draft) | Tafseer-point (2+ sehmat) | Grade |
|---|---|---|---|---|
| U1 | ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ | अल्लाह - उसके सिवा कोई इबादत के लायक़ नहीं। | IK: Allah hi sab makhlooq ka akela Rabb; MQ: "Allah" zaat ka naam, usi ke siwa kuch ibadat ke laayak nahi. | maana hua |
| U2 | ٱلْحَىُّ ٱلْقَيُّومُ | वो हमेशा ज़िंदा है और सबको थामे-सँभाले हुए है; सब उसके सहारे हैं, वो किसी के सहारे नहीं। | IK: "never dies; sustains all; creation needs Him, He needs none"; MQ: Hayy = hamesha zinda, Qayyum = khud qaim aur sabko qaim rakhne wala; QT: Qatadah "qa'im bi-tadbir"; Qayyum = "kisi par munhasir nahi". | maana hua |
| U3 | لَا تَأْخُذُهُۥ سِنَةٌ وَلَا نَوْمٌ | न उसे ऊँघ आती है, न नींद। | IK: kami/ghaflat/jahalat kabhi nahi; "sinah" halka ghunoon, "nawm" gehri neend; MQ: sinah = neend ki shuruaati ghunood; QT: "sinah = nu'as" (sab ke nazdeek). (Musa-shishe wali kahani chhodi: C1.) | maana hua |
| U4 | لَّهُۥ مَا فِى ٱلسَّمَٰوَٰتِ وَمَا فِى ٱلْأَرْضِ | आसमानों और ज़मीन में जो कुछ है, सब उसी का है। | IK: sab uske banday, uski saltanat; MQ: "lam" malkiyat ka, wahi ikhtiyar wala. | maana hua |
| U5 | مَن ذَا ٱلَّذِى يَشْفَعُ عِندَهُۥٓ إِلَّا بِإِذْنِهِۦ | कौन है जो उसकी इजाज़त के बिना उसके सामने किसी की सिफ़ारिश कर सके? | IK: koi dam nahi maar sakta, 53:26/21:28 jaise; MQ: koi bhi sifarish bina ijaazat nahi - jise ijaazat mile wo bolega; QT: ijaazat sirf unko jinko Allah izzat de, aur wo bhi jis se wo razi ho. (Video me kisi khaas shakhs ki sifarish ka zikr/behes nahi.) | maana hua |
| U6 | يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ | वो उनके आगे-पीछे, सामने की और छुपी - सब बातें जानता है। | IK: maazi, haal, mustaqbil sab; MQ: dono maani (aage-peeche ke halat / zahir-chhupa) jaiz; QT: Mujahid "aage = duniya, peeche = aakhirat". | maana hua (dono maani jaiz) |
| U7 | وَلَا يُحِيطُونَ بِشَىْءٍ مِّنْ عِلْمِهِۦٓ إِلَّا بِمَا شَآءَ | उसके इल्म का कोई हिस्सा कोई घेर नहीं सकता - सिर्फ़ उतना जितना वो ख़ुद बता दे। | IK: jo Allah bataye utna hi, 20:110; MQ: poora ihata sirf Allah ka; QT: "ilm yahan ma'lum ke maani me". | maana hua |
| U8 | وَسِعَ كُرْسِيُّهُ ٱلسَّمَٰوَٰتِ وَٱلْأَرْضَ | उसकी कुर्सी आसमानों और ज़मीन को समेटे हुए है। (kursi ki hakikat: section 4) | IK, MQ, QT, TB: azmat; Kursi pe 4 qaul (K1-K4). Allah ka baithna/jagah-mohtaj hona nahi (MQ, QT-Bayhaqi, IK-Salaf). | maana hua (azmat) / ikhtilaaf (hakikat) |
| U9 | وَلَا يَـُٔودُهُۥ حِفْظُهُمَا | और उन दोनों की निगहबानी उसे ज़रा भी भारी/थकाने वाली नहीं। | IK: bojh nahi, aasan; MQ: poori qudrat se kuch mushkil nahi; QT: Ibn Abbas, Hasan, Qatadah "yuthqiluhu"; TB 5799-5809 (Ibn Abbas, Qatadah, Mujahid...). | maana hua |
| U10 | وَهُوَ ٱلْعَلِىُّ ٱلْعَظِيمُ | और वही सबसे बुलंद, सबसे अज़ीम है। | IK: 13:9 "al-Kabir al-Muta'al" jaisa; QT: "ulu-ul-qadr wal-manzila" (martabe ki bulandi), jagah ki bulandi ke maani me nahi; MQ: izzat, quwwat, bartari usi ki. | maana hua |

## 4. Kursi ka matlab (U8) - seedhe lafz me kehne se pehle
| ID | Raay | Source | Grade |
|---|---|---|---|
| K1 | Kursi = Allah ka **ilm** (Ibn Abbas, Sa'id ibn Jubayr se). Tabari isi ko Quran ke zaahir se mutabiq maanta hai ("wa la yauduhu hifzuhuma" ki daleel); Qurtubi likhta hai Tabari ne ise tarjeeh di. | TB 5787-5788 + Tabari ka nateeja; QT 2:255 | ikhtilaaf (ek maashhoor raay) |
| K2 | Kursi = **Arsh ke saamne ek azeem makhlooq** ("padon ki jagah" kaha gaya: Ibn Abbas mauquf - Hakim "sahih"; Abu Musa al-Ash'ari - Tabari ki sanad ke editor: munqati'). Qurtubi: "baaki riwayatein Ibn Abbas wagairah ki isi ki taraf ishara karti hain". | IK 2:255 (Waki' via Ibn Abbas; Hakim); QT 2:255; TB 5789-5792; Ibn Abi Hatim [2601] | ikhtilaaf (zyadatar riwayat is taraf: QT) |
| K3 | **Azmat ki misaal:** saat aasman us Kursi me aise jaise veeran maidan me padi ek anguthi/halqa; Arsh Kursi se usi tarah bada. (Abu Dharr RA, marfu') | QT 2:255 (Ajurri; Ibn Hibban "Sahih"; Bayhaqi "sahih" kaha); Ma'ariful Qur'an 2:255 (Abu Dharr, Ibn Kathir se); IK (Dahhak via Ibn Abbas, mauquf); Albani Silsila Sahiha 109 (web search: Islamland/IslamQA - not opened) | maana hua (anguthi wali misaal) |
| K4 | Hasan al-Basri: Kursi = Arsh hi. | QT (Ibn Atiyya: "ye pasandeeda nahi"), TB 5795 | chhoda (na-pasand) |
| K5 | Kursi koi "taqht jis par Allah baithe" nahi - Allah baithne/khade hone aur jagah se paak. Salaf ka tareeqa: sifat ko jaise aayi waise maano, makhlooq se tashbeeh na do. | MQ 2:255 ("above sitting and standing and all spatial location"); QT ("al-'Ali = ulu al-qadr, not al-makan"; Bayhaqi: "laisa fihi ithbat al-makan"); IK (last para) | maana hua |
| K6 | Kuch tarjume lafz "kursi" ki jagah "prabhuta/hukumat" likhte hain (hi.farooq "कुर्सी (प्रभुता)", Maududi "hukumat"); al-Umari/Mahmud Hasan/hi.hindi "kursi" hi. | translation_options.md | ikhtilaaf - video me "कुर्सी" bolo + K2/K3 ka core |
**Video ke liye surakshit line:** "कुर्सी की हक़ीक़त पर उलमा के कई क़ौल हैं - इब्ने अब्बास रज़ि. का एक क़ौल अल्लाह का इल्म; ज़्यादातर रिवायतों के मुताबिक़ अर्श के सामने एक अज़ीम मख़लूक़। नबी ﷺ ने बताया कि सातों आसमान उसके मुक़ाबले वीराने में पड़े छल्ले जैसे हैं। हर क़ौल का सार एक: अल्लाह की अज़मत इतनी कि आसमान-ज़मीन उसके सामने बहुत छोटे, और वो किसी जगह या तख़्त का मोहताज नहीं।" (K3 wala "नबी ﷺ ने बताया" = Abu Dharr hadith, maana hua.)

## 5. Fazilat - sirf SAHIH (channel brief) 
| ID | Daava | Source (kitab + number) | Grade | Video me? |
|---|---|---|---|---|
| FZ-A | **Quran ki sabse azeem (أعظم) aayat.** Nabi ﷺ: "ऐ अबुल-मुन्ज़िर! तुम्हारे पास अल्लाह की किताब की कौन-सी आयत सबसे अज़ीम है?" Ubayy bin Ka'b ne 2:255 padhi; Nabi ﷺ ne seena thapthapa kar kaha "तुम्हें इल्म मुबारक, अबुल-मुन्ज़िर!" | **Sahih Muslim 810** (Book 6/Hadith 313 ka dataset ref; Abd al-Baqi no. 810). Arabic: "يَا أَبَا الْمُنْذِرِ أَتَدْرِي أَىُّ آيَةٍ مِنْ كِتَابِ اللَّهِ مَعَكَ أَعْظَمُ"... "اللَّهُ لاَ إِلَهَ إِلاَّ هُوَ الْحَىُّ الْقَيُّومُ" ... "وَاللَّهِ لِيَهْنِكَ الْعِلْمُ أَبَا الْمُنْذِرِ". Samarthan: Ahmad (IK, MQ: Ubayy aur Abu Dharr), Qurtubi ("rawa al-a'imma"). | **maana hua** (Muslim) | **HAAN** |
| FZ-B | **Sote waqt** padhne par Allah ki taraf se ek nigehbaan saath rehta hai aur subah tak shaitan qareeb nahi aata. | **Sahih al-Bukhari 2311** (Wakalah; poori kahani Abu Hurayrah), **3275** (Bad' al-khalq), **5010** (Fada'il al-Qur'an) - teeno me wahi jumla: "إِذَا أَوَيْتَ إِلَى فِرَاشِكَ فَاقْرَأْ آيَةَ الْكُرْسِيِّ ... لَنْ يَزَالَ عَلَيْكَ مِنَ اللَّهِ حَافِظٌ وَلاَ يَقْرَبَنَّكَ شَيْطَانٌ حَتَّى تُصْبِحَ" (2311). Nabi ﷺ: "सच कहा, जबकि वो बड़ा झूठा है - वो शैतान था." Samarthan: Nasa'i 'Amal al-Yawm wa al-Layla (IK ne likha), IK, Qurtubi (Bukhari ka hawala). | **maana hua** (Sahih Bukhari). Nuance: Bukhari ne sanad "وقال عثمان بن الهيثم" se shuru ki (ta'liq form; Uthman unke seedhe ustaad). Fath al-Bari me mausool hone ka bayaan **PC par confirm** (is container me nahi khula). | **HAAN**, shabd: "बुख़ारी की हदीस में है" |
| FZ-C | Har farz namaz ke baad padhne par "jannat me jaane se sirf maut roke hui hai" (Abu Umamah). | Nasa'i, 'Amal al-Yawm wa al-Layla 100 / Sunan al-Kubra 9848; Tabarani Mu'jam al-Kabir 7532 (web-search secondary: Mufti WP Malaysia, Darul Ifta Birmingham - not opened). Ma'ariful Qur'an & Qurtubi bina darja ke naql karte hain. | **ikhtilaaf**: Ibn Hibban aur Albani ne sahih kaha (islamweb fatwa, secondary); Ibn al-Jawzi ne mawdu' (kai ne ise 'shiddat' kaha); sanad ka mukhya sawal Muhammad bin Himyar; Ali/Anas wali sanadein kamzor. Hamara channel niyam: sirf sahih. | **NAHI** (chhoda; user chahe to alag faisla) |
| FZ-D | "Baqarah ki sayyid-ul-ayat", "ism-e-azam", "Arsh ke paaye ke paas tasbih", "ek tihaai Quran", subah-shaam hifazat (Tirmidhi 2879), ghoul (Tirmidhi 2880) | C5-C10 | daif / ikhtilaaf / darja nahi | NAHI |
| FZ-E | Abu Dharr RA: "Quran ki kaun si aayat sabse azeem utri?" - "Ayat al-Kursi" (Ahmad) | Qurtubi 2:255 ("Abu Dharr ki lambi hadith"), MQ, IK (Ahmad ke hawale) - **ek hi chain ka text khula nahi** | maana hua (FZ-A ka samarthan; alag daava nahi) | Sirf FZ-A ke saath, "ek aur riwayat" jaise |

**Thumbnail chip "क़ुरआन की सबसे महान आयत":** FZ-A (أعظم) isko surakshit roop se support karta hai. Behtar/surakshit shabd:
(1) "क़ुरआन की सबसे अज़ीम आयत" ya (2) "हदीस के मुताबिक़: क़ुरआन की सबसे अज़ीम आयत" (chhota label). "सबसे बड़ी" mat likho (lambai ka bhram ho sakta hai).
Dhyan: hadith me "अज़ीम" ka matlab martaba/azmat; doosri ayaton ko kam ka daava nahi - "sirf ye" jaisa lagne wala kuch na likho.

## 6. Galat fehmiyan / jo MAT kaho (Kalam ke liye)
- "Padhte hi har musibat ka pakka ilaaj / jaadu ki hifazat / ta'wiz": **nahi**. Hadith: Allah ki taraf se hafiz ka zikr - bharosa aur dua, natija Allah ke haath. "Guarantee", "100%", "kabhi nuksaan nahi" jaise shabd BLOCKER.
- "Kursi koi taqht/kursi jis par Allah baithe hai": **nahi** (K5). Kursi ko insaani furniture jaisa na dikhao/bolo.
- "Kursi = Arsh": Hasan ki raay, na-pasand (K4).
- "Sabse lambi ayah": galat; wording FZ-A hi.
- Shaitan/jinn ke darr wali kahaniyan, "bhoot bhagane" jaisi baat: nahi (C7, C13). FZ-B bolna ho to sirf hadith ke shabd; shaitan ka koi drishya nahi.
- "Har namaz ke baad = seedhe jannat": FZ-C ikhtilaaf - nahi.
- "Sifarish" (U5): kisi khaas shakhs/waliyon ki sifarish ka behes nahi (firqa-behes). Sirf "Allah ki ijaazat ke bina nahi".
- "Hay-Qayyum ko insaan ka naam": fiqh/naam-rakhne ki baat (MQ me hai) - video me nahi.
- Ayah ko "tilawat" ki tarah suna'na: nahi (format). Arabic sirf screen par.

## 7. Video sujhaav (Kalam ke liye; Khoji ka kaam sirf sujhaav)
**Title (search-first):** `Ayatul Kursi ka Matlab Hindi Mein | Tarjuma aur Tafseer (Line by Line)` - Hindi: "आयतुल कुर्सी का मतलब हिंदी में | तर्जुमा और तफ़सीर".
**Thumbnail line (maujooda chip + hook):** chip "क़ुरआन की सबसे अज़ीम आयत"; hook "10 लाइनें - हर लाइन का आसान मतलब" (maujooda "असली मतलब" me 'doosre ghalat' ka ishara - halka clickbait; wapas dekho).
**3 hook ideas (30-40 s me wada, darr nahi, jhoota wada nahi):**
1. **Sawaal-hook (hadith):** "Nabi ﷺ ne ek sahabi se poochha: tumhare paas Allah ki kitab ki sabse azeem ayah kaun si hai? ... unhone jo ayah padhi, aaj hum roz padhte hain. Aaj uski 10 lines ka matlab, ek-ek karke." (FZ-A; koi drishya nahi - sirf jagah/diya/raat; script me "Nabi ﷺ" naam bolna theek.)
2. **"10 lines, 10 baatein":** "Roz padhte hain - magar kya pata har line Allah ke baare me kya batati hai? 'Hayy', 'Qayyum', 'Kursi' - teen shabd jo log aksar bina matlab ke padhte hain." (U2, U8)
3. **Sukoon-hook:** "'Na unghh, na neend' - jis Rabb ke baare me ye line hai, wo hamare har raat ke akelepan me bhi dekh raha hai." (U3 + FZ-B ka sirf sahih hissa; koi guarantee nahi; kisi bhi dar ka zikr nahi)
**Script must-have:** length 4-6 min; hook ka wada pehle 30-40 s me; pehli ayah (poori, Arabic screen par, tilawat nahi) ~35 s ke andar; kam se kam 1, zyada se zyada 2 SAWAAL (SAWAAL voice, 3-3.5 min ke gap ka niyam; ek ~1:30-2:00 par "Kursi kya hai?", doosra ~4:00 par "ye hamari zindagi me kya?" agar 5-6 min); 10 units order me, har unit ke baad ek line ka matlab; FZ-A (azeem) aur FZ-B (sote waqt) hi; Kursi (K1-K3, K5) surakshit line; ant me 2-3 seekh (jaise: Allah ki nigehbani ka yaqeen, sirf usi par bharosa, ayah ko samajh kar padhna).
**Script must-NOT:** FZ-C/D, C1-C15, shan-e-nuzul gadhna, koi aisi "guarantee", jinn/shaitan ki kahani ke drishya, Nabi/Sahabi/farishta ka koi aakar, firqa-behes, fiqh (kitni baar/kab padhna wajib), "tilawat", tarjume ka copy, hadith ke shabdon me apna izafa.
**Visual notes (sirf jagah/mahaul):** raat ka khula aasmaan aur taare, rait ka veeran maidan (K3 ke "halqa/anguthi" ke liye wide dune + chhota gol patthar/ring ka symbol), tel ka diya, khajoor ke ped, patthar/mitti ke ghar (7vi sadi Madina), simple takiya + bistar (sote waqt) bina insaan ke; Musafir peeth se; 'Arsh/Kursi' ka koi taqht/aadmi/farishta nahi - sirf noor/aasman. Koi pakki sadak, bijli, gumbad, minar nahi (Madina ke us daur ki masjid ka pakka khaaka nahi - "pata nahi").

## 8. Ant: ginti, licence, khatre
- **Ginti:** maana hua **21** (P1-P4, N1-N2, U1-U10, K3, K5, FZ-A, FZ-B, FZ-E; U8 ki hakikat aur P1 ki ayat-ginti ikhtilaaf alag likhi) · ikhtilaaf **4** (K1, K2, K6, FZ-C) + 2 upa-baatein (U8 hakikat, P1 ginti 286/287) · chhoda gaya **18** (C1-C15, N3, K4, FZ-D; inme C7/C8 ikhtilaaf wale) · anumaan **1** (P5).
- **Arabic:** Tanzil Uthmani, CC BY 3.0 - ALLOWED; PC par ek baar tanzil.net se is ayah ka byte-milaan baaki.
- **Hindi:** saral bhaavarth (translation_options.md); copy-risk kam; Munshi side-by-side.
- **Bade khatre / PC par confirm (is container me nahi khule):**
  1. sunnah.com / quran.com / tanzil.net / altafsir / islamweb / islamqa (blocked): hadith numbers (Muslim 810; Bukhari 2311/3275/5010) GitHub dataset `fawazahmed0/hadith-api` se mile (text sunnah.com wala); sunnah.com par khol kar number, Arabic aur English dobara dekho.
  2. Bukhari 2311/3275/5010 ki "wa qala ... Uthman" ta'liq-form aur Fath al-Bari ka bayan.
  3. Nasa'i `'Amal al-Yawm wa al-Layla` 100 / Kubra 9848 ka asli text aur ulama ka darja (Albani Sahiha 972 ka number confirm nahi) - abhi use nahi karna, par agar user kehta hai to Munshi kholega.
  4. Abu Dharr wali Kursi-hadith ka Silsila Sahiha 109 (web-search se; printed number check) - K3 ke liye Qurtubi ka "Ibn Hibban/Bayhaqi sahih" kaafi hai.
  5. Wahidi altafsir par 2:255 ki entry na hone ki pushti (dataset se).
  6. `يَـُٔودُهُۥ` ka libass/Amiri rendering.
  7. Tafseer datasets (spa5k/tafsir_api) me edition-wise text quran.com / qul.tarteel.ai se hai - muqabla ek-do jagah PC par.
