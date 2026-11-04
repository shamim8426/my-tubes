# Fact-check 015 Worktrees (source: https://code.claude.com/docs/en/worktrees.md, read 2026-11-03)

| Claim in the video | Docs text (quote) | Result |
|---|---|---|
| Two sessions in one folder can collide; worktree gives own folder + branch | "Isolate parallel Claude Code sessions in separate git worktrees so changes don't collide." / "a separate working directory with its own files and branch" | PASS (collision shown as illustration) |
| --worktree with a name creates the worktree under .claude/worktrees/ on a new branch | "Pass `--worktree` or `-w` with a name to create an isolated worktree ... created under `.claude/worktrees/<name>/` ... on a new branch named `worktree-<name>`" | PASS |
| Example: claude --worktree feature-auth, second terminal with another name (bugfix) | "claude --worktree feature-auth"; "Run the command again with a different name in another terminal to start a second isolated session." (name bugfix is an invented example, labelled EXAMPLE) | PASS |
| On exit Claude checks the worktree; clean + unnamed is removed automatically | "Claude checks the worktree for work that removal would delete"; "The worktree is clean: for an unnamed session, Claude removes the worktree and its branch automatically." | PASS |
| Work left -> Claude asks keep or remove | "The worktree has work in it: Claude prompts you to keep or remove the worktree." | PASS |
| Removing deletes folder and branch | "Removing deletes the worktree directory and its branch, along with all the work in them" | PASS |
| Worktree is a fresh checkout so .env is not there | "A worktree is a fresh checkout, so untracked files like `.env` or `.env.local` ... are not present." | PASS |
| .worktreeinclude copies files that match AND are gitignored | "Only files that match a pattern and are also gitignored are copied, so tracked files are never duplicated." | PASS |
