# Munshi — story 005 (Long 04 + Short A) — script/plan R1 — 2026-10-20

VERDICT: FIX (2 BLOCKER + 11 MINOR, all free; no paid call needed for any fix). STOP: none (ledger balance ₹279.81 > ₹50, no copyright doubt, channel ID untouched).

## Verified
- script.md vs long/lines.json: 48/48 spoken lines word for word, speakers right, order right; line 21 = pause 1.5 s + sfx pump; line 43 golu + with [tara, tinku]. Short lines 24/26/27/31/32/34/36 = long text, speaker, scene.
- Narrator trims 3/16/24/34/45 vs the approved draft (.specstory): only "वो/मोहल्ले के", "पुरानी/दोनों", "लकड़ी का", "पांडे जी की" and a full stop removed -> meaning kept; no dialogue touched.
- Chorus code (make_short build_voice / check_tts_spend): every "with" voice is counted in the spend check, own CAST voice + pitch, own atempo, trimmed and mixed from the same start, gain 1.2/sqrt(n), clipped to int16. OK.
- Speeds: long meta speed is a dict -> channel.json golu 0.95 / tara 1.0 / tinku 1.0 merged (story >= 5). Short meta sets all kids explicitly.
- Length (measured raw TTS rates from 003/004 caches, s/char; kids: Golu rate .. Tara/Tinku sample rate): long 3:59 .. 4:16 (mid 4:06) -> over/at the 4:00 max. Intro ends ~10.5 s (> 10). First word ~0.65 s. Short A 36.1–36.7 s (OK).
- Originality vs 001–004: closest = 004 (Gulmohar, narrator, Pandey, heart-warming twist). Differs in moral (friendship vs loneliness/fear), plot shape (riddle treasure hunt vs night ghost watch), genre (adventure/puzzle vs night comedy), leads (Golu ki toli vs Golu/Dadi/neighbours), setting (sunny lanes/hand pump vs night roof) = 5 axes; ending type similar (identity twist). PASS.
- Logic/bible: Dadi ~70, 1965 = 60 yrs, Kammo from Kamla; Pandey ~45, Bablu (~10 in 1965) = his father; no name clash (no रमेश/शीला/बबलू/कम्मो before; Pappu doodhwala untouched); torch (28) before hand (31); patch replanted (45, scene 16); Golu–Tara friends only; Tinku teased ("बुद्धू") but his thin arm wins (30, 31); Mitthu never uses hands in prompts.
- scene_prompts: 14 scenes (2–7, 9–16), scene 8 via covers [7, 8] (make_short maps it); + Pandey sheet = 15 new images (<= 16), 16:9, 1K; refs = only the scene's characters; gen_scenes adds STYLE_PAINTED block, sheet_painted refs, Mitthu/Tinku/Tara notes and name_guard. name_guard OK on prompts, metas, lines, script, gen_painted.py. Map (3) and photo (13) prompts say no writing.
- Pandey painted sheet already made: ₹4.84 + GST ₹0.87 = ₹5.71 (quick look: plump, moustache, khaki + cap, no text; formal check at images stage).
- SFX creak_377552 (Mafon2) and pump_832465 (qubodup): Freesound pages show CC0 only; register rows present. Music 5 moods all CC BY rows with attribution; credits are appended by make_short.
- Metadata: long title 64 chars (hook in first 40), desc 335, 5 hashtags, 15 tags 268 chars; Short title 79, 4 hashtags, 10 tags. No Kammo/Bablu/Babuji/father in any metadata, no "for kids".
- gen_short_cover.py now has the painted branch (LAYOUT_PAINTED + style block + sheet_painted + notes + guard; uncommitted with painted.py).

## BLOCKER (free)
- B1 scene 7 / 8 (lines 13–15): image 7 is a running chase, scene 8 = crops of it, but lines 14–15 say the children hide behind a wall and Tara reads the map again -> picture contradicts the script for ~12 s. Fix: rewrite scene 7 prompt to "just escaped: the three crouch hiding behind a low brick wall at the end of the lane, panting; Tinku peeks back over the wall, Tara unfolds the map on her knees, Golu catches his breath; Mitthu lands on the wall; dust still in the air"; move line 13 ("भागो!!", sfx comedy) to scene 6 (Pandey bursting out, Tinku present). Keep covers [7, 8] (scene 8 = close crop on Tara + map).
- B2 scene 12 (lines 28–32): prompt has Tinku's arm already in the crack "up to the elbow" while lines 28–30 say "पहले टॉर्च से देखते हैं" / nothing inside yet / "डाल दिया" only at 31 -> wrong order (and the child-safety beat). Fix: "{tara} shines a small torch into the crack, the beam shows a tiny glint deep inside; {tinku} kneels at the crack, sleeve pushed up, his very thin hand just slipping into the opening; {golu} holds his breath".

