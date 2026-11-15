# DOCUMENTARY EDITING PLAYBOOK (all channels, long explainers 8-20 min) - a procedure, not an essay

Born from Reality Check 001 (asteroid defence), 2026-11-08. Sources: `channels/reality-check/stories/001_asteroid-defence/long/{edit_style_study,visual_audit,footage_map_fixes}.md`, `channels/reality-check/brand/STYLE_LEARNINGS.md`, `shared/STYLE_LIBRARY.md`. Principles only; never copy another channel's frames, words or titles (RULES 12, 12c). Copyright rules always win.
Used by: Kalam (write script so every line can be shown), Sampadak (edit plan), Kaarigar (build), Munshi (checklist G).

## A. BEFORE BUILDING: the shot table (mandatory, nothing is built without it)
Write `<video folder>/shot_table.md` with ONE row per script line (line numbers = voiceover lines):

| line | claim (what is said, 1 short phrase) | visual type (see B) | source: real / animation / mix | in-out (s, from timing json) | overlay (label text + word it lands on) | sound cue |
|---|---|---|---|---|---|---|

Rules:
1. Every line has a MOVING visual that shows the claim. Banned as the content of a shot: a text card, a static image, a static chart, an unrelated clip ("generic space footage"), a clip that was chosen only because it looked nice.
2. A card (text/number/rule) is allowed only as the END of an animation (it builds on and holds 1.5-2.5 s).
3. Check each row with this question: "If the sound were off, would the picture still tell the viewer what is being said?" If no, redo the row.
4. A clip may be used for ONE claim only. Reuse of a clip for another claim = filler = not allowed.
5. If no real footage truly shows the sentence, DRAW our own animation (free, code). Never fill with something close.
6. Audit an old build the same way (see `visual_audit.md`): verdict per shot ok / weak / card / static, then fix every non-ok row.
7. Fix list for bad footage goes in `footage_map_fixes.md` (clip, problem, fix) and is applied via `footage_overrides.json`, not by editing the map.

## B. LOOKUP: statement type -> what to show
| statement type | show |
|---|---|
| a number / size ("140 m") | SCALE LADDER: continuous zoom-out, object next to a known one (bus, city strip, scale bar); rung label on the spoken number word |
| a comparison ("7 vs 33") | split screen or a two-ball demo; ghost (expected) vs real result slams over it; counter running |
| an event / disaster | real footage trimmed to the peak, or reconstructed top view + side view (expanding blast ring, trees falling radially, dots reacting) |
| a process / mechanism | ONE picture, ONE moving part, a one-line rule that builds on after the motion; no formula |
| a time / duration | clock or timeline bar with a running counter; period bar filling; years -> months -> days ladder |
| a prediction / probability | chart DRAWN LIVE (line grows, uncertainty band opens, flash at the key point); never a pasted static chart |
| a method / option list | mini-demos in sequence, 6-8 s each, same 3-part layout (craft / rock / result), then a table built row by row |
| a definition / jargon word | one orange arrow or label on the moving picture; show it, say it once, move on; no formula (a hard equation may be shown 2-3 s with "one idea") |
| a source / fact claim ([n]) | our own neutral source card shown 2-3 s, key phrase highlighted yellow while it is read; credit chip for real media |
| a question / hook | the unanswered visual (empty telescope cone, "?" gap, ghost orbit) so the viewer waits for the answer |
| a conclusion / verdict | calm real footage (slow push) + verdict stamp or status card at the END; last 20 s nothing essential (end screen) |
| a repeated key word (e.g. "dhakka") | ONE fixed symbol (same colour, same direction) every time; first time word and symbol appear together, later it only pulses 0.3 s on the word |
Palette per meaning, fixed for the video: navy bg, orange = our push/spacecraft, cyan = asteroid/object, red = unknown, green/teal = status.

