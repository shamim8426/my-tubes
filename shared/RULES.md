# Munshi RULES — Story-Channel

Shared rules for every channel. Munshi reads this file first, then `channels/<key>/RULES.md`.
- Channel RULES can be stricter than shared RULES, never looser. Copyright, channel ID, secrets and upload safety can never be relaxed by a channel.


These are the hard rules. If a builder summary, a script or a file disagrees with them, the rule wins and the step is not PASS. Edit this file to add new rules; Munshi reads it fresh every time.
- A measured value outside a RULES limit is always FIX, never PASS, even if small. (in R1; after R2 see section 11)

## 1. Budget
- Prepaid Google Cloud budget: ₹500, auto-reload off. Current balance is whatever `cost_log.csv` says.
- Every paid call (Gemini image ≈ ₹3.24 each at 1K, Gemini TTS per line) must be in `cost_log.csv` with date, project, item, ₹.
- No paid call without the user's OK first. A fix that costs money is always ASK, never FIX.
- Flag it if a step cost more than 30% above its estimate (e.g. LONG_01 TTS: estimate ₹4.85, actual ₹6.63).

## 2. Story and characters (from `channel_bible.md`)
- Characters must match their approved sheets: face, clothes, colours, age look. Compare each scene image against the sheet with Read.
- The action in each image must match what the line says at that moment (who is holding what, who is talking).

## 3. Audio
- Final loudness: -14 LUFS integrated (±1), true peak ≤ -1.0 dBFS.
- Music sits under the voice: 12–14 dB below for Shorts, up to ~18–20 dB for narration-heavy long videos. If it is quieter than 20 dB under, flag it.
- Music level is measured one way only: integrated LUFS of the voice-only stem vs the music-only stem over the same speech sections. Builder and Munshi both use this method.
- Mood changes get a crossfade (≥1 s). No sudden music cuts under dialogue.
- No leaked background audio, clicks, or a line cut off mid-word.

## 4. Captions
- One `.srt` per video, Hindi, UTF-8.
- Each caption must appear while that line is being spoken (±0.3 s), over the right character's shot.
- Lines whose timing was estimated rather than taken from Whisper must be listed in the report.

## 5. Video
- Long video: 1920×1080, 30 fps, H.264, 16:9. Short: 1080×1920, ≤60 s, 9:16.
- Target length: the duration the user approved at preview. Before preview, the script estimate is only a guide. Final must be within ±10% of the approved preview length; outside that is ASK.
- Preview builds (960×540) are only for review. They are never uploaded.

## 6. Thumbnail
- 1280×720, JPG or PNG, ≤ 2 MB.
- Hindi text is rendered by libass/FFmpeg (HarfBuzz shaping), never drawn by the AI. Zoom in and check matras and joined letters (ड़, दु, क्ष, etc.).
- Text readable on a phone: letter height ≥ ~12% of frame height, high contrast, max ~4 words.
- Thumbnail text must not repeat the title word for word.
- No spoilers: no ending, no twist, no mystery answer.
- Bottom-right corner (~15% × 12%) has nothing important, because YouTube puts the duration there.

## 7. Metadata
- Title ≤ 100 characters, no `<` or `>`. Description ≤ 5000 characters.
- Tags total ≤ 500 characters. 3–5 hashtags in the description (the first 3 show above the title; more than 15 and YouTube ignores all of them).
- Every CC BY music track used (e.g. Incompetech / Kevin MacLeod) is credited in the description exactly as its licence asks.
- Made-for-kids and AI-disclosure values come from `channels/<key>/channel.json`. Never guess them.

## 8. Publishing
- Fixed publish times: long video at 19:00 IST, its Short at 21:00 IST the same day.
  - Long upload finished before 18:45 IST -> long publishes 19:00 the same day; otherwise 19:00 the next day.
  - Short upload finished before 20:45 IST -> Short publishes 21:00 the same day as its long; otherwise both move to the next day.
  - A Short not made from a long (e.g. Dadi Jasoos case) also publishes at 21:00.
- Per day per channel: at most one long (19:00) and one Short (21:00).
- Planned frequency: long videos 2-3 per week, Shorts daily (from stories already made, ₹0).
- Nothing goes Public or gets scheduled without the user's OK in that conversation.
- One upload per video. If `output/upload_result.json` exists, do not upload again.
- Short -> Long link (MANDATORY): every Short made from a long video must (a) have the long video's URL in its description with a short CTA line, (b) get an automatic first comment "पूरी कहानी यहाँ देखें 👉 <long URL>" posted right after it becomes public, and (c) the user sets in Studio: Related video = the long video, and pins that comment. The YouTube API cannot set Related video or pin comments, so (c) stays manual; Munshi shows this checklist after every Short upload and asks about it at the start of the next session until the user confirms.

