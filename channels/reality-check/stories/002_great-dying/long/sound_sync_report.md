# 002 sound sync report

Mix timeline: `voiceover_full.wav` (744.24 s) is placed at t=0 and the mix is 752.24 s (8 s music tail), the same length as the video; cross-correlation of the voice energy envelope against the video's audio track gave offset 0.00 s at 0, 150, 300, 500 and 700 s (audio of `002_long_preview.mp4` and of the previous upload). All times below are absolute video seconds from `audio/voiceover_timing.json` (line start/end; no word-level times exist in that file).

## 1. Plan vs timing json (all 104 lines)
Largest delta of a plan line start vs timing json: line 40 = +0.05 s; lines with |delta| > 0.1 s: none.

## 2. Music cues (fade-in start, equal-power crossfade over xf seconds)
| cue | track | fade-in start | xf s | next line start | cue start rel. to line | where |
|---|---|---|---|---|---|---|
| Ancient Rite (open) | Ancient_Rite | 0:00.0 | 4.5 | L1 0:00.0 | +0.00 s | plain boundary (-0.75 s before line) |
| Lightless Dawn A | Lightless_Dawn | 0:27.7 | 4.5 | L6 0:35.8 | -8.09 s | inside music-off hold [27.4, 32.9] |
| Lightless Dawn B (catastrophe) | Lightless_Dawn | 1:48.9 | 5.0 | L18 1:49.7 | -0.75 s | plain boundary (-0.75 s before line) |
| Ancient Rite (evidence, quiet) | Ancient_Rite | 3:49.7 | 4.5 | L35 3:52.9 | -3.18 s | inside music-off hold [229.4, 234.6] |
| Lightless Dawn C (lava, denser) | Lightless_Dawn | 5:12.7 | 4.5 | L46 5:12.7 | -0.01 s | inside music-off hold [312.4, 319.3] |
| Ancient Rite (four killers) | Ancient_Rite | 6:46.1 | 5.0 | L59 6:46.9 | -0.75 s | plain boundary (-0.75 s before line) |
| Lightless Dawn D (uncertainty, quiet) | Lightless_Dawn | 8:19.5 | 4.5 | L72 8:25.0 | -5.53 s | inside music-off hold [499.2, 504.9] |
| Ancient Rite (hope, brighter) | Ancient_Rite | 9:05.9 | 2.4 | L78 9:08.9 | -2.97 s | inside music-off hold [545.6, 548.6] |
| Lightless Dawn E (why it matters) | Lightless_Dawn | 10:32.5 | 3.2 | L91 10:36.2 | -3.72 s | inside music-off hold [632.2, 636.0] |
| Ancient Rite (ending drone) | Ancient_Rite | 11:38.0 | 4.5 | L100 11:45.0 | -7.03 s | inside music-off hold [697.7, 704.6] |

## 3. Music-off windows (cosine ramp down 2.5 s before, hold, ramp up 3.0 s after; depth -30 dB)
| window | pivot line | line start | line end | hold start vs line start | hold end vs next line start |
|---|---|---|---|---|---|
| 0:27.4-0:32.9 | L5 | 0:27.6 | 0:34.4 | -0.16 s | -2.89 s |
| 3:49.4-3:54.6 | L35 | 3:52.9 | 3:54.7 | -3.48 s | -0.57 s |
| 5:12.4-5:19.3 | L46 | 5:12.7 | 5:20.0 | -0.31 s | -1.14 s |
| 6:15.9-6:20.4 | L54 | 6:16.3 | 6:20.1 | -0.43 s | -0.14 s |
| 8:19.2-8:24.9 | L71 | 8:19.5 | 8:24.6 | -0.26 s | -0.13 s |
| 9:05.6-9:08.6 | L78 | 9:08.9 | 9:13.6 | -3.27 s | -5.48 s |
| 10:32.2-10:36.0 | L91 | 10:36.2 | 10:40.8 | -4.02 s | -5.27 s |
| 11:37.7-11:44.6 | L99 | 11:38.0 | 11:44.6 | -0.28 s | -0.43 s |

## 4. SFX / ambience events (41; all from sound_event_plan.md; delta = plan time minus time rebuilt from the timing json; must be <= 0.1 s)
Events over 0.1 s delta or outside their line (+-1 s): 0

