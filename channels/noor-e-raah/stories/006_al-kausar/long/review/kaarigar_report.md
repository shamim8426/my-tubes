# 006 al-kausar - Kaarigar report (2026-11-12)
- PC checks: Arabic byte-equal to tanzil.net download (fixed mark order + 108:1 alif+U+0653; Bismillah stripped); sha256 in research/sources.json. Muslim (Anas) line 11 confirmed in open source (fawazahmed0 eng-muslim book 4 hadith 56 = sunnah.com 400a) -> KEPT, no renumber; end_from 34. name_guard OK.
- Files: long/lines.json, images.json (0 new, 17 clips from 10 library images), render.json (tempo 1.15), edit_plan.json (soft_glow, same as 005), thumbnail.json, long/output/006_al-kausar_final.mp4 (3:28.6, 1920x1080 30fps, -14.0 LUFS), .srt, thumbnails v3A/B/C.
- TTS: Algieba, style "clear, steady, slightly brisk, not slow" (channel.json ustaad style updated per RULES 1d). Free key exhausted -> paid fallback. 24 lines, 205.8 s. Cost Rs 9.08 incl GST. Whisper 22/24; lines 23 ("tabri" heard as other word) and 32 ("liye" spelling) accepted as Whisper variants (.ok written) -> Munshi should listen to these two.
- Code change: scripts/noor_render.py now reads render.json "tempo" (was hard-coded 1.08).
- Thumbnail: PC Pillow has no raqm -> Aref Ruqaa path fails; built with --arabic amiri (libass). Wallpaper free Cloudflare (Rs0).
- Bug fixed mid-way: first final had Bismillah in Arabic (my Tanzil strip bug); old file in _to_delete/old_final_bismillah_bug/. Rebuilt.
- Minor: 10-word AYAH 1 Arabic line is tight to the screen edges (~30 px). Not uploaded.
