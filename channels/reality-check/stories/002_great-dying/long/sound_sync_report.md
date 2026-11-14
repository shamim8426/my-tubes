# 002 sound sync report

Mix timeline: `voiceover_full.wav` (744.24 s) is placed at t=0 and the mix is 752.24 s (8 s music tail), the same length as the video; cross-correlation of the voice energy envelope against the video's audio track gave offset 0.00 s at 0, 150, 300, 500 and 700 s (audio of `002_long_preview.mp4` and of the previous upload). All times below are absolute video seconds from `audio/voiceover_timing.json` (line start/end; no word-level times exist in that file).

## 1. Plan vs timing json (all 104 lines)
Largest delta of a plan line start vs timing json: line 40 = +0.05 s; lines with |delta| > 0.1 s: none.

## 2. Music cues (fade-in start, equal-power crossfade over xf seconds)
| cue | track | fade-in start | xf s | next line start | cue start rel. to line | where |
|---|---|---|---|---|---|---|
| Disquiet | Disquiet | 0:00.0 | 4.5 | L1 0:00.0 | +0.00 s | plain boundary (-0.75 s before line) |
| Quietude | Quietude_Sections_Merged | 0:27.7 | 4.5 | L6 0:35.8 | -8.09 s | inside music-off hold [27.4, 32.9] |
| Giant Wyrm | Giant_Wyrm | 1:48.9 | 4.5 | L18 1:49.7 | -0.75 s | plain boundary (-0.75 s before line) |
| Ancient Rite | Ancient_Rite | 3:49.7 | 4.5 | L35 3:52.9 | -3.18 s | inside music-off hold [229.4, 234.6] |
| Lightless Dawn | Lightless_Dawn | 5:12.7 | 4.5 | L46 5:12.7 | -0.01 s | inside music-off hold [312.4, 319.3] |
| Disquiet 2 | Disquiet | 6:46.1 | 4.5 | L59 6:46.9 | -0.75 s | plain boundary (-0.75 s before line) |
| Inspired | Inspired | 9:05.9 | 2.4 | L78 9:08.9 | -2.97 s | inside music-off hold [545.6, 548.6] |
| Meditation Impromptu 01 | Meditation_Impromptu_01 | 10:32.5 | 3.2 | L91 10:36.2 | -3.72 s | inside music-off hold [632.2, 636.0] |
| Quietude reprise | Quietude_Sections_Merged | 11:38.0 | 4.5 | L100 11:45.0 | -7.03 s | inside music-off hold [697.7, 704.6] |

## 3. Music-off windows (cosine ramp down 3.0 s before, hold, ramp up 3.5 s after; depth -26 dB)
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

## 4. SFX / ambience events (141; all from sound_event_plan.md; delta = plan time minus time rebuilt from the timing json; must be <= 0.1 s)
Events over 0.1 s delta or outside their line (+-1 s): 0

