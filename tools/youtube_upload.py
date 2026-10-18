#!/usr/bin/env python3
"""YouTube uploader for Story-Channel, used by the Munshi agent.

Usage:
    python tools/youtube_upload.py --job long-videos/long_01/output/upload.json --dry-run
    python tools/youtube_upload.py --job long-videos/long_01/output/upload.json
    python tools/youtube_upload.py --job ... --extras-only   # retry thumbnail/captions/playlist

One-time setup: see the youtube-publish skill. Needs
    pip install google-api-python-client google-auth-oauthlib
and secrets/client_secret.json (OAuth "Desktop app" client).
"""
import argparse
import datetime as dt
import json
import random
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SECRETS = ROOT / "secrets"
CLIENT_SECRET = SECRETS / "client_secret.json"
TOKEN = SECRETS / "youtube_token.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",  # captions + playlists
]
RETRY_STATUS = {500, 502, 503, 504}
MAX_RETRIES = 8


def resolve(job_path: Path, p):
    if not p:
        return None
    p = Path(p)
    return p if p.is_absolute() else (job_path.parent / p).resolve()


def validate(job: dict, job_path: Path) -> list:
    errs = []
    title = job.get("title", "")
    desc = job.get("description", "")
    tags = job.get("tags", [])
    if not title:
        errs.append("title missing")
    if len(title) > 100:
        errs.append(f"title too long ({len(title)} > 100)")
    if len(desc) > 5000:
        errs.append(f"description too long ({len(desc)} > 5000)")
    for name, val in (("title", title), ("description", desc)):
        if "<" in val or ">" in val:
            errs.append(f"{name} contains < or >")
    if sum(len(t) for t in tags) + max(len(tags) - 1, 0) > 500:
        errs.append("tags exceed 500 characters")
    hashtags = [w for w in desc.split() if w.startswith("#")]
    if len(hashtags) > 15:
        errs.append(f"{len(hashtags)} hashtags in description (>15: YouTube ignores all)")
    if not isinstance(job.get("made_for_kids"), bool):
        errs.append("made_for_kids must be true/false (set it in munshi/channel_config.json)")

    video = resolve(job_path, job.get("video"))
    if not video or not video.exists():
        errs.append(f"video not found: {video}")
    elif "preview" in video.name.lower():
        errs.append("video looks like a preview build; upload final only")

    thumb = resolve(job_path, job.get("thumbnail"))
    if thumb:
        if not thumb.exists():
            errs.append(f"thumbnail not found: {thumb}")
        elif thumb.stat().st_size > 2 * 1024 * 1024:
            errs.append("thumbnail larger than 2 MB")
        elif thumb.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            errs.append("thumbnail must be .jpg or .png")

    srt = resolve(job_path, job.get("captions"))
    if srt and not srt.exists():
        errs.append(f"captions not found: {srt}")

    pub = job.get("publish_at")
    if pub:
        try:
            t = dt.datetime.fromisoformat(pub)
            if t.tzinfo is None:
                errs.append("publish_at needs a timezone, e.g. 2026-10-21T19:00:00+05:30")
            elif t <= dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15):
                errs.append("publish_at must be at least 15 minutes in the future")
        except ValueError:
            errs.append("publish_at is not ISO 8601")
    if job.get("privacy", "private") not in ("private", "unlisted", "public"):
        errs.append("privacy must be private, unlisted or public")
    return errs


