# Munshi — 003 long_02 — 2026-10-19

## Scene images R2 (img 09, 13, 18, 26) — PASS
Opened full size + zoom crops (r2_img26_*.jpg, r2_img18_stick.jpg) vs scene_prompts.json, bible, sheets (dadi, golu, pandey, sharma, mitthu; sona; Raju ref = 002 scene_04).
- 13: exactly one Dadi on one charpai (green saree yellow border, bun, round glasses, one stick), Golu running in (yellow tee, blue shorts, red shoes); khaprail tiled roof, brown door, fields. R1 BLOCKER fixed.
- 09: Raju (brown shirt, apron, sooty kettle) + Mitthu flying, beak open, no hands; exactly two customers (young man green shirt, young woman salwar-kameez); no old/bald man. R1 BLOCKER fixed.
- 18: Dadi holds ONE stick, crook end resting on Pandey's open diary (scribbles, no text), other hand empty; Pandey surprised; Sharma + Golu watch at red gate. R1 MINOR fixed.
- 26: Sharma (only once) on roof hugging Sona (golden tabby, white paws, green collar, happy); crowd below: one grey-haired man in blue shirt with full hair, no glasses, not Sharma-like; no white-haired old woman. R1 BLOCKER fixed.
Notes (no action): 09 chai stall has a gas burner, same as the approved Raju ref (not a village kitchen, so channel rule not hit); 26 slim boy in yellow tee in the crowd, not Golu's build/shorts; 26 Mitthu perched in tree (fits).
Regenerations: 1 each (v1 in images/_v1) -> under the 2-regen cap.

## Long thumbnail R1 — FIX (free, minor)
long/output/long_02_thumbnail.png: 1280x720 RGB PNG, 1.22 MB.
- Text "सोना चोरी!" (Mukta via libass): सो, ना, चो, री shaped correctly (zoom r1_thumb_text_zoom.jpg); glyph height ~13% each line; 2 words; yellow/red-orange with thick black outline on dark blurred panel.
- Title "आधी बात, पूरा हंगामा! मिट्ठू ने सब बता दिया | किस्सागो" does not contain the text -> no repeat.
- No cat anywhere (raw art checked too); no spoiler. Hook = line 1 Mitthu "सोना चोरी!" at 0 s -> promise kept (verify at preview).
- Bottom-right 15%x12% (x>1088, y>634): plain lane only (r1_thumb_brcorner.jpg). Logo bottom-left.
- 160x90 (r1_thumb_160x90_x4.jpg): Mitthu face/beak, Sharma panic face and both text lines still recognisable. Focal point = Mitthu.
- Mitthu = sheet (green, red beak, red ring, no hands); Sharma = sheet.
MINOR: no row in shared/assets_license.csv for long_02_thumbnail.png (Gemini art + Mukta OFL + Kissago logo) -> add row (free).
Notes: hard vertical edge at x~567 between blurred panel and art (generated so in raw; style choice); small bald peeker with moustache/yellow shirt at left wall is not Sharma-like (no glasses, dark side hair).
