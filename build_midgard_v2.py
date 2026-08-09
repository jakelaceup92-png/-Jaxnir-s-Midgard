from PIL import Image, ImageDraw, ImageFilter
import math, random, numpy as np

W,H,S=1920,150,2
N=56
w,h=W*S,H*S
rng=random.Random(8462)
ROCK=(10,22,34,255); ROCK2=(17,36,51,255); SNOW=(162,200,225,255); SNOWHI=(205,230,242,255)
PINE=(5,19,28,255); PINE2=(10,32,45,255); WOOD=(77,48,32,255); WOOD2=(112,70,42,255)
DARK=(35,23,20,255); GOLD=(255,222,144,255); AMBER=(255,186,88,255); WATER=(4,24,40,255); WATER2=(8,50,76,255)

def sc(v): return int(round(v*S))
def poly(d,pts,fill): d.polygon([(sc(x),sc(y)) for x,y in pts],fill=fill)
def line(d,pts,fill,width=1): d.line([(sc(x),sc(y)) for x,y in pts],fill=fill,width=max(1,sc(width)),joint='curve')

def glow(base,x,y,rx,ry,color,alpha=80):
    gw,gh=sc(rx*2+6),sc(ry*2+6)
    arr=np.zeros((gh,gw,4),dtype=np.uint8); yy,xx=np.ogrid[:gh,:gw]
    cx,cy=gw/2,gh/2; q=((xx-cx)/(gw/2))**2+((yy-cy)/(gh/2))**2
    a=(np.clip(1-q,0,1)**1.8*alpha).astype(np.uint8)
    arr[...,0]=color[0];arr[...,1]=color[1];arr[...,2]=color[2];arr[...,3]=a
    base.alpha_composite(Image.fromarray(arr,'RGBA'),(sc(x-rx-3),sc(y-ry-3)))

def ground(base):
    d=ImageDraw.Draw(base)
    # Low layered mountain silhouettes only; everything above them stays transparent.
    poly(d,[(0,111),(95,92),(185,103),(290,84),(390,101),(510,78),(630,100),(755,76),(890,101),(1020,82),(1150,102),(1275,88),(1395,107),(1525,93),(1650,108),(1770,91),(1920,104),(1920,150),(0,150)],(12,30,47,225))
    for p in [[(250,91),(290,84),(326,94),(307,90),(292,93),(278,89)],[(470,86),(510,78),(546,88),(527,84),(511,87),(495,83)],[(716,84),(755,76),(792,86),(772,82),(756,85),(740,81)],[(989,89),(1020,82),(1052,90),(1037,87),(1020,90),(1005,86)],[(1735,99),(1770,91),(1803,101),(1786,97),(1770,100),(1754,96)]]: poly(d,p,(67,113,151,185))
    poly(d,[(0,94),(110,66),(215,87),(320,56),(430,88),(560,58),(690,93),(830,58),(950,91),(1080,55),(1210,90),(1350,60),(1460,85),(1600,58),(1740,90),(1860,61),(1920,76),(1920,150),(0,150)],(8,23,38,248))
    # Foreground snow shelf.
    top=[]
    for x in range(0,W+1,32): top.append((x,120+4*math.sin(x*.011)+2*math.sin(x*.027+.7)))
    poly(d,top+[(W,150),(0,150)],ROCK)
    lower=[(x,y+8+2*math.sin(x*.018)) for x,y in reversed(top)]
    poly(d,top+lower,(112,162,195,255)); line(d,top,(192,222,238,225),1.2)
    # Dark fjord on right.
    poly(d,[(1220,121),(1360,116),(1510,118),(1660,114),(1920,116),(1920,150),(1260,150)],WATER)
    for y in range(124,150,5): line(d,[(1255,y),(1910,y-1)],(18,74+(y-124),104+(y-124),125),.65)
    # Ground texture.
    for _ in range(220):
        x=rng.randrange(0,W); y=rng.randrange(126,H); r=rng.choice([1,1,2,2,3])
        d.ellipse((sc(x),sc(y),sc(x+r),sc(y+r*.6)),fill=(172,203,218,rng.randrange(15,55)))

