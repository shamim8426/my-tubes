p='channels/devrobolab/templates/deck_template.html'
s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,b)

# CSS
rep(".dot3{display:flex", ".ic .f{fill:var(--fc,#FFD60A)}\n.dot3{display:flex")

# icon set + helpers (before B.statement builders: after smode)
rep("function tag(p,sc,txt)", r"""const IC={
terminal:'<rect class="f" x="2.5" y="4" width="19" height="16" rx="3"/><path d="M7 10l3 2.5-3 2.5M13 15.5h4.5"/>',
code:'<rect class="f" x="2.5" y="4" width="19" height="16" rx="3"/><path d="M10 9.5l-3 2.5 3 2.5M14 9.5l3 2.5-3 2.5"/>',
desktop:'<rect class="f" x="2.5" y="4" width="19" height="12.5" rx="2"/><path d="M9 20.5h6M12 16.5v4"/>',
globe:'<circle class="f" cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3.5 3.5 3.5 14.5 0 18M12 3c-3.5 3.5-3.5 14.5 0 18"/>',
phone:'<rect class="f" x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
file:'<path class="f" d="M6 2.5h8l4.5 4.5v14.5H6z"/><path d="M14 2.5V7h4.5M9 12h6M9 16h6"/>',
folder:'<path class="f" d="M2.5 6.5a2 2 0 0 1 2-2h5l2 2.5h8a2 2 0 0 1 2 2v9.5a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z"/>',
gear:'<circle class="f" cx="12" cy="12" r="6.5"/><circle cx="12" cy="12" r="2.3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1"/>',
bolt:'<path class="f" d="M13 2.5L5 13.5h6l-1 8 8-11h-6z"/>',
lock:'<rect class="f" x="4.5" y="10.5" width="15" height="11" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
plug:'<path d="M8.5 2.5v5M15.5 2.5v5"/><path class="f" d="M5.5 7.5h13v4a6.5 6.5 0 0 1-13 0z"/><path d="M12 18v3.5"/>',
sparkle:'<path class="f" d="M12 2.5l2.2 7.3 7.3 2.2-7.3 2.2L12 21.5l-2.2-7.3L2.5 12l7.3-2.2z"/>',
magnifier:'<circle class="f" cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5l6 6"/>',
check:'<circle class="f" cx="12" cy="12" r="9.5"/><path d="M7.5 12.5l3 3 6-7"/>',
cross:'<circle class="f" cx="12" cy="12" r="9.5"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7"/>',
arrow:'<path d="M3 12h17M14 6l6 6-6 6"/>',
clock:'<circle class="f" cx="12" cy="12" r="9.5"/><path d="M12 6.5V12l3.5 2.5"/>',
branch:'<circle class="f" cx="6" cy="5" r="2.5"/><circle class="f" cx="6" cy="19" r="2.5"/><circle class="f" cx="18" cy="9" r="2.5"/><path d="M6 7.5v9M18 11.5c0 4-5 4.5-12 6"/>',
chat:'<path class="f" d="M4 4.5h16a1.5 1.5 0 0 1 1.5 1.5v9.5a1.5 1.5 0 0 1-1.5 1.5h-8l-5 4v-4H4a1.5 1.5 0 0 1-1.5-1.5V6A1.5 1.5 0 0 1 4 4.5z"/><path d="M7.5 10h9M7.5 13h5"/>',
key:'<circle class="f" cx="8" cy="14" r="5"/><path d="M12 10.5l9-8M17.5 6l2.5 2.5M15 8.5l2 2"/>',
bulb:'<path class="f" d="M12 2.5a6.5 6.5 0 0 0-3.5 12v2.5h7v-2.5A6.5 6.5 0 0 0 12 2.5z"/><path d="M9.5 20.5h5M10.5 22.5h3"/>',
box:'<path class="f" d="M3 7.5l9-4.5 9 4.5v9l-9 4.5-9-4.5z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/>',
shield:'<path class="f" d="M12 2.5l8 3v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10v-6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
rocket:'<path class="f" d="M12 2.5c4 2 6 6 5.5 11l-3 3h-5l-3-3C6 8.5 8 4.5 12 2.5z"/><circle cx="12" cy="9.5" r="2"/><path d="M7.5 15L4.5 18.5M16.5 15l3 3.5M10 19.5l2 2 2-2"/>',
cursor:'<path class="f" d="M5 3l14 7-6 2-2 6z"/><path d="M13 12l5 5"/>',
play:'<circle class="f" cx="12" cy="12" r="9.5"/><path d="M10 8l6 4-6 4z" fill="#111"/>',
user:'<circle class="f" cx="12" cy="8" r="4"/><path d="M4.5 21c0-4.5 3.5-7 7.5-7s7.5 2.5 7.5 7"/>',
bug:'<ellipse class="f" cx="12" cy="14" rx="5" ry="6.5"/><path d="M12 7.5V20.5M7 11L3.5 9M17 11l3.5-2M7 16l-3.5 1.5M17 16l3.5 1.5M9.5 6.5L8 3.5M14.5 6.5L16 3.5"/>'};
function icSvg(name,sz,sw,fc){return `<svg class="ic" viewBox="0 0 24 24" width="${sz}" height="${sz}" fill="none" stroke="#111" stroke-width="${sw||1.7}" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible;flex:none;--fc:${fc||'#FFD60A'}">${IC[name]||IC.sparkle}</svg>`}
function icHtml(h){return h.replace(/<i data-ic="(\w+)"(?: data-s="(\d+)")?(?: data-f="(#\w+)")?><\/i>/g,(m,n,z,f)=>icSvg(n,z||84,1.7,f))}
function orbPos(O,lt){const a=((O.a0||0)+(O.w||12)*lt)*Math.PI/180;return [O.cx+O.rx*Math.cos(a),O.cy+(O.ry||O.rx)*Math.sin(a)]}
function ptOf(v,lt){return Array.isArray(v)?v:orbPos(v.orbit,lt)}
function polyAt(P,u){let tot=0;const seg=[];for(let i=1;i<P.length;i++){const d=Math.hypot(P[i][0]-P[i-1][0],P[i][1]-P[i-1][1]);seg.push(d);tot+=d}
  let t=c(u)*tot;for(let i=0;i<seg.length;i++){if(t<=seg[i]||i===seg.length-1){const q=seg[i]?t/seg[i]:0;return [P[i][0]+(P[i+1][0]-P[i][0])*q,P[i][1]+(P[i+1][1]-P[i][1])*q]}t-=seg[i]}return P[P.length-1]}
function tag(p,sc,txt)""")

