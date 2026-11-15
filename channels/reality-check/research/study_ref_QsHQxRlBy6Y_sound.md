# Sound study of the reference documentary (https://youtu.be/QsHQxRlBy6Y, 22:39, Hindi explainer, presenter + graphics)

Study date 2026-11-14 (second, sound-only pass; first pass = `study_ref_QsHQxRlBy6Y.md`). Rules: shared/RULES.md 12c. yt-dlp without login/cookies (one HTTP 429 on an extra subtitle track, retried without it, no sign-in or bot check appeared), media only in git-ignored `study/ref_sound_QsHQxRlBy6Y/`, deleted after the analysis. TECHNIQUE ONLY: no audio, clip, frame, voice, phrase, title or thumbnail of the reference is reused; everything in `long/sound_event_plan.md` is our own recipe for our own synthesised or CC0 sounds. Nothing uploaded, no paid call, nothing committed.

## 0. Method and limits (read this first)
- Audio: 32 kHz stereo decode, mid = (L+R)/2 (voice, almost all of the sub bass), side = (L-R)/2 (voice-free, so it is the best proxy for music + wide effects). Levels are dBFS in a band, calibrated to the file RMS. "vs voice peak" = band peak of the event minus the voice-band (200-3400 Hz, 50 ms frames) 95th percentile, which is -14.0 dBFS. Bands: sub 25-70 Hz, bass 70-250, low-mid 250-1k, mid 1-3k, high 3-6k, 6-10k, 10-15.5k.
- Detectors: (1) sub-band onset detector (rise of 14+ dB over a 2-4 s local median and a peak above -31 dBFS; voice plosives stay below that); (2) side-channel onset detector (rise of 14+ dB over the 3 s median) for swells and wide events; (3) noise-burst detector on the mid channel (6-10 kHz above -36 dBFS, spectrally flat, longer than 0.2 s, to separate it from the short Hindi sibilants); (4) music-off detector (side channel below -52 dBFS for 0.8 s or more); (5) a tick-grid check (event intervals); (6) ffmpeg scene cuts (threshold 0.35, 454 cuts) to see whether a sound sits on a cut. Every event class was spot-checked against a frame at the event time (120 contact-sheet frames viewed) and against the channel's own captions (the English auto-translation of the Hindi track; text below is paraphrased).
- Limits: no stem separation, so quiet effects that sit under the voice in the same band (a soft tick at -30 dB) can be missed; the log is complete for everything louder than about -30 dB vs voice peak in the sub band, and for noise bursts above -36 dBFS in 6-10 kHz. About 30 "soft thud" candidates between -23 and -31 dBFS in the sub band may be voice plosives or music bass movement rather than SFX; they are tagged "soft" and counted separately. Loudness of the whole file: -16.7 LUFS integrated, LRA 5.4 LU, true peak +0.8 dBFS (do not copy the peak).
- Correction to the first study: the 8-10 "silences" are NOT silence. They are music-off windows (side channel empty for 0.9-7.7 s, ten of them, listed in 1.4) while the NARRATOR CONTINUES; between the words the file is digitally quiet (70-250 Hz band falls to -67 dBFS, no room tone, no ambience). Only 19:40.96-19:41.6 is a true all-silent gap (0.6 s). Also the first study said "no hits" in the 17:20-18:05 block: there IS a rhythmic tick pulse (1.5 below), and "no ambience" is right except thunder-like rumbles at the opening lightning.

## 1. Sound event log

### 1.1 Reading key
`T` = start time m:ss.s. Types: BOOM = big sub impact (sub peak -9..+7 vs voice peak), THUD = softer sub thump, RISE = sub riser/reverse swell into a hit, AIR = short noise burst (what a "whoosh" is in this video), TICK = graphic tick/pop, PULSE = rhythmic tick ostinato, SWELL = music/pad swell seen in the side channel, OFF = music-off window (voice continues), BED = bed change. Level = peak of the event band relative to the voice peak in dB. Spectrum: fundamental / centroid; "noisy vs tonal"; attack (time from -10 dB to peak) and decay (time to fall 10 dB). Narration is paraphrased English.

