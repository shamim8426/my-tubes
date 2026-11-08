# Reality Check - Asli: VIDEO STUDY (6 videos) - 2026-11-07

Rs 0. yt-dlp (no login/cookies, 720p max) -> `study/rc/` (git-ignored), ffmpeg scene-detect, faster-whisper small (CPU), ebur128. Sirf tareeke likhe hain (RULES 12c HARD): koi frame/script/title/thumbnail hu-ba-hu nahi; frames Gemini ko nahi diye; downloaded files analysis ke baad delete.
Videos (link `research/study_candidates_2026-11-07.md` me): V1 Kurzgesagt asteroid (12:43), V2 Real Engineering DART (13:26), V3 Astrum DART (14:31), V5 Dhruv Rathee black hole, Hindi (18:38), V6 Vigyan Recharge asteroid defence, Hindi (15:54), V9 Veritasium electricity (14:48).

## 0. Naap ki seemayein (imaandari)
- Scene-detect (threshold 0.3) sirf hard cuts pakadta hai; dissolve, lagataar animation/camera move, aur ek jaisi dikhne wali cuts chhoot jaati hain -> cuts/min **kam-se-kam** hai. V9 ka ek 171 s ka shot ek hi set ka talking footage hai (cuts miss).
- Whisper `small` Hindi me phrase-level timestamps deta hai aur text kharab hai: V5/V6 ke **pauses aur exact wpm bharosemand nahi** (V5 first-60-s ~170 words, V6 ~150 wpm sirf andaza). English videos ke numbers pakke hain.
- Music vs voice: stems nahi hain, isliye "bolte waqt music kitna neeche" naap nahi sakta. Maine voice-RMS (-15.7 se -21.7 dBFS) aur >0.7 s pauses ke beech ka RMS (music bed + room) compare kiya = upper-bound.
- Sponsor/ad hisse numbers me shaamil hain (nonvoice). 6 videos = chhota sample; "engagement" retention nahi hai.

## 1. Har video ka chhota card
| | V1 Kurzgesagt | V2 Real Eng. | V3 Astrum | V5 Dhruv (Hindi) | V6 Vigyan (Hindi) | V9 Veritasium |
|---|---|---|---|---|---|---|
| Lambai | 12:43 (content 0:08-11:18; end me 85 s game promo) | 13:26 (end me ~70 s sponsor) | 14:31 (sponsor 0:00-0:23 + 13:00-14:12) | 18:38 | 15:54 | 14:48 (sponsor 0:00-0:03 mention + 13:20-14:45) |
| Cuts total, cuts/min | 90, 7.1 | 158, 11.8 | 82, 5.7 | 314, 16.9 | 233, 14.7 | 80, 5.4 |
| Avg / median shot (s) | 8.4 / 6.0 | 5.1 / 2.6 | 10.5 / 4.5 | 3.5 / 1.0 | 4.1 / 2.1 | 11.0 / 4.2 |
| Shots >8 s, >15 s | 27, 12 | 23, 12 | 32, 21 | 36, 14 | 33, 12 | 27, 13 |
| Pehle 60 s ke cuts vs baaki (cuts/min) | 5 (ad ke saath) vs 7.3 | 14 vs 11.6 | 9 vs 5.4 | 19 vs 16.7 | 19 vs 14.4 | 10 vs 5.1 |
| Words/min overall / articulation | 169 / 194 | 143 / 164 | 145 / 177 | ~100*/~138* (*unreliable) | 150 / 175 (rough) | 167 / 189 |
| Sentence length (words) mean / p90 | 7.9 / 12 | 12.4 / 17 | 14.7 / 18 | n/a | ~11 / 18 | 12.3 / 18 |
| Pauses >=0.25 s: per min, median, p90 | 18, 0.49 s, 0.78 s | 14, 0.56, 0.79 | 14.6, 0.64, 1.02 (67 pauses >=0.8 s) | n/a | n/a | 12.5, 0.52, 0.87 |
| Pauses >2 s (poori video) | 2 | 1 | 3 | ? | ? | 4 |
| Loudness LUFS / LRA / peak | -16.0 / 2.6 / -2.3 | -21.7 / 2.8 / -3.9 | -20.1 / 4.3 / -0.2 | -16 (peak +0.8) / 4.3 | -17.1 / 4.8 / +0.4 | -15.8 / 5.1 / +0.1 |
| Voice vs pause-RMS (dB) | 7.9 | 3.6 | 8.3 | ~0 (clips ki awaaz) | ~0.3 (clips) | 7.8 |
| Hook (pehle 10 s) | 8-s ad, phir "imagine" stadium-size asteroid 2 hafte me; fir real near-miss + "koi plan nahi" | Exact date + weight + speed ka ek event, number-led | NASA live launch footage, mission ka maqsad 23 s ke baad | "2014 me ... film" yaad dilao, phir mystery | "maan lo" bada patthar aa raha, stake | Ek thought-experiment circuit + sawaal 0:03 par, "jawab comments me likho" 0:46 par |
| Mukhya jawab/reveal kab | ~10:59 (86%) "bach gaye" simulation | 10:17 (77%) number | 7:27 (51%) number | video ke ant me | ant me, user se raay | 11:36 (78%) |
| Source/credit on screen | nahi (sirf "not to scale" tag) | numbered [n] refs + "Credits: ASI/NASA" | "Credit: ..." lines, patron list | "Courtesy: ..." corner label | kam/nahi dikha | naam caption + aakhir me patrons |
| "Pata nahi/unknown" | nahi | nahi | "+/- 2 minutes" margin, size "unknown" | n/a | n/a | nahi |
| Thumbnail | 2 shabd + 1 label, bada illustrated object + laal teer | 2 shabd, spacecraft close-up, do-rang text | "NO EXPLANATION" + BEFORE/AFTER do photos | 3 shabd + chehra + haath (face-led) | 4 shabd + chehra + asteroid/missile | 5 shabd, diagram par text |

