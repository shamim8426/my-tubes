#!/bin/bash
# SessionEnd hook, cloud (web) session only: start tools/sync.sh in the background and return at once
# (hooks get ~10 s). On the Windows PC this does nothing; there tools/sync_bg.ps1 does the same job.
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "$(dirname "$0")/.." || exit 0
nohup bash tools/sync.sh "auto: cloud session end" >/dev/null 2>&1 &
exit 0
