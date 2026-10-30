# Carry-over (MINOR issues to fix in pipeline)

## 001_al-fatiha (script R2, 2026-10-24) — open
- done (Kalam, 2026-10-24) | long/review/script_sheet.md header abhi "round R1" likhta hai -> agli sheet rebuild par "R2".
- done (Kalam, 2026-10-24: "क़ुरआन की लिखी किताब — मुसहफ़ — का पहला पन्ना") | script line 4: "मुसहफ़, यानी क़ुरआन की लिखी किताब, का पहला पन्ना" — TTS me atak sakta hai; chaho to "ये मुसहफ़ — यानी क़ुरआन की लिखी किताब — का पहला पन्ना है" jaisa kram (sirf bahaav, matlab wahi).
- done (Kalam, 2026-10-24: "...इन्हें देने वाले की ख़ूबियों को सराहना, यही हम्द है।") | script line 27 (MISAAL): do baar "तारीफ़" + do dash — bolne me bhaari; ek vaakya me saral karo (matlab wahi: hamd = dene wale aur uski khoobiyon ki tareef).

## 001_al-fatiha (script do-awaaz R2, 2026-10-24) — open
- done (R3 2026-10-24: note ab "line 43, 22 shabd") | script LENGTH ESTIMATE: "SAWAAL ki sabse lambi line 18 shabd" -> asal 22 (line 44); sirf note sudhaaro.
- done (R3 2026-10-24: Soaring/Quietude/River Flute shared/music/noor/ me, register + channel.json + SOURCES mile) | music: Water_Prelude + Meditation_Impromptu_02 ab shared/music/noor/_options/ me, register/channel.json path shared/music/noor/; _options ke 5 aur tracks register me nahi. Audio stage se pehle: lagne wale tracks sahi path + register + SOURCES credit (bina register = BLOCKER).
- done (R3 2026-10-24: user ne 12, 29, 90 hatayi, 11 rakhi -> 8:12) | lambai ~8:31 (~8:40 asli) vs ~8:00 — user approval par Kalam ki optional cuts (lines 29, 12, 90, 11).

## 001_al-fatiha (script do-awaaz R3, 2026-10-24) — open
- open | long/review/script_sheet.md: (b) ke neeche "Line 28: Bismillah..." -> line 27; (c) notes "Line 96 viewers se sawaal" -> line 95 (sirf number).
- open | audio stage: line 14 Soaring -> Quietude ≥1 s crossfade (shared RULES 3), dialogue ke beech nahi; line 23 (Quietude) aur 88 (River Flute) par track jaari rahe, restart nahi.
- open | audio stage: wind_birds_petebuchwald_288899 aur gentle_breeze me paani ki awaaz nahi (kaan se), Soaring me beat/percussion nahi (RULES 1c) — mix me jaancho.

## 001_al-fatiha (images R2, 2026-10-25) — open
- open | long/review/tts_report.md purana hai (12:50, "Whisper OK 53/62"); lines.json 62/62 tts_ok + .ok sab maujood. Report refresh karo (sirf bookkeeping, ₹0).
- open | 08_predawn_houses: darwaze ke daayein (x~675-700, y~510-560) safed plaster ka khamba/buttress, upar gol gaanth. Munshi: deewar ka hissa, insaan nahi. Agar user ko aakaar dikhe: free rect {fx 0.249, fy 0.5, zc 2.2} (x 35-655, ghar + darwaza + lantern rehte hain), delogo nahi.
- open | 24_crescent_night_valley: rect window (x 0.445-0.996) tent se bahar, par usme ab bhi laal chattan/mesa (American look, jo 08 me user ne hataya). End screen hai, niyam nahi tootta; agli kahaniyon ke prompts me "no mesas, no red sandstone" pehle se likho.
- open | 06 khidki ka chiraag phir diya-jaisa (R1 note 5); agle prompts me "spouted Arabian clay oil lamp".

## 001_al-fatiha (FINAL R2, 2026-10-25) — open
- open | first audible word 1.05 s (line placed 0.80 s, TTS wav has ~0.25 s lead breath); RULES 13 ≤1.0 s. Next video: LEAD 0.7 or trim TTS lead silence.
- open | thumbnail main Hindi text ≈8% of frame height (rule ~12%); next thumbnail bigger font / fewer words per line.
- open | metadata chapter ayah 5 at 4:43 begins 0.4 s before line 59 ends; chapter time = swoosh time floored (4:44), not cue time.

## 002_ayatul-kursi (images R1, 2026-10-30) — open
- fixed | 12_bedtime_room_lamp: glass-chimney lamp (STYLE_NOOR 1 "never a modern lantern") -> fixed free by a fixed crop in images.json (rect fx 0.75 fy 0.5 zc 1.55 = x 489-1370, lamp at x~390 out of frame); Munshi final to confirm on the render.
- open | 04_date_palm_path: tiny metal wall lantern at ~(912,450) (small, mid-ground; accepted). Next prompts: "no lantern, only an old clay oil lamp".
- open | 06_oasis_spring / 08_vast_panorama / 11_sunrays_clouds are more saturated/illustrated than the matte set; 08 and 11 show snow peaks/pine (not Arabian, used only for "vastness"). Next prompts: keep one matte painted family, Arabian landscapes only.

## 003_al-ikhlas (images R1, 2026-10-30) - open
- open | 08_empty_room_morning_b: rect fx .7 drops the window; optional fx 0.4 fy 0.6 (free).
- open | 03_makka_valley_night: tiny warm window glows on far houses; accepted.
