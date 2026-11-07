# DevRoboLab daily plan (user 2026-11-07; SUPERSEDES the older DAILY PLAN lines in DAILY_COMMON.md and RESUME.md)

Status: ACTIVE (user 2026-11-07): the 5 scheduled tasks below run every day and upload PRIVATE; the user makes videos public in Studio. The user can still ask for a video any time.

## Formats (decided)
- AI news: SHORT (9:16, 35-40 s).
- Claude for Everyone feature (Claude app, not Claude Code): LONG (16:9, about 3 min). Playlist PLEklr-qY9V3U, title "Claude Feature NN: ...".
- Claude Code feature: LONG (16:9, about 3 min). Playlist PLGTgifZfJLow, title "Claude Code NN: ...". (This replaces "Claude Code Short only" in STYLE_LIBRARY/RESUME.)
- Claude in daily life: SHORT. NEW playlist (name: user decides; not created yet). Example-led Shorts: how to connect a tool or connector and what to say to Claude (one video per type, list in the Topic order section below; first Zomato).
- Fifth video: a Short cut from that day's long video (teaser, ends "Poora video channel par hai").
- A feature long is never also its own full Short topic twice; the cut Short only shows the best part.

## Slots (IST) and rough work time
| Time | Video | Format | Work | Upload (private) |
| 05:30 | AI news | Short | about 1 h | by 06:30 |
| 06:30 | Claude for Everyone feature | Long | about 2.5 h | by 09:00 (hard stop) |
| 20:30 | Claude Code feature | Long | about 2.5 h | about 23:00 |
| 23:00 | Daily life (Zomato first) | Short | about 1-1.5 h (research first) | about 00:15 |
| 00:30 | Short cut from the latest long (last 24 h) | Short | about 1 h | about 01:30 |
(user 2026-11-07: ALL morning work finished by 09:00; no work from 09:00 to 20:00. Tasks run one after the other; a task waits if the previous run is still running.)
One run at a time, never in parallel. Each run: research from the official source, script, voice, build, self-review of frames, loudness check, private upload to the right playlist, topic_queue.json + log.md + sync, one status line to the user.
Suggested public order for the user (Studio): news and Claude for Everyone after 09:00, the night videos next morning. Thumbnails and going public are always the user's manual step.

