# Carry-over (MINOR issues to fix in pipeline)

| Date | Project | Issue (RULES 13) | Fix | Status |
|---|---|---|---|---|
| 2026-10-18 | long_01 (uploaded, not changed) | Dadi–Golu opening ~12.8 s (max 10 s) | builder warns when lines marked `"part": "intro"` end after 10 s; script template section 0 | fixed in pipeline |
| 2026-10-18 | long_01 (uploaded, not changed) | last spoken line is the moral, not a question to viewers | builder warns if the last spoken line is not a question; script template + step-review Script stage | fixed in pipeline |
| 2026-10-18 | short_01_jadui-kadhai (uploaded, not changed) | burned captions had 60 px side margins (right 15% not kept free) | caption margins 170 px left/right, bottom 480 px (25%) for all Shorts | fixed in pipeline |
| 2026-10-18 | brand banner_v2 (R2 PASS-WITH-NOTES) | logo panel bottom-right corner overlaps back of Mitthu's head (~x1300-1400, y850-930) | background re-cropped (gen_brand.reframe zoom 1.28, ax 0.78): Mitthu now clear of the panel | fixed 2026-10-18 |
| 2026-10-18 | brand banner_v2 (R2 PASS-WITH-NOTES) | mobile safe crop (x507-2053) shows Golu only, Dadi's face cut at right edge | background shifted right (ax 0.78): Dadi now fully outside the mobile crop, Golu fully inside; no cut face | fixed 2026-10-18 |
