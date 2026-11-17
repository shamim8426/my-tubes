# Noor daily Long runbook (user 2026-11-09). Task `noor-daily-long`, nightly after 03:30 IST (after the Short). Hinglish to the user.
Read first: CLAUDE.md, channels/noor-e-raah/RULES.md (all, esp. 1, 1d, 2a, 3, 5), channel_brief.md, learnings.md (LAGU KARO), series_queue.json, `python scripts/noor_daily.py next` and `preflight`.
Format = the existing surah explainer (kept as-is) EXCEPT (RULES 1d): ONE narrator (Charon, 2026-11-13) only, NO questions, NO SAWAAL voice, NO opening "tilawat nahi / qari se sunein" line, straight to the point, tempo 1.15, NO new images (reuse image_library.md and earlier stories' images, "reuse" in images.json; new image only if truly missing, free Cloudflare first). Private upload only; never publish.
1. `noor_daily.py next` -> the item and stage. If a Long was already uploaded today, stop. Do exactly the next stage chain: Khoji dossier -> Kalam script (one narrator, no questions, no [NOTE]) -> Munshi script PASS -> images (reuse only) -> TTS (Algieba; free key first, paid fallback; Whisper line check) -> Sampadak edit -> noor_render build -> thumbnail (noor_thumb_v3) -> Munshi final -> upload private + first-comment task (youtube-publish skill) -> mark uploaded.
2. Cost: Rs 0 images; TTS only (target <= Rs 20). If the free/paid TTS cannot finish, stop and log; never exceed the Rs 120 hard cap; floor Rs 50.
3. Log in log.md, update series_queue via noor_daily.py mark, sync (tools\sync.ps1). Stall rule: no step waits over 2 hours; log the reason and stop.

(user 2026-11-15, ALWAYS) Visuals follow RULES 2h: people-driven big image per ayah block (ordinary fictional people, faces allowed; never Nabi/Sahabi/Quran-named/angel/Allah). No ChatGPT: make images yourself, free Cloudflare flux first; if the free quota is exhausted, paid Gemini for max 3-4 images per video. Simple everyday Hindi (RULES 2f).
(user 2026-11-15) Publishing follows DAILY_HISTORY 7h: auto public/schedule inside 00:00-09:00 IST only after channel.json api_audited is true; until then upload PRIVATE and give a Studio action line.

(user 2026-11-15) AFTER the Long is uploaded: cut one Short from it per channels/noor-e-raah/scheduled_tasks/SHORT_FROM_LONG.md (Rs 0). Daily total 4 videos = 2 Longs + 2 Shorts. The Imaan Short series is retired.

(user 2026-11-17, ALWAYS) FOLLOW RULES 2i (storytelling v2: ayah read once then story-style Hindi explanation, 2-4 scene-matched images per ayah, up to 5:00, one single soft music track, no questions, no lesson, short final summary; history stories: script and images match line by line). It overrides any older line here that says reuse-only images, word-by-word blocks or per-line music cues.

(user 2026-11-17, ALWAYS) FOLLOW RULES 2k: Charon-only finals (preflight; if Charon unavailable wait/retry, never Edge), NO next-video announcement at the end, warm music, next surah = first planned item of series_queue (al-kafirun; al-fil is done).

(user 2026-11-17, ALWAYS) Story videos follow RULES 2l (template = stories/013_teen-musafir-gufa-sample; faceless images, phrase lines, gold keywords, one warm track, source-line ending, Charon only).

(user 2026-11-17, ALWAYS) Surah videos: RULES 2m (same template as story videos; ayah read once, story-style phrase-line explanation, faceless scene images per ayah).
