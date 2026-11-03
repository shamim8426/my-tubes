p='channels/yellow-bot/templates/deck_template.html'
s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:70],s.count(a))
    s=s.replace(a,b)

# ---- CSS + DOM
rep(".ic .f{fill:var(--fc,#FFD60A)}", """.ic .f{fill:var(--fc,#FFD60A)}
.gl{background:linear-gradient(100deg,#111 0%,#111 calc(var(--g,-30%) - 14%),#FFD60A calc(var(--g,-30%) - 4%),#fff var(--g,-30%),#FFD60A calc(var(--g,-30%) + 4%),#111 calc(var(--g,-30%) + 14%),#111 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
#portal{position:absolute;border-radius:50%;border:38px solid #FFD60A;box-shadow:0 0 0 8px #111,inset 0 0 0 8px #111,0 0 90px 30px rgba(255,214,10,.55);display:none;box-sizing:border-box;pointer-events:none}""")
rep('<div id="bar"></div><div id="rail"></div>','<div id="bar"></div><div id="rail"></div><div id="portal"></div><svg width="0" height="0" style="position:absolute"><filter id="goo" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur in="SourceGraphic" stdDeviation="7" result="b"/><feColorMatrix in="b" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 24 -10"/></filter></svg>')

# ---- helpers
rep("function tag(p,sc,txt)", r"""const rn=(i,k)=>{const v=Math.sin(i*127.1+k*311.7+7.3)*43758.5453;return v-Math.floor(v)};
function cv(root){const e=document.createElement('canvas');e.width=1080;e.height=1920;e.style.cssText='position:absolute;left:0;top:0;width:1080px;height:1920px';root.appendChild(e);return {el:e,g:e.getContext('2d')}}
function star(g,x,y,r,rot,fill,stroke,lw){g.save();g.translate(x,y);g.rotate(rot||0);g.beginPath();for(let i=0;i<8;i++){const a=i*Math.PI/4-Math.PI/2,rr=i%2?r*.28:r;g.lineTo(Math.cos(a)*rr,Math.sin(a)*rr)}g.closePath();if(fill){g.fillStyle=fill;g.fill()}if(stroke){g.lineWidth=lw||2.5;g.strokeStyle=stroke;g.lineJoin='round';g.stroke()}g.restore()}
function glow(g,x,y,r,a){const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,'rgba(255,214,10,'+a+')');gr.addColorStop(1,'rgba(255,214,10,0)');g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()}
function wandPath(L){const S=L.shape||'poly',P=[],M=110;
  if(S==='circle'){for(let i=0;i<=M;i++){const th=-1.2+i/M*Math.PI*2*1.04;P.push([L.cx+L.rx*Math.cos(th),L.cy+L.ry*Math.sin(th)])}}
  else{const pts=L.pts||[L.from,L.to];for(let i=0;i<=M;i++){const p=polyAt(pts,i/M);P.push(S==='underline'?[p[0],p[1]+Math.sin(i/M*Math.PI*4)*6]:p)}}
  return P}
function tag(p,sc,txt)""")