### 1.2 Hook (0:00-1:54)
| T | type | length / shape | vs voice peak | spectrum | on screen | narration |
|---|---|---|---|---|---|---|
| 0:00.3 | BOOM (file starts on it) | rises from silence in under 0.2 s, decay 0.3 s | -1 | sub 25-70 Hz (pk -15 dBFS), centroid 200 Hz, tonal | opening Earth/orbit shot | "42,000 years ago something seemed to break the sky" (first sentence starts at once) |
| 0:02.3 | SWELL | atk 0.13 s, dec 0.8 s | -7 (side -21) | pad/low strings, centroid 670 Hz, tonal | same shot | same sentence |
| 0:09.7 | BOOM (thunder-like rumble) | atk 0.37 s, dec 0.42 s, tail 0.4 s | 0 | sub 20-90 Hz, soft onset, no noise: a distant thunder | lightning over a dark plain | "terrible lightning storms all over the sky" |
| 0:11.5 | BOOM (thunder 2) | atk 0.30 s, dec 0.42 s | -1 | same | second lightning | same |
| 0:15.8 | RISE+BOOM+AIR | 0.7 s swell into hit at 0:16.2 (sub -13 dBFS = +1) then one 0.29 s noise burst | +1 | hit sub 66 Hz; noise 6-10 kHz -20 dBFS, centroid 1.2 -> 0.9 kHz (falls), flat 0.46 | big sun flare filling the frame | "radiation from space ... destroyed the ozone layer" |
| 0:19.3 | SWELL | s-curve rise | | - | UV/ozone shot | |
| 0:25.0 | BOOM (card) | atk 0.16 s, decay 1.3 s, tail 1.7 s | +2 | pure sine 66 Hz, 94% of energy under 100 Hz, 0.1% above 1 kHz | headline card ("... broke down 42,000 years ago ... sudden climate change") appears, red highlight on key words | "ultraviolet radiation rose, climate changed" |
| 0:27.9 | THUD | 0.6 s | -4 | sub, 20% > 1 kHz | cut | "humans lived in caves" |
| 0:30.1 | AIR | 0.24 s | -7 (6-10k -21) | centroid 4.3 -> 4.0 kHz, flat 0.20 | cut to the host (first face at 0:30) | "cave art ..." |
| 0:33.2 | AIR | 0.21 s | -8 | centroid 2.8 -> 4.0 kHz rising | cave-art cut (red torch light) | "cave art suddenly became popular" |
| 0:40.5 | BOOM | atk 0.30 s, dec 1.07 s, tail 1.2 s | 0 | sub, soft | dark globe cut | "due to UV humans used caves as shelters" |
| 0:50.7 | TICK | 0.06 s | -18 (side hi -32) | centroid 2.7 kHz, flat 0.28 | extinct-animal photo | "giant kangaroos and wombats vanished" |
| 0:56.9 | BOOM (stamp) | atk 0.11 s, decay 1.09 s, tail 1.4 s | 0 | sub; the red "EXTINCT" stamp lands on three vintage photos | "Neanderthals were also wiped out" |
| 1:02.1 | BOOM (reveal) | atk 0.16 s, short: decay 0.16 s, tail 0.2 s | +5 (loudest of the hook) | sub 51 Hz, 98% under 100 Hz | the Neanderthal face; yellow label "closest relative of Homo sapiens" | same |
| 1:03.9 | AIR | 0.21 s | -6 | centroid 1.5 -> 2.0 kHz | face moves | |
| 1:05.4 | BOOM-soft + AIR | hit decay 0.06 s; noise 0.21 s rising 0.7 -> 5.7 kHz | -4 | electric crackle zap | host cut with glowing "?" icon | "but the question is, what happened?" |
| 1:10.6 | TICK/blip + THUD | atk 0.14 s, decay 0.21 s; side hi +26 dB, centroid 1.5 kHz, flat 0.23 | -7 | glassy pop | soil cross-section with a ruler "20 km" | "the answer was under our feet, 3000 km deep" |
| 1:21.2 | AIR | 0.32 s | -9 | centroid 3.0 -> 5.6 kHz | host cut | "... even above the Earth" |
| 1:26.8 | RISE+THUD | pre-riser 1.2 s, then hit | -8 | sub swell, centroid 105 -> 176 Hz | globe with the red/green South Atlantic anomaly | "the region between South America and Africa" |
| 1:33.2 | THUD (glitch) | atk 0.08 s, decay 0.19 s, 15% energy above 1 kHz | -6 | thump + click | telescope/satellite cutaway | "satellite equipment malfunctions" |
| 1:40.1 | AIR | 0.24 s, rising 0.7 -> 5.2 kHz | -7 | | aurora over night Earth | "this region is called the Bermuda Triangle of space" |
| 1:42.4 | BOOM | pre 0.6 s, decay 0.46 s, tail 3.0 s | -1 | sub 35-51 Hz, 96% under 100 Hz | title lock-up "BERMUDA TRIANGLE OF SPACE" | same |
| 1:43.8 | RISE+BOOM | 2.0 s swell then hit | -1 | sub 35-39 Hz, 54% under 100 Hz | same title held | "let us understand in depth" |
| 1:47.4 | AIR (long) + SWELL | 0.93 s, centroid 3.4 -> 1.7 kHz falling, flat 0.35; music-only 1:48-1:54, side swell peaks at -14 dBFS (the loudest music in the body) | -14 (noise), music full | the longest noise sound in the whole film (0.93 s) | transition from the title to the host | host line, then "video number" lock-up |
| 1:49.9 | THUD | | -3 | | title/lock-up | |
| 1:54-3:17 | sponsor block (excluded, own-product promo, lighter bed, confetti, 5 AIR bursts 0.3-0.45 s, one BOOM +45 dB at 2:09.2 with a wide noise burst on an image montage) | | | | | not relevant for us (no sponsor) |

