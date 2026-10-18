# Story-Channel: set up a NEW Windows system from GitHub in one go.
#
# On a new PC (PowerShell, normal user, not Administrator):
#   1. Get this file (from your GitHub repo page, or your backup copy) and run:
#        powershell -ExecutionPolicy Bypass -File deploy.ps1 -Repo yourname/story-channel
#   2. Follow the prompts (GitHub login in browser, API keys once).
# Running it again later is safe: it only fills in what is missing.
param(
    [string]$Repo = "",
    [string]$Path = "D:\Story-Channel"
)

$ErrorActionPreference = "Stop"
function Step([string]$m) { Write-Host ""; Write-Host "==> $m" -ForegroundColor Cyan }
function Warn([string]$m) { Write-Host "    ! $m" -ForegroundColor Yellow }
function Have([string]$c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }
function RefreshPath {
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [Environment]::GetEnvironmentVariable("Path", "User") + ";" +
                (Join-Path $env:USERPROFILE ".local\bin")
}
function WingetInstall([string]$id, [string]$cmd) {
    if (Have $cmd) { Write-Host "    $cmd already installed"; return }
    winget install --id $id -e --silent --accept-package-agreements --accept-source-agreements
    RefreshPath
    if (-not (Have $cmd)) { Warn "$cmd still not found. Close PowerShell, open a new one, run deploy.ps1 again." }
}
function HavePython {
    $p = Get-Command python -ErrorAction SilentlyContinue
    return ($p -and ($p.Source -notlike "*WindowsApps*"))
}

# If this script already sits inside a cloned repo, use that folder.
if (Test-Path (Join-Path $PSScriptRoot ".git")) { $Path = $PSScriptRoot }

Step "1/10 Basic tools (winget)"
if (-not (Have "winget")) { throw "winget not found. Install 'App Installer' from Microsoft Store, then run again." }
WingetInstall "Git.Git" "git"
WingetInstall "GitHub.cli" "gh"
if (-not (HavePython)) {
    winget install --id Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
    RefreshPath
} else { Write-Host "    python already installed" }
WingetInstall "Gyan.FFmpeg" "ffmpeg"
# EXTRA_TOOLS: Claude Code adds any other tools the pipeline needs here.

Step "2/10 Claude Code"
if (-not (Have "claude")) {
    Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression
    RefreshPath
} else { Write-Host "    claude already installed" }

Step "3/10 GitHub login"
gh auth status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { gh auth login --hostname github.com --git-protocol https --web }
gh auth setup-git

Step "4/10 Project download"
$drive = Split-Path -Qualifier $Path
if (-not (Test-Path $drive)) {
    $Path = Read-Host "Drive $drive is not on this PC. Full folder path for the project (e.g. C:\Story-Channel)"
}
if (Test-Path (Join-Path $Path ".git")) {
    git -C $Path pull --rebase --autostash
} else {
    if (-not $Repo) { $Repo = Read-Host "GitHub repo (e.g. yourname/story-channel)" }
    gh repo clone $Repo $Path
}
Set-Location $Path

Step "5/10 Git identity"
if (-not (git config --global user.name)) {
    git config --global user.name (Read-Host "Your name for git commits")
}
if (-not (git config --global user.email)) {
    git config --global user.email (Read-Host "Your email for git commits")
}

Step "6/10 Python packages (whisper/torch can take a while)"
python -m pip install --upgrade pip
if (Test-Path "requirements.txt") { python -m pip install -r requirements.txt }

Step "7/10 Fonts"
$fontDir = Join-Path $Path "fonts"
if (Test-Path $fontDir) {
    $userFonts = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Fonts"
    New-Item -ItemType Directory -Force $userFonts | Out-Null
    Get-ChildItem $fontDir -Include *.ttf, *.otf -Recurse | ForEach-Object {
        $target = Join-Path $userFonts $_.Name
        if (-not (Test-Path $target)) {
            Copy-Item $_.FullName $target
            New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts" `
                -Name $_.BaseName -Value $target -PropertyType String -Force | Out-Null
            Write-Host "    font installed: $($_.Name)"
        }
    }
}

Step "8/10 Claude setup (agents, skills, CLAUDE.md) -> $env:USERPROFILE\.claude"
$home2 = Join-Path $Path "claude-home"
$dst = Join-Path $env:USERPROFILE ".claude"
if (Test-Path $home2) {
    New-Item -ItemType Directory -Force $dst | Out-Null
    Get-ChildItem $home2 | ForEach-Object {
        $t = Join-Path $dst $_.Name
        if (Test-Path $t) {
            $bak = "$t.bak-" + (Get-Date -Format "yyyyMMdd-HHmmss")
            Rename-Item $t $bak
            Write-Host "    existing $($_.Name) kept as $bak"
        }
        Copy-Item $_.FullName $t -Recurse -Force
    }
}

Step "9/10 Secrets (.env, secrets\)"
$envFile = Join-Path $Path ".env"
if (-not (Test-Path $envFile)) {
    $lines = @()
    $keys = @()
    if (Test-Path ".env.example") {
        $keys = Get-Content ".env.example" | Where-Object { $_ -match '=' } | ForEach-Object { ($_ -split '=', 2)[0].Trim() }
    }
    foreach ($k in $keys) {
        $s = Read-Host "Value for $k (input hidden)" -AsSecureString
        $plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
        $lines += "$k=$plain"
    }
    Set-Content -Path $envFile -Value $lines -Encoding UTF8
    Write-Host "    .env created with $($keys.Count) keys"
} else { Write-Host "    .env already present" }
New-Item -ItemType Directory -Force (Join-Path $Path "secrets") | Out-Null
if (-not (Test-Path (Join-Path $Path "secrets\client_secret.json"))) {
    Warn "secrets\client_secret.json missing. Copy it from your backup, or download again: Google Cloud Console > Credentials > your Desktop OAuth client > Download JSON."
    Warn "YouTube login (youtube_token.json) will be asked again on the first upload. That is normal."
}

Step "10/10 Nightly auto-sync + checks"
try {
    $action = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Path\tools\sync.ps1`" -Message `"nightly sync`""
    $trigger = New-ScheduledTaskTrigger -Daily -At 11:30pm
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
    Register-ScheduledTask -TaskName "StoryChannel-Sync" -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
    Write-Host "    nightly sync task: 11:30 PM (runs later if PC was off)"
} catch { Warn "Could not create the nightly task: $($_.Exception.Message)" }

Write-Host ""
foreach ($c in @("git", "gh", "python", "ffmpeg", "claude")) {
    if (Have $c) { Write-Host ("    OK   " + $c) -ForegroundColor Green } else { Write-Host ("    MISSING " + $c) -ForegroundColor Red }
}
python -c "import googleapiclient, google_auth_oauthlib; print('    OK   youtube libs')"
if (Test-Path "tools\youtube_upload.py") { python -m py_compile tools\youtube_upload.py; Write-Host "    OK   youtube_upload.py" }

Write-Host ""
Write-Host "Done. Next: open a new terminal, then:  cd `"$Path`"  and run  claude  (log in once)." -ForegroundColor Cyan
