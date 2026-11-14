# Study: Dhruv Rathee - "Something Weird is Happening Inside Earth" (2026-11-13, 22:39 incl. 84 s sponsor block, Hindi, 480p study copy)

Study date 2026-11-14, RULES 12c: yt-dlp without login, media only in git-ignored `study/`, deleted after analysis. Technique only: no frame/clip/audio/voice/script phrase/title/thumbnail of this video is reused. Topic of the video: Earth's magnetic north pole drift, pole flips, the 42,000-year-ago event, the satellite "Bermuda Triangle". Presenter-led (host on a chroma-key aurora set, about 30% of screen time) plus a heavy graphics/AI-footage layer (about 70%). Our channel is faceless, so the presenter beats must be replaced by a "reset" beat (see section D).

How measured: ffmpeg ebur128, scipy STFT, mid/side split (side channel = music/ambience proxy, voice is almost all mid), 100 ms RMS frames, scene detect (threshold 0.4, cuts <0.5 s merged), 272 frames at 5 s (14 contact sheets) plus full-size frames at graphic moments, and the channel's own Hindi captions (machine translation to English) for timing and structure. Limits: no stem separation, so music level under voice is an estimate (a range); instrumentation is inferred from spectrum, not heard note by note; tempo detection says "no steady pulse".

---------------------------------------------------------------------------
## A) BACKGROUND MUSIC (priority)

### A1. Character in one paragraph
A single, consistent "dark cinematic ambient bed": low drones/pads and sub-bass weight, no drum kit, no melody hook, no steady beat. Autocorrelation tempo confidence in the body is r = 0.06-0.15 (no pulse; values below 0.3 mean "none"); onset density only 1-2.5 per second and most of those are speech or SFX. Music-only moments (no voice) show sub+bass carrying the energy: band shares relative to total: sub (20-100 Hz) -2 to -6 dB, bass (100-250 Hz) -3 to -9 dB, mids -3 to -11 dB, highs 4-12 kHz -9 to -28 dB, so it is bass-heavy and dark (spectral centroid 155-570 Hz of the full mix in music-only spots; 500-1300 Hz of the side channel in the body). Genre in words: hybrid cinematic/ambient underscore: slow evolving synth-pad and low-string-like drone, soft sub impacts, risers/reverse swells and hit stings at transitions. No percussion groove at all. Mood: serious, uneasy, curious, "something is happening under your feet", never triumphant, never comic. The same timbre is used for the whole video: spectral self-similarity of the side channel is 0.92 at 10 s lag and still 0.78-0.84 at 2-10 minute lag, i.e. one sound world, ~9-12 cue regions that change slowly, no stylistic jumps and no loop that you "notice".

(Exception: the sponsor block 1:54-3:17 has a lighter, brighter bed, about 6 dB quieter in the side channel than the intro; it is a separate cue and is excluded from the comparisons below.)

### A2. Level numbers
- Whole-file loudness (voice + music + sfx): -16.7 LUFS integrated, loudness range 5.4 LU (LRA low -19.8, high -14.5), true peak +0.8 dBFS (slightly hot, YouTube will normalise it down).
- Voice-active frames (100 ms RMS, mid): P90 about -15.6 dBFS, median over the body about -22 dBFS (averaged speech+pauses), mean body RMS -19.4 dBFS.
- Music bed under speech (pause-only frames, 122 s collected from the 3-20 min body): -34.8 dBFS RMS. So the bed sits about 15-16 dB below the speech level (range by minute: 12 dB in the first 3 minutes and last minute, 15-19 dB in the body, 20 dB at 19-20 min). In LU terms: bed about -15 to -20 LU below the voice; during the intro and outro it comes up to about -12 LU.
- Full-level music (no voice): -14.6 dBFS (0:16-0:20 hit), -17.5 (title sting 1:48-1:54), -15.7 (outro drone 22:31-22:36). Voice and music peaks are therefore about equal when voice stops: the music rides about +18-20 dB above its under-voice level in voice gaps (that is the "swell").
- Per-minute pause floor (P10 of 100 ms RMS) drifts from -26 dBFS (min 0-1) to -31..-36 (min 5-20): the music gets quieter as the video goes on and the explanation gets denser. It comes back up at the very end (-28 in the last minute).
- Side-channel (music proxy) median per minute: -32 (min 0-2), -38..-40 (min 2-5), -41 (min 5-20), -37..-38 (min 20-22). Same story: loud open, quiet middle, small rise at the finish.

