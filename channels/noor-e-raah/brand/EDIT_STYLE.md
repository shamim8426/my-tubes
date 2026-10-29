# नूर-ए-राह — edit style (for the Sampadak)

Rules live in `channels/noor-e-raah/RULES.md` (1c, 2, 2a, 2b) and `brand/STYLE_NOOR.md`; this file says how the
finishing edit looks. Format of the plan: `tools/edit_fx.py` docstring. `scripts/noor_render.py` reads
`long/edit_plan.json` and applies ONLY the colour look (grade, vignette, grain) to the picture, before libass draws
the Arabic and Hindi text (so the text keeps its colours). Nothing else from the plan is used for Noor.

## 1. Mood
Calm, respectful, unhurried. The edit must never be noticed: it supports the ayah, never competes with it.

## 2. Look (default plan for every Noor video)
`{"grade": "soft_glow", "vignette": 0.12, "grain": 1.5}` — almost neutral, a little warmth, edges slightly darker,
very fine grain. Tested 2026-10-29 on Al-Fatiha: centre a little warmer/brighter, corners ~8 % darker, text unchanged.
Allowed range: vignette 0-0.18, grain 0-2.0. `grade` "warm_story" is NOT used here (too sweet).

## 3. Transitions
Only the builder's slow crossfade between shots (XF 0.5 s). No whip, flash, dip, shake, punch-in, speed ramp.

## 4. Text on screen
Only what the builder already draws: Arabic ayah (Amiri, libass), Hindi subtitles (Mukta, Ustaad white / Sawaal soft
gold), the "सरल भावार्थ — माने हुए तर्जुमों के आधार पर" label and info cards. The Sampadak adds NO text, no tags,
no pop-ups, no title card. Never anything over the Arabic.

## 5. Sound
Unchanged: continuous soft instrumental ~19 LU under the voice, one soft swoosh per ayah, mood ambience (RULES 1c).
No tilawat, no vocals, no beat, no comedy/tension stings, no extra SFX. (`sfx`/`ambience` keys of the plan are ignored.)

## 6. Never
- Anything that hides, tints, shakes, zooms or flashes the Arabic or Hindi text.
- Any effect that makes a place look scary or a worship scene dramatic; any "cinematic trailer" feel.
- A person/Prophet/Sahabi/angel image (RULES 2, 2a) — also not as a light, shadow or silhouette.

## 7. Learned from results / approved by the user
- 2026-10-29: look test only (no user opinion yet). Retention drop points of Al-Fatiha (14-19 s, 33-38 s) are fixed in
  the SCRIPT (hook promise within 30-40 s, first ayah soon), not by effects.
