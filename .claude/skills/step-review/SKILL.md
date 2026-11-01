---
name: step-review
description: Stage-by-stage review checklist for Story-Channel videos (script to thumbnail); returns PASS / FIX / ASK. Used by the munshi agent after every production step.
---

# Step review for Story-Channel

Use this after every production step of a video in the Story-Channel project. Always read `shared/RULES.md`, then `channels/<key>/RULES.md`, and `channels/<key>/channel_bible.md` first. Verify by opening files yourself; never accept a summary as proof.

## General method
1. Identify the video folder (e.g. `channels/jugnu-stories/stories/001_lalchi-halwai/long`) and the stage just finished.
2. List the files the stage produced and confirm each exists, with size and date.
3. Run the stage checklist below. For every item record what you actually opened or measured.
4. Decide the verdict: PASS (all verified), FIX (free fix needed), ASK (paid fix, story change, or taste call).
5. Report in the munshi format and append one line to `channels/<key>/log.md`.
6. Frames/contact sheets you extract go to the video's `review/` as JPG (quality ~85), never PNG. Only `review/*.md` reports are kept in git.

## Stage checklists

### 0. New asset added
- Any new music/SFX/font/image from outside: licence verified and row added to assets_license.csv before it is used.

### 1. Script
- Duration estimate vs target (narration ~2.5 words/sec in Hindi; Gemini Dadi voice runs slower, so add ~25%).
- Every line has a speaker that exists in `channel_bible.md` or in the project's character list.
- Opening hook in the first 10 s; moral stated clearly at the end.
- Long video: the Dadi–Golu opening is max 10 s (lines marked `"part": "intro"`), and the last spoken line is one specific question to viewers about the story (template: `channels/_template/stories/000_story-slug/script/script.md`).
- Mystery videos: the clue is fair and visible, and the answer is not in the title.
- Mitthu never does anything that needs hands.
- Originality: run RULES section 12 checks.
- Algorithm: run RULES section 13 checks.

