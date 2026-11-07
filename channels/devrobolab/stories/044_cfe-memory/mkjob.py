import json
from pathlib import Path
H = Path(__file__).parent
desc = ("Claude Feature 05 (Claude for Everyone): Memory. Claude aapki baatcheet se chhote topics yaad rakhta hai (kaam, project, pasand). "
 "Settings me Your Claude kholkar 'Generate memory from chats' toggle se Pause ya Reset karo. Manage se topics dekho, edit ya delete karo. "
 "Ek chat bina memory ke: nayi chat me plus dabake Memory band karo (pehla message bhejne se pehle), ya ghost icon se Incognito chat. "
 "Har project ki apni memory. Dhyan rakho: chat delete karne se uski memory nahi mitati, usse alag se delete karna padta hai.\n\n"
 "Source (official):\nhttps://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context\n\n"
 "Unofficial channel, not affiliated with Anthropic.\n\n"
 "Note: the Settings and chat screens in this video are our own illustration (not a recording). The official page screenshot is our own capture with the key line highlighted. Names in the examples are made up. Synthetic voice.\n\n"
 "Music: \"Funkorama\" Kevin MacLeod (incompetech.com)\nLicensed under Creative Commons: By Attribution 4.0 License\nhttp://creativecommons.org/licenses/by/4.0/\n\n"
 "#Claude #ClaudeMemory #ClaudeForEveryone #AI #Hinglish")
job = {"channel_key": "devrobolab", "channel_name": "DevRoboLab", "channel_id": "UCpElgKdJOgQiyfwdGXz6GmA", "format": "long", "parent_video_id": None,
 "title": "Claude Feature 05: Claude ko aapki baatein yaad rakhna (Memory)", "description": desc,
 "tags": ["Claude", "Claude Memory", "Claude for Everyone", "Claude app tutorial", "AI tools", "Hinglish", "Hindi tech"],
 "video": "long_final.mp4", "language": "hi", "made_for_kids": False, "contains_synthetic_media": True, "category_id": "28", "privacy": "private", "playlist_id": "PLEklr-qY9V3U"}
(H / "output/upload.json").write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8"); print(len(job["title"]), "title chars")

