# नूर-ए-राह — style guide

Rules live in `channels/noor-e-raah/RULES.md` (sections 1c, 2, 2a); this file records the look and where its parts are.

## 1. Image style
- **001 Al-Fatiha:** style a "cinematic painted" (block: `scripts/noor_look_test.py` STYLES["a_cinematic_painted"]);
  landscapes, lamps and places only, no people.
- **From 002 (Al-Baqarah 1-5):** "immersive" andaaz (RULES 2a). Style to be confirmed by the user from the tests:
  - `samples/immersive_test/` — cinematic watercolor (4 scenes)
  - `samples/musafir_test/` — Musafir v1, V1 cinematic painted vs V2 cinematic matte
  - `samples/musafir_v2/`, `samples/musafir_v3/` — V2 cinematic matte (film still, painterly, god rays, depth of field,
    warm golden grade; block in `scripts/noor_musafir_v3.py` STYLE)
- Never: a studio/film/artist name in a prompt (name_guard), AI-drawn letters, domes/minarets in old-era scenes, a
  modern lantern (use an old clay oil lamp), red sandstone/mesa landscapes for the Hijaz (use black-brown granite hills,
  dry wadis).

## 2. People
- HARD RULE (RULES 2a, user 2026-10-26): people only as close details — hands, feet, holding/giving/picking up (like the demo's open hand); no full figures or faces acting a scene, AI or stock. Never any Prophet, Sahabi, angel or named person in any form. Musafir and worship scenes only from behind/far.
- Never any Prophet, the Prophet ﷺ, his family, a Sahabi, an angel or a person named in the Quran — only places and symbols.
- Worship (dua, namaz, sajda) only from far/behind with the correct posture. Dua: elbows close to the body, hands in
  front of the chest below the chin, palms up toward the face, head bowed straight down (not turned).

## 3. Musafir (permanent character, final v3, Munshi R2 PASS 2026-10-25)
- Slim young man 18-20, clean-shaven, short dark hair, beige/khaki plain kurta-pajama, small cloth shoulder bag, bare
  head or small plain cap, sandals. No white robe + white head cloth, no turban, no beard.
- **Only from behind** (directly or max ~20° off, head turned away); never three-quarter / lost profile / side profile.
- References: `characters/musafir/sheet_v3.png` (standing, sitting, dua — all from behind) and, for scene prompts,
  only `characters/musafir/ref_back_dua.png`. Prompt text: `scripts/noor_musafir_v3.py` LOOK / NOFACE / DUA.
- Script and captions never hint that he is any special or named person: he is "एक मुसाफ़िर".

## 4. Text and sound
- Arabic: Amiri through libass/ASS only (Tanzil text byte-for-byte; ffmpeg drawtext puts the harakat off their
  letters). In libass Amiri draws ~4.35x smaller than its size number (AMIRI_ASS_K in scripts/noor_render.py).
  Hindi: Mukta through libass/ASS only (drawtext drops the nuqta of क़ु). Subtitles: Ustaad white, Sawaal soft gold.
- Music continuous through the video (Soaring / Quietude / River Flute), ~19 LU under the voice; a soft swoosh as each
  ayah comes in; ambience by mood (RULES 1c).
- Camera moves: eased, sub-pixel (tools/parallax.py), zoom 1.00→1.07 or ~4% pan, one move per 6-8 s.

## 5. Thumbnail (v3, 2026-10-30; `scripts/noor_thumb_v3.py`)
- Arabic surah name: Aref Ruqaa Bold (calligraphy, OFL), drawn with Pillow + libraqm (HarfBuzz) as gold with glow; NOT by
  libass because this ffmpeg's libass cannot shape Aref Ruqaa (tofu boxes). Never ffmpeg drawtext, never AI-drawn letters.
  Video text stays libass + Amiri (section 4). `--arabic amiri` = the old libass path. The Arabic string comes from
  `surah_titles.json` / Tanzil names and is checked by Munshi (thumbnail stage).
- Hindi name + hook line + chip: libass (Mukta ExtraBold). Hook = one short, true, respectful line; "*word*" in yellow.
  No fear, no false promise, no "ban/halal/haram" claims, no person image. YouTube's time stamp covers the bottom-right.
- Three layouts (A left column, B centred, C hook-first); Nigraan compares CTR later (learnings.md).
