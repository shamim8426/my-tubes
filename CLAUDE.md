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
- Koi bhi badlav ho to pehle sirf `--preview` banao. `--final` tabhi banao jab user bole "final banao".
- Sirf badla hua scene ya line dobara banao, baaki cache se lo (`cache/<channel>/<story>/<video>/` scene clips, story ka `audio/tts_cache/` TTS). Kabhi poori video shuru se mat banao (cache mat mitao) jab tak user na kahe.
- User ke kai badlav ek saath aayein to sab ek hi build me lagao, har badlav par alag build mat chalao.
- Image/TTS par paisa lagne se pehle cost batao aur user se poocho. Paisa sirf cache miss par lage; make_short bina `--spend` ke paid TTS se pehle ruk kar estimate dikhata hai.
- Build ke baad hamesha batao: preview ya final, scenes cached/naye, build time, aur kharcha.
- Shorts ka music ab 3.5 dB dheema hai (`MUSIC_BELOW_VOICE_DB["short"] = 12.5`, stem method se 12-14 LU target); Case 01 ke agle rebuild par bhi lagega.

## Munshi (review + publish)
- Har production step ke baad `munshi` subagent ko bulao aur uska verdict mujhe dikhao. FIX ho to free fix karo aur dobara review karwao; ASK ho to mujhse poochho.
- Upload sirf `munshi` karega, `youtube-publish` skill ke hisaab se, meri "ha" ke baad.
- Naye niyam: sab channels ke liye `shared/RULES.md`, sirf ek channel ke liye `channels/<key>/RULES.md` (channel ke niyam sakht ho sakte hain, dheele kabhi nahi).
- **Short -> Long checklist:** session shuru hote hi `channels/<key>/log.md` me `related_video: pending` ya `pin_comment: pending` dikhe to user ko yaad dilao (Studio: Related video = long video, first comment pin). User "ho gaya" bole to us line me `related_video: done, pin_comment: done` (aur date) likho.
- Munshi ka log aur carry-over: `channels/<key>/log.md`, `channels/<key>/carry_over.md`.

## Auto mode (shared/RULES.md section 14)
- Script approve hone ke baad sheets -> scene images -> voice samples -> TTS -> thumbnail -> PREVIEW tak sab apne aap chalao (paid bhi), har kadam par user se mat poochho.
- Har paid call se pehle: story ka kul kharcha (cost_log.csv) ₹130 se upar na jaaye, aur bacha balance ₹50 se neeche na aaye — warna ruko aur poochho. Scene image max 2 baar regenerate.
- Munshi har stage review kare; R1 FIX apne aap theek karo; R2 ke baad sirf MINOR -> aage badho; BLOCKER / copyright shak / channel ID mismatch -> ruko aur poochho.
- User se sirf script approval aur preview approval par milna. Preview approval = us long video ka upload "ha" (phir final -> Munshi -> upload -> Short flow).
- Har auto kadam channel log.md me (kharcha ab tak ke saath) aur user ko ek chhoti status line. Stages `channels/<key>/pipeline_queue.json` me.

## GitHub sync
- Har milestone ke baad sync chalao: `powershell -NoProfile -ExecutionPolicy Bypass -File tools\sync.ps1 -Message "<project>: <milestone>"`.
  Milestones: script approved, scene images done, TTS done, final build done, thumbnail done, uploaded (Munshi PUBLISHED ke baad).
- Session band hone par hook aur raat 11:30 ka task apne aap sync karte hain.
- Sync log: `shared/sync.log`. Koi ERROR dikhe to mujhe batao.
- Secrets (.env, secrets/) kabhi repo me nahi jaate; sync.ps1 aisa hone par ruk jaata hai.
