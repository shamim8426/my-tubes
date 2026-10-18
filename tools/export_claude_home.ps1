# Copies the user-level Claude Code setup (C:\Users\<you>\.claude) into claude-home/ in the repo.
# Whitelist only: credentials, history, transcripts and caches are never copied.
$Root = Split-Path -Parent $PSScriptRoot
$Src = Join-Path $env:USERPROFILE ".claude"
$Dst = Join-Path $Root "claude-home"
$Items = @("CLAUDE.md", "settings.json", "agents", "skills", "commands", "output-styles", "hooks")

if (-not (Test-Path $Src)) { return }
New-Item -ItemType Directory -Force $Dst | Out-Null

foreach ($i in $Items) {
    $s = Join-Path $Src $i
    $d = Join-Path $Dst $i
    if (-not (Test-Path $s)) { continue }

    if ($i -eq "settings.json") {
        $txt = Get-Content $s -Raw
        if ($txt -match '(?i)"[A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*"\s*:') {
            Write-Host "settings.json has key/token-like entries; NOT exported. Move secrets to .env."
            continue
        }
    }
    # claude-home/ is a generated mirror, so refresh it fully
    if (Test-Path $d) { Remove-Item $d -Recurse -Force }
    Copy-Item $s $d -Recurse -Force
}