## 2. Voice (English pakke, Hindi andaza)
- Awaaz **lagataar chalti hai, dheemi nahi**: 143-169 wpm, articulation 164-194. Sabse tez (V1, V9) ~170 wpm par chhote wakya (8-12 words); V2/V3 ~145 wpm par lambe wakya (12-15).
- Pause: median 0.5-0.64 s, 90% pauses <=1.0 s, poori video me 1-4 pauses hi 2 s se lambe (jo hain wo scene/b-roll badalte waqt). Pause per min 12-18.
- Pehla shabd 0.0 s (6/6, V5 me ek shabd ka namaste).
- Emphasis ka tareeka: chhote tukde (ek-do shabd ki line), number ko wakya ke ant me, ek tez pause ke baad naya wakya. (Tareeka, shabd nahi.)
- Tone: seedha, thoda dramatic (V1), engineering-calm (V2), conversational (V9), josh wala (V5/V6).
- Hinglish mixing (V5/V6, rough): ~30-40% shabd English (system, mission, momentum, successful, comment, nuclear bomb) Hindi me ghule hue; English technical term English me hi bolte hain; kisi ne unka Hindi anuvaad nahi kiya. V6 aakhir me user se sawaal ("kya sahi laga/kya galat comment karo").

## 3. Edit rhythm
- Animated 2D (V1) ya CGI + NASA footage (V2/V3): 5.4-11.8 cuts/min; face-led Hindi (V5/V6): 14.7-16.9 cuts/min (har ~3.5-4 s, median 1-2 s: inserts, text cards, clips).
- Pehle 60 s me cut-rate 1.3-2x (V2, V3, V5, V6, V9); sirf V1 me ad ke karan kam. Aakhri 1.5-2 min me cuts girte hain (promo/end).
- Beech me rhythm: 2-min bins me cuts 4 se 52: tez bursts ke baad shaant stretch.
- 8 s se lambe shots 2/min tak (23-36 per video), lekin tab shot ke andar animation/camera-move/orbit chal rahi hoti hai. 15 s+ shots 12-21 per video: ye retention-risk (V3 me 21 lambi NASA clips).
- Transitions: sab hard cut; kuch slow dissolve; whip/flash lagbhag nahi. V1 me smooth zoom/pan animation.

