# Munshi RULES — Story-Channel

Shared rules for every channel. Munshi reads this file first, then `channels/<key>/RULES.md`.
- Channel RULES can be stricter than shared RULES, never looser. Copyright, channel ID, secrets and upload safety can never be relaxed by a channel.


These are the hard rules. If a builder summary, a script or a file disagrees with them, the rule wins and the step is not PASS. Edit this file to add new rules; Munshi reads it fresh every time.
- A measured value outside a RULES limit is always FIX, never PASS, even if small. (in R1; after R2 see section 11)

## 1. Budget
- Prepaid Google Cloud budget: ₹500, auto-reload off. Current balance is whatever `cost_log.csv` says.
- Every paid call (Gemini image ≈ ₹3.24 each at 1K, Gemini TTS per line) must be in `cost_log.csv` with date, project, item, ₹.
- Outside auto mode: no paid call without the user's OK first; a fix that costs money is ASK, never FIX.
- In auto mode (after script approval, sections 14/15): NO paid call needs the user's OK. Stop and ask only in these 3 cases:
  1. Google balance below ₹50 (or the API says credits are depleted) — tell the user to recharge.
  2. A copyright doubt.
  3. A channel ID mismatch.
  Everything else (budget, failed regenerations, BLOCKERs after R2) is handled without asking, as in section 15, and logged.
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
- From story 004 (section 15): no preview build; long video max 4:00 (target 3:40–4:00), Short max 40 s (target 35–40 s); the script is written to that length from measured TTS speed. These limits replace the preview-length rule above.

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
- Publish timing (user rule 2026-10-21; replaces the old fixed "long 19:00 / Short 21:00" slots). Decided right AFTER the upload finishes, from the real IST clock (Asia/Kolkata); `tools/youtube_upload.py` with `"publish_at": "auto"` does it (`tools/publish_slot.py`):
  - Upload finished 19:00–23:59 IST -> the long goes public NOW; its Short 60 min after the long (if that is after 23:59, the Short also goes public now).
  - Upload finished 00:00–18:59 IST -> the long is scheduled 19:00 the SAME day; its Short 20:00 the same day.
  - One long per day: a day that already has a long (public or scheduled; checked in every upload_result.json and via the YouTube API) gets no second long -> the next free day 19:00, its Short 20:00.
  - A Short uploaded after its time has passed goes public now. A stand-alone Short (e.g. Dadi Jasoos case) follows the same clock at 20:00.
  - Optional `earliest_date` in upload.json (e.g. a festival story): the long is not placed before that date; the rules above still apply from that date.
- API audit not passed (channel.json `api_audited: false`, the current state): videos upload as private. Right after the upload the user gets one clear STUDIO ACTION message: video ID, title and the exact action ("abhi PUBLIC karo" or "<date> 19:00 par SCHEDULE karo"), a separate line for the Short, the Short's Related video (long ID) and when the first comment arrives to pin. When the user says "ho gaya", log it. Once `api_audited` is true, the uploader sets public / publishAt itself and the message is only a report.
- First comment: a scheduled task 5 min after the real publish time (public now -> 5 min after the upload); it retries for up to 3 h while the video is still private.
- Planned frequency: long videos 2-3 per week, Shorts daily (from stories already made, ₹0).
- Nothing goes Public or gets scheduled without the user's OK, except in auto mode (section 14): there the script approval covers the upload and its publish timing above; a scheduled video keeps the "rok do" veto window before its time (a video that goes public now has none).
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
- Content: no real brand logos, no film/TV/cartoon characters (Indian TV cartoon heroes, big-studio characters, etc.), no celebrity likeness, no copied song lyrics, no copied text from modern books. Old folk tales (Panchatantra, Jataka, Akbar-Birbal) are public domain, but we always write our own version, never copy a modern retelling.
- Image prompts never name a studio, franchise or living artist (no "<studio> style" or "in the style of ..."); see section 12a.
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
- Length outside ±10% of the approved preview length (stories up to 003). From story 004: long video over 4:00 or Short over 40 s (section 15).
- Story problem: moral missing or a scene that contradicts the script.

MINOR (everything else that breaks a RULES limit only slightly), e.g.: caption off by 0.3–1 s, caption shorter than 0.4 s, music level within 3 dB of target, thumbnail text slightly under the size rule, small silent gaps, missing colour tags, tiny cosmetic issues.
Taste points (pacing feel, colour choice, music phrase) are "Note" only and never count as problems.

