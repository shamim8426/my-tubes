---
name: yellow-bot-short
description: Make, upload (private) and log one Yellow Bot Short (channel key yellow-bot, AI explainer Shorts in Hinglish) from an official source page. Use when the user says "yellow bot short", "next yellow bot video", "news check" for Yellow Bot, or "yellow bot analytics".
---

# Yellow Bot Short (thin checklist; the rules live in the files named here, never copy them into this skill)

Read first, in order: `channels/yellow-bot/RULES.md`, `channels/yellow-bot/STYLE_GUIDE.md` (v4, ending rule, enhancements log), `channels/yellow-bot/brand/STYLE_LEARNINGS.md` (what we learnt from studying other channels, incl. Endings; principles only), `channels/yellow-bot/brand/LONG_FORM_LEARNINGS.md` (for LONG 16:9 videos: hook, structure, number cards, ending stack; principles only), `channels/yellow-bot/learnings.md` (Nigraan's lessons from our own analytics), `shared/RULES.md` (sections 1, 3, 6-8, 10-16), `channels/yellow-bot/topic_queue.json`. These override this skill.

## 0. Before starting
- Tell the user time and cost in one line (CLAUDE.md). Balance floor Rs 50 (shared by all channels): below it, stop and ask.
- Topic (user 2026-11-04: Shorts must look useful to ordinary people; one Short a day on the latest AI update): 1) a `"priority": "news"` item from the newest news digest, 2) else the first `todo` with `"audience": "A"` (everyday use), then B, then C (technical/reference, last); or the topic the user names. Order confirmed by the user 2026-11-04. Not mechanical: a B/C topic may move up if today's news ties to it, or if analytics show that kind of topic (direct, everyday benefit) performs better. Title = the benefit for the viewer. Primary source = the official page only; non-Claude topics say 'Unofficial channel, not affiliated with <org>.'

## 1. Build
- Daily style rule (STYLE_GUIDE 'Channel direction'): one style per day for all that day's Shorts, a new style or one new improvement the next day. Whole-AI channel, always inside YouTube's guidelines.
- Copy the newest story's `gen_deck.py` (e.g. `stories/021_how-claude-code-works/`) into `stories/<NNN>_<slug>/`; write script and `deck.json` via `scripts/build_deck.py` and `templates/deck_template.html`.
- Style: own look, layman first, symbols with meaning, hook with a claim by 0.3 s, 45-75 s (hard cap 75 s; a re-voiced line must never be longer). Engine fields are listed in STYLE_GUIDE.
- Voice: Gemini TTS. Free key first; if `gemini-3.8-flash-tts` hits its 100/day cap use `GEMINI_TTS_MODEL=gemini-3.8-flash-lite-tts` (free key, about 3 requests per minute, wait ~70 s on 429). Never use `noor_run.py` for this.
- Retime effects to real spoken words with Whisper (`anchors` in a scene).
- Render with `scripts/html_video.py`, mix with the ffmpeg limiter to about -14 LUFS, true peak under -1 dBTP. Check the file with ffprobe and look at a frame sheet: no cut-off text.
- Ending: line A (normal) or B (magic) from STYLE_GUIDE; variables `CTA_VOICE`, `CTA_SCREEN`, `CTA_PILL`.

## 2. Check and send
- Fact-check every claim against the source page. Send `output/short.mp4` to the user with `SendUserFile`. Upload only after the user says yes.

## 3. Upload (only on the user's word)
- Always PRIVATE (`api_audited` false). Dry run first, then `python tools\youtube_upload.py --job <story>\output\upload.json`. Thumbnail API returns 403 (phone verification): the user sets it in Studio.
- After the upload: topic_queue (`status` uploaded, `story` set; keep JSON format), `log.md` line (URL, length, LUFS, rough spots), STYLE_GUIDE note if the engine or style changed, then sync: `powershell -NoProfile -ExecutionPolicy Bypass -File tools\sync.ps1 -Message "yellow-bot <NNN>: <what>"` (simple English; with `$ErrorActionPreference="Continue"`; check `.git\sync.lock` afterwards).

## 3b. Long news digest (16:9)
- A 3-4 minute landscape digest of 4-5 AI items (whole field) follows STYLE_GUIDE 'Long news digest (16:9)': deck.json `"format": "landscape"`, copy `stories/025_*/gen_deck.py`, upload.json `"format": "long"` with the Latest AI Updates `playlist_id`, private only.

## 4. Other jobs
- News watch: `channels/yellow-bot/NEWS_WATCH.md` (twice a day, whole AI field).
- Study another channel: `channels/yellow-bot/brand/LEARNING_PROCESS.md` (RULES 12c; downloads only in git-ignored `study/`, never reuse their frames, audio, script or exact titles; delete after recording learnings).
- Analytics: `.venv\Scripts\python.exe -X utf8 tools\yt_analytics.py yellow-bot fetch` writes `channels/yellow-bot/analytics/`. YouTube data lags 2-3 days; small counts (under 1,000 views) are signals only. Studio numbers can be higher than the API for the newest days.
- Manual items for the user: thumbnails in Studio; OAuth token renewal (`tools/yt_auth.py yellow-bot`); making a video public.

## Never
- No public upload, no secrets in the repo, no deleting project files (move to `_to_delete`), no copying another channel's look.
