# edit_notes (Sampadak) - Noor 002 Ayatul Kursi, long
Plan: {"grade": "soft_glow", "vignette": 0.10, "grain": 1.5} (EDIT_STYLE section 2; look only, nothing else used by noor_render).
- Length 5:32.3, 34 lines, 11 ayat, 51 shots (4.5-7.9 s). Edit does not change timing.
- Vignette 0.10 (not 0.12): many scenes are already dark (01 night dunes, 02 lamp, 07 rooftops, 09 door, 12 bedroom);
  corners must not turn muddy. Grain 1.5 kept; fine grain helps the flat sky/dune gradients (01, 05, 10).
- Too dark/flat: 01, 02, 05, 07 are dark but intentional (night mood); 10 ring-in-desert is flat. Not fixable by a look, left plain.
- Saturation: 06_oasis, 08_vast_panorama, 11_sunrays are richer than the matte set (Munshi). A saturation tweak is not
  available in the allowed grade set; soft_glow only adds slight warmth. Cannot be fixed here; image regen is a Sanchalak/user call.
- Retention (learnings.md): Al-Fatiha drops at 14-19 s and 33-38 s come from script pacing and the 2:20 first ayah;
  a colour look cannot fix them. Script/shot order is the lever (first ayah within 30-40 s, image change every 8-10 s in the first minute).
- Frames checked in 40 s test (review/edit_frame_10s/25s/38s.jpg): 10 s title card fine, Arabic + Hindi readable, image not muddy.
  25 s Madina dawn, label/info boxes readable, colours natural.
- PROBLEM at 38 s (not caused by the look): full ayah of 4 Arabic lines fills the frame and the 4th line runs into the bottom
  Hindi subtitle box; two Hindi lines also overlap (garbled text). Builder/text layout issue (ayah too long for the frame or
  subtitle overlap at the line change), needs a fix in noor_render/_text.ass or line split before final.
- Deliberately not added: transitions, punch-in, SFX, text (EDIT_STYLE 3-5).
- 2026-10-30 (Sanchalak): the 38 s overlap was a builder layout bug (50-word ayah, libass line spacing); fixed in scripts/noor_render.py (ayah_lines: manual wrap, measured geometry, BASIC measuring like the PC); Al-Fatiha ASS output identical; checked on still frames of ayat 1, 2, 6, 9.
