# 011_mehmaan-aur-bujha-chiraag — Munshi FINAL R2 (Long fixes + Short quick check), 2026-11-17

VERDICT: PASS-WITH-NOTES (0 BLOCKER, 0 MAJOR). Auto-mode STOP: none. Rs0. Not uploaded (as asked).

## Long (output/video.mp4, built 03:27 after script.json 03:14)
- 1920x1080, 30 fps, 247.48 s; ebur128 I -14.2 LUFS, TP -1.5 dBFS, LRA 3.5. SRT 36 cues, now `HH:MM:SS,mmm`.
- B1 fixed: line 4 `sfx: []`; no `camel_bell`, `254270`, `93340` anywhere in script.json.
- New beds by CREDITS.md title: night_crickets_268962 = "Cicada Insects" (harryScary, CC0), market_crowd_139981 = "Market environment" (Oscar de Avila, CC0). Whisper small on both: 0 speech segments. All 11 sfx/amb in use checked by title: steps, cloth rustle, door creak, desert wind, leaves, courtroom murmur (faint, -14 dB), fire; no music/horn/tune by name.
- Frames (start + later in clip): L4 empty road to town; L7 = 009/19 night road, no person; L17 crop: both backs, clay lamp, no glass lantern, faces hidden; L18 = 009/18 clay lamp + bag, night interior, no glass; L23 = 002/07 rooftops, one lit window; L28 = 001/11 open door at sunrise, no person; L30 card border straight (motion false), Arabic == Tanzil; L33 = 010/19 palm-roof stalls, no lanterns, no castle, no people.
- Ayah `وَيُؤْثِرُونَ عَلَىٰٓ أَنفُسِهِمْ وَلَوْ كَانَ بِهِمْ خَصَاصَةٌ` == Tanzil quran-uthmani 59:9 substring at offset 154, ends before `وَمَن` (full clause).

## Short (shorts/short.mp4)
- 1080x1920, 30 fps, 54.04 s (< 60), AAC 48 kHz stereo, I -14.3 LUFS, TP -4.3 dBFS.
- Lines 1,15,17,21,25,28,29,30 (Long text unchanged, every line whole). Hook = line 1 from 0.0 s (guest from behind at a lit door); first 1 s without caption (cover frame).
- Captions bottom at ~1420-1500 px (74-78%); src tags at 345 px (18%); "पूरी कहानी" at 300 px (15.6%); ayah 420 px, ayah src 600 px. No overlap of tags and captions; all inside 15-85%.
- Ayah in work_short/subs.ass == script.json ayah_ar == Tanzil bytes (1 occurrence); on screen whole, x ~335-750, not cropped.
- Depiction: no Prophet, no angel; couple/wife/child/guest only from behind; no faces.
- short.srt 8 cues, ends 53.99 s, text == script lines.
- upload.json: title 60 chars incl. #shorts; Tanzil CC BY 3.0, Quran 59:9, Bukhari 3798/4889/2325, Muslim 2054, AI disclosure, music credits; synthetic true; made_for_kids false; private; channel_id UCmw4fs9jN49GTq7wVSdYm6w; name_guard OK. LONG_URL x2 = placeholders, fill after the Long upload.

## MINOR (carry_over.md, no regen)
1. Short ayah card: Arabic 84 px reads small with a large empty card below (next time ~110-120 px, text centred).
2. L25 wall lanterns (modern look) also show in Short ~32-36 s; L15 daylight door also in Short ~10-15 s.
3. R1 left-overs: L11/L12 same image, L14 pose, L24 daylight, L8 fortress, L3 tiled roofs.
