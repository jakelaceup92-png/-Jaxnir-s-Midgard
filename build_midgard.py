from PIL import Image, ImageDraw, ImageFilter
import math, random, numpy as np, os

W,H,S=1600,150,2
w,h=W*S,H*S
rng=random.Random(42)
C={
'sky0':(1,7,18),'sky1':(3,18,42),'sky2':(7,36,74),'electric':(53,142,255),'ice':(142,201,235),
'snow':(174,210,233),'snow2':(99,154,195),'mount_far':(16,35,63),'mount_mid':(10,26,47),'mount_near':(6,18,33),
'pine':(5,17,27),'pine2':(11,31,43),'wood':(73,49,35),'wood2':(103,68,44),'wood_dark':(34,24,22),
'amber':(255,184,84),'amber2':(255,114,35),'water0':(3,17,32),'water1':(6,37,61)}

def grad(size,a,b):
    W0,H0=size
    arr=np.zeros((H0,W0,4),dtype=np.uint8)
    for y in range(H0):
        t=y/(H0-1)
        col=[int(a[i]*(1-t)+b[i]*t) for i in range(3)]
        arr[y,:,0:3]=col;arr[y,:,3]=255
    return Image.fromarray(arr,'RGBA')

def poly(draw,pts,fill):
    draw.polygon([(int(x*S),int(y*S)) for x,y in pts],fill=fill)

def glow(size,circles,blur=10):
    layer=Image.new('RGBA',size,(0,0,0,0));d=ImageDraw.Draw(layer)
    for x,y,r,col,a in circles:
        d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=(*col,a))
    return layer.filter(ImageFilter.GaussianBlur(blur*S))

def pine(img,x,y,scale=1,near=True):
    d=ImageDraw.Draw(img)
    d.rectangle((int((x-1.2)*S),int((y-2)*S),int((x+1.2)*S),int((y+7)*S)),fill=(40,29,22,255))
    col=C['pine'] if near else C['pine2']
    for yy,ww in [(y-48*scale,14*scale),(y-37*scale,19*scale),(y-26*scale,24*scale),(y-14*scale,29*scale)]:
        poly(d,[(x,yy),(x-ww,y-1),(x+ww,y-1)],(*col,255))
    if near:
        for yy,ww in [(y-32*scale,13*scale),(y-18*scale,18*scale)]:
            d.line(((x-ww*.65)*S,yy*S,x*S,(yy-2.4*scale)*S,(x+ww*.65)*S,yy*S),fill=(94,153,192,130),width=S)

def building(img,x,y,wid,hei,roof_h,windows=2):
    d=ImageDraw.Draw(img)
    d.ellipse(((x-8)*S,(y+hei-2)*S,(x+wid+8)*S,(y+hei+7)*S),fill=(0,0,0,50))
    d.rectangle((x*S,y*S,(x+wid)*S,(y+hei)*S),fill=(*C['wood_dark'],255))
    d.rectangle(((x+4)*S,(y+3)*S,(x+wid-4)*S,(y+hei)*S),fill=(*C['wood'],255))
    for xx in range(x+10,x+wid-6,18):
        d.rectangle((xx*S,y*S,(xx+2)*S,(y+hei)*S),fill=(*C['wood2'],190))
    poly(d,[(x-7,y),(x+wid/2,y-roof_h),(x+wid+7,y)],(10,18,26,255))
    poly(d,[(x-2,y-1),(x+wid/2,y-roof_h+4),(x+wid+2,y-1),(x+wid-4,y+2),(x+wid*.66,y-roof_h*.34),(x+wid*.5,y-roof_h*.14),(x+wid*.32,y-roof_h*.34),(x+4,y+2)],(130,177,205,235))
    d.line(((x-7)*S,y*S,(x+wid/2)*S,(y-roof_h)*S,(x+wid+7)*S,y*S),fill=(108,167,208,180),width=2*S)
    gl=Image.new('RGBA',img.size,(0,0,0,0));gd=ImageDraw.Draw(gl)
    for i in range(windows):
        wx=x+wid*(i+1)/(windows+1); wy=y+hei*.47
        gd.ellipse(((wx-16)*S,(wy-12)*S,(wx+16)*S,(wy+12)*S),fill=(255,138,42,72))
        d.rectangle(((wx-5)*S,(wy-4)*S,(wx+5)*S,(wy+5)*S),fill=(235,133,45,255))
        d.rectangle(((wx-3)*S,(wy-2)*S,(wx+3)*S,(wy+3)*S),fill=(255,225,139,255))
        d.line((wx*S,(wy-4)*S,wx*S,(wy+5)*S),fill=(80,45,27,255),width=S)
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(7*S)))
    d=ImageDraw.Draw(img)
    dw=max(8,int(wid*.13))
    d.rectangle(((x+wid/2-dw/2)*S,(y+hei-dw*1.4)*S,(x+wid/2+dw/2)*S,(y+hei)*S),fill=(30,21,18,255))
    d.rectangle(((x+wid/2-dw/2+2)*S,(y+hei-dw*1.4+3)*S,(x+wid/2+dw/2-2)*S,(y+hei)*S),fill=(92,56,34,255))
    cx=x+wid*.78
    d.rectangle((cx*S,(y-roof_h+5)*S,(cx+5)*S,(y+1)*S),fill=(49,34,29,255))
    d.rectangle(((cx-1)*S,(y-roof_h+4)*S,(cx+6)*S,(y-roof_h+6)*S),fill=(14,17,20,255))
    return (cx+2.5,y-roof_h+4)

