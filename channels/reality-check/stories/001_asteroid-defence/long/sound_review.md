# Sound review (2026-11-08)

## What the 6 studied videos did with sound (from brand/VIDEO_STUDY_2026-11-07.md, STYLE_GUIDE s.12)
The notes are THIN on sound; only these facts exist:
- Loudness: -15.8 to -22 LUFS integrated, LRA 2.6-5.1; 3 of 6 had peak >= 0 dBFS (clip risk). Ours: -14 LUFS / TP <= -1.5.
- Music: stems were not available, so music-vs-voice during speech could NOT be measured. Only upper bound from pauses: music is 4-8 dB under voice RMS in pauses (rises in pauses, sits lower while speaking). The "18-22 dB under" blog number is unverified.
- NOT in the notes: SFX types, SFX count, ducking curve, silence-before-reveal use, music genre per chapter. Nothing was measured there, so we do not claim the references did it. The design below follows repo rules (STYLE_GUIDE row "SFX: soft pop for text, low thud for impact, 14-20 dB under"; Jugnu EDIT_STYLE: accents 12-20 dB under, ambience 28 dB under, 12-20 accents per 4 min; RULES: mood change = crossfade >= 1 s; music ~12-14 LU under voice, measured on speech sections).
- Repo RULES: every external audio file needs a row in shared/assets_license.csv; own synthesised files = licence "own". STYLE_LIBRARY 7: "NO whoosh" was a DevRoboLab-only user rule, not for this channel.

## Previous state
Preview = voice + ONE loop (shared/music/mystery_bed.wav at 0.6 gain), no SFX, no chapter change, no ducking.

## New design (tools/rc_sound.py)
5 own synthesised pad beds by mood (curious, tense, calm, mystery, hopeful), 15 SFX, 2 ambiences; all in shared/sfx/rc and shared/music/rc, registered in assets_license.csv. Cue list: long/sound_cues.md. Stems: cache/reality-check/001/sound/.
