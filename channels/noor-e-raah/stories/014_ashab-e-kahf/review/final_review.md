# Munshi FINAL R1 — 014 Ashab-e-Kahf (Quran 18:9-26) — 2026-11-19

STEP: final R1 (Long) + Short quick check + script R2   PROJECT: noor-e-raah/014_ashab-e-kahf
VERDICT: Long **PASS-WITH-NOTES**, Short **PASS** (1 trivial metadata fix done by Munshi). STOP condition: none.

## Script R2 (R1 fixes 1-7)
- script.md / script.json: L4 -> 16_dawn_cave, L18 -> 05_leave_town, L38 -> 04_youths_stand, L43-45 -> 14_people_cave, L46 stays 15_stars_cave. Verified in frames too (19 s cave + town; 100 s youths + dog; 206 s youths facing townspeople; 233/240 s crowd at cave).
- L40 "क़ुरआन समझाने वाले पुराने आलिम लिखते हैं..." (hedge kept, F12 tafseer), L46 "क़ुरआन में आया है: कहो, मेरा रब ही..." (18:22), L49 "...हर छिपी बात, बस वही जानता है" (18:26). All three match the ayat; plain Hindi (2f). OK.
- 52 lines, no viewer question, no lesson line, no teaser; last line L52 = source line only (2k/2l). OK.

## Long (output/video.mp4)
- ffprobe: 297.55 s (4:57.5, inside 4:00-5:00 with only 2.5 s margin), 1920x1080 h264 30 fps, AAC 48 kHz mono.
- ebur128: I -14.9 LUFS, LRA 2.8. Music bed present between lines (0.1 s RMS p5 ~ -31 dB, not silence); one track Quietude_Sections_Merged for all 52 lines (script.json), in licence register line 144 (CC BY 4.0, The Imperfectionist).
- SRT: 52 blocks, monotonic, 2.6-9.5 s each, ends 297.405 s; text == script.
- Arabic: script.json "ar" for L7 (18:13 from إِنَّهُمْ), L20 (18:10 from رَبَّنَآ), L47 (18:25 full) = byte-equal suffixes of research/quran-uthmani.txt (Tanzil). Rendered by history_build.py via libass Amiri (RULES 1c). Frames 37 s / 108 s / 262 s: full line visible, not cut at edges, harakat in place; Arabic y~90-200, source label y~330, ucharan y~870 -> no overlap.
- Captions: Mukta in dark box, 1-2 balanced lines, readable at 800 px width; gold keywords present (ईमान, गुफा वाले, सही राह, कुत्ता, पत्थर, पुराने सिक्के, गिनती, तीन/पाँच, मेरा रब ही, तीन सौ साल, अल्लाह ही).
- Depiction (2e/2j): no Prophet, no angel; all people faceless storybook figures with white heads/glow; no human face anywhere in 19 frames.
- Thumbnail: faceless sleepers in cave, "गुफा वाले नौजवान / 309 साल की नींद", label "क़ुरआन • सूरह अल-कह्फ़". 300+9 = Quran 18:25. OK.

## Short (short/output/short.mp4)
- 48.74 s (< 60), 1080x1920, -14.3 LUFS (within ±1). Long lines 22-30 consecutive (18:11, 18:17-18), no new spoken wording; no Arabic ayah in this run, so RULES 2b ayah-completeness n/a; every sentence complete.
- Edges: l22 leading silence 0.28 s (fade-in 0.3 s does not eat the first word); l30 voice ends ~48.0 s, fade-out starts 48.08 s -> last word intact, but only ~0.1 s hold before the fade (carry_over asks 0.5 s) = MINOR 6.
- Captions at ~74-82 % height, tag at ~18 % -> inside 15-85 %. Faceless figures + dog only.
- Hook: frame 0 = sleepers in cave + "फिर अल्लाह ने उनके कानों पर पर्दा डाल दिया" — visual hook ok; spoken start "फिर" is a cold connective (MINOR).

## Metadata
- Long upload.json: title 78 chars, privacy private, made_for_kids false, contains_synthetic_media true, sources (Quran 18:9-26, Tanzil CC BY 3.0 attribution + link, bhaavarth note, Ibn Kathir / Tabari / Ma'ariful Qur'an), AI disclosure, music credit CC BY 4.0 with link, tafseer-claim note. channel_id UCmw4fs9jN49GTq7wVSdYm6w == channel.json. name_guard OK.
- Short upload.json: same channel_id, private, synthetic true, sources + AI + music credit; LONG_ID placeholder (filled after Long upload, not a defect). name_guard OK.
- **Munshi trivial fix:** Short title was 73 chars (SHORT_FROM_LONG.md limit 70) -> removed "और ": "गुफा में सदियों की नींद, दरवाज़े पर उनका कुत्ता | असहाब-ए-कहफ़ #shorts" (70). name_guard re-run OK.

## MINOR (carry_over, no rebuild)
1. Long length 4:57.5 = only 2.5 s under the 5:00 cap; next story aim ~4:40.
2. 07_dua_cave: hands raised to shoulder height beside the heads (2a wording prefers hands in front of chest below chin); respectful, from the back, accepted in script R1; prompt "hands in front of chest" next time.
3. Short tag "18:11-18" reads as a range 11-18; the run is 18:11 + 18:17-18. Next time "18:11, 17-18".
4. Short opens on "फिर ..." (connective); SHORT_FROM_LONG step 1 also asks for a closing pointer to the full video — not possible without new wording; description link + first comment cover it.
5. Carried from script R1: 02_town_idols bowing crowd, 08 has 5 sleepers vs 4 elsewhere, 10 dog "gloves", 13 market faux text.

Frames: review/final/*.jpg, sheets review/final_sheetA.jpg, final_sheetB.jpg, final_sheetS.jpg.
Agla kadam: Long upload (private, api_audited false -> STUDIO ACTION), then Short with LONG_ID filled. Upload not done by this review.