### 1.3 Chapter 1: Earth layers and the field (3:17-6:08)
| T | type | length / shape | vs voice peak | spectrum | on screen | narration |
|---|---|---|---|---|---|---|
| 3:16.2-3:17.7 | SWELL x2 (bed in) | atk 0.14/0.06 s, decay 0.05/0.13 s | -9..-12 | centroid 510-710 Hz | black frame -> host "Hello!" | |
| 3:19.6-3:22.6 | OFF (3.0 s) | side empty, voice only | - | - | host: "to find the answer we first dive under our feet" | |
| 3:22.4 | THUD (bed returns) | atk 0.14 s, decay 0.13 s | -16 | sub 24 dBFS band -30 | Earth appears | "the earth has four layers" |
| 3:26.0 / 3:27.0 / 3:28.1 / 3:29.5 | TICK x4 | atk 0.03-0.05 s, decay 0.06-0.19 s | -23..-30 (side total -37..-44 dBFS) | centroid 1.3-2.1 kHz, flat 0.1-0.26: glassy pop with a touch of noise | numbered rings pulse on the cutaway: crust 1, mantle 2, outer core 3, inner core 4 | "crust, mantle, outer core, inner core" |
| 3:36.8 | THUD | decay 0.58 s, tail 1.2 s | -17 | sub | "2,900 km" label | "a sea of melted iron" |
| 3:47.7 | THUD | decay 0.40 s | -9 | sub 125 Hz | spinning outer core with currents | "electric currents" |
| 3:59.7 | TICK shimmer | atk 0.32 s, centroid 4.6 kHz, flat 0.25 | -20 | bright shimmer | field loops appear around a wire | "electric currents make a magnetic field" |
| 4:01.7 | THUD | | -11 | sub | layers cutaway | |
| 4:05.0 | AIR (draw) + THUD | 0.67 s soft noise, centroid 950 Hz (narrow, low), flat 0.55; sub hit -25 dBFS decay 0.38 s | -14 (noise), -11 (hit) | airy and low, NOT a sweep | field lines draw outward from the core | "this makes the Earth's field" |
| 4:06.4 / 4:11.0 | THUD / TICK | | -14 / -23 | | field lines around the globe | |
| 4:15.6 | THUD | pre 0.7 s, decay 0.53 s | -14 | sub | school-book bar magnet | "drawn as a magnet, but there is no magnet" |
| 4:24.7 | BOOM + SWELL | sub -8 dBFS, decay 0.29 s, music swell 4:23-4:26 (side -18) | +6 | sub 31 Hz and below, bed swells | sun vs "magnetic shield" | "an invisible shield against the sun" |
| 4:29.7 | SWELL | atk 0.37 s | -13 | | "MAGNETIC SHIELD" label | |
| 4:40.9 | BOOM-soft | pre 0.4 s | -11 | | host cut | "a very common misconception" |
| 4:58.9 / 5:07.4 / 5:31.5 | THUD x3 | decay 0.34-0.42 s | -17 / -16 / -16 | sub | labels "GEOGRAPHIC NORTH POLE", "MAGNETIC NORTH POLE", ring "~120 km LOOP - EVERY DAY" | |

### 1.4 Chapter 2: the 1831 story and the speed (6:08-9:05)
| T | type | length / shape | vs voice peak | spectrum | on screen | narration |
|---|---|---|---|---|---|---|
| 6:08.2-6:15.7 | OFF (7.5 s) | side empty, voice continues | - | between words the file is digitally quiet | host: "now the question is why does the pole keep moving? go back 200 years" | |
| 6:14.1 / 6:16.0 | AIR x2 | 0.30 s each, 6-10k -31/-34 dBFS, flat 0.49/0.43 | -17..-20 | | orange-red-white flash | |
| 6:16.4-6:18.4 | RISE | sub rises from -48 to -15 dBFS in 2.0 s | up to +1 | sub swell | flash/white-out then the Arctic map | |
| 6:18.5 | BOOM + cut-out | atk 0.22 s, d10 0.29 s, then the sub falls to -47 within 0.6 s and the bed comes back | +1 | sub 51 Hz fundamental | map of Canada in red | "Boothia Peninsula, Arctic Canada" |
| 6:54.3 | AIR | 0.26 s | -10 | centroid 2.7 -> 2.2 kHz | white flash on a vintage engraving | "he declared it British territory" |
| 7:02.5 | BOOM (loudest of the body) | atk 0.27 s, tail 0.6 s, 97% under 100 Hz | +7 | sub 51 Hz | map line drawn from the magnetic to the geographic pole | "about 1600 km south of the geographic pole" |
| 7:05.8 | BOOM | atk 0.13 s | 0 | sub 27-117 Hz | red distance chip appears on the line | "1600 km apart" |
| 7:23.6 | RISE+BOOM | pre-riser 1.9 s, atk 0.58 s | -3 | sub | map path begins | "the speed was slow at first, 9-15 km/yr" |
| 7:46.0 | RISE+BOOM | pre 0.8 s | -7 | sub | map pole path continues, speeds up | "it almost started to run" |
| 7:48.8 | RISE | pre 1.5 s | -14 | | path on the map | "1990: 55 km per year" |
| 7:59.3 | BOOM (bar jump) | atk 0.14 s, decay 0.11 s | -3 | sub 43 Hz | the red bar "51.5" shoots up in the pole-drift bar chart | "its speed became 4 times" |
| 8:00.3 / 8:03.3 | AIR x2 | 0.29/0.27 s, centroids 1.7 -> 5.5 kHz / 2.1 -> 5.0 kHz (both rise) | -10 / -9 | | a small red bar and the curved arrow drawn on the chart | |
| 8:19.2 | BOOM | atk 0.05 s, tail 1.1 s | -3 | sub 66 Hz | map: the pole crosses to the Eastern hemisphere, Russia | "today it is moving to Siberia" |
| 8:33-9:02 | BED ONLY | no events | | | NOAA emergency update, WMM card | |

