from playwright.sync_api import sync_playwright
URL="https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":560,"height":1400}); pg.goto(URL,wait_until="networkidle",timeout=60000)
    t=pg.inner_text('article'); open('raw/page.txt','w',encoding='utf-8').write(t); print(len(t)); b.close()
