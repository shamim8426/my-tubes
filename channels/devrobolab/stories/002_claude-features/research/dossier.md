# Dossier - Short 002: 5 Claude Code features (read 2026-10-31, official docs only)
| Feature | What the video says | Source page (code.claude.com/docs/en/...) |
|---|---|---|
| Plan Mode | Shift+Tab; Claude reads files and proposes a plan, makes no edits until you approve | common-workflows ("Plan before editing") |
| Subagents | each runs in its own context window; project agents live in .claude/agents/ | sub-agents |
| Skills | SKILL.md; Claude uses it when relevant; the body loads only when it is used | skills |
| Hooks | user-defined shell commands run at set points in Claude Code's lifecycle; certain actions always happen instead of relying on the LLM to choose; configured in a settings file | hooks-guide |
| MCP | `claude mcp add` connects external tools and data; verify you trust a server (prompt-injection risk) | mcp |
Not claimed: any speed/accuracy/benefit numbers, version numbers, or "most people do not know". Re-read the pages before every new Short (docs change often).
Images: AI-generated, no people/text/logos (Cloudflare free engine, Rs0). Voice: Gemini TTS (Charon), about Rs1. Music: "Soaring" Kevin MacLeod, CC BY 4.0.
