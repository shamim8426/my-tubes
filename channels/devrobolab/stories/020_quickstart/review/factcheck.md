# Fact-check 020 quickstart (source: https://code.claude.com/docs/en/quickstart.md, read 2026-11-04)
Glosses ("terminal = text wali window") are explanations, not features. UI mocks (code cards, browser window) are illustrative, no real UI text is claimed.
- "4 steps: install, login, pehla sawal, pehla code change" -> page headings "Step 1: Install Claude Code", "Step 2: Start your first session" (login prompt on first use), "Step 3: Ask your first question", "Step 4: Make your first code change".
- Open a terminal, run the install command -> "To install Claude Code, open a terminal and run the command for your system." Command shown: `curl -fsSL https://claude.ai/install.sh | bash` (macOS, Linux, WSL).
- `claude --version`; version number -> "run `claude --version`. A working installation prints a version number." and "The command prints a version number followed by `(Claude Code)`." (on screen: "<version number> (Claude Code)", no number invented)
- Step 2: `cd /path/to/your/project` then `claude` -> "cd /path/to/your/project / claude" in the page.
- First login prompt, browser prompts -> "Claude Code prompts you to log in on first use. For Claude subscription or Console accounts, follow the prompts to complete authentication in your browser."
- Account chips Pro / Max / Ultra / Team / Enterprise / Console -> "Claude Pro, Max, Ultra, Team, or Enterprise" and "Claude Console (API access with pre-paid credits)".
- Login only once -> "Once logged in, your credentials are stored and you won't need to log in again."
- Step 3 question -> "what does this project do?"; "Claude will analyze your files and provide a summary."
- Claude reads files itself, no context to add -> "Claude Code reads your project files as needed. You don't have to manually add context."
- Step 4 prompt -> "add a hello world function to the main file"; "Claude Code finds the appropriate file and shows you the change. If it asks before making the change, select Yes to approve."
- Git by talking -> "Claude Code makes Git operations conversational" with prompt "commit my changes with a descriptive message".
- /help, /clear -> session commands table: "/help Show available commands", "/clear Clear conversation history".
- Shift+Tab -> "Press Shift+Tab at any time to switch the permission mode of the session you're in."
