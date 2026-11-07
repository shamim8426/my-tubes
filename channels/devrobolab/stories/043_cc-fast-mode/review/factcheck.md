# Fact check: Claude Code Short 043, Fast mode (2026-11-07)
Source (official): https://code.claude.com/docs/en/fast-mode (captured with our own Playwright, raw/article.png)

| Claim in the video | Official page says | Result |
|---|---|---|
| Fast mode makes Claude Code up to 2.5x faster | "making the model up to 2.5x faster at a higher cost per token" | PASS |
| Same Opus model, same quality, only faster | "Fast mode is not a different model... identical quality and capabilities with faster responses" | PASS |
| Type /fast, press Space to toggle, then Enter | "Run /fast, press Space to toggle on or off, then press Enter to confirm" | PASS |
| Screen shows Fast mode ON and a small icon near the prompt | "confirmation message: 'Fast mode ON'"; "A small ↯ icon appears next to the prompt" | PASS (icon drawn as a bolt, labelled Illustration) |
| Works only on Opus | "supported on Opus 5.5, Opus 5, and Opus 4.8. It is not available on Sonnet, Haiku, or other models." | PASS |
| Every token costs more | "up to 2.5x faster at a higher cost per token" (pricing $8/$40 Opus 5.5; not said in the video) | PASS |
| On subscription plans it uses usage credits | "available via usage credits only and not included in the subscription rate limits" (shown as the one doc note with live marker) | PASS |
| Turn it on at the start of a session; turn it off with /fast when cost matters | "enable fast mode at the start of a session"; "toggle it off when cost matters more than latency" | PASS |

Not claimed: prices, Opus version numbers, deprecation dates (page text may change). The terminal window is our own illustration (labelled), not a recording.
