# Dossier - Short 001: CLAUDE.md
Single source (official): https://code.claude.com/docs/en/memory (read 2026-10-31). Every on-screen / spoken claim:

| ID | Claim in the video | Where it comes from on the page |
|---|---|---|
| F1 | Each Claude Code session starts with a fresh context window; two mechanisms carry knowledge across sessions (CLAUDE.md, auto memory) | intro of the page |
| F2 | CLAUDE.md = instructions you write; loaded at the start of every conversation | "CLAUDE.md vs auto memory" table |
| F3 | Project file: `./CLAUDE.md` or `./.claude/CLAUDE.md`, shared with the team via source control | memory locations table |
| F4 | User file: `~/.claude/CLAUDE.md`, applies to all your projects | memory locations table |
| F5 | `/init` generates a starting CLAUDE.md; Claude analyses the codebase | note under "Set up a project CLAUDE.md" |
| F6 | Target under 200 lines per file; contradicting instructions may be picked arbitrarily | "Write effective instructions" (Size, Consistency) |
| F7 | CLAUDE.md is context, not enforced configuration; to block an action use a PreToolUse hook | intro of the page |

Not claimed: anything about auto memory details, managed policy files, `.claude/rules/`, CLAUDE.local.md (left out to keep the Short to one idea).
To re-check before each new Short: docs change often (this page was read on 2026-10-31).