## C. RHYTHM
- Shot length: median 4-6 s, average about 6 s. Cuts per minute follow difficulty, NOT a flat rate: calm intro and verdict 7-9; normal 9-11; hardest explanation block 14-20.
- Hard cuts by default. A 5-8 frame warm flash (orange/yellow) ONLY at block boundaries (chapter start, each REVEAL, the answer): about 1 per 40-60 s. Never on every cut.
- Never hold more than 7 s without a sub-cut or camera move (RULES 13 max 8). 10-14 s only for a drawn animation that keeps one part moving.
- No shot under 1.5 s except number-flash bursts (max 3 per minute).
- Labels land ON the spoken word (0 to +0.3 s after it, never before) and hold 3-4 s; one fixed box style (bottom third, 5-6% height, bold); max 2 text items on screen. Name/year chips appear when spoken.
- A picture that introduces a new object leads the voice by 0.2-0.5 s; it never lags.
- Strong footage gets a SILENT HOLD (no label, no SFX, voice may rest) of 1.5-3 s.
- Breath space = 0.5-0.8 s visual hold, never dead audio.
- Every still moves: push 1.00 -> 1.06 or parallax; every graphic moves each frame.
- Verify with scene-detect: cuts/min per chapter and a "no shot > 7 s without change" report.

## D. FOOTAGE RULES
- Licence: public domain with credit chip (bottom-left, 70% opacity, first 4 s). SKIP clips with co-credit (e.g. a private company), identifiable faces, narration, baked text/logos/captions, or a doubtful licence. Log in `shared/assets_license.csv`. When in doubt: ask, do not use.
- Dirty clip: crop (fractions of the SOURCE frame) to hide baked text/pillarbox, or choose a clean time window; check the whole clip for black starts, red dropouts, graphics, faces (face scan) before choosing the window.
- Low-res (<720p) or weak clips: use only as a DIMMED, softly blurred BACKGROUND under a small card or animation, never full-bleed.
- Real footage 2-4 s, trimmed from the first MOVING frame to the last informative frame; never play a clip whole.
- Targets: about 50-75% of the runtime real or real+animation mix; the rest own animation. No people-face stock, no film clips.
- AI stills (free flux) only for true gaps, with parallax and an "AI illustration" chip; never for evidence.
- Look every used clip/still in a frame before the map is final (poster or 3 frames). A map made from filenames only is wrong.

## E. SOUND
- A mood bed per section (calm / mystery / tension / reveal / outro), continuous, no dead air; music about 13 LU under voice in speech.
- SFX at the event itself (impact on the impact frame, tick on a label); max one SFX per beat; SFX peaks 18-26 dB under the voice RMS; ambience about 30 dB under; never inside the first 0.2 s of a spoken number.
- Duck music 0.25 s on hits/flash boundaries; voice stays on top.
- Levels: voice about -15 LUFS, final mix -14 LUFS (two-pass loudnorm, TP -1.5), LRA under 4 LU.
- One cue per visual event; plan cues from `shot_specs.json` + timing json (never fixed seconds), so a TTS redo moves them.
- Silence (a 0.3-0.6 s drop of the bed) BEFORE a reveal, then the hit.
- Real footage may play with its own sound only if licensed and clean; otherwise our SFX.

