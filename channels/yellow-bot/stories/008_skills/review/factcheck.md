# Fact-check 008 Skills (second pass, 2026-10-31) - source https://code.claude.com/docs/en/skills.md
PASS - each claim matched by grep on the page text.
| Scene | Claim | Docs quote |
|---|---|---|
| hook | Same instructions pasted again and again -> make a skill | "Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat" |
| what | SKILL.md with instructions; Claude uses it, or /skill-name | "Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`." |
| file | Folder with SKILL.md; description tells Claude when | "Create a directory for the skill"; "the `description` helps Claude decide when to load the skill automatically"; description "Recommended" |
| file | Example text | summarize-changes example (description + instructions) |
| load | Description always in context, full skill on invoke | "Description always in context, full skill loads when invoked" |
| who | Default: both can invoke | "By default, both you and Claude can invoke any skill." |
| who | disable-model-invocation: true, e.g. /deploy | "`disable-model-invocation: true`: Claude can't invoke the skill on its own ... like `/commit`, `/deploy`" |
| where | Personal / Project / Plugin | table: Personal `~/.claude/skills/...` All your projects; Project `.claude/skills/...` "Commit it so your team gets it too"; Plugin: "Wherever the plugin is enabled" |
