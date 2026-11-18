from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 560, "height": 900}, device_scale_factor=3)
    pg.goto("https://code.claude.com/docs/en/skills", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
    for sel in ("button:has-text('Reject all cookies')", "button:has-text('Reject all')"):
        try: pg.click(sel, timeout=2000); break
        except Exception: pass
    pg.evaluate("""() => { for (const t of ['All your projects on this machine','Sessions in this repository']) { const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); let n;
      while((n=w.nextNode())){const i=n.nodeValue.indexOf(t); if(i>=0 && !n.parentElement.closest('nav,aside,header')){const rg=document.createRange(); rg.setStart(n,i); rg.setEnd(n,i+t.length); const m=document.createElement('mark'); m.style.cssText='background:#FFD60A;color:#111'; rg.surroundContents(m); break;}} } }""")
    for name in ("Personal", "Project"):
        row = pg.locator("tr").filter(has=pg.locator("td:first-child", has_text=name)).first; row.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        bb = row.bounding_box(); print(name, bb); row.screenshot(path=f"row_{name.lower()}.png")
    b.close()
