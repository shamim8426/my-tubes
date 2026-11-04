# Fact-check 023 (source: https://code.claude.com/docs/en/features-overview.md, read 2026-11-04)
Analogies (fridge note, recipe card) are labelled explanations.
- CLAUDE.md = "Persistent context loaded every conversation"; "Loads: Every session, automatically"; example "Use pnpm, not npm. Run tests before committing." (page's own example).
- Skill = "Instructions, knowledge, and workflows Claude can use"; loads "On demand"; trigger "You keep typing the same prompt to start a task -> Save it as a user-invocable skill"; example "/deploy runs your deployment checklist".
- Hook = "Script, HTTP request... triggered by events"; "Fires on its event without Claude deciding"; example "Run ESLint after every file edit".
- Caution: "An instruction like 'never edit .env' in CLAUDE.md or a skill is a request, not a guarantee. A PreToolUse hook that blocks the edit is enforcement."
- Recap lines restate the table "When to use it".
