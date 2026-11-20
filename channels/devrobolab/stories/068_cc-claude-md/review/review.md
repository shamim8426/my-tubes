# 068 self-review

## Round 1 (frames every 5 s before the full render, 2026-11-19 ~22:50)
1. ALL: visuals too small for 16:9, empty band between cards and text (y ~650-830). Fix: visual layer scaled 1.2x about (960,400); text drawn on its own layer.
2. write 126-141 s: editor + Commands/Conventions/Gotchas cards vanish during "Example 2/3" (only text on screen). Cause: anchor "check" matched the token "typecheck". Fix: use the 2nd "check".
3. size 166-172 s: big "200" had a large grey card shadow behind plain text. Fix: no shadow for big numbers.
4. mistakes ~214-217 s: only the numeral "3" on screen until "टकराने". Fix: the two colliding chips enter at "तीसरी".
5. mistakes 3: terminal at y 680 would touch the text after the 1.2x scale. Fix: moved up (chips 250, pill 360, terminal 600).
