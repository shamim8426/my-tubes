# Reality Check - Asli: STYLE GUIDE (science explainer, Hinglish, face-less)

Date: 2026-11-07. Status: PROPOSAL, nothing applied until the user approves. Rs 0, no download, no video watched.
Only principles; no frame, script, title or thumbnail of anyone is copied (RULES 12c HARD, 10, 12a).

## 0. Honest evidence note (padho pehle)
- `yt_read.py` ka quota aaj khatam tha aur download ki ijazat nahi hai, isliye is guide me **koi measured retention/CTR data nahi hai**.
- WebSearch ne zyada tar creator-marketing blogs diye (vidIQ, 1of10, AIR Media-Tech, subscribr, outlierkit...). Unke numbers (jaise "2.3x CTR", "20% higher retention") **unverified** hain; main unhe sirf `[blog]` label ke saath, "hypothesis" ki tarah likh raha hoon.
- Labels: `[blog]` = web article, unverified number; `[craft]` = standard video/audio craft ya repo me already tested learning; `[repo]` = hamari STYLE_LIBRARY / RULES se; `[src]` = primary/official source (facts ke liye); `[test]` = pehli 3 videos me A/B karke Nigraan se check karna hai.
- Isliye har rule ko "starting default" maano; Nigraan ka 48 h / 7 din data (50%+ retention pehle 30 s, avg view duration, CTR) rule ko badlega. 500 impressions se kam = kam data.
- Hindi Hinglish-specific: 2 Hindi videos (Dhruv Rathee, Vigyan Recharge) ab padhe gaye [video-study], dekho section 12 (search me Hinglish title/thumbnail ka koi study nahi). Hindi ke liye points `[craft]` + `[test]` hain.

## 1. Kyun chalte hain high-performing science explainers (7 karan)
1. **Ek sawaal, ek vaada.** Title+thumbnail ek saaf sawaal uthate hain; pehle 30 s me wohi sawaal "tension" ban jaata hai; video us vaade ko nibhata hai. Jhootha vaada = early cliff `[blog]`, aur RULES 13 me misleading = BLOCKER `[repo]`.
2. **Bade scale ya khatre se shuru, phir hope.** Ek analysis kehti hai ek bade explainer channel pehle bade khatre/andhere sawaal ko dekhta hai aur phir umeed se jawab deta hai, isse optimism "kamaya hua" lagta hai `[blog, opinion]`. Hamare liye: DART ki kahani "bachne ka tareeka mil gaya, aur kaise" wali hai.
3. **Har wakya agle wakya ka sawaal ya jawab deta hai.** "Resolution rate": har line pichhli line ka kuch poora kare ya naya sawaal khole `[blog]`. Script ka sabse bada rule.
4. **Dikhana, sirf bolna nahi.** Jo bola jaata hai wahi usi second dikhta hai (RULES 13 + STYLE_LIBRARY 0.6) `[repo]`.
5. **Imaandari + exact numbers.** "33 minute (+/-1)" jaisa exact number bharosa banata hai. Hamare fact: Dimorphos ka orbit DART se -33.0 +/- 1.0 min badla (Thomas et al., Nature 616, 448, 2023); sirf momentum se ~7 min ka andaza tha, baaki ejecta ka kaam `[src: ui.adsabs.harvard.edu/abs/2023Natur.616..448T]`. Ye "andaza galat nikla, kyun?" wala reveal hai = natural curiosity gap.
6. **Rhythm: shant explanation + beech-beech me energy bursts** (pattern interrupts) `[blog + craft]`.
7. **Ek hi tone, ek hi visual bhasha** (brand): viewer pehle 3 s me pehchaan le `[craft]`.

