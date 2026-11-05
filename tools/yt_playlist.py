"""Create a public YouTube playlist on a channel (checks channel id first).
Usage: python tools/yt_playlist.py <channel_key> "<title>" "<description>"
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yt_auth import config, service  # noqa: E402


def main():
    key, title, desc = sys.argv[1], sys.argv[2], sys.argv[3]
    cfg = config(key)
    yt = service(key, interactive=False)
    mine = yt.channels().list(part="id,snippet", mine=True).execute()["items"][0]
    want = cfg.get("channel_id") or cfg.get("youtube_channel_id")
    if want and mine["id"] != want:
        sys.exit(f"WRONG CHANNEL {mine['id']} != {want}. Nothing created.")
    r = yt.playlists().insert(part="snippet,status", body={
        "snippet": {"title": title, "description": desc},
        "status": {"privacyStatus": "public"}}).execute()
    print(json.dumps({"playlist_id": r["id"], "title": title}))


if __name__ == "__main__":
    main()
