import re,sys,os
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
MAIL='hello@hellospool.com'; CALL=f'mailto:{MAIL}?subject=30-minute%20call%20about%20our%20system'
def header(cur):
    links=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV)
    return f'''<header class="top">
  <a class="brand" href="index.html" aria-label="Spool home">{logo}</a>
  <nav aria-label="Main">{links}</nav>
  <div class="right"><a class="pill pill-sm" href="contact.html"{" aria-current=\"page\"" if cur=="contact.html" else ""}>Contact</a><a class="pill pill-sm pill-blue" href="contact.html#call">Book a call</a></div>
</header>'''
def footer():
    pages=''.join(f'<a href="{h}">{t}</a>' for h,t in [('index.html','Home')]+NAV[:3]+MORE)
    pages2=''.join(f'<a href="{h}">{t}</a>' for h,t in NAV[3:]+[('contact.html','Contact')])
    return f'''<footer>
  <div class="foot-top">
    <div class="foot-brand">
      <a href="index.html" aria-label="Spool home">{logo.replace('height="26"','height="28"')}</a>
      <p>Automated maintenance for the custom software your business runs on.</p>
      <a class="pill pill-sm pill-blue" href="contact.html#call">Book a call</a>
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
      <a href="{CALL}">Ask for a 30-minute call</a>
      <span>Spool Oy<br>Helsinki, Finland</span>
    </div>
  </div>
  <div class="foot-base"><span>© 2026 Spool Oy</span><span>Helsinki, Finland</span></div>
</footer>'''
def closing(h='Tell us about the system you depend on',p='Three quick questions, then a 30-minute call. We’ll tell you honestly whether Spool fits.',quiz=True):
    inner=f'''<div class="actions"><a class="pill pill-blue" href="{CALL}">Book a 30-minute call</a></div>'''
    if quiz: inner=f'''<div class="quiz" data-quiz>{inner}</div>'''
    return f'''<section class="block closing" id="call">
    <h2>{h}</h2>
    <p>{p}</p>
    {inner}
    <p class="or">Or write to <a href="mailto:{MAIL}">{MAIL}</a></p>
  </section>'''
