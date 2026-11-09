# Munshi review - 001 asteroid-defence - script v2 - R1 (FACT CHECK + length/timing)
Date 2026-11-07. VERDICT: **FIX** (0 BLOCKER, 3 MAJOR, several MINOR; all fixes free, no paid call). Line refs: "L##" = voiceover line number, "file:##" = line in script/script.md.

## Measured (python, not trusted from the header)
- voiceover_clean.txt: 2406 words (headings excluded), 160 lines. No digits, no Latin, no [ ] tags (checked by regex). Nuqta letters present throughout. At 130 wpm = 18:30 (+6 s chapter pauses = 18:37). Inside 2,350-2,600 and inside the 18-20 min band.
- Sentences: 287, mean 8.4 words, max 17. 8 sentences are 16-17 words (L15, L35, L70, L74, L92, L93, L130, L132; all carry spelled numbers, MINOR). 130 of 287 (45%) are UNDER 8 words (staccato; MINOR rhythm note for the TTS).
- THE ANSWER (L104, "यानी यान का धक्का, और ऊपर से मलबे का धक्का") starts after 1450 of 2406 words = 60.3% (about 11:09 raw, 11:14 in script) -> inside 51-86%. Verified.
- Script header claims (2406 words, 160 shots, longest 12 s, 13 cuts in first 60 s) match my count. "285 sentences" is actually 287 (trivial).
- name_guard.py: OK on script.md, voiceover_clean.txt and all 3 shorts/script.md.
- Arithmetic checked: 6.1449 km/s = 22,121 km/h (OK "लगभग 22,000"); 11h55 - 32 = 11h23 (OK, 33 -> 11h22 noted); 1,920 s / 73 s = 26.3 (OK "25 गुना से भी ज़्यादा"); 33 - 7 = 26; 23 Nov 2021 -> 26 Sep 2022 = 10 months; 6x10^6 kg = 6,000 t; (1.1-5.5)x10^7 kg = 11,000-55,000 t; 5 kt = 5,000 t; 66 Myr = "छह करोड़ साठ लाख"; 58.7% = "उनसठ"; beta 2.2-4.9 > 2 so "मलबे का धक्का यान से बड़ा" is correct for the whole range. No impact year anywhere in the Long; no film name; no politics.

## Fact check vs dossier (fact lines vs [F#])
All 160 lines tagged or marked "framing". Numbers and strength of "कहना" match F1-F26 (Chelyabinsk ~1,600 / ~500 kt / glass; Tunguska ranges; Chicxulub consensus + volcano minority; Hera "plan" only; Apophis 340/375 m, 32,000 km, 100 yr, 2.7% (2004); YR4 3 -> 0.004%, Moon 1.7/3.8/4.3 -> out 5 Mar 2026; beta 3.6 only "if densities equal", range 2.2-4.9; ejecta >1,000 t / >6,000 t / 11,000-55,000 t; nuclear = simulation, untested). Fear guard OK: DANGER L20/L31 -> STATUS L37; L73 -> L75; L82 -> L92/L96; L91 -> L92. Sections 8/9: V1 "verified" is honest (arXiv abstract, Nature page not opened); V3 "partly (secondary)" honest; V5 honestly "not closed". I could not open primary sources myself (no web fetch tool): checking is against the dossier only, so every OPEN V (V2, V4, V6, V7, V10-V14, V17-V19) remains a gate before TTS/publish.