def pine(base,x,y,s=1,deep=False):
    d=ImageDraw.Draw(base); col=PINE2 if deep else PINE
    d.rectangle((sc(x-1.2*s),sc(y-7*s),sc(x+1.2*s),sc(y+2)),fill=(42,30,22,255))
    for yy,ww0 in [(y-55*s,15*s),(y-43*s,21*s),(y-30*s,27*s),(y-17*s,33*s)]: poly(d,[(x,yy),(x-ww0,y-2),(x+ww0,y-2)],col)
    if not deep:
        for yy,ww0 in [(y-36*s,14*s),(y-22*s,20*s),(y-10*s,25*s)]: line(d,[(x-ww0*.7,yy),(x,yy-2*s),(x+ww0*.64,yy)],(58,105,137,130),.75)

def lit_window(base,x,y,ww=9,hh=7):
    glow(base,x,y,18,12,(255,141,49),58); d=ImageDraw.Draw(base)
    d.rectangle((sc(x-ww/2),sc(y-hh/2),sc(x+ww/2),sc(y+hh/2)),fill=(226,127,44,255))
    d.rectangle((sc(x-ww/2+2),sc(y-hh/2+1.5),sc(x+ww/2-2),sc(y+hh/2-1.5)),fill=GOLD)
    line(d,[(x,y-hh/2),(x,y+hh/2)],(84,47,28,255),.7); line(d,[(x-ww/2,y),(x+ww/2,y)],(84,47,28,255),.7)

def house(base,x,g,width,height,roof,windows=2):
    d=ImageDraw.Draw(base); y=g-height
    d.ellipse((sc(x-8),sc(g-3),sc(x+width+8),sc(g+5)),fill=(0,0,0,60))
    d.rectangle((sc(x),sc(g-5),sc(x+width),sc(g)),fill=(28,29,29,255))
    for k in range(0,int(width),14): d.rectangle((sc(x+k),sc(g-5),sc(x+k+10),sc(g-2)),fill=(48,50,49,255))
    d.rectangle((sc(x),sc(y),sc(x+width),sc(g-5)),fill=DARK); d.rectangle((sc(x+4),sc(y+3),sc(x+width-4),sc(g-5)),fill=WOOD)
    for xx in np.linspace(x+9,x+width-9,max(4,int(width/24))):
        d.rectangle((sc(xx-1),sc(y+2),sc(xx+1),sc(g-5)),fill=(127,81,47,210)); line(d,[(xx+2,y+4),(xx+4,g-8)],(42,29,23,120),.55)
    poly(d,[(x-9,y+4),(x+width/2,y-roof),(x+width+9,y+4)],(9,17,23,255))
    poly(d,[(x-7,y+1),(x+width/2,y-roof+3),(x+width+7,y+1),(x+width-3,y+1),(x+width*.72,y-roof*.34),(x+width*.51,y-roof*.12),(x+width*.29,y-roof*.34),(x+3,y+1)],(116,164,194,245))
    line(d,[(x-8,y+2),(x+width/2,y-roof+1),(x+width+8,y+2)],(205,230,242,225),1.3)
    for f in np.linspace(.16,.84,7):
        xx=x+width*f; line(d,[(xx,y-roof*(1-abs(f-.5)*2)*.60),(xx+7,y+1)],(40,63,76,120),.55)
    dw=max(11,width*.12); d.rectangle((sc(x+width*.5-dw/2),sc(g-height*.53),sc(x+width*.5+dw/2),sc(g-5)),fill=(30,21,18,255)); d.rectangle((sc(x+width*.5-dw/2+3),sc(g-height*.48),sc(x+width*.5+dw/2-3),sc(g-5)),fill=(92,55,33,255))
    for i in range(windows): lit_window(base,x+width*(i+1)/(windows+1),y+height*.47,10 if width>100 else 9,7)
    cx=x+width*.78; d.rectangle((sc(cx),sc(y-roof*.66),sc(cx+6),sc(y+2)),fill=(42,29,25,255)); d.rectangle((sc(cx-1),sc(y-roof*.68),sc(cx+7),sc(y-roof*.64)),fill=(16,18,20,255))
    return cx+3,y-roof*.68

