"""DevRoboLab growth snapshot (read-only). Uses secrets/devrobolab/token.json (YouTube Data + Analytics both work with it).
Usage: D:\my-tubes\.venv\Scripts\python.exe -X utf8 channels/devrobolab/growth/fetch_snapshot.py [start YYYY-MM-DD]
Writes growth/snapshots/<today>.md : totals, daily views, traffic, format, audience, per-video table sorted by views."""
import sys, datetime as dt
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
ROOT = Path(__file__).resolve().parents[3]
c = Credentials.from_authorized_user_file(str(ROOT / "secrets/devrobolab/token.json")); c.refresh(Request())
a = build("youtubeAnalytics", "v2", credentials=c); y = build("youtube", "v3", credentials=c)
start = sys.argv[1] if len(sys.argv) > 1 else "2026-10-31"
end = dt.date.today().isoformat()
def q(**k):
    try: return a.reports().query(ids="channel==MINE", startDate=start, endDate=end, **k).execute().get("rows", [])
    except Exception as e: return [["ERR", str(e)[:100]]]
ch = y.channels().list(part="statistics,contentDetails", mine=True).execute()["items"][0]
L = [f"# Snapshot {end} (from {start})", f"Channel: {ch['statistics']}", ""]
L += ["## Daily (day, views, minutes, subs)"] + [str(r) for r in q(dimensions="day", metrics="views,estimatedMinutesWatched,subscribersGained", sort="day")]
L += ["", "## Traffic (source, views, minutes)"] + [str(r) for r in q(dimensions="insightTrafficSourceType", metrics="views,estimatedMinutesWatched", sort="-views")]
L += ["", "## Format (type, views, min, avgDur s, avg %, subs)"] + [str(r) for r in q(dimensions="creatorContentType", metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained")]
L += ["", "## Audience age/gender %"] + [str(r) for r in q(dimensions="ageGroup,gender", metrics="viewerPercentage", sort="-viewerPercentage", maxResults=8)]
L += ["", "## Search terms (YouTube search)"] + [str(r) for r in q(dimensions="insightTrafficSourceDetail", metrics="views", filters="insightTrafficSourceType==YT_SEARCH", sort="-views", maxResults=15)]
rows = q(dimensions="video", metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments", sort="-views", maxResults=200)
ids = [r[0] for r in rows if r[0] != "ERR"]; info = {}
for i in range(0, len(ids), 50):
    for v in y.videos().list(part="snippet,contentDetails,status", id=",".join(ids[i:i+50])).execute()["items"]:
        info[v["id"]] = (v["snippet"]["publishedAt"][:10], v["contentDetails"]["duration"], v["status"]["privacyStatus"], v["snippet"]["title"][:70])
L += ["", "## Videos (id | published | duration | privacy | views, min, avgDur s, avg %, subs, likes, comments | title)"]
for r in rows:
    if r[0] in info: L.append(f"{r[0]} | {info[r[0]][0]} | {info[r[0]][1]} | {info[r[0]][2]} | {r[1:]} | {info[r[0]][3]}")
out = ROOT / "channels/devrobolab/growth/snapshots" / f"{end}.md"
out.write_text("\n".join(L), encoding="utf-8"); print(out)
