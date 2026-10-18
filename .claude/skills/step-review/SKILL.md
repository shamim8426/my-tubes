---
name: step-review
description: Stage-by-stage review checklist for Story-Channel videos (script to thumbnail); returns PASS / FIX / ASK. Used by the munshi agent after every production step.
---

# Step review for Story-Channel

Use this after every production step of a video in the Story-Channel project. Always read `shared/RULES.md`, then `channels/<key>/RULES.md`, and `channels/<key>/channel_bible.md` first. Verify by opening files yourself; never accept a summary as proof.

## General method
1. Identify the video folder (e.g. `channels/dadi-ki-kahaniyan/stories/001_lalchi-halwai/long`) and the stage just finished.
2. List the files the stage produced and confirm each exists, with size and date.
3. Run the stage checklist below. For every item record what you actually opened or measured.
4. Decide the verdict: PASS (all verified), FIX (free fix needed), ASK (paid fix, story change, or taste call).
5. Report in the munshi format and append one line to `channels/<key>/log.md`.

## Stage checklists

### 0. New asset added
- Any new music/SFX/font/image from outside: licence verified and row added to assets_license.csv before it is used.

### 1. Script
- Duration estimate vs target (narration ~2.5 words/sec in Hindi; Gemini Dadi voice runs slower, so add ~25%).
- Every line has a speaker that exists in `channel_bible.md` or in the project's character list.
- Opening hook in the first 10 s; moral stated clearly at the end.
- Mystery videos: the clue is fair and visible, and the answer is not in the title.
- Mitthu never does anything that needs hands.
- Originality: run RULES section 12 checks.

### 2. Scene breakdown (`*_SCENES.md`, `shots.json`)
- Every script line maps to a scene; no scene without a line or a music-only note.
- Shared-image scene pairs have a different crop/zoom that actually shows the subject of the line.
- Image count and cost estimate (₹3.24 each) match the plan.

### 3. Character sheets
- Look at each sheet with Read. Face, clothes, colours, age look match `channel_bible.md` or the approved spec.
- Props are period/setting correct (mitti ka chulha, not gas stove).

### 4. Scene images
- Make or open a contact sheet. Each image: correct characters, matching their sheets; location consistent; the action of the line is visible (who holds what, who is speaking).
- No garbled AI text in the image, no extra fingers or broken faces in the main subject.
- 16:9 for long, 9:16 for shorts.

### 5. Voice samples / TTS
- `ffprobe` every wav: duration > 0, no silence-only files.
- Count TTS files = count of spoken lines in `lines.json`.
- Run Whisper on each line and compare the transcript with its text; list mismatches.
- Cost vs estimate; flag if >30% over.

### 6. Preview build
- `ffprobe`: resolution 960x540, duration vs target.
- Extract one frame per line (mid-line timestamp) and check the right character/scene is on screen.
- Music cue list matches the mood plan; crossfades present.
- Captions: count, and timing of a sample of lines vs Whisper.

### 7. Final build
- `ffprobe`: 1920x1080 (or 1080x1920 for shorts), 30 fps, H.264 + AAC.
- Loudness via `ffmpeg -af ebur128` or loudnorm print: -14 LUFS ±1, true peak <= -1.0 dBFS.
- Music level under voice within the RULES range.
- Same frame-per-line check as preview, at full resolution.
- `.srt` present, UTF-8; lines estimated rather than Whisper-timed are listed.
- Duration within the range the user approved at preview.
- Copyright: run the RULES section 10 checks against shared/assets_license.csv. Any miss is FIX.

### 8. Thumbnail
- 1280x720, <= 2 MB, jpg/png.
- Zoom on the Hindi text: matras and joined letters correct.
- Text large enough for phone (letter height >= ~12% of frame), <= ~4 words, does not repeat the title.
- No spoiler. Bottom-right corner clear. Characters match their sheets.

### 9. Metadata (`meta.json` / `long_XX.txt`)
- Title <= 100 chars, description <= 5000, tags <= 500 chars, 3-5 hashtags.
- Every CC BY music track used is credited.
- Mystery: no answer anywhere; pinned-comment text prepared for after 24 h.
- made_for_kids and AI disclosure taken from `channels/<key>/channel.json`.
- Copyright: run the RULES section 10 checks against shared/assets_license.csv. Any miss is FIX.

## Report format
Write in Hinglish, friendly but professional, address the user as "bhai". Keep it short.

STEP / PROJECT / VERDICT line, then: Kya check kiya, Problems (what, where, suggested fix, cost), Agla kadam.
