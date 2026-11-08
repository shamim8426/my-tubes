# 001 visual audit and v3 rebuild notes (2026-11-08)
Audit of the previous build (contact sheets of cache real/ clips, one frame per shot; sheets in cache/reality-check/001/audit/sheet_*.png). Shot number = script line (154 shots). Verdicts: ok / weak (footage does not show the line) / card (text or number card is the content) / static (chart or box that does not move).

## Audit of the old real-look build (v2)
| lines | what the old shot showed | verdict | v3 action |
|---|---|---|---|
| 1-3 | real DART impact replay, DRACO approach, speed chip | ok | kept (real) |
| 4-8 | blurred stills with number chips (7 min, 33 min, 73 s), small orbit icon | card/weak | scene dhakka_main: hit, push arrow, orbit shortens with counter, 3 dials |
| 14-16 | Milky Way still + "Chapter 1" card; Earth loop; Trinity photo with number card | weak/card | scenes earth_incoming, airburst_years, airburst_city |
| 17-21 | plume model + ~500 kt card, ~1,600 card, AI window still | weak/card | scene chely: fireball, blast ring, 1,600 dots, flash then late shock wave breaks windows |
| 22-23 | blurred Sun video with diagram on top | weak (Sun footage unrelated) | scene unseen: Sun-side approach, empty telescope cone |
| 24-27 | Kulik photo / AI forest / Barringer crater (wrong crater) / range bar | weak/static | tunguska_date, airburst_side (height 5-10 km, trees fall radially), trees_top, estimate_swarm |
| 28-32 | different asteroid photos + size cards | weak (stills, no scale) | scene size_ladder: continuous zoom-out, city strip and scale bar, rung ladder |
| 33-34 | Chicxulub radar still + bars; Mt St Helens + bars | static | scene extinction (dust darkens Earth, species fade; volcano) |
| 35-38 | meteor video + static chart; ISS night + status card | static/card | rare_ladder (timeline with flashes + uncertainty band), known_unknown |
| 39-45 | launch flash, DART illustration, size/period chips over stills | mixed | can_we_push, acronym (real bg), pair_scale (real DRACO insets), safe_target |
| 46-48 | launch footage, DRACO frame + chips, illustration | ok/weak | 46 kept real; journey scene; 48 real impact replay (final approach to flash) |
| 49-56 | empty "Akela dhakka" card, bars over stills, SVS orbit still | card/static | push_basic (two balls, one orange arrow), crit73, result_orbit |
| 57-60 | radar dish photo with numbers, checkmark card, PEHLI BAAR text on black | card | two_methods (light curve + radar), still_orbiting |
| 61-62 | AI still with "?", survey text | weak | clue, then survey sweep |
| 63-71 | NEO count video with cards, dot grids over blur | card/static | survey_sky (sweep, telescopes, blink compare), dots_found (95 of 100, 25,000 grid) |
| 72-80 | goal bars, NEO Surveyor renders with chips | static/card | goals timeline, neo_surveyor (dark rock vs infrared glow, launch date) |
| 81-88 | line charts drawn static, name card | static | yr4_chart (drawn live), film_vs_real |
| 89-96 | Apophis render + bars, orbit diagrams | weak | apophis (size bracket, 32,000 km flyby inside satellite ring, 100-year bar, 2.7% curve) |
| 97-110 | the push: boxes with arrows over stills ("beta = 1" cards) | static/card (this was the user's main complaint) | recap_dials + push_full: sticky ball, rubble pile, debris, ek dhakka + extra dhakka arrows stack, beta 1 / 3.6 / 2.2-4.9, 2.7 mm/s, laps add up |
| 111-114 | AI ejecta stills, range bars | weak/static | ejecta (cone, pinwheel, ton blocks, range bar) |
| 115-124 | boxes over footage | card | mass_unknown, solar_orbit, summary3 |
| 125-137 | one box row per method over SDO/DART stills | static | method_demo/tractor_demo/laser_demo (craft, rock, result path), exercise (4 lanes with checks), nuclear (standoff burst), nuclear_caveats |
| 138-140 | two empty boxes, unrelated stills | card | film_plan (timeline bars, diverging paths) |
| 141-148 | AI Hera still, solar-system chart with chips | weak | hera (route draw-on, orbit with job list, cubesat release, arrival timeline) |
| 149-159 | empty rounded boxes over blurred asteroid | card | unknowns, verdict (stamps appear on the spoken verdict), final3 |
Totals (154 shots): ok 5, weak 49, card/static 100. After v3 only lines 1-3, 46 and 48 are real footage; 146 shots are own motion graphics; 2 real shots have no overlay.

## Method
Own code only (numpy/OpenCV/Pillow -> ffmpeg), rs 0: tools/rc_explain.py (toolkit), rc_explain_scenes.py, rc_explain_a..e.py (scenes), integrated through `scene` keys in footage_overrides.json (rc_real_look.render_real; VER not bumped). Generator: long/_gen_overrides_v3.py (previous overrides: footage_overrides_v2_backup.json). Colours: orange = ek dhakka (craft push), gold = extra dhakka (debris), amber = labels, cyan = asteroid, red = unknown. Master scenes run across several lines (sync key), so one animation continues over cuts. Hard cuts; warm 7-frame flash only at chapter starts and the two reveals (lines 5, 14, 39, 63, 97, 104, 124, 141, 152).

## Step A notes (first 5 minutes, lines 1-62)
- Rendered 54 new shots in 870 s (11 workers). 001_v3_first5min.mp4 = v3 picture + the existing final mix audio of 001_long_real_v2.mp4 (voice timing unchanged); the full re-mix (rc_sound.py) comes after the full build.
- Frames at line midpoints checked for lines 1-62: each shows what the line says (size ladder with scale bar for 28-32, ball + arrow for 49, orbit counter for 53-54, etc.).
- Known small issues: line 6 mid-frame is nearly empty (rock + pause before the 'extra dhakka?' arrow); line 16 sub-label overlaps the number box slightly; the two-methods panels (57) are small. Long shots without a hard cut run inside master scenes (they change every 4-7 s by view or animation phase).

## v4 (2026-11-08): real NASA footage mixed back in (REAL / MIX / ANIM)
- Generator long/_gen_overrides_v4.py (v3 overrides kept as footage_overrides_v3_backup.json; VER not bumped, 135 of 155 shots re-rendered, 20 cached). New code: scene['mix'] in tools/rc_explain.py = real sub-cuts (mode real: full-bleed footage + credit chip + small caption) and under-layers (mode under: real footage/still dimmed and softened behind our animation, scene drawn on black and keyed over it); scene['punch'] = slow 1.00-1.05 camera push on drawn shots of 8 s or more.
- Screen time (1026 s of lines): REAL full-bleed 143 s (14 percent: DART approach/last images/launch, Chelyabinsk plume, SOHO, perseids, NEOWISE, Apophis animation, Catalina, telescope/light-curve stills, Chicxulub relief, ISS/Orion Earth), MIX 634 s (62 percent: our push/beta, orbit, ladder, survey and method animations over real DRACO/Dimorphos stills, NEOWISE, Apophis radar, Sun, Earth, nuclear-test photos), ANIM only 249 s (24 percent: Tunguska, size rungs 29-31, rare ladder, methods tractor/laser, film plan, verdict, etc., no matching real footage exists).
- Fixed: line 76 (real NEOWISE for 4.2 s, panels after), line 6 (rock now sits on real Dimorphos boulder field), line 16 sub-label moved down (no overlap), long drawn holds get a camera push.
- Check: shot starts vs voiceover_timing starts, 0 of 154 lines out of 0.05 s tolerance (155 clips, 1124.13 s). 12 midpoint frames (lines 4, 17, 22, 32, 50, 57, 67, 76, 89, 103, 125, 157) show what the line says.
- Remaining weak: line 125 (12 s) has only a 4 s real cut then one animation; Tunguska 24-27 and size rungs 29-31 have no real footage (kept drawn); real clips of 360p (Chelyabinsk plume) look soft; some under-layers are stills with slow drift only; Hubble DART ejecta (111-112) and Hera (141-148) have no real footage in the library (DRACO stills used).
