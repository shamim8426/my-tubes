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

---

## Round R4 (2026-10-30) — NEW FORMAT: UCHARAN lines + fuller MATLAB + intro note (lines 70-88)

Verdict: **PASS-WITH-NOTES** (no BLOCKER, no MAJOR). 2 free fixes before the build (both MINOR, trivial), 4 cosmetic notes.

### What I opened and measured
- script.md (all 247 lines), research/ucharan.md, research/sources.json (ayah, TRANSLIT_TANZIL, TRANSLIT_Q411, T3), dossier.md (U1-U10, K1-K6, section 6), channel RULES.md (lines 40-42), docs/NOOR_DAILY_RUN.md, scripts/noor_build.py, scripts/noor_render.py, long/images.json, render.json, the old lines.json and audio/tts.
- Code checks (temp copy in the scratchpad, lines.json NOT touched): parse of the new script with `noor_build.parse`; old-vs-new text compare per line number; `noor_render.timeline()` and `shots_for()` run on the parsed items with real durations for the old lines and a word-based estimate for the 19 new/renumbered lines.

### 1. Arabic == Tanzil (PASS)
- `ayah.text` sha256 (UTF-8) = cdf04bda... matches sources.json `ayah_string_sha256_utf8`; 408 code points, 50 words.
- `ARABIC:` of AYAH 1 == sources.json text (byte-equal, True). The 10 chunks of AYAH 2..11 joined with spaces == the whole ayah (True), each chunk is a substring. No normalisation visible.
- PC byte-check against live tanzil.net is still open (known, same as R2/R3).

### 2. UCHARAN lines (PASS-WITH-NOTES)
- The 10 script lines (71-80) are identical to the "Line text" of ucharan.md (True). Characters: only Devanagari + space, no ASCII, no ZWJ/ZWNJ, no brackets/tags/meaning. Nuqta is the combining U+093C everywhere (no pre-composed U+0958..095F) = consistent.
- Word-by-word against the Arabic and TRANSLIT_TANZIL / Q411 (50 of 50 words): all faithful. No missing/extra/changed word. Last vowel dropped at the jumla end as the rule says (हुव, नौम, अर्ज़, इज़्निह, शा, अज़ीम); a long final vowel is kept (हिफ़्ज़ुहुमा) which matches Q411 "hifzuhumaa". Fine.
- Spelling choices that read sensibly in plain Hindi: क़/ख़/फ़/ज़ for ق/خ/ف/ذ-ظ-ض; ع as vowel only (यशफ़उ, इंदहू, वसिअ); "यअलमु" with अ for ع-sukun is the usual way.
- Notes (MINOR, no fix needed):
  - U4 (line 74) "फ़ी अल अर्ज़" is written apart while U2 and U8 elide the article ("अल हय्युल", "वल अर्ज़"). Plain reading is fine; if you want it neat: "फ़िल अर्ज़". Not a faithfulness error (Tanzil Latin has "fee alardi").
  - U7 (line 77) ends "बिमा शा": the hamza of शآء is dropped (Tanzil Latin "shaa"); Q411 has "shaaa'". Acceptable for plain reading.
  - Every ث/ذ/ظ/ض is "ज़": the Hindi convention, no meaning change.
- Tilawat check: UCHARAN text has no chant markers; channel.json Ustaad style already says "never singing or chanting". At TTS time, listen for any tune on lines 71-80 (BLOCKER if tilawat-like).

