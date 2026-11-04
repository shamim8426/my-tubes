# Fact-check 016 Plugins overview (source: https://code.claude.com/docs/en/plugins/overview.md, read 2026-11-03)
(The queue URL /plugins-overview.md is a 404; the page now lives at /plugins/overview.md, same title.)

| Claim in the video | Docs text (quote) | Result |
|---|---|---|
| Plugin packs skills, agents, hooks, MCP servers as one unit | "A Claude Code plugin is a directory of skills, agents, hooks, MCP servers, or other components that Claude Code installs and loads as one unit." | PASS |
| Manifest gives the plugin its name (shown in docs screenshot) | "The manifest, a JSON file at `.claude-plugin/plugin.json`, gives the plugin its name" | PASS |
| Components: skills, agents, hooks, MCP servers | Component list: Skills, Agents, Hooks, A hooks module, MCP servers ("such as") | PASS |
| Run /plugin, Discover tab lists plugins from marketplaces | "run `/plugin` ... install one from the **Discover** tab, which lists the plugins from your marketplaces" | PASS |
| Marketplaces tab shows Context cost for official plugins | "open the plugin from the **Marketplaces** tab in `/plugin`. Plugins in Anthropic's official marketplace show a **Context cost** estimate there." | PASS |
| Installed tab has "Not used recently" group | "the **Installed** tab's **Not used recently** group lists plugins you could turn off" | PASS |
| Enabled plugin is part of every session | "An enabled plugin is part of every session, not only the sessions where you use it." | PASS |
| Name+description of skills/agents Claude can invoke on its own are in context every turn | "for each skill, agent, and command that Claude can invoke on its own, the name and description are in Claude's context on every turn" | PASS |
| MCP servers and hooks run | "MCP servers the plugin defines run alongside each session where it's enabled, and its hooks fire at their events." | PASS |
| Plugin runs as you | "what the plugin runs, it runs as you" | PASS |
