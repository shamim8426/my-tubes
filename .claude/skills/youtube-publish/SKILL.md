---
name: youtube-publish
description: Upload and schedule an approved Story-Channel video to YouTube with tools/youtube_upload.py, including one-time OAuth setup. Used by the munshi agent after the user approves the final build.
---

# Publish a video to YouTube

Uses `tools/youtube_upload.py` (YouTube Data API v3). Never upload without the user's explicit OK in this conversation, except in auto mode (shared/RULES.md section 14): there the script approval is the OK, uploads are always scheduled (private until the slot), and the user can veto before the slot with `tools/veto.py <video_id>`.

## One-time setup (guide the user, they do the clicks in Google Cloud Console)
1. Use the same Google Cloud project as Gemini, or a new one. Enable **YouTube Data API v3**.
2. OAuth consent screen: User type External. Add the channel's Google account as a test user. Then **Publish app** (move it to In production). If it stays in Testing, the refresh token expires every 7 days and uploads stop working.
3. Credentials: Create OAuth client ID, type **Desktop app**. Download JSON and save it as `secrets/client_secret.json`. Make sure `secrets/` is in `.gitignore`.
4. `pip install google-api-python-client google-auth-oauthlib`
5. First real run opens a browser: pick the right Google account AND the right channel, accept the "unverified app" warning (it is the user's own app). Token is saved to `secrets/youtube_token_<channel_key>.json`; later runs are silent.
6. Phone-verify the channel in YouTube Studio, otherwise custom thumbnails fail.

## Important limit: unaudited API projects
Videos uploaded through the API from a project that has not passed YouTube's API audit are locked to **private**, and scheduling may not take effect. Until the audit is approved:
- Upload as private (the script does this when `publish_at` is set).
- Tell the user the one Studio step left: open the studio_url and set Schedule / Public.
- Suggest applying for the audit (YouTube API Services audit and quota extension form, free, takes a few weeks). After approval, scheduling becomes fully automatic.
Quota: default 10,000 units/day; one upload costs about 1,600, thumbnail 50, captions 400. Check the current numbers in the docs if uploads fail with quotaExceeded.

## Per-video steps
1. Confirm in `channels/<key>/log.md`: PASS for final build, thumbnail and metadata of this project. Confirm `output/upload_result.json` does not exist.
2. Read `channels/<key>/channel.json` for made_for_kids, contains_synthetic_media, category_id, language, publish time, playlist id. If made_for_kids is null, ASK the user and save the answer there.
3. Pick publish time per RULES section 8 and `publish_times_ist` in channel.json: long video 19:00 IST, Short 21:00 IST.
   - Long: upload finished before 18:45 IST -> 19:00 the same day, else 19:00 the next day.
   - Short of a long: same day as its long at 21:00 if its upload finishes before 20:45 IST, else both move to the next day.
   - Stand-alone Short (e.g. Dadi Jasoos case): 21:00.
   - Check other projects' `output/upload_result.json` (`publish_at`) + `upload.json` (`format`): at most one long (19:00) and one Short (21:00) per day per channel.
4. Write `output/upload.json`:
   - channel_key, channel_name, channel_id (from `channels/<key>/channel.json`)
   - format: "long" or "short"
   - Short: parent_video_id = the long video's id if the Short is cut from a long video (null for a stand-alone Short). The script then puts "पूरी कहानी यहाँ देखें 👉 <long URL>" at the top of the description and, after upload, schedules the first comment (task StoryChannel-Comment-<video_id>, publish_at + 5 min, tools/post_comment.py) and writes "related_video: pending, pin_comment: pending" to channels/<key>/log.md.
   - title, description, tags (from the approved metadata file)
   - video: final mp4 (never *_preview*)
   - thumbnail, captions (.srt), language "hi", captions_name "Hindi"
   - made_for_kids, contains_synthetic_media, category_id
   - publish_at like 2026-10-21T19:00:00+05:30 (or privacy "private" with no publish_at)
   - playlist_id if configured
5. `python tools/youtube_upload.py --job <upload.json> --dry-run`. Fix any PROBLEMS.
   If the script says WRONG CHANNEL, stop and tell the user; never edit channel_id to make it pass.
6. Show the user: title, publish time IST, made-for-kids, playlist, thumbnail file. Wait for ha/ok (auto mode: do not wait; after upload show one status line with link + slot).
7. Run without --dry-run. If thumbnail/captions/playlist failed, fix the cause and run with `--extras-only`.
8. Report: video URL, studio URL, what succeeded, and what still needs a click in Studio (schedule if locked private, pinned comment, end screen). Pinning a comment is not possible through the API.
8a. Veto ("rok do" before the slot): `python tools/veto.py <video_id>` (dry run first by default; add `--apply`) sets the video private and removes publishAt, logs it, and marks the story vetoed in pipeline_queue.json.
8b. Short with a parent: show the user the manual checklist (Studio: Related video = long video; pin the first comment once it is posted) — RULES section 8.
9. Append a PUBLISHED line to `channels/<key>/log.md` and update the story's `story.md` status.
