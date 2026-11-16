# Short-from-Long runbook (user 2026-11-15). Used by BOTH daily tasks (History 02:30, Surah Long 04:10).
Daily total = 4 videos: 2 Longs (history story + surah) + 1 Short cut from each Long. The separate "Imaan Short" series (talking cute characters) is RETIRED: do not make those.

After the Long is built and Munshi-passed (same run), cut ONE Short from it. Cost Rs 0 (reuse the Long's own images, audio, music; no new TTS, no new images, no paid calls).
1. Pick the strongest self-contained part of the Long: the main point / most moving moment, 35-59 s (under 60 s), starting on a hook line (first 2 s must make the viewer stay). A new viewer must clearly see that the video tells something good and meaningful (hook -> main point -> one-line ending pointing to the full video).
2. Build 9:16 (1080x1920) with ffmpeg (tools\ffmpeg\ffmpeg.exe): the Long's picture filled/zoomed to the frame (blurred copy of the same frame as background if needed), burned Hindi subtitles in the safe area (15%-85% height), the same voice + soft music, -14 LUFS. Arabic ayah only as exact Tanzil bytes, never cropped. RULES 2e still applies (no Prophet/Sahaba faces, no angels).
3. Use only the Long's sourced script lines (no new wording). Title: Hindi hook + #shorts, <= 70 chars; description: one line + link to the Long + same sources/AI disclosure; contains_synthetic_media true.
4. Munshi quick check (hook, < 60 s, subtitles in safe area, -14 LUFS, depiction rule, sources). Fix free issues once.
5. Upload with the same publishing rule as its Long (DAILY_HISTORY 7h): api_audited true -> auto public/schedule inside 00:00-09:00 IST (Short 60 min after its Long); false -> PRIVATE + Studio action line (schedule time, Related video = the Long, pin comment). Log in log.md (link, length, Rs 0), sync.
6. If this step fails, the Long stays valid; log the reason and stop (never delay the Long for the Short).
