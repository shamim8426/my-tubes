# Munshi review — Kissago Painted style test (R1, 2026-10-20)

STEP: style migration test (not a production step, no upload)   PROJECT: style_migration   VERDICT: PASS (with notes, no BLOCKER)

## Kya check kiya
- shared/RULES.md 11, 12, 12a; brand/STYLE_PAINTED.md; channel_bible.md section 2.
- Sheets: dadi/golu/mitthu `sheet_painted.png` (1264x848) vs old `*_sheet.png`, via sheets_compare.png.
  Old sheets: `git diff HEAD` clean for dadi_sheet.png, golu_sheet.png, mitthu_sheet.png (unchanged).
- Scenes: scene_A.png, scene_B.png (1376x768, 1K) full view + full-res crops (faces, Mitthu, corners, stray marks).
- Prompts: scripts/gen_painted.py (SHEET, SHEETS, SCENES) + style block (STYLE_PAINTED.md section 1) + scripts/gemini_image.py diff (only a `style=` override, no names).
- Name grep: tools/name_guard.py (hashed block list of studio/film/anime/artist names, plus "in the style of") over *.py/md/json/jsonl/csv/txt + file/folder names.
- Parallax: report.json (guard), compare.mp4 (1920x540, 12 s), new_A/B_parallax_forced.mp4 (1920x1080, 30 fps, 6 s): first vs last frame, 2x crops of Dadi hair/bun/pallu, Golu hair vs field, Mitthu feathers/tail, lantern, frame borders.
- Cost: `story_budget.py style_migration` + cost_log.csv rows.

## Findings
1. Sheets — identity kept. Dadi: round face, white bun, round golden specs, red bindi, light green saree + yellow border, gold bangles, wooden stick. Golu: messy black hair, yellow T-shirt, blue half-pants, white socks, red shoes. Mitthu: green, red beak, red neck ring, wings + feet only, NO hands in all 6 poses. No labels/text on the new sheets.
   - MINOR: Mitthu painted sheet adds a black throat/chin band above the red ring (real ring-neck look), clearest in the 3 bust views; old sheet has only a thin red ring. Bible only says "hara tota, laal choonch", so not a bible break, but it will propagate as the reference. Free way out: add "only a thin red neck ring, no black band" to Mitthu's scene prompts from story 005. Regen of the sheet only if the user wants it (~₹5.5, would nearly use up the ₹35 cap).
2. Scenes — A (evening aangan): mud house, khaprail roof, brown wooden door, tulsi pot, charpai, gulmohar, fields; Dadi/Golu/Mitthu match painted sheets; Mitthu on branch, feet only. B (night chhat): flat roofs, water tanks, clotheslines, lantern, steel jug, chatai; faces clearly readable (lantern + moon rim); Golu's red shoes kept beside the mat, white socks on. No text/logos/watermark in either (a tiny mark right of Dadi's pallu in B is a wall pipe fitting, not text).
   - Note: Dadi has no stick in A/B (sitting, fine). Saree in B is a deeper green than "halki hari" (night light) — Note only.
3. Copyright/lookalike — "Kya ye kisi jaane-maane kirdaar ya scene ki nakal lagti hai?"
   - dadi sheet: Nahi. golu sheet: Nahi. mitthu sheet: Nahi (realistic Indian ring-neck parakeet). scene_A: Nahi (Indian mud house + gulmohar; no block-list element). scene_B: Nahi (Indian rooftop at night; no creature, bus, castle, broom, spirit).
   - Prompts and style block: zero studio/film/artist names, no "in the style of". Grep hits only in shared/RULES.md section 10 (rule text giving forbidden examples), _to_delete/, a Whisper tokenizer vocab, and .specstory chat history (private repo) — none are prompts, file names or metadata. No file/folder name contains such a name.
   - Note: style block uses the generic word "2D anime illustration" (a medium, not a name; allowed by 12a). Optional extra distance: "2D painted illustration" in a future edit.
4. Parallax — guard put both painted scenes on zoom (jump 0.27 / 0.33; old Long 03 scene_16 also fell back at 0.20). Forced half-motion clips at full res: no halo, no edge smear, no stretched pixels at Dadi's hair/bun/spectacles, Golu's hair vs field, Mitthu's feathers/tail/feet, lantern glass/handle, or frame borders. Painted textures (soft washes) hide depth seams well. Recommendation: painted images are parallax-safe; keep the guard as the default anyway (it is cheap insurance); do not force full-amp parallax without a test.
5. Cost — style_migration: ₹23.61 + GST ₹4.25 = ₹27.86 actual (6 calls: 3 sheets ₹4.37–4.66, 2 scenes ₹5.01/4.98, 1 TTS cap check ₹0.03), cap ₹35, left ₹7.14. No regeneration. Per-image cost (~₹5 + GST) is the same as story 004, so the ₹100–110 story budget is unaffected. Ledger balance ₹302.78 (> ₹50). No STOP condition.

## Recommendation
Approve "Kissago Painted" for story 005. Before 005: either accept Mitthu's black throat band, or add the "no black band" line to his prompts (free). Old sheets and story 004 untouched.

## R2 — Mitthu painted sheet v2 (2026-10-20, Munshi)
Verdict: PASS-WITH-NOTES (v2 is the final sheet; no regeneration left: style_migration ₹33.29 of ₹35, 1 regen used)
- Checked at full res (1264x848) + 3x neck zooms of all 6 poses, v2 vs v1 (review/mitthu_neck_v2.jpg, review/mitthu_neck_v1.jpg) and old flat mitthu_sheet.png.
- (1) Black band: STILL THERE, in all 6 poses — a dark green-black chin/throat patch between the beak and the red ring (wedge-shaped, widest under the beak). It is not the inside of the mouth: in pose 4 (open beak) the mouth inside is brown-pink with a tongue, and the dark patch sits separately below it. v2's patch is a bit softer/greener and smaller than v1's (v1 is nearer pure black, wider in poses 1, 4, 5), so v2 is slightly better than v1, but the prompt line did not remove it. (It matches a real Indian ringneck's black chin stripe, which is why the model keeps adding it.)
- (2) Identity: OK — green body, red hooked beak, thin red neck ring, wings and orange feet only, no hands/fingers, no text/labels. Same bird as the old flat sheet apart from the chin patch.
- (3) Lookalike: "Kya ye kisi jaane-maane kirdaar ki nakal lagti hai?" — Nahi. A generic storybook ringneck parakeet.
- MINOR (not a BLOCKER): the chin patch differs from the bible look (old sheet has no black). Ways out (free): (a) in story 005 scene prompts add for Mitthu: "only a thin red ring around his neck; throat and chin plain green, no black patch"; since the sheet is the reference, the patch may still come through, so (b) the builder can, for free, paint the chin patch green locally on a copy of the sheet used as the ref (no API call); then check Mitthu's throat in story 005 image review.