### 1.5 Chapter 3: why it matters, why it moves (9:02-12:12)
| T | type | length / shape | vs voice peak | spectrum | on screen | narration |
|---|---|---|---|---|---|---|
| 9:02.5 | BOOM + flash | atk 0.26 s, d10 0.66 s, tail 2.4 s; 0.4 s air hiss at 9:03.5 (6-10k -35/-26 dBFS) | -6 | sub 70 -> 31 Hz glides down | host blurred into a flash | "you might wonder, what difference does it make?" |
| 9:05.5-9:11.6 | OFF (6.2 s) | | | | host | "if an invisible point slips, what difference to us?" |
| 9:13.7-9:24 | soft THUD/SWELL x5 | 0.1-0.5 s, side S -24..-27 | -11..-14 | centroid 170-460 Hz | airport runway numbers, cockpit with a compass | "18, 27, 36 ..." |
| 9:22.1 | SWELL + flash | S -24 | -10 | | yellow/red light leak | |
| 9:42.7 | THUD | tail 1.2 s | -11 | | runway diagram | |
| 9:49.0 / 9:50.5 | SWELL x2 | atk 0.29 s, dec 0.34 s | -12 | | host blurred by an orange leak | |
| 9:54.6 | THUD | | -13 | | NOAA article card "Airport runway names shift with the magnetic field", date circled | |
| 10:04.1 | AIR | 0.24 s | -9 | centroid 1.0 -> 3.5 kHz rising | aerial runway | |
| 10:27.4 | AIR (glitch) | 0.29 s, 6-10k -17 dBFS (loudest noise burst in the film), centroid 3.6 -> 1.1 kHz falling | -3 | digital buzz | phone map showing red "ERROR" | "compass shows the wrong direction" |
| 10:29.0 | RISE | atk 1.7 s | -4 | sub 90 -> 121 Hz | military control room | "military navigation" |
| 10:33.7 | BOOM | atk 0.26 s, d10 0.67 s, tail 2.4 s | -6 | sub 102 -> 31 Hz | red alarm-style map | "so roughly speaking it is a big impact" |
| 10:36.4-10:44.1 | OFF (7.7 s) | | | | host | "but now the question: why is the pole pulled so much?" |
| 11:49.2 | BOOM | atk 0.18 s | 0 | sub 27 Hz | Livermore figure: red magnetic lobes under Canada/Siberia | "the Canada lobe stretched" |
| 12:03.9 | THUD | tail 2.0 s | -13 | | map with the pole arrow | "the pole shifted towards Siberia" |
| 12:24.6 | SWELL | S -19 | -5 | | globe with field lines | "poles flip ... hundreds of times" |

### 1.6 Chapter 4: flips, the stone compass, the sea floor (12:12-15:40)
| T | type | length / shape | vs voice peak | spectrum | on screen | narration |
|---|---|---|---|---|---|---|
| 12:29.9 | BOOM-soft | atk 0.37 s | -3 | sub | black frame into the 1905 lab scene | "in 1905 a French physicist ..." |
| 12:32.6 | AIR + THUD | 0.24 s, centroid 5.7 -> 3.9 kHz | -13 | | lab scene with "1905" | |
| 12:46.2 | THUD | pre 1.0 s, tail 1.5 s | -14 | | host | "lava freezes the field direction" |
| 12:50.6 / 12:55.1 / 12:56.2 | THUD x3 | 0.05-0.11 s | -17 / -17 / -13 | soft | lava map, then dots with N-S compass pins | "a stone compass" |
| 13:05.0 | AIR | 0.22 s | -10 | | lab | |
| 13:17.1-13:34.3 | OFF x4 (1.2, 2.1, 0.9, 1.4 s) | broken music at the reversal | | | lab, then host | "scientists made fun of it for decades" |
| 13:23.2 | SWELL | S -30 | -16 | | pink Earth with field lines | |
| 13:34.6 | BOOM-soft + AIR | decay 0.14 s, tail 3.0 s; noise 0.35 s centroid 4.1 kHz | -15 | | host with red box "1" | "but in 1960, a map of the ocean proved him right" |
| 13:36.4 | RISE+THUD | pre 2.0 s | -14 | sub | 1960 sea-floor map | |
| 13:44-14:11 | SWELL x6 | S -25..-31, decay 0.2-0.5 s | -11..-17 | centroid 170-320 Hz | ship with winch, zebra-stripe field globe, host gestures, vent footage | "magnetic stripes ... mirror images ... new lava" |
| 14:13.5 | BOOM | atk 0.18 s, tail 2.9 s | -5 | sub 31 -> 23 Hz (deep) | undersea vent footage | "lava keeps filling in" |
| 14:21.5 | THUD on a hard cut | atk 0.05 s, 19% above 1 kHz | -8 | thump + click | cut back to the host | "the sea floor worked as a tape recorder" |
| 14:25.1 | THUD | | -13 | | compass pins | |
| 14:44.7 | RISE+BOOM | atk 1.34 s, pre 1.4 s, sub -8 dBFS | +6 | sub rises 1.4 s then hits | Earth rises from orbit | "the numbers they found shocked everyone" |
| 14:52.6 | RISE | atk 1.36 s | -13 | | sea-floor stripes, hand drawing | |
| 15:25.3 | AIR | 0.21 s, centroid 5.2 -> 4.1 kHz | -9 | | host | "listen to this carefully" |
| 15:00-15:40 | BED ONLY | the counter 11 -> 183 and the three key numbers have NO hit, NO tick | | | barcode counter | "183 flips, every 4.3 lakh years, last 7.8 lakh years ago" |

