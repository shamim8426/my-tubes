# Final review - imaan_short_03_cute.mp4 (2026-11-10) - VERDICT: FIX
Checked: ffprobe/ffmpeg (1080x1920, 44.09 s, aac), ebur128, frames at 1/7/13/20/24/25/27/33/41 s + contact sheet 30-44 s, Tanzil uthmani 94:5-6 bytes, name_guard on lines_v3.json, cost_log.csv.
- BLOCKER 1 (visual): last line (nani "देखा बेटी? सब्र का फल...", ~37.5-43 s) shows a broken mouth-overlay: grey vertical bar + smeared stretched-skin block covering nose/mouth. Fix free: rebuild shot 7 (nani_happy) in build_v3.py/talk.py (mouth patch/landmarks failed on that image), or use still + sway without mouth patch for that shot.
- BLOCKER 2 (Arabic bytes): on-screen ayah in build_v3.py is not byte-equal to Tanzil 94:6. Screen: U+0651 comes after U+064E order swapped (0646 064E 0651); Tanzil: 0646 0651 064E (shadda then fatha). Fix: take the text from the Tanzil file (94|6) instead of typing it. Whole ayah shown, source line "सूरह अल-इन्शिराह . आयत 94:6" present. Only 94:6 is shown/spoken (94:5 not used; fine). Also glyphs in the rendered frame look thin/odd with Amiri; check after fix.
- OK: subtitles at y~1415-1600 of 1920 (inside safe area, readable); no cut sentence (all 7 lines complete); loudness -14.6 LUFS, TP -1.2 dBFS; no Prophet/Sahabi/Quran-named person/angel (Sana, Nani fictional), no Allah depiction (only the word Allah in speech); no recitation audio; name_guard OK.
- Cost: story 006 TTS in cost_log.csv approx Rs 1-3 total (v2 lines ~0.1 each + v3 l07 0.11) = far below Rs 20.
- NOTE: duration 44 s vs order ">=60 s": user knowingly chose this 44 s version on 2026-11-09 (also within 60 s Short limit of uploader).
- NOTE: channel.json contains_synthetic_media is false; upload.json must set true.
## Draft metadata (use after fix; not created yet, no job file written)
title: सब्र का फल हमेशा मीठा होता है | Noor-e-Raah
description: मुश्किल में भरोसा मत छोड़ो: "बेशक, हर मुश्किल के साथ आसानी है।" (क़ुरआन, सूरह अल-इन्शिराह 94:6). सीख: सब्र और अल्लाह पर भरोसा. Arabic text: Tanzil.net (Uthmani). AI-generated animation and voice. #ImaanShorts #Sabr
playlist imaan_shorts PLdhrP4DE-lC8, private, contains_synthetic_media true, made_for_kids false.

## Round 2 (2026-11-10) - VERDICT: PASS-WITH-NOTES
- BLOCKER 1 fixed (frame 40 s clean). BLOCKER 2 dropped: v3.ass Ayah == Tanzil 94|6 codepoint-for-codepoint (0646 0651 064E); my earlier byte read was wrong.
- 44.09 s, 1080x1920, -14.6 LUFS, TP -1.2. MINOR (carry): mouth overlay flat at ~23 s; ayah thin over hijab edge.
- Uploaded PRIVATE: https://youtu.be/IAblU-7CQ_8, synthetic=true, playlist PLdhrP4DE-lC8 ok.
