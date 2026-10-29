# Noor-e-Raah — daily run (one surah video per day, private upload)

User decisions (2026-10-30): one video a day, uploaded PRIVATE automatically (the user makes it public in Studio after
watching it; if something is wrong the user asks for an update); top-up of AI Studio credit is the user's job;
thumbnail = Arabic calligraphy + Hindi name + one honest hook over a dark Islamic wallpaper; no script checkpoint
(Munshi's review replaces it, the user's check of the private video is the final gate).

The Sanchalak (main session) follows this list. Rules live in `shared/RULES.md`, `channels/noor-e-raah/RULES.md`,
`CLAUDE.md`; this file only orders the work. Queue: `channels/noor-e-raah/series_queue.json`
(`python scripts/noor_daily.py status|next|preflight|mark`).

## Daily steps (cloud session, auto mode)
1. `git pull --ff-only origin main`; `python scripts/noor_daily.py preflight` — FAILED = stop, write the reasons to
   `channels/noor-e-raah/log.md`, sync, end (never retry loops, never go below the Rs50 floor).
2. `python scripts/noor_daily.py next` — the item to run (status `script_ok` or later; earlier = not ready, stop and log).
3. Nigraan (`nigraan-noor`) report on the last uploaded video (free); apply "LAGU KARO".
4. `kaarigar-noor` stages, ONE stage per call, in the background, each followed by Munshi when the stage contract says so:
   `images` (paid) -> `tts` (free key first) -> `music_sfx` -> `shots` -> **`edit`** (agent `sampadak`, Noor = look only)
   -> `build_long` (`scripts/noor_render.py <story>`) -> `thumbnail` (`scripts/noor_thumb_v3.py`, one wallpaper image
   with `--generate`: FREE FIRST (Cloudflare flux, Rs0), paid Gemini only as fallback (user 2026-10-30); layouts A/B/C; Munshi picks by the thumbnail checklist, the default is C unless Nigraan data says otherwise)
   -> Munshi final.
5. Upload (Munshi, `youtube-publish` skill): private + STUDIO ACTION text; upload the chosen thumbnail via the API
   (needs the channel's phone verification; if the API says 403 the thumbnail file path is put into the STUDIO ACTION
   text instead); first-comment task; add the video to the series playlist (`playlist.id` in series_queue.json).
6. `python scripts/noor_daily.py mark <key> uploaded --note "<video id>"`; `story_budget.py <story> --log`; one status
   line in `channels/noor-e-raah/log.md` and `channel_brief.md`; `bash tools/sync.sh "noor <NNN>: uploaded private"`.
7. Tell the user (PushNotification if available): title, video link, "private, dekh kar public kar dijiye", cost, balance left.

## Stop conditions (ask the user, do not retry)
Balance < story cap + floor · any Munshi BLOCKER open (also Arabic != Tanzil, a person image, a hadith without a sahih
source) · copyright doubt · channel ID mismatch · HTTP 402/403/429 or quota errors · render/ffmpeg failure twice.

## When the user asks for an update to an uploaded private video
Fix with the smallest rebuild (scene cache, TTS cache stay), Munshi R1, re-upload as a NEW private video (never change or
delete the old one on YouTube yourself; tell the user which video to delete), log it, sync.

## Scheduling
A cloud scheduled task (fires once a day, new session, prompt: "Noor daily run: follow docs/NOOR_DAILY_RUN.md")
is created only after: the first scripts are Munshi-PASSed, the user topped up, and the user said go.
