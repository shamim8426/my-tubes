# Claude news watch (user rule 2026-11-04): check at least twice a day, notify, suggest videos

Why: Yellow Bot explains Claude / Claude Code to people. A new model, feature, command or doc page is the best Short topic, and being early matters. The user wants a notification plus a video suggestion for every real update.

## How it runs
- A local scheduled task (id `claude-news-watch`, 09:00 and 18:00 local time; it runs while the Claude app is open, else on next launch) follows this file. On demand the user can say 'news check'.
- Step 1: `D:\my-tubes\.venv\Scripts\python.exe -X utf8 D:\my-tubes\scripts\yb_news_check.py` (dry check, prints what is NEW since the last saved state). Sources: Claude Code changelog (new versions + 'Added' bullets), docs index llms.txt (a NEW page = a new feature/topic), Anthropic news (models, products), API release notes (new dated entries).
- Step 2: nothing new -> do nothing else (no notification, no file), except run the script with --commit so last_run is saved. Something new -> read the details (changelog bullets; open each NEW doc page and each NEW news article with WebFetch and read what it says; official sources only), decide what matters to viewers.
- Step 3: write `channels/yellow-bot/research/news/<YYYY-MM-DD>_<HHMM>.md`: per item: what it is (2 lines, layman Hinglish), source URL, why viewers care, urgency (post within 24 h / 48 h / this week / low), a SUGGESTED SHORT (Hinglish title <= 70 chars, the hook line with a number or a concrete promise, the docs page to use as the only source, 4-5 beat outline per STYLE_GUIDE v4), and whether it is a new MODEL (model launches get their own note: name, what changed, price/availability only if stated by the source, and a Short + a longer video idea).
- Step 4: add the suggested topics to `channels/yellow-bot/topic_queue.json` ONLY as entries with status "todo" (never "uploaded", never reorder, keep the file's formatting exactly: load with json, dump indent=2, ensure_ascii=False, same line endings, and verify the round trip of the untouched file first), with a `"priority": "news"` field; new docs pages not yet in the queue are added the same way.
- Step 5: run `yb_news_check.py --commit` to save the state, then send ONE PushNotification (under 200 chars, Hinglish, e.g. 'Claude Code 2.1.318: naya /xyz aaya. Short suggestion: ... Digest: channels/yellow-bot/research/news/...'). One notification per run, only when something real is new (a new version with user-facing 'Added' items, a new model, a new docs page, a new Anthropic product/feature announcement). Pure fixes, enterprise/admin-only or SDK-internal items are mentioned in the digest only (no push).

## Never
- No upload, no paid call (no Gemini/TTS/images), no video build, no git commit/push (the nightly sync does it), no secrets, no deleting files, no edits to STYLE_GUIDE/RULES.
- No claims beyond what the official source says; never invent a price, limit or release date. Unsure = write 'docs me nahi likha'.
- Unofficial channel: suggestions must keep 'Unofficial channel, not affiliated with Anthropic.' in mind.

## When the user approves a suggestion
The Sanchalak builds it like any Yellow Bot Short (STYLE_GUIDE v4, layman first, own look, never a copy), private upload, then sync.
