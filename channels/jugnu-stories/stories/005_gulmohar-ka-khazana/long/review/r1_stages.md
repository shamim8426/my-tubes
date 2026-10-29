# Munshi R1 — stages (images, audio, shot plan, thumbnail/cover, cost) — story 005 long_04 + short_01

Date 2026-10-21 · RULES 15 auto · Verdict: **FIX** (all free) · STOP: none (balance ₹176.56 ledger, no copyright doubt, channel not touched)

## Measured
- Images: 14 scenes + Pandey painted sheet, all 1376x768 / 1K, 15 new (<= 16), no regens. Painted look in all. Looks = painted sheets (Golu, Tara, Tinku thin + orange-cream stripes everywhere, no cap/scarf/mark/wand; Dadi; Pandey; Mitthu no hands, throat plain green in 4/5/10/14/15/16, tiny dark chin line in 2 and 7). Children innocent. Lookalike question (12a) for every image + sheet + thumb + cover: Nahi. No readable writing: map 3 = scribble strokes, map 4/6/7 = pictures/squiggles, photos 13/14/15 no text. name_guard OK (prompts, script, both meta).
- Fixed scenes: 7 = hiding at the wall, Tara studying the map (ok for lines 14-15 via scene 8 crops); 12 = torch on, Tinku's hand only at the opening (ok); 10 = Golu pumping with full water (see M1).
- Audio: voice.wav long 237.40 s (first word 0.50 s, intro ends 8.93 s, last line ends 230.40 s, +7 s hold) = 3:57.4 <= 4:00. Short 36.69 s (last line 34.69 + 2 s) in 35-40. 51 TTS files = 51 cost rows; every clip has >= 0.23 s tail (no cut words), peaks <= -0.5 dBFS, voice.wav no clipping (chorus line 43 incl.). Voices from scripts/voices.py: narrator Charon, Dadi Gacrux, Golu Leda, Pandey Algenib, Tara Pulcherrima, Tinku Achernar, Mitthu Laomedeia. Median F0 Tara ~214 Hz vs Tinku ~304 Hz (well apart). Whisper text check happens in the final build.
- afade "Result too large": only when the LAST music segment is < 1.5 s (fade st = length - 1.5 < 0), i.e. the --seconds 1 test. Full builds: long last mood run (seekh) ~47.9 s, Short last run (jaadu) ~10.4 s -> cannot happen. No fix needed; optional hardening in build_audio: d = min(1.5, length), st = max(0, length - d).
- Cost: story_budget = ₹92.34 + GST ₹16.62 = ₹108.96 (cap ₹110). Final build ₹0. Note RULES 1: +52% vs the per-call estimate column (₹71.82), but equal to PLAN.md (~₹108).

## BLOCKER (free)
- B1 Short line 3 (Tinku "मैं? अंदर मकड़ी...") 11.97-19.10 s: Tinku NOT in frame (safe_rect picked box [0.5..0.6] because the shot's fy 0.45 is nearer that box; crop moved 0.77 -> 0.57). Fix: shot [0.5, 0.5, 1.0, 0.79, 0.5] -> Tinku at 28-63% of crop (verified).
- B2 Short scene 12 (lines 4-5): shots.json subjects "12" do not match the image -> Tinku's face sits at 86-100% of the crop (button zone), hand in the crack not shown. Fix: subjects "12" = [[0.33,0.3,0.51,0.75],[0.53,0.35,0.70,0.80]]; line 4 shot [0.5,0.5,1.0,0.44,0.5]; line 5 shot [0.5,0.4,1.1,0.42,0.5] (verified: face, hand at crack, torch inside 3-85%).

## FIX (RULES 13 > 8 s, free)
- F1 Short lines 1+2 (both narrator = one shot) 11.97 s: line 1 "shots": [[[0.5,0.45,1.0,0.55,0.5],6.0],[[0.5,0.5,1.25,0.57,0.5],null]] (6.0 + 5.97 s, verified).
- F2 Long line 35 (Tara) 10.87 s: "shots": [[[0.5,0.25,1.5],5.0],[[0.515,0.6,2.0],null]] (second = photo insert while she reads the names).
- F3 Long line 38 (Dadi) 13.40 s: "shots": [[[0.62,0.42,1.7],6.5],[[0.55,0.5,1.25],null]].
- F4 Long lines 41+42 (Pandey, same speaker -> line 42 shot ignored) 8.99 s: line 42 "scene": 13, "shot": [0.515,0.6,2.0] (photo insert on "ये तो मेरे बाबूजी हैं"; also hides the scene-15 photo, M3). Alt. without revisiting scene 13: line 41 "shots": [[[0.2,0.42,1.6],4.6],[[0.42,0.4,1.3],null]].

## MINOR (free in R1)
- M1 Scene 10 shows water already flowing while lines 19-20 ask for the pump (water/handle in the Tinku and Tara crops). Fix: lines 19-20 "scene": 9, shots 19 [0.78,0.55,1.7], 20 [0.5,0.55,1.7]; line 18 stays sc10 Mitthu close (no water in that crop).
- M2 End screen: Dadi close [0.12,0.6,1.7] runs 215.94-220.44 (3 s into the last 20 s), and close [0.3,0.55,1.25] puts Tinku at ~74% width. Fix line 48 "shots": [[[0.12,0.6,1.7],1.45],["wide",7],[[0.25,0.55,1.15],6],["wide",null]] (all <= 8 s; line 49's shot is ignored, same speaker).
- M3 Photo continuity: scene 13 = four children; scene 14 = one young woman; scene 15 = bald man. Covered for line 42 by F4; optional line 39 ("गोल-मटोल बबलू कौन है") "scene": 13, "shot": [0.46,0.6,2.2] on the chubby boy.
- M4 Long line 8 Mitthu shot [0.66,0.3,1.9] cuts his body at the bottom -> [0.66,0.4,1.9].
- M5 Thumbnail: line 2 "ये खज़ाना?" white on cream sky, weak at 160x90; letters ~11% of height (< 12%). Re-render text only: both lines yellow (or darker panel), font +15%. Matras OK, no title repeat, no Dadi/Pandey/photo/twist, bottom-right clear, 1280x720 1.45 MB.
- M6 Short cover: label "किस्सागो" (pos y 341) is hidden under the title (title spans 15-37.5%). Re-render text only: label at 15-19%, title smaller (~170) in ~20-36%, no overlap. Matras OK (डिब्बा), text inside 15-85%, hero Tinku 42-52%, Golu/Tara faces 64-73%, no spoiler, 1080x1920.
- M7 Register: no rows yet for 005 (14 scene images, characters/pandey/sheet_painted.png, long_04_thumbnail.png, short cover). Add 17 rows (format of 004 rows 89-102).
- Notes (carry_over, nothing regenerated): scene 11 Tara not pushing her hand (line 24); scene 13 two tops vs "एक लट्टू"; map design differs between images 2/3/4/6/7; Tara small bindi in scene 6; scene 3 three hands around the map; Mitthu chin line in 2/7; meta narrator speed 1.0 (PLAN said 0.95) - length fine anyway.

Builder: verify the changed shots with a --plan / shot-time print before FINAL (scene 13 revisit in F4/M3). Report parallax vs zoom count per shot in the final (carry_over).
