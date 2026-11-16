# 006 al-kausar — script review (SURAH CHECK) — Munshi, 2026-11-12
VERDICT: FIX (chhote, free fixes; koi BLOCKER nahi; koi ASK nahi, Rs0)

## Kya khola / naapa
script.md, research/dossier.md, sources.json, ucharan.md, channel RULES (1, 1a, 1c, 1d, 2, 2a), image files, tools/name_guard.py.

## Verified (PASS)
- RULES 1d: ek hi narrator (USTAAD); koi sawaal nahi (script me '?' nahi, "SAWAAL"/"[NOTE]" sirf header me "nahi hai" likhne ke liye); koi tilawat disclaimer nahi.
- Arabic: 4 ARABIC lines code se sources.json ayat[].text se byte-compare: AYAH 1 (teeno ayat space se juda) + 108:1, 108:2, 108:3 = sab byte-barabar. (sha256 / Tanzil.net byte-milaan / Amiri zoom PC par baaki, jaisa dossier me likha.)
- UCHARAN lines 13, 19, 25 = ucharan.md ki "Line:" se akshar-akshar barabar; teeno apne BHAAVARTH (14, 20, 26) se pehle.
- Line numbering 1..35 bina gap; aakhri bolti line 34, aakhri cue 35; end_from 34 sahi. Har jumla me 2-3 matlab vaakya (16-17, 22-23, 28-30) with tags.
- Koi C1-C9 content nahi (Ka'b, Hudaybiyya, bete ki wafat, 16 maane, nahar ka roop-varnan, wanhar ke tafseeli qaul, qibla, be-aulaad: kuch nahi). Taane dene wale ka koi naam nahi. "abtar" = jad-kata / be-nishaan (be-aulaad kahin nahi). Koi fazilat / sawab / guarantee ka daava nahi. "Sabse chhoti surah" nahi. Makki/Madani = ikhtilaaf (line 10), "zyadatar" nahi. Nahar sirf "riwayaton me" (line 16).
- Honorifics theek (Anas "anhu", Ibn Abbas "anhuma"). Visuals: koi insaan/Nabi/Sahabi/farishta/janwar/qurbani nahi, caption me "jannat" nahi; 10 library image IDs (002/05, 002/06, 002/09, 002/11, 003/02, 003/03, 003/04, 003/05, 003/08, 003/09) sab maujood; 0 nayi image Rs0. name_guard: OK.
- Length: USTAAD 482 shabd (maine ginti ki, header se match) x0.45 + UCHARAN 10 shabd + gaps = ~4:14; pehla poora Arabic ~0:25-0:28. Target 4-6 min me (kinaare par). Dhyan: channel RULES 1c purani line "~7-8 min" kehti hai; aapke diye 4-6 min target par script theek hai, 3 ayat ki surah ke liye natural. Asli TTS 4:00 se kam aaye to koi dikkat nahi.
- Nigraan LAGU KARO: hook + pehla Arabic ~0:27, parichay ek line, pehle 60 s me koi image ~8-10 s se lambi nahi: lage hain.

## Shan-e-nuzul sheet (har baat alag)
| Line | Baat | Source | Grade |
|---|---|---|---|
| 3, 8 | Makka ke kuch virodhi nabi SAW ko "abtar" keh kar taana dete the; surah uska jawab | Tabari 108, Ibn Kathir EN 108, Ma'ariful 108 (sources.json TB_108, IK_EN_108, MQ_108; N1) | maana hua (core) |
| 9 | Naam par riwayaton me ikhtilaaf, naam nahi liya; Tabari: aayat khaas shakhs par utri ho to bhi matlab aam | TB_108, IK_EN_108 (N1, M3) | maana hua |
| 10 | Makki/Madani par ulama me ikhtilaaf | Qurtubi 108 (QT_108), TB/IK/MQ koi faisla nahi (P2) | ikhtilaaf, sahi bola |
| 11 | Anas (Muslim): unghh ke baad muskura kar surah padhi | QT_108 + SUNNAH_MUSLIM (sunnah.com khula nahi, number nahi) (N2) | sahih, PC confirm baaki (MINOR neeche) |

## FIX items
1. MAJOR — line 33: "इब्ने कसीर के मुताबिक़ जो आपसे बैर रखे, असल में वही कट जाता है।" Dossier (M3/M5, IK) sirf ye kehta hai ki nabi SAW se bair rakhne wala abtar hai. Ise seedha sunne wale ("आपसे") par laga dena dossier se bahar ki baat hai aur kisi ko "abtar ka misdaaq" banane wali line hai (dossier "Ye mat kaho"). Fix: "इब्ने कसीर के मुताबिक़ सूरह का जवाब यही है कि नबी सल्लल्लाहु अलैहि वसल्लम से बैर रखने वाला ही कटा हुआ है" aur seekh wala hissa sirf "ताने का जवाब बैर नहीं, शुक्र और भरोसा" tak rakho (ye dossier ka SEEKH-3 hai).
2. MAJOR (copied wording, RULES 1a) — line 20: "अपने रब ही के लिए नमाज़ पढ़ो" Muhammad Farooq Khan ke tarjume (T2 column) se hu-ba-hu; line 26 "जड़-कटा" bhi unka shabd (par yahan "be-nishaan" saath hai, theek). Line 20 apne shabdon me badlo, jaise "तो अपने रब के लिए ही नमाज़ अदा करो और उसी के लिए क़ुर्बानी दो" (teeno tarjumon ka saanjha matlab wahi rahe). Line 14 ("तुम्हें कौसर दिया") chhoti hone se theek.
3. MINOR — line 29: "यानी ताना देने वाला नहीं, बल्कि जवाब यही रहा।" saaf nahi / adhoora. Likho: "यानी बे-निशान ताना देने वाला हुआ, नबी सल्लल्लाहु अलैहि वसल्लम का ज़िक्र नहीं।" (M3, IK).
4. MINOR — lines 23 aur 31: "शुक्र में इबादत भी पूरी होनी चाहिए" / "इसीलिए आता है" dossier M4 se thoda aage hai (Tabari: ata aam, isliye ibadat ka hukm bhi aam). Dossier ke shabdon ke paas rakho: "जब अता आम है, तो इबादत का हुक्म भी आम है।"
5. MINOR — line 11 (N2): Muslim ka hadith sirf Qurtubi ke zariye aaya, sunnah.com khula nahi. PC par confirm hone tak rakho; confirm na ho to line 11 hata do (script baaki ka kuch nahi bigadta). Description ki Sources list me "number PC se confirm baaki" jaisi line mat jaane do (production me hata do).
6. MINOR — IMAGES section: "Kul ~16 clips" asal me ~18 clips (10 base). RULES ki limit sirf nayi images par hai (0 nayi) isliye theek; bas ginti sahi kar do. Lines 34-35 me "I crop / D crop" ek rect pakka likho (same image+rect dobara na ho).
7. MINOR (note) — line 8 "मक्का के कुछ विरोधी" aur line 10 Makki/Madani ikhtilaaf saath me thoda takrate hain; dossier ki apni video-line yahi hai isliye rakha ja sakta hai; chaho to line 8 me "मक्का के" ki jagah "कुछ" rakho.

Free ya paid: sab fix free (sirf script text). Koi STOP condition nahi (balance/copyright/channel ID).

Agla kadam: Kalam items 1-2 (aur ho sake to 3-6) theek karke dobara review (R2); phir PC par Arabic byte-milaan + sha256 + Amiri zoom + Muslim number.

---
## R2 — Munshi, 2026-11-12
VERDICT: PASS (koi BLOCKER/MAJOR nahi; Rs0; koi STOP condition nahi)
Kya check kiya: script.md dobara poora padha, dossier M3/M4/P6 se line 29/31 milaye.
- Item 1 (line 33): theek — ab "ताने का जवाब बैर नहीं, भरोसा और शुक्र है", sunne wale par abtar nahi lagaya. Line 29 me IK ki "zikr qayamat tak" dossier (M3/P6) me hai.
- Item 2 (line 20): apne shabdon me, theek. Item 3 (line 29): saaf. Item 4 (23, 31): "ata aam -> ibadat ka hukm aam" Tabari/M4 ke andar.
- Item 5 (line 11): rakha, PC par Muslim number+text confirm ki shart saaf likhi hai (header, SOURCES, CONTINUITY).
- Item 6: ~17-18 clips, 0 nayi, lines 34-35 rect pakka. Item 7: "मक्का के" hata diya (line 8).
- Arabic/UCHARAN lines ab tak badli nahi (R1 byte-check valid); line numbers 1..35, end_from 34.
MINOR (carry_over): line 33 "बाक़ी फ़ैसला अल्लाह पर" dossier me nahi, halka hai; chaho to hata do. Line 30 aur 33 ki "रूहानी सिलसिला"/seekh thode dohrate hain (taste).
PC par baaki: Arabic Tanzil byte-milaan + sha256, Amiri zoom, Muslim (Anas) number, Makki/Madani metadata.

## PC checks (2026-11-12, Kaarigar)
- Arabic vs Tanzil (tanzil.net uthmani txt download): script + sources.json had Quran-Academy-style mark order (fatha before shadda; 108:1 precomposed madd alif U+0622). FIXED to Tanzil bytes (shadda first, alif + U+0653) in script.md, sources.json, dossier.md, ucharan.md; all 4 ARABIC lines now byte-equal; sha256 filled in sources.json.
- Muslim (Anas) line 11: CONFIRMED in open source fawazahmed0 eng-muslim (book 4, hadith 56; = sunnah.com 400a): dozed, raised head smiling, "a Sura has just been revealed to me". Line 11 text matches, no number spoken -> line 11 KEPT, no renumbering, end_from 34 unchanged.
- name_guard: OK.
