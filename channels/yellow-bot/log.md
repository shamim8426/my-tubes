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
- 2026-10-31 007 Subagents UPLOADED private: https://youtu.be/XdC3f07GzXw (50.9 s, -15.0 LUFS, TP -1.4; free TTS 5 lines + paid 2 lines ~Rs0.1; ~35 min incl. setup). Fact-check PASS (review/factcheck.md). New: stage layer 'meter' (context bar).
- 2026-10-31 008 Skills UPLOADED private: https://youtu.be/yl0Cjc4E_1w (56.0 s, -14.9 LUFS, TP -1.7; TTS ~Rs1.2 paid after free quota; ~20 min). Fact-check PASS. New: paste-stack merge opener (box layers with tilt).
- 2026-10-31 009 MCP UPLOADED private: https://youtu.be/XjGT3YxVC3Q (64.8 s, -14.9 LUFS, TP -1.3; TTS ~Rs1.4 paid; ~25 min). Fact-check PASS. New: traveling copy-paste bubble then MCP badge in stage opener.
- 2026-10-31 010 Memory UPLOADED private: https://youtu.be/jQWCNgezK38 (55.3 s, -15.1 LUFS, TP -1.7; TTS ~Rs1.2 paid; ~20 min). Fact-check PASS. New: session-gap opener (CLAUDE.md doc slides between Session 1 and 2).
- 2026-10-31 011 Checkpointing UPLOADED private: https://youtu.be/z9LEeI0YNKo (49.0 s, -15.4 LUFS, TP -1.2; TTS ~Rs1.2 paid; ~20 min). Fact-check PASS. New: undo opener (doc messy -> two Esc key caps -> clean).

- 2026-10-31 012 Tools UPLOADED private: https://youtu.be/whEYixIMx0Q (51.2 s, -15.0 LUFS, TP -1.8; voice 1 free + 5 paid ~Rs1.2; ~45 min incl. new svgbot layer). Fact-check PASS (review/factcheck.md). First video in FORMAT v3: concept cards opener, docs screenshot proof, terminal example, nuance (compare), svgbot recap, CTA without quiz.

- 2026-10-31 thumbnails: scripts/make_thumb.py + templates/thumb_template.html (HTML -> PNG, 16:9 and 9:16); thumb.json + PNGs made for 006-012. API thumbnails.set returned 403 (channel not phone-verified); user to verify in Studio, then `youtube_upload.py --job <upload.json> --extras-only` per video (upload.json needs "thumbnail").
- 2026-11-01 nigraan-yellow agent added (.claude/agents/nigraan-yellow.md). Analytics token missing: user must run 'python tools/yt_analytics.py yellow-bot login' on PC. Videos 007-011 still private.
