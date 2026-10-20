# Munshi review: STYLE_LEARNINGS.md (2026-10-20, R1)

VERDICT: FIX (MINOR only, all free text edits; no BLOCKER, no STOP)

Checked: read the doc fully; tools/name_guard.py = OK; RULES 3, 6, 10, 12, 12a, 13, 15 read fresh; STYLE_PAINTED.md has no change vs HEAD (style block still ends at "warm golden natural light, lush ..."); tools/parallax.py AMP = 0.035, so 0.0175 = existing half-motion guard value; git status: only STYLE_LEARNINGS.md new; no new jpg/webp/mp4/gif from the research in the repo (new media today are only our own story 004 / painted test / brand files); scratchpad holds yt-dlp metadata JSON only (outside repo, no media).

1. Names: PASS. No channel name, URL, handle, studio, film, anime or artist name; source written as "Reference: ek cozy-ambience channel (research notes)".
2. No copy: PASS. Principles are general and rewritten for Gulmohar Mohalla; no single video scene, title or thumbnail described.
3. Originality: PASS. Own story, Dadi's voice, own cast kept; cozy ideas use only our characters and places; nothing near the 12a block list.
4. Proposals: not applied (PASS); RULES fit needs these text fixes:
   - M1 "opening mood" placement breaks RULES 13 (first spoken line <= 1.0 s, intro before story <= 10 s, question set in first 30 s). Write: never at the start; only at a mid pause or after the twist, and not in the last 20 s (end screen).
   - M2 Shorts not covered: write "cozy segments only in long videos" (Short max 40 s, first word <= 0.5 s).
   - M3 Freesound ambience: add "each sound checked on its own licence page, CC0 / CC BY 4.0 only, row in shared/assets_license.csv" (RULES 10). The extra 4-6 dB music dip only where there is no voice; speech sections keep RULES 3 levels.
   - M4 "1 in 3 thumbnails with very small or no text" conflicts with RULES 6 (text letter height >= ~12%) and 12a "our own text". Keep text per RULES 6, or the user changes the rule first.
   - M5 "glowing lamplight" in the verbatim style block goes on every prompt (also daylight scenes). Better as a night/rain line in section 3 (Light), not in section 1.
   - M6 Fingerprint: drop "~10.8 M", "of 32 videos", "within ~2 weeks" and the quoted description phrases ("ASMR", "put on headphones"); keep rounded, general findings. Do not use ASMR/headphones keywords in our metadata.
   - M7 "Monsoon week": each story must still differ in 3 of 6 points (RULES 12); rain alone is a shared setting.
5. Third-party media: PASS (none in repo).

Note outside this doc (user decides): the tracked file .specstory/history/2026-10-17_08-25-27Z-pasted-content-id-aeaa.md (modified, not yet synced) holds the reference channel's handle/URL, video IDs and verbatim titles/description from this research; name_guard already flags this file at HEAD too. It goes to GitHub with the next sync. Suggest: git-ignore .specstory/ (or leave it out of sync) - user's call, no deletion.

# R2 (2026-10-20)

VERDICT: PASS-WITH-NOTES (no BLOCKER, no STOP)

Re-read the whole doc; name_guard OK; STYLE_PAINTED.md still unchanged vs HEAD; git status: no new media.
- M1+M2 fixed: placement line = long only, never in Shorts, never at start (1.0 s / 10 s / 30 s), never in last 20 s, only mid pause or after the twist.
- M3 fixed: extra music drop only in the wordless part, RULES 3 level wherever someone speaks; Freesound per-sound licence, CC0 / CC BY 4.0, register row.
- M4 fixed: thumbnails keep our own text per RULES 6 (>= ~12%); only stronger warm/cool contrast proposed.
- M5 fixed: "glowing lamplight" moved to section 3 Night/Rain light lines; style block stays verbatim.
- M6 fixed: 10.8 M, 32/15, 2-week window, "ASMR" and headphones phrases gone; note added not to borrow their listening keywords.
- M7 fixed: monsoon-week stories must differ in >= 3 RULES 12 points.
Note (MINOR, carry only): the table still says "all 15" and "9 of the top 10"; rounding these to "the top videos" / "most of the top videos" would remove the last count. Proposals 1 and 3 both edit section 3 (Light); merge them when applying.
Still open for the user (outside this doc): .specstory/ transcript with the reference handle/URL goes to GitHub on next sync.
