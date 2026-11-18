# 063 Tasks in Gemini (AI news deep dive Long) - self-review 2026-11-18

Final file: output/long_final_fixed.mp4 (388.8 s = 6:29, 1920x1080, -14.6 LUFS, true peak -1.3 dBTP).

## Round 0 (pre-render, sheets every 5 s: review/sheet_00..03.png)
1. 0-5 s hook: "FREE in 6 countries" chip overlapped the official toggle crop -> crop 1180 -> 1020 px, chips moved to x 1500. fixed
2. 105-106 s who_d: empty opening until the first tile -> tiles shown dimmed from beat start, lit at their word. fixed
3. 165-167 s ex1_c: empty Summary card -> summary lines from beat start + 0.4 s. fixed
4. 208-211 s ex3_a: only the headline for ~2.5 s -> "goal" chip at beat start + 0.2 s. fixed
5. 225-227 s ex3_b: empty right half until the PDF word -> PDF card at min(word, beat + 1.0 s). fixed
6. 240-246 s safe_a: empty card ~6 s until "hardware-isolated" -> VM drawing from beat start, highlighted at the word. fixed
7. 278-284 s us_a: empty ~5 s until "phone" -> 4 tiles dimmed from beat start, lit at their words. fixed
Also: help-page crops had a side drawer over the text (900 px capture) and the release notes page came in another language -> recaptured at 1280 px with ?hl=en. fixed

## Round 1 (full render, sheets every 5 s: review/final/csheet_01..04.png; action frames: review/actions.png)
8. Loudness -15.3 LUFS (outside -14 +-1) -> two-pass loudnorm audio remux (video copied): -14.6 LUFS, TP -1.3. fixed
9. 195-200 s ex2_b: lower half empty ~4 s while the prompt types -> dimmed "Schedule" chip + briefing skeleton from beat start; range 180.0-208.5 re-rendered and spliced (tools/splice_video.py), checked frames 179.9 / 196.0 / 208.6 (review/splice_check.png). fixed

## Checks (PASS)
- Every spoken action on screen at its word (review/actions.png): tap Task 129.1, Submit 140.4, Take over 147.5, Confirm 179.1, Monday 187.6, Pause 205.2, Resume 207.1, Download 228.5, Take control 276.2, US only 295.6, 15 tasks 310.5, Turn off 347.1, Follow 384.8, India 12.7 / 82.3.
- Hindi captions via Chromium, matras correct in all sheets; no caption-only frame > 0.5 s.
- No overlaps / cut text in the final sheets (minor: cursor tip covers part of the "Turn off" button for ~0.5 s, accepted).
- Length 6:29 (5:00-8:00), 1110 words, chapters in the description match scene starts.
- Facts: all spoken claims in review/facts.md F1-F24 with 2+ official sources (file list detail only S2, noted). Illustrations labelled on screen.
- No real person / account / order / payment shown. name_guard OK.