### A3. Section-by-section music map (energy 1-5, 5 = most; measured from side-channel level, bass level and event density; times m:ss)
| Section | Voice content | Music | Energy |
|---|---|---|---|
| 0:00-1:44 cold open | the mystery event, species vanish, the sky "breaks", then today's satellite glitch | Big, bass-heavy, bright-ish cue with hits at 0:07-0:09, 0:15-0:20 (the loudest 4 s of the open), 0:25-0:29, 1:25-1:27; first 6 s already at full bed (M -16 dBFS) | 4-5 |
| 1:44-1:54 | "let's understand this" + "Video #" title card | Sting/title hit, S -23 dB at 1:50, music-only 1:48-1:54 | 4 |
| 1:54-3:17 sponsor | own-course promo | Lighter, quieter bed (S -37..-41 dB), upbeat-neutral, separate cue; flash-wipe whooshes | 2 |
| 3:17-3:22 | content restarts: "to find the answer we dive under our feet" | Total silence (3:20.2-3:22.5 side channel empty, M < -40 dB at 3:16-3:17) then bed in | 1 |
| 3:22-4:25 Earth layers / outer core | numbers: 4 layers, 2,250 km, 2,900 km, "sea of molten iron" | Low drone, sub weight (L band -27 to -29), S -33..-36; slight rise 3:30-3:50 as the core animation spins | 3 |
| 4:25-5:45 two north poles / compass | misconception reveal, 120 km loop per day | Quietest-ish pad (S -39..-45), low movement, a hit at 4:23-4:26 (sun vs "magnetic shield") | 2 |
| 5:45-6:08 | opposite poles attract | pad continues, S -40..-44 | 2 |
| 6:08-6:15 | "why does the pole keep moving? go 200 years back" | music OFF (6:08.4-6:15.4; M falls to -40 dB at 6:12) | 1 |
| 6:15-7:20 Ross 1831 story | explorer, compass needle, flag on stones | cinematic cue restarts after the red/orange flash at 6:16 with a hit at ~6:18; low, steady, S -37..-45 | 3 |
| 7:20-8:20 speed up | 9 -> 15 -> 55 km/year, bar chart, cricket pitch, "it started to run" | slight swell at 7:45 (S -32 on "started to run"), then back to -37; bass bed (L -34..-28) | 3 |
| 8:20-9:05 NOAA emergency update | WMM updated 10 months early | calm pad S -36..-40 | 2 |
| 9:05-9:11 | "you might wonder, what difference does it make to us" | music OFF (9:05.5-9:11.6, white flash) | 1 |
| 9:11-10:36 airports, Maps, military | runway numbers, phone compass | light pad, S -40..-44 (min 9:25-9:55) then rising S -36..-33 at 10:05-10:35 as stakes rise | 2-3 |
| 10:36-10:44 | "but why is the pole pulled so much?" | music OFF (10:36.7-10:43.9) | 1 |
| 10:44-12:15 the two lobes / tug of war | science paper, red lobes, flow change 1970-99 | thin, low bed, S -39..-42, centroid of side drops to 450-650 Hz (darker, more static) | 2 |
| 12:15-13:20 Brunhes 1905 | lava layer as "stone compass" | warm cue, story tone, S -38..-45 (quiet, almost nothing: voice carries) | 2 |
| 13:20-13:34 | "scientists made fun of it for decades ... in 1960 a map in the ocean proved him right" | music dips to -50..-52 dB side, OFF 13:24.0-13:34.0 | 1 |
| 13:34-14:40 ocean-floor zebra / tape recorder | zebra stripes, mirror images, "tape recorder" analogy | bed back, S -36..-45, short sub-hit about 14:40-14:48 (S -29, L -23) when the numbers are revealed | 3 |
| 14:48-15:40 183 flips counter | 183 flips, every 4.3 lakh years, last 7.8 lakh years ago | bed S -41..-44, calm: the counter animation is the event; no music hit | 2 |
| 15:40-17:20 Laschamp / 2021 study / Neanderthals | scary claim | lowest sustained bed (S -41..-44, pause floor -32..-35) | 2 |
| 17:20-18:05 "will we vanish? next flip 2034" | rhetorical build, "overdue" | S -45..-51 (about 6-8 dB drop for 30 s, then recovery to -42 at 18:00): the quietest 30 s of the film, no hits | 1-2 |
| 18:05-19:38 the debunk / "not so bad" | NASA: field weakens, does not vanish; counter-study; flip takes 1-10k years | bed stable at S -40..-43, centroid of side only 410-540 Hz (the darkest and calmest cue) | 2 |
| 19:38-19:42 | "no mass extinction found. research still going on" | music OFF (19:38.6-19:42.1, S -52..-64 dB) | 1 |
| 19:42-20:15 animals | whales, turtles, birds | light bed with a slight lift (S -35 at 20:10-20:20) | 2 |
| 20:15-21:40 modern tech / satellites / Bermuda Triangle of space | today's risk, tie back to the hook | S -33..-38 (louder, about 5 dB above the debunk section), centroid 1000-1300 Hz (brighter), hits at 20:22 (field animation), 20:37-20:47 | 3-4 |
| 21:40-21:44 | "it never stayed in one place; today the speed has decreased" | music OFF (21:40-21:44) | 1 |
| 21:44-22:08 closing facts, question to viewer | speed 50-60 -> 35 km/yr; "will humans see the next flip or finish before?" | bed returns S -42..-47 then lifts | 2-3 |
| 22:08-22:36 end screen | "watch the Neanderthal video", sponsor reminder | brighter sting 22:05 (S -33), brand sting + sub drone 22:31-22:36 (S -22, loudest music of the film: -15.7 dBFS, centroid 155 Hz) | 4 |