# ---- layer builders
rep("    else if(k==='text'){el=mk(root,", r"""    else if(k==='dust'||k==='wand'||k==='assemble'||k==='shock'||k==='aura'||k==='poof'){const C=cv(root);el=C.el;const g=C.g;L.x=0;L.y=0;
      const clr=()=>g.clearRect(0,0,1080,1920);
      if(k==='dust')L.fx=(lt)=>{clr();const n=L.n||60,at=L.at||0,dur=L.dur||0,life=L.life||1.2,F=L.from||[540,900];if(lt<at||lt>at+dur+life)return;
        for(let i=0;i<n;i++){const b=at+(L.mode==='fountain'?i/n*dur:0),age=lt-b;if(age<0||age>life)continue;const u=age/life,sp=(L.speed||520)*(.35+.65*rn(i,2));
          const ang=L.mode==='fountain'?-Math.PI/2+(rn(i,1)-.5)*(L.spread||1.2):rn(i,1)*Math.PI*2,dr=1-.45*u;
          const x=F[0]+Math.cos(ang)*sp*age*dr,y=F[1]+Math.sin(ang)*sp*age*dr+.5*(L.grav||500)*age*age,s=(L.size||16)*(.5+rn(i,3))*(1-.3*u),t=i%5;
          g.globalAlpha=Math.max(0,1-u*u);
          if(t===0||t===3)star(g,x,y,s*1.3,age*3+i,'#FFD60A','#111',2.5);
          else if(t===1){glow(g,x,y,s*2.6,.55);g.fillStyle='#FFD60A';g.beginPath();g.arc(x,y,s*.5,0,7);g.fill()}
          else if(t===2){g.fillStyle='#111';g.beginPath();g.arc(x,y,s*.35,0,7);g.fill()}
          else star(g,x,y,s*.9,-age*2,'#fff','#111',2)}
        g.globalAlpha=1};
      if(k==='wand'){L.P=wandPath(L);L.fx=(lt)=>{clr();const P=L.P,at=L.at||0,dur=L.dur||1,N=P.length-1;if(lt<at-.02)return;
        const at_=(t)=>P[Math.min(N,Math.floor(eo(c((t-at)/dur))*N))],m=Math.floor(eo(c((lt-at)/dur))*N),fa=L.fadeAt!=null?1-c((lt-L.fadeAt)/.4):1;
        if(fa<=0)return;g.globalAlpha=fa;
        if(m>1){g.lineCap='round';g.lineJoin='round';g.beginPath();for(let i=0;i<=m;i++)i?g.lineTo(P[i][0],P[i][1]):g.moveTo(P[i][0],P[i][1]);g.lineWidth=(L.sw||18)+9;g.strokeStyle='#111';g.stroke();g.lineWidth=L.sw||18;g.strokeStyle='#FFD60A';g.stroke()}
        for(let q=0;q<16;q++){const tk=lt-q*.04;if(tk<at)continue;const p=at_(tk),a=(1-q/16)*fa;g.globalAlpha=a;star(g,p[0]+(rn(q,5)-.5)*q*4,p[1]+(rn(q,6)-.5)*q*4+q*1.5,(L.ss||22)*(1-q/20),tk*5+q,q%3?'#FFD60A':'#fff','#111',2.2)}
        const hf=c(1-(lt-at-dur)/.35);if(hf>0){const p=at_(lt);g.globalAlpha=hf*fa;glow(g,p[0],p[1],95,.9);star(g,p[0],p[1],36,lt*4,'#fff','#111',3)}g.globalAlpha=1}}
      if(k==='assemble')L.fx=(lt)=>{clr();const at=L.at||0,dur=L.dur||1,cx=L.cx||540,cy=L.cy||900,size=L.size||200;let u=c((lt-at)/dur);if(L.reverse)u=1-u;if(!L.reverse&&lt<at)return;
        if(!L.pts){const oc=document.createElement('canvas');oc.width=1000;oc.height=Math.ceil(size*1.5);const o=oc.getContext('2d');o.font='800 '+size+'px Pop';o.textAlign='center';o.textBaseline='middle';o.fillStyle='#000';o.fillText(L.text,500,oc.height/2);
          const d=o.getImageData(0,0,oc.width,oc.height).data,gap=L.gap||8,pts=[];for(let y=0;y<oc.height;y+=gap)for(let x=0;x<oc.width;x+=gap)if(d[(y*oc.width+x)*4+3]>140)pts.push([cx+x-500,cy+y-oc.height/2]);L.pts=pts}
        const ca=c((u-.82)/.18);
        L.pts.forEach((T,i)=>{const dl=rn(i,1)*.45,q=eo(c((u-dl)/.55)),a=rn(i,2)*Math.PI*2,rad=230+rn(i,3)*380,sw=(1-q)*Math.sin(lt*2.2+i)*34;
          const x=T[0]+(Math.cos(a)*rad+sw)*(1-q),y=T[1]+(Math.sin(a)*rad*.8)*(1-q);g.globalAlpha=(.25+.75*q)*(1-ca);g.fillStyle=i%6===0?'#FFD60A':'#111';g.beginPath();g.arc(x,y,(L.dot||3.6)*(.6+.6*q),0,7);g.fill()});
        if(ca>0){g.globalAlpha=ca;g.font='800 '+size+'px Pop';g.textAlign='center';g.textBaseline='middle';g.fillStyle=L.color||'#111';g.fillText(L.text,cx,cy)}g.globalAlpha=1};
      if(k==='shock')L.fx=(lt)=>{clr();const at=L.at||0,dur=L.dur||.9,R=L.r||900,F=L.from||[540,900];if(lt<at||lt>at+dur+.4)return;
        for(let j=0;j<(L.rings||2);j++){const u=c((lt-at-j*.14)/dur);if(u<=0||u>=1)continue;const rad=R*eo(u),w=70*(1-u)+8;g.globalAlpha=1-u;g.lineWidth=w+12;g.strokeStyle='#111';g.beginPath();g.arc(F[0],F[1],rad,0,7);g.stroke();g.lineWidth=w;g.strokeStyle='#FFD60A';g.stroke();
          for(let q=0;q<14;q++){const an=q/14*Math.PI*2+j;star(g,F[0]+Math.cos(an)*rad,F[1]+Math.sin(an)*rad,16*(1-u),an*3,'#fff','#111',2)}}
        const u0=c((lt-at)/.35);if(u0<1){g.globalAlpha=1;glow(g,F[0],F[1],380*u0+80,(1-u0)*.85)}g.globalAlpha=1};
      if(k==='aura')L.fx=(lt)=>{clr();const at=L.at||0,dur=L.dur||2,F=L.from||[540,900],env=c((lt-at)/.35)*c((at+dur-lt)/.45);if(env<=0)return;const R=L.r||340;g.globalAlpha=env;glow(g,F[0],F[1],R*(1+.06*Math.sin(lt*6)),.9);
        const R2=L.rayLen||820,nr=L.rays||14;for(let i=0;i<nr;i++){const a0=lt*.5+i*Math.PI*2/nr,w=.075,gr=g.createRadialGradient(F[0],F[1],40,F[0],F[1],R2);gr.addColorStop(0,'rgba(255,214,10,.55)');gr.addColorStop(1,'rgba(255,214,10,0)');g.fillStyle=gr;g.beginPath();g.moveTo(F[0],F[1]);g.lineTo(F[0]+Math.cos(a0-w)*R2,F[1]+Math.sin(a0-w)*R2);g.lineTo(F[0]+Math.cos(a0+w)*R2,F[1]+Math.sin(a0+w)*R2);g.closePath();g.fill()}
        const ph=(lt*1.1)%1;g.globalAlpha=env*(1-ph);g.lineWidth=10;g.strokeStyle='#FFD60A';g.beginPath();g.arc(F[0],F[1],R*(.8+.8*ph),0,7);g.stroke();g.globalAlpha=1};
      if(k==='poof')L.fx=(lt)=>{clr();const at=L.at||0,dur=L.dur||.7,F=L.from||[540,900],sz=L.size||240,u=c((lt-at)/dur);if(u<=0||u>=1)return;
        for(let i=0;i<10;i++){const an=i/10*Math.PI*2+rn(i,1),d=eo(u)*sz*(.55+.5*rn(i,2)),r=sz*(.3+.32*eo(u))*(.65+.35*rn(i,3)),x=F[0]+Math.cos(an)*d,y=F[1]+Math.sin(an)*d*.8-eo(u)*sz*.25;
          g.globalAlpha=1-u*u;g.fillStyle='#fff';g.strokeStyle='#111';g.lineWidth=Math.max(2,6*(1-u));g.beginPath();g.arc(x,y,r,0,7);g.fill();g.stroke()}
        g.fillStyle='#fff';g.globalAlpha=1-u;g.beginPath();g.arc(F[0],F[1]-eo(u)*sz*.1,sz*.45*(1+u*.3),0,7);g.fill();g.globalAlpha=1}}
    else if(k==='glinttext'){el=mk(root,`left:0;top:0;width:${L.w||900}px;text-align:${L.align||'center'};font-size:${L.size||150}px;font-weight:800;line-height:1.1;white-space:nowrap;${L.css||''}`,'<span class="gl">'+L.html+'</span>','abs');L.glEl=el.firstChild;
      L.fx=(lt)=>{const q=c((lt-L.glint[0])/(L.glint[1]||.7));L.glEl.style.setProperty('--g',(q<=0||q>=1?-40:-20+q*140)+'%')}}
    else if(k==='morph'){const sz=L.size||260;el=mk(root,`left:0;top:0;width:${sz}px;height:${sz}px`,'','abs');
      L.ms=(L.icons||[]).map(n=>{const d=mk(el,'left:0;top:0;width:100%;height:100%;opacity:0',icSvg(n,sz,L.sw,L.fc),'abs');return d});
      L.fx=(lt)=>{const ts=L.ts||[],md=L.md||.5;let cur=0;ts.forEach((t,j)=>{if(lt>=t)cur=j+1});L.ms.forEach(d=>d.style.opacity=0);
        if(cur===0){L.ms[0].style.opacity=1;L.ms[0].style.transform='none';el.style.filter='none';return}
        const j=cur-1,p=c((lt-ts[j])/md),A=L.ms[j],B=L.ms[j+1];
        if(p>=1){B.style.opacity=1;B.style.transform='none';el.style.filter='none';return}
        A.style.opacity=1-p*1.15;A.style.transform=`scale(${1-.28*p})`;B.style.opacity=Math.min(1,p*1.4);B.style.transform=`scale(${.72+.28*p})`;el.style.filter='url(#goo)'}}
    else if(k==='card3d'){const w=L.w||600,h=L.h||360;el=mk(root,`left:0;top:0;width:${w}px;height:${h}px;perspective:1400px`,'','abs');
      const inn=mk(el,`left:0;top:0;width:${w}px;height:${h}px;transform-style:preserve-3d`,'','abs');
      mk(inn,`left:0;top:0;width:${w}px;height:${h}px;backface-visibility:hidden;${L.fcss||''}`,icHtml(L.front||''),'abs');
      mk(inn,`left:0;top:0;width:${w}px;height:${h}px;backface-visibility:hidden;transform:rotateY(180deg);${L.bcss||L.fcss||''}`,icHtml(L.back||''),'abs');L.inner=inn}
    else if(k==='magnet'){L.x=0;L.y=0;el=mk(root,'left:0;top:0;width:1080px;height:1920px','','abs');const sz=L.size||110;
      L.mi=(L.items||[]).map((it,i)=>{const grp=[];for(let j=0;j<7;j++)grp.push(mk(el,`left:0;top:0;width:${sz}px;height:${sz}px;opacity:0`,icSvg(it.name,sz,L.sw,L.fc),'abs'));return {it,grp,i}});
      L.fx=(lt)=>{const T=L.to;L.mi.forEach(({it,grp,i})=>{const t0=(L.at||0)+i*(L.stag||.18),dur=L.dur||.8,S=it.from,mx=(S[0]+T[0])/2,my=(S[1]+T[1])/2,dx=T[0]-S[0],dy=T[1]-S[1],ln=Math.hypot(dx,dy)||1,ar=(L.arc||260)*(i%2?1:-1),cx=mx-dy/ln*ar,cy=my+dx/ln*ar;
          grp.forEach((d,j)=>{const tt=lt-t0-j*.035,u=c(tt/dur),v=u*u,x=(1-v)*(1-v)*S[0]+2*(1-v)*v*cx+v*v*T[0],y=(1-v)*(1-v)*S[1]+2*(1-v)*v*cy+v*v*T[1];
            const on=tt>=0&&(j===0?u<1:u<1),sc2=j===0?(1-.55*c((u-.78)/.22)):(.8-.08*j);d.style.opacity=on?(j===0?1:.5*(1-j/7)):0;d.style.transform=`translate(${x-sz/2}px,${y-sz/2}px) scale(${sc2})`})})}}
    else if(k==='text'){el=mk(root,""")

