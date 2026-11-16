# Munshi final review - 009 asma-khajoor-ki-guthliyan (2026-11-15) - VERDICT: FIX (1 BLOCKER, free fix)

Checked: script.json (28 lines) vs dossier F1-F14, output/video.mp4 (4:04.6, 1920x1080 h264/aac), video.srt (28 cues, match script), loudness (ebur128), images used in lines.

## Facts (R1 FIX items L2, L3, L14, L16, L26 all verified fixed)
- L2 hedged "रहा होगा" (reconstruction). L3 "माना जाता है" hedged (not in dossier, MINOR: generic context). L14 ok (MINOR: "बार-बार" is inference from F5). L16 matches F7 (ikh ikh = camel-sit command). L26 matches F14 (73 AH, ~100, no "days" gap claim).
- L7-9 F1-F3, L11-13 F5-F6, L15-19 F7-F10, L21-22 F11, L23-25 F12-F13: match. No invented dialogue (only Asma's/Zubayr's own hadith words, attributed), no inner thoughts beyond hadith (shame/ghayra = F8). Excluded W items absent. Last line L28 carries src tag (Bukhari 5224, Muslim 2182a, Bukhari 3907).
- No anachronism seen in images. Description (Sources + AI-assisted disclosure + music credits) not yet present: must be added at upload.

## BLOCKER
- L17 image 05_road_camel.png: foreground bearded man with partly visible face (profile) at left = reads as the Prophet/companion in the scene where he meets Asma (RULES 2a). Free fix: swap L17 to 15_road_tracks.png (empty lane) or crop/zoom to the right half (woman from side/back, loaded basket) so the man is out of frame; rebuild that line only + re-mux.

## OK on depiction
- 04_woman_noon (L14): back view, face not visible, distant figures tiny. 02_house_morning (L4, L6): woman seated, face turned away/hidden by scarf; others far/back. 05_head_load_path, 03_horse_stall, 07_night_house, 08_night_town: back/side, no detailed face. 01_market_day: generic vendor, not a Sahabi scene.

## MINOR (carry_over)
- Loudness -16.3 LUFS integrated (target ~-14; LRA 4.1). YouTube will not boost; optional loudnorm to -14 on re-mux.
- 05_head_load_path has haze/glare (style rule says no haze).
- Hadith Arabic not on screen, so no Tanzil/Arabic check needed.
