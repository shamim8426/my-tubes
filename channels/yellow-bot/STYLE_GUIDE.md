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
- 011 Checkpointing: stage opener 'undo' (doc turns messy, two Esc key caps pop, doc un-messes; reuses doc 'mess' keyframes in reverse). Note: TTS paid key has a 10 req/min limit; wait 20 s and rerun --tts --paid.

## v3 FORMAT (user 2026-10-31, from video 7 on; applies to every video)
Reference pages (open in a browser): brand/reference_tools_short.html (5-scene storyboard of a full Short) and brand/reference_svg_robot.html (2D SVG robot animation).
1. WHAT IS SAID MUST BE SEEN. Every term/step/claim the voice says gets its own visual in the same second: a card, icon, docs screenshot, terminal line, diagram or highlighted code line. No scene where the voice talks and the screen only has a title.
2. Goal of each video: explain ONE feature/tool of Claude Code from the official docs with a REAL example, professionally, so the viewer understands and it looks attractive. NO quiz, NO "guess karo" moments. A single open question in the CTA only.
3. Default scene order (vary it a little each video): (1) concept as cards/icons -> (2) docs proof (real docs screenshot scrolling) -> (3) real example as terminal/steps with permission/result chips -> (4) the nuance from the docs (what is easy to get wrong) -> (5) 3-point recap + open question.
4. SVG robot (layer kind `svgbot`, see below) is used SOMETIMES in between (about one scene per video), for explaining/pointing; the PNG robots stay for opener/recap. Do not put a robot in every scene.
5. Use good HTML technique: design tokens (white/black/yellow only), one type scale (Poppins + IBM Plex Mono), inline SVG icons with equal stroke, easing (ease-out / back), staggered reveal timed to the voice cues, real docs screenshots (scripts/docs_shot.py), no bitmap for anything that can be SVG/CSS. Cost stays Rs0 for visuals.
6. Nothing is added just for decoration; if a scene does not help understanding, cut it.

### Layer kind `svgbot` (in stage scenes, templates/deck_template.html)
{"kind":"svgbot","size":720,"x":20,"y":520,"flip":false,
 "k":[[t,{"x":..,"y":..,"s":..,"o":..,"ar":angle,"al":angle,"e":"b"}], ...],   # ar/al = right/left arm angle in deg (0 hanging, -150 raised up, -86 pointing sideways right; al mirrored: +150 raised, +86 pointing left)
 "talk":[[t0,t1],..]   # mouth moves in these windows (use the voice cue times)
 "wag":[[t0,t1],..]    # right arm waves
 "nod":[[t0,t1],..]}   # head nods
Eyes blink, body breathes and antenna bobs automatically. The robot box is 400:520 wide:tall; it fills about the middle 230 px of that width.

### Layer kind `draw` (whiteboard draw-on, in stage scenes; example: stories/012_tools/deck_whiteboard_demo.json)
Hand-drawn diagram that draws itself, line by line, in the white/black/yellow look. Use it for flows and relations (A -> B -> C), circling the important part, underlining a note.
{"kind":"draw","x":0,"y":420,"w":1080,"h":1100,"sw":7,"items":[
  {"t":"box","x":90,"y":40,"w":470,"h":140,"label":"Read","size":56,"fill":"#FFD60A","fo":.55,"at":1.0,"dur":.9},
  {"t":"arrow","from":[325,190],"to":[325,310],"at":2.0,"dur":.6},
  {"t":"circle","cx":325,"cy":390,"rx":262,"ry":92,"at":5.4,"dur":.8},
  {"t":"line","from":[650,420],"to":[900,418],"color":"#FFD60A","at":6.2,"dur":.4},
  {"t":"text","x":650,"y":395,"text":"poochta hai","size":46,"at":6.0,"dur":.5}]}
`at` = seconds after the scene starts (take them from the voice cue times, like the other stage layers); `dur` = how long the stroke takes. Wobble is seeded, so every frame is the same for the same t. Labels fade in after their box is drawn. Keep text >= 40 px; keep side notes at least 40 px away from circles.
- 012 Permission modes: stage opener 'status-bar cycle' (mode pill swaps in place as Shift+Tab key cap pops: manual -> accept edits -> plan).
- 013 Context window: stage scene where the `meter` collapses 0.95 -> 0.25 on the 'structured summary' cue and hand-drawn check ticks (two `draw` line items) draw on each 'survives compaction' row.
- 014 Sessions: session-picker mock in a stage scene; a yellow selection bar slides between rows on the 'arrow keys' / 'Enter' cues, key-cap chips pop in for arrows, Enter and Space.
- 015 Worktrees: first real use of the `draw` layer (one arrow splits into two hand-drawn 'worktree A/B' boxes with 'alag branch' labels); opener doc visibly messes up when two session pills collide.
- 016 Plugins overview: 'gather-and-pack' opener (four chips Skill/Agent/Hooks/MCP fly into a my-plugin/ box, box pulses via scale keyframe, 'ek install, ek unit' pill pops).
- 017 Statusline: 'stdin pipe' opener (JSON packet card slides into a 'your script' card, output appears as a dark status-bar line with a yellow `meter` filling to 42%); svgbot raises both arms in the recap.
- 018 Headless: 'command-line assembly' opener (dark terminal card gets `$`, `claude`, then yellow `-p` and `"prompt"` chips in sequence, then a 'jawab print + exit code 0' result card).