# ---- applyLayer additions
rep("  if(L.orbit){const hs","  if(L.z){x+=Math.sin(lt*.9)*30*L.z;y+=Math.cos(lt*.7)*16*L.z}\n  if(L.orbit){const hs")
rep("  if(L.fx)L.fx(lt,o);\n","  if(L.fx)L.fx(lt,o);\n  if(L.inner){const ry=kfv(k,lt,'ry',0)+(L.tilt?Math.sin(lt*1.7)*L.tilt:0),rx=kfv(k,lt,'rx',0)+(L.tilt?Math.cos(lt*1.3)*L.tilt*.5:0);L.inner.style.transform=`rotateX(${rx}deg) rotateY(${ry}deg)`}\n")

# ---- portal transition
rep("const TR=['fade','push','iris','zoom'];","const TR=['fade','push','iris','zoom','portal'];")
rep("scenes.forEach(s2=>{s2.root.style.transform='';s2.root.style.clipPath='none'});","scenes.forEach(s2=>{s2.root.style.transform='';s2.root.style.clipPath='none'});E('portal').style.display='none';")
rep("if(cur>0&&['push','iris','zoom'].includes(sc.wipe)&&lt<(sc.trd||.5)){","if(cur>0&&['push','iris','zoom','portal'].includes(sc.wipe)&&lt<(sc.trd||.5)){")
rep("else if(sc.wipe==='iris'){sc.root.style.clipPath=`circle(${q*1300}px at 50% 52%)`}","else if(sc.wipe==='iris'){sc.root.style.clipPath=`circle(${q*1300}px at 50% 52%)`}\n    else if(sc.wipe==='portal'){const R=q*1350,P2=E('portal');sc.root.style.clipPath=`circle(${Math.max(0,R-36)}px at 50% 50%)`;P2.style.display='block';P2.style.width=P2.style.height=(2*R)+'px';P2.style.left=(540-R)+'px';P2.style.top=(960-R)+'px';P2.style.opacity=1-c((q-.78)/.22)}")
open(p,'w',encoding='utf-8').write(s)
print('ok')
