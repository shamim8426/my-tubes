# TTS review - 005_an-nas (Munshi) - R1 - VERDICT: PASS (MINOR only)

Checked: all 38 lines in lines.json have a wav + .ok (24 kHz mono, total 309.4 s); every line text matches script/script.md word-for-word (normalised compare, 0 mismatches, no invented or missing line); peak/lead/tail on all 38; tts_report.md Whisper transcripts for the 5 flagged lines; assets_license.csv.

## Flagged lines (21, 23, 47, 48, 53) - judged from the Whisper transcripts in tts_report.md (no local Whisper available to me, no audio listened)
- 21 (4.4 s) and 23 (10.2 s): "बादशाह" is read back as "बाच्चाह/बाज्चा" - this is the same sh/d spelling noise seen in 004; every other word present, duration right. PASS (MINOR: listen once at the build check).
- 47 (19.7 s): all clauses present; "सल्लल्लाहु अलैहि", "ऐसी" garbled only in Whisper spelling; length matches 004's equivalent (20.6 s). PASS.
- 48 (20.9 s): all clauses present (बुख़ारी, आइशा, हर रात, हथेलियाँ, फूँककर, क़ुल हुवल्लाहु अहद, तीन बार); length matches 004 line 50. PASS.
- 53 (13.8 s): all clauses present; "माआरिफ़ुल" and "दोनों" spelling noise only. Lead 0.06 s (very tight but not clipped). PASS.
No line needs a retake. Retake cost would be 0.

## Other checks
- UCHARAN lines 14, 20, 25, 30, 37, 42: 3.6 / 2.1 / 2.5 / 4.6 / 4.5 / 4.3 s - short plain readings, no held notes; text matches the script ucharan; no tilawat audio anywhere. (research/ucharan.md is not in the repo; matched to script.md ucharan lines instead - MINOR.)
- Voices: sawaal lines 3, 35, 50, 55 and ustaad lines per speaker field; no role swap seen in the files.
- Clipping: none (peaks 0.64-0.94). Lead silence 0.06-0.35 s (first word well under 1.0 s); tails 0.01-0.91 s (line 3 tail 0.01 s, line 14 0.91 s).
- Length: voice 309.4 s plus gaps/pauses is consistent with the ~5:57 plan (under long max 4:00 rule does not apply to Surah mode per channel rules; builder to confirm total in script timing).
- Music/ambience: Soaring (Kevin MacLeod, CC BY 4.0) and night_wind_crickets_felixblume_165526 (CC0) are in shared/assets_license.csv; Soaring credit must go in the description. Not yet mixed (audio/ has only tts/), so levels (20-24 LU under) and continuous music (RULES 1c) are for the final build check.
- Cost: Rs 12.07 incl. GST, 54 calls, far under Rs 120.

## MINOR (carry_over)
- Listen once to 21/23 "बादशाह" in the final build.
- Line 3 tail 0.01 s: check the join to the next line has a pause.
- ucharan.md not found for cross-check.

No STOP condition.

VERDICT: PASS