## 2. Title patterns (Hinglish)
Rules `[blog + repo RULES 13 + bible 3]`:
- Pehle 40 characters me hook + asli search word (concept ka naam: "asteroid", "DART", "planetary defence", "Kessler syndrome"); mobile truncation.
- Total ~55-70 chars + suffix `| Reality Check - Asli` (suffix cut ho sakta hai, isliye keyword suffix se pehle).
- Roman Hinglish, ek sawaal ya ek surprising number. Ek hi bhavna (curiosity), ALL CAPS sirf 1 shabd, max 1 emoji ya nahi.
- Formats (alag-alag try, `[test]`):
  - Sawaal + vaada: "Kya Hum Asteroid Ko Rok Sakte Hain? DART Ka Asli Sach"
  - Number + shock: "33 Minute Ka Fark: NASA Ne Ek Asteroid Ka Raasta Kaise Badla"
  - Andaza galat: "Asteroid Rokna Aasan Tha? Asli Science Ulti Nikli"
  - Kitna-sach: "Asteroid Se Bachna: Kitna Sach, Kitna Jhoot" (Bible 3 "verdict" format)
- Avoid: movie name as the headline (bible 2: at most spoken hook), "SHOCKING/100% sach", misleading claims, Hindi Devanagari + English dono ek hi title me bhar dena (confusing search), ?? !!! stack, duniya khatam jaisa jhootha darr. Politics/hot topics nahi.
- Hindi search ke liye description me Devanagari line bhi ("क्या हम क्षुद्रग्रह को रोक सकते हैं?") `[test]`.

## 3. Thumbnail
General `[blog]` (sab sources ek jaisa kehte hain; numbers unverified): 3-5 shabd max (hum 1-3), ek focal point, high contrast, phone size (~200x112 px) par padhne layak. RULES 13: 160x90 downscale check, max 4 words `[repo]`.
Hamare liye:
- Ek bada object (asteroid / spacecraft / grah), ek rang accent, andhera background. Face nahi.
- Text: 1-3 shabd, Roman Hinglish ya Devanagari dono padhe jaate hain; bada bold font (Mukta ExtraBold), letter height >= 12% (RULES 6). AI se akshar kabhi nahi; text overlay Pillow/raqm ya Chromium se `[repo STYLE_LIBRARY 11]`.
- Number thumbnail me kaam karta hai ("33 MIN") kyunki chhota aur surprising `[craft]`.
- Thumbnail vaada = video ke pehle 60 s me dikhna (RULES 13).
- Real NASA image (public domain) ko crop+contrast; credit description me. Koi movie poster/still nahi.
**3 concepts, asteroid-defence (alag style, kisi ka copy nahi):**
- **A. "Do rastey" (diagram):** kaala background, ek seedhi patli safed line jo ek chhote chamakte neele Earth ki taraf jaati hai aur beech me ek chhota asteroid se ek laal-narangi moda hua raasta. Text: "RUK GAYA?" (do shabd, peela). Style = clean science diagram.
- **B. "Number card":** bada "33" (peela, poori height ka 45%) aur chhota "MIN" ke neeche; peeche dhundhla DART-impact ka real NASA image, dim. Style = number-led.
- **C. "Close crater photo":** ek ubad-khabad asteroid (real/CC image) ka extreme close-up, ek taraf se garam narangi roshni, baaki andhera; ek neela ghera "BACH SAKTE HAIN?" (3 shabd). Style = moody object-portrait.
(Nigraan ke saath A/B: Long ke liye 3 variants rakho, YouTube "Test & compare" se `[test]`.)

