# Fact-check 007 Subagents (second pass, 2026-10-31) - source https://code.claude.com/docs/en/sub-agents.md
PASS - every claim matched by grep against the page text.

| Scene | Claim | Docs quote |
|---|---|---|
| hook | Big task goes to a helper, main chat gets only a summary | "the subagent does that work in its own context and returns only the summary" |
| what | Own context window, system prompt, tools, permissions | "Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions" |
| file | Markdown file in .claude/agents | "Subagents are Markdown files with YAML frontmatter"; table: `.claude/agents/` = Current project |
| file | name + description required; tools, model optional | "Only `name` and `description` are required."; tools/model rows: Required "No" |
| file | Body = system prompt | "The body becomes the system prompt" |
| call | Name in prompt, Claude decides | "Natural language: name the subagent in your prompt; Claude decides whether to delegate" |
| call | @-mention always runs it | "@-mention: guarantees the subagent runs for one task" |
| call | --agent flag, whole session | "Session-wide: the whole session runs as that subagent via the `--agent` flag or the `agent` setting" |
| parallel | auth/db/API parallel, Claude combines | "Research the authentication, database, and API modules in parallel using separate subagents" / "Each subagent explores its area independently, then Claude synthesizes the findings" |
| when | Main chat for back-and-forth, quick change | "frequent back-and-forth or iterative refinement"; "making a quick, targeted change" |
| when | Subagent for verbose output, tool limits, summary | "produces verbose output you don't need"; "enforce specific tool restrictions or permissions"; "can return a summary" |
| when | Run tests, report only failing | "run the test suite and report only the failing tests with their error messages" |
