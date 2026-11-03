# AI news watch (user rule 2026-11-04): whole AI field, at least twice a day, notify, suggest videos

Why: Yellow Bot keeps people updated about AI. Any new model, feature, enhancement or free/open tool, from ANY AI organisation (Anthropic, OpenAI, Google, Meta, Mistral, DeepSeek, Alibaba Qwen, xAI, Microsoft, NVIDIA, Hugging Face, GitHub Copilot, Cursor, Ollama, Stability, ElevenLabs, ...), can be a Short, and being early matters. The user wants to KNOW twice a day and get a video suggestion for every real update.

## How it runs
- Local scheduled task `claude-news-watch` (09:00 and 18:00 local time; runs while the Claude app is open, otherwise on next launch). On demand the user can say 'news check'.
- Step 1: `D:\my-tubes\.venv\Scripts\python.exe -X utf8 D:\my-tubes\scripts\yb_news_check.py` (dry check; prints what is NEW since the last saved state). Add `--recent 3` to also list the latest items per source (for a first look or a quiet day).
  - Claude: Claude Code changelog (new versions + 'Added'), docs index llms.txt (new page = new feature/topic), Anthropic news, API release notes.
  - Rest of the field: `channels/yellow-bot/research/news_sources.json` (RSS feeds, blog-link watchers, Hacker News high-point AI stories, and trade press only to cover labs that block us). Add a source = add a line (its first run only builds a baseline). Known gaps: xAI, Microsoft AI blog, Runway, Perplexity block or moved; HN + press cover them.
- Step 2: nothing new -> run the script with `--commit` (saves last_run) and stop: no notification, no file.
- Step 3 (something new): OPEN each promising item's page with WebFetch (the organisation's own page; press/HN items are only pointers to the primary source: find it) and read what it really says. Decide what matters to ordinary viewers.
  - Worth a suggestion: a new MODEL (any org: what is new, who can use it, free/paid only if the page says), a user-facing FEATURE or enhancement people can use now, a free/open/local tool, a creative-AI tool (image, video, voice, music), a coding-agent update, a big change in limits/pricing if stated, an AI product from a big platform (Apple, Google, Meta, Microsoft...).
  - Digest only (no push): bug fixes, enterprise/admin/SDK-internal items, funding/valuation/legal/politics, benchmarks without a usable product, rumours.
- Step 4: write `channels/yellow-bot/research/news/<YYYY-MM-DD>_<HHMM>.md`, grouped: Models / Tools and features / Open-source and free / Creative AI / Dev tools / Claude. Per item: organisation, what it is (2 lines, layman Hinglish), the PRIMARY source URL, why viewers care, urgency (post within 24 h / 48 h / this week / low), and a SUGGESTED SHORT (Hinglish title <= 70 chars, hook line with a number or a concrete promise, the one official page to use as the only source, 4-5 beat outline per STYLE_GUIDE v4, layman first). A big model launch also gets a longer-video idea. Put the 1-3 best items first ('TOP PICKS').
- Step 5: add the suggested topics to `channels/yellow-bot/topic_queue.json` ONLY as new entries with status "todo", `"priority": "news"` and the organisation in a `"org"` field (never mark anything uploaded, never reorder; load with json, verify the untouched round trip, dump indent=2, ensure_ascii=False, same line endings). Claude docs pages not yet in the queue are added the same way.
- Step 6: `yb_news_check.py --commit` (saves state), then ONE PushNotification (under 200 characters, Hinglish): the best 1-2 items with organisation + a call to action, e.g. 'AI update: <Org> ne <naya model/feature> launch kiya. Short idea ready. Digest: research/news/<file>'. One notification per run, only when a real user-facing update exists.

## Never
- No upload, no paid call (Gemini/TTS/images), no video build, no git commit/push (the nightly sync does it), no secrets, no deleting files, no edits to STYLE_GUIDE or RULES.
- No claim beyond what the primary source says; never invent a price, limit, date, benchmark or availability. Unsure = 'page me nahi likha'.
- Never copy another organisation's wording, images or logos into a video; explain in our own words and our own look.

## When the user approves a suggestion
The Sanchalak builds it like any Yellow Bot Short (STYLE_GUIDE v4, layman first, own look, never a copy), private upload, then sync. For a non-Claude topic the description carries 'Unofficial channel, not affiliated with <organisation>.'
