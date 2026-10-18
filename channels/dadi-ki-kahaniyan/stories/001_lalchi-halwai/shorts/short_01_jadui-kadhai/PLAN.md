# Short 01 — जादुई कड़ाही (from story 001, Long 01) — PLAN (not built yet)

- **Format:** 1080x1920, ~54 s (target 45–60 s), burned Hindi captions, same story images + cached TTS → **₹0**
- **Goal:** pull viewers to the full Long 01 video. Hook in the first 3 s, stop on a cliffhanger **before** the twist
  (coin → mitti), end card text "पूरी कहानी चैनल पर".
- **Folder:** this folder gets `project.json` (kind short, name `short_01_jadui-kadhai`), `lines.json`, `shots.json`,
  `meta.json` after approval. Images/audio come from the story (`../../images`, `../../audio/tts_cache`).

## Lines (all already in the TTS cache — exact same text + speaker, so no new TTS)

| # | Long line | Scene/img | Speaker | Text | ~sec | Why |
|---|---|---|---|---|---|---|
| 1 | 22 | 16 | sadhu | ये जादुई कड़ाही है, बेटा। इसमें जो डालोगे, दुगना हो जाएगा। | 8.3 | **Hook:** "ये जादुई कड़ाही है" is heard in the first ~1.5 s; the promise "जो डालो, दुगना" matches the Long 01 thumbnail |
| 2 | 24 | 17 | dadi_story | उस शाम छोटू ने कड़ाही में एक मुट्ठी आटा डाला... और आटा दो मुट्ठी हो गया! (+ magic sting) | 8.9 | proof the magic works — the visual payoff |
| 3 | 25 | 17 | chhotu | अरे वाह! ये तो सच में जादू है! | 3.4 | reaction, keeps pace |
| 4 | 29 | 20 | dadi_story | पर ये बात घसीटा की नज़रों से छुपी नहीं रही। | 4.4 | turn: the villain sees it (music → tension) |
| 5 | 30 | 20 | ghasita | आटा? हुँह! उस कड़ाही में तो सोना होना चाहिए... मेरा सोना! | 6.1 | greed = the theme of the story |
| 6 | 31 | 21 | dadi_story | उसी रात, जब छोटू सो रहा था, घसीटा दबे पाँव आया और कड़ाही चुरा ले गया। | 9.3 | rising tension |
| 7 | 32 | 22 | dadi_story | दुकान में दीया जलाकर उसने कड़ाही में एक सोने का सिक्का डाला... | 7.9 | set-up of the payoff |
| 8 | 33 | 22 | ghasita | चल, दुगना कर! | 1.8 | **cliffhanger** — cut here, before line 34 "...वो मिट्टी बन गया!" |
| — | — | 22 | — | end card "पूरी कहानी चैनल पर" (burned text, no voice) | 3.0 | CTA, ₹0 (no new TTS) |

Estimate: ~50 s voice after trimming + 7 gaps × 0.3 s + 3 s end card ≈ **54–55 s**.

**Left out on purpose:** lines 34–39 (coin turns to mitti, everything turns to mitti) = the twist; lines 41–54 (moral,
ending, Chhotu's shop) = the ending; line 23 ("…लालच के लिए नहीं") would fit the theme but pushes the Short past 60 s.
Option if you prefer the warning in: swap line 29 (4.4 s) for line 23 (7.3 s) → ~57 s.

## Framing (16:9 story images → 9:16) — needs a small free builder change

A plain centre crop loses the speaker in 2 of 5 scenes (see `review/crop_plan.png`, red box = centre 9:16):

| Scene | Centre crop shows | Plan (crop window centre x on the source image) |
|---|---|---|
| 16 (line 1, Sadhu speaks) | kadhai + half Chhotu, Sadhu cut off | window at x≈0.62: Sadhu + glowing kadhai |
| 17 (lines 2–3) | kadhai with flour ✅ | centre; 2nd shot window x≈0.36 on Chhotu for line 3 |
| 20 (lines 4–5) | empty ground ✗ | line 4: window x≈0.30 on the glowing kadhai; line 5: window x≈0.85 on Ghasita |
| 21 (line 6) | between Chhotu and Ghasita | slow pan from Chhotu asleep (x≈0.25) to Ghasita with the kadhai (x≈0.75) |
| 22 (lines 7–8 + end card) | Ghasita + kadhai ✅ but the kadhai already holds brown lumps that **hint at the mitti twist** | close-up on face + hand + coin only (top part), kadhai inside kept out of frame |

Builder change (₹0): let each shot choose where the 9:16 window sits on a wider image (`crop_x`, default = centre,
so Long 01 / Case 01 stay identical). Then `shots.json` + per-line `shot` overrides use it.

## Audio
- Music moods: jaadu (Enchanted Valley) for lines 1–3 → tension (Hidden Agenda) from line 4, 1.5 s crossfade;
  magic sting after line 2. Both tracks are in `shared/assets_license.csv` (CC BY 4.0) → credits in the description
  come from the register automatically.
- **Shorts music 3–4 dB quieter** (CLAUDE.md note): `MUSIC_BELOW_VOICE_DB["short"]` 9 → 12.5, checked with the stem
  method; target 12–14 LU. (Case 01 is not rebuilt; this only applies to new Short builds.)
- Loudness -14 LUFS, true peak ≤ -1 dBFS (final build).

## Captions
- Burned in (Shorts), Mukta, above the bottom 20% (Shorts UI overlay). Captions shorter than 0.45 s are merged
  automatically. All 8 lines had good Whisper coverage in Long 01 (only lines 2 and 50 of Long 01 were proportional —
  neither is used here).

## Carry-over / known MINORs
- `channels/dadi-ki-kahaniyan/carry_over.md` is empty (no MINOR waived after an R2 yet).
- Already fixed in the pipeline and so covered here: short captions merged, bt709 tags, pause-music offset,
  music level by stem method. Still to do in this build: Shorts music −3.5 dB (above).

## Concerns to decide before the preview (all ₹0 unless you choose the paid option)
1. **Sharpness:** a 9:16 window from a 1376x768 image is ~432x768 px, upscaled ~2.5x to 1080x1920 (more on
   close-ups). It will look softer than Case 01. The preview will show how much. Paid option only if you want it:
   5 new vertical images ≈ 5 × ₹3.24 = ₹16.20 (not planned).
2. **Hook wording on screen:** the first caption is "ये जादुई कड़ाही है, बेटा।" — no extra title text in the first 3 s,
   so the picture stays clean. Say if you want a top title like "जो डालो, दुगना!" for the first 3 s (₹0).
3. **Publish slot:** Long 01 is scheduled 20 Oct 19:00 IST. Under RULES section 8 the Short can go the same day at
   ≥ 21:00 (2-hour gap), so viewers can already find the full story — or any later day 19:00–23:59.

## Draft metadata (for approval)
- Title: `जो डालो, दुगना! जादुई कड़ाही का राज़ | दादी की कहानियाँ #shorts`
- Description: "रामपुर के लालची हलवाई घसीटा ने चुरा ली जादुई कड़ाही… पर आगे क्या हुआ? पूरी कहानी चैनल पर देखिए।"
  + music credits (from the register) + 3–5 hashtags: `#shorts #दादीकीकहानियाँ #HindiKahani #MoralStory`
- No "for kids" wording anywhere (title, description, tags, end card).
