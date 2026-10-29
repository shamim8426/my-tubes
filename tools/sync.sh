#!/bin/bash
# Story-Channel -> GitHub sync for Linux / Claude Code cloud sessions (same steps as tools/sync.ps1).
# Usage: bash tools/sync.sh "long_02: final build"
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MSG="${1:-}"
LOG="$ROOT/shared/sync.log"
MAX_BYTES=$((50 * 1024 * 1024))
mkdir -p "$ROOT/shared"

log() { line="$(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S')  $1"; echo "$line" >> "$LOG"; echo "$line"; }

[ -d .git ] || { log "ERROR: not a git repo"; exit 1; }

# one sync at a time
LOCK=.git/sync.lock
if [ -f "$LOCK" ] && [ -n "$(find "$LOCK" -mmin -30 2>/dev/null)" ]; then log "another sync is running, skipped"; exit 0; fi
touch "$LOCK"
trap 'rm -f "$LOCK"' EXIT

# keep .env.example in sync: key names only, never values
if [ -f .env ]; then
  grep -E '^\s*[A-Za-z_][A-Za-z0-9_]*\s*=' .env | sed -E 's/\s*=.*$/=/; s/^\s*//' > .env.example
fi

git -c core.quotepath=false add -A

# secret guard: abort if anything secret-looking got staged
bad=$(git -c core.quotepath=false diff --cached --name-only --diff-filter=AM |
  grep -E '(^|/)\.env$|^secrets/|client_secret.*\.json$|youtube_token.*\.json$|\.credentials\.json$' || true)
if [ -n "$bad" ]; then
  git reset -q
  log "ABORTED: secret file was about to be pushed: $(echo $bad). Fix .gitignore."
  exit 1
fi

# size guard: unstage files over 50 MB (GitHub blocks >100 MB)
git -c core.quotepath=false diff --cached --name-only --diff-filter=AM | while IFS= read -r f; do
  if [ -f "$f" ] && [ "$(stat -c %s "$f")" -gt "$MAX_BYTES" ]; then
    git reset -q -- "$f"; log "SKIPPED big file (>50MB): $f"
  fi
done

if git diff --cached --quiet; then log "no changes"; exit 0; fi

[ -n "$MSG" ] || MSG="auto sync $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M') (cloud)"
git commit -q -m "$MSG" || { log "ERROR: commit failed"; exit 1; }

branch="$(git branch --show-current)"
if ! git pull -q --rebase --autostash origin "$branch"; then
  git rebase --abort 2>/dev/null
  log "ERROR: pull/rebase conflict. Commit is saved locally; ask Claude Code to resolve."
  exit 1
fi
git push -q -u origin "$branch" || { log "ERROR: push failed. Commit is saved locally."; exit 1; }
log "pushed: $MSG (branch $branch)"