Energy summary: steps of about 1-2 levels, not smooth curves. Min = 1 (silence), max = 5 (cold open 0:15-0:20). The body sits at level 2 (about 60% of runtime), level 3 for 4 "story/scale" passages, level 1 at 8 pivot points. Opening 105 s are 4-5; first 3 s are not silent.

### A4. Drops to silence (the technique to copy)
Near-silence (side channel empty, mid below -40 dBFS at the gap) happens 8 times in 22 minutes, each 1.5-8 s long, about once per 2.3 min, ALWAYS at a pivot line, never mid-explanation:
1. 3:16-3:22 content restart after the sponsor block ("dive under our feet")
2. 6:08-6:15 "why does the pole keep moving? go back 200 years" (turn to the history story)
3. 9:05-9:11 "what difference does it make to us?" (turn from science to relevance)
4. 10:36-10:44 "but why is the pole being pulled so hard?" (turn to the cause)
5. 13:24-13:34 "scientists made fun of it for decades... then a map in the ocean proved him right" (reversal)
6. 19:38-19:42 "no mass extinction was found; research still going" (uncertainty line)
7. 21:40-21:44 "it is shifting because it was never in one place; today the speed has fallen" (the answer)
8. 22:xx end of speech before the brand sting.
Nearly every one is paired with a visual reset: a light-leak/white flash 0.4-0.6 s (6:16, 9:02, 11:42, 14:17, 16:22) or a hard cut to the presenter. Rule: a question or reversal line gets silence under the first 3-6 s, then the bed comes back on the next sentence with a soft hit.

### A5. Swells / hits and SFX
- Side-channel events above -27 dBFS and shorter than 1 s: about 40 in the body, 1.9 per minute, mostly 0.3-0.7 s whooshes on flash transitions, number labels and graphic entrances (e.g. 4:23, 6:46, 7:44 "started to run", 8:15, 13:28, 14:40-14:48, 20:22, 21:00). These are SFX (whoosh, impact, soft glitch), not music. Sustained music swells above -27 dB for 2-6 s: 0:15-0:20, 1:48-1:54, 2:03-2:10 (sponsor), 4:23-4:26, 22:31-22:36.
- Every impact sits on a visual event (globe spin, animation start, flash, title) and almost never on a sentence start.
- Ambience: none audible except the wind/ocean-like bed of the stock footage where the footage is shown (very low). No room tone gaps: even in pauses the floor is -30 to -35 dBFS (so the bed never drops out except at the 8 pivot points).
- Voice: recorded close and dry, even, level -15..-17 dBFS peak band, light de-essing; no reverb.

### A6. Cue changes
Novelty (side-channel spectrum) peaks at about 3:20, 4:20, 7:30, 10:50, 14:50, 17:30, 18:10, 19:40, 21:50, plus the silence breaks above: roughly 9-12 cue regions, so a cue change about every 2-2.5 minutes, 6-8 of them hidden inside a silence gap or flash transition (the new cue starts when the gap ends). Repetition vs progression: same palette throughout (self-similarity 0.78-0.92), cue to cue differences are in brightness and density, not genre; no recurring melodic motif. Progression is "dark -> a little brighter near the tech/satellite stakes -> brand sting at the end".

### A7. How to find the same character (free tracks)
Search terms (Pixabay Music, YouTube Audio Library, Kevin MacLeod "Dark / Ambient / Suspense" and "Cinematic"):
1. "dark ambient drone" / "cinematic drone" (no beat)
2. "documentary underscore" "investigative" "tension pad"
3. "cinematic ambient", "space ambient", "deep space", "sci-fi ambient", "ethereal pad"
4. "low strings tension", "suspense ambient", "mysterious"
5. "sub bass hit" / "cinematic impact" / "riser" / "reverse swell" for stings (separate short files)
6. "documentary background" "no drums" "minimal"
7. Kevin MacLeod (incompetech) genres: "Dark", "Ambient", "Suspense" (examples to audition: Dark Fog, Ossuary series); avoid driven/trailer-style tracks. Verify each track's licence in shared/assets_license.csv before use.
8. BPM: not needed (no pulse); if the track has one, choose a very slow 60-80 BPM pulse that is below -25 dB; reject anything with a clear 100+ BPM beat, hi-hats, or a melody lead.
Keep: stereo wide pad, sub weight, 2-3 min tracks with slow evolution. Reject: epic trailer percussion, piano melodies, glitch/techno, lo-fi.

