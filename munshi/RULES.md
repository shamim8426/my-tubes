# Munshi RULES — Story-Channel

These are the hard rules. If a builder summary, a script or a file disagrees with them, the rule wins and the step is not PASS. Edit this file to add new rules; Munshi reads it fresh every time.

## 1. Budget
- Prepaid Google Cloud budget: ₹500, auto-reload off. Current balance is whatever `cost_log.csv` says.
- Every paid call (Gemini image ≈ ₹3.24 each at 1K, Gemini TTS per line) must be in `cost_log.csv` with date, project, item, ₹.
- No paid call without the user's OK first. A fix that costs money is always ASK, never FIX.
- Flag it if a step cost more than 30% above its estimate (e.g. LONG_01 TTS: estimate ₹4.85, actual ₹6.63).

## 2. Story and characters (from `channel_bible.md`)
- Characters must match their approved sheets: face, clothes, colours, age look. Compare each scene image against the sheet with Read.
- Dadi (Kamla Devi) narrates. Every other character speaks their own lines in their own voice.
- Mitthu (parrot) has no hands: no hand gestures, holding things or pointing with hands.
- Setting: Dadi's home, the Golu–Mitthu opening/closing frame and all Dadi Jasoos cases are in Gulmohar Mohalla. The story Dadi narrates inside a moral-story video can be set in any village or town the approved script names (e.g. Rampur in LONG_01); check location consistency against that script. Village kitchens still use a mitti ka chulha, never a gas stove.
- The action in each image must match what the line says at that moment (who is holding what, who is talking).

## 3. Audio
- Final loudness: -14 LUFS integrated (±1), true peak ≤ -1.0 dBFS.
- Music sits under the voice: 12–14 dB below for Shorts, up to ~18–20 dB for narration-heavy long videos. If it is quieter than 20 dB under, flag it.
- Mood changes get a crossfade (≥1 s). No sudden music cuts under dialogue.
- No leaked background audio, clicks, or a line cut off mid-word.

## 4. Captions
- One `.srt` per video, Hindi, UTF-8.
- Each caption must appear while that line is being spoken (±0.3 s), over the right character's shot.
- Lines whose timing was estimated rather than taken from Whisper must be listed in the report.

## 5. Video
- Long video: 1920×1080, 30 fps, H.264, 16:9. Short: 1080×1920, ≤60 s, 9:16.
- Target length is set in the script. Allowed: ±10%, or inside the user's stated range. Anything beyond that is ASK.
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

## 8. Publishing
- Default publish time: 7:00 PM IST.
- At least 2 days between two long videos on the same channel. Shorts can go on other days.
- Nothing goes Public or gets scheduled without the user's OK in that conversation.
- One upload per video. If `output/upload_result.json` exists, do not upload again.

## 9. Safety
- Never show or commit `.env`, `secrets/`, API keys or OAuth tokens.
- Never delete files; move them to `_to_delete/`.
