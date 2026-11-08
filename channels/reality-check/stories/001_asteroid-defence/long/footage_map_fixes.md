# footage_map_fixes - what is wrong in footage_map.md and how the builder works around it

Applied through `long/footage_overrides.json` (read by `tools/rc_real_look.py`; the map file itself is unchanged). `crop` = fractions of the SOURCE frame (hides baked text / pillarbox), `segs` = one entry per cut. Every clip/still used by the map was looked at (poster / frames); verdicts:

## Unusable as mapped (fixed by override)
| shot(s) | clip | problem | fix |
|---|---|---|---|
| 1, 2, 8, 50, 59, 125 | footage/jhuapl_dart_impact_replay.mp4 (= svs_dart_impact_replay_1080p.mp4, identical) | 0-28 s is black (mean luminance 0-3); picture is a 1024 px square with black pillars; red dropout after ~34.5 s | window 29.0-34.2 s only (Dimorphos fills the frame, rubble rushing past), crop to the square [0.2333,0,0.7667,1] |
| 4, 97, 133 | footage/svs_dart_infographic_anim.mp4 | baked DART logo, 'Original orbit', 'Earth-based observations' | NASA DRACO / illustration stills with parallax instead |
| 3 | footage/draco_final_image.png | only the top 10 percent has picture (rest black) | draco_penultimate_image.png |
| 8 | footage/jhuapl_dart_before_impact_closeup.png | wire-frame mesh render, not a photo | replay window 29.3-34.4 (blurred under cards) |
| 15, 137 | footage2/earth/earth_fleet_vantage.mp4 | satellite names, NASA logo, captions baked in | airglow_iss.mp4 (clean ISS night Earth) |
| 10-13 (cut), 94, 158 | earth/black_marble_night.mp4 | captions baked at 0-8 s and later | Earth stills (iss_night_wiseman, orion_earth_2026, iss_aurora_kopra) |
| 17, 19, 20, 28 | history_impacts/chelyabinsk_bolide_plume.mp4 | date/observation read-out top-left (about top 12 percent), low-res 640x360, first 18 s very dark | windows 19-32 / 100-107 / 118-125 / 140-148 s, crop top 14 percent (1.16x zoom) |
| 18 | meteors/whatsup_nov2026.mp4 | collage of 3 clips, not a fireball | whatsup_perseids_2021 28-36 s (real meteor streaks), crop bottom 10 percent (credit text) |
| 19 | asteroids/neo_osirisrex_target.mp4 | white flare first, then green hazard graphic and 'NASA PLANETARY SCIENCE' / 'Name: 2012 DA14' text | dropped (also shot 28) |
| 24, 26 | history_impacts/tunguska_kulik_expedition.jpg | NEEDS USER OK (script: avoid expedition photos) so the old build fell back to a plain dot-grid graphic | free AI stills (Cloudflare flux, Rs 0): ai_stills/shot_024.png taiga from above, shot_026.png radial fallen trees; shown with 'AI illustration' chip |
| 30 | asteroids/eros_global.jpg | baked 'Anaglyphs / Stereo Pairs' | mathilde_mosaic.jpg |
| 35 | meteors/whatsup_perseids_2022.mp4 100-107 s | Saturn graphic with credit text, then empty dusk | perseid_ingalls_2.jpg (real Perseid photo) |
| 36, 63 | whatsup_perseids_2021 | 63 window runs into the 'AUGUST 2021' calendar graphic (about 40 s) | 36 = 28-31.5 s, 63 = 32-37 s |
| 39, 45 | launch/dart_isolated_launch.mp4, falcon9_crew2_drone.mp4 | co-credit (SpaceX) NEEDS USER OK, 640x360, so build fell back to graphic | footage/nasa_dart_recap_large.mp4 launch fire 37.5-43.5 and 38-45 s (NASA, clean, bright; after about 46 s the recap shows UI graphics) |
| 16 | scale_analogies/trinity_fireball_6ms.jpg | '0.006 SEC' scale bar at the bottom | crop bottom 15 percent |
| 68, 72, 76, 79, 81, 160 | asteroids/neowise_legacy.mp4 | map windows 43-50 s and 34-41 s are talking heads (two NASA scientists, faces), 58 s / 62 s baked titles | face-free windows (crop top 10 percent for 'ANIMATION' / "ARTIST'S CONCEPT" labels): 98-104, 50.5-55.5, 122-130, 160.5-166.5, 73.5-81.5, 154-162 s. Face scan of the whole clip: faces at about 6, 14-22, 38-48, 94, 106-118, 138, 146-150 s. |

## Still weak / not fixed (listed, low priority, mostly after line 91 or already blurred)
- footage/svs_bennu_keyhole_animation_1080p.mp4 (53 cut, 110, 139): blue animation with baked date counter ('august 2xx') and yellow sun, graphic look.
- footage2/comets/soho_comets.mp4 (55, 129): NASA Heliophysics title card and 'comet counter' graphics baked in.
- footage2/asteroids/neo_discovered_count_2023.mp4 (64, 67): baked 'NEAR-EARTH ASTEROIDS DISCOVERED TO DATE' title and the 32,266 counter (REAL-BG only).
- footage2/asteroids/psyche_animations_reel.mp4 (126): tiny spacecraft dot, graphic.
- footage2/observatories/webb_mirrors_trailer.mp4 (141): a slate with 'Title: Webb Mirrors Glamour Trailer' appears inside the 8-15.5 s window.
- footage2/craters/chicxulub_space_radar.jpg (33): narrow colour strip, very soft when zoomed (REAL-BG).
- footage/svs_yarkovsky_effect_720p.mp4 (56, 130): small asteroid on black with a white pointer line, plain.
- footage2/launch/lucy_rollout.mp4 (46): people and a building at night at 290 s, unrelated.
- footage/nasa_didymos_ridge_formation.mp4 (9 cut, 52, 145, 156): small coloured simulation on black.
- earth/iss_earth_views_hq.mp4, earth/orion_earth_timelapse.mp4: usable but plain.
- footage2/earth/iss_sunrise_exp7.jpg has a text strip at the bottom edge: crop bottom 8 percent if used.
- footage/nasa_dart_explainer_large.mp4: unusable as full frame (Spanish captions in the lower quarter); only a crop of more than 1.3x would hide them.
- footage/nasa_dart_recap_large.mp4: baked year titles ('2017', 'NASA' logo) except the launch fire window used above.

## Builder changes in the same pass (tools/rc_real_look.py, rc_build_long.py)
- `footage_overrides.json` (per-shot cuts, crops, windows), crop for videos and stills, exact windows, local per-cut time.
- Cut pace: a new cut about every 5.5 s (was 7/11 s steps); each cut of an override shot can be a different clip.
- REAL-BG look lighter (blur sigma 1.6 at 800x450, 66 percent brightness instead of 50 percent blur at 480x270).
- Chips/labels/credit chips sit on dark rounded panels (58-60 percent opacity).
- Depth-parallax clips are now a fixed 8 s per still (cache key = still + crop + preset), so they survive the TTS re-timing; made 5 at a time (`--plx-all` pre-makes every still in the map and overrides).
