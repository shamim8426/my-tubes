# InsiderForce presentation spec (living file; user 2026-11-18: follow it closely)
Rule: copy the PRESENTATION STYLE (layout, motion, pacing, text animation, callouts, transitions, SFX timing, ending). Never their frames, audio, script words, titles, logo, mascot or watermark (RUN_COMMON section 14).
Each run: study one fresh InsiderForce Short (RUN_COMMON "Fresh style per video"), add concrete findings below, then apply everything here.

## 2026-11-18 findings (studied two 87-93 s Shorts, 608x1080, ~6 hard cuts; everything else is animated entrances)
- BACKGROUND: flat very light grey/white (about #EBEBEB to #F4F4F4), no gradient, no grid. Our version: flat white/very light grey. NO mascot/robot of ours (user 2026-11-18).
- TEXT: centred, lower-middle (about 55-80% of height), sentence builds WORD BY WORD in step with voice. Mixed weight in one line: normal grey words + BOLD near-black keywords. New words fade/slide up 8-12 px; a word "pops" from grey to bold when it is the key one. 2-3 lines max, 3-8 words per beat; whole text swaps every 2-3 s. Size about 4-5% of height. Occasional italic word + a thin curved underline swoosh for a "simple/easy" moment.
- CARDS: white rounded rectangles (radius ~14 px) with a SOFT, large, diagonal drop shadow, placed in upper half. Cards slide/scale in with slight overshoot; contain real moving screen recordings or UI mock-ups. Several cards stack/arrange in a collage (2-4 items) that pop in one after another (photos, logos, a sticky note pinned with a red pin).
- ICON ON A STRING: a glossy 3D-looking icon/logo in a white circle hangs from a thin vertical line above the text and bounces in; used for a tool/brand name. Starburst accent lines (small orange rays) pop at a card corner when a card appears.
- LISTS: arrow bullets "->" appear one by one, each line types/fades in, key words bold.
- BEATS: every 2-3 s something new enters (card, icon, text swap); never a static screen. Hard cut only when the scene changes; between ideas the old card shrinks/slides away as the new one slides in.
- VIDEO INSIDE CARDS: moving content inside the card (screen recording of the tool working, or stock b-roll) so there is always motion. For us: animated UI mock-up playing inside a card, or free HD stock clips (Pixabay API key PIXABAY_API_KEY_FREE in .env) cropped to the card.
- WATERMARK: faint small text bottom centre. (Ours: only 'DevRoboLab' small, faint, bottom.)
- ENDING: voice call to follow; text swap; no long outro.

## 2026-11-18 30-FPS study (Short about publishing a Claude Code site; 2,596 frames analysed)
- Motion: 85% of frames carry motion, only ~1% are static. Big change roughly every 2-3 s; each swap takes about 5 frames (0.17 s) of fast motion, then the new element drifts slowly. The whole composition also drifts/zooms slowly the entire time (camera feel), cards float.
- Entrances: card pops from small with overshoot in about 4-5 frames; word fades in over 3-4 frames while rising slightly; key words go bold; text block re-lays out as words arrive. Icon drops on a thin string and swings; a small status icon inside it animates (lock opens, gear spins).
- Contents of cards are real playing screen recordings, not stills. A URL pill with globe and copy icon appears when a link is produced.
- Structure of the script: claim in first 4 s -> tool name -> one prompt copy -> what the agent does in 3 short steps -> supported file types -> manual drag-and-drop alternative -> what makes it different -> compatible agents -> follow call. About 25 spoken lines in 87 s; ours is 40-45 s.
- Ours (067): same grammar with our own cube/gear/agent icons, animated site mock, drop zone, file cards, URL pill; no mascot.

## 2026-11-19 study (one 101 s listicle Short, 608x1080 30 fps, ~28 scene changes = one every ~3.6 s; principles only)
- ITEM NUMERAL: each list item opens with a GIANT numeral (about 30% of height, near-black, fading to transparent at its bottom edge) with the item name in bold under it, held ~1 s, then the item's card slides in. Ours: chapter opener = big numeral + chapter name for ~1.2 s on the chapter's first words.
- STARBURST CORNERS: big soft orange ray bursts sit half outside the frame in two opposite corners on the hook and on a giant-number moment (frame "pulse"), then slide out. Ours: accent-colour rays on hook + big number beats only.
- HUB DIAGRAM: one centre icon, thin lines draw out one by one to 3-5 satellite icons (each pops in at the end of its line) while the voice lists them. Ours: centre file/tool icon, satellites = places/options.
- CHOOSER ROW: 3 small white cards in a row; the "selected" one scales up ~1.25x with a stronger shadow, then the selection moves to the next (shows automatic switching / picking).
- GIANT NUMBER INSIDE A SENTENCE: the running caption stops and the key number appears 2.5x bigger on its own line ("95%"), rest of the sentence continues small below.
- SPARKLE BULLETS: a heading line, then 3-4 items with a 4-point star bullet appear one per spoken word, left-aligned block centred on screen.
- TILTED DARK CARDS: dark UI cards sit with a slight 3D tilt/rotation and a very large soft shadow on the light background; they drift slowly.
- ITALIC EMPHASIS: one word in a sentence set in italic (e.g. "every single") instead of bold, for tone.