## 4. Graphics (kya dikha)
- V1: 2D flat vector, gehra navy/purple background + neon gulabi/narangi/teal; orbit diagram "not to scale" tag, number chip ("x 3,000"), date chip ("2019"), before/after side-by-side, zoom-in circle callout, countdown clock card, map + arrow.
- V2: 3D render + asli NASA photo/video + patli safed line diagram kaale par; title label ("TRAJECTORY", "BINARY SYSTEM") top-left chhota; numbered ref [n] kone me; distance counter overlay.
- V3: CGI + NASA frames; simple annotated plots (hare dots + legend), "32 minutes!" ka chhota label orbit ke upar, 3-frame before/after strip (+22 min/+5 hr/+8 hr), credit kone me.
- V9: live-action experiment + patli rangeen field-lines wale 3D/2D diagram kaale par, equation card, expert ka naam caption, scale diagram ("wire spacing not to scale").
- V5/V6: presenter ke peeche space background, numbered header cards ("1. ..." peele highlight chip me), article screenshot, formula board; V5/V6 films ke clips bhi use karte hain (hum nahi karenge).
- Text: chhota (1-4 shabd) label, number bada; ek rang accent (peela/hara/gulabi); sab me kaala/gehra background. Source label hamesha chhota, kone me.

## 5. Structure
- Hook (0-60 s): concrete stake/event -> "ye sach hai" ka saboot (real example) -> vaada (is video me kya milega). Context/itihas baad me.
- Mukhya jawab 51-86% par; usse pehle 2-3 chhote sawaal/number chalte hain, aur "jawab pehle likho" (V9) jaisa engagement device bhi.
- Koi saaf chapter badge ya midpoint-recap nahi dikha (6/6).
- Aakhir: V1 simulation ka payoff + game promo; V2/V3/V9 sponsor + patrons + "pichhli video"; V6 sawaal comments ko. Generic "like subscribe" lagbhag nahi.
- Sponsor/ad: 4/6 me shuru ya aakhir me (30 s - 90 s).
- Title ka vaada: V3 ka thumbnail "koi explanation nahi" kehta hai par video 7:27 par explain kar deta hai (vaada tut-ta hai). V2/V9 ka vaada poora nibhta hai.

## 6. COMMON PATTERNS (4+/6)
1. Pehla shabd 0 s par, koi greeting/logo intro nahi (6/6).
2. Pehle 10 s me ek concrete scenario/event/number (6/6).
3. Awaaz lagataar 143-175 wpm, pause median ~0.5 s, 2 s se lambi dead air nahi (English 4/4 pakka).
4. Pehle 60 s me cut-rate average se zyada (5/6).
5. Mukhya jawab runtime ke 51-86% par, beech me chhote reveals (4/4 jahan naap saka; Hindi 2 me ant me).
6. Gehra/kaala background + ek accent rang + chhote text labels + "not to scale"/credit kone me (5/6).
7. Sponsor/promo 4/6 (shuru ya aakhir).
8. Thumbnail: 2-5 shabd bade bold caps, ek bada focal object, 1-2 rang (6/6); face sirf 2 Hindi me.
9. Loudness -15.8 se -22 LUFS (6/6 hamare -14 se shaant).
10. Koi saaf chapter badge nahi (6/6).

## 7. DIFFERENCES
- Cuts/min: face-less animation/CGI 5-12 vs face-led Hindi 15-17.
- Wakya: V1 7.9 words (chhote) vs V3 14.7 (lambe).
- Source: V2/V3/V5 credit labels vs V1/V9 nahi. Uncertainty ("+/- 2 minutes", "unknown") sirf V3 me.
- Loudness: V2 -21.7 (shaant) vs V1/V9 -16.
- Hook: V1 (hypothetical) / V2 (real event + number) / V9 (sawaal, jawab pehle comments me).

