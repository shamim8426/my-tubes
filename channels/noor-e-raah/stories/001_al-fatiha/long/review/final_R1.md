# 001 Al-Fatiha — FINAL build check R1 (Munshi, 2026-10-25)

STEP: final (stage 7 + 8 + 9 + SURAH CHECK)   PROJECT: noor-e-raah/001_al-fatiha   VERDICT: FIX
Cost: ₹0. No STOP condition (balance / copyright / channel ID): none hit.

Files: long/output/001_al-fatiha_final.mp4 (14:47), timeline.json, 001_al-fatiha.srt, 001_al-fatiha_thumbnail.jpg, metadata.md.
Frames: long/review/final_frames/r1/ (85 JPG: 14 ayah, 62 lines, start/end, images 06/08/24), sheets in final_frames/sheets/.

## 1. Tech (measured)
- ffprobe: 1920x1080, 30/1 fps, H.264 High, yuv420p, bt709 (space/primaries/transfer), tv range; AAC LC 48 kHz stereo 192 kb/s; 474.03 s (7:54). OK.
- ebur128 (true peak): I = -14.0 LUFS, TP = -1.1 dBFS, LRA 6.2. OK.

## 2. Ayah windows
- Arabic text bytes: _ayah1..7.txt == script.md ARABIC lines == official Tanzil quran-uthmani (downloaded again today, default options) 7/7 byte-equal.
- **BLOCKER A — Arabic rendering (ffmpeg drawtext): harakat misplaced.** The letters are right but the marks are not placed
  on their letters: in ayah 5 (4:45–4:56) fathas/sukun float between the words, the shadda of إِيَّاكَ is shifted; in ayah 7
  (6:13–6:29) عَلَيْهِمْ shows stacked fathas over the ain, marks hang over the word gaps. Same renderer for ayat 1–6 and the
  intro title سُورَةُ ٱلْفَاتِحَةِ (0:00–0:17). A viewer can read a wrong vowel = Quran text shown wrongly.
  Crops: final_frames/sheets/crop_ay5.jpg, crop_ay7.jpg, crop_ay12346.jpg. (Builder's own compare_ayah5_video_vs_libass.jpg
  shows libass places the marks correctly.)
  Free fix: render the Arabic (ayat + title) through libass (ASS style "Amiri", fontsdir shared/fonts, same text bytes
  from the _ayah files, \an8 at the same position) or a PIL+raqm PNG overlay; drop drawtext for Arabic. ₹0. Then send me
  the 14 ayah frames + title frame for a quick re-check.
- Label "सरल भावार्थ — माने हुए तर्जुमों के आधार पर" shown exactly over each bhaavarth line (7/7, ASS Label events =
  line windows). OK.
- Music through windows (pre-duck stem, 0.5 s bins from fade-1 s to off+1 s): no gap in any of 7 windows (lowest bin
  -52 dB, whole-video p5 -50.5). The Quietude -> River Flute crossfade sits inside ayah 1 (150.9–152.4 s), smooth. OK.
- Swoosh: one per ayah at swoosh time (7/7), slow ~0.5 s rise, peak (400 ms) about -22 dBFS in the final vs bhaavarth
  speech peaks -9 to -14 dBFS. Soft, not a hit. OK (level see MINOR 1).

## 3. Lines / captions / voices
- _text.ass: 62 subtitle events, text == timeline/lines text 62/62, style == speaker 62/62 (Sub_ustaad white, Sub_sawaal gold),
  start/end within 0.3 s of the line. SRT: 62 blocks, UTF-8 (no BOM), text 62/62, shortest 2.45 s.
- All 62 timeline line texts appear verbatim in the approved script.md (R3 PASS).
- 62 mid-line frames (sheets/lines_1..7.jpg): right caption, right colour, nothing cut off (2-line wrap on 70 and 81 fine),
  cards (0:28–0:58, 7:14–7:37) readable. Nuqta: क़ुरआन / ज़बान / फ़ातिहा visible at full-res zoom (sheets/quran_zoom*.jpg).
- Voices: render uses the R2-passed wavs (Algieba = ustaad, Sulafat = sawaal), atempo 1.08 (pitch kept); no recitation audio.

## 4. Images
- Images 06 (1:24–1:33) and 08 (1:47–1:55) full-res frames: houses, steps, doors, lamps — no person/figure/shape. OK.
- Image 24 (7:37–7:54, 3 shots, fx 1.0 / zc 1.8): crescent, valley, cliff — no tent in any frame (7:39, 7:45, 7:50, 7:52, 7:53). OK.
- No AI text, no dome/minaret/Ka'ba, no Prophet/Sahabi/angel in any of the 85 frames.
- motion_check (jerk_rms): 3:04.5 0.064, 5:23 0.094, 7:39 0.087 = smooth; 6:00 (image 21, dunes) 0.14–0.23 depending on patch
  (low texture inflates it; no shake seen in frames) -> Note, eye check.

