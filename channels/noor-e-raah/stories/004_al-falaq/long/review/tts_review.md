# TTS review - 004_al-falaq (Munshi) - VERDICT: FIX (1 BLOCKER: line 40)

Checked: 43 wav (24 kHz mono, 402.8 s), .ok files, own Whisper-small (hi) re-run on 5, 14, 21, 27, 34, 40, 22, 47, 49, 50, 51, 52 (line 49 also in 3 slices of its tail); peak/RMS/clip/lead/tail/longest-pause/f0 on all 43.

## BLOCKER
- **Line 40 (ucharan of ayah 6, "वमिन शर्रि हासिदिन इज़ा हसद") is the WRONG audio.** 17.92 s long (a 5-word ucharan should be ~4 s). Whisper (and the line's own .ok file) show the voice spoke invented text: "और वो भी जब वो हसद करने लगे, क्योंकि हसद एक ऐसी चीज़ है जो हमारे दिलों को ख़राब कर देती है, हम अल्लाह की दी हुई नेमतों पर शुक्र करना भूल जाते हैं और दूसरों के हक़ में बुरा सोचने लगते हैं". The ucharan words are not spoken at all, and it adds an unsourced religious/moral claim (no dossier tag). The "Whisper OK 43/43" in tts_report.md is wrong for this line. Not tilawat, but the script text and on-screen ucharan will not match the audio.
  - Fix (free wording, then one TTS retake by builder): keep the same words but give the model a clear stop, e.g. "वमिन शर्रि हासिदिन, इज़ा हसद।" (comma after हासिदिन, danda at end), same pattern that worked for lines 27 and 34. Accept the take only if duration <= 6 s and the Whisper text contains हासिद + हसद and nothing else. Do not let the .ok check pass on "ok" alone: compare words to the line text.

## Accepted-by-Sanchalak lines
- **Line 22** ("दूसरी आयत: उसकी बनाई हर चीज़ की बुराई से"): Whisper "तुस्री आयात, उसकी बनाई हर चीस की बुराई से" - all words present; only ज़ -> स is Whisper's usual spelling noise. "दूसरी" read as "दूस्री/तुस्री" by Whisper, a little soft but understandable. PASS.
- **Line 47** (Sawaal): "तो यानी सुबहा के रब की पना हर चीस की बुराई से रात से जादू से और जलन से" - every clause present ("चीज़" present; Whisper wrote चीस). PASS.
- **Line 49** (long hadith, 20.64 s): Whisper loops on "गईं" when fed whole, but the tail is real speech (RMS 0.07-0.17 up to 20 s, tail 0.24 s). Re-transcribed slices 14.0-20.6 s: "और फिर क़ुल अऊज़ु बिरब्बिल फ़लक़ और क़ुल अऊज़ु बिरब्बिन्नास का ज़िक्र किया". With the first part (मुस्लिम, उक़्बा बिन आमिर, रज़ियल्लाहु अन्हु, नबी सल्लल्लाहु अलैहि वसल्लम ने फ़रमाया, "क्या तुमने नहीं देखा ... कभी नहीं देखी गईं?") every word is present. No clip, no cut-off. PASS (the 'गईईई' in Whisper is its own loop, not an audio stretch: "गईं" words at 12.0 and 14.0 s are normal length).
- **Line 50** (Bukhari, 21.0 s): complete - बुख़ारी, आइशा रज़ियल्लाहु अन्हा, नबी सल्लल्लाहु अलैहि वसल्लम, हर रात, हथेलियाँ जोड़कर फूँकते, and all three surahs named (हुवल्लाहु अहद, अऊज़ु बिरब्बिल फ़लक़, बिरब्बिन्नास), "पढ़ते". PASS.
- **Line 51**: complete ("जहाँ तक हाथ पहुँचता, सिर, चेहरे ... जिस्म के आगे के हिस्से ... तीन बार करते थे"). PASS.
- **Line 52**: complete (रिवायत के तौर पर, कोई हुक्म या वादा नहीं). PASS.

## Other checks
- Line 5 (honest note): full, incl. "तिलावत नहीं ... किसी क़ारी से सुनें". PASS.
- UCHARAN plain reading (pitch spread by my autocorr method, narration lines 10-15 st): 14 = 8.5 st, 3.2 s; 21 = 12.5 st but only 3.1 s of 4 words (no sustained note, Whisper reads back the words "मिन शर्री मा ख़लक़"); 27 = 6.9 st, 4.2 s; 34 = 8.2 st, 3.6 s. All short, no melody, no held notes: plain reading, not chanting. (Line 40 is the exception, but it is narration, not chanting.)
- Pronunciation: नफ़्फ़ासाति - the doubled फ़ is audible (0.7 s "नफ़्फ़ा" then "साति" 0.5 s), "फ़िल उक़द" Whisper writes "उगध" (क़ -> ग/ख noise, unverifiable by ear) - MINOR. "वमिन" in 34 is heard as "वा-मिन", in 27 "वम/वमिन" (Whisper adds a leading "और" in 27 and .ok) - sounds like a short lead-in vowel, acceptable plain reading - MINOR. 14 "अऊज़ु" -> "आवुजु" and "बिरब्बिल" -> "बिरभ्बिल" is Whisper noise.
- Clipping: none except line 54 has 1 sample at full scale (pk 1.00) - harmless. Other peaks 0.69-0.90, RMS 0.09-0.18; no loud/quiet outlier.
- Gaps: lead 0.20-0.44 s, tail 0.18-0.54 s, longest internal pause 1.04 s (line 18). No dead air, no cut-offs.
- Voices: Ustaad f0 median 88-137 Hz (one male voice; 137 on line 45 is a high-ish outlier but same timbre range), Sawaal 173-245 Hz (female; line 47 at 173 is lower but still female range and same voice in the .ok). No swapped voice.
- Sources/claims: hadith lines have source names and hedged wording; no tilawat audio anywhere.

## Notes (MINOR, to carry_over, no redo)
- 34 and 27 "वमिन" start with a short extra vowel; 34 "उक़द" Whisper writes ग/ख; line 54 one clipped sample; line 45 Ustaad pitch a little high.
- Process: tts_report.md claims Whisper OK 43/43 - the check must compare words, not just "got a transcript".

## Verdict
FIX: redo only line 40 (new take per the wording above, accept only if <= 6 s and words match). Everything else PASS. Total voice will drop by ~14 s. No STOP condition; cost of one TTS retake is within the story budget (spent Rs 14.47 of 120), free TTS first per the Free-first rule.
