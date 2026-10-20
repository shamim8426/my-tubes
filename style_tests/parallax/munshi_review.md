# Munshi review: 2.5D parallax style test (story 004 images 02/04/05/06)

STEP: style test (not production, no upload)   PROJECT: 004_chhat-par-bhoot images   VERDICT: FIX (2 BLOCKER, 5 MINOR, all free)
Date: 2026-10-20. Round: R1. STOP condition: none. Cost: Rs 0.

## What I checked (my own frames, not the builder's)
- ffprobe on all new/old/short/compare clips.
- Start / middle / end frames (n=0, 90, 179) of every new and old clip; full-res crops (start|mid|end) of Golu+Mitthu, Dadi (04), Kamla hand, rug, Pandey, wires/flowers (05), Mitthu wings, lathi, Pandey face (06), white figure + clothesline (02); source images scaled to 1920x1080 for side-by-side.
- Frame-to-frame difference curve (tblend + signalstats) for jitter.
- Caption band (bottom 25%) max luma on scene_02 (fireflies).
- Model config/README, licence register row, .gitignore, grep for Base/Large/Giant.
- git status: no paid source file in channels/ changed.

## Tech
All new clips: h264 High, yuv420p, tv range, 30/1 fps, 180 frames = 6.000 s. Long 1920x1080, Short 1080x1920, compare 1920x540. colorspace bt709, but color_primaries/transfer untagged (same as the old make_short clips).

## BLOCKER
- B1 scene_02: the white figure on the roof (the story's "bhoot", key subject) has its head cut by the top edge for the WHOLE clip and more at the end (push_in). Old zoom starts at full frame (figure complete). Cause: constant OVERSCAN 1.08 (parallax.py line 48) plus the push_in. Same overscan crops ~4% off every edge in every clip (scene_06 Pandey's shoes touch the bottom edge). Free fix: overscan only as much as the move needs (~1.03-1.04 for amp 0.035), and/or a subject-safe check (key subject bbox stays >= 3% inside the frame at every frame, else pull_out / smaller amp / cy shift).
- B2 scenes 05 and 06 (daylight, busy backgrounds): visible edge smears at full res. 05: grey ghost beside Kamla's raised hand/wrist, smeared fringe at Pandey's elbow over the blue wall, ghost strip between Mishra's rug and Pandey's arm (end frame), streaks at the flower tips / wires (end frame). 06: green/pink streaks next to the top of Pandey's lathi and his hand (start frame), streaks left of the cap (end frame). The guard reported "ok" although jump = 0.32 (05) and 0.14 (06). Free fix: stricter guard on depth jump (e.g. jump > 0.10 -> halve, > 0.25 -> Ken Burns fallback), wider plate inpaint/feather, or amp 0.0175 for busy daylight scenes. Re-render the same 4 test clips after the fix.

## MINOR
- m1 scene_04: Dadi's walking stick (bible prop) is outside the frame for the whole clip (overscan); old zoom shows it at the start. Fixed by B1.
- m2 scene_04: small soft green/grey smear between Dadi's raised arm and the saree shoulder.
- m3 color_primaries / color_trc untagged; add bt709 tags to the encoder (old clips same).
- m4 short_scene_04: Golu's pointing finger goes to ~93% of the width at the end (right 15% = YouTube buttons). Use cx a little left or pull_out for this shot.
- m5 render time 1.5-3x the old zoom (see Speed).

## What is good
- scene_04 Golu + Mitthu (feathers, hair, fan) and Dadi's hair/glasses: clean, no halo, no face wobble.
- scene_06 Mitthu's spread wings: clean edges, no feather tearing.
- Motion: cosine ease in/out, smooth curves, no frame spikes (max deviation 0.05-0.10 on a 0.3-3.3 scale). Presets fit the mood (02 push_in tension, 04 static_breathe tension, 05 pan_left comedy, 06 gentle_orbit khushi). Subtle, not swimmy; 05/06 move more (busy images), still OK.
- Overlays: fireflies (02) and dust (04) small and faint, kept in 5-75% height by code; the caption band shows nothing extra.
- No edge/border shows in any frame.

