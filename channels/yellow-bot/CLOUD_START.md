# yellow Bot - START HERE (brief for a fresh session, cloud or PC)

You are working ONLY on the YouTube channel "yellow Bot" (key `yellow-bot`, ID UCpElgKdJOgQiyfwdGXz6GmA). Talk to the user in Hinglish.
IGNORE all Jugnu Stories / Noor-e-Raah rules in CLAUDE.md (Sanchalak, Kaarigar, Munshi, Kalam, auto mode, stories). They do not apply here.
Only these apply from CLAUDE.md: Hinglish replies, simple-English commit messages `<area>: <what changed>`, sync after milestones (`bash tools/sync.sh "yellow-bot: ..."` in cloud),
"time + cost estimate in one line before any task", cloud notes (secrets via env, one place at a time).

## What the channel is
Short Hinglish explainers (35-70 s, 1080x1920) of Claude Code features, from the OFFICIAL docs only (https://code.claude.com/docs, index /llms.txt).
Look: white background, black + yellow text, cute robot mascot, picture-story opener, Funkorama music. The theme is fixed and approved: copy the reference video, do not redesign.
Reference (best example): channels/yellow-bot/stories/006_hooks/ (deck.json, output/upload.json; live at https://youtu.be/GpVCvYrwqd4).
Read in this order: channels/yellow-bot/RULES.md, channel_bible.md, STYLE_GUIDE.md (v2, binding), log.md (last 20 lines), topic_queue.json (status per docs page).

## Your job
Make new Shorts, one topic at a time from topic_queue.json (status "todo"), and upload each as PRIVATE. The user reviews in Studio and makes them public.
Targets (user wants 10 Shorts/day): DAILY GOAL = 10 videos made AND uploaded. Today the YouTube API quota of project yellow-bot-devrobo allows only 6 uploads/day (~1,600 of 10,000 units each).
So: day 1 = 3-4 videos; from day 2 = up to 6/day; go to 10/day ONLY when the user says the quota was raised (extension form). Never make more videos than can be uploaded in the same session
(mp4 files are git-ignored and vanish when a cloud session ends, so no backlog). NEVER create another Google Cloud project/OAuth client to get more quota (against YouTube API terms).
Keep going topic after topic in the same session until the day's count is reached or a STOP condition happens. If quota error 403 appears, stop uploading for the day and say so.
Budget: paid Gemini TTS ~Rs1.6/video is allowed; hard cap Rs20/day; stop if Google balance < Rs50. Everything else (images, music, render) is free.

## FORMAT v3 (user 2026-10-31) - overrides anything above that conflicts
From the next video on: read STYLE_GUIDE.md section "v3 FORMAT" and open channels/yellow-bot/brand/reference_tools_short.html and reference_svg_robot.html (look at the code) before writing a deck.
Key points: (1) everything the voice says must be shown on screen at the same moment (cards, docs screenshot, terminal example, diagram); (2) no quiz or "guess karo" - explain ONE feature from the docs with a REAL example, professionally; (3) use the new layer kind "svgbot" (2D SVG robot with moving arms/mouth) in about one scene per video, besides the PNG robots; (4) scene order: concept cards -> docs proof -> real example -> docs nuance -> 3-point recap + open question.
Check each video's stills (`--still`) for text that is cut off or overlapping before upload.

## Preflight (do first, report in 5 lines, then start)
1. `git pull` is current (main). Venv works. `playwright install chromium` done (cloud has no Chrome; renderers fall back to Chromium).
2. secrets/yellow-bot/token.json + client_secret.json exist; GEMINI key in env. `tools/youtube_upload.py --job channels/yellow-bot/stories/006_hooks/output/upload.json --dry-run` prints "Dry run OK" (channel check passes; note: the mp4 is not in git, so the dry run may say video not found - that is fine, the channel/token part must pass).
3. https://code.claude.com/docs/llms.txt, api.cloudflare.com, generativelanguage.googleapis.com, www.googleapis.com reachable.
4. Say: "~X min per video, Rs Y, I need nothing from you" and ask nothing else. If a preflight item fails, STOP and tell the user exactly what is missing.
FIRST RUN = ONE topic only (prove the whole chain), tell the user the link, and ask "aur banau?" before doing more.

## Per video
1. Source = the topic's docs page only. Read it fully.
2. Folder channels/yellow-bot/stories/<NNN>_<slug>/ (NNN = next number after the highest existing). Write deck.json in the 006_hooks format: 7 scenes, 45-65 s.
   - Scene 1 (0-7 s) = type "stage": the robot DEMONSTRATES the feature as a picture story (layers with keyframes, like 006 scene 0). Never a text-only opener.
   - Other scenes: different layouts, never the same order as the previous video (statement, chips, flow, docs, code, list, compare, hub, cta).
   - Every video adds at least one NEW enhancement (new animation/scene type/robot pose); note it in STYLE_GUIDE.md.
   - Voice text: casual Hinglish (Devanagari + English words mix), on-screen text Roman Hinglish. music: Funkorama start 6 rel 12.
3. Fact-check in a SECOND pass: every claim vs the docs text (names of events/commands/flags exact). Remove anything not on the page. Save review/factcheck.md (claim -> quote). Cannot fix -> status "blocked", next topic.
4. Voice: `python -X utf8 scripts/build_deck.py <story> --tts` (free first); if free quota is over: `--tts --paid` only if today's total < Rs20 and balance >= Rs50. --tts only fills MISSING s_XX.wav files (to change a line, move its wav away first).
5. Render: `--render`. Check with ffprobe: 1080x1920, h264, yuv420p, 35-75 s; loudness about -14 LUFS, true peak <= -1 dBFS; look at stills (`--still t1,t2,...`) for overlap/clipped text and robots touching text.
6. upload.json: copy 006_hooks/output/upload.json. Title Hinglish <= 70 chars + "#shorts"; description = 2 lines + "Source (official docs): <url>" + "Unofficial channel, not affiliated with Anthropic." + Funkorama credit block + hashtags; privacy "private"; parent_video_id null; category_id 28; made_for_kids false; contains_synthetic_media true.
7. `python -X utf8 tools/youtube_upload.py --job <upload.json> --dry-run`, then without --dry-run. ALWAYS private; never public/schedule.
8. topic_queue.json: status "uploaded" + story; log.md one line (link, cost, time); sync.

## STOP and tell the user ONLY for
login/token failure (token expires ~2026-11-07 in Testing mode; re-login needs the user's browser), quota error 403, balance < Rs50, an unfixable fact mismatch, channel ID mismatch. Anything else: handle it yourself and log it.

## Final report (short)
How many made/uploaded, links, cost today, blocked topics, what you changed in STYLE_GUIDE (new enhancement), and everything synced.
