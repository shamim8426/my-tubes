"""Own Playwright capture of official pages: per key sentence a plain crop of its paragraph + per-line rects (live marker is animated in make.py)."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
H = Path(__file__).parent
CM = "https://code.claude.com/docs/en/code-mode"
LL = "https://huggingface.co/blog/ggml-org/llama-cpp-v1"
GR = "https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/"
JOBS = {
    "cm_a": (CM, "Claude writes a piece of JavaScript that makes the tool calls"),
    "cm_b": (CM, "Code Mode is experimental and off by default."),
    "ll_a": (LL, "llama.cpp makes it possible to run multi-modal LLMs across a wide range of hardware"),
    "ll_b": (LL, "both llama.cpp and ggml will reflect API and ABI incompatibilities with major-version bumps"),
    "gr_a": (GR, "30% to 100% higher success rate"),
    "gr_b": (GR, "rolling out to our robotics partners"),
}
FIND_ONE = r"""([k, txt]) => { const norm = s => s.replace(/\s+/g, ' '); const c = [...document.querySelectorAll('p,li,div,blockquote,span')].filter(b => b.offsetParent !== null && b.textContent.length < 800 && norm(b.textContent).includes(txt)); if (!c.length) return false; c.sort((a, b) => a.textContent.length - b.textContent.length); c[0].setAttribute('data-blk', k); return true; }"""
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
        pg = b.new_context(bypass_csp=True, viewport={"width": 700, "height": 1400}, device_scale_factor=2).new_page()
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




