# Mood music library (all channels)

Default / permanent channel bed: `shared/music/doc2/Ossuary_6_Air.mp3` (Kevin MacLeod "Ossuary 6 - Air", CC BY 4.0; user pick 2026-11-15). Scenes switch to mood tracks per the script's cue sheet via `tools/rc_music_select.py`, which feeds `tools/rc_music_mix.py` (speaker-band calibration: music 10-13 LU under the voice in 150 Hz-8 kHz, 4-6 s equal-power crossfades at section boundaries, smooth music-off ramps at pivots, sub booms only at section starts, no whooshes/sweeps).
Rules: no track twice in a row; mid share (150 Hz-2 kHz) >= 25 % so it is audible on phones; no vocals, no strong drums. Data per track in `mood_library.json` (length, usable start / loop end, beat strength, onsets/s, brightness, sub/mid share, repetitiveness, incompetech feel/instruments tags). Rebuild: `python tools/rc_mood_library.py --pieces <incompetech pieces.json>`.

## curious_mystery
- **Investigations** (1.6 min, CC BY 4.0): light detective pizzicato/keys, curious, not scary. Beat 0.37, onsets 2.23/s, brightness 777 Hz, mid 70%, sub 29%. `shared/music/tension/Investigations.mp3`
- **Hidden Agenda** (2.2 min, CC BY 4.0): quiet suspicious synth + bass line, 'something is off'. Beat 0.54, onsets 2.88/s, brightness 992 Hz, mid 52%, sub 46%. `shared/music/tension/Hidden_Agenda.mp3`
- **Dreamy Flashback** (2.1 min, CC BY 4.0): soft dreamy electronic texture, gentle movement, curious. Beat 0.45, onsets 3.07/s, brightness 443 Hz, mid 69%, sub 31%. `shared/music/neutral/Dreamy_Flashback.mp3`

## calm_wonder
- **Ethereal Relaxation** (28.1 min, CC BY 4.0): slow airy synth pad, 28 min, thoughtful wonder. Beat 0.23, onsets 1.58/s, brightness 433 Hz, mid 89%, sub 11%. `shared/music/neutral/Ethereal_Relaxation.mp3`
- **Fresh Air** (4.9 min, CC BY 4.0): calm open pad with soft piano colour, morning feel. Beat 0.08, onsets 0.77/s, brightness 425 Hz, mid 51%, sub 49%. `shared/music/neutral/Fresh_Air.mp3`
- **Quietude Sections Merged** (8.1 min, CC BY 4.0): ambient synth soundscape, evolving, neutral and calm. Beat 0.72, onsets 2.02/s, brightness 635 Hz, mid 56%, sub 44%. `shared/music/noor/Quietude_Sections_Merged.mp3`
- **Ossuary 6 - Air** (4.2 min, CC BY 4.0): default channel bed: airy dark-neutral ambient (needs mid EQ on phones). Beat 0.91, onsets 3.4/s, brightness 866 Hz, mid 14%, sub 86%. `shared/music/doc2/Ossuary_6_Air.mp3`

## rising_tension
- **Disquiet** (3.1 min, CC BY 4.0): uneasy low strings and pads, slowly building, no drums. Beat 0.25, onsets 1.38/s, brightness 514 Hz, mid 81%, sub 18%. `shared/music/doc2/Disquiet.mp3`
- **Gathering Darkness** (4.4 min, CC BY 4.0): pulsing dark synth build, ominous, cinematic. Beat 0.86, onsets 3.25/s, brightness 886 Hz, mid 29%, sub 66%. `shared/music/doc2/Gathering_Darkness.mp3`
- **Unseen Horrors** (4.2 min, CC BY 4.0): thin suspense texture, high tension, use low. Beat 0.66, onsets 3.06/s, brightness 1571 Hz, mid 40%, sub 53%. `shared/music/doc2/Unseen_Horrors.mp3`

## danger_dark
- **Giant Wyrm** (4.3 min, CC BY 4.0): heavy low strings and drones, menacing, slow. Beat 0.37, onsets 1.56/s, brightness 491 Hz, mid 29%, sub 70%. `shared/music/doc2/Giant_Wyrm.mp3`
- **Lightless Dawn** (6.3 min, CC BY 4.0): dark slow pad, bleak, serious. Beat 0.17, onsets 1.7/s, brightness 480 Hz, mid 44%, sub 56%. `shared/music/clean/Lightless_Dawn.mp3`
- **Dark Fog** (4.0 min, CC BY 4.0): dark pulsing atmosphere, foreboding. Beat 0.5, onsets 2.46/s, brightness 1011 Hz, mid 38%, sub 62%. `shared/music/doc2/Dark_Fog.mp3`

## loss_somber
- **Sad Trio** (4.2 min, CC BY 4.0): sad slow string trio, grief. Beat 0.18, onsets 1.57/s, brightness 896 Hz, mid 96%, sub 3%. `shared/music/dukh/Sad_Trio.mp3`
- **Peaceful Desolation** (1.5 min, CC BY 4.0): lonely sparse pad and piano, empty world. Beat 0.54, onsets 1.47/s, brightness 988 Hz, mid 79%, sub 20%. `shared/music/seekh/Peaceful_Desolation.mp3`
- **Meditation Impromptu 02** (4.2 min, CC BY 4.0): slow sad piano with pad, quiet loss. Beat 0.13, onsets 1.5/s, brightness 635 Hz, mid 99%, sub 0%. `shared/music/doc/Meditation_Impromptu_02.mp3`
- **Heartbreaking** (1.6 min, CC BY 4.0): emotional strings, heavy sadness (use rarely). Beat 0.27, onsets 1.35/s, brightness 977 Hz, mid 99%, sub 1%. `shared/music/dukh/Heartbreaking.mp3`

