# Munshi — script R3 (do awaaz, user faisle: 3 lines hatayi + music tracks + spelling) — 001 Al-Fatiha — 2026-10-24

VERDICT: PASS (0 BLOCKER, 0 MAJOR; 3 chhote notes -> carry_over.md, audio stage / sheet). STOP condition: koi nahi. Kharcha ₹0.

## Khud jaancha (Kalam ki summary par bharosa nahi)
- Arabic: 7/7 ARABIC lines aaj dobara download ki official tanzil.net quran-uthmani (txt-2) se byte-equal; HEAD (1ce4e44) se bhi byte-equal.
- BHAAVARTH: 7/7 commit 5ded601 (R2 PASS) aur HEAD se shabd-ba-shabd identical (program se).
- 5-shabd overlap (62 spoken lines, nukta hata kar) vs al-Umari (sheet (a)), Tanzil hi.farooq, hi.hindi (aaj download): 0 / 0 / 0. 4-shabd sirf aam vaakyansh ("अल्लाह के नाम से", "इबादत करते हैं और", "से मदद माँगते हैं") — theek.
- Ginti (program): 96 numbered lines (1..96 lagaatar), 62 spoken; USTAAD 719 / 45, SAWAAL 197 / 17, speaker badle 28 -> 363.1 + 98.5 + 16.8 + 14 = 492.4 s = 8:12 (script ka hisaab sahi). >25 shabd sirf line 81 (1:7 BHAAVARTH, 28, R2 wali). SAWAAL ki sabse lambi line 43 = 22 shabd (note ab sahi).
- Spelling: script me "क़ुरआन" 16 baar, sheet me 6; "क़ुरान" / "कुरान" / bina nukta "कुरआन" = 0 / 0 / 0.
- name_guard: OK (script aur sheet dono par khud chalaya).
- Music credits: SOURCES ki 3 lines `shared/assets_license.csv` (Soaring, Quietude_Sections_Merged, River_Flute) ke attribution_text se akshar-akshar (newline -> " — ") mili (program se). Earth/Water/Meditation credit hata. "Ambience: freesound.org (CC0)" maujood. Quietude ka FMA page khola: CC BY 4.0 (Attribution 4.0 International) — register sahi.
- Files: shared/music/noor/ me teeno track (ffprobe: Soaring 380 s, Quietude 484 s, River Flute 1228 s); shared/sfx/noor/ me chaaron ambience — har ek register me, path channel.json "music" se mila.

## Hatayi lines — bahaav / niyam
| Purani line | Hatane ke baad | Munshi |
|---|---|---|
| 12 (as-Salat/al-Hamd/ar-Ruqya/ash-Shifa, S4–S7) | 10 "कई नाम" -> 11 as-Sab'ul-Mathani -> 12 SAWAAL "अच्छा! तो एक बात में — इस सूरह में है क्या?" -> 13 [S20] | THEEK. RULES 1 "other names" (bahuvachan) do naamon se poora; "कई नाम" dossier S8 (Qurtubi 12 naam) ke andar. SCREEN note ab do cards — mel khata hai. S4 ab sirf line 26 ki hadith ke saath (sahi). |
| 29 (SAWAAL "दिल को छूने वाली बात") | 27 USTAAD -> 28 fade-out (AYAH 1) | THEEK — section ka kudrati ant; koi niyam ka khaali-pan nahi |
| 90 (SAWAAL "पहले शुक्र, फिर माँग") | 91 -> 92 -> 93 USTAAD seekh 1-2-3 lagaatar | THEEK — seekh 2–3 (RULES 1.4) poore; teen USTAAD lines ek saath, bahaav theek |

