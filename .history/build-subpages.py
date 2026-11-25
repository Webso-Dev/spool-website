import re,sys,os,json
root=sys.argv[1]; os.chdir(root)
s=open('index.html').read()
def cut(a,b,frm=0,inc=True):
    i=s.index(a,frm); j=s.index(b,i)+(len(b) if inc else 0); return s[i:j]
logo=re.search(r'<svg class="spool-logo".*?</svg>',s,re.S).group(0)
flow=cut('<div class="flow" role="img"','</ul>\n    </div>',inc=True)
ex=cut('<div class="ex-area">','<div class="feed"',inc=False); exall=s[s.index('<div class="ex-area">'):s.index('</section>',s.index('<div class="ex-area">'))].rstrip()
stack=cut('<div class="stack">','</ul></div>')
scope=cut('<div class="cells c3 scope">','</section>',inc=False).rstrip()
NAV=[('how-it-works.html','How it works'),('features.html','Features'),('pricing.html','Pricing'),('security.html','Security'),('about.html','About')]
MORE=[('what-we-maintain.html','What we maintain'),('compare.html','Compare')]
gv=s[s.index('<div class="gains" id="cmp0"'):s.index('<div class="switch">')]
import re as _re
cards=_re.findall(r'<div class="gain">.*?</p></div>',gv,_re.S)
def gains(c): return '<div class="gains">'+''.join(chr(10)+'      '+x for x in c)+chr(10)+'    </div>'
def figs(items,plain=False): return '<div class="figs'+(' plain' if plain else '')+'">'+''.join(f'<div><b class="num">{a}</b><span>{b}</span></div>' for a,b in items)+'</div>'
MAIL='hello@hellospool.com'; CALL='https://cal.com/pekka/spool'
def header(cur):
    links=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV)
    return f'''<header class="top">
  <a class="brand" href="./" aria-label="Spool home">{logo}</a>
  <nav aria-label="Main">{links}</nav>
  <div class="right"><a class="pill pill-sm" href="contact.html"{" aria-current=\"page\"" if cur=="contact.html" else ""}>Contact</a><a class="pill pill-sm pill-blue" href="https://cal.com/pekka/spool" target="_blank" rel="noopener">Book a call</a></div>
</header>'''
def footer():
    pages=''.join(f'<a href="{h}">{t}</a>' for h,t in [('./','Home')]+NAV[:3]+MORE)
    pages2=''.join(f'<a href="{h}">{t}</a>' for h,t in NAV[3:]+[('contact.html','Contact')])
    return f'''<footer>
  <div class="foot-top">
    <div class="foot-brand">
      <a href="./" aria-label="Spool home">{logo.replace('height="26"','height="28"')}</a>
      <p>Automated maintenance for the custom software your business runs on.</p>
      <a class="pill pill-sm pill-blue" href="https://cal.com/pekka/spool" target="_blank" rel="noopener">Book a call</a>
    </div>
    <nav aria-label="Product">
      <h4>Product</h4>
      {pages}
    </nav>
    <nav aria-label="Company">
      <h4>Company</h4>
      {pages2}
    </nav>
    <div class="foot-contact">
      <h4>Contact</h4>
      <a href="mailto:{MAIL}">{MAIL}</a>
      <a href="{CALL}" target="_blank" rel="noopener">Book a 30-minute call</a>
      <span>Helsinki, Finland</span>
    </div>
  </div>
  <div class="foot-base"><span>© 2026 Spool</span><span>Helsinki, Finland</span></div>
</footer>'''
def closing(h='Tell us about the system you depend on',p='Three quick questions, then a 30-minute call. We’ll tell you honestly whether Spool fits.',quiz=True):
    inner=f'''<div class="actions"><a class="pill pill-blue" href="{CALL}" target="_blank" rel="noopener">Book a 30-minute call</a></div>'''
    if quiz: inner=f'''<div class="quiz" data-quiz>{inner}</div>'''
    return f'''<section class="block closing" id="call">
    <h2>{h}</h2>
    <p>{p}</p>
    {inner}
    <p class="or">Or write to <a href="mailto:{MAIL}">{MAIL}</a></p>
  </section>'''