### 1.7 Chapter 5: the scare and the honest answer (15:40-22:08)
| T | type | length / shape | vs voice peak | spectrum | on screen | narration |
|---|---|---|---|---|---|---|
| 15:48.9 | THUD | tail 1.0 s | -12 | sub | compass at night | "actually a temporary flip took place" |
| 15:53.9 / 15:57.0 | THUD x2 | | -14 / -13 | | compass needle moves | |
| 16:13.6 | THUD | | -13 | | Science paper figure | "in 2021 a study ..." |
| 16:20.0 / 16:20.9 | RISE+THUD | pre 1.6 s, tail 2.2 s | -13 | | field shield CG collapsing | "we had almost no invisible shield" |
| 16:31.7 | THUD | | -14 | | paper page | |
| 16:41.9 | RISE | atk 1.38 s | -12 | | host | "Neanderthals died because of it" |
| 16:43.9 | AIR | 0.29 s, 4.8 -> 3.2 kHz | -8 | | host | |
| 17:05.6 | BOOM | atk 0.18 s, d10 0.99 s, tail 3.1 s | -5 | sub 23-31 Hz | CBN news card "pole is shifting, prompting fears of coming chaos" with orange highlight | "claims that the poles would flip" |
| 17:26.6-18:01.4 | PULSE x about 80 | grid of 0.19 s (0.38, 0.59, 0.78 s ... = about 77 BPM sixteenths), each 0.03-0.06 s decay, centroid 450-700 Hz, mid band, hi < -80 dBFS, side level -31..-41 dBFS | -17..-27 | tonal pluck/pizzicato ostinato, narrow, centre-wide | host speaking to camera | "will we disappear like Neanderthals? when is the next flip? overdue ... 2034 plus minus 3" |
| 17:49.4 | THUD (big) | atk 0.14 s, tail 1.6 s | -9 | sub | host | "but other scientists say there is no schedule" |
| 18:02.7 | THUD | pulse ends hard at 18:01.4, then hit; d10 0.77 s | -11 | sub | host | "10,000 or 5 crore years" |
| 18:24.9 | BOOM + flash | atk 0.08 s, tail 2.1 s | 0 | sub 35 Hz, 88% under 100 Hz | orange-yellow light leak, host | "your children's children will live shorter than the flip" |
| 18:39.7 | AIR | 0.46 s, centroid 6.0 -> 5.3 kHz, flat 0.48 (brightest burst) | -14 | airy, high | host blurred then sharp (blur pull-in) | "not that much bad news actually" |
| 18:54.6 | THUD | d10 0.96 s | -10 | | rock-cave cut, Neanderthals | |
| 19:11.1 | THUD | | -10 | | host | "the 2021 study was questioned" |
| 19:16.1 | AIR | 0.26 s | -6 | | NLM comment card "Comment on a global environmental crisis 42,000 years ago" | "10 scientists published a counter study" |
| 19:36.4 | THUD | d10 0.99 s | -10 | | host | "research is still going on" |
| 19:38.1-19:42.7 | OFF (4.6 s) | all-silent 0.6 s at 19:40.96 | | | host | the uncertainty line |
| 20:05.1 | THUD | | -9 | | host | "next flip: big impact on migrating animals" |
| 20:15.3 | RISE+BOOM | pre 2.1 s | -1 | | host, "thankfully we do not live in caves" | |
| 20:17.2 | RISE | atk 4.6 s (slow) | -20 | | | |
| 20:38.7 | RISE+BOOM | pre 2.1 s | 0 | sub | city / power-grid CG | "today the biggest threat is modern technology" |
| 20:40.5 | RISE | atk 4.3 s (slow, long) | -16 | | phone with an empty battery | |
| 21:13.7 | THUD | | -10 | | host | "if the field weakens everywhere, the triangle spreads" |
| 21:40.5-21:44.4 | OFF (3.9 s) | | | | host | "it is shifting because it was never in one place; today the speed fell" |
| 21:46.4 | THUD | | -17 | | BGS news card (movement slowed to about 35 km/yr) | |
| 21:53.1 | THUD | | -10 | | host | closing question |
| 22:08.2 | BOOM-soft | | -1 | | host "watch the next video" | |
| 22:31.1 | BOOM + drone (end card) | sub -20 dBFS, d10 4.7 s, tail 5.2 s, centroid 155 Hz | -6 | sub drone 24 Hz | end card "PRODUCED BY" logo built from field lines | |

### 1.8 What was measured for the whole file (rates, body only = 22:39 minus sponsor and end card = about 20.7 min)
- BOOM-class (sub peak above -23 dBFS): 26 -> 1.3 per minute. Soft thuds (-23..-31): 39 -> 1.9 per minute (partly voice). RISE (pre-riser 1.4 s or longer, or attack 1.0 s or longer): 12 -> 0.6 per minute. AIR (noise burst 6-10 kHz above -36 dBFS): 25 -> 1.2 per minute, median 0.26 s, median centroid 2.8 kHz, 10-15 kHz band median 12 dB below the 6-10 kHz band. Music-off windows: 10 detections = 7 distinct places (about once per 3 minutes; the 13:17-13:34 reversal is four short cuts of the bed). Cue changes: 9-12 regions (first study).
- Position vs cuts (454 hard cuts): 36% of the sub events (28 of 77) and 43% of the big ones (20 of 46) start within 0.35 s of a hard cut or flash; in the last third of the film nearly every big hit sits exactly on a cut (offset under 0.1 s). The rest sit on a graphic starting (bar jump, line drawn, label chip, stamp, counter reaching the value). Almost none sit on a sentence start.
- The counter at 15:00 (the one key statistic, 183 flips) has no hit and no tick: graphics that only explain get no effect; effects mark REVEALS, CUTS and VALUE LANDINGS.

