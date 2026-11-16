# 007 al-asr — script review (SURAH CHECK) — Munshi, 2026-11-13
VERDICT: FIX (chhote free text-fix; koi BLOCKER nahi, koi ASK nahi, Rs0; koi STOP condition nahi)

## Kya khola / naapa
script.md, research/dossier.md, sources.json, ucharan.md, long/images.json, long/render.json, thumbnail.json, channel RULES (1, 1a, 1c, 1d, 2, 2a), 006 script_review.md (format), series_queue.json, assets_license.csv, tools/name_guard.py. Arabic/UCHARAN/numbering code se jaanche (python).

## Verified (PASS)
- RULES 1d: sirf USTAAD; script me '?' ya '؟' nahi; koi SAWAAL line, koi intro-note, koi tilawat disclaimer nahi.
- Arabic (code se byte-compare, sources.json ayat[].text): 7 ARABIC lines, sab True. AYAH 1 = (103:1 ka text.split(' ')[4], yaani Bismillah-prefix ke baad ka akela `وَٱلْعَصْرِ`) + 103:2 + 103:3 space se joda = barabar. AYAH 2 = 103:1 (bina Bismillah), AYAH 3 = 103:2, AYAH 4-7 = 103:3 ke shabd [0:3],[3:5],[5:7],[7:9]; ye chaaron joda hua == poori 103:3 (9 shabd). Header ka Bismillah-wala note sahi hai.
- UCHARAN: 6 lines (12, 19, 25, 31, 37, 43) ucharan.md ke "Line:" aur table se akshar-akshar barabar (6/6 True); har ek apne BHAAVARTH (13, 20, 26, 32, 38, 44) se pehle.
- Line numbering 1..52 bina gap (code se); aakhri bolti line 51, aakhri cue 52, render.json end_from 51 sahi. Cards render.json (line 4, 48-50) script ke SCREEN notes se milte hain.
- Har jumla me 2-3 matlab vaakya: 103:1 = lines 15-17 (3), 103:2 = 22-23 (2), jumla 1 = 28-29, jumla 2 = 34-35, jumla 3 = 40-41 (2 line, 3 vaakya), jumla 4 = 46-47 (3 vaakya).
- Tag-to-dossier: koi C1-C6 nahi (Musaylima, Ali ki qira'at, asr ke saare maane, qasam ke fiqh, "subah jaan bechta hai", Ibn Taymiyya sab bahar; Shafi'i kathan bhi nahi, jo dossier me chhoda nahi tha par optional tha). Nuzool kramank ("13") nahi bola (P3 "pata nahi"). Koi Sahabi ka naam nahi, Tabarani ka naam/rawi nahi (line 10 "रिवायत में आता है"). Koi sawab/fazilat/guarantee shabd nahi. "नमाज़े अस्र की क़सम" tarjuma nahi liya; asr-namaz sirf ikhtilaaf ki ek line (17, bina tarjeeh).
- Bhaavarth (13, 20, 26, 32, 38, 44) T1/T2/T3 me se kisi ek ki ibaarat hu-ba-hu nahi (ek chhoti baat neeche item 2). "हुक्म/ताकीद/वसीयत" ki jagah "याद दिलाते रहे" (dossier ki salaah).
- Images: images.json ke 13 base reuse files sab maujood (D: par exists True), 0 nayi image, Rs0. Pehle 60 s me koi clip ~10 s se lambi nahi (script ka plan). Koi insaan/Nabi/Sahabi/farishta nahi, ghadi nahi.
- Music/audio: Soaring aur River Flute dono assets_license.csv me, CC BY 4.0, credit SOURCES me; ~19 LU channel RULES 1c ke mutabiq (user 2026-10-25 se; purani 20-24 line badli hui hai). Har Arabic par ek swoosh. Tempo 1.11 RULES ke mutabiq.
- name_guard.py: OK. Thumbnail.json: hook "*वक़्त* की क़सम — घाटे में इंसान" (<=4 bade shabd, koi sawaal/chehra/ghadi nahi), title search-phrase pehle, suffix "| Noor-e-Raah". Nigraan LAGU KARO (hook + pehla Arabic ~0:25, parichay ek line, 103vi/3 ayat sirf screen card): lage hain.
- Length: USTAAD 434 shabd (maine khud ginti ki, header se match) x ~0.45 = ~195 s + UCHARAN 20 shabd ~15 s + gaps ~44 s = ~254 s, yaani ~4:14 (band +-0:25). RULES 15 ka long max 4:00 is Jugnu profile ka hai; Noor ka target 3:30-4:30 hai, 006 jaisa. Asli TTS 4:30 se upar aaye to script ka fallback trim: lines 16, 35, 41.

