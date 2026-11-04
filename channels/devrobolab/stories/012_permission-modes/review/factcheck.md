# Fact-check 012 Permission modes (second pass, 2026-11-01) - source https://code.claude.com/docs/en/permission-modes.md
PASS - each claim matched by grep on the page text.
| Scene | Claim | Docs quote |
|---|---|---|
| hook | Modes decide whether Claude asks | "A permission mode sets which actions Claude can take in a session without asking you first." |
| hook/cli | Shift+Tab cycles; status bar shows mode | "press `Shift+Tab` to cycle permission modes"; "gray `⏸ manual mode on`", `⏵⏵ accept edits on`, `⏸ plan mode on` |
| modes | Manual = reads only; acceptEdits = reads + file edits + fs commands; plan = research/propose; auto = classifier | Modes table: `default` "Reads only"; `acceptEdits` "Reads, file edits, and common filesystem commands"; "Plan mode tells Claude to research and propose changes without making them"; "a second model, the classifier, reviews actions instead of you" |
| cli | claude --permission-mode plan; Shift+Tab; /plan per prompt | "claude --permission-mode plan"; "prefixing a single prompt with `/plan`" |
| plan | Edits blocked until approve | "edits stay blocked until you approve the plan" |
| extreme | dontAsk = pre-approved tools, locked-down CI; bypass = everything, isolated containers/VMs | Modes table: dontAsk "Locked-down CI and scripts"; bypassPermissions "Everything" / "Isolated containers and VMs only" |
| rules | Deny rules block in every mode incl. bypass | "Deny rules block in every mode, including `bypassPermissions`." |
| rules | Protected paths never auto-approved (except bypass) | "Writes to protected paths are never auto-approved except in `bypassPermissions` mode ..." |
| rules | Layer permission rules on modes | "Modes set the baseline. Layer permission rules on top" |
