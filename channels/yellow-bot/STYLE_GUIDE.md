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

## v4 FORMAT: motion + symbols + layman (user OK 2026-11-04, from the study of one AI-tools Shorts channel and videos 019/020)
Rules (binding from the next video; v2/v3 stay valid underneath):
1. OUR OWN LOOK, NEVER A COPY. Learnings from other channels are principles only (clear pacing, readable large type, several moving explanatory elements, text in step with the voice). Our signature stays: white canvas, black + yellow #FFD60A, heavy Poppins + Plex Mono, yellow highlighter marker, our robot + svgbot, hand-drawn `draw` strokes, key-caps, terminal cards, sticky notes. Never adopt another channel's palette, hero device, rank cards or CTA pattern. How we learn: LEARNING_PROCESS.md.
2. LAYMAN FIRST. Define each new term in plain words the first time (spoken AND shown), one everyday analogy per key idea ('jaise ...', labelled as analogy, never a new fact), one tiny 'you say X -> it does Y' example, one 'why it matters to me' sentence. Short sentences, no unexplained jargon. Claims stay docs-only. Give each key point time to be read; large type stays.
3. SYMBOLS WITH MEANING. Every icon/symbol must mean something the voice says (no decoration). 3-6 moving symbols per beat, a new visual event every ~1.5-2.5 s (15-35 changes/min), clean white canvas, one dominant subject per beat.
4. HOOK RULE: claim as text within 0.3 s of the first spoken word, with a number; first moving visual within 3 s. No half-empty lower half: fill build-up moments with supporting symbols (known rough spots in 020: 0-3 s, 10 s, 22 s, 42 s).
5. Length 45-75 s (hard cap 75, drop lower-value content rather than speed up). Mix to about -14 LUFS with a limiter pass, true peak <= -1 dBFS (a +1.3 dB gain + limiter 0.83 worked on 020).
6. Look at stills across the WHOLE final render before upload (text wrap, overlaps, empty halves).
7. Voice: gemini-3.8-flash-tts (Charon) is the default. It has a per-model daily request cap (100/day on Tier 1, shared by ALL channels): if it returns 429 'requests per day', set GEMINI_TTS_MODEL=gemini-3.8-flash-lite-tts (worked on 020; 3.1-flash-tts-preview and 2.5-flash-preview-tts return 400). Use ONE model per video. Costs ~Rs 1.2-1.8 per video.

