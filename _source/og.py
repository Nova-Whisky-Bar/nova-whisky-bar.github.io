from PIL import Image, ImageDraw, ImageFont
import sys
SERIF="/usr/share/fonts/opentype/noto/NotoSerifCJK-SemiBold.ttc"; SANS="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
W,H=1200,630
im=Image.new("RGB",(W,H),"#F6F4EF"); d=ImageDraw.Draw(im)
ink="#1A1917"; stone="#6B665E"; whisky="#8C5A2B"; line="#DBD6CC"
def f(p,s): return ImageFont.truetype(p,s,index=3)
d.rectangle([40,40,W-40,H-40],outline=line,width=2)
d.line([(80,110),(W-80,110)],fill=line,width=1)
d.text((80,74),"22.6°N  ·  KAOHSIUNG",font=f(SANS,22),fill=stone)
d.text((W-80,74),"Formerly Highlander Inn Takao",font=f(SANS,22),fill=stone,anchor="ra")
d.text((76,160),"Nova Whisky Bar",font=f(SERIF,100),fill=ink)
d.text((80,300),"新星威士忌酒館",font=f(SERIF,60),fill=ink)
d.line([(80,405),(160,405)],fill=whisky,width=3)
d.text((80,430),"高雄苓雅區・威士忌酒吧",font=f(SANS,34),fill=ink)
d.text((80,486),"單一麥芽・獨立裝瓶・安靜的夜晚",font=f(SANS,28),fill=stone)
cx,cy,R=1040,470,62
d.polygon([(cx,cy-R),(cx+R*.18,cy-R*.18),(cx+R,cy),(cx+R*.18,cy+R*.18),(cx,cy+R),(cx-R*.18,cy+R*.18),(cx-R,cy),(cx-R*.18,cy-R*.18)],fill=whisky)
for out in sys.argv[1:]: im.save(out+"/assets/og.png",optimize=True)
