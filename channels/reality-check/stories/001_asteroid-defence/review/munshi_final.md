# Munshi final review - 001 asteroid-defence (Long, 18:44) - 2026-11-08
VERDICT: FIX (free metadata fixes + 1 voice line + on-screen labels). 0 BLOCKER. Video is private, so fix before it goes public.
Line numbers = audio/voiceover_timing.json "line" (video time in brackets).

## Measured
Duration 1124.14 s (18:44, within 18-20 min). Loudness -14.0 LUFS, LRA 4.2, true peak -1.6 dBFS. 1920x1080 30 fps, AAC 48 kHz. name_guard OK. final == preview (byte-identical). 17 frames (line midpoints) checked: no face, no film clip, no baked logo, no cut-off Hindi/Roman text; thumbnail readable, no face/logo. Counters finish on the spoken numbers (1,600; 80 million).

## Problems
| # | Sev | Where | Problem | Fix |
|---|---|---|---|---|
| 1 | MAJOR | line 26 (2:02.5-2:10.1) + on-screen "~80 million ped gire" | "about 8 crore trees in ~2,000 km2" - 80 million trees is a disputed figure (traces to a 1934 remark about 8,000 km2, popularised by a 1982 non-peer-reviewed paper; Boslough & Bruno 2025). 80M trees on 2,000 km2 is also not consistent. Surveyed area ~2,150 km2 (Wikipedia/Kulik surveys; NASA says ~2,000 km2). | Voice: "कोई गड्ढा नहीं बना। पर लगभग दो हज़ार वर्ग किलोमीटर का जंगल गिर गया।" Screen: "~2,000 km2 ka jungle gira" (drop 80 million). Re-TTS this one line (free Gemini TTS first; if only paid works = ASK). |
| 2 | MAJOR | line 146 (16:26-16:36) | Card says "27 Oct 2026: ESA ki jaari tasveer" but the picture is OUR illustration of two asteroids, not ESA's image. | Change label to "ESA ki 27 Oct 2026 ki tasveer ka hamara chitra (illustration)" or show the real ESA image link card. Free (re-render text). |
| 3 | MAJOR | lines 111-112 (11:49-12:04) | "Hubble ne ye sab hote dekha": cone/pinwheel are our animation, credit says NASA/Johns Hopkins APL, no "animation" label (shot_specs even lists NASA/ESA/STScI/J.-Y. Li). Looks like real Hubble data. | Add on-screen "Our animation, not the real Hubble image" and credit "Illustration based on NASA/ESA Hubble results"; keep ESA/STScI out of credit unless the real image is used. Same for line 61 (5:42) if it shows the same style. |
| 4 | MAJOR (metadata) | upload.json description | https://www.nasa.gov/mission/dart/ returns 404; https://www.esa.int/Hera returns 404. | NASA DART: https://science.nasa.gov/mission/dart/ ; ESA Hera: https://www.esa.int/Space_Safety/Hera (both 200). The other two are OK (nasa.gov/planetarydefense -> science.nasa.gov/planetary-defense/ ; cneos.jpl.nasa.gov 200). |
| 5 | MAJOR (metadata) | description | Line 71 (6:53) says "aaj ki taza sankhya aur tareekh vivaran me di gayi hai" but the description has no such number. | Add: "Date-stamped (8 Nov 2026): JPL SBDB lists about 11,650 near-Earth objects with H<22 (about 140 m+), roughly 47% of the ~25,000 estimated (CNEOS/JPL). About 95% of the 1 km+ class (868 objects with H<17.75) are known." Label it as an approximation. |
| 6 | MINOR | line 20 | ~1,600 injured: Russian health ministry figure 1,491 (Wikipedia), Popova 2013 ~1,600. | Say "डेढ़ हज़ार से ज़्यादा" if you re-do TTS anyway; else keep (rounded, hedged). |
| 7 | MINOR | line 46 (4:12) | Launch "23 Nov 2021" is US Pacific date; UTC is 24 Nov 06:21 (line 1 uses UTC). | "चौबीस नवंबर (यूटीसी)" or leave; low risk. |
| 8 | MINOR | line 94 (9:44) | ESA: visible to the naked eye from "parts of Europe, Africa and Asia", not "Eastern hemisphere". | "यूरोप, अफ़्रीका और एशिया के कुछ हिस्सों से नंगी आँख से दिखाई दे सकता है।" |
| 9 | MINOR | line 83 (8:21) | NASA wording: highest probability for an object "of this size or larger", not ">30 m". | "इस आकार के या उससे बड़े पिंड के लिए". |
| 10 | MINOR | line 114 (12:10) | "11,000-55,000 t" (Ferrari 2025) not verifiable by me; ALMA (Roth et al. 2023) gives 1.3-6.4 x10^7 kg = 13,000-64,000 t. | "कुछ अध्ययन दस हज़ार टन से भी ऊपर बताते हैं।" |
| 11 | MINOR | lines 133, 129 (14:14-14:50) | LLNL 2021 simulation numbers (V14) and 2023 exercise (V19): no primary source found by me. Lines are hedged ("simulation", "only computer simulation"). | Keep if dossier source (King et al., Acta Astronautica) is confirmed; else cut numbers. |
| 12 | MINOR | line 74 (7:12) and line 68 (6:35) | 59% by 2040 (V17) not verifiable; 1 km goal "2010" - Wikipedia says met "by 2011". | "लगभग साठ प्रतिशत"; "दो हज़ार दस-ग्यारह तक". |
| 13 | MINOR | line 96 (9:56-10:05) | Background is Goldstone/Green Bank Apophis radar (credit NSF/AUI/GBO needed), shown with only "NASA/JPL-Caltech"; baked radar caption cut at top edge. | Credit "NASA/JPL-Caltech and NSF/AUI/GBO" (screen + description); crop top. |
| 14 | MINOR | description | "AI illustrations (labelled on screen)": no AI stills seen in sampled frames, and animations are not labelled (see #2,#3). "sirf 7 minute badalna tha" is loose (7 min = calc. if only the spacecraft push). | "parts are our own animations/illustrations (labelled), not real footage"; "...7 minute ka hisaab tha". |

## Fact check (open gates)
Confirmed (2+ sources): V1 (Nature abstract/arXiv + NASA/Wikipedia: 33 +/-1 min, 73 s, 7 min calc), V2 (580 kg, ~22,000 km/h; launch 24 Nov UTC), V3 (Science Advances 2026 paper exists via Crossref; 11.7 um/s; 0.15 s from secondary page), V6 (Apophis 340/375 m ESA, 2.7% in 2004, 13 Apr 2029 ~31,600 km, 100 yrs NASA+ESA), V7 (generic "legal questions" line is safe), V9 (ESA page today: Hera first light 27 Oct 2026, rendezvous Nov 2026, target 151 m; no arrival yet), V10 (3.1% peak 18 Feb, 0.004% on 24 Feb NASA blog, Moon 3.8->4.3% NASA 5 Jun 2025, Moon ruled out 5 Mar 2026), V13 (NEO Surveyor NET Sept 2027, 90% in 10 yrs), V18 first half (Moreno et al. >6x10^6 kg). Changed: V12 trees (#1). Partly: V11 injured (#6). Not verifiable: V14, V17, V19, V18 second figure, V5 NASA/CNEOS primary (I used JPL SBDB count as proxy).
Update-at-publish: Hera lines 146-148 still correct as of 8 Nov 2026; recheck on publish day.

## Licence/credits
PD-NASA/Commons-PD items only in sampled frames; credits seen: NASA/JHUAPL, JPL-Caltech, Goddard SVS, NASA (ISS), US DOE. No faces, narration or baked logos in samples. Co-credit clips flagged in LICENSE_LOG (Univ. Wisconsin Milky Way, Univ. Arizona/CSS Catalina, SpaceX, ESA/STScI Hubble, UCLA/MPS/DLR/IDA Dawn) were not seen in sampled frames; builder to confirm none is in the final (shot_specs media list has none except #3). Synthetic-voice disclosure present; contains_synthetic_media true.

## User to verify / do in Studio
1. After fixes: confirm Altered/synthetic content = yes; Made for kids = no; description Sources URLs open.
2. Re-check ESA Hera page on publish day (arrival news).
3. Decide: re-TTS line 26 (free key) vs cut the line.
4. Pin first comment, add end screen (last ~20 s are empty by design), set public/schedule per RULES 8.