## hope_recovery
- **Healing** (8.7 min, CC BY 4.0): soft healing pads, recovery, warm. Beat 0.14, onsets 1.35/s, brightness 761 Hz, mid 99%, sub 1%. `shared/music/neutral/Healing.mp3`
- **Airship Serenity** (4.0 min, CC BY 4.0): floating calm synths, quietly uplifting. Beat 0.88, onsets 5.03/s, brightness 1052 Hz, mid 51%, sub 49%. `shared/music/neutral/Airship_Serenity.mp3`
- **Reawakening** (3.6 min, CC BY 4.0): piano and cello, gentle recovery. Beat 0.55, onsets 2.22/s, brightness 614 Hz, mid 79%, sub 21%. `shared/music/neutral/Reawakening.mp3`
- **Wish Background** (19.6 min, CC BY 4.0): soft piano/strings/celesta bed, 19 min, hopeful. Beat 0.47, onsets 2.41/s, brightness 1317 Hz, mid 89%, sub 9%. `shared/music/neutral/Wish_Background.mp3`

## time_night
- **Mesmerize** (7.1 min, CC BY 4.0): slow evolving electronic texture, hypnotic, night. Beat 0.15, onsets 0.9/s, brightness 407 Hz, mid 60%, sub 40%. `shared/music/neutral/Mesmerize.mp3`
- **Rising Tide** (4.6 min, CC BY 4.0): steady soft pulse, clock-like motion, no drums. Beat 0.69, onsets 2.91/s, brightness 709 Hz, mid 39%, sub 60%. `shared/music/doc2/Rising_Tide.mp3`
- **Clean Soul** (5.1 min, CC BY 4.0): warm slow electronic ambience, late-night calm. Beat 0.17, onsets 1.44/s, brightness 252 Hz, mid 31%, sub 69%. `shared/music/neutral/Clean_Soul.mp3`

## reflective_serious
- **Meditation Impromptu 01** (3.5 min, CC BY 4.0): slow solo piano, thoughtful, serious. Beat 0.13, onsets 1.09/s, brightness 600 Hz, mid 100%, sub 0%. `shared/music/doc/Meditation_Impromptu_01.mp3`
- **Meditation Impromptu 03** (4.3 min, CC BY 4.0): slow piano, reflective, a little warmer. Beat 0.09, onsets 1.12/s, brightness 625 Hz, mid 99%, sub 1%. `shared/music/doc/Meditation_Impromptu_03.mp3`
- **Gymnopedie No 1** (3.1 min, CC BY 4.0): classic slow piano, calm reflection. Beat 0.49, onsets 1.05/s, brightness 539 Hz, mid 95%, sub 5%. `shared/music/doc/Gymnopedie_No_1.mp3`

## discovery_awe
- **Bathed in the Light** (2.8 min, CC BY 4.0): bright swelling pads, sense of awe. Beat 0.83, onsets 3.04/s, brightness 1028 Hz, mid 47%, sub 52%. `shared/music/neutral/Bathed_in_the_Light.mp3`
- **Ossuary 1 - A Beginning** (3.1 min, CC BY 4.0): spacious ambient opening, wonder. Beat 0.87, onsets 2.97/s, brightness 1161 Hz, mid 69%, sub 30%. `shared/music/doc2/Ossuary_1_A_Beginning.mp3`
- **Soaring** (6.3 min, CC BY 4.0): uplifting strings, big open feel (use low). Beat 0.91, onsets 2.73/s, brightness 898 Hz, mid 55%, sub 45%. `shared/music/noor/Soaring.mp3`

## ending_resolution
- **Ossuary 5 - Rest** (3.9 min, CC BY 4.0): calm resolving ambient, closure. Beat 0.93, onsets 2.91/s, brightness 595 Hz, mid 32%, sub 68%. `shared/music/doc2/Ossuary_5_Rest.mp3`
- **Dreams Become Real** (6.8 min, CC BY 4.0): gentle warm pad/piano, soft resolution. Beat 0.22, onsets 2.8/s, brightness 407 Hz, mid 74%, sub 26%. `shared/music/jaadu/Dreams_Become_Real.mp3`
- **Enchanted Valley** (3.2 min, CC BY 4.0): soft airy textures, peaceful ending. Beat 0.44, onsets 1.85/s, brightness 1105 Hz, mid 90%, sub 9%. `shared/music/jaadu/Enchanted_Valley.mp3`

## Excluded (kept for reference)
- Epic Unease (rising_tension): vocals
- Inspired (hope_recovery): mostly sub-bass (mid share 21%)
- Lasting Hope (hope_recovery): vocals
- Ascending the Vale (discovery_awe): vocals

Credit lines: every track's `credit` field in mood_library.json goes in the description when used (CC BY 4.0).
