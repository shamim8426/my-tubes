# Post-mortem 48 h (late, 2026-10-29) — kmYyRGdykjY "Surah Al-Fatiha ka Matlab Hindi Mein | Roz Padhte Hain, Samajhte Hain? | Noor-e-Raah"

Nigraan Noor · pehli report · read-only, ₹0 · data fetch 2026-10-29 ~21:30 IST (`fetch` + `reach-fetch`, dobara nahi chalaya)

## Data kab ka
- Asli publish: **2026-10-25 22:40 IST** (API `publishedAt` 17:10:15Z) — plan 19:00 IST schedule tha; Studio action
  ~3 h 40 min der se hua (isliye 25 Oct ko sirf 8 impressions). 48 h = 27 Oct 22:40 (nikal chuka), **7 din = 1 Nov 22:40 IST**.
- Analytics API (views, AVD, retention, traffic): sirf **25-26 Oct** tak. Reporting API (impressions/CTR): **25-27 Oct** tak.
- Public counter (Data API, 29 Oct): **261 views**, 2 likes, 0 comments, 1 subscriber.

### 261 vs 56 ka farak
Public view counter lagbhag live hai; YouTube Analytics ka data 2-3 din pichhe chalta hai (PT din ke hisaab se process
hota hai). Analytics me abhi sirf 25 Oct (1 view) + 26 Oct (55 views) = 56 hain. 27 Oct ke 661 impressions reach me
aa gaye par us din ke views Analytics me abhi nahi; 27-29 Oct ke ~205 views agle 2-3 din me jud jayenge. Koi galti nahi.

## Numbers
| Metric | Value | Note |
|---|---|---|
| Impressions (25-27 Oct) | **871** (8 / 202 / 661) | >= 500, CTR par halki seekh chal sakti hai |
| CTR | **~4.9%** kul (12.5% / 8.4% / **3.8%**) | ~43 clicks; jaise YouTube naye logon ko dikhata gaya, CTR gira |
| Views (Analytics, 25-26 Oct) | 56 (engaged **18**) | public counter 261 |
| AVD | **2:38** (158 s) = **33.4%** of 7:54 | |
| Watch time | 48 min | |
| Retention @30 s | **72%** (engaged viewers ka) | curve sirf ~18 logon par (har step = 1 aadmi) -> **kam data** |
| Relative retention | 0.18-0.92 (zyaadatar 0.3-0.7) | same-length videos se neeche |
| Likes / comments / shares / subs gained | 2 / 0 / 0 / 0 (API) | channel par 1 subscriber |

### Traffic
| Source | Views (25-26 Oct) | Impressions (25-27 Oct) | Clicks (approx) |
|---|---|---|---|
| Browse features / Home ("SUBSCRIBER" type, "what-to-watch") | 55 | 859 (98.6%) | 42 |
| YouTube search | 0 | **9** | 0 |
| Channel page / playlist | 1 | 3 | 1 |
Device: ~97% mobile (Android). 56 views me se sirf 18 engaged: baaki zyaadatar Home feed ka mobile inline-autoplay
(bina click / bina awaaz ke) view lagta hai.

## Thumbnail (upload par 403 hua tha)
Live thumbnail (`i.ytimg.com/vi/kmYyRGdykjY/maxresdefault.jpg`, 29 Oct) **custom hai**: diyon ki qataar + Bismillah
(Arabic) + bada Roman text "**7 AAYATON KA ASLI MATLAB**" (golden "ASLI MATLAB"). Ye repo ki kisi file
(`001_al-fatiha_thumbnail.jpg` / `_v2A` / `_v2B`) se match nahi karta — user ne Studio me alag/naya banakar lagaya.
Kab laga, ye data se pata nahi; isliye CTR girawat ko thumbnail se nahi jod sakte. User se: kab lagaya, aur file
repo me `output/` me rakh dein (aage A/B ke liye).

