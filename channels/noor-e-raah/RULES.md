# Channel RULES — नूर-ए-राह (noor-e-raah)

Only the rules special to this channel. Read `shared/RULES.md` first; everything there applies here too.
- Channel RULES can be stricter than shared RULES, never looser. Copyright, channel ID, secrets and upload safety can never be relaxed by a channel.

## 1. Format FINAL (user, 2026-10-24) — surah explainer, TILAWAT NAHI
- **No recitation audio at all**: no human tilawat, no AI tilawat, no clip of any qari. Any recitation audio in a
  video = BLOCKER. (The earlier tilawat research / recording plan is closed; `docs/IJAAZAT_NAMA_TILAWAT.md` stays only
  as a document.)
- **Music: very soft instrumental only** (section 1c, user 2026-10-24; replaces the earlier "no music" rule). No vocals,
  no nasheed, no beat.
- Every video, in this order:
  1. **SURAH KA PARICHAY**: name and its meaning; Makki/Madani; number of ayat; order in the Quran (number); order of
     revelation (only if an accepted list gives it, with source); other names of the surah; its main message in 1–2 lines.
  2. **SHAN-E-NUZUL** (when, where, in what circumstances): ONLY from accepted books (e.g. Tafsir Ibn Kathir,
     al-Wahidi "Asbab al-Nuzul", accepted Hindi/Urdu tafseer). Every point has its source. Where scholars differ (e.g.
     Makki vs Madani): "ज़्यादातर उलमा के मुताबिक़ ..." + the other view, both with sources. Weak / disputed narrations are
     NEVER in the video; they go to the dossier's "chhodi gayi" list.
  3. **AAYAT-DAR-AAYAT**: the Arabic ayah on screen (font, exact text from the licensed source, no audio); the narrator
     reads the translation chosen per section 1a; then the simple meaning (only from the dossier, agreed in 2+
     tafseer); where it fits, one modern example marked [MISAAL] in the script.
  4. **SEEKH**: 2–3 practical lessons from the surah. At the end a hint of the next video.
- Content comes only from the story's dossier (Khoji, section 3 below). A shan-e-nuzul statement without a source =
  BLOCKER.

## 1c. Music and sound (user, 2026-10-24) — channel.json "background_music": "soft"
- VERY soft instrumental: ambient pad, light ney/flute, soft piano or light oud notes; no beat/rhythm, no vocals, no
  catchy tune. Plus light natural ambience by the scene's mood (wind, birds, rain, water, crickets, desert wind).
- Level: music **~19 LU below the narration as heard in the mix** (user 2026-10-25: "thoda zyada"; was 20–24), with
  ducking; light warm reverb on the voices; swoosh ~14 LU under the voice.
- Arabic (ayat, surah title, thumbnail) is drawn by **libass (ASS, font Amiri)**, never by ffmpeg drawtext — drawtext puts
  the harakat off their letters (Munshi final R1 2026-10-25). Hindi screen text likewise libass (nuqta).
- **Music is continuous through the whole video (user 2026-10-25; replaces the earlier fade-out rule): it does NOT
  stop for an ayah.** As each new ayah comes on screen, one soft swoosh (`shared/sfx/noor/swoosh_*`, ~14 LU under the
  voice) brings the Arabic in. Track changes only by a slow crossfade. Music stopping/gapping around an ayah = MINOR;
  a loud hit or a beat = BLOCKER.
- Sources ONLY: (1) YouTube Audio Library (the user downloads in Studio into `shared/music/noor/`; note the licence
  type; "Attribution required" -> credit), (2) Kevin MacLeod / Incompetech (CC BY 4.0, credit), (3) Pixabay only as
  backup. Every track in `shared/assets_license.csv` before use; credits in the description.
- Script cues: `[MUSIC soft: <mood>]`, `[AMBIENCE: <sound>]`, `[SWOOSH — ARABIC ON SCREEN]` (older scripts:
  `[MUSIC fade-out 1s — ARABIC ON SCREEN]` = the same, the music plays on), `[MUSIC: <track>]` for a crossfade.

## 1a. Tarjuma (user, 2026-10-24) — never ask anyone for permission (no emails / permission requests)
Use the first that is available, in this order:
1. A Hindi translation whose own website terms say CLEARLY that commercial / YouTube use with credit is allowed
   (terms text + link in the dossier).
2. A copyright-free old translation: translator died 60+ years ago (India rule), with proof (death year from 2 reliable
   sources) in the dossier. Read word for word; an Urdu one only in our own letter-for-letter Devanagari transliteration.
