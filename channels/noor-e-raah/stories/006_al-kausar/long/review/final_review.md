# 006 al-kausar LONG - Munshi FINAL review (R1) - 2026-11-12

VERDICT: PASS-WITH-NOTES (0 BLOCKER, 0 MAJOR, 3 MINOR)

Verified myself:
- Arabic: 4 Arabic blocks in lines.json compared to a fresh Tanzil Uthmani download (tanzil.net): 108:1-3 byte-equal (Bismillah prefix of 108:1 correctly stripped); the full-surah line == the 3 ayat joined by spaces.
- Voice: all 24 spoken lines are speaker "ustaad" only (one narrator). No "?" question lines, no SAWAAL, no tilawat disclaimer in script/srt (RULES 1d).
- TTS lines 23 and 32 (re-transcribed with faster-whisper small, hi + ur; I cannot listen to audio): 23 = "...tabri (heard as ttori) ke mutabiq ye baat ek namaz ya ek qurbani taksimit nahi, ata aam hai, isliye ibadat ka hukm bhi aam hai" - all words present, 9.2 s (normal for 23 words); same "tabri" sound is heard correctly as "tabri" in lines 9 and 31 by the same voice. 32 = all words incl. "liye" present (Urdu transcript: "...sirf isi rab ke liye hai, kisi aur ke liye nahi..."). Accepted as Whisper-small spelling variants. Suggest a human ear on line 23 "tabri" only if time allows.
- Video: 1920x1080 h264 30fps, 208.6 s (3:28.6, under 4:00 long max), AAC 48k; integrated -14.0 LUFS, true peak -1.9 dBFS, LRA 5.6.
- Frames (JPG in review/f/): opening title (Arabic title + Hindi + series, caption); 10-word full-surah Arabic line (t=25 s): all words and marks inside the frame, closest mark ~35 px from the left/right edge - tight but not cut; ayah 3 (t=105 s) clean; subtitle bands on 1080p inside safe area; seekh card frame with Hindi ok. No human face/figure, no Nabi/Sahabi image.
- SRT matches script text. Chapters (timeline.json: ayah fades 74.5 / 101.3 / 130.3 s, seekh 177 s) used in upload.json: 0:00, 0:09, 0:18, 0:31, 1:14, 1:41, 2:10, 2:57 (ascending, first 0:00, each >10 s).
- upload.json: title 95 chars (script option 1), sources block (Tanzil CC BY 3.0, tafseer list, Muslim 400a, music CC BY 4.0, Amiri/Mukta), no questions, first comment is a statement (no question). name_guard OK, dry-run OK. contains_synthetic_media set TRUE (AI narrator + AI images; channel.json default is false - Sanchalak may confirm).
- Thumbnail choice: v3C (hook "ताना दिया गया — जवाब ये उतरा" large, Arabic title top-left, chip + surah name, no face, river/dawn scene). v3A has a bigger surah title but the hook is small; C is the right pick for curiosity + 4 big words. Wallpaper free Cloudflare (Rs0).
- Cost: TTS Rs 9.08 incl GST (free key exhausted -> paid fallback, logged); images Rs 0 (17 clips from 10 library images, 0 new); thumbnail Rs 0. Well under Rs 100/120.
- Sources/facts: script R2 already PASS (SURAH CHECK); Kaarigar PC checks (Tanzil bytes, Muslim book 4 hadith 56 = sunnah.com 400a) reported; I re-did the Tanzil byte check.

MINOR (go to carry_over, no regeneration):
1. Line 31 repeats line 23's sentence word for word ("तबरी के मुताबिक़ अता आम है, इसलिए इबादत का हुक्म भी आम है") - repetition in seekh.
2. 10-word Arabic line is ~35 px from the screen edges (Kaarigar noted ~30 px); fine on TV/phone but tight.
3. Thumbnail Arabic title uses Amiri (no raqm on PC); acceptable, looks fine.
