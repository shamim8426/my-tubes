# Nigraan Noor: 2-day check, 2026-11-19 (scheduled run `nigraan-noor-2day`)

Data: `yt_analytics.py fetch` 2026-11-19 08:29 IST (Analytics rows end **2026-11-16**, a 2-3 day lag), reach
(Reporting `channel_reach_basic_a1`/`combined_a1`) to **2026-11-15**, public counters (Data API) live. ₹0, read-only.
One combined file for this round (instead of one file per video) because most videos have only a few views.
The first fetch hit a transient Analytics HTTP 500 on epHC_mBxEEg, and one retry worked.

Channel: 15 public + 4 private videos, **5 subscribers**, 361 lifetime views, 205 watch minutes (Analytics to 16 Nov).

## Checked (2+ days of data)
| Video | Type | Public since (IST) | Impr. | CTR | Views (pub) | AVD | AVD% | Top source | Check |
|---|---|---|---|---|---|---|---|---|---|
| 7fikMFw0OUQ Khawla (history) | L 3:23 | 15 Nov 19:08 | **1,067** | **0.9%** | 40 | 0:53 | 26.4% | Suggested 16 | 48 h |
| V3oXzLv13r4 Asma (history) | L 4:05 | 15 Nov 11:13 | 8 | 12.5% | 3 | 0:03 | 1.3% | - | 48 h, kam data |
| G10QXNZTxLQ Al-Asr | L 3:29 | 13 Nov 09:17 | 5 | 0% | 3 | - | - | external 1 | 48 h, kam data (7 d next run) |
| kmYyRGdykjY Al-Fatiha | L 7:54 | 25 Oct | 1,077 | 4.8% (Home 4.6%, search 12.5%) | 270 | 1:57 | 24.7% | Subscriber 260 | 7 d+ |
| 3fj1U_Q4Ku8 Al-Ikhlas | L 5:41 | 30 Oct | 153 | 2.6% (search 4.4%) | 19 | 2:24 | 42.4% | Search 9 | 7 d+, kam data |
| 5EjERhAwqRI An-Nas | L 5:32 | 4 Nov | 130 | 3.1% (search 2.0%) | 24 | 2:12 | 39.8% | Subscriber 16 | 7 d+, kam data |
| rRtM7wFIVcA Ayatul Kursi | L 7:22 | 30 Oct | 54 | 0% | 4 | 0 | 0% | search 1 | 7 d+, kam data |
| Je03wdD0EvY Al-Falaq | L 6:48 | 31 Oct | 53 | 3.8% | 4 | 0 | 0.2% | search 3 | 7 d+, kam data |

**Too new (published 17-19 Nov, no Analytics rows yet):** M7UXpH-W3IY Al-Fil, GCvLJ8jAS0Y + IXyFUmgacck Mehmaan
(v1 + v2), RoKAMWLpInE Mehmaan Short, hcS8zjiYeJ4 gufa sample, RkuSG9EZYXM + S6uelFj74Z8 Kafirun, and the private
mT0O-uwlthk/epHC_mBxEEg (Kahf) and aeb-ASeWlOo/7332dw93wCk (Ad-Duha).
Public-counter hint only: **RoKAMWLpInE Short 360 views, 16 likes (4.4%) in ~35 h**, the best Short so far;
S6uelFj74Z8 Kafirun Short 77 views, 5 likes in ~28 h. All Longs from 17-18 Nov have 1-4 views.

## Findings
1. **Khawla: YouTube tested it, but the packaging failed.** On 15 Nov it got 1,059 *suggested* impressions (the first
   Noor video past 500 impressions from suggested), but CTR was only 0.9%, so the test stopped after a day (11-16: 7
   views). The title opens with an unknown name ("Khawla bint Thalaba ki Kahani | ..."). The thumbnail is low-contrast
   brown on brown, with a small figure, a translucent text band, and text over the figure, so it is weak at
   sidebar size.
2. **Khawla retention: the drop happens in the first 10 s.** It falls 100% -> 59% at 10 s, 41% at 30 s and 29% at
   39 s, then stays flat at ~24% to the end (people who stay, finish). Line 2 at 0:06 is "ये बहुत पुरानी बात है, मदीना
   शहर की... नाम था ख़ौला... पति का नाम था औस" (background and names straight after the hook). Al-Fatiha showed the
   same pattern (14-19 s, "पहले नाम..."). Two videos now point the same way, but both are kam data (19 and 61
   engaged views).
3. **Surah explainers get a little search traffic, and stories get suggested traffic.** Ikhlas had 45 search
   impressions at 4.4% CTR and Nas 51 at 2.0%; the "Surah X ka Matlab Hindi Mein" titles do get found. The Khawla
   history story was shown next to other videos (suggested). Explainers that people do watch hold them better
   (Ikhlas 42%, Nas 40% AVD vs Khawla 26%).
4. **Bulk publishing.** The publish times show 2 Longs public in the same minute on 17 Nov (14:01 UTC) and 3 Longs in
   one minute on 18 Nov (03:50-03:51 UTC). Each got 1-4 views. Asma got only 8 impressions on the same day Khawla got
   1,067. This goes against "ek din, ek Long" (RULES 8), and same-day Longs compete for the 5 subscribers and for the
   first test.
5. **Policy risk: duplicates are public.** GCvLJ8jAS0Y (Mehmaan v1) and IXyFUmgacck (v2) are both public with the
   **same title**. log.md 2026-11-17 says v1 was to be deleted. hcS8zjiYeJ4 (the gufa *sample*, which the user said
   should not have been uploaded) is also public. Repeated near-identical uploads are what YouTube's
   "reused/repetitive content" review looks for (YPP), and they split views.

## 3 improvements for the next videos
1. History titles start with the human situation in plain words, with the name after `|`. Thumbnails get one big
   subject, a dark contrasting background, and 3-4 big words on the side away from the figure (no translucent band),
   checked at 168 px width.
2. After the hook line, go straight into the scene or conflict. Give background and names after ~20 s, woven into the
   scene.
3. Publish at most one Long a day, with its Short ~60 min later. Never publish 2-3 Longs in the same minute.

## User (Studio)
- Make GCvLJ8jAS0Y **private** (or delete it), but first set RoKAMWLpInE's Related video to **IXyFUmgacck**. Make
  hcS8zjiYeJ4 private or delete it, as already decided.
- Khawla 7fikMFw0OUQ: Studio -> Content -> video -> Thumbnail -> **Test & compare** with 2-3 new thumbnails (rule 1
  above). Optional: change the title to the new pattern.
- For Shorts swipe data, export Studio Advanced mode -> Shorts "Viewed vs swiped away" CSV ->
  `analytics/studio_csv/2026-11-2x_shorts_swipe.csv`.
