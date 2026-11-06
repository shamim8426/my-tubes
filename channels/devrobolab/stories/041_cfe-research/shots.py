"""Official-page screenshots (own Playwright capture of support.claude.com), key sentences marked yellow; rects -> raw/rects.json"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
H = Path(__file__).parent
URL = "https://support.claude.com/en/articles/11088861-use-research-on-claude"
KEYS = {
 "intro": "It runs multiple searches that build on each other",
 "avail": "paid Claude plans (Pro, Max, Ultra, Team, or Enterprise) using Claude on the web, Claude Desktop, or Claude Mobile",
 "needweb": "You must have web search turned on for research to function.",
 "plus": "Click the",
 "indicator": "A blue indicator will appear on the bottom of the chat window.",
 "connectors": "Claude researches the web and your connected tools, including Google Workspace (Gmail, Google Calendar, and Google Docs)",
 "mobile": "When you start research in Claude Mobile, Claude only searches the web and doesn\u2019t use your connectors.",
 "limits": "research sessions can use up your limits faster",
}
JS = """(keys) => {
 const out = {}; const root = document.querySelector('article') || document.body;
 const blocks = [...root.querySelectorAll('p,li')];
 for (let [k, txt] of Object.entries(keys)) {
   const norm = s => s.replace(/\\s+/g, ' ');
   let blk = null, st = -1;
   if (k === 'plus') { blk = blocks.find(b => norm(b.textContent).startsWith('Click the')); st = 0; txt = norm(blk.textContent).split('Click the indicator')[0].split(' A blue')[0]; }
   else for (const b of blocks) { const i = norm(b.textContent).indexOf(txt); if (i >= 0) { blk = b; st = i; break; } }
   if (!blk) { out[k] = null; continue; }
   const en = st + txt.length; let pos = 0; const w = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT); const nodes = []; let n;
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
    for sel in ['button:has-text("Reject")', 'button:has-text("Reject all")']:
        try: pg.click(sel, timeout=1500)
        except Exception: pass
    pg.add_style_tag(content="header,nav,footer,[class*=cookie],[id*=cookie],[class*=Cookie]{display:none!important} body{background:#fff!important} article p,article li{font-size:23px!important;line-height:1.5!important} article h2{font-size:30px!important} article h3{font-size:25px!important}")
    art = pg.query_selector('article') or pg.query_selector('main')
    art.screenshot(path=str(H / "raw/article_plain.png"))  # v6: same page WITHOUT yellow marks (highlight is animated in the video)
    pg.evaluate(JS, KEYS)
    box = art.bounding_box(); print("article box", box)
    rects = {}; lines = {}
    for k in KEYS:
        els = pg.query_selector_all(f'mark[data-k="{k}"]')
        if els:
            rs = [e.bounding_box() for e in els]; x0 = min(r["x"] for r in rs); y0 = min(r["y"] for r in rs); x1 = max(r["x"] + r["width"] for r in rs); y1 = max(r["y"] + r["height"] for r in rs)
            rects[k] = [x0 - box["x"], y0 - box["y"], x1 - x0, y1 - y0]
            lines[k] = [[r[0] - box["x"], r[1] - box["y"], r[2], r[3]] for e in els for r in e.evaluate("e=>[...e.getClientRects()].map(r=>[r.x,r.y,r.width,r.height])")]
        else: rects[k] = None
    art.screenshot(path=str(H / "raw/article.png"))
    json.dump({"box": box, "rects": rects, "lines": lines}, open(H / "raw/rects.json", "w"), indent=1)
    print(json.dumps(rects, indent=1)); b.close()
