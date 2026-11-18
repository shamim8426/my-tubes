"""Own Playwright capture of the official Google pages with the key phrase marked yellow -> raw/shot_<key>.png + raw/rects.json
(viewport 900x1100 css, DPR 2). Run from the story folder."""
import json
from playwright.sync_api import sync_playwright
BLOG = "https://blog.google/innovation-and-ai/products/gemini-app/tasks-in-gemini-free-new-features/"
HELP = "https://support.google.com/gemini/answer/17094507?hl=en&co=GENIE.Platform%3DAndroid"
SCHED = "https://support.google.com/gemini/answer/17094710?hl=en&co=GENIE.Platform%3DAndroid"
REL = "https://gemini.google/release-notes/?hl=en"
SEC = "https://blog.google/security/how-geminis-defense-in-depth-approach-works/"
MARKS = [
    ("blogfree", BLOG, "rolling out free of charge for hundreds of millions of people"),
    ("vm", BLOG, "hardware-isolated virtual machine"),
    ("inject", BLOG, "prompt-injection filters"),
    ("usfirst", BLOG, "advanced features, starting in the U.S."),
    ("helpfree", HELP, "Available without a Google AI subscription in Australia, Canada, India, Japan, South Korea, and the US."),
    ("age", HELP, "Be 18 or over."),
    ("inbox", HELP, "declutter your inbox"),
    ("price", HELP, "monitor and alert you when the prices of flights and hotels drop"),
    ("research", HELP, "pull research with cited sources"),
    ("tap", HELP, "Above the text box, tap Task."),
    ("control", HELP, "You can take control of the browser at any time."),
    ("fifteen", HELP, "You can have up to 15 tasks running at a given time."),
    ("exp", HELP, "ability to handle tasks is experimental"),
    ("off", HELP, "tap Turn off."),
    ("paused", HELP, "Your schedules and tasks are paused and not deleted."),
    ("monday", SCHED, "like every Monday morning"),
    ("hydrogen", REL, "running on our new Hydrogen 4 model"),
    ("english", REL, "Rolling out in English on web, Android, and iOS for users in the U.S."),
    ("microvm", SEC, "hardware-isolated microVMs built specifically for agents"),
    ("confirm", SEC, "require explicit confirmation before high-impact actions"),
]
JS = """(t) => { document.querySelectorAll('mark.__m').forEach(m=>{m.replaceWith(...m.childNodes)});
 const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
 while ((n = w.nextNode())) { const i = n.nodeValue.indexOf(t); if (i >= 0 && n.parentElement.offsetParent !== null && !['SCRIPT','STYLE'].includes(n.parentElement.tagName)) {
  const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + t.length); const m = document.createElement('mark'); m.className='__m';
  m.style.cssText='background:#FFD60A;color:#111;padding:0 2px;border-radius:3px'; rg.surroundContents(m);
  m.scrollIntoView({block:'center'}); const b = m.getBoundingClientRect(); const c = m.closest('p,li,div'); const cb = c ? c.getBoundingClientRect() : b;
  return [b.x, b.y, b.width, b.height, cb.x, cb.width]; } } return null; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 1100}, device_scale_factor=2)
    import sys; ONLY = set(sys.argv[1:])
    cur = None; res = {}
    for k, url, txt in MARKS:
        if ONLY and k not in ONLY: continue
        if url != cur:
            pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(3500); cur = url
            for sel in ("button:has-text('Reject all')", "button:has-text('Reject')", "button:has-text('Decline')", "button:has-text('Accept only')"):
                try: pg.click(sel, timeout=1200); break
                except Exception: pass
            pg.add_style_tag(content="iframe {visibility:hidden !important} header, [role=banner], .header, .glue-header {position:static !important}")
            # open collapsed help sections so hidden phrases are visible
            pg.evaluate("() => document.querySelectorAll('details').forEach(d => d.open = true)")
        r = pg.evaluate(JS, txt); res[k] = r
        if r: pg.wait_for_timeout(400); pg.screenshot(path=f"raw/shot_{k}.png")
        print(k, r, flush=True)
    if not ONLY or "toggle" in ONLY:
        pg.goto(BLOG, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(4000); pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(500)
        pg.screenshot(path="raw/shot_toggle.png"); print("toggle shot")
    b.close()
old = json.load(open("raw/rects.json")) if ONLY else {}
old.update(res); json.dump(old, open("raw/rects.json", "w"), indent=1)