### A8. Cue-sheet template for a 12-14 min science documentary (our format; levels 1-5, under-voice bed level in dBFS RMS where our voice peaks about -15 dBFS)
| Time | Role | Level | Notes |
|---|---|---|---|
| 0:00-0:08 | cold-open image + first sentence | 4 | bass drone + 1 riser into the first number; hit at 0:05-0:08 |
| 0:08-0:45 | hook story | 4 -> 3 | bed at about -12 LU under voice, 2-3 SFX hits on graphic entrances |
| 0:45-1:00 | "the question" line | 1 | music OFF 3-5 s, then soft pad back in |
| 1:00-3:00 | setup + scale numbers | 3 | -16 LU under voice, slight rise on the number reveal |
| 3:00-6:30 | mechanism block 1 | 2 | quiet pad, -18..-20 LU, sub drops only on a diagram's first move |
| 6:30 | pivot ("but why?") | 1 | OFF 3-6 s + light-leak transition; new cue starts |
| 6:30-9:30 | story / history block | 3 | warmer cue, centroid higher, -16 LU |
| 9:30 | pivot (reversal / "what scientists found") | 1 | OFF 3-6 s |
| 9:30-11:30 | evidence / counter-evidence | 2 | calmest cue, -19..-20 LU; no hits |
| 11:30-12:30 | stakes / "so what for us" | 3 -> 4 | brighter, bed +4 dB, hits on the 1-2 key lines |
| 12:30 | answer line | 1 | OFF 3-4 s |
| 12:30-13:30 | close + callback to hook | 2 -> 3 | bed back to -16 LU |
| 13:30-end | end card | 4 | brand sting + sub drone, music-only 5-6 s |
Total: 8-10 cues, 5-7 silence gaps of 2-6 s, 1 loudest section (the open), 1 quietest section (the debunk/uncertainty block), SFX 1.5-2 per minute.

---------------------------------------------------------------------------
## B) EDITING

### B1. Shot length and cut rate (scene detect threshold 0.4, cuts closer than 0.5 s merged; dissolves and continuous moves are not counted, so real visual change is higher)
- Detected shots 224 in 22:39 content; length percentiles 10/25/50/75/90 = 0.8 / 1.9 / 4.0 / 7.5 / 13.2 s; mean 6.0 s; max 35.5 s (a talking hold). Under 1 s: 12%, 1-3 s: 23%, 3-6 s: 30%, over 6 s: 34%.
- Cuts per minute by 2-min window: 9.5, 7, 4, 11, 11, 9, 10.5, 12, 8.5, 12.5, 13.5, 3.5. The 4-6 min window (concept of "two poles") is the calmest (4/min); fastest at the end of the evidence (18-22 min) 12-13/min. Looking at 5 s contact sheets, a new image appears at least every 5 s in 95% of samples (counting dissolves, animated graphics and light-leaks). Average information change ~ every 4 s.
- Screen-time split (272 frames at 5 s): host on camera about 30% (81 frames, 6.7 min, average 5-15 s per appearance, 45 appearances); explanatory graphics about 40%; archival/AI-generated footage about 18%; article/paper/screenshot cards 12% (about 33 frames); sponsor block 5%. Host never talks to camera for more than 35 s (the max 35.5 s shot is the sponsor).
- Pattern: host (5-15 s) -> graphic or footage for the explanation (10-25 s) -> host line (5-10 s) -> next graphic. The host is a punctuation line for the key sentences (a rhetorical question, a rule, a transition), not the main picture.

### B2. Cut types
- Hard cuts: majority (about 70%).
- Light-leak / film-burn flash wipe (orange -> red -> white, 0.4-0.6 s with an SFX whoosh, bright flash frame at the middle) used at 6:16, 9:02, 11:42, 12:12, 14:17, 16:22 and into/out of sponsor segments: at the start of a new block/question (about 1 per 2-3 min, always a section boundary). Matching music silence follows the flash.
- Dissolve / soft cross-fade for graphic-to-graphic (e.g. map to map, 0.3-0.5 s).
- Blur pull-in (defocus to sharp, 0.5 s) used after the sponsor block into the science (3:17) and for the "title" returns.
- Match/zoom-through (globe rotate to another map view); "page turn" to a notebook sheet (4:12, 5:47); the jump from the host into a graphic uses a quick push-in on the graphic's first frame.
- Glitch/blur in the red-flash (6:17).

### B3. Camera moves and motion
- Every still is moving: slow push-in or parallax (AI re-enactment stills: ship/compass at 6:27-6:55, lab at 12:32-13:17); AI footage is labelled "REPRESENTATIONAL" in small caps top-right.
- 3D fly-over (7:22 ice landscape with a thin line drawn into the distance, 12:52 magma), globe rotates on every earth view; map zooms from a polar overview to a close label and back.
- Map elements draw on: dots appear, a dashed/solid line is drawn over 2-3 s, labels pop with a small tick.
- Host shots: medium close-up, subject slightly off-centre (left third in about half, right third in the other half, alternating so overlays fit), no camera move, occasional punch-in (about 8%), hand gestures, light vignette.

