# 009 Al-Kafirun: Munshi FINAL R1 (Long + Short quick check), 2026-11-18

VERDICT: **Long PASS-WITH-NOTES** (0 BLOCKER, upload OK). **Short FIX** (4 free items, one ~2 min rebuild, Rs0; no new Munshi round needed, all MINOR).
STOP condition: none (ledger balance Rs543 > Rs50, no copyright doubt, channel_id UCmw4fs9jN49GTq7wVSdYm6w = channel.json).

## Opened and measured
- Long output/video.mp4: 1920x1080, 30 fps, H.264, AAC **96 kHz mono** (from the alimiter step; YouTube accepts it; next time `-ar 48000`). 4:28.8 (RULES 2i/2n 4:00-5:00 OK).
- Loudness: Long **-14.7 LUFS, TP -1.3 dBFS**; Short **-14.4 LUFS, TP -1.4 dBFS**. No silence > 1.2 s under -45 dB (music continuous). Music bed in the voice gaps ~17 dB under speech (RMS estimate; RULES 1c ~19, within 3 dB, OK).
- Arabic: 6/6 strings in work/subs.ass == sources.json `text` (sha256 match) == raw Tanzil v1.1 lines 109|1-6. Zoomed all 6 cards: harakat on their letters, dark outline (ayah_outline 6) reads well, nothing cut. Short shows the same Long cards (Arabic whole in the panel).
- SRT: 45 cues == 45 script lines, text identical. Timing is from TTS lengths (not Whisper) for ALL 45 lines; cue = wav + 0.40 s pad. Spot-checked in the final mix with Whisper word stamps: L5 voice at 29.42 (cue 29.60), L35 at 195.88 (cue 195.94), L45 ends 267.54 (cue end 268.76): within 0.3 s.
- TTS spot-listen (Whisper small, my own run) of L5, L21, L35, L36, L45: every word present; "एक अल्लाह" heard as "एक लाह/आल्लाह" (natural liaison), L35 "नहीं लड़े" heard correctly ("लडे"), insaaf/sauda = phonetic variants. Accept. One voice for all 45 lines (Charon, gemini-3.8-flash-lite-tts): RULES 2k met (voice Charon); timbre may differ a little from 008 (Note).
- R1 script fixes verified in script.json + srt: L3 Madani view, L7, L14, L15, L18, L21, L33 "यक़ीन", 60:8 as two faithful lines (L35-36, conditions kept, "नहीं रोकता"), L37-38 Bukhari 2620 split with "हाँ", L39-40 Muslim 726 "पढ़ीं", L42 source named. Dropped summary line: OK in meaning (bartaav point stays at L34-36).
- Frames: one per line (review/final/sheet_long_1-3.jpg) + zooms. Faceless storybook, blank heads, dark gloved hands, modest dress, dua posture (06) hands in front of chest. Stand-in fixes applied: L11-14 = 04b (no people), L37-38 = 01b (no people), L39-41 = 09b (no people), L9 = 03. No Nabi/Sahabi/angel, no dome/minaret, no AI letters.
- Thumbnail 1280x720, 151 KB, Hindi matras OK, bottom-right empty, readable at 160x90, no spoiler.
- Metadata (Long): title 88 chars, hook words first; description 1866 chars with Tanzil CC BY 3.0 attribution + link, saral bhaavarth line, tafseer + 60:8 + 5 hadith numbers, River Flute exact CC BY 4.0 credit, Amiri/Mukta OFL, AI note, "no Nabi/Sahabi shown" note; 3 hashtags; tags 275 chars; made_for_kids false; synthetic true (as 008 and SHORT_FROM_LONG; channel.json still says false, stale); privacy private. name_guard: OK (both jobs).
- Short: 1080x1920, 51.8 s (< 60, SHORT_FROM_LONG 35-59), ayat 109:1-3 consecutive = Long L12-21, every ayah complete (full Arabic card + bhaavarth + full matlab), no cut sentence at start; first word ~0.4 s; captions bottom at 79% height, label at ~17%.
- Cost: cost_log 125 rows for 009 = **Rs12.85 incl GST** (TTS only; story_budget.py with the story path prints Rs0, ledger lookup misses the path: Note). Cap Rs120 OK.

