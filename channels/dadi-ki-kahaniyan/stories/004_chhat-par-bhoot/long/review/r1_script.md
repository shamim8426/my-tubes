# Munshi R1 — script / plan stage — 004_chhat-par-bhoot (Long 03 + Short A)

Date: 2026-10-19 · Profile: shared/RULES.md section 15 · Verdict: **FIX** (MINOR only, all free) · STOP condition: none

## Verified
- script.md (approved v1) vs long/lines.json: 42 entries = 40 spoken + 2 music-only beats (crickets 0.3 s, footsteps 1.5 s). All 40 spoken lines match the script word for word with the right speaker (scripted diff). Script line 19 = footsteps beat. 386 words.
- make_short.build_voice logic read: pause entry at index 0 -> 0.3 s, Golu gets gap 0.6 -> first word ~0.90 s (<= 1.0 ok, thin margin). Line 2 af atempo=1.25 x narrator 0.8 = net 1.0. pause_before 1.0 on line 27 adds to the 0.6 gap. Footsteps beat costs 0.6 + 1.5 (+0.6 to Golu).
- Re-measured rates myself from Long 02 per-line wavs (energy trim as make_short.trim, normalised to speed 1.0): narrator 0.405, dadi 0.483, golu 0.354, gupta 0.360, mitthu 0.562, pandey 0.491, sharma 0.391 s/word. PLAN rates (raw untrimmed / tempo, minus ~0.5 s per line) are the same data, method sound. Only slip: PLAN pandey 0.559 is at speed 1.0, Long 03 runs pandey at 0.95 (+~1 s total, Note).
- Long estimate (make_short logic, Mishra 0.45-0.54 s/word @1.0): 3:42-3:47 (builder ~3:43). Inside 3:40-4:00; margin to 4:00 ~13 s, to 3:40 only 2-7 s.
- Last spoken line is a specific viewer question (line 41). Conflict at 0 s (ghost on roof), title promise (white figure on roof) on screen at 0 s via scene 2.
- Short A: 10 entries (lines 1, 12, 15-21, 26), text = long lines, no scene 13/14, no Mishra name/face; caption_from 1.0; end card 2.0 s inside end_hold 2.0; cover block: label किस्सागो, title "छत पर भूत?" (3 words, ends ?, not the Short title), hero Pandey, figure from behind, Golu + Mitthu, refs pandey/golu/mitthu, all shown things exist in the Short.
- Cost: recomputed from shared/pricing.json with the real ref counts (40 refs over 15 scenes, sheet 2 style refs, ~500 thinking tok): scenes ~₹72.5, sheet ~₹4.7, thumb + cover ~₹10, TTS ~₹4.5 (Short reuses long TTS cache) => ~₹92-94 incl. 18% GST, = PLAN ₹94; room for ~3 regens inside ₹110. cost_log: no 004 row yet (₹0 spent). Balance checkpoint ₹429.58 (> ₹50).
- Images: 15 scenes (ids 2-16) + Mishra sheet = 16; gen_scenes.py and gen_long_characters.py hard-code size="1K"; budget guard check() before each call. Refs = scene characters (+ location refs from story 003); Gupta sheet from 003, Dadi/Golu/Mitthu/Pandey/Sharma from channel characters/ (all exist).
- Prompts: base forces night blue-black with faces lit, never scary, white figure = person in a shawl with face hidden, Mitthu bird with no hands, no text. Face hidden in scenes 2, 9, 12; first shown in 13. Looks for Pandey/Sharma/Gupta match bible + 003 sheet; Mishra look in bible row (Story 004) = user spec; voice Enceladus in voices.py.
- Originality (RULES 12): closest = Long 02 (003). Differs in moral (loneliness/fear of the unknown vs checking rumours), genre/tone (night spooky-comedy turning emotional vs daytime farce), ending type (friendship + community chai vs apology/FIR torn), main conflict (fear of a "ghost" vs false theft rumour) = 4 axes; same setting + host ensemble; shape "mohalla panics, Dadi finds an innocent outsider" repeats (Note). No 5-word phrase reused from stories 001-003. Case 01: 5 axes differ, Long 01: 6.
- Metadata: long title 55 chars, hook in first 40, desc 324, 5 hashtags, 16 tags (266/500), no kids wording. Short title 69, 4 hashtags, 11 tags (161). CC BY credits are added at upload from the register (as Long 02 upload.json); the 4 tracks (Investigations, Monkeys Spinning Monkeys, Touching Moments Two - Higher, Carefree) all have CC BY 4.0 rows.
- RULES 6: thumbnail "छत पर भूत?" = 3-word phrase inside the title, not the whole title -> rule not broken; phrase overlap = Note (user's choice).
- SFX: night_822935 ("cricket chirping (slow)", _sinny_) and steps_682886 ("Very_Slow_Footsteps_Hardwood.wav", drewsimko): both Freesound pages show CC0 (publicdomain/zero/1.0) — checked myself; register rows 86/87 present; comedy_sting_731262 row 45.

## Problems (all MINOR, free)
- M1 intro length: lines 1-2 end at ~10.0-10.2 s by both rate methods (Golu line has 2 "..." pauses -> likely more). RULES 13 max 10 s. Fix: line 2 af atempo=1.32-1.35 (net ~1.06-1.08) and/or crickets pause 0.3 -> 0.15; builder re-measures after TTS (intro must end <= 9.8 s).
- M2 Short A length: my estimate 38.2 s (builder ~36 s) with 6 "..." pauses not fully counted; Short 003 came out ~12% over its script estimate. Max 40 s is a BLOCKER at final. Fix: speed 1.08, gap 0.15 / 0.30 (Short 003 values, no warble) -> ~36.7 s; re-measure after TTS; fallback pause 1.2 -> 0.8.
- M3 scene 15: Mitthu speaks line 38 here but prompt only says "Mitthu the green parrot" (no {mitthu} look, no ref) -> off-model risk. Fix: use {mitthu} and add "mitthu" ref (+~₹0.2).
- M4 scene 16: "a few other neighbours softly visible behind them" -> duplicate/lookalike risk (Long 02 BLOCKERs img09/26). Fix: "no other people", or name the ones meant. Also end screen (last 20 s = lines 40-41 + 8 s hold): compose the group in the left ~60%, right side open starry sky.
- M5 long description "सीख: जिससे हम डरते हैं, अक्सर वो बस अकेला होता है।" and pinned_comment "... कोई 'मिश्रा दादा' ..." hint/name the twist. Fix: moral line e.g. "डर को देख लो, तो वो आधा रह जाता है।"; pinned comment without the name.

## Notes (no action needed)
- Thumbnail concept "Golu and Pandey ji hugging" never happens in the video (main promise, the roof figure, does) — consider Golu clinging to Dadi / Pandey shaking with lathi.
- Line 1 Golu voice over scene 2 (POV, nobody else on screen) — intended hook.
- Scene 12: hooded faceless white figure lit by lantern can read as ghostly — check "gentle" at image review.
- Short: quick mood flip tension -> comedy (line 2) -> tension (line 3) in ~8 s; "night" sfx defined but unused.
- PLAN §4 cites "< 30 s RULES 13"; for story 004 the reason is the 35-40 s target (RULES 15). Without lines 1/12 the Short is ~30.5 s incl. hold.
- shared/sfx/CREDITS.md lists night_822933 and steps_324584, which are not in shared/sfx (stale lines).
- Hashtags 4/5 same as Long 02 — rotate one or two next time.
