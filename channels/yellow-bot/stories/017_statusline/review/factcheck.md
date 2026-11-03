# Fact-check 017 Statusline (source: https://code.claude.com/docs/en/statusline, read 2026-11-03)

| Claim in the video | Docs text (quote) | Result |
|---|---|---|
| Status line sits at the bottom of Claude Code | "a customizable bar at the bottom of Claude Code that runs any shell script you configure" | PASS |
| It receives JSON data (stdin), script output is shown (stdout) | "It receives JSON session data on stdin and displays whatever your script prints" | PASS |
| Useful for context usage, cost, git | "monitor context window usage as you work", "track session costs", "git branch and status always visible" | PASS |
| /statusline makes the script for you | "Claude Code generates a script file in ~/.claude/ and updates your settings automatically" | PASS |
| settings: statusLine, type command, command = script path | `"statusLine": {"type": "command", "command": "~/.claude/statusline.sh"}` ; "Set type to "command" and point command to a script path" | PASS |
| Example bar "[Opus] my-app | 42% context", 42% meter | Illustrative; docs example shows model name, directory, context percentage ("[Opus 5.5] ... 42%") | PASS (illustrative) |
| Runs locally, no API tokens | "The status line runs locally and does not consume API tokens." | PASS |
| Hides during help menu and permission prompts | "It temporarily hides during certain UI interactions, including the help menu and permission prompts." | PASS |
| Runs again after each new assistant message | "it runs again when: A new assistant message arrives" | PASS |
