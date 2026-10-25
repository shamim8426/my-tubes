# Musafir test — Munshi R1 (2026-10-25)

Test, not production. Folder: `channels/noor-e-raah/samples/musafir_test/` (sheet + 3 scenes x 2 styles, all 1376x768).
Prompts: `scripts/noor_musafir_test.py`. Rules: `channels/noor-e-raah/RULES.md` 2a (Musafir). Review cost ₹0, no regeneration.
Zoom crops (4x, JPG q85): `review/<image>__head|hand*.jpg`.

**VERDICT: ASK** (retry = paid test images; 4 of 7 images have a BLOCKER). No STOP condition.

| Image | Face | Hands (fingers) | Posture | Verdict |
|---|---|---|---|---|
| musafir_sheet | fig1/3/4 back: none (fig3 beard edge only). **fig2 side silhouette: nose, lips, beard profile readable** | fig4 L 5 / R 5; fig1 hands at sides, partly hidden; fig2/fig3 hidden | **fig4 "dua": hands beside head, above shoulders, palms facing back = "hands up", not dua** | BLOCKER x2 (fig2 profile, fig4 posture) |
| 1_dua_sunrise V1 painted | none (back, beard edge at right cheek) | L 5 / R 5 | **hands at head height, wide apart, beside head = wrong for dua** | BLOCKER (posture) |
| 1_dua_sunrise V2 matte | none (back) | L 5 / R 5 | **same as V1: hands up beside head, palms backward** | BLOCKER (posture) |
| 2_two_paths V1 painted | **pure side profile silhouette: nose, lips, moustache/beard line clearly readable** (copy of sheet fig2) | R hand in shadow, ~4 curled visible, no anomaly | standing, fine | BLOCKER (face profile) |
| 2_two_paths V2 matte | lost profile from behind: beard + cheek edge only, no eye/nose/lips | R hand relaxed, 4 fingers + thumb hidden, ok | standing, fine | PASS |
| 3_night_stars V1 painted | lost profile: beard edge + faint cheek, no eye/nose/lips | not visible (in robe) | sitting, fine | PASS |
| 3_night_stars V2 matte | lost profile: beard + lit cheek edge, no eye/nose/lips | R hand on knee: **fingers fused, count unreadable** (MINOR); L hand barely visible in dark | sitting, fine | PASS-WITH-NOTES |

Other checks: no domes, minarets, text, logos, modern objects, extra limbs, other people in any image. Lamps (3 V1/V2)
are small clay oil lamps = old era, ok. Man looks generic (no famous resemblance).

Consistency with sheet: good across all 6 — same white wrapped turban, cream long robe, frayed outer cloth, small cloth
bag on a cross strap, leather sandals, short dark beard, same build. Small drift: outer cloth / bag strap side flips in
2 V2 and 3 V1/V2 (MINOR, acceptable). 3 V1: head turned up-right while legs extend left — slightly twisted but plausible.

Note (taste/sensitivity): a robed, bearded, turbaned man in the desert can be read by some viewers as a Prophet/Sahabi
figure. Design is the user's choice (RULES 2a); script/captions must never imply he is a named person.

## Root causes
1. Sheet prompt asks for "(2) side view in deep shadow so the face is a dark silhouette" — the model draws a crisp
   profile outline (nose, lips, beard), and scene 2 V1 copies it from the reference.
2. "both hands raised in dua, seen from the back" — the model reads it as arms up beside the head, palms out.
   The sheet (fig4) then teaches this wrong pose to every dua scene.

## Suggested prompt wording for a retry (wording only)
- Sheet view (2): replace with "standing, seen from behind at a three-quarter angle (lost profile): only the back of
  the cheek and the edge of the beard show; nose, lips and eyes are turned away and not visible. Never a pure side
  profile, never a profile silhouette outline."
- Sheet view (4) and scene 1: "making dua, seen from directly behind: elbows bent and close to the body, both forearms
  raised in front of his chest, hands held together a little apart at chest height (below the chin), palms open and
  facing upward toward his face; from behind, the hands are mostly hidden by his shoulders, only the fingertips may
  show; head slightly bowed. NOT hands beside the head, NOT above the shoulders, NOT palms facing forward, NOT waving."
- Alternative for scene 1: wide shot, figure small in the frame (about 1/6 of the image height), same posture.
- NOFACE add: "Never a side profile of the face; if the head is turned, show only the back of the cheek and the beard
  edge (lost profile), the head cloth shading the face."
- Hands add: "hands relaxed and clearly drawn with five separate fingers, or hidden in the sleeves."
- Scene 2: replace "seen from the side with his face in deep shadow" with "seen from behind at a three-quarter angle
  (lost profile), looking toward the two paths".
- Keep: sheet as reference, LOOK block, clay lamp, no domes/text.

Retry need (estimate only, user decides): sheet + scene 1 (2 styles) + scene 2 V1 = 4 images; or if one style is
chosen, sheet + scene 1 + scene 2 = 3 images.
