# Munshi log

## Earlier work (moved from channels/_new_claude_explainer, 2026-10-31)
﻿- 2026-10-31 Short 001 (CLAUDE.md) built: 53.4 s, 1080x1920, -14.9 LUFS, TP -1.5 dBFS; voice Gemini TTS ~Rs1; renderer scripts/kinetic_short.py; not uploaded (no channel yet), Munshi review not run.
- 2026-10-31 Short 002 (5 Claude Code features) built: 69.7 s, 1080x1920, -15.1 LUFS, TP -0.9; 6 HD images free (Cloudflare Rs0), TTS ~Rs1; renderer scripts/kinetic_short.py v1 (gradient + image cards + Poppins); not uploaded, Munshi not run; voice alternates in audio/alt/.
- 2026-10-31 decks built (not rendered): 003 Subagents (1/7 voice lines done, free key), 004 Skills, 005 MCP. Renderer: scripts/build_deck.py + templates/deck_template.html (white, black+yellow, 9 scene types). BLOCKED: free Gemini TTS quota used up (429); paid key not used (user: free only).
- 2026-10-31 003 Subagents (60.6 s), 004 Skills (50.1 s), 005 MCP (55.3 s) RENDERED: output/short.mp4 each, -15 LUFS, TP -0.9; paid TTS key used (user OK 'option 3'); not reviewed by Munshi, not uploaded (channel not created).
- 2026-10-31 006 Hooks + music Funkorama (Kevin MacLeod CC BY 4.0, rel 12 LU); 004 Skills music version short_music.mp4 (remux). Scripts: music_preview.py, remux_music.py. Credit line required in description.
- 2026-10-31 multi-robot support: mascot/team.png (4 robots in one image, free Cloudflare) + 'robots' with crop in deck_template/build_deck; demo stills only (deck_robots_demo.json, --deck flag). Crops need tightening before real use.
- 2026-10-31 stage scene type (keyframed picture-story layers) added; 006 Hooks opener rebuilt as robot demo (edit -> PostToolUse hook -> Hook helper -> file cleaned); voice s_00 regenerated (free key, Rs0); total 63.5 s. STYLE_GUIDE v2 written (channel theme + 'every video adds one enhancement' rule).

- 2026-10-31 006 Hooks UPLOADED private: https://youtu.be/GpVCvYrwqd4 (63.5 s, yuv420p after range fix in html_video.py; channel.json short_max_seconds 75; contains_synthetic_media true; not Munshi-reviewed, user asked direct upload). Studio: user makes it public.