## F. BUILD PROCESS (Reality Check chain; copy the idea for other channels)
Chain: `tools/rc_build_long.py <NNN>` (per-shot render from `long/shot_specs.json` + `audio/voiceover_timing.json`, cache `cache/<channel>/<NNN>/shot_<n>_<hash>.mp4`, only changed shots re-render) -> `tools/rc_real_look.py` (real-footage look, called by `--look real`, the default; reads `long/footage_map.md` + `footage_overrides.json`; overrides can carry `"scene": {...}`) -> `tools/rc_explain.py` + `rc_explain_*.py` (own animated scenes, `SCENES[name]`; one animation can run across several shots with `sync`) -> `tools/rc_sound.py <NNN>` (synthesised SFX/beds, stems, loudnorm, REMUX with `-c:v copy`).
Exact final assembly (the part that went wrong):
1. `rc_build_long` / `rc_real_look` write `cache/.../list_real.txt` ONLY (the concat list). They do not produce the final file in real mode.
2. Concat VIDEO-ONLY: `ffmpeg -f concat -safe 0 -i list_real.txt -c copy long/output/<NNN>_long_preview_oldsound.mp4`.
3. Then run `python tools/rc_sound.py <NNN>`; it remuxes voice + music + SFX into the final long preview from that `_oldsound` file. Always check the file you deliver was written AFTER this step.
4. Never bump `VER` / `TK_VER` for convenience: it changes every hash and WIPES the cache (full rebuild, hours). Bump only when a look changes on purpose; scene functions are already hashed by their own source.
5. Check frames at the MIDPOINT of each line (not at the cut) and compare with the spoken text of that line.
6. Check A/V sync: shot start times in the concat vs `voiceover_timing.json` line starts (tolerance 1-2 frames); after concat, total duration = audio duration.
7. Send a person only a 360p copy under 28 MB; keep the full file local. Name the file with its build time and say which sound pass it has.
8. Machine load: use at most 6 workers (`--workers 6`, `--plx-workers` 3-5); more freezes the PC. Run long builds in the background, report real time after.
9. Always `--shots N,M` / `--seconds N` for a test first; full build only when the proof looks right.
Mistakes made on 2026-11-08 (do not repeat):
- Sent the OLD-look video after a remux (the remux used an old concat). Fix: step 3 check + open a frame of the delivered file before sending.
- Text cards that explained nothing (card repeated the sentence). Fix: section A rule 1-3.
- Gemini TTS daily cap = 100 requests/day on the key, SHARED by all channels (hit at line 92 of 160). Check `scripts/daily_spend.py` / quota before a TTS run; plan big TTS across days; finish a story's voice with ONE model (re-do draft lines on the main model after reset).
- Machine overload from 10 workers while other jobs ran. Fix: 6 workers max.
- Footage chosen by filename: black starts, baked text, talking heads, co-credit. Fix: section D look-first.

## G. CHECKLIST for Munshi / Sampadak (every long video; PASS only if all 10 are yes)
1. `shot_table.md` exists and every script line has a moving visual; no text card, static image or unrelated clip as content.
2. Frames at line midpoints (every 5th line + all reveals) match the spoken text.
3. Statement types use the section B visual (numbers = ladder, mechanism = one moving part, probability = live chart).
4. Median shot 4-6 s; no shot > 7 s without a sub-cut/move; cuts/min follow difficulty; flashes only at block boundaries.
5. Labels land on the spoken word (0 to +0.3 s) and hold 3-4 s; max 2 text items; Roman text, plain digits.
6. Every real clip is licensed (PD + credit chip, no co-credit/faces/baked text), logged in `assets_license.csv`; low-res only as dim background; real+mix 50-75%.
7. Sound: bed continuous, SFX on events, loudness -14 LUFS (voice about -15), LRA < 4, silence before reveals.
8. A/V sync checked (shot starts vs timing json; video duration = audio duration).
9. The delivered file is the post-`rc_sound` remux (not `_oldsound`), a frame of it was opened, 360p copy < 28 MB for review.
10. Cost and quota logged (TTS requests today, story spend vs cap); `log.md` + `carry_over.md` updated; STYLE_LIBRARY gets any new learning.

