import re, os, html, json
OUT='/workspace/diler-consult'
PLX='/workspace/consult/plx'
EMAIL='info@toromovers.com'
KEY='e2f8f8d8-34b9-425d-ad45-cba50184ec8e'
CTA='/order/?service=llc-formation#order'
DISC='Diler Services LLC is not a law firm and does not give legal or tax advice.'
SITE='https://dilerservices.com'
ARROW='<span><i class="fa-solid fa-arrow-right-long"></i></span>'

def img(name, alt, cls='', w=1200, lazy=True, attrs=''):
    return (f'<img src="/assets/img/{name}-{w}.webp" srcset="/assets/img/{name}-640.webp 640w, /assets/img/{name}-1200.webp 1200w" '
            f'sizes="(min-width: 992px) 50vw, 100vw" alt="{alt}" class="{cls}" {"loading=\"lazy\" decoding=\"async\"" if lazy else "fetchpriority=\"high\""} {attrs}>')

def btn(href, text, extra=''):
    return f'<div class="theme-btn4 margin-t32 d-inline-block margn-left {extra}"><a href="{href}" class="theme-btn5 font-outfit font-16 weight-700">{text} {ARROW}</a></div>'

def tag(t, extra='margin-b20'):
    return f'<span class="maximum font-outfit font-16 lineh-16 color-12 weight-500 {extra} d-inline-block">{t}</span>'

NAV=[('/','Home'),('/about/','About Us'),('/services/','Our Services'),('/how-it-works/','How It Works'),('/faqs/','FAQs'),('/blog/','Guides'),('/contact/','Contact')]

PAL_JS="<script>(function(){try{var q=new URLSearchParams(location.search).get('palette'),s=sessionStorage;if(q)s.setItem('dsPal',q);var p=s.getItem('dsPal');if(/^[abc]$/.test(p||'')){document.documentElement.classList.add('pal-'+p);var l=document.createElement('link');l.rel='stylesheet';l.href='/assets/css/palettes.css';document.head.appendChild(l)}}catch(e){}})()</script>"
def head(title, desc, path, extra_head=''):
    hero_font = ''
    pre = '<link rel="preload" as="image" href="/assets/img/consultation-1-640.webp" imagesrcset="/assets/img/consultation-1-640.webp 640w, /assets/img/consultation-1-1200.webp 1200w" imagesizes="(min-width: 992px) 50vw, 100vw">' if path=='/' else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}{path}">

<link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/3603c1d7f7.woff2" crossorigin>

<link rel="stylesheet" href="/assets/css/{"home" if path=="/" else "inner"}.min.css">
{PAL_JS}
{pre}{extra_head}
</head>
<body>
<div class="paginacontainer"><div class="progress-wrap"><svg class="progress-circle svg-content" viewBox="-1 -1 102 102"><path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98"/></svg></div></div>
'''

LOGO='<span class="ds-logo">Diler <b>Services</b></span>'

def header(path):
    home = path=='/'
    def a(h,t):
        if home and h!='/':
            pass
        act=' class="font-outfit font-18 weight-500 color-1 active"' if h==path else ' class="font-outfit font-18 weight-500 color-1"'
        return f'<li><a href="{h}"{act}>{t}</a></li>'
    items=''.join(a(h,t) for h,t in NAV)
    mitems=''.join(f'<li><a href="{h}" class="font-outfit font-16 weight-500 color">{t}</a></li>' for h,t in NAV)
    return f'''<header class="header about-bg d-none d-lg-block">
<div class="header-area header" id="header"><div class="container"><div class="row"><div class="col-12"><div class="header-elements">
<div class="site-logo"><a href="/" aria-label="Diler Services home">{LOGO}</a></div>
<div class="main-menu-ex homepage5 mainmenuex"><ul>{items}</ul></div>
<div class="contact-3 d-lg-block d-none"><div class="all-3-btn theme-btn1"><div class="theme-btn4"><a href="{CTA}" class="theme-btn5 font-outfit font-16 weight-700">Start your LLC {ARROW}</a></div></div></div>
</div></div></div></div></div>
</header>
<div class="mobile-header mobile-header-4 d-block d-lg-none homepagesmall"><div class="container-fluid"><div class="col-12"><div class="mobile-header-elements">
<div class="mobile-logo"><a href="/" aria-label="Diler Services home">{LOGO}</a></div>
<button type="button" class="mobile-nav-icon dots-menu" aria-label="Open menu"><i class="fa-solid fa-bars"></i></button>
</div></div></div></div>
<div class="mobile-sidebar">
<div class="logoicons-area"><div class="logos">{LOGO}</div><button type="button" class="menu-close" aria-label="Close menu"><i class="fa-solid fa-xmark"></i></button></div>
<div class="mobile-nav"><ul class="mobile-nav-list">{mitems}</ul>
<div class="allmobilesection"><a href="{CTA}" class="font-outfit font-18 lineh-18 weight-700 color mobilemenubtn">Start your LLC</a>
<div class="single-footer single-footer-menu single-footer4"><h3 class="font-outfit font-24 lineh-24 weight-600 color margin-b margin-t24">Contact Info</h3>
<div class="footer4-contact-info"><div class="contact-info-single"><div class="contact-info-icon"><img src="/assets/images/icons/email4.svg" alt="" width="20" height="20"></div><div class="contact-info-text"><a href="mailto:{EMAIL}" class="font-outfit font-16 lineh-26 weight-500 color-21">{EMAIL}</a></div></div></div>
<p class="ds-disc-m">{DISC}</p></div></div></div>
</div>
'''

def breadcrumb(title, crumb=None, sub=None, h1=True):
    crumb = crumb or title
    tg = 'h1' if h1 else 'p'
    s = f'<p class="font-18 lineh-28 color weight-400 ds-crumb-sub">{sub}</p>' if sub else ''
    return f'''<div class="welcomeabout-area ds-inner-hero"><div class="container"><div class="row"><div class="col-lg-12"><div class="welcomeaboiut2 text-center">