## 2. Summary table (the reference's sound vocabulary; per minute over the body, 20.7 min)
| sound type | per minute | typical level vs voice peak | typical length | spectral recipe | used for | NOT used for |
|---|---|---|---|---|---|---|
| Music bed | continuous | bed -15 dB under speech in the body (-12 open/close, -19..-20 in the debunk block), music-only parts reach about 0 dB | 9-12 cues of 1.5-2.5 min | dark ambient: sub 20-100 Hz and bass 100-250 Hz carry it, centroid of the full mix 155-570 Hz, 4-12 kHz -9..-28 dB re total, no beat (tempo confidence 0.06-0.15), no melody | everything | never stops except the OFF windows |
| BOOM (big sub impact) | 1.3 | median -3 (range -9 .. +7) | attack 0.05-0.4 s, 10 dB decay 0.1-1.3 s, audible tail 0.2-3 s | one sine 27-66 Hz (35-51 Hz typical), 94-98% of energy under 100 Hz, under 3% above 1 kHz; sometimes glides down 70 -> 31 Hz; no noise layer | title/headline cards, stamps, a face/label reveal, the first frame after a flash, a value landing in a chart, hard cut back to the host | on a sentence start, on explanatory motion (the 183-flips counter) |
| THUD (soft sub) | 1.9 (some may be voice) | -9 .. -17 | 0.1-0.5 s | 55-125 Hz sine-like thump; 10-20% energy above 1 kHz when it sits on a cut (a click is added) | map line/label appearing, paper/card appearing, cut to host | between graphics that do not change |
| RISE (sub riser) | 0.6 | peak -3..-14 | 1.2-2.1 s (a few slow ones 4.3-4.6 s) | low only: sub 30-60 Hz rising 20-30 dB plus pad swell in the side channel (centroid 150-500 Hz); NO high-frequency noise, hard stop at the hit | the 1-2 s before a flash or title (6:16, 10:29, 14:44, 20:15, 20:38) | stand-alone; never as the sound of a camera move |
| AIR (the "whoosh") | 1.2 | 6-10 kHz band -17..-33 dBFS, i.e. about -8..-14 dB overall (always smaller than the voice) | median 0.26 s (0.21-0.46; one of 0.93 s on the title) | broadband air burst, centroid 2.8 kHz median (0.7-6 kHz), 10-15 kHz band 12 dB under the 6-10 kHz band, flat; direction of the "sweep" is mixed (half rising, half falling) and tiny; centre-panned | flash/blur cut, host jump cut, arrow or line drawn, a new card; on the glitchy "ERROR" the burst is a digital buzz | long pans, sentence starts, every cut (only 25 in 20 minutes) |
| TICK (graphic pop) | about 1.5 | -20..-30 | 0.06-0.2 s | 1.3-2.1 kHz glassy pop, a little noise, very quiet (side total -37..-44 dBFS) | numbered rings (4 ticks 1.0-1.4 s apart), shimmer on field loops, small labels | counters and bars (silent) |
| PULSE (tick ostinato) | 1 passage only (17:26-18:01, 35 s) | -17..-27 | each 0.03-0.06 s | tonal pluck 450-700 Hz on a 0.19 s grid (about 77 BPM sixteenths), with gaps: intervals 0.38/0.59/0.78 s; nothing above 3 kHz | rhetorical-fear passage "will we disappear? overdue, 2034", stops hard 1.3 s before the debunk | any explanation |
| Thunder-like rumble | 2 events in the opening | 0 | 0.4-1 s | sub rumble 20-90 Hz, soft onset | lightning shots at 0:09.7 and 0:11.5 | - |
| Ambience / room tone | none measured | - | - | the stereo side channel is digitally empty in OFF windows; between words the mid channel falls to -60 dBFS | - | nothing hisses under the voice |
| Music-off window | 7 places in 22.6 min (10 detections, every 3 min) | - | 3.0-7.7 s (13:17-13:34 is four broken ones) | the bed is cut within 0.3 s; the new cue starts at a hit as the window ends | question lines, reversal, uncertainty, the answer, "so what for us" | explanation, counters |
| End brand sting | 1 | -6 | drone 5 s | sub 24 Hz drone + wide pad | end card | - |

