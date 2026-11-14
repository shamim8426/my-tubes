# 002 Great Dying - sound event plan (v5, built from the reference sound study; techniques only)

Source of the rules: `channels/reality-check/research/study_ref_QsHQxRlBy6Y_sound.md` (measured on the reference documentary, 2026-11-14). Nothing here copies any audio from it. Written 2026-11-14, nothing built, nothing uploaded, no paid call.
Timing: `audio/voiceover_timing.json` (744 s, 104 lines). Scene facts: `long/footage_overrides.json` (graphic start times inside each line) and `long/shot_specs.json`. All event times below are ABSOLUTE video seconds (m:ss.s) = line start + offset, so after any TTS re-time re-run the offsets from the line starts.

## 0. What changes against the current mix (v4)
1. REMOVE every swipe-style whoosh/sweep and every "riser" that is a noise sweep. In v4 there were 25 soft whoosh/sub-hit SFX plus noise risers; the user called them swipe-like. Replace them with the five reference-like event types below. No event in this plan is a filtered-noise sweep.
2. Keep the music bed family, cue list and loudness chain of `sound_cues.md` (dark ambient, -15 LU under voice in the body, -12 at open/close, -19 in analytic parts). The reference shows the bed is not the problem; the effects were.
3. The reference "silence" is MUSIC OFF with the voice continuing (voice only, true digital quiet between words, no room tone). Our 8 OFF windows follow that: 3-7 s, always at a question / reversal / uncertainty / answer line, new cue enters as the window ends.

## 1. Event types (all synthesised or sampled to this recipe; levels are dB relative to the voice PEAK = 0 dB, bed = about -15)
| code | what it is | spectrum / shape | level vs voice peak | length | where |
|---|---|---|---|---|---|
| BOOM | big sub impact | sine 35-66 Hz (optional 2nd harmonic at -18 dB), 94-98% of energy below 100 Hz, attack 5-20 ms, exponential decay, no noise, optional 1.25x->1x pitch drop over 0.25 s, nothing above 400 Hz | -4 (range -9..+2) | tail 1.3-2 s | title card, flash cut into a new chapter, main reveal (about 4 in the film) |
| BOOM-soft | same sound, quieter and shorter | same, 45-60 Hz, decay 0.4-1.1 s | -8 | 0.4-1.2 s | chapter flashes, big numbers, stamps (about 12) |
| THUD | soft sub thud | 55-80 Hz sine, attack 10 ms, decay 0.25-0.4 s | -13 | 0.3 s | graphic lands on its value (bar, gauge, counter end, caption) |
| RISE | sub riser into a BOOM | sine 30->58 Hz glide + noise low-passed at 350 Hz (never above), +20 dB over 1.2-1.8 s, hard stop at the boom | peak -12 | 1.2-1.8 s | only inside a voice gap, directly before a flash/boom (4 in the film) |
| AIR | air tick (this is the "whoosh" replacement) | band 1.5-6 kHz noise, centre-panned, 5 ms attack, 120-200 ms decay, low-pass 8 kHz, 4 ms-room reverb, NO frequency movement | -20 (always under a boom) | 0.25 s | on flashes and arrow/line draws only (9 in the film) |
| TICK | UI tick | 1.3-2.2 kHz glass/pluck, 40-90 ms, no noise | -24 (key one -20) | 0.08 s | label / list item / timeline pin / pin drop |
| CLOCK | analog clock tick | 2 kHz band click 30 ms + body at 400 Hz, dry | -26 | 0.05 s | only where the graphic is a clock (lines 30, 31, 42) |
| AMB | scene ambience | low-passed (below 3 kHz) loops, 1-1.5 s fades, one at a time | -22..-34 | 3-10 s | only where the footage shows that thing |
| MUSIC-OFF | bed to silence (voice continues) | bed to under -60 dBFS in 0.3 s, back with a 1.5-2 s fade at the next cue | - | 3-7 s | 8 pivot lines |
| BED | bed ride | +4/+9 dB swell in voice gaps, -3/-6 dB dips on uncertainty lines | - | 2-4 s | see rows |

Order of cutting if the mix feels busy: drop TICK first (the 30 single-label ticks), then CLOCK, then AIR; never drop BOOM / RISE / MUSIC-OFF / AMB (AMB is the scene-matched part the user asked for).

