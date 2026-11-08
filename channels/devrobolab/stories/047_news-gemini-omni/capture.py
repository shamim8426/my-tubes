import json, sys
from playwright.sync_api import sync_playwright
URL = "https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/"
MARKS = {"len": "15 seconds", "price": "$0.07", "cut": "30%", "edit": "conversational", "where": "Google Vids", "caution": "fast sports"}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 1100}, device_scale_factor=2)
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(4000)
    for sel in ("button:has-text('Reject all')", "button:has-text('Decline')", "button:has-text('Reject')"):
        try: pg.click(sel, timeout=1500); break
        except Exception: pass
    res = {}
    for k, txt in MARKS.items():
        r = pg.evaluate("""(t) => { document.querySelectorAll('mark.__m').forEach(m=>{m.replaceWith(...m.childNodes)});
            const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
            while ((n = w.nextNode())) { const i = n.nodeValue.toLowerCase().indexOf(t.toLowerCase()); if (i >= 0 && n.parentElement.offsetParent !== null && !['SCRIPT','STYLE'].includes(n.parentElement.tagName)) {
                const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + t.length); const m = document.createElement('mark'); m.className='__m'; m.style.cssText='background:#FFD60A;color:#111;padding:0 2px'; rg.surroundContents(m);
                m.scrollIntoView({block:'center'}); const b = m.getBoundingClientRect(); return [b.x, b.y, b.width, b.height, n.nodeValue.slice(Math.max(0,i-60), i+80)]; } } return null; }""", txt)
        res[k] = r
        if r: pg.wait_for_timeout(400); pg.screenshot(path=f"raw/shot_{k}.png")
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500); pg.screenshot(path="raw/shot_top.png")
    json.dump(res, open("raw/rects.json", "w"), indent=1); b.close()
print(json.dumps(res, indent=1)[:900])
