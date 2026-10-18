# Story-Channel -> GitHub sync. Safe to run any time; does nothing if there are no changes.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tools\sync.ps1 -Message "long_02: final build"
param([string]$Message = "")

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$LogDir = Join-Path $Root "munshi"
New-Item -ItemType Directory -Force $LogDir | Out-Null
$Log = Join-Path $LogDir "sync.log"
$MaxBytes = 50MB

function Log([string]$m) {
    $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $m
    Add-Content -Path $Log -Value $line -Encoding UTF8
    Write-Host $line
}

if (-not (Test-Path (Join-Path $Root ".git"))) { Log "ERROR: not a git repo, run deploy.ps1 first"; exit 1 }

# one sync at a time
$Lock = Join-Path $Root ".git\sync.lock"
if ((Test-Path $Lock) -and ((Get-Item $Lock).LastWriteTime -gt (Get-Date).AddMinutes(-30))) {
    Log "another sync is running, skipped"; exit 0
}
New-Item -ItemType File -Force $Lock | Out-Null

try {
    # 1. copy user-level Claude setup (agents, skills, CLAUDE.md...) into claude-home/
    & (Join-Path $PSScriptRoot "export_claude_home.ps1")

    # 2. keep .env.example in sync: key names only, never values
    $envFile = Join-Path $Root ".env"
    if (Test-Path $envFile) {
        $keys = Get-Content $envFile | Where-Object { $_ -match '^\s*[A-Za-z_][A-Za-z0-9_]*\s*=' } |
            ForEach-Object { ($_ -split '=', 2)[0].Trim() + "=" }
        Set-Content -Path (Join-Path $Root ".env.example") -Value $keys -Encoding UTF8
    }

    git -c core.quotepath=false add -A

    # 3. secret guard: abort if anything secret-looking got staged
    $staged = @(git -c core.quotepath=false diff --cached --name-only --diff-filter=AM)
    $bad = $staged | Where-Object { $_ -match '(^|/)\.env$|^secrets/|client_secret.*\.json$|youtube_token\.json$|\.credentials\.json$' }
    if ($bad) {
        git reset -q
        Log ("ABORTED: secret file was about to be pushed: " + ($bad -join ", ") + ". Fix .gitignore.")
        exit 1
    }

    # 4. size guard: unstage files over 50 MB (GitHub blocks >100 MB)
    foreach ($f in $staged) {
        $p = Join-Path $Root $f
        if ((Test-Path $p) -and ((Get-Item $p).Length -gt $MaxBytes)) {
            git reset -q -- "$f"
            Log ("SKIPPED big file (>50MB): " + $f)
        }
    }

    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { Log "no changes"; exit 0 }

    if (-not $Message) { $Message = "auto sync " + (Get-Date -Format "yyyy-MM-dd HH:mm") }
    git commit -q -m "$Message"
    if ($LASTEXITCODE -ne 0) { Log "ERROR: commit failed"; exit 1 }

    git pull -q --rebase --autostash
    if ($LASTEXITCODE -ne 0) {
        git rebase --abort 2>$null
        Log "ERROR: pull/rebase conflict. Commit is saved locally; ask Claude Code to resolve."
        exit 1
    }
    git push -q
    if ($LASTEXITCODE -ne 0) { Log "ERROR: push failed (internet / gh auth?). Commit is saved locally."; exit 1 }

    $kb = [double]((git count-objects -v | Select-String "size-pack").ToString().Split(":")[1].Trim())
    $size = "{0:N0} MB" -f ($kb / 1024)
    Log ("pushed: " + $Message + "  (repo pack size " + $size + ")")
}
finally {
    Remove-Item $Lock -Force -ErrorAction SilentlyContinue
}
