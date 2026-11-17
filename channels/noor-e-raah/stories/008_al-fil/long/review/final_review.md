# 008 Al-Fil — Munshi FINAL R1 (Long) + Short quick check — 2026-11-17

VERDICT: PASS-WITH-NOTES (0 BLOCKER, 0 MAJOR; 1 free FIX done by Munshi: chapters)

## Long (long/output/008_al-fil_final.mp4)
- ffprobe: 1920x1080 h264 30 fps, AAC 48 kHz stereo, 234.0 s (3:54). ebur128: -14.5 LUFS, TP -1.5 dBFS, LRA 7.1.
- Arabic on screen (_text.ass, libass Amiri): full surah block (3 rows joined) + 10 jumla blocks == research/sources.json ayat
  bytes (code compare); sources.json 105:1-5 == Tanzil quran-uthmani.txt lines 6189-6193 (Bismillah prefix stripped), sha256 ok.
- Ucharan on screen 10/10 == research/ucharan.md Devanagari column.
- One narrator: lines.json 42/42 speaker ustaad (Charon); no SAWAAL, no question lines (line 15/25 = Quran tarjuma),
  no tilawat disclaimer (0 hits for तिलावत/क़ारी in srt).
- SRT: 42 cues, UTF-8, text == lines.json 42/42, times == timeline.json; first word 0.8 s.
- Music: Soaring 0.8-33.1 s -> crossfade -> River Flute to 233 s, continuous, no gap at ayat; breeze ambience; swoosh per ayah.
  Stem method: voice -18.5 LUFS vs music -36.2 LUFS = 17.7 LU (target ~19) -> MINOR.
  All tracks/sfx/fonts in shared/assets_license.csv; Kevin MacLeod CC BY credits in description.
- Frames: contact sheet review/final_frames/contact_4s.jpg; zooms review/final_frames/zoom_p0*.jpg, zoom_p11*.jpg.
  New images p01/p05/p06/p11: ordinary fictional people (RULES 2h), modest dress (women in hijab), no Nabi/Sahabi/angel,
  no halo/wings, no text, no domes/minarets. Hands checked: p01 elder hands 5 fingers, p05 hands ok, p06 pointing hands ok;
  p11 hands are never on screen (only top-left crops used). Shan-e-nuzul/intro/seekh = places only (RULES 2). No dua scene.
- Thumbnail v3C: 1280x720, Amiri title + Mukta Hindi, matras ok, bottom-right empty, text != title.
- upload.json: title 88 chars, description 1.9k, 3 hashtags, tags 208 chars, Sources + Tanzil CC BY 3.0 + bhaavarth line +
  music credits + AI line, contains_synthetic_media true, made_for_kids false, privacy private, no publish_at.
  name_guard OK (long + short upload.json).
- FIX done (Rs0): chapter "0:00 शुरुआत" was only 8 s (YouTube needs >= 10 s per chapter, otherwise no chapters at all) ->
  merged into "0:00 शुरुआत और सूरह का परिचय". All chapter times match timeline.json.

## Shan-e-nuzul statements (RULES 3)
- [N1] line 8/12: no separate sabab-e-nuzul; surah refers to Ashab al-Fil; Ibn Ishaq via Ibn Kathir: reminder to Quraysh — Ibn Kathir (EN), Tabari, Qurtubi — maana hua.
- [N3] line 9: Abraha, ruler of Yemen, set out with an elephant and army to destroy the Kaaba — Ibn Kathir (EN), Tabari, Qurtubi, Ma'ariful — maana hua (church reason left out = ikhtilaaf, not in video).
- [N5] line 10: the elephant stopped and sat down — Ibn Kathir (EN), Tabari, Ma'ariful, Qurtubi — maana hua.
- [N2] line 11: the year called Aam al-Fil — Ibn Kathir (EN), Qurtubi, Ma'ariful, Alim — maana hua (gap years = ikhtilaaf, not in video).
- Links: research/dossier.md section "Surah parichay + Shan-e-Nuzul", research/sources.json source_keys. (Checked against dossier; sources opened at script SURAH CHECK 2026-11-14.)

## Short (shorts/short.mp4)
- 1080x1920 h264 30 fps, 41.4 s, -14.5 LUFS, TP -1.6 dBFS.
- Hook: Whisper first word 0.74 s ("एक लश्कर हाथी ..."); first frame = surah title card, no caption in first 1 s.
- 105:5 complete: jumla 1 + jumla 2 Arabic (Long frames, Tanzil bytes) + both bhaavarth + both matlab lines.
- End: Whisper of last 5 s ends "पहली सीख ... अल्लाह के सामने कुछ नहीं" at 41.04 s, nothing of line 64 after it. Start: no cut.
- Subtitles ~69% height, label ~18% (inside 15-85%). Title 68 chars with #shorts. LONG_ID placeholders replaced after the Long upload.

## MINOR (carry_over)
1. 105:5 blocks (Long 3:04-3:31 and the Short body): p11 crops (fx 0.25/0.15, zc 1.7) cut out the hands + chaff; the screen shows blurred villagers and a little straw — weak image/line match. Next time crop on the hands (fx ~0.6, fy ~0.5).
2. Music 17.7 LU under the voice (target ~19).
3. Short 41.4 s is over the shared 40 s profile; kept because RULES 2b (complete ayah) wins and Noor Shorts of 54-70 s were accepted before.
4. Short Arabic small (Long frame scaled to 1080 wide), as in 011.
5. p05 (kneeling man in rich robe at fallen stones) may be read as Abraha; Abraha is not a Nabi/Sahabi/Quran-named person, so allowed — note only.
6. No playlist id in upload.json (as 007; channel.json playlist id looks short/unverified).