<{tg} class="font-outfit font-60 lineh-64 weight-600 color margin-b24 ds-bc-title">{title}</{tg}>{s}
<p class="font-20 weight-500 font-outfit lineh-20 color"><a href="/" class="color">Home</a><span><i class="fa-solid fa-angle-right"></i></span> {crumb}</p>
</div></div></div></div><img src="/assets/images/elementor/elementor6.png" alt="" class="elementor-6"></div>
'''

ICDIM={'icon4.png':'width="38" height="32"','icon6.png':'width="35" height="32"'}
SERVICES=[
 ('llc-formation','LLC Formation','$89','plus the $125 Florida state fee',['Articles of Organization prepared','Filed with the State of Florida','Submitted within 1 business day'],'icon2.svg','/llc-formation/'),
 ('ein-filing','EIN Filing','$95','flat service fee',['IRS employer identification number','Used for banking and payroll','Confirmation delivered by email'],'icon1.svg','/services/ein-filing/'),
 ('registered-agent','Registered Agent','$13.99/mo','or $169 per year',['Florida registered agent address','Official notices received for you','Same-day mail forwarding'],'icon3.svg','/services/registered-agent/'),
 ('formation-bundle','Formation Bundle','$299','total, state fee included',['LLC formation and EIN filing','Florida state fee included','One flat total, saves $10'],'icon4.png','/services/formation-bundle/'),
 ('annual-report','Annual Report','$99','plus state fee ($149 if late)',['Florida annual report filed','Due January 1 to May 1','Keeps the company active'],'icon5.png','/services/annual-report/'),
 ('dba','DBA (Fictitious Name)','$129','plus the state fee at cost',['Fictitious name registration','Operate under a brand name','Filed with the State of Florida'],'icon6.png','/services/dba/'),
 ('amendment','Amendments','$99','plus the state fee at cost',['Update members or managers','Change addresses or the name','Filed with the State of Florida'],'icon2.svg','/services/amendment/'),
 ('reinstatement','Reinstatement','$299','plus the state fees at cost',['Restore an inactive company','Past due reports brought current','Return to active status'],'icon1.svg','/services/reinstatement/'),
]

def service_cards(items):
    out=''
    for i,(k,n,p,note,pts,ic,href) in enumerate(items):
        anim='fade-down' if i<3 else 'fade-up'
        out+=f'''<div class="col-lg-4 col-md-6 ds-cardcol" data-aos="{anim}" data-aos-duration="{1000+200*(i%3)}"><div class="service-after-before ds-card">
<div class="service2-icon ds-card-icon"><img src="/assets/images/icons/{ic}" alt="" width="40" height="40"></div>
<a href="{href}"><h3 class="font-outfit font-22 weight-600 lineh-28 color-17 margin-b ds-card-title">{n}</h3></a>
<p class="font-outfit font-16 lineh-26 weight-400 color-15 ds-card-desc">{'. '.join(pts)}.</p>
<p class="ds-price font-outfit weight-700 color-17">{p} <span class="weight-400 font-16">{note}</span></p>
<div class="ds-card-actions"><a href="/order/?service={k}#order" class="ds-buy">Order now</a><a href="{href}" class="font-16 font-outfit weight-700 color-17 lineh-26 learn-more">Details {ARROW}</a></div>
</div></div>'''
    return out

def services_section(title_tag, h, items, more=True):
    m = f'<div class="row"><div class="col-lg-12 text-center" data-aos="fade-up" data-aos-duration="1200"><div class="theme-btn4 d-inline-block margin-left service-center"><a href="/services/" class="theme-btn5 font-outfit font-16 weight-700 margin-t32">View all services {ARROW}</a></div></div></div>' if more else ''
    return f'''<div class="service2-section-areas section-padding8" id="service">
<img src="/assets/images/elementor/elementor9.png" alt="" class="elementoe5">
<div class="container"><div class="row"><div class="col-lg-12" data-aos="fade-down" data-aos-duration="800"><div class="service-haeder-text text-center margin-b60">
{tag(title_tag)}<h2 class="font-outfit font-44 weight-600 lineh-52 color-17 margin-b20">{h}</h2></div></div></div>
<div class="row">{service_cards(items)}</div>{m}</div>
<img src="/assets/images/elementor/elementor8.png" alt="" class="elementor-7 aniamtion-key-2"></div>
'''

def plan_row(name, price, per, desc, feats, key, dur):
    half=(len(feats)+1)//2
    def ul(fs):
        return '<ul>'+''.join(f'<li class="margin-b24"><span><i class="fa-solid fa-check"></i></span> <p class="font-16 font-outfit lineh-20 weight-500 color-17">{f}</p></li>' for f in fs)+'</ul>'
    return f'''<div class="row"><div class="col-lg-1"></div><div class="col-lg-10" data-aos="fade-down" data-aos-duration="{dur}"><div class="tabs2-area margin-b30"><div class="row">
