import sys
from playwright.sync_api import sync_playwright
URLS = {"best": "https://support.claude.com/en/articles/9797557-usage-limit-best-practices",
        "limits": "https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work",
        "projects": "https://support.claude.com/en/articles/9517075-what-are-projects"}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 1100})
    for k, u in URLS.items():
        pg.goto(u, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(3000)
        t = pg.evaluate("() => (document.querySelector('article') || document.body).innerText")
        open(f"raw/page_{k}.txt", "w", encoding="utf-8").write(u + "\n\n" + t)
        print(k, len(t))
    b.close()
