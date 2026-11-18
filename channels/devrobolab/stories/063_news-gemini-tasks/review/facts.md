# Facts used in 063 (Tasks in Gemini, AI news deep dive Long). Every spoken/on-screen claim -> 2+ official sources.
S1 https://blog.google/innovation-and-ai/products/gemini-app/tasks-in-gemini-free-new-features/ (Nov 17 2026)
S2 https://support.google.com/gemini/answer/17094507 (Manage your tasks & workflows in Gemini Apps)
S3 https://support.google.com/gemini/answer/17094710 (Create & manage schedules for tasks in Gemini)
S4 https://gemini.google/release-notes/ (entry 2026.11.17)
S5 https://blog.google/security/how-geminis-defense-in-depth-approach-works/ (Nov 17 2026)

| # | Claim in video | Scene | Sources | Check |
|---|---|---|---|---|
| F1 | Tasks in Gemini released Nov 17 (2026) | hook | S1 date, S4 entry 2026.11.17 | PASS |
| F2 | Free without subscription in 6 countries incl. India (Australia, Canada, India, Japan, South Korea, US) | hook, who, cta | S1, S2, S3, S4 | PASS |
| F3 | Task = hand over a whole multi-step job, works in background, notifies when done | what | S4 ("work on your behalf in the background ... notify you the moment your results are ready"), S2 (automate complex workflows) | PASS |
| F4 | Help-page examples: clean inbox/archive newsletters, to-do list after a holiday, flight/hotel price alerts in budget, research with sources -> PDF | what | S2 (examples list); S4 (morning briefing, itinerary, repetitive research) | PASS |
| F5 | Uses connected apps (Gmail, Calendar) and a browser when needed | what | S2 (Connected Apps, Workspace, local/remote browser); S1 (Calendar, Gmail, Password Manager) | PASS |
| F6 | Earlier name Spark | what | S2 FAQ "Where did Spark go?"; S4 Spark entry (May 2026) | PASS |
| F7 | Runs on Gemini 4 Hydrogen model | what | S1 ("Gemini 4 Hydrogen model"), S4 ("Hydrogen 4 model") | PASS |
| F8 | Elsewhere with Google AI Pro/Ultra, not in EEA, Nigeria, Switzerland, UK | who | S2, S3 | PASS |
| F9 | Conditions: 18+, personal account (work/school not yet), History on | who | S2, S3 | PASS |
| F10 | Mobile app, Mac app, gemini.google.com | who | S2, S3 | PASS |
| F11 | Rolling out (may not be visible yet) | who | S1 "rolling out", S4 "rolling out" | PASS |
| F12 | Turn on: tap Task above the text box (Chat/Task toggle); follow on-screen steps; describe task + when; Submit | start | S2 (create a task; turn back on), S3 (schedule conversationally steps), S1 (toggle from Chat to Task) | PASS |
| F13 | Check progress in the task thread; Gemini asks you to take over e.g. sign-in | start | S2 (check a task, take over), S5 (hands browser to you at sign-in walls) | PASS |
| F14 | Asks confirmation before delete / send / buy / forms | ex1, safety, cta | S2 (confirmations list), S1 (pauses before Buy), S5 (explicit confirmation for high-impact actions), S4 (1-tap confirmation before sending/booking) | PASS |
| F15 | Schedules: time based (every Monday morning) or event based (an email arrives); pause / resume | ex2 | S3 (intro + pause/resume), S2 ("around a specific time or after an event", pause & resume schedules in a thread) | PASS |
| F16 | Research with cited sources into downloadable files: PDF, documents, spreadsheets, presentations | ex3 | S2 (intro + "files Gemini can create"); S4 (automating repetitive research) | PASS (file list: S2 only; research part 2 sources) |
| F17 | Each task in a hardware-isolated virtual machine for your account | safety | S1, S5 | PASS |
| F18 | Prompt-injection filters + Google Safe Browsing limit links | safety | S1, S5 | PASS |
| F19 | You can take control of the browser any time | safety | S2, S5 ("steer or stop a live browser session at any time") | PASS |
| F20 | Calls to businesses, Google Pay checkout, texting, email forwarding: US only, English, for now | us, cta | S4 (each entry: US, English; "call US businesses"), S1 ("advanced features, starting in the U.S.") | PASS |
| F21 | Up to 15 tasks at a time; a schedule does not run if 15 are running | limits, cta | S2, S3 | PASS |
| F22 | Usage limit grows with use/complexity; Gemini warns near the limit | limits | S2, S3 (runs skipped at usage limit) | PASS |
| F23 | Experimental, can make mistakes; some sites block it, last step may be yours; avoid scheduling sensitive tasks | limits | S2 (experimental, supervision; "Avoid scheduling tasks you find sensitive"), S1 (sites block, hands final step back) | PASS |
| F24 | Turn off: Menu > Settings > Task settings > Turn off; deletes remote browser + remote code data; tasks/threads/files kept; schedules paused | off | S2; S3 (turning off pauses schedules) | PASS |

Illustrations (labelled on screen): app screens, inbox mails, to-do items, briefing numbers, air-purifier PDF, confirm dialog, VM drawing - examples only, no real account.
Third-party/other orgs: none. Description says "Unofficial channel, not affiliated with Google."
