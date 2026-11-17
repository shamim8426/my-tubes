# Self-review: Long 061 usage-limit saving (2026-11-17)

## Round 0 (before the full render): contact sheets every 5 s from the timeline (review/sheet_00..03.png) + check frames (review/fix1.png)
| # | Time | Problem | Fix | Status |
|---|---|---|---|---|
| 1 | 124-166 s (clear) | Whisper base returned 60 of 127 words (17 s gap), every beat of the scene fired ~15 s late, a 25 s static picture | wt_fix.py: Whisper small, beam 5, no previous-text conditioning (126 words, max gap 0.98 s) | fixed |
| 2 | 50-56 s (how_c) | official crop placed at the bottom right overlapped the caption strip, tiles half empty | crop moved to the right middle (1000x420) next to the tiles | fixed |
| 3 | 110-123 s (batch_c) | the 5 separate messages had other equations than the 1-message version (same work must look the same) | both sides now show the same 5 equations | fixed |
| 4 | 220 s (set_b) | about 2 s with only the TIP banner (tools card waited for "Gmail") | card enters at the scene start | fixed |
| 5 | 263-266 s (limit_a) | empty screen under the title until "pehla" | 3 option cards enter at the start, each lights up when spoken | fixed |
| 6 | 275 s (limit_a) | usage-credits crop at y 880 would overlap cards and caption | crop removed (fact stays on card 3, source in description) | fixed |
| 7 | 281 s (limit_b) | blank until "marzi" | official crop on screen from the scene start | fixed |
| 8 | 146 s (clear_c) | empty prompt card ~1.5 s before "manager" | field labels (To/About/Reason/Tone/Length) visible from the start, values fill in when spoken | fixed |
| 9 | upload.json | description had ">" (Settings > Usage), rejected by the uploader rule | written as "Settings me Usage" | fixed |

## Round 1 (finished render output/long_final.mp4, 320.7 s = 5:21)
- Contact sheet every 5 s (review/vsheet_01.png, 64 frames): no blank frame without a picture, no overlap, no cut text, Hindi matras correct in all captions, official crops readable with the yellow phrase.
- Exact frames at the spoken action words (review/actions.png): Usage click 58.5 s, Verified Ultra 46.2 s, 5 -> 1 message 123.2 s, prompt filled 152.0 s, quiz typed 191.4 s, thinking OFF 217.5 s, tools OFF 226.4 s, + New chat 245.8 s, no fixed count 285.6 s, + Follow 317.0 s: all on screen at the word.
- Facts match review/facts.md (20 rows PASS). name_guard OK. Length 5:21 (5:00-8:00 OK).
| 10 | whole video | loudness -15.4 LUFS (outside -14 +-1), TP -1.35 | two-pass loudnorm audio remux, video copied: output/long_final_ln.mp4 = -14.7 LUFS, peak -1.4 dBFS, 320.7 s | fixed |
Result: PASS, upload output/long_final_ln.mp4.
