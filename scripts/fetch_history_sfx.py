"""Download CC0 period-appropriate sound effects / ambiences for History videos from Freesound (token auth, HQ mp3 previews).
    .venv\\Scripts\\python -X utf8 scripts\\fetch_history_sfx.py
Output: shared/sfx/history/<kind>_<id>.mp3 + shared/sfx/history/CREDITS.md. CC0 only, no music. Rs0."""
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
OUT = ROOT / "shared/sfx/history"
OUT.mkdir(parents=True, exist_ok=True)
API = "https://freesound.org/apiv2/search/text/"
# kind -> (query, duration filter)
WANT = {
    "market_crowd": ("market crowd", "[5 TO 90]"),
    "camel_bell": ("bell", "[2 TO 20]"),
    "camel_groan": ("camel", "[1 TO 8]"),
    "horse_neigh": ("horse neigh", "[1 TO 8]"),
    "hooves": ("horse hooves", "[1 TO 20]"),
    "well_water": ("water pouring", "[2 TO 15]"),
    "steps_sand": ("footsteps sand gravel walking", "[3 TO 15]"),
    "palm_leaves": ("leaves rustle wind", "[3 TO 40]"),
    "fire_crackle": ("small fire crackle campfire", "[6 TO 30]"),
    "stone_grind": ("stone grinding", "[2 TO 20]"),
    "wood_door": ("wooden door open close old", "[1 TO 6]"),
    "crowd_far": ("crowd murmur", "[5 TO 90]"),
    "goat_sheep": ("goats bleating", "[3 TO 20]"),
    "night_crickets": ("crickets night", "[5 TO 60]"),
    "wind_desert": ("desert wind", "[8 TO 40]"),
    "cloth_rustle": ("cloth fabric rustle", "[1 TO 5]"),
}


def main():
    token = os.environ["FREESOUND_API_KEY"]
    credits = ["# History SFX (Freesound, CC0 only)\n"]
    for kind, (q, dur) in WANT.items():
        got = 0
        r = requests.get(API, params={"query": q, "filter": f'license:"Creative Commons 0" duration:{dur}',
                                      "fields": "id,name,username,duration,previews,url", "page_size": 8, "sort": "rating_desc",
                                      "token": token}, timeout=30)
        if not r.ok:
            print(kind, "search failed", r.status_code)
            continue
        for s in r.json().get("results", []):
            if got >= 2:
                break
            p = s["previews"].get("preview-hq-mp3")
            f = OUT / f"{kind}_{s['id']}.mp3"
            if not f.exists():
                a = requests.get(p, timeout=60)
                if not a.ok:
                    continue
                f.write_bytes(a.content)
            credits.append(f"- `{f.name}` - \"{s['name']}\" by {s['username']} ({s['duration']:.1f}s, CC0) {s['url']}\n")
            got += 1
        print(kind, got)
    (OUT / "CREDITS.md").write_text("".join(credits), encoding="utf-8")


main()
