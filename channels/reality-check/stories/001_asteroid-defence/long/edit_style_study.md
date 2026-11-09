# 001 asteroid defence - REBUILD PLAN from the study of two Hindi space explainers (2026-11-08)
Source: channels/reality-check/brand/STYLE_LEARNINGS.md (principles only; no frames/text/titles reused). Rs 0. Notes only; no tool code or footage was edited.
Ref A = presenter-led, explains best (diagrams + hand analogy + numbers ladder). Ref B = faceless, fast stock/CG montage, explains less (clips often do not show what is said; some shots reused as filler). We copy A's explaining method and B's faceless rhythm; we avoid B's filler. NO film clips, no people-face stock.

## 1. Targets (measurable)
- Shot length: median 4-6 s, avg ~6 s over 18-19 min (about 9-11 cuts/min on average) with NO flat rate: calm 7-9 cuts/min in intro and Hera/verdict, dense 14-20 cuts/min inside ch4 (the 33-minute answer) and the ch3 detection ladder. Max 8 s without a visible change (RULES 13); 10-14 s allowed ONLY for a drawn animation that keeps one part moving. No shot <1.5 s except number-flash bursts (max 3 per minute).
- Every shot has motion: slow push 1.00->1.06 / parallax, or a drawn element that moves (arrow, orbit, bar fill, ring). No static text card; a card is allowed only as the END of an animation (builds on, holds 1.5-2.5 s).
- Hard cuts by default. A 5-8 frame warm flash (orange/yellow, 1 SFX hit) ONLY at block boundaries (about 1 per 40-60 s, ~20 in all): chapter starts, each REVEAL, the answer. Never flash on every cut.
- Number labels appear ON the spoken number word (0 to +0.3 s after it, never before), hold 3-4 s, one fixed box style (bottom third, 5-6% height, bold, white on dark/orange chip), max 2 text items on screen. Source label [n] bottom-left 2-3 s as already planned.
- Pictures that introduce a new object lead the voice by 0.2-0.5 s (picture first, word second); they never lag. Trims: start on the first MOVING frame; end on the last informative frame; real footage 2-4 s max, trimmed to the peak, never played whole.
- Sound at cuts: soft tick/whoosh (<0.15 s) on every graphic-type change; hit + 0.25 s music duck on flash boundaries and REVEAL cards; music bed continuous (no dead air); voice mix about -16 to -18 LUFS, LRA under 4 LU. Breath space = 0.5-0.8 s visual hold, not silence.
- Weak footage hidden by: <=3 s, motion, label on top, never reused for another claim. If no footage truly shows the sentence, draw our own graphic (we already plan 138 own-graphic shots); never fill with generic space clips.

## 2. Explanation recipe (use in all 7 sections)
Question line on screen (small, 2 s) -> picture that SHOWS the answer with one moving part -> one-line rule card that builds on -> ONE number from a ladder. Introduce each idea by the problem it solves. Show hard material (the beta formula) 2-3 s, say it is one idea, move on. Numbers as ladders: small, medium, then the shocking one, each on its spoken word.

## 3. Section by section (intro + ch1..ch6; times from script v2)
1. Intro 0:00-1:04 (7 vs 33). Scale problem -> disappointment. NASA approach still with push-in 0-5 s, impact replay trimmed to the flash; then ONE long drawn orbit (rc_orbit_anim): the "7 min" bar grows, the real "33 min" slams over it (BEFORE/AFTER); 73 s as a tiny scale-compare bar. 8-10 cuts/min, number flashes allowed here. Low drone + one impact hit on 33.
2. Ch1 1:04-3:39 stones from the sky. SIZE LADDER animation (continuous zoom-out, bus 20 m -> 50-60 m -> 140 m+ -> 1 km -> 10 km, rung label on each spoken word); Chelyabinsk and Tunguska as own drawn top-views (blast ring, trees falling radially), no photos. 9-11 cuts/min. Replaces text-card shots.
3. Ch2 3:39-6:17 DART. Spacecraft + asteroid drawn to scale with a distance bar, countdown 7 -> 0, impact = flash + debris cone; the expected 7 min as a faint ghost orbit on screen. Real NASA stills only for the true impact and tail, 2-3 s each.
4. Ch3 6:17-10:32 detect first. Trajectory diagram with an EMPTY telescope view and a sun-glare wedge (red 'andekha'); warning-time ladder years -> months -> days; survey sweep lights dots one by one. 12-16 cuts/min; flash at each reveal.
5. Ch4 10:32-13:41 THE ANSWER (densest). The push explained with two balls (section 5, item 4): sticks -> one arrow; debris flies out -> second arrow stacks; beta = total arrow / first arrow, shown last. 14-20 cuts/min with 8-10 s build animations. One flash only at the REVEAL.
6. Ch5 13:41-16:00 methods. Each method = one 6-8 s mini-demo in the same layout (spacecraft | rock | result bar), then a comparison table built row by row. 10-12 cuts/min.
7. Ch6 16:00-18:38 Hera and verdict. Calm: status and verdict cards, slow push on the orbit with the new period, 6-8 cuts/min, the closing viewer question; last 20 s nothing essential (end screen), ~20 s music tail.

