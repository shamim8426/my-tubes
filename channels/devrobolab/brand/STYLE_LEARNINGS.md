# DevRoboLab - style learnings from a study of one AI-tools explainer Shorts channel (2026-11-03)

Source: 6 Shorts of one channel, 92-113 s each, studied under RULES 12c; all downloads deleted on 2026-11-04 (see research/study_log.md). Only abstract,
numeric style findings are kept here. No frames, lines, titles or names are reused. Measured on 360x640 sources.

## Text
- Look: very light grey background (about #F2F2F2), near-black sans text (geometric grotesque, regular + semibold/bold mix), a faint small grey watermark line at the bottom. Calm, "product-page" feel, not loud.
- Size: body line about 4.5-5.5% of frame height (our statement scene at 104 px = 5.4%, so we are already as large or larger). Hook / number line about 6-7%. Key line spans 60-75% of frame width.
- Case: sentence case; ALL CAPS only for one hero word (a number or a quoted keyword).
- Words at once: 3-6 per line, up to 3-4 stacked lines (about 12 words max on screen). Block centred in the lower-middle (y about 62-82%), leaving the upper half to the visual.
- Reveal: WORD BY WORD in step with speech (about 3 words/s). The upcoming word first appears grey, slightly blurred and lower, then turns black as it is spoken. The key word of each line is bold/semibold, the rest regular: weight contrast, not colour, is the emphasis. A full line is replaced by cross-fade, not scrolled.
- Entry: each word fades + rises 8-12 px in 0.15-0.2 s, no overshoot on words. The whole block exits with a quick fade/blur at the end of the beat.
- Lists: 2-3 short rows, each led by a small round icon (check, cross, star); rows appear one by one on the spoken item (0.3-0.6 s apart).
- Special: a rank label ("Number N") centred and bold at about 6% height with a small mascot beside it; a short italic phrase for a twist.
- No outline, no heavy shadow, no highlight box; emphasis = weight and size only.

## Motion / edit
- Voice speed 177-200 words/min (English), almost no pauses (longest gap under 1 s; 1-9 gaps over 0.4 s per video): very dense.
- A new visual unit every 2-4 s (scene-score cuts 9-27 per minute, mean about 13/min; busiest video 26/min). Most "cuts" are object swaps inside one clean canvas, not hard camera cuts. Average shot about 4-5 s with constant motion inside it.
- Every unit is ONE clean subject centred on the plain background: a laptop / phone / window mock-up with soft drop shadow, a big app icon, a 3D-looking object, a pixel mascot, a code or document window. Subject enters with scale 0.6 -> 1 + fade (0.3-0.4 s) and leaves by fade or a slight push-down.
- 3-5 moving elements together: hub-and-spoke diagram (centre icon + 4-6 small logos orbiting or branching on thin lines), an icon tree that grows as lines draw, a stack of cards, a progress bar filling, a loading ring, a number swap.
- Callouts: thin connector lines with right-angle elbows, drawn on over about 0.4 s; round icon badges (about 10% width) as nodes; a small red warning triangle for a problem; a tooltip-style label on a mascot.
- Zoom/shake: gentle slow push on screen mock-ups (1.00 -> 1.06 over the beat). No camera shake, no speed ramps. Transitions: soft cross-fade/blur between subjects, no colour wipes.
- Quiet background layer: faint dot grid, large pale arcs, small sparkle accents; one warm accent colour used on one decorative shape per scene entering from a corner.
- Screen recordings: dark UI windows shown as floating mock-ups (rounded corners, shadow, slight perspective), never full-bleed; the bottom text area stays clear.
- Counters: a loading bar with percent, a big-number swap for a claim, a countdown listicle where the rank label opens each beat.

## Structure
- Hook: the claim is spoken from word 1 (0.0 s) and is on screen as text within 0.3 s; it states result + tool category + a surprising number or "free". Hook 6-8 s, including the first visual payoff.
- Beats: hook -> 2-3 benefits/negatives as a tick/cross list (about 3 s) -> why it was hard (problem with a number, 8-12 s) -> the tool introduced by name on a clean card (about 3 s) -> how it works through an everyday analogy visual (15-25 s) -> proof / use cases -> CTA.
- Listicle variant: "Number N" cards at a fixed rhythm (about 9-12 s per item), each = mascot + command chip + 2-line explanation + small mock-up.
- Tool intro: the name appears alone, large, centred, 1-2 s with its logo; features then shown as moving mock-ups, not described.
- Claim vs picture: every claim has a matching visual within about 0.3 s of being spoken (number -> number graphic; problem -> warning icon; agents -> mascot group).
- Ending: last 12-15 s = comment-keyword CTA (one big quoted word, about 7% height) + a free-resource offer shown as an open-book/PDF mock-up + a follow line with a logo; hard stop, no loop reveal. Length 92-113 s (longer than our 35-75 s).

## Sound
- A constant light music bed mixed low under a close, bright, compressed voice (mean loudness about -14 to -15 dB, peaks 0 dB): voice-forward.
- Short soft whoosh/click accents at object swaps, no loud hits. Voice: confident, quick, even pitch, clipped sentence ends.

## What makes it clear vs our current format
- One dominant subject + one short text block per screen: nothing competes. Ours often uses full-text scenes (statement/list) without a moving subject.
- Word-by-word grey -> black reveal paces the eye with the voice; ours reveals a whole row at once.
- Constant micro-motion (floating shadows, drawing lines, bobbing) keeps still frames alive.
- Do NOT copy: pale grey palette and smaller type. Our white/black/yellow marker look with larger bold type is stronger on a phone.

## Map to DevRoboLab (ranked by impact on clarity vs effort)
Our system: scenes statement/chips/flow/docs/code/list/compare/hub/cta/stage; stage layers img/box/doc/hook/text/meter/svgbot/draw; keyframes x/y/s/o/r; row-level "rise" plus highlighter "wipe"; parse() already splits text into .w word spans.

1. Word-by-word reveal in sync with speech (impact high, effort S-M). Partial support: words exist as spans but anims are per row. Needs a new anim kind 'words' (stagger 0.12-0.2 s per word from a cue, fade + rise 10 px, upcoming word grey -> #111) for statement and stage text; optional deck field "stream":true. Highlighter wipe stays on key words.
2. One dominant moving subject per beat (impact high, effort M). Supported via stage (img/box/doc/svgbot). Needs 3-4 reusable stage presets (device mock-up, app-icon card, doc/code window) with a soft shadow option on box and a scale 0.6 -> 1 entry keyframe; mostly content habit.
3. Hub-and-spoke / orbit with small logo nodes (impact high, effort M). hub scene exists (centre + popping nodes). Needs connector lines via the draw layer, a slow orbit (group rotation keyframe r) and round icon badges.
4. Tick / cross icon list with rows on the spoken item (impact medium-high, effort S). list/chips exist; add round check/cross glyphs and 0.3-0.6 s cues: template tweak only.
5. Progress / loading bar + number swap (impact medium, effort S). Stage 'meter' with keyframe f covers the bar; add a percent label bound to f and a big-number swap using a text layer with o/s keyframes.
6. Hook rule: claim as text at 0.3 s with a number, first visual payoff by 6-8 s (impact high, effort XS). No code: add to the script/deck checklist (first cue at 0.0-0.3 s, first stage layer within 3 s).
7. Soft blur-fade between subjects instead of only the yellow wipe (impact medium, effort S-M). Add scene option wipe:"fade" (0.25 s cross-fade); keep yellow wipe for chapter changes as our brand signature.
8. Quiet background layer: faint dot grid / pale arcs / one yellow accent shape (impact low-medium, effort S). Scene css option with slow drift keyframes.
9. Comment-keyword CTA with a free-resource mock-up (impact medium, effort S). cta scene exists; add an open-book/doc image through the docs/img layer.
10. Slow push on screen mock-ups (impact low, effort XS). Already supported by stage s keyframes (1.0 -> 1.06).
11. Density target: 15-25 visual changes per minute, one every 2-4 s; lengths stay 35-75 s.
12. Not adopting: grey palette, small type.

## Endings (second look, 2026-11-04: ONE Short of the studied channel, last ~20 s only; abstract, numbers only)
- Length and rhythm: the ending is about 16-20 s of a 100 s Short and has THREE beats in a fixed order: (1) payoff recap in one sentence with 2-3 bold words, (2) a 'value exchange' ask, (3) a follow ask. Each beat is one sentence of about 8-14 words (voice about 3.2 words/s), nothing after the last word (hard stop, no loop).
- Beat 2, the ask is a TRADE, not a plain 'comment': the viewer is promised a free resource for a one-word comment. Screen: the keyword is a big quoted word at the top (about 6-7% of frame height) and stays up for the whole beat (about 10 s); below it a 3D mock-up of the resource (a book) tilts in, then flips open to show pages while a short benefit line streams word by word.
- Beat 3, the follow ask is GATED: following is presented as the condition for receiving the resource ('only followers get it'). Screen: the channel name in heavy type with the word 'follow' in italics above it, a big brand mark (logo with a small crown) gets its own hero moment on a faint grid, and a second line streams in below. About 4-5 s.
- The brand name is spoken and shown at the same moment; one brand mark on a clean background; faint watermark line at the bottom through the whole video.
- Visual change inside the ending: roughly every 3-4 s (keyword card -> resource mock-up -> pages -> brand mark), all on the plain pale background, no new colours.
- What we take (principles only): end with a short, concrete REASON to follow (a promise of value), say and show the channel name together, give the brand mark one clean hero moment, keep each sentence short, stop on the last word. What we do NOT take: the comment-keyword + ebook trade as a pattern, the gated 'only followers receive it' wording, the crown logo idea, the pale grey background, or any of their sentences. Our endings are original, in our look (robot, Follow pill with a cursor click, bell, dust burst), and only promise what we really deliver.

## 2026-11-07 Study (Badar Munir editing style)
See shared/STYLE_LIBRARY.md section 8. Apply to AI-news Shorts: split screen (top proof, bottom mascot), 1-3 word captions at the seam, new top picture every 2-3 s, 2-4 small boxes, hard cuts + zoom-in, no copied footage/words.
