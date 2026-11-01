---
name: find-skills
description: Find and add skills for the user's ideas. Use when the user says "skill find karo", "koi skill hai kya", "find skills", "mere idea ke liye skill", or describes a task and wants a ready-made skill (or plugin) for it. Searches the user's claude.ai skill catalog and plugin catalog and shows an add/install card.
---

# Find skills for an idea

Talk to the user in Hinglish. First say in one line: ~3 min, Rs0.

1. Turn the user's idea into 3-6 short English keywords (task, file type, domain; e.g. "video", "youtube", "seo", "pptx").
2. Load the tools if they are deferred: `ToolSearch` with `select:SearchSkills,ListSkills` (and `SearchPlugins` / `SuggestPluginInstall` for plugins).
3. `SearchSkills` with the keywords. Also `ListSkills` with the same keywords to see what the user already has enabled.
4. If results fit: call `SuggestSkills` (trigger `user_asked`) so the user gets the add card. Do not describe the skills again in text; give one line each only if there is no card.
5. Also run `SearchPlugins` with the same keywords; if a plugin fits, show it with `SuggestPluginInstall`.
6. Nothing found: say so plainly, then offer to build a custom skill (`skill-creator`) or a project skill in `.claude/skills/<name>/SKILL.md`.
7. Never add or enable anything for the user; the card/install step is the user's click. No secrets, no paid calls.
