# Fact-check 021 how-claude-code-works (source: https://code.claude.com/docs/en/how-claude-code-works.md, read 2026-11-04)
Analogies ("jaise ek jaadugar", "jaise ek toolbox") are labelled explanations, not features. The magic-trick framing is a storytelling device only.
- "tum bolo: fix the failing tests" -> page example: 'When you say "fix the failing tests," Claude might: ...'
- Tests run again, checked -> "6. Run the tests again to verify"; phases: "gather context, take action, and verify results".
- Three phases -> "When you give Claude a task, it works through three phases: gather context, take action, and verify results."
- "Agentic loop = baar baar ghoomne wala chakkar" -> page title "The agentic loop"; "repeating until task complete" (diagram alt text: "...verifying results, and repeating until task complete"); "A bug fix cycles through all three phases repeatedly."
- gather context = read files to understand -> "searching files to understand your code"; take action = change code -> "editing to make changes"; verify = run tests -> "running tests to check its work".
- You need not name files/commands -> "You don't need to specify which files to read or what commands to run. Claude figures that out."
- Tools; text only without tools -> "Without tools, Claude can only respond with text. With tools, Claude can act: read your code, edit files, run commands, search the web..."
- Five tool categories shown (files, search, run, web, code intelligence) -> table: File operations / Search / Execution / Web / Code intelligence ("requires code intelligence plugins").
- You can interrupt -> "You're part of this loop too. You can interrupt at any point to steer Claude".
- Esc stops immediately -> "Press Esc to stop Claude immediately. The running tool call is canceled and Claude waits for your next instruction."
- Correction + Enter -> "Type a correction and press Enter without stopping Claude... it reads the message as soon as those calls finish... and adjusts before its next step." Example text on screen: "The issue is in the session handling" (page's own example).
- Delegate, don't dictate -> section heading "Delegate, don't dictate".
- Final CTA line (follow Yellow Bot): channel promo, no docs claim.