<div class="col-lg-4"><div class="pricing2-textarea"><h3 class="font-outfit font-24 weight-500 lineh-26 color-17 margin-b20">{name}</h3><div class="space20"></div>
<p class="pricing-heading font-outfit color-17 margin-b weight-700 font-44">{price}<span class="font-outfit font-20 weight-500 lineh-20 color-17">{per}</span></p>
<p class="font-outfit font-16 color-15 weight-400 lineh-26">{desc}</p>
{btn('/order/?service='+key+'#order','Order now')}</div></div>
<div class="col-lg-8"><div class="features-textarea"><div class="row">
<div class="col-lg-6"><div class="features-author-area"><h4 class="font-24 font-outfit lineh-24 color-17 margin-b24 weight-600">Included</h4><div class="features-list">{ul(feats[:half])}</div></div></div>
<div class="col-lg-6"><div class="features-author-area margin-t45"><div class="features-list">{ul(feats[half:])}</div></div></div>
</div></div></div></div></div></div></div>'''

def pricing_section():
    A=[('LLC Formation','$89',' + state fee','The $125 Florida state fee is passed through at cost. Submitted within 1 business day of complete information, or the $89 service fee is refunded.',['Articles of Organization prepared','Filed with the State of Florida','State fee paid at cost','State confirmation delivered','Free name refile','Email support'],'llc-formation'),
       ('Formation Bundle','$299',' total','LLC formation, the $125 Florida state fee and EIN filing in one flat total. Save $10 versus ordering separately.',['Articles of Organization prepared','Florida state fee included','EIN application prepared and submitted','EIN confirmation letter delivered','Free name refile','Single point of contact'],'formation-bundle'),
       ('Registered Agent','$13.99','/month','Or $169 per year. Billed separately and not included in formation or the bundle.',['Florida registered agent address','Official notices received for you','Same-day mail forwarding','Required for every Florida LLC','Annual report reminders','Monthly or yearly billing'],'registered-agent')]
    B=[('Annual Report','$99',' + state fee','$149 if filed late. The state fee is passed through at cost.',['Florida annual report filed','Due between January 1 and May 1','Keeps the company active','Deadline reminders'],'annual-report'),
       ('DBA (Fictitious Name)','$129',' + state fee','The state fee is passed through at cost.',['Fictitious name registration','Operate under a brand name','Filed with the State of Florida','Confirmation delivered'],'dba'),
       ('Amendments','$99',' + state fee','The state fee is passed through at cost.',['Update members or managers','Change addresses or the company name','Filed with the State of Florida','Confirmation delivered'],'amendment'),
       ('Reinstatement','$299',' + state fees','State fees are passed through at cost.',['Restore an inactive company','Past due reports brought current','Return to active status','Confirmation delivered'],'reinstatement')]
    a=''.join(plan_row(*p,1000+200*i) for i,p in enumerate(A))
    b=''.join(plan_row(*p,1000) for i,p in enumerate(B))
    return f'''<div class="pricing2-plan-section-area section-padding8" id="pricing"><div class="container">
<div class="row"><div class="col-lg-12" data-aos="fade-down" data-aos-duration="800"><div class="pricing-pan2-header text-center">{tag('Pricing')}<h2 class="font-outfit font-44 weight-600 lineh-52 color-17">Transparent Pricing for Business Formation</h2>
<p class="font-outfit font-16 lineh-26 color-15 margin-t">Flat service fees. State fees at cost, every time.</p></div></div></div>
<div class="row"><div class="col-lg-12 text-center" data-aos="fade-down" data-aos-duration="800"><div class="plan-toggle-wrap margin-t32"><div class="toggle-inner">
<input id="ce-toggle" type="checkbox" aria-label="Switch between formation and compliance pricing"><span class="custom-toggle"></span>
<span class="t-month font-outfit font-16 lineh-26 weight-500 colop">Formation</span><span class="t-year font-outfit font-16 lineh-26 weight-500 colop">Compliance</span>
</div></div></div>
<div class="col-lg-12"><div class="tab-content"><div id="monthly" style="display:block;">{a}</div><div id="yearly" style="display:none;">{b}</div></div></div></div>
</div></div>'''

FAQ_GROUPS=json.load(open('/workspace/consult/gen/faq.json'))

def faq_carousel():
    items=[]
    pick=[(0,1),(0,2),(1,0),(1,3),(2,2),(3,2)]
    for g,i in pick:
        q=FAQ_GROUPS[g]['items'][i]
        items.append(f'''<div class="testimonial-autor-area"><div class="qutio1 margin-b"><img src="/assets/images/icons/quito1.svg" alt="" width="48" height="36"></div>
<h3 class="font-outfit font-20 lineh-28 weight-600 color-17 margin-t">{q['q']}</h3>
<p class="font-outfit font-16 lineh-26 weight-400 color-17 margin-b24 margin-t">{q['a']}</p><div class="border-4 margin-b24"></div>
<div class="mans-author"><div class="names-text"><p class="font-14 weight-600 color-15 font-outfit">{FAQ_GROUPS[g]['title']}</p></div></div></div>''')
    return f'''<div class="testimonial2-scetion-area section-padding5" id="faq">
