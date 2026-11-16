# 011_mehmaan-aur-bujha-chiraag — Munshi FINAL R1 (history Long), 2026-11-17

VERDICT: FIX (1 BLOCKER, free fix; 4 MAJOR image fixes, free; rest MINOR). Auto-mode STOP: none (copyright item has a clear free fix). Rs0.

## Measured
- video.mp4: 1920x1080, 30 fps, H.264, AAC 48 kHz mono, 247.48 s (<= 5:00 per DAILY_HISTORY 7e). First voice at 0.0 s.
- Loudness (ebur128): I -14.2 LUFS, TP -1.5 dBFS, LRA 3.5 LU. OK.
- Music under voice: present in all gaps measured (RMS -18 to -26 dB in gaps at 15.8, 148.2, 151.0, 163.9, 185.8 s). OK.
- SRT: 36 cues, text == script.json 36/36, starts == wav timeline (+0.45 s). Format issue: `0:00:10,13` (1-digit hour, 2-digit centiseconds) — see M8.
- Arabic on card (line 30, 186.8-192.0 s): `وَيُؤْثِرُونَ عَلَىٰٓ أَنفُسِهِمْ وَلَوْ كَانَ بِهِمْ خَصَاصَةٌ` == Tanzil 59:9 byte substring (offset 154, word-bounded, complete clause before `وَمَن`). Hindi line below, no overlap; source tag "सूरह अल-हश्र 59:9". OK.
- R1 script fixes: L19, L23, L27, L31, L34 rewritten as asked; L29 src = सहीह बुख़ारी 3798. All 6 applied.
- Depiction (every head zoomed, source images + one frame per line): NO Prophet in any frame (L7-L11, L28 = empty places / lit door). Host/wife/guest only from behind (01, 02, 14, 15, 17); children from behind / lost profile, no features (02, 15). Faces only ordinary townspeople (03, 18, 33). No angel. No RULES 2e breach.
- upload.json: title 77 chars, desc 1400, tags 154, 5 hashtags, synthetic true (DAILY_HISTORY 7), made_for_kids false, privacy private (publish_at removed by builder, fine while api_audited false), channel_id matches channel.json. Sources + Tanzil CC BY 3.0 + AI line + all 6 music credits present. name_guard: OK. Thumbnail 1280x720, matras OK, back view only.

## BLOCKER
B1. Line 4 (~21.7-27 s) SFX `shared/sfx/history/camel_bell_162811.mp3` is NOT a camel bell: per shared/sfx/history/CREDITS.md it is Freesound "Music Box 'Light Up My Life'" = a music-box version of a commercial song (RULES 10: no commercial song in any form; Noor 1c: no tune). Fix (free): remove the sfx from line 4 in script.json and re-mix audio (clips cached). Do not use camel_bell_578543 either (it is a "Church Bell").

## MAJOR (free fixes: swap image file under the line key, re-render only that clip)
M1. L7 "एक आदमी नबी ﷺ के पास आया" shows 010's `09_telling_story` = a hooded woman (Khawla scene) — wrong gender. Use `stories/009_asma-khajoor-ki-guthliyan/images/19_night_desert_road.png` (empty road into town).
M2. L18 "पत्नी ने ... चिराग़ जलाया" (night, inside) shows a DAYTIME street of men. Use `stories/009_asma-khajoor-ki-guthliyan/images/18_provisions_bag.png` (clay lamp lit beside food bundle, night interior; no glass).
M3. L33 market: glass hurricane lanterns (hanging + on ground) and a castle on the hill (RULES 2g). Use `stories/010_khawla-allah-ne-sun-li/images/19_morning_market.png` (simple palm-roof stalls, no lanterns; fits "देने के लिए अमीर होना ज़रूरी नहीं").
M4. L17 couple scene: glass hurricane lantern on the wall left of the couple. Fix: crop `17_couple_talk.png` to x 43%-100%, y 22%-79% (removes lantern, keeps both backs) and resize to 1920x1080; or accept as MINOR if the crop is too soft.

## MINOR
1. L23 "अँधेरे में पति-पत्नी ... खा रहे हों" shows an outdoor moonlit palm street; better `stories/002_ayatul-kursi/images/07_moonlit_rooftops_lamp.png` (sleeping town, one lit window).
2. L24 "मेहमान ने आराम से खाना खाया": bread on a mat in an open DAYTIME courtyard (night scene). Keep or reuse a night interior.
3. L11 and L12 use the identical image (09_mosque_wall) back to back; L12 "एक आदमी खड़ा हुआ" shows no one.
4. L15 wife at hearth: door/window show daylight in a night scene. L28 (morning) uses a night image.
5. L8 palm alley: fortress with crenellated walls top-left (2g); L13 / L25 wall sconces look like modern fittings; L03 tiled roofs.
6. L14 host image is 010's "angry_husband" (clenched fists) — reads angry for a hospitality line.
7. L30 ayah card has motion=true: parallax bends the left gold border (wavy line at ~x 10-30 px). Set "motion": false for the card.
8. video.srt timestamps `H:MM:SS,cc` (centiseconds) — YouTube may read `,13` as 13 ms (up to ~0.9 s early). Fix in history_build.py ts(): `HH:MM:SS,mmm`. Same in 010.
9. Amb `night_crickets_254270.mp3` is Freesound "Midnight train horn, with a dose of crickets": tonal bursts at ~615 Hz every ~5 s in the source (s 0, 4-5, 9-10, 14-15, 20-21, 27); used on 15 lines. Faint, not confirmable by ear here. Swap to night_crickets_268962 in the same re-mix.
10. Amb `market_crowd_93340.mp3` (L33) is "New Orleans ambience" (may carry street music/English). Swap to market_crowd_139981 in the same re-mix.
11. Thumbnail text 9 words (rule ~4); fine to keep.

## Shan-e-nuzul / fact lines (history)
- [F12/F13] L28-L29 Prophet ﷺ said Allah was pleased; 59:9 revealed about them — Bukhari 3798, 4889; Muslim 2054 — sahih.
- [F5] L13 Abu Talha "एक रिवायत में" — Muslim 2054c — sahih, hedged correctly.
- [F14] L4-L6 Muhajirin/Ansar, sharing date fruit — Quran 59:8-9, Bukhari 2325, 3780 — sahih.
