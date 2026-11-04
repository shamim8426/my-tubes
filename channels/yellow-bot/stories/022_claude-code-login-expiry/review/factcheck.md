# Fact-check 022 (source: https://code.claude.com/docs/en/changelog.md, entry 2.1.318, dated 2026-11-04, read 2026-11-04)
Analogy "jaise metro card ki expiry date" is a labelled explanation, not a feature. Placeholders <date> in mock-ups: the page gives no output format, so none is invented.
- "Claude Code 2.1.318, 4 Nov 2026" -> "Version: 2.1.318, Release date: November 4, 2026".
- "claude auth status me date jab tak claude.ai sign-in chalega, loginExpiresAt" -> "Added the date a stored claude.ai sign-in ends to `claude auth status` (`loginExpiresAt`)".
- "claude -p ki JSON report me credential_expires_at" -> "...and to `claude -p` JSON results (`credential_expires_at`)".
- "text output me khatam hone se 10 din pehle 1 line warning" -> "Added a one-line stderr warning to `claude -p` text output, starting 10 days before a stored claude.ai sign-in ends".
- "date nikalne ke baad sign-in fail; error saaf; claude -p me claude auth login aur claude setup-token ka naam" -> "Fixed the sign-in failure when a stored claude.ai login reaches its time limit: it now says so, and in `claude -p` names `claude auth login` and `claude setup-token`".
- Nothing about how long a login lasts, price or limits is claimed. Description: source URL + "Unofficial channel, not affiliated with Anthropic."
