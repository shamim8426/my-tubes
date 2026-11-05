# Fact-check 030 Output styles (second pass, 2026-11-05/06) - source https://code.claude.com/docs/en/output-styles.md
PASS - claims matched by grep on the page text (see quotes).
| Scene | Claim | Docs quote |
|---|---|---|
| hook | Output style sets Claude's role/tone/format; four built-in styles besides default | "An output style is a set of instructions that sets Claude's role, tone, and response format"; "four built-in styles besides its default" (Proactive, Concise, Explanatory, Learning) |
| concise | First sentence = result; no lead-in/recap | "the first sentence of a response states what happened or what the answer is"; "leaves out the lead-in, the step-by-step narration, and the closing recap" |
| explain | Insight blocks explain the choices | "adds short explanations of why it made the choices it made ... in a block labeled `Insight`"; "aren't written into your files as comments" |
| learn | Claude leaves code for you, TODO(human) | "it leaves a few lines for you"; "marks the spot with a `TODO(human)` comment" |
| proactive | Starts work right away, no questions on routine decisions | "starts implementing as soon as you send a task. It makes reasonable assumptions about routine decisions rather than stopping to ask" |
| switch | /output-style concise; instructions not guarantee; hook for every time | "run `/output-style <style>` to switch, for example `/output-style concise`"; "It doesn't guarantee that something always happens or never happens"; "For something that has to happen every time ... use a hook" |
Assets: docs screenshots by shoot.py (own screenshots of the official page, key sentence marked); sneaker photo = Wikimedia Commons "Adidas SL 72 OG.jpg" (CC0; shows adidas branding, used only as a generic sneaker); characters = AI-drawn stickers (labelled on screen).
