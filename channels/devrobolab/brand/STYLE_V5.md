# DevRoboLab STYLE v5 (Shorts, 9:16) - from one Hinglish AI-news Short study + LONG_FORM_LEARNINGS

Source: one 38.6 s vertical Short (4K, 60 fps) from a Hinglish AI-news creator, studied 2026-11-06 under RULES 12c (study/s2, yt-dlp without cookies,
4 fps contact sheets + 1 fps frames + Whisper). Merged with brand/LONG_FORM_LEARNINGS.md. ONLY abstract principles are kept: no frames, lines, titles,
names or product wording are reused. Study files are deleted within 24 h (see research/study_log.md).

## 1. Measured shape of the study Short (38.6 s)
- Structure: face-cam (about 2 s) -> real screen/UI footage (about 5-6 s) -> face-cam -> UI -> face-cam -> UI ... The face-cam is NOT one long block: it comes
  back every 4-8 s as a "presenter beat" and takes about 45% of the runtime; the other 55% is real source footage (product UI, repo page, laptop b-roll, social profile).
- 13-14 visual segments in 38 s = a new picture about every 2.8 s. Between face and UI the transition is a short motion-blur whip/push (about 6-8 frames)
  or a page-flip/3D tilt of the UI card; inside a UI segment the picture moves all the time (scroll, cursor, auto-zoom into the clicked thing).
- Words: about 85 words in 38 s = roughly 130-140 wpm incl. gaps; the hook line comes in the first 0.3 s, no greeting, no channel intro.
- Order (reusable skeleton): 0-3 s hook = the news + the benefit ("free / now you can"); 3-8 s what it is in one plain line + its name; 8-15 s what it does for
  YOU (personal, on your own device); 15-28 s 3-4 concrete capabilities, each shown by REAL UI (not described); 28-34 s the unusual angle (open source / runs locally);
  34-38 s CTA with a comment keyword.

## 2. Hook (0-3 s)
- Frame 1 already shows something moving or a loud brand-colour logo lockup in the top third + the presenter below; the first caption is on screen from frame 1.
- Hook = "good news + what it costs you (nothing)". A small pattern interrupt lands at 2-3 s (falling-money overlay on the face-cam for about 2 s) so the free
  claim is felt visually, not only heard.
- For us (robot presenter, no face): frame 1 = robot + one huge claim card (6-8 words max) + the product logo/screenshot; money/free claims get an overlay (coins, sparks).

## 3. Visual rules
- Background for UI segments: near-black grid/texture; the real screenshot sits as a rounded white card at about 70-80% of frame width, centred or in the upper
  60%, with the captions below it. The card is BIG and legible; UI is never shrunk to a thumbnail.
- The card is never static: slow scroll of the page, a cursor/highlight on the thing being said, or a scale-in with slight 3D tilt on entry (about 0.3 s).
- Real screenshots/recordings carry the proof; every capability named in the voice is on screen within 1 s of being said (voice and picture change together).
- Colour: one saturated UI accent (violet-blue caption chip) + one brand gradient on the CTA word. Ours stays white/black/yellow marker + robot (see EDIT_STYLE.md);
  take the PRINCIPLE (one accent chip colour, one gradient only on the CTA word), not their colours.
- Overlays with meaning only (money rain for "free", laptop code b-roll for "runs on your PC"); b-roll is a single bright clip with a shallow-depth look,
  held 2-3 s, never decoration while the voice explains something else.

## 4. Captions
- Burned bold sans, ALL CAPS, 2-3 words per chunk, chunk changes about every 0.5-0.8 s following the voice; text sits in a solid rounded chip (opaque box behind the text),
  placed at about 72-75% of height on face segments and 66-72% on UI segments (inside the 15-85% safe area, above the platform buttons).
- Current chunk only (no karaoke highlight), the chip width follows the text; the key word of the line may be tinted. Chip is opaque so it reads on busy UI.
- Caption typos are tolerated by the creator; ours must be spelled correctly (Hinglish in Roman script, product names correct).

## 5. Cuts, motion, transitions
- Cut on the word, not on the pause: the picture changes at the first syllable of the new idea. Average shot 2.5-3 s, longest 6 s; no shot repeats the same layout twice.
- Face->UI and UI->face use a fast blur-push (3-8 frames); UI->UI inside one topic is a hard cut or scroll; only one "wow" transition (page flip/3D tilt) per Short.
- Zoom: punch-in of 5-10% on the presenter at emphasis words, ease-out; UI gets a slow push of 3-5% over the whole segment.
- No shake, no glitch, no speed ramps; at most one motion-blur per 6-8 s.

## 6. Sound
- Voice-forward and compressed, about -14 LUFS; a low music bed that never swells under speech; short soft whooshes on the blur transitions and a click/pop
  on the card entry (barely audible, -22 dB or lower). No silence gaps longer than 0.3 s inside the Short (the CTA end may breathe 0.4 s).

## 7. CTA (last 4-5 s)
- Presenter returns to full face; a big stacked lock-up "Comment / KEYWORD / for link" appears in the lower-middle, one-word gradient keyword, and stays to the end.
- CTA text is spoken twice in different words (once as the offer, once as the action); caption chip sits under the lock-up. The final frame is a still of the CTA, so
  the loop restart feels natural. For us: the keyword goes in CTA_PILL, link goes in the pinned comment (do not promise a DM).

## 8. Retention devices
- Open loop at 0-3 s ("free, new, you can do X") closed by the real UI demo at 15-28 s; a micro-loop before each capability ("and the best part...").
- Pattern interrupt every 5-8 s: face <-> UI <-> b-roll rotation, one overlay, one big-number or name card; never three same-type segments in a row.
- One concrete example prompt/task typed live on screen (about 3 s of cursor + text) beats three abstract adjectives.

## 9. Merge with LONG_FORM_LEARNINGS (what carries over to a 35-40 s Short)
- Numbers before concepts: one big-number card in the first 10 s (price, count, date).
- One named everyday example (not a person): carry a single task through the Short ("write an email", "find a headphone under X").
- Source line (3% height) under every real screenshot; official page only (RULES: no unverified claims).
- Jargon pill first time a term appears (2.5-3% height minimum for any text on a phone).
- Not copied: 16-19 min structure, paid-workshop plug, dark glass look, repeated promise.

## 10. Checklist for the next Short (Claude Feature 03 onwards)
1. Frame 1: robot + 6-8-word claim card + logo/screenshot; first caption chip visible at 0.0 s.
2. Timeline in 2.5-3 s beats; list them in deck.json with beat type (robot / UI card / b-roll / number card / CTA) and never repeat a type twice in a row.
3. At least 55% of runtime = real UI screenshots with scroll or cursor motion (the existing screenshot method).
4. One overlay with meaning, one blur-push transition type, one 3D-tilt/page-flip entry max.
5. Caption chips: opaque, 2-3 words, 66-75% height, correct spelling; key word tinted.
6. End: stacked CTA lock-up (KEYWORD word gradient/yellow) for the last 4 s, spoken twice; pinned comment has the link.
7. Loudness -14 LUFS, music low, soft whooshes on blur transitions only.
8. Length 35-40 s; a new picture at least every 3 s; no caption longer than 3 words at once.
