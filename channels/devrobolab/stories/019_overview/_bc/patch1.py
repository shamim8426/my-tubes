import re
p='channels/devrobolab/templates/deck_template.html'
s=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a,s.count(a))
    s=s.replace(a,b)
# CSS
rep(".dot3{display:flex", """.mk .w{background:linear-gradient(#FFD60A,#FFD60A) no-repeat 0 97%/var(--mw,0%) 20%}
.sticky{background:#FFD60A;color:#111;border-radius:8px 8px 8px 46px;box-shadow:0 20px 34px rgba(0,0,0,.2)}
.torn{background:#fff;border:5px solid #111;border-bottom:0;box-shadow:0 18px 30px rgba(0,0,0,.14);clip-path:polygon(0 0,100% 0,100% 95%,95% 100%,90% 95%,85% 100%,80% 95%,75% 100%,70% 95%,65% 100%,60% 95%,55% 100%,50% 95%,45% 100%,40% 95%,35% 100%,30% 95%,25% 100%,20% 95%,15% 100%,10% 95%,5% 100%,0 95%)}
.keycap{display:inline-flex;align-items:center;justify-content:center;border:5px solid #111;border-bottom-width:13px;border-radius:22px;background:#fff;font-family:Mono,monospace;font-weight:700;padding:4px 26px;line-height:1.1}
#rail{position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none;display:none}
.dot3{display:flex""")
# words helper + streamRow
rep("function tag(p,sc,txt)", """function applyWords(ws,lt,t0,step,mode){
  ws.forEach((w,i)=>{const tw=t0+i*step,p=c((lt-tw)/.2),h=w.querySelector('[data-h]');
    if(mode==='grey'){const e=eo(p),g=Math.round(196-179*e);w.style.color='rgb('+g+','+g+','+g+')';w.style.opacity=.55+.45*e;w.style.filter=e<1?'blur('+((1-e)*2.4)+'px)':'none';w.style.transform='translateY('+((1-e)*10)+'px)'}
    else{const b=p<=0?0:back(p);w.style.opacity=c(p*2.5);w.style.transform='translateY('+(-(1-b)*30)+'px)';w.style.setProperty('--mw',(eo(c((lt-tw-.04)/.3))*100)+'%')}
    if(h)h.style.setProperty('--w',(eo(c((lt-tw-.08)/.4))*100)+'%')})}
function streamRow(sc,row,t,mode,step){if(mode!=='grey')row.classList.add('mk');reg(sc,row,t,'words',.2,{ws:[...row.querySelectorAll('.w')],step:step||.16,mode:mode})}
function smode(v){return v==='grey'?'grey':'marker'}
function tag(p,sc,txt)""")
# statement
rep("""    const row=mk(box,`font-size:${size}px`,parse(ln),'line');
    reg(sc,row,cue(sc,i,.5+i*.6),'rise',.55,{dy:70});""",
"""    const row=mk(box,`font-size:${size}px`,parse(ln),'line');
    if(sc.stream){streamRow(sc,row,cue(sc,i,.5+i*.6),smode(sc.stream),sc.step);return}
    reg(sc,row,cue(sc,i,.5+i*.6),'rise',.55,{dy:70});""")
# list icons
rep("""    row.innerHTML=`<div class="${i%2?'ink':'yel'}" style="flex:none;width:150px;height:150px;border-radius:36px;display:flex;align-items:center;justify-content:center;font-size:96px;font-weight:800">${i+1}</div><div><div style="font-size:${sc.ksize||88}px;font-weight:800;line-height:1.05">${it.k}</div><div style="font-size:${sc.dsize||52}px;font-weight:700;line-height:1.25;color:#333;margin-top:10px">${it.d}</div></div>`;""",
"""    const glyph=sc.icons?(it.ok===false?`<svg width="150" height="150" viewBox="0 0 150 150" style="flex:none"><circle cx="75" cy="75" r="68" fill="#111"/><path d="M48 48L102 102M102 48L48 102" stroke="#fff" stroke-width="16" stroke-linecap="round"/></svg>`:`<svg width="150" height="150" viewBox="0 0 150 150" style="flex:none"><circle cx="75" cy="75" r="68" fill="#FFD60A" stroke="#111" stroke-width="8"/><path d="M42 78L65 101L110 52" fill="none" stroke="#111" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>`):`<div class="${i%2?'ink':'yel'}" style="flex:none;width:150px;height:150px;border-radius:36px;display:flex;align-items:center;justify-content:center;font-size:96px;font-weight:800">${i+1}</div>`;
    row.innerHTML=`${glyph}<div><div style="font-size:${sc.ksize||88}px;font-weight:800;line-height:1.05">${it.k}</div>${(it.d||!sc.icons)?`<div style="font-size:${sc.dsize||52}px;font-weight:700;line-height:1.25;color:#333;margin-top:10px">${it.d}</div>`:''}</div>`;""")
