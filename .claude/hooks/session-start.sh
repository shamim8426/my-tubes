#!/bin/bash
# Story-Channel: Claude Code cloud (web) session setup. Linux only; does nothing on the Windows PC.
# Python packages -> .venv (with .venv/Scripts/python.exe pointing at the Linux python, so the
# Windows-style commands in CLAUDE.md and settings.json work here too), fonts, depth model, secrets.
set -euo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}"

# Both PC and cloud: bring in work pushed from the other place. Only on main with a clean tree, fast-forward only
# (never a merge or conflict); offline or diverged = skipped, sync.ps1 / sync.sh rebase later as before.
if [ "$(git branch --show-current 2>/dev/null)" = "main" ] && [ -z "$(git status --porcelain 2>/dev/null)" ]; then
  timeout 60 git pull -q --ff-only origin main >/dev/null 2>&1 || echo "session-start: git pull skipped (offline or diverged)" >&2
fi

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# 1. Python packages: only when requirements.txt or this script changed since the last good install
hashes=.venv/.session-start.sha256
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  rm -f "$hashes"
  [ -x .venv/bin/python ] || uv venv -q --seed .venv
  # torch CPU build if download.pytorch.org is allowed, else the normal PyPI build
  VIRTUAL_ENV="$PWD/.venv" uv pip install -q torch --index-url https://download.pytorch.org/whl/cpu 2>/dev/null \
    || echo "session-start: download.pytorch.org not reachable, torch comes from PyPI" >&2
  VIRTUAL_ENV="$PWD/.venv" uv pip install -q -r requirements.txt
  # study download / trend research (RULES 12c): on the PC these are tools/yt-dlp.exe + tools/deno
  VIRTUAL_ENV="$PWD/.venv" uv pip install -q -U yt-dlp deno
  sha256sum .claude/hooks/session-start.sh requirements.txt > "$hashes"
fi

# Windows-style paths used in CLAUDE.md / settings.json (.venv\Scripts\python)
mkdir -p .venv/Scripts
for n in python python.exe; do ln -sf ../bin/python ".venv/Scripts/$n"; done
# tools/yt-dlp.exe as on the PC (git-ignored), so RULES 12c / trend-research commands stay the same
ln -sf ../.venv/bin/yt-dlp tools/yt-dlp.exe

# 2. Fonts (Mukta, Amiri, Rozha One) for ffmpeg/libass captions
mkdir -p "$HOME/.local/share/fonts"
cp -u shared/fonts/*.ttf "$HOME/.local/share/fonts/" 2>/dev/null || true
command -v fc-cache >/dev/null && fc-cache -f "$HOME/.local/share/fonts" >/dev/null 2>&1 || true

# 3. Depth model for 2.5D parallax (ONLY Depth Anything V2 Small, Apache-2.0). Needs huggingface.co allowed.
if [ ! -f models/depth-anything-v2-small/model.safetensors ]; then
  .venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('depth-anything/Depth-Anything-V2-Small-hf', local_dir='models/depth-anything-v2-small', allow_patterns=['*.json','*.safetensors','*.md'])" >/dev/null 2>&1 \
    || echo "session-start: depth model not downloaded (huggingface.co blocked?); until then build with --motion zoom" >&2
fi

# 4. secrets/ folder from the environment variable STORY_SECRETS_B64 (base64 of a tar.gz of secrets/).
#    API keys (GEMINI_API_KEY ...) are read straight from environment variables; no .env needed.
if [ -n "${STORY_SECRETS_B64:-}" ] && [ ! -d secrets ]; then
  mkdir -p secrets
  printf '%s' "$STORY_SECRETS_B64" | base64 -d | tar -xz -C secrets \
    || { echo "session-start: STORY_SECRETS_B64 could not be unpacked" >&2; rm -rf secrets; }
fi
# channel renamed 2026-10-29 (dadi-ki-kahaniyan -> jugnu-stories): an older secrets archive still uses the old key
if [ -d secrets/dadi-ki-kahaniyan ] && [ ! -d secrets/jugnu-stories ]; then mv secrets/dadi-ki-kahaniyan secrets/jugnu-stories; fi
if [ -f secrets/youtube_token_dadi-ki-kahaniyan.json ] && [ ! -f secrets/youtube_token_jugnu-stories.json ]; then
  mv secrets/youtube_token_dadi-ki-kahaniyan.json secrets/youtube_token_jugnu-stories.json
fi

# 5. Session environment
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export PATH=\"$PWD/.venv/bin:\$PATH\""
    echo "export PYTHONUTF8=1"
    echo "export TZ=Asia/Kolkata"
  } >> "$CLAUDE_ENV_FILE"
fi