def static_scene():
    im=Image.new('RGBA',(w,h),(0,0,0,0)); ground(im)
    for x in list(range(15,390,37))+list(range(1030,1220,42))+list(range(1710,1920,36)): pine(im,x,124+rng.randint(-1,3),rng.uniform(.55,.8),True)
    for x in [25,72,126,184,244,310,1010,1070,1730,1785,1845,1903]: pine(im,x,134,rng.uniform(.72,1.1),False)
    chim=[]
    for a in [(120,131,92,34,19,2),(230,132,70,29,16,1),(320,130,108,39,23,2),(450,132,77,30,17,1),(548,130,154,44,28,3),(742,131,87,33,20,2),(850,132,74,29,17,1),(950,131,124,37,22,2),(1090,132,78,30,17,1),(600,129,185,49,33,4)]: chim.append(house(im,*a))
    d=ImageDraw.Draw(im)
    # Rune stone, fences and tiny props.
    poly(d,[(506,130),(516,92),(527,130)],(48,57,61,255)); line(d,[(516,101),(516,121)],(79,185,245,235),1.25); line(d,[(509,110),(523,110)],(79,185,245,215),1.15); glow(im,516,110,19,24,(61,153,235),45)
    for a,b in [(75,110),(790,830),(1040,1080)]:
        for xx in range(a,b,12): line(d,[(xx,125),(xx,136)],(81,54,37,255),1.3)
        line(d,[(a,129),(b,129)],(98,62,40,255),1.1)
    for x,y in [(292,131),(442,132),(820,132),(1068,132)]:
        d.ellipse((sc(x-4),sc(y-8),sc(x+4),sc(y+1)),fill=(79,48,30,255)); line(d,[(x-3,y-5),(x+3,y-5)],(139,95,55,255),.7)
    # Blacksmith forge.
    poly(d,[(1110,111),(1160,86),(1216,111)],(8,16,21,255)); line(d,[(1114,109),(1160,89),(1212,109)],(113,157,182,205),1.1); d.rectangle((sc(1114),sc(110),sc(1212),sc(133)),fill=(42,29,24,255))
    d.rectangle((sc(1124),sc(116),sc(1161),sc(132)),fill=(20,18,18,255)); glow(im,1143,124,28,19,(255,93,24),105); d.rectangle((sc(1129),sc(119),sc(1157),sc(130)),fill=(135,40,18,255)); d.rectangle((sc(1135),sc(122),sc(1152),sc(128)),fill=(250,105,27,255)); d.rectangle((sc(1140),sc(124),sc(1148),sc(128)),fill=(255,220,122,255))
    d.rectangle((sc(1181),sc(122),sc(1211),sc(127)),fill=(61,67,71,255)); poly(d,[(1185,122),(1177,118),(1208,118),(1214,122)],(73,80,84,255)); d.rectangle((sc(1191),sc(127),sc(1202),sc(135)),fill=(43,47,50,255))
    # Dock and lanterns.
    poly(d,[(1225,121),(1675,117),(1679,126),(1228,130)],(62,40,28,255)); line(d,[(1225,121),(1675,117)],(144,96,54,255),1.15)
    for xx in range(1240,1670,28): line(d,[(xx,121),(xx+1,129)],(37,27,22,255),.7)
    for xx in range(1242,1670,68): d.rectangle((sc(xx),sc(124),sc(xx+5),sc(154)),fill=(32,24,22,255))
    for xx in [1250,1440,1635]:
        line(d,[(xx,117),(xx,96)],(84,56,37,255),1.7); glow(im,xx,96,16,13,(255,163,62),48); d.rectangle((sc(xx-3),sc(92),sc(xx+3),sc(99)),fill=(37,31,27,255)); d.rectangle((sc(xx-1.5),sc(94),sc(xx+1.5),sc(97)),fill=(255,194,91,255))
    return im,chim

