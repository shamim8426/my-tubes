# <Channel name> — edit style (for the Sampadak)

Copy this file to `channels/<key>/brand/EDIT_STYLE.md` and fill it once for a new channel. The Sampadak
(`.claude/agents/sampadak.md`) reads it before every video. Rules live in `shared/RULES.md` and the channel RULES;
this file only says how the finishing edit should LOOK and SOUND. Format of the plan: `tools/edit_fx.py` docstring.

## 1. Mood in one line
(e.g. "warm, playful, quick" or "calm, respectful, slow")

## 2. Look (grade / vignette / grain / light leak)
- grade: `warm_story` | `soft_glow` | `none`   · vignette: 0-0.25 · grain: 0-3.0 · light_leak: yes/no (day scenes only)

## 3. Transitions at scene changes
- allowed: cut | whip | flash | dip   · default: cut   · where each is allowed (e.g. whip only on chase scenes)
- banned: (list)

## 4. Camera / punch-ins / shake
- max punch-ins per minute: N · zoom 1.08-1.16 · shake only for: (e.g. a comic shout) · banned over: (e.g. Arabic text)

## 5. Text on screen (edit_fx styles: title | tag | note | pop)
- title: where/when · name tags: first appearance of each character · notes: riddles/clues (never the answer)
- fonts: Mukta (Hindi), Amiri (Arabic, libass only); never AI-drawn letters

## 6. Sound design
- allowed SFX (shared/sfx/, registered): ... · level: below the voice by N dB (accents 14-20 dB, ambience 26-30 dB)
- where: (reveals, jokes, scene changes) · never: (e.g. music/beat/vocals over religious text)

## 7. Never
- (channel-specific hard bans)

## 8. Learned from results (Nigraan) / approved by the user
- (date · what worked · what to repeat)