# box html placeholders
rep("""else if(k==='box'){el=mk(root,`left:0;top:0;${L.css||''}`,L.html||'','abs '+(L.cls||''));""","""else if(k==='box'){el=mk(root,`left:0;top:0;${L.css||''}`,icHtml(L.html||''),'abs '+(L.cls||''));""")

# new layer kinds
rep("    else if(k==='text'){el=mk(root,", r"""    else if(k==='icon'){const sz=L.size||120;
      el=mk(root,`left:0;top:0;width:${L.lw||sz}px;display:flex;flex-direction:column;align-items:center`,icSvg(L.name,sz,L.sw,L.fill===false?'#fff':(L.fc||'#FFD60A'))+(L.label?`<div style="font-size:${L.ls||34}px;font-weight:800;line-height:1.1;margin-top:8px;text-align:center;white-space:nowrap">${L.label}</div>`:''),'abs');
      L.ic=[...el.querySelectorAll('svg *')];L.ic.forEach(n=>n.setAttribute('pathLength',1))}
    else if(k==='flow'){const ns='http://www.w3.org/2000/svg';L.x=0;L.y=0;
      el=mk(root,'left:0;top:0;width:1080px;height:1920px','<svg width="1080" height="1920" style="overflow:visible;display:block"></svg>','abs');const svg=el.firstChild;
      const NS=(t,a)=>{const e=document.createElementNS(ns,t);Object.entries(a||{}).forEach(([n,v])=>e.setAttribute(n,v));svg.appendChild(e);return e};
      const col=L.color||'#111';
      L.pl=NS('path',{fill:'none',stroke:col,'stroke-width':L.sw||7,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1});L.pl.style.strokeDasharray='1 1';
      L.hd=L.head===false?null:NS('path',{fill:'none',stroke:col,'stroke-width':L.sw||7,'stroke-linecap':'round','stroke-linejoin':'round'});
      L.pk=[];const n=L.n||2,r=L.r||15;for(let i=0;i<n;i++){const g=[NS('circle',{r:r*.5,fill:'#FFD60A',opacity:0}),NS('circle',{r:r*.72,fill:'#FFD60A',opacity:0}),NS('circle',{r:r,fill:'#FFD60A',stroke:'#111','stroke-width':5,opacity:0})];L.pk.push(g)}
      L.fx=(lt)=>{const P=(L.pts||[L.from,L.to]).map(v=>ptOf(v,lt));const at=L.at||0,du=L.dur||.6,q=c((lt-at)/du);
        L.pl.setAttribute('d','M'+P.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L'));L.pl.style.strokeDashoffset=String(1-eo(q));L.pl.setAttribute('stroke-opacity',q>0?1:0);
        if(L.hd){const a=P[P.length-2],b=P[P.length-1],an=Math.atan2(b[1]-a[1],b[0]-a[0]),hl=L.hl||30;L.hd.setAttribute('d',`M${b[0]-hl*Math.cos(an-.5)} ${b[1]-hl*Math.sin(an-.5)} L${b[0]} ${b[1]} L${b[0]-hl*Math.cos(an+.5)} ${b[1]-hl*Math.sin(an+.5)}`);L.hd.setAttribute('stroke-opacity',q>=.95?1:0)}
        const per=L.per||1.5,t0=at+du;L.pk.forEach((g,i)=>{const ph=(lt-t0-i*per/n)/per,on=ph>=0&&(L.until==null||lt<L.until);const u=ph-Math.floor(ph);
          g.forEach((e,j)=>{const pp=polyAt(P,Math.max(0,u-(2-j)*.045));e.setAttribute('cx',pp[0]);e.setAttribute('cy',pp[1]);e.setAttribute('opacity',on?[.35,.6,1][j]:0)})})}}
    else if(k==='ring'){const sz=L.size||260,sw=L.sw||26,rad=(sz-sw-14)/2,C=2*Math.PI*rad;
      el=mk(root,`left:0;top:0;width:${sz}px;height:${sz}px`,`<svg width="${sz}" height="${sz}" viewBox="0 0 ${sz} ${sz}" style="display:block"><circle cx="${sz/2}" cy="${sz/2}" r="${rad}" fill="none" stroke="#eee" stroke-width="${sw}"/><circle class="rb" cx="${sz/2}" cy="${sz/2}" r="${rad}" fill="none" stroke="#111" stroke-width="${sw+10}" stroke-linecap="round" transform="rotate(-90 ${sz/2} ${sz/2})"/><circle class="ry" cx="${sz/2}" cy="${sz/2}" r="${rad}" fill="none" stroke="#FFD60A" stroke-width="${sw}" stroke-linecap="round" transform="rotate(-90 ${sz/2} ${sz/2})"/></svg><div style="position:absolute;left:0;top:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:${sz*.27}px;font-weight:800">0%</div>`,'abs');
      const rb=el.querySelector('.rb'),ry=el.querySelector('.ry'),lb=el.lastChild;
      L.fx=(lt)=>{const f=c(kfv(L.k||[],lt,'f',L.f||0));const d=f*C;rb.setAttribute('stroke-dasharray',f<=0?'0 '+C:Math.max(.1,d)+' '+C);ry.setAttribute('stroke-dasharray',f<=0?'0 '+C:Math.max(.1,d)+' '+C);rb.setAttribute('opacity',f<=0?0:1);ry.setAttribute('opacity',f<=0?0:1);lb.textContent=Math.round(f*(L.mul||100))+(L.unit||'%')}}
    else if(k==='spark'){const ns='http://www.w3.org/2000/svg';L.x=0;L.y=0;
      el=mk(root,'left:0;top:0;width:1080px;height:1920px','<svg width="1080" height="1920" style="overflow:visible;display:block"></svg>','abs');const svg=el.firstChild;
      L.st=(L.pts||[]).map((p,i)=>{const e=document.createElementNS(ns,'path');e.setAttribute('d','M0 -1 L.26 -.26 1 0 .26 .26 0 1 -.26 .26 -1 0 -.26 -.26Z');e.setAttribute('fill','#FFD60A');e.setAttribute('stroke','#111');e.setAttribute('stroke-width',3.5);e.setAttribute('vector-effect','non-scaling-stroke');e.setAttribute('stroke-linejoin','round');svg.appendChild(e);return {e,x:p[0],y:p[1],s:p[2]||24,ph:p[3]!=null?p[3]:i*1.7}});
      L.fx=(lt)=>{L.st.forEach(S=>{const q=Math.max(0,Math.sin(lt*(L.sp||4)+S.ph));const sc=S.s*(.15+.85*q);S.e.setAttribute('transform',`translate(${S.x} ${S.y}) rotate(${q*40}) scale(${sc})`);S.e.setAttribute('opacity',q>.02?1:0)})}}
    else if(k==='typed'){el=mk(root,`left:0;top:0;width:${L.w||900}px;font-size:${L.size||56}px;font-weight:700;white-space:pre;color:${L.color||'#111'};${L.css||''}`,'','abs'+(L.mono?' mono':''));
      L.fx=(lt)=>{const tx=L.text||'',cps=L.cps||14,n=Math.floor(c((lt-(L.sat||0))/(tx.length/cps))*tx.length);const on=lt>=(L.sat||0)-.01;
        el.innerHTML=tx.slice(0,n).replace(/&/g,'&amp;').replace(/</g,'&lt;')+(L.cursor!==false&&on&&(n<tx.length||Math.floor(lt*2.6)%2===0)?'<span style="color:#FFD60A;background:#FFD60A">&nbsp;</span>':'')}}
    else if(k==='text'){el=mk(root,""")

