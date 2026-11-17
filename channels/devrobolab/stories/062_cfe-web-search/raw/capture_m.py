import json
from playwright.sync_api import sync_playwright
PAGES = {
 "ws": ("https://support.claude.com/en/articles/10684626-enabling-and-using-web-search",
        {"plus": "lower left", "toggle": "Web search", "check": "checkmark", "cite": "citations", "cap": "Capabilities",
         "limits": "contribute to these limits", "newexp": "new Claude", "tip": "Search the web", "verify": "multiple sources"}),
 "blog": ("https://claude.com/blog/web-search",
          {"global": "available globally", "latest": "latest events"}),
}
with sync_playwright() as p:
    b = p.chromium.launch(); res = {}
    for name, (url, marks) in PAGES.items():
        pg = b.new_page(viewport={"width": 430, "height": 932}, device_scale_factor=2.5)
        pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
        for sel in ("button:has-text('Reject all')", "button:has-text('Decline')", "button:has-text('Reject')"):
            try: pg.click(sel, timeout=1500); break
            except Exception: pass
        res[name + "_text"] = pg.evaluate("document.body.innerText")[:6000]
        for k, txt in marks.items():
            r = pg.evaluate("""(t) => { document.querySelectorAll('mark.__m').forEach(m=>{m.replaceWith(...m.childNodes)});
                const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
                while ((n = w.nextNode())) { const i = n.nodeValue.toLowerCase().indexOf(t.toLowerCase()); if (i >= 0 && n.parentElement.offsetParent !== null && !['SCRIPT','STYLE','A','BUTTON','H1','TITLE'].includes(n.parentElement.tagName) && n.nodeValue.length > 30) {
                    const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + t.length); const m = document.createElement('mark'); m.className='__m'; m.style.cssText='background:#FFD60A;color:#111;padding:0 2px'; rg.surroundContents(m);
                    m.scrollIntoView({block:'center'}); const b = m.getBoundingClientRect(); return [b.x, b.y, b.width, b.height, n.nodeValue.slice(Math.max(0,i-80), i+160)]; } } return null; }""", txt)
            res[f"{name}_{k}"] = r
            if r: pg.wait_for_timeout(400); pg.screenshot(path=f"m_{name}_{k}.png")
        pg.close()
    json.dump(res, open("rects_m.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False); b.close()
for k, v in res.items():
    if not k.endswith("_text"): print(k, v)
