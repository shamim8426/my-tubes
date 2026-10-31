# Claude explainer Shorts - style guide v2 (user-approved 2026-10-31; this is the channel theme, ALL videos follow it)

## Look
- White background, black + yellow (#FFD60A) only. Big text that matches what is spoken (highlighter marker on key words).
- Fonts: Poppins ExtraBold/Bold/Medium, IBM Plex Mono (code), Mukta (rare Devanagari). Yellow wipe on every cut.
- Cute robot mascot (mascot/*.png: wave, think, work, stop, thumbs, team.png lineup). More robots allowed when the idea needs a team.
- Music: Funkorama (Kevin MacLeod, CC BY 4.0) 12 LU under the voice, ducked. Credit line in every description. Loudness -14 LUFS, peak <= -1 dBFS.

## Language
- Conversational Hinglish. On screen: Roman script, very few Devanagari words. Voice (Gemini TTS, Charon): casual Indian tech YouTuber, no sing-song.
- Content = official docs only (code.claude.com), every claim sourced. Never copy another creator's material.

## Structure of every Short (35-70 s, one idea)
1. OPENER (first 6-7 s) = PICTURE STORY, not text: the robot DEMONSTRATES the feature (user 2026-10-31: "robot dikhaye ki asli me kaise use hota hai").
   Scene type `stage` (layers with keyframes: img, box, doc, hook, text). Reference: 006_hooks scene 0.
2. What it is -> real example (flow) -> config/code -> options (list) -> the one useful trick (compare) -> CTA.
3. Docs scenes show the real docs page scrolling (scripts/docs_shot.py). Every scene uses a DIFFERENT layout from the one before.
4. EVERY NEW VIDEO adds at least one new enhancement (new scene type, animation, robot pose, sound or explanation device); log it in log.md and add it here.

## Tools (all local, free-first)
- scripts/build_deck.py <story> [--tts [--paid]] [--still t1,t2] [--render]; deck.json -> build/deck.html -> output/short.mp4.
- NOTE: --tts only fills MISSING s_XX.wav and then exits; to change a line, move its wav away, run --tts, then --render.
- Scene types: statement, chips, flow, docs, code, list, compare, hub, cta, stage (+ per-scene robot/robots). Template: templates/deck_template.html.
- html_video.py (Playwright + real Chrome + ffmpeg), remux_music.py, music_preview.py, gen_robot.py (free Cloudflare).
- Free-first: Cloudflare images, free Gemini TTS key; paid TTS only with user OK (given 2026-10-31, ~Rs1.3/video).

## Open items
- Subagents (003), MCP (005), Skills (004): redo with Hinglish + robot + music + picture-story opener.
- Tighten team.png crops (centres ~0.156/0.38/0.61/0.84, width ~0.2).
- Channel not created yet (user gives channel ID + language); Munshi review and upload not done.

## Enhancements log
- 007 Subagents: stage layer kind `meter` (yellow progress bar, keyframe `f` 0-1) to show a context window filling. Note: keyframes interpolate from the previous keyframe, so repeat `o:1` to hold opacity.
- 008 Skills: stage opener 'paste-stack merge' (3 tilted paste bubbles collapse into one SKILL.md doc; box layers with keyframe r tilt).
- 009 MCP: stage opener traveling bubble (copy-paste bubble flies to Claude, then MCP badge connects tools; keyframes x/y/r on box layers).
- 010 Memory: stage opener 'session gap' (two session pills, a CLAUDE.md doc bridges them, '?' bubble then 'yaad hai!').
