# 005_an-nas IMAGES review (R1)

Checked: images.json (28 clips), all 18 files in images\, crops computed with tools/parallax.shot_rect and viewed on long\review\images_sheet.jpg, the two new images opened in full, script '## IMAGES' plan, cost_log rows, name_guard.

## Checks
- No person / figure / face / hand / text / dome / minaret / Ka'ba in any base image or crop: OK. Vasvasa / shaitan / jinn never shown (only dark, lamp, door, path, window): OK.
- Reuse sources: all 14 base files exist in images\ (copies of 001-003 images, own AI images already used in earlier approved videos). No (image, rect) repeated: OK.
- 12_bedtime_room_lamp (carry_over 002 chimney lamp at x~390 of 1376): rect P (fx .75, fy .5, zc 1.55) = x 484-1365, lamp out of frame; P_b (fx .65, fy .25, zc 1.8) = x 508-1266, y 0-427, lamp (y 470-600) out of frame. OK.
- New images: 11_shuttered_window_night.png and 12_dawn_hijaz_valley_lamp.png are our own Cloudflare (cf-flux-2-klein-4b) images, 1920x1088, cost_log rows 1051-1053 exist at Rs 0 (free). Own AI images, no licence-register row needed. name_guard on images.json prompts: OK. 0 paid images, Rs 0, within budget.
- Shot vs lines: line 3-6 night/star/lamp/path, ayah 1 stars, lines 10-12 Makka-like valley (no gumbad/minar), 114:1-3 lamp/door/lamp, 114:4 window (shuttered window = vasvasa 'hidden', no figure), 114:5 fading path, 114:6 dawn ridge, hadith bedtime room, seekh empty room morning, ant dawn valley with lamp. Matches.

## BLOCKER
None.

## MINOR (go to carry_over.md, no regeneration)
1. First minute: line 4 (USTAAD, ~21 words, est. ~10-10.5 s) runs on ONE clip 01_one_star_night_b; the plan had two crops (9-14 / 14-20 s). Slightly over the ~8 s rule. images.json can only split on line starts, so no free split; accepted, or builder adds a second A crop only if the sync tool supports sub-line starts.
2. 11_shuttered_window_night: shutters are half open (not 'tightly shut') and the 'lamp' on the sill reads like a small clay pot/vase; brick-block walls instead of mud-brick; 1920x1088 render is slightly cleaner/CG than the matte family. Accepted (nothing forbidden).
3. 12_dawn_hijaz_valley_lamp: flatter illustrated style, rocks have faint reddish tint; no red sandstone mass, no snow/pine. Accepted.
4. Reused: 18_lamp_toward_light has a small metal-and-glass lantern on a post (STYLE_NOOR 'never modern lantern'; accepted in 001); 23_golden_valley_full_light has tan sandstone cliffs (mesa-like, accepted in 001); 06_makka_night_houses tiny glowing windows (accepted).
5. 07_moonlit_rooftops_lamp and 09_morning_palm_path are copied in images\ but unused (plan swapped them for the two new images). Harmless.

## Changes made
None (no images.json edit needed).

VERDICT: PASS
