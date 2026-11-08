# Review: Claude Code 03 (.claude directory) long, 2026-11-07 night
Checked: frame every 3 s of the render (and of the finished mp4), exact frames at action words (ls .claude typing, settings.json lines, npm test, choose-row file chips), automatic low-content scan every 0.25 s, loudness, length, facts vs facts.md.

## Mistakes found and fixed BEFORE the full render (preview frames, same code)
1. 0-8 s hook, 130-210 s: cards ran off the screen edge (zoom K too big for photo + terminal pair). Fixed with K 1.0-1.1 and bigger cards.
2. Chapter badge label pill overlapped the number square for short labels ("3 TERMINAL DEMO"). Fixed: pill placed by its width.
3. Purge terminal prompt showed "$ $". Fixed ("~ $").
4. CTA scene: Comment / DIRECTORY / Follow pills and the Watch next cards touched. Fixed spacing (K 1.0).
5. Whisper base gave 6 words for the terminal demo scene: all action times collapsed. Fixed with medium model anchors (patch_wt.py). Learning written (tools/learn.py).
6. two_a (42.6-60.9 s): no cards for 5 s, only a placeholder pill. Fixed: both file cards enter at the start.
7. data_b: 30-day card too low (near caption). Fixed layout.
## Mistake found AFTER the full render, fixed by range splice
8. 135.0-145.2 s (mine_b): "managed settings win" pill crowded the caption. Moved up; re-rendered only 135.0-145.2 and spliced (same 6366 frames, 212.2 s). fixed.
## Remaining notes (not mistakes)
- ~0.2 s near-empty frames at two hard cuts (42.5 s, 60.75 s window fade-in), under the 0.5 s rule.
- Dark terminal windows trigger the low-content scan; they are not blank.
## Numbers
Length 3:32.2 (6366 frames), loudness -14.7 LUFS, true peak -1.4 dBFS. Words about 520. Facts: every claim matches review/facts.md (official page only). settings.json example is labelled "example"; terminal screens labelled "Illustration, not a recording".
Style variants: dark neon, highlight=MINT, mono terminal font, photo cards (4 free Cloudflare), terminal demo take, choose-file table, 2x2 extras grid, recap, end card; no robot. cta: "Kaam ki lagi? Dost ko bhejo, comment me DIRECTORY likho."