## MINOR (free)
- M1 length: est 3:59–4:16 vs max 4:00. Set now: gap 0.5 -> 0.4 (−4.8 s) and narrator 0.9 -> 0.95 (−4.3 s) -> est ~3:50–4:07 (mid ~3:57). After TTS (cached, free): if > 3:58 -> end_hold 8 -> 7, then gap 0.35; if < 3:40 -> gap back to 0.5. Dialogue never cut.
- M2 intro: line 2 ends ~10.5 s (> 10). Add "af": "atempo=1.1" to line 2 (narrator ~0.99 for the hook) -> ~9.9 s; verify after TTS.
- M3 scene 10 (lines 18–23): Golu already pumping with water gushing while Mitthu/Tinku/Tara talk and Tara only asks him to pump in line 20. Prompt: "{golu} grips the handle with both hands, just starting to pump, a first trickle of water".
- M4 scene 6: "{pandey} in his vest-and-uniform at home" fights the look/sheet (khaki uniform + cap). Drop "in his vest-and-uniform at home".
- M5 scenes 3/4 (lines 4–6): Tara says "इस पर कुछ लिखा है" and they read a verse, but the map has pictures only. Add "a few rows of very faded, smudged ink lines like old handwriting, blurred and unreadable, no letters or numbers" (images stage checks no letter shapes).
- M6 scene 13 (line 39 "गोल-मटोल बबलू"): photo should show four children incl. one chubby boy and one girl with two braids (Kammo); add to the prompt (faces still soft, no writing).
- M7 line 35 "1965": TTS may say the digits oddly. Put "उन्नीस सौ पैंसठ" in "text" and the original line with 1965 in "caption" (make_short supports it); spoken words unchanged.
- M8 long/meta.json "thumbnail" has only "text" -> gen_thumb_painted.py needs "prompt", "refs" (and optional "lines") -> KeyError. Add them from the script THUMBNAIL line (characters right of 42%, BR corner plain); keep the map as the focal object and the tin box small (the box appears only at ~2:21; the map at 0 s keeps RULES 13 promise).
- M9 Short cover prompt says "Lower part (61%-82%)" -> "61%-80%" (LAYOUT_PAINTED + carry_over 2026-10-20 cover row).
- M10 long tag "बच्चों की टोली" -> "गोलू की टोली" (family-audience wording, safe side).
- M11 PLAN.md cost: TTS ₹3 -> ~₹6–7 (004: 41 lines = ₹4.98 incl. GST; 005 = 50 calls), so total ~₹108 of ₹110 (sheet ₹5.71 actual + 14 x ~₹5.9 + thumb ~₹6.2 + cover ~₹6.8). Write down now which scene becomes a crop if one regen is needed (e.g. scene 9 -> crop of image 10/11) so a regen never crosses ₹110. Pipeline: gen_short_cover.py budget check uses ₹3.24 (004 cover actual ₹6.78) -> use pricing estimate.

## Notes (no action needed)
- Title "दादी का 60 साल पुराना राज़!" hints the box is Dadi's while the thumbnail asks "किसका है ये खज़ाना?" — user's title, not a Jasoos mystery, Pandey twist stays hidden.
- Line 41 "भाभी जी" fitted the old draft (Pandey = Pappu, Dadi's friend); with Bablu = his father, "अम्मा जी/चाची जी" fits the generation. Dialogue is user-approved; change only if the user wants.
- Line 49 ends with "!" -> make_short will warn "last line not a question"; RULES 13 is met (a specific question to viewers).
- Tinku voice = Achernar (bible, channel.json, voices.py; user's choice) — Tara/Tinku pitch separation to be checked at the audio stage.
- Short title "60 साल पुराना डिब्बा" — the Short does not say 60 years, but it is true in the story; not misleading.
- Long 05 will need the RULES 12 channel-variety note.

---
# R2 — 2026-10-20 — PASS-WITH-NOTES
- B1 OK: scene 7 = hiding behind the low wall (Tinku peeks, Tara kneels with map, Golu panting, Mitthu on wall), covers [7, 8]; line 13 now scene 6 (Tinku present). Scene 7 has no own line, only feeds scene 8 crops (fine).
- B2 OK: scene 12 torch + glint first, Tinku kneeling, sleeve rolled, hand only starting into the crack.
- M1/M2 OK: gap 0.4, narrator 0.95, line 2 af atempo=1.1 -> re-estimate long 3:50 / 3:57 / 4:08 (kids low/mid/high), intro ~9.4 s, Short 36.1-36.7 s unchanged. After-TTS rules written in PLAN.md -> carry_over row (verify at audio stage).
- M3-M6 OK in prompts (sc10 first gush, sc6 khaki uniform and cap, sc3/4 unreadable smudges no letters/numbers, sc13 chubby boy + girl with braids).
- M7 OK: line 35 text "उन्नीस सौ पैंसठ", script.md notes (1965). Note: make_short caption override does accept a different word count (maps by character position); no change needed, srt shows the spoken words.
- M8 OK: thumbnail lines/prompt/refs, map focal, small tin box, no Dadi/Pandey/photo. M9 OK 61%-80%. M10 OK "गोलू की टोली". M11 OK PLAN TTS ₹6-7, total ~₹108, fallback scene 9 -> crop 10/11; gen_short_cover check 5.0.
- name_guard OK on scene_prompts, both metas, lines. Line 41 "भाभी जी" kept (user-approved). No STOP; story ₹5.71.
