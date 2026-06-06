# Generate Telugu-labelled figures as SVG-in-HTML (browser shapes Telugu correctly).
import math, os
OUT = os.path.expanduser("~/Desktop/Projects/symmetra-paper-telugu/figures")
os.makedirs(OUT, exist_ok=True)
FONT = "Sree Krushnadevaraya"
def g(x,mu,s): return math.exp(-((x-mu)**2)/(2*s*s))
def poly(pts,w=2.0,fill="none"):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{fill}" stroke="black" stroke-width="{w}"/>'
def line(x1,y1,x2,y2,w=1.5,dash=""):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="black" stroke-width="{w}"{d}/>'
def arrow(x1,y1,x2,y2,w=1.5):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="black" stroke-width="{w}" marker-end="url(#ah)"/>'
def carrow(x1,y1,cx,cy,x2,y2,w=1.4):
    return f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="black" stroke-width="{w}" marker-end="url(#ah)"/>'
def circle(cx,cy,r,w=1.6,fill="none"):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="black" stroke-width="{w}"/>'
def T(x,y,lines,size=15,anchor="middle",lh=20,italic=False):
    if isinstance(lines,str): lines=[lines]
    st=' font-style="italic"' if italic else ''
    sp="".join(f'<tspan x="{x:.1f}" dy="{0 if i==0 else lh}">{l}</tspan>' for i,l in enumerate(lines))
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}"{st} fill="black">{sp}</text>'
def Trot(x,y,s,size=14):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="{size}" fill="black" transform="rotate(-90 {x:.1f} {y:.1f})">{s}</text>'
def write(name,w,h,title,body):
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
         '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="7.5" refY="3" orient="auto" markerUnits="strokeWidth">'
         '<path d="M0,0 L7.5,3 L0,6 Z" fill="black"/></marker></defs>'
         f'<rect width="{w}" height="{h}" fill="white"/>{T(w/2,32,title,size=16)}{body}</svg>')
    html=(f'<!DOCTYPE html><html><head><meta charset="utf-8">'
          f'<link href="https://fonts.googleapis.com/css2?family=Sree+Krushnadevaraya&display=swap" rel="stylesheet">'
          f'<style>html,body{{margin:0;padding:0;background:#fff}}svg text{{font-family:\'{FONT}\',serif}}</style>'
          f'</head><body>{svg}</body></html>')
    open(os.path.join(OUT,name+".html"),"w",encoding="utf-8").write(html)

# ---- FIG 1: axis ----
w,h=680,375; yB=278; xL,xR=110,570; mu=340; sig=66; amp=185
curve=[(x, yB-amp*g(x,mu,sig)) for x in range(xL,xR+1,3)]
b=line(95,yB,585,yB,1.4)
b+=arrow(120,yB,78,yB,1.4)+arrow(560,yB,602,yB,1.4)
b+=poly(curve,2.0)
b+=line(mu,yB,mu,yB-amp,0.9,dash="5,4")
b+=circle(mu,yB-amp,4,fill="black")
b+=T(80,258,"−∞",size=15)+T(600,258,"+∞",size=15)
b+=T(mu,72,["జీవ కేంద్రం","తనను తాను తెలుసుకున్న పదార్థం"],size=15,lh=21)
b+=T(150,305,["శుద్ధ పదార్థం","(చైతన్యం లేదు)","— నిర్జీవం —"],size=13.5,lh=19)
b+=T(530,305,["శుద్ధ చైతన్యం","(పదార్థం లేదు)","— నిర్జీవం —"],size=13.5,lh=19)
b+=Trot(40,180,"సజీవత్వం / స్వీకరణ",size=13.5)
write("fig1_axis",w,h,"చిత్రం 1. అక్షం: రెండు నిర్జీవ చివరలు, ఒక జీవ కేంద్రం",b)

# ---- FIG 2: grip gauge ----
w,h=560,335; cx,cy,R=280,250,150
arc=[(cx+R*math.cos(math.radians(a)), cy-R*math.sin(math.radians(a))) for a in range(180,-1,-3)]
b=poly(arc,2.0)
for a in range(0,181,18):
    x1=cx+(R-9)*math.cos(math.radians(a)); y1=cy-(R-9)*math.sin(math.radians(a))
    x2=cx+R*math.cos(math.radians(a)); y2=cy-R*math.sin(math.radians(a))
    b+=line(x1,y1,x2,y2,1.0)
na=math.radians(58); b+=arrow(cx,cy,cx+(R-28)*math.cos(na),cy-(R-28)*math.sin(na),2.2)
b+=circle(cx,cy,6,fill="black")
b+=T(120,278,"బిగపట్టు",size=15)+T(120,298,"(జారడం)",size=12.5,italic=True)
b+=T(440,278,"తెరిచిన పట్టు",size=15)+T(440,298,"(నివాసం)",size=12.5,italic=True)
write("fig2_grip",w,h,"చిత్రం 2. పట్టు: ఒకే ముల్లు — బిగపట్టు నుండి తెరిచిన పట్టుకు",b)

