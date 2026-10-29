#!/usr/bin/env python3
"""One-off rebrand: replace the old channel name in already uploaded videos (title, description, tags).

Usage:
    python tools/rebrand_update.py --channel jugnu-stories              (dry run: read + show old -> new, change nothing)
    python tools/rebrand_update.py --channel jugnu-stories --apply      (after the user's OK: videos.update)
    add --thumb <video_id>=<png> to also set a new custom thumbnail on --apply (not for Shorts)

Reads the videos through the API (videos.list, 1 unit each); --apply calls videos.update (50 units each, snippet only:
privacy and schedule are not touched). Never prints tokens.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import youtube_upload as yu  # noqa: E402

# order matters: the full old tagline first, then names and hashtags
REPLACE = [
    # (b) Case 01: series name in the title, brand at the end
    ("| दादी की कहानियाँ केस #1 #shorts", "| दादी जासूस केस #1 | Jugnu Stories #shorts"),
    # (c) Case 01: 8 hashtags -> 5 (RULES 7)
    ("#दादीकीकहानियाँ #DadiKiKahaniyan #HindiMystery #पहेली #MysteryShorts #HindiCartoon #DetectiveStory #Shorts",
     "#Shorts #JugnuStories #दादीजासूस #HindiMystery #पहेली"),
    ("दादी की कहानियाँ — दादी हर हफ़्ते सुनाती हैं एक नई कहानी, जो हँसाए भी और सिखाए भी।",
     "Jugnu Stories — हर शाम एक नया किस्सा, जो हँसाए भी और सिखाए भी।"),
    ("#दादीकीकहानियाँ", "#JugnuStories"),
    ("#DadiKiKahaniyan", "#Jugnu Stories"),
    ("दादी की कहानियाँ", "Jugnu Stories"),
    ("Dadi Ki Kahaniyan", "Jugnu Stories"),
]


# (a) tags: kids-only wording -> family wording (RULES 7 family rule, channel made_for_kids = false)
TAG_REPLACE = {"Kids Story Hindi": "Family Story Hindi", "बच्चों की कहानी": "परिवार की कहानी"}


def rebrand(text: str) -> str:
    for a, b in REPLACE:
        text = text.replace(a, b)
    return text


def find_video_ids(yt, channel_id, known):
    """Our known video ids + every upload on the channel that still carries the old name."""
    ch = yt.channels().list(part="contentDetails", id=channel_id).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = list(known), None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=page).execute()
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page:
            return list(dict.fromkeys(ids))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--thumb", action="append", default=[], help="video_id=path.png (applied with --apply)")
    a = ap.parse_args()
    cfg = json.loads((ROOT / "channels" / a.channel / "channel.json").read_text(encoding="utf-8"))
    job = {"channel_key": cfg["channel_key"], "channel_id": cfg["channel_id"], "channel_name": cfg["display_name"]}
    yt = yu.get_service(job)
    yu.check_channel(yt, job)
    known = [json.loads(p.read_text(encoding="utf-8"))["video_id"]
             for p in (ROOT / "channels" / a.channel).rglob("upload_result.json")]
    ids = find_video_ids(yt, cfg["channel_id"], known)
    items = []
    for i in range(0, len(ids), 50):
        items += yt.videos().list(part="snippet,status", id=",".join(ids[i:i + 50])).execute().get("items", [])
    thumbs = dict(t.split("=", 1) for t in a.thumb)
    changed = 0
    for v in items:
        sn = v["snippet"]
        new_title, new_desc = rebrand(sn["title"]), rebrand(sn.get("description", ""))
        new_tags = list(dict.fromkeys(TAG_REPLACE.get(t, rebrand(t)) for t in sn.get("tags", [])))
        if (new_title, new_desc, new_tags) == (sn["title"], sn.get("description", ""), sn.get("tags", [])) \
                and v["id"] not in thumbs:
            continue
        changed += 1
        print(f"=== {v['id']}  ({v['status'].get('privacyStatus')}, publishAt {v['status'].get('publishAt', '-')})")
        print(f"TITLE old: {sn['title']}\nTITLE new: {new_title}")
        old_lines, new_lines = sn.get("description", "").splitlines(), new_desc.splitlines()
        for o, n in zip(old_lines, new_lines):
            if o != n:
                print(f"DESC  old: {o}\nDESC  new: {n}")
        if new_tags != sn.get("tags", []):
            print(f"TAGS  old: {', '.join(sn.get('tags', []))}\nTAGS  new: {', '.join(new_tags)}")
        if v["id"] in thumbs:
            print(f"THUMB new: {thumbs[v['id']]}")
        if len(new_title) > 100 or len(new_desc) > 5000:
            sys.exit(f"STOP: {v['id']} new title/description too long")
        if a.apply:
            body = {"id": v["id"], "snippet": {**{k: sn[k] for k in ("categoryId", "defaultLanguage", "defaultAudioLanguage")
                                                  if k in sn},
                                               "title": new_title, "description": new_desc, "tags": new_tags}}
            yt.videos().update(part="snippet", body=body).execute()
            print("  -> updated")
            if v["id"] in thumbs:
                from googleapiclient.http import MediaFileUpload
                p = Path(thumbs[v["id"]])
                yt.thumbnails().set(videoId=v["id"], media_body=MediaFileUpload(str(p), mimetype="image/png")).execute()
                print("  -> thumbnail set")
    print(f"\n{changed} video(s) {'updated' if a.apply else 'would change'}; {'' if a.apply else 'DRY RUN, nothing changed.'}")


if __name__ == "__main__":
    main()