SITE='https://www.hellospool.com'   # change here when the site moves to its own domain
PAGES=[]
def seo(file,title,desc,ogdesc=None):
    url=SITE+'/'+('' if file=='index.html' else file[:-5]); PAGES.append(url)
    return f'''<link rel="canonical" href="{url}">
<meta property="og:site_name" content="Spool">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{ogdesc or desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Spool — your software, maintained without a break">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{ogdesc or desc}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">'''
# links carry no .html: vercel.json turns on cleanUrls, so /pricing serves pricing.html
def clean(html): return re.sub(r'href="([a-z-]+)\.html([#"])',r'href="\1\2',html)
def head(title,desc,file):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#151414">
{seo(file,title,desc)}
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/hankengrotesk/v12/ieVn2YZDLWuGJpnzaiwFXS9tYtpd59CxCis4.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://fonts.gstatic.com/s/ibmplexmono/v23/-F63fjptAgt5VM-kVkqdyU8n1i8q131nj-o.woff2">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
'''
def feats(items): return '<ul class="feats">'+''.join(f'\n      <li><i></i><div><h3>{a}</h3><p>{b}</p></div></li>' for a,b in items)+'\n    </ul>'
def rows(items,plain=False): return '<ol class="rows'+(' plain' if plain else '')+'">'+''.join(f'\n      <li><div><h3>{a}</h3><p>{b}</p></div></li>' for a,b in items)+'\n    </ol>'
def sect(h,p,body,id_=''): return f'''
  <section class="block"{f' id="{id_}"' if id_ else ''}>
    <div class="head">
      <h2>{h}</h2>{f"""
      <p>{p}</p>""" if p else ''}
    </div>
    {body}
  </section>
'''
def page(file,title,desc,h1,lead,body,close=None,cta=True,mark=None,hero=None):
    hero=hero or f'''<div class="hero-wrap">
  <section class="hero sm">
    {dot(MARK[mark],'mark') if mark else ''}
    <h1>{h1}</h1>
    <p>{lead}</p>{"""
    <div class="actions"><a class="pill pill-light" href="https://cal.com/pekka/spool" target="_blank" rel="noopener">Book a 30-minute call</a></div>""" if cta else ''}
  </section>