## Rules that stay
- Upload PRIVATE only. Never public, never delete, never change security/permission settings.
- Look: STYLE_LIBRARY sections 0, 9, 10: full-screen showing area, no face, no robot box, normal-size text, colours change every video (log `style variants:` + highlight colour), long videos with chapter badge, long dark demo take, number card, recap, end card; last-line CTA rotates.
- Facts only from official sources (support.claude.com, claude.com docs, anthropic.com, code.claude.com). Third-party items (e.g. Zomato) are labelled as examples/third-party, with no real order, account or payment ever shown; a company logo only small and only if its own page allows media use.
- MONEY (user 2026-11-07, binding): DevRoboLab spends at most **Rs 30 per day in total (all videos)**; floor **Rs 50** (balance Rs 536 on 2026-11-07, about Rs 3 per long and Rs 1 per Short, so the day's 5 videos need about Rs 10-15). Free key / free Cloudflare first, paid only when needed. Enforced in code: `shared/pricing.json budget.channel_daily_cap_inr` (day = 05:00-04:59), `gemini_keys.post` stops paid calls, `python scripts/daily_spend.py devrobolab` shows today's spend. Other channels' limits: the user decides separately.
- Sync timing/words: every action on screen is tied to the real word times (wordtimes.py -> wt.json, T(scene, token)). Hindi captions are rendered by Chromium (`build_caps()` in `stories/044_cfe-memory/make_final.py`) because Pillow here has no raqm. Reference build for longs: `make_final.py` (per-beat zoom K, no blank frames).
- Self-review before upload: frame sheet every 3 s; fail = no upload, report instead (checks: Hindi matras, blank frames, overlaps, cut text, sync of each spoken step, loudness -14 +-1, length 2:00-6:00 long / <= 40 s news Short).

## Things that can stop the automatic runs (tell the user)
- PC/app must be on at the slot time; if it was off the run still does the same work when it starts.
- YouTube login (Testing mode) expires every 7 days: run `tools/yt_auth.py` weekly, or move the Google Cloud project to Production.
- Balance about 35-40 days at about Rs 12-15/day; recharge before Rs 50.
- A stalled run: re-run once, then tell the user the cause (stall rule in RESUME.md).

## Topic order
- Claude for Everyone: queue items with series "claude-for-everyone" (tier A first). Done: 01-05 (Projects, Artifacts, Research, File upload, Memory). Next: image input, styles, resume/job, study help, email writing ...
- Claude Code: queue items from code.claude.com docs (80+ todo). Done: 02 fast mode (Short). Next candidate: "Explore the .claude directory" (official page already read on 2026-11-07).
- Daily life (user 2026-11-07): ONE video per TYPE of everyday use, never a second video of the same type. Example: Zomato (food delivery) is done once; NO Swiggy or any other food-delivery app after it, and the same for every other type. Each Short shows how to connect/start it and how to use it in daily life, with one concrete example. Order (one each, skip a type that is already in log.md, then stop and tell the user when the list is finished; never loop back to a done type):
  1. Food delivery: Zomato connector (Settings > Connectors > Add custom connector; payment by QR per third-party guides; research first, label third-party)
  2. Email: Gmail search + reply drafts (Claude only drafts, you send)
  3. Calendar: ask about your schedule (read questions only; Claude cannot create/change events)
  4. Documents: ask questions about a Google Drive file or a PDF
  5. Photos: fridge photo -> what can I cook
  6. Money: understand a bill or expenses from a photo/PDF
  7. Study: notes and a quiz from a chapter
  8. Job: resume fix and interview practice
  9. Travel: trip plan with web search
  10. Shopping: compare two products with web search
  11. Writing: Hindi-English message / translation
  Every topic is checked first against an official or clearly reliable source; third-party items are labelled and never show a real order, account or payment; if it cannot be confirmed, skip that type and take the next.
- News: from NEWS_WATCH.md as before.

## Open items for the user
- Name of the daily-life series/playlist (then create the playlist).
- When to switch on the 4-5 scheduled tasks (08:00, 10:00, 14:00, 20:00, 23:00).
- Studio: thumbnail for Claude Feature 05 (https://youtu.be/zfOBSjw3RA0); public when ready.

## Review and partial fix (user 2026-11-07, every video)
After building a video: review it (frames every 3 s + the exact frame of every spoken action word, Hindi matras, blank frames, overlaps, cut text, sizes, loudness, length, facts), write the mistakes in `review/review.md`, then fix ONLY those parts: change the code for those scenes, re-render only that time range (`make_final.py range t0 t1 output/part.mp4`) and splice it into the finished video (`tools/splice_video.py orig part t0 t1 out`, frame accurate, audio unchanged; tested on 044: same 5166 frames, 172.2 s). Re-check the fixed ranges. Max 2 rounds; still wrong = no upload, report. Full re-render only if the script/voice changes.

## Scheduled tasks (user 2026-11-07: "schedule me add kar do taki upload tak ka kaam apne aap ho")
Common steps for every task: `scheduled_tasks/RUN_COMMON.md`. Task prompts (backups): `scheduled_tasks/<taskId>.md`.
| Task id | Cron (local) | Slot |
| devrobolab-news-short | 15 5 * * * | 05:30 AI news Short |
| devrobolab-cfe-long | 15 6 * * * | 06:30 Claude for Everyone long (done by 09:00) |
| devrobolab-claude-code-long | 20 20 * * * | 20:30 Claude Code long |
| devrobolab-daily-life-short | 50 22 * * * | 23:00 Daily-life Short |
| devrobolab-long-cut-short | 20 0 * * * | 00:30 Short cut from the latest long |
| devrobolab-retry-night | 0 21,22 * * * | 21:00 and 22:00: do any slot that has no upload today (PC was off) |
The old tasks (devrobolab-daily-videos, devrobolab-afternoon-videos, devrobolab-evening-videos, claude-news-watch) are NOT to be recreated.
