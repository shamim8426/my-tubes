from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 760, "height": 900}, device_scale_factor=2)
    pg.goto("https://code.claude.com/docs/en/skills", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
    for t in ("All your projects on this machine", "Sessions in this repository"):
        r = pg.evaluate("""(t) => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
          while ((n = w.nextNode())) { const i = n.nodeValue.indexOf(t); if (i >= 0 && !n.parentElement.closest('nav,aside,header')) {
            const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + t.length); const m = document.createElement('mark'); m.style.cssText='background:#FFD60A;color:#111';
            rg.surroundContents(m); m.scrollIntoView({block:'center'}); const b=m.getBoundingClientRect(); return [b.x,b.y]; } } return null; }""", t)
        print(t, r)
    pg.wait_for_timeout(500); pg.screenshot(path="w_table.png"); b.close()
