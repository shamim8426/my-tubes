---
name: youtube-publish
description: Upload and schedule an approved Story-Channel video to YouTube with tools/youtube_upload.py, including one-time OAuth setup. Used by the munshi agent after the user approves the final build.
---

# Publish a video to YouTube

Uses `tools/youtube_upload.py` (YouTube Data API v3). Never upload without the user's explicit OK in this conversation, except in auto mode (shared/RULES.md section 14): there the script approval is the OK, publish timing follows RULES section 8 (public now or scheduled, decided after the upload), and the user can veto a scheduled video before its time with `tools/veto.py <video_id>`.

## One-time setup (guide the user, they do the clicks in Google Cloud Console)
1. Use the same Google Cloud project as Gemini, or a new one. Enable **YouTube Data API v3**.
2. OAuth consent screen: User type External. Add the channel's Google account as a test user. Then **Publish app** (move it to In production). If it stays in Testing, the refresh token expires every 7 days and uploads stop working.
3. Credentials: Create OAuth client ID, type **Desktop app**. Download JSON and save it as `secrets/client_secret.json`. Make sure `secrets/` is in `.gitignore`.
4. `pip install google-api-python-client google-auth-oauthlib`
5. First real run opens a browser: pick the right Google account AND the right channel, accept the "unverified app" warning (it is the user's own app). Token is saved to `secrets/youtube_token_<channel_key>.json`; later runs are silent.
6. Phone-verify the channel in YouTube Studio, otherwise custom thumbnails fail.

## Important limit: unaudited API projects
Videos uploaded through the API from a project that has not passed YouTube's API audit are locked to **private**, and scheduling may not take effect. Until the audit is approved:
- Upload as private (the script always does this with `"publish_at": "auto"`).
- Give the user the STUDIO ACTION message (step 8): make Public now or set the Schedule in Studio.
- Suggest applying for the audit (YouTube API Services audit and quota extension form, free, takes a few weeks). After approval, scheduling becomes fully automatic.
Quota: default 10,000 units/day; one upload costs about 1,600, thumbnail 50, captions 400. Check the current numbers in the docs if uploads fail with quotaExceeded.

## Per-video steps
1. Confirm in `channels/<key>/log.md`: PASS for final build, thumbnail and metadata of this project. Confirm `output/upload_result.json` does not exist.
   Name check (RULES 12a): `python tools/name_guard.py <meta.json> <.txt> <upload.json>` must print OK. `tools/youtube_upload.py` also refuses (dry-run and upload) when a studio/film/anime/artist name is in the title, description, tags, comment, playlist or file names: BLOCK, never work around it.
2. Read `channels/<key>/channel.json` for made_for_kids, contains_synthetic_media, category_id, language, publish time, playlist id. If made_for_kids is null, ASK the user and save the answer there.
3. Publish time (RULES section 8, rule of 2026-10-21): do NOT pick a fixed slot. Set `"publish_at": "auto"`; the uploader
   decides right AFTER the upload from the IST clock (`tools/publish_slot.py`, check with
   `python tools/publish_slot.py <key> long|short [--parent <long id>] [--now <IST time>]`):
   - 19:00–23:59 -> long public now; its Short = long time + 60 min (after 23:59 -> Short public now too).
   - 00:00–18:59 -> long 19:00 the same day; its Short 20:00 the same day.
   - One long per day: days with a long (all upload_result.json + the channel's videos via the API) are skipped -> next free day 19:00 / 20:00.
   - Stand-alone Short: same clock at 20:00. Optional `earliest_date` (YYYY-MM-DD) for a festival story.
   - Upload the long first: the Short's time comes from the long's `planned_publish_at`.
4. Write `output/upload.json`:
   - channel_key, channel_name, channel_id (from `channels/<key>/channel.json`)
   - format: "long" or "short"
   - Short: parent_video_id = the long video's id if the Short is cut from a long video (null for a stand-alone Short). The script then puts "पूरी कहानी यहाँ देखें 👉 <long URL>" at the top of the description and, after upload, schedules the first comment (task StoryChannel-Comment-<video_id>, real publish time + 5 min, tools/post_comment.py) and writes "related_video: pending, pin_comment: pending" to channels/<key>/log.md.
   - title, description, tags (from the approved metadata file)
   - video: final mp4 (never *_preview*)
   - thumbnail, captions (.srt), language "hi", captions_name "Hindi"
   - made_for_kids, contains_synthetic_media, category_id
   - publish_at "auto" (section 3; an explicit time must be 19:00 for a long / 20:00 for a Short), optional earliest_date
   - first_comment (long, optional): text of the long's first comment (same task, real publish time + 5 min)
   - playlist_id if configured
5. `python tools/youtube_upload.py --job <upload.json> --dry-run`. Fix any PROBLEMS.
   If the script says WRONG CHANNEL, stop and tell the user; never edit channel_id to make it pass.
6. Show the user: title, publish time IST, made-for-kids, playlist, thumbnail file. Wait for ha/ok (auto mode: do not wait; after upload show one status line with link + public now / scheduled time).
7. Run without --dry-run. If thumbnail/captions/playlist failed, fix the cause and run with `--extras-only`.
8. Report: video URL, studio URL, what succeeded, and what still needs a click in Studio (pinned comment, end screen). Pinning a comment is not possible through the API.
   STUDIO ACTION (while channel.json `api_audited` is false): the uploader prints and saves (`studio_action` in upload_result.json, a `studio_action: pending` line in log.md) the exact step. Give it to the user as ONE clear message right after the upload(s): per video its ID, title and "abhi PUBLIC karo" or "<date> 19:00 par SCHEDULE karo" (a separate line for the Short), the Short's Related video (long ID) and when the first comment comes (to pin). When the user says "ho gaya": log `studio_action: done` (date) and set `status` in upload_result.json to "public (manual)" / "scheduled (manual)". When `api_audited` is true the uploader sets public/publishAt itself and the message is a report only.
8a. Veto ("rok do" before a scheduled time; a video already public cannot be vetoed): `python tools/veto.py <video_id>` (dry run first by default; add `--apply`) sets the video private and removes publishAt, logs it, and marks the story vetoed in pipeline_queue.json.
8b. Short with a parent: show the user the manual checklist (Studio: Related video = long video; pin the first comment once it is posted) — RULES section 8.
9. Append a PUBLISHED line to `channels/<key>/log.md` and update the story's `story.md` status.
   Also fill the story's row in `channels/<key>/story_registry.md`: "Publish (IST)" = video ids + publish time. Views/Likes are filled later, when analytics are read.