<img src="/assets/images/elementor/elementor8.png" alt="" class="elementor-5 aniamtion-key-1">
<div class="container"><div class="row"><div class="col-lg-12" data-aos="fade-down" data-aos-duration="800"><div class="testimonial2-header text-center margin-b60">
{tag('FAQs')}<h2 class="font-outfit font-44 weight-600 lineh-52 color-17">Frequently Asked Questions</h2>
<p class="font-outfit font-16 lineh-26 color-15 margin-t">Straight answers about formation, EIN filing and registered agent service.</p></div></div></div>
<div class="row"><div class="col-lg-12" data-aos="fade-down" data-aos-duration="1200"><div class="testomonial2-carousel-area owl-carousel">{''.join(items)}</div></div></div>
<div class="row"><div class="col-lg-12 text-center">{btn('/faqs/','View all FAQs')}</div></div></div></div>'''

GUIDES=[
 ('how-to-form-a-florida-llc-from-any-state','LLC Formation','How to Form a Florida LLC From Any State','A Florida LLC can be formed by an owner who lives in any state. This guide explains the requirements, the state filing fee, the registered agent rule, and the steps from name search to EIN.','founder-laptop-1','Florida LLC formation guide'),
 ('florida-annual-report-deadline-cost-late-fees','Compliance','Florida Annual Report: Deadline, Cost and Late Fees','Every Florida LLC must file an annual report between January 1 and May 1. This guide explains the deadline, the state fee, the $400 late fee, and what happens if the report is not filed.','signing-documents-1','annual report guide'),
 ('what-a-florida-registered-agent-does','Registered Agent','What a Florida Registered Agent Does and Why You Need One','Every Florida LLC must maintain a registered agent and registered office in Florida. This guide explains who can serve, what the agent does, and how to choose a reliable provider.','mailbox-1','registered agent guide'),
]

def blog_section(heading_tag='Guides', h='Florida Business Formation Guides'):
    g0=GUIDES[0]
    side=''
    for i,g in enumerate(GUIDES[1:]):
        side+=f'''<div class="blog-auhtor2-text {'margin-b30' if i==0 else ''}" data-aos="zoom-in" data-aos-duration="{1200+200*i}"><div class="blog2-ahtuor2">
<div class="blog-date-list margin-b"><img src="/assets/images/icons/daterane.png" alt="" class="ts" width="20" height="20"><span class="font-16 lineh-16 font-outfit weight-500 color-17 ts">October 20, 2026 &middot; {g[1]}</span></div>
<a href="/blog/{g[0]}/"><h3 class="font-20 font-outfit color-17 lineh-28 weight-600 margin-b14 ts">{g[2]}</h3></a>
<p class="font-16 font-outfit lineh-26 weight-400 color-17 margin-b24 ts">{g[3]}</p>
<a href="/blog/{g[0]}/" class="font-16 font-outfit weight-700 color-17 ts lineh-26 text-uppercase d-inline-block learn-more">Read the {g[5]} {ARROW}</a></div></div>'''
    return f'''<div class="blog2-scetion-area section-padding5" id="blog"><div class="container">
<div class="row"><div class="col-lg-12" data-aos="fade-down" data-aos-duration="800"><div class="blog2-textarea text-center margin-b60">{tag(heading_tag)}<h2 class="font-outfit font-44 weight-600 lineh-52 color-17">{h}</h2></div></div></div>
<div class="row align-items-center">
<div class="col-lg-6" data-aos="zoom-out" data-aos-duration="1000"><div class="blog2-author-area"><div class="blog2-images">{img(g0[4],'Founder working on a laptop',cls='ds-cover ds-blog-big')}</div>
<div class="blog-auhtor2-text blog2-author-poition" data-aos="zoom-out" data-aos-duration="1400"><div class="blog2-ahtuor2 blog-2ahthor">
<div class="blog-date-list margin-b"><img src="/assets/images/icons/daterange1.png" alt="" width="20" height="20"><span class="font-16 lineh-16 font-outfit weight-500 color ts">October 20, 2026 &middot; {g0[1]}</span></div>
<a href="/blog/{g0[0]}/" class="ts"><h3 class="font-20 font-outfit color lineh-28 weight-600 margin-b ts">{g0[2]}</h3></a>
<p class="font-16 font-outfit lineh-26 weight-400 color ts">{g0[3]}</p>
<a href="/blog/{g0[0]}/" class="font-16 font-outfit weight-700 color lineh-26 text-uppercase margin-t32 d-inline-block learn-more learn-more1 ts">Read the {g0[5]} {ARROW}</a></div></div></div></div>
<div class="col-lg-6">{side}</div></div></div></div>'''

SERVICE_OPTS=['LLC Formation','EIN Filing','Registered Agent','Formation Bundle (LLC, State Fee, EIN)','Annual Report','DBA (Fictitious Name)','Amendment','Reinstatement','Other or not sure']

def contact_section(h_tag='Contact Us', h='Let\u2019s talk about your business'):
    opts=''.join(f'<option value="{o}">{o}</option>' for o in SERVICE_OPTS)
    return f'''<div class="contact2-section-area section-padding5" id="contact">
