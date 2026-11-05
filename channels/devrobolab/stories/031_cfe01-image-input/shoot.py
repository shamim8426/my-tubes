"""Own screenshots of the official Claude Help Center article (key sentences marked yellow). Run: python shoot.py"""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
OUT = Path(__file__).parent / "shots"
URL = "https://support.claude.com/en/articles/8241126-upload-files-to-claude"
# name: (first phrase, last phrase, [phrases to mark])
R = {"intro": ("This article explains how to upload documents and images to Claude", "This article explains how to upload documents and images to Claude", ["upload documents and images to Claude"]),
     "how": ("You can upload files to Claude in several ways", "You can also copy images and paste them from your clipboard into Claude.", ['Add files or photos', 'copy images and paste them from your clipboard']),
     "formats": ("Claude supports the following image formats", "WebP", ["JPEG", "PNG", "GIF", "WebP"]),
     "limits": ("Chat uploads", "Up to 8000x8000 pixels", ["Up to 20 files per chat", "Up to 8000x8000 pixels"]),
     "tips": ("Use images that are 1000x1000 pixels or larger", "Avoid small or low-resolution images where possible", ["1000x1000 pixels or larger", "Avoid small or low-resolution images"]),
     "project": ("Files can be uploaded to individual chats", "for persistent reference across conversations", ["project's Files section"])}
MARK = """(ph)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const i=n.nodeValue.indexOf(ph);if(i>=0&&n.parentElement.offsetParent!==null&&!/^(SCRIPT|STYLE|TITLE)$/.test(n.parentElement.tagName)){
  const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+ph.length);const m=document.createElement('mark');m.style.cssText='background:#FFD60A;color:#111;padding:2px 4px;border-radius:5px';
  try{r.surroundContents(m)}catch(e){};return true}}return false}"""
BOX = """(ph)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){if(n.nodeValue.includes(ph)&&n.parentElement.offsetParent!==null&&!/^(SCRIPT|STYLE|TITLE)$/.test(n.parentElement.tagName)){
  const e=n.parentElement.closest('p,li,h1,h2,h3,td')||n.parentElement;const r=e.getBoundingClientRect();return [r.left,r.top+scrollY,r.right,r.bottom+scrollY]}}return null}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 420, "height": 1000}, device_scale_factor=2, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/150 Safari/537.36")
    print("status", pg.goto(URL, wait_until="networkidle", timeout=60000).status)
    pg.evaluate("document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e).position;if(s==='fixed'||s==='sticky'){e.style.visibility='hidden'}})")
    boxes = {name: (pg.evaluate(BOX, a), pg.evaluate(BOX, z)) for name, (a, z, marks) in R.items()}
    for name, (a, z, marks) in R.items():
        for m in marks: pg.evaluate(MARK, m)
    pg.wait_for_timeout(500)
    pg.screenshot(path=str(OUT / "_full.png"), full_page=True)
    full = Image.open(OUT / "_full.png").convert("RGB")
    for name, (a, z, marks) in R.items():
        ba, bz = boxes[name]
        print(name, ba, bz)
        if ba and bz:
            x0, x1 = min(ba[0], bz[0]) - 10, max(ba[2], bz[2]) + 10
            full.crop((int(max(0, x0) * 2), int((ba[1] - 8) * 2), int(min(420, x1) * 2), int((bz[3] + 8) * 2))).save(OUT / f"{name}.png")
    b.close()
