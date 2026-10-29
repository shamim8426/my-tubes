# Munshi — SCRIPT review R1 — noor-e-raah 002_ayatul-kursi (2026-10-29)
VERDICT: FIX (MINOR only; no BLOCKER, no MAJOR). Free fixes below; after them PASS.

## Verified myself
- Arabic: code compare. script AYAH 1 == sources.json ayah.text; the 10 pieces joined (space) == whole; sha256 cdf04bda... matches; lines.json arabic entries identical; all 66 lines.json texts occur verbatim in script.md.
- Tags: P1-P4, N1, N2, U1-U10, K1, K2, K3, K5, FZ-A, FZ-B all exist in dossier, same grades. No C1-C15 / N3 / K4 / FZ-C / FZ-D content. K1/K2 told as ikhtilaaf ("कई क़ौल", "ज़्यादातर रिवायतों"). K6 handled (word "कुर्सी").
- Shan-e-nuzul sheet: [N1][N2] line 7 "koi mazboot khaas waqia nahi" | Wahidi dataset (2:256 only), IK, MQ, Jalalayn, Baghawi | maana hua. [P1][P2] line 5 | Tanzil metadata, IK 2:1 | maana hua. [P3] line 6 | Bukhari 2311/3275/5010, Qurtubi | maana hua.
- Fazilat: FZ-A (Muslim 810) lines 4, 57-58 wording = dossier; "हदीस के मुताबिक़ ... सबसे अज़ीम" chip wording ok. FZ-B (Bukhari) line 59 "बुख़ारी की हदीस में है" + line 60 "भरोसा और दुआ, नतीजा उसी के हाथ" = dossier-allowed; no guarantee/jaadu/taweez/jinn word.
- Bhaavarth: own words, no 5+ word run from T1/T2/T3 (compared with translation_options.md); core meaning same as all 3; label line present in header and screen notes.
- Structure: 2 real sawaal (line 3 ~0:03, line 61 ~4:46; gap ~4:40); line 23 misaal, 55 reaction, 66 comment request (no deeni claim); only USTAAD makes deeni statements. Hook promise ("10 lines, 10 baatein", "sabse azeem") within ~12 s; words before AYAH 1 = 77 -> first Arabic ~0:35; parichay+shan-e-nuzul ~19 s; ending prompt + next-video hint (Al-Ikhlas, 4 ayat = true).
- Images: 20 entries (12 new, 8 reuse), no person/Prophet/angel/throne/Allah depiction/writing; "ring in sand" = K3 misaal; name_guard OK on images.json, script.md, metadata.md, thumbnail.json. Prompts simple (places, sky, lamp).
- thumbnail.json chip/hook honest (dossier FZ-A safe wording; hook is a question, no fear); title search-first. metadata.md Tanzil line byte-identical to 001; no "chhoda gaya" claim; 286/287 line matches P1.