def make_base():
    base=grad((w,h),C['sky0'],C['sky2']);d=ImageDraw.Draw(base)
    for _ in range(240):
        x=rng.randrange(0,w); y=rng.randrange(0,int(58*S)); r=rng.choice([1,1,1,2,2])
        d.ellipse((x-r,y-r,x+r,y+r),fill=(120,180,245,rng.randrange(70,170)))
    neb=Image.new('RGBA',(w,h),(0,0,0,0));nd=ImageDraw.Draw(neb)
    for i in range(8):
        pts=[]
        for xx in range(-40,W+120,85):
            yy=(15+i*4)+math.sin(xx*.008+i)*8+rng.uniform(-1.5,1.5)
            pts.append((xx*S,yy*S))
        nd.line(pts,fill=(25,95,220,34),width=3*S)
    base=Image.alpha_composite(base,neb.filter(ImageFilter.GaussianBlur(7*S)));d=ImageDraw.Draw(base)
    poly(d,[(0,76),(120,42),(210,66),(318,28),(420,64),(540,32),(655,70),(770,37),(890,68),(1015,30),(1140,60),(1260,26),(1390,64),(1515,25),(1600,48),(1600,150),(0,150)],(*C['mount_far'],245))
    for p in [[(275,41),(318,28),(353,43),(336,38),(320,41),(309,36),(297,43)],[(500,46),(540,32),(579,49),(558,43),(541,47),(526,40)],[(978,45),(1015,30),(1050,46),(1035,41),(1017,45),(1004,39)],[(1224,39),(1260,26),(1293,42),(1278,38),(1260,42),(1248,35)],[(1474,38),(1515,25),(1550,41),(1534,36),(1516,40),(1503,34)]]:
        poly(d,p,(83,128,168,185))
    poly(d,[(0,94),(110,66),(215,87),(320,56),(430,88),(560,58),(690,93),(830,58),(950,91),(1080,55),(1210,90),(1350,60),(1460,85),(1600,58),(1600,150),(0,150)],(*C['mount_mid'],255))
    fg=Image.new('RGBA',(w,h),(0,0,0,0));fd=ImageDraw.Draw(fg);fd.ellipse((300*S,55*S,1320*S,130*S),fill=(39,111,190,32));base=Image.alpha_composite(base,fg.filter(ImageFilter.GaussianBlur(30*S)));d=ImageDraw.Draw(base)
    poly(d,[(0,88),(140,97),(300,112),(450,127),(0,150)],(*C['mount_near'],255));poly(d,[(1600,84),(1460,97),(1325,110),(1180,127),(1600,150)],(*C['mount_near'],255))
    poly(d,[(0,117),(110,111),(210,116),(320,108),(430,116),(545,105),(660,113),(780,102),(900,114),(1015,108),(1120,118),(1240,111),(1360,119),(1480,112),(1600,117),(1600,150),(0,150)],(*C['snow2'],255))
    poly(d,[(0,127),(120,120),(250,126),(370,117),(490,126),(620,115),(750,123),(880,114),(1010,124),(1140,117),(1270,126),(1400,119),(1600,125),(1600,150),(0,150)],(*C['snow'],255))
    poly(d,[(990,109),(1090,103),(1200,105),(1325,101),(1450,104),(1600,101),(1600,150),(1015,150)],(*C['water0'],255))
    for yy in range(109,150):
        t=(yy-109)/41; col=tuple(int(C['water1'][i]*(1-t)+C['water0'][i]*t) for i in range(3)); d.rectangle((1000*S,yy*S,1600*S,(yy+1)*S),fill=(*col,255))
    d.line((990*S,109*S,1090*S,103*S,1200*S,105*S,1325*S,101*S,1450*S,104*S,1600*S,101*S),fill=(108,169,210,180),width=2*S)
    for x in list(range(20,360,35))+list(range(1270,1600,34)): pine(base,x,126+rng.randint(-2,2),rng.uniform(.55,.92),False)
    for x in [25,68,118,176,238,300,1315,1373,1436,1500,1565]: pine(base,x,133,rng.uniform(.75,1.12),True)
    chim=[]
    for args in [(280,105,90,32,18,2),(385,112,68,26,16,1),(470,98,112,38,24,2),(600,86,190,48,31,4),(815,105,88,30,20,2),(915,111,72,26,16,1)]: chim.append(building(base,*args))
    chim.append(building(base,820,108,142,30,16,1))
    d=ImageDraw.Draw(base);d.rectangle((555*S,111*S,560*S,143*S),fill=(48,39,32,255));d.ellipse((549*S,107*S,566*S,115*S),fill=(17,31,45,255));d.line((557*S,109*S,557*S,114*S),fill=(84,186,250,220),width=S);d.line((553*S,112*S,561*S,112*S),fill=(84,186,250,220),width=S)
    base.alpha_composite(glow((w,h),[(865,129,30,C['amber2'],105),(873,129,16,C['amber'],110)],8));d=ImageDraw.Draw(base)
    d.rectangle((842*S,122*S,886*S,141*S),fill=(18,17,18,255));d.rectangle((848*S,125*S,880*S,138*S),fill=(107,35,19,255));d.rectangle((854*S,128*S,874*S,136*S),fill=(246,100,28,255));d.rectangle((861*S,130*S,868*S,135*S),fill=(255,216,116,255));d.rectangle((900*S,128*S,927*S,133*S),fill=(62,68,73,255));d.rectangle((908*S,133*S,919*S,142*S),fill=(43,47,51,255))
    d.rectangle((1040*S,108*S,1440*S,114*S),fill=(48,34,26,255));d.rectangle((1040*S,108*S,1440*S,110*S),fill=(126,86,49,255))
    for xx in range(1055,1440,55): d.rectangle((xx*S,112*S,(xx+6)*S,145*S),fill=(28,22,20,255))
    for xx in [1060,1200,1380]:
        d.rectangle((xx*S,91*S,(xx+3)*S,113*S),fill=(78,54,34,255));base.alpha_composite(glow((w,h),[(xx+1.5,91,14,C['amber'],70)],6));d=ImageDraw.Draw(base);d.rectangle(((xx-2)*S,87*S,(xx+5)*S,94*S),fill=(34,28,25,255));d.rectangle((xx*S,89*S,(xx+3)*S,92*S),fill=(255,191,91,255))
    refl=Image.new('RGBA',(w,h),(0,0,0,0));rd=ImageDraw.Draw(refl)
    for x in [1120,1210,1320,1410]:
        for k in range(6):
            alpha=max(0,42-k*6);width=16+k*3;yy=115+k*5;rd.line(((x-width)*S,yy*S,(x+width)*S,yy*S),fill=(255,168,64,alpha),width=S)
    base=Image.alpha_composite(base,refl.filter(ImageFilter.GaussianBlur(1.2*S)))
    d=ImageDraw.Draw(base)
    for _ in range(160):
        x=rng.randrange(0,w);y=rng.randrange(int(114*S),h);d.ellipse((x,y,x+rng.randint(1,4),y+rng.randint(1,3)),fill=(220,237,246,rng.randint(8,28)))
    base.alpha_composite(glow((w,h),[(280,94,65,C['electric'],22),(800,90,90,C['electric'],20),(1370,87,70,C['electric'],22)],18))
    return base,chim