## H. CRAFT STANDARD (user 2026-11-14, from video 002 on): I decide music, editing grammar and explanation method myself, like a professional documentary editor. Do not ask the user to choose these.
Music (a score, not a bed):
1. Write a cue sheet from the script's emotional arc BEFORE picking tracks: hook (suspense, sparse) -> world/context (warm wonder) -> trouble rising (pulse, low strings, percussion) -> peak/reveal (impact hit, full swell) -> explanation (restrained, steady) -> hope/recovery (uplifting) -> why it matters (serious) -> end (resolution, long fade). At least 3 clearly different energy levels per film; one recurring theme returns at start/end.
2. Pick real melodic tracks with progression (not minimal piano loops, drones, meditation tracks, ostinato 'trance' loops, white-noise pads). Check objectively: tempo, onset density, spectral centroid, RMS dynamics over time, self-similarity (repetitiveness). Reject tracks that sound the same all through.
3. Music is audible but subordinate: about 12-16 LU under the voice on speech (research 2026-11-14: underscore ~-18 dB vs voice -6 to -12; my earlier 21-24 LU was too quiet and the music vanished; finish by ear, never near-silent for minutes, never drowning), side-chain duck on speech, swell +3 to +6 dB in silent holds and at section changes, hits aligned to reveals (e.g. the big number), silence just before a key number so it lands. Crossfade tracks 4-6 s on the section boundary.
4. Send the user VIDEO clips with the mix (never audio-only), 3 moods: opening, peak, ending. Free commercial-safe sources only; log licence rows + description credit.
Editing grammar (documentary):
5. Sequence: establishing wide -> detail -> context; every line its own picture, never repeat an image except as a deliberate callback; motivated cuts only; hard cuts for energy, dissolves for time passing/section change; J-cut/L-cut (picture leads or trails the voice by 0.3-0.5 s); slow push-ins/parallax on stills; one consistent colour grade (mid-tone), subtle vignette/grain.
6. Explaining: show the idea in a HALF/side/bottom panel over live footage, never a full-screen block; build step by step (one new element per beat), analogy first then number, scale comparison for big numbers, say the key number once and show it once; maps: globe/zoom-in to the region, pins and labels appear on the spoken word; chapter titles at section changes.
7. Structure: hook in 15 s (the question/most striking fact), promise, evidence, mechanism, counter-view/uncertainty (label estimates), so-what, short takeaway; a one-line recap about every 3 minutes; plain spoken Hindi.
Process: before every new video, re-read this section, write the cue sheet and the shot table, make a 60 s sample with picture + music (not audio-only), get the user's OK, then build.

Research-backed additions (research/documentary_craft_2026-11-14.md):
8. 3-5 distinct cues per 12 min with entrances and exits, not one looped bed; build energy by LAYERING (pulse, then strings) rather than changing tempo; bring one theme back at the thesis and the end.
9. Music dropped to near-silence or a low drone just before the key reveal; cues after silence hit harder; keep diagnostic ambient sound; no vocals; cut low-end mud and busy mids under narration.
10. Visual/sound reset (new shot type, panel, sound change) roughly every 8-20 s in the first 30 s, then every 25-45 s; do not over-edit; resolve every open loop honestly; check our own Studio retention graph after each video and note dips in learnings.
11. Music licences: Pixabay (no attribution, but keep the licence certificate per track, Content ID claims still possible), YouTube Audio Library filter 'Attribution not required', Kevin MacLeod CC BY 4.0 (exact credit line), Uppbeat free tier (per-video credit, ~3 downloads/month), Free Music Archive only CC0/CC BY (no NC/ND). Log every track in shared/assets_license.csv.
12. EVERY on-screen event gets a fitting sound (user 2026-11-14): eruption/lava (rumble+crackle), explosion/impact, waves, wind, fire, bubbles, ticks for timelines and counters, map pin/line draw, bars rising, gauge, graphic in/out whoosh, globe rotation, section riser + hit; plus ambient beds per scene type. Audible, ~10-14 LU under the voice peak, never over key numbers or sentence starts. Build an event list (line -> event -> sound) from the shot table.
13. Next-video rule (user 2026-11-14): follow the analysed reference style fully (research/study_ref_QsHQxRlBy6Y.md checklist): graphic per statement type synced to the word, side/bottom panels, number ladder then human unit in 5-8 s, one analogy with its own picture about every 1.7 min and a question about every 1.5 min, opposing source shown as prominently as the supporting one, honest 'research still going on' ending, picture change at least every 5 s (median ~4 s), warm flash only at pivots, plan real 2-4 s pauses in the TTS after pivot lines so music-off moments are audible.
