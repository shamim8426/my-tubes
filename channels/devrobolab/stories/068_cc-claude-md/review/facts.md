# 068 facts (every spoken claim -> source). Sources: S1 https://code.claude.com/docs/en/memory , S2 https://code.claude.com/docs/en/best-practices , S3 https://code.claude.com/docs/en/commands (fetched 2026-11-19). Full notes: channels/devrobolab/research/claude_md.md

| # | Scene | Claim (spoken) | Source | Check |
|---|---|---|---|---|
| F1 | hook/what | Each new session starts with an empty context window; earlier conversation is not remembered | S1 intro "Each Claude Code session begins with a fresh context window"; S2 | PASS |
| F2 | hook/what | CLAUDE.md = markdown file with your project instructions, Claude reads it at the start of every session | S1 "CLAUDE.md files"; S2 "loads CLAUDE.md into every session" | PASS |
| F3 | what | Write what you explain again and again | S1 "write down what you'd otherwise re-explain" | PASS |
| F4 | what | Read as context, not a hard lock | S1 "context, not enforced configuration"; S2 "no guarantee" | PASS |
| F5 | where | Project folder file: whole team, goes to git | S1 table "Team-shared ... via source control" | PASS |
| F6 | where | ~/.claude/CLAUDE.md applies to all your projects | S1 table "Personal preferences for all projects" | PASS |
| F7 | where | CLAUDE.local.md only for you in this project, add to .gitignore | S1 table + import section; S2 "add that file to .gitignore" | PASS |
| F8 | where | Managed file that IT team keeps for everyone | S1 table "Organization-wide instructions managed by IT/DevOps" | PASS |
| F9 | where | Reads files in current folder and every folder above, joins them (concatenated) | S1 "How CLAUDE.md files load" | PASS |
| F10 | where | Sub-folder files load when Claude works on a file in that folder | S1 "loads each one once Claude reads, writes, or edits another file in that subdirectory" | PASS |
| F11 | init | /init: reads codebase, starting file with build commands, test instructions, conventions | S1 tip; S3 /init row; S2 | PASS |
| F12 | init | Existing file: /init suggests improvements, doesn't overwrite | S1 tip "suggests improvements rather than overwriting it" | PASS |
| F13 | init | /memory -> pick file -> opens in your editor | S1 "/memory ... Select any file to open it in your editor"; S3 /memory row | PASS |
| F14 | init | /context all -> Memory files list | S1; S2 | PASS |
| F15 | write | Only what Claude can't work out from code; examples commands (install, one test file, typecheck), conventions (error helper file, legacy folder patterns), gotchas (integration tests need DATABASE_URL) | S2 "Keep CLAUDE.md short" example file | PASS |
| F16 | write | "Use 2-space indentation" not "Format code properly"; "Run npm test before committing" not "Test your changes" | S1 "Write effective instructions" | PASS |
| F17 | write | Add when Claude repeats a mistake / you type the same correction again | S1 "When to add"; S2 "correct twice" | PASS |
| F18 | size | Under 200 lines; longer = more context, less adherence | S1 "Size"; S2 | PASS |
| F19 | size | @ import e.g. @README; up to four hops; imported files load fully, cost not reduced | S1 "Import additional files" + "Size" | PASS |
| F20 | size | .claude/rules with `paths` frontmatter loads only when Claude works on matching files | S1 "Path-specific rules"; S2 "Scope rules" | PASS |
| F21 | mistakes | Don't write architecture/file layout, Claude reads repo itself | S2 table "Claude reads the repo itself" | PASS |
| F22 | mistakes | IMPORTANT often doesn't fix; file too long or no-exception rule (e.g. never read .env) -> hook | S2 note + "Never read .env" example | PASS |
| F23 | mistakes | Conflicting instructions -> Claude may pick one; /doctor prompt-audit finds conflicts and outdated items | S1 "Consistency" + "Audit your instruction files"; S2 | PASS |

On-screen example file text is our own illustration based on S2's example (labelled "example").
