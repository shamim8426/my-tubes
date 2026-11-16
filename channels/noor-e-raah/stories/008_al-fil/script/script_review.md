# 008 al-fil — script review (SURAH CHECK) — Munshi, 2026-11-14
VERDICT: PASS (BLOCKER/MAJOR koi nahi; 4 MINOR free text-tweaks, TTS se pehle lagana behtar; Rs0; koi STOP condition nahi)

## Kya khola / naapa
script.md, research/dossier.md, sources.json, ucharan.md, long/images.json, long/render.json, 007 render.json (dhaancha), series_queue.json, channel RULES (1, 1a, 1c, 1d, 2, 2a), tools/name_guard.py. Tafseer ke asli text khud kholkar milaaye (spa5k tafsir_api raw JSON): Ibn Kathir EN 105, Ma'ariful EN 105, Qurtubi AR 105. Code se: Arabic join, UCHARAN match, line numbering, shabd ginti, vaakya ginti, images.json ki 12 base files exist.

## Verified (PASS)
- RULES 1d: sirf USTAAD; koi SAWAAL line, koi sawaal-vaakya (? ya ؟) nahi; koi [NOTE], koi tilawat-disclaimer, koi intro-note nahi. Line 15/25 "क्या तुमने नहीं देखा / क्या उसने..." Quran ke shabdon ka bhaavarth hai, darshak se sawaal nahi (theek).
- Arabic (code se): 11 ARABIC lines. AYAH 1 == 105:1..105:5 (sources.json ayat[].text) space se joda = True. Jumla blocks: 105:1, 105:2, 105:3, 105:4, 105:5 me har ek ke 2 chunk join karne par poori ayat se barabar = 5/5 True.
- UCHARAN: 10 lines (14, 19, 24, 29, 34, 39, 44, 49, 54, 59), har ek ucharan.md ke Devanagari column se akshar-akshar barabar (10/10 True), har ek apne BHAAVARTH (15..60) se pehle. Plain reading, tilawat jaisa kuch nahi.
- Line numbering 1..67 file ke kram me, koi gap nahi (code se); aakhri bolti line 66, aakhri cue 67 (sabse bade number). render.json end_from 66 sahi; cards (line 4, 63-65) script ke SCREEN notes se milte hain; format 007 jaisa (tempo 1.11, tagline, series).
- Har jumla me 2-3 chhote vaakya (BHAAVARTH + MATLAB): jumla 1 = 3, baaki 2-3 (jumla 3 ka BHAAVARTH adhoora vaakya hai jo agle jumla me poora hota hai, neeche MINOR 3).
- Dropped items sach me spoken text me nahi (grep): P3 nuzool kramank, P4 "अलम तरा" doosra naam (sirf ucharan line me pehle shabd ke taur par, naam ke taur par nahi), CE saal 570/571, lashkar ki ginti (60,000), Abdul-Muttalib/N4 (poori drop), Nabi ﷺ ki paidaish, Mahmud naam, Hudaybiyyah, parindon ka rang, patthar ginti, gore vivaran, fazilat. Kewal HEADER/CHECKS ke "DROP" notes me hain (spoken nahi).
- Koi "chhoda gaya" (C1-C10) baat nahi; koi firqa/fiqh/ilzam nahi; "guarantee/sawab/hifazat ki dua" jaise shabd nahi. Seekh (63-65) dossier M6 (IK/Qurtubi/Ma'ariful ka core) se.
- Images/RULES 2, 2a, 1d: images.json 21 entries, 12 base files sab reuse aur maujood, 0 nayi, Rs0. Koi Nabi/Sahabi/farishta/insaan/haathi/lashkar/parinda image me nahi (10_ring_in_desert me sirf ek chhoti dhaatu ki anguthi, 09_lit_door band darwaza, 02 diya). Same (image, rect) dobara nahi; pehle ~60 s me koi clip ~10 s se lambi nahi.
- Tarjuma: line 15, 20, 25, 30, 35, 40, 45, 50, 55, 60 teeno tarjumon (Suhel Farooq Khan, Muhammad Farooq Khan, Mahmud al-Hasan) se matlab me milte hain; "ऐ रसूल" aur "खरन्जों की कंकरियाँ" nahi liye; kisi ek ki ibaarat copy nahi.
- Music/audio: Soaring + River Flute, CC BY 4.0, credit SOURCES me (007 jaisa); ~19 LU, har Arabic par ek swoosh (RULES 1c). Koi tilawat nahi.
- name_guard.py: OK.
- Length estimate: 393 shabd (367 USTAAD + 26 UCHARAN; meri ginti header se match). 007 final (3:28.8, 434 shabd, 7 blocks) se: voice ~0.42 s/shabd ~ 165 s + 11 blocks ke overhead ~40 s = ~3:25-3:35; band 3:11-3:51 me, 4:00 se neeche. Pehla poora Arabic ~0:17 (line 5, hook+parichay ke baad) theek. Plausible.

## Shan-e-nuzul / parichay sheet (har baat alag, source khud khola)
| Line | Baat | Source | Grade |
|---|---|---|---|
| 3, 9 | Abraha (Yemen ka hakim) ne hathi ke saath lashkar le kar Ka'ba dhaane ka irada kiya / nikla | dossier N3; Ibn Kathir EN 105 (Abrahah, elephant, church Al-Qullays, march), Ma'ariful EN 105, Tabari, Qurtubi | maana hua. Girja/jalane wale ka zikr nahi (theek) |
| 4 | Naam "अल-फ़ील" pehli ayat ke "अस्हाबिल फ़ील" se; hathi = फ़ील | dossier P1; Qurtubi 105 | maana hua |
| 4 | Makki surah | dossier P2; Qurtubi AR 105 khola: "وَهِيَ مَكِّيَّةٌ بِإِجْمَاعٍ" (ijma'); quran.com, Alim | maana hua, koi madani raay nahi mili |
| 3, 65 | Allah apne Ghar ki hifazat karta hai; chaal bekaar | dossier P5; IK EN ("one of the favors Allah did for the Quraysh... saved them from the People of the Elephant who tried to tear down the Ka'bah"), Ma'ariful, Qurtubi | maana hua |
| 6 | Surah ka bahav: yaad dilana, chaal bekaar, parinde, kankar, bhoosa | dossier P6; Tabari, IK EN | maana hua |
| 8 | Is surah ka alag sabab-e-nuzul nahi; surah khud jaane-maane waqie ki taraf ishara | dossier N1; IK EN 105 (koi alag sabab nahi, surah us waqie ka zikr), Tabari/Qurtubi (waqia detail me, sabab ke taur par nahi) | maana hua (negative baat, saaf shabdon me, "ek hi source" se nahi) |
| 10 | Hathi aage badhne se ruk gaya aur baith gaya | dossier N5; IK EN 105 ("it knelt... refused"), Ma'ariful EN 105 ("knelt and sat down... efforts in vain", Makka ki taraf mudne par baitha) , Tabari, Qurtubi | maana hua. Mahmud naam spoken me nahi |
| 11 | Ye waqia usi saal jise Arab "आमुल फ़ील" kehte; koi ankda nahi | dossier N2; Qurtubi AR khola: "عام الفيل" (Muqatil/Kalbi ka fasle ka ikhtilaaf video me nahi), IK EN, Ma'ariful ("this event took place in the very year Prophet was born" popular view) | maana hua (saal ka naam). MINOR 2 dekho |
| 12 | Nabi ﷺ ne ye ehsaan Quraysh ko yaad dilaya | dossier N1/M7; IK EN 105 khola: "Ibn Ishaq said that when Allah sent Muhammad with prophethood, among the things he used to recount to the Quraysh as blessings Allah had favored them with was His defending them from the Abyssinians" + IK ka apna kathan "one of the favors Allah did for the Quraysh" | maana hua; riwayat Ibn Ishaq ki hai, IK ne nakal ki. MINOR 1 dekho |
| 17 | "अलम तरा" = waqia itna mash'hoor ki maano sab ne dekha; "रब" = Allah | dossier M1/K1; Ma'ariful, IK EN, Tabari | maana hua |
| 22 | Ashab-il-feel = Abraha ka lashkar jo Yemen se aaya | dossier K2; Tabari, IK, Qurtubi, Ma'ariful | maana hua |
| 27 | Kayd = chaal/saazish | dossier K3/M2; Tabari, IK | maana hua |
| 32 | Tadleel = bekaar/galat raaste par | dossier K4; Tabari, IK, Qurtubi | maana hua |
| 37 | Allah ne unpar parinde bheje | dossier K5/M3; Tabari, IK, Qurtubi | maana hua |
| 42 | Ababeel = jhund ke jhund, ek ke peeche ek | dossier K6; Tabari, IK (Ibn 'Abbas, Hasan, Qatada, Mujahid) | maana hua |
| 47 | Parinde unpar kankar phenkte the | dossier K7/M4; Tabari, IK, Ma'ariful | maana hua |
| 52 | Sijjeel = pakki mitti ka kankar-patthar | dossier K8; Tabari, IK | maana hua |
| 57 | Phir Allah ne unhe ek anjaam par pahuncha diya | dossier K9/M5; Tabari, IK | maana hua |
| 62 | Asf ma'kool = khaaya hua bhoosa, poori barbaadi | dossier K10; IK EN khola (Sa'id bin Jubayr, Hasan, Ibn 'Abbas: straw/shell of grain; "Allah destroyed them, annihilated them"), Tabari | maana hua |
| 63-65 | Seekh: taaqat Allah ke saamne kuch nahi; chaal faisla nahi rok sakti; Allah apne Ghar ki hifazat karta hai | dossier M6/K11; IK, Qurtubi, Ma'ariful | maana hua (seekh) |
Koi sabab-e-nuzul gadha nahi gaya; koi chhoda-gaya (C1-C10) baat nahi; koi ek-source baat (P3, P4, C4 60,000, N4) spoken nahi.

## MINOR (free text-tweak, TTS se pehle lagao; R2 ke baad carry_over me bhi chalega)
1. Line 12: "इब्ने कसीर के मुताबिक़ नबी ﷺ ने..." — ye baat asal me Ibn Ishaq ki riwayat hai jo Ibn Kathir ne di (single chain). Behtar: "इब्ने कसीर, इब्ने इस्हाक़ की रिवायत लेकर, बताते हैं कि नबी सल्लल्लाहु अलैहि वसल्लम ने ये एहसान क़ुरैश को याद दिलाया।" Ya IK ka apna kathan lo: "इब्ने कसीर के मुताबिक़ ये क़ुरैश पर अल्लाह के एहसानों में से एक है" (M7, 2+ source).
2. Line 11: "ज़्यादातर रिवायतों के मुताबिक़" ka hedge galat taur par bahas ka ehsaas deta hai (bahas waqia aur paidaish ke fasle par hai, jo video me nahi). Saaf: "ये वाक़िया उस साल हुआ, जिसे अरब 'आमुल फ़ील', यानी हाथी का साल, कहते थे।" (Qurtubi ka "عام الفيل" naam).
3. Line 25 (jumla 3 BHAAVARTH) "क्या उसने उनकी चाल को" bina viram ke adhoora vaakya hai; TTS me awaaz ladakhdaa sakti hai. Agle block ka "दूसरा हिस्सा: बेकार नहीं कर दिया।" iska poora karta hai; theek hai, par Whisper check me "को" ke baad ka thehrav dhyan se dekho (same for 35, 45, 55 jahan vaakya agle block me chalta hai).
4. sources.json ayat[0].words = 8 hai, Arabic me 7 shabd hain (5+2 chunks). Sirf metadata, video par asar nahi; PC par sha256 ke saath theek karo.

## PC par abhi baaki (script ko roke nahi)
sha256 (sources.json me null) aur Amiri zoom (105:1 `بِأَصْحَٰبِ`, `رَبُّكَ`; 105:2 `فِى`; 105:4 `مِّن`, `سِجِّيلٍ`; 105:5 `مَّأْكُولٍۭ`, `كَعَصْفٍ`); Tanzil licence page dobara kholna; ucharan.md ke 4 open points (ज़ vs द in तज़्लील, तैरन, कैफ़ा, jumla-block vowels) — script ne ucharan.md ka tay roop liya, MAJOR nahi. Voice Charon: DAILY_LONG.md abhi purana Algieba likha hai — runbook update karna builder ka kaam.

## Agla kadam
Script PASS: TTS ke liye aage badho (auto mode, RULES 1d/15). Upar ke MINOR 1-3 free text me turant laga sakte ho (TTS se pehle sasta). Asli TTS length 3:55 paar kare to pehle line 11, 12, 6 (aakhri hissa) trim.
