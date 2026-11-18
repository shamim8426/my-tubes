from playwright.sync_api import sync_playwright
URLS = {"blog": "https://blog.google/innovation-and-ai/products/gemini-app/tasks-in-gemini-free-new-features/",
        "help": "https://support.google.com/gemini/answer/17094507?hl=en&co=GENIE.Platform%3DAndroid",
        "sched": "https://support.google.com/gemini/answer/17094710?hl=en&co=GENIE.Platform%3DAndroid",
        "sec": "https://blog.google/security/how-geminis-defense-in-depth-approach-works/",
        "rel": "https://gemini.google/release-notes/"}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 1100})
    for k, u in URLS.items():
        pg.goto(u, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(3500)
        t = pg.evaluate("() => (document.querySelector('article') || document.querySelector('main') || document.body).innerText")
        open(f"raw/page_{k}.txt", "w", encoding="utf-8").write(u + "\n\n" + t); print(k, len(t))
    b.close()
