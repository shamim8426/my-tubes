# Munshi - SCRIPT + PACKAGE review R1 - noor-e-raah 004_al-falaq (2026-10-31)
VERDICT: PASS-WITH-NOTES (after my free fixes; no BLOCKER left)

## Fixed by me (free, line numbers unchanged)
1. ARABIC mark order (would have been BLOCKER "Arabic != Tanzil"): sources.json / script / ucharan.md / dossier / translation_options had fatha-or-kasra BEFORE shadda (U+064E/U+0650/U+064F + U+0651). Tanzil (risan uthmani.json, file sha adaebb37... = same as 003) stores shadda FIRST (U+0651 then the vowel). Swapped in all 5 files, recomputed sha256_utf8 in sources.json. Now script AYAH 1 == ' '.join(5 ayat) and the 5 single ARABIC lines == Tanzil bytes (Bismillah prefix of 113:1 stripped). 113:4 ends kasra U+0650 (final glyph OK).
2. Script line 31 (M3): "डर, शरारत और नुक़सान की बातें" -> "जानवर, ख़राबी और शरारत की बातें" (dossier M3 says jaanwar/kharabi/shararat; "dar" was not in the source).

## Verified myself
- noor_build parse (temp copy only): 43 lines, 16 cues, 6 ARABIC, numbers 1..59 in file order, last spoken 57, 58, last cue 59; render.json end_from 57 correct. UCHARAN 14/21/27/34/40 each before its BHAAVARTH, equal to ucharan.md "Line text", NFC.
- Words: USTAAD 688 (UCHARAN excluded), UCHARAN 23, SAWAAL 95 -> ~7:07 estimate (RULES 1c ~7-8 min). First full Arabic (AYAH 1) ~0:30.
- UCHARAN decisions: (a) ث = स: ACCEPTED, same in all lines, matches plain Hindi-Urdu usage. (b) "शर्रिन नफ़्फ़ासाति": ACCEPTED (assimilated lam, nun + doubled nun, long a after ff and after s from the dagger alifs, final kasra kept mid-ayah). (c) "फ़िल उक़द": ACCEPTED (long ee of fee shortens before wasl, lam pronounced, waqf on उक़द). (d) "वमिन": ACCEPTED (one Arabic word, as 003). Others (बिरब्बिल, अऊज़ु, ग़ासिक़िन, हासिदिन, इज़ा) match TRANSLIT_TANZIL/Q411. Listening check at TTS: Algieba must not chant; "नफ़्फ़ासाति" must not lose the doubled फ़/न.
- Tags P1,P2,P3,P6,N1/N2,Z1,Z2,M1-M6,T2,T3,NOTE,NEXT,MISAAL exist in the dossier with the same grade. No Z3, no C1-C13, no Labid/knots/sihr event (grep), no revelation order, no fiqh, no "guarantee/badal".
- Shan-e-nuzul sheet (each statement): line 10 [P2] Mu'awwidhatayn | Ibn Kathir, Qurtubi, Ma'ariful Qur'an | maana hua | OK. Line 11 [P3] Makki/Madani ikhtilaaf ("ज़्यादातर" NOT used) | Qurtubi (makki qawl), Ibn Kathir "madaniyyatan", Tanzil metadata | ikhtilaaf | OK. Line 12 [N1][N2] "koi sahih-darje ka khaas waqia nahi" | N2 "behtar" wording, Ibn Kathir/Qurtubi/Tabari/MQ | maana hua | OK (see note 1).
- Hadith: line 49 Muslim 814 ('Uqba bin 'Amir) wording = Z1; lines 50-51 Bukhari 5017/5748 (Aisha) = Z2 (palms, blow, Ikhlas+Falaq+Nas, wipe head/face/front, 3 times); line 52 states riwayat only, no hukm/promise. Honorifics full. Only sahih.
- Bhaavarth 15/22/28/35/41: own words, no run of 5+ words from Umari/Mahmud Hasan/Tanzil hi.hindi, same meaning in all three (har cheez, stree-ling "वालियों"). Label in header.
- Sawaal: real questions = line 3 (~0:01) and line 53 (~6:10) = 2, gap ~6 min; 32 misaal, 47 recap, 58 comment request = not questions, no deeni claim. MISAAL 1 (max 2). Intro note once (line 5).
- Images (images.json): 32 entries = 18 `reuse` + 14 crops, 0 new; all 18 reuse paths exist on disk; no (base image, rect) pair repeated; crop base ids all present. Reasons are in the file; thumbnail wallpaper new (free engine first). 113:4 = symbolic footpaths crop, no rope/hand/person. No Prophet/Sahabi/angel/person. Pacing from my TTS-rate estimate: 01 0-8.3, crop 8.3-15.4, 04 15.4-22.4, 05 22.4-30.1, 06 30.1-43 (builder MAX_SHOT split), 03 43-52, crop 52-62: about 8 s each, none static beyond the MAX_SHOT split.
- Ambience/music: shared/sfx/noor has night_wind_crickets, wind_birds, gentle_breeze, swoosh; music Soaring + River_Flute exist; all in assets_license.csv (CC BY 4.0 / CC0).
- Thumbnail: Arabic title, chip "सुबह के रब की पनाह", hook question, no title-word repeat, no people, honest. Title starts with search phrase (86 chars).
- upload.json == metadata.md: Tanzil notice, ucharan-not-tilawat line, saral-bhaavarth line, ikhtilaaf + no-sahih-incident lines, Sources, MUSIC credits, ambience CC0, fonts, AI line, hadith "no hukm/promise" line; category 27, made_for_kids false, publish_at auto. Sihr event absent from description.
- Screen text: render.json cards (lines 6, 54-56) match script; text_scale default 1.35 in force.

## Notes (MINOR / INFO)
1. MINOR: line 12 is true but terse: Bukhari 5763 (sihr event) is sahih, only its link to the revelation is not. Sanchalak chose this wording; keep. Do not add the event.
2. MINOR: first shot (line 3) ~8.3 s and 03 valley ~8.6 s are at the ~8 s limit; if real TTS runs longer, builder should split with an extra crop. Not a blocker.
3. INFO: 002 script still has 1 kasra+shadda pair in the wrong order (U+0650 U+0651) - not mine to change; check at 002 if re-rendered.
4. PC items open: sunnah.com numbering Muslim 814, Bukhari 5017/5748 (keep "सहीह हदीसें" only if confirmed); Amiri zoom on 113:4 ٱلنَّفَّٰثَٰتِ; Whisper per-line TTS check; CHAPTERS_TODO.