<img src="/assets/images/elementor/elementor8.png" alt="" class="elementor14 aniamtion-key-1">
<div class="container"><div class="row"><div class="col-lg-12" data-aos="fade-down" data-aos-duration="800"><div class="contact2-header text-center margin-b60">{tag(h_tag)}<h2 class="font-outfit font-44 weight-600 lineh-52 color-17">{h}</h2></div></div></div>
<div class="col-lg-12" data-aos="fade-right" data-aos-duration="1000"><div class="contact2-all-contact"><div class="row align-items-center">
<div class="col-lg-6"><div class="contact2-maincontact">
<h3 class="font-24 font-outfit lineh-24 color-17 weight-600 margin-b">Order or Request Information</h3>
<p class="font-16 font-outfit lineh-26 weight-400 color-15 margin-b24">Describe the service required, and Diler Services will respond with a checklist.</p>
<form class="contact-from-area diler-form" method="POST" action="https://api.web3forms.com/submit">
<input type="hidden" name="access_key" value="{KEY}"><input type="hidden" name="subject" value="New website inquiry: Diler Services"><input type="hidden" name="from_name" value="Diler Services Website">
<input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off">
<div class="row">
<div class="col-lg-6"><div class="first-input"><label class="visually-hidden" for="cf-name">Full name</label><input id="cf-name" type="text" name="Name" placeholder="Full name *" required autocomplete="name"></div></div>
<div class="col-lg-6"><div class="first-input"><label class="visually-hidden" for="cf-email">Email address</label><input id="cf-email" type="email" name="Email" placeholder="Email address *" required autocomplete="email"></div></div>
<div class="col-lg-12"><div class="first-input"><label class="visually-hidden" for="cf-biz">Business name</label><input id="cf-biz" type="text" name="Business name" placeholder="Business name" autocomplete="organization"></div></div>
<div class="col-lg-12"><div class="first-input"><div class="first-name-input"><label class="visually-hidden" for="cf-service">Service</label><select id="cf-service" name="Service" class="country-area nice-select6" required>{opts}</select></div></div></div>
<div class="col-lg-12"><div class="textarea"><label class="visually-hidden" for="cf-msg">Message</label><textarea id="cf-msg" name="Message" cols="30" rows="6" placeholder="Message *" required></textarea></div></div>
<div class="col-lg-12"><div class="dzFormMsg" role="status"></div><div class="theme-btn4 margin-t32 margn-left"><button type="submit" class="theme-btn5 font-outfit font-16 weight-700">Submit Request {ARROW}</button></div>
<p class="font-14 color-15 margin-t">{DISC}</p></div>
</div></form></div></div>
<div class="col-lg-6">
<div class="contact-padding" data-aos="fade-right" data-aos-duration="1000"><div class="contact2-auhtor-section"><div class="clock-area"><img src="/assets/images/icons/email3.svg" alt="" width="32" height="32"></div>
<div class="contact-location"><h3 class="font-20 font-outfit lineh-24 color-17 weight-600 margin-b">Send a message</h3><p class="font-outfit font-16 lineh-26 color-17 weight-400"><a href="mailto:{EMAIL}" class="color-17">{EMAIL}</a></p></div></div></div>
<div class="contact-padding margin-t" data-aos="fade-right" data-aos-duration="1200"><div class="contact2-auhtor-section contact-phonr-bg"><div class="clock-area"><img src="/assets/images/icons/clock1.svg" alt="" width="32" height="32"></div>
<div class="contact-location"><h3 class="font-20 font-outfit lineh-24 color weight-600 margin-b">Response by email</h3><p class="font-outfit font-16 lineh-26 color weight-400">Diler Services responds to every inquiry by email.</p></div></div></div>
</div></div></div></div></div>
<img src="/assets/images/elementor/elementor12.png" class="elementor13" alt=""></div>'''

def cta_section():
    return f'''<div class="cta2-section-area section-padding7"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="fade-right" data-aos-duration="1000"><div class="cta2-textarea"><h2 class="font-outfit font-44 lineh-52 color weight-600 margin-b">Have a Question Before You Order?</h2>
<p class="font-outfit font-16 lineh-26 weight-400 color">Leave your email and Diler Services will reply by email. LLC formation is $89 plus the $125 Florida state fee at cost.</p></div></div>
<div class="col-lg-2"></div>
<div class="col-lg-4" data-aos="fade-left" data-aos-duration="1000"><div class="cta2-from-area">
<form class="diler-form" method="POST" action="https://api.web3forms.com/submit"><input type="hidden" name="access_key" value="{KEY}"><input type="hidden" name="subject" value="Question from the website: Diler Services"><input type="hidden" name="from_name" value="Diler Services Website"><input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off">
<div class="input1-area"><label class="visually-hidden" for="cta-email">Email address</label><input id="cta-email" type="email" name="Email" placeholder="Email address" required autocomplete="email"></div>
<div class="theme5-btn"><button type="submit" class="font-16 weight-700 lineh-16 color font-outfit">Ask a question {ARROW}</button></div>
<div class="dzFormMsg" role="status"></div></form></div></div>
</div></div><img src="/assets/images/elementor/elementor13.png" alt="" class="elementor-13"></div>'''

def footer():
    svc=''.join(f'<li><a href="/order/?service={s[0]}#order" class="font-outfit font-16 color-21 lineh-16 weight-400 {"margin-t d-inline-block" if i else ""}">{s[1]}</a></li>' for i,s in enumerate(SERVICES[:6]))
    links=[('/about/','About Us'),('/why-diler-services/','Why Diler Services'),('/services/','Our Services'),('/faqs/','FAQs'),('/blog/','Guides'),('/contact/','Contact')]
    ll=''.join(f'<li><a href="{h}" class="font-outfit font-16 color-21 lineh-16 weight-400 {"margin-t d-inline-block" if i else ""}">{t}</a></li>' for i,(h,t) in enumerate(links))
    return f'''<footer class="footer2-section-area"><div class="container"><div class="row"><div class="col-lg-12"><div class="footer-all-padding section-padding5"><div class="row">
