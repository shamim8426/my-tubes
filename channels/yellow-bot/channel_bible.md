# Channel bible - yellow Bot (yellow-bot)

## Idea
Short Hinglish explainers of Claude Code features from the official docs, in a white/black/yellow presentation style with a cute robot mascot.
Audience: Indian beginners/devs who want to use Claude Code properly. Tone: friendly desi tech YouTuber, clear, not funny-for-the-sake-of-it.

## Mascot
- Cute round robot: dark visor, glowing yellow eyes, white + yellow body, small antenna (mascot/*.png: wave, think, work, stop, thumbs; team.png for 4-robot lineups).
- Claude robot = the one who edits/works; "helper" robots (gear, magnifier, clipboard, book) = hooks, subagents, tools. Look never changes.

## Format of every Short
1. Picture-story opener (0-7 s): the robot demonstrates the feature. 2. What it is. 3. Real example. 4. Config/code (docs shot or typing card). 5. Options/list. 6. One useful trick (compare). 7. CTA (comment question).
Details and scene types: STYLE_GUIDE.md, templates/deck_template.html. Build: `scripts/build_deck.py`.

## Voice
Gemini TTS `Charon`, casual Hinglish, no sing-song (style text in each deck.json).

## Do not
No copying of other creators' scripts/visuals; no third-party logos; no unverified claims; no fake "official" look.