## 2. Music: cues and OFF windows (all voice-continues)
| window | what is said | OFF from-to | enters after |
|---|---|---|---|
| W1 | L5 "how did this happen? how do we know?" | 0:27.4-0:32.9 | cue 2 Quietude (fade 2 s) |
| W2 | L34-35 "how do we know? the answer is in the stones" | 3:49.4-3:54.6 | cue 4 Dark Fog |
| W3 | L46 "where did so much carbon come from?" | 5:12.4-5:19.3 | cue 5 Impact Prelude under the RISE |
| W4 | L54 "the answer is not lava, it is gas" | 6:15.9-6:20.4 | gas cue returns with the BOOM at L55 (6:20.5) |
| W5 | L71 "how big the damage was is not settled" | 8:19.2-8:24.9 | bed returns at L72 (8:25) |
| W6 | L77 "a bit of good news" | 9:05.6-9:08.6 | cue 7 Inspired |
| W7 | L90 "last question: does it matter today?" | 10:32.2-10:36.0 | cue 8 Lightless Dawn |
| W8 | L99 "will the same disaster happen today?" | 11:37.7-11:44.6 | cue 9 Quietude reprise |
(Total OFF 8 windows, 44 s = 6% of the film; the reference has 7 places in 22.6 min, 3-8 s each.) Cue changes 2->3 (L18 flash), 5->6 (L59) are hidden under a boom tail, the others inside an OFF window; cue changes never happen mid-sentence on a plain bed.

## 3. Ambience beds (AMB), scene-matched and only where the picture shows it
sea surf (L1), dry wind (L2, L84 cold wind), forest wind (L12), underwater room tone + bubbles (L14-15), eruption rumble (L4), lava roar/gas (L48, L49, L52), gas hiss + bubbles (L45, L55), fire crackle (L57), warm sub swell (L60), warm-water bubbles (L63-65), soda fizz (L67). Levels -22..-34 dB vs voice peak, never two at once, none inside a MUSIC-OFF window except the voice. Sources: section 5 of the study.
Explosions: there is no explosion in the script; the only impact-like events are BOOM/BOOM-soft above (sub only, nothing above 400 Hz).

## 4. Totals (this plan)
- BOOM 4, BOOM-soft 12, RISE 4, THUD 25, AIR 9, TICK 61 (30 of them are single-label ticks, optional), CLOCK 11, AMB 15, MUSIC-OFF 8, BED rides 3.
- Without the optional ticks: about 5.4 events/minute (reference body: big hits 1.3 + soft thuds 1.9 + risers 0.6 + air ticks 1.2 + graphic ticks about 1.5 per minute).
- Never on a sentence start except the 2 section flashes and the 2 title/answer booms; never inside the first 0.2 s of a spoken number; at most one event per 0.6 s except tick ladders (squares, lists).

