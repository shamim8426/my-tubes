# Ucharan (Arabic -> Devanagari) — Surah Al-Ikhlas 112 | Kalam, 2026-10-30

Format (user 2026-10-30, as 002): each jumla (`[AYAH 2..5]` = ayah 1..4) gets one `UCHARAN` line = the SAME Arabic words in Devanagari, read plainly by the Ustaad (NOT tilawat) and shown under the Arabic on screen. This file lets Munshi check every chunk.

**Sources:** Arabic = Tanzil Uthmani (sources.json `ayat[].text`, copied into the script by code; the chunks below are cut from the same strings by word position, never retyped). Latin check text = Tanzil transliteration, edition `ara-quran-la` (fawazahmed0/quran-api, source tanzil.net) = column 3 (sources.json `TRANSLIT_TANZIL`); column 4 = quran411 (`ara-quran-la1`, `TRANSLIT_Q411`) for the pausal (waqf) and joined (wasl) forms. Latin is used ONLY to check consonants/vowels; it is not shown or spoken; the Devanagari is our own writing. Fact `T3`.

**Rules used (as 002):** ق=क़ · ف=फ़ · ع = vowel only · long vowels kept (यूलद) · at the END of a jumla the last vowel is dropped (waqf): अहद, समद, यूलद · the article joins as pronounced (हुवल्लाहु = huwa+Allahu, अल्लाहुस्समद = Allahu+as-samad, per quran411 'huwal laahu', 'hus-samad').

**Decisions to check:** (1) 112:4 `يَكُن لَّهُۥ`: the Arabic has the nun assimilated into the lam (shadda on the lam of lahu); quran411 gives 'yakul-lahu'. Two words kept, nun spoken as lam: **यकुल लहू** (not 'यकुन लहू', which would be a wrong reading). (2) 112:1 'huwa Allahu' is one run in speech: **हुवल्लाहु** (dossier suggestion; both Arabic words are present). (3) 112:2 'Allahu as-samadu' run together: **अल्लाहुस्समद**; the plain-reading TTS may need a small pause — Munshi listens (Whisper cannot judge Arabic words).

Check done by code: the Arabic chunks of each ayah joined with a space == Tanzil ayah string (words 4/2/4/5); Latin chunks joined == Tanzil Latin tokens of that ayah; Devanagari chunks joined == the script line text.

## AYAH 2 = 112:1  (script line 14)

Arabic: قُلْ هُوَ ٱللَّهُ أَحَدٌ

| # | Arabic chunk | Tanzil Latin (ara-quran-la) | Quran411 (waqf/wasl) | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | قُلْ | Qul | Qul | क़ुल |
| 2 | هُوَ ٱللَّهُ | huwa Allahu | huwal laahu | हुवल्लाहु |
| 3 | أَحَدٌ | ahadun | ahad | अहद |

Line text: "क़ुल हुवल्लाहु अहद"

## AYAH 3 = 112:2  (script line 20)

Arabic: ٱللَّهُ ٱلصَّمَدُ

| # | Arabic chunk | Tanzil Latin (ara-quran-la) | Quran411 (waqf/wasl) | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | ٱللَّهُ ٱلصَّمَدُ | Allahu alssamadu | Allah hus-samad | अल्लाहुस्समद |

Line text: "अल्लाहुस्समद"

## AYAH 4 = 112:3  (script line 27)

Arabic: لَمْ يَلِدْ وَلَمْ يُولَدْ

| # | Arabic chunk | Tanzil Latin (ara-quran-la) | Quran411 (waqf/wasl) | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | لَمْ | Lam | Lam | लम |
| 2 | يَلِدْ | yalid | yalid | यलिद |
| 3 | وَلَمْ | walam | wa lam | वलम |
| 4 | يُولَدْ | yooladu | yoolad | यूलद |

Line text: "लम यलिद वलम यूलद"

## AYAH 5 = 112:4  (script line 33)

Arabic: وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ

| # | Arabic chunk | Tanzil Latin (ara-quran-la) | Quran411 (waqf/wasl) | Devanagari (spoken + on screen) |
|---|---|---|---|---|
| 1 | وَلَمْ | Walam | Wa lam | वलम |
| 2 | يَكُن لَّهُۥ | yakun lahu | yakul-lahu | यकुल लहू |
| 3 | كُفُوًا | kufuwan | kufuwan | कुफ़ुवन |
| 4 | أَحَدٌۢ | ahadun | ahad | अहद |

Line text: "वलम यकुल लहू कुफ़ुवन अहद"

## Cross-check text (quran411, whole surah, pausal forms)
Qul huwal laahu ahad; Allah hus-samad; Lam yalid wa lam yoolad; Wa lam yakul-lahu kufuwan ahad