Rounds:
- Round 1 (R1): full review for that stage; BLOCKER and MINOR both come back as FIX (free) or ASK (paid).
- Round 2 (R2): re-check only what changed and what failed in R1.
- After R2: if any BLOCKER remains → ASK the user, stop (outside auto mode; in auto mode see section 15: fix it yourself, never ask). If only MINOR remain → verdict "PASS-WITH-NOTES": the stage is passed and the pipeline moves on to the next step (including upload when the user has approved it). No third round.
- From story 004 (section 15): stage reviews (script timing, images, audio) are R1 + R2; after R2 MINOR issues are only logged to carry_over.md (nothing regenerated) and the flow moves on. The final video gets ONE check (R1 only): no BLOCKER -> upload. A BLOCKER may get max 1 paid regeneration per image.
- Every MINOR waived after R2 is written to channels/<key>/carry_over.md (project, issue, suggested fix). Before the next video's build, the builder reads carry_over.md and fixes those causes in the pipeline, then marks them done.

These limits never weaken: copyright (section 10), channel ID check, secrets, and the full pre-upload check.
At the end of each review, add one line to channels/<key>/log.md with the round (R1/R2), verdict and approximate time taken.

## 12. Originality (YouTube "inauthentic content" policy)
- Every new story must differ clearly from all previous stories of the channel in at least 3 of: moral, main conflict/plot shape, setting, lead characters, genre/tone (comedy, mystery, emotional, adventure), ending type.
- At script stage Munshi compares the new script with every previous story.md in the channel and lists the closest match and what is different. If fewer than 3 differ -> BLOCKER (ASK the user).
- Titles and thumbnails must not follow one fixed template word-for-word across videos.
- The channel name suffix (`title_suffix` in channels/<key>/channel.json, e.g. "| किस्सागो") may stay the same in every title — it is branding. The rest of the title (story name, hook, extra keywords) must vary; do not repeat the same keyword block (like "| Hindi Moral Story | Hindi Kahani") in every video. Rotate keywords or put them in tags/description instead.
- No two videos may reuse the same narration audio. Shorts cut from their own long video are allowed.
- Every 5th long video Munshi writes a short "channel variety" note in log.md: genres used, morals used, what to try next.

### 12b. Nayapan (freshness) — strict, for every story option and script
1. No folk tale / old story retold: no known old story in a new dress, even with new names or characters (Panchatantra, Jataka, Hitopadesh, Akbar-Birbal, Tenali Raman, Vikram-Betaal, Aesop, foreign fairy tales; the thirsty crow, hare and tortoise, the golden egg, the greedy dog, the lion and the mouse, the honest woodcutter, the magic lamp, "the wolf is coming" and the like). A moral may be shared, but the plot, the order of events and the twist must be new.
2. Worn tropes only with a truly new twist, and the option must say so: cruel step-family, poor vs rich direct revenge, the greedy one simply punished, a magic object fixes everything, "it was a dream" ending, a god/fairy arrives to solve it, the plain reversal "the thief was a helper". Endings always come from the characters' understanding, effort or friendship — never from magic.
3. An option with nayapan below 7/10 is never offered. Kalam asks itself: "Would a child say 'I have heard this before'?" — if yes, drop it.
4. From trends only the topic, mood or hook type may be taken — never a plot, twist, character, specific dialogue or title.
Munshi: a plot/twist/title too close to a known story or to a video in the latest trends reference list = MAJOR, even with different names.

