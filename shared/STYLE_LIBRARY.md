# STYLE LIBRARY (ALL channels) - styles, edits, graphics, motions, sound and process learnings from our own videos

**Standing rule (user 2026-11-07):** every learning from a video (style, edit, graphic, motion, sound, layout, process) is written HERE, in this common file, not only in one channel's folder, so every channel and every session can use it. After each video: add or update an entry (date, channel, what worked / what the user disliked, the code that does it). Channel-specific look stays in `channels/<key>/STYLE_GUIDE.md` or `brand/`, but must link here when the idea can be reused. Read this file before building any video. Copyright and originality limits (RULES 10, 12, 12a, 12c) always win: we only take abstract principles from other channels, never their frames, audio, words or titles.

Code that is shared lives in `scripts/` and `tools/`; ready-to-copy reference builds live in `shared/style_library/`.

## 1. Showing a source document (articles, docs pages)
- NEVER show the whole page, never repeat the same page card. User: "har baar sara document dikhana zaroori nahi, bas kabhi bahut important point dikhao."
- Show only ONE crop of the key block, small, on a taped paper note (or inside a phone / TV news frame): `scripts/dev_v6.py` (phone, paper, tv frames); the screenshot comes from `stories/<n>/shots.py` (own Playwright capture; also saves `raw/article_plain.png` without marks + per-line rects `lines` in `raw/rects.json`).
- The yellow marker is LIVE: it wipes line by line, left to right, in the seconds the voice speaks that phrase (beat field `hl=(t_start, t_end)` taken from the word times, linear). Never a static highlight baked in the screenshot.

## 2. Real images with motion (what is said must be seen)
- Mostly real-looking photos with motion, HTML/graphics only sometimes. For web / Desktop / Mobile show THREE photos, one per spoken word, as cards that slide in with overshoot and a label chip (WEB / DESKTOP / MOBILE).
- Photos: free Cloudflare flux (`scripts/cf_image.py`, Rs 0, 1344x768), prompts "realistic product photo of ... no text"; stored in `stories/<n>/raw/photos/`. Real third-party news footage is NOT allowed (RULES 10, licence row needed); allowed = official/own/licensed (CC0, Pixabay, Wikimedia) with a row in `shared/assets_license.csv`.
- Motion on photos: slow Ken Burns (zoom 1.0 to 1.15, small pan) inside a rounded card (`photo()` / `photo_dyn()`), shadow, slight rotation (+-1.5 deg).
- Screens that PLAY: the animated UI is perspective-warped onto the screen of the photo (`screen_comp()` with measured screen corners per photo; `QUAD` dict in the reference build), then zoomed toward the screen. Measure corners with a coordinate grid drawn on the photo.

## 3. Dark UI walkthrough (explaining a Claude / app feature, Claude Feature 01/02 look)
- Everything that is DONE inside the app is shown in a dark UI: black background, window #121212, sidebar #0C0C0C, accent orange #D97757, text #EEE, blue chip for the "Research" indicator; cursor + click ripple + click punch-in (+0.035 scale, decays 0.25 s), STEP banners (orange chips: STEP 1 ... STEP 4), a small "Illustration" tag (it is our animation, not a recording).
- States are driven by the times of the spoken words (`T(scene, token)`): toggle ON, + pressed (menu pops), item selected (turns orange), question typed (about 0.5 s), send, steps with spinner then green tick (about 0.4 s each), report card with bars.
- Ask the question INSIDE the demo too (typing in the input), not on a photo. Make it continuous: enable steps -> ask -> sources in ONE scene.
- Speed: user said the demo felt slow; typing 0.5 s, rows 0.4 s, cursor arrives 0.25 s before each click.
- Code: `walk_win`, `walk_cursor`, `walk_scene`, `S_hook`, `S_main` in `shared/style_library/feature_walkthrough_make_v10.py` (copy it into the new story, change the texts and times).

## 4. Editing, layout, captions
- Calm editing: hard cuts, no blur-push, no progress bar, no yellow wipe on every cut; one idea per scene; fewer, bigger shots.
- Sizes: cards <= 960 px wide, content inside y 190-1250 of 1920, caption chip at y about 1385 (kinetic: current chunk only, key word yellow, 2-3 words), small source line at y about 1290 only when a document is shown. Nothing overlaps the caption or the source line.
- Chips: use pad (40, 2) and 128 px vertical spacing for 74 px text, or the glyph tops are clipped and chips overlap.
- One big-number card early (e.g. "5+ SEARCHES"), plans as three stacked chips popping on their words, usage meter for limits, robot only for emphasis/CTA.
- Soft light background (cream with yellow glow) for photo scenes, black for UI-walkthrough scenes; the change is the "stylish cut".

