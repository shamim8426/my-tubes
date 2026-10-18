# Create a new channel folder from channels/_template.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tools\new_channel.ps1 -Key my-channel -Name "My Channel"
param(
    [Parameter(Mandatory = $true)][string]$Key,
    [Parameter(Mandatory = $true)][string]$Name
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if ($Key -notmatch '^[a-z0-9][a-z0-9-]*$') { throw "Key must be lowercase letters, digits and '-' (e.g. islamic-stories)." }
$Template = Join-Path $Root "channels\_template"
$Dst = Join-Path $Root "channels\$Key"
if (Test-Path $Dst) { throw "channels\$Key already exists. Nothing changed." }

Copy-Item $Template $Dst -Recurse
$utf8 = New-Object System.Text.UTF8Encoding($false)
foreach ($f in @("channel.json", "RULES.md", "channel_bible.md")) {
    $p = Join-Path $Dst $f
    $t = [IO.File]::ReadAllText($p, $utf8).Replace("CHANNEL_KEY", $Key).Replace("CHANNEL_NAME", $Name)
    [IO.File]::WriteAllText($p, $t, $utf8)
}
# check the result
$cfg = Get-Content (Join-Path $Dst "channel.json") -Raw -Encoding UTF8 | ConvertFrom-Json
if ($cfg.channel_key -ne $Key) { throw "channel.json was not filled correctly." }

Write-Host "Created channels\$Key (from channels\_template)."
Write-Host "Still to fill before the first video:"
Write-Host "  1. channels\$Key\channel.json: channel_id (YouTube Studio > Settings > Channel > Advanced, starts with UC), made_for_kids (true/false), playlists"
Write-Host "  2. channels\$Key\channel_bible.md: characters, setting, tone, story format"
Write-Host "  3. channels\$Key\RULES.md: rules special to this channel (can only be stricter than shared\RULES.md)"
Write-Host "  4. Rename stories\000_story-slug for the first story (e.g. 001_<slug>)"
