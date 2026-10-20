---
name: new-story
description: Start a new Kissago story with the Kalam script writer. Use when the user says "nayi kahani", "story ideas", "kahani options", "script likho" or asks for a script for a chosen story idea.
---

# New story (Kalam)

1. Call the `kalam` subagent (Agent tool, `subagent_type: "kalam"`):
   - for ideas: "5 story options for channel <key>" (+ any theme the user gave);
   - for a script: the chosen idea and any user notes.
2. Kalam reads the bible, RULES, style guides, carry_over, log and `channels/<key>/story_registry.md`, writes, runs
   the Munshi script review and fixes it. Show the user Kalam's result (options or final script + Munshi verdict,
   length and cost estimate, open decisions).
3. Nothing paid starts here. Only the user's "approved" starts the production pipeline (RULES 14/15); then Kalam
   adds the story's row to the registry.
