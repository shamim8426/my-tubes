# Night tidy of the common learnings (user 2026-11-07)

Goal: `shared/STYLE_LIBRARY.md` keeps ONLY good, useful, non-duplicate learnings that every channel and session can follow. New learnings land automatically in section 13 (the inbox, written by `tools/learn.py`); a night task cleans them up. Nothing of the user's is ever lost silently: the tidy log lists every removal with the reason, and git history keeps the old text.

## What the nightly tidy does (one pass, about 10-20 minutes, no paid calls, no video work)
1. Start: `git pull --ff-only` (or `git merge --ff-only origin/main`). If another DevRoboLab run is still running, wait; if it runs past 03:00, skip tonight. Only run at night (start 01:30-05:00); if started between 05:00 and 20:00 do nothing and report "raat ko".
2. Read all of `shared/STYLE_LIBRARY.md`. For every line in section 13 (the inbox):
   - **Useful and new** -> move it into the right numbered section (1-12), rewritten short and clear (what to do next time, one example, the date), or merge it into an existing bullet that says the same.
   - **Duplicate or says the same as an existing rule** -> merge into the one best bullet; keep the clearest wording; do not keep two copies.
   - **Wrong, outdated, replaced by a later user decision, or only about one single video** -> delete it (write it in the tidy log with the reason).
   - **Unclear** -> keep it in the inbox with `(unclear: needs the user)` and mention it in the report.
3. Also scan sections 0-12 for duplicates and contradictions (e.g. an older rule that a later user decision replaced, like the split-screen idea replaced by section 9). Keep the LATEST user decision, mark the older one "replaced by section N" or remove it. Never remove or weaken a line marked "user ... binding" unless a later user line replaces it; then keep the later one.
4. Keep the learnings that teach something: every kept rule says what to do and why (the mistake it prevents) in one or two sentences. The file stays easy to read: sections in order, no walls of text.
5. Check that the "Index of builds" still points to files that exist (`shared/style_library/*`, `tools/*`, `scripts/*`).
6. Write `shared/style_library/TIDY_LOG.md` (newest on top): date, how many inbox lines were moved / merged / deleted / left, and each deletion with its reason in one line.
7. Commit ONLY `shared/STYLE_LIBRARY.md` and `shared/style_library/TIDY_LOG.md` with the message `style library: night tidy <date>` and push to main (`git push origin HEAD:main`; on a rejected push fetch, merge and retry up to 3 times).
8. Report in short Hinglish: what was moved/merged/deleted, anything unclear for the user.

## Never
Never touch videos, secrets, channel plans, other files, or the user's rules' meaning; never copy other creators' frames/words into the library; never make anything public.
