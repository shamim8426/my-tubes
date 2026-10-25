# 001_al-fatiha — Munshi R2: images 06/08/24 + TTS bookkeeping (2026-10-25)

VERDICT: PASS-WITH-NOTES (0 BLOCKER, 0 MAJOR; notes go to carry_over.md). Review cost ₹0. No STOP condition: no copyright doubt, channel ID not touched, no paid call.

## 1. images/06_makka_night_houses.png (regenerated, 1376x768, line 18, shan-e-nuzul Makka)
Old file is in `_to_delete/noor_001_old_images/`. images.json no longer has a "rect" for 06, so the whole image can be on screen. I checked all of it.
Zoom crops (brightened 2.2x) in `r2_crops/`: 06_stairs_left, 06_stairs_mid, 06_alley_mid, 06_zoom_blob, 06_lit_window, 06_lit_house_leftwall, 06_stairs_bottom_right, 06_right_house, 06_left_door, 06_left_upper_house, 06_roofs_left/mid/right, 06_hill_right, 06_lane_bottom.
- All stairs (left, middle, far alley, bottom right) are empty. All doors are closed or empty dark openings. The windows are empty apart from the one lamp. Roof edges, alley and dark corners: no person, figure, silhouette, shadow-figure or animal.
- The small dark blob in the alley (x~630, y~530, about 5 px) is a pebble with a pale patch (06_zoom_blob.jpg). It is not a figure.
- No dome, no minaret, no Ka'ba, no text or letters. The hills are black-brown rock, which matches the Hijaz.
- Note: the window lamp is diya-shaped again (same as R1 note 5). Taste only, so it goes to carry_over.
Result: clean. The R1 BLOCKER is closed.

## 2. images/08_predawn_houses.png (regenerated, 1376x768, line 22)
Crops: 08_doorway, 08_zoom_doorway_in, 08_zoom_doorway_contrast, 08_zoom_left_of_door, 08_house_left, 08_house_right, 08_zoom_white_shape, 08_context_3x, 08_palms_mid, 08_zoom_dot_far, 08_zoom_dot_contrast, 08_far_valley, 08_hills_top, 08_left_rocks, 08_right_rocks, 08_foreground.
- Hijaz look: yes. The hills are dark black-brown, jagged and granite-like. The wadi floor is dry sand with scattered stones. There are date palms, flat-roofed mud-brick houses with wooden rain spouts, and dry grass bushes. There is no cactus, no red sandstone, no mesa or flat-topped cliff, and no ladders. It no longer reads as an American desert.
- No dome, minaret, Ka'ba or text.
- Checked shapes, none of them a figure:
  - Inside the open door (x~560-590, y~515-545) there is a lighter grey wedge. It reads as the door leaf or interior wall. It starts at mid-door height and has no head or shoulders.
  - Next to the house corner, right of the door (x~675-700, y~510-560), there is a pale plaster pillar/buttress with a rounded knob on top. At 3x without brightening (08_context_3x.jpg) it reads as part of the wall and its stepped base. It is NOT a figure, but it is the one spot a viewer could read as a person in white. Free fallback if the user sees a figure: images.json "rect" {fx 0.249, fy 0.5, zc 2.2} → window x 35-655, y 210-559. The house front, the door, the lantern and the palm stay in view; the pillar is out. Do not use delogo.
  - Distant dark dot near the middle palm (x 830-851, y 470-482; the dark core is about 4x3 px): a stone or shrub, not a figure or animal.
  - The lantern by the door is the same kind as in 01/07 (accepted in R1).
Result: clean, and it reads as the Hijaz.

## 3. images/24_crescent_night_valley.png: rect window vs tent
images.json: "rect" {fx 1.0, fy 0.4, zc 1.8}. noor_render.shots_for uses this rect for every shot of this image. noor_render.source() crops shot_rect(1376, 768, 16/9, 0.5, 0.5, 1.0, 0.4, 1.8) FIRST and only then resizes and warps, so the motion can never show pixels outside the crop.
- Computed with tools/parallax.shot_rect: x0 612.1, y0 93.9, w 758.5, h 426.7 → x 0.445-0.996, y 0.122-0.678.
- The tent and fire are at x 0.33-0.36 (454-495 px). They are fully outside the window, with a 117 px margin. Overlay: `r2_crops/24_window_overlay.jpg` (red = window, yellow = tent band).
- Inside the window: the crescent moon, stars, distant hills, the right cliff and bushes. No figure or text.
- Note: the window still shows red rock and mesa landforms (the same American look the user removed from 08). This is an end screen and not a shan-e-nuzul scene, so no rule is broken. Carry_over.

## 4. TTS bookkeeping (R1 item 8)
I read long/lines.json myself: 62 spoken lines, 62/62 tts_ok = true, 62/62 wav present, 62/62 .ok present.
- Lines 4, 56, 58, 64, 67, 83: "user_accepted": "2026-10-25", and the .ok text reads "user accepted 2026-10-25 (listened: 'sab theek hain, waise hi rakho')".
- Lines 69, 81, 86: the .ok files hold the current Whisper text.
- A rerun of the tts stage now keeps every take, so it no longer deletes wavs.
- MINOR: long/review/tts_report.md is still the old one (12:50, "Whisper OK 53/62", lists 4/56/58/64/67 as missing). It is only bookkeeping, so it goes to carry_over.

## Carry-over (channels/noor-e-raah/carry_over.md)
tts_report refresh; the 08 pillar with its free rect fallback; the 24 mesa look; the diya-shaped lamp.

## Next
Images + TTS are done for R2. The builder moves to the next stage (mix/render as per RULES 15).