## Problems
1. **MAJOR** L136 (file:619) "अंतरराष्ट्रीय संधियाँ" (plural) - dossier F22 gives one treaty (Outer Space Treaty), UNOOSA text not opened (V7 still OPEN). Fix (free): use the V7 fallback "क़ानूनी सवाल भी हैं" or cut the line until the treaty text is checked.
2. **MAJOR** L103 (file:480) rocket-exhaust comparison and L101 (file:472) "वो पत्थरों के ढीले ढेर जैसा था" stated flat. L103 is an explanatory analogy not in dossier and NOT listed in section 9 (only L66 is flagged NF); L101/L150 state "rubble pile" as fact while dossier F21 says only "rubble-pile-like" and L117 says the interior is unknown. Fix: add L103 to section 9 as NF; soften L101 to "ढीले पत्थरों के ढेर जैसा माना जाता है" (and L150 "एक ऐसे पिंड पर चला है, जो ढीले पत्थरों का ढेर लगता है").
3. **MAJOR** Description Sources block (file:815-824) is missing rows promised in the header at file:795 and needed by V18/V3: Moreno et al. 2023 (PSJ), Ferrari et al. 2025, Makadia/Eggl et al. (Sci. Adv. 2026 doi), Politecnico di Milano 2023 exercise study (V19), LICIACube credit. RULES 16 wants the Sources list complete. Fix: add the rows (primary links to be filled).
4. MINOR L29 (file:171) "पूरा जंगल बिछ जाता है" overstates F4 (about 80 million trees over ~2,000 km2); say "जंगल का बड़ा हिस्सा".
5. MINOR L88 (file:417) "फ़िल्मों में अक्सर वैज्ञानिक एक दिन पक्का ऐलान कर देते हैं" is a generalisation about films; dossier F25 only supports the real-process side. Soften to "फ़िल्मों में कभी-कभी".
6. MINOR L72-73 (file:351-355) "इनमें से" is ambiguous after the 25,000 line; say "एक सौ चालीस मीटर से बड़े पिंडों में से". The US Congress goal is a fact, not politics (OK).
7. MINOR L94 (file:441) naked-eye line and L90/L93 numbers still V6 OPEN; if not closed before TTS, cut L94 (as the script already says).
8. MINOR L146-L148 (file:664-672) Hera: arrival is due in November 2026, so this block will probably be out of date at publish; TTS for these 3 lines will have to be re-made (small cost). Plan them as a swappable block now.
9. MINOR Shots: every line has CUT, graphic types are all from the section-2 list, red अनजान label present on all UNKNOWN lines, 13 cuts in first 60 s. But 40 lines run longer than 8 s with a single CUT, 4 of them 12 s (L88, L108, L125, L151) and L62, L93, L128, L135, L139, L150, L156 at 10-11 s. Fix: add a second cue (zoom / sub-card / hold-change) inside those lines so the visual changes every <=8 s.
10. MINOR Source labels [n] are used (file lines for L15-L145; [17] Moreno and [18] Ferrari only inside L114) but section 11 has no numbered Sources list, so the numbers are not defined anywhere. Fix: number the Sources block in the same order or drop numbers.
11. MINOR Short 1 note (short_01.../script.md:9) typo "mlbe" (मलबा). Short 2 L3 (short_02.../script.md:5) speaks "अपोफ़िस दो हज़ार उनतीस में टकराएगा" (the myth) while the note beside it says "no year of impact": drop the year in speech ("अपोफ़िस धरती से टकराएगा?"), the date can stay on the card as flyby.

## Shorts (v2 consistency)
Facts in the 3 Shorts match v2 (22,000 km/h, 7 vs 33, 73 s, 33 +/-1, 140 m+ ~25,000 and 40-44%, 100-year NASA line). No mention of ejecta, beta, Hubble, unknown mass or Hera in any Short; Short 1 ends on the question, Short 3 loops, Short 2 withholds the answer to Q3. Lengths 62-63 words (~34-35 s). Short 3 L4 still needs the dated V5 number before build (already noted).

## Agla kadam
Builder/Kalam: do items 1-3 (MAJOR) plus the MINOR text edits, re-run the word count (stay 2,350-2,600, answer at 51-86%), then R2 (MINOR-only after that goes to carry_over). Close the OPEN V gates (V7, V10-V14, V17-V19, V6) in a browser before TTS; V5 and V9 stay UPDATE-AT-PUBLISH. No STOP condition hit (balance / copyright / channel ID unaffected).