| type | line | mix time | time from timing json | delta s | offset into line | check |
|---|---|---|---|---|---|---|
| AMB | L1 | 0:00.0 | 0:00.0 | +0.00 | +0.0 s | ok |
| BOOM-soft | L1 | 0:00.3 | 0:00.3 | +0.00 | +0.3 s | ok |
| AMB | L2 | 0:10.1 | 0:10.1 | +0.01 | +3.0 s | ok |
| THUD | L3 | 0:17.7 | 0:17.7 | +0.04 | +4.6 s | ok |
| AMB | L4 | 0:19.7 | 0:19.7 | +0.01 | +0.3 s | ok |
| TICK | L4 | 0:21.4 | 0:21.4 | +0.01 | +2.0 s | ok |
| BOOM | L4 | 0:24.4 | 0:24.4 | +0.01 | +5.0 s | ok |
| AIR | L6 | 0:35.7 | 0:35.7 | +0.01 | -0.1 s | ok |
| BOOM-soft | L6 | 0:35.8 | 0:35.8 | +0.01 | +0.0 s | ok |
| TICK | L10 | 1:02.1 | 1:02.1 | -0.01 | +0.2 s | ok |
| TICK | L11 | 1:05.1 | 1:05.1 | +0.04 | +0.3 s | ok |
| TICK | L11 | 1:07.3 | 1:07.3 | +0.04 | +2.5 s | ok |
| TICK | L11 | 1:08.7 | 1:08.7 | +0.04 | +3.9 s | ok |
| AMB | L12 | 1:11.1 | 1:11.1 | +0.03 | +0.3 s | ok |
| TICK | L13 | 1:23.0 | 1:23.0 | +0.02 | +7.6 s | ok |
| AMB | L14 | 1:25.2 | 1:25.2 | +0.01 | +0.0 s | ok |
| TICK | L16 | 1:41.8 | 1:41.8 | +0.03 | +3.4 s | ok |
| RISE | L17 | 1:47.9 | 1:47.9 | +0.00 | +4.2 s | ok |
| AIR | L18 | 1:49.6 | 1:49.5 | +0.05 | -0.1 s | ok |
| BOOM | L18 | 1:49.8 | 1:49.8 | +0.05 | +0.1 s | ok |
| TICK | L19 | 1:58.2 | 1:58.2 | +0.02 | +1.8 s | ok |
| TICK | L21 | 2:08.8 | 2:08.8 | -0.02 | +0.3 s | ok |
| TICK | L21 | 2:09.2 | 2:09.2 | -0.02 | +0.7 s | ok |
| TICK | L21 | 2:09.5 | 2:09.5 | -0.02 | +1.0 s | ok |
| TICK | L21 | 2:09.9 | 2:09.9 | -0.02 | +1.4 s | ok |
| TICK | L21 | 2:10.2 | 2:10.2 | -0.02 | +1.7 s | ok |
| BOOM-soft | L21 | 2:12.1 | 2:12.1 | -0.02 | +3.6 s | ok |
| BOOM-soft | L22 | 2:18.0 | 2:18.0 | -0.01 | +3.0 s | ok |
| THUD | L24 | 2:33.1 | 2:33.1 | -0.05 | +2.2 s | ok |
| THUD | L25 | 2:44.7 | 2:44.7 | -0.02 | +5.0 s | ok |
| THUD | L26 | 2:52.7 | 2:52.7 | +0.03 | +4.5 s | ok |
| THUD | L29 | 3:13.2 | 3:13.2 | +0.02 | +7.1 s | ok |
| CLOCK | L30 | 3:16.9 | 3:16.9 | -0.01 | +0.5 s | ok |
| CLOCK | L30 | 3:17.9 | 3:17.9 | -0.01 | +1.5 s | ok |
| CLOCK | L30 | 3:18.9 | 3:18.9 | -0.01 | +2.5 s | ok |
| CLOCK | L31 | 3:21.0 | 3:21.0 | -0.02 | +0.4 s | ok |
| CLOCK | L31 | 3:22.0 | 3:22.0 | -0.02 | +1.4 s | ok |
| THUD | L31 | 3:23.1 | 3:23.1 | -0.02 | +2.5 s | ok |
| TICK | L33 | 3:41.5 | 3:41.5 | +0.02 | +7.0 s | ok |
| BOOM-soft | L34 | 3:48.4 | 3:48.4 | +0.03 | -0.1 s | ok |
| AIR | L34 | 3:48.4 | 3:48.4 | +0.03 | -0.1 s | ok |
| TICK | L36 | 4:00.4 | 4:00.4 | +0.03 | +5.2 s | ok |
| THUD | L37 | 4:06.0 | 4:06.0 | +0.00 | +0.3 s | ok |
| TICK | L39 | 4:24.2 | 4:24.2 | +0.00 | +3.0 s | ok |
| THUD | L40 | 4:30.1 | 4:30.1 | +0.05 | +3.1 s | ok |
| TICK | L41 | 4:40.0 | 4:40.0 | -0.04 | +6.9 s | ok |
| AIR | L41 | 4:40.7 | 4:40.7 | -0.04 | +7.6 s | ok |
| TICK | L41 | 4:41.7 | 4:41.7 | -0.04 | +8.6 s | ok |
| CLOCK | L42 | 4:43.9 | 4:43.9 | +0.01 | +0.3 s | ok |
| CLOCK | L42 | 4:44.9 | 4:44.9 | +0.01 | +1.3 s | ok |
| CLOCK | L42 | 4:45.9 | 4:45.9 | +0.01 | +2.3 s | ok |
| CLOCK | L42 | 4:46.9 | 4:46.9 | +0.01 | +3.3 s | ok |
| CLOCK | L42 | 4:47.9 | 4:47.9 | +0.01 | +4.3 s | ok |
| CLOCK | L42 | 4:48.9 | 4:48.9 | +0.01 | +5.3 s | ok |
| THUD | L43 | 4:54.7 | 4:54.7 | +0.00 | +3.5 s | ok |
| THUD | L44 | 5:03.2 | 5:03.2 | -0.03 | +3.3 s | ok |
| AMB | L45 | 5:06.9 | 5:06.9 | +0.00 | +0.0 s | ok |
| TICK | L45 | 5:07.9 | 5:07.9 | +0.00 | +1.0 s | ok |
| RISE | L46 | 5:18.6 | 5:18.6 | -0.01 | +5.9 s | ok |
| BOOM | L47 | 5:20.4 | 5:20.4 | -0.04 | -0.0 s | ok |
| AMB | L48 | 5:28.3 | 5:28.3 | +0.01 | +0.2 s | ok |
| THUD | L48 | 5:30.6 | 5:30.6 | +0.01 | +2.5 s | ok |
| AMB | L49 | 5:35.5 | 5:35.5 | +0.04 | +0.0 s | ok |
| TICK | L49 | 5:35.8 | 5:35.8 | +0.04 | +0.3 s | ok |
| THUD | L49 | 5:37.0 | 5:37.0 | +0.04 | +1.5 s | ok |
| AIR | L50 | 5:41.6 | 5:41.6 | -0.05 | +0.5 s | ok |
| THUD | L50 | 5:46.0 | 5:46.0 | -0.05 | +4.9 s | ok |
| TICK | L51 | 5:55.1 | 5:55.1 | -0.02 | +4.6 s | ok |
| AMB | L52 | 5:57.3 | 5:57.3 | -0.03 | -0.0 s | ok |
| TICK | L52 | 5:59.3 | 5:59.3 | -0.03 | +2.0 s | ok |
| BOOM-soft | L53 | 6:07.6 | 6:07.6 | -0.02 | -0.1 s | ok |
| AIR | L53 | 6:07.6 | 6:07.6 | -0.02 | -0.1 s | ok |
| BOOM | L55 | 6:20.5 | 6:20.5 | -0.04 | -0.0 s | ok |
| AMB | L55 | 6:20.5 | 6:20.5 | -0.04 | -0.0 s | ok |
| TICK | L56 | 6:28.4 | 6:28.3 | +0.05 | +3.8 s | ok |
| AMB | L57 | 6:33.0 | 6:33.0 | +0.04 | +0.4 s | ok |
| TICK | L58 | 6:40.9 | 6:40.9 | -0.05 | +0.6 s | ok |
| BOOM-soft | L59 | 6:47.0 | 6:47.0 | +0.04 | +0.1 s | ok |
| TICK | L60 | 6:49.5 | 6:49.5 | -0.01 | +0.2 s | ok |
| AMB | L60 | 6:49.8 | 6:49.8 | -0.01 | +0.5 s | ok |
| TICK | L61 | 6:57.7 | 6:57.7 | -0.02 | +0.4 s | ok |
| THUD | L61 | 7:02.3 | 7:02.3 | -0.02 | +5.0 s | ok |
| THUD | L62 | 7:08.8 | 7:08.8 | -0.01 | +4.0 s | ok |
| TICK | L63 | 7:14.8 | 7:14.8 | +0.02 | +0.4 s | ok |
| AMB | L63 | 7:14.9 | 7:14.9 | +0.02 | +0.5 s | ok |
| THUD | L65 | 7:32.1 | 7:32.1 | +0.04 | +4.5 s | ok |
| TICK | L66 | 7:34.4 | 7:34.3 | +0.05 | +0.3 s | ok |
| TICK | L66 | 7:34.6 | 7:34.6 | +0.05 | +0.6 s | ok |
| TICK | L66 | 7:34.8 | 7:34.8 | +0.05 | +0.8 s | ok |
| TICK | L66 | 7:34.9 | 7:34.8 | +0.05 | +0.8 s | ok |
| TICK | L66 | 7:35.2 | 7:35.1 | +0.05 | +1.1 s | ok |
| TICK | L66 | 7:37.1 | 7:37.1 | +0.05 | +3.1 s | ok |
| TICK | L66 | 7:37.4 | 7:37.3 | +0.05 | +3.3 s | ok |
| TICK | L66 | 7:37.7 | 7:37.6 | +0.05 | +3.6 s | ok |
| TICK | L66 | 7:37.9 | 7:37.8 | +0.05 | +3.8 s | ok |
| TICK | L67 | 7:42.6 | 7:42.6 | -0.04 | +0.3 s | ok |
| TICK | L67 | 7:46.3 | 7:46.3 | -0.04 | +4.0 s | ok |
| AMB | L67 | 7:49.6 | 7:49.6 | -0.04 | +7.3 s | ok |
| TICK | L69 | 7:56.9 | 7:56.9 | +0.02 | +0.4 s | ok |
| TICK | L70 | 8:10.7 | 8:10.7 | +0.01 | +5.0 s | ok |
| TICK | L70 | 8:14.7 | 8:14.7 | +0.01 | +9.0 s | ok |
| BOOM-soft | L72 | 8:25.2 | 8:25.2 | -0.03 | +0.2 s | ok |
| TICK | L73 | 8:30.2 | 8:30.2 | +0.02 | +0.3 s | ok |
| TICK | L73 | 8:32.2 | 8:32.2 | +0.02 | +2.3 s | ok |
| TICK | L73 | 8:34.3 | 8:34.3 | +0.02 | +4.4 s | ok |
| TICK | L73 | 8:36.3 | 8:36.3 | +0.02 | +6.4 s | ok |
| AIR | L74 | 8:40.9 | 8:40.9 | +0.03 | +1.5 s | ok |
| TICK | L74 | 8:42.0 | 8:42.0 | +0.03 | +2.6 s | ok |
| THUD | L74 | 8:44.4 | 8:44.4 | +0.03 | +5.0 s | ok |
| RISE | L76 | 9:03.3 | 9:03.3 | +0.03 | +7.2 s | ok |
| AIR | L77 | 9:04.5 | 9:04.5 | -0.02 | -0.1 s | ok |
| BOOM-soft | L77 | 9:04.6 | 9:04.6 | -0.02 | -0.0 s | ok |
| THUD | L78 | 9:08.9 | 9:08.9 | +0.03 | +0.0 s | ok |
| TICK | L79 | 9:14.6 | 9:14.6 | +0.02 | +0.5 s | ok |
| TICK | L81 | 9:31.7 | 9:31.7 | -0.02 | +1.1 s | ok |
| TICK | L81 | 9:33.5 | 9:33.5 | -0.02 | +2.9 s | ok |
| TICK | L81 | 9:35.0 | 9:35.0 | -0.02 | +4.4 s | ok |
| TICK | L83 | 9:40.8 | 9:40.8 | +0.04 | +0.4 s | ok |
| TICK | L84 | 9:48.2 | 9:48.2 | +0.03 | +3.0 s | ok |
| AMB | L84 | 9:53.5 | 9:53.5 | +0.03 | +8.3 s | ok |
| TICK | L86 | 10:08.2 | 10:08.2 | -0.03 | +3.2 s | ok |
| TICK | L88 | 10:14.6 | 10:14.6 | -0.05 | +0.4 s | ok |
| THUD | L88 | 10:19.6 | 10:19.6 | -0.05 | +5.4 s | ok |
| TICK | L89 | 10:22.6 | 10:22.6 | -0.02 | +0.4 s | ok |
| RISE | L89 | 10:29.0 | 10:29.0 | -0.02 | +6.8 s | ok |
| AIR | L90 | 10:31.2 | 10:31.2 | -0.03 | -0.1 s | ok |
| BOOM-soft | L90 | 10:31.3 | 10:31.3 | -0.03 | -0.0 s | ok |
| TICK | L92 | 10:41.7 | 10:41.7 | +0.03 | +0.4 s | ok |
| THUD | L92 | 10:47.8 | 10:47.8 | +0.03 | +6.5 s | ok |
| TICK | L94 | 11:01.3 | 11:01.3 | +0.03 | +0.3 s | ok |
| THUD | L94 | 11:05.0 | 11:05.0 | +0.03 | +4.0 s | ok |
| TICK | L94 | 11:08.0 | 11:08.0 | +0.03 | +7.0 s | ok |
| TICK | L95 | 11:11.7 | 11:11.7 | +0.04 | +0.4 s | ok |
| THUD | L96 | 11:22.5 | 11:22.5 | +0.05 | +4.8 s | ok |
| TICK | L97 | 11:27.8 | 11:27.8 | -0.02 | +2.5 s | ok |
| THUD | L98 | 11:35.6 | 11:35.6 | -0.05 | +5.0 s | ok |
| THUD | L100 | 11:45.2 | 11:45.2 | -0.03 | +0.2 s | ok |
| BOOM-soft | L100 | 11:50.6 | 11:50.6 | -0.03 | +5.6 s | ok |
| TICK | L101 | 11:53.7 | 11:53.7 | +0.00 | +0.5 s | ok |
| THUD | L101 | 11:56.2 | 11:56.2 | +0.00 | +3.0 s | ok |
| BOOM-soft | L104 | 12:23.8 | 12:23.8 | +0.03 | +7.5 s | ok |

