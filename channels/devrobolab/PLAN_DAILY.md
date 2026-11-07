# DevRoboLab daily plan (user 2026-11-07; SUPERSEDES the older DAILY PLAN lines in DAILY_COMMON.md and RESUME.md)

Status: PLAN ONLY. No scheduled tasks exist on this account. The user said: "sirf plan likho" (do not create tasks yet). Run a slot only when the user asks ("agla video", "aaj ka batch"), until the user says to switch on the tasks.

## Formats (decided)
- AI news: SHORT (9:16, 35-40 s).
- Claude for Everyone feature (Claude app, not Claude Code): LONG (16:9, about 3 min). Playlist PLEklr-qY9V3U, title "Claude Feature NN: ...".
- Claude Code feature: LONG (16:9, about 3 min). Playlist PLGTgifZfJLow, title "Claude Code NN: ...". (This replaces "Claude Code Short only" in STYLE_LIBRARY/RESUME.)
- Claude in daily life: SHORT. NEW playlist (name: user decides; not created yet). Example-led Shorts: how to connect a tool or connector and what to say to Claude (first topic: Zomato connector for ordering food; then Gmail drafts, Calendar questions, Drive/PDF questions).
- Fifth video: a Short cut from that day's long video (teaser, ends "Poora video channel par hai").
- A feature long is never also its own full Short topic twice; the cut Short only shows the best part.

## Slots (IST) and rough work time
| Time | Video | Format | Work | Upload (private) |
| 08:00 | AI news | Short | about 1 h | about 09:15 |
| 10:00 | Daily life | Short | about 1.5 h (research first) | about 11:45 |
| 14:00 | Claude Code feature | Long | about 2.5 h | about 16:45 |
| 20:00 | Claude for Everyone feature | Long | about 2.5 h | about 22:45 |
| 23:00 | Short cut from one of the day's longs | Short | about 1 h | about 00:15 |
One run at a time, never in parallel. Each run: research from the official source, script, voice, build, self-review of frames, loudness check, private upload to the right playlist, topic_queue.json + log.md + sync, one status line to the user.
Suggested public order for the user (Studio): news 09:30, daily life 12:30, Claude Code 17:00, Claude for Everyone 21:00. Thumbnails and going public are always the user's manual step.

## Rules that stay
- Upload PRIVATE only. Never public, never delete, never change security/permission settings.
- Look: STYLE_LIBRARY sections 0, 9, 10: full-screen showing area, no face, no robot box, normal-size text, colours change every video (log `style variants:` + highlight colour), long videos with chapter badge, long dark demo take, number card, recap, end card; last-line CTA rotates.
- Facts only from official sources (support.claude.com, claude.com docs, anthropic.com, code.claude.com). Third-party items (e.g. Zomato) are labelled as examples/third-party, with no real order, account or payment ever shown; a company logo only small and only if its own page allows media use.
- Voice: free key first, then the paid key; per-run cap Rs 15; floor Rs 50 (balance Rs 536 on 2026-11-07, about Rs 3 per video). Stop paid work below Rs 50.
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
- Daily life: first = Zomato connector (Settings > Connectors > Add custom connector; payment by QR per third-party guides; research first, label third-party), then Gmail drafts, Calendar summary, Drive/PDF questions.
- News: from NEWS_WATCH.md as before.

## Open items for the user
- Name of the daily-life series/playlist (then create the playlist).
- When to switch on the 4-5 scheduled tasks (08:00, 10:00, 14:00, 20:00, 23:00).
- Studio: thumbnail for Claude Feature 05 (https://youtu.be/zfOBSjw3RA0); public when ready.