## Do awaaz niyam (RULES 1b)
17 SAWAAL lines (3, 5, 9, 12, 16, 19, 25, 38, 42, 43, 56, 67, 69, 76, 83, 90, 95) dobara padhi: koi hukm / fazeelat / hadith / tafseer daava nahi; nayi line 12 sirf sawaal. Har [S#]/[M#] USTAAD ki line par. MISAAL 2 (1:2, 1:5) — max 2 ke andar.

## Music / ambience cues (RULES 1c)
- Har aayat block (7/7, program se + padh kar): `[MUSIC fade-out 1s — ARABIC ON SCREEN]` -> `[AMBIENCE: gentle breeze]` -> ARABIC -> USTAAD BHAAVARTH -> `[MUSIC back slowly: River Flute — matlab]`. On-screen Arabic ke neeche koi music cue nahi; header (26–29) aur SCREEN note (93–96) ka timing niyam ek jaisa.
- Track naam: Soaring (1), Quietude – Ambient Synth Soundscape Pack (01 Sections Merged) (14, 23), River Flute (31…82 back cues, 88, 96) — user ke faisle aur register titles se exact; channel.json tracks ke paths se mel.
- Paani ambience: 16 AMBIENCE cues me koi paani/nadi/baarish/lehar/chashma nahi (sirf gentle breeze, desert wind + night wind/crickets, birds). MISAAL birds 41/44 aur 66/68 par, River Flute ke neeche "bahut dheemi".
- Tilawat / vocal / beat cue: koi nahi.

## Parichay / shan-e-nuzul — har baat alag (R2 se maadda wahi; sirf line number badle, purani 12 hati)
| Line | [S#] | Baat | Source link(s) | Grade | Munshi |
|---|---|---|---|---|---|
| 4 | S17 | sabse azeem surah | https://sunnah.com/bukhari:4474 ; IK muqaddama | maana hua | OK |
| 6 | S1 | Fatiha = kholne wali | Qurtubi bab 1; IK muqaddama | maana hua | OK |
| 7 | S12, S10 | pehli surah, 7 aayat, ittifaq | https://tanzil.net/res/text/metadata/quran-data.js ; IK muqaddama | maana hua | OK |
| 8 | S11 | is ginti me Bismillah aayat 1 | IK; Qurtubi | ikhtilaaf | OK (dossier ki ijaazat wali ek line) |
| 10–11 | S2, S3 | Umm al-Quran, as-Sab' al-Mathani | https://sunnah.com/bukhari:4704 ; https://sunnah.com/bukhari:4474 ; IK; Qurtubi | maana hua | OK |
| 13 | S20 | markazi paigham | https://api.quran.com/api/v4/tafsirs/169/by_ayah/1:5 ; Tafheem; MQ 1:6 | maana hua | OK |
| 17 | S15 | khaas waqiye ki mazboot riwayat nahi | IK; Qurtubi; Wahidi | ikhtilaaf | OK |
| 18 | S15, S9 | zyadatar: Makki, shuruaati daur | IK 1:1; Qurtubi bab 2; Wahidi | ikhtilaaf | OK ("ज़्यादातर उलमा के मुताबिक़") |
| 20 | S9 | doosri raay: Madani | IK; Qurtubi; Wahidi | ikhtilaaf | OK |
| 21 | S9 | teesri raay: do baar | Qurtubi; IK | ikhtilaaf | OK |
| 22 | S9 | Ibn Kathir: pehli raay zyada munasib | IK | ikhtilaaf | OK |
| 26–27 | S16, S4 | hadith-e-qudsi taqseem + "jo maanga" | https://sunnah.com/muslim:395a ; https://api.quran.com/api/v4/tafsirs/169/by_ayah/1:5 | maana hua | OK |
| 45, 51, 59, 71, 87 | S16 | har hisse ka jawab | https://sunnah.com/muslim:395a | maana hua | OK |
| 91 | S20 | pehle tareef phir maang = behtar tareeqa | https://api.quran.com/api/v4/tafsirs/169/by_ayah/1:5 | maana hua | OK |

C1–C10 me se kuch nahi; 1:7 me qaum ka naam nahi; maslak/firqa naam nahi; nuzool kram nahi bola.

## Notes (MINOR, carry_over.md — script dobara review nahi chahiye)
1. Sheet (b) ke neeche "Line 28: Bismillah ka jawab nahi" -> ab line 27; sheet (c) notes "Line 96 viewers se sawaal" -> ab line 95. Sirf number.
2. Audio stage: line 14 par Soaring -> Quietude badlaav ke liye ≥1 s crossfade (shared RULES 3), dialogue ke beech nahi. Line 23 (Quietude) aur 88 (River Flute) par track pehle se chal raha hai — "jaari rahe, dobara shuru nahi" saaf rakho.
3. Audio stage: wind_birds_petebuchwald_288899.mp3 aur gentle breeze me paani/nadi ki awaaz na ho (kaan se suno); Soaring me beat/percussion na ho (RULES 1c) — user ne sample sun kar chuna, phir bhi mix me jaancho.