## Shan-e-nuzul sheet (har baat alag)
| Line | Baat | Source | Grade |
|---|---|---|---|
| 8 | Is surah ke utarne ka koi khaas waqia Tabari, Ibn Kathir, Qurtubi, Ma'ariful me nahi milta | dossier N1 (sources: Tabari 103, IK EN 103, Qurtubi 103, Ma'ariful 103) | maana hua (negative). Note: dossier C1 ke mutabiq IK EN apne aaghaaz me 'Amr/Musaylima ko "context" ke taur par deta hai, sabab-e-nuzul ke taur par nahi; "khaas waqia nahi" kehna isliye theek, par MINOR item 5 dekho |
| 9 | Zyadatar ulama ke mutabiq makki; Qatada wagairah ne madani bhi kaha | dossier P2 (Qurtubi 103, Alim/Malik intro, quran.com) | ikhtilaaf, "zyadatar" teen source se, theek |
| 10 | Riwayat me aata hai: nabi ke do saathi milte to ek-doosre ko ye surah sunate aur salam karke hi alag hote | dossier N3 (Tabarani; IK EN + Ma'ariful dono ne diya) | maana hua, PC confirm baaki (Tabarani number/darja/rawi) |
| 3, 6 | Qasam -> insaan ghate me -> bachne ki 4 baatein (mukhya sandesh) | dossier P5 (IK EN, Tabari, Ma'ariful) | maana hua |
| 4 | Naam pehli ayat ke "al-'asr" shabd se | dossier P1 | maana hua |
Koi sabab-e-nuzul gadha nahi gaya; koi "chhoda gaya" (C1-C6) baat nahi.

## FIX items
1. MINOR (dossier se bahar ka shabd) — line 16: "सुबह, शाम, दिन और रात, सब।" Dossier M1 (Tabari "dahr") me "shaam, raat, din sab" hai; "subah" nahi. Fix: "शाम, रात, दिन, सब" ya "सुबह" hata do (sirf "दिन और रात, सब"). Matlab ka farq nahi, par dossier se milao.
2. MINOR (T1 se lagbhag hu-ba-hu) — line 20: "बेशक इंसान घाटे में है।" Suhel Farooq Khan (T1) ka "बेशक इन्सान घाटे में है" bas nukta-spelling ke farq se wahi hai (006 R1 me aisi line MAJOR thi). Chhoti baat hai aur teeno tarjumon ka saanjha matlab hai, isliye MINOR; behtar: "दूसरी आयत: हर इंसान घाटे में पड़ा हुआ है।" (M2 ke "poori insaaniyat" se bhi milta hai). Line 26 "मगर वो लोग, जो ईमान लाए" T1 ke "मगर जो लोग ईमान लाए" ka ulta kram hai, theek; chaho to "सिवाय उनके जो ईमान लाए" jaisa do.
3. MINOR — line 10: Tabarani riwayat ka number/darja/rawi PC par confirm baaki (sources.json pc_check 4). Jab tak confirm na ho, line 10 ka shabd "रिवायत में आता है" aur koi naam nahi rakho (abhi waisa hi hai). Confirm na ho sake to line 10 hata do; koi renumber ki zaroorat nahi mat maano — hatane par numbering 1..51 fir se karo aur end_from badlo. Description ki Sources me "number baaki" wali line mat jaane do.
4. MINOR (repeat) — line 3 aur line 6 ek hi vaakya do baar: "वक़्त की क़सम, इंसान का घाटा, और घाटे से बचने का रास्ता / चार बातें". Hook aur AYAH 1 ke baad dono 25 s ke andar hain. Line 6 ko chhota karo, jaise "ये रही पूरी सूरह।" ya sirf "घाटे से बचने की चार बातें" par rakho (taste, 1-2 s bachega).
5. MINOR (wording) — line 8 chaar tafseer ke naam leta hai par tafseer-pages WebFetch (summary tool) se khule the (sources.json note). Safe wording: "माने हुए तफ़्सीरों में नहीं मिलता" (dossier N1 ki apni video-line), naam hata do ya "तबरी और इब्ने कसीर समेत" jaisa halka rakho. Taaki IK ke C1 "context" se takrao ka jokhim na rahe.
6. MINOR (PC, baaki) — sha256 aur Amiri render zoom (103:2 khanjari alif/alif maksura, 103:3 ke sukoon, do khanjari alif, shadda): sources.json ke 103:1 ka bina-Bismillah hash naya nikalna hai (script header me likha hai). Makki/Madani Tanzil metadata. Ye BLOCKER nahi, Kaarigar PC par kare.
7. MINOR (taste) — line 28 "पहली शर्त ईमान है" aur line 49 "दोनों चाहिए" dossier M3/K5 ke andar hai; theek, sirf dhyan rahe ki "शर्त" shabd fiqh-sa na lage. Chaho to "पहली बात ईमान है" rakho.

R2 ke baad ye sab MINOR carry_over.md me ja sakte hain; BLOCKER/MAJOR koi nahi.

Free ya paid: sab fix free (sirf script text). Koi STOP condition nahi (balance/copyright/channel ID: Tanzil CC BY 3.0 credit SOURCES me hai, music licence register me hai).

Agla kadam: Kalam items 1-2, 4-5 (aur 3, 7 chaho to) theek karke R2; phir PC par Arabic sha256 + Amiri zoom, Tabarani number, Makki/Madani metadata, phir sheets/TTS.

---
## R2 — Munshi, 2026-11-13
VERDICT: PASS-WITH-NOTES (BLOCKER/MAJOR koi nahi, ASK nahi, Rs0, koi STOP condition nahi)

Dobara khola: script.md lines 6, 8, 16, 20, 28 + Arabic/UCHARAN/numbering (code se).
- Item 1 (line 16): "शाम, दिन और रात, सब" — "सुबह" hat gaya, dossier M1 se mila. FIXED.
- Item 2 (line 20): "हर इंसान घाटे में पड़ा हुआ है" — T1 se alag. FIXED.
- Item 4 (line 6): "ये रही पूरी सूरह। इसमें घाटे से बचने की चार बातें आती हैं।" — hook se ab sirf halka dohrao (taste). FIXED.
- Item 5 (line 8): "माने हुए तफ़्सीरों में नहीं मिलता" — tafseer ke naam hat gaye, N1 ki video-line. FIXED.
- Item 7 (line 28): "पहली बात ईमान है" (line 49 "दोनों चाहिए" waisi hi). FIXED.
- Item 3 (line 10): "रिवायत में आता है", koi naam nahi; CONTINUITY + SOURCES me PC confirm flagged. MINOR OPEN -> carry_over.
- Arabic: 7 blocks sources.json se byte-barabar (True x7); UCHARAN 6/6 ucharan.md se match; numbering 1..52 bina gap (script ke hisse me); koi '?' nahi; end_from 51 wahi.
- Item 6 (PC: sha256, Amiri zoom, Makki/Madani metadata) OPEN -> Kaarigar PC par.
Carry_over (MINOR): Tabarani number/darja (jab tak confirm na ho, description me naam/number nahi; confirm na ho to line 10 hatao aur numbering/end_from badlo); sha256 + Amiri zoom.
Agla kadam: Kaarigar PC checks, phir sheets/TTS.
