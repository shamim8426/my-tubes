# YouTube Uploader — setup record

How the automatic YouTube upload for **दादी की कहानियाँ (Dadi Ki Kahaniyan)** is set up, and how to use or rebuild it.
Set up on 18 Oct 2026. First upload: Long 01 (https://youtu.be/Ogfqow8rbGY).

> No secrets are in this file. `secrets/` and `.env` are never committed.

## 1. Pieces

| Piece | Where | In git? |
|---|---|---|
| Upload script | `tools/youtube_upload.py` | yes |
| Publish steps (for Munshi) | `.claude/skills/youtube-publish/SKILL.md` | yes |
| Channel settings | `channels/dadi-ki-kahaniyan/channel.json` | yes |
| Per-video job | `<video folder>/output/upload.json` (written by Munshi) | yes |
| Upload result | `<video folder>/output/upload_result.json` (video id, URLs) | yes |
| OAuth client | `secrets/client_secret.json` | **no** (keep a copy in Drive / password manager) |
| Login token | `secrets/youtube_token_dadi-ki-kahaniyan.json` | **no** (re-created by logging in again) |
| Python libs | `google-api-python-client`, `google-auth-oauthlib` (in `requirements.txt`) | yes |

## 2. Google Cloud settings (project: "Default Gemini Project")

Account: `shamimx.ali@gmail.com` (personal, not the ami.com work account).

1. **APIs & Services:** *YouTube Data API v3* enabled. The API itself is free (daily quota 10,000 units; one upload ≈ 1,600, thumbnail 50, captions 400).
2. **Google Auth Platform → Branding**
   - App name: `Dadi Ki Kahaniyan Uploader`
   - Support / developer email: `shamimx.ali@gmail.com`
   - Home page: https://www.youtube.com/channel/UCy071_4g4vGemktFHybqkhQ
   - Privacy policy: https://gist.github.com/shamim8426/9fdc382c9ac9a02777195c7c5969a1b6 (public gist on GitHub `shamim8426`)
   - Authorized domains: `youtube.com`, `github.com`
   - No logo (a logo would trigger Google verification).
3. **Audience:** User type *External*, test user `shamimx.ali@gmail.com`, publishing status **In production**
   (in *Testing* the login expires every 7 days).
4. **Clients:** OAuth client `story-channel-uploader`, type **Desktop app**, "AI-powered agent" option **off**.
   Its JSON is saved as `secrets/client_secret.json`.
5. **YouTube:** channel phone-verified (needed for custom thumbnails).

The app is not verified by Google. That is fine for our own channel: the login screen shows an "unverified app" warning
(Advanced → Go to Dadi Ki Kahaniyan Uploader). Scopes asked: `youtube.upload` and `youtube.force-ssl` (captions + playlists;
the script never deletes anything).

## 3. Channel config (`channels/dadi-ki-kahaniyan/channel.json`; the upload script reads it by `channel_key` and stops if the job's channel_id differs)

| Key | Value |
|---|---|
| channel_key | `dadi-ki-kahaniyan` |
| channel_id | `UCy071_4g4vGemktFHybqkhQ` |
| made_for_kids | `false` (user's final decision: family content) |
| contains_synthetic_media | `false` |
| category_id | `1` |
| default_language | `hi` |
| publish_window_ist | `19:00`–`23:59` (same day as upload; RULES section 8) |
| max_long_per_day | `1` |
| min_gap_hours_short_long | `2` |
| playlists | not filled yet |

## 4. Safety checks in the script

- **Channel lock:** after login it asks YouTube which channel is logged in; if it is not `channel_id`, it stops with
  `WRONG CHANNEL` and uploads nothing. Never edit `channel_id` to make it pass.
- **One token per channel:** `secrets/youtube_token_<channel_key>.json`.
- **Real final only:** `ffprobe` checks size (long 1920x1080, short 1080x1920 and ≤60 s), h264, yuv420p. A renamed
  preview is caught. ffprobe comes from PATH, else `tools/ffmpeg/bin/ffprobe.exe` or `tools/ffmpeg/ffprobe.exe`.
- **Metadata limits:** title ≤100, description ≤5000, tags ≤500 chars, ≤15 hashtags, no `<` `>`.
- **No duplicates:** if `upload_result.json` already has a video id, it refuses (use `--extras-only` to retry
  thumbnail/captions/playlist).
- `publish_at` must have a timezone, be ≥15 min in the future and fall inside 19:00–23:59 IST; scheduled videos go up
  as private + publishAt.

## 5. How an upload happens

1. Munshi gives PASS for final build, thumbnail, metadata and copyright (logged in `channels/dadi-ki-kahaniyan/log.md`).
2. Munshi writes `output/upload.json` and runs
   `.venv\Scripts\python tools\youtube_upload.py --job <project>\output\upload.json --dry-run`.
3. The user sees the summary and says "upload karo" / "ha".
4. Munshi runs the same command without `--dry-run`, then writes a PUBLISHED line in `channels/dadi-ki-kahaniyan/log.md`.
5. Builder runs `tools\sync.ps1 -Message "<project>: uploaded"`.

Still done by hand in YouTube Studio: check the schedule (see 6), pin the comment after publish, end screen,
playlist (until playlist ids are in the config), and watch for copyright claims (RULES section 10).

## 6. Known limit: API audit

Until the Google Cloud project passes the *YouTube API Services audit*, videos uploaded through the API can be locked to
private and the `publishAt` time may be ignored. After every upload, open the Studio link and check Visibility; if it only
says Private, set Schedule by hand. Applying for the audit (free, a few weeks) removes this step.

## 7. New PC / lost token

1. `deploy.ps1` installs Python libs and FFmpeg.
2. Copy `client_secret.json` from your backup into `secrets/` (or download it again: Google Auth Platform → Clients →
   story-channel-uploader → download).
3. First upload (or a login test) opens the browser: choose `shamimx.ali@gmail.com`, channel **दादी की कहानियाँ**,
   accept the unverified-app warning and both permissions. The token is saved again.

If the login ever stops working: delete `secrets/youtube_token_dadi-ki-kahaniyan.json` and log in again. To remove
access completely: https://myaccount.google.com/permissions.

## 8. Adding another channel later

Run `tools\new_channel.ps1 -Key <key> -Name "<name>"`, then fill `channel_id` in `channels/<key>/channel.json`; the same OAuth client works.
On the first upload for that channel, log in and pick that channel; a separate token file is created.
