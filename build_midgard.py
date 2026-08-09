from PIL import Image,ImageDraw,ImageFilter
import numpy as np,random,math,os
W,H,S=1920,150,2;w,h=W*S,H*S;r=random.Random(88)
def grad(a,b):
 A=np.zeros((h,w,4),np.uint8)
 for y in range(h):
  t=y/(h-1);A[y,:,:3]=[int(a[i]*(1-t)+b[i]*t) for i in range(3)];A[y,:,3]=255
 return Image.fromarray(A,'RGBA')
def sm(a,n=70):
 k=np.ones(n)/n;return np.convolve(np.pad(a,(n//2,n//2),'edge'),k,'same')[n//2:-n//2]
def prof(seed,base,amp):
 g=np.random.default_rng(seed);xs=np.linspace(0,w,25);ys=base*S+g.normal(0,amp*S,25)
 for q in g.choice(range(2,23),4,False):ys[q]-=g.uniform(.7,1.6)*amp*S
 return sm(np.interp(np.arange(w),xs,ys),90)
def mount(im,seed,base,amp,top,bot,alpha,snow):
 p=prof(seed,base,amp);m=np.zeros((h,w),np.uint8)
 for x,y in enumerate(np.clip(p.astype(int),0,h-1)):m[y:,x]=alpha
 f=grad(top,bot);f.putalpha(Image.fromarray(m));im.alpha_composite(f)
 d=ImageDraw.Draw(im)
 for x in range(0,w,12):
  y=int(p[x]);
  if y<snow*S:d.line((x,y,x+10,min(h-1,y+3*S)),fill=(125,176,210,90),width=S)
def glow(im,x,y,rr,c=(255,155,55),a=80,b=7):
 g=Image.new('RGBA',(w,h));d=ImageDraw.Draw(g);d.ellipse(((x-rr)*S,(y-rr)*S,(x+rr)*S,(y+rr)*S),fill=(*c,a));im.alpha_composite(g.filter(ImageFilter.GaussianBlur(b*S)))
def pine(im,x,y,s=1,far=0):
 d=ImageDraw.Draw(im);c=(6,17,25,255) if not far else (15,35,46,215)
 d.rectangle(((x-1)*S,(y-15*s)*S,(x+1)*S,(y+2)*S),fill=(42,30,22,220))
 for i in range(6):
  yy=y-(48-i*7)*s;ww=(8+i*4)*s
  d.polygon([(x*S,int((yy-5*s)*S)),(int((x-ww)*S),int((yy+10*s)*S)),(int((x-ww*.4)*S),int((yy+8*s)*S)),(int((x+ww)*S),int((yy+11*s)*S))],fill=c)
  if not far and i>1:d.line(((x-ww*.45)*S,(yy+7*s)*S,(x+ww*.35)*S,(yy+7*s)*S),fill=(105,160,190,80),width=S)
def house(im,x,y,wd,hd,roof,n=2):
 d=ImageDraw.Draw(im);d.ellipse(((x-7)*S,(y+hd-2)*S,(x+wd+8)*S,(y+hd+5)*S),fill=(0,0,0,65))
 d.rectangle((x*S,y*S,(x+wd)*S,(y+hd)*S),fill=(73,46,32,255))
 for yy in range(y+4,y+hd,5):d.line(((x+2)*S,yy*S,(x+wd-2)*S,yy*S),fill=(155,98,54,50),width=S)
 for xx in [x+6,x+wd//2,x+wd-6]:d.line((xx*S,y*S,xx*S,(y+hd)*S),fill=(37,25,21,210),width=2*S)
 d.polygon([((x-9)*S,(y+1)*S),((x+wd/2)*S,(y-roof)*S),((x+wd+9)*S,(y+1)*S)],fill=(9,17,24,255))
 d.line(((x-5)*S,y*S,(x+wd/2)*S,(y-roof+2)*S,(x+wd+5)*S,y*S),fill=(188,221,238,225),width=3*S)
 for i in range(n):
  wx=x+wd*(i+1)/(n+1);wy=y+hd*.5;glow(im,wx,wy,12)
  d=ImageDraw.Draw(im);d.rectangle(((wx-4)*S,(wy-4)*S,(wx+4)*S,(wy+4)*S),fill=(252,205,115,255));d.line((wx*S,(wy-4)*S,wx*S,(wy+4)*S),fill=(100,57,32,255),width=S)
 d.rectangle(((x+wd*.44)*S,(y+hd-17)*S,(x+wd*.56)*S,(y+hd)*S),fill=(83,49,31,255))
 cx=x+wd*.78;d.rectangle((cx*S,(y-roof+5)*S,(cx+5)*S,(y+2)*S),fill=(47,32,28,255));return cx+2,y-roof+4
base=grad((2,8,20),(7,29,53));d=ImageDraw.Draw(base)
for _ in range(360):
 x=r.randrange(w);y=r.randrange(60*S);q=r.choice([1,1,1,2]);d.ellipse((x-q,y-q,x+q,y+q),fill=(125,190,250,r.randrange(70,180)))
glow(base,950,30,620,(30,90,210),22,48)
mount(base,1,82,18,(27,53,88),(12,28,50),230,55);mount(base,2,101,15,(17,42,69),(8,23,39),248,76);mount(base,3,118,10,(11,30,47),(5,18,31),255,98)
d=ImageDraw.Draw(base);p=prof(5,130,4);g=[(x/S,p[x]/S) for x in range(0,w,24*S)]+[(W,H),(0,H)];d.polygon([(int(x*S),int(y*S)) for x,y in g],fill=(174,210,231,255))
p=prof(6,143,2.5);g=[(x/S,p[x]/S) for x in range(0,w,24*S)]+[(W,H),(0,H)];d.polygon([(int(x*S),int(y*S)) for x,y in g],fill=(86,127,156,255))
d.polygon([(1160*S,126*S),(1280*S,120*S),(1440*S,123*S),(1600*S,117*S),(1770*S,121*S),(W*S,117*S),(W*S,H*S),(1160*S,H*S)],fill=(3,17,31,255))
for yy in range(126,150):d.line((1160*S,yy*S,W*S,yy*S),fill=(5,34-max(0,yy-126)//2,60-max(0,yy-126),255),width=S)
for x in list(range(10,380,30))+list(range(1600,1910,28)):pine(base,x,138,r.uniform(.48,.75),1)
for x in [20,62,112,165,225,292,355,1530,1590,1660,1730,1800,1870,1910]:pine(base,x,145,r.uniform(.72,1.02),0)
chim=[]
for z in [(420,108,92,31,19,2),(520,115,70,25,15,1),(610,100,116,38,23,2),(748,89,214,49,32,4),(985,106,98,30,19,2),(1095,114,78,25,15,1)]:chim.append(house(base,*z))
d=ImageDraw.Draw(base)
for x,y,wd,hd in [(390,121,42,15),(580,119,38,14),(705,116,45,17),(930,119,36,14),(1140,120,33,13)]:
 d.rectangle((x*S,y*S,(x+wd)*S,(y+hd)*S),fill=(55,40,32,235));d.polygon([((x-4)*S,y*S),((x+wd/2)*S,(y-11)*S),((x+wd+4)*S,y*S)],fill=(10,18,25,245));glow(base,x+wd*.35,y+hd*.5,7,(255,155,58),55,4)
d=ImageDraw.Draw(base);d.rectangle((1015*S,119*S,1110*S,147*S),fill=(45,29,24,255));d.polygon([(1008*S,120*S),(1062*S,92*S),(1117*S,120*S)],fill=(10,18,25,255));d.line((1011*S,118*S,1062*S,96*S,1114*S,118*S),fill=(180,210,225,150),width=3*S);glow(base,1040,134,28,(255,92,26),90,7)
d=ImageDraw.Draw(base);d.rectangle((1020*S,126*S,1058*S,145*S),fill=(24,18,17,255));d.rectangle((1027*S,130*S,1051*S,140*S),fill=(239,89,27,255));d.rectangle((1073*S,134*S,1100*S,139*S),fill=(67,71,75,255))
d.rectangle((1200*S,119*S,1730*S,125*S),fill=(61,40,29,255));d.rectangle((1200*S,119*S,1730*S,121*S),fill=(143,91,50,255))
for xx in range(1218,1730,62):d.rectangle((xx*S,124*S,(xx+7)*S,150*S),fill=(28,22,20,255))
for xx in [1230,1410,1590,1700]:d.rectangle((xx*S,101*S,(xx+3)*S,119*S),fill=(77,52,34,255));glow(base,xx+1,101,14,(255,181,79),70,6)
for xx in range(385,735,28):d.rectangle((xx*S,132*S,(xx+3)*S,145*S),fill=(72,51,36,230))
d.line((385*S,136*S,735*S,136*S),fill=(105,72,46,210),width=2*S)
def person(im,x,y,step=0,co=(75,95,110),carry=0):
 d=ImageDraw.Draw(im);d.line(((x-2)*S,(y-2)*S,(x-3+step)*S,(y+6)*S),fill=(24,25,29,255),width=2*S);d.line(((x+2)*S,(y-2)*S,(x+3-step)*S,(y+6)*S),fill=(24,25,29,255),width=2*S);d.polygon([((x-6)*S,(y-15)*S),((x+6)*S,(y-15)*S),((x+7)*S,(y-2)*S),((x-7)*S,(y-2)*S)],fill=(*co,255));d.ellipse(((x-4)*S,(y-23)*S,(x+4)*S,(y-15)*S),fill=(183,132,99,255));d.pieslice(((x-5)*S,(y-25)*S,(x+5)*S,(y-17)*S),180,360,fill=(47,36,30,255))
 if carry:d.rectangle(((x+6)*S,(y-12)*S,(x+14)*S,(y-5)*S),fill=(103,71,44,255))
def ship(im,ph):
 d=ImageDraw.Draw(im);x=1335;y=122+math.sin(ph*6.283)*1.7
 for k in range(4):yy=y+27+k*5;d.line(((x-10-k*8)*S,yy*S,(x+275+k*8)*S,yy*S),fill=(79,152,196,38-k*6),width=S)
 d.polygon([(x*S,(y+4)*S),((x+255)*S,(y+4)*S),((x+234)*S,(y+24)*S),((x+18)*S,(y+25)*S)],fill=(25,18,18,255));d.polygon([((x+10)*S,(y+4)*S),((x+245)*S,(y+5)*S),((x+225)*S,(y+18)*S),((x+28)*S,(y+20)*S)],fill=(116,70,42,255))
 cols=[(42,72,94),(97,58,49),(48,83,107),(108,70,44)]
 for i,xx in enumerate(range(x+22,x+230,23)):d.ellipse(((xx-7)*S,(y+9)*S,(xx+7)*S,(y+23)*S),fill=(*cols[i%4],255),outline=(170,119,72,255),width=2*S)
 m=x+128;d.line((m*S,(y+8)*S,m*S,(y-63)*S),fill=(108,76,46,255),width=4*S);d.polygon([((m+6)*S,(y-58)*S),((m+91)*S,(y-49)*S),((m+88)*S,(y-22)*S),((m+7)*S,(y-15)*S)],fill=(42,78,108,255));d.line((m*S,(y-61)*S,(x+28)*S,(y+15)*S),fill=(157,124,79,180),width=S);d.line((m*S,(y-61)*S,(x+232)*S,(y+13)*S),fill=(157,124,79,180),width=S)
def dragon(im,ph):
 if ph<.72 or ph>.95:return
 u=(ph-.72)/.23;x=-120+u*(W+240);y=37+math.sin(u*3.14)*5;d=ImageDraw.Draw(im);c=(4,14,23,225);s=.55
 d.line(((x-50*s)*S,(y+2)*S,(x-125*s)*S,(y+4)*S),fill=c,width=3*S);d.ellipse(((x-45*s)*S,(y-7*s)*S,(x+26*s)*S,(y+10*s)*S),fill=c);d.line(((x+18*s)*S,y*S,(x+50*s)*S,(y-10*s)*S),fill=c,width=4*S)
 f=math.sin(u*25)*8;d.polygon([((x-12*s)*S,(y-3*s)*S),((x-65*s)*S,(y-(32+f)*s)*S),((x-38*s)*S,(y+7*s)*S)],fill=c);d.polygon([((x+4*s)*S,(y-4*s)*S),((x+36*s)*S,(y-(38+f)*s)*S),((x+28*s)*S,(y+6*s)*S)],fill=c)
N=60;fs=[]
for i in range(N):
 ph=i/N;im=base.copy();d=ImageDraw.Draw(im)
 for k in range(10):yy=126+k*2.2+math.sin(ph*6.283+k)*.8;d.line(((1180+k*35)*S,yy*S,(1880-k*20)*S,yy*S),fill=(62,143,189,32),width=S)
 smk=Image.new('RGBA',(w,h));sd=ImageDraw.Draw(smk)
 for j,(cx,cy) in enumerate(chim):
  for k in range(3):
   a=(ph+j*.13+k*.26)%1;sx=cx+math.sin((a+j)*5)*3;sy=cy-a*(25+5*k);rr=3+5*a;sd.ellipse(((sx-rr)*S,(sy-rr)*S,(sx+rr)*S,(sy+rr)*S),fill=(158,169,178,int(58*(1-a))))
 im.alpha_composite(smk.filter(ImageFilter.GaussianBlur(2*S)));glow(im,800,140,25,(255,91,25),60,7);d=ImageDraw.Draw(im);f=math.sin(ph*44)*4;d.polygon([(792*S,145*S),(796*S,(130-f)*S),(800*S,138*S),(804*S,(123+f)*S),(809*S,145*S)],fill=(230,76,21,255))
 ham=math.sin(ph*37.7);bx,by=1116,142;d.ellipse(((bx-4)*S,(by-22)*S,(bx+4)*S,(by-14)*S),fill=(183,131,96,255));d.rectangle(((bx-6)*S,(by-14)*S,(bx+6)*S,(by-3)*S),fill=(67,59,58,255));hx=bx+12;hy=by-14+(8 if ham>.1 else -5);d.line(((bx+4)*S,(by-11)*S,hx*S,hy*S),fill=(183,132,99,255),width=2*S);d.rectangle(((hx-4)*S,(hy-2)*S,(hx+5)*S,(hy+2)*S),fill=(63,67,71,255))
 if ham>.88:
  for q in range(8):ang=q*.8+ph*13;rr=5+(q%4)*2;px=1129+math.cos(ang)*rr;py=136-math.sin(ang)*rr;d.ellipse(((px-1)*S,(py-1)*S,(px+1)*S,(py+1)*S),fill=(255,185,68,230))
 routes=[(430,640,142,(76,97,114),0),(600,820,142,(111,78,61),1),(820,1000,141,(67,91,106),0),(1000,1170,139,(80,79,101),0),(1190,1510,126,(85,98,109),0),(1500,1700,125,(73,88,102),0)]
 for j,(a,b,y,c,ca) in enumerate(routes):
  q=(ph*(.34+.04*j)+j*.14)%1;t=q*2 if q<.5 else (1-q)*2;x=a+(b-a)*t;person(im,x,y,math.sin(ph*62.8+j)*2.2,c,ca)
 ship(im,ph);dragon(im,ph)
 for q in range(38):x=(q*187+i*19)%W;y=(q*31+i*4)%105;d.ellipse((x*S,y*S,(x+1)*S,(y+1)*S),fill=(220,241,255,85))
 small=im.resize((W,H),Image.Resampling.LANCZOS);arr=np.array(small);lum=arr[:,:,:3].max(2);ma=np.where(lum>190,np.clip((lum-190)*2,0,70),0).astype(np.uint8);bl=small.copy();bl.putalpha(Image.fromarray(ma));small=Image.alpha_composite(small,bl.filter(ImageFilter.GaussianBlur(2)));fs.append(small.convert('P',palette=Image.Palette.ADAPTIVE,colors=255))
fs[0].save('midgard_bottom.gif',save_all=True,append_images=fs[1:],duration=110,loop=0,optimize=True,disposal=2)
print(os.path.getsize('midgard_bottom.gif'))