## Retention kahan girti hai (lines.json/timeline.json se) — KAM DATA (18 engaged viewers)
| Samay | Retention | Us waqt kya chal raha tha |
|---|---|---|
| 0-14 s | 94-100% | hook: SAWAAL "क्या हम उसका मतलब जानते हैं?" + USTAAD intro, ek hi image 01_dawn_valley (17.5 s) |
| **14-19 s** | 100% -> **72%** | hook khatam (16.4 s), image badli (17.5 s 02_valley_sunrise), "पहले नाम। 'फ़ातिहा' का मतलब क्या है?" — vaada "matlab" ka tha, mila "naam" |
| **33-38 s** | 67% -> **50%** | "हम जो गिनती ले रहे हैं, उसमें बिस्मिल्लाह पहली आयत है।" (ginti ki technical baat), wahi image 21 s se |
| ~52 s | 50% -> 44% | "'अस-सब्उल-मसानी'..." (naamon ki list) |
| ~95 s | 44% -> 39% | shan-e-nuzul: "और कोई दूसरी राय भी है?" (ulama ki raayein) |
| ~118 s | 39% -> 33% | "अब आयतें..." — pehli aayat ka matlab 140.8 s (2:20) par aata hai |
| 3:00-6:10 | 28% sthir | aayat-dar-aayat: jo ruke, wo ruke rahe (achha) |
| ~6:10 | 28% -> 22% | aayat 6-7 |
| 7:25-7:54 | 22-28% | seekh/ant par halka uchhal (log aage skip karke seekh dekh rahe) |

Pattern (hint): 2:20 tak — jab tak pehli aayat ka matlab shuru hota — **2/3 engaged viewers chale gaye**. Ghatane wali
cheezein: parichay ke technical hisse (ginti, naam, raayein) aur ek image par 17-21 s.

## Sabse badi kamzori
Hook "matlab" ka vaada karta hai, par asli matlab 2:20 par shuru hota hai; beech ka 2 min parichay/shan-e-nuzul me
aadhe log nikal gaye. Doosri: search se lagbhag zero reach (9 impressions) — saari reach Home feed se.

## 3 sudhaar (agli video, Al-Baqarah 1-5)
1. **Vaada 30 s ke andar poora karo**: hook ke turant baad pehli aayat (Arabic + bhaavarth) — parichay/naam/ginti/
   shan-e-nuzul ki raayein max 30-40 s, ya aayaton ke beech chhote tukdon me. (LAGU KARO, hint level.)
2. **Ek image max ~8-10 s pehle 1 minute me** (abhi 17-21 s per image): pehle 60 s me har vaakya/sawaal par naya
   drishya ya crop/zoom (free, budget nahi badhta). (Agle round ke liye — ek waqt me 1-2 badlav, isliye abhi Prayog me.)
3. **Search ke shabd**: title ka pehla hissa wahi jo log likhte hain ("Surah Baqarah ki pehli 5 aayat ka matlab /
   tarjuma Hindi"), tags me Hindi + Roman dono; Kalam/trends me "search intent" check. 9 search impressions = abhi
   koi saboot nahi ki title kaam kar raha hai.

## "Kam data" warnings
- Retention curve / drop points: ~18 engaged viewers -> sirf HINT, pakki seekh nahi.
- CTR: 871 impressions (>500) par sirf 1 video, koi tulna nahi; 3.8% (din 3) ko "kam" ya "theek" kehna abhi jaldi.
- Subscribers 1, comments 0: koi nateeja nahi.

## Agla
- 7 din post-mortem: **1 Nov 2026 22:40 IST ke baad** (`fetch` + `reach-fetch`, ek-ek baar).
- Studio CSV (optional, ₹0): Studio -> Analytics -> Advanced mode -> video kmYyRGdykjY -> Reach tab -> Export current
  view -> CSV -> `channels/noor-e-raah/analytics/studio_csv/2026-11-01_reach.csv`.

Files: `analytics/videos.csv`, `analytics/video_kmYyRGdykjY.json`, `analytics/channel_totals.json`,
`analytics/reach/channel_reach_*_a1_2026-10-2[5-7].csv`, `stories/001_al-fatiha/long/output/timeline.json`.
