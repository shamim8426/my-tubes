"""Download CC0 sound-effect candidates from Freesound (HQ previews, token auth).

Usage: python scripts/fetch_sfx.py
Output: shared/sfx/<kind>_<id>.mp3 + shared/sfx/CREDITS.md (CC0: no attribution needed, kept for records)
"""
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
OUT = ROOT / "shared" / "sfx"
API = "https://freesound.org/apiv2/search/"

WANT = {
    "comedy_sting": "cartoon boing",
    "tension_sting": "suspense sting dramatic",
    "whoosh": "whoosh swish",
    "magic": "magic sparkle chime",
}
PER_KIND = 2


def main():
    token = os.environ.get("FREESOUND_API_KEY")
    if not token:
        raise SystemExit("FREESOUND_API_KEY missing in .env")
    OUT.mkdir(parents=True, exist_ok=True)
    cfile = OUT / "CREDITS.md"
    credits = cfile.read_text(encoding="utf-8").splitlines() if cfile.exists() else ["# Sound effects (Freesound, all CC0)", ""]
    kinds = sys.argv[1:] or list(WANT)
    for kind in kinds:
        query = WANT[kind]
        r = requests.get(API, params={
            "query": query, "filter": 'license:"Creative Commons 0" duration:[0.3 TO 4]',
            "sort": "score", "page_size": 10,
            "fields": "id,name,username,license,duration,previews,url,avg_rating,num_downloads",
        }, headers={"Authorization": f"Token {token}"}, timeout=30)
        r.raise_for_status()
        results = r.json()["results"][:PER_KIND]
        for s in results:
            f = OUT / f"{kind}_{s['id']}.mp3"
            f.write_bytes(requests.get(s["previews"]["preview-hq-mp3"], timeout=60).content)
            line = f"- `{f.name}` — \"{s['name']}\" by {s['username']} ({s['duration']:.1f}s, CC0) {s['url']}"
            if line not in credits:
                credits.append(line)
            print(kind, line)
    cfile.write_text("\n".join(credits) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
