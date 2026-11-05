# DevRoboLab - edit style (user feedback 2026-11-06, binding for every new video)

User said: "kuch match hi nahi kar raha jo bol rahe ho vo dikh nahi raha, audio-video sync nahi, koi motion nahi, editing style nahi, HTML nahi, real photos/clips."

## 1. Mood
Fast, clear, real-feel explainer. One visual idea per phrase, always what is being said, never a decoration.

## 2. Match + sync (hard rule)
- Cut the script into BEATS (a phrase of 2-4 s). Each beat gets ONE visual that depicts that phrase (object, action, real UI crop). No generic stock that only "looks related".
- Visual change happens exactly on the first spoken word of the beat: measure real word times with Whisper (stories/036_cfe02-edited/wordtimes.py -> wt.json), never estimate from text length. If Whisper drops words (n_whisper < 85% of tokens) fall back to character position inside the measured voice duration.
- Caption (Roman Hinglish, 3-6 words, key word yellow) pops word by word at the beat start. Callout (screenshot of the official page) slides in on the trigger word.

## 3. Images (no HTML cards)
- Priority: real CC0/public-domain photos (Openverse API: license=cc0,pdm; StockSnap/Rawpixel work; Wikimedia is rate-limited; Pixabay/Pexels blocked in cloud) -> else free Cloudflare FLUX photoreal images of OBJECTS/ACTIONS that depict the phrase (no people/faces, no text) -> else AI sticker. Screenshots of the official help page are proof callouts only.
- Never reuse one photo (e.g. the old sneaker/manuscript) as a default. Label AI images as AI-drawn in the description.

## 4. Motion and editing
- A new visual every 2-4 s. AI beats: 2.5D parallax (tools/parallax.py, push_in / pull_out / pan_right / gentle_orbit; never the same preset twice in a row) + extra punch-in 1.0 -> 1.10. Photo beats: blurred-fill band + strong Ken Burns 1.0 -> 1.30 with tilt and a little shake.
- Transitions: whip-pan with motion blur inside a scene; white flash + cross-dissolve between scenes. Thin yellow progress bar on top, soft vignette, light grain.
- Sound: whoosh (shared/sfx/whoosh_803771.mp3, -9 dB) at every cut, UI pop (magic_376747.mp3, -14 dB) on every callout, Funkorama music 24 dB under the voice, -14 LUFS, TP <= -1.5.

## 5. Text
- Captions: Poppins ExtraBold with black outline, lower third (y about 80%), pop scale 1.12 on each new word. Titles only as a short caption, never a card.

## 6. Never
- HTML-card look, diagrams that replace a real image, a text page as the main visual, a photo that does not show the spoken thing, images that are not synced to the voice.

## 7. Renderer
scripts/photo_video.py (helpers) + stories/036_cfe02-edited/make.py (beats table, whip/flash, SFX, kinetic captions). Reuse make.py as the template for new videos.