</div>'''
    html=head(title,desc,file)+header(file)+'\n\n<main>\n'+hero+'\n\n<div class="frame">'+body+'\n  '+(closing() if close is None else close)+'\n\n</div>\n</main>\n\n'+footer()+'\n<script src="assets/site.js"></script>\n</body>\n</html>\n'
    open(file,'w').write(clean(html)); print('wrote',file,len(html))


MARK={
'arrow':[".......","....#..",".....#.","#######",".....#.","....#..","......."],
'grid':["###.###","###.###","###.###",".......","###.###","###.###","###.###"],
'bars':["#......","#......","#..#...","#..#...","#..#..#","#..#..#","#..#..#"],
'shield':["#######","#######","#######",".#####.",".#####.","..###..","...#..."],
'spool':["#######",".#####.","..###..","..###..","..###..",".#####.","#######"],
'mail':["#######","##...##","#.#.#.#","#..#..#","#.....#","#######"],
'stack':[".......","#######",".......","#######",".......","#######","......."],
'versus':[".......","##.....","##.....","##.....","##..##.","##..##.","##..##."],
'eye':[".......","..###..",".#...#.","#..#..#",".#...#.","..###..","......."],
'play':["##.....","####...","######.","#######","######.","####...","##....."],
'lock':["..###..",".#...#.",".#...#.","#######","###.###","###.###","#######"],
'cloud':[".......","..##...",".####..","######.","#######","#######","......."],
'plug':[".#...#.",".#...#.","#######","#######",".#####.","..###..","...#..."],
}
def dot(rows,cls='dot-icon'):
    c=''.join('<circle cx="%d" cy="%d" r="2.6"%s/>'%(x*10+5,y*10+5,' class="on"' if ch=='#' else '') for y,r in enumerate(rows) for x,ch in enumerate(r))
    return f'<svg class="dot-icon {cls}" viewBox="0 0 70 {len(rows)*10}" aria-hidden="true">{c}</svg>'
def el(x,y,w,h,cls,o=0): return f'<i class="{cls}" style="--x:{x};--y:{y};--w:{w};--h:{h};--o:{o}"></i>'
def key(b,a): return f'<dl class="key"><div><dt>Before</dt><dd>{b}</dd></div><div class="now"><dt>With Spool</dt><dd>{a}</dd></div></dl>'
def group(icon,h,p,items):
    lis=''.join(f'<li><i></i><div><h3>{a}</h3><p>{b}</p></div></li>' for a,b in items)
    return f"""
  <section class="block group">
    <div class="group-head">{dot(MARK[icon],'glyph')}<h2>{h}</h2><p>{p}</p></div>
    <ul class="feats two">{lis}</ul>
  </section>
"""
def stepgrid(items): return '<ol class="cells c3 stepgrid">'+''.join(chr(10)+'      <li class="cell"><div class="step-top">'+dot(MARK[m])+'<span>'+str(n+1)+'</span></div><h3>'+a+'</h3><p>'+b+'</p></li>' for n,(m,a,b) in enumerate(items))+chr(10)+'    </ol>'
def tag(kind,text): return f'<em class="{kind}">{text}</em>'
def limitrows(items):
    return '<ol class="steps static">'+''.join(f'<li><i></i><time>{t}</time><div class="card"><b>{a}</b><small>{b}</small></div>{tag(k,l)}</li>' for t,a,b,k,l in items)+'</ol>'

FOUND=[('New versions','Frameworks, runtimes and libraries your system depends on.'),('Infrastructure releases','Servers, databases and cloud services.'),('API changes','When a supplier or a bank changes their interface.'),('Security vulnerabilities','Handled first, as soon as they are published.'),('Production errors','Spotted in your error logs before they are reported.'),('Requests from your team','They land in the same queue as everything else.')]
SAFE=[('A full audit trail','Who or what changed each line, when, and why.'),('Ready for NIS2','Each security fix is logged with when it was published and patched.'),('EU data residency','Models and hosting can stay inside the EU.'),('Your code stays yours','We work in your repositories and cloud accounts.'),('You set the limits','You decide what goes live on its own and what waits for you.'),('Free to leave','The changelog and decision records stay in your repository.')]

# ---- How it works
page('how-it-works.html','How Spool works — from a problem to production','How Spool uses AI to find maintenance work on your custom software, do it within the limits you set, and write down every change.',
 'From a problem to production,<br>without a meeting','Spool finds the maintenance work, does it, and writes down what it did. Here is each step.',
 sect('Everything lands in one queue','Work Spool finds and work your team asks for go through the same automated steps, and end up in production and in your repository.',flow)
 +sect('Six steps, the same for every change','Spool’s AI does these on its own. A person steps in only where you have said one should.',
  stepgrid([('eye','It finds the work','Spool watches for new package versions, infrastructure releases, changes in the APIs you depend on, security vulnerabilities and errors in production. Requests from your team land in the same queue.'),
        ('grid','It plans the change','Each ticket gets a plan before any code is written. Security vulnerabilities go to the front of the queue.'),
        ('play','It builds and tests','The change is made in your repository and run against your tests. Tests that no longer match are rewritten and flagged.'),
        ('shield','It checks against your limits','You decide which kinds of change can go live on their own. Anything outside those limits waits for a Spool engineer or for your approval.'),
        ('arrow','It goes live','The change is deployed to production through your own pipeline and cloud accounts.'),
        ('stack','It is written down','A changelog entry, a decision record and an audit trail are added to your repository, so anyone can see what changed and why.')]))
 +'\n  <section class="block" id="ticket">\n    '+exall+'\n  </section>\n',mark='arrow')

# ---- Features
page('features.html','Spool features — automated maintenance for custom software','Everything Spool does: finds maintenance work on its own, plans, builds, tests and deploys it, keeps you in control, and fits into the tools you already use.',
 'Everything Spool does,<br>in one place','Automated maintenance for custom software, from finding the work to writing it down.',
 group('eye','It finds the work','Most maintenance starts before anyone has filed a ticket.',FOUND)
 +group('play','It does the work','The same automated steps for every change.',[('Plans the change','Every ticket gets a plan before any code is written.'),('Builds and tests','In your repository, against your own tests.'),('Deploys to production','Through your own pipeline and cloud accounts.'),('Every ticket finished','Each ticket we accept gets done.'),('Hours, not days','A change takes one to three hours instead of three to five days.'),('One queue, one owner','You never chase two organisations for one change.')])
 +group('lock','You stay in control','Spool runs on its own only as far as you allow.',[('You set the limits','You decide what goes live on its own and what waits for you.'),('Approvals are recorded','Who approved a change is stored with the change.'),('A full audit trail','Who or what changed each line, when, and why.'),('Changelog and decision records','Written to your repository with every change.'),('Ready for NIS2','Each security fix is logged with when it was published and patched.'),('Free to leave','The code, the history and the knowledge are already with you.')])
 +group('plug','It fits what you have','No engineering setup to build first.',[('Your own tools','Set up in your Jira, GitHub, Sentry and cloud.'),('Two to three weeks','From the first call to the first tickets done.'),('One person on your side','An architect or a product owner is enough.'),('EU data residency','Models and hosting can stay inside the EU.'),('Your code stays yours','We work in your repositories and cloud accounts.'),('Pay for finished work','Not for hours, and not for developer-months.')]),mark='grid')

# ---- Pricing
def cellrow(items): return '<div class="cells c3 scope">'+''.join(chr(10)+'      <div class="cell">'+dot(MARK[m])+'<div><h3>'+a+'</h3><p>'+b+'</p></div></div>' for m,a,b in items)+chr(10)+'    </div>'
invoice='''<div class="inv">
      <div class="inv-sum"><b>One fixed price</b><span>Set from the amount of work we maintain, and agreed before we start.</span></div>
      <dl class="inv-lines">
        <div class="paid"><dt>Finished maintenance work</dt><dd>Fixed price</dd></div>
        <div><dt>Estimates</dt><dd>€0</dd></div>
        <div><dt>Clarifications</dt><dd>€0</dd></div>
        <div><dt>Waiting</dt><dd>€0</dd></div>
        <div><dt>Work that isn’t finished</dt><dd>€0</dd></div>
      </dl>
    </div>'''
sixth='<div class="gain"><div class="viz"><div class="dm">'+el(0,1,25,3,'mid',0)+el(0,5,4,3,'on',1)+'</div>'+key('€720,000 a year','€117,000 a year')+'</div><h3>About a sixth of the cost</h3><p>A typical setup from our own years as a vendor: six offshore developers, replaced by Spool and one architect on your side.</p></div>'
page('pricing.html','Spool pricing — pay for finished work, not hours','Spool is priced on the amount of work it maintains, with a fixed estimate after we look at your systems. No hourly billing.',
 'You pay for finished work,<br>not for hours','One fixed price for the maintenance of your systems, agreed before we start.',
 sect('What is on the invoice','One line you pay for. No hourly rate and no developer-months.',invoice)
 +sect('What is included','The same for every customer.',
  feats([('Work Spool finds itself','Versions, infrastructure, API changes, vulnerabilities and production errors.'),('Requests from your team','Bug fixes and small improvements, in the same queue.'),('Setup in your tools','Two to three weeks, in your own Jira, GitHub, Sentry and cloud.'),('A full audit trail','Changelog and decision records in your repository.'),('Your limits','You decide what goes live on its own.'),('No lock-in','The code and the knowledge stay with you.')]))
 +sect('What the price depends on','We look at your systems first, free of charge, and then give you a fixed estimate.',
  cellrow([('grid','What your systems are built with','Languages, frameworks and where they run.'),
           ('bars','How much changes in a normal month','Updates, fixes and requests from your team.'),
           ('stack','What is waiting in the backlog','Work that has piled up before we start.')]))
 +sect('What it replaces','Two examples from our own work.','<div class="gains two">'+chr(10)+'      '+cards[0]+chr(10)+'      '+sixth+chr(10)+'    </div>'),
 close=closing('Get a fixed estimate','Three quick questions, then a 30-minute call. Bring your vendor contract and a rough idea of the backlog.'),mark='bars')

# ---- Security
page('security.html','Security and compliance — Spool','How Spool keeps your code, data and audit trail under your control: your repositories, your cloud accounts, your limits, and a record of every change.',
 'Your code, your accounts,<br>your limits','Spool works inside your own repositories and cloud. Every change it makes is recorded where you can see it.',
 sect('Safe to hand your systems to','What every customer gets, whatever we maintain.',feats(SAFE))
 +sect('You decide how much runs on its own','For each kind of change, you set whether it goes live automatically or waits for a person. Three examples:',
  '<div class="ex-static"><div class="tk">'+limitrows([
   ('Below','Version update','Inside your limit, so it is built, tested and deployed, then recorded.','auto','Automated'),
   ('Above','New field on order confirmations','Outside your limit, so it is prepared and waits for the person you named.','you','Your approval'),
   ('First','Security vulnerability','Goes to the front of the queue. Published and patched times are logged.','auto','Automated')])+'</div></div>')
 +sect('Nothing is held on our side','If you stop using Spool, the code, the history and the knowledge are already with you.',
  cellrow([('stack','Your repository','Every change lives here, with its changelog entry and decision record.'),('cloud','Your cloud','Every deployment runs through your own accounts and pipeline.'),('plug','Your tools','Tickets and errors stay in your own Jira and Sentry.')])),
 close=closing('Have a security question?','Send it to us, or book a call and bring your security lead. We will answer in writing.',quiz=False),mark='shield')

# ---- About
def resub(card,p): return re.sub(r'<p>.*?</p></div>$','<p>'+p+'</p></div>',card,flags=re.S)
page('about.html','About Spool — Helsinki','Spool automates the maintenance of custom business software. It comes out of years of running a software consultancy and doing that maintenance by the hour.',
 'We used to be<br>the vendor','Spool comes out of years of maintaining other companies’ custom software by the hour.',
 '''
  <section class="block">
    <figure class="statement">
      <blockquote><p class="lead">“We ran a software consultancy for years. We built custom systems for our clients, then billed by the hour to keep them running. In time we saw that most of that maintenance did not need us. Spool is what we built to do it instead.”</p></blockquote>
      <figcaption class="by"><b>Pekka Mattinen</b>, CEO</figcaption>
    </figure>
  </section>
