import json,subprocess,time,urllib.parse
UA="devrobolab-research/1.0 (video asset search)"
OUT=str(__import__("pathlib").Path(__file__).resolve().parent / "raw") + "/"
def api(params):
    out=subprocess.run(["curl","-s","--max-time","30","-A",UA,"https://commons.wikimedia.org/w/api.php?"+params+"&format=json"],capture_output=True,text=True).stdout
    try:return json.loads(out)
    except Exception:return None
log={}
for key,term in [("desk","office desk"),("folder","filing cabinet folders"),("library","library bookshelf"),("notebook","notebook pen desk")]:
    time.sleep(30)
    d=api("action=query&generator=search&gsrsearch="+urllib.parse.quote(term+" filetype:bitmap")+"&gsrnamespace=6&gsrlimit=30&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1600")
    c=[]
    for p in (d or {}).get("query",{}).get("pages",{}).values():
        ii=p["imageinfo"][0];lic=ii["extmetadata"].get("LicenseShortName",{}).get("value","")
        if (lic in("CC0","Public domain","CC0 1.0") or lic.lower().startswith("pd")) and ii["width"]>=1400:
            c.append((p["title"],lic,ii["thumburl"],ii["descriptionurl"],ii["width"],ii["height"]))
    log[key]=c;print(key,len(c),flush=True)
    for i,x in enumerate(c[:3]):
        time.sleep(5);subprocess.run(["curl","-s","--max-time","60","-A",UA,"-o",f"{OUT}{key}_{i}.jpg",x[2]])
json.dump(log,open(OUT+"photos.json","w"),indent=1);print("done")