def head(title,desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#151414">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
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
    <div class="actions"><a class="pill pill-light" href="contact.html#call">Book a 30-minute call</a></div>""" if cta else ''}
  </section>
</div>'''
    html=head(title,desc)+header(file)+'\n\n<main>\n'+hero+'\n\n<div class="frame">'+body+'\n  '+(closing() if close is None else close)+'\n\n</div>\n</main>\n\n'+footer()+'\n<script src="assets/site.js"></script>\n</body>\n</html>\n'
    open(file,'w').write(html); print('wrote',file,len(html))


MARK={
'arrow':[".......","....#..",".....#.","#######",".....#.","....#..","......."],
'grid':["###.###","###.###","###.###",".......","###.###","###.###","###.###"],
'bars':["#......","#......","#..#...","#..#...","#..#..#","#..#..#","#..#..#"],
'shield':["#######","#######","#######",".#####.",".#####.","..###..","...#..."],
'spool':["#######",".#####.","..###..","..###..","..###..",".#####.","#######"],
'mail':["#######","##...##","#.#.#.#","#..#..#","#.....#","#######","......."],
'stack':[".......","#######",".......","#######",".......","#######","......."],
'versus':[".......","##.....","##.....","##.....","##..##.","##..##.","##..##."],
'eye':[".......","..###..",".#...#.","#..#..#",".#...#.","..###..","......."],
'play':["##.....","####...","######.","#######","######.","####...","##....."],
'lock':["..###..",".#...#.",".#...#.","#######","###.###","###.###","#######"],
'plug':[".#...#.",".#...#.","#######","#######",".#####.","..###..","...#..."],
}
def dot(rows,cls='dot-icon'):
    c=''.join('<circle cx="%d" cy="%d" r="2.6"%s/>'%(x*10+5,y*10+5,' class="on"' if ch=='#' else '') for y,r in enumerate(rows) for x,ch in enumerate(r))
    return f'<svg class="dot-icon {cls}" viewBox="0 0 70 70" aria-hidden="true">{c}</svg>'
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
def tag(kind,text): return f'<em class="{kind}">{text}</em>'
def limitrows(items):
    return '<ol class="steps static">'+''.join(f'<li><i></i><time>{t}</time><div class="card"><b>{a}</b><small>{b}</small></div>{tag(k,l)}</li>' for t,a,b,k,l in items)+'</ol>'

FOUND=[('New versions','Frameworks, runtimes and libraries your system depends on.'),('Infrastructure releases','Servers, databases and cloud services.'),('API changes','When a supplier or a bank changes their interface.'),('Security vulnerabilities','Handled first, as soon as they are published.'),('Production errors','Spotted in your error logs before they are reported.'),('Requests from your team','They land in the same queue as everything else.')]
SAFE=[('A full audit trail','Who or what changed each line, when, and why.'),('Ready for NIS2','Each security fix is logged with when it was published and patched.'),('EU data residency','Models and hosting can stay inside the EU.'),('Your code stays yours','We work in your repositories and cloud accounts.'),('You set the limits','You decide what goes live on its own and what waits for you.'),('Free to leave','The changelog and decision records stay in your repository.')]

# ---- How it works
page('how-it-works.html','How Spool works — from a problem to production','How Spool finds maintenance work on your custom software, does it automatically within the limits you set, and writes down every change.',
 'From a problem to production,<br>without a meeting','Spool finds the maintenance work, does it, and writes down what it did. Here is each step.',
 sect('Six steps, the same for every change','Our software does these on its own. A person steps in only where you have said one should.',
  rows([('It finds the work','Spool watches for new package versions, infrastructure releases, changes in the APIs you depend on, security vulnerabilities and errors in production. Requests from your team land in the same queue.'),
        ('It plans the change','Each ticket gets a plan before any code is written. Security vulnerabilities go to the front of the queue.'),
        ('It builds and tests','The change is made in your repository and run against your tests. Tests that no longer match are rewritten and flagged.'),
        ('It checks against your limits','You decide which kinds of change can go live on their own. Anything outside those limits waits for a Spool engineer or for your approval.'),
        ('It goes live','The change is deployed to production through your own pipeline and cloud accounts.'),
        ('It is written down','A changelog entry, a decision record and an audit trail are added to your repository, so anyone can see what changed and why.')]))
 +sect('Everything lands in one queue','Work Spool finds and work your team asks for go through the same automated steps, and end up in production and in your repository.',flow)
 +'\n  <section class="block" id="ticket">\n    '+exall+'\n  </section>\n'
 +sect('Getting started','Spool is set up inside the tools you already use.',
  figs([('2–3 weeks','from the first call to the first tickets done'),('Your tools','set up in your own Jira, GitHub, Sentry and cloud'),('One person','on your side: an architect or a product owner')],plain=True)),mark='arrow')

# ---- Features
page('features.html','Spool features — automated maintenance for custom software','Everything Spool does: finds maintenance work on its own, plans, builds, tests and deploys it, keeps you in control, and fits into the tools you already use.',
 'Everything Spool does,<br>in one place','Automated maintenance for custom software, from finding the work to writing it down.',
 group('eye','It finds the work','Most maintenance starts before anyone has filed a ticket.',FOUND)
 +group('play','It does the work','The same automated steps for every change.',[('Plans the change','Every ticket gets a plan before any code is written.'),('Builds and tests','In your repository, against your own tests.'),('Deploys to production','Through your own pipeline and cloud accounts.'),('Every ticket finished','Each ticket we accept gets done.'),('Hours, not days','A change takes one to three hours instead of three to five days.'),('One queue, one owner','You never chase two organisations for one change.')])
 +group('lock','You stay in control','Spool runs on its own only as far as you allow.',[('You set the limits','You decide what goes live on its own and what waits for you.'),('Approvals are recorded','Who approved a change is stored with the change.'),('A full audit trail','Who or what changed each line, when, and why.'),('Changelog and decision records','Written to your repository with every change.'),('Ready for NIS2','Each security fix is logged with when it was published and patched.'),('Free to leave','The code, the history and the knowledge are already with you.')])
 +group('plug','It fits what you have','No engineering setup to build first.',[('Your own tools','Set up in your Jira, GitHub, Sentry and cloud.'),('Two to three weeks','From the first call to the first tickets done.'),('One person on your side','An architect or a product owner is enough.'),('EU data residency','Models and hosting can stay inside the EU.'),('Your code stays yours','We work in your repositories and cloud accounts.'),('Pay for finished work','Not for hours, and not for developer-months.')]),mark='grid')

# ---- Pricing
costviz='<div class="gains one"><div class="gain wide"><div class="viz"><div class="dm">'+el(0,1,25,3,'mid',0)+el(0,5,4,3,'on',1)+'</div>'+key('€720,000 a year for six offshore developers','€117,000 a year for Spool and one architect on your side')+'</div><h3>About a sixth of the cost</h3><p>A typical setup, from our own years as a vendor: the same maintenance work, done by Spool with one architect on your side.</p></div></div>'
page('pricing.html','Spool pricing — pay for finished work, not hours','Spool is priced on the amount of work it maintains, from €30,000 a year, with a fixed estimate after we look at your systems. No hourly billing.',
 'You pay for finished work,<br>not for hours','Priced on the amount of work we maintain, from €30,000 a year.',
 sect('From €30,000 a year','One price for the maintenance of your systems. No hourly rate and no developer-months.',
  figs([('€30,000','a year is where prices start'),('Fixed','estimate, given after we look at your systems'),('€0','for estimates, clarifications or waiting')],plain=True))
 +sect('How the price is set','Three steps, and the first is free.',
  rows([('We look at your systems','What they are built with, how much changes in a normal month, and what is waiting in the backlog.'),
        ('You get a fixed estimate','Priced on the amount of work we maintain, not on hours.'),
        ('You pay for finished work','Every ticket we accept gets done.')]))
 +sect('What it replaces','',costviz)
 +sect('What is included','The same for every customer.',
  feats([('Work Spool finds itself','Versions, infrastructure, API changes, vulnerabilities and production errors.'),('Requests from your team','Bug fixes and small improvements, in the same queue.'),('Setup in your tools','Two to three weeks, in your own Jira, GitHub, Sentry and cloud.'),('A full audit trail','Changelog and decision records in your repository.'),('Your limits','You decide what goes live on its own.'),('No lock-in','The code and the knowledge stay with you.')])),
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
  figs([('Your repository','holds every change, with its changelog entry and decision record'),('Your cloud','runs every deployment, through your own accounts and pipeline'),('Your tools','keep the tickets and errors, in your own Jira and Sentry')],plain=True)),
 close=closing('Have a security question?','Send it to us, or book a call and bring your security lead. We will answer in writing.',quiz=False),mark='shield')

# ---- About
page('about.html','About Spool — Helsinki','Spool is a Helsinki company that automates the maintenance of custom business software. It was built by people who ran a software consultancy for years.',
 'We used to be<br>the vendor','Spool is built by people who spent years maintaining other companies’ custom software by the hour.',
 '''
  <section class="block">
    <div class="statement">
      <p class="lead">We ran a software consultancy for years. We built custom systems for our clients, then billed by the hour to keep them running. In time we saw that most of that maintenance did not need us. Spool is what we built to do it instead.</p>
      <p class="by"><b>How Spool started</b>, Helsinki</p>
    </div>
  </section>
'''+sect('Our own first case','An ERP for a chain of car-repair shops that we had built and maintained ourselves.',
  figs([('€5,600','a week for maintenance, before'),('€1,500','a week for maintenance, with Spool'),('1–3 hours','from a request to production, down from 3–5 days')]))
 +sect('What we believe','Three things we learned from the other side of the invoice.',
  feats([('You should pay for finished work','Not for hours, and not for developer-months.'),('The knowledge should stay with you','Every change is written down in your own repository.'),('Maintenance should not wait','Hours from a problem to production, not days.')]))
 +sect('The company','',
  figs([('Spool Oy','a Finnish company'),('Helsinki','is where we are based'),('Pekka Mattinen','is our CEO. He takes the first call with every new customer')],plain=True)),cta=False,mark='spool')

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
    <div class="split-card"><div class="quiz" data-quiz><div class="actions"><a class="pill pill-blue" href="{CALL}">Book a 30-minute call</a></div></div></div>
  </section>
</div>'''
page('contact.html','Contact Spool — book a 30-minute call','Book a 30-minute call with Spool, or write to hello@hellospool.com. Bring your vendor contract and a rough idea of your backlog.',
 '','',
 sect('What happens on the call','Thirty minutes, and you leave with a clear answer.',
  rows([('You describe the system','What it does, who built it, and who keeps it running today.'),
        ('We look at the maintenance','Bring your vendor contract, or a rough idea of the backlog and what it costs you.'),
        ('We tell you whether Spool fits','If it does, we give you a fixed estimate after looking at your systems. If it does not, we say so.')]))
 +f'''
  <section class="block">
    <div class="reach">
      <div><span>Write to us</span><a href="mailto:{MAIL}">{MAIL}</a><p>We answer within one working day.</p></div>
      <div><span>Ask for a call</span><a href="{CALL}">Suggest a time by email</a><p>Send a couple of times that suit you and we will confirm one.</p></div>
      <div><span>Where we are</span><b>Spool Oy</b><p>Helsinki, Finland</p></div>
    </div>
  </section>
''',close='',cta=False,hero=contact_hero)

# ---- What we maintain
page('what-we-maintain.html','What Spool maintains — custom software, kept running','The kinds of maintenance Spool takes over for custom business software: version updates, infrastructure, APIs, security fixes, bug fixes and small improvements.',
 'The custom systems<br>your business runs on','Systems an outside vendor or your own team built for you and still keeps running: order handling, production planning, the integrations around your ERP.',
 sect('Six kinds of work','Everything that keeps a system running and current, without making it a new system.',scope)
 +sect('Systems we keep running','The languages, databases and clouds most custom business software is built on.',stack.replace('<small>Systems we keep running</small>','').replace('class="stack"','class="stack bare"'))
 +group('eye','Work Spool finds without being asked','Most maintenance starts before anyone has filed a ticket.',FOUND),mark='stack')

# ---- Compare
page('compare.html','Spool compared with an outside vendor or your own team','What changes when Spool takes over maintenance from an offshore team, a consultancy or your own developers: cost, speed and who does the work.',
 'Compared with<br>what you have now','Most companies keep custom software running with an outside vendor or with their own developers. Here is what changes with Spool.',
 sect('Instead of an outside vendor','An offshore team or a consultancy, billed by the hour.',gains(cards[:3]))
 +sect('Instead of your own developers','An in-house team that also builds new things.',gains(cards[3:])),mark='versus')

# ---- Home: shared footer and closing
h=open('index.html').read()
i=h.index('<footer>'); j=h.index('</footer>',i)+9; h=h[:i]+footer()+h[j:]
i=h.index('<section class="block closing" id="call">'); j=h.index('</section>',i)+10; h=h[:i]+closing()+h[j:]
open('index.html','w').write(h); print('home footer and closing updated')