## 3. What makes it feel professional and subtle, and why the user dislikes "swipe" whooshes
### 3.1 Why it sounds expensive (measured)
1. LOW instead of HIGH. The impacts are single sine booms (27-66 Hz, under 3% above 1 kHz). On phone speakers they are barely heard, on headphones they are felt. Effects do not add a bright layer that fights the voice; the only high-frequency material in the whole film is 25 short air bursts (1.2/min), 6-10 kHz peaks at -8..-14 dB overall and a 10-15 kHz band 12 dB lower.
2. SHORT. The air bursts last 0.21-0.46 s (median 0.26 s), and the one long one (0.93 s) is on the title lock-up. There is no 1-2 s sweep anywhere.
3. NO REGULAR SWEEP SHAPE. Of the 30 detected bursts about half rise in centroid and half fall (the direction changes with the picture), so the ear never hears one "swipe" repeated. Our v4 used the same 0.9 s up-sweep (300 Hz -> 5 kHz) twenty-five times.
4. FLASHES GET A BOOM, NOT A WHOOSH. At 6:16, 9:02, 14:13, 18:25 the light-leak/flash cut is a sub boom with a 2-3 s tail and, at most, a 0.3 s air tick at -17..-20 dB vs voice; the riser before it (6:16.4-6:18.4, 14:44) is a sub swell with no noise.
5. SOUND ON REVEALS, NOT ON MOTION. Stamps, headline cards, face/label reveals, a bar jumping, a line drawn between two places and hard cuts get a hit. Explanatory moves (counter climbing to 183, the 120 km loop, bars growing) get nothing. Almost nothing sits on a sentence start; the voice always has the first word.
6. SPARSE. 5.4-6 effect events per minute including quiet ticks, one at most per 0.6 s, big ones about 1.3 per minute. Whole sections (9:11-9:50, 15:00-15:40, 18:05-19:36) are bed only.
7. SILENCE AS AN EFFECT. 7 music-off places of 3-8 s at the pivot lines; voice only and dry. The new cue starts with a hit as the window ends, which is the "drop".
8. ONE SOUND WORLD. The side channel self-similarity is 0.92 at 10 s lag and 0.78-0.84 at 2-10 min, so beds change by brightness, not genre; effects are all the same family (sub + short air + glass tick).
9. LEVEL DISCIPLINE. Voice peak 0 dB, bed -15, impact peaks -3, ticks -24, air -10..-14 overall; the loudest thing in the film besides the end card is the voice-level impact on the 3 biggest reveals (+6/+7 dB sub-band, which is low and brief).

### 3.2 Why "swipe-like" whooshes bother the user (these are the exact causes, all absent in the reference)
- A pitched/filtered noise sweep (low -> high or high -> low over 0.6-1.5 s) is the signature sound of a stock "swipe/transition whoosh"; the ear hears the movement of the filter as a "swipe" and it signals a template.
- It is repeated: same shape, same length on every cut (25 times in 12.5 min). Reference: 25 bursts in 20 min, each different in centroid, direction and length.
- It is bright: 3-8 kHz noise and an 8-14 kHz hiss sit on top of a dark bed and next to the voice's sibilance; reference 6-10 kHz is -8..-14 dB overall, with the 10-15 kHz band 12 dB lower.
- It is long and loud relative to the voice (0.9-1.5 s, -6..-10 dB); reference bursts 0.26 s.
- It is placed on cuts that have no motion in the picture and sometimes at sentence starts, so it competes with the first word.
- Rises before it (noise riser) build a "trailer" feeling. Reference risers are sub-only (nothing above 350-500 Hz) and only before a flash/title.
- It tends to be panned left-right. Reference bursts are centre-weighted.
HOW THE REFERENCE AVOIDS IT: low-pass at about 8-9 kHz and 12 dB of high-frequency roll-off, 0.2-0.3 s, centre, no pitch/filter movement, a short room tail, a sub boom instead of the whoosh on flashes, pitch-down (the sub glides 70 -> 31 Hz) instead of pitch-up, and ticks/stamps instead of sweeps for graphics.

### 3.3 Exact recipes for our own synthesis/sampling (tools/rc_sound.py style; do not copy any reference audio)
- BOOM: `sine(f0=62 -> 38 Hz exp glide over 0.25 s) * env(attack 8 ms, exp decay tau 0.45 s)` + 2nd harmonic at -18 dB, low-pass 400 Hz, 60 Hz high-pass off, peak -4 dB vs voice peak; second layer optional: 10 ms noise click band 700-1800 Hz at -26 dB vs the boom for hits on a cut (gives the 15% above 1 kHz seen on cut-hits).
- BOOM-soft/THUD: same sine 55-80 Hz, tau 0.12-0.2 s, level -8 / -13.
- RISE: noise lowpassed at 350 Hz (24 dB/oct) fading +20 dB over 1.2-1.8 s + sine glide 30 -> 58 Hz, abrupt stop (0.02 s fade) exactly at the BOOM; max peak -12.
- AIR: white noise -> band 1.5-6 kHz (HP 1.5k, LP 6k, then a gentle LP at 8 kHz), envelope attack 5 ms, decay tau 0.08 s to -30 dB at 0.25 s, a 4-6 ms comb/room reverb of 120 ms; do NOT automate the filter; mono or +-10% stereo width.
- TICK: damped sine 1.6 kHz (or 1.3-2.2 kHz) 8 ms attack, tau 25 ms, plus 5% noise; -24 dB; rising ladder for lists/squares (1.4 -> 2.0 kHz), falling for removals (1.8 -> 1.3 kHz).
- CLOCK: 30 ms band click 2 kHz + 400 Hz body, dry, -26 dB, 1 per second.
- PULSE (optional, not in this video unless a fear passage appears): 480-650 Hz plucks, 40 ms, on a 0.19 s grid with gaps.
- OFF window: gain to -80 dB in 0.3 s, back with a 1.5-2 s fade at the next cue.
- Thunder-like rumble (optional hook use): lowpass 90 Hz noise, attack 0.35 s, decay 0.8 s, -14 dB vs voice peak.