Engine fields (all opt-in; old decks render unchanged, verified by pixel-diff on 34 stills; template: templates/deck_template.html, times in scripts/build_deck.py):
- Word-by-word text: "stream": true (yellow marker sweeps under each spoken word, words drop in with a small spring; **key** keeps the full highlighter) or "grey" (grey -> black variant); `step` (stagger, default 0.16 s), `sat` (start time, stage text layers). Works on statement scenes and stage `text` layers.
- list scene: "icons": true (round check/cross rows on the spoken item; item "ok": false = cross; "d" optional), "head" (+ hy, hsize).
- Icon layer: {"kind":"icon","name":..,"size":..,"label":..,"fill":false}; 28 names: terminal, code, desktop, globe, phone, file, folder, gear, bolt, lock, plug, sparkle, magnifier, check, cross, arrow, clock, branch, chat, key, bulb, box, shield, rocket, cursor, play, user, bug. Inside a box html: <i data-ic="file" data-s="84"></i>.
- Motions on any layer: float (number or {a,f,ph}), pulse, spin (+ spinAt), orbit {cx,cy,rx,ry,a0,w}, wig (wiggle start time), drawon [t,dur] (icons), in + ind + spring (pop-in 0.6 -> 1 with overshoot) and out, push (slow 1.0 -> 1.06 zoom, seconds), sh (soft shadow), stream, grey.
- Layer kinds: flow (connector with travelling dots: from, to | pts, at, dur, n, per, r, head, until; an endpoint may be {"orbit":{...}} to follow an orbiting icon), spark (twinkling stars: pts), typed (typing + blinking cursor: text, sat, cps, mono), ring (progress ring: size, sw, keyframe f, mul, unit), count (bouncing counter: to, pre, suf, size, css, keyframe f); meter with "pct": true (+ mul, unit) shows a percent label.
- Scene options: "wipe": "fade" | "push" | "iris" | "zoom" (trd = duration; the yellow wipe stays our brand signature, use the others sparingly), cam: [[t,{x,y,s}],...] (camera push/pan), hideN (hide the n/N scene counter when a step ring is on screen). Deck-level "rail": true (yellow progress rail with dots and n/N). CSS classes: bubble (and 'bubble y'), keycap, sticky, torn.
- Times: any layer time may be a voice phrase with offsets, e.g. "phrase|0.3|-0.1" (stagger = offsets).
- No new field needed for: before/after split, picture-in-picture robot, highlighter circle/underline (use boxes, images, the `draw` layer).
Reference decks: stories/019_overview (first v4 video, https://youtu.be/BHwc7iL1ujk, public), stories/020_quickstart (max-motion demo, https://youtu.be/R5eSmgK_xrM). Generators: gen_deck.py inside those folders (edit it and re-run instead of editing deck.json).
Learnings behind these rules: brand/STYLE_LEARNINGS.md (numeric, abstract) and research/study_log.md.

### Enhancements log (v4)
- 019 Overview: stream word reveal (marker), icons list, count + pct meter, sticky/torn/keycap cards, sh + in/spring, wipe fade, rail, phrase times, layman explanations.
- 020 Quickstart: 28-icon SVG set, float/pulse/spin/orbit/wig/drawon, flow (travelling dots), spark, typed (cursor), ring (step 1/4..4/4), count, cam push, wipes push/iris/zoom, hideN, before/after split, PiP robot; voice via gemini-3.8-flash-lite-tts (per-model daily cap).
- Keep adding here: every new video logs its new device; every new study/learning goes to STYLE_LEARNINGS.md first, then (after it proves itself) a rule above.

### Ending / CTA rule (user 2026-11-04; replaces the 'one open question' ending of v3 for new Shorts)
- The LAST spoken line is a short FOLLOW call for Yellow Bot, not a 'comment me batao' question. Say the channel name and show it on screen at the same moment, give the brand mark (our robot) one clean hero moment, keep it to one sentence of about 8-14 words (~3-4 s), stop on the last word (no loop, no reveal). Only promise what we really deliver (new AI tricks, plain-language explanations); never promise a gift, ebook or resource we do not have.
- TWO lines in rotation (user choice): (A) normal Shorts (user chose 2026-11-04, replaces the earlier 'AI की बात seedhi bhasha me chahiye?' line): 'AI के ऐसे काम के features चाहिए? Yellow Bot को follow करो।' (B) magic-trick Shorts: 'एक follow, और AI का अगला जादू आपकी screen पर। Yellow Bot को follow करो।' More lines may be added only after the user approves them.
- Visual (our own look): robot waves/thumbs-up, a big yellow 'Follow' pill clicked by a cursor with a small dust burst, a wiggling bell, 'Yellow Bot' in heavy Poppins, white canvas. In gen_deck.py the ending lives in three variables at the top: CTA_VOICE, CTA_SCREEN, CTA_PILL (last scene). Already published videos keep their old ending.
- Basis: brand/STYLE_LEARNINGS.md 'Endings' (principles only; no wording of another channel is used).


## Enhancements log 2026-11-04 (021)
- Scene field anchors: real spoken-word times (measure with Whisper) pin effects to the voice. Numeric phrase cues work ("phrase|0.3|-0.1"). Morph timestamps resolve. hideN, bell icon, portal chip hide added.
- Free TTS route: gemini-3.8-flash-lite-tts on the free key (Rs 0; per-minute limit ~3 requests, wait ~70 s) when the paid model hits its 100/day cap. Set env GEMINI_TTS_MODEL.
- Length rule: stay under 75 s; a re-voiced line must not be longer.

## Channel direction and daily style rule (user 2026-11-04)
- Yellow Bot is a whole-AI channel (any organisation, model, feature, free tool), not only Claude. Claude docs Shorts are the base set for now; the topic scope will widen as the channel grows (target: 1,000+ subscribers).
- Goal now: build a strong BASE first (content quality, editing, visuals, technical ideas in simple language any ordinary person understands), improve it from analytics, then apply it to the planned daily Shorts. Main aim: keep improving and give good-quality content, always inside YouTube's guidelines (original value, honest title and thumbnail, accurate facts from the primary source, no spam tags, no misleading claims).
- DAILY STYLE RULE: one style per DAY. All Shorts of one day share one style (a minimum of 3-4 videos per style); the next day changes the style and adds one small improvement or something new, learnt from the earlier videos and from analytics. Not a different look for every video within a day.
- Every style change is logged here (what is new, why) and judged by analytics after 2-3 days (data lags; under 1,000 views is only a signal).

## Enhancements log 2026-11-04 (Day 1 pack, 022-024)
- Day 1 style 'clean product-page' (contrast to the 'magic' look of 019-021): deck fields `bg` + `bgGrid` (calm #F3F5F9 dotted page), light/dark product windows with soft shadow, white cards, yellow highlighter + robot kept as brand mark, `wipe: fade` only, no dust/wand/portal effects. Helpers: templates/ydeck_helpers.py (window, card, line, cta_scene, finish; content shifted down 120 px so the lower half is used).
- Measured word times: scripts/yb_wordtimes.py (Whisper small, local) writes wt.json; gen_deck attaches `wt` to scenes and build_deck.phrase_time interpolates it, so any cue phrase is timed to the real voice (replaces hand-made anchors).
- Teaching structure used: hook with the problem -> one labelled analogy -> demo/3 steps with a real command mock-up -> one caution -> recap -> ending line A.
- Free TTS limits (2026-11-04): each free model has its own 10 requests/day cap; one 7-scene Short needs 7. Plan 1 Short per model per day, or keep scenes few.
- Mix: html_video output is about -15.6 LUFS; extra `volume=1.6dB,alimiter=limit=0.85` gives -14.2..-14.7 LUFS, TP about -1.2.

## Long news digest (16:9) (first one: story 025, 2026-11-05)
- Format: 1920x1080 landscape, 3:00-4:00 (hard max 4:30), upload.json `"format": "long"`, title Hinglish <= 70 chars without #shorts, PRIVATE, playlist 'Latest AI Updates' (`"playlist_id": "PLTCArDe2LLAo"`, see research/playlist_latest_ai_updates.txt).
- Engine field: deck.json `"format": "landscape"` (build_deck sets w 1920 / h 1080, hides the per-scene tag unless `"tag_on": true`; output/video.mp4). html_video.py and html_scene.py read the size from the deck page; old 1080x1920 decks are unchanged (pixel-diff 0 on 21 stills of 019, 021, 024). Stage coordinates are in the 1920x1080 canvas; keep 100 px side margins, text >= 60 px for key lines.
- Style 'news bulletin': calm #F3F5F9 page, ticker pill top-left ('AI NEWS DIGEST . date') and 'n / 5' pill top-right, dark lower-third with item title + yellow 'Source: <org>' tag on every item, white cards with simple symbols, robot as brand mark (hook, recap, follow).
- Structure: hook 0-10 s (what you learn today), 4-5 items of 30-40 s (what happened in one sentence, why a normal person should care, one concrete example or what to do, source), 20 s recap, closing line A (CTA_VOICE/CTA_SCREEN/CTA_PILL). Layman first; say what the page does NOT state ('page me nahi likha'); non-Claude items carry 'Unofficial channel, not affiliated with <org>.' in the description with every source URL and a chapter list.
- Cost: voice about Rs 1.5 per minute incl. GST (gemini-3.8-flash-tts, one model per video); a 3.5 min digest is about Rs 5. Images, music and render are free. Generator pattern: stories/025_ai-news-digest-2026-11-05/gen_deck.py.
