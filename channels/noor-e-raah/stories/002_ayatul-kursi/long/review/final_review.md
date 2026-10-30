# Final review - 002 Ayatul Kursi long (Munshi, 2026-10-29)
VERDICT: FIX (not uploaded)

Verified OK: 1920x1080 / 30 fps / H264+AAC / 332.3 s; -14.2 LUFS, true peak -1.6 dBFS; no .part file; Arabic ASS text == sources.json (whole ayah 4 lines joined == Tanzil string, incl. yaودُهُۥ); whole-ayah frame (35-44 s) clean, 4 lines above subtitles; ring and bedtime images clean (lamp out, no person); chapters match timeline (0:00, 0:16, 0:35 ... 4:45); music credits (Soaring, River Flute) + swoosh/ambience CC0 in assets_license.csv; name_guard OK; no playlist_id; category 27, kids false; srt 34 cues.

1. MAJOR - Hindi burned subtitles/cards are mis-shaped (libass): i-matra misplaced or lost ("बिस्तर" shows as "बस्ितर", "कि" shows as "क" + gap in frames at 262 s and 193 s, "मुताबिक़" -> "मुताबक्कि़" at 180 s), halant visible in "अल्लाह", "सल्लल्लाहु", "कुर्सी" (title card too). Wrong spelling on screen across the whole video. Fix (free): find why Mukta Bold/libass does not shape (font file or libass build; test one ASS line with another Devanagari font e.g. Noto Sans Devanagari / ass shaping), re-render captions text, re-measure.
2. MAJOR - two-line subtitle boxes overlap (180 s: line-1 and line-2 background boxes overlap vertically; also 262 s three lines wide, very long - 3 lines of ~75 chars). Shorten/wrap at ~2 lines, line spacing so boxes do not overlap.
3. MINOR - thumbnail chip and hook: "क़ुरआन" nuqta lost ("कुरआन"), halant visible in "कुर्सी"; same shaping cause as item 1.
4. MINOR - metadata: description has English "Images and voices: AI-generated." (channel note asked Hindi line 'Is video ke drishya aur awaaz AI ki madad se banaye gaye hain.'); contains_synthetic_media false per user decision.
5. NOT DONE (blocked by FIX): Whisper spot-check of 5 lines, line 57 listening, swoosh/gap audio check. Do them on the re-rendered video.
