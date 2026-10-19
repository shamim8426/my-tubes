# Munshi R2 — script / plan stage — 004_chhat-par-bhoot (Long 03 + Short A)

Date: 2026-10-19 · Verdict: **PASS-WITH-NOTES** (RULES 15: MINOR after R2 -> carry_over.md) · STOP condition: none · Rs0

## R1 items re-checked (opened the files myself)
- M1 fixed: long/lines.json crickets pause 0.15, line 2 af atempo=1.33 (net 1.064). Re-estimate (make_short logic, Long 02 measured rates): Golu first word 0.75 s, intro ends ~9.66 s (<= 9.8 target). Long total 3:42-3:46 (Mishra 0.45-0.54 s/word @1.0).
- M2 fixed: Short meta speed 1.08, gap 0.15 / 0.30, one mood (tension), sfx only steps -> estimate 36.7 s (35-40 ok).
- M3 fixed: scene 15 uses {mitthu} + ref "mitthu" (7 refs, +~Rs0.2), "No other people".
- M4 fixed: scene 16 = Dadi, Golu, Mishra dada, Mitthu only ("Exactly these four, no other people"), group in left 60%, right side open starry sky.
- M5 fixed: description moral "डर को देख लो, तो वो आधा रह जाता है।", pinned comment has no Mishra name / twist; hashtags rotated (#किस्सागो #छतपरभूत #HindiStory #BhootKiKahani #MohallaKahani, 5).
- Notes: PLAN §1/§4 updated (0.15 s, atempo 1.33, 1.08/0.15/0.30, RULES 15 reason); CREDITS.md stale lines marked "moved to _to_delete/sfx_unused".

## New problem from the fix (MINOR, free -> carry_over)
- N1 Short A: lines.json line 4 (Pandey "सीढ़ी...") still has "sfx_after": "comedy", but meta "sfx" now only has "steps". make_short.py line 595 does SFX_DIR / meta["sfx"][kind] -> KeyError, the Short build stops. Fix before the Short build: add "comedy": "comedy_sting_731262.mp3" back to Short meta sfx (register row 45, CC0), or remove the sfx_after.

## Notes
- Long lower margin thin: at Mishra 0.45 s/word the estimate is 3:41.6 (1.6 s over 3:40). After TTS, if under 3:40: raise end_hold / gap (free).
- Pinned comment wording "आपने कभी किसी चीज़ से डरकर बाद में हँसी आई हो?" reads a bit off; e.g. "क्या आपको भी कभी किसी चीज़ से डरने के बाद हँसी आई है?" (taste).
