# Fact-check 009 MCP (second pass, 2026-10-31) - source https://code.claude.com/docs/en/mcp.md
PASS - each claim matched by grep on the page text.
| Scene | Claim | Docs quote |
|---|---|---|
| hook | Stop copy-pasting from tools; connect directly | "Connect a server when you find yourself copying data into chat from another tool ... Claude can read and act on that system directly instead of working from what you paste" |
| what | MCP = Model Context Protocol, open source standard | "Model Context Protocol (MCP), an open source standard for AI-tool integrations" |
| what | Issue trackers, monitoring, databases, designs | "What you can do with MCP": JIRA issue, Sentry and Statsig, PostgreSQL database, Figma designs |
| example | JIRA ENG-4521 feature + PR on GitHub | "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub." |
| add | HTTP recommended for remote | "HTTP servers are the recommended option for connecting to remote MCP servers." |
| add | Command syntax / Notion example | `claude mcp add --transport http <name> <url>`; `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| add | list and /mcp | "# List all configured servers: claude mcp list"; "# (within Claude Code) Check server status: /mcp" |
| scope | Local default, only you; Project .mcp.json via version control; User all projects | "Local scope is the default"; scope table: Project - Yes, via version control - `.mcp.json`; User - All your projects |
| types | stdio = local process on your machine; HTTP = cloud services | "Stdio servers run as local processes on your machine."; HTTP "most widely supported transport for cloud-based services" |
| types | Trust the server first | "Verify you trust each server before connecting it." |
