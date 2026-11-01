# PC sync after cloud work (for Claude Code on the Windows PC)

The user worked in a Claude Code cloud (web) session. All that work is already pushed to GitHub `main`.
Bring it to this PC, check that the PC setup still works, and report to the user in Hinglish.
Read only, no paid calls (no Gemini image/TTS, no upload).

## What came from the cloud (2026-10-29)
- `.claude/hooks/session-start.sh` + `SessionStart` hook in `.claude/settings.json`: on the PC it only does
  `git pull --ff-only` on a clean `main`; the rest runs only in the cloud (`CLAUDE_CODE_REMOTE=true`).
- `SessionEnd`: the powershell sync is unchanged; a second hook `tools/session_end_cloud.sh` does nothing on the PC.
- `tools/sync.sh` (Linux copy of `sync.ps1`, cloud only), `CLAUDE.md` section "Cloud (web) session".
- Noor scripts (`noor_render.py` etc.): ffmpeg from PATH if `tools/ffmpeg` is missing (PC unchanged).
- `requirements.txt`: `opencv-python-headless==5.0.0.*` (no reinstall needed on the PC).
- Fresh analytics + reach reports in `channels/*/analytics/`.

## Steps (PowerShell, in `D:\my-tubes`)
1. `git status` and `git branch --show-current`. Must be on `main`.
2. Sync (commits PC changes, pulls the cloud work, pushes):
   `powershell -NoProfile -ExecutionPolicy Bypass -File tools\sync.ps1 -Message "<simple English message>"`
   Then read the last lines of `shared\sync.log`.
3. If there is a pull/rebase conflict: do not force anything. Show the user the conflicting files. Logs and data
   files (`cost_log.csv`, `usage_log.jsonl`, `shared/sync.log`, `channels/*/log.md`, analytics files) keep BOTH
   sides' lines; for anything else ask the user. Never `git push --force`, never commit `.env` or `secrets/`.
4. Check the PC setup:
   - `bash .claude/hooks/session-start.sh; echo $LASTEXITCODE` -> must end with 0 and print nothing else.
   - `.\.venv\Scripts\python -X utf8 scripts\test_pricing.py` -> "ALL ... CHECKS PASSED".
   - `.\.venv\Scripts\python -X utf8 scripts\state.py status`.
5. `git status` -> "up to date with 'origin/main'" and "nothing to commit".

## Report to the user (Hinglish, short)
- Sync OK or not (last `sync.log` line), conflicts if any.
- Hook check, test_pricing, state.py status: OK / problem (with the exact error).

## Rule: commit messages
Always simple English, short, present tense: `<area>: <what changed>`
(e.g. `nigraan: analytics fetch`, `kissago 006: scene images done`, `pc: sync cloud work`). No Hinglish.
