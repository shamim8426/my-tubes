# DevRoboLab: resume on another Claude account or PC (keyword: "devrobolab resume karo")

Plan (user 2026-11-05, final): 3 long + 3 Shorts a day, all uploaded PRIVATE.
- 08:00 `devrobolab-daily-videos`: AI news long (real assets) + Short
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