### 1b. Surah script (channel noor-e-raah)
- Order: parichay -> shan-e-nuzul -> aayat-dar-aayat -> seekh + next-video hint.
- Every [S#]/[M#] exists in the dossier with the same grade; open the main sources. Missing source = BLOCKER;
  anything from "chhoda gaya" = BLOCKER; ikhtilaaf told as certain = MAJOR.
- Every ayah: ARABIC and TARJUMA match the dossier's source letter for letter; licences of both in
  shared/assets_license.csv (missing = copyright doubt, ASK).
- No recitation audio, no vocal/beat music, music continuous (does not stop for an ayah; one soft swoosh per ayah, RULES 1c), no visual of any Prophet/Sahabi/angel (even silhouette/shadow) = BLOCKER.
- Review sheet lists every shan-e-nuzul statement on its own line with its source link(s).

### 2. Scene breakdown (`*_SCENES.md`, `shots.json`)
- Every script line maps to a scene; no scene without a line or a music-only note.
- Shared-image scene pairs have a different crop/zoom that actually shows the subject of the line.
- Image count and cost estimate (₹3.24 each) match the plan.

### 3. Character sheets
- Look at each sheet with Read. Face, clothes, colours, age look match `channel_bible.md` or the approved spec.
- Jugnu Stories story 008+: characters are cut-outs (cast v3 PNGs, `tools/compose_scene.py`): only cast v3 / same-style side characters (any old-cast character or an AI-drawn character = BLOCKER); background has no people/animals of its own; feet on the ground, sizes consistent, light matches, nobody cut by the frame edge.
- Props are period/setting correct (mitti ka chulha, not gas stove).

### 4. Scene images
- Lookalike (RULES 12a), every image incl. thumbnails and sheets: "Kya ye kisi jaane-maane kirdaar ya scene ki nakal lagti hai?" Yes -> BLOCKER: new prompt + 1 regen, still yes -> drop the shot (crop/zoom another image); never use such an image even if paid. From story 005: Jugnu Painted look (STYLE_PAINTED.md), painted sheets as references, Mitthu's throat plain green.
- Make or open a contact sheet. Each image: correct characters, matching their sheets; location consistent; the action of the line is visible (who holds what, who is speaking).
- No garbled AI text in the image, no extra fingers or broken faces in the main subject.
- 16:9 for long, 9:16 for shorts.

### 5. Voice samples / TTS
- `ffprobe` every wav: duration > 0, no silence-only files.
- Count TTS files = count of spoken lines in `lines.json`.
- Run Whisper on each line and compare the transcript with its text; list mismatches.
- Cost vs estimate; flag if >30% over.

### 5b. Edit (Sampadak: `edit_plan.json`)
- `channels/<key>/brand/EDIT_STYLE.md` exists and the plan uses only what it allows (Noor: look only, nothing else).
- `review/edit_notes.md` gives a reason (beat / retention drop point) for each kind of effect; no effects "everywhere".
- Every SFX/ambience file in the plan is in `shared/assets_license.csv`; all anchors are real line numbers.
- A test build of the first 30-40 s ran; length and line timing unchanged; loudness still -14 LUFS +/-1, TP <= -1.0.
- Look at 3+ frames: Arabic/Hindi text untouched and readable, no effect over faces' meaning, Shorts safe zone free
  (bottom 20 %, right 15 %), riddle notes never show the answer. Any breach of EDIT_STYLE "Never" = BLOCKER.

### 6. Preview build
- `ffprobe`: resolution 960x540, duration vs target.
- Extract one frame per line (mid-line timestamp) and check the right character/scene is on screen.
- Music cue list matches the mood plan; crossfades present.
- Captions: count, and timing of a sample of lines vs Whisper.
- Algorithm: run RULES section 13 checks.

### 7. Final build
- `ffprobe`: 1920x1080 (or 1080x1920 for shorts), 30 fps, H.264 + AAC.
- Loudness via `ffmpeg -af ebur128` or loudnorm print: -14 LUFS ±1, true peak <= -1.0 dBFS.
- Music level under voice within the RULES range.
- Same frame-per-line check as preview, at full resolution.
- `.srt` present, UTF-8; lines estimated rather than Whisper-timed are listed.
- Duration within the range the user approved at preview.
- Copyright: run the RULES section 10 checks against shared/assets_license.csv. Any miss is FIX.
- Algorithm: run RULES section 13 checks.
- Parallax artifacts (default motion, RULES 15): for every scene extract the first, middle and last frame of each
  shot and look at full-resolution crops of character edges. Look for: halos or smears at outlines, inpaint
  smear in the revealed sliver, feathers/wings (Mitthu), hair, Dadi's stick, Pandey's lathi, wires and tree edges
  ghosting, faces stretched or wobbling, any frame edge or border showing, jitter. The build prints the guard's
  "motion halved / zoom fallback" list and shared/parallax_log.jsonl has every shot's decision. A visible artifact
  on a face or a key character -> BLOCKER: fix free by rebuilding that scene with smaller motion or
  `--motion zoom` for it (log it); minor edge softness elsewhere -> MINOR.
- Shorts no-reveal (RULES 13): the Short (frames, captions, end card, title, description, cover) shows nothing of the discovery/answer/twist — not what was found, not who did it. Any reveal = BLOCKER.
- Shorts crop safety: in each shot the speaking character's face, hands and gesture are fully inside the crop and
  out of the right 15% (YouTube buttons) and bottom 20%; shots.json "subjects" boxes drive the builder's check.

### 8. Thumbnail
- 1280x720, <= 2 MB, jpg/png.
- Zoom on the Hindi text: matras and joined letters correct.
- Text large enough for phone (letter height >= ~12% of frame), <= ~4 words, does not repeat the title.
- No spoiler. Bottom-right corner clear. Characters match their sheets.
- Algorithm: run RULES section 13 checks.

### 9. Metadata (`meta.json` / `long_XX.txt`)
- Title <= 100 chars, description <= 5000, tags <= 500 chars, 3-5 hashtags.
- Every CC BY music track used is credited.
- Mystery: no answer anywhere; pinned-comment text prepared for after 24 h.
- made_for_kids and AI disclosure taken from `channels/<key>/channel.json`.
- Copyright: run the RULES section 10 checks against shared/assets_license.csv. Any miss is FIX.
- Algorithm: run RULES section 13 checks.
- Names (RULES 12a): run `python tools/name_guard.py <meta.json> <output .txt> <upload.json>`; any studio, film, anime or artist name in title, description, tags, hashtags, thumbnail text, pinned/first comment, playlist or file names = BLOCKER (upload BLOCK).

## Report format
Write in Hinglish, friendly but professional, address the user as "bhai". Keep it short.

STEP / PROJECT / VERDICT line, then: Kya check kiya, Problems (what, where, suggested fix, cost), Agla kadam.
