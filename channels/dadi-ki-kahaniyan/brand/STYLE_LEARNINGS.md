# Style learnings for Kissago Painted (research notes, 2026-10-20)

Reference: ek cozy-ambience channel (research notes). Only public metadata was read (titles, duration, views, upload
date, descriptions of its most-viewed videos) and 3 thumbnails were looked at once (not stored). No video,
audio, frame or thumbnail is kept anywhere. Nothing below copies a specific scene, title or thumbnail: these are
general principles, rewritten for Gulmohar Mohalla. Status: PROPOSAL — nothing here is applied until the user approves.

## What the numbers say
| Signal | Finding |
|---|---|
| Length | the top videos are 5–9 min (median about 7 min); within that range length does not decide views |
| Topic | most of the top videos are monsoon rain + home cooking + family; the one non-rain video (hot summer) is the lowest |
| Spread | one very large breakout, then a group in the low millions, then a long tail; the strongest videos came in one short burst on the same topic (a topic streak that worked) |
| Format | no narration, no plot: wordless ambience + daily-life visuals, made for relaxed listening |
| Engagement | likes ~0.3–0.4% of views: watched as background ambience, not discussed |

## 1. Colour and light
1. One warm light source against a cool world: a lit doorway, lamp or chulha glowing orange inside a blue-green rainy scene. This warm/cool contrast is the strongest pull in the thumbnails.
2. Saturated, wet greens (banana leaves, palms, moss) and dark slate rain-clouds; warm terracotta tiles and brass.
3. Night and storm scenes stay readable: faces lit by the warm source, never muddy.
4. Food is shown in golden, glossy close-up with steam.
For us: Gulmohar's flame-orange stays our signature accent; monsoon adds slate-blue sky + wet greens; Dadi's lantern / chulha / Raju's stall is the warm source.

## 2. Composition
1. One main figure, one-third into the frame, medium-wide, with the house/doorway as the second subject behind.
2. Plenty of environment: rain streaks, trees, roof, sky take 40–60% of the frame — the place is a character.
3. Depth layers are always clear (foreground plants → figure → house → sky) — this suits our parallax.
4. A detail insert (hands, utensils, food, water) between wide shots.
For us: Dadi/Golu one-third in, aangan or chhat behind; one "detail" shot per scene (Dadi's hands with tea, Golu's paper boat, Mitthu's feet on the railing).

## 3. Pace (inferred from format, not measured)
1. Long, calm holds; slow drifting camera; few hard cuts.
2. Rhythm comes from small actions repeated (pouring, stirring, rain dripping), not from dialogue.
3. Scene changes follow the day: morning → work → meal → night.
For us: keep our story pace (shots ~2.6 s) for plot, but add short slow "breathing" moments (see cozy segments) with 6–8 s shots and gentler parallax.

## 4. Sound (inferred from descriptions)
1. Nature ambience is the main track: rain on tiles, thunder far away, wind in leaves, cooking sounds.
2. Music, if any, very low; silence is allowed.
3. Made for relaxed listening.
For us: only in the wordless part of a cozy segment, drop the music 4–6 dB more and add ambience (rain, crickets, chulha crackle, tea pouring) from Freesound; wherever Dadi or anyone speaks, the RULES 3 music level stays. Every sound's licence is checked on its own Freesound page (only CC0 or CC BY 4.0) and gets a row in shared/assets_license.csv (RULES 10).

## 5. Topics that worked
1. Monsoon rain (by far the strongest), 2. home cooking with steam, 3. family meal / children at home, 4. 1990s / nostalgia framing, 5. village daily routine.
Weak: hot-summer framing.
For us: rainy-day and cooking moments fit Dadi naturally; rain-themed stories (e.g. a mystery during the monsoon) are worth one test.

## 6. Title and thumbnail structure (no words copied)
1. Title: a nostalgia/time frame + a weather emoji + "|" + the daily activity + family, ~70–100 characters, calm and descriptive, not clickbait.
2. Description: long (2–4k characters), sensory sentences, emoji bullet list of moments, an invitation to relax and listen. (We do not borrow their listening keywords for our metadata.)
3. Thumbnails carry NO text; emotion comes from a face (worried, surprised) or from appetising food close-up.
For us: keep our hook titles (story question) but try one calm sensory phrase + one weather emoji; thumbnails keep our own text as RULES 6 requires (letter height ≥ ~12%), and try a stronger warm/cool contrast (warm lit doorway/lantern in a cool scene); our characters' faces stay the emotion carrier.

## 7. Length vs views
1. 5–9 min is their whole range; topic drove the difference, not length.
2. A run of same-topic videos (a streak) lifted all of them.
For us: our 3:40–4:00 story format stays (RULES 15); a cozy segment of 10–20 s fits inside it; consider a "monsoon week" of 2–3 rain stories — each still differs from the others in at least 3 of RULES 12's points (moral, plot, setting, lead characters, genre, ending), the rain alone is not enough.

## What stays ours and better
1. **Kahani:** every video has a real story (mystery or moral) with a twist and a question to the viewer — they have none.
2. **Dadi ki awaaz:** a warm narrator/Dadi voice and dialogue in Hindi — they are wordless ambience.
3. **Apne kirdaar:** Dadi, Golu, Mitthu and the Gulmohar Mohalla cast recur and grow — they use anonymous figures.

## Proposed improvements for STYLE_PAINTED.md (NOT applied — wait for approval)
1. **Light (section 3), not the style block:** add "glowing lamplight" to the Night and Rain light lines only, so day scenes stay sunny. Gives the warm-inside/cool-outside look in night and rain scenes. The style block in section 1 stays verbatim as approved.
2. **Palette:** add a "monsoon" row: slate-blue rain clouds, wet saturated greens, silver rain streaks, one warm orange lit doorway/lantern as the focal accent.
3. **Light:** add "Rain (baarish): diffuse cool daylight, wet reflective ground, one warm interior light visible".
4. **Camera/parallax:** cozy segments use `static_breathe` / `pull_out` at half motion (amp 0.0175) — calmer than story shots.
5. **Shot length:** cozy segments 6–8 s per shot (still within RULES 13's 8 s); story shots unchanged.

## Cozy segment ideas (10–20 s each, Kissago's own)
1. **Baarish me chai:** rain on the aangan's tiles, Dadi pours chai from a brass kettle on the chulha, steam, Mitthu shakes rain off under the eaves.
2. **Kaagaz ki naav:** monsoon puddles in the gali, Golu floats a paper boat, Raju's stall lamp glowing behind.
3. **Laalten wali raat:** power cut, lantern on the floor, Dadi makes rotis on the tawa, crickets outside.
4. **Subah ki dhoop:** morning sun over the chhat, Dadi waters the tulsi, Mitthu sunbathes on the railing, gulmohar petals drift.
5. **Shaam ke pakode:** evening drizzle, the mohalla gathers under Raju's tin roof, pakodas frying, warm light on wet faces.
Placement (RULES 13): long videos only, never in Shorts (max 40 s, first word ≤ 0.5 s); never at the start (first spoken line ≤ 1.0 s, intro ≤ 10 s, the story's question inside the first 30 s) and never in the last 20 s (end screen). Only at a natural pause in the middle or right after the twist, with ambience sound and gentle parallax; no new characters needed.
