import json, urllib.request, re, os, base64, io
from PIL import Image, ImageDraw, ImageFont
URL="https://cdn.prod.website-files.com/6aa5926f78a0f4db2f6d1d20/6ad8879bf0d24d5cff716db8_zarion%20ai%20hero.json"
with urllib.request.urlopen(URL,timeout=40) as f: obj=json.load(f)
stats={"texts":0,"colors":0,"assets":0}
def alter_color(c):
    if not isinstance(c,list) or len(c)<3 or any(not isinstance(x,(int,float)) for x in c[:3]): return
    if not all(0<=x<=1 for x in c[:3]):return
    r,g,b=c[:3]
    # blue / cyan / cool gray accents; preserve white/black/greens/orange.
    delta=max(b-r,b-g)
    if delta<=.035 or b<.19:return
    strength=min(1,max(0,(delta-.035)/.12))
    lum=(r+g+b)/3
    target=(min(1,.63+lum*.27),min(1,.24+lum*.31),min(1,.13+lum*.29))
    for i in range(3):c[i]=round(c[i]*(1-strength)+target[i]*strength,6)
    stats["colors"]+=1
def visit(v):
    if isinstance(v,list):
        for x in v:visit(x)
    elif isinstance(v,dict):
        # Color keyframes for fills and strokes.
        if v.get("ty") in ("fl","st") and isinstance(v.get("c"),dict):
            key=v["c"].get("k")
            if isinstance(key,list):
                if len(key) in (3,4) and isinstance(key[0],(int,float)):alter_color(key)
                else:
                    for frame in key:
                        if isinstance(frame,dict):
                            for k in ("s","e"):
                                val=frame.get(k)
                                if isinstance(val,list):
                                    if val and isinstance(val[0],list):val=val[0]
                                    alter_color(val)
        if "t" in v and isinstance(v["t"],dict) and isinstance(v["t"].get("d"),dict):
            for frame in v["t"]["d"].get("k",[]):
                st=frame.get("s",{})
                if isinstance(st,dict) and isinstance(st.get("t"),str):
                    old=st["t"];new=re.sub("zarion","latera",old,flags=re.I)
                    if new!=old:stats["texts"]+=1
                    st["t"]=new
                    if isinstance(st.get("fc"),list):alter_color(st["fc"])
        for vv in v.values():visit(vv)
visit(obj)
# The source uses embedded raster assets too. Recolor saturated blue in the
# PNG layer pixels; this also updates blue labels that are not vector shapes.
for asset in obj.get("assets",[]):
    p=asset.get("p","")
    if not (isinstance(p,str) and p.startswith("data:image/")):continue
    try:
        prefix,payload=p.split(",",1)
        im=Image.open(io.BytesIO(base64.b64decode(payload))).convert("RGBA")
        pixels=im.load();w,h=im.size
        for yy in range(h):
            for xx in range(w):
                r,g,b,a=pixels[xx,yy]
                if a==0:continue
                d=max(b-r,b-g)
                if d>12 and b>70:
                    amount=min(1,(d-12)/52)
                    lum=(r+g+b)/3
                    tr=min(255,int(153+lum*.27));tg=min(255,int(50+lum*.30));tb=min(255,int(25+lum*.28))
                    pixels[xx,yy]=(int(r+(tr-r)*amount),int(g+(tg-g)*amount),int(b+(tb-b)*amount),a)
        out=io.BytesIO();im.save(out,format="PNG",optimize=True)
        asset["p"]="data:image/png;base64,"+base64.b64encode(out.getvalue()).decode()
        stats["assets"]+=1
    except Exception as exc:print("asset skipped",asset.get("id"),exc)
os.makedirs("projetos/zarion/assets",exist_ok=True)
path="projetos/zarion/assets/latera-hero.json"
with open(path,"w",encoding="utf-8") as f:json.dump(obj,f,ensure_ascii=False,separators=(",",":"))
print("GENERATED",path,os.path.getsize(path),stats)
