# 062 How-to Short (Claude me web search kaise on karein): self-review

## Round 0 (frames before the full render, review/sheet_*.png)
| # | Time | Problem | Fix |
| 1 | 0.0-19.6 | Big grey block behind the drawn chat UI (shadow drawn for the whole transparent sprite) | card_enter(shad=False) for chatui |
| 2 | 7.3-48.2 | Official page crops unreadable (about 20 px text, 1000 px desktop capture) | Recaptured at phone width 430 px, dsf 2.5 (raw/capture_m.py), crops 900-960 px wide, text about 35 px |
| 3 | 32.3-48.2 | Lower half of the caution scene empty (thin crops) | Bigger crops + settings path chips (Organization settings, Capabilities, Web search ON), usage meter illustration, globe for 'Claude searches by itself' |
| 4 | 0.0-0.4 | First frame (= Short cover) had the menu half open | Hook shows the finished state (menu open, tick, Web search on) from frame 0 |
| 5 | 4.5-6.5 | '2 CLICKS' chip touched the answer card, '+ SOURCE LINKS' overlapped it | Moved chips/card apart |
| 6 | 19.6-28 | Tips crop heading cut at the top | Crop box moved up 15 px |
| 7 | 33.5-36 | Team scene empty below the chips for ~2.5 s | 'Owner > sab members' chip until the path chips start |
All checked again on review/fix_*.png: fixed.

## Round 1 (full render, review/final_sheet_*.png every 3 s + review/act_sheet_*.png at action words)
- Loudness -15.6 LUFS (out of band) -> two-pass loudnorm audio remux -> -14.7 LUFS, peak -1.4 dBFS. fixed
- 18.0-19.6 'OFF: CLICK AGAIN' chip sat on top of the still-open menu -> menu closes on the word. fixed (range 7.34-19.64 re-rendered + spliced)
- 32.3-33.4 caution scene: only the title chip for ~1 s -> Team crop enters at scene start. fixed (range 32.30-48.24 re-rendered + spliced)
- Action words checked on screen at their spoken time: plus (10.4), Web search (13.0), tick (15.3), off (18.2), search the web (25.3), citations (27.4), Organization settings path (37.8), web search usage (39.7), follow (53.2): all PASS.
- Length 53.9 s (50-60 PASS), 1618 frames after splice, captions Roman Hinglish (no Devanagari on screen), no overlap/cut text, beginner check PASS (citations defined, steps shown one by one), facts = review/facts.md F1-F11 PASS, name_guard OK.
Verdict: PASS, upload.
