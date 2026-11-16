import json
from playwright.sync_api import sync_playwright
URL = "https://code.claude.com/docs/en/best-practices"
MARKS = {"top": "Give Claude a check to run", "pass": "comes back pass or fail", "ev": "ask Claude for", "hook": "make it a hook, a deny rule"}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 1000}, device_scale_factor=2)
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
    for sel in ("button:has-text('Reject all')", "button:has-text('Decline')", "button:has-text('Reject')"):
        try: pg.click(sel, timeout=1500); break
        except Exception: pass
    res = {}
    for k, txt in MARKS.items():
        r = pg.evaluate("""(t) => { document.querySelectorAll('mark.__m').forEach(m=>{m.replaceWith(...m.childNodes)});
            const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
            while ((n = w.nextNode())) { const i = n.nodeValue.toLowerCase().indexOf(t.toLowerCase()); if (i >= 0 && n.parentElement.offsetParent !== null && !['SCRIPT','STYLE'].includes(n.parentElement.tagName)) {
                const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + t.length); const m = document.createElement('mark'); m.className='__m'; m.style.cssText='background:#FFD60A;color:#111;padding:0 2px'; rg.surroundContents(m);
                m.scrollIntoView({block:'center'}); const b = m.getBoundingClientRect(); return [b.x, b.y, b.width, b.height, n.nodeValue.slice(Math.max(0,i-60), i+120)]; } } return null; }""", txt)
        res[k] = r
        if r: pg.wait_for_timeout(400); pg.screenshot(path=f"shot_{k}.png")
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300); pg.screenshot(path="shot_top.png")
    json.dump(res, open("rects.json", "w"), indent=1); b.close()
print(json.dumps(res, indent=1)[:1500])