3. Otherwise **SARAL BHAAVARTH**: the meaning of 2–3 accepted translations in our own simple words (no copy of any one);
   on screen "सरल भावार्थ — माने हुए तर्जुमों के आधार पर". Munshi compares every line with all three translations
   side by side: different meaning = BLOCKER, copied wording = MAJOR.
Arabic text: Tanzil terms (verbatim, no change, no Unicode normalisation; attribution + link in the description).
Rule order for choosing (user, 2026-10-24): 1) far from any firqa/maslak (no maslak name on screen), 2) licence clear,
3) easy language.
**DECIDED 2026-10-24: SARAL BHAAVARTH for the channel.** Why: (1) the only "copyright free" Hindi translation
(CPS/Goodword, Maulana Wahiduddin Khan, imprint page 3: "This translation of the Quran is copyright free") says nothing
about commercial use, neither in the PDF nor on cpsglobal.org/goodwordquran.com, and a related CPS English text is listed
under CC BY-NC-ND on archive.org; (2) the public-domain old translations (Shaikh-ul-Hind 1920, Thanvi, Kanzul Iman) carry a
maslak identity and old/heavy language; (3) the bhaavarth is licence-safe, easy, and checked line by line against three
accepted translations. Revisit only if a translation's own terms say commercial/YouTube use clearly.

## 1b. Two voices (user, 2026-10-24) — a conversation in everyday language
- **USTAAD** (Gemini voice Algieba): Arabic ayah announcement, bhaavarth, matlab, parichay and shan-e-nuzul. Only the
  Ustaad makes a religious claim, and only from the dossier sources.
- **SAWAAL** (Gemini voice Sulafat): the ordinary person's questions ("iska matlab hamari zindagi me kya hai?"), the
  [MISAAL] stories and short summaries. Respectful and soft; never states a religious ruling or fact on her own.
- Long ~8:00, at most 2 MISAAL per video.
- **Questions (user 2026-10-25, from story 002):** SAWAAL asks at most **3-4 real questions per video**, never in quick
  succession — a gap of **3-3.5 minutes** between questions (user 2026-10-25; was 1.5-2 min). In a ~8 min video that
  means about 3 questions (e.g. near the start, ~3:00-3:30, ~6:30). Her other lines are short reactions, a misaal or a
  summary, not new questions. Munshi counts the question lines; more than 4, or two less than ~3 min apart = MAJOR.
- TTS completeness: EVERY line is checked with Whisper against its text; a missing word = make that line again on the
  free key (max 2 tries); still missing = shorten/simplify that line (same meaning) and make it again. Sulafat dropped a
  clause in the audition, so this check is never skipped.

## 2. Visuals
- **Never any image, face, silhouette, shadow, outline or back-view of any Prophet (Nabi), of the Prophet Muhammad ﷺ,
  his family or any Sahabi** — not even blurred, from far or as light. Any such image = BLOCKER (never used, even if paid).
- Shan-e-nuzul scenes show only places and mood: valleys of Makka, desert, night sky, old houses, lamps, empty paths.
  No crowds acting out a narration; no angel shown in any form.
- Arabic text is rendered by us in an Arabic font (licence in `shared/assets_license.csv`), never drawn by AI.
  Hindi text likewise. No AI-written letters in images.
- No studio/artist/brand names in prompts (shared RULES 12a).

### 2a. "Immersive" andaaz (user 2026-10-25) — from story 002 (Al-Baqarah 1-5); 001 Al-Fatiha stays as it is
- **Ordinary people may appear, faces included** (user 2026-10-26; before: back/far/silhouette only) — AI or stock.
  Conditions: never resembling a real/famous person; modest dress; a stock person (real, identifiable) never in a sin,
  punishment or Jahannam context (stock licence: no "bad light"). Musafir and worship scenes keep their own rules below.
- **NEVER, in any form (not from the back, not far, not as silhouette/shadow/light):** any Prophet (Nabi), the
  Prophet Muhammad ﷺ, his family, any Sahabi, any angel, and any person named in the Quran (e.g. Musa, Ibrahim, Yusuf,
  Maryam AS, Firaun …). Their stories are shown only through places and symbols (sea, staff-less landscape, well,
  palm, light). = BLOCKER.
- **Worship scenes** (dua, namaz, sajda) only from far or from the back; Munshi checks the posture is correct and
  respectful (no wrong/odd namaz posture, no mixed or immodest dress). Wrong posture = BLOCKER.
- **POV shots first:** prefer "darshak ki aankh" shots — the viewer's own hands raised in dua, their own steps on a path,
  what they see — over third-person scenes.
