# किस्सागो | Kissago — Story Channel

## Project dhaancha (multi-channel)
- `channels/<channel_key>/`: channel.json, RULES.md, channel_bible.md, log.md, carry_over.md, brand/, characters/ (permanent characters + voices/)
- `channels/<key>/stories/<NNN>_<slug>/`: story.md (status), script/, scene_prompts.json, characters/ (sirf is kahani ke), images/, audio/
  - `long/` aur `shorts/short_<NN>_<slug>/`: project.json, lines.json, shots.json, meta.json, review/, output/
- `shared/`: music/, sfx/, fonts/, assets_license.csv, RULES.md (sab channels ke common niyam), sync.log
- `channels/_template/`: naye channel/kahani ka khaali dhaancha. Naya channel: `powershell -File tools\new_channel.ps1 -Key <key> -Name "<naam>"`

## किस्सागो | Kissago (channel key: dadi-ki-kahaniyan; pehle "दादी की कहानियाँ")
Title suffix aur thumbnail label `channels/dadi-ki-kahaniyan/channel.json` (`title_suffix`, `brand_label`) se lo.
Har script, case file aur image prompt se pehle [channels/dadi-ki-kahaniyan/channel_bible.md](channels/dadi-ki-kahaniyan/channel_bible.md) padho aur uske rules exactly follow karo:
- Permanent characters ka look kabhi mat badlo — bible ke exact descriptions use karo.
- Script: 110–140 words, 2-sec hook, Golu ka ek galat guess, Dadi ka ek clue observation, end me "बताओ, दोषी कौन?". Answer alag file me.
- Naye suspects ka look case file me likho; dobara aayein to wahi look use karo.
- Har paid image ke baad user ko batao: is image ka cost (₹), aaj ka total, aur ₹500 budget me se kitna bacha. `scripts/gemini_image.py` ye apne aap `cost_log.csv` me likhta aur print karta hai.
- Paisa lagne wala koi bhi naya kaam user se pooch kar hi karo. User se Hinglish me baat karo.
- Paid image/TTS se PEHLE har chinta batao aur jawab ka intezaar karo: answer spoil hona, Shorts (9:16) vs 16:9, YouTube safe area, AI se Hindi text. Kai sudhaar hon to sab ek hi generation me jodo.

## Video build workflow
Command: `.\.venv\Scripts\python -X utf8 scripts\make_short.py <video folder> [--preview | --final] [--spend] [--plan] [--seconds N]`
(video folder = `channels/<key>/stories/<story>/long` ya `.../shorts/short_<NN>_<slug>`; `--plan` sirf paths/inputs check karta hai, `--seconds N` pehle N second ka test preview)
- Koi bhi badlav ho to pehle sirf `--preview` banao. `--final` tabhi banao jab user bole "final banao" — auto mode (RULES 14) me Munshi ke preview PASS ke baad apne aap.
- Sirf badla hua scene ya line dobara banao, baaki cache se lo (`cache/<channel>/<story>/<video>/` scene clips, story ka `audio/tts_cache/` TTS). Kabhi poori video shuru se mat banao (cache mat mitao) jab tak user na kahe.
- User ke kai badlav ek saath aayein to sab ek hi build me lagao, har badlav par alag build mat chalao.
- Image/TTS par paisa lagne se pehle cost batao aur user se poocho. Paisa sirf cache miss par lage; make_short bina `--spend` ke paid TTS se pehle ruk kar estimate dikhata hai.
- Build ke baad hamesha batao: preview ya final, scenes cached/naye, build time, aur kharcha.
- Shorts ka music ab 3.5 dB dheema hai (`MUSIC_BELOW_VOICE_DB["short"] = 12.5`, stem method se 12-14 LU target); Case 01 ke agle rebuild par bhi lagega.

