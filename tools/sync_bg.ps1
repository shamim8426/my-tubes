# Starts sync.ps1 in a hidden background process and returns immediately.
# Used by the Claude Code SessionEnd hook (hooks only get a few seconds).
param([string]$Message = "auto: session end")
$sync = Join-Path $PSScriptRoot "sync.ps1"
Start-Process -WindowStyle Hidden -FilePath "powershell.exe" `
    -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$sync`"", "-Message", "`"$Message`"")
