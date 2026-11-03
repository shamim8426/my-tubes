p='channels/yellow-bot/templates/deck_template.html'
s=open(p,encoding='utf-8').read()
a="B.list=(sc,root)=>{\n  tag(root,sc);\n"
assert a in s
s=s.replace(a,a+"  if(sc.head){const h=mk(root,`left:80px;top:${sc.hy||220}px;width:920px;font-size:${sc.hsize||84}px`,parse(sc.head),'abs line');streamRow(sc,h,.35,'marker',.15)}\n")
open(p,'w',encoding='utf-8').write(s)
g='channels/yellow-bot/stories/019_overview/gen_deck.py'
t=open(g,encoding='utf-8').read()
assert 'icons=True, y0=300, rh=330,' in t
t=t.replace('icons=True, y0=300, rh=330,','icons=True, head="Tumhe **fayda**? Wo boring kaam", hy=230, y0=500, rh=320,')
open(g,'w',encoding='utf-8').write(t)
print('ok')
