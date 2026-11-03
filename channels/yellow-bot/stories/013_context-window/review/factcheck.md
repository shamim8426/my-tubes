# Fact-check 013 Context window (source: https://code.claude.com/docs/en/context-window, read 2026-11-03)

| Claim in the video | Docs text (quote) | Result |
|---|---|---|
| Context window holds instructions, files read, Claude's own responses | "holds everything Claude knows about your session: your instructions, the files it reads, its own responses, and content that never appears in your terminal" | PASS |
| It fills as the session runs | "plays a full session from startup to compaction: ... what each file read, rule, and hook adds as Claude works" | PASS |
| After compaction project-root CLAUDE.md and auto memory are re-injected from disk | Table: "Project-root CLAUDE.md and unscoped rules - Re-injected from disk"; "Auto memory - Re-injected from disk" | PASS |
| /compact makes a structured summary | "you run /compact, which replaces the conversation with a structured summary" | PASS |
| System prompt and output style still apply | Table: "System prompt and output style - Both still apply" | PASS |
| /compact focus on the auth bug fix; summary keeps what you choose | "run /compact with instructions, like /compact focus on the auth bug fix ... The summary keeps what you choose instead of what the automatic pass guesses is important." | PASS |
| /context shows live breakdown | "run /context for a live breakdown by category" | PASS |
| Path-scoped rules are summarized away | "compaction summarizes them away with everything else" | PASS |
| Fix: drop paths: frontmatter or move to project-root CLAUDE.md | "drop the paths: frontmatter or move it to the project-root CLAUDE.md" | PASS |
| Open question (when do you run /compact) | Not a claim | n/a |
