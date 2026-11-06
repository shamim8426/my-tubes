"""Official-page screenshots (own Playwright capture of support.claude.com), key sentences marked yellow; rects -> raw/rects.json"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
H = Path(__file__).parent
URL = "https://claude.com/resources/articles/introducing-personal-finance-in-claude"
KEYS = {
 "intro": "securely connect your bank and card accounts and ask in your own words",
 "readonly": "Access is read-only, and Personal Finance can't move, manage, or invest your money.",
 "avail": "starts rolling out in beta this week, on the Pro, Max, and Ultra plans in the US",
 "plaid": "Your accounts are only connected once you sign in to your bank yourself through Plaid",
 "nopass": "so Claude doesn't ask for or see your bank password",
 "example": "it adds up your spending across the accounts you connected and sorts it by category",
 "mistakes": "Claude can make mistakes in its answers, so ask which transactions are behind a number, and check important figures with your bank.",
 "noadvice": "it isn't designed to give investment advice",
}
JS = """(keys) => {
 const out = {}; const root = document.querySelector('div.text-rich-text--article');
 const norm = s => s.replace(/\\s+/g, ' ').replace(/[\\u2018\\u2019]/g, "'");
 const blocks = [...root.querySelectorAll('p,li')];
 for (let [k, txt] of Object.entries(keys)) {
   let blk = null, st = -1;
   for (const b of blocks) { const i = norm(b.textContent).indexOf(txt); if (i >= 0) { blk = b; st = i; break; } }
   if (!blk) { out[k] = null; continue; }
   const en = st + txt.length; const w = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT); const nodes = []; let n;
   while ((n = w.nextNode())) nodes.push(n);
   let acc = 0;
   for (const nd of nodes) {
     const t = norm(nd.textContent); const a = Math.max(st, acc), z = Math.min(en, acc + t.length);
     if (z > a && t.trim()) { const r = document.createRange(); r.setStart(nd, a - acc); r.setEnd(nd, Math.min(nd.textContent.length, z - acc));
       const m = document.createElement('mark'); m.setAttribute('data-k', k); m.style.cssText = 'background:#FFD60A;color:#111;border-radius:3px;padding:0 1px'; try { r.surroundContents(m); } catch (e) {} }
     acc += t.length;
   }
 }
 return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 560, "height": 1400}, device_scale_factor=2)
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    for sel in ['button:has-text("Reject")', 'button:has-text("Reject all")', 'button:has-text("Decline")']:
        try: pg.click(sel, timeout=1500)
        except Exception: pass
    pg.add_style_tag(content="header,nav,footer,[class*=cookie],[id*=cookie],[class*=Cookie]{display:none!important} body{background:#fff!important} div.text-rich-text--article{background:#fff;padding:6px} div.text-rich-text--article p,div.text-rich-text--article li{font-size:23px!important;line-height:1.5!important} div.text-rich-text--article h2,div.text-rich-text--article h3{font-size:30px!important;line-height:1.25!important}")
    for y in range(0, 6000, 500):
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(500)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1500)
    pg.evaluate(JS, KEYS)
    art = pg.query_selector('div.text-rich-text--article')
    box = art.bounding_box(); print("article box", box)
    rects = {}
    for k in KEYS:
        els = pg.query_selector_all(f'mark[data-k="{k}"]')
        if els:
            rs = [e.bounding_box() for e in els]; x0 = min(r["x"] for r in rs); y0 = min(r["y"] for r in rs); x1 = max(r["x"] + r["width"] for r in rs); y1 = max(r["y"] + r["height"] for r in rs)
            rects[k] = [x0 - box["x"], y0 - box["y"], x1 - x0, y1 - y0]
        else: rects[k] = None
    for n, im in enumerate([e for e in art.query_selector_all('img') if (e.bounding_box() or {}).get('height', 0) > 120]):
        r = im.bounding_box(); rects[f"img{n}"] = [r["x"] - box["x"], r["y"] - box["y"], r["width"], r["height"]]
    art.screenshot(path=str(H / "raw/article.png"))
    json.dump({"box": box, "rects": rects}, open(H / "raw/rects.json", "w"), indent=1)
    print(json.dumps(rects, indent=1)); b.close()