base,chimneys=make_base()

def draw_ship(frame, phase):
    layer=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(layer)
    x=1180;y=110+math.sin(phase*2*math.pi)*1.8;pitch=math.sin(phase*2*math.pi+1.2)*0.7
    d.ellipse(((x-8)*S,(y+20)*S,(x+205)*S,(y+35)*S),fill=(59,116,153,30))
    poly(d,[(x,y+4),(x+190,y+4),(x+176,y+21),(x+18,y+22)],(28,20,20,255));poly(d,[(x+8,y+4),(x+181,y+5),(x+168,y+16),(x+22,y+17)],(112,70,44,255))
    d.line((x*S,(y+4)*S,(x+190)*S,(y+4)*S),fill=(190,129,73,170),width=2*S)
    d.line(((x+3)*S,(y+2)*S,(x-10)*S,(y-13)*S,(x+1)*S,(y-27)*S,(x+8)*S,(y-10)*S),fill=(88,55,36,255),width=3*S)
    for i,xx in enumerate(range(x+18,x+170,20)):
        col=[(40,68,90),(92,58,47),(49,82,103),(102,68,44)][i%4]
        d.ellipse(((xx-7)*S,(y+7)*S,(xx+7)*S,(y+21)*S),fill=(*col,255),outline=(161,116,72,255),width=2*S)
    mast=x+94;d.line((mast*S,(y+8)*S,mast*S,(y-55)*S),fill=(113,80,48,255),width=4*S)
    poly(d,[(mast+5,y-50),(mast+62,y-43),(mast+80,y-25),(mast+5,y-18)],(42,82,115,255));poly(d,[(mast+14,y-45),(mast+52,y-39),(mast+66,y-27),(mast+14,y-23)],(95,146,173,95))
    d.line((mast*S,(y-51)*S,(mast-52)*S,(y+8)*S),fill=(158,125,82,190),width=S);d.line((mast*S,(y-51)*S,(x+175)*S,(y+5)*S),fill=(158,125,82,190),width=S)
    d.line(((x+12)*S,(y+7)*S,1100*S,113*S),fill=(160,128,85,180),width=2*S);d.line(((x+178)*S,(y+7)*S,1400*S,113*S),fill=(160,128,85,180),width=2*S)
    rot=layer.rotate(pitch,resample=Image.Resampling.BICUBIC,center=((x+95)*S,(y+8)*S));frame.alpha_composite(rot)
    d2=ImageDraw.Draw(frame)
    for k in range(3):
        yy=y+27+k*6+math.sin(phase*2*math.pi+k)*1.5
        d2.arc(((x-20-k*5)*S,(yy-2)*S,(x+215+k*5)*S,(yy+8)*S),0,180,fill=(76,151,196,80-k*15),width=S)

