r"""Put the generated thumbnails on YouTube (thumbnails.set, DevRoboLab token). IDs are checked against the channel's own upload list first.
    .venv\Scripts\python -X utf8 channels\devrobolab\thumbnails\apply_thumbs.py [video_id ...]     (no ids = all; --check = only validate)
A thumbnail is only set when the file exists; a 403/other error is printed and the run goes on with the next one. Never changes anything else on a video."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import make_thumbs

c = Credentials.from_authorized_user_file(str(ROOT / "secrets/devrobolab/token.json")); y = build("youtube", "v3", credentials=c)
ch = y.channels().list(part="contentDetails", mine=True).execute()["items"][0]
up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
have = set(); tok = None
while True:
    r = y.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
    have |= {i["contentDetails"]["videoId"] for i in r["items"]}; tok = r.get("nextPageToken")
    if not tok: break
args = [a for a in sys.argv[1:] if not a.startswith("--")]
bad = [v[0] for v in make_thumbs.VIDEOS if v[0] not in have]
print("channel videos:", len(have), "| designs:", len(make_thumbs.VIDEOS), "| IDs not on the channel:", bad)
if bad or "--check" in sys.argv:
    sys.exit(1 if bad else 0)
ok = fail = 0
for vid, ori, *_ in make_thumbs.VIDEOS:
    if args and vid not in args: continue
    f = make_thumbs.OUT / f"{vid}_{'16x9' if ori == make_thumbs.L else '9x16'}.png"
    if not f.exists(): print("missing", f.name); fail += 1; continue
    try:
        y.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(f), mimetype="image/png")).execute()
        print("set", vid, f.name, f.stat().st_size // 1024, "KB"); ok += 1
    except HttpError as e:
        print("FAIL", vid, e.resp.status, str(e)[:160]); fail += 1
print("done: set", ok, "failed", fail)