'''+sect('How we got here','No client asked us to replace ourselves. We worked that part out on our own.',
  rows([('We built custom systems','The order systems, ERPs and portals our clients’ businesses run on.'),
        ('We billed by the hour to keep them running','Version updates, API changes, security fixes and bugs, month after month.'),
        ('We saw that most of it did not need us','The same kinds of change kept coming back, and each one followed the same steps.'),
        ('We automated our own work','Spool finds the work, does it within the limits you set, and writes down every change.')]))
 +sect('Our own first case','An ERP for a chain of car-repair shops that we had built and maintained ourselves.',
  '<div class="gains two">'+chr(10)+'      '+resub(cards[0],'What the maintenance of that one system cost, before and after.')+chr(10)+'      '+resub(cards[1],'From a request to the change running in production.')+chr(10)+'    </div>')
 +sect('What we believe','Three things we learned from the other side of the invoice.',
  cellrow([('bars','You should pay for finished work','Not for hours, and not for developer-months.'),
           ('lock','The knowledge should stay with you','Every change is written down in your own repository.'),
           ('arrow','Maintenance should not wait','Hours from a problem to production, not days.')])),cta=False,mark='spool')

# ---- Contact
contact_hero=f'''<div class="hero-wrap">
  <section class="hero sm split">
    <div class="split-text">
      {dot(MARK['mail'],'mark')}
      <h1>Tell us about the system you depend on</h1>
      <p>Three quick questions, then a 30-minute call. We’ll tell you honestly whether Spool fits.</p>
      <ul class="split-list"><li>Takes about a minute</li><li>No sales deck</li><li>A fixed estimate if Spool fits</li></ul>
      <p class="split-mail">Or write to <a href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
    <div class="split-card"><div class="quiz" data-quiz><div class="actions"><a class="pill pill-blue" href="{CALL}" target="_blank" rel="noopener">Book a 30-minute call</a></div></div></div>
  </section>
