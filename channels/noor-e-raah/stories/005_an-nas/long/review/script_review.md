# Munshi - SCRIPT review R1 (SURAH CHECK) - noor-e-raah 005_an-nas (2026-11-03)
VERDICT (R2, current): PASS (all R1 items 1-9 fixed; no BLOCKER/MAJOR; no STOP; Rs0). R1 verdict was: FIX (2 MAJOR, 8 MINOR; no BLOCKER; no STOP condition; cost Rs0; free fixes only)

## FIX (numbered)
1. MAJOR - line 40 [M3] "ख़तरा बाहर का नहीं, अंदर का है" and line 18 [M1] "क्योंकि ख़तरा लोगों के दिलों का है": these are the dossier writer's own inference (M3 row has only a bracket "(andar ka khatra)"; M1 "kyunki" is not a tafseer statement). Line 40 also contradicts line 45 (whisperers can be "इंसानों में से", i.e. outside people). Fix: line 40 keep only "सुदूर = सीने/दिल; वसवसा लोगों के दिलों में डाला जाता है"; line 18 drop "क्योंकि..." or attribute it to a tafseer that says it.
2. MAJOR - line 53 [M5] attributes to Ma'ariful Qur'an "अन-नास में अंदर के ख़तरे से". sources.json M5 says Ma'ariful: Falaq = worldly hardships, Nas = trials of the HEREAFTER; "inner" is not in M5 (only in the dossier P6/M5 table as "andar/akhirat"; MQ_114 page holds only ayah 1). Fix: use "आख़िरत की आज़माइशों से" exactly as M5, or drop the attribution and keep the Falaq+Nas pairing as plain seekh with no tafseer name.
3. MINOR - line 45: second sentence (Ibn Kathir "सुरक्षित वही जिसे अल्लाह बचाए") is M5, tagged [M4]. Tag [M4][M5] or move it.
4. MINOR - header line 30 says "6 ayat sirf screen card par, bolne me nahi", but line 4 "छह आयतें" and line 8 "छह छोटी आयतें" are spoken in the first minute (learnings: no counting lines in minute 1). Fix: remove the spoken count in 4 and 8 (or correct the header).
5. MINOR - copy risk (RULES 1a, MINOR): line 38 "जो लोगों के दिलों में" = 5-word run identical to Tanzil hi.hindi (Suhel Farooq Khan, ayah 5) and "वसवसा डालता है" = Farooq Khan; line 31 "वसवसा डालने वाले की बुराई से" ~ Farooq Khan ayah 4. Meaning is right; rephrase in own words (e.g. "जो इंसानों के सीनों में बुरे ख़याल डालता रहता है").
6. MINOR - IMAGES: (a) "Kul: 17 clips" is wrong, the table has 29 clips (16 base A-P is right). (b) My word-rate check: lines 3-6 = 22+24+14+16 words ~ 36-37 s, so first full Arabic (line 7) lands ~0:36, not 0:31 (still inside the 30-40 s target, OK) and line 4 alone is ~11.5 s on one crop (A crop 9-17 s in the plan). Fix: re-time the plan to ~0:36 and add a second crop for line 4 so no clip passes ~8-10 s.
7. MINOR - header line 26 says Arabic "PC par Tanzil se byte-milaan ho chuka (Sanchalak)", but sources.json "note"/"pc_check" and dossier STATUS still say NOT byte-verified, and no Tanzil file is in the repo for me to compare. What I verified: all 7 script ARABIC lines == sources.json ayat[].text byte-exact, AYAH 1 == ' '.join(6 ayat), sha256_utf8 of the 6 single ayat == sources.json. Fix: update sources.json/dossier once the PC check is really done (Munshi cannot confirm it). Carry the Amiri zoom (shadda, dagger alif 114:3) to the build review.
8. MINOR - line 51 [P6] "डर या बेचैनी में पहला सहारा..." generalises P6 (refuge from the whisperer's evil). Tie it to the vasvasa wording or retag as seekh with the sentence limited to P6.
9. MINOR - line 35 [MISAAL] "ये कई लोगों ने महसूस किया है" is an unsourced empirical claim (not religious). Soften ("कई बार ऐसा होता है" / "सोचिए, ...") ; no other change. MISAAL count 1 (max 2) OK.
10. INFO/MINOR - length: my count USTAAD 539 + UCHARAN 21 + SAWAAL 82 words = same as the script (~357 s = 5:57), but the band top 6:20 exceeds the queue target 4-6 min. Keep the planned trims (18, 34, 49) ready. Shared RULES s.15 "long max 4:00" is overridden for Noor by channel RULES 1c / NOOR_DAILY_RUN (7-8 min accepted; 004 ~7:07 passed); queue target 4-6 is met.

## Verified myself
- ARABIC: 7 lines (1 whole + 6) == sources.json, byte-exact; sha256 of 6 ayat match. Bismillah absent. No normalisation.
- UCHARAN lines 14/20/25/30/37/42 == ucharan.md "Line:" text exactly (list equality), each before its BHAAVARTH (15/21/26/31/38/43). Word-level checks vs Tanzil/Q411 Latin: OK (assimilated lam forms, अल्लज़ी, युवस्विसु, इलाहिन). Plain reading, no tilawat cue in script. Intro note once (line 5).
- Numbering 1..56 in file order, no gaps; last two spoken 54, 55; last cue 56; end_from 54 correct.
- Tags: P1,P2,P3,P6,N2,T2,T3,M1-M5,Z1,Z2,NOTE,NEXT,MISAAL all exist in dossier/sources.json with the same grade. Z3 and C1-C8 absent (grep: no Labid, jaadu, girah, 11, qareen, khoon, shaitan roop). No revelation-order number, no fiqh/hukm/"guarantee".
- Hook honest: queue hook_hint (An-Nasr "जीत मिले तो...") correctly NOT used; line 3/4 match surah's main message P6. Promise paid at line 4 + Arabic at ~0:36 (target 30-40 s). Parichay is one line (6). Title option 1 starts with the search phrase.
- Sawaal: real questions = line 3 (~0:01) and line 50 (~5:15) = 2, gap ~5 min (>= 3-3.5). Lines 35 and 55 are not questions; no deeni claim by SAWAAL. Misaal 1.
- Bhaavarth 15/21/26/31/38/43 vs the three translations (translation_options.md): same meaning in all three; Tanzil brackets "(शैतानी)", "(ख़ुदा के नाम से)", "(ऐ रसूल)" not used; no copy except the small runs in item 5. Label present.
- Images: all 15 `.../` paths + A (003/01_one_star_night) exist = 16 base images. I opened 001 images 05, 18, 22, 23, 06: only places/lamps/paths, no person, no figure (001 ones are not in image_library.md; add after video). Dark lamp F/G, door M, lamp N etc. are library images already passed in 002/003. First 60 s plan has no clip > ~8 s except item 6(b). Same (image, rect) not repeated.

## Shan-e-nuzul sheet (each statement)
- Line 10 [P2] An-Nas + Al-Falaq = "मुअव्विज़तैन" | Ibn Kathir EN, Qurtubi 114, Ma'ariful (IK_EN_114, QT_114, MQ_114) | maana hua | OK.
- Line 11 [P3] Makki/Madani "उलमा में इख़्तिलाफ़" ("ज़्यादातर" NOT used; grep: absent in whole script) | Qurtubi 113 (Makki: al-Hasan, Ikrima, Ata, Jabir; Madani: Ibn Abbas one report, Qatada), Ibn Kathir AR "wa huma madaniyyatan", Tanzil metadata "meccan" | ikhtilaaf | OK (note: QT_113 / IK_AR_113 / TANZIL_CH were read in 004, not re-opened for 005 - dossier says so; acceptable, same sources).
- Line 12 [N2] "कोई सहीह-दर्जे की ख़ास वजह नहीं मिलती" | N1 (IK, QT, Tabari, MQ 114 pages carry no cause) | maana hua | OK. No sihr/Labid event, no "isliye utri". Hadith line 47 (Muslim 814 "tonight") is placed in the hadith section as a report, not as a cause: OK.
- Z1 / Z2 (hadith): line 47 = Z1 (Muslim 814, Uqba bin Amir); line 48 = Z2 (Bukhari 5017/5748, Aisha: palms, blow, Ikhlas+Falaq+Nas, wipe head/face/body, 3 times); line 49 states riwayat only, no hukm/promise. Honorifics full (अन्हु / अन्हा correct). **PC check needed**: sunnah.com returned 403 (SUNNAH_MUSLIM_814 / SUNNAH_BUKHARI opened:false); wording comes from 004 hadith-api reading. The script flags it (line 223, SOURCES, source map "PC check needed"). Do not upload the description's hadith numbers as confirmed until the user/PC confirms them.

## Continuity
Aisha/Uqba names only spoken, no screen figure. No dates, ages or relations in this script. Next video hint (al-Kausar, queue order 5) matches series_queue.

## Next
Builder fixes items 1-2 (MAJOR) and 3-9 (MINOR), then ask for R2. After R2 only-MINOR = PASS-WITH-NOTES (RULES s.15, carry_over.md). Open for PC: byte-check vs tanzil.net, sunnah.com numbers, Amiri zoom, Whisper check per TTS line.

## R2 (2026-11-03)
VERDICT: PASS
- Items 1-2 (MAJOR) fixed: line 40 now only "sudoor = seene/dil" [M3]; line 18 no "kyunki"; line 53 = "aakhirat ki aazmaishen" exactly as M5.
- Item 3: line 45 tagged [M4][M5]. Item 4: no spoken "chhah" in lines 4/8 (line 55 end only, fine). Item 5: lines 31/38 reworded. Item 6: 29 clips, line 4 has two crops, first 60 s clips <= ~8 s. Item 7: header now honest (PC check pending). Items 8, 9: lines 51, 35 softened. Item 10 INFO: trims 18, 34, 49 ready.
- Re-verified by code: 7 ARABIC lines == sources.json ayat byte-exact, AYAH 1 == joined 6; 6 UCHARAN lines == ucharan.md "Line:" and sit before their BHAAVARTH; numbering 1..56 no gaps; last spoken 54, 55; cue 56; end_from 54.
- Open for PC/build (not blockers): byte-check vs tanzil.net, sunnah.com numbers (Muslim 814, Bukhari 5017/5748), Amiri zoom (shadda, dagger alif 114:3), Whisper check per TTS line. Update sources.json/dossier PC-check note.
