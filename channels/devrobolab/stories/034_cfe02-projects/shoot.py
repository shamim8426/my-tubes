"""Own screenshots of the official Claude Help Center project articles, key sentences marked. Run: python shoot.py"""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
OUT = Path(__file__).parent / "shots"
U1 = "https://support.claude.com/en/articles/9517075-what-are-projects"
U2 = "https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects"
R = {U1: {"intro": ("Projects allow you to create self-contained workspaces", "have focused chats with Claude.", ["self-contained workspaces", "focused chats with Claude"]),
          "free": ("Projects are available to all users", "Free users can create a maximum of five projects.", ["all users", "maximum of five projects"])},
     U2: {"create": ("Hover over the left side of your account and click", "will not have access to these details", ["+ New Project", "will not have access to these details"]),
          "knowledge": ("find the project knowledge base", "Anything you upload to this space will be used across all of your chats within that project.", ["used across all of your chats within that project"]),
          "instr": ("Set project instructions", "Claude will use these instructions for all the chats within the project.", ["Set project instructions", "for all the chats within the project"]),
          "ctx": ("Context is not shared across chats within a project", "Context is not shared across chats within a project", ["Context is not shared across chats"])}}
MARK = """(ph)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const i=n.nodeValue.indexOf(ph);if(i>=0&&n.parentElement.offsetParent!==null&&!/^(SCRIPT|STYLE|TITLE)$/.test(n.parentElement.tagName)){
  const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+ph.length);const m=document.createElement('mark');m.style.cssText='background:#FFD60A;color:#111;padding:2px 4px;border-radius:5px';
  try{r.surroundContents(m)}catch(e){};return true}}return false}"""
BOX = """(ph)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){if(n.nodeValue.includes(ph)&&n.parentElement.offsetParent!==null&&!/^(SCRIPT|STYLE|TITLE)$/.test(n.parentElement.tagName)){
  const e=n.parentElement.closest('p,li,h1,h2,h3,td')||n.parentElement;const r=e.getBoundingClientRect();return [r.left,r.top+scrollY,r.right,r.bottom+scrollY]}}return null}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for url, items in R.items():
        pg = b.new_page(viewport={"width": 420, "height": 1000}, device_scale_factor=2, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/150 Safari/537.36")
        print("status", pg.goto(url, wait_until="networkidle", timeout=60000).status)
        pg.evaluate("document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e).position;if(s==='fixed'||s==='sticky'){e.style.visibility='hidden'}})")
        boxes = {n: (pg.evaluate(BOX, a), pg.evaluate(BOX, z)) for n, (a, z, m) in items.items()}
        for n, (a, z, marks) in items.items():
            for m in marks: pg.evaluate(MARK, m)
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / "_full.png"), full_page=True)
        full = Image.open(OUT / "_full.png").convert("RGB")
        for n in items:
            ba, bz = boxes[n]; print(n, ba, bz)
            if ba and bz:
                x0, x1 = min(ba[0], bz[0]) - 10, max(ba[2], bz[2]) + 10
                full.crop((int(max(0, x0) * 2), int((ba[1] - 8) * 2), int(min(420, x1) * 2), int((bz[3] + 8) * 2))).save(OUT / f"{n}.png")
        pg.close()
    b.close()
