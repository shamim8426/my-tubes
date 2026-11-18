# Research: Claude Code me apna (custom) slash command kaise banayein (2026-11-18, story 064)

Search phrase (DIRECTIVES 10 rank 3): "Claude Code custom slash commands kaise banayein".

## Official sources
- S1 https://code.claude.com/docs/en/skills ("Extend Claude with skills"; https://code.claude.com/docs/en/slash-commands opens the same page)
- S2 https://code.claude.com/docs/en/commands ("Commands" reference)

## Facts (copied, each checked on the page on 2026-11-18)
- Custom commands have been merged into skills; existing `.claude/commands/` files keep working. (S1, box at top)
- A Markdown file in `.claude/commands/` is the older format and still works ... "Prefer a skill for new work". (S1)
- Project location: `.claude/skills/<skill-name>/SKILL.md` = sessions in this repository; personal: `~/.claude/skills/<skill-name>/SKILL.md` = all your projects on this machine. (S1 table)
- Command name = frontmatter `name` or the directory name; `.claude/skills/deploy-staging/SKILL.md` -> `/deploy-staging`. Old format: `.claude/commands/deploy.md` -> `/deploy`. (S1 naming table)
- Frontmatter between `---` markers at the top of SKILL.md, instructions as Markdown after the closing `---`. All fields optional; only `description` recommended so Claude knows when to use the skill. (S1)
- `$ARGUMENTS` = all arguments passed when invoking the skill. Example fix-issue: "When you run `/fix-issue 123`, Claude receives "Fix GitHub issue 123 following our coding standards..."" (S1)
- `disable-model-invocation: true` = Claude does not load it on its own; you trigger it with `/name`. (S1) Also S1: by default both you and Claude can invoke any skill.
- Live change detection: Claude Code watches skill directories; adding/editing a skill under `~/.claude/skills/` or project `.claude/skills/` is picked up in the current session without restart. If you create a top-level skills directory that did not exist when the session started, run `/reload-skills`. (S1)
- `/reload-skills`: re-scan skill and command directories so skills added on disk during the session become available without restarting. (S2)
- "To add your own commands, see skills." Type `/` to see the commands available to you. A command is only recognized at the start of your message; text after the name becomes its arguments. (S2)

## How-to steps (checked against S1 "Create your first skill" + naming table)
1. Project me folder: `.claude/skills/fix-issue/`
2. Usme file `SKILL.md`: frontmatter `description`, neeche steps, `$ARGUMENTS` jahan input chahiye.
3. Claude Code me `/fix-issue 123` likho.
4. Session pehle se chal raha tha aur `.claude/skills` naya bana? `/reload-skills`.
5. Har project ke liye: `~/.claude/skills/...`.

## Dropped / not used
- `allowed-tools`, `argument-hint`, `$0/$1`, dynamic context `!` - true but too much for a 55 s beginner Short.
- No claim about personal `~/.claude/commands/` (S1 does not mention it).