def draw_villager(frame,x,y,dir=1,step=0,coat=(74,95,111)):
    d=ImageDraw.Draw(frame)
    d.line(((x-2)*S,(y-2)*S,(x-3+step*dir)*S,(y+6)*S),fill=(26,28,32,255),width=2*S);d.line(((x+2)*S,(y-2)*S,(x+3-step*dir)*S,(y+6)*S),fill=(26,28,32,255),width=2*S)
    poly(d,[(x-6,y-15),(x+6,y-15),(x+7,y-2),(x-7,y-2)],(*coat,255));d.rectangle(((x-6)*S,(y-8)*S,(x+6)*S,(y-5)*S),fill=(48,36,31,255));d.ellipse(((x-4)*S,(y-23)*S,(x+4)*S,(y-15)*S),fill=(187,136,104,255));poly(d,[(x-4,y-20),(x,y-25),(x+4,y-20),(x+4,y-17),(x-4,y-17)],(46,36,31,255))

def draw_dragon(frame,phase):
    if not (0.30 <= phase <= 0.72): return
    p=(phase-0.30)/(0.42);x=-120 + p*(W+260); y=30+math.sin(p*math.pi)*8;d=ImageDraw.Draw(frame);col=(4,14,24,225);hi=(22,53,77,200)
    d.line(((x-65)*S,(y+2)*S,(x-105)*S,(y+10)*S,(x-135)*S,(y+4)*S),fill=col,width=5*S);d.ellipse(((x-55)*S,(y-7)*S,(x+28)*S,(y+12)*S),fill=col);d.ellipse(((x-35)*S,(y-5)*S,(x+18)*S,(y+5)*S),fill=hi)
    poly(d,[(x+18,y-3),(x+43,y-15),(x+70,y-9),(x+81,y-3),(x+66,y+2),(x+38,y+1)],col);d.ellipse(((x+64)*S,(y-8)*S,(x+68)*S,(y-4)*S),fill=(94,200,255,255))
    flap=math.sin(p*math.pi*8)*10;poly(d,[(x-25,y-3),(x-78,y-36-flap),(x-52,y-9),(x-88,y-20-flap*.4),(x-42,y+8)],col);poly(d,[(x+2,y-4),(x+34,y-42-flap),(x+28,y-10),(x+62,y-25-flap*.4),(x+30,y+6)],col)

