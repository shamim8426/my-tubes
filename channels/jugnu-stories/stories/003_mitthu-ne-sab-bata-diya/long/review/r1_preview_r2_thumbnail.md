# Munshi — 003 long_02 — 2026-10-19 (preview R1 + thumbnail R2)

## Long thumbnail R2 — PASS
- R1 MINOR fixed: shared/assets_license.csv row 84 = long/output/long_02_thumbnail.png (own Gemini art + Mukta libass + logo_horizontal, Rozha One/Mukta OFL). Row 85 = Short A cover (checked too).
- Thumbnail file unchanged since R1 (1,219,227 B, 17:08). All R1 PASS items stand.

## Long 02 PREVIEW R1 — FIX (1 BLOCKER, 4 MINOR; all free)
File: long/output/long_02_preview.mp4 — 960x540 h264 yuv420p 24 fps + AAC 48k st, 291.08 s (target 4:45-5:15 ok).
Line timing re-computed from long_02_work line wavs (trim + gap 0.4 + end hold 1.5) = 291.09 s, matches the file.
Frames: 3 per line (start+0.35 / mid / end-0.3) -> review/r1_preview_3pt_1..8.jpg; mid-line sheet r1_preview_lines_1..4.jpg.

PASS items
- Story = script v3: 57 lines, speaker/text/scene identical to script.md; scene images match the action.
- Section 13: first word 0.00 s; intro (lines 1-2) ends 8.43 s; Mitthu "सोना चोरी!" on screen from 0 s (title/thumbnail promise kept); Sona missing at 32.4 s; last spoken line = question to viewers (283.3-289.6 s).
- Audio: -13.9 LUFS / -1.4 dBTP; music 12.9 LU under voice (stem method, speech sections); per-speaker voices as lines.json.
- Captions (.srt): 221 cues, UTF-8, text per line = lines.json exactly for all 57 lines, shortest cue 0.46 s, last cue 289.59 s. All 57 lines timed PROPORTIONALLY (Whisper runs on --final) -> re-check at final.
- Copyright: 5 music (Monkeys Spinning Monkeys, Life of Riley, Investigations [tension/], Dreams Become Real, Peaceful Desolation; Kevin MacLeod CC BY 4.0, attribution_text present) + 2 SFX (Freesound CC0) + Mukta OFL all registered; credits are added from the register at --final -> verify in long_02.txt.
- Metadata: title 54 chars (hook in first 40), desc 352, 5 hashtags, 18 tags 267/500, no kids wording, no cat/twist in title/desc/tags.
- Paid files: images/ + audio/ unchanged by the build (newest image 17:06 = logged regen, builds 17:12).

BLOCKER
- B1 line 34 raghu (161.08-164.68 s): first ~1.9 s (160.98-162.98) is the scene-17 close-up at x0.3 = Gupta/Sharma/Golu, Raghu not on screen. Fix: lines.json line 34 "shot": [0.72, 0.5, 1.7].

MINOR
- M1 shots > 8 s (RULES 13): line 45 dadi 216.77-228.51 (11.7 s, one close-up), line 54 dadi 266.60-277.31 (10.7 s), line 35 dadi 164.98-173.16 (8.2 s). Fix: "shots" split into 2 close-ups (e.g. Dadi close then Dadi+Golu/Pandey wider).
- M2 line 4 sharma (17.42-20.52): last 1.45 s (19.07-20.82) is the cat close-up, Sharma only legs. Fix: line 4 "shots": cat close ~1.5 s, then [0.55, 0.35, 1.7] Sharma.
- M3 music dropout under dialogue (RULES 3): music stem is digital silence 256.5-257.2 s during line 51 Pandey. Cause: seekh/Peaceful_Desolation.mp3 starts with 2.23 s silence (jaadu/Dreams_Become_Real.mp3 has 1.57 s -> dip to -50 dB at 165.9 s). Fix: start those tracks after their lead-in silence (offset ~2.2 s / ~1.6 s; ideally skip lead silence in build_audio for every track).
- M4 end screen (RULES 13): last 20 s = 271-291 s carry Dadi's moral + the viewer question; end_hold only 1.5 s, so end-screen elements will sit over the speakers. Fix: end_hold ~6-8 s on a calm wide shot (length stays < 5:15) and keep scene 29/30 speakers in the left ~60%.

Notes (no action): Pandey talks with the whistle in his mouth (image 15, lines 26-30); line 43 Dadi voice over the clue insert (no people, ok); narrator atempo 0.8 = taste; preview 24 fps by design.
STOP conditions: none hit. Cost of fixes ₹0.