BASE,CHIM=static_scene()

def smoke(ph):
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(lay)
    for j,(cx,cy) in enumerate(CHIM[:9]):
        for k in range(3):
            p=(ph+j*.11+k*.28)%1; x=cx+math.sin((p+j)*6.28)*2+p*3; y=cy-p*31-k*2; r=2.8+p*5.5
            d.ellipse((sc(x-r),sc(y-r),sc(x+r),sc(y+r)),fill=(158,177,187,int(50*(1-p))))
    return lay.filter(ImageFilter.GaussianBlur(sc(1.15)))

def water(ph):
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(lay)
    for j,y in enumerate([126,132,139,147]):
        off=math.sin(ph*6.28+j*.9)*10
        for x in range(1270,1900,100): line(d,[(x+off,y),(x+off+34,y+.3*math.sin(ph*6.28+x))],(61,141,190,36 if j<2 else 25),.65)
    for x in [1250,1440,1635]:
        for k in range(4):
            yy=128+k*7; span=(7+k*3)*(.8+.2*math.sin(ph*6.28+k)); line(d,[(x-span,yy),(x+span,yy)],(255,158,61,max(12,45-k*8)),.75)
    return lay

def person(lay,x,y,s,dr,walk,col,carry=False):
    d=ImageDraw.Draw(lay); d.ellipse((sc(x-5*s),sc(y-1),sc(x+5*s),sc(y+2)),fill=(0,0,0,55))
    line(d,[(x-2*s,y-4*s),(x-2*s+walk*dr,y+1)],(27,28,30,255),1.5*s); line(d,[(x+2*s,y-4*s),(x+2*s-walk*dr,y+1)],(27,28,30,255),1.5*s)
    poly(d,[(x-5*s,y-16*s),(x+4*s,y-16*s),(x+6*s,y-4*s),(x-6*s,y-4*s)],col); d.rectangle((sc(x-5*s),sc(y-8*s),sc(x+5*s),sc(y-6*s)),fill=(48,34,27,255)); d.ellipse((sc(x-3.5*s),sc(y-23*s),sc(x+3.5*s),sc(y-16*s)),fill=(184,134,98,255)); d.pieslice((sc(x-4*s),sc(y-24*s),sc(x+4*s),sc(y-16*s)),180,360,fill=(47,35,29,255)); line(d,[(x+4*s,y-13*s),(x+7*s*dr,y-7*s)],(176,126,91,255),1.25*s)
    if carry: d.rectangle((sc(x+5*dr*s),sc(y-11*s),sc(x+11*dr*s),sc(y-5*s)),fill=(92,60,37,255))

def people(ph):
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); paths=[(150,520,133,1,(68,87,102,255),False),(430,760,134,-1,(91,64,53,255),True),(710,1010,133,1,(55,74,91,255),False),(965,1210,134,-1,(76,63,88,255),True),(1240,1410,127,1,(74,90,94,255),False)]
    for i,(a,b,y,dr,col,carry) in enumerate(paths):
        p=(ph+i*.19)%1; x=a+(b-a)*p if dr==1 else b-(b-a)*p; person(lay,x,y,.72 if i==4 else .8,dr,math.sin(p*6.28*8)*2.1,col,carry)
    return lay