# ---- FIG 3: maintained centre ----
w,h=680,375; base=305; mu=340; sig=150; amp=190; apex=base-amp
dome=[(x, base-amp*g(x,mu,sig)) for x in range(95,586,3)]
b=poly(dome,2.0)
b+=circle(mu,apex-11,11,fill="white")
b+=arrow(305,apex+30,255,apex+95,1.3)+T(243,apex+78,"జారడం",size=13,italic=True,anchor="end")
b+=arrow(375,apex+30,425,apex+95,1.3)+T(437,apex+78,"జారడం",size=13,italic=True,anchor="start")
b+=carrow(455,75,400,70,360,apex-16,1.3)+T(470,66,["నిరంతర","సరిచేత"],size=13,anchor="start",lh=18)
b+=T(120,338,"నిర్జీవ ధ్రువం",size=12.5,anchor="start")+T(560,338,"నిర్జీవ ధ్రువం",size=12.5,anchor="end")
write("fig3_centre",w,h,"చిత్రం 3. నివాసం చేరుకునేది కాదు, నిలబెట్టుకునేది",b)

# ---- FIG 4: blind spot ----
w,h=710,390; x0,x1=120,660; yTop,yBot=80,330
def gx(t): return x0+t*(x1-x0)
def gy(a): return yBot-a*(yBot-yTop)
sig_curve=[(gx(t/100.0), gy(1/(1+math.exp((t/100.0-0.5)*12)))) for t in range(0,101)]
xmid=gx(0.5)
# shaded blind zone (t>0.5 under curve)
shade_pts=[(gx(t/100.0), gy(1/(1+math.exp((t/100.0-0.5)*12)))) for t in range(50,101)]
shade=f'<polygon points="{xmid:.1f},{yBot:.1f} '+" ".join(f"{x:.1f},{y:.1f}" for x,y in shade_pts)+f' {x1:.1f},{yBot:.1f}" fill="black" fill-opacity="0.09"/>'
b=shade
b+=line(x0,yTop,x0,yBot,1.2)+line(x0,yBot,x1,yBot,1.2)
b+=poly(sig_curve,2.0)
b+=line(xmid,yTop,xmid,yBot,0.9,dash="5,4")
b+=T(108,yTop+5,"స్పష్టం",size=12.5,anchor="end")+T(108,yBot,"అంధం",size=12.5,anchor="end")
b+=T(x0,yBot+22,"తెరిచిన",size=12.5)+T(x1,yBot+22,"బిగపట్టు",size=12.5)
b+=Trot(58,205,"స్వీయ-గ్రహింపు",size=13.5)
b+=T((x0+x1)/2,yBot+45,"పట్టు  (తెరిచిన → బిగపట్టు)",size=13.5)
b+=T(gx(0.78),gy(0.62),"అంధ ప్రాంతం",size=14,italic=True)
b+=carrow(gx(0.5),gy(0.78),gx(0.62),gy(0.7),gx(0.74),gy(0.12),1.2)
b+=T(gx(0.42),gy(0.86),["బాహ్య తనిఖీలు:","టోటెమ్ · సమయం · ఒక వ్యక్తి"],size=12.5,lh=18)
write("fig4_blindspot",w,h,"చిత్రం 4. అంధ బిందువు: అవసరమైన చోటే స్వీయ-గ్రహింపు విఫలం",b)

# ---- FIG 5: node & whole ----
w,h=710,360; nx,ny,nr=180,195,55; wx,wy,wr=470,195,92
b=circle(nx,ny,nr,1.6)+circle(wx,wy,wr,1.6)
b+=T(nx,ny+6,"నోడ్",size=15)+T(wx,wy-4,["మొత్తం","వ్యవస్థ"],size=15,lh=23)
b+=carrow(nx+58,ny-18,305,ny-70,wx-96,ny-18,1.4)+T(305,ny-78,"విచలనం",size=13.5,italic=True)
b+=carrow(wx-96,ny+18,305,ny+70,nx+58,ny+18,1.4)+T(305,ny+92,"మేలు చేస్తే బహుమతి  /  హాని చేస్తే ఖర్చు",size=12.5)
b+=carrow(wx+wr-6,ny-30,wx+wr+40,ny,wx+wr-6,ny+30,1.2)+T(wx+wr+48,ny+5,["దిశ","మారుతుంది"],size=12.5,anchor="start",lh=17)
write("fig5_node_whole",w,h,"చిత్రం 5. నోడ్ మరియు మొత్తం: విచలనానికి అనుమతి, కానీ ఖర్చుతో",b)
print("html written:", sorted(f for f in os.listdir(OUT) if f.endswith('.html')))