### B4. Colour grade and palettes
- Dark "science" scenes: near-black (#0A0C10-#10141A) background, desaturated; accents orange (#FF9F43-ish, for the magnetic field and the pole), red (#E8262B, alerts/key data), yellow highlighter (#F2E22F), cyan-teal map ocean (#1FA9BC), green glow (#45E58B for labels like "4 LAYERS" and depth numbers).
- Parchment/sepia scenes (history/geology: flip-record chart, Ross map, ocean-floor zebra): cream #E9D8B4 background, brown linework, red counter number, typewriter/mono caps title (e.g. "MAGNETIC REVERSAL RECORD").
- Document scenes: paper-white (#F4F2EA) or dark news page with logo top-left, serif body.
- Host set: virtual aurora/forest/campfire backdrop (green-red aurora, black pine silhouettes), the host in a navy tee; the backdrop supplies the only saturated colour, so it also acts as the "channel look".
- Overall: warm highlights, deep blacks, bloom on glows, slight film grain on archival; no teal-orange look.

### B5. Text, lower thirds, chapter cards
- No chapter cards, no section titles. Sections are marked by (a) a flash transition, (b) a rhetorical question line from the host, (c) a theme change of background colour (dark, then parchment, then paper). A "VIDEO #" counter and a brand/title lock-up appear only once, after the hook (1:48-1:54, glowing white sans caps over the globe), plus one big title "BERMUDA TRIANGLE OF SPACE" (at 1:42 and again at 21:12, same type: bold geometric caps with soft glow, 12% of frame height, centred).
- Labels on host shots: year chip top-left (white box, dark bold caps "1990", about 7% height, appears 1 s after the word), glowing electric "?" top right at a question line (1:07, 9:07), "LINK IN PINNED COMMENT" caps at bottom, QR at top-right (sponsor).
- Date/location lower third on footage: "1 JUN 1831" white bold caps on a black rectangle at the left, upper-mid third (about 20% from the top, 5% from the left edge) while the picture's lower area stays clean. "EL CASTILLO CAVE / Cantabria, Spain" is a pin label with a thin leader line to a boxed citation card (logo + 3-line serif/sans quote) at the right 45% of frame.
- Tags: "SOURCE: AUTHOR ET AL (YEAR)" small caps bottom-right (about 2.5% height) on every chart/map/paper; "REPRESENTATIONAL" top-right on AI/CG; "COURTESY: <channel>" bottom-right on stock.
- Max 2 text elements at once. Body text of article cards is shown large (about 3.5-4.5% of frame height per line, 6-9 lines), and read aloud while a highlighter sweeps the key words.

### B6. Graphics catalogue (what is used for which statement type)
| Statement type | Graphic | Position in frame | Style/animation | Sync to words |
|---|---|---|---|---|
| structure/depth (core, layers) | 3D cutaway globe, concentric layers, glowing core | centre, 60% of height | rotates; label call-outs with thin leader line; numbers count "2,900 KM" in green bold sans top-left; depth ruler vertical at right edge with a travelling dot over stock rock/lava footage ("DEPTH 265 km" yellow mono) | label appears exactly on the spoken number; ruler scrolls as the narration "dives" |
| process (currents, field lines) | animated thin orange field lines around Earth; yellow coils inside the core; sun vs shield | centre or left 60% | slow loop, lines draw on over 2-3 s | stays while the explanation is spoken |
| geography claim (2 points + distance) | dark satellite polar map or flat blue map with white outlines | full-screen, labels at points, distance chip on the line | points pulse, dashed line draws 2-3 s, label chip dark box + white caps | each label appears on the word naming it; the line draws while the number is spoken |
| time series / speed (km/year) | bar chart on near-black, white bars, the "scary" bars switch to red | chart fills 85% of frame; title red caps top-left; values bold white above each bar; source bottom-right | bars grow left to right one per spoken value; a green trend curve draws over; the y-axis rescales (from 15 to 60) to show the jump | each bar appears as its number is spoken; the 4x jump = axis rescale + red recolor |
| scale analogy (cricket pitch / Delhi->Kanyakumari) | simple vector pitch with bracket "~40 m"; India map with a vertical line | full-screen / centre | line draws on | analogy graphic appears at the end of the analogy sentence (0.3 s early) |
| "proof" source | article/paper/web page screenshot (NASA, NOAA, NPR, journal) | full-screen, logo top-left | yellow/orange highlighter sweeps phrase by phrase while it is read; circles drawn around dates; red highlighter on the sceptic sentence; paper zooms into a figure | the highlight starts on the first word of the spoken quote and ends on the last word |
| history (explorer, lab, ship) | AI/CG re-enactment video stills with push-in, "REPRESENTATIONAL" tag | full-screen | slow push-in, flares, shallow depth of field close-ups on the object (compass needle) | the object close-up arrives when the object is named |
| encyclopedia items (extinct animals) | 3 to 6 vintage illustrations as polaroid/cards on dark | grid 3x2, each 25% of width | card flips/stamps, a red "EXTINCT" stamp (about 20% of frame) hits at the verb | stamp lands on the word "vanished" |
| count/record | "magnetic reversal record" barcode chart with a counter (FLIPS 11 -> 183), timeline scrubbing from 8 crore years to today | full-screen parchment | the barcode scrolls, the counter increments | counter reaches 183 on the spoken number |
| feeling/risk (phone map, airport cockpit) | human-scale stock (hand on phone map, cockpit compass, runway numbers) | full-screen | stock with slight push-in; the red/white runway numbers highlighted | each footage item matches a noun in the line |
| "?" beat | glowing electric blue "?" | host shot top-right, 12% of height | lightning outline pulses | on the question line |

### B7. B-roll variety and repeats
- 15-20 unique graphic families; Earth globe (stock-like CG) re-appears 12+ times but always with a different data layer (UV, magnetic field, pole path, anomaly map, satellite glitch), so repeats look purposeful. Stock footage was almost never reused for a different claim (only the host set repeats, which is the channel's anchor). 33 article/paper cards each tied to a different claim and each with its own highlight.
- Mixed sources: real documentary clips (credited "COURTESY" bottom-right), NASA/NOAA/ESA CG, AI re-enactments (tagged), vintage line art, own vector charts.

### B8. First 30 s (hook)
0-8 s: one precise claim ("42,000 years ago, something broke the sky") over a Hollywood-style Earth-from-orbit shot; 8-20 s: aurora with silhouetted early humans, magnetic field line CG, sun flare (each shot 3-5 s, with sub hits at 0:15-0:20); 20-30 s: UV radiation meter graphic ("NORMAL -> EXTREME" tick bar, white caps bottom-centre), a news/academic headline card with a key phrase highlighted ("... CAUSED MASSIVE SUDDEN CLIMATE CHANGE", red highlight), then the host appears at 0:32 (first face at 32 s). 0:32-1:05: cave art, extinct animals stamped, the Neanderthal mention; 1:05 asks the real question; 1:08 gives a vague answer ("under our feet, 3000 km deep"); 1:16 jumps to "today, 2026" with the satellite glitch; 1:44 "let us understand". So: claim -> consequences in a rising list (5 items in 40 s) -> the question -> a teaser that it is happening now -> promise. First 105 s are the strongest music and the highest cut density.

---------------------------------------------------------------------------
## C) EXPLANATION

(from the channel's own Hindi captions; Hindi/Hinglish: the narration is simple Hindi with common English words and numbers; I give English paraphrases only.)

- Hook timing: question stated at 1:05 (65 s in), teaser at 1:16 (76 s), "let us understand" at 1:44 (104 s). Face-time begins at 32 s. 82 s of "claim -> question" before the host promises to explain. (Too long for us as is: we should state the question inside the first 25-35 s.)
- Sponsor block 1:54-3:17 (84 s, own products) is a hard mid-roll after the hook; content restarts with a blur and silence. Skip for our channel (no sponsor), but note it comes after the hook, before any explanation.
- Structure of the explainer (content from 3:17 to 22:08, 18:51): 1) layers of Earth, molten-iron sea (3:17-4:30, 1.2 min) -> 2) the magnetic field as an invisible shield (4:23) -> 3) common misconception: two North Poles (4:40-5:45) -> 4) the question "why does it move?" (6:10) -> 5) a 1831 story (6:14-7:15) -> 6) numbers ladder of speed (7:16-8:20) -> 7) an Indian-scale analogy (8:24) -> 8) real-world stake: NOAA emergency update (8:33-9:00) -> 9) "what difference does it make?" airports/Maps/military (9:02-10:35) -> 10) "why?" two lobes tug of war (10:38-12:10) -> 11) "this is where the real fear begins": flips (12:12) -> 12) a second story (Brunhes 1905, 12:30-13:30) -> 13) the ridicule then proof (1960 ocean-floor stripes, zebra and tape-recorder analogies, 13:34-15:00) -> 14) 183 flips, the average, "listen carefully" (15:00-15:40) -> 15) the apparent contradiction (42k years ago) answered: a temporary flip (15:38-16:10) -> 16) the scary claim with sources (16:10-17:00) -> 17) rhetorical fear question "will we vanish?" (17:17) -> 18) "next flip overdue; 2034 +/- 3" (17:35) -> 19) counter-voices: random, not sudden, 1-10k years, "your children's lifetime is shorter than the flip" (17:49-18:30) -> 20) NASA: weakens not vanishes; the 2021 claim was challenged (18:42-19:36) -> 21) honest verdict: "research still going on" (19:36) -> 22) what is certain: animals that navigate (19:41-20:15) -> 23) biggest risk is modern technology/satellites, back to the hook's Bermuda Triangle (20:27-21:23) -> 24) the answer to the opening and the current speed (21:23-21:55) -> 25) closing question (21:55-22:08).
- Pattern: problem -> story -> number -> everyday consequence -> deeper "why" -> scare -> honest limit -> tie back to the hook. Roughly 3 mini-arcs of 5-7 min each; at each boundary a "But / Now the question is" line plus silence plus a flash.
- Rhetorical questions: 12 question marks in 21 min of speech (about 0.6/min) and a "you might wonder / you might think" turn at 4:40, 7:07, 9:02, 12:12, 15:38, 17:17, 18:08. Every question line is spoken to the camera.
- Sentence length (English rendering of Hindi cues, 257 sentences): mean 13.3 words, median 12, 90th percentile 22; 25% are 8 words or fewer. Speech rate approximately 165 English words per minute of the translation (Hindi spoken at a calm, steady pace, no hurry, pauses of 0.4-1 s at pivot lines). Short sentences carry the key facts ("It is a fixed point.", "That is, Magnetic North Pole."); long sentences only carry lists of causes.
- Analogies (all physical, local or school-textbook): "sea of molten iron" (spinning currents), "invisible shield", school-book magnet picture vs reality ("it is drawn as a magnet but there is no magnet"), the compass needle as a small magnet (opposite poles attract, shown with a paper-sheet bar-magnet diagram), "where the needle bends straight down", cricket pitch (40 m per day), "think of it as Delhi moving beyond Kanyakumari" (Indian scale for a distance), runway numbers = compass headings (180 degrees = runway 18), zebra stripes (sea-floor magnetic stripes), "seabed as a tape recorder", "stone compass" (lava crystals freezing the field direction), "tug of war" between two lobes, "your children's children's whole life is shorter than the flip". About 11 analogies in 19 minutes = one per 1.7 min, each with its own visual built from the analogy's object.
- Number handling: 97 numbers in the speech, about 4.7 per minute; numbers always come as a ladder or comparison, in units the viewer knows: km per year, then metres per day, then cricket pitches; "9-15 km/yr" -> "55 km/yr" -> "4 times"; "1600 km" -> "390 km"; "183 flips / 4.3 lakh years / 7.8 lakh years ago"; big numbers use Indian units (lakh, crore: "8 crore years", "4.3 lakh years"). Each number appears on screen the moment it is said (bar label, counter, chip), then is converted into a human unit within 5-8 s.
- Recap/repeat: key figures restated 2-3 times ("every 4.3 lakh years" at 15:18, 15:26, 17:28; "7.8 lakh years ago" at 15:34, 17:32; "Bermuda Triangle of space" at 1:40, 21:09), with "listen carefully" before the one number that matters. The hook's question is answered explicitly at 21:23-21:40.
- Sources and honesty: every scientific claim has a screenshot card with logo (NASA, NOAA, USGS, NPR, a journal, a press release), source line "SOURCE: AUTHOR ET AL (YEAR)", and the opposing paper is shown as well (2021 claim, then the comment paper in red) with the line "this proposition is unproven"; the speaker ends with "research is still going on". So the video builds trust by displaying the dissenting source on screen. Strongly consistent with our RULES (every fact [F#] with 2+ sources and a Munshi fact check).
- Tone/language: friendly, conversational, a bit dramatic at the hook ("seemed to break the sky"), calm and analytical in the middle, reassuring at the end ("the good news is..."). Plain words, English technical terms kept (magnetic field, lobes, excursion), no jargon without a gloss in the same sentence. Direct address "you". Pronunciation corrections included in the speech ("not X, X") are kept as humanising slips.

---------------------------------------------------------------------------
## D) APPLY TO THE NEXT VIDEO (Reality Check, faceless, plain Hindi) - checklist with numbers

MUSIC
- [ ] One bed family for the whole video: dark cinematic ambient drone/pad with sub weight, no beat, no melody (A7 keywords). 8-10 cue regions of 1.5-2.5 min, all the same family (brightness and density change, not genre).
- [ ] Level: bed 15-16 dB below speech in the body (target about -35 dBFS RMS under a voice at -19/-15 dBFS peaks), 12 dB in the first 90 s and the last 60 s, 18-20 dB in the debunk/uncertainty block. Integrated mix near -16..-17 LUFS (true peak under -1 dBFS; the reference was +0.8, do not copy).
- [ ] 5-7 silence gaps of 2-6 s (music OFF to under -40 dBFS at the gap, voice only), at pivot lines only: "why?", reversal, "so what", the answer. Start the new cue right after the gap (the gap hides the cue change).
- [ ] Opening: bed already audible at 0 s, one big bass hit/riser at 0:05-0:08 and again as the question/first scale number lands; the loudest music-only moments are the open (4 s at about -15 dBFS), the title card, the end card.
- [ ] SFX: 1.5-2 per minute, whooshes on flash/section transitions and number labels, a soft sub hit when an animation starts; never on a sentence start.
- [ ] Quietest cue (about 6-8 dB lower than the others, no hits) for the explanation of the hard/uncertain science; brighter, slightly louder cue for the "what it means for us" stakes block (about +4 dB); finish with a brand sting + sub drone, 5-6 s music-only.
- [ ] Search/make free tracks with the A7 keywords; keep stings as separate short files.

EDITING / GRAPHICS
- [ ] Visual change at least every 5 s, median shot 4 s, 8-13 hard cuts per minute with dissolves and animated graphics on top; slowest in the "concept" block (4/min), fastest in the closing evidence and stakes (12-13/min). Never a still without a slow push.
- [ ] Faceless substitute for the host: a "reset" beat of 5-8 s every 20-40 s: a clean full-screen question card/diagram with the key sentence as 2-5 word kicker, or a calm hero shot with the voice only, with the glowing "?" on question lines. Keep the backdrop of the reset beat constant (our channel set).
- [ ] Palettes: dark science (near-black + one accent per meaning: orange = main object, red = alert/key data, green = depth/label numbers, yellow = highlighter), parchment/sepia for history, paper-white for documents. Max 2 text elements, labels 4-7% height, titles 12% height.
- [ ] Graphic per statement type from B6: 3D cutaway for structure, flat map with two points and a drawn line for distance, bar chart (white bars, the big one red, axis rescales on the jump), counter for repeat events, depth ruler at the right edge for dives, parchment strip chart for history, article/paper card with a moving highlight for every proof claim, source tag bottom-right (small caps), "REPRESENTATIONAL" tag top-right on AI/CG re-enactments.
- [ ] Highlight sync: the highlighter must start on the first word of the quoted line and end on the last (ours: word-level timing from TTS), the number label appears on the number word (within 0.3 s), the analogy graphic appears right at the analogy.
- [ ] Source cards: show the dissenting/limiting source with the same prominence as the supporting one; put the date inside a yellow ellipse; zoom into the exact figure from the paper.
- [ ] Transitions: hard cuts, 0.3-0.5 s dissolves for graphic-to-graphic, a warm light-leak/flash (0.4-0.6 s with whoosh) only at section pivots (about 1 per 2-3 min), blur pull-in after any long break; ties directly to a music silence gap.
- [ ] Lower-third dates/places as a small white-on-black chip at the upper-left third (not over the lower subtitle area), appearing 0.3 s after the word.
- [ ] First 30 s: claim in the first sentence at 0-8 s, a rising list of 4-5 consequences with new pictures every 3-5 s, a labelled data card with the key phrase highlighted at 20-30 s (headline-style card), question by 35-45 s, teaser of "this is relevant now" by about 60 s. (Reference took 65 s to the question; we aim for 35-45 s.)
- [ ] Stills from AI/CG that are re-enactments get the "REPRESENTATIONAL" label and a slow push + a shallow-depth close-up of the key object.

EXPLANATION
- [ ] Section arc: problem -> story (dated, named, one object) -> numbers ladder -> everyday consequence -> the deeper "why" -> the scary claim -> the honest limit (with the opposing source shown) -> tie back to the opening question and answer it in one clear line.
- [ ] Sentence length: mean 12-13 words (Hindi words), median 12, never over 25; 25% of sentences 8 words or fewer; speech about 150-165 words per minute (translation basis), pauses of 0.4-1 s at pivots.
- [ ] One analogy per 1.7-2 minutes, always an everyday or textbook object, and its own picture; give an Indian-scale comparison for every large distance/time (Delhi-Kanyakumari, cricket pitch, lakh/crore).
- [ ] Numbers: about 4-5 per minute, each as a ladder (small -> big -> shocking), converted to a human unit within 5-8 s; repeat the one key number 2-3 times with "listen carefully"; Indian units (lakh, crore).
- [ ] Rhetorical question about every 1.5 min (0.6/min), spoken as a pivot, each followed by a music silence and a visual reset.
- [ ] Always include one "common misconception" beat (the reference uses two North Poles) and one "so what for me" beat (phone compass, airports) before going deeper.
- [ ] Credibility: card with logo and source line for every scientific claim, the opposing view displayed, "research is still going on" if not settled. Keep our [F#] + 2 sources rule.
- [ ] End: answer the opening question explicitly, give the current/most recent number, finish on a question to the viewer, then a next-video card with a 5-6 s music-only brand sting.