## 5. Smoothness and loudness (v5 fixed mix, measured)
- Applied music gain (env + section level + leveler, 100 Hz): max 3.8 dB/s outside the designed music-off ramps, 0 one-second windows over 6 dB/s. Music-off ramps are cosine, 3.0 s down (ending at the pivot line start) and 3.5 s up, depth -26 dB; their peak is 13.2 dB/s (designed, no steps). Speech-gap swell is +1.5/+2.5 dB with 1.0 s rise and 0.8 s fall. Fade-in 8 s from -24 dB, fade-out 14 s.
- Music cues changed from rhythmic to beatless beds: removed Gathering Darkness, Dark Fog, Impact Prelude (onset density 2.3-3.4/s, 160-170 bpm); now Disquiet, Quietude, Giant Wyrm, Ancient Rite, Lightless Dawn, Disquiet (2nd region), Inspired, Meditation Impromptu 01, Quietude reprise.
- Cue changes: crossfade 2.4-4.5 s equal-power; plain boundaries start 0.75 s before a line (L18, L59); the other six happen inside a music-off hold (inaudible) and the music then rises over 3.5 s into the next section.
- The only abrupt sounds left are the planned sub BOOM/BOOM-soft hits (5-8 ms attack, sub-only) at the end of music-off holds and at flashes.
- Mix: -14.0 LUFS, true peak -1.7 dBFS, 752.24 s. Windows (20 s at 30/150/300/450/600/720): -13.0 / -13.3 / -13.2 / -14.3 / -15.0 / -15.0 LUFS. Music(+fx) vs voice per 30 s in speech: -9 to -19 LU, body mostly -12..-17.