## Short FIX (free, make before the Short upload)
1. **Blurred background shows a huge, edge-cut copy of the Arabic ayah** (s01 at 2 s, s09 at 47 s). SHORT_FROM_LONG: Arabic never cropped. Fix in short/make_short.py: build `[bg]` from a text-free source, e.g. `crop=1920:560:0:330` (below the Arabic, above the ucharan) or the line's own image, then blur.
2. **Single-line captions reach ~88% width** (L17, L18 at 11%-88%): RULES 13 keeps the right 15% clear. Fix: Cap style MarginL/MarginR 80 -> 170 (lines wrap to 2, still inside 15-85% height).
3. **Fade-out touches the last word**: "बनाता" ends 51.24 s, afade starts 51.05 s. Fix: `t1 = T[B][1] + 0.5` (hold) so the 0.6 s fade starts after the voice.
4. **Vertical cover file missing** (RULES 14): save `short/output/cover.jpg` (1080x1920, frame at ~1.2 s when the ayah card is fully in).
After the rebuild the builder checks: frames at 2 s and 47 s have no Arabic in the background, caption right edge <= 85%, LUFS -14 +-1, TP <= -1. Then upload; no new Munshi round.

## Long notes (MINOR, to carry_over; no rebuild)
- First ayah at 1:09 (learnings LAGU KARO 30-40 s); reason: RULES 1 order parichay + shan-e-nuzul. Next surah: parichay <= 30 s.
- Final summary now 2 lines (L44-45); RULES 2i asks 3-5 short lines.
- Shots longer than 8 s on one move: L3 11.3 s, L36 10.2 s, L38 10.0 s, L33 9.0 s (RULES 13 / motion max 8 s). Split such lines into two presets.
- Caption box: darker vertical stripes where a gold word or the Amiri ﷺ starts/ends (libass BorderStyle 3 draws one box per run, overlaps double the alpha). Seen on almost every gold line since 2026-11-13. Builder fix: Sub style BorderStyle 4 (one box per event) or an opaque BackColour.
- ﷺ in captions renders small (Amiri at 62 px inside Mukta text): readable, Note.
- Thumbnail hook 6 words (learnings: <= 3-4); title + thumbnail promise "Lakum Deenukum ka sahi matlab" is kept at 2:49-3:36 (not misleading), but RULES 13 wants it inside the first 60 s.
- L24-25 (ayah 5) + L29 on 09_dawn_walk: lone man from behind while the ayah says "मैं". Allowed as an ordinary believer (2h), but for first-person ayah lines prefer group/no-person shots (Note).
- No per-ayah swoosh (RULES 1c); 2i/2m template is silent on it (Note).

## Shan-e-nuzul / fact lines (unchanged from script R1, fixes verified)
| Line | Statement | Dossier | Grade |
|---|---|---|---|
| L1-L3 | 6 ayat, name, 109th; Makki per most, Madani view noted | P1, P2 (Tanzil, Qurtubi, Ibn 'Ashur, Tafheem, quran.com) | maana hua / ikhtilaaf told as such |
| L4 | al-Muqashqisha | P4 (Qurtubi, Ibn 'Ashur) | maana hua |
| L6-L11 | idols; Quraysh chiefs refused, wanted a middle way, many times; surah = final answer | N1, N2 (Tabari, Ibn 'Ashur, Ma'ariful, Tafheem, Qurtubi) | maana hua |
| L27-L29 | three views on the repetition, told as "उलमा/कुछ कहते हैं" | K2 a-c (Qurtubi, Tabari, Ibn Kathir, Ma'ariful) | ikhtilaaf |
| L32-L36 | not "all paths same"; separation in worship, not dealings; 60:8 faithful | K3, K4 (Quran 60:8, Ibn Kathir) | maana hua |
| L37-L38 | Bukhari 2620 | K4 | sahih |
| L39-L41 | Muslim 726, Muslim 1218 | Z1, Z2 | sahih |
| L42-L43 | Abu Dawud 5055, Tirmidhi 3403 | Z3 | sahih/hasan |
Source pages not re-opened on the web in this run (no web tool); hadith numbers match the dossier and standard sunnah.com numbering.

## Upload notes
- Long first: upload.json has no `publish_at` (api_audited false -> private, as 008). Then fill LONG_ID in the Short job in all 3 places (description link, first_comment, parent_video_id) before the Short upload.
- STUDIO ACTION + related_video/pin_comment pending lines after the uploads.
