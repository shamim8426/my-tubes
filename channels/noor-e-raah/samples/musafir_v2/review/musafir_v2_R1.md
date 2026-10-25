# Musafir v2 — Munshi R1 (images) — 2026-10-25

Files: samples/musafir_v2/musafir_v2_sheet.png, 1_dua_sunrise__V2.png, 2_two_paths__V2.png (all 1376x768, 1K).
Prompts: scripts/noor_musafir_v2.py. Rules: channels/noor-e-raah/RULES.md 2a (Musafir v2). Cost of review: Rs 0.
Zoom crops (4x, face edges 8x) in this folder (JPG).

| Image | Face | Beard | Clothes v2 | Fingers | Dua posture | Verdict |
|---|---|---|---|---|---|---|
| Sheet fig1 (back) | none | none | ok | both hands curled, fingers merged, no extras | - | ok |
| Sheet fig2 (lost profile) | eyelashes, brow, nose tip and lip edge readable (near side profile) | none | ok | R hand curled, ~4 visible, no extras | - | BLOCKER |
| Sheet fig3 (sitting) | eyelash/brow tip sticks out past the cheek line (small, 8x) | none | ok | hands hidden | - | BLOCKER (strict "eyes never") |
| Sheet fig4 (dua, back) | none | none | ok | hands hidden by body | elbows close, forearms forward, head bowed: correct | ok |
| 1_dua_sunrise | none (back of head only) | none | ok, bag, sandals | hands hidden | elbows close, hands in front, nothing beside head; head bow slight/barely readable | PASS (note) |
| 2_two_paths | nose tip + eyelash tip past the cheek line, chin/lip edge | none | ok | R hand curled, fingers merged, no extras; L hidden by bag | - | BLOCKER |

Consistency: same young slim man, knee-length off-white kurta, loose pajama, cross-body bag, sandals, same wrapped
head cloth in all three: consistent. Ordinary traveller: yes, young villager look; no robe/cloak, no beard.
Notes (MINOR/taste): head cloth is a neat wrapped turban-cap (small, not grand) — allowed, but all-white kurta + white
wrap leans slightly "pious figure"; a faded earth-tone kurta or bare head would read more "ordinary". Hands everywhere
are curled with merged fingers (no extra fingers) — acceptable at this size.
No domes, minarets, text, other people.

Finding: the "lost profile" view leaked face features in 3/3 attempts (sheet fig2, fig3, scene 2) after v1 also
failed. The model cannot hold a lost profile; use back views only.

Prompt fixes (exact wording) — see report to builder. Free way out: use only sheet fig1 + fig4 (crop) as reference.
Verdict: ASK (regeneration = paid; user decides). No STOP condition.
