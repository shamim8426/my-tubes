# Musafir v3 — Munshi R1 (images) — 2026-10-25

Files: samples/musafir_v3/musafir_v3_sheet.png, 2_two_paths__V2.png (both 1376x768, 1K); ref crop
musafir_v3_ref_back_dua.png (sheet fig1 + fig3); compare_musafir_v3.jpg. Prompts: scripts/noor_musafir_v3.py.
User rule v3: beige/khaki plain kurta-pajama, shoulder bag, small plain cap or bare head; only from directly behind
(max ~20 deg, head turned away), no face feature past the head/cheek outline; dua = elbows close, hands in front of chest
below chin, palms up, head bowed. Review cost Rs 0, no regeneration.
Zoom crops (JPG, this folder): sheet_fig1_head_8x, sheet_fig1_hands_4x, sheet_fig2_head_8x, sheet_fig2_hands_4x,
sheet_fig3_head_8x, sheet_fig3_faceedge_16x, sheet_fig3_hands_4x, sheet_fig3_body_2x, s2_head_8x, s2_handL_8x,
s2_handR_8x, s2_body_2x, s2_body_4x.

| Image | Face | Clothes v3 | Fingers | Dua posture | Verdict |
|---|---|---|---|---|---|
| Sheet fig1 (standing) | none: back of head, both ears | beige kurta-pajama, grey-olive bag, bare head, sandals | both hands curled at sides, fingers merged, no extras | - | ok |
| Sheet fig2 (sitting) | none: back of head, both ears | ok | hands hidden (resting forward) | - | ok |
| Sheet fig3 (dua) | head turned ~20-25 deg to his left and bowed; at 16x a small dark mark (~3x5 px) sticks out past the cheek line under the temple = eyebrow / eyelash tip; jaw line visible (normal from behind) | ok | hands hidden in front of body | head clearly bowed, elbows close to body, forearms forward, nothing beside the head; hands sit lower (waist / low chest), palms not visible -> can read as "looking at something in his hands" | BLOCKER (strict: feature past the outline); posture otherwise OK |
| 2_two_paths (v3) | none: square back view, both ears, neck, no feature past the outline | ok, same beige, bare head, bag on same side, strap same shoulder | L hand curled, mitten-like merged fingers, no extras; R hand dark, half hidden, no extras | - | PASS (notes) |

Consistency sheet <-> scene 2: same slim young man, short dark hair, same beige knee-length kurta + loose pajama, same
bag and strap side, sandals: consistent. Ordinary young traveller: yes (clean-shaven, bare head, everyday clothes, no
robe/turban/white). No other people, domes, minarets, text, logos.

Notes:
- Scene 2 landscape: red/orange sandstone canyon (Southwest / Petra feel), not Hijaz (black-brown basalt / granite hills,
  sandy wadi). MINOR note; use Hijaz wording if the scene is made for a real story.
- Hands are mitten-like (merged fingers) at this size: MINOR, acceptable.
- Sheet fig3 is the dua reference and its pixels went into musafir_v3_ref_back_dua.png. Scene 2 did not copy the turn,
  but for future scenes use a ref without fig3, or a free retouch of the 3x5 px mark (paint background over it),
  before using it as a dua reference. Strict prompt word: "head bowed straight down, centred on the spine, not turned".
- Kept v2 scene 1 (1_dua_sunrise__V2: white kurta + white cap) now mismatches v3: off-white vs beige and a clearly
  readable white cap vs bare head. Figure is small, but next to scene 2 it reads as another person / the "pious white"
  look the user rejected. Recommend remake to v3 look (paid ~Rs 6, user decision).

Verdict: FIX for sheet fig3 (free: retouch the mark or drop fig3 from refs); scene 2 PASS-WITH-NOTES. No STOP.

## R2 — 2026-10-25 (only the R1 FIX item)

Builder fix: cv2.inpaint (Telea r4) on sheet fig3, mask x 1080-1089 / y 139-155; original in
_to_delete/noor_musafir_v3_orig/musafir_v3_sheet.png; ref crop rebuilt.
Checked: pixel diff fixed sheet vs original = 143 px changed, all inside x 1080-1088 / y 139-154 (fig1 + fig2 + rest of
fig3 byte-identical); musafir_v3_ref_back_dua.png == hstack(fixed sheet left third, right third) exactly;
2_two_paths__V2.png not touched (mtime 17:15, before the fix). Crops: R2_fig3_head_8x.jpg, R2_fig3_faceedge_16x.jpg.
Result: the dark eyebrow/eyelash tip is gone; the cheek outline now runs smooth from temple to jaw, no feature past it.
At 16x the patched spot is a slightly softer skin tone than its surroundings; at 8x and at 1:1 no smudge or blotch is
visible. Posture note from R1 (hands low, palms not visible) stays a note.
Verdict R2: PASS (sheet v3 + ref crop OK as reference; scene 2 PASS-WITH-NOTES unchanged; scene 1 v2 remake still
the user's call, ~Rs 6). Rs 0. No STOP.
