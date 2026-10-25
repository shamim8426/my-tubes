# Stage contracts (Kaarigar → Sanchalak)

One Kaarigar call = one stage. Before: `python scripts/state.py start <key> <story> <stage>` (refuses if the channel is
busy; paid stages also hold the channel's paid lock). After: `done` (with `--cost`) or `fail --note`. The Sanchalak
then checks the contract below itself (`python scripts/state.py check <key> <story> <stage>` + the listed checks) and
only then moves on. Time limits are in `scripts/state.py` LIMIT_MIN; over the limit = STALE (shown in shared/status.md,
one line in shared/incidents.md); the Sanchalak checks with Monitor / the files before deciding.

Report back (max ~15 lines): files made, actual cost (₹, GST incl.), budget left (story cap + account), warnings, next
stage, Munshi needed yes/no. Long logs go to files, never into the report.

| Stage | Paid? | Limit | Must exist / be true after the stage | Munshi after |
|---|---|---|---|---|
| status | no | 10 min | shared/status.md refreshed; report lists the channel's story, stage, open items | no |
| sheets | yes | 30 min | new character sheets in characters/<name>/ (Kissago) or characters/musafir/ (Noor); cost_log rows | yes (sheets) |
| images | yes | 60 min | every image in the plan exists (Kissago scene_prompts.json / Noor long/images.json); 16:9 or 9:16 as planned; name_guard OK | yes (images) |
| tts | yes (free key first) | 60 min | long/lines.json: every spoken line has audio + seconds + tts_ok (Noor) / TTS cache complete (Kissago); report of lines that missed words | yes (audio) |
| music_sfx | no | 15 min | every track/SFX used is in shared/assets_license.csv | no |
| shots | no | 15 min | shots.json / images.json timing covers every line; no visual longer than the channel's max | no |
| build_long | no | 60 min | long/output/<story>_final.mp4 (no .part.mp4 left), 1920x1080 30 fps H.264+AAC, ~-14 LUFS; .srt | yes (final) |
| build_short | no | 30 min | shorts/<short>/output/*.mp4 1080x1920, ≤ channel max length; Noor: last ayah complete (RULES 2b) | yes (final) |
| thumbnail | maybe (1 image) | 15 min | 1280x720 ≤ 2 MB; Arabic/Hindi via libass (Noor); no AI text | yes (thumbnail) |
| upload | no | 30 min | only after Munshi PASS + the user's OK (or auto mode where allowed); upload_result.json with video_id; private + STUDIO ACTION while api_audited is false | Munshi does it |
| comments | no | 10 min | scheduled comment task exists or comment_id saved | no |
| sync | no | 10 min | tools/sync.ps1 line "pushed" in shared/sync.log; no secret staged | no |

Never in any stage: delete (move to _to_delete/), overwrite a paid file, print .env/secrets, change a video's
visibility or delete on YouTube, retry loops on 402/403/429 (stop and report), touch another channel's folder.