## 5. Music / ambience
- Stem method (voice after its mix chain vs ducked music, speech sections only): voice -21.0, music -38.8 LUFS =
  **17.8 LU under** (Soaring 17.4, Quietude 19.2, River Flute 17.6). Ambience -45.3 LUFS.
- Ambience names in timeline: breeze / desert+night / birds+breeze only; no water anywhere (also none under River Flute). OK.
- Ending: last line ends 7:50.0, River Flute fades 7:50–7:53, breeze alone to 7:53.5, then fade. OK.

## 6. Thumbnail
- 1280x720 JPG, 113 KB. Hindi correct at zoom (रोज़, पढ़ते, हैं, समझते, ज़बान nuqta OK). Bottom-right clear. 160x90 still readable.
- **BLOCKER B — Arabic ٱلْفَاتِحَة (drawtext): kasra of ت has dropped ~110 px down onto the Hindi line (stroke above "ज़बान"),
  sukun of lam missing/misplaced, fathas float high.** Crop: sheets/thumb_zoom_ar.jpg, thumb_zoom_hi.jpg.
  Free fix: same libass/raqm render, ₹0.
- MINOR: main text "रोज़ पढ़ते हैं… समझते हैं?" letter height ~7% of frame (rule ~12%).

## 7. Metadata draft
- Titles: 73 / 58 / 60 chars, all with "| नूर-ए-राह", no < >. Description 2211 chars. Tags 11, 192 chars. Hashtags 3.
- Tanzil attribution + link: OK. Music: Soaring, Quietude, River Flute credits = register text word for word, but joined
  with " — " instead of the register's line breaks (MINOR: paste the 3 register lines as they are). Ambience CC0 line OK
  (swoosh is also freesound CC0, covered). Fonts + "AI-generated" line OK.
- Hadith numbers (Bukhari 4474/4704/5007, Muslim 395) are in dossier.md. name_guard: OK.
- **Chapters do not match this build (FIX).** Corrected (Arabic swoosh time / first line of section, floored):
  0:00 शुरुआत · 0:18 सूरह का परिचय · 1:13 शान-ए-नुज़ूल · 1:55 आयत-दर-आयत · 2:18 आयत 1 · 2:44 आयत 2 · 3:42 आयत 3 ·
  **4:08** आयत 4 (was 4:09) · **4:44** आयत 5 (was 4:46) · **5:45** आयत 6 (was 5:46) · **6:13** आयत 7 (was 6:15) · **7:10** सीख (was 7:13).
  If the Arabic re-render changes any timing (it should not), recompute.
- ASK (user only): made_for_kids (channel.json null), contains_synthetic_media (channel.json false; AI voices + AI images),
  category (1 vs 27), which title.

