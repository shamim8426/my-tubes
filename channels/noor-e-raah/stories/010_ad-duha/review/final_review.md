# 010 Ad-Duha: Munshi FINAL R1 (Long + Short quick check), 2026-11-19

VERDICT: **FIX** (1 MAJOR, free: music bed too loud; Long + Short re-mix, Rs0). 0 BLOCKER. Everything else PASS.
STOP condition: none (no balance/copyright issue; channel_id UCmw4fs9jN49GTq7wVSdYm6w == channel.json; Soaring CC BY 4.0 in assets_license.csv).

## Opened and measured
- Long output/video.mp4: 1920x1080, 30 fps, H.264, AAC 48 kHz mono, 4:54.5 (RULES 2n 4:00-5:00 OK). -14.4 LUFS, LRA 2.6, **TP -0.6 dBFS**.
- Short short/output/short.mp4: 1080x1920, 47.7 s (<60), -14.4 LUFS, TP -1.4.
- Arabic: 11/11 ayah strings in work/subs.ass == script.json `ar` == tanzil_93.json (sha256 ok) == raw quran-uthmani.txt 93|1-11 (93:1 = line minus Bismillah). Zoom sheet review/final/ayah_cards_zoom.jpg: Amiri, harakat on letters, dark outline, nothing cut, all 11 readable (bright sky 93:3/93:4/93:8 too).
- Ucharan on screen (Tr events) 11/11 == ucharan.md Devanagari column (+ "।").
- SRT: 56 cues == 56 script lines, text identical, no overlaps, first 0.00, last ends 294.39. voice.wav: no line has speech within 80 ms of its cue edges (no cut word). Whisper small (my run on the final mix) L9, L28, L45, L53, L56: all words present, last word ends 0.5-1.4 s before cue end.
- One narrator (Charon, script.json voice), no "?", no disclaimer, no teaser; ends on the 3-line summary (L54-56).
- Frames, one per line (review/final/sheet_long_1-3.jpg): ayat 3-8 (L19-L41) have NO person; Nabi lines L7 (empty roof + mat), L28-29 (stars sky), L32-33 (lamp doorway), L40 (well) have no person; L45 man + child = the carer (as R2). Faceless storybook, blank heads, modest dress. No Nabi/Sahabi/angel, no dome/minaret, no AI letters. R2 image fixes (r_04b_light_sky, r_10b_stars_sky, 7 crops) are in the video.
- Thumbnail = v3C (cmp), 1280x720, 225 KB; "तुम्हारे रब ने छोड़ा नहीं" = 93:3 (honest), readable at 160x90, bottom-right clear.
- upload.json: title 83 chars, description 1841 (Tanzil CC BY 3.0 2007-2026 + link, bhaavarth basis, tafseer list, hadith numbers, Soaring exact CC BY 4.0 credit, OFL fonts, AI note), 14 tags (228 chars), made_for_kids false, synthetic true, privacy private, no publish_at (api_audited false), channel_id OK. name_guard: OK.
- Short: hook at 0 s (93:1 card + "वज़्ज़ुहा" from ~0.25 s), ayat 93:1-3 complete (= Long L12-21, ends on L21's full sentence), voice ends 47.11 s, fade starts 47.38 s (last word intact), captions 73-77% height inside 15-85%, Arabic whole in the panel, blurred bg from crop 330-890 (no Arabic; only an unreadable blur of the 93:x label at the top edge), cover.jpg 1080x1920 = frame at 1.0 s with the 93:1 card.
- Cost: cost_log 82 rows for 010 = ~Rs8.76 incl GST (TTS only). Cap OK.

## FIX (MAJOR, free) - music bed far too loud in every pause
Soaring.mp3 is -18.8 dBFS RMS; River_Flute (009) is -28.9. script.json kept music_vol 0.5, so the bed is ~10 dB louder than 009.
Measured (mix level in 0.25 s windows where work/voice.wav is silent vs speech windows): **010 bed only 4.2 dB under speech** (009: 20.1 dB; RULES 1c ~19 LU, 2i "never competing with the voice"). The sidechain releases in each of the ~60 pauses, so the music swells to almost voice level between lines (pumping).
Exact fix:
1. script.json `music_vol` 0.5 -> **0.16** (-10 dB; matches 009's effective level).
2. Re-run the Long mix with history_build.py (video/clips unchanged), then the same loudness step, but limiter ceiling so **TP <= -1.0 dBTP** (now -0.6).
3. Re-run short/make_short.py (re-cuts from the new Long; nothing else changes).
4. Builder checks: Long + Short -14 +-1 LUFS, TP <= -1.0; bed in voice-silent windows >= 16 dB under speech median (same method), no silence > 1 s.
After that a quick Munshi audio-only verify (~5 min), then upload. Images/srt/thumbnail/upload.json need no change.

## MINOR / notes (carry_over, no rebuild for them)
- L28 "हाथ उठाए": Whisper (builder's run and mine) hears "हाथ अथ उठाए" (possible small stutter). Builder accepted by length; listen once at 2:15-2:26; if it is a stutter, re-TTS L28 (free key first).
- First ayah at 0:54.6 (learnings 30-40 s).
- Shots > 8 s on one move: L45 11.2 s, L28 10.1 s, L32 ~9 s.
- 93:9 card: the Src label "सूरह अद-दुहा 93:9" sits over the white blank head of 11_orphan_care (low contrast); push the head lower / use the crop.
- Thumbnail label "ग्यारह आयतें" is too small at 160 px (Note).
- 014_ashab-e-kahf (already uploaded private) has the same loud bed (Quietude -17.5 dBFS RMS, music_vol 0.5): bed only 3.7 dB under speech. Re-mix + re-upload is the user's call.
- Rule for next videos: set music_vol per track (Soaring/Quietude ~0.16, River_Flute 0.5), or normalise the 3 tracks to the same RMS once.

## Shan-e-nuzul / fact lines
Unchanged from script R1/R2 (review/script_review.md table); text in the video == script.json (srt 56/56).

## R2 audio-only verify, 2026-11-19: VERDICT **PASS** (MAJOR fixed; upload OK)
- script.json music_vol = 0.12 (0.16 gave 15.9 dB per builder). Long re-mixed, +3.3 dB + alimiter.
- Long: 1920x1080, AAC 48 kHz, 4:54.5, **-14.5 LUFS, TP -1.5 dBFS**; no silence > 1 s under -45 dB (bed continuous). Bed in voice-silent windows (work/voice.wav < -60 dB, 0.25 s) **18.3 dB under speech** (bed -31.8, loudest pause window -19.3); RULES 1c ~19 OK. End fades smoothly to -49 dB.
- Short: 1080x1920, 47.7 s, **-14.2 LUFS, TP -1.4**; bed 19.2 dB under speech; tail after the last word ~-31 to -42 dB (no swell), head fades in, voice from ~0.3 s.
- Video unchanged: L19 frame at 88.05 s identical to the R1 frame (PSNR inf). srt/thumbnail/upload.json unchanged.
- R1 MINORs stay in carry_over (L28 listen, first ayah 0:54, >8 s shots, 93:9 label, thumbnail label).