## Munshi (review + publish)
- Har production step ke baad `munshi` subagent ko bulao aur uska verdict mujhe dikhao. FIX ho to free fix karo aur dobara review karwao; ASK ho to mujhse poochho.
- Upload sirf `munshi` karega, `youtube-publish` skill ke hisaab se, meri "ha" ke baad — auto mode (RULES 14) me script approval hi "ha" hai, upload hamesha scheduled (veto window).
- Naye niyam: sab channels ke liye `shared/RULES.md`, sirf ek channel ke liye `channels/<key>/RULES.md` (channel ke niyam sakht ho sakte hain, dheele kabhi nahi).
- **Short -> Long checklist:** session shuru hote hi `channels/<key>/log.md` me `related_video: pending` ya `pin_comment: pending` dikhe to user ko yaad dilao (Studio: Related video = long video, first comment pin). User "ho gaya" bole to us line me `related_video: done, pin_comment: done` (aur date) likho.
- Munshi ka log aur carry-over: `channels/<key>/log.md`, `channels/<key>/carry_over.md`.

## Auto mode (shared/RULES.md section 14)
- Sirf ek human checkpoint: script approval. Uske baad sheets -> images -> voice samples -> TTS -> preview -> Munshi R1 (auto fix) + R2 -> final -> Munshi final -> long thumbnail -> upload -> Auto Short (build, review, upload) -> first comments -> sync, sab apne aap. Preview par user se nahi milna.
- Har video scheduled upload hota hai (slot tak private: long 19:00, Short 21:00), kabhi turant public nahi. Long upload 18:45 IST ke baad ho to agle din ka slot.
- Har upload ke turant baad user ko ek status line: video link + slot. User slot se pehle "rok do" bole to `.\.venv\Scripts\python -X utf8 tools\veto.py <video_id> --apply` chalao (private + publishAt hatao), log.md me likho, us story ki pipeline pause (pipeline_queue.json: vetoed).
- Long thumbnail API se apne aap. Short cover API se nahi lagta: Short ka pehla frame hi cover (hook visual, pehle 1 s caption nahi, text 15%-85% height me) + ek vertical cover file output/ me manual use ke liye.
- Ruko aur poochho: story kharcha ₹130 se upar, balance ₹50 se neeche (ya credits khatam), kisi scene ki 3rd regeneration, R2 ke baad BLOCKER, copyright shak, channel ID mismatch.
- Uploads ke baad manual Studio checklist: Short ka Related video, first comment pin, aur jab tak API audit pass na ho, schedule confirm/set karna.
- Har auto kadam channel log.md me (kharcha ab tak ke saath) aur user ko ek chhoti status line. Stages `channels/<key>/pipeline_queue.json` me.

## Production profile (shared/RULES.md section 15, story 004 / Long 03 se)
- Long 02 (story 003) aur uska Short jaise hain waise rahenge. Story 004 se: sirf script approval; koi preview nahi — Munshi stage R1+R2 (script timing, images, audio) ke baad seedha FINAL; final par Munshi ka ek hi check (R1) -> scheduled upload (veto window).
- Lambai: long max 4:00 (target 3:40–4:00), Short max 40 s (target 35–40 s); script measured TTS speed se likho.
- Kharcha: ₹100–110 ASLI (usageMetadata, reference images samet) per story (long + Short + thumbnail). Kuch banane se pehle asli kharche ka andaza; ₹110 se upar ho to plan saral karo, kabhi budget se upar shuru mat karo. Max 16 nayi scene images (baaki crop/zoom), sirf 1K, refs sirf us scene ke kirdaar, purani sheets dobara, regen max 1 aur sirf BLOCKER par.
- R2 ke baad MINOR sirf carry_over.md me, kuch regenerate nahi. Ruko sirf BLOCKER / copyright shak / channel ID mismatch par.

## GitHub sync
- Har milestone ke baad sync chalao: `powershell -NoProfile -ExecutionPolicy Bypass -File tools\sync.ps1 -Message "<project>: <milestone>"`.
  Milestones: script approved, scene images done, TTS done, final build done, thumbnail done, uploaded (Munshi PUBLISHED ke baad).
- Session band hone par hook aur raat 11:30 ka task apne aap sync karte hain.
- Sync log: `shared/sync.log`. Koi ERROR dikhe to mujhe batao.
- Secrets (.env, secrets/) kabhi repo me nahi jaate; sync.ps1 aisa hone par ruk jaata hai.