## 8. Hamare liye kya lagu karein (20 min, face-less, Hinglish)
Voice
- TTS 150-165 wpm; 20 min ~ 3,000-3,300 shabd (ye 6 videos ke 12-19 min se lambi hai, isliye beech me variety zaroori).
- Wakya mean 8-13 shabd, p90 <= 18; har 1-2 min me ek 2-4 shabd ki chhoti line.
- Pauses: comma/full-stop se median 0.5 s, 12-18 pauses/min; 0.8-1.0 s sirf zor ke liye (~2/min); 2 s+ sirf scene badlte waqt, max 1-2 poori video me.
- English technical words English me, baaki Roman Hindi; Hindi anuvaad nahi.
Edit rhythm
- Cut + naya visual: avg shot 4-6 s (10-14 cuts/min static images ke saath), diagram/orbit animation me 8-15 s chal sakta hai agar andar motion ho.
- Pehle 60 s me 12-18 cuts; hook ke baad 6-9 cuts/min; mukhya jawab ke paas burst; aakhri 60-90 s dheema, end screen ke liye khali.
- 15 s se lamba koi shot nahi (retention-risk, V3 jaisa).
Graphics list jo hume banana hai (priority)
1. Orbit animation (Dimorphos Didymos ke around) + period label (11 h 55 -> 11 h 23).
2. Scale-compare cards (asteroid vs imarat/shehar) + "not to scale" tag.
3. Number card: bada number + chhota unit chip ("33 MIN", "x" multiplier).
4. Before/After pair frame (2 panel side-by-side) + 3-frame timeline strip.
5. Trajectory/miss-distance diagram, patli safed lines kaale par, label top-left.
6. Date/timeline chip + countdown clock card.
7. Credit/Source label (kone me, 2-3 s) + numbered [n] jo description ke source list se milta hai.
8. Verdict card (Sach / Aadha sach / Abhi unknown).
9. Ek accent rang (peela ya narangi), navy-black background; ek video, ek theme.
Hook / structure
- 0-10 s: concrete event + exact number; 10-30 s: stake + vaada; mukhya jawab ~70-78% par; beech me har 2-3 min chhota number/sawaal; ek "pehle apna andaza likho" jaisa comment prompt 1:00 se pehle (V9 se seekha tareeka); aakhir me ek specific sawaal.
- Sponsor nahi: last 60-90 s end screen. Chapter badge/midpoint reset ko `[test]` rakho (studied me nahi).
Thumbnail
- 2-4 shabd bold caps (Roman Hinglish), ek bada object (asli NASA/asteroid), 1-2 rang, face nahi; ek variant number-led, ek before/after pair-led, ek diagram-led (pair/diagram dono studied videos me chale).
- Title ka vaada pehle 60 s me poora; "koi explain nahi kar sakta" jaisa jhootha vaada nahi (V3 galat udaharan).
Loudness
- -14 +/-1 LUFS (studied sab usse shaant), peak <= -1.4 dBFS (3 videos ka peak >= 0 dBFS = clip risk); LRA 3-5.
Music
- Pauses me music thoda upar uthne do (voice RMS se 4-8 dB neeche), bolte waqt aur neeche; asli level humare stems se naapna hai.

## 9. Kya NAHI karna
- Films/Hollywood clips, presenter-face jaisi Hindi channels ki nakal (V5/V6) - copyright + hamara face-less brand.
- Sponsor-pehle ya 1+ min ka end ad.
- Title/thumbnail me "explain nahi ho sakta" jaisa vaada jo video 50% par tod de.
- 15 s+ ka ek shot ya ek hi NASA clip dobara dobara.
- Peak 0 dBFS ke upar; 2 s+ dead air; generic "like/subscribe" CTA.
- Kisi ka frame, script wording, thumbnail layout hu-ba-hu, ya channel naam metadata me.

## 10. STYLE_GUIDE.md me kya badla
Section 12 + inline labels `[video-study]` (pace, pauses, shot length, cut-rate, music, loudness, hook, reset, source). Midpoint reset / chapter badge / music 18-22 dB ko "unverified [test]" kiya.
