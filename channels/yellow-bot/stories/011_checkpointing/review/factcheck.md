# Fact-check 011 Checkpointing (second pass, 2026-10-31) - source https://code.claude.com/docs/en/checkpointing.md
PASS - each claim matched by grep on the page text.
| Scene | Claim | Docs quote |
|---|---|---|
| hook | Undo bad edits; Esc twice | "quickly undo changes and rewind to previous states"; "Run `/rewind`, or press `Esc` twice when the prompt input is empty" |
| what | Checkpoint before each prompt; works after resume | "captures the state of your code before each prompt you send that starts a turn"; "you can still run `/rewind` after you resume a session" |
| menu | Restore code and conversation / conversation / code / Summarize from here | the four bullets of the rewind menu (Summarize from here: "freeing context window space") |
| open | /rewind or Esc Esc on empty prompt; text in prompt -> Esc Esc clears it | "If the prompt input contains text, double `Esc` clears it instead of opening the menu." |
| use | Try approaches without losing starting point | "Exploring alternatives: try different implementation approaches without losing your starting point" |
| limit | Not Git; quick session recovery | "Checkpoints are designed for quick, session-level recovery. For permanent version history ... use version control, such as Git" |
| limit | Bash-only changed file not tracked | "A file that only Bash commands changed isn't tracked and stays as it is." |
