# Review 050 (Claude Feature 06, Voice mode)
Pre-render contact sheet (every 2 s), found and fixed in code before the full render:
1. Captions "Chat box me SOUND WAVE icon par click karo", "HANDS-FREE me ruko to Claude jawab deta hai", "AUDIO save nahi hota, TRANSCRIPT rehta hai" were wider than the 1080 frame (cut at both edges). Fixed: split into two shorter phrases each.
2. 0-1 s of the hook: big empty white card (keyboard appeared only at the first spoken word). Fixed: keyboard from 0.25 s.
3. 4.7-6.8 s (start scene): lower half of the screen empty until the voice picker. Fixed: phone home screen shown from the scene start, wave icon ring starts at the word "sound wave".

Post-render review (contact sheet every 2 s of output/short.mp4; 36.8 s, 1080x1920, -14.9 LUFS, TP -1.4 dBFS):
4. 12-18 s (modes): caption strip overlapped the bottom of the PUSH-TO-TALK card. Fixed: both cards moved up 50-90 px.
5. 19-22 s (extra) and 25-28 s (caution): lower half empty for about 2.7 s before the second card. Fixed: language card enters at "badal sakte" (T extra 7), official note enters at "usage" (T caution 4).
Fix round 1: full re-render (code-only layout change, audio unchanged).

Fix round 1 checked (12-33 s sheet every 1.5 s): modes caption overlap fixed, no empty lower half longer than about 1.2 s (caution 'Dhyan rakho' first words, accepted). Final: 36.8 s, -14.9 LUFS, TP -1.4 dBFS. fixed.
