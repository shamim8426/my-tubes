"""Own Playwright capture of official pages: per key sentence a plain crop of its paragraph + per-line rects (live marker is animated in make.py)."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
H = Path(__file__).parent
C = "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/"
D_ = "https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/"
F = "https://code.claude.com/docs/en/changelog"
JOBS = {
    "carbon_a": (C, "Carbon is our strongest model"),
    "carbon_p": (C, "$2 per million input tokens and $10 per million output tokens"),
    "fable": (F, "now the default Fable model"),
    "dec_a": (D_, "Evaluate up to 1,000 yes/no"),
    "dec_l": (D_, "150-250 ms end-to-end"),
    "dec_p": (D_, "$0.10 per 1M input tokens"),
}
FIND_ONE = r"""([k, txt]) => { const norm = s => s.replace(/\s+/g, ' '); const b = [...document.querySelectorAll('p,li')].find(b => norm(b.textContent).includes(txt)); if (!b) return false; b.setAttribute('data-blk', k); return true; }"""
MARK = r"""([k, txt]) => { const blk = document.querySelector('[data-blk="'+k+'"]'); const norm = s => s.replace(/\s+/g, ' ');
 const full = norm(blk.textContent); const st = full.indexOf(txt), en = st + txt.length; const w = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT); let n, acc = 0; const nodes = [];
 while ((n = w.nextNode())) nodes.push(n);
 for (const nd of nodes) { const t = norm(nd.textContent); const a = Math.max(st, acc), z = Math.min(en, acc + t.length);
   if (z > a && t.trim()) { const r = document.createRange(); r.setStart(nd, Math.max(0, a - acc)); r.setEnd(nd, Math.min(nd.textContent.length, z - acc)); const m = document.createElement('mark'); m.setAttribute('data-k', k); try { r.surroundContents(m); } catch (e) {} }
   acc += t.length; } }"""
only = sys.argv[1:] or list(JOBS)
bj = H / "raw/blocks.json"
info = json.load(open(bj, encoding="utf-8")) if bj.exists() else {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for k in only:
        url, txt = JOBS[k]
        pg = b.new_page(viewport={"width": 700, "height": 1400}, device_scale_factor=2)
        pg.goto(url, wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(4000)
        for sel in ['button:has-text("Reject")', 'button:has-text("Decline")']:
            try: pg.click(sel, timeout=1200)
            except Exception: pass
        pg.add_style_tag(content="header,nav,footer,[class*=cookie],[id*=cookie],[class*=consent]{display:none!important} body{background:#fff!important} p,li{font-size:25px!important;line-height:1.5!important;color:#111!important} mark{background:transparent!important;color:inherit!important}")
        if not pg.evaluate(FIND_ONE, [k, txt]):
            print(k, "NOT FOUND"); pg.close(); continue
        pg.evaluate(MARK, [k, txt]); el = pg.query_selector(f'[data-blk="{k}"]'); el.scroll_into_view_if_needed(); bx = el.bounding_box()
        lines = pg.evaluate("k=>{const o=[];document.querySelectorAll('mark[data-k=\"'+k+'\"]').forEach(m=>[...m.getClientRects()].forEach(r=>o.push([r.x,r.y,r.width,r.height])));return o}", k)
        el.screenshot(path=str(H / f"raw/blocks/{k}.png"))
        info[k] = {"box": bx, "lines": [[l[0] - bx["x"], l[1] - bx["y"], l[2], l[3]] for l in lines]}
        print(k, bx["width"], bx["height"], len(lines)); pg.close()
    b.close()
json.dump(info, open(bj, "w"), indent=1)

