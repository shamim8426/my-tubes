# Fact-check 019 overview (source: https://code.claude.com/docs/en/overview.md, read 2026-11-04)
Analogies ("jaise ek assistant", "ek dimaag, kai darwaze", CLAUDE.md "parchi") are labelled explanations, not features.
- "5 jagah chalta hai" -> tabs: Terminal, VS Code, Desktop app, Web, JetBrains; "Claude Code runs on several surfaces: the terminal, IDE extensions, a desktop app, and the web."
- Helper reads files, writes code, runs commands -> "reads your codebase, edits files, runs commands, and integrates with your development tools."
- agentic -> "Claude Code is an agentic coding tool" (meaning 'khud kaam karne wala' = plain-words gloss)
- login bug example; sees whole project, edits several files, checks -> "Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works." / "understands your entire codebase and can work across multiple files"
- Terminal = text window for commands -> "The full-featured CLI for working with Claude Code directly in your terminal." (gloss of 'terminal')
- VS Code: inline diffs -> "inline diffs, @-mentions, plan review, and conversation history directly in your editor"
- JetBrains: IntelliJ / PyCharm / WebStorm, diff -> "IntelliJ IDEA, PyCharm, WebStorm... interactive diff viewing"
- IDE = code editors (VS Code, JetBrains) -> "IDE extensions"; gloss only.
- Desktop app, sessions side by side -> "run multiple sessions side by side"
- Web: browser, no setup; tasks in parallel; claude.ai/code -> "Run Claude Code in your browser with no local setup... run multiple tasks in parallel. Start coding at claude.ai/code."
- boring tasks: tests, bug fix, commit + PR -> "writing tests for untested code, fixing lint errors..." / "For bugs, paste an error message... implements a fix" / "stages changes, writes commit messages, creates branches, and opens pull requests."
- same engine; CLAUDE.md, settings, MCP work everywhere -> "Each surface connects to the same underlying Claude Code engine, so your repo's CLAUDE.md files, settings, and MCP servers work across all of them."
- CLAUDE.md = project rules file read each session -> "a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards..."
- MCP = connect outside tools -> "open standard for connecting AI tools to external data sources"
