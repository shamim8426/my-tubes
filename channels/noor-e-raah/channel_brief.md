# Channel brief — नूर-ए-राह | Noor-e-Raah (key: noor-e-raah)

One page for the Kaarigar and every agent. Rules are not copied — only referenced. The Kaarigar updates "Abhi ki
series / plan" after every video; the Sanchalak updates "Bade faisle" after every decision.

## Maqsad aur darshak
Quran ki surah, aasaan Hindi me (series "शुरू से क़ुरआन", tagline "क़ुरआन, आसान ज़बान में।") for Hindi-speaking
families: parichay → shan-e-nuzul → aayat-dar-aayat (saral bhaavarth + matlab) → seekh (channel RULES 1).

## Look
001: style a "cinematic painted", places only. From 002: "immersive" (RULES 2a) — POV first, HARD RULE: people only as
close details - hands/feet, no full figures or faces acting a scene (2026-10-26; never a Prophet/Sahabi/angel in any
form; Musafir + worship only from behind/far); style choice from the tests pending (`brand/STYLE_NOOR.md`).

## Awaazein + roles (RULES 1b, channel.json "voices")
FROM 2026-11-10 (RULES 1d): ONE narrator only (Algieba), no questions, no tilawat disclaimer, tempo 1.15, reuse existing images. (Old: USTAAD + SAWAAL.)
USTAAD = Algieba (aayat, bhaavarth, matlab, parichay, shan-e-nuzul; only he makes religious claims, with sources).
SAWAAL = Sulafat (questions — from 002 max 3-4, 3-3.5 min apart; misaal; short summaries). Tempo 1.08 in render.

## Kirdaar
Musafir (from 002): young, clean-shaven, beige kurta-pajama, shoulder bag, bare head/small cap — ONLY from behind
(RULES 2a; `characters/musafir/sheet_v3.png`, scene ref `ref_back_dua.png`).

## Music
Continuous soft instrumental (Soaring / Quietude / River Flute), ~19 LU under the voice, one soft swoosh per ayah,
ambience by mood (RULES 1c).

## Pakke niyam (hawale)
No tilawat (RULES 1) · tarjuma = SARAL BHAAVARTH (1a) · Arabic only Tanzil bytes via libass/Amiri; Hindi via libass
(1c, STYLE_NOOR) · never any Prophet/Sahabi/angel/Quran-named person in any form (2, 2a) · Shorts: last ayah complete
(2b) · sources + grades, nothing from "chhoda gaya" (3) · fazilat only from sahih hadith (Khoji dossier) · Gemini free
key first for TTS, images paid (5) · budget target ₹100, HARD limit ₹120 per story (Long + Shorts + thumbnail), ₹50 floor (shared RULES) · Munshi BLOCKER open = no upload ·
private + STUDIO ACTION while api_audited false.

## Learnings ka saar (Nigraan, `learnings.md`)
Empty — first post-mortem of Al-Fatiha 48 h after it went live.

## Abhi ki series / plan
2026-10-30: series_queue.json (10 items, 002-011), then 012 Al-Baqarah 1-5. Demand check: research/surah_demand_2026-10-30.md.
001 Al-Fatiha uploaded private (kmYyRGdykjY), STUDIO ACTION: schedule 2026-10-25 19:00, thumbnail by hand (v2A/v2B to
choose), pin comment. Next: 4 Shorts of Al-Fatiha (needs a 9:16 renderer), then 002 Al-Baqarah 1-5.

2026-11-04: 002-005 uploaded private (series queue: ayatul-kursi, al-ikhlas, al-falaq, an-nas done; next 006 al-kausar needs a Khoji dossier). 005 An-Nas: https://youtu.be/5EjERhAwqRI (5:31.9, -14.1 LUFS, 14 reused base images + 2 new free Cloudflare images, story cost Rs 15.48; STUDIO ACTION pending: watch, schedule 2026-11-04 19:00 IST, pin first comment ~19:05). Lesson: never run noor_run.py with --until after TTS is done (its tts stage retakes flagged lines = paid); Gemini paid key has a 100 requests/day cap shared by all channels.

## Bade faisle
- 2026-10-30 (user) Free first for AI images: wallpapers via Cloudflare flux (scripts/cf_image.py, Rs0), Gemini paid only as fallback.
- 2026-10-30 (user) Daily series: 10 short, most-searched surahs BEFORE Al-Baqarah, one video a day, auto edit + PRIVATE upload; the user
  makes it public after watching and asks for updates. No script checkpoint (Munshi reviews). New playlist. Top-up by the user.
  Thumbnail v3 (Arabic calligraphy + Hindi + hook). Run book: docs/NOOR_DAILY_RUN.md; queue: series_queue.json.
- 2026-10-24 Format final: no tilawat; saral bhaavarth; two voices.
- 2026-10-25 Music continuous + swoosh; style a default for 001; Musafir v3; questions max 3-4, 3-3.5 min apart;
  Shorts never cut an ayah; Arabic via libass.


## Daily plan (user 2026-11-09)
Nightly after 02:00 IST: one Long (surah, RULES 1d) + one Short (Imaan Shorts, RULES 2c/2d), both private. Tasks: noor-daily-short, noor-daily-long; runbooks `scheduled_tasks/`.
