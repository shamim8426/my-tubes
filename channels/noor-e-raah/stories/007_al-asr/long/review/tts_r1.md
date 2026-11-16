# 007_al-asr TTS/audio R1 + script recheck (Munshi, 2026-11-13) - PASS-WITH-NOTES
- Numbering 1..51 consistent: script.md, lines.json (34 spoken lines, cues 1,2,5,7,10,13..), images.json, render.json (cards 4, 47-49, end_from 50). No gap; Tabarani line gone from spoken text (only mentioned in header/notes).
- Arabic: lines.json 7 Arabic blocks == sources.json (Tanzil, pc_check done) byte-for-byte; 103:1 = word[4] stripped of Bismillah; 103:3 split 3/2/2/2 words joins back to full ayah; script.md ARABIC lines == lines.json.
- UCHARAN lines 11,18,24,30,36,42 == research/ucharan.md exactly.
- One narrator (ustaad/Algieba, 34/34), no '?' in spoken text, no disclaimer/tilawat claim, no named Sahabi.
- Audio: 34 wavs, durations == lines.json, total 183.6 s; sample peak max 0.892 (-1.0 dBFS), no clipping.
- Whisper (faster-whisper small, re-run by Munshi on all 34 lines incl. UCHARAN): every line present, only Whisper Hindi spelling noise. Lines 31 ("और जिन्होंने अच्छे काम किए") and 49 (all three seekh points, "3." heard) confirmed false positives. UCHARAN: 11,18,24,42 clean; 30 heard "वा अमिलु स्वाले हाद" and 36 "तबा सव भिल हख" (small model Arabic-in-Hindi weak; length+rhythm normal, no dropped word seen) - MINOR, spot listen if time.
- Line 19 heard "हर इन्सान घाटे में पड़ा हूँ आ है" (= "हुआ है"), line 48 "दोनों" heard "दोन हूँ" - Whisper noise, words not missing.