| type | line | mix time | time from timing json | delta s | offset into line | check |
|---|---|---|---|---|---|---|
| BOOM-soft | L1 | 0:00.3 | 0:00.3 | +0.00 | +0.3 s | ok |
| THUD | L3 | 0:17.7 | 0:17.7 | +0.04 | +4.6 s | ok |
| BOOM | L4 | 0:24.4 | 0:24.4 | +0.01 | +5.0 s | ok |
| BOOM-soft | L6 | 0:35.8 | 0:35.8 | +0.01 | +0.0 s | ok |
| BOOM | L18 | 1:49.8 | 1:49.8 | +0.05 | +0.1 s | ok |
| BOOM-soft | L21 | 2:12.1 | 2:12.1 | -0.02 | +3.6 s | ok |
| BOOM-soft | L22 | 2:18.0 | 2:18.0 | -0.01 | +3.0 s | ok |
| THUD | L24 | 2:33.1 | 2:33.1 | -0.05 | +2.2 s | ok |
| THUD | L25 | 2:44.7 | 2:44.7 | -0.02 | +5.0 s | ok |
| THUD | L26 | 2:52.7 | 2:52.7 | +0.03 | +4.5 s | ok |
| THUD | L29 | 3:13.2 | 3:13.2 | +0.02 | +7.1 s | ok |
| THUD | L31 | 3:23.1 | 3:23.1 | -0.02 | +2.5 s | ok |
| BOOM-soft | L34 | 3:48.4 | 3:48.4 | +0.03 | -0.1 s | ok |
| THUD | L37 | 4:06.0 | 4:06.0 | +0.00 | +0.3 s | ok |
| THUD | L40 | 4:30.1 | 4:30.1 | +0.05 | +3.1 s | ok |
| THUD | L43 | 4:54.7 | 4:54.7 | +0.00 | +3.5 s | ok |
| THUD | L44 | 5:03.2 | 5:03.2 | -0.03 | +3.3 s | ok |
| BOOM | L47 | 5:20.4 | 5:20.4 | -0.04 | -0.0 s | ok |
| THUD | L48 | 5:30.6 | 5:30.6 | +0.01 | +2.5 s | ok |
| THUD | L49 | 5:37.0 | 5:37.0 | +0.04 | +1.5 s | ok |
| THUD | L50 | 5:46.0 | 5:46.0 | -0.05 | +4.9 s | ok |
| BOOM-soft | L53 | 6:07.6 | 6:07.6 | -0.02 | -0.1 s | ok |
| BOOM | L55 | 6:20.5 | 6:20.5 | -0.04 | -0.0 s | ok |
| BOOM-soft | L59 | 6:47.0 | 6:47.0 | +0.04 | +0.1 s | ok |
| THUD | L61 | 7:02.3 | 7:02.3 | -0.02 | +5.0 s | ok |
| THUD | L62 | 7:08.8 | 7:08.8 | -0.01 | +4.0 s | ok |
| THUD | L65 | 7:32.1 | 7:32.1 | +0.04 | +4.5 s | ok |
| BOOM-soft | L72 | 8:25.2 | 8:25.2 | -0.03 | +0.2 s | ok |
| THUD | L74 | 8:44.4 | 8:44.4 | +0.03 | +5.0 s | ok |
| BOOM-soft | L77 | 9:04.6 | 9:04.6 | -0.02 | -0.0 s | ok |
| THUD | L78 | 9:08.9 | 9:08.9 | +0.03 | +0.0 s | ok |
| THUD | L88 | 10:19.6 | 10:19.6 | -0.05 | +5.4 s | ok |
| BOOM-soft | L90 | 10:31.3 | 10:31.3 | -0.03 | -0.0 s | ok |
| THUD | L92 | 10:47.8 | 10:47.8 | +0.03 | +6.5 s | ok |
| THUD | L94 | 11:05.0 | 11:05.0 | +0.03 | +4.0 s | ok |
| THUD | L96 | 11:22.5 | 11:22.5 | +0.05 | +4.8 s | ok |
| THUD | L98 | 11:35.6 | 11:35.6 | -0.05 | +5.0 s | ok |
| THUD | L100 | 11:45.2 | 11:45.2 | -0.03 | +0.2 s | ok |
| BOOM-soft | L100 | 11:50.6 | 11:50.6 | -0.03 | +5.6 s | ok |
| THUD | L101 | 11:56.2 | 11:56.2 | +0.00 | +3.0 s | ok |
| BOOM-soft | L104 | 12:23.8 | 12:23.8 | +0.03 | +7.5 s | ok |