### 12a. Visual style, copyright and brand (Kissago Painted and any channel style)
- No studio, film, anime or artist name ANYWHERE: image prompts, file/folder names, titles, descriptions, tags, hashtags, thumbnail text, comments, playlists, community posts. Internally the style is only called by its own name (e.g. "Kissago Painted", `channels/<key>/brand/STYLE_PAINTED.md`). A name found in metadata = upload BLOCK.
- Nothing may look like an existing anime/film character, creature, vehicle, building or famous scene. Block list (kept here, never in prompts): a huge furry magical forest creature; small black soot-like creatures; a girl flying on a broom; a masked shadow spirit; a magic cat-shaped bus or any living bus; a bus stop in the rain with an umbrella and a big creature; floating castles or walking castles; giant robots/mecha; famous mascots or cartoon characters of any brand.
- Only our own characters (Dadi, Golu, Mitthu and the channel bible's characters) and an Indian setting: clothes, faces, homes all Indian.
- After every image Munshi asks: "Kya ye kisi jaane-maane kirdaar ya scene ki nakal lagti hai?" If yes -> MAJOR (BLOCKER): change the prompt and regenerate once; if it still looks like one, drop that shot (crop/zoom another image). An image that looks like a famous character is never used, even if it was already paid for.
- Thumbnails use the channel's own style and our own text.
- YouTube originality: story, script, voices and characters stay our own; the visual style is only a look.
- Sensitive subjects: never mock any religion, caste, politics, region, skin colour/looks or disability; festivals and rituals are shown with respect and correct facts (no guesses — check `channels/<key>/festival_calendar.md` and reliable sources). Boys and girls get equal and good roles (Tara is known for her brains and courage). No real person, brand or real place name (Gulmohar Mohalla and our own invented places only). Any breach = BLOCKER.
- Children (Golu, Tara, Tinku and any child): always age-appropriate, innocent and family-friendly in looks, poses and words; a girl is described by her nature, not her looks. Never any romance/crush angle between children (stories, thumbnails, titles, descriptions, comments). A child may be teased (e.g. Tinku's thinness) but the story never ends by putting them down — it becomes their strength or friends stand by them. Any breach = BLOCKER.

### 12c. Study download (user rule 2026-10-22)
- WHEN: only when the user gives a link and says "isse seekho". Never on our own initiative.
- HOW: `tools/yt-dlp.exe`, no login and no cookies (the user's YouTube account is never connected), max 480p, only into
  the git-ignored `study/` folder at the project root (never any other repo folder, never synced). Learn from: FFmpeg
  frames at every shot change + every 2 s, and Whisper used ONLY for numbers (each line's length, speaking rate, where
  the silences are). No dialogue/script text is ever saved.
- AFTER: video, frames and audio are deleted right after the analysis (max 24 h). Log in `channels/<key>/log.md`: when,
  which link, why, deleted. Add the link + title (no channel name) to `channels/<key>/research/study_log.md`.
- WHAT we learn (general methods only): hook structure, shot length, camera moves, text/graphics style and placement,
  transitions, colour and light, when music/SFX change, voice pace, the CTA. Result goes to
  `channels/<key>/brand/STYLE_LEARNINGS.md` with "how we build it with our tools"; nothing is applied before the user agrees.
- STRICT BAN (never in our videos): any frame, clip, image, audio, music, SFX or voice from the download; their script,
  dialogue, plot, order of events, twist, characters, title or thumbnail; their channel name anywhere (metadata, prompts,
  files); study frames are never given to Gemini or any image model as a reference. A breach = BLOCKER.
- Munshi: every new script, thumbnail and Short is compared with the videos in study_log.md; a plot, dialogue, title or
  visual too close = MAJOR.

## 13. Audience & algorithm (CTR, retention, session)
Long videos:
- Hook: the first spoken line must start within 1.0 s. The first 30 s must set up the story's main question or conflict. Any frame/intro before the story itself (Dadi-Golu opening) is max 10 s.
- Promise kept: whatever the title and thumbnail promise (e.g. the magic cauldron) must appear on screen within the first 60 s. A title/thumbnail that promises something the video does not show is a BLOCKER (misleading).
- Visual change: no single shot stays without a cut or new camera move for more than 8 s.
- End: the last 20 s carry no essential visuals or captions in the end-screen area, so end-screen elements can sit there. The last spoken line asks viewers one specific question about the story (for comments), not a generic "like and subscribe".
Shorts:
- No reveal (user rule 2026-10-21): a Short cut from a long video stops BEFORE the discovery/answer — it never shows or names what was found, who did it, or the twist (e.g. no box contents, no culprit, no photo). It ends on the question or the moment of discovery ("मिल गया!!"), so the long video keeps the payoff. A reveal in a Short = BLOCKER.
- First frame is a strong visual (no title card, no black frame). First word within 0.5 s.
- Length 30-58 s (stories up to 003). From story 004: max 40 s, target 35-40 s (section 15).
- Captions and key visuals stay out of the bottom 20% and right 15% (YouTube buttons).
- Ending is either a cliffhanger towards the long video or a clean loop back to the first frame.
Thumbnail:
- Readable at phone size: Munshi downscales it to 160x90 px and checks the main face/emotion and the text are still recognisable.
- One clear focal point (a face with strong emotion or the key object), max 4 words, high contrast.
Title:
- The hook words come in the first 40 characters (mobile cuts long titles). Curiosity is fine, misleading is not.
Session:
- Every long video goes into its channel playlist, gets an end screen (next video + subscribe), and every Short from it has Related video = that long (manual Studio checklist).
Severity: a misleading title/thumbnail is a BLOCKER; the rest are FIX in R1 and MINOR after R2 (section 11).

## 14. Auto mode (after script approval)
From story 004, section 15 (production profile) overrides this section where they differ: no preview, budget ₹100–110 actual per story instead of the ₹130 cap, max 1 regeneration per image (BLOCKER only) instead of 2, final check R1 only. Everything else here (veto window, slots, covers, stop conditions, Studio checklist, logging) still applies.
- Human checkpoint: ONLY script approval. After that everything runs automatically without asking for each step: assets (character sheets, voice samples), scene images, TTS, preview, Munshi R1 (FIX items fixed automatically, free or paid within the cap) + R2, final build, Munshi final review, long thumbnail, upload, Auto Short flow (section 8: build, review, upload), first comments, sync.
- Publish timing: section 8 (decided after the upload from the IST clock: 19:00–23:59 public now, otherwise 19:00 the same day; Short +60 min; one long per day). Right after each upload, show the user one status line (video link + public now / scheduled time) and, while the API is unaudited, the STUDIO ACTION message. Veto window for scheduled videos: if the user says "rok do" before the time, run `tools/veto.py <video_id>` (sets the video private and removes publishAt via the API), log it in the channel log.md, and pause the pipeline for that story.
- Thumbnails: the long thumbnail is set via the API automatically. Short covers cannot be set by the API: the Short's first frame is its cover (hook visual, no caption in the first 1 s, any text inside 15%-85% of the height); also save a vertical cover file (1080x1920) in the Short's output/ for manual use.
- Stop conditions: ONLY the 3 in section 1 (balance below ₹50 -> ask the user to recharge, copyright doubt, channel ID mismatch). Budget cap, regeneration limits and BLOCKERs after R2 never stop the flow; they are handled as in section 15 (story 003 used a ₹130 cap and max 2 regenerations).
- Manual Studio checklist after uploads (the API cannot do these): Related video for the Short = its long video, pin the first comment, and — until the API audit passes — the STUDIO ACTION (make public now / set the schedule). Munshi shows it after the uploads and asks about it at the start of the next session until the user confirms.
- Every auto step is logged in the channel log.md with cost so far, and shown to the user as one short status line.
- pipeline_queue.json tracks each story's stages (script_approved -> assets -> images -> tts -> preview -> final -> uploaded -> short_uploaded -> done, or stopped/vetoed with the reason).

## 15. Production profile (user's standing instructions, from story 004 onwards)
- Only human checkpoint: script approval. Everything after that runs automatically with Munshi reviews: assets, images, TTS, final build, thumbnail, upload, Short, comments, sync.
- Length: long video max 4:00 (target 3:40–4:00). Short max 40 s (target 35–40 s). The script is written to this length using measured TTS speed.
- Cost: ₹100–110 per story in ACTUAL cost (usageMetadata, incl. reference images), covering long + its Short + thumbnail. Before generating anything, estimate the actual cost; if above ₹110, simplify the plan first (fewer new images, more crop/zoom reuse) — never start over budget.
  - Max 16 new scene images per long video; the rest are crops/zooms of those.
  - 1K images only. Reference images: only the characters present in that scene.
  - Reuse existing character sheets; new sheets only for genuinely new characters.
  - Max 1 paid regeneration per image, and only for a BLOCKER.
- No preview video. Munshi reviews the stages (script timing, images, audio) — R1 and R2 — and right after R2 the FINAL video is built directly.
- After R2: MINOR issues are ignored (logged to carry_over.md), nothing is regenerated, move to the next step.
- No paid call needs the user's OK. Stop and ask ONLY when: (1) the Google balance is below ₹50 (ask the user to recharge), (2) there is a copyright doubt, (3) the channel ID does not match. Everything else is handled without asking and written to the channel log.md:
  - Cost about to cross ₹110: do not ask — shrink the plan yourself (fewer new images, more crop/zoom reuse) and continue.
  - A BLOCKER still in an image after its 1 regeneration: do not ask — build that scene from a crop/zoom of a good image (or move the scene's line onto another image) and continue.
  - Any BLOCKER after R2 that can be fixed for free: fix it yourself. One that cannot be fixed for free: handle it the same way (crop/zoom reuse, move the line to another image), never by asking.
- Final video: Munshi does one final check (R1 only). If no BLOCKER -> upload; publish timing per section 8 (public now or scheduled from the IST clock right after the upload; "rok do" possible before a scheduled time; STUDIO ACTION message while the API is unaudited).
- Default motion = 2.5D parallax (Depth Anything V2 Small, local, free); artifact par zoom fallback.
- Story 005 se image style = Kissago Painted; style block aur sheet_painted reference zaroori. (`channels/<key>/brand/STYLE_PAINTED.md` section 1 verbatim at the end of every image prompt, `characters/<name>/sheet_painted.png` as the character reference; `scripts/gen_scenes.py` does both and runs `tools/name_guard.py` on every prompt; section 12a applies.)
  (`scripts/make_short.py --motion parallax` is the default, `--motion zoom` keeps the old Ken Burns; the guard in `tools/parallax.py` halves the motion or falls back to zoom per shot and logs it in shared/parallax_log.jsonl. Shorts: shots.json "subjects" boxes keep each speaker's face/hands/gesture inside 3-85% of the crop width.)
