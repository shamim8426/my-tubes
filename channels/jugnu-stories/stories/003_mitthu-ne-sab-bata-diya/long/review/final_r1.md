# Munshi — 003 long_02 — 2026-10-19 — FINAL R1 (pre-upload) — FIX

File: long/output/long_02.mp4 — 1920x1080 H.264 High yuv420p tv/bt709 30 fps + AAC LC 48 kHz stereo, 296.59 s (preview 296.58 s, 0%). 144.0 MB.

Verified (PASS items)
- Loudness (ebur128 on the mp4): -14.0 LUFS I, LRA 6.1, true peak -1.4 dBFS.
- Music under voice (stem method, 0-289.6 s): voice.wav -15.7 LUFS vs music.wav -28.5 LUFS = 12.8 LU (long range ok).
- Frame per line: output/long_02_framecheck.png (57 frames) = right speaker on screen for every line, same shots as preview R2.
- Paid sources: git status clean for story images/, audio/, characters/ and channel characters/; thumbnail unchanged since commit c548bb0 (1280x720). No new cost_log rows after 17:07 (story Rs103.16/130).
- .srt: UTF-8, 226 cues, no overlaps, no cue < 0.4 s, first cue 0.00 s, last ends 289.59 s.
- Metadata (meta.json = long_02.txt): title 54 chars (hook in first 40), desc 352 + credits, 5 hashtags, 18 tags (267/500), no kids wording, no < >. 5 CC BY tracks used (comedy/khushi/tension/jaadu/seekh moods in lines.json) = 5 exact Incompetech credits; SFX comedy_sting_731262 + tension_sting_578351 = CC0 rows 45/47; Mukta/Rozha OFL, scene images/TTS/thumbnail own Gemini rows 61/79-84.

Problem (MINOR, R1 -> FIX, free)
Builder said "Whisper timing", but 7 of 57 lines fell back to PROPORTIONAL timing (Whisper coverage <75%): lines 9, 22, 41, 48, 51, 53, 57. Audio itself is complete (Whisper on chunks hears all words). Inside lines 22 and 57 the pauses make proportional cues early (RULES 4 limit 0.3 s):
- line 22 (starts 104.34 s; speech segments 0-0.86 / 1.72-4.98 / 5.64-5.92 / 6.40-7.28 s):
  cue 85 "सबके कहने से" 105.095 -> should start 106.06 (0.97 s early)
  cue 86 "बात सच नहीं" 106.731 -> 107.31 ; cue 87 "हो जाती।" 108.241 -> 108.46 (end 109.32)
  cue 88 "चलो," 109.373 -> 109.98-110.26 (0.61 s early)
  cue 89 "ज़रा देखते हैं।" 109.877 -> 110.74 (0.86 s early), end 111.89 ok
- line 57 (starts 283.33 s; speech 0-1.24 / 2.06-6.14 s):
  cue 223 "— क्या आपने" 284.871 -> 285.39 (0.52 s early); cue 224 285.93 -> 286.31; cue 225 286.99 -> 287.22; cue 226 288.338 -> 288.39, end 289.47
- lines 9, 41, 48, 51, 53: cue starts within 0.3 s of speech, ok.
Fix (Rs0): re-time those cues in long_02.srt (sidecar only, burn_captions=false, mp4 does not change). Pipeline fix (carry_over): proportional fallback should spread words over VAD speech segments, not the whole clip.

STOP conditions: none. Cost Rs0. Upload not run (needs PASS).
