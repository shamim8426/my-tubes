import json
from pathlib import Path
H = Path(__file__).parent
desc = ("Claude Code 04: prompt caching. Claude Code har message par poora context dobara bhejta hai, aur prompt caching se API purana hissa sasti cached rate par padh leti hai, sirf naya hissa process karti hai. "
 "Video me: prefix match ka niyam (system prompt, CLAUDE.md, conversation), kya cache todta hai (model badalna, fast mode, tool definitions, bahut saari images), terminal demo (/model aur /usage ka Prompt cache line), "
 "kya cache nahi todta (files edit, permission mode, output style, skills, /recap, /rewind, CLAUDE.md ka mid-session edit), /compact ka kharcha, cache ki lifetime (TTL: subscription par 1 ghanta, API key par 5 minute, promptCacheTtl setting), "
 "aur cache hit rate kaise check karein (cache read vs cache creation tokens).\n\n"
 "Source (official):\nhttps://code.claude.com/docs/en/prompt-caching\n\n"
 "Unofficial channel, not affiliated with Anthropic.\n\n"
 "Note: the terminal screens in this video are our own illustration (not a recording); the numbers shown are examples. Synthetic voice.\n\n"
 "Music: \"Funkorama\" Kevin MacLeod (incompetech.com)\nLicensed under Creative Commons: By Attribution 4.0 License\nhttp://creativecommons.org/licenses/by/4.0/\n\n"
 "#ClaudeCode #Claude #AI #Hinglish #Developer")
job = {"channel_key": "devrobolab", "channel_name": "DevRoboLab", "channel_id": "UCpElgKdJOgQiyfwdGXz6GmA", "format": "long", "parent_video_id": None,
 "title": "Claude Code 04: Prompt caching, kya cache todta hai", "description": desc,
 "tags": ["Claude Code", "prompt caching", "Claude Code tutorial", "AI coding", "token usage", "Hinglish", "Hindi tech"],
 "video": "long.mp4", "language": "hi", "made_for_kids": False, "contains_synthetic_media": True, "category_id": "28", "privacy": "private", "playlist_id": "PLGTgifZfJLow"}
(H / "output/upload.json").write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8"); print(len(job["title"]), "title chars", ("<" in desc or ">" in desc))