## 4. Hook, structure, pacing (18-20 min)
### 4.1 Pehle 30 s `[blog + repo RULES 13]`
- 0-1 s: visual hook (move karta hua object / number / dhamaka), pehla shabd 1.0 s ke andar (6/6 videos me pehla shabd 0.0 s par; sirf ek me 1 shabd ka namaste) `[video-study: confirmed]`. Koi greeting/logo intro nahi.
- 0-10 s: title ka vaada sach saabit karne wala ek concrete example ("Ek spacecraft ne ek asteroid ko 22,000 km/h ki raftaar se ... aur uska orbit 33 minute badal gaya", fact [F#] dossier se).
- 10-20 s: aapke liye kyun zaroori (stake), 20-30 s: "is video me hum teen cheezein dekhenge" + pehla open loop. Context/itihas baad me.
- Hook pattern `[video-study]`: 6/6 pehle 10 s me ek concrete scenario/event dete hain ("imagine ... 2 hafte me", exact date+speed, ek thought-experiment sawaal); koi bhi context/itihas se shuru nahi karta. Pattern (3 me se ek): (a) **Andaza vs nateeja** (7 min ka andaza, nateeja 33), (b) **Stake** (kya ho agar hum kuch na karein), (c) **Sawaal bina jawab** (answer 14:00 par).
### 4.2 Structure (template, minutes) `[craft + repo STYLE_LIBRARY 10]`
0:00 hook | 0:30 vaada + roadmap | 1:00 ch1 (maamla kya hai, scale ek number card) | 3:00 **reveal #1** (pehla "arre!") | 5:00 ch2 (kaise kaam karta hai, diagram) | 7:30 reveal #2 | 10:00 ch3 (jo galat ho sakta hai / limit) | 12:30 reveal #3 | 15:00 ch4 (aage kya, India/duniya) | 17:30 verdict card ("Sach / Aadha sach / Abhi pata nahi") | 18:30 recap 3 points + ek sawaal | 19:00 end screen (last 20 s khali).
- Har 2-3 min me naya sawaal/reveal (bible 4); har chapter ke ant me agle chapter ka mini open loop `[blog]`.
- Midpoint reset: studied videos me koi saaf recap/reset nahi dikha; unme badi baat 51-85% runtime par aati hai aur beech me chhote naye sawaal/numbers `[video-study]`. Hamare liye optional `[test]`.
- Chapters (timestamps description me): 6-9 chapters; chapter badge on screen (STYLE_LIBRARY 10) `[repo]`.
- "Pehle jaisa jawab": unknown ko "abhi pata nahi" bolna structure ka hissa hai (section 7).
### 4.3 Pacing
- Bolne ki raftaar: 6 videos me English 143-169 words/min overall (articulation 164-194), Hindi presenter ~150-175 `[video-study: confirmed]`; Hinglish TTS ~150-165 wpm rakho; TTS ko 1.0x par rakho; pauses: median 0.5-0.64 s, 12-18 pauses/min (>=0.25 s), 0.8-1.0 s sirf zor dene par `[video-study: confirmed]`; 18-20 min = ~2,700-3,200 shabd. Measured TTS speed se script likho (RULES 15 jaisa).
- Visual change: har 4-8 s kuch badle (naya card, zoom, label, cut); shot 8 s se zyada bina move nahi (RULES 13). Measured: median shot 2.6-6 s (CGI/animation videos), average 5-11 s; 8 s se lambe shots 2/min tak aate hain par tabhi jab shot ke andar lagataar motion/animation ho `[video-study]`. Hamare static images par 4-8 s rule rakho `[test]`.
- Pehle 60 s me cut-rate average se 1.3-2x (5/6 videos: 9-19 cuts pehle 60 s me), aakhri ~90 s me dheema `[video-study]`. Beech me bursts: per-2-min cuts 4-52 ke beech jhoolta hai `[video-study]`.
- 2 s se lambi dead air kisi video me nahi (6 me se sirf 1-4 pauses >2 s poori video me) `[video-study: confirmed]`; reveal se pehle 1 s silence kisi me naap me nahi mila, `[test]`.

## 5. Editing (face-less, low budget)
| Cheez | Niyam | Label |
|---|---|---|
| Visual order of preference | (1) apne diagram/animation (HTML/CSS/matplotlib/Chromium), (2) NASA/ESA public-domain footage & images (licence row `shared/assets_license.csv`), (3) Wikimedia CC with credit, (4) Cloudflare flux free image, (5) paid image sirf last | repo RULES 15 |
| Mix | ~50% diagram/animation, ~30% real footage/photos, ~15% number/text cards, ~5% AI image | craft, `[test]` |
| Text on screen | ek hi idea; keyword accent colour; ek line 3-6 shabd; chhote source credit bottom-left | repo STYLE_LIBRARY 10 |
| Captions | ek line, neeche-beech, safe area (bottom 20% / right 15% Shorts), spoken word bright | repo |
| Zoom/punch-in | key object par 1.08-1.16, ek scene me ek | repo edit_fx |
| Parallax | sirf photo/NASA still par; akele kaafi nahi (bible 4) | repo |
| Transitions | hard cut + 4-6 frame dissolve; "dip to black" sirf chapter badalne par; whoosh nahi | repo |
| Music | Pauses me music voice RMS se sirf 4-8 dB neeche mila (music pauses me upar uthta hai); bolte waqt ka asli level stem ke bina naap nahi paaye; 18-22 dB number `[blog]` UNVERIFIED, starting default rakho aur ear/LUFS se check karo | video-study partial |
| SFX | sirf soft pop (text), low thud (impact), 14-20 dB neeche | repo |
| Colour grade | ek cool-neela space grade + ek warm accent (narangi/peela); edit_fx `none` ya `soft_glow` | craft |
| Loudness | 6 videos: -15.8 se -22 LUFS, LRA 2.6-5.1, 3 videos ka peak >= 0 dBFS; hamara -14 +/-1 / peak <= -1.4 theek aur safer (YouTube normalise karta hai) | repo + video-study |
| Theme | har video ek theme: dark-neon ya light-sketch; ek video me mix nahi | repo STYLE_LIBRARY 10 |
18-20 min tak dhyaan kya rakhta hai: (1) naye reveal ka rhythm, (2) har scene me kuch naya dikhna, (3) chapter badge se "main kahan hoon" ka ehsaas, (4) beech me quiet-loud variation, (5) aakhir me payoff jo hook me bola.

## 6. Retention killers aur fixes
| Killer | Fix |
|---|---|
| Lambi intro/channel pehchaan pehle | 0-1 s visual hook, branding sirf end me |
| Context/itihas pehle | pehle example/stake, itihas 1:00 ke baad |
| Ek jaisi awaaz-lay (monotone TTS) | punctuation se pauses, emphasis words, har 2 min me lay badlo (section 8) |
| Static image 8 s+ | motion/zoom/pan ya card badlo |
| Text ki deewar | 1 idea, 3-6 shabd |
| Jargon bina samjhaye | pehli baar me ek line ka matlab + ek analogy |
| Jhootha vaada | title/thumbnail ka vaada 60 s me dikhao |
| 8-10 min ka sag | midpoint reset + number card + reveal #2 |
| Lagataar ek hi rang/music | chapter-wise tone badlo |
| Aakhir me kamzor | verdict card + ek sawaal comment ke liye (RULES 13) |
| Sirf hum bol rahe, koi source nahi | source cards (section 7) |

### 6.1 Shorts ke 3 angle formats (max 40 s, RULES 13/15) `[repo + craft]`
1. **Andaza vs nateeja (hook in 1 s):** 0-1 s bada number "7 -> 33" + bolo "Andaza 7 minute ka tha." 5-30 s: do cheezein dikhao, ant me sawaal "Baaki 26 minute kahan se aaye?" **jawab Long me** (no-reveal rule).
2. **Myth/sach flash:** "Kya asteroid par bomb girane se kaam banta hai?" 1 s visual (blast diagram); 3 quick points; ant: "Asli jawab alag hai, poora video link me."
3. **Loop:** aakhri line pehli line ka seedha antim hissa ("... aur isi liye pehla sawaal wapas aata hai: kya hum bach sakte hain?"), last frame = pehla frame, taaki auto-replay se watch-time badhe `[craft, test]`.
Sab: pehla frame asli visual (no title card), pehla shabd 0.5 s ke andar, captions 15%-85% height ke andar, last 3 s CTA nahi; "Related video = Long" manual Studio.

## 7. Credibility
- Source card (har major claim par): chhota "Source: NASA / Nature 616 (2023)" bottom-left 2-3 s; paper ka title page ek card me, key line highlight (STYLE_LIBRARY 10) `[repo]`.
- Description me sources ki puri list (channel promise, bible 4).
- "Pata nahi / abhi unknown" bolna: ek line me ("Ye abhi koi nahi jaanta; sabse behtar andaza ye hai ...") + screen par "UNKNOWN" label. Verdict table: Sach / Aadha sach / Sach nahi / Abhi unknown (scout file ke jaisa) `[repo]`.
- Numbers ke saath uncertainty ("+/- 1 minute"); "andaza" vs "naap" ka fark.
- Galat fact mila = pinned correction + description fix usi din (channel RULES).
- Movie ka zikr sirf bolkar, ek line se zyada nahi; koi clip/poster nahi.

## 8. AI voice ko natural banana `[craft + repo tts_pronunciation]`
- Script chhote wakya (8-18 shabd), ek wakya ek idea. Lambe wakya TTS me saans todte hain.
- Punctuation = pause: comma ~0.2 s, full stop ~0.4 s, naya para ~0.6 s; reveal se pehle `...` ya alag line.
- Emphasis: zaroori shabd wakya ke ant me rakho; CAPS ya `*star*` TTS-prompt me sirf agar engine support kare (pehle chhota test).
- Pronunciation: `shared/tts_pronunciation.md` me asteroid, DART, Dimorphos ("dai-MOR-fos"), Didymos, Apophis, Kessler; ek **glossary test clip** har naye video ke pehle (ि ी ं ्र wale Hindi shabd bhi, STYLE_LIBRARY 11).
- Hinglish: English technical words English me, baaki Hindi Roman me; ek hi script me do spelling nahi.
- Lay badlo: 1-2 jagah dheema (reveal), 1-2 jagah thoda tez (list); chhoti "filler" reaction lines ("Ruko ...", "Ab dhyaan se suno") sirf kam.
- Voice ek hi rakho (bible 5 abhi TODO: user decision).

## 9. Hamare tools se mapping (existing vs gap)
**Already hai:**
- `tools/edit_fx.py`: colour grade, vignette, grain, punch-ins, shake, transitions (cut/whip/flash/dip), text styles (title/tag/note/pop), SFX + ambience (`edit_plan.json`). Reality-check `EDIT_STYLE.md` abhi template khaali hai.
- `scripts/make_short.py`: Shorts build, scene cache, captions (Hindi captions ke liye PC par build, cloud nahi).
- `tools/parallax.py` + `tools/motion_check.py`: 2.5D parallax, eased zoom/pan.
- `shared/style_library/long_video_make_final.py`: 16:9 long builder with chapter badge, Whisper word-time action sync, Chromium Hindi captions, loudnorm.
- `scripts/html_scene.py`, `scripts/html_video.py`, `scripts/kinetic_short.py`: HTML/CSS/Chromium based animated cards (diagrams ke liye base).
- `tools/text_pil.py` (Pillow+raqm Hindi), `scripts/cf_image.py` (free images), `scripts/gemini_tts.py`, `tools/splice_video.py`, `tools/learn.py`, `scripts/story_budget.py`, `tools/name_guard.py`.
**Gap (naya banana):**
1. **Science diagram/animation library:** orbit (Dimorphos around Didymos, period change), trajectory miss-distance, scale bars, timeline, bar/number reveal, labelled-arrow scenes; HTML/SVG + Chromium ya matplotlib, parametric JSON se (`shared/style_library/`). Sabse bada gap.
2. **NASA/ESA/Wikimedia fetcher + licence logger:** official image/video ki public-domain/CC check, `assets_license.csv` row apne aap, credit text auto.
3. **Source card + number card + verdict table + chapter badge** reusable templates (16:9, Hinglish).
4. **Script -> scene plan -> timing tool for 18-20 min** (word-count/WPM check, "naya reveal har 3 min" linter, "8 s se zyada ek shot" linter).
5. **Long (16:9) builder jo `long_video_make_final.py` ko science scenes ke saath jodta ho**, cache aur range re-render (`splice_video.py`) ke saath.
6. **TTS glossary test + pronunciation file** (reality-check ke naye shabd).
7. **Thumbnail builder (16:9, Hinglish text, number-card, 160x90 check)**, jugnu thumbnail code se alag.
8. **Retention check tool:** Nigraan ka `yt_analytics.py` se retention curve vs hamare chapter map (kahan drop).
9. **Reality-check EDIT_STYLE.md** bharna aur voice/palette/logo (bible 5 TODO, user decision).

## 10. Agle kadam
User: voice, palette, per-video cap; Sanchalak: Munshi ko is guide ke checklist (alag file ya section 11) ka use karne do; Nigraan: pehli 3 videos ke baad is guide ke `[test]` labels update karo.

# 11. PRE-PUBLISH ENGAGEMENT CHECKLIST (1 page)
Title / Thumbnail
- [ ] Pehle 40 chars me hook + asli search word; kisi movie ka naam headline me nahi.
- [ ] Title ka vaada pehle 60 s me dikhta hai (misleading = BLOCKER).
- [ ] Thumbnail: ek focal object, 1-3 shabd, letter height >= 12%, 160x90 par padhne layak, 3 variants (A/B).
Hook
- [ ] Pehla shabd <= 1.0 s, pehla frame asli visual (no logo/greeting).
- [ ] 0-10 s me ek concrete example, 10-20 s me stake, 20-30 s me roadmap + open loop.
- [ ] Hook line ka payoff video me aata hai.
Structure
- [ ] 6-9 chapters, chapter badge, description me timestamps.
- [ ] Har 2-3 min me naya reveal/sawaal; midpoint reset ~9-10 min.
- [ ] Verdict card + recap + ek specific sawaal (generic "like/subscribe" nahi); last 20 s end screen ke liye khali.
Pacing / editing
- [ ] Koi shot 8 s se zyada bina move/cut nahi; har bola hua usi second dikhta hai.
- [ ] Har 2-3 min me tez-cut burst, reveal se pehle ~1 s silence, koi 2 s+ dead air nahi.
- [ ] Ek theme (dark-neon ya light-sketch), ek accent colour, text normal size, ek idea per scene.
- [ ] Music voice se 18-22 dB neeche (build 10-12), -14 LUFS +/-1, peak <= -1.4 dBFS.
- [ ] Hindi text ि ी ं ्र ke saath test (Chromium/raqm).
Credibility
- [ ] Har claim ka [F#] 2+ sources; major claim par screen par source card.
- [ ] "Abhi unknown" / "andaza" jahan sach me wahi hai, wahi bola gaya.
- [ ] Description me sources list; contains_synthetic_media true.
Voice
- [ ] Wakya 8-18 shabd, pauses punctuation se, glossary test clip pass.
Copyright / safety
- [ ] Sab footage/images ka licence row; koi movie clip/poster/music nahi; name_guard pass.
- [ ] Study ka koi frame/script/title/thumbnail nahi.
Shorts
- [ ] 35-40 s, pehla frame visual, pehla shabd <= 0.5 s, reveal Long me, captions safe area me, ya loop/cliffhanger.


## 12. [video-study 2026-11-07] Kya confirm hua / ghalat nikla
Detail aur numbers: `brand/VIDEO_STUDY_2026-11-07.md` (6 videos, 12-19 min). Label `[video-study]` = naapa hua.
- CONFIRMED: pehla shabd 0 s par; concrete hook pehle 10 s; sentence 8-15 words; English pauses median ~0.5 s, >2 s dead air nahi; first-60-s me zyada cuts; dark-space + ek accent rang; 1-5 shabd ka thumbnail text; Hindi channels ke title/thumbnail Roman English me.
- GHALAT / badla: (a) "midpoint reset" aur "chapter badge" kisi studied video me nahi dikha, `[test]` banaya; (b) music "18-22 dB neeche" naap nahi paaya (pauses me sirf 4-8 dB); (c) "reveal #1 = 3:00" ki jagah studied videos me ek mukhya jawab 51-85% par aata hai, beech me chhote reveals; (d) blog ka "8 s shot cap" soft nikla; (e) loudness hamara -14 un sab (-16 se -22) se zyada loud, theek hai.
- NAYA: sponsor/ad 4/6 me, shuru ya aakhir me; hum sponsor-free hain isliye last ~90 s CTA/end screen ke liye khali. Title ka vaada aakhir tak tut sakta hai (ek video ka title "koi explanation nahi" kehta hai par video 7:27 par samjha deta hai); hum aisa nahi karenge (RULES 13).
