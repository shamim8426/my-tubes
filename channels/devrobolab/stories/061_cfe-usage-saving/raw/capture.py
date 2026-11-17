"""Own Playwright capture of the official Claude help pages with the key phrase marked yellow -> raw/shot_<key>.png + raw/rects.json
(viewport 900x1100 css, DPR 2). Run from the story folder."""
import json
from playwright.sync_api import sync_playwright
BEST = "https://support.claude.com/en/articles/9797557-usage-limit-best-practices"
LIM = "https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work"
MARKS = [
    ("session", LIM, "a session limit that resets every five hours"),
    ("same", LIM, "counts towards the same usage limit"),
    ("usage", BEST, "to view progress bars showing how much of your five-hour session"),
    ("factors", BEST, "Additional factors that affect your usage limits include"),
    ("batch", BEST, "send them all in one message"),
    ("vague", BEST, "Avoid vague queries that may require clarification"),
    ("cache", BEST, "count less against your limits than new content"),
    ("expire", BEST, "Caches expire after a period of inactivity"),
    ("effort", LIM, "Higher effort uses more tokens"),
    ("tools", LIM, "Tools and connectors are token-intensive"),
    ("long", LIM, "Longer conversations that trigger automatic context management consume more of your usage limit"),
    ("earlier", BEST, "As mentioned earlier"),
    ("credits", LIM, "With usage credits enabled"),
    ("adjust", LIM, "We may adjust usage limits at our discretion"),
]
JS = """(t) => { document.querySelectorAll('mark.__m').forEach(m=>{m.replaceWith(...m.childNodes)});
 const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
 while ((n = w.nextNode())) { const i = n.nodeValue.indexOf(t); if (i >= 0 && n.parentElement.offsetParent !== null && !['SCRIPT','STYLE'].includes(n.parentElement.tagName)) {
  const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + t.length); const m = document.createElement('mark'); m.className='__m';
  m.style.cssText='background:#FFD60A;color:#111;padding:0 2px;border-radius:3px'; rg.surroundContents(m);
  m.scrollIntoView({block:'center'}); const b = m.getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; } } return null; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 1100}, device_scale_factor=2)
    cur = None; res = {}
    for k, url, txt in MARKS:
        if url != cur:
            pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(3500); cur = url
            for sel in ("button:has-text('Reject')", "button:has-text('Decline')", "button:has-text('Accept only')"):
                try: pg.click(sel, timeout=1200); break
                except Exception: pass
            pg.add_style_tag(content="iframe {visibility:hidden !important}")
        r = pg.evaluate(JS, txt); res[k] = r
        if r: pg.wait_for_timeout(350); pg.screenshot(path=f"raw/shot_{k}.png")
        print(k, r)
    b.close()
json.dump(res, open("raw/rects.json", "w"), indent=1)
