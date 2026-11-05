import json,subprocess,time,urllib.parse
UA="devrobolab-research/1.0 (video asset search)"
def api(params):
    out=subprocess.run(["curl","-s","--max-time","30","-A",UA,"https://commons.wikimedia.org/w/api.php?"+params+"&format=json"],capture_output=True,text=True).stdout
    try:return json.loads(out)
    except Exception:return None
log={}
for key,term in [("scissors","scissors photo"),("magnifier","magnifying glass photo"),("pencil","pencil photo")]:
    time.sleep(30)
    d=api("action=query&generator=search&gsrsearch="+urllib.parse.quote(term+" filetype:bitmap")+"&gsrnamespace=6&gsrlimit=15&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1400")
    cands=[]
    for p in (d or {}).get("query",{}).get("pages",{}).values():
        ii=p["imageinfo"][0];lic=ii["extmetadata"].get("LicenseShortName",{}).get("value","")
        if lic in("CC0","Public domain","CC0 1.0") or lic.lower().startswith("pd"):
            cands.append((p["title"],lic,ii["thumburl"],ii["descriptionurl"],ii["width"],ii["height"]))
    log[key]=cands
    for i,c in enumerate(cands[:3]):
        subprocess.run(["curl","-s","--max-time","60","-A",UA,"-o",f"{key}_{i}.jpg",c[2]])
json.dump(log,open("photos.json","w"),indent=1)
print("done",{k:len(v) for k,v in log.items()})