def smith(ph):
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(lay); x=1193;y=133
    d.rectangle((sc(x-5),sc(y-17),sc(x+5),sc(y-4)),fill=(71,46,35,255)); d.ellipse((sc(x-4),sc(y-24),sc(x+4),sc(y-16)),fill=(171,116,83,255)); d.pieslice((sc(x-5),sc(y-25),sc(x+5),sc(y-17)),180,360,fill=(39,30,26,255))
    a=-1.15+(math.sin(ph*6.28*4)+1)*.75; hx=x+math.cos(a)*14; hy=y-11+math.sin(a)*14; line(d,[(x+3,y-12),(hx,hy)],(160,115,76,255),1.5); dx=-math.sin(a)*5;dy=math.cos(a)*5; line(d,[(hx-dx,hy-dy),(hx+dx,hy+dy)],(68,73,76,255),3)
    if math.sin(ph*6.28*4)>.78:
        for k in range(10):
            ang=.15+k*.34; rr=4+((ph*100+k*7)%1)*16; sx=1200+math.cos(ang)*rr;sy=123-math.sin(ang)*rr; d.ellipse((sc(sx-1),sc(sy-1),sc(sx+1),sc(sy+1)),fill=(255,min(235,170+k*5),70,220))
    return lay

def longship(ph):
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); x=1485;y=118+math.sin(ph*6.28)*2.2; ang=math.sin(ph*6.28+1)*.45
    ship=Image.new('RGBA',(sc(350),sc(120)),(0,0,0,0)); d=ImageDraw.Draw(ship)
    poly(d,[(12,68),(330,68),(304,91),(45,94)],(29,20,18,255)); poly(d,[(27,67),(316,69),(292,84),(51,86)],(120,73,43,255)); line(d,[(36,72),(305,73)],(189,124,68,190),1.2)
    for yy in [76,81]: line(d,[(50,yy),(292,yy+1)],(62,39,29,190),.75)
    poly(d,[(22,66),(7,47),(16,29),(27,42),(34,63)],(54,36,27,255)); d.ellipse((sc(12),sc(29),sc(21),sc(37)),fill=(64,44,31,255)); line(d,[(16,30),(10,19)],(88,58,36,255),1.1)
    cols=[(42,73,98,255),(96,56,43,255),(48,83,102,255),(107,67,40,255)]
    for i,xx in enumerate(range(55,292,28)):
        d.ellipse((sc(xx-8),sc(67),sc(xx+8),sc(83)),fill=cols[i%4],outline=(165,116,69,255),width=sc(1)); d.ellipse((sc(xx-2),sc(73),sc(xx+2),sc(77)),fill=(165,116,69,255))
    line(d,[(178,68),(178,6)],(115,80,49,255),2.4); line(d,[(128,22),(228,22)],(107,75,47,255),1.55)
    poly(d,[(135,24),(218,24),(210,60),(141,58)],(42,77,104,255))
    for xx in [147,164,181,198]: poly(d,[(xx,25),(xx+10,25),(xx+7,58),(xx-2,58)],(73,116,142,210))
    line(d,[(135,24),(210,60)],(177,199,202,115),.65); line(d,[(218,24),(141,58)],(177,199,202,90),.65); line(d,[(178,7),(60,80)],(149,119,79,180),.65); line(d,[(178,7),(300,78)],(149,119,79,180),.65)
    for xx in [70,105,248,282]: line(d,[(xx,82),(xx+(-17 if xx<178 else 17),101)],(126,84,50,255),1.25)
    ship=ship.rotate(ang,resample=Image.Resampling.BICUBIC,center=(sc(175),sc(72)),expand=False); lay.alpha_composite(ship,(sc(x-175),sc(y-72))); d=ImageDraw.Draw(lay)
    for k in range(5):
        yy=y+28+k*5;span=125-k*13; line(d,[(x-span,yy),(x+span,yy+math.sin(ph*6.28+k)*.7)],(63,125,158,36-k*5),.75)
    line(d,[(x-140,y+3),(1335,119)],(134,100,65,190),.75)
    return lay

def fire(ph):
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); x=803;y=137; glow(lay,x,y-8,28,20,(255,112,30),110);d=ImageDraw.Draw(lay); f=math.sin(ph*6.28*5)*4
    poly(d,[(x-7,y),(x-4,y-15-f*.4),(x,y-8),(x+3,y-22+f),(x+8,y)],(226,75,22,255)); poly(d,[(x-3,y),(x,y-11-f*.2),(x+4,y)],(255,211,105,255)); line(d,[(x-11,y+2),(x+11,y-1)],(83,48,29,255),2.8); line(d,[(x-10,y-1),(x+10,y+2)],(83,48,29,255),2.8)
    return lay

