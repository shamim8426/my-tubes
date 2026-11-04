p='channels/devrobolab/templates/deck_template.html'
s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:70],s.count(a))
    s=s.replace(a,b)
# hide scene tag chip during portal
rep("s2.root.style.background=''});","s2.root.style.background='';const tg0=s2.root.querySelector('.tag');if(tg0)tg0.style.visibility=''});")
rep("else if(sc.wipe==='portal'){sc.root.style.background='#fff';","else if(sc.wipe==='portal'){[sc,pv].forEach(z=>{const tg=z.root.querySelector('.tag');if(tg)tg.style.visibility='hidden'});sc.root.style.background='#fff';")
# assemble waits for the Poppins font
rep("if(k==='assemble')L.fx=(lt)=>{clr();","if(k==='assemble')L.fx=(lt)=>{clr();if(document.fonts&&document.fonts.check&&!document.fonts.check('800 40px Pop'))return;")
rep("const scenes=D.scenes;","const scenes=D.scenes;if(document.fonts&&document.fonts.load)document.fonts.load('800 40px Pop');")
open(p,'w',encoding='utf-8').write(s)
print('ok')
