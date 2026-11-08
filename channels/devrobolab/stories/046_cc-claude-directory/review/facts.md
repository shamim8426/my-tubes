# Facts: Claude Code 03, "Explore the .claude directory"
Source (only): https://code.claude.com/docs/en/claude-directory.md (fetched 2026-11-07)

- F1 Claude Code reads instructions, settings, skills, subagents, memory from the project directory and from ~/.claude. Commit project files to git to share with the team; ~/.claude is personal and applies across all projects. [page intro]
- F2 On Windows ~/.claude = %USERPROFILE%\.claude; CLAUDE_CONFIG_DIR moves it. [page]
- F3 Most users only edit CLAUDE.md and settings.json; the rest is optional. AGENTS.md can be read in place of CLAUDE.md. [page]
- F4 CLAUDE.md: instructions loaded every session. settings.json: permissions, hooks, env vars, model defaults. settings.local.json: personal overrides (project only). .mcp.json: team-shared MCP servers (project only). [File reference table]
- F5 skills/<name>/SKILL.md invoked with /name; agents/*.md subagents with own prompt and tools; rules/*.md topic-scoped, optionally path-gated; output-styles/*.md adjust how Claude works. [table]
- F6 CLAUDE.local.md: private preferences, create manually and add to .gitignore. [What's not shown]
- F7 Managed settings deployed by the organization take precedence over every settings file (narrow exceptions). [note]
- F8 Application data (transcripts, prompt history) is plaintext, not encrypted; a .env read by a tool is written to the transcript. [Plaintext storage]
- F9 Default cleanupPeriodDays = 30 (minimum 1). [Cleaned up automatically]
- F10 `claude purge <path> --dry-run` prints the plan; purge deletes transcripts and auto memory of one project, per-session tasks/debug/file-history, matching history lines, the project's entry in ~/.claude.json. [Clear local data]
- F11 Do not delete ~/.claude.json, ~/.claude/settings.json, ~/.claude/plugins/. [Clear local data]
- Example settings.json content in the video (npm test allow) is our illustration, labelled as an example.
