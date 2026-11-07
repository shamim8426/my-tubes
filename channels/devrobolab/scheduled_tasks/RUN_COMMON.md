# DevRoboLab scheduled run: common steps (every slot task reads this; user 2026-11-07)

Project: D:\my-tubes (Windows). Python: D:\my-tubes\.venv\Scripts\python.exe -X utf8. Run long Python/ffmpeg steps from PowerShell with `$env:PATH += ";D:\my-tubes\tools\ffmpeg"` first (Bash PATH does not reach Python's ffmpeg calls), long renders in the background. Work without asking anyone; at the end report.

## 0. Before anything
- `git -C D:\my-tubes pull --ff-only` (main). If git is half-merged or `.git\sync.lock` exists, stop and report.
- Another DevRoboLab run still running (status running in list_task_runs)? Then wait for it; never two runs in parallel.
- Balance: `.venv\Scripts\python.exe -X utf8 -c "import sys; sys.path.insert(0,'scripts'); import cost_log; print(cost_log.remaining())"`. Below Rs 65 (floor Rs 50 + one run): no paid call, report "recharge".
- Read: CLAUDE.md, channels/devrobolab/PLAN_DAILY.md (formats, slots, rules), DAILY_COMMON.md (voice, budget, real assets, upload, logging), shared/STYLE_LIBRARY.md sections 0, 9, 10 (look), channels/devrobolab/log.md last 30 lines, topic_queue.json.


## 0a. WORK WINDOW (user 2026-11-07, binding): NO daytime work
Work only in the morning (06:00-10:30 start) and at night (start 20:00-02:00), local time. If a task starts between 10:30 and 20:00 (the PC/app was off at the slot and opened late), do NOTHING: exit at once with the report "din ka time, kaam raat ko (retry 21:00 / 22:00)". Never start a new video after 02:00.
Retry rule: if a slot was missed because the PC was not available, it is retried at 21:00 and, if still missing, at 22:00 by the task `devrobolab-retry-night` (it only does slots that have no upload today, one at a time, and exits if another DevRoboLab run is still running). After 22:00 the slot is skipped for today (no extra retries); the next day continues normally.
Dates: a run that finishes after midnight counts for the day it started.

## 1. Make the video (own new story folder `channels/devrobolab/stories/<next free number>_<slug>/`)
1. Topic: as the slot task says. Facts ONLY from the official page(s) (WebFetch); write `review/facts.md` (each fact + URL). Third-party things (e.g. a Zomato connector) are labelled as third-party/example on screen, never a real order, account or payment.
2. Script `deck.json` (Hinglish in Devanagari + English tech words, same voice/style block as story 044). Long: 450-550 words (about 3 min). Short: 90-110 words (35-40 s). Hook in the first 2 s, one caution, short recap, rotating last-line CTA (different from the previous video in log.md).
3. Voice: copy `tts.py` + `wordtimes.py` from stories/044_cfe-memory; `tts.py` (free key), if the free quota is used up `tts.py --paid` (per-run cap Rs 15, never below floor). Then `wordtimes.py` -> wt.json.
4. Build: LONG = copy `stories/044_cfe-memory/make_final.py` (16:9, per-beat zoom K, dark UI/terminal demo, chapter badge, Chromium Hindi captions `build_caps()`, every on-screen action tied to `T(scene, token)` = the time the word is spoken). SHORT = same helpers at 1080x1920 (see stories/045_cfe-file-upload for a 9:16 build): full-screen showing area, no face, no robot box (robot only for a moment at hook/CTA), small caption strip at the bottom. Pick a NEW highlight colour (not the previous video's) and log it. Free Cloudflare photos only (scripts/cf_image.py), no text in images.

## 2. Self-review, then fix ONLY the broken parts (user rule 2026-11-07)
1. Before the full render: frames every 3 s (`make_final.py frames 1 4 7 ...`) as contact sheets; look at every sheet.
2. Full render. Then review again: contact sheets every 3 s of the finished video + exact frames at each spoken action word (plus, click, toggle, delete ...): is the action on screen exactly when the word is spoken? Hindi matras correct (no broken "ि")? No blank frame (only caption) longer than 0.5 s? Nothing overlapping or cut off? Cards using the screen (not tiny)? Loudness -14 +-1 LUFS, true peak <= -1 dBTP (ffmpeg ebur128)? Length (long 2:00-6:00, Short <= 40 s; cut-Short <= 60 s)? Facts match review/facts.md?
3. Write every mistake with its time range into `review/review.md`.
4. Fix: change the code for those scenes only, then re-render ONLY the broken range and splice it in, never the whole video:
   `make_final.py range <t0> <t1> output/part.mp4` then `python tools/splice_video.py output/<video>.mp4 output/part.mp4 <t0> <t1> output/<video>_fixed.mp4` (frame accurate, audio copied). Use whole-scene boundaries for t0/t1. Only if the audio/script itself changes, re-render fully.
5. Look again at the fixed ranges (frames at t0, the action words, t1) and note "fixed" in review.md. At most 2 fix rounds; if a mistake is still there, DO NOT upload: report what is wrong.

## 3. Upload (private) and log
- `output/upload.json` like stories/044_cfe-memory/output/upload.json (privacy private, made_for_kids false, synthetic media true, language hi, category 28, right playlist_id, honest Hinglish description with official source URLs, "Unofficial channel, not affiliated with Anthropic.", illustration/synthetic-voice note, Funkorama credit, no "<" or ">" in the description; long title without #shorts, Short title ends with #shorts; title <= 70 chars). `tools/name_guard.py` on title+description.
- `tools/youtube_upload.py --job <upload.json> --dry-run`, then without --dry-run. Never public, never publish_at, never delete anything on YouTube.
- topic_queue.json (status uploaded, story, video_id, series, series_index), log.md line (URL, length, LUFS, cost, style variants, review findings fixed), then `powershell -NoProfile -ExecutionPolicy Bypass -File tools\sync.ps1 -Message "devrobolab <story>: uploaded private"`.
- Final message (Hinglish, short): video link, private, playlist, cost (Rs), balance, mistakes found and fixed, anything the user must do in Studio (thumbnail, public).
- Login (OAuth Testing mode) expired? Report "run tools/yt_auth.py" and stop before upload; leave the finished video in output/.