## 4. How this maps to video 002
See `channels/reality-check/stories/002_great-dying/long/sound_event_plan.md` (all 104 lines, absolute times, type, level vs voice, reason). Key mapping choices:
- 4 BOOMs (card "THE GREAT DYING" 0:24.4, flash into the catastrophe 1:49.8, Siberia reveal 5:20.4, "carbon dioxide" answer 6:20.5) + 12 BOOM-soft (flashes, "the biggest", 96%, killers, hope, last question, key stakes line, end).
- 4 RISEs, each inside a voice gap right before a flash/boom (1:47.9, 5:18.6, 9:03.3, 10:29.1).
- 8 MUSIC-OFF windows of 3-7 s at the question/answer/uncertainty lines (W1-W8).
- Scene-matched AMB beds only where the picture shows the thing: sea, dry wind, forest wind, eruption, lava (3 times), gas/bubbles, fire crackle, warm-water bubbles, soda fizz, cold wind.
- Counters, bars, gauges, timelines have no sound except one THUD when the value lands; list items and squares get quiet ticks; the 4 killers (list) get 4 ticks.
- No whoosh sweeps, no noise risers, no stereo swipes anywhere.

## 5. Source list (free, commercial-safe) and searchable sounds
Licence rules for us: use CC0 or Pixabay/Mixkit-style licences with commercial use and no attribution; CC BY is allowed only if the credit goes in the description (log it in `shared/assets_license.csv`); reject CC BY-NC, "personal use", BBC RemArc (non-commercial), and any file with a content-ID claim. Verify each Freesound file's licence through the API field `license` (existing convention in the csv: "CC0 (verified via Freesound API)"). Download only what the plan needs; synthesise BOOM/THUD/RISE/TICK/CLOCK/AIR ourselves (no licence needed).
| source | licence | note |
|---|---|---|
| Freesound.org (filter License = Creative Commons 0; or CC BY with credit) | CC0 / CC BY 4.0 per file | best for ambience; check file licence every time; avoid CC BY-NC and sampling+ |
| Pixabay Sound Effects (pixabay.com/sound-effects) | Pixabay Content License: commercial use, no attribution; cannot resell the sound standalone | good for risers/impacts, but its "whoosh/swish" library is exactly the swipe style: take only booms, ambience, ticks |
| Mixkit sound effects | Mixkit licence: free for commercial use, no attribution (cannot be sold standalone) | ambience and UI ticks |
| YouTube Audio Library (Studio -> Audio library -> Sound effects) | free for use in YouTube videos; check the per-track attribution flag | already usable for our channel; safe for Content-ID |
| Sonniss GDC Game Audio Bundles | royalty-free commercial licence, no attribution | large high-quality packs of impacts, ambience, drones; keep the licence text with the pack |
| NASA / USGS audio (volcano, sonification, Earth sounds) | mostly public domain (NASA media guidelines: no implied endorsement); check each file | for eruption/rumble references |
| Own synthesis (tools/rc_sound.py, numpy) | own | for BOOM, THUD, RISE, AIR, TICK, CLOCK, OFF |

Search keywords by type (use "CC0" filter on Freesound; length 1-10 s for events, 20-90 s loops for ambience):
- BOOM / sub: "sub drop", "cinematic sub boom", "low impact 40 hz", "deep boom single", "sine sub hit"
- THUD: "soft low thud", "kick drum sub single", "heartbeat thud soft"
- RISE: "sub riser", "reverse swell low", "drone swell tension" (reject anything bright, "noise riser", "white noise sweep")
- AIR (instead of whoosh): "air puff short", "breath of air", "soft air burst", "air hit short" (reject "swipe", "swoosh", "whoosh long", "transition sweep")
- TICK: "ui tick glass", "soft pop ui", "interface blip soft", "pluck click short"
- CLOCK: "analog clock tick single", "wall clock tick slow"
- AMB sea / wind: "ocean waves distant calm", "desert wind soft", "forest wind leaves soft", "cold wind soft", "wind gentle howl low"
- AMB eruption / lava / gas: "volcano rumble distant", "eruption rumble low", "lava crackle", "lava flow rumble", "gas hiss steam low", "fire crackle low"
- AMB water: "underwater ambience low", "underwater bubbles rising", "bubbles stream soft", "soda fizz short", "carbonated drink fizz"
- Thunder (optional): "distant thunder rumble low"
(That is 30 concrete queries; the ambience set is what the video really needs: sea, wind x3, eruption, lava x2, gas, fire, bubbles x2, soda.) Candidates already in the repo (shared/assets_license.csv): desert/mountain wind and gentle breeze files (felix.blume, petebuchwald, mario1298, CC0), "light slow swoosh" (CC0, only as a quiet AIR if rewritten; do not use unfiltered), night ambience. Reuse before searching.

## 6. Deletion log
Deleted after the analysis: the whole `study/ref_sound_QsHQxRlBy6Y/` folder (video 65 MB, caption file, 32 kHz decode, cut list, feature files), and my temporary frame/contact-sheet/spectrogram files in the scratchpad. Kept: this written analysis and our own derived recipes only.
