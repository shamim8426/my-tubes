# DevRoboLab: resume on another Claude account or PC (keyword: "devrobolab resume karo")

Plan (user 2026-11-05, final): 2 long + 3 Shorts a day, all uploaded PRIVATE.
- 08:00 `devrobolab-daily-videos`: AI news SHORT only (real assets, no long video)
- 14:00 `devrobolab-afternoon-videos`: Claude Code feature long + Short
- 20:00 `devrobolab-evening-videos`: Claude for Everyone long + Short
Rules: DAILY_COMMON.md (all runs), series/*/README.md, STYLE_GUIDE.md, NEWS_WATCH.md.

## When the user says "devrobolab resume karo"
1. Read: CLAUDE.md, this file, DAILY_COMMON.md, STYLE_GUIDE.md ('Channel direction and daily style rule'), series/README.md, research/daily/<today>.md (what already ran today), memory repo shamim8426/claude-memory topics/devrobolab.md.
2. Call list_scheduled_tasks. For each of the three task ids above that is MISSING or has a different prompt: create/update it from `scheduled_tasks/<taskId>.md` here (copy the text after the front matter as the prompt, description from the front matter; crons in LOCAL time: `47 7 * * *`, `0 14 * * *`, `54 19 * * *`; the minutes are early on purpose to offset the app's start delay). Old tasks `claude-news-watch` must stay disabled.
3. Check the machine: secrets/devrobolab/{token.json,analytics_token.json,client_secret.json} exist (never in git; copy by hand on a new PC; OAuth login in Testing mode expires every 7 days: re-run tools/yt_auth.py), `.env` Gemini keys, `.venv`, Chrome, ffmpeg. Run `.venv\Scripts\python.exe -X utf8 -c "import sys; sys.path.insert(0,'scripts'); import cost_log; print(cost_log.remaining())"` (floor Rs 50).
4. Work out which of today's runs already happened (research/daily, stories folders, upload results, topic_queue) and run only what is missing. Never publish; never run two runs in parallel; stop paid work below Rs 50.
5. Tell the user in Hinglish: which tasks exist, what ran, what is left.
Keep these backups in sync when a task prompt changes (copy from C:\Users\<user>\.claude\scheduled-tasks\<taskId>\SKILL.md).

## Stall rule (user 2026-11-05)
Whenever a daily run is found stalled (status running but its transcript/last_activity has not moved for more than 10 minutes, or the task time passed with no run), do NOT ask: find the cause (often a pending permission prompt or a hung tool call), fix it if it is inside the project (not security settings), stop the stalled session (stop_session) and re-run the task ONCE (run_scheduled_task). If it stalls again, tell the user plainly with the cause and what he must do. Never change permission/security settings myself; never kill OS processes without his approval. No background watchdog task exists (user decided not to add one): stalls are only noticed when the user or a session checks, so on every user message in a DevRoboLab session first check list_task_runs for today's runs.

## Handover state (2026-11-05, before switching Claude account)
- AI news is a SHORT only (08:00). 14:00 = Claude Code long + Short. 20:00 = Claude for Everyone long + Short (playlist PLEklr-qY9V3U, queue items "series":"claude-for-everyone").
- No scheduled tasks exist after the account switch: on the new account say "devrobolab resume karo" and create the 3 tasks from the backups here (crons 47 7 / 0 14 / 54 19), then run "Run now" once on each to pre-approve tools. `.claude/settings.local.json` (allow Bash, PowerShell, Read, Edit, Write, Glob, Grep, WebFetch, WebSearch) is local to this PC and not in git: recreate it if the folder is on another PC (user runs it himself, Claude may not change permissions).
- Today (2026-11-05): Short 027 (ChatGPT Images 2.6 GIFs) with real page screenshots is DONE: https://youtu.be/tMsznaDv0dU (private); the first version LBVBeMjUHFU (no real screenshots) must be deleted by the user in Studio. Long 026 is unfinished and not planned. Afternoon (Claude Code) and evening (Claude for Everyone) videos of 2026-11-05 are NOT made yet: do them first on the new account if the user wants them today.
- NEXT IMPROVEMENT (user): rebuild Short 027 in VISUAL STANDARD v2 (big real screenshots, AI images, less HTML) if he asks; later also a scene-wise render cache in scripts/html_video.py (only changed scenes re-render; ~30-45 min work).
- Balance about Rs 543 (floor Rs 50, shared); OAuth token (Testing mode) expires about 2026-11-07, run tools/yt_auth.py or move the Google Cloud project to Production.
