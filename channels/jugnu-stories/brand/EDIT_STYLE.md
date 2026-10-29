# Jugnu Stories — edit style (for the Sampadak)

Rules: `shared/RULES.md` (3 audio, 4 captions, 13 algorithm) and `channels/jugnu-stories/RULES.md`; look of the
pictures: `brand/STYLE_PAINTED.md`. Format of the plan: `tools/edit_fx.py` docstring. `scripts/make_short.py` reads
`<video folder>/edit_plan.json` (`--no-edit` ignores it). STATUS: pilot look from story 005 Long (2026-10-29,
`channels/jugnu-stories/stories/005_gulmohar-ka-khazana/long/edit_plan.json`), the user has not given an opinion yet.

## 1. Mood
Warm, playful, quick: a mohalla comedy with a mystery. The edit adds energy at jokes and reveals and stays calm in
the cozy/wordless parts (STYLE_PAINTED section 7).

## 2. Look
`grade: warm_story`, vignette 0.22, grain 3.0 (the pilot values). `light_leak` over daytime golden scenes only.
Painted pictures stay painted: never push saturation beyond the grade's 1.08.

## 3. Transitions
- `whip` only on chase / "भागो" / arrival moments (pilot: scenes 5, 6, 8, 9, 11, 15 of story 005).
- `dip` (soft dark dip) for the calm turn to the evening / the moral (pilot: scenes 14, 16).
- `flash` only for a magic reveal, max once per video. Everything else = plain cut (the picture's own parallax moves).

## 4. Punch-ins / shake
- Long: 3-6 punch-ins per 4 minutes, zoom 1.10-1.16, 1.4-3.4 s each, on jokes, shouts, reveals. One comic shake max
  (0.55 s) on the funniest shout.
- Shorts: none (captions are burned into the frames; the builder skips them anyway).

## 5. Text on screen
- `title` once, top of the frame (not over faces), right after the intro; `tag` (name tag) on a character's FIRST
  appearance (Hindi names); `note` for riddle/clue text read aloud; `pop` for counting beats synced to Whisper word
  times. A note never shows the answer of a mystery.
- Fonts: Mukta Bold / ExtraBold only (libass). No AI-drawn letters.

## 6. Sound design
- From `shared/sfx/` (registered): whoosh_803771 / whoosh_142348 on whips, paper_353125 for the map/photo, magic_376745
  / 376747 for ticks and reveals, run_816792, pump_832465, tension_sting_578351 before the suspense, comedy_sting_731261 /
  731262 on jokes, birds_841386 as a daytime bed.
- Accents 12-20 dB below the voice, ambience 28 dB below. 12-20 accents per 4 minutes at most; none in cozy/wordless parts.

## 7. Never
- Effects over a Short's bottom 20 % / right 15 % safe zone; any effect that mocks a child's looks (RULES 12 sensitive).
- Anything that changes the length or the line timing; stings over a serious emotional line.
- Competitor frames/clips/sounds (RULES 12c).

## 8. Learned from results / approved by the user
- 2026-10-29: pilot built on story 005 Long (preview, ₹0), length 237.4 s unchanged, -14.0 LUFS, before/after sent to the
  user. Waiting for the user's opinion (what is too much / too little).