## 8. Shan-e-nuzul statements on screen (text unchanged since script R3 PASS; sources opened in R1–R3)
- L17 [S15] "किसी ख़ास वाक़िये की कोई मज़बूत रिवायत नहीं मिलती" — al-Wahidi Asbab al-Nuzul (altafsir.com), Qurtubi (Bayhaqi: munqati') — ikhtilaaf (jagah/waqt), said without certainty claim. OK
- L18 [S15, S9] "ज़्यादातर उलमा के मुताबिक़ मक्की … शुरुआती दौर" — Ibn Kathir muqaddama (quran.ksu.edu.sa sura1-aya1), Qurtubi, Wahidi, Tafheem — ikhtilaaf, told as majority view. OK
- L20 [S9] "कुछ उलमा ने इसे मदीना में उतरी सूरह माना" — same sources — ikhtilaaf. OK
- L21 [S9] "दो बार उतरी" — Qurtubi (al-Tha'labi), Ibn Kathir — ikhtilaaf. OK
- L22 [S9] "इब्न कसीर के नज़दीक पहली राय ज़्यादा मुनासिब" — Ibn Kathir (والأول أشبه) — ikhtilaaf. OK
- Card 0:28 "मक्की (ज़्यादातर उलमा)" — S9 — OK.

## Problems
BLOCKER
1. Arabic harakat misplaced in all drawtext Arabic: ayat 2:18–2:30, 2:44–2:56, 3:42–3:51, 4:08–4:18, 4:44–4:56,
   5:45–5:54, 6:13–6:29 (clearest in 5 and 7) + title 0:00–0:17. Fix: libass/raqm Arabic render, ₹0.
2. Thumbnail Arabic ٱلْفَاتِحَة same bug (kasra on the Hindi line). Fix: same, ₹0.
MINOR
1. Music 17.8 LU under voice (user target 19; RULES 1c text still says 20–24). Cause: noor_render takes the mono voice
   stem (-16) as reference, but in the mix the voice sits ~-21 (stereo + aecho). Fix: measure the voice after its chain
   (or MUSIC_BELOW ~20.2); swoosh then also lands ~14 LU under. Also write the user's 19 LU decision into RULES 1c.
2. First word at 1.5 s (RULES 13: ≤1.0 s). Fix: LEAD 1.5 -> 0.8 (then recompute chapters, all shift -0.7 s).
3. Last 20 s: captions 94/95 at the bottom + end card text (7:34–7:54); tail after last line only 4 s. Keep end-screen
   elements top-right/left in Studio, or move those two captions up.
4. Thumbnail main text ~7% height (rule ~12%).
5. Music credits: use the register's line breaks verbatim.
Note: image 21 motion jerk 0.14–0.23 at 6:00 (dunes, low texture) — eye check only.

Agla kadam: builder fixes BLOCKER 1+2 (Arabic via libass, ₹0) + chapters in metadata.md, re-renders the final; Munshi
re-checks only the Arabic frames, thumbnail and chapters; then the user's metadata ASKs; upload only after the user's OK.

---

# R2 — re-check of the R1 fixes (Munshi, 2026-10-25, build 17:46)

VERDICT: **PASS-WITH-NOTES** (0 BLOCKER, 3 MINOR -> carry_over.md). ₹0. No STOP condition.
Frames: long/review/final_frames/r2/ (title, 14 ayah, L94/L95); sheets + comparisons: final_frames/sheets_r2/.

- **Tech:** 1920x1080, 30 fps, H.264, yuv420p bt709, AAC; 473.33 s (7:53). ebur128: I -14.1 LUFS, TP -1.1 dBFS. OK.
- **Arabic (BLOCKER A, fixed):** 7 Ayah + 1 ArTitle events in _text.ass (Amiri, libass); drawtext Arabic gone. Text bytes
  7/7 = official Tanzil quran-uthmani. Reference: I rendered the same Tanzil bytes with Windows DirectWrite (WPF,
  full OpenType shaping) and with plain libass, no size trick (sheets_r2/cmp2.jpg, cmp5.jpg, cmp7.jpg,
  ref_wpf_title.jpg). The video matches the DirectWrite reference mark for mark: every fatha/kasra/damma/sukun/shadda
  sits on its letter. No doubled fathas, nothing floating between words. Amiri itself places all upper harakat at one
  common height (design, same in DirectWrite).
  Fit: ayah 7 spans x≈125–1800, inside the frame. Arabic→label gap ≈10 px (tightest: ayah 1 and 3, kasra of م),
  no touching (sheets_r2/z3.jpg, labels.jpg). Subtitles are at the bottom, no overlap.
- **Thumbnail (BLOCKER B, fixed):** 1280x720, 113 KB; ٱلْفَاتِحَة via libass: sukun on lam, kasra under ت, fathas on ف/ح,
  with a clear gap above the Hindi line. Hindi nuqta OK, bottom-right clear, readable at 160x90.
- **Music:** stem method, speech only: voice -21.0, ducked music -40.0 = **19.0 LU under** (Soaring 18.6, Quietude 20.3,
  River Flute 18.8). OK (RULES 1c now ~19).
- **Music continuity:** no gap in any ayah window; lowest 0.5 s bin is -49.7 to -53.7 dB.
- **Swoosh:** 400 ms peak ≈ -26.5 dBFS vs bhaavarth speech peak ≈ -12.5 dBFS, i.e. ~14 dB under. Soft. OK.
- **First word:** line 3 placed at 0.80 s. The voice stem shows a faint breath from 0.80 s and the audible word from
  1.05 s. MINOR (0.05 s over 1.0 s; LEAD 0.7 would give ≈0.95 s).
- **End captions:** lines 94/95 (7:36–7:49) now in the top band (y≈180), above the end card. The lower and middle area
  is free for end-screen elements. OK.
- **Captions/SRT:** 62/62 text and style match the new timeline; SRT 62 blocks, timings within 0.3 s. OK.
- **Chapters (metadata.md) vs new timeline:**
  - Section chapters match exactly: 0:00, 0:17, 1:12, 1:55, 7:09.
  - Ayah chapters use the ayah cue (swoosh -0.5 s): 2:17 / 2:43 / 3:41 / 4:07 / 4:43 / 5:44 / 6:12. These match the
    swoosh times (2:17, 2:43, 3:41, 4:07, 5:44, 6:12).
  - Note: ayah 5 at 4:43 starts 0.4 s before line 59 ends; 4:44 would be cleaner.
- **Music credits:** now the register's 3 lines verbatim per track. OK.
- **name_guard:** OK.

MINOR (-> carry_over.md): (1) audible first word 1.05 s; (2) thumbnail main text ≈8% height (rule ~12%); (3) ayah 5
chapter 4:43 -> 4:44 (cosmetic).
Still for the USER before upload (ASK): made_for_kids, contains_synthetic_media, category, title choice.
