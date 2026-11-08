"""Own Playwright capture of Google's official blog post: per key sentence a plain crop of its paragraph + per-line rects (live marker is animated in make.py)."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
H = Path(__file__).parent
URL = "https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/"
KEYS = {
 "len": "up to 15 seconds long",
 "price": "dropped the price 30%",
 "edit": "fix a detail with a follow-up edit",
 "vids": "no additional cost in Google Vids",
 "limit": "fast sports action",
}
FIND = """(keys) => { const out = {}; const norm = s => s.replace(/\s+/g, ' ');
 const blocks = [...document.querySelectorAll('p,li')];
 for (const [k, txt] of Object.entries(keys)) { const b = blocks.find(b => norm(b.textContent).includes(txt)); if (!b) { out[k] = null; continue; } b.setAttribute('data-blk', k); out[k] = txt; } return out; }"""
MARK = """([k, txt]) => { const blk = document.querySelector('[data-blk="'+k+'"]'); const norm = s => s.replace(/\s+/g, ' ');
 const full = norm(blk.textContent); const st = full.indexOf(txt), en = st + txt.length; const w = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT); let n, acc = 0; const nodes = [];
 while ((n = w.nextNode())) nodes.push(n);
 for (const nd of nodes) { const t = norm(nd.textContent); const a = Math.max(st, acc), z = Math.min(en, acc + t.length);
   if (z > a && t.trim()) { const r = document.createRange(); r.setStart(nd, Math.max(0, a - acc)); r.setEnd(nd, Math.min(nd.textContent.length, z - acc)); const m = document.createElement('mark'); m.setAttribute('data-k', k); try { r.surroundContents(m); } catch (e) {} }
   acc += t.length; } }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 700, "height": 1400}, device_scale_factor=2)
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    for sel in ['button:has-text("Reject")', 'button:has-text("Reject all")', 'button:has-text("Decline")']:
        try: pg.click(sel, timeout=1500)
        except Exception: pass
    pg.add_style_tag(content="header,nav,footer,[class*=cookie],[id*=cookie],[class*=Cookie],[class*=consent]{display:none!important} body{background:#fff!important} p,li{font-size:25px!important;line-height:1.5!important;color:#111!important} mark{background:transparent!important;color:inherit!important}")
    print(pg.evaluate(FIND, KEYS)); info = {}
    for k, txt in KEYS.items():
        pg.evaluate(MARK, [k, txt])
        el = pg.query_selector(f'[data-blk="{k}"]')
        if not el: continue
        el.scroll_into_view_if_needed(); bx = el.bounding_box()
        lines = pg.evaluate("k=>{const o=[];document.querySelectorAll('mark[data-k=\"'+k+'\"]').forEach(m=>[...m.getClientRects()].forEach(r=>o.push([r.x,r.y,r.width,r.height])));return o}", k)
        el.screenshot(path=str(H / f"raw/blocks/{k}.png"))
        info[k] = {"box": bx, "lines": [[l[0] - bx["x"], l[1] - bx["y"], l[2], l[3]] for l in lines]}
        print(k, bx["width"], bx["height"], len(lines))
    pg.screenshot(path=str(H / "raw/page_top.png"), clip={"x": 0, "y": 0, "width": 700, "height": 1100}) if False else None
    json.dump(info, open(H / "raw/blocks.json", "w"), indent=1); b.close()
