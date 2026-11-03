p='channels/yellow-bot/templates/deck_template.html'
s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,b)
rep(".ic .f{fill:var(--fc,#FFD60A)}", """.ic .f{fill:var(--fc,#FFD60A)}
.bubble{background:#fff;border:6px solid #111;border-radius:44px;box-shadow:0 16px 30px rgba(0,0,0,.14)}
.bubble::after{content:"";position:absolute;left:70px;bottom:-26px;width:38px;height:38px;background:#fff;border-right:6px solid #111;border-bottom:6px solid #111;transform:rotate(45deg)}
.bubble.y{background:#FFD60A}.bubble.y::after{background:#FFD60A}""")
# transitions + camera in setT
rep("const nf=scenes[cur+1]&&scenes[cur+1].wipe==='fade';", "const TR=['fade','push','iris','zoom'];const nf=scenes[cur+1]&&TR.includes(scenes[cur+1].wipe);")
rep("  if(cur>0&&sc.wipe==='fade'&&lt<.25){const q=eio(lt/.25),pv=scenes[cur-1],pl=pv.end-pv.start-.001;pv.root.style.display='block';pv.anims.forEach(it=>applyItem(it,pl));if(pv.upd)pv.upd(pl);pv.root.style.opacity=1-q;sc.root.style.opacity=q}",
"""  if(cur>0&&sc.wipe==='fade'&&lt<.25){const q=eio(lt/.25),pv=scenes[cur-1],pl=pv.end-pv.start-.001;pv.root.style.display='block';pv.anims.forEach(it=>applyItem(it,pl));if(pv.upd)pv.upd(pl);pv.root.style.opacity=1-q;sc.root.style.opacity=q}
  scenes.forEach(s2=>{s2.root.style.transform='';s2.root.style.clipPath='none'});
  const camOf=(s2,l2)=>{if(!s2.cam)return '';const kk=s2.cam,cx=kfv(kk,l2,'x',0),cy=kfv(kk,l2,'y',0),cs=kfv(kk,l2,'s',1);return `translate(${cx}px,${cy}px) scale(${cs})`};
  if(sc.cam)sc.root.style.transform=camOf(sc,lt);
  if(cur>0&&['push','iris','zoom'].includes(sc.wipe)&&lt<(sc.trd||.5)){const D2=sc.trd||.5,q=eio(lt/D2),pv=scenes[cur-1],pl=pv.end-pv.start-.001;pv.root.style.display='block';pv.anims.forEach(it=>applyItem(it,pl));if(pv.upd)pv.upd(pl);pv.root.style.opacity=1;sc.root.style.opacity=1;
    const cc=camOf(sc,lt);
    if(sc.wipe==='push'){pv.root.style.transform=`translateX(${-q*W}px)`;sc.root.style.transform=`translateX(${(1-q)*W}px) ${cc}`}
    else if(sc.wipe==='iris'){sc.root.style.clipPath=`circle(${q*1300}px at 50% 52%)`}
    else{pv.root.style.transform=`scale(${1+q*.7})`;pv.root.style.opacity=1-q;sc.root.style.transform=`scale(${.75+.25*q}) ${cc}`;sc.root.style.opacity=q}}""")
rep("if(cur>0&&lt<wd&&sc.wipe!=='fade'){","if(cur>0&&lt<wd&&!TR.includes(sc.wipe)){")
open(p,'w',encoding='utf-8').write(s)
print('ok')