def get_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                sys.exit(f"Missing {CLIENT_SECRET}. Do the one-time setup first.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        SECRETS.mkdir(exist_ok=True)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def with_retry(fn, label):
    from googleapiclient.errors import HttpError

    for attempt in range(MAX_RETRIES + 1):
        try:
            return fn()
        except HttpError as e:
            if e.resp.status not in RETRY_STATUS or attempt == MAX_RETRIES:
                raise
        except (ConnectionError, OSError, TimeoutError):
            if attempt == MAX_RETRIES:
                raise
        wait = min(2 ** attempt + random.random(), 60)
        print(f"{label}: retry {attempt + 1} in {wait:.0f}s")
        time.sleep(wait)


def upload_video(yt, job, job_path):
    from googleapiclient.http import MediaFileUpload

    status = {
        "privacyStatus": job.get("privacy", "private"),
        "selfDeclaredMadeForKids": job["made_for_kids"],
    }
    if "contains_synthetic_media" in job:
        status["containsSyntheticMedia"] = bool(job["contains_synthetic_media"])
    if job.get("publish_at"):
        status["privacyStatus"] = "private"  # required by YouTube for scheduling
        status["publishAt"] = job["publish_at"]

    body = {
        "snippet": {
            "title": job["title"],
            "description": job.get("description", ""),
            "tags": job.get("tags", []),
            "categoryId": str(job.get("category_id", "1")),
            "defaultLanguage": job.get("language", "hi"),
            "defaultAudioLanguage": job.get("language", "hi"),
        },
        "status": status,
    }
    media = MediaFileUpload(str(resolve(job_path, job["video"])), mimetype="video/mp4",
                            chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        st, response = with_retry(req.next_chunk, "upload")
        if st:
            print(f"upload {int(st.progress() * 100)}%")
    return response["id"]


def do_extras(yt, job, job_path, video_id, result):
    from googleapiclient.http import MediaFileUpload

    thumb = resolve(job_path, job.get("thumbnail"))
    if thumb and not result.get("thumbnail_ok"):
        try:
            mt = "image/png" if thumb.suffix.lower() == ".png" else "image/jpeg"
            with_retry(lambda: yt.thumbnails().set(
                videoId=video_id, media_body=MediaFileUpload(str(thumb), mimetype=mt)).execute(),
                "thumbnail")
            result["thumbnail_ok"] = True
        except Exception as e:  # usually: channel not phone-verified
            result["thumbnail_error"] = str(e)[:300]

    srt = resolve(job_path, job.get("captions"))
    if srt and not result.get("captions_ok"):
        try:
            lang = job.get("language", "hi")
            with_retry(lambda: yt.captions().insert(
                part="snippet",
                body={"snippet": {"videoId": video_id, "language": lang,
                                  "name": job.get("captions_name", "Hindi"), "isDraft": False}},
                media_body=MediaFileUpload(str(srt), mimetype="application/octet-stream"),
            ).execute(), "captions")
            result["captions_ok"] = True
        except Exception as e:
            result["captions_error"] = str(e)[:300]

    pl = job.get("playlist_id")
    if pl and not result.get("playlist_ok"):
        try:
            with_retry(lambda: yt.playlistItems().insert(
                part="snippet",
                body={"snippet": {"playlistId": pl,
                                  "resourceId": {"kind": "youtube#video", "videoId": video_id}}},
            ).execute(), "playlist")
            result["playlist_ok"] = True
        except Exception as e:
            result["playlist_error"] = str(e)[:300]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True, help="path to upload.json")
    ap.add_argument("--dry-run", action="store_true", help="validate only, no network")
    ap.add_argument("--extras-only", action="store_true",
                    help="retry thumbnail/captions/playlist for an already uploaded video")
    args = ap.parse_args()

    job_path = Path(args.job).resolve()
    job = json.loads(job_path.read_text(encoding="utf-8"))
    result_path = job_path.parent / "upload_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}

    errs = validate(job, job_path)
    print("Title:       ", job.get("title"))
    print("Video:       ", resolve(job_path, job.get("video")))
    print("Privacy:     ", "scheduled" if job.get("publish_at") else job.get("privacy", "private"))
    print("Publish at:  ", job.get("publish_at") or "-")
    print("Made for kids:", job.get("made_for_kids"))
    print("Thumbnail:   ", job.get("thumbnail") or "-")
    print("Captions:    ", job.get("captions") or "-")
    print("Playlist:    ", job.get("playlist_id") or "-")
    if errs:
        print("\nPROBLEMS:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    if args.dry_run:
        print("\nDry run OK. Nothing uploaded.")
        return

    if result.get("video_id") and not args.extras_only:
        sys.exit(f"Already uploaded as {result['video_id']}. Use --extras-only to retry extras.")
    if args.extras_only and not result.get("video_id"):
        sys.exit("No video_id in upload_result.json; nothing to retry.")

    yt = get_service()
    if not result.get("video_id"):
        vid = upload_video(yt, job, job_path)
        result.update({
            "video_id": vid,
            "url": f"https://youtu.be/{vid}",
            "studio_url": f"https://studio.youtube.com/video/{vid}/edit",
            "uploaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "publish_at": job.get("publish_at"),
        })
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Uploaded:", result["url"])

    do_extras(yt, job, job_path, result["video_id"], result)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