### 3. New MATLAB sentences vs dossier (PASS)
Line | Tag | Support in dossier | Verdict
- 81 | U1 | IK: Allah is the one Rabb of all creation; MQ: "Allah" is the Name of the Being, none else worthy of worship | OK
- 82 | U4 | IK: all His servants, His kingdom; MQ: ownership + authority (ikhtiyar) | OK
- 83 | U5 | IK: no one dares speak; MQ: the one given permission speaks. Nothing from QT "whom Allah honours and is pleased with", no named intercessor | OK, no new claim
- 84 | U6 | IK: past, present, future; MQ: both readings allowed (aage-peeche + zahir-chhupa) | OK
- 85 | K5 | = the dossier "Video ke liye surakshit line" (K1/K2/K3/K5 wording) | OK, restores the K5 note missing since R3
- 86 | U9 | IK: no burden, easy; QT: yuthqiluhu (heavy) | OK
- The earlier lines 18, 19, 24, 32, 40, 44, 45, 54 are unchanged text with their tags. Line 32's "सिफ़ारिश यानी किसी के हक़ में बात करना" is a plain word gloss (old line, kept).
- No fatwa, no new fazilat, no "chhoda gaya" item (C1-C15, N3, K4, FZ-C, FZ-D), no guarantee/jaadu/taweez words (grep clean; only in the header's "do not say" list). Language is simple Hindi.
- Sentence count: every jumla has 3 sentences (BHAAVARTH + 2 MATLAB) except U3 (+ MISAAL line) and U8 (BHAAVARTH + 3 sourced K lines = 4). U8 is over "2-3" by one, but all are tagged and K5 is the safe line: accept (RULES allows where the dossier needs it).

### 4. Rules / sawaal / sources (PASS)
- SAWAAL: real questions = line 3 (0:01) and line 61 (~6:35) = 2 (limit for this video 2). Gap ~6.5 min (rule 3-3.5 min). Lines 23 (MISAAL, human drowsiness, no deeni claim) and 88 (comment request, no "?") are not real questions. No deeni claim in any SAWAAL line.
- Deeni lines are all USTAAD; honorifics present (line 44, 45, 57-59). Hadith lines: Muslim 810 / Bukhari 2311 as in R1-R3 (sunnah.com wording still to open on the PC).
- Intro note line 70 [NOTE]: present once, no deeni claim, wording equal to RULES 41 and NOOR_DAILY_RUN.
- RULES.md (lines 40-42) has the 7-8 min decision, the pronunciation rule and the Munshi checklist; docs/NOOR_DAILY_RUN.md has the script-format section. Consistent with the script. RULES 1c: cues are `[SWOOSH — ARABIC ON SCREEN]` + `[MUSIC continue: River Flute — matlab]`, music never stops; AYAH 1 has the swoosh, no UCHARAN (as intended).
- Nigraan LAGU KARO: hook promise in line 4 at ~0:07 (OK); first full ayah ~0:42 (see 6); the "technical" lines (counting) are not present. Mat-dohrao list: no repeat.
- Sources block lists Tanzil, three translations, tafseer, hadith, music, ambience. UCHARAN source is in sources.json (T3) but is not in the SOURCES block: add one line for the description: "उच्चारण (देवनागरी): टंज़ील ट्रांसलिटरेशन से मिलाकर, पढ़ने की मदद, तिलावत नहीं" (MINOR).

### 5. Parser and renderer (PASS, 1 free fix in images.json)
- `noor_build.parse`: 51 spoken lines; regex reads `USTAAD — UCHARAN` (role "ucharan"), `SAWAAL — MISAAL`, `[NOTE]` tag outside the quotes is fine. Line numbers are unique; order in the file is the order of play; the LAST two lines are 87, 88, cue 89 (highest).
- Old-vs-new compare: for every old line number that still exists the text and speaker are IDENTICAL (no stale cached wav problem). New numbers: 70-88 (19 lines) need TTS (free key first); old 65/66 cache is simply not used (stale files stay in audio/tts, harmless).
- `noor_render`: `end_from` = lines[-2].n = 87 -> only lines 87 and 88 get the top position/end card (no other n >= 87). `ucharan` lines: shown as Translit under the Arabic from their start to the end of the Arabic block (translit selection `a0 <= start < off`, ucharan starts 2.0 s after the Arabic), skipped as bottom subtitles; label moves to y 640 (tr_mode). Arabic block stays until the "continue" cue (after BHAAVARTH) so UCHARAN and BHAAVARTH are both covered. `render.json` cards use lines 5, 62-64 only (unchanged numbers) = OK.
- The .srt will also contain the 10 UCHARAN lines (srt() writes all lines): harmless/helpful for CC; fine.
- **FIX (free, MINOR but do before the build): images.json entry `05_dawn_horizon_c` with `start: {line: 18}`.** With the new block structure line 18 is U2's MATLAB (AYAH 3). My shots_for() run puts the dawn-horizon crop at 85.6-101.0 s, i.e. it REPLACES the oasis image (`06_oasis_spring`, AYAH 3 "Hayy-Qayyum") for the second half of that block (oasis only 73.1-85.6). The dawn image itself now already runs 51.3-73.1 s (22 s) in 3 auto-split shots of ~7.3 s (cap 8 s), so the extra split is not needed. Fix: delete the `05_dawn_horizon_c` entry (preferred), or change it to `start: {line: 81}` (U1 MATLAB). Everything else maps right: line 45 (ayah 9 block), 57, 59, 61, 87 exist; images 01..12 all present.

### 6. Timing estimate (PASS-WITH-NOTES)
- Timeline run with real old-line durations (sec/word 0.497 before TEMPO 1.08) and estimated new lines (ucharan x1.3 per word): total about **444 s = 7:24** (Kalam: ~7:20; range 7:00-7:45). Inside the 7-8 min decision. If real TTS makes it > 8:00 the script's own trim order (second sentence of 82/84/86, line 83) is sensible.
- First full Arabic (AYAH 1): about **0:42** (a0 = 42.4 s; swoosh 41.8 s). RULES: ~35 s target, the honest note may push it to ~40 s. So ~2 s over the allowance (note itself ~7 s). Intro 0-7 s hook, 7-15 s promise, 16-23 s note, 24-35 s parichay (line 5, 10.7 s), 36-41 s shan-e-nuzul (line 7). First jumla UCHARAN 54 s, BHAAVARTH 58-63 s, MATLAB to 73 s.
  - Judgement: acceptable (MINOR, no regeneration): the note is a user decision and the first Arabic is still at the end of the first minute-less window. Optional free tweak that gets it to ~35 s and puts the note exactly where it matters: move line 70 to just after line 9 / before the first UCHARAN (it would then play ~46-53 s, 1 s before the first UCHARAN at ~54 s). If the user wants the note in the intro, keep as is.
- Other timeline checks: sawaal 1 at 0:01, 2 at 6:35; section line 61 etc. in the 6:35-7:10 range. Header/tables are stale (cosmetic): "line 23 ~2:50" is really ~1:55, "line 61 ~6:50" is ~6:35, "line 88 ~7:20" is ~7:10.

### 7. Process risks for the builder (not script faults)
- `noor_build.tts` runs a Whisper-hi word check and retries up to 2 more times (paid if the free key is exhausted) when words are "missing". Devanagari-spelled Arabic words (lines 71-80) are the likeliest to fail that check, since Whisper will write them differently. Suggest: for role ucharan, check only that the line is not silent / lasts about the word count, or accept after the first take and let Munshi listen; do not spend retry money on them. Cost is small (10 short lines), stays far under the Rs120 cap; free key first (RULES 15).
- The old 5:30 video (ckcufoYVPH8, private, `long/output/upload_result.json` exists) is the OLD format. The new build is a replacement: Sanchalak/user must decide update/replace in Studio; Munshi's duplicate guard will refuse a second upload while upload_result.json exists. Not a script issue.

### Fixes list
1. (free, before build) images.json: remove `05_dawn_horizon_c` (line 18) or set `start: {line: 81}`.
2. (free, optional) SOURCES block: add the UCHARAN source line.
3. (free, optional) move line 70 after line 9 for first Arabic ~0:35; otherwise accept ~0:42.
4. (cosmetic) refresh stale times in the HEADER/SAWAAL table; optional "फ़िल अर्ज़" in line 74.
