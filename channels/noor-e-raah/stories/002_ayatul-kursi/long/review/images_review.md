# 002 images review (Munshi) - VERDICT: FIX (1 BLOCKER-by-style-guide, free fix; rest MINOR)
Checked: all 12 PNGs opened one by one + images.json crops (computed against 1376x768).
Clean on all 12: no person/figure/silhouette/hands, no Prophet/Sahabi/angel hint, no throne, no letters/writing/signs, no domes/minarets, no studio/artist look-alike, no red mesa.
1. BLOCKER (STYLE_NOOR s1 "never a modern lantern"): 12_bedtime_room_lamp - the lamp is a glass-chimney kerosene lamp, not an old clay oil lamp. Free fix: do not use as-is; reuse 02_lamp_on_stone crop (or 05/03 crop) for line 59 with empty-room feel, or crop/zoom 12 on bed+window (x 330-1150, y 0-560) so the lamp is out of frame (lamp at x~390,y~530; a crop starting x>=480 drops it). Bed, pillow, window, no person otherwise right.
2. MINOR: 04_date_palm_path - tiny metal wall lantern glowing at ~(912,450). Small, mid-ground; accept (carry_over) or the reuse 04_b crop (fx .5 fy .55 zc 1.2 = x 115-1260) still contains it; ok to leave.
3. MINOR: style consistency - 06_oasis_spring, 11_sunrays_clouds, 08_vast_panorama, 04 are more saturated/illustrated than 01/02/05/07/10 (more matte). Same painted family, acceptable; 06 (very saturated) is the outlier. No regen.
4. MINOR: 08 (snow peaks, green sea coast) and 11 (pines, snow mountains) are not Arabian; used only as "heavens and earth / vastness" ayah images, no place claim. Accept.
5. (d) script match OK: 10_ring_in_desert shows one small clear metal ring in the lower middle (688,595) - good for K3 misaal; 09 lit door plain panels, no letters; 07 single lit window; 03 empty lane; 01/05 calm upper area.
6. (e) subtitle band: lower 15% quiet on 01,02,05,07,08,09,10,11; busy-ish but ok on 03,04,06,12 (ground/foliage texture, nothing important). 
7. (f) crops: all rects sensible. 10_b (fx .5 fy .68 zc 1.7): crop y 296-748, ring lands at ~66% height, ~40 px wide, visible and above the band; nicer if fy=.72. 02_b (zc1.5): flame+lamp inside. 05_c, 01_b/c, 04_b, 08_b, 03_b, 05_b fine.
Cost note: none checked here (images stage log says est Rs 55-60).
