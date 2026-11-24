from PIL import Image, ImageDraw, ImageFont
import subprocess, sys, os, io
HERE=os.path.dirname(os.path.abspath(__file__)); B=os.path.join(HERE,"brand")
SANS="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def raster(fn,w=None,h=None):
    args=["rsvg-convert"]+(["-w",str(w)] if w else [])+(["-h",str(h)] if h else [])+[os.path.join(B,fn)]
    return Image.open(io.BytesIO(subprocess.check_output(args))).convert("RGBA")
W,H=1200,630
im=Image.new("RGBA",(W,H),"#F6F4EF"); d=ImageDraw.Draw(im)
stone="#6B665E"; whisky="#8C5A2B"; line="#DBD6CC"; ink="#1A1917"
d.rectangle([40,40,W-40,H-40],outline=line,width=2)
mark=raster("logo-mark-amber.svg",h=400); im.alpha_composite(mark,(110,(H-mark.height)//2))
d.line([(500,140),(500,490)],fill=line,width=2)
en=raster("logo-en.svg",w=520); im.alpha_composite(en,(560,150))
zh=raster("logo-zh.svg",w=440); im.alpha_composite(zh,(562,150+en.height+34))
f=lambda s:ImageFont.truetype(SANS,s,index=3)
y=150+en.height+34+zh.height+40
d.line([(562,y),(642,y)],fill=whisky,width=3)
d.text((562,y+22),"高雄苓雅區・威士忌酒吧",font=f(30),fill=ink)
d.text((562,y+68),"22.6°N · Formerly Highlander Inn Takao",font=f(22),fill=stone)
for out in sys.argv[1:]: im.convert("RGB").save(os.path.join(out,"assets","og.png"),optimize=True)
