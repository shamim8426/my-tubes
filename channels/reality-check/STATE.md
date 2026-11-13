# STATE (written 2026-11-09, read this FIRST in a new chat; do not read the old chat unless the user says "poora purana context padho")

User talks Hindi/Hinglish. KEEP REPLIES SHORT (3-5 lines, only the key point + what the user must do); details only on request. User's Claude Pro weekly limit was 88% used; it resets Thu 2026-11-12 13:30 IST (account-fixed, not tied to billing). Avoid heavy agents/long runs until then; ask token/time estimate before big work (CLAUDE.md).

## Work place
- Worktree: D:\my-tubes\.claude\worktrees\devrobolab-042-041-upload-eb9807 (branch claude/science-eda238). Python: D:\my-tubes\.venv\Scripts\python.exe -X utf8. Secrets live in D:\my-tubes\secrets (reality-check token done). ffmpeg in tools/ffmpeg.
- GIT (updated 2026-11-09): notes, learnings, STATE.md and tools ARE committed and pushed to GitHub main (user OK'd this; tools/learn.py works again). Still NEVER commit media (videos, footage, audio, cache; footage2/footage are 4 GB, untracked). Other git actions (sync scripts, big commits) only if the user asks. The old 'learn.py diverged' problem is fixed.

## Channel
- YouTube channel renamed by user to **Possibilities**, handle @PossibilitiesHindi (was Reality Check - Asli; same channel_id UCy071_4g4vGemktFHybqkhQ; folder/key stays channels/reality-check). Tagline: "Kya ho sakta hai?". DP + banner (black + bright yellow, option E) are set by the user; channel description/keywords updated via API (no "Reality Check" left). Brand code: tools/rc_brand_final.py (+ rc_brand_variants*.py), files in channels/reality-check/brand/.
- New direction (user): calculation-based FUTURE SCENARIOS from published numbers and known science ("kya ho sakta hai"), label every estimate as our estimate, never claim new theories, 2 sources per number, Munshi check BEFORE publish. Not repeating common topics (black hole basics). Candidate ideas: (1) 60 m asteroid hits India in 2032 - warning time, push needed, city effect (we already have DART dossier/footage); (2) Mumbai under sea-level rise by 2100 (IPCC scenarios); (3) 1 million people to Mars - rockets, cost, years; (4) Starship Delhi-New York in 30 min feasibility; (5) how safe if all nations fund asteroid defence (DART/Hera/NEO Surveyor timeline). Market research + growth plan (verdict BLEND; honest odds ~70-80% 1,000 subs / ~45-60% YPP in 12 months with ~45-50 Longs; YPP needs 1,000 subs + 4,000 public watch hours; Longs 10-14 min first): channels/reality-check/research/growth_plan.md and trends_2026-11-08.md. Idea demand for the 5 scenarios above NOT yet measured (yt_read search budget 10/day was used up on 2026-11-08).

## Video 001 (DART) - DONE
- Live and PUBLIC (user made it public): https://youtu.be/ClKig-GZxGY, title "DART Ka Dhakka: 7 Minute Ka Hisaab, 33 Kaise Ho Gaya?", 18:44, 1080p, thumbnail set, description/tags updated for Possibilities. Munshi verdict was FIX (0 blockers); user chose to keep as is. Open mistakes (fix later, not urgent): line 26 (2:02) "80 million trees" disputed -> needs re-TTS; line 146 (16:26) "ESA ki jaari tasveer" label shows our drawing; lines 111-112 (11:49) "Hubble ne dekha" shows our animation unlabelled; plus 10 minors. Full list: stories/001_asteroid-defence/review/munshi_final.md and carry_over.md.
- Cost: story spend about Rs 52 of Rs 150 cap; Gemini balance about Rs 483. Gemini TTS main model = 100 requests/day shared by all channels.
- Final master (1080p) channels/reality-check/stories/001_asteroid-defence/long/output/001_long_preview.mp4 (= 001_long_final.mp4); backups 001_long_v3_animation.mp4, 001_long_real_v2.mp4, 001_long_graphic_oldlook.mp4.

## How a video is built (works, reuse)
rc_tts.py (Gemini Kore voice, cuts.json) -> shots from audio/voiceover_timing.json -> tools/rc_build_long.py <story> (real footage + own animations: tools/rc_explain*.py scenes plugged via long/footage_overrides.json; DART-specific animations need NEW ones per topic) -> it only writes cache list_real.txt: concat video-only to long/output/<story>_long_preview_oldsound.mp4 -> tools/rc_sound.py <story> remuxes with sound -> check 12 frames at line midpoints + A/V sync -> 360p copy (<28 MB) for chat -> upload with tools/youtube_upload.py --job upload.json from D:\my-tubes (private first; thumbnail via API works) -> Munshi review. NEVER bump VER (wipes cache). Max 6 render workers (user PC gets slow).
- The rules to follow for every new video: shared/DOCUMENTARY_PLAYBOOK.md (every script line needs a moving visual, planned in a shot table BEFORE building; no text cards, no static images; label own animations/illustrations; real footage only if public domain with credit). Style notes: channels/reality-check/brand/STYLE_LEARNINGS.md, long/edit_style_study.md. On-screen text Roman/Hinglish with plain digits, never Devanagari; narration Devanagari.
- Reference-style learning: median shot 4-6 s, mostly hard cuts, warm flash only at block boundaries, labels land on the spoken number, number ladder / one-picture-one-moving-part animations.

## DevRoboLab (other channel)
- 047 Gemini Omni news Short: I uploaded it private https://youtu.be/D06bMMghOLM; the user says they had already uploaded their own version, so there may be a duplicate: the user decides which to delete in Studio (never delete myself). User's own link not given yet.
- The 06:40 CFE long (Claude Feature 06) was never made (topic overlapped Feature 04; needs a different topic).

## Pending for the user
- Nothing blocking. Optional: fix the DART mistakes later; decide the next video topic (after Thu 12 Nov 13:30 IST), then ask Khoji/Kalam for a script and measure demand first (about 20 min analysis).
## Next step suggestion
After the limit resets: short demand check of the 5 scenario ideas, pick one, script (Kalam) with sources, shot table per the playbook, then build.

## User preferences and repeated complaints (from the old chat; follow these)
- Visuals must SHOW what the voice says, always as MOTION (video), never static images, text cards or empty boxes. Real footage + our animations mixed; real footage preferred where it truly shows the thing. "Dhakka/push" style words must be explained visually and simply. Plain everyday Hindi, no heavy words, calm documentary, no teasers/comment-bait/"raaz kholenge" lines.
- Sound must match each scene (several sounds, mood-matched music), not one background bed; silence/own sound of strong footage allowed.
- The user dislikes: me sending a wrong/old file (I once sent the old-look video after a remux; always verify frames before sending), unrequested extras, long replies, and being asked the same thing twice (do it yourself when you can, e.g. I ran yt_auth myself).
- User wants: first a short sample (1 min) before a full render; time + cost estimate before work; chat copies under ~28 MB (SendUserFile limit 30 MB) at 360p; DP/banner options shown as several different designs (colour, structure) not one; final art = option E black + bright yellow.
- Money goal: the channel must earn; user asked for honest analysis of what works, trends, and what to change; they accepted that growth is never guaranteed. They said small mistakes in the first video are OK, save them and fix later.
- Rules they set: no git sync; no videos in git; on-screen text Roman not Devanagari; keep my replies brief (token saving: they are on Claude Pro, weekly limit nearly used).
- If you need the exact old discussion, the old chat transcript is saved: C:\Users\ashamim\.claude\projects\D--my-tubes--claude-worktrees-devrobolab-042-041-upload-eb9807\2dd02847-a669-4cd3-ab72-e9d06310716e.jsonl (huge: read only the part needed, e.g. grep, when the user says "poora purana context padho").

## Weekly plan (user, 2026-11-09)
- Work starts every THURSDAY after the Claude weekly limit resets (13:30 IST), first start Thu 2026-11-12 around 20:00 IST. Goal: 2 videos per week (user's target); first one finished by Fri-Sun, then script for the next. Be honest if 2 Longs/week does not fit tokens/time (a video took ~4-6 h machine time + many tokens); fallback = 1 Long + 1 shorter/Short.
- Content must be very accurate (2 sources per number, estimates labelled, Munshi check before publish). New topics each time (scenario/"kya ho sakta hai" style), motion/animation style as in DART video, explained clearly (DART-style explanation was liked).
- VOICE: use a MALE Gemini voice (Kore, used in video 001, is female-sounding). Audition 2-3 male voices (e.g. Charon, Fenrir, Orus, Puck) on one script paragraph before the full TTS (tiny cost).
- LANGUAGE: everyday spoken Hindi as the user talks, no heavy technical/"AI-sounding" Hindi words, no words like "anjaan"; short sentences; conversational, explainer tone (user's reference creator: a popular Hindi explainer; copy the STYLE: plain words, simple analogies, tone/pacing; never copy script, voice or exact phrases). Before scripting, re-read the saved study notes (STYLE_LEARNINGS.md, edit_style_study.md) and channels/reality-check/stories/001_asteroid-defence/script/script.md for the DART explanation structure that worked.

## Status 2026-11-13
- Claude weekly limit reset on Thu 2026-11-12: now ~10% used; next reset Thu 2026-11-19 13:30 IST. Old chat had ~440k tokens, so the user is starting a NEW chat from this file.
- NEXT: (1) short demand check of the 5 scenario ideas (~20 min, Rs 0; yt_read has 10 searches/day), (2) user picks the topic, (3) script with sources (Kalam style, plain spoken Hindi), (4) audition 2-3 MALE Gemini voices, (5) shot table per DOCUMENTARY_PLAYBOOK.md, then build with the proven pipeline. Give a time/token estimate before each big step. Short replies.

## Video 002: Great Dying (started 2026-11-13, user picked it)
- Topic: end-Permian mass extinction ("96% of life lost"), past-science documentary. Topic research: research/interest_map_2026-11-13.md (top areas: deep ocean, earth science, extinction, brain/sleep, longevity; space/asteroid max 1 in 5 videos) and research/demand_check_2026-11-13.md.
- User's wishes for 002: MALE voice; real documentary feel, "like watching a movie"; good footage + clear explanation; graphics good-looking and MID-TONE (not very dark like 001, not too light); editing clean so people understand; reuse what worked in 001. Length 10-14 min.
- Flow: dossier + script -> user approves script (only checkpoint) -> male voice audition -> shot table (playbook) -> build -> Munshi check BEFORE publish.

## Decision 2026-11-13: narrator voice = Charon (male)
- User chose Gemini voice **Charon** for 002 and the channel going forward (samples: stories/002_great-dying/audio/voice_test/). Run TTS with `tools/rc_tts.py <story> --voice Charon` (default in the tool is still Kore); style prompt used for the test: male documentary narrator, everyday spoken Hindi, calm, warm, natural pace, slight emphasis on numbers, not theatrical. 90 s sample = 226 words, free key, Rs 0.
- 002 script still awaits the user's approval (voiceover_clean.txt); Munshi FACT CHECK of 14 VERIFY gates recommended before TTS.
