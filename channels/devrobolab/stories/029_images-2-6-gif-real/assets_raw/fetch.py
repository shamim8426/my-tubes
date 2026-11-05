import json,subprocess,time,urllib.parse
UA="devrobolab-research/1.0 (video asset search)"
def api(params):
    url="https://commons.wikimedia.org/w/api.php?"+params+"&format=json"
    out=subprocess.run(["curl","-s","--max-time","30","-A",UA,url],capture_output=True,text=True).stdout
    try:return json.loads(out)
    except Exception:return None
time.sleep(70)
res={}
d=api("action=query&titles="+urllib.parse.quote("File:Houston sneakers (Unsplash).jpg")+"&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1400")
for p in (d or {}).get("query",{}).get("pages",{}).values():
    ii=p["imageinfo"][0];res["houston"]=[(p["title"],ii["extmetadata"]["LicenseShortName"]["value"],ii["thumburl"],ii["descriptionurl"])]
for k,t in [("flip","flip book"),("film","film strip")]:
    time.sleep(25)
    d=api("action=query&generator=search&gsrsearch="+urllib.parse.quote(t)+"&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1000")
    r=[]
    for p in (d or {}).get("query",{}).get("pages",{}).values():
        ii=p["imageinfo"][0];r.append((p["title"],ii["extmetadata"].get("LicenseShortName",{}).get("value"),ii["thumburl"],ii["descriptionurl"]))
    res[k]=r
json.dump(res,open("cands3.json","w"),indent=1)
print("done",{k:len(v) for k,v in res.items()})
