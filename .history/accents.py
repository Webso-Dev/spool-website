import re,sys,math,colorsys,json
css_path=sys.argv[1]; s=open(css_path).read()
# ---- OKLCH helpers
def lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def gam(c): return 12.92*c if c<=0.0031308 else 1.055*(c**(1/2.4))-0.055
def to_oklch(r,g,b):
    r,g,b=lin(r),lin(g),lin(b)
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; m=0.2119034982*r+0.6806995451*g+0.1073969566*b; t=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,t=l**(1/3),m**(1/3),t**(1/3)
    L=0.2104542553*l+0.7936177850*m-0.0040720468*t; a=1.9779984951*l-2.4285922050*m+0.4505937099*t; b2=0.0259040371*l+0.7827717662*m-0.8086757660*t
    return L,math.hypot(a,b2),math.degrees(math.atan2(b2,a))%360
def to_rgb(L,C,h):
    a=C*math.cos(math.radians(h)); b=C*math.sin(math.radians(h))
    l=(L+0.3963377774*a+0.2158037573*b)**3; m=(L-0.1055613458*a-0.0638541728*b)**3; t=(L-0.0894841775*a-1.2914855480*b)**3
    return (4.0767416621*l-3.3077115913*m+0.2309699292*t, -1.2684380046*l+2.6097574011*m-0.3413193965*t, -0.0041960863*l-0.7034186147*m+1.7076147010*t)
def fit(L,C,h):
    lo,hi=0,C
    for _ in range(24):
        mid=(lo+hi)/2; r,g,b=to_rgb(L,mid,h)
        if all(-1e-4<=x<=1+1e-4 for x in (r,g,b)): lo=mid
        else: hi=mid
    r,g,b=to_rgb(L,lo,h); return tuple(min(1,max(0,gam(min(1,max(0,x))))) for x in (r,g,b))
def hexs(rgb,alpha): return '#'+''.join('%02x'%round(x*255) for x in rgb)+alpha
# ---- find every blue literal
def parse(h):
    h=h[1:]
    if len(h) in (3,4): h=''.join(c*2 for c in h)
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4)), h[6:8]
lits={}
for m in re.finditer(r'#[0-9a-fA-F]{3,8}\b',s):
    t=m.group(0)
    if len(t)-1 not in (3,4,6,8): continue
    rgb,al=parse(t); hh,ll,ss=colorsys.rgb_to_hls(*rgb)
    if 205<=hh*360<=262 and ss>=0.22 and not (ll>0.985): lits.setdefault(t.lower(),(rgb,al))
names={t:'--a%d'%i for i,t in enumerate(sorted(lits))}
s=re.sub(r'#[0-9a-fA-F]{3,8}\b',lambda m:'var(%s)'%names[m.group(0).lower()] if m.group(0).lower() in names else m.group(0),s)
BASE=to_oklch(0x2f/255,0x6b/255,0xff/255)[2]
THEMES=[('blue','Blue',None),('violet','Violet',300),('green','Green',152),('teal','Teal',200),('orange','Orange',52),('rose','Rose',12)]
out=['\n/* ---- Accent colours. Every blue in this file is one of these variables; each accent below\n   is the same set turned to another hue at the same lightness. Generated, do not edit by hand. ---- */']
swatch={}
for key,label,hue in THEMES:
    decl=[]
    for t,(rgb,al) in sorted(lits.items()):
        if hue is None: v=t
        else:
            L,C,h=to_oklch(*rgb); v=hexs(fit(L,C,(h-BASE+hue)%360),al)
        decl.append('%s:%s'%(names[t],v))
        if t=='#2f6bff': swatch[key]=v
    out.append((':root' if hue is None else 'html[data-accent="%s"]'%key)+'{'+';'.join(decl)+'}')
s+='\n'.join(out)+'''
/* The accent switcher at the very top of the page */
.accents{display:flex;align-items:center;justify-content:center;gap:10px;padding:10px 16px 0;font-size:13.5px;color:var(--fg-3)}
.accents button{width:22px;height:22px;padding:0;border-radius:50%;border:0;background:var(--sw);cursor:pointer;box-shadow:inset 0 1px 0 #ffffff59,0 0 0 2px var(--bg),0 0 0 3px transparent;transition:box-shadow .15s,transform .12s}
.accents button:hover{transform:scale(1.12)}
.accents button[aria-pressed="true"]{box-shadow:inset 0 1px 0 #ffffff59,0 0 0 2px var(--bg),0 0 0 4px #f0e3de}
'''
open(css_path,'w').write(s)
print(len(lits),'blue colours turned into variables')
print(json.dumps([[k,l,swatch[k]] for k,l,_ in THEMES]))
