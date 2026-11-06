# Channel RULES - DevRoboLab (devrobolab)

Only the rules special to this channel. Read `shared/RULES.md` first; everything there applies here too.
- Channel RULES can be stricter than shared RULES, never looser. Copyright, channel ID, secrets and upload safety can never be relaxed by a channel.

## Content
- Topic: Claude Code / Claude features explained as Shorts. Source ONLY the official docs (https://code.claude.com/docs, index llms.txt). No blogs, no other creators' material.
- Scope widened by the user 2026-11-04: also AI NEWS from the whole field (new models, features, enhancements, free/open tools from any AI organisation) to keep viewers updated. Source = the organisation's OWN official page/docs/blog/changelog for that item (never press or other creators as the only source; press/HN only to discover). Every claim traceable to that page; price/limit/date/benchmark only if the page states it. Description: the source URL + 'Unofficial channel, not affiliated with <organisation>.' Never use another organisation's logos/branding or a product's official voice; describe, do not imitate. Item selection and daily suggestions: NEWS_WATCH.md.
- Every claim must be traceable to the docs page of that topic; the source URL goes in the video description. `yb-jaanchak` (fact-check) must PASS before any upload.
- Unofficial channel: description always says "Unofficial channel, not affiliated with Anthropic." Never use Anthropic/Claude logos or official branding; no "Claude" in the channel name.
- No claims about prices, limits or availability unless the page states them; say "docs ke hisaab se" when unsure.

## Look (STYLE_GUIDE.md v2 is binding)
- White background, black + yellow text, robot mascot, conversational Hinglish (Roman script), Funkorama music (Kevin MacLeod, CC BY 4.0).
- First 6-7 s = picture story (scene type `stage`), never plain text. Every video adds at least one new enhancement; layouts differ from the previous video.
- Music credit line in every description: "Music: Funkorama by Kevin MacLeod (incompetech.com), CC BY 4.0".

## Production and publishing
- Shorts only for now (35-70 s, 1080x1920). Long videos later, after Shorts data (see log.md).
- Upload is always PRIVATE (api_audited false). The user makes videos public in Studio. Never schedule or publish automatically.
- Own Google Cloud project `yellow-bot-devrobo` (own YouTube quota 10,000 units/day = 6 uploads/day). Queue the rest for the next day.
- Start at 3-6 uploads/day; raise only after the user OKs (repetitive-content risk).
- Cost: voice paid Gemini TTS ~Rs1.6 per video allowed (user 2026-10-31); daily cap Rs20; stop if Google balance < Rs50. Images/music/slides are free (Cloudflare, local HTML render).
- OAuth app is in Testing mode: token expires after 7 days (renew `tools/yt_auth.py devrobolab`, renewed 2026-11-06, next due ~2026-11-13).

## Metadata
- Title: topic + hook in Hinglish, max 70 chars, suffix `| DevRoboLab` is optional (Shorts). Tags in Hinglish + English (claude code, ai, hooks, mcp ...).
- category_id 28 (Science & Technology), made_for_kids false, default_language hi.
