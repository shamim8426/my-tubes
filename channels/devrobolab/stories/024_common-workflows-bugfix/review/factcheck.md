# Fact-check 024 (source: https://code.claude.com/docs/en/common-workflows.md, section "Fix bugs efficiently", read 2026-11-04)
The doctor/symptoms analogy is a labelled explanation. Option A/B/C cards are an illustration of "a few ways", not page text.
- Step 1 "Share the error with Claude": prompt "I'm seeing an error when I run npm test".
- Step 2 "Ask for fix recommendations": prompt "suggest a few ways to fix the @ts-ignore in user.ts".
- Step 3 "Apply the fix": prompt "update user.ts to add the null check you suggested".
- Tips: "Tell Claude the command to reproduce the issue and get a stack trace; Mention any steps to reproduce the error; Let Claude know if the error is intermittent or consistent."
- "Sirf error kaafi nahi" is our wording of the tips (not a page quote).
