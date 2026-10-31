# Noor-e-Raah — daily run (one surah video per day, private upload)

User decisions (2026-10-30): one video a day, uploaded PRIVATE automatically (the user makes it public in Studio after
watching it; if something is wrong the user asks for an update); top-up of AI Studio credit is the user's job;
thumbnail = Arabic calligraphy + Hindi name + one honest hook over a dark Islamic wallpaper; no script checkpoint
(Munshi's review replaces it, the user's check of the private video is the final gate).

The Sanchalak (main session) follows this list. Rules live in `shared/RULES.md`, `channels/noor-e-raah/RULES.md`,
`CLAUDE.md`; this file only orders the work. Queue: `channels/noor-e-raah/series_queue.json`
(`python scripts/noor_daily.py status|next|preflight|mark`).

## Script format for EVERY surah (Kalam brief; user 2026-10-30)
- Every Arabic block `[AYAH n]` of a jumla/ayah (not the "whole ayah" overview block) gets, right after the `ARABIC:` line and
  before the BHAAVARTH line, `N. USTAAD — UCHARAN: "<the same Arabic words in Devanagari>"` (clean Devanagari with nuqta, no
  brackets/tags/meaning; last vowel dropped at the end of the jumla). The Ustaad reads it plainly, NOT tilawat; the renderer shows
  it under the Arabic. Per-jumla table Arabic -> Devanagari + source (Tanzil transliteration) in `research/ucharan.md`, source
  recorded in `research/sources.json`.
- Then BHAAVARTH + MATLAB = fuller meaning, 2-3 short sentences per jumla in plain Hindi; a tafsir/context point only if the
  dossier has it with a tag [U#]/[K#]; no unsourced claim.
- ONE honest note once in the intro (Ustaad, tag [NOTE]): "ये पढ़ने की मदद है, तिलावत नहीं — सही तिलावत किसी क़ारी से सुनें।"
- Length ~7-8 min is accepted. Number lines in file order; the LAST two lines must have the highest numbers (renderer: `n >= end_from`).
- Munshi checks each UCHARAN line against `ucharan.md` and the Tanzil Arabic, and that no line is read as tilawat.

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

## Unattended + restart-safe run (2026-10-31)
Container restarts kill background processes. Everything mechanical is now resumable:
- `scripts/noor_render.py` renders the picture in 60 s chunks, in parallel (workers = min(4, CPUs); `--workers N`), into
  `long/output/_chunks/` (signature-checked: any change of script/images/text/look invalidates old chunks). A restart redoes only the
  unfinished chunk; `--keep-chunks` keeps them. Quality is identical to the old single pass (PSNR 138 dB inside a chunk).
- `scripts/noor_run.py <story> [--detach] [--status] [--until STAGE]` runs parse -> images -> tts (rate-limit retries, 75 s waits)
  -> [gate Munshi tts_review PASS] -> render -> thumbnail -> [gate Munshi final_review PASS] -> upload -> queue mark + budget log + log.md + sync.
  Every stage skips what already exists; exit 0 done / 3 waiting for a Munshi review / 1 failed. Upload is never retried automatically.
- After a container restart or any stop: the Sanchalak runs `noor_run.py <story> --detach` (then `--status`), and calls Munshi whenever
  the driver says WAITING (Munshi writes `VERDICT: PASS|FIX|ASK` in the review file named).
