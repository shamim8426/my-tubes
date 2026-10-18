# दादी की कहानियाँ (Dadi Ki Kahaniyan) — Story Channel

Har script, case file aur image prompt se pehle [channel_bible.md](channel_bible.md) padho aur uske rules exactly follow karo:
- Permanent characters ka look kabhi mat badlo — bible ke exact descriptions use karo.
- Script: 110–140 words, 2-sec hook, Golu ka ek galat guess, Dadi ka ek clue observation, end me "बताओ, दोषी कौन?". Answer alag file me.
- Naye suspects ka look case file me likho; dobara aayein to wahi look use karo.
- Har paid image ke baad user ko batao: is image ka cost (₹), aaj ka total, aur ₹500 budget me se kitna bacha. `scripts/gemini_image.py` ye apne aap `cost_log.csv` me likhta aur print karta hai.
- Paisa lagne wala koi bhi naya kaam user se pooch kar hi karo. User se Hinglish me baat karo.
- Paid image/TTS se PEHLE har chinta batao aur jawab ka intezaar karo: answer spoil hona, Shorts (9:16) vs 16:9, YouTube safe area, AI se Hindi text. Kai sudhaar hon to sab ek hi generation me jodo.

## Video build workflow
Command: `.\.venv\Scripts\python -X utf8 scripts\make_short.py <case> [--preview | --final] [--spend]`
- Koi bhi badlav ho to pehle sirf `--preview` banao. `--final` tabhi banao jab user bole "final banao".
- Sirf badla hua scene ya line dobara banao, baaki cache se lo (`cache/<case>/` scene clips, `audio/<case>/tts_cache/` TTS). Kabhi poori video shuru se mat banao (cache mat mitao) jab tak user na kahe.
- User ke kai badlav ek saath aayein to sab ek hi build me lagao, har badlav par alag build mat chalao.
- Image/TTS par paisa lagne se pehle cost batao aur user se poocho. Paisa sirf cache miss par lage; make_short bina `--spend` ke paid TTS se pehle ruk kar estimate dikhata hai.
- Build ke baad hamesha batao: preview ya final, scenes cached/naye, build time, aur kharcha.
- Yaad rakhna: Shorts ka music agle build me 3-4 dB dheema karna hai (stem method se 12-14 LU target).

## Munshi (review + publish)
- Har production step ke baad `munshi` subagent ko bulao aur uska verdict mujhe dikhao. FIX ho to free fix karo aur dobara review karwao; ASK ho to mujhse poochho.
- Upload sirf `munshi` karega, `youtube-publish` skill ke hisaab se, meri "ha" ke baad.
- Naye rules `munshi/RULES.md` me jaate hain.

## GitHub sync
- Har milestone ke baad sync chalao: `powershell -NoProfile -ExecutionPolicy Bypass -File tools\sync.ps1 -Message "<project>: <milestone>"`.
  Milestones: script approved, scene images done, TTS done, final build done, thumbnail done, uploaded (Munshi PUBLISHED ke baad).
- Session band hone par hook aur raat 11:30 ka task apne aap sync karte hain.
- Sync log: `munshi/sync.log`. Koi ERROR dikhe to mujhe batao.
- Secrets (.env, secrets/) kabhi repo me nahi jaate; sync.ps1 aisa hone par ruk jaata hai.
