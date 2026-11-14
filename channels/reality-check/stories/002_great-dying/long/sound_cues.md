# 002 Great Dying - sound cue sheet v4 (dark cinematic ambient family, per the reference study + playbook H)

Rules used: one family of dark ambient/cinematic beds (drone/pad/low strings), a cue change every ~1.5-2.5 min changing brightness/density; music ~15-16 LU under the voice in the body, ~12 LU at open/end, ~19 LU in analytical parts; swell when the voice stops (silent holds >= 1.2 s: +9 dB); music FULLY OFF 2.5-3 s at 8 pivot lines (question / reversal / answer) and the next cue/hit starts as the gap ends; 7 soft impact hits on reveals; 25 soft whoosh / sub-hit SFX on graphic starts (about 2 per minute, never on sentence starts); no near-silent stretch longer than 3.5 s except the planned OFF windows; high-pass 60 Hz, low-pass 9 kHz; mix loudnorm -14 LUFS, true peak -1.7 dBFS.

| time | lines | mood / why (script arc) | energy 1-5 | track | hit / silence points |
|---|---|---|---|---|---|
| 0:00-0:36 | 1-5 | hook, suspense, sparse | 3 (open, ~12 LU under voice) | Disquiet | title-card hit 0:24; music OFF 0:27-0:30 at 'ye hua kaise?' |
| 0:36-1:44 | 6-16 | the Permian world, warm wonder, light | 2 | Quietude (The Imperfectionist, CC BY 4.0) | soft globe flash |
| 1:44-3:48 | 17-33 | disaster begins, numbers, rising density | 3 | Gathering Darkness | '96%' hit 2:18; dip before 96% / 4-19 |
| 3:48-5:35 | 34-48 | evidence (layers, ash, carbon): analytical, calm, quieter | 2 (about -19 LU) | Dark Fog | OFF 3:48-3:51 ('kaise pata?'); OFF 5:12-5:15 ('kaha se aaya?') then Siberia hit 5:15 |
| 5:35-6:47 | 49-58 | Siberian lava and gas: heavy, dark, powerful | 5 | Impact Prelude | lava hit 5:35; OFF 6:16-6:18 then 'the answer: gas' hit 6:18 |
| 6:47-9:05 | 59-76 | the four killers: low strings, driving tension | 3-4 | Giant Wyrm | OFF 8:19-8:22 (uncertainty line); four-killers hit 6:47 |
| 9:05-10:31 | 77-89 | survivors and recovery: brighter, hopeful | 3 | Inspired | OFF 9:04-9:07 then hope hit 9:07 |
| 10:31-11:38 | 90-98 | why it matters today: serious, restrained | 2 | Lightless Dawn | OFF 10:31-10:34 ('akhiri sawal'); dip before 1-1.5 C |
| 11:38-12:32 | 99-104 | ending: resolution, drone swell when the voice stops, 14 s fade | 3 (close, ~12 LU) | Quietude (reprise) | OFF 11:37-11:40 then closing hit 11:40 |

Tools: `tools/rc_music_analyze.py` (tempo, onset density, centroid, RMS dynamics, repetitiveness, flatness; 33 candidates measured, results in `cache/reality-check/002/music_analysis.txt`), `tools/rc_music_mix.py` + `long/music_cues.json`. Rejected: Touching Moments Two Higher (piano phrases fall to -50 dB every ~10 s = the 'du du' dips), Gymnopedie / Meditation Impromptu (slow minimal piano loops), Kick Shock / Mechanolith / Dangerous (trailer percussion).
Verified (full 752.24 s mix): -14.0 LUFS, LRA 4.4 LU, true peak -1.7 dBFS; music vs voice by 10 s window: open -11, body -14 to -20, lava -14, end -14 LU; 8 fully-off windows; longest quiet stretch 3.5 s; music stem spectral flatness 0.022 (tonal).

Credit block (CC BY 4.0) for the description when used:
Music: "Disquiet", "Gathering Darkness", "Dark Fog", "Impact Prelude", "Giant Wyrm", "Inspired", "Lightless Dawn", "Discovery Hit" by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0 License, http://creativecommons.org/licenses/by/4.0/ . "Quietude - Ambient Synth Soundscape Pack (01 Sections Merged)" by The Imperfectionist (freemusicarchive.org), CC BY 4.0.

Video sample clips (picture + new mix, 360p): `output/sound_samples/002_music_v4_clip_1_open_0-60s.mp4`, `..._2_lava_5m25-6m05.mp4`, `..._3_ending_last30s.mp4`. Not remuxed into the full video, nothing uploaded.
