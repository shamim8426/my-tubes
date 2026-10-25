# 001_al-fatiha — Munshi R1: scene images + TTS audio (2026-10-25)

VERDICT: FIX (1 BLOCKER, free fix; 1 MINOR, free) — cost of review ₹0. No STOP condition (balance ledger ₹366.64 > ₹50; no copyright doubt; channel ID not touched).

## 1. Images (23 files, all 1376x768, no duplicates)
Opened every image with Read + zoom crops of every lamp/door/dark corner (`review/r1_crops/*.jpg`).
No text/letters, no Ka'ba/dome/minaret, no angel shape, nothing resembling a known film/franchise scene, nothing disrespectful.

| # | Image | Finding | Severity | Fix | Cost |
|---|---|---|---|---|---|
| 1 | 06_makka_night_houses.png (line 18, shan-e-nuzul Makka) | A small hooded, seated human-like figure next to the stairs, about x 790-835, y 525-605 (crop `r1_crops/06_stairs.jpg`). RULES 2: no person/silhouette, especially in a shan-e-nuzul scene. | BLOCKER | Free: use the crop x 0-770, y 230-663 (16:9) scaled to 1920x1080. It keeps the lit window and the houses, the figure is out (test `r1_crops/06_test_cropleft.jpg`). Make it a new file, e.g. `images/06_makka_night_houses_crop.png`, and point images.json at it. Check that parallax/pan never brings x>770 into view. Do not use delogo (`06_test_delogo_zoom.jpg` leaves a smear). Paid option: one regeneration (~₹3.26 + GST), only if the user wants it. | ₹0 |
| 2 | 08_predawn_houses.png | Ladders, flat mesas: reads more like a Southwest-US pueblo than the Hijaz. Not a rule breach. | Note | Optional: none needed. Next prompts: "no ladders, no mesa/butte landforms". | ₹0 |
| 3 | 21_straight_desert_path.png (ayah 6) | The path looks like a paved road with kerbs (the modern-road worry). The "no pakki sadak" rule only covers the shan-e-nuzul Makka scenes. This one is the ayah-6 metaphor, so no breach. | Note | Keep, or use 22 for ayah 6 as well (22 has faint tyre tracks, also a little modern). | ₹0 |
| 4 | 24_crescent_night_valley.png | The "distant lamp" is a modern A-frame camping tent with a lamp. Mesas/buttes again. No figure (zoom `24_tent.jpg`). | Note | Keep (end screen, tiny), or crop the left edge. | ₹0 |
| 5 | 03 / 05 / 09 lamps | Indian-diya-shaped clay lamps. Viewers may connect a row of diyas (03) with a festival look. Taste only. | Note | User's taste call; for next videos write "spouted Arabian clay oil lamp". | ₹0 |
| 6 | 12_worlds_panorama.png | The SCREEN note and prompt ask for a distant bird flock; there are no birds. Sea, mountains, Milky Way and fields are all there. | Note | none | ₹0 |
| 7 | 19_tea_medicine_window.png | Prompt says morning, image is dusk with an oil lamp. Pine trees outside. The window reflections are the lamp and cup, no figure (zoom `19_window.jpg`). The MISAAL is modern, so this is fine. | Note | none | ₹0 |

Checked and clean: 01 (lantern), 02, 04, 05 (dark doorway, not a figure: `05_door.jpg`), 07 (lantern), 10, 11 (open door is empty: `11_door.jpg`), 13, 14, 15, 16 (lantern post, not a figure: `16_post.jpg`), 17, 18, 22, 23.
SCREEN notes vs images.json start lines: match (Makka valley/houses/night/pre-dawn for shan-e-nuzul; ayah images per the cues; 17 at line 57, 19 at MISAAL line 67).
Cost: 19 new images x ₹3.26 = ₹61.94 + GST (1K). Story so far ₹90.85 + GST ₹16.35 = ₹107.20 (cap ₹150).

## 2. Audio (TTS)
- lines.json: 62 spoken lines (45 USTAAD, 17 SAWAAL), each has audio, seconds and tts_ok. All 62 wavs are present, 24 kHz mono PCM. Total 446.2 s. The lines.json seconds match the wav lengths (all within 0.05 s). ffprobe on 004, 081, 095: OK.
- Voices: noor_build.py takes the voice from channel.json (ustaad=Algieba, sawaal=Sulafat). Median pitch per line: all 45 USTAAD lines 88-178 Hz (male), all 17 SAWAAL lines 197-296 Hz (female). No mix-up.
- Pace 1.6-3.1 w/s. Line 11 is 1.18 w/s (Arabic name 'अस-सब्उल-मसानी', fine). Peaks -0.9 to -5.7 dBFS, no clipping. Lead/trail silence ≤0.51 s, no internal gap >1.2 s.
- No tilawat: no spoken line contains ayah text (grep), and the Whisper transcripts are Hindi only. Line 8 says the word 'बिस्मिल्लाह' inside a sentence, which is not recitation.
- User-accepted lines 4, 56, 58, 64, 67, 83 (user 2026-10-25 "sab theek hain, waise hi rakho"): accepted, not flagged.

| # | Item | Finding | Severity | Fix | Cost |
|---|---|---|---|---|---|
| 8 | lines.json / audio/tts/*.ok / tts_report.md | 9 lines still have tts_ok=false: the 6 accepted ones plus 69, 81, 86. I re-ran Whisper small with the current matcher (noor_audition.missing). 69, 81 and 86 now PASS (no word missing); 56 and 67 also pass. The flags and tts_report.md are stale. Risk: `noor_build.py tts` on a line without .ok deletes the wav and regenerates it (paid), so a re-run would throw away the 6 accepted takes. | MINOR | Free: write .ok for 69, 81, 86 (current Whisper text). Record the user acceptance for 4, 56, 58, 64, 67, 83, e.g. a .ok holding "user accepted 2026-10-25" or a `user_accepted` field. Set tts_ok=true and refresh tts_report.md. Never re-run the tts stage before this. | ₹0 |
| 9 | 81, 86 | Whisper heard 'भटग'/'बदख' (भटक) and 'हुस्सा' (ग़ुस्सा). The matcher passes, and this is probably Whisper missing the nuqta. | Note | Optional 20-s listen; no action needed. | ₹0 |

## 3. Licences (shared/assets_license.csv)
All present: Soaring, River Flute (Kevin MacLeod, CC BY 4.0), Quietude Sections Merged (The Imperfectionist, CC BY 4.0), 4 Freesound CC0 ambience files (desert wind, night wind+crickets, wind+birds, gentle breeze), Amiri-Regular.ttf (OFL, row 154), Mukta-Bold.ttf (OFL, row 52; noor_render.py uses "Mukta Bold"), Tanzil Arabic text (CC BY 3.0, row 140). No unregistered asset is referenced in noor_render.py.

## Next
Builder: apply fix 1 (crop for 06) and fix 8 (.ok / acceptance bookkeeping), then R2 checks only those two.
