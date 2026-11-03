# Fact-check 014 Sessions (source: https://code.claude.com/docs/en/sessions, read 2026-11-03)

| Claim in the video | Docs text (quote) | Result |
|---|---|---|
| A session is a saved conversation, saved locally | "A session is a saved conversation tied to a project directory. Claude Code stores it locally as you work" | PASS |
| You can return after exiting or /clear | "so you can return to one after exiting or running /clear" | PASS |
| claude --continue opens most recent session | Table: "Reopens the most recent session in the current directory" | PASS |
| claude --resume opens picker | Table: "Opens the session picker" | PASS |
| /resume switches from inside | Table: "Switches to a different session from inside an active session" | PASS |
| Name: claude -n, /rename | Table: "claude -n auth-refactor"; "/rename auth-refactor" | PASS |
| Picker: arrows navigate, Enter resumes, Space previews | Table: "Navigate between sessions" (up/down), "Enter Resume the highlighted session", "Space Preview the session content" | PASS |
| /branch makes a copy, original unchanged; optional name | "creates a copy of the conversation so far ... leaving the original intact"; "/branch try-streaming-approach"; "claude --continue --fork-session" | PASS |
| Default name like my-app-3f is not a resume handle | "The default isn't a resume handle." example "my-app-3f" | PASS |
| Generated title / own name works | "Only the generated title works as a resume handle"; "You can pass either title to claude --resume" | PASS |
| Picker rows fix-login, try-streaming; resume auth-refactor | Illustrative names, labelled "example" on screen (auth-refactor from docs) | PASS (labelled) |
