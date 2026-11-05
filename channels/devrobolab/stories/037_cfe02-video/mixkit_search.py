"""List Mixkit stock videos (JSON-LD on tag pages) with their licence label. Only 'Free License' items are kept. Run: python mixkit_search.py"""
import json, re, subprocess, time
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/150 Safari/537.36"
TAGS = ["typing", "laptop", "documents", "folder", "files", "writing", "coding", "chat", "smartphone", "office", "lock", "desk", "paper", "notebook", "paperwork", "computer"]
out = {}
for tag in TAGS:
    h = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, f"https://mixkit.co/free-stock-video/{tag}/"], capture_output=True, text=True).stdout
    items = []
    def walk(o):
        if isinstance(o, dict):
            if o.get("@type") == "VideoObject": items.append({"name": o.get("name"), "desc": (o.get("description") or "")[:140], "url": o.get("contentUrl"), "thumb": o.get("thumbnailUrl"), "lic": str(o.get("license"))[-40:], "page": o.get("@id")})
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for m in re.finditer(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', h, flags=re.S):
        try: walk(json.loads(m.group(1)))
        except Exception: pass
    seen = set(); items = [i for i in items if i["url"] and not (i["url"] in seen or seen.add(i["url"])) and "videoFree" in i["lic"]]
    out[tag] = items
    print(tag, len(items), flush=True)
    time.sleep(2)
json.dump(out, open("raw/mixkit_candidates.json", "w"), indent=1, ensure_ascii=False)