## Licence
models/depth-anything-v2-small: config backbone hidden_size 384, 6 heads (= ViT-S, Small); README "license: apache-2.0", "Depth Anything V2 Small". Register row present (Apache-2.0, notes Base/Large/Giant CC BY-NC not used). parallax.py loads only models/depth-anything-v2-small and asserts hidden_size 384; HF cache only has Depth-Anything-V2-Small-hf; no Base/Large/Giant anywhere in code. models/ and *.mp4 are git-ignored. OK.

## Speed (report.json, wall time per 6 s clip)
- No overlay: 17-19 s wall (CPU 50 s). With overlay: 36-40 s wall (CPU 73-77 s). Old zoom: 12.6-14.2 s.
- Long ~3:45 (~32-38 shots, <= 8 s): ~12 min wall without overlays, up to ~25 min if every shot had overlays; realistic mix ~15-18 min (old zoom ~8 min). Only once per scene; cache reuses it.
- Short 40 s: ~2 min without overlays, ~4.5 min with.

## Recommendation
Do not make parallax the default yet. After the free B1 + B2 fixes, re-render the same 4 clips + Short and give them to Munshi for R2. If R2 is clean: parallax default with the stricter guard (night/simple scenes parallax, busy daylight scenes auto-fallback to halved motion or Ken Burns).

---

# R2 (2026-10-20, re-rendered clips 09:04-09:07)

VERDICT: PASS-WITH-NOTES (0 BLOCKER, 2 MINOR -> carry_over for the parallax rollout). STOP: none. Cost: Rs 0.

## Re-checked (own frames n=0/90/179, full-res crops, ffprobe, diff curves)
- Tech: all 5 clips h264, yuv420p, 30 fps, 180 frames; colorspace/primaries/transfer now bt709/bt709/bt709 (m3 fixed).
- B1 fixed: scene_02 white figure complete (head + feet) in start, mid and end frames, clothesline poles in frame. scene_06 Pandey's and Golu's shoes fully in frame. scene_04 Dadi's stick visible all clip (m1 fixed).
- B2 fixed: scene_05 now Ken Burns fallback (guard: jump 0.32) - Kamla's hand, Pandey's elbow, rug edge, wires all clean, same look as the old zoom. scene_06 at amp 0.0175: lathi, hand, cap, Mitthu wings clean; only a very faint streak next to the lathi top (start frame) and left of the cap (end frame), not visible at normal size.
- m2 fixed: no smear between Dadi's raised arm and the saree shoulder.
- Motion: scene_06 eased curve, no spikes (max 0.08); scene_05 flat linear zoom (as old).

## MINOR (remaining)
- R2-m1 short_scene_04 (cx 0.64 overcorrected): Golu's pointing hand is now cut off by the right edge for the whole clip (the "pointing at the roof" action is lost), and Mitthu sits at ~90-98% width at the end (right 15% button zone). Free fix: cx ~0.68-0.70 with pull_out (or static_breathe), so Golu + Mitthu + the hand sit inside 0-85% width; check each Short crop with frames.
- R2-m2 scene_06: faint residual streaks at strong edges even at half motion (cosmetic). Optional: fallback threshold 0.25 -> ~0.20 for daylight/busy images.

## Speed (R2 report.json)
- Parallax 6 s clip: 29-40 s wall (CPU 70-82 s); Ken Burns fallback 26.5 s (depth + guard run first); Short 22 s. Old zoom 12.6-14.2 s.
- Long ~3:45: ~18-25 min wall; Short 40 s: ~2.5-4.5 min. Once per scene (cache).

## Recommendation
Parallax as the default motion for long videos: YES, with the current guard (fallback/halving is logged in report.json). For Shorts: yes, but every 9:16 crop gets a frame check (key subject + action inside 0-85% width, out of bottom 20%) until R2-m1 is handled in the builder.
