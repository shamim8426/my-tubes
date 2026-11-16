# Facts - Claude Code 06 (Best practices). Source only: https://code.claude.com/docs/en/best-practices
1. "Claude stops when the work looks done... If you give it something that comes back pass or fail, Claude can close that loop itself." - PASS (crop shown, highlighted).
2. Check can be a test file, a build's exit code, a linter, a script diffing output, a browser screenshot - PASS (test, build, linter named).
3. Options: in the prompt ("run the auth tests after, and keep going until they pass"), as a goal (/goal all tests in tests/auth pass and lint is clean), as a Stop hook (runs script when Claude tries to end its turn; exit code 2 sends Claude back to work) - PASS.
4. "Ask Claude for evidence: the command it ran and its output" - PASS.
5. "If something has to happen every time, make it a hook, a deny rule, or a managed setting. CLAUDE.md is for guidelines" ; example rule "Never read .env" - PASS (crop shown).
6. Terminal windows and output "24 passed, 0 failed" are illustrations; labelled on screen.