# applyLayer
rep("const k=L.k||[],x=kfv(k,lt,'x',L.x),y0=","const k=L.k||[];let x=kfv(k,lt,'x',L.x);const y0=")
rep("  if(L.in!=null){const q=c((lt-L.in)","""  if(L.float){const F=typeof L.float==='number'?{a:L.float}:L.float;y+=Math.sin(lt*(F.f||1.8)+(F.ph||0))*(F.a||8)}
  if(L.orbit){const hs=(L.size||0)/2,P=orbPos(L.orbit,lt);x=P[0]-hs;y=P[1]-hs+(L.float?0:0)}
  if(L.pulse)s*=1+L.pulse*Math.sin(lt*4+(L.ph||0));
  if(L.drawon&&lt<L.drawon[0])o=0;
  if(L.in!=null){const q=c((lt-L.in)""")
rep("  const r=r0+(L.swing","  let r=r0+(L.swing")
rep("  L.el.style.opacity=o;L.el.style.transform=","""  if(L.spin)r+=L.spin*Math.max(0,lt-(L.spinAt||0));
  if(L.wig!=null&&lt>L.wig){const d=lt-L.wig;r+=Math.sin(d*34)*5*Math.max(0,1-d/.6)}
  if(L.ic&&L.drawon){const q=c((lt-L.drawon[0])/(L.drawon[1]||.6));L.ic.forEach(n=>{if(q>=1){n.style.strokeDasharray='none';n.style.strokeDashoffset='0'}else{n.style.strokeDasharray='1 1';n.style.strokeDashoffset=String(1-eo(q))}if(n.classList&&n.classList.contains('f'))n.style.fillOpacity=q>=1?1:Math.max(0,(q-.5)*2)})}
  L.el.style.opacity=o;L.el.style.transform=""")
