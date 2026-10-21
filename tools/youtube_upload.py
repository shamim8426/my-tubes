#!/usr/bin/env python3
"""YouTube uploader for Story-Channel, used by the Munshi agent.

Usage:
    python tools/youtube_upload.py --job channels/dadi-ki-kahaniyan/stories/001_lalchi-halwai/long/output/upload.json --dry-run
    python tools/youtube_upload.py --job channels/dadi-ki-kahaniyan/stories/001_lalchi-halwai/long/output/upload.json
    python tools/youtube_upload.py --job ... --extras-only   # retry thumbnail/captions/playlist

Safety: refuses to upload unless the logged-in channel ID matches job["channel_id"],
and unless ffprobe confirms the file is a real final build (size, codec, pix_fmt).
One token per channel: secrets/youtube_token_<channel_key>.json.

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
FORMATS = {  # what a final upload must look like
    "long": {"width": 1920, "height": 1080, "max_seconds": None},
    "short": {"width": 1080, "height": 1920, "max_seconds": 60},
}
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


def token_path(job):
    return SECRETS / f"youtube_token_{job['channel_key']}.json"


def probe(video: Path):
    """Return (width, height, codec, pix_fmt, seconds) using ffprobe."""
    import shutil
    import subprocess

    ffprobe = shutil.which("ffprobe")
    if not ffprobe:  # fallback: project's own FFmpeg build (bin/ layout, or flat tools/ffmpeg on this PC)
        ffprobe = next((str(p) for p in (ROOT / "tools" / "ffmpeg" / "bin" / "ffprobe.exe",
                                          ROOT / "tools" / "ffmpeg" / "ffprobe.exe") if p.exists()), None)
    if not ffprobe:
        raise RuntimeError("ffprobe not found (install FFmpeg)")
    out = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,codec_name,pix_fmt",
         "-show_entries", "format=duration", "-of", "json", str(video)],
        capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    st = (d.get("streams") or [{}])[0]
    return (st.get("width"), st.get("height"), st.get("codec_name"),
            st.get("pix_fmt"), float(d.get("format", {}).get("duration", 0)))


def validate(job: dict, job_path: Path) -> list:
    errs = []
    key = job.get("channel_key", "")
    if not key or not all(c.isalnum() or c in "-_" for c in key):
        errs.append("channel_key missing/invalid (e.g. dadi-ki-kahaniyan)")
    cid = job.get("channel_id", "")
    if not (isinstance(cid, str) and cid.startswith("UC") and len(cid) == 24):
        errs.append("channel_id missing/invalid (24 chars, starts with UC; set it in channels/<key>/channel.json)")
    cfg = {}
    if key and not errs:  # the job must match the channel's own config (channels/<key>/channel.json)
        cfg_file = ROOT / "channels" / key / "channel.json"
        if not cfg_file.exists():
            errs.append(f"no channel config: {cfg_file.relative_to(ROOT).as_posix()}")
        else:
            cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
            if cfg.get("channel_id") != cid:
                errs.append(f"channel_id {cid} does not match {cfg_file.relative_to(ROOT).as_posix()} ({cfg.get('channel_id')})")
            if job.get("made_for_kids") != cfg.get("made_for_kids"):
                errs.append("made_for_kids differs from the channel config")
    fmt = job.get("format")
    if fmt not in FORMATS:
        errs.append("format must be 'long' or 'short'")
    if fmt == "short" and "parent_video_id" not in job:
        errs.append("short needs parent_video_id (the long video's id; null only for a stand-alone Short)")
    title = job.get("title", "")
    desc = job.get("description", "")
    tags = job.get("tags", [])
    if not title:
        errs.append("title missing")
    # RULES 12a: no studio/film/anime/artist name in any metadata or file name (hashed list in tools/name_guard.py)
    from name_guard import find_names
    meta_text = " ".join([title, desc, " ".join(tags), str(job.get("first_comment", "")), str(job.get("playlist", "")),
                          *(Path(str(job.get(k, ""))).name.replace("_", " ").replace("-", " ")
                            for k in ("video", "thumbnail", "captions"))])
    if find_names(meta_text):
        errs.append("BLOCK (RULES 12a): a studio/film/anime/artist name is in the title/description/tags/comment/"
                    "file names - remove it before upload")
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
        errs.append("made_for_kids must be true/false (set it in channels/<key>/channel.json)")

    video = resolve(job_path, job.get("video"))
    if not video or not video.exists():
        errs.append(f"video not found: {video}")
    else:
        if "preview" in video.name.lower():
            errs.append("video looks like a preview build; upload final only")
        if fmt in FORMATS:
            try:
                w, h, codec, pix, secs = probe(video)
                want = FORMATS[fmt]
                if (w, h) != (want["width"], want["height"]):
                    errs.append(f"video is {w}x{h}, a final {fmt} must be {want['width']}x{want['height']}")
                if codec != "h264":
                    errs.append(f"video codec is {codec}, expected h264")
                if pix != "yuv420p":
                    errs.append(f"pixel format is {pix}, expected yuv420p")
                if secs < 5:
                    errs.append(f"video is only {secs:.1f}s long")
                if want["max_seconds"] and secs > want["max_seconds"]:
                    errs.append(f"short is {secs:.1f}s, max {want['max_seconds']}s")
                job["_probe"] = f"{w}x{h} {codec} {pix} {secs:.1f}s"
            except Exception as e:
                errs.append(f"ffprobe failed: {e}")

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
    if fmt == "short" and pub == "auto" and job.get("parent_video_id"):
        from publish_slot import find_result, result_publish_time
        if not result_publish_time(find_result(job["parent_video_id"]) or {}):
            errs.append(f"parent {job['parent_video_id']}: no upload_result.json with a publish time (upload the long first)")
    if pub and pub != "auto":  # "auto" = decided after the upload from the IST clock (RULES section 8)
        try:
            t = dt.datetime.fromisoformat(pub)
            if t.tzinfo is None:
                errs.append("publish_at needs a timezone, e.g. 2026-10-21T19:00:00+05:30")
            elif t <= dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15):
                errs.append("publish_at must be at least 15 minutes in the future")
            if t.tzinfo is not None:  # slot per format (RULES section 8; channel.json publish_times_ist)
                ist = t.astimezone(dt.timezone(dt.timedelta(hours=5, minutes=30)))
                want = cfg.get("publish_times_ist", {"long": "19:00", "short": "20:00"}).get(fmt)
                if want and f"{ist:%H:%M}" != want:
                    errs.append(f"publish_at is {ist:%H:%M} IST; a scheduled {fmt} video publishes at {want} IST "
                                "(or use \"publish_at\": \"auto\")")
        except ValueError:
            errs.append("publish_at is not ISO 8601 (or \"auto\")")
    if job.get("earliest_date"):
        try:
            dt.date.fromisoformat(job["earliest_date"])
        except ValueError:
            errs.append("earliest_date must be YYYY-MM-DD")
    if job.get("privacy", "private") not in ("private", "unlisted", "public"):
        errs.append("privacy must be private, unlisted or public")
    return errs


def add_parent_link(job):
    """Short made from a long video: put the long video's link with a CTA line at the top of the description
    (RULES section 8, Short -> Long link). Returns the line (or None)."""
    pid = job.get("parent_video_id")
    if job.get("format") != "short" or not pid:
        return None
    from post_comment import comment_text
    line = comment_text(pid)
    if line not in job.get("description", ""):
        job["description"] = line + "\n\n" + job.get("description", "")
    return line


def plan_publish(yt, job, result):
    """RULES section 8: decide public-now or the schedule from the IST clock right after the upload.
    Returns (when, mode) and stores planned_publish_at / publish_action in result."""
    import publish_slot as ps

    now = ps.now_ist()
    long_time, gap, _ = ps.channel_times(job["channel_key"])
    earliest = dt.date.fromisoformat(job["earliest_date"]) if job.get("earliest_date") else None
    if job["format"] == "long":
        taken = ps.local_long_days(job["channel_key"], result["video_id"])
        try:
            taken |= ps.api_long_days(yt, result["video_id"])
        except Exception as e:  # the local list still counts
            print("note: channel video list not read from the API:", str(e)[:200])
        when, mode = ps.plan_long(now, taken, long_time, earliest)
    elif job.get("parent_video_id"):
        parent = ps.find_result(job["parent_video_id"])
        when, mode = ps.plan_short(now, dt.datetime.fromisoformat(ps.result_publish_time(parent)), gap)
    else:
        when, mode = ps.plan_standalone_short(now, long_time, gap, earliest)
    result["planned_publish_at"] = when.isoformat(timespec="minutes")
    result["publish_action"] = "public_now" if mode == "now" else "schedule"
    return when, mode


def apply_publish(yt, job, result, when, mode):
    """Audited API project (channel.json api_audited = true): set public / publishAt ourselves.
    Otherwise the video stays private and the user gets a STUDIO ACTION message."""
    cfg = json.loads((ROOT / "channels" / job["channel_key"] / "channel.json").read_text(encoding="utf-8"))
    vid = result["video_id"]
    if cfg.get("api_audited"):
        from veto import STATUS_KEEP
        cur = yt.videos().list(part="status", id=vid).execute()["items"][0]["status"]
        body = {k: cur[k] for k in STATUS_KEEP if k in cur}
        if mode == "now":
            body["privacyStatus"] = "public"
        else:
            body.update(privacyStatus="private", publishAt=when.isoformat())
        with_retry(lambda: yt.videos().update(part="status", body={"id": vid, "status": body}).execute(), "status")
        result["status"] = "public (api)" if mode == "now" else "scheduled (api)"
        return None
    result["status"] = "private - studio action pending"
    what = "abhi PUBLIC karo" if mode == "now" else f"{when:%Y-%m-%d %H:%M} IST par SCHEDULE karo"
    lines = [f"STUDIO ACTION ({job['format']}): {vid} \"{job['title']}\"",
             f"  -> {what}   ({result['studio_url']})"]
    if job["format"] == "short" and job.get("parent_video_id"):
        lines.append(f"  -> Related video = {job['parent_video_id']} (https://youtu.be/{job['parent_video_id']})")
    if result.get("comment_task_at"):
        lines.append(f"  -> first comment ~{dt.datetime.fromisoformat(result['comment_task_at']):%Y-%m-%d %H:%M} IST "
                     "aayega: tab pin karo")
    return "\n".join(lines)


def comment_followups(job, job_path, result, when):
    """Schedule the first comment (real publish time + 5 min) and, for a Short of a long, add the manual
    checklist to the channel log (Related video + pin comment stay manual; the API cannot do them)."""
    from post_comment import schedule_task
    when = when + dt.timedelta(minutes=5)
    try:
        result["comment_task"] = schedule_task(job_path, result["video_id"], when)
        result["comment_task_at"] = when.isoformat(timespec="minutes")
    except Exception as e:
        result["comment_task_error"] = str(e)[:300]
    if job.get("format") == "short" and job.get("parent_video_id"):
        log_file = ROOT / "channels" / job["channel_key"] / "log.md"
        with log_file.open("a", encoding="utf-8") as f:
            f.write(f"{dt.date.today().isoformat()} | {Path(job['video']).stem} | short->long checklist | "
                    f"video {result['video_id']} -> long {job['parent_video_id']} | "
                    "related_video: pending, pin_comment: pending\n")


def get_service(job):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    tok = token_path(job)
    creds = None
    if tok.exists():
        creds = Credentials.from_authorized_user_file(str(tok), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                sys.exit(f"Missing {CLIENT_SECRET}. Do the one-time setup first.")
            print(f"Browser login: pick the Google account AND the channel '{job.get('channel_name', job['channel_key'])}'.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        SECRETS.mkdir(exist_ok=True)
        tok.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def check_channel(yt, job):
    """Stop unless the logged-in channel is exactly the configured one."""
    items = yt.channels().list(part="id,snippet", mine=True).execute().get("items", [])
    if not items:
        sys.exit("Logged-in Google account has no YouTube channel. Nothing uploaded.")
    got = items[0]["id"]
    title = items[0]["snippet"]["title"]
    if got != job["channel_id"]:
        sys.exit(f"WRONG CHANNEL: logged in as '{title}' ({got}), expected {job['channel_id']}. "
                 f"Nothing uploaded. Delete {token_path(job).name} in secrets/ and log in again with the right channel.")
    print(f"Channel OK: {title} ({got})")


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
    if job.get("publish_at") == "auto":
        status["privacyStatus"] = "private"  # public/schedule is decided after the upload (plan_publish)
    elif job.get("publish_at"):
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
    ap.add_argument("--force-thumbnail", action="store_true",
                    help="with --extras-only: set the thumbnail again even if it was set before (e.g. after a rebrand)")
    args = ap.parse_args()

    job_path = Path(args.job).resolve()
    job = json.loads(job_path.read_text(encoding="utf-8"))
    result_path = job_path.parent / "upload_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}

    parent_line = add_parent_link(job)
    errs = validate(job, job_path)
    print("Channel:     ", job.get("channel_name") or job.get("channel_key"), job.get("channel_id"))
    print("Title:       ", job.get("title"))
    print("Video:       ", resolve(job_path, job.get("video")))
    print("Privacy:     ", "auto (RULES 8, after upload)" if job.get("publish_at") == "auto"
          else "scheduled" if job.get("publish_at") else job.get("privacy", "private"))
    print("Publish at:  ", job.get("publish_at") or "-", f"(earliest {job['earliest_date']})" if job.get("earliest_date") else "")
    if job.get("publish_at") == "auto" and not errs:
        import publish_slot as ps
        now = ps.now_ist()
        long_time, gap, _ = ps.channel_times(job["channel_key"])
        earliest = dt.date.fromisoformat(job["earliest_date"]) if job.get("earliest_date") else None
        if job.get("format") == "long":
            when, mode = ps.plan_long(now, ps.local_long_days(job["channel_key"]), long_time, earliest)
        elif job.get("parent_video_id"):
            when, mode = ps.plan_short(now, dt.datetime.fromisoformat(
                ps.result_publish_time(ps.find_result(job["parent_video_id"]))), gap)
        else:
            when, mode = ps.plan_standalone_short(now, long_time, gap, earliest)
        print("If done now: ", "PUBLIC NOW" if mode == "now" else f"SCHEDULE {when:%Y-%m-%d %H:%M} IST",
              "(local list only; the real decision is made after the upload)")
    print("Made for kids:", job.get("made_for_kids"))
    print("Thumbnail:   ", job.get("thumbnail") or "-")
    print("Captions:    ", job.get("captions") or "-")
    print("Playlist:    ", job.get("playlist_id") or "-")
    print("Video check: ", job.get("_probe", "-"))
    if job.get("format") == "short":
        print("Parent long: ", job.get("parent_video_id") or "- (stand-alone Short)")
        if parent_line:
            print("Desc line 1: ", parent_line)
            print("1st comment: ", parent_line, "(scheduled task, real publish time + 5 min)")
    elif job.get("first_comment"):
        print("1st comment: ", job["first_comment"], "(scheduled task, real publish time + 5 min)")
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

    yt = get_service(job)
    check_channel(yt, job)
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

    if args.force_thumbnail:
        result.pop("thumbnail_ok", None)
    do_extras(yt, job, job_path, result["video_id"], result)
    auto = job.get("publish_at") == "auto"
    if auto and not result.get("planned_publish_at"):
        when, mode = plan_publish(yt, job, result)
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    elif auto:
        when = dt.datetime.fromisoformat(result["planned_publish_at"])
        mode = "now" if result.get("publish_action") == "public_now" else "schedule"
    else:
        when = dt.datetime.fromisoformat(job["publish_at"]) if job.get("publish_at") else dt.datetime.now(dt.timezone.utc)
    if (parent_line or job.get("first_comment")) and not result.get("comment_task") and not result.get("comment_id"):
        comment_followups(job, job_path, result, max(when, dt.datetime.now(dt.timezone.utc)))
    if auto and not result.get("status"):
        msg = apply_publish(yt, job, result, when, mode)
        if msg:
            result["studio_action"] = msg
            log_file = ROOT / "channels" / job["channel_key"] / "log.md"
            with log_file.open("a", encoding="utf-8") as f:
                f.write(f"{dt.date.today().isoformat()} | {Path(job['video']).stem} | studio action | video "
                        f"{result['video_id']} | {result['publish_action']} {result['planned_publish_at']} | "
                        "studio_action: pending\n")
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("studio_action") and result.get("status", "").startswith("private"):
        print("\n" + result["studio_action"])


if __name__ == "__main__":
    main()
