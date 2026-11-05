import json,subprocess,time,urllib.parse,sys
UA="devrobolab-research/1.0 (video asset search)"
OUT="/home/user/story-channel/channels/devrobolab/stories/033_photos/raw/"
def api(params):
    out=subprocess.run(["curl","-s","--max-time","30","-A",UA,"https://commons.wikimedia.org/w/api.php?"+params+"&format=json"],capture_output=True,text=True).stdout
    try:return json.loads(out)
    except Exception:return None
log={}
for key,term in [("receipt","paper receipt"),("plant","plant leaf green"),("cat","cat portrait"),("note","handwritten note paper"),("sign","street sign"),("book","open book")]:
    time.sleep(25)
    d=api("action=query&generator=search&gsrsearch="+urllib.parse.quote(term+" filetype:bitmap")+"&gsrnamespace=6&gsrlimit=20&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1400")
    c=[]
    for p in (d or {}).get("query",{}).get("pages",{}).values():
        ii=p["imageinfo"][0];lic=ii["extmetadata"].get("LicenseShortName",{}).get("value","")
        if (lic in("CC0","Public domain","CC0 1.0") or lic.lower().startswith("pd")) and ii["width"]>=1200:
            c.append((p["title"],lic,ii["thumburl"],ii["descriptionurl"],ii["width"],ii["height"]))
    log[key]=c;print(key,len(c),flush=True)
    for i,x in enumerate(c[:2]):
        time.sleep(4)
        f=f"{OUT}{key}_{i}.jpg";subprocess.run(["curl","-s","--max-time","60","-A",UA,"-o",f,x[2]])
json.dump(log,open(OUT+"photos.json","w"),indent=1);print("done")
