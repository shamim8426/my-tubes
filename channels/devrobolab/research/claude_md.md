# Research: Claude Code CLAUDE.md file (Long 068, day key 2026-11-19, type 0 Claude Code)
Searched phrase: "Claude Code CLAUDE.md file kaise likhein" (growth/DIRECTIVES.md list 10 rank 2).
Official sources (fetched 2026-11-19 22:15 IST):
- S1 https://code.claude.com/docs/en/memory  (How Claude remembers your project)
- S2 https://code.claude.com/docs/en/best-practices  (section "Keep CLAUDE.md short")
- S3 https://code.claude.com/docs/en/commands  (rows /init, /memory; "First session in a repo")

## Facts (each with 2+ official sources where the fact appears on more than one page; single-page facts are marked)
1. Each session starts with a fresh context window; CLAUDE.md carries instructions across sessions, Claude reads it at the start of every session. S1 (intro + "CLAUDE.md files"), S2 ("Claude Code loads CLAUDE.md into every session").
2. CLAUDE.md is a plain markdown file of instructions you write. S1, S2.
3. Claude treats it as context, not enforced configuration. S1 ("context, not enforced configuration"), S2 ("no guarantee that it'll follow"; "CLAUDE.md is for guidelines").
4. Write down what you'd otherwise re-explain; add when Claude makes the same mistake a second time / you type the same correction again. S1 ("When to add"), S2 ("Anything you've had to correct twice already").
5. Locations: project ./CLAUDE.md or ./.claude/CLAUDE.md (team, shared via source control); user ~/.claude/CLAUDE.md (all your projects); ./CLAUDE.local.md (personal, this project, add to .gitignore); managed policy file (organization-wide, IT/DevOps). S1 table; S2 (CLAUDE.local.md + .gitignore).
6. Loads CLAUDE.md from current working directory and every directory above it; all concatenated, not overriding; closer files read last; subdirectory files load on demand when Claude reads/writes/edits a file in that subdirectory. S1 ("How CLAUDE.md files load"). Single page (S1) - core loading doc.
7. /init generates a starting CLAUDE.md: Claude analyzes the codebase, adds build commands, test instructions, conventions; if a CLAUDE.md exists it suggests improvements rather than overwriting. S1 (tip), S3 (/init row "Initialize project with a CLAUDE.md guide"; "Run /init to generate a starter CLAUDE.md, then /memory to refine it"), S2 ("/init generates a starting version from your codebase").
8. /memory lists CLAUDE.md files; selecting one opens it in your editor (creates it if missing). S1 ("View and edit with /memory"), S3 (/memory row "Edit CLAUDE.md files").
9. Confirm loading: /context all -> list under "Memory files". S1, S2 ("run /context all to confirm that Claude loaded the file").
10. What to write: only what Claude can't work out from the code: exact test/typecheck/lint commands, misleading places, decisions not in the repo; example sections Commands / Conventions / Gotchas (pnpm install, run one test file, typecheck; use error helpers in src/lib/errors.ts; src/legacy/ don't copy patterns; integration tests need DATABASE_URL). S2 (example file), S1 ("build commands, conventions, project layout").
11. Concrete instructions: "Use 2-space indentation" instead of "Format code properly"; "Run npm test before committing" instead of "Test your changes". S1. (S2 same idea: exact commands.)
12. Size: target under 200 lines per CLAUDE.md; longer files consume more context and reduce adherence. S1 ("Size"), S2 ("The memory guide recommends staying under 200").
13. Imports: @path/to/import syntax, relative or absolute, recursive max depth four hops; imports help organise but don't reduce context cost; paths in backticks are not imported. S1 (single page, import section).
14. .claude/rules/ with YAML frontmatter `paths:` -> loads only when Claude works with matching files. S1 ("Path-specific rules"), S2 ("Scope rules to one part of the codebase").
15. Don't describe architecture/file layout: Claude reads the repo itself. S2 (table: "Describe your architecture ... Claude reads the repo itself").
16. Adding IMPORTANT probably won't fix an ignored line: file too long, or rule that can't have exceptions -> hook. Example rule "Never read .env". S2 (note + "Never read .env"), S1 ("To block an action regardless ... use a PreToolUse hook").
17. Contradicting instructions -> Claude may pick one arbitrarily; `/doctor prompt-audit` checks outdated/conflicting content and changes nothing until you ask. S1 ("Consistency", "Audit your instruction files"), S2 ("/doctor prompt-audit flags instructions ... contradict each other").

Dropped (not needed / India-only rule): managed-policy OS paths, AGENTS.md, auto memory details, CLAUDE_CODE_NEW_INIT, Cowork notes, version numbers.