</div>'''
page('contact.html','Contact Spool — book a 30-minute call','Book a 30-minute call with Spool, or write to hello@hellospool.com. Bring your vendor contract and a rough idea of your backlog.',
 '','',
 '',close='',cta=False,hero=contact_hero)

# ---- What we maintain
page('what-we-maintain.html','What Spool maintains — custom software, kept running','The kinds of maintenance Spool takes over for custom business software: version updates, infrastructure, APIs, security fixes, bug fixes and small improvements.',
 'The custom systems<br>your business runs on','Systems an outside vendor or your own team built for you and still keeps running: order handling, production planning, the integrations around your ERP.',
 sect('Six kinds of work','Everything that keeps a system running and current, without making it a new system.',scope)
 +group('eye','Work Spool finds without being asked','Most maintenance starts before anyone has filed a ticket.',FOUND)
 +sect('Systems we keep running','The languages, databases and clouds most custom business software is built on.',stack.replace('<small>Systems we keep running</small>','').replace('class="stack"','class="stack bare"')),mark='stack')

# ---- Compare
page('compare.html','Spool compared with an outside vendor or your own team','What changes when Spool takes over maintenance from an offshore team, a consultancy or your own developers: cost, speed and who does the work.',
 'Compared with<br>what you have now','Most companies keep custom software running with an outside vendor or with their own developers. Here is what changes with Spool.',
 sect('Instead of an outside vendor','An offshore team or a consultancy, billed by the hour.',gains(cards[:3]))
 +sect('Instead of your own developers','An in-house team that also builds new things.',gains(cards[3:])),mark='versus')

# ---- Home: shared footer and closing
h=open('index.html').read()
i=h.index('<footer>'); j=h.index('</footer>',i)+9; h=h[:i]+footer()+h[j:]
i=h.index('<section class="block closing" id="call">'); j=h.index('</section>',i)+10; h=h[:i]+closing()+h[j:]
ht=re.search(r'<title>(.*?)</title>',h).group(1); hd=re.search(r'<meta name="description" content="(.*?)">',h).group(1)
HOME_OG='Your custom software, maintained without a break. Every change live in hours, with one owner and a written record.'
ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":[
 {"@type":"Organization","@id":SITE+"/#org","name":"Spool","alternateName":"Spool AI","url":SITE+"/","logo":SITE+"/assets/icon-512.png","email":"hello@hellospool.com","description":hd,"address":{"@type":"PostalAddress","addressLocality":"Helsinki","addressCountry":"FI"}},
 {"@type":"WebSite","@id":SITE+"/#site","name":"Spool","url":SITE+"/","publisher":{"@id":SITE+"/#org"},"inLanguage":"en"}]},ensure_ascii=False)+'</script>'
i=h.index('<meta name="theme-color"'); i=h.index('\n',i)+1; j=h.index('<link rel="preconnect"')
h=h[:i]+seo('index.html',ht,hd,HOME_OG)+'\n'+ld+'\n'+h[j:]
open('index.html','w').write(clean(h)); print('home head, footer and closing updated')
PAGES.sort(key=lambda u:(u!=SITE+'/',u))
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+u+'</loc></url>\n' for u in PAGES)+'</urlset>\n')
open('robots.txt','w').write('User-agent: *\nAllow: /\nDisallow: /versions/\nDisallow: /.history/\nDisallow: /index-v\n\nSitemap: '+SITE+'/sitemap.xml\n')
open('site.webmanifest','w').write(json.dumps({"name":"Spool","short_name":"Spool","description":"Automated maintenance for the custom software your business runs on.","start_url":"/","display":"browser","background_color":"#151414","theme_color":"#151414","icons":[{"src":"assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"assets/icon-512.png","sizes":"512x512","type":"image/png"}]},indent=2)+'\n')
print('sitemap',len(PAGES),'urls; robots.txt; site.webmanifest')