<div class="col-lg-4"><div class="footer-logo2"><a href="/" aria-label="Diler Services home">{LOGO}</a>
<p class="font-16 lineh-26 color weight-400 font-outfit margin-b24 margin-t">Florida LLC formation, EIN filing and registered agent service for business owners nationwide. Flat published prices, state fees at cost.</p>
{btn(CTA,'Start your LLC','ds-foot-btn')}</div></div>
<div class="col-lg-2 col-md-6"><div class="our-service-area"><h2 class="font-20 color-21 lineh-20 font-outfit margin-b24 weight-600">Our services</h2><div class="servicefooter-list"><ul>{svc}</ul></div></div></div>
<div class="col-lg-1"></div>
<div class="col-lg-2 col-md-6"><div class="our-service-area"><h2 class="font-20 color-21 lineh-20 font-outfit margin-b24 weight-600">Useful Links</h2><div class="servicefooter-list"><ul>{ll}</ul></div></div></div>
<div class="col-lg-3 col-md-6"><div class="contact-footer"><h2 class="font-20 color-21 lineh-20 font-outfit margin-b24 weight-600">Contact Us</h2>
<div class="email4"><img src="/assets/images/icons/email4.svg" alt="" width="20" height="20"><a href="mailto:{EMAIL}" class="font-16 lineh-24 color-21 weight-400 font-outfit">{EMAIL}</a></div>
<div class="email4 margin-t"><img src="/assets/images/icons/location3.svg" alt="" width="20" height="20"><span class="font-16 lineh-24 color-21 weight-400 font-outfit">Serving business owners in every state</span></div>
</div></div>
</div></div></div></div></div>
<div class="border-10"></div>
<div class="copyright"><div class="row"><div class="col-lg-12 text-center"><div class="copyright1">
<p class="font-outfit font-16 lineh-26 weight-500 ds-disclaimer">{DISC}</p>
<p class="font-outfit font-14 lineh-26 weight-400">&copy; 2026 Diler Services LLC. All rights reserved. <a href="/privacy-policy/">Privacy Policy</a> &middot; <a href="/terms-of-service/">Terms of Service</a> &middot; <a href="/refund-policy/">Refund Policy</a></p>
</div></div></div></div>
<img src="/assets/images/elementor/elementor14.png" alt="" class="elementor-14"></footer>
<div class="ds-sticky d-lg-none"><a href="{CTA}" class="theme-btn5 font-outfit font-16 weight-700">Start your LLC {ARROW}</a></div>
'''

SCRIPTS='''<script src="/assets/js/plugins/jquery-3-6-0.min.js" defer></script>
<script src="/assets/js/plugins/jquery.waypoints.min.js" defer></script>
<script src="/assets/js/plugins/owl.carousel.min.js" defer></script>
<script src="/assets/js/plugins/counter.js" defer></script>
<script src="/assets/js/plugins/aos.js" defer></script>
<script src="/assets/js/plugins/jquery.nice-select.js" defer></script>
<script src="/assets/js/plugins/mobilemenu.js" defer></script>
<script src="/assets/js/diler.js" defer></script>
'''

def page(path, title, desc, body, extra_head='', extra_js=''):
    doc=head(title,desc,path,extra_head).replace('<body>','<body class="ds-inner">' if path!='/' else '<body>')+header(path)+'<main>'+body+'</main>'+footer()+SCRIPTS+extra_js+'</body></html>'
    if path.endswith('.html'):
        fn=os.path.join(OUT,path.strip('/'))
    else:
        d=os.path.join(OUT, path.strip('/')); os.makedirs(d,exist_ok=True); fn=os.path.join(d,'index.html')
    open(fn,'w').write(doc)

# ---------- prose extraction from Proposal A ----------
ALLOWED={'h1','h2','h3','h4','p','ul','ol','li','a','strong','em','b','i','table','thead','tbody','tr','th','td','blockquote','br'}
def clean(fragment):
    fragment=re.sub(r'<(script|style|svg|form|button|img|picture|figure)[^>]*>.*?</\1>','',fragment,flags=re.S)
    fragment=re.sub(r'<(img|input|source)[^>]*>','',fragment)
    def rep(m):
        close,tagn,attrs=m.group(1),m.group(2).lower(),m.group(3)
        if tagn not in ALLOWED: return ''
        if close: return f'</{tagn}>'
        if tagn=='a':
            h=re.search(r'href="([^"]*)"',attrs)
            return f'<a href="{h.group(1) if h else "#"}">'
        return f'<{tagn}>'
    out=re.sub(r'<(/?)([a-zA-Z0-9]+)([^>]*)>',rep,fragment)
    out=re.sub(r'<(p|li|h2|h3|h4|a|strong)>\s*</\1>','',out)
    out=re.sub(r'\n\s*\n+','\n',out)
    return out.strip()

def main_of(rel):
    s=open(os.path.join(PLX,rel)).read()
    return re.search(r'<main[^>]*>(.*)</main>',s,re.S).group(1)

def article(rel):
    m=main_of(rel)
    # prefer <article>
    a=re.search(r'<article[^>]*>(.*?)</article>',m,re.S)
    frag=a.group(1) if a else m
    c=clean(frag)
    h1=re.search(r'<h1>(.*?)</h1>',c,re.S)
    t=re.sub(r'<[^>]+>','',h1.group(1)).strip() if h1 else ''
    c=re.sub(r'<h1>.*?</h1>','',c,count=1,flags=re.S)
    return t,c

def prose_section(c, side=None):
    aside = f'<div class="col-lg-4"><div class="ds-aside" data-aos="fade-left" data-aos-duration="1000">{side}</div></div>' if side else ''
    col='col-lg-8' if side else 'col-lg-9 mx-auto'
    return f'<div class="ds-prose-area section-padding5"><div class="container"><div class="row"><div class="{col}"><div class="ds-prose">{c}</div></div>{aside}</div></div></div>'

ASIDE=f'''<h3 class="font-outfit font-24 weight-600 color-17 margin-b">Start your Florida LLC</h3>
<p class="font-16 lineh-26 color-15">LLC formation is $89 plus the $125 Florida state fee at cost. Submitted within 1 business day of complete information.</p>
{btn(CTA,'Start your LLC')}
<div class="ds-aside-links"><h4 class="font-outfit font-20 weight-600 color-17 margin-t32 margin-b">Guides</h4><ul>'''+''.join(f'<li><a href="/blog/{g[0]}/">{g[2]}</a></li>' for g in GUIDES)+'</ul></div>'

# ================= HOME =================
def faq_schema(items):
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q['q'],"acceptedAnswer":{"@type":"Answer","text":q['a']}} for q in items]})+'</script>'

ORG='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"ProfessionalService","name":"Diler Services LLC","url":SITE,"email":EMAIL,"areaServed":"US","description":"Florida LLC formation, EIN filing and registered agent service for business owners nationwide."})+'</script>'

hero=f'''<div class="welcome2-section-area"><div class="container"><div class="row align-items-center">
<div class="col-lg-5"><div class="welcome2-textarea">
{tag('Start Your Business the Right Way','margin-b24')}
<h1 class="font-outfit font-56 weight-600 lineh-64 color-17 margin-b18 ds-hero-h1">Form Your Florida LLC <span class="succes">From Any State</span></h1>
<p class="font-16 lineh-26 color-17 weight-400 font-outfit">Diler Services provides Florida LLC formation for business owners nationwide, with clear flat pricing, state fees at cost, and submission within 1 business day of complete information.</p>
<div class="theme-btn4 margin-t32 d-inline-block margn-left"><a href="{CTA}" class="theme-btn5 font-outfit font-16 weight-700">Start your LLC {ARROW}</a></div>
</div></div>
<div class="col-lg-1"></div>
<div class="col-lg-6"><div class="welcome2-images-area"><div class="welcome-imgs-area"><div class="main-img">
{img('consultation-1','Business owner reviewing formation documents with an advisor',cls='main-imgs ds-cover ds-hero-img',lazy=False,attrs='width="1200" height="800"')}
<div class="ecommer aniamtion-key-2 ds-price-card"><p class="ds-pc-t">Formation</p><p class="ds-pc-p">$89</p><p class="ds-pc-n">plus the $125 Florida state fee at cost</p></div>
</div>
<img src="/assets/images/elementor/elementor7.png" alt="" class="elementor-8 aniamtion-key-1"><img src="/assets/images/elementor/elementor8.png" alt="" class="elementor9 aniamtion-key-2">
</div></div></div>
</div></div><img src="/assets/images/elementor/elementor6.png" alt="" class="elementor-6"></div>'''

about=f'''<div class="about2-section-area section-padding5" id="about"><div class="container"><div class="row align-items-center">
<div class="col-lg-6"><div class="about2-author-images">
<div class="about2-scetion-images" data-aos="zoom-out" data-aos-duration="1200">{img('signing-documents-2','Signing business formation documents',cls='ds-cover ds-ab-main')}</div>
<div class="row"><div class="col-6" data-aos="fade-up" data-aos-duration="1400"><div class="about-2-authr1">{img('founder-laptop-2','Founder working on a laptop',cls='ds-cover ds-ab-small')}</div></div>
<div class="col-6" data-aos="fade-up" data-aos-duration="1600"><div class="about-2-authr1">{img('florida-skyline-palms-1','Florida skyline with palm trees',cls='ds-cover ds-ab-small')}</div></div></div>
</div></div>
<div class="col-lg-6" data-aos="fade-left" data-aos-duration="800"><div class="about-2-textarea">
{tag('About Us')}
<h2 class="font-outfit font-44 weight-600 lineh-52 color-17 margin-b20" data-aos="fade-left" data-aos-duration="1000">A Business Formation Partner Built on Clear Standards</h2>
<div class="pera-background" data-aos="fade-left" data-aos-duration="1200"><p class="font-outfit font-16 lineh-26 color-17 weight-500">Diler Services prepares and files LLC paperwork, obtains EINs, and serves as registered agent.</p></div>
<p class="font-outfit font-16 lineh-26 colorp weight-400">Every engagement includes flat published pricing, state fees at cost, and direct, professional communication.</p>
<ul class="ds-ticks"><li>Clear flat pricing</li><li>Fast submission</li><li>Client centered service</li><li>Organized records</li></ul>
<div class="theme-btn4 margin-t32 d-inline-block margn-left" data-aos="fade-up" data-aos-duration="1400"><a href="/about/" class="theme-btn5 font-outfit font-16 weight-700">More about us {ARROW}</a></div>
</div></div></div></div></div>'''

company=f'''<div class="company-section-area section-padding5"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="fade-left" data-aos-duration="800"><div class="company-progress-area">
{tag('Transparent Pricing')}
<h2 class="font-outfit font-44 weight-600 lineh-52 color-17 margin-b20">One flat formation fee. The state fee at cost.</h2>
<p class="margin-b8">LLC formation is a $89 service fee plus the $125 Florida state fee, passed through at cost. The formation bundle with EIN filing totals $299.</p>
<div class="progress7 margin-b12"><div class="bussibess-plan"><span class="font-16 font-outfit lineh-16 color-17 weight-500 international1">Diler Services formation fee</span><p class="font-16 font-outfit lineh-16 color-17 weight-500">$89</p></div>
<div class="progress-wrap3 progress3" data-progress-percent="79"><div class="progress-bar3 progress3"></div></div></div>
<div class="bussibess-plan"><span class="font-16 font-outfit lineh-16 color-17 weight-500 international1">Florida state fee, at cost</span><p class="font-16 font-outfit lineh-16 color-17 weight-500">$125</p></div>
<div class="progress-wrap3 progress3" data-progress-percent="21"><div class="progress-bar3 progress3"></div></div>
<div class="theme-btn4 margin-t32 d-inline-block margn-left service-center" data-aos="fade-left" data-aos-duration="1200"><a href="{CTA}" class="theme-btn5 font-outfit font-16 weight-700 margin-b12">Start your LLC {ARROW}</a></div>
</div></div>
<div class="col-lg-6" data-aos="zoom-out" data-aos-duration="1000"><div class="company-images">{img('office-bright-2','Bright modern office',cls='ds-cover ds-company')}</div></div>
</div></div></div>'''

def counters():
    C=[('','1','','Business day to submit'),('$','89','','Formation service fee'),('$','125','','Florida state fee at cost'),('','8','','Filing services')]
    out=''
    for i,(pre,n,suf,l) in enumerate(C):
        out+=f'<div class="col-lg-3 col-md-6" data-aos="zoom-in" data-aos-duration="{800+200*i}"><div class="countre2-boxarea text-center"><div class="counter-box"><p class="font-outfit font-44 lineh-52 color-17 weight-600 ds-count">{pre}<span class="counter">{n}</span>{suf}</p><p class="font-outfit font-16 lineh-16 color-15 weight-400 margin-t">{l}</p></div></div></div>'
    return f'<div class="counter2-section-area"><img src="/assets/images/elementor/elementor10.png" alt="" class="elementor-10"><div class="container"><div class="row">{out}</div></div><img src="/assets/images/elementor/elementor8.png" alt="" class="elementor-3 aniamtion-key-2"></div>'

STEPS=[('client1.svg','01 Send Your Information','Tell us your business name, owners or managers, and mailing address.'),
       ('client2.svg','02 Document Preparation','Diler Services prepares the Articles of Organization for the State of Florida.'),
       ('client3.svg','03 Filing With the State','Diler Services submits within 1 business day of receiving complete information.'),
       ('client1.svg','04 Confirmation','The client receives the state confirmation and, if ordered, the EIN letter.')]
def steps_section(h='From order to state confirmation, in four clear steps.', steps=STEPS):
    boxes=''.join(f'''<div class="animationdiv" data-aos="fade-left" data-aos-duration="{1000+200*i}"><div class="client-author-area {'margin-b30' if i<len(steps)-1 else ''}"><div class="client-icon"><img src="/assets/images/icons/{ic}" alt="" width="40" height="40"></div>