rep("  if(L.pctEl){","  if(L.fx)L.fx(lt,o);\n  if(L.pctEl){")
open(p,'w',encoding='utf-8').write(s)

# build_deck: resolve_layer generalised
b='scripts/build_deck.py'
t=open(b,encoding='utf-8').read()
i=t.index("def resolve_layer"); j=t.index("def resolve_cues")
new='''def resolve_layer(sc, dur, L):
    L = dict(L)
    for f in ("sat", "in", "out", "hlAt", "at", "wig", "spinAt", "until"):
        if isinstance(L.get(f), str):
            L[f] = rt(sc, dur, L[f])
    if isinstance(L.get("drawon"), list) and isinstance(L["drawon"][0], str):
        L["drawon"] = [rt(sc, dur, L["drawon"][0])] + L["drawon"][1:]
    if L.get("k"):
        L["k"] = [[rt(sc, dur, f[0]), f[1]] for f in L["k"]]
    for f in ("talk", "wag", "nod"):
        if L.get(f):
            L[f] = [[rt(sc, dur, a), rt(sc, dur, b)] for a, b in L[f]]
    if L.get("items"):
        L["items"] = [dict(i, at=rt(sc, dur, i["at"])) if isinstance(i.get("at"), str) else i for i in L["items"]]
    return L


'''
t=t[:i]+new+t[j:]
open(b,'w',encoding='utf-8').write(t)
print('ok')
