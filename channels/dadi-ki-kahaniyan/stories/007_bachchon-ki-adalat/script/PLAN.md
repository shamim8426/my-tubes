# Story 007 — production plan (RULES 15, auto)

Approved 2026-10-21 (title 1, thumbnail "फ़ैसला क्या होगा?", no cozy pal, line 37 removed).

## Length
Estimate after the user's cut of line 37: ~3:48 (~227.7 s; range ~3:40–3:54), intro (lines 1–2) ~8.8 s.
Settings: gap 0.35, end_hold 7, narrator 1.0, dadi 0.9, pandey / pandey_soft / sharma_fond 0.95, kids from channel.json.
After TTS: > 3:58 -> end_hold 7 -> 6, then gap 0.33; < 3:40 -> gap 0.45, then end_hold 8. Never cut dialogue or jokes.

## Voices
New style keys in scripts/voices.py (old keys untouched, cache keys of 003–005 unchanged):
`pandey_soft` (Algenib, whispering, amused) for lines 20, 22; `sharma_fond` (Sadachbia, flustered then laughing at
himself) for lines 12, 26, 29.

## Images (Kissago Painted, 1K, refs only for the characters in the scene)
| Item | Count | Est. (actual incl. GST) |
|---|---|---|
| Sharma ji painted sheet (`gen_painted.py sheets --budget=007_bachchon-ki-adalat sharma`) | 1 | ₹6.1 |
| Scene images 1–13 (`gen_scenes.py`) | 13 | ₹78.9 |
| Long thumbnail (`gen_thumb_painted.py`) | 1 | ₹6.1 |
| Short cover (`gen_short_cover.py`) | 1 | ₹6.1 |
| TTS (52 long lines; Short re-uses the long's lines at other speeds -> new TTS only where speed differs) | — | ~₹7–9 |
| **Total** | 16 images | **~₹104–106** (cap ₹110) |
Over ₹110 -> shrink, never stop (RULES 15): image 12 -> crop of 13 (Mitthu drinking at the full bowl), then image 8 ->
crop of 13 (Sharma ji with the cord). Max 1 regeneration per image, BLOCKER only.
Balance before start: ledger ₹176.56 (floor ₹50) -> enough for this story.

## Shots
Camera crops (lines.json "shot"/"shots", shots.json closes) are set after the images exist, by looking at each image.
Every shot ≤ 8 s; lines 14, 17, 29, 39, 43, 44, 48, 54 get two shots. Last 20 s: wide/left-group crops of img 13 only.

## Short A (`shorts/short_01_pande-ji-katghare-me`)
Lines 1, 11, 13, 14, 15, 16, 17, 18; kids 1.05, Pandey 1.0, gaps 0.15/0.30, end card 2 s "पांडे जी को क्या सज़ा मिली?
पूरी कहानी नीचे दिए लिंक पर" -> target 35–40 s. Images 6-crop, 3, 4, 5, 6-crop only (no perch, no bowl). First frame =
Tara with the belan raised. Never: Mitthu's case, the bowl, any verdict, Golu's self-sentence, the moral.

## Publish
`"publish_at": "auto"` (RULES 8): 23 Oct is the first free day. STUDIO ACTION message after the uploads (API unaudited).