## 4. Current build -> what to replace
Current long/output/001_long_real_chat.mp4 + tools/rc_real_look.py: many shots are text cards or do not show what is said. Rebuild order: (1) list every shot whose card only repeats the spoken sentence and swap in the matching animation below; (2) keep shots that already show a moving diagram; (3) flash boundary on every REVEAL/chapter start only; (4) re-time cuts to the per-chapter rhythm (no shot added without new information); (5) add the tick/whoosh layer from rc_sound; (6) verify with scene-detect: cuts/min per chapter, and a "no shot >8 s without change" report.

## 5. Animations to build (own, code-drawn, free; palette: navy bg, orange = push / our spacecraft, cyan = asteroid, red = unknown)
1. SIZE LADDER: continuous zoom-out with five silhouettes and a city strip for scale; labels on spoken words.
2. BLAST RING: expanding ring on a top-down map, radius label (km), dots (windows/trees) react as it passes.
3. ORBIT SHORTENING (extend rc_orbit_anim): ghost 7 min orbit vs real 33 min, period bar fills.
4. THE PUSH (momentum made simple): two balls on a flat floor. A: small ball hits big ball and sticks -> one orange arrow (length 1). B: same hit but pieces fly out the front -> big ball gets a second arrow behind the first (recoil, like a balloon letting air out); arrows stack = 1 + extra; beta = total / first. Same colours and direction always; legend 'ek dhakka' / 'extra dhakka'.
5. DETECTION SWEEP: sky grid, scan line, dots appear; sun-glare wedge hides a zone.
6. WARNING-TIME BAR: years -> months -> days, response options grey out one by one.
7. TRAJECTORY draw-on: thin white line grows from the Sun side with ticks.
8. METHOD MINI-DEMOS x4 in one shared three-part layout.
9. NUMBER LADDER chips (73 s / 7 min / 33 min) timed to the spoken words with scale bars.
10. SOURCE CARD: our own neutral page-style card with the key phrase highlighted yellow as it is read, only where a [n] source is spoken.

## 6. The repeated word 'dhakka' (push), kept simple
ONE visual for ONE word: the orange arrow. First time word and arrow appear together (ball hits, arrow grows). Later times the arrow pulses 0.3 s on the word instead of a new text card. Only two kinds: 'ek dhakka' (spacecraft hit, one arrow) and 'extra dhakka' (debris recoil, lighter second arrow with a plus), always the same two colours. No 'momentum' or formulas on screen; on the beta line show it 2-3 s and say it as 'total dhakka, kitne guna'. The script is NOT changed here; at a later pass Kalam could cut the 25 uses to those two named kinds.

## 7. Thumbnail and title proposal for 001 (principles from the refs; nothing copied)
Thumbnail: dark space background; ONE big warm-glowing object (asteroid with a bright impact flash, or a drawn orbit ring) filling the right ~55%; small spacecraft silhouette for scale; no face. Text: 3 big words top-left, e.g. '7 MIN? NAHI, 33' (yellow box on the first word, white for the rest, text ~25% of frame height, readable at 160x90), accent = our orange on navy. One focal point (the flash), high contrast, bottom 10% empty or one small label.
Title options (keyword and the question inside the first 40 characters, no misleading promise):
1. DART Ka Dhakka: 7 Minute Ka Hisaab, 33 Kaise Ho Gaya?
2. Kya Hum Asteroid Ko Sach Mein Mod Sakte Hain? DART Ka Asli Result
3. 7 Minute Socha Tha, Nikle 33: Asteroid Ko Dhakka Dene Ki Asli Kahani
Pick after the Nigraan check; the thumbnail must keep the 7-vs-33 promise and the video must show it within 60 s (RULES 13).

## 8. Limits of this study (honest)
Scene detect misses dissolves and continuous camera moves, so cut counts are minimums. Contact sheets were 1 frame per 5 s; Ref A presenter share is about half the runtime by eye only (face detection was unavailable). Whisper small/Hindi finished only the first ~2 min of Ref A, so word-to-visual timing (label on the number word, +-1 s) comes from that part plus the sheets. Two refs = a small sample; Ref B is a 57k-view video, Ref A 16.7M.
