# Fact-check 010 Memory (second pass, 2026-10-31) - source https://code.claude.com/docs/en/memory.md
PASS - each claim matched by grep on the page text.
| Scene | Claim | Docs quote |
|---|---|---|
| hook | Fresh context each session; two mechanisms carry knowledge | "Each Claude Code session begins with a fresh context window. Two mechanisms carry knowledge across sessions" |
| two | CLAUDE.md = you write; auto memory = Claude writes from corrections | "CLAUDE.md files: instructions you write..."; "Auto memory: notes Claude writes itself based on your corrections and preferences" |
| two | Both load every session | "Both are loaded at the start of every conversation." |
| write | Concrete examples | "Write instructions that are concrete enough to verify: 'Use 2-space indentation'; 'Run `npm test` before committing'; 'API handlers live in `src/api/handlers/`'" |
| where | Project ./CLAUDE.md team; User ~/.claude/CLAUDE.md all projects; Local CLAUDE.local.md only you, gitignore | Location table (Project: team via source control; User: only you, all projects; Local: "add to `.gitignore`") |
| auto | Claude notes in MEMORY.md; first 200 lines / 25KB loaded | "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation." ; "ask Claude to remember something ... saves it to auto memory" |
| tips | /init starting CLAUDE.md; /memory browse+edit; under 200 lines | "Run `/init` to generate a starting CLAUDE.md"; "Run `/memory` to browse and open memory files"; "target under 200 lines per CLAUDE.md file" |
