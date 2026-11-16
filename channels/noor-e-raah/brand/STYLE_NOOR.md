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

## 6. "Imaan Shorts" talking close-up (user 2026-11-09, playlist imaan_short PLdhrP4DE-lC8; RULES 2c)
- Look: cute 3D storybook faces (huge glossy eyes, round cheeks), warm lamp light, face close-ups; characters speak in first person (no narrator); Hindi subtitle box low-middle (above the Shorts UI), ayah Arabic + source at the top via libass.
- Free pipeline in `stories/006_imaan-shorts/short/`: gen_v3.py (CF flux, reference via input_image_0), tts_v3.py, talk.py (audio-driven mouth), build_v3.py. Full-motion route: Kaggle LTX-Video (`kaggle/ltx_full`), prompt must name the motion, guidance 5, 73-81 frames; queue may stall.
- Learnings (tools/learn.py was blocked: main diverged from origin): CF reference image keeps one face; PIL has no Raqm on Windows -> libass; parallax.MAX_SECONDS=20 or video drifts; LTX 97 frames OOM on T4.

## 7. Daily story graphics learned from a reference Short (study 2026-11-13, "myth-busting hadith" Short, 37 s, 9:16; style only, nothing copied)
- Look: warm cinematic 3D-illustration, golden lamp light vs deep indigo night with a crescent moon, cosy lived-in rooms (plants, lantern, tea, mosque-silhouette frame), glowing light on the Quran, abstract dark smoke for the "bad" force (no creature face). Rich, soft, high-contrast; never flat or cartoonish.
- People: characters shown from BEHIND or tiny/far, hijab/long dress, never a face; the "family" feeling (grandmother + girl) carries emotion. Fits RULES 2e.
- Story shape (about 37 s): question hook -> common belief/myth -> short scene with named characters -> "the truth is the opposite" -> the hadith/ayah on screen with source tag -> action line ("open it and recite"). Works for Shorts and as the first 40 s of a Long.
- Cadence: ~16 images in 37 s (one new picture every ~2.3 s), slow push/pull, soft cross-fade; bottom ~35% of the 9:16 frame is a dark gradient where the caption sits; caption = small elegant serif, 1-2 lines, key word in GOLD; hadith/ayah line gets a tiny source tag ("Sahih Muslim 780 · sunnah.com"). Voice calm, mean -19 dB before mastering, soft music under it.
- Our builder support (scripts/history_build.py): per-line `"gold": ["word"]` (keyword highlight) and `"src": "source tag"`; 25% motion shots (parallax) -> later 50% -> 100%; 16:9 Long uses ~5-6 s per shot, Shorts ~2-3 s.
- Hard: never copy their images, characters, script, wording or channel name; only the method above.
- **Image prompt base (user 2026-11-13, replaces the hazy one):** "Polished cinematic 3D-illustration film still, ultra sharp crisp focus, high contrast, deep rich saturated colors, clean clear air, absolutely no haze, no fog, no mist, no dust clouds, no washed-out whites, no bloom, deep dark shadows". NEVER use words haze / mist / dust haze / soft glow in prompts (they made the first images whitish and blurry). Day scenes = vivid blue sky + hard shadows; night = deep indigo + warm lamp gold. Generate at 1920x1088. Check each image for modern leftovers (street lamp posts, wires) and wide-angle warping before use. In the builder, `edit_plan` soft_glow/grain must stay off for history videos (they also whiten).

## 8. History videos = documentary look (user 2026-11-13, binding for every `noor-daily-history` video)
- Feel: a real documentary reconstruction; the viewer must "remember that era": authentic mud-brick/palm-trunk houses, plain wool/linen robes, leather sandals, clay pots, woven mats, camels. Day scenes are daytime (vivid blue sky, hard shadows), night scenes are night (deep indigo + lamp/fire gold). No haze/fog/mist, no whitish blur. Crisp.
- People: MORE people (bazaar crowds, families by a fire) but always small/from behind/no portraits, anatomically correct (every prompt says "exactly two arms and two hands with five fingers each, no extra limbs, no merged bodies"); look at every people image before use; regenerate or crop if any limb/hand is wrong.
- Generators: scenes with people = Gemini image (paid, ~Rs 4-6 each, max 3-4 per video, inside the Rs120 story cap, "photorealistic cinematic digital painting" style block); empty scenes/objects/interiors = free Cloudflare flux 1920x1088. Same base prompt as section 7 + period clause.
- Motion: 25% of shots (parallax + camera move), 75% stills with eased push/pull/pan (later 50%, then 100%). Camera move chosen by content: push-in on emotion/key line, pull-out on reveal, pan along a street/path.
- Sound design follows the SCRIPT line by line (`amb` = looping bed per line, `sfx` = one-shots with offset): market line = crowd + camel bell; house morning = birds + wind; horse = neigh + palm leaves; walking with load = footsteps on sand + wind; camel = groan; hand mill = stone grinding + low fire; night = crickets + fire/door; far crowd for town shots. Library: shared/sfx/history/ (CC0, `scripts/fetch_history_sfx.py`), plus shared/sfx/noor. Music: soft flute/oud-like bed at -17 dB under voice, voice mean ~-19 dB before loudnorm -14 LUFS.
- Editing: caption bottom, gold keyword, source tag on hadith lines, 4-6 s per shot in Longs (2-3 s in Shorts), soft cross-fade, no flashy transitions, no soft_glow/grain.
