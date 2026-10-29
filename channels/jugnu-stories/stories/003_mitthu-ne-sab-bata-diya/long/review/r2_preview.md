# Munshi — 003 long_02 — 2026-10-19 — PREVIEW R2 — PASS

File: long/output/long_02_preview.mp4 — 960x540 h264 24 fps + AAC, 296.58 s. Line timing re-computed from long_02_work wavs (trim + gap 0.4 + end_hold 7.0) = 296.59 s, matches.
Frames: review/r2_preview_a.jpg, r2_preview_b.jpg, r2_preview_end.jpg (timestamps on each frame).

R1 items
- B1 line 34 raghu (161.08-164.68): Raghu (blue check shirt, cycle, cans) on screen at 161.2 / 162.5 / 164.4 s. FIXED.
- M1 shots > 8 s: line 35 Dadi close 165.08-169.08 then Dadi+Pandey wider to 172.86; line 45 Dadi close 216.87-220.87, paw-print thali insert to 224.87, two-shot to 228.21; line 54 Dadi close 266.7-271.7, wider to 277.01. Longest shot now ~7 s (end wide). FIXED.
- M2 line 4 sharma (17.42-20.52): cat close 17.42-18.92, Sharma face/body on screen 19.2 and 20.3 s. FIXED.
- M3 music stem (silencedetect -50 dB, d 0.2): no silence at ~165.9 s or ~256.5 s any more; RMS 164-169 s and 254-259 s steady -29..-38 dB. Build log path: leading_silence() skips 1.57 s / 2.24 s. FIXED.
- M4 end: end_hold 7.0; line 57 close 283.33-289.6, then calm wide 289.6-296.6 (Dadi, Golu, Mitthu left/centre, Sharma + Sona on chair right, nothing essential). Lines 54-57 speakers (Dadi, Golu, Mitthu, Dadi) sit in the left ~60%. FIXED.

Re-measured (because the audio changed): -14.0 LUFS / -1.4 dBTP; music 12.8 LU under voice (voice stem -15.7 vs music stem -28.5 over 0-289.6 s); .srt 221 cues, last cue 288.34-289.59 s.

Notes (no action)
- Short music rests: stem dips below -50 dB for 0.2-0.75 s at e.g. 33.7, 38.8 (0.75 s), 53.3, 122.7, 127.8 s. Source = quiet staccato passages of the comedy track after the -13 dB gain (max -54.6 dB, not digital silence, no cut), so not the R1 M3 fault.
- A long FINAL (long_02.mp4) already exists; this R2 covers the PREVIEW only. Final needs its own Munshi final review (Whisper timing, credits in description) before upload.
STOP conditions: none. Cost ₹0.
