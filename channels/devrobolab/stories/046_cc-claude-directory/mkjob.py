import json
from pathlib import Path
H = Path(__file__).parent
desc = ("Claude Code 03: .claude folder. Claude Code apni instructions, settings, skills, subagents aur memory do jagah se padhta hai: project ka .claude folder (git me commit, team ke saath share) aur home folder ka .claude (sirf aapke liye). "
 "Zyadatar log sirf CLAUDE.md aur settings.json badalte hain. Video me: terminal demo (ls .claude, settings.json permissions, CLAUDE.md me tests ki command), kaun si baat kis file me jaye (CLAUDE.md, settings.json, .mcp.json, settings.local.json), "
 "optional folders (skills, agents, rules, output-styles), CLAUDE.local.md aur AGENTS.md, managed settings, aur chetavni: transcripts plain text me hote hain (.env ki value bhi ja sakti hai), 30 din baad auto delete, claude purge ko pehle --dry-run se chalao, aur claude.json, settings.json, plugins kabhi delete mat karo.\n\n"
 "Source (official):\nhttps://code.claude.com/docs/en/claude-directory\n\n"
 "Unofficial channel, not affiliated with Anthropic.\n\n"
 "Note: the terminal and file screens in this video are our own illustration (not a recording); the settings.json content is an example. Synthetic voice.\n\n"
 "Music: \"Funkorama\" Kevin MacLeod (incompetech.com)\nLicensed under Creative Commons: By Attribution 4.0 License\nhttp://creativecommons.org/licenses/by/4.0/\n\n"
 "#ClaudeCode #Claude #AI #Hinglish #Developer")
job = {"channel_key": "devrobolab", "channel_name": "DevRoboLab", "channel_id": "UCpElgKdJOgQiyfwdGXz6GmA", "format": "long", "parent_video_id": None,
 "title": "Claude Code 03: .claude folder me kaun si files hoti hain", "description": desc,
 "tags": ["Claude Code", "CLAUDE.md", "settings.json", ".claude folder", "Claude Code tutorial", "AI coding", "Hinglish", "Hindi tech"],
 "video": "long.mp4", "language": "hi", "made_for_kids": False, "contains_synthetic_media": True, "category_id": "28", "privacy": "private", "playlist_id": "PLGTgifZfJLow"}
(H / "output/upload.json").write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8"); print(len(job["title"]), "title chars", ("<" in desc or ">" in desc))
