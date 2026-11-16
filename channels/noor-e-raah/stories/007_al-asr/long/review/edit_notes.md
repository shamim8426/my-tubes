# edit_notes 007 Al-Asr (long) - Sampadak

- Plan: same as 006 Al-Kausar: `{"grade":"soft_glow","vignette":0.10,"grain":1.5}` (EDIT_STYLE s2: range vignette 0-0.18, grain 0-2.0).
- Only colour look. noor_render.py applies it to the picture BEFORE libass, so Arabic/Hindi text, cards and end card stay untouched.
- No transitions (builder crossfade XF 0.5 only), no punch-in, shake, whip, SFX, ambience, text: EDIT_STYLE s3-s6.
- Beats left plain on purpose: ayah lines, SCREEN cards (line 4 intro, 47-49 takeaways), end card (from line 50). Retention fixes belong in the script, not effects.
- Vignette 0.10 (not 0.12) so the edges stay gentle behind the Arabic; same as 006.
- No frames extracted / no preview render (timeline not built yet; lines.json has 84 entries, no images in output yet). Length/timing unchanged: plan never moves lines.
- User decision: none.