## 5. Sound
- NO whoosh / swipe sounds (user 2026-11-07). Voice + low music only (Funkorama, 12 LU under voice). Cloud renders measured -15.1 LUFS, peak -1.4 dBFS (target -14, +-1 allowed; re-check before upload).

## 6. Process and tooling learnings
- Show 4-6 stills as a contact sheet before a full render; render two videos in parallel (4 CPUs, about 4 min instead of 10-12 each).
- Fresh cloud container: `.venv/bin/pip install opencv-python-headless playwright pillow numpy` (system python has no cv2). Do not reuse the name `H` for another variable (canvas height).
- YouTube cannot replace a video file: upload the new private video, then delete the old private one only after the user says yes (`videos.delete` with the channel token works; check it is private first). Thumbnails (API 403) and going public stay manual in Studio.
- Ask which series a look belongs to: Claude for Everyone = app UI walkthrough; Claude Code = terminal mock-ups; AI news = device/paper crops of the official article.
- Write every user feedback into this file the same day; also keep the channel `log.md` line.

## 7. Index of builds that use these ideas
- `stories/041_cfe-research/make_v10.py` (Claude Feature 03): photos + playing screens + dark walkthrough + live marker note.
- `stories/042_news-personal-finance/make.py` + `scripts/dev_v6.py`: AI news Short with device / paper / TV crops (v6; not yet moved to v7).
- `stories/039_cfe02-demo`, `stories/040_cfe03-artifacts`: the original dark UI walkthroughs (HTML based).

## 8. Study: "Badar Munir" style (RULES 12c, 2026-11-07; principles only, nothing copied)
Watched 4 Shorts (28-83 s) + 1 long (6 min, same channel) + 1 long edit tutorial (11 min, other channel, linked by the user). Measured with ffmpeg scene detection + contact sheets.
- **Cut rhythm.** Shorts: a new picture every 1.2-3 s (33 s Short = about 27 changes; 82 s Short = about 25). Long: about 5 s per cut on average, but the screen-recording stretches run 15-25 s with only cursor/zoom motion; talking-head stretches are cut every 3-6 s. So: faster in Shorts, calm long takes only where a real demo plays.
- **Short layout = split screen 9:16.** Top 45-50 %: the "proof" (website capture, app UI, logo card, comparison card); bottom 50 %: presenter. Seam at about y 48 %. Every new fact = a new top picture, bottom stays the same, so the viewer's eye stays on the face while the top changes. One full-frame presenter shot at the start (hook) and one at the end (CTA).
- **Captions.** ONE to three words at a time, centred on the seam (y about 48-52 %), small (cap height about 2.5-3 % of frame, about 48-56 px of 1920), bold sans, white on a dark pill OR dark text on a lime-green (#B8F03C-like) highlight chip for the current word. Never more than one chip. Long: bold white word-pair under the demo, key words in lime, bottom 12 %.
- **Boxes / text cards.** Dark navy card (#0B1020-like) with small cap label ("BETTER / CHEAPER / FASTER" stacked 3 lines, last word in blue/orange), or white card with 2-3 tiny UI mock-ups side by side with a 10-12 px caption row below ("MODEL A | MODEL B" alternating colours). 2-4 boxes per scene, always different layout per scene, big empty margins; nothing touches the caption.
- **Comparison logo bar.** Persistent small logo pair "A vs B" in the top-left through the hook (two logos about 12 % of width, names under them). Logos are small, unmodified.
- **Long video structure.** Chapter title card ("Problem 1: ...") on black with serif-italic accent word, then presenter in a rounded 16:9 box beside the screen, BEFORE / AFTER side-by-side frames with tiny chips ("BEFORE", "AFTER"), a hand-drawn "formula" card ("A = B + C"), numbered cards (03 ...) that scroll like a deck. Screen recordings are light UI with orange accent; lower-third = small grey line + big bold green-yellow keyword.
- **Transitions.** Almost all HARD cuts or very short slide/blur (about 6 frames); no long wipes. Zoom-in on the part of the screen that is spoken about (1.0 to 1.3 over 2 s) instead of a transition. Screen elements highlighted by a thin rounded rectangle, not by arrows.
- **Graphics.** Real captured pages / UI (not drawn), tiny logo chips, simple line icons, one big number card ("20,000 TOKENS") per Short, a keyboard-close-up B-roll for "typing" (stock-like), blurred background plate behind a card for focus.
- **What this means for us (DevRoboLab).** AI-news Short: split screen is allowed in our own look = top 45 % real thing (phone/device with the written fact, small logo if the press page allows, how-it-works steps), bottom 55 % = our robot/mascot or a calm photo; one-to-three-word captions at the seam; a new top picture every 2-3 s; max 2-4 boxes, small, different layout every scene. Do NOT copy: presenter footage, their lime colour as brand, their captions/words/titles, their card texts.
