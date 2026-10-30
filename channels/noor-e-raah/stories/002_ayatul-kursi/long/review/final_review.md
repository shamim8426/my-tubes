# Final review - 002 Ayatul Kursi long (Munshi, 2026-10-29)
VERDICT: FIX (not uploaded)

Verified OK: 1920x1080 / 30 fps / H264+AAC / 332.3 s; -14.2 LUFS, true peak -1.6 dBFS; no .part file; Arabic ASS text == sources.json (whole ayah 4 lines joined == Tanzil string, incl. yaودُهُۥ); whole-ayah frame (35-44 s) clean, 4 lines above subtitles; ring and bedtime images clean (lamp out, no person); chapters match timeline (0:00, 0:16, 0:35 ... 4:45); music credits (Soaring, River Flute) + swoosh/ambience CC0 in assets_license.csv; name_guard OK; no playlist_id; category 27, kids false; srt 34 cues.

1. MAJOR - Hindi burned subtitles/cards are mis-shaped (libass): i-matra misplaced or lost ("बिस्तर" shows as "बस्ितर", "कि" shows as "क" + gap in frames at 262 s and 193 s, "मुताबिक़" -> "मुताबक्कि़" at 180 s), halant visible in "अल्लाह", "सल्लल्लाहु", "कुर्सी" (title card too). Wrong spelling on screen across the whole video. Fix (free): find why Mukta Bold/libass does not shape (font file or libass build; test one ASS line with another Devanagari font e.g. Noto Sans Devanagari / ass shaping), re-render captions text, re-measure.
2. MAJOR - two-line subtitle boxes overlap (180 s: line-1 and line-2 background boxes overlap vertically; also 262 s three lines wide, very long - 3 lines of ~75 chars). Shorten/wrap at ~2 lines, line spacing so boxes do not overlap.
3. MINOR - thumbnail chip and hook: "क़ुरआन" nuqta lost ("कुरआन"), halant visible in "कुर्सी"; same shaping cause as item 1.
4. MINOR - metadata: description has English "Images and voices: AI-generated." (channel note asked Hindi line 'Is video ke drishya aur awaaz AI ki madad se banaye gaye hain.'); contains_synthetic_media false per user decision.
5. NOT DONE (blocked by FIX): Whisper spot-check of 5 lines, line 57 listening, swoosh/gap audio check. Do them on the re-rendered video.

---
# R2 (Munshi, 2026-10-30) - VERDICT: PASS (not uploaded)
Frames checked in the new final (1, 20, 40, 90, 150, 180, 195, 262, 305, 331 s + thumbnail, zoomed on nuqta): Hindi now shaped correctly (Pillow+raqm) - i-matra, nuqta (क़ुरआन, मुताबिक़, बक़रह, अज़ीम, रोज़), बिस्तर, कुर्सी, अल्लाह, सल्लल्लाहु all correct, no visible halant. Title card, bhaavarth label, 1-line/2-line (180 s) and longest (262 s) subtitles: one merged box, no overlap, no collision with Arabic (ayah block sits above), inside safe area. Cards (62-64) and end card readable. Thumbnail: chip + hook + "आयतुल कुर्सी" correct; bottom-right empty.
Measured: 1920x1080 30fps 332.3 s, -14.2 LUFS, TP -1.6; music stem continuous (no dips >6 dB except start/end fades); dry-run OK (schedule 2026-10-30 19:00 IST decision, kids false, thumbnail + srt attached). Description now has Hindi AI-disclosure line (English line also remains - harmless).
Whisper (small) spot-check of lines 3, 21, 30, 57, 64: audio matches script text (small-model spelling noise only); line 57 (Ubayy ibn Ka'b) audible and correct.
MINOR (carry_over, no rebuild): Whisper model small has misspellings only; none in video.