<div class="client-main-pera"><h3 class="font-24 lineh-26 weight-600 font-outfit color-17 margin-b14">{t}</h3><p class="font-outfit font-16 lineh-26 weight-400 color-22">{d}</p></div></div></div>''' for i,(ic,t,d) in enumerate(steps))
    return f'''<div class="client-section-area section-padding5" id="how"><div class="container"><div class="row align-items-center">
<div class="col-lg-6">{boxes}</div>
<div class="col-lg-6" data-aos="fade-right" data-aos-duration="1000"><div class="works-text-area">{tag('How It Works')}
<h2 class="font-outfit font-44 weight-600 lineh-52 color-17 margin-b24">{h}</h2>
<p class="font-outfit font-16 lineh-26 weight-400 color-17 margin-b">Submit the request form with the service required, and Diler Services will respond with a concise checklist.</p>
<p class="font-outfit font-16 lineh-26 weight-400 color-17 margin-b">If the state rejects the business name, Diler Services refiles at no additional service fee. Legal and tax questions are referred to a licensed attorney or CPA.</p>
{btn(CTA,'Start your LLC')}</div></div></div></div></div>'''

WHY=[('Clear flat pricing','Every service has a published flat fee.','State fees are passed through at cost, without markup.','office-plants-1'),
     ('1-business-day submission','Filings are submitted within 1 business day of complete information.','If not, the $89 formation service fee is refunded.','founder-laptop-3'),
     ('Free name refile','If the State of Florida rejects the requested name, Diler Services refiles.','There is no additional service fee for the refile.','miami-shore-skyline-2')]
def why_section():
    cards=''.join(f'''<div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-duration="{1000+200*i}"><div class="single-portfolio singlecase"><div class="portfolio-images singleportfolio">{img(im,t,cls='ds-cover ds-case')}</div>
