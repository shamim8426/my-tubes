import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path(__file__).parent/"shots"
URL="https://code.claude.com/docs/en/output-styles"
ITEMS=[("intro","Claude Code includes four built-in styles besides its default",None),
 ("concise","the first sentence of a response states what happened or what the answer is",None),
 ("explain","withAuth",'pre'),
 ("learn","Learn by Doing",'pre'),
 ("cmd","/output-style concise",None),
 ("json","outputStyle",'pre')]
JS="""([phrase,tag])=>{
 const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n,hit=null;
 while(n=w.nextNode()){const i=n.nodeValue.indexOf(phrase);if(i>=0&&n.parentElement&&!/^(SCRIPT|STYLE)$/.test(n.parentElement.tagName)&&n.parentElement.offsetParent!==null){hit=[n,i];break}}
 if(!hit)return null;const [node,i]=hit;
 const r=document.createRange();r.setStart(node,i);r.setEnd(node,i+phrase.length);
 const m=document.createElement('mark');m.style.cssText='background:#FFD60A;color:#111;padding:2px 4px;border-radius:5px';
 try{r.surroundContents(m)}catch(e){}
 let el=m.parentElement;
 if(tag){const p=m.closest(tag);if(p)el=p}else{const b=m.closest('p,li,pre,td');if(b)el=b}
 el.setAttribute('data-shot','1');return true}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":380,"height":1100},device_scale_factor=2)
    r=pg.goto(URL,wait_until="networkidle",timeout=60000);print("status",r.status)
    for sel in ["button:has-text('Reject')","button:has-text('Decline')"]:
        try:
            pg.click(sel,timeout=1500)
        except Exception:pass
    for name,phrase,tag in ITEMS:
        pg.evaluate("document.querySelectorAll('[data-shot]').forEach(e=>e.removeAttribute('data-shot'))")
        if name in("explain","json"):
            ok=pg.evaluate("(ph)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n,e=null;while(n=w.nextNode()){if(n.nodeValue.includes(ph)&&n.parentElement.offsetParent!==null){e=n.parentElement.closest('pre')||n.parentElement.closest('[class*=code],figure')||n.parentElement.parentElement;break}}if(!e)return null;e.setAttribute('data-shot','1');return true}",phrase)
        else:
            ok=pg.evaluate(JS,[phrase,tag])
        print(name,ok)
        if name in("explain","json"):print(name,ok)
        if ok:
            el=pg.query_selector('[data-shot]');el.scroll_into_view_if_needed()
            pg.evaluate("document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e).position;if(s==='fixed'||s==='sticky'){e.style.visibility='hidden'}})")
            el.screenshot(path=str(OUT/f"{name}.png"))
    b.close()
