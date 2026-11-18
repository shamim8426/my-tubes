# 064 facts (every spoken/on-screen claim -> official source). Research: channels/devrobolab/research/custom_slash_commands.md
S1 = https://code.claude.com/docs/en/skills   S2 = https://code.claude.com/docs/en/commands

| # | Claim in video | Source | Status |
|---|---|---|---|
| F1 | Apna slash command = ek file (SKILL.md); custom commands are merged into skills | S1 | PASS |
| F2 | Project folder `.claude/skills/fix-issue/` with `SKILL.md` inside | S1 locations table | PASS |
| F3 | Folder name becomes the command (`/fix-issue`) | S1 naming table | PASS |
| F4 | Frontmatter between `---` lines at the top; `description` = what it does / when to use | S1 frontmatter | PASS |
| F5 | Steps/instructions written as Markdown below the frontmatter | S1 frontmatter | PASS |
| F6 | `$ARGUMENTS` gets what you type; `/fix-issue 123` -> "Fix GitHub issue 123 ..." | S1 arguments + fix-issue example | PASS |
| F7 | Session already running and the skills folder is new -> run `/reload-skills` | S1 live change detection + S2 /reload-skills | PASS |
| F8 | For all projects: `~/.claude/skills/` (personal) | S1 locations table | PASS |
| F9 | Old `.claude/commands/` files still work; prefer skills for new work | S1 | PASS |
| F10 | Type `/` to see your commands; command only at the start of the message | S2 | PASS |