<div class="portfolio-textarea"><h3 class="font-24 weight-600 font-outfit lineh-28 color-17 margin-b14"><a href="/why-diler-services/" class="color-17">{t}</a></h3><p class="font-outfit weight-400 color-17 lineh-26 font-16">{a}</p>
<div class="portfolio-visible-textarea margin-t"><p class="font-outfit weight-400 color-17 lineh-26 font-16">{b}</p><a href="/why-diler-services/" class="font-16 font-outfit weight-700 color lineh-26 ts text-uppercase margin-t30 d-inline-block learn-more1 learn-more">More on {t.lower()} {ARROW}</a></div></div></div></div>''' for i,(t,a,b,im) in enumerate(WHY))
    return f'''<div class="case-study-scetion-area section-padding8" id="why"><img src="/assets/images/elementor/elementor8.png" alt="" class="elementor-5 aniamtion-key-1"><div class="container">
<div class="row"><div class="col-lg-12" data-aos="fade-down" data-aos-duration="800"><div class="case-study-header text-center margin-b60">{tag('Why Diler Services')}<h2 class="font-outfit font-44 weight-600 lineh-52 color-17">Clear commitments on every filing</h2></div></div></div>
<div class="row">{cards}</div></div><img src="/assets/images/elementor/elementor11.png" alt="" class="elementor-11"></div>'''

allfaq=[q for g in FAQ_GROUPS for q in g['items']]
home_body=hero+about+services_section('Our Services','Business Formation Services To Start and Protect Your Company',SERVICES[:6])+company+counters()+steps_section()+why_section()+pricing_section()+faq_carousel()+blog_section()+contact_section()+cta_section()
page('/', 'Florida LLC Formation From Any State | Diler Services', 'Form your Florida LLC from any state. $89 service fee plus the $125 Florida state fee at cost, EIN filing and registered agent service. Submitted within 1 business day.', home_body, ORG+faq_schema([FAQ_GROUPS[g]['items'][i] for g,i in [(0,1),(0,2),(1,0),(1,3),(2,2),(3,2)]]))

