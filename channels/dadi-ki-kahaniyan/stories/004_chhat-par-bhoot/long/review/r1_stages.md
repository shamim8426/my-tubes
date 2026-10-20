# Story 004 छत पर भूत? — Munshi stage review R1 (2026-10-20)

Profile: RULES 15 (no preview; stages R1 + R2, then FINAL). Auto mode: no STOP condition hit
(ledger balance ₹330.64 > ₹50, no copyright doubt, channel ID not in scope at this stage).

| Stage | Verdict | Severity |
|---|---|---|
| A Scene images (13) + Mishra sheet | PASS (notes) | no BLOCKER |
| B Audio / timing | PASS (notes) | no BLOCKER |
| C Shot plan (long + Short) + overlays | FIX | MINOR x6 (RULES 13 shot length = FIX in R1) |
| D Thumbnail + Short cover | FIX | MINOR x3 |
| E Cost | PASS | ₹98.88 actual incl. GST <= ₹110 |
| Register (RULES 10) | FIX | MINOR: no rows for story 004 images/sheet/thumb/cover |

## A Images (all 13 opened full size + sheets contact sheet review/r1_sheets.jpg)
- Looks match sheets: Dadi (green saree yellow border, round glasses, stick), Golu (chubby, yellow/blue, red shoes),
  Mitthu (no hands anywhere: perches/flaps only), Pandey, Sharma (bald, rect. glasses, brown jacket), Gupta (pink saree),
  Mishra (= sheet: white hair, moustache, round glasses, cream shawl). No duplicates/look-alikes, no text.
- White figure: sc02 small, from behind; sc12 back of the shawl, head covered; first face = sc13 (Mishra). Not scary.
- Action vs lines ok: sc04 Golu points + fan, Mitthu on shoulder, Dadi waves "so ja"; sc05 Gupta "this tall", Sharma
  hugs mattress; sc06 lathi + laddoos; sc07 knees knocking on stairs; sc08 Gupta shutting door (balcony, lit windows);
  sc10 hug + Mitthu flapping; sc11 lantern + Golu behind saree; sc13 reveal; sc14 Saptarishi (7 stars) + both pointing;
  sc15 chai/pakode, Pandey sheepish, lathi behind back; sc16 four only, group in left ~55%.
- Notes (no action): sc04 Golu barefoot at home; sc04 vs sc10 room/window differ; sc07 brighter than deep-blue night;
  line 33 (narrator "अकेलापन देखा") sits on the happy pointing image 14 (optional free: put it on sc13 Mishra close).

## B Audio (40 cache files used, keys recomputed with make_short.tts_key; timeline re-simulated; Whisper small on all 40)
- Long: first word 0.75 s, intro ends 9.44 s, speech end 216.32 s + end_hold 8 = 224.32 s (3:44). Short: first word
  0.00 s, 36.42 + 2 = 38.42 s. Builder numbers confirmed.
- Whisper: every line complete, no cut words (line 42 "कमेंट में बताइए" present at 0-1.2 s; line 31 ends "हूँ";
  line 13 "देखूँगा" soft but present). Mishra = Enceladus (voice is part of the cache key). Mitthu +5 st.
- Notes: intro narrator line plays at net 1.0x (atempo 1.25 x 0.8) vs 0.8x for all other narration (audible pace
  step into line 4, taste); narrator_8987b0c049aa8128.wav (old long intro, ₹0.18) unused.

## C Shot plan — FIX (free)
1. Long shots > 8 s (RULES 13): sc13 line 29 Mishra 11.7 s; sc13 lines 31+32 Mishra 12.6 s (same speaker = no cut);
   sc16 lines 41+42+end_hold 24.7 s on one Dadi close [0.15,0.55,1.7]. Fix with "shots" splits (<= 8 s each).
   Note: a same-speaker line gets no cut of its own, so put the split for 41-42 on line 41.
2. End screen (last 20 s = 204.3-224.3 s): the Dadi close puts Mishra in the right 70-94% of the frame. Use the sc16
   wide (group left, sky right) for the end of line 42 + end_hold, split into <= 8 s moves.
3. Short last shot sc12 = 8.06 s (line 10 + 2 s end card): split line 10 into 2 shots.
4. Short subjects sc08 box [0.86,0.42,0.97,0.80] is NOT Gupta (that is tree/balcony). Gupta = x 0.68-0.85,
   y 0.28-0.80 -> box [0.68,0.28,0.86,0.80]. Current crop shows her by luck (face at 5-30% of crop).
5. Short sc06 box ends at 0.45 and leaves out Pandey's lathi hand (x 0.45-0.49): it sits in the right 15% (buttons).
   Box [0.20,0.10,0.49,0.55] (face + lathi hand; hip hand may go).
6. Overlay sc11 diya at (0.43,0.47) is on Dadi's shoulder; lantern is at (0.30,0.47). sc12/13/16 positions ok.
   Note: diya glow is frame-anchored, so in close-ups it does not follow the lantern (soft wash, acceptable).
- Long close-ups (contact sheet review/r1_long_crops.jpg): every speaker shot shows the speaker. Short crops
  (shorts/.../review/r1_short_crops.jpg): faces inside 3-85%, figure never shows a face.

## D Thumbnail / cover
- long_03_thumbnail.png 1280x720 1.07 MB; text 13.2% / 16.9% height, matras ok (छ, भू), no spoiler (figure from
  behind), BR corner clear (logo bottom-left), 160x90 readable.
- MINOR: thumbnail text "छत पर भूत?" is word-for-word inside the title "आधी रात छत पर भूत? ..." (RULES 6). Free fix:
  re-render text only (raw art cached), e.g. "सफ़ेद साया!" / "कौन है वहाँ?".
- Cover 1080x1920: label measured 14.3-17.1% (top < 15%) -> label_y 0.162 -> ~0.172; title 19.6-30.2% ok; matras ok;
  figure faceless/hooded, no Mishra face. MINOR: Golu's face at 80-90% height (channel layout: no faces in 82-100%).
- Register: add rows for long_03_thumbnail.png and the cover.

## E Cost
story_budget.py: ₹83.79 + GST ₹15.08 = ₹98.88 <= ₹110. 16 paid images (sheet + 13 scenes + thumb + cover), all 1K,
0 regenerations, ≤16 new scene images. Per-call estimated_inr sums to ₹65.03 (actual +29% excl. GST); plan estimate
~₹101 held. Final build needs no paid call (all TTS cached).