## 5. Line table (all 104 lines)
| line | start | what the line says (short) | scene | sound events: time, type, level vs voice peak (0 dB), why |
|---|---|---|---|---|
| 1 | 0:00.0 | लगभग पच्चीस करोड़ साल पहले की धरती। समंद... | meter | 0:00.0 **AMB** -31 dB: calm distant sea surf (low-passed 3 kHz) under the real sea clip 0-3.8 s, fade out by 5.5 s<br>0:00.3 **BOOM-soft** -8 dB: opening soft sub boom 45 Hz, tail 1.2 s (the reference file starts with a sub hit at 0.3 s); cue 1 "Disquiet" already running at -12 under the voice |
| 2 | 0:07.1 | पानी में ऑक्सीजन बहुत कम बची है। किनारे ... | meter | 0:10.1 **AMB** -33 dB: dry hot wind, thin, low-passed, over the dead-forest cut (second half of the line); fade out by 12.6 |
| 3 | 0:13.1 | समंदर के हर सौ तरह के जीवों में से, अस्स... | counter | 0:17.7 **THUD** -13 dB: caption "more than 80 gone forever" lands (counter finished at 4.7 s) |
| 4 | 0:19.4 | ये धरती के पूरे इतिहास की सबसे बड़ी तबाह... | timeline | 0:19.7 **AMB** -24 dB: eruption rumble swell 30-90 Hz + low-passed crackle below 1.2 kHz under the Poas eruption clip, peaks at 4.5 s, ends inside the boom tail<br>0:21.4 **TICK** -22 dB: timeline marker pin<br>0:24.4 **BOOM** -4 dB: "THE GREAT DYING" card (reference 0:25 headline-card boom: 66 Hz sine, 1.3 s decay, tail 1.7 s) |
| 5 | 0:27.6 | ये हुआ कैसे? और इतनी पुरानी बात हमें पता... | real | **0:27.4 MUSIC-OFF**: music OFF 27.4-32.9 (5.5 s) at the question "how did this happen?"; voice only, no SFX; cue 2 "Quietude" fades in from 32.9 (2 s) |
| 6 | 0:35.8 | पहले ये देखते हैं कि वो दुनिया थी कैसी। | flash real | 0:35.7 **AIR** -20 dB: 0.25 s air tick on the globe flash (no sweep), under the boom<br>0:35.8 **BOOM-soft** -8 dB: section start on the globe flash; cue 2 already present |
| 7 | 0:39.2 | उस वक़्त धरती का नक़्शा आज जैसा नहीं था।... | real | bed only (no event) |
| 8 | 0:46.6 | ज़मीन का एक ही बहुत बड़ा टुकड़ा था। नाम ... | real | bed only (no event) |
| 9 | 0:55.1 | आज का भारत भी उसी का हिस्सा था। अफ़्रीका... | real | bed only (no event) |
| 10 | 1:01.9 | इस दौर को पर्मियन कहते हैं। |  | 1:02.1 **TICK** -24 dB: label "The Permian period" |
| 11 | 1:04.8 | तब डायनासोर नहीं थे। चिड़ियाँ नहीं थीं। ... | list | 1:05.1 **TICK** -24 dB: list item 1 (no dinosaurs / no birds / no flowers)<br>1:07.3 **TICK** -24 dB: list item 2 (no dinosaurs / no birds / no flowers)<br>1:08.7 **TICK** -24 dB: list item 3 (no dinosaurs / no birds / no flowers) |
| 12 | 1:10.8 | पर ज़िंदगी भरपूर थी। ज़मीन पर घने जंगल थ... | real | 1:11.1 **AMB** -33 dB: wind in dense leaves, very soft (dense forest cut), 1 s fades |
| 13 | 1:15.4 | उनमें ऐसे शिकारी घूमते थे, जिनके दाँत तल... |  | 1:23.0 **TICK** -24 dB: label "Some were as big as a bear" |
| 14 | 1:25.2 | और समंदर रीफ़ से भरे थे। सीपियाँ, मछलिया... | real | 1:25.2 **AMB** -34 dB: underwater room tone with sparse far bubbles under the reef cut (lines 14-15, then fade) |
| 15 | 1:31.8 | ट्राइलोबाइट, यानी कवच वाले छोटे जीव, जो ... | real | bed only (no event) |
| 16 | 1:38.4 | ये पच्चीस करोड़ साल से भी ज़्यादा वक़्त ... | tline | 1:41.8 **TICK** -22 dB: timeline mark ("250 million years") |
| 17 | 1:43.7 | यानी सब कुछ ठीक चल रहा था। फिर, सब बदल ग... | real | 1:47.9 **RISE** -12 dB: sub riser 30->58 Hz + noise below 350 Hz, 1.8 s; starts at "then everything changed" and ends in the boom of line 18; sits inside the 1.4 s voice gap (gap swell +9 dB) |
| 18 | 1:49.7 | लगभग पच्चीस करोड़ बीस लाख साल पहले, जीव ... | flash | 1:49.6 **AIR** -20 dB: 0.25 s air tick on the flash, under the boom<br>1:49.8 **BOOM** -4 dB: flash cut + "About 252 million years ago": sub boom 40 Hz, tail 2 s; CUE CHANGE 2->3 "Gathering Darkness" hidden under the tail |
| 19 | 1:56.4 | जब किसी जीव की पूरी नस्ल खत्म हो जाए, एक... |  | 1:58.2 **TICK** -24 dB: label "Extinction: a whole kind is gone" |
| 20 | 2:03.2 | और जब बहुत सारी नस्लें एक साथ खत्म हों, ... |  | bed only (no event) |
| 21 | 2:08.5 | धरती पर ऐसा पाँच बार बड़े पैमाने पर हुआ ... | squares | 2:08.8 **TICK** -26 dB: five squares appear (rising pitch 1.4->2.0 kHz), square 1<br>2:09.2 **TICK** -26 dB: five squares appear (rising pitch 1.4->2.0 kHz), square 2<br>2:09.5 **TICK** -26 dB: five squares appear (rising pitch 1.4->2.0 kHz), square 3<br>2:09.9 **TICK** -26 dB: five squares appear (rising pitch 1.4->2.0 kHz), square 4<br>2:10.2 **TICK** -26 dB: five squares appear (rising pitch 1.4->2.0 kHz), square 5<br>2:12.1 **BOOM-soft** -8 dB: "This one was the biggest" (stamp-like; reference EXTINCT stamp = boom with 1.1 s tail) |
| 22 | 2:15.0 | अब नंबर देखिए। आपने शायद सुना होगा, कि छ... | big | 2:18.0 **BOOM-soft** -8 dB: the "96%" count finishes; music dips -3 dB for the 1.0 s before |
| 23 | 2:20.6 | ये नंबर थोड़ा समझना ज़रूरी है। छियानवे प... | bars | bed only (no event) |
| 24 | 2:30.9 | नया हिसाब कहता है, इक्यासी परसेंट। तो सह... | bars | 2:33.1 **THUD** -13 dB: second bar (81%) appears |
| 25 | 2:39.7 | इसे ऐसे समझिए। मान लीजिए समंदर में सौ तर... | counter | 2:44.7 **THUD** -13 dB: dot field finishes: only 4 to 19 left |
| 26 | 2:48.2 | ज़मीन पर भी हाल बुरा था। रीढ़ की हड्डी व... | counter | 2:52.7 **THUD** -13 dB: 70% of land animals gone |
| 27 | 2:56.2 | ट्राइलोबाइट, जो इतने लंबे वक़्त से थे, प... | real | bed only (no event) |
| 28 | 3:01.8 | पुरानी रीफ़ बनाने वाले मूँगे, यानी कोरल,... | real | bed only (no event) |
| 29 | 3:06.1 | और कीड़े-मकोड़े, जो आम तौर पर हर मुसीबत ... | real | 3:13.2 **THUD** -13 dB: "never at such a scale before" |
| 30 | 3:16.4 | अब सवाल ये है कि ये सब कितनी जल्दी हुआ? | clock | 3:16.9 **CLOCK** -26 dB: clock element: slow dry analog tick (1 per second, 2 kHz, 30 ms)<br>3:17.9 **CLOCK** -26 dB: clock element: slow dry analog tick (1 per second, 2 kHz, 30 ms)<br>3:18.9 **CLOCK** -26 dB: clock element: slow dry analog tick (1 per second, 2 kHz, 30 ms) |
| 31 | 3:20.6 | जवाब है: समंदर में, लगभग साठ हज़ार साल म... | clock | 3:21.0 **CLOCK** -26 dB: clock tick<br>3:22.0 **CLOCK** -26 dB: clock tick<br>3:23.1 **THUD** -13 dB: "sixty thousand years": clock stops, 0.3 s of nothing, then thud |
| 32 | 3:26.9 | साठ हज़ार साल सुनने में बहुत लगता है। पर... | real | bed only (no event) |
| 33 | 3:34.5 | इसे ऐसे समझिए। धरती पर जीवन की पूरी कहान... | tline | 3:41.5 **TICK** -20 dB: single sharp click for the 1.5-second sliver of the 24-hour film; bed dips -4 dB for 0.7 s before it |
| 34 | 3:48.5 | अब आप पूछेंगे, पच्चीस करोड़ साल पुरानी ब... | flash | 3:48.4 **BOOM-soft** -8 dB: flash cut on "how do we know?"<br>3:48.4 **AIR** -20 dB: 0.25 s air tick under the boom<br>**3:49.4 MUSIC-OFF**: music OFF 229.4-234.6 (5.2 s): question + "the answer is in the stones"; cue 4 "Dark Fog" fades in from 234.6 |
| 35 | 3:52.9 | जवाब पत्थरों में है। |  | bed only (no event) |
| 36 | 3:55.2 | चीन में एक जगह है, मेइशान। वहाँ पहाड़ी क... |  | 4:00.4 **TICK** -24 dB: label "Meishan, China" |
| 37 | 4:05.7 | नीचे की परत पुरानी, ऊपर की नई। हर परत, उ... | layers | 4:06.0 **THUD** -13 dB: rock layers stack in |
| 38 | 4:12.9 | नीचे की परतों में ढेर सारे जीवों के फ़ॉस... | real | bed only (no event) |
| 39 | 4:21.2 | फिर कुछ पतली परतें आती हैं। और उनके ऊपर,... | layers | 4:24.2 **TICK** -24 dB: label "many fossils below, almost none above" |
| 40 | 4:27.1 | अब तारीख़ कैसे पता चली? इन परतों के बीच ... | layers | 4:30.1 **THUD** -13 dB: volcanic-ash layer drawn between the layers |
| 41 | 4:33.1 | उस राख में बहुत छोटे क्रिस्टल होते हैं। ... | arrow | 4:40.0 **TICK** -24 dB: label "uranium slowly turns into lead"<br>4:40.7 **AIR** -20 dB: arrow draw uranium->lead, 0.3 s soft air tick (not a sweep)<br>4:41.7 **TICK** -26 dB: label "lead" |
| 42 | 4:43.6 | ये एक घड़ी की तरह काम करता है। कितना यूर... | clock | 4:43.9 **CLOCK** -26 dB: clock element "like a clock": analog tick, 1 per second<br>4:44.9 **CLOCK** -26 dB: clock element "like a clock": analog tick, 1 per second<br>4:45.9 **CLOCK** -26 dB: clock element "like a clock": analog tick, 1 per second<br>4:46.9 **CLOCK** -26 dB: clock element "like a clock": analog tick, 1 per second<br>4:47.9 **CLOCK** -26 dB: clock element "like a clock": analog tick, 1 per second<br>4:48.9 **CLOCK** -26 dB: clock element "like a clock": analog tick, 1 per second |
| 43 | 4:51.2 | इसी घड़ी ने बताया: तबाही से ठीक पहले की ... | layers | 4:54.7 **THUD** -13 dB: "only about 60,000 years apart" |
| 44 | 4:59.9 | दूसरा सुराग़ कार्बन में मिला। उसी वक़्त ... | curve | 5:03.2 **THUD** -13 dB: carbon curve jumps |
| 45 | 5:06.9 | इसका सीधा मतलब: हवा और समंदर में, कहीं स... | bubbles | 5:06.9 **AMB** -32 dB: gentle gas bubbles under the "new carbon" graphic, to 312.3<br>5:07.9 **TICK** -24 dB: label "A lot of new carbon entered air and sea" |
| 46 | 5:12.7 | तो इतना कार्बन आया कहाँ से? इसका जवाब ची... | real | **5:12.4 MUSIC-OFF**: music OFF 312.4-319.3 (6.9 s): "where did so much carbon come from? ... Siberia"<br>5:18.6 **RISE** -12 dB: sub riser 1.8 s (318.6-320.4) out of the off window into the Siberia boom; cue 5 "Impact Prelude" enters under it |
| 47 | 5:20.4 | साइबेरिया में, जमे हुए लावा की परतें दूर... | real | 5:20.4 **BOOM** -4 dB: "in Siberia" reveal: sub boom 38 Hz, tail 2 s (reference 6:18.5: 1.0 s riser then a -13 dB hit, bed returns) |
| 48 | 5:28.1 | ये कोई एक पहाड़ वाला वॉल्केनो नहीं था। ज... | real | 5:28.3 **AMB** -26 dB: lava fountain at night: low roar/gas hiss band-limited below 1.5 kHz, 1 s fade in, runs to 335.5<br>5:30.6 **THUD** -13 dB: "long cracks opened": crack thud |
| 49 | 5:35.5 | कितना लावा? अंदाज़ा है बीस से पचास लाख घ... |  | 5:35.5 **AMB** -28 dB: viscous low lava-river rumble + very soft crackle, to 341.1<br>5:35.8 **TICK** -24 dB: label "How much lava?"<br>5:37.0 **THUD** -13 dB: "twenty to fifty lakh cubic km" |
| 50 | 5:41.1 | इतना, कि पूरे भारत पर बिछा दें, तो लगभग ... | india | 5:41.6 **AIR** -20 dB: India map covered by a lava layer: soft air tick on the draw<br>5:46.0 **THUD** -13 dB: "one kilometre thick layer" |
| 51 | 5:50.5 | और जब उसी राख वाली घड़ी से इस लावा की उम... | bars | 5:55.1 **TICK** -24 dB: label "The same time" |
| 52 | 5:57.3 | ये सब एक झटके में नहीं हुआ। लावा कई लाख ... | tline | 5:57.3 **AMB** -32 dB: lava fountain (day) roar, thin, to 366.4<br>5:59.3 **TICK** -22 dB: timeline mark |
| 53 | 6:07.7 | पर यहाँ एक उलझन है। साइबेरिया तो दुनिया ... | flash real | 6:07.6 **BOOM-soft** -8 dB: flash cut on the "puzzle" question (the question line itself keeps the bed)<br>6:07.6 **AIR** -20 dB: 0.25 s air tick under the boom<br>**6:15.9 MUSIC-OFF**: music OFF 375.9-380.4 (4.5 s): "the answer is not lava, the answer is gas" |
| 54 | 6:16.3 | जवाब लावा नहीं है। जवाब गैस है। | real | bed only (no event) |
| 55 | 6:20.5 | लावा के साथ बहुत सारी कार्बन डाइऑक्साइड ... | bubbles | 6:20.5 **BOOM** -4 dB: "carbon dioxide came out": the answer hit as the bed returns<br>6:20.5 **AMB** -30 dB: gas hiss + rising bubbles under the bubbles graphic, to 384.1, thin to 392 |
| 56 | 6:24.6 | और एक बात ने इसे और बिगाड़ा। साइबेरिया क... |  | 6:28.4 **TICK** -24 dB: label "thick layers of coal and salt" |
| 57 | 6:32.6 | गरम लावा ज़मीन के अंदर ही अंदर इन परतों ... | section | 6:33.0 **AMB** -30 dB: fire crackle (cooking coal), low-passed, 393.0-399.8 |
| 58 | 6:40.2 | कुछ साइंटिस्ट्स को वहाँ जले हुए कोयले के... |  | 6:40.9 **TICK** -24 dB: label "burnt coal pieces found" |
| 59 | 6:46.9 | अब चार बड़ी चीज़ें हुईं। |  | 6:47.0 **BOOM-soft** -8 dB: "four big things happened"; CUE CHANGE 5->6 "Giant Wyrm" under the boom |
| 60 | 6:49.3 | पहली: गर्मी। कार्बन डाइऑक्साइड धरती की ग... | blanket | 6:49.5 **TICK** -24 dB: label "1. Heat"<br>6:49.8 **AMB** -22 dB: warm low sub swell 5 s under the blanket graphic (sub drone rises 4 dB, no noise) |
| 61 | 6:57.3 | गरम इलाक़ों में समंदर की ऊपरी सतह का टेम... | gauge | 6:57.7 **TICK** -24 dB: label "Warm seas 8-10 degrees hotter"<br>7:02.3 **THUD** -13 dB: gauge reaches +8-10 C |
| 62 | 7:04.8 | आठ-दस डिग्री कम लगता है? हमारे शरीर का ट... |  | 7:08.8 **THUD** -13 dB: "Earth had a high fever" |
| 63 | 7:14.4 | दूसरी: ऑक्सीजन। गरम पानी में ऑक्सीजन कम ... | bubbles | 7:14.8 **TICK** -24 dB: label "2. Oxygen"<br>7:14.9 **AMB** -30 dB: bubbles escaping from warm water, 434.9-439.0, thinning through line 64 |
| 64 | 7:19.5 | और गर्मी में जीवों को ऑक्सीजन ज़्यादा चा... | bars | bed only (no event) |
| 65 | 7:27.6 | एक स्टडी का हिसाब है, कि समंदर की लगभग अ... | gauge | 7:32.1 **THUD** -13 dB: gauge shows about 80% oxygen lost; bubbles are gone by now |
| 66 | 7:34.1 | सोचिए, आपके कमरे की हवा से ऑक्सीजन के पा... | squares | 7:34.4 **TICK** -26 dB: room of five squares: square 1 appears<br>7:34.6 **TICK** -26 dB: room of five squares: square 2 appears<br>7:34.8 **TICK** -26 dB: room of five squares: square 3 appears<br>7:34.9 **TICK** -26 dB: room of five squares: square 4 appears<br>7:35.2 **TICK** -26 dB: room of five squares: square 5 appears<br>7:37.1 **TICK** -26 dB: four squares removed (falling pitch 1.8->1.3 kHz), 1<br>7:37.4 **TICK** -26 dB: four squares removed (falling pitch 1.8->1.3 kHz), 2<br>7:37.7 **TICK** -26 dB: four squares removed (falling pitch 1.8->1.3 kHz), 3<br>7:37.9 **TICK** -26 dB: four squares removed (falling pitch 1.8->1.3 kHz), 4 |
| 67 | 7:42.3 | तीसरी: खट्टा पानी। कार्बन डाइऑक्साइड पान... | bubbles | 7:42.6 **TICK** -24 dB: label "3. Sour water"<br>7:46.3 **TICK** -24 dB: label "CO2 dissolves"<br>7:49.6 **AMB** -22 dB: soda fizz, 1.4 s, band 2-7 kHz, soft attack (only on the word "soda") |
| 68 | 7:51.4 | ऐसे पानी में सीपियों और कोरल के खोल ठीक ... | real | bed only (no event) |
| 69 | 7:56.5 | और चौथी चीज़ ज़मीन पर हुई। धरती के ऊपर ओ... |  | 7:56.9 **TICK** -24 dB: label "4. The ozone layer" |
| 70 | 8:05.7 | सबूत इशारा करते हैं कि वॉल्केनो की गैसों... |  | 8:10.7 **TICK** -24 dB: label "volcano gases may have weakened it"<br>8:14.7 **TICK** -24 dB: label "pollen found" |
| 71 | 8:19.5 | ये नुक़सान कितना बड़ा था, इस पर अभी पक्क... |  | **8:19.2 MUSIC-OFF**: music OFF 499.2-504.9 (5.7 s): "how big the damage was is not settled" (uncertainty line) |
| 72 | 8:25.0 | तो अब पूरी तस्वीर देखिए। क़ातिल कोई एक च... |  | 8:25.2 **BOOM-soft** -8 dB: "the killer was not one thing": bed returns with the hit |
| 73 | 8:29.9 | गर्मी, कम ऑक्सीजन, खट्टा पानी, और तेज़ ध... | list | 8:30.2 **TICK** -24 dB: list item 1: Heat<br>8:32.2 **TICK** -24 dB: list item 2: Low oxygen<br>8:34.3 **TICK** -24 dB: list item 3: Sour water<br>8:36.3 **TICK** -20 dB: list item 4: Strong sunlight |
| 74 | 8:39.4 | जो जीव एक चोट से बचा, वो दूसरी से मारा ग... | arrow | 8:40.9 **AIR** -20 dB: arrow draw "survived heat -> killed by low oxygen", 0.3 s<br>8:42.0 **TICK** -24 dB: label "killed by low oxygen"<br>8:44.4 **THUD** -13 dB: "one hit, then another" |
| 75 | 8:47.2 | वैसे, सारे सवाल हल नहीं हुए हैं। जैसे, ज... |  | 8:51.0 BED: bed dips -6 dB for 3 s on "still debated" (no OFF: one OFF window per uncertainty block) |
| 76 | 8:56.1 | पर इस बात पर ज़्यादातर साइंटिस्ट एक राय ... |  | 9:03.3 **RISE** -12 dB: sub riser 1.2 s (543.3-544.5) inside the gap before the flash of line 77 |
| 77 | 9:04.6 | अब एक अच्छी बात। सब कुछ खत्म नहीं हुआ। | flash | 9:04.5 **AIR** -20 dB: 0.25 s air tick under the boom<br>9:04.6 **BOOM-soft** -8 dB: flash cut + "a bit of good news"<br>**9:05.6 MUSIC-OFF**: music OFF 545.6-548.6 (3 s); cue 7 "Inspired" fades in at 548.6 |
| 78 | 9:08.9 | ज़मीन पर एक जानवर बचा, जिसका नाम है लिस्... | real | 9:08.9 **THUD** -13 dB: "Lystrosaurus": bed returns |
| 79 | 9:14.1 | सुअर जितना बड़ा। छोटी टाँगें, चोंच जैसा ... |  | 9:14.6 **TICK** -24 dB: label "Pig-sized" |
| 80 | 9:23.4 | पर तबाही के बाद की चट्टानों में, ज़मीन क... |  | bed only (no event) |
| 81 | 9:30.6 | इसके फ़ॉसिल दक्षिण अफ़्रीका में मिले, अं... | real | 9:31.7 **TICK** -26 dB: globe pin drop 1 (South Africa / Antarctica / India)<br>9:33.5 **TICK** -26 dB: globe pin drop 2 (South Africa / Antarctica / India)<br>9:35.0 **TICK** -26 dB: globe pin drop 3 (South Africa / Antarctica / India) |
| 82 | 9:36.2 | ये बचा कैसे? पक्का किसी को नहीं पता। |  | bed only (no event) |
| 83 | 9:40.4 | एक अंदाज़ा ये है कि ये ज़मीन में बिल खोद... |  | 9:40.8 **TICK** -24 dB: label "one guess: burrows" |
| 84 | 9:45.2 | अंटार्कटिका वाले लिस्ट्रोसॉरस के दाँतों ... |  | 9:48.2 **TICK** -24 dB: label "teeth hint at a long sleep"<br>9:53.5 **AMB** -34 dB: soft cold wind, 593.5-598.2 on "like bears in winter" |
| 85 | 9:58.7 | समंदर में भी कुछ जीव बचे। पर दुनिया को व... |  | bed only (no event) |
| 86 | 10:05.0 | कितना? लगभग अस्सी से नब्बे लाख साल। | tline | 10:08.2 **TICK** -22 dB: timeline mark "80-90 lakh years" |
| 87 | 10:09.3 | क्योंकि तबाही के बाद भी, लाखों साल तक गर... | gauge | bed only (no event) |
| 88 | 10:14.2 | फिर धीरे-धीरे, इसी खाली दुनिया में नए जी... |  | 10:14.6 **TICK** -24 dB: label "dinosaurs about 20 million years later"<br>10:19.6 **THUD** -13 dB: "dinosaurs came out" |
| 89 | 10:22.2 | और बचे हुए जीवों की एक दूसरी शाखा से, बह... |  | 10:22.6 **TICK** -24 dB: label "much later: mammals"<br>10:29.0 **RISE** -14 dB: sub riser 1.2 s (629.0-631.2) into the flash of line 90 |
| 90 | 10:31.3 | अब आख़िरी सवाल। क्या इसका आज से कोई लेना... | flash | 10:31.2 **AIR** -20 dB: 0.25 s air tick under the boom<br>10:31.3 **BOOM-soft** -8 dB: flash cut + "last question"; then music OFF<br>**10:32.3 MUSIC-OFF**: music OFF 632.2-636.0 (3.8 s); cue 8 "Lightless Dawn" fades in at 636.0 |
| 91 | 10:36.2 | यहाँ हम सिर्फ़ वही कहेंगे, जो स्टडीज़ कह... |  | bed only (no event) |
| 92 | 10:41.3 | पहली बात। आज भी हवा में कार्बन डाइऑक्साइ... | curve | 10:41.7 **TICK** -24 dB: label "CO2 is rising again"<br>10:47.8 **THUD** -13 dB: curve peaks at "our burnt coal, oil and gas" |
| 93 | 10:51.8 | दूसरी बात, रफ़्तार। स्टडीज़ का अंदाज़ा ह... | bars | bed only (no event) |
| 94 | 11:01.0 | कितना ज़्यादा, इस पर नंबर अलग-अलग हैं। ए... | bars | 11:01.3 **TICK** -24 dB: label "How much faster?"<br>11:05.0 **THUD** -13 dB: bar "14 times" fills<br>11:08.0 **TICK** -24 dB: bar "2 times" appears |
| 95 | 11:11.3 | तीसरी बात, जो उतनी ही ज़रूरी है। कुल मिल... |  | 11:11.7 **TICK** -24 dB: label "Third" |
| 96 | 11:17.8 | तब गैस हज़ारों साल तक निकलती रही। और गरम... | gauge | 11:22.5 **THUD** -13 dB: gauge: seas 8-10 C hotter |
| 97 | 11:25.3 | आज तक पूरी धरती का औसत लगभग एक से डेढ़ ड... | gauge | 11:27.8 **TICK** -26 dB: gauge: today +1-1.5 C (much smaller, so softer than line 96, no thud) |
| 98 | 11:30.6 | और इसी स्टडी के साइंटिस्ट कहते हैं, कि ह... | bars | 11:35.6 **THUD** -13 dB: label "not enough coal and oil"; bed dips -3 dB for 2 s |
| 99 | 11:38.0 | तो क्या आज वैसी ही तबाही होने वाली है? ज... |  | **11:37.7 MUSIC-OFF**: music OFF 697.7-704.6 (6.9 s): "will the same disaster happen today?"; cue 9 "Quietude (reprise)" fades in at 704.6 |
| 100 | 11:45.0 | पर वो एक बात ज़रूर कहती हैं। समंदर का गर... | gauge | 11:45.2 **THUD** -13 dB: two gauges (heat + oxygen) start together<br>11:50.6 **BOOM-soft** -8 dB: "the way (pattern) is the same": second key line of the stakes block |
| 101 | 11:53.2 | एक हिसाब के मुताबिक़, अगर हम गैस छोड़ना ... | bars | 11:53.7 **TICK** -24 dB: bars: risk if we keep releasing<br>11:56.2 **THUD** -13 dB: "if we cut quickly: 70% lower" bar drops |
| 102 | 12:04.5 | उस वक़्त के जीवों के पास कोई रास्ता नहीं... |  | 12:04.5 BED: bed rises +4 dB across the 4.5 s line (reference: closing block back to -12 LU) |
| 103 | 12:09.1 | पच्चीस करोड़ साल पहले, धरती की ज़्यादातर... |  | 12:09.1 BED: bed stays at -12 LU under the voice; no SFX |
| 104 | 12:16.3 | जो थोड़ी सी बची, उसी से आज की पूरी दुनिय... |  | 12:23.8 **BOOM-soft** -8 dB: end sting: soft boom + drone swell when the voice stops (743.8), 14 s fade; music-only tail 5-6 s |