# 064 self-review (Claude Code me slash command kaise banayein)

## Round 0: pre-render frames (review/sheet_*.png, fix_1.png)
| # | Time | Problem | Fix |
|---|---|---|---|
| 1 | 0.0-4.5 s (hook) | lower half (y 1000-1400) empty under the terminal | drawn "Har baar type" long-prompt card, struck out on "उसे" | fixed |
| 2 | 7.3-8.5 s (hook) | terminal re-typed the command = blank terminal body ~1 s | terminal stays full (result from frame 0), orange pulse ring on "slash fix issue" instead | fixed |
| 3 | 9.6-19.5 s (steps) | official crop on top, folder tree mid, lower 1100-1400 empty until "Folder का नाम" | tree on top + banner, chips mid, official crop at the bottom from scene start | fixed |
| 4 | 21.1-22.6 s (file) | empty SKILL.md editor before "तीन dash" | placeholder line "# khaali file ... upar se likhiye" + SKILL.md chip | fixed |
| 5 | 32.5-35.4 s (file) | lower half empty until the result card | result card on "एक सौ तेईस" (tok 36) + SKILL.md body line card from scene part start | fixed |
| 6 | 38.3-43 s (note) | lower half empty until /reload-skills | terminal "claude (session chal raha)" from scene start, "+ .claude/skills/ NAYA" chip on "नया बना", reload typed on "slash reload" | fixed |
| 7 | 45.3-48 s (note) | location table crop unreadable (whole 3-column table scaled to 960 px) | own Playwright element screenshots of the Personal + Project rows, empty column gaps removed | fixed |
| 8 | 45.3 s (note) | "Project" row crop was the wrong table row (/run-skill-generator, text match "project") | match the first cell exactly (td:first-child) | fixed |
| 9 | 49-51 s (note) | lower half sparse | "commands/deploy.md = /deploy" (docs naming table) + "NAYA KAAM: skills/" chips | fixed |

## Round 1: full render (output/short.mp4)
- Length 56.93 s (50-60 OK), 1080x1920, 159 words; beginner check: each step defined (folder, file, description, $ARGUMENTS shown with 123 example) - OK.
- Contact sheets every 3 s (final_sheet_1..3): no blank frame > 0.5 s, nothing cut/overlapping, crops readable (table rows re-captured).
- Action frames (act_sheet_1): 6.6 s pulse on "slash fix issue"; 17.0 s SKILL.md in tree on "SKILL dot md"; 29.4 s $ARGUMENTS highlighted; 33.9 s result card on "एक सौ तेईस"; 43.6 s /reload-skills typing on "slash reload"; 46.6 s ~/.claude path on "home"; 49.5 s commands/ chips on "पुरानी commands"; 56.2 s + FOLLOW on "follow" - all OK.
- Facts: every claim in facts.md F1-F10 (official docs), nothing extra.
- Loudness: -15.5 LUFS (out of -14 +-1) -> two-pass loudnorm audio remux (video copied): -14.8 LUFS, peak -1.4 dBFS. fixed.
- Captions Roman Hinglish (no Devanagari on screen, no matra risk).
- Verdict: PASS.