def snow(frame):
    lay=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(lay); rr=random.Random(1000)
    for i in range(66):
        bx=rr.uniform(0,W);by=rr.uniform(72,H);sp=rr.uniform(.6,1.4);x=(bx+frame*sp*2.2)%W;y=(by+frame*sp)%H;r=rr.choice([.5,.7,1]);d.ellipse((sc(x-r),sc(y-r),sc(x+r),sc(y+r)),fill=(225,241,249,120))
    return lay

def dragon(frame):
    lay=Image.new('RGBA',(w,h),(0,0,0,0));start,end=14,48
    if not start<=frame<=end:return lay
    p=(frame-start)/(end-start);x=-120+p*(W+250);y=40+5*math.sin(p*6.28);s=.55;d=ImageDraw.Draw(lay)
    line(d,[(x-42*s,y+3),(x-78*s,y+10),(x-108*s,y+3),(x-132*s,y-3)],(6,19,30,235),4*s);d.ellipse((sc(x-42*s),sc(y-12*s),sc(x+35*s),sc(y+14*s)),fill=(8,24,37,240));poly(d,[(x+24*s,y-7*s),(x+48*s,y-20*s),(x+70*s,y-17*s),(x+86*s,y-9*s),(x+68*s,y-4*s),(x+45*s,y-2*s),(x+28*s,y+5*s)],(7,21,32,245));poly(d,[(x+52*s,y-19*s),(x+57*s,y-29*s),(x+63*s,y-18*s)],(5,16,26,250));d.ellipse((sc(x+69*s),sc(y-13*s),sc(x+72*s),sc(y-10*s)),fill=(84,181,244,255))
    flap=math.sin(p*math.pi*10);wy=-33*s-flap*9*s;poly(d,[(x-18*s,y-5*s),(x-66*s,y+wy),(x-49*s,y-8*s),(x-86*s,y-18*s),(x-33*s,y+8*s)],(6,18,29,240));poly(d,[(x+1*s,y-7*s),(x+43*s,y+wy-4*s),(x+31*s,y-10*s),(x+65*s,y-20*s),(x+26*s,y+7*s)],(6,18,29,240));line(d,[(x-66*s,y+wy),(x-18*s,y-5*s),(x+43*s,y+wy-4*s)],(57,126,177,95),.7)
    return lay

def to_gif(im):
    alpha=im.getchannel('A'); bg=Image.new('RGB',im.size,(2,8,18)); bg.paste(im.convert('RGB'),mask=alpha)
    p=bg.quantize(colors=255,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.FLOYDSTEINBERG); arr=np.array(p); arr[np.array(alpha)<12]=255
    out=Image.fromarray(arr.astype(np.uint8),'P'); pal=p.getpalette()[:765]+[0,0,0];pal += [0]*(768-len(pal));out.putpalette(pal);out.info['transparency']=255;return out

frames=[]
for i in range(N):
    ph=i/N;fr=BASE.copy();fr=Image.alpha_composite(fr,water(ph));fr=Image.alpha_composite(fr,smoke(ph));fr=Image.alpha_composite(fr,people(ph));fr=Image.alpha_composite(fr,smith(ph));fr=Image.alpha_composite(fr,fire(ph));fr=Image.alpha_composite(fr,longship(ph));fr=Image.alpha_composite(fr,dragon(i));fr=Image.alpha_composite(fr,snow(i));frames.append(fr.resize((W,H),Image.Resampling.LANCZOS))
frames=[to_gif(f) for f in frames]
frames[0].save('midgard_bottom_v2.gif',save_all=True,append_images=frames[1:],duration=95,loop=0,transparency=255,disposal=2,optimize=False)
print('Rendered midgard_bottom_v2.gif',W,H,N)
