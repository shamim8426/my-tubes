# Fact-check 018 Headless (source: https://code.claude.com/docs/en/headless, read 2026-11-03)

| Claim in the video | Docs text (quote) | Result |
|---|---|---|
| claude -p runs Claude Code without the interactive chat | "To run Claude Code in non-interactive mode, pass -p with your prompt" | PASS |
| Answer is printed; exit code 0 on success | "claude -p "What does the auth module do?"" "asks Claude a question ... and prints the response"; "Claude Code exits with code 0 on success" | PASS |
| --allowedTools "Read,Edit,Bash" runs these tools without asking | "Use --allowedTools to let Claude use certain tools without prompting... Listing Read and Edit lets Claude read and edit files without asking ... Listing Bash does the same for shell commands" | PASS |
| --output-format json gives structured result | "json: structured JSON with result, session ID, and metadata" ; example `claude -p "Summarize this project" --output-format json` | PASS |
| --continue continues earlier conversation | "Use --continue to continue the most recent conversation" | PASS |
| --output-format: text, json, stream-json | "text (default) ... json ... stream-json" | PASS |
| Without --bare, claude -p loads hooks, MCP servers, CLAUDE.md | "Without it, claude -p discovers and loads them as an interactive session would"; --bare skips "hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md" | PASS |
| --bare gives same result on every machine (CI) | "Bare mode is useful for CI and scripts where you need the same result on every machine"; "In CI ... add --bare" | PASS |
| Example file/prompt "Fix bug in auth.py" | Shortened from the docs example "Find and fix the bug in auth.py"; labelled EXAMPLE | PASS (illustrative) |