## 9. Safety
- Never show or commit `.env`, `secrets/`, API keys or OAuth tokens.
- Never delete files; move them to `_to_delete/`.
- Paid source files (story images/, audio/, characters/) are read-only for every build. Builds write only to their own _work/ and output/ folders. After every build Munshi checks that no paid source file changed (git status / hash). Any change is a BLOCKER.

## 10. Copyright (STRICT — any violation is FIX and blocks upload)
- Every external file used in any video (music, sound effect, font, image, footage, voice) must have a row in `shared/assets_license.csv`: path, source_url, author, license, attribution_text, date_added. No row = not allowed.
- Allowed licences only: CC0; CC BY 4.0 (with exact credit in the description); SIL OFL (fonts); YouTube Audio Library tracks (follow their attribution note); our own Gemini-generated images/voices; our own recordings.
- Never allowed: CC BY-NC (non-commercial, conflicts with monetization), CC BY-ND (we edit/mix), CC BY-SA, "free for personal use", Freesound "Sampling+", unknown source, anything ripped from YouTube/Spotify/Instagram/films/TV, Bollywood or any commercial song (even hummed or sung by TTS), Google/Pinterest images.
- Freesound: licence is per sound. Check each file's own licence page; only CC0 or CC BY 4.0.
- Content: no real brand logos, no film/TV/cartoon characters (Chhota Bheem, Motu Patlu, Disney, etc.), no celebrity likeness, no copied song lyrics, no copied text from modern books. Old folk tales (Panchatantra, Jataka, Akbar-Birbal) are public domain, but we always write our own version, never copy a modern retelling.
- Image prompts never name a studio, franchise or living artist ("Pixar style", "Ghibli style", etc.).
- Before upload, Munshi checks: every audio/image/font file in the final build is in the register, every CC BY item is credited in the description exactly as its licence asks, and no source audio from outside our pipeline is in the mix.
- After upload: if YouTube Studio shows any copyright claim or strike, stop all new uploads and tell the user. CC music sometimes gets false Content ID claims; dispute only with the licence proof from the register, after the user agrees.

## 11. Review limits and severity
Every problem Munshi reports is marked BLOCKER or MINOR.

BLOCKER (never waived, in any round):
- Copyright (section 10), wrong channel, any secret exposed.
- Wrong character on screen for a line, wrong voice for a character, a line missing or cut off.
- Caption more than 1 s away from its line, or caption text not matching what is spoken.
- Loudness outside -14 LUFS ±1, true peak above -1.0 dBFS, audible clipping or leaked outside audio.
- Wrong resolution/codec, or a preview file used as final.
- Thumbnail: broken Hindi matras, spoiler, unreadable text, important thing in the bottom-right corner.
- Metadata: title over 100 chars, more than 15 hashtags, missing CC BY credit, "for kids" wording (title, thumbnail, description or tags), mystery answer revealed.
- Length outside ±10% of the approved preview length.
- Story problem: moral missing or a scene that contradicts the script.

MINOR (everything else that breaks a RULES limit only slightly), e.g.: caption off by 0.3–1 s, caption shorter than 0.4 s, music level within 3 dB of target, thumbnail text slightly under the size rule, small silent gaps, missing colour tags, tiny cosmetic issues.
Taste points (pacing feel, colour choice, music phrase) are "Note" only and never count as problems.

Rounds:
- Round 1 (R1): full review for that stage; BLOCKER and MINOR both come back as FIX (free) or ASK (paid).
- Round 2 (R2): re-check only what changed and what failed in R1.
- After R2: if any BLOCKER remains → ASK the user, stop. If only MINOR remain → verdict "PASS-WITH-NOTES": the stage is passed and the pipeline moves on to the next step (including upload when the user has approved it). No third round.
- Every MINOR waived after R2 is written to channels/<key>/carry_over.md (project, issue, suggested fix). Before the next video's build, the builder reads carry_over.md and fixes those causes in the pipeline, then marks them done.

These limits never weaken: copyright (section 10), channel ID check, secrets, and the full pre-upload check.
At the end of each review, add one line to channels/<key>/log.md with the round (R1/R2), verdict and approximate time taken.

## 12. Originality (YouTube "inauthentic content" policy)
- Every new story must differ clearly from all previous stories of the channel in at least 3 of: moral, main conflict/plot shape, setting, lead characters, genre/tone (comedy, mystery, emotional, adventure), ending type.
- At script stage Munshi compares the new script with every previous story.md in the channel and lists the closest match and what is different. If fewer than 3 differ -> BLOCKER (ASK the user).
- Titles and thumbnails must not follow one fixed template word-for-word across videos.
- No two videos may reuse the same narration audio. Shorts cut from their own long video are allowed.
- Every 5th long video Munshi writes a short "channel variety" note in log.md: genres used, morals used, what to try next.
