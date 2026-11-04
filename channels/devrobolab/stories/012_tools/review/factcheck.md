# Fact-check 012 Tools (source: https://code.claude.com/docs/en/tools-reference, read 2026-10-31)

| Claim in the video | Docs text (quote) | Result |
|---|---|---|
| Claude Code has tools for reading files, editing files, running commands | Table: `Read` "Reads the contents of files", `Edit` "Makes targeted edits to specific files", `Bash` "Executes shell commands in your environment" | PASS |
| Read = permission "No" | Table row `Read` ... "No" | PASS |
| Edit = permission "Yes" | Table row `Edit` ... "Yes" | PASS |
| Bash = permission "Yes" | Table row `Bash` ... "Yes" | PASS |
| Agent = permission "No" | Table row `Agent` ... "No" | PASS |
| Bash read-only commands run without prompting | Note: "`Bash` is marked Yes but runs a built-in set of read-only commands without prompting." | PASS |
| Read prompts for paths outside the working directory | Note: "File-access tools marked No, including `Read`, `Grep`, and `Glob`, still prompt for paths outside the working directory and additional directories." | PASS |
| New tool = connect an MCP server; reusable workflow = write a skill | "To add custom tools, connect an MCP server. To extend Claude with reusable prompt-based workflows, write a skill" | PASS |
| Example (login bug, auth.js, npm test) | Illustrative, labelled "EXAMPLE" on screen; file name and command are invented, behaviour follows the table (Read No, Edit Yes, Bash Yes; npm test is not in the read-only set claimed by the docs, so it is described only as "Bash asks", not as a guarantee) | PASS (labelled example) |
| Not claimed: Grep/Glob availability | Docs say Grep/Glob are absent by default on macOS, Linux and WSL, so they are NOT shown as cards in the video | PASS |
