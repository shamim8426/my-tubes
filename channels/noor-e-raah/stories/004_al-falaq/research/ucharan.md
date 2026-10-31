# Ucharan (Arabic -> Devanagari) — Surah Al-Falaq 113 | Kalam, 2026-10-31

Format (RULES 1c, 2026-10-30): each jumla block (`[AYAH 2..6]` = ayah 1..5) gets one `UCHARAN` line = the SAME Arabic words in Devanagari, read plainly by the Ustaad (NOT tilawat) and shown under the Arabic on screen.

**Sources:** Arabic = Tanzil Uthmani (`sources.json` `ayat[].text`, copied into the script by code). Latin check text = Tanzil transliteration `ara-quran-la` (`TRANSLIT_TANZIL`) and quran411 `ara-quran-la1` (`TRANSLIT_Q411`, pausal/joined forms). Latin is used ONLY to check consonants/vowels; the Devanagari is our own writing. Fact `T3`.

**Rules used (as 003):** ق=क़ · ف=फ़ · غ=ग़ · خ=ख़ · ذ=ज़ · ث=स · ع = vowel only · the article joins as pronounced (बिरब्बिल = birabbi + al-falaq) · at the END of a jumla the last vowel is dropped (waqf): फ़लक़, ख़लक़, वक़ब, उक़द, हसद · `وَمِن` is one Arabic word, written वमिन (as 003 वलम).

**Decisions to check:** (1) 113:4 `شَرِّ ٱلنَّفَّٰثَٰتِ`: the lam of al- is assimilated (shaddah on nun-fa), so the run is "sharri-n-naffathati": **शर्रिन नफ़्फ़ासाति** (quran411 'sharrin-naffaa-thaati'). (2) `ث` is written स (th as in Hindi-speakers' plain reading); Munshi may prefer थ - keep one choice, consistently. (3) `إِذَا` = इज़ा. (4) 113:1: the pausal form `ٱلْفَلَقِ` -> फ़लक़ (not फ़लक़ि).

Check done by code: Arabic chunks of each ayah joined with a space == Tanzil ayah string; Latin chunks joined == Tanzil Latin tokens; Devanagari chunks joined == the script line text.

## AYAH 2 = 113:1  (script line 14)

Arabic: قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ

| # | Arabic chunk | Tanzil Latin | Quran411 | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | قُلْ | Qul | Qul | क़ुल |
| 2 | أَعُوذُ | aAAoothu | a'uzoo | अऊज़ु |
| 3 | بِرَبِّ ٱلْفَلَقِ | birabbi alfalaqi | bi rabbil-falaq | बिरब्बिल फ़लक़ |

Line text: "क़ुल अऊज़ु बिरब्बिल फ़लक़"

## AYAH 3 = 113:2  (script line 21)

Arabic: مِن شَرِّ مَا خَلَقَ

| # | Arabic chunk | Tanzil Latin | Quran411 | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | مِن | Min | Min | मिन |
| 2 | شَرِّ | sharri | sharri | शर्रि |
| 3 | مَا | ma | ma | मा |
| 4 | خَلَقَ | khalaqa | khalaq | ख़लक़ |

Line text: "मिन शर्रि मा ख़लक़"

## AYAH 4 = 113:3  (script line 27)

Arabic: وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ

| # | Arabic chunk | Tanzil Latin | Quran411 | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | وَمِن | Wamin | Wa min | वमिन |
| 2 | شَرِّ | sharri | sharri | शर्रि |
| 3 | غَاسِقٍ | ghasiqin | ghasiqin | ग़ासिक़िन |
| 4 | إِذَا | itha | iza | इज़ा |
| 5 | وَقَبَ | waqaba | waqab | वक़ब |

Line text: "वमिन शर्रि ग़ासिक़िन इज़ा वक़ब"

## AYAH 5 = 113:4  (script line 34)

Arabic: وَمِن شَرِّ ٱلنَّفَّٰثَٰتِ فِى ٱلْعُقَدِ

| # | Arabic chunk | Tanzil Latin | Quran411 | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | وَمِن | Wamin | Wa min | वमिन |
| 2 | شَرِّ ٱلنَّفَّٰثَٰتِ | sharri alnnaffathati | sharrin-naffaa-thaati | शर्रिन नफ़्फ़ासाति |
| 3 | فِى ٱلْعُقَدِ | fee alAAuqadi | fil 'uqad | फ़िल उक़द |

Line text: "वमिन शर्रिन नफ़्फ़ासाति फ़िल उक़द"

## AYAH 6 = 113:5  (script line 40)

Arabic: وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ

| # | Arabic chunk | Tanzil Latin | Quran411 | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | وَمِن | Wamin | Wa min | वमिन |
| 2 | شَرِّ | sharri | sharri | शर्रि |
| 3 | حَاسِدٍ | hasidin | haasidin | हासिदिन |
| 4 | إِذَا | itha | iza | इज़ा |
| 5 | حَسَدَ | hasada | hasad | हसद |

Line text: "वमिन शर्रि हासिदिन इज़ा हसद"