## Problems
1. MINOR - script.md lines 8, 11, 15, 20, 25 ... 51 and lines.json cues type=music "fade-out 1s — ARABIC ON SCREEN" + "back slowly: River Flute" (lines 10, 13, 17 ...): RULES 1c says music is continuous, only a soft swoosh at each Arabic block; a builder reading the cue literally would stop the music (MINOR, loud hit/beat would be BLOCKER). Fix (free): rewrite these cues as "[SWOOSH — ARABIC ON SCREEN]" and delete the "back slowly" cues; keep only the track-change crossfades (Soaring -> River Flute at the first AYAH, line 56).
2. MINOR - line 59: in Bukhari 2311 the "bistar par jao to Ayatul Kursi padho ..." words are told to Abu Hurayrah and the Prophet then says "सच कहा"; the line reads as a plain Nabi order. Fix: add 'नबी सल्लल्लाहु अलैहि वसल्लम ने इसकी तस्दीक़ की' style attribution OR keep exactly the dossier FZ-B text and confirm the wording on sunnah.com (PC). Do not add shaitan story/visuals.
3. MINOR - first minute, image 05_dawn_horizon (ayah 2) is the only image from ~46 s to ~62 s (16 s). Fix (free): in shots.json give it 2 shots/crops (<= 8-10 s each), same for any other image > 10 s in the first minute.
4. MINOR - length: my count 665 words (script says 664) = ~266 s + gaps/Arabic ~65 s = ~5:30 (script's own estimate 5:23). On the edge of 5:30; real TTS may exceed. Apply the script's own trim list (lines 55, 60 stays with 59, 6+7 merge) only if real audio > 5:30; up to 6:00 is allowed by series_queue but 4-6 min is NOT yet written into channel RULES/bible ("Long ~8:00", RULES 1b) — series_queue itself says it needs the user's OK. Also RULES 1b "3-3.5 min gap / ~3 questions in 8 min" was waived by the script for a ~5 min video (2 questions, ~4:40 apart: fine). Record the user's 4-6 min decision in RULES/log (sources dated 2026-10-30 though today's clock is 2026-10-29 - clock/date should be checked).
5. MINOR - thumbnail.json: wallpaper is a paid Gemini image (Rs3.81+GST, mosque hall with pointed arches). Free-first rule: log why a free flux image was not used (or swap to free); the video body itself avoids domes/minarets, the thumbnail does not conflict with that.
6. INFO - metadata.md is a DRAFT (chapters TODO until render); long/meta.json is an empty template (fill at build); SOURCES lists hi.hindi authors, whose Tanzil terms are non-commercial - no text copied, so only noted (same as 001).

## Judgement on tone
Nothing disrespectful or misleading found. "सबसे अज़ीम" is always hadith-attributed; Kursi shown only as sky + small ring, no throne; Allah not placed in a place (K5 line 46, line 54).

## Must be confirmed on a PC (not possible here)
- Byte compare of 2:255 against tanzil.net quran-uthmani (strip BOM); render zoom of `يَـُٔودُهُۥ` in libass/Amiri.
- sunnah.com: Muslim 810 and Bukhari 2311/3275/5010 Arabic+English wording, ta'liq form, who-says-what.
- Real TTS (Whisper per-line check, total length <= 5:30), real timing of first Arabic <= ~35 s.

---
# R2 (2026-10-29) - VERDICT: PASS-WITH-NOTES (no BLOCKER, no MAJOR)

## Verified
1. Cues: script.md + long/lines.json use `[SWOOSH — ARABIC ON SCREEN]` / `[MUSIC continue: River Flute — matlab]`. noor_build.py CUE regex accepts SWOOSH and maps it to music "swoosh — ARABIC ON SCREEN"; noor_render.py treats "swoosh" + ARABIC like old "fade-out" (music_to not called, music plays on) and "continue" like "back slowly" (crossfade to same track, no stop). Final "fade-out" (end) branch unchanged. 001 lines.json / folder: git diff clean. RULES.md 1c documents both cue names (lines 41-42). Music continuous in code.
2. Line 59 now: report form (Abu Hurayrah ki riwayat, "उन्हें बताया गया", nigehbaan + subah tak shaitan qareeb nahi, "नबी ﷺ ने फ़रमाया कि उसने सच कहा"), matches FZ-B ("बुख़ारी की हदीस में है"); no shaitan story, no guarantee; line 60 = bharosa/dua, natija uske haath. Small note (MINOR): "उसने सच कहा" has no named "उसने" (the one who told) - fine for audio but still confirm wording on sunnah.com (PC, already open item). No overclaim.
3. Images: MAX_SHOT = 8 s in noor_render so the builder auto-splits every image into <= 8 s shots (different move each); so no static >8 s shot. Per-image estimates (lines.json words at ~2.5 w/s + 2 s Arabic alone; real TTS later): 05_dawn_horizon (ayah 2, ~38-51 s) ~13 s and 05_dawn_horizon_c (line 18 -> ayah 4, ~56-70 s) ~14 s; 04_date_palm_path (line 6 -> ayah 1) ~10 s; others <= ~9 s. Note: oasis (ayah 3) now sits between the two dawn images, so dawn returns after the oasis; fine (free reuse). Over ~10 s: 05_dawn_horizon, 05_dawn_horizon_c (two 8 s-capped shots each), borderline 04_date_palm_path.
4. Arabic: AYAH 1 == sources.json ayah text, 10 pieces joined == whole, sha256 cdf04bda matches; lines.json arabic == script ARABIC (11 == 11). Tags all in dossier (P1-P4, N1, N2, U1-U7, U9, U10, K1-K3, K5, FZ-A, FZ-B), no C1-C15/N3/K4/FZ-C/FZ-D content (only the "not said" list mentions). name_guard OK on script.md, images.json, thumbnail.json, long/output/metadata.md.
5. RULES.md line 40 has the 4-6 min series length. log.md 2026-10-30 line gives the free-first reason (cloudflare blocked in cloud network; paid Rs3.81+GST, user choice). Date note: log uses 2026-10-30 while clock is 2026-10-29 (cosmetic).

## Still open (PC / later)
tanzil.net byte compare + Amiri render of يَـُٔودُهُۥ; sunnah.com Muslim 810 / Bukhari 2311/3275/5010 wording; real TTS length <= 5:30 and first Arabic <= ~35 s (my estimate ~0:33). Metadata draft chapters at render.

---
# R3 (2026-10-29) - quick re-check after free trim (lines 6, 14, 28, 36, 46, 50, 55 removed) - VERDICT: PASS-WITH-NOTES

## Verified
1. Structure complete: parichay (5) -> shan-e-nuzul statement (7, N1/N2 kept) -> whole ayah (AYAH 1) -> 10 units, each with Arabic + bhaavarth (12,16,21,26,30,34,38,42,48,52) -> hadith 57-60 -> seekh 62-64 -> next video 65 + comment prompt 66. lines.json has 34 lines, none of the removed numbers. Missing matlab for U1, U4, U6, U9 is acceptable: bhaavarth alone is accurate and not misleading. U10 line 54 still says "ऊँचाई जगह के मानी में नहीं" (K5 core). Kursi K1/K2/K3 lines 44/45 kept, ikhtilaaf wording intact.
2. Tags: only tags that lost every line are P3 and K5 (+ U1/U4/U6/U9 matlab; U4 still cited at 63). No spoken claim lacks a tag. Source map rows (P3 line 6, U-row, K5 line 46, line 55 refs, sawaal table line 55) are stale text only; trim note at top covers it.
3. Real sawaal: line 3 (0:00) and line 61 (~4:50): 2, gap ~4:45. OK.
4. First full Arabic: lines 3-7 end ~32.6 s, first Arabic block ~34-35 s (line 9 ends 38.7 s). Total plan 5:32 (332.3 s), within 4-6 min series rule.
5. images.json 04_date_palm_path start line 7; render.json card line 5 until 5: consistent. Images not yet generated here (plan lists them missing), nothing else changed.
6. No "chhoda gaya" content added. Arabic: AYAH 1 == sources.json ayah text, 10 units joined == whole (code compare, True/True).

## Notes (MINOR, carry_over)
- K5 line (Allah not in a place / not needing throne) removed: after the Kursi lines 44/45 only line 54 carries the idea. Dossier "safe line" ideally stays; if length allows later, re-add as one short Ustaad line after 45 (about 8 s, 5:40). Not a blocker.
- Refresh stale line numbers in SOURCE MAP / sawaal table (cosmetic).
