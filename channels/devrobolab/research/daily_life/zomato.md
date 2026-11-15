# Daily life 01: Zomato connector (2026-11-13)
Sources: https://github.com/Zomato/mcp-server-manifest (Zomato, third-party), https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp (Anthropic official)
- Zomato MCP endpoint: https://mcp-server.zomato.com/mcp (Zomato repo). Features: find restaurants, menu, cart, order, payment by QR.
- Zomato repo: "only for testing purposes", disclaims liability; third-party apps restricted; OAuth only for whitelisted redirects (Claude is listed per directories).
- Claude steps (official): Customize > Connectors > + Add > Add custom connector > name > server URL > Continue > Authentication (sign in) > Add. Turn on per chat: + > Connectors. Free plan: 1 custom connector.
- Caution (official): only connect servers you trust; prompt injection; review permissions; allow tools carefully.
- Prompts: "Mere paas Rs 300 hain, paas me veg restaurant dikhao", "Menu me se 2 paneer item cart me daalo", "Order track karo".
- Our rule: third-party, example only, no real order/account/payment shown. Payment = QR by user, Claude never pays.
