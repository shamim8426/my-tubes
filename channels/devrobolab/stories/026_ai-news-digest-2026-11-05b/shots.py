"""Official-page proof screenshots: real Chrome via Playwright, key sentence marked yellow."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE = Path(__file__).parent
JOBS = {
 "img26": ("https://openai.com/index/introducing-images-2-6", ["Images 2.6 generates images 50% faster than before.", "Images 2.6 is available globally today in ChatGPT and Codex across all subscription tiers"]),
 "voxtral": ("https://mistral.ai/news/voxtral-3", ["Accurate transcription across 50+ languages", "Available today through"]),
 "xcode": ("https://github.blog/changelog/2026-11-04-github-copilot-is-now-available-in-xcodes-coding-assistant", ["The integration is now in public preview", "All Copilot plans are supported."]),
 "dharma": ("https://huggingface.co/blog/Dharma-AI/dharma-field-extractor", ["A 2-billion-parameter model that extracts exactly the fields you ask for", "returns structured JSON"]),
}
JS = """(s)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const i=n.nodeValue.indexOf(s);if(i>=0&&n.parentElement&&n.parentElement.offsetParent!==null){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+s.length);const m=document.createElement('mark');m.style.cssText='background:#FFD60A;color:#111;padding:2px 3px;border-radius:4px';r.surroundContents(m);m.scrollIntoView({block:'center'});const b=m.getBoundingClientRect();return [b.top+window.scrollY,b.bottom+window.scrollY]}}return null}"""
with sync_playwright() as p:
    try: b = p.chromium.launch(channel="chrome")
    except Exception: b = p.chromium.launch()
    for key, (url, finds) in JOBS.items():
        pg = b.new_page(viewport={"width": 1200, "height": 900}, device_scale_factor=1.5, color_scheme="light")
        pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(3500)
        pg.evaluate("document.querySelectorAll('*').forEach(e=>{const p=getComputedStyle(e).position;if(p==='fixed'||p==='sticky')e.style.display='none'})")
        for k, f in enumerate(finds):
            pos = pg.evaluate(JS, f)
            print(key, k, pos)
            if not pos: continue
            y0 = max(0, int(pos[0]) - 150)
            pg.screenshot(path=str(HERE / "img" / f"{key}_{k}.png"), full_page=True, clip={"x": 0, "y": y0, "width": 1200, "height": 675})
        pg.close()
    b.close()
