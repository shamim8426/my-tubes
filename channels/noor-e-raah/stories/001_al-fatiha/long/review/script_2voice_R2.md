# Munshi — script R2 (do awaaz version USTAAD/SAWAAL) — 001 Al-Fatiha — 2026-10-24

VERDICT: PASS-WITH-NOTES (0 BLOCKER, 0 MAJOR, 3 MINOR/notes -> carry_over.md). STOP condition: koi nahi. Kharcha ₹0.

## Khud jaancha (Kalam ki summary par bharosa nahi)
- Arabic: 7/7 ARABIC lines official tanzil.net quran-uthmani (R1 wali download) se byte-equal.
- BHAAVARTH: 7/7 lines commit 5ded601 (R2 PASS ek-narrator version) se shabd-ba-shabd identical (program se).
- 5-shabd overlap (65 spoken lines, nukta hata kar) vs al-Umari, hi.farooq, hi.hindi: 0 / 0 / 0. 4-shabd: "अल्लाह के नाम से", "इबादत करते हैं और", "से मदद माँगते हैं" (line 66, SAWAAL, aam vaakyansh) — theek.
- Ginti (program): 65 lines; USTAAD 733 / 46, SAWAAL 216 / 19, speaker badle 32 -> 511.4 s = 8:31 (script ka hisaab sahi). Sirf line 79 > 25 shabd (28, BHAAVARTH, R2 wali). SAWAAL ki sabse lambi line 22 shabd (line 44) — script "18" likhti hai (MINOR, neeche).
- name_guard: OK (script par khud chalaya).
- Music credit lines: shared/assets_license.csv 141/144/147 se akshar-akshar mile.

## R1 findings — haal
| # | R1 | Ab | Munshi |
|---|---|---|---|
| 1 | MAJOR line 28 "हर हिस्से पर" | "'और मेरे बंदे को वो मिलेगा जो उसने माँगा।' फिर हदीस बताती है कि फ़ातिहा के हिस्सों पर अल्लाह की तरफ़ से जवाब आता है।" | THEEK — quote Muslim 395 ki shuruaati baat se milta hai; "हर" hata, Bismillah par jawab ka daava nahi |
| 2 | MAJOR Arabic/music samay | Header (23–26) aur SCREEN note (89–92) dono: Arabic ka pehla frame fade poora hone ke baad; music back tabhi jab Arabic (animation samet) hat chuki | THEEK — dono jagah ek hi niyam; har aayat block me cue kram 30/31 -> ARABIC -> BHAAVARTH -> back (7/7 blocks dekhe) |
| 3 | line 57 | "मालिक तो वो हमेशा है; ..." | THEEK (IK 1:4, MQ 1:4) |
| 4 | line 44 | "ख़ूबियों को सराहना... क्या यही हम्द है?" | THEEK (M2); SAWAAL sawaal ki shakl me |
| 5 | line 45 | "हाँ, यही। और इस आयत पर हदीस में अल्लाह का जवाब है: ..." | THEEK |
| 6 | line 59 | "— 'बुज़ुर्गी' यानी बड़ाई।" | THEEK |
| 7 | line 67–68 | 67 SAWAAL sawaal, 68 USTAAD bharosa wali baat [M5][MISAAL] | THEEK — koi hukm nahi; dossier M5 + misaal note (line 167) ke andar; C10 (wasila) nahi chheda |
| 8 | SOURCES music credit | 3 Kevin MacLeod lines + ambience SFX note | THEEK |

## Shan-e-nuzul / parichay — har baat alag (R1 se badla nahi; sirf 28 badli)
| Line | [S#] | Baat | Source link(s) | Grade | Munshi |
|---|---|---|---|---|---|
| 4 | S17 | sabse azeem surah | https://sunnah.com/bukhari:4474 ; IK muqaddama | maana hua | OK |
| 6 | S1 | Fatiha = kholne wali | Qurtubi bab 1; IK muqaddama | maana hua | OK |
| 7 | S12, S10 | pehli surah, 7 aayat, ittifaq | https://tanzil.net (quran-data); IK muqaddama | maana hua | OK |
| 8 | S11 | is ginti me Bismillah aayat 1 | IK muqaddama; Qurtubi | ikhtilaaf | OK (dossier ki ijaazat wali ek line) |
| 10–12 | S2–S7 | naam | https://sunnah.com/bukhari:4704 ; https://sunnah.com/bukhari:5007 ; https://sunnah.com/muslim:395a ; IK; Qurtubi | maana hua | OK |
| 14 | S20 | markazi paigham | Tafheem; https://api.quran.com/api/v4/tafsirs/169/by_ayah/1:5 ; MQ 1:6 | maana hua | OK |
| 18 | S15 | khaas waqiye ki mazboot riwayat nahi | IK; Qurtubi (Bayhaqi munqati'); Wahidi | ikhtilaaf | OK |
| 19 | S15, S9 | zyadatar: Makki, shuruaati daur | IK 1:1; Qurtubi bab 2; Wahidi | ikhtilaaf | OK |
| 21 | S9 | doosri raay: Madani | IK; Qurtubi; Wahidi | ikhtilaaf | OK |
| 22 | S9 | teesri raay: do baar | Qurtubi (Tha'labi); IK | ikhtilaaf | OK |
| 23 | S9 | Ibn Kathir: pehli raay zyada munasib | IK (والأول أشبه) | ikhtilaaf | OK |
| 27–28 | S16, S4 | hadith-e-qudsi taqseem + "jo maanga" | https://sunnah.com/muslim:395a ; https://api.quran.com/api/v4/tafsirs/169/by_ayah/1:5 | maana hua | OK (R2) |
| 45, 51, 59, 69, 85 | S16 | har hisse ka jawab (hamd / tareef / buzurgi / bayni-wa-bayna / li-abdi) | https://sunnah.com/muslim:395a (IK 1:5 me matn) | maana hua | OK |
| 89 | S20 | pehle tareef phir maang = behtar tareeqa | https://api.quran.com/api/v4/tafsirs/169/by_ayah/1:5 | maana hua | OK |

C1–C10 me se kuch nahi; 1:7 me qaum ka naam nahi; maslak/firqa naam nahi; nuzool kram nahi bola. SAWAAL ki 19 lines dobara padhi: koi hukm/fazeelat/hadith/tafseer daava nahi. Visuals: koi insaan/Nabi/Sahabi/farishta/Ka'ba nahi. Tilawat audio nahi.

## MINOR / notes (carry_over.md)
1. LENGTH ESTIMATE: "SAWAAL ki sabse lambi line 18 shabd" galat — line 44 = 22 shabd (≤ 25, niyam ke andar). Sirf note theek karo.
2. Music files: `Water_Prelude.mp3` aur `Meditation_Impromptu_02.mp3` ab `shared/music/noor/_options/` me hain, par register (141–149) aur channel.json music list `shared/music/noor/` path dikhate hain; `_options/` me 5 aur tracks (New_Direction, Quietude_Sections_Merged, River_Flute, Soaring, Tranquility) register me nahi. Audio stage se pehle: jo track asal me lage wahi `shared/music/noor/` me, sahi path + source + licence register me, aur SOURCES me sirf unki credit line. Bina register wala track video me = BLOCKER (audio stage).
3. Lambai ~8:31 (leads/fades ke saath ~8:40) vs RULES 1b "~8:00": user ki pasand — Kalam ki optional cuts (29, 12, 90, 11) user approval par.
