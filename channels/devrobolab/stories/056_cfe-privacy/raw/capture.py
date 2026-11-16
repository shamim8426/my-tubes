import json
from playwright.sync_api import sync_playwright
PAGES = {
 "priv": ("https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings",
          {"toggle": "Help Improve our AI models", "notundo": "Data already included in model training", "plans": "Claude Free, Pro, and Max"}),
 "inc": ("https://support.claude.com/en/articles/12260368-use-incognito-chats",
         {"ghost": "ghost icon", "label": "Incognito chat", "nosave": "aren't saved to your chat history", "reopen": "can't be reopened", "proj": "only available outside"}),
}
with sync_playwright() as p:
    b = p.chromium.launch(); res = {}
    for name, (url, marks) in PAGES.items():
        pg = b.new_page(viewport={"width": 1000, "height": 1000}, device_scale_factor=2)
        pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
        for sel in ("button:has-text('Reject all')", "button:has-text('Decline')", "button:has-text('Reject')"):
            try: pg.click(sel, timeout=1500); break
            except Exception: pass
        for k, txt in marks.items():
            r = pg.evaluate("""(t) => { document.querySelectorAll('mark.__m').forEach(m=>{m.replaceWith(...m.childNodes)});
                const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
                while ((n = w.nextNode())) { const i = n.nodeValue.toLowerCase().indexOf(t.toLowerCase()); if (i >= 0 && n.parentElement.offsetParent !== null && !['SCRIPT','STYLE'].includes(n.parentElement.tagName)) {
                    const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + t.length); const m = document.createElement('mark'); m.className='__m'; m.style.cssText='background:#FFD60A;color:#111;padding:0 2px'; rg.surroundContents(m);
                    m.scrollIntoView({block:'center'}); const b = m.getBoundingClientRect(); return [b.x, b.y, b.width, b.height, n.nodeValue.slice(Math.max(0,i-60), i+120)]; } } return null; }""", txt)
            res[f"{name}_{k}"] = r
            if r: pg.wait_for_timeout(400); pg.screenshot(path=f"shot_{name}_{k}.png")
        pg.close()
    json.dump(res, open("rects.json", "w"), indent=1); b.close()
print(json.dumps(res, indent=1)[:3000])