frames=[]
N=60
for i in range(N):
    phase=i/N;fr=base.copy();wd=ImageDraw.Draw(fr)
    for k in range(6):
        yy=114+k*6+math.sin(phase*2*math.pi+k*.7)*1.2;x0=1005+k*35+math.sin(phase*2*math.pi+k)*12;wd.line((x0*S,yy*S,(x0+380-k*25)*S,yy*S),fill=(61,141,190,45),width=S)
    sm=Image.new('RGBA',(w,h),(0,0,0,0));sd=ImageDraw.Draw(sm)
    for j,(cx,cy) in enumerate(chimneys):
        for k in range(3):
            a=(phase+j*.11+k*.22)%1;sx=cx + math.sin((a+j)*5)*3 + k*2;sy=cy - a*(24+6*k);rr=3+5*a+k;sd.ellipse(((sx-rr)*S,(sy-rr)*S,(sx+rr)*S,(sy+rr)*S),fill=(145,160,170,int(70*(1-a))))
    fr.alpha_composite(sm.filter(ImageFilter.GaussianBlur(2*S)))
    ff=Image.new('RGBA',(w,h),(0,0,0,0));fd=ImageDraw.Draw(ff);fx,fy=700,138;fd.ellipse(((fx-22)*S,(fy-18)*S,(fx+22)*S,(fy+14)*S),fill=(255,105,28,45));fr.alpha_composite(ff.filter(ImageFilter.GaussianBlur(8*S)));fd=ImageDraw.Draw(fr);flick=math.sin(phase*2*math.pi*7)*4;poly(fd,[(fx-8,fy),(fx-5,fy-14-flick),(fx,fy-7),(fx+3,fy-21+flick),(fx+8,fy)],(224,73,21,255));poly(fd,[(fx-4,fy),(fx,fy-11-flick*.3),(fx+4,fy)],(255,200,82,255))
    bx,by=902,133;hammer=math.sin(phase*2*math.pi*5);fd.rectangle(((bx-4)*S,(by-13)*S,(bx+4)*S,by*S),fill=(92,63,45,255));fd.ellipse(((bx-4)*S,(by-20)*S,(bx+4)*S,(by-12)*S),fill=(183,132,99,255));hx=bx+11;hy=by-15 + (8 if hammer>0 else -5);fd.line(((bx+4)*S,(by-10)*S,hx*S,hy*S),fill=(183,132,99,255),width=2*S);fd.rectangle(((hx-3)*S,(hy-2)*S,(hx+5)*S,(hy+2)*S),fill=(63,67,71,255))
    if hammer>0.85:
        for s in range(7):
            ang=s*.8+phase*12;rad=5+(s%3)*3;px=914+math.cos(ang)*rad;py=130-math.sin(ang)*rad;fd.ellipse(((px-1)*S,(py-1)*S,(px+1)*S,(py+1)*S),fill=(255,184,70,220))
    people=[(0,330,138,530,138,1,(78,99,114)),(1,500,137,760,137,1,(110,78,61)),(2,780,136,940,136,-1,(68,91,105)),(3,980,132,1085,125,1,(78,78,102)),(4,1100,118,1370,118,1,(84,97,108)),(5,410,140,300,140,-1,(95,75,65))]
    for j,x1,y1,x2,y2,dirc,coat in people:
        q=(phase*(.35+.07*j)+j*.15)%1;t=q*2 if q<.5 else (1-q)*2;x=x1+(x2-x1)*t;y=y1+(y2-y1)*t;step=math.sin(phase*2*math.pi*10+j)*2.5;draw_villager(fr,x,y,dirc,step,coat)
    draw_ship(fr,phase);draw_dragon(fr,phase);fd=ImageDraw.Draw(fr)
    for s in range(38):
        sx=(s*137+i*13)%W;sy=(s*29+i*4+(s%7)*11)%H
        if sy<105:
            r=1 if s%4 else 2;fd.ellipse(((sx-r)*S,(sy-r)*S,(sx+r)*S,(sy+r)*S),fill=(205,235,255,110))
    frames.append(fr.resize((W,H),Image.Resampling.LANCZOS).convert('P',palette=Image.Palette.ADAPTIVE,colors=255))

frames[0].save('midgard_bottom.gif',save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True,disposal=2)
print('built',os.path.getsize('midgard_bottom.gif'))