# stage box shadow + count
rep("""else if(k==='box'){el=mk(root,`left:0;top:0;${L.css||''}`,L.html||'','abs '+(L.cls||''))}""",
"""else if(k==='box'){el=mk(root,`left:0;top:0;${L.css||''}`,L.html||'','abs '+(L.cls||''));if(L.sh)el.style.boxShadow='0 26px 60px rgba(0,0,0,.20)'}
    else if(k==='count'){el=mk(root,`left:0;top:0;font-size:${L.size||200}px;font-weight:800;line-height:1;${L.css||''}`,'0','abs');L.cnt=1}""")
# meter pct
rep("L.fillEl=el.firstChild}","L.fillEl=el.firstChild;if(L.pct)L.pctEl=mk(el,`left:0;top:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:${(L.h||56)*.62}px`,'0%','abs')}")
# text stream
rep("L.hls=[...el.querySelectorAll('[data-h]')]}","L.hls=[...el.querySelectorAll('[data-h]')];if(L.stream){L.mode=smode(L.stream);if(L.mode==='marker')el.classList.add('mk');L.ws=[...el.querySelectorAll('.w')]}}")
# applyLayer
rep("""const y=y0+(L.bob?Math.sin(lt*2.4)*10:0);""","""let s=s0,o=o0;let y=y0+(L.bob?Math.sin(lt*2.4)*10:0);
  if(L.in!=null){const q=c((lt-L.in)/(L.ind||.35));s*=.6+.4*(L.spring?back(q):eo(q));o*=lt<L.in?0:c(q*2.2)}
  if(L.out!=null){const q=c((lt-L.out)/.25);o*=1-q;y+=30*q}
  if(L.push)s*=1+.06*c((lt-(L.in||0))/L.push);
  if(L.cnt){const f=kfv(k,lt,'f',0),pv=f*(L.to||1),v=Math.floor(pv+1e-6),fr=pv>=(L.to||1)?1:pv-Math.floor(pv);L.el.textContent=(L.pre||'')+v+(L.suf||'');s*=1+.22*Math.max(0,1-fr*3.5)}
  if(L.ws){applyWords(L.ws,lt,L.sat||0,L.step||.16,L.mode);if(L.mode==='grey')o*=c((lt-((L.sat||0)-.15))/.2)}""")
rep("s=kfv(k,lt,'s',1),r0=kfv(k,lt,'r',0),o=c(kfv(k,lt,'o',1));","s0=kfv(k,lt,'s',1),r0=kfv(k,lt,'r',0),o0=c(kfv(k,lt,'o',1));")
rep("  if(L.fillEl){","  if(L.pctEl){L.pctEl.textContent=Math.round(c(kfv(k,lt,'f',L.f||0))*(L.mul||100))+(L.unit||'%')}\n  if(L.fillEl){")
rep("function applyItem(it,lt){\n","function applyItem(it,lt){\n  if(it.kind==='words'){const el=it.el;if(lt<it.t0){el.style.opacity=0;return}el.style.opacity=1;applyWords(it.ws,lt,it.t0,it.step,it.mode);return}\n")
rep("window.SFX=", """if(D.rail){const R=E('rail');R.style.display='block';const n=scenes.length,y0=330,y1=1620;
  R.innerHTML='<div style="position:absolute;left:1040px;top:'+y0+'px;width:14px;height:'+(y1-y0)+'px;border-radius:7px;background:#eee"></div><div id="railf" style="position:absolute;left:1040px;top:'+y0+'px;width:14px;height:0;border-radius:7px;background:#FFD60A;border:3px solid #111;box-sizing:border-box"></div>';
  scenes.forEach((s,i)=>{mk(R,'left:1033px;top:'+(y0+(y1-y0)*i/(n-1)-14)+'px;width:28px;height:28px;border-radius:14px;background:#fff;border:5px solid #111','','abs')});
  mk(R,'left:880px;top:110px;font-size:44px;font-weight:800;width:150px;text-align:right;line-height:1.55','','abs').id='railn'}
window.SFX=""")
rep("const out=c((sc.end-t)/.2);sc.root.style.opacity=cur===scenes.length-1?1:(.15+.85*out);",
"""const nf=scenes[cur+1]&&scenes[cur+1].wipe==='fade';
  const out=nf?1:c((sc.end-t)/.2);sc.root.style.opacity=cur===scenes.length-1?1:(.15+.85*out);
  if(D.rail){const n=scenes.length;E('railf').style.height=((1290)*c((cur+c(lt/(sc.end-sc.start)))/(n-1)))+'px';E('railn').textContent=(cur+1)+'/'+n}
  if(cur>0&&sc.wipe==='fade'&&lt<.25){const q=eio(lt/.25),pv=scenes[cur-1],pl=pv.end-pv.start-.001;pv.root.style.display='block';pv.anims.forEach(it=>applyItem(it,pl));if(pv.upd)pv.upd(pl);pv.root.style.opacity=1-q;sc.root.style.opacity=q}""")
rep("if(cur>0&&lt<wd){","if(cur>0&&lt<wd&&sc.wipe!=='fade'){")
rep('<div id="bar"></div>','<div id="bar"></div><div id="rail"></div>')
open(p,'w',encoding='utf-8').write(s)
print('ok')
