# Research: Tasks in Gemini (Google, 2026-11-17) - AI news deep dive Long (day key 2026-11-18, type 2)

Why this item: biggest consumer AI launch of the last days that India viewers can use now (India is one of the 6 countries where it is free without a subscription). Hard numbers: 6 countries, 15 tasks at once, 18+.
Skipped: OpenAI GPT-6.2 Astra/Sol (openai.com page returns 403 / "Internal Server Error" to our fetch; only GitHub changelog confirms availability, no numbers -> not 2 official sources). Rumble-2-Flash ASR (good, but smaller audience; keep for a news Short).

## Official sources (all fetched 2026-11-18 21:40-21:55 IST; page texts saved in raw/page_*.txt)
- S1 Google blog (Josh Woodward), "Put Gemini to work for you", Nov 17 2026: https://blog.google/innovation-and-ai/products/gemini-app/tasks-in-gemini-free-new-features/
- S2 Gemini Apps Help "Manage your tasks & workflows in Gemini Apps": https://support.google.com/gemini/answer/17094507
- S3 Gemini Apps Help "Create & manage schedules for tasks in Gemini": https://support.google.com/gemini/answer/17094710
- S4 Gemini release notes, entry 2026.11.17 "Find Ways to Save Time and Money with Tasks in Gemini": https://gemini.google/release-notes/
- S5 Google security blog, "How Gemini's defense-in-depth approach works", Nov 17 2026: https://blog.google/security/how-geminis-defense-in-depth-approach-works/

## Facts (number / claim -> sources). Only these go in the video.
- Launched / rolling out Nov 17, 2026 -> S1 (date), S4 (entry 2026.11.17).
- Free (no subscription) in US, Japan, Korea, Canada, Australia, India; "hundreds of millions" -> S1, S4, S2, S3.
- Runs on the new Gemini 4 Hydrogen model (S4 writes "Hydrogen 4") -> S1, S4.
- Needs: 18+, personal Google Account (not work/school), History on -> S2, S3.
- With Google AI Pro/Ultra: everywhere else Gemini Apps work, except EEA, Nigeria, Switzerland, UK -> S2, S3.
- Only in Gemini mobile app, Gemini app on Mac, web app gemini.google.com -> S2, S3.
- Turn on: open app / gemini.google.com, above the text box tap Task -> S2 (create a task + turn back on), S3 (schedule conversationally: tap Task above the text box); S1: toggle on the home screen from Chat to Task.
- Earlier name Spark (beta) -> S2 FAQ "Where did Spark go?", S4 (Spark entry May 2026).
- Example jobs: declutter inbox (summarize/archive newsletters, unsubscribe), urgent to-do list, flight/hotel price drop alerts within budget, research with cited sources packaged as PDF/doc/sheet/slides files -> S2; S4: daily morning briefing across emails and calendar, trip itinerary, automating repetitive research.
- Uses Connected Apps, websites you are signed into, Personal Intelligence, location -> S2; S1: Calendar, Gmail, Password Manager, more than 60 apps.
- Schedules: time-based (e.g. every Monday morning) or condition-based (e.g. when an email arrives) -> S3 intro; S2 "around a specific time or after an event". S4 "scheduling a daily morning briefing".
- Up to 15 tasks running at the same time; a schedule does not run if 15 are already running -> S2; S3 limits (WebFetch read of the collapsed section: "Tasks running at once: 15 maximum").
- Usage limits are compute-based; higher with higher subscriptions; Gemini warns near the limit -> S2 (S3 says runs are skipped at the usage limit).
- Browser: local or remote browser; you can take control of the browser any time -> S2; S5 (hands the live cloud browser to you at sign-in walls, you can steer or stop it any time).
- Confirmations: asks before sending, deleting, sharing sensitive info, purchases, financial transactions, submitting forms -> S2 (WebFetch of collapsed section); S1 (pauses for confirmation before critical steps like clicking Buy); S5 (high-impact actions pause for explicit confirmation even with Always allow); S4 (1-tap confirmation before sending/booking).
- Isolation: each task in a hardware-isolated virtual machine (microVM) of Google Cloud Agent Compute Engine -> S1, S5.
- Prompt-injection filters scan search results/web pages/emails + Google Safe Browsing limits links -> S1, S5.
- US-only for now: Google Pay checkout, texting Gemini, email forwarding to gemini@google.com (English, US), calling US businesses -> S4 (each entry), S1 ("advanced features, starting in the U.S.").
- Some websites block the assistant; Gemini may hand the last step back -> S1; S2 ("for certain actions, Gemini will ask you to take over").
- Experimental, can make mistakes; your supervision matters -> S2 ("Gemini's ability to handle tasks is experimental ... your supervision is important").  S1 asks for thumbs down feedback when it misses.
- Turn off: Menu > Settings > Task settings > "Use task mode to hand off work" > Turn off; deletes remote browser + remote code execution data; tasks, threads, schedules, files NOT deleted; schedules paused -> S2; S3 FAQ "What happens to my schedules if I turn off task mode" (pauses).

## Dropped (only one source or not useful)
- Exact schedule frequency/count limits for free vs Pro (10 vs 50, once a day): only S3 collapsed section -> not used.
- File type list in detail (.tex, .tsx...): only S2 -> only "PDF, documents, spreadsheets, presentations" (S2 intro) used.
- $389 bill, $10 discount, 60+ apps, 5-state calling exclusion: author anecdotes / single source -> not used.
