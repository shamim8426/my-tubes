# Munshi RULES — Story-Channel

These are the hard rules. If a builder summary, a script or a file disagrees with them, the rule wins and the step is not PASS. Edit this file to add new rules; Munshi reads it fresh every time.
- A measured value outside a RULES limit is always FIX, never PASS, even if small. (in R1; after R2 see section 11)

## 1. Budget
- Prepaid Google Cloud budget: ₹500, auto-reload off. Current balance is whatever `cost_log.csv` says.
- Every paid call (Gemini image ≈ ₹3.24 each at 1K, Gemini TTS per line) must be in `cost_log.csv` with date, project, item, ₹.
- No paid call without the user's OK first. A fix that costs money is always ASK, never FIX.
- Flag it if a step cost more than 30% above its estimate (e.g. LONG_01 TTS: estimate ₹4.85, actual ₹6.63).

## 2. Story and characters (from `channel_bible.md`)
- Characters must match their approved sheets: face, clothes, colours, age look. Compare each scene image against the sheet with Read.
- Dadi (Kamla Devi) narrates. Every other character speaks their own lines in their own voice.
- Mitthu (parrot) has no hands: no hand gestures, holding things or pointing with hands.
- Dadi's home (in Gulmohar Mohalla): a kacha mud house with a tiled roof, BROWN wooden door, swept aangan, green fields behind, exactly like the channel banner (`channel_assets/_work/banner_art.png`). There is no green door.
- Setting: Dadi's home, the Golu–Mitthu opening/closing frame and all Dadi Jasoos cases are in Gulmohar Mohalla. The story Dadi narrates inside a moral-story video can be set in any village or town the approved script names (e.g. Rampur in LONG_01); check location consistency against that script. Village kitchens still use a mitti ka chulha, never a gas stove.
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
- Mystery (Dadi Jasoos) videos: the answer never goes in the title, description or thumbnail. It goes in the pinned comment 24 h after publishing.
- Made-for-kids and AI-disclosure values come from `munshi/channel_config.json`. Never guess them.
- Dadi Ki Kahaniyan is set to made_for_kids = false (family audience, decided by the user). So title, thumbnail, description and tags must speak to the whole family, not only to children: no "for kids" / "बच्चों के लिए" / nursery-style wording. Flag any such wording as FIX.

## 8. Publishing
- Default publish time: 7:00 PM IST.
- At least 2 days between two long videos on the same channel. Shorts can go on other days.
- Nothing goes Public or gets scheduled without the user's OK in that conversation.
- One upload per video. If `output/upload_result.json` exists, do not upload again.

## 9. Safety
- Never show or commit `.env`, `secrets/`, API keys or OAuth tokens.
- Never delete files; move them to `_to_delete/`.

## 10. Copyright (STRICT — any violation is FIX and blocks upload)
- Every external file used in any video (music, sound effect, font, image, footage, voice) must have a row in `munshi/assets_license.csv`: path, source_url, author, license, attribution_text, date_added. No row = not allowed.
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
- Every MINOR waived after R2 is written to munshi/carry_over.md (project, issue, suggested fix). Before the next video's build, the builder reads carry_over.md and fixes those causes in the pipeline, then marks them done.

These limits never weaken: copyright (section 10), channel ID check, secrets, and the full pre-upload check.
At the end of each review, add one line to munshi/log.md with the round (R1/R2), verdict and approximate time taken.
