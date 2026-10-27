---
name: trend-research
description: Public-metadata trend research for Hindi kids/moral/family story channels (top videos of the last 6-12 months + the next festival). Used by Kalam before every set of story options. Writes channels/<key>/research/trends_<YYYY-MM-DD>.md. Free, no downloads (study downloads only per RULES 12c).
---

# Trend research (Kalam step a)

## Freshness
- Look for the newest `channels/<key>/research/trends_*.md`.
  - **< 7 days old:** no full research. Add only 5–10 new top videos (and the next festival if missing), update the
    patterns, save as a new dated file (copy + update).
  - **≥ 7 days old or none:** full research below.

## Data (public metadata only)
- `WebSearch` to find Hindi kids / moral / family / animated story channels and their most viewed videos of the
  last 6–12 months, plus top videos about the next festival from `channels/<key>/festival_calendar.md`.
- `tools/yt-dlp.exe --flat-playlist --skip-download -J <channel>/videos` (and `--skip-download -j <video>` for
  upload date) — title, views, duration, upload date, channel. ~30 videos.
- **Never download** video, audio or thumbnails for trend research (the only exception is a user-requested study, shared/RULES.md 12c, done separately); never keep frames or screenshots in the repo. A thumbnail may only be
  looked at once by URL to understand colour/emotion — never stored, never given to Gemini as a reference. If a
  tool auto-saves a copy outside the repo, delete it after looking.
- If YouTube blocks or rate-limits: do not bypass; work with what was found and say so in the file.
- Keep raw JSON in the session scratchpad, not in the repo.

## Output: `channels/<key>/research/trends_<YYYY-MM-DD>.md`
1. Date, how many videos/channels, data limits.
2. **Patterns** — everything RULES 12b ALLOWS (style, pacing, structure, topics, moods, title/thumbnail shape); never their script, plot+twist, characters, exact titles or visuals:
   - topics (top 5), hook types, title shape/emotion (length, question vs exclamation, emoji use — described, not
     quoted), thumbnail colour/emotion, length vs views, what worked in Shorts.
   - what this means for Kissago (our characters, Gulmohar Mohalla, Kissago Painted).
3. **Reference list (internal only):** title + link of each video looked at — Munshi uses it to check that our plots,
   twists and titles are not too close. This list never goes into any title, description, tag, comment or prompt.
4. Run `python tools/name_guard.py <file>` on the **patterns part**: no studio/film/anime/artist names there
   (RULES 12a). Channel names and titles appear only in the reference list.