- Style for 002 onward: to be chosen after the "cinematic watercolor" / "Musafir" tests (`samples/immersive_test/`,
  `samples/musafir_test/`).
- **"Musafir" — the one permanent character, FINAL look v3 (user 2026-10-25, Munshi R2 PASS; from story 002):** an
  ordinary slim YOUNG man of 18-20, CLEAN-SHAVEN, short dark hair, plain light earth-tone (beige/khaki) kurta-pajama, a
  small cloth bag on the shoulder, bare head or a small plain cap, simple sandals. NOT white clothes with a white head
  cloth, NO robe/cloak, NO turban (so he never looks like a Prophet or a Sahabi). Not resembling any specific or famous
  person. Reference: `characters/musafir/sheet_v3.png`; for scene prompts use ONLY `characters/musafir/ref_back_dua.png`
  (standing + dua views), never a sheet view with a turned head.
- **Musafir is shown ONLY FROM BEHIND** — directly behind or at most ~20° off, head turned away. No part of the face
  ever: no nose tip, eyelash, eyebrow, lip or chin past the outline of the head/cheek. Never a three-quarter view, a
  "lost profile", a side profile or a profile silhouette (tested twice: the model cannot hold those angles). The full
  body may be shown. Any face feature = BLOCKER (Munshi zooms 8x/16x on every head).
- **Script, captions, titles and descriptions NEVER hint that the Musafir is any special or named person** — he is just
  "एक मुसाफ़िर", an ordinary traveller like the viewer. A hint = BLOCKER.
- Dua posture (Musafir or anyone): elbows bent and close to the body, hands in front of the chest below the chin, palms
  open facing up toward the face, head slightly bowed — never hands beside the head, above the shoulders or palms forward. His look comes from his
  character sheet (`characters/musafir/sheet_*.png`, used as the image reference) and never changes. Hands: exactly
  five fingers (Munshi zooms). Dua/worship poses only from the back or far, correct and respectful. Face detail = BLOCKER.

## 2b. Shorts (user 2026-10-25)
- **A Short never ends on a half ayah.** Every ayah that appears in a Short is complete: the full Arabic on screen
  (whole ayah, never cut) + its complete bhaavarth line, and if its matlab is used, the whole matlab sentence(s). If the
  time limit does not allow the complete last ayah, drop that ayah — never cut it, never end mid-sentence.
- No sentence is cut anywhere in a Short (start or end); the last spoken line ends naturally before the end card.
- Munshi checks every Short: last ayah complete + no cut sentence; a half ayah or cut line = BLOCKER.

## 3. Research (Khoji, mode "surah") and review (Munshi)
- Dossier per video: `stories/<NNN>_<slug>/research/dossier.md` + `sources.json`, with the section
  **"Surah parichay + Shan-e-Nuzul"**: every point has source(s) and a grade: **maana hua** / **ikhtilaaf** /
  **chhoda gaya** (weak or disputed — never in the video).
- Arabic text and Hindi translation: one fixed source each, its licence checked and written in the dossier and in
  `shared/assets_license.csv` before the script. A licence doubt = copyright doubt (stop and ask the user).
- No sectarian (firqa) debate, no fiqh rulings, no judging other religions or people. Respectful tone throughout.
- Munshi checks every shan-e-nuzul and meaning line against the dossier and opens its sources; the review sheet
  (`long/review/<round>.md`) lists every shan-e-nuzul statement with its source link(s) separately.

## 4. Pilot
- Story 001 = Al-Fatiha in this format. Dossier and script are free (₹0). Voice audition and look test only after the
  Google balance is recharged (balance below ₹50 = no paid call).

## 5. Gemini key (user, 2026-10-24)
- `GEMINI_API_KEY_FREE` (this channel's own Google project, no billing) is used ONLY for this channel's work, never
  for Kissago or any other channel. Free first; on 429 (free quota) the same request goes to the paid `GEMINI_API_KEY`
  (`scripts/gemini_keys.py`; a free call is logged with actual ₹0 and "free" in the size column).
- Production TTS (user, 2026-10-24): free first; as soon as the free quota is used up (429) the same line goes to the
  paid key — never wait for the next day. (Paid only while the balance is above the ₹50 floor; below it = stop and ask
  for a recharge.) The `free_only` mode (stop on 429) is only for auditions/tests the user marks as ₹0.

## Metadata
- Description: the sources list (tafseer books, Arabic text source, translation source with its attribution).
- `contains_synthetic_media`: set per channel decision before the first upload (AI narrator voice / AI images).
