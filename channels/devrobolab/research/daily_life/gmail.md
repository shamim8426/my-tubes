# Daily life 02: Gmail connector (2026-11-14)
Sources (official): https://claude.com/docs/connectors/google/gmail.md ; https://support.claude.com/en/articles/10166901-use-google-workspace-connectors
- Setup (claude.com docs): Customize > Connectors (claude.ai) > find Gmail > Connect > sign in to Google, grant permissions. Button becomes Disconnect. Once. Pro/Max/Ultra/Team/Enterprise; Team/Enterprise owner enables first.
- In chat: + (lower left) > Connectors > turn on Gmail. Claude searches email only when needed, answers with citations/links to the mails.
- Example prompts (official docs): "What did Sarah say about the project deadline?", "Find emails about the Q4 budget review", "Summarize my conversation with the sales team last week".
- Conflict: claude.com Gmail page says read-only (cannot create/send/modify). support.claude.com Workspace page says draft/send/reply/forward with approval before each. => Script claims only: search/read + Claude writes reply TEXT in the chat, user checks and sends themselves; caution says pages differ, check connector settings, approve/verify before anything is sent.
- Limits: attachment content not accessible (metadata only); cannot see images embedded in mails; only your own account's mail.
- Privacy: no training on Gmail/Drive/Calendar connector data (support page).
