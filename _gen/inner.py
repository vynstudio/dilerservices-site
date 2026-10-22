exec(open('/workspace/consult/gen/build_head.py').read())
BS='<script src="/assets/js/plugins/bootstrap.min.js" defer></script>'
AR='<span><i class="fa-solid fa-arrow-right"></i></span>'
def b6(href,text,extra='',dark=False):
    return f'<a href="{href}" class="theme6-btn6 font-ks lineh-16 weight-700 color font-16 {extra}">{text} {AR}</a>'
def span3(t): return f'<span class="about3span font-ks lineh-16 font-16 weight-600 color-29 d-inline-block margin-b24">{t}</span>'
CHECK='<span><img src="/assets/images/icons/check1.png" alt="" width="20" height="20"></span>'

def cta5():
    return f'''<div class="cta5-section-area section-padding4"><img src="/assets/images/elementor/elementor72.png" alt="" class="elementors72"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="fade-right" data-aos-duration="1000"><div class="cta5-auhtor6-area"><h2 class="font-lora font-48 lineh-52 color weight-600 margin-b">Start Your Business With a Clear, Flat Price.</h2>
<p class="font-ks font-16 lineh-26 weight-500 color-21">LLC formation is $89 plus the $125 Florida state fee at cost. Questions first? Diler Services replies by email.</p></div></div>
<div class="col-lg-2"></div>
<div class="col-lg-4" data-aos="fade-left" data-aos-duration="1000"><div class="cta5-btn5-sexction">
<a href="{CTA}" class="theme6-btn6 bakgrnd5 font-ks lineh-16 weight-700 color font-16">Start your LLC {AR}</a>
<a href="/contact/" class="theme6-btn6 backgrnd6 font-ks lineh-16 weight-700 color-29 font-16">Ask a question {AR}</a></div></div>
</div></div><img src="/assets/images/elementor/elementor72.png" alt="" class="elementors73"></div>'''

def faq_two_col(items, title='Frequently Asked Questions', uid='a', heading_tag='h2', bg=''):
    half=(len(items)+1)//2
    def col(its,off):
        out=''
        for j,q in enumerate(its):
            n=f'{uid}{off+j}'; first=(j==0)
            out+=f'''<div class="accordion-item borderlefts {'m-0' if j==len(its)-1 else ''}"><h3 class="accordion-header"><button class="accordion-button {'' if first else 'collapsed'}" type="button" data-bs-toggle="collapse" data-bs-target="#c{n}" aria-expanded="{'true' if first else 'false'}" aria-controls="c{n}">{q['q']}</button></h3>
<div id="c{n}" class="accordion-collapse collapse {'show' if first else ''}" data-bs-parent="#acc{uid}{off}"><div class="accordion-body"><p class="font-ks font-16 lineh-26 weight-500 color-30">{q['a']}</p></div></div></div>'''
        return f'<div class="accordion accordian4" id="acc{uid}{off}">{out}</div>'
    head=f'<div class="row"><div class="col-lg-7 m-auto"><div class="faq-textarea margin-b60 text-center" data-aos="fade-down" data-aos-duration="800"><{heading_tag} class="font-lora font-48 lineh-52 color-29 weight-600 margin-b">{title}</{heading_tag}></div></div></div>' if title else ''
    return f'''<div class="faq-section-area section-padding5 {bg}"><img src="/assets/images/elementor/elementor23.png" alt="" class="elementor24"><div class="container">{head}
<div class="row"><div class="col-lg-12"><div class="accordian-area accourbutton"><div class="row">
<div class="col-lg-6" data-aos="fade-up" data-aos-duration="900">{col(items[:half],0)}</div><div class="col-lg-6" data-aos="fade-up" data-aos-duration="1100">{col(items[half:],100)}</div>
</div></div></div></div></div><img src="/assets/images/elementor/elementor23.png" alt="" class="elementor25"></div>'''

def email_help():
    return f'''<div class="needed-section"><h2 class="font-lora font-24 lineh-30 weight-600 color-29 margin-b24">Questions? Email Diler Services</h2><a href="mailto:{EMAIL}" class="font-16 weight-700 color fon-ks lineh-16"><img src="/assets/images/icons/email4.svg" alt="" width="20" height="20"> {EMAIL}</a></div>'''

def quote_form(subject='Question from a service page'):
    return f'''<div class="quito-contact"><h2 class="font-24 lineh-24 weight-600 color-29 font-lora margin-b20">Ask a Question</h2>
<form class="diler-form" method="POST" action="https://api.web3forms.com/submit"><input type="hidden" name="access_key" value="{KEY}"><input type="hidden" name="subject" value="{subject}: Diler Services"><input type="hidden" name="from_name" value="Diler Services Website"><input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off">
<div class="quitoinput"><label class="visually-hidden" for="q-name">Your name</label><input id="q-name" type="text" name="Name" placeholder="Your name" required autocomplete="name"></div>
<div class="quitoinput"><label class="visually-hidden" for="q-email">Email address</label><input id="q-email" type="email" name="Email" placeholder="Email address" required autocomplete="email"></div>
<div class="quitoinput"><label class="visually-hidden" for="q-msg">Your question</label><textarea id="q-msg" name="Message" rows="5" placeholder="Your question" required></textarea></div>
<button type="submit" class="quitobtn font-ks font-16 lineh-16 weight-700 color">Send question {AR}</button><div class="dzFormMsg" role="status"></div></form></div>'''

def services_sidebar(active):
    links=''.join(f'<div class="singlepalnning-area margin-b20 {"ds-on" if s[0]==active else ""}"><a href="{s[6]}" class="font-18 font-ks lineh-18 weight-600 color-29 ts">{s[1]}</a><span><i class="fa-solid fa-angle-right ts"></i></span></div>' for s in SERVICES)
    return f'<div class="serviceour-area"><h2 class="font-lora font-24 lineh-24 weight-600 color-29 margin-b24">Our Services</h2>{links}</div>'+email_help()+quote_form()

# ================= ABOUT (about.html) =================
def fact_boxes():
    F=[('','1','','Business day to submit'),('$','89','','Formation service fee'),('$','125','','Florida state fee at cost'),('','8','','Filing services')]
    out=''
    for i,(p,n,u,l) in enumerate(F):
        cls='margin-b20 margin-t32' if i<2 else ''
        out+=f'<div class="col-lg-6 col-md-6 col-6"><div class="counter3-boxarea4 text-center {cls}"><div class="counter4-boxarea4"><p class="font-lora font-40 lineh-40 color-29 margin-b weight-600 ds-count">{p}<span class="counter">{n}</span>{u}</p><p class="font-ks font-16 lineh-16 weight-500 color-30">{l}</p></div></div></div>'
    return f'<div class="counter3-area3"><div class="row">{out}</div></div>'

about3=f'''<div class="about3-section-area section-padding5"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="zoom-out" data-aos-duration="1000"><div class="about3-images1">{img('consultation-2','Formation consultation at a desk',cls='ds-cover ds-about3')}<img src="/assets/images/elementor/elementor17.png" alt="" class="elementor-9 keyframe3"></div></div>
<div class="col-lg-6" data-aos="fade-left" data-aos-duration="1000"><div class="about3-textarea1">{span3('About Us')}
<h2 class="font-lora font-48 lineh-56 weight-600 color-29 margin-b20">Precise Filings. Clear Pricing. Reliable Service.</h2>
<p class="font-ks font-16 lineh-26 weight-500 color-30">Diler Services LLC provides Florida LLC formation, EIN filing and registered agent service to business owners nationwide. Every engagement follows the same standard: flat published prices, state fees at cost, and precise, timely communication.</p>
{fact_boxes()}
{b6(CTA,'Start your LLC','margin-t32')}</div></div></div></div></div>'''

def lawprovide(h, paras, boxes, btn_html):
    icons=['gudeiance1.svg','consulting1.svg','support1.svg']
    bx=''.join(f'''<div class="lawprovide-boaxrea {'margin-b30' if i<len(boxes)-1 else ''}" data-aos="fade-left" data-aos-duration="{900+200*i}"><div class="guidiance-boxarea"><img src="/assets/images/icons/{icons[i%3]}" alt="" class="ts" width="40" height="40"></div>
<div class="lax-conultingprovide"><a href="{hr}" class="color-29"><h3 class="font-lora font-24 lineh-28 weight-600 color-29 margin-b14 ts">{t}</h3></a><p class="font-ks lineh-26 weight-500 color-30 font-16 ts">{d}</p></div></div>''' for i,(t,d,hr) in enumerate(boxes))
    ps=''.join(f'<p class="font-ks font-16 weight-500 lineh-26 margin-b20 color-30">{p}</p>' for p in paras)
    return f'''<div class="lawprovide-section-area section-padding5"><img src="/assets/images/elementor/elementor23.png" alt="" class="elementor24"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="fade-right" data-aos-duration="1000"><div class="lawprovide-textarea"><h2 class="font-lora font-48 lineh-56 weight-600 color-29 margin-b20">{h}</h2>{ps}{btn_html}</div></div>
<div class="col-lg-6">{bx}</div></div></div><img src="/assets/images/elementor/elementor23.png" alt="" class="elementor25"></div>'''

def mission(h, paras, items, im, alt, btn_html, reverse=False):
    lis=''.join(f'<li class="font-ks font-16 lineh-22 weight-600 color-17 {"margin-b20" if i<len(items)-1 else ""}">{CHECK}{t}</li>' for i,t in enumerate(items))
    ps=''.join(f'<p class="font-ks font-16 lineh-26 weight-500 color-30 margin-b">{p}</p>' for p in paras)
    return f'''<div class="mission-area-starts section-padding5"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="zoom-out" data-aos-duration="1000"><div class="missionimg">{img(im,alt,cls='missionimg2 ds-cover ds-mission')}<img src="/assets/images/elementor/elementor17.png" alt="" class="elementor-9 keyframe3"></div></div>
<div class="col-lg-6" data-aos="fade-left" data-aos-duration="1000"><div class="missiontextarea"><h2 class="font-lora font-48 lineh-56 weight-600 color-29 margin-b20">{h}</h2>{ps}<ul>{lis}</ul>{btn_html}</div></div>
</div></div></div>'''

def vission(h, intro, tabs, im, alt, btn_html):
    nav=''.join(f'<li class="nav-item" role="presentation"><button class="nav-link {"active" if i==0 else ""} nav-btn1" id="t{i}-tab" data-bs-toggle="pill" data-bs-target="#t{i}" type="button" role="tab" aria-controls="t{i}" aria-selected="{"true" if i==0 else "false"}">{t}</button></li>' for i,(t,_) in enumerate(tabs))
    panes=''.join(f'<div class="tab-pane fade {"show active" if i==0 else ""}" id="t{i}" role="tabpanel" aria-labelledby="t{i}-tab" tabindex="0">'+''.join(f'<p class="font-ks font-16 weight-500 lineh-26 margin-b20 color-30"><span class="weight-700 color-29">{a}</span> {b}</p>' for a,b in ps)+'</div>' for i,(_,ps) in enumerate(tabs))
    return f'''<div class="vission-section-area section-padding5"><img src="/assets/images/elementor/elementor23.png" alt="" class="elementor24"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="fade-right" data-aos-duration="1000"><div class="vission-textarea"><h2 class="font-48 lineh-56 font-lora weight-600 color-29 margin-b20">{h}</h2>
<p class="font-16 lineh-26 weight-500 color-30 margin-b24">{intro}</p><div class="border7 margin-b20"></div>
<div class="nav-section-area"><ul class="nav nav-pills mb-3" role="tablist">{nav}</ul><div class="tab-content">{panes}</div></div>{btn_html}</div></div>
<div class="col-lg-6" data-aos="zoom-out" data-aos-duration="1000"><div class="vissionimages">{img(im,alt,cls='ds-cover ds-vission')}<img src="/assets/images/elementor/elementor17.png" alt="" class="elementor-23 keyframe3"></div></div>
</div></div><img src="/assets/images/elementor/elementor23.png" alt="" class="elementor25"></div>'''

ABOUT_TABS=[('Mission',[('Our mission.','To make forming and maintaining a business clear, efficient and affordable. Diler Services prepares and files documents and keeps each client informed.'),('Referrals.','Legal and tax questions are referred to a licensed attorney or CPA.')]),
 ('Vision',[('Our vision.','To be the filing partner business owners trust, with transparent pricing and no unexpected charges.')]),
 ('Why Choose Us',[('Flat pricing.','Every service has a published flat fee. State fees are passed through at cost, without markup.'),('1-business-day submission.','Filings are submitted within 1 business day of complete information, or the $89 formation service fee is refunded.')])]
page('/about/','About Diler Services | Florida Business Formation','Diler Services LLC provides Florida LLC formation, EIN filing and registered agent service to business owners nationwide, with flat prices and state fees at cost.',
 breadcrumb('About Us')+about3+
 lawprovide('What Diler Services Prepares and Files',['Diler Services prepares and files LLC paperwork, obtains EINs, and serves as registered agent.','Every engagement includes flat published pricing, state fees at cost, and direct, professional communication.'],
   [('LLC Formation','Articles of Organization prepared and filed with the State of Florida. $89 plus the $125 state fee at cost.','/llc-formation/'),('EIN Filing','IRS employer identification number application prepared and submitted. $95 flat service fee.','/services/ein-filing/'),('Registered Agent','Official notices received for your company and forwarded the same day. $13.99 per month or $169 per year.','/services/registered-agent/')],
   b6('/services/','View all services','margin-t32'))+
 mission('The Process',['Submit the order form with the service required. Diler Services replies with a concise checklist of the information needed to file.'],
   ['Step 1: Order the service required','Step 2: Provide the business name, members or managers, and a mailing address','Step 3: Diler Services prepares the Articles of Organization','Step 4: Filing within 1 business day of complete information','Step 5: State confirmation and, where ordered, the EIN letter','Step 6: Ongoing registered agent support'],
   'signing-documents-2','Signing business formation documents',b6('/how-it-works/','See how it works','margin-t32'))+
 vission('The Mission, Your Success','Diler Services provides Florida business filings for owners nationwide under clear commitments.',ABOUT_TABS,'founder-laptop-2','Founder working on a laptop',b6(CTA,'Start your LLC','margin-t32'))+cta5(), '', BS)

# ================= HOW IT WORKS (about.html layouts) =================
page('/how-it-works/','How It Works | Diler Services','How Diler Services forms a Florida LLC: send your information, document preparation, filing with the state within 1 business day, and confirmation.',
 breadcrumb('How It Works')+
 lawprovide('From Order to State Confirmation',['Submit the request form with the service required, and Diler Services will respond with a concise checklist.','If the state rejects the business name, Diler Services refiles at no additional service fee.'],
   [('01 Send Your Information','Tell us your business name, owners or managers, and mailing address.','/order/'),('02 Document Preparation','Diler Services prepares the Articles of Organization for the State of Florida.','/llc-formation/'),('03 Filing With the State','Diler Services submits within 1 business day of receiving complete information.','/refund-policy/')],b6(CTA,'Start your LLC','margin-t32'))+
 mission('04 Confirmation',['The client receives the state confirmation and, if ordered, the EIN letter.','As registered agent, Diler Services receives legal notices for the company and forwards them the same day.'],
   ['Free name refile','Service fee guarantee','State fee at cost','Email support'],'opening-mail-2','Opening official mail',b6('/services/','Compare services','margin-t32'))+
 faq_two_col(FAQ_GROUPS[0]['items'][1:5]+FAQ_GROUPS[2]['items'][1:3],'Questions About the Process','h')+cta5(), faq_schema(FAQ_GROUPS[0]['items'][1:5]+FAQ_GROUPS[2]['items'][1:3]), BS)

# ================= WHY =================
WHY_TABS=[('Pricing',[('Clear flat pricing.','Every service has a published flat fee. State fees are passed through at cost, without markup.')]),
 ('Speed',[('1-business-day submission.','Filings are submitted within 1 business day of complete information, or the $89 formation service fee is refunded.')]),
 ('Refile',[('Free name refile.','If the State of Florida rejects the requested name, Diler Services refiles at no additional service fee.')])]
page('/why-diler-services/','Why Diler Services | Florida LLC Formation','Five clear commitments: flat pricing, 1-business-day submission, a free name refile, direct communication, and same-day mail forwarding.',
 breadcrumb('Why Diler Services')+
 vission('Five Clear Commitments','Diler Services provides Florida business filings for owners nationwide under five clear commitments: flat pricing, fast submission, a free name refile, direct communication, and same-day mail forwarding.',WHY_TABS,'office-plants-1','Bright office with plants',b6(CTA,'Start your LLC','margin-t32'))+
 lawprovide('Communication and Mail',['Service is delivered by email, in English and Spanish.'],
  [('Direct communication','Service is available in English and Spanish.','/contact/'),('Same-day mail forwarding','Registered agent clients receive documents forwarded the same day they arrive.','/services/registered-agent/'),('Not a law firm','Diler Services LLC is not a law firm and does not give legal or tax advice. Legal and tax questions are referred to a licensed attorney or CPA.','/terms-of-service/')],b6('/about/','About Diler Services','margin-t32'))+cta5(), '', BS)

# ================= SERVICES (servicev1.html) =================
SV_ICONS=['planning1.svg','planning2.svg','plan3.svg','plan4.svg','plan5.svg','plan6.svg','plan7.svg','plan8.svg']
grid=''.join(f'''<div class="col-lg-3 col-md-6 ds-cardcol" data-aos="zoom-in" data-aos-duration="{800+100*i}"><div class="ds-sv-card text-center">
<div class="service5-icons margin-b20"><img src="/assets/images/icons/{SV_ICONS[i]}" alt="" width="40" height="40"></div>
<a href="{s[6]}" class="ds-sv-title"><h3 class="font-lora font-20 lineh-26 weight-600 color-31">{s[1]}</h3></a><p class="ds-sv-price">{s[2]} <span>{s[3]}</span></p>
<div class="ds-sv-actions"><a href="/order/?service={s[0]}#order" class="ds-buy">Order now</a><a href="{s[6]}" class="ds-sv-more">Details</a></div></div></div>''' for i,s in enumerate(SERVICES))
servicev1=f'''<div class="servicev1-section-area section-padding5"><div class="container"><div class="row"><div class="col-lg-7 m-auto"><div class="servicev1-textarea margin-b60 text-center" data-aos="fade-down" data-aos-duration="800">
<h2 class="font-48 font-lora weight-600 color-29 lineh-56">Business Formation Services To Start and Protect Your Company</h2><p class="font-ks font-16 color-30 margin-t">Flat prices, state fees at cost, and filing within 1 business day of complete information.</p></div></div></div>
<div class="row">{grid}</div></div></div>'''
page('/services/','Services | Diler Services','Florida LLC formation $89 plus state fee at cost, EIN filing $95, registered agent $13.99 per month or $169 per year, annual reports, DBA, amendments and reinstatement.',
 breadcrumb('Our Services')+servicev1+faq_two_col(FAQ_GROUPS[3]['items']+FAQ_GROUPS[1]['items'][3:4]+FAQ_GROUPS[2]['items'][0:1],'Pricing Questions','s','h2','otherbg')+cta5(), faq_schema(FAQ_GROUPS[3]['items']), BS)

# ================= PRICING =================
page('/pricing/','Pricing | Diler Services','Transparent pricing: LLC formation $89 plus the $125 Florida state fee at cost, formation bundle $299, registered agent $13.99 per month or $169 per year.',
 breadcrumb('Pricing')+pricing_section().replace('<h2 class="font-outfit font-44 weight-600 lineh-52 color-17">Transparent Pricing for Business Formation</h2>','<h2 class="font-outfit font-44 weight-600 lineh-52 color-17">Flat Service Fees, State Fees at Cost</h2>')+faq_two_col(FAQ_GROUPS[3]['items'],'Pricing and Refunds','p')+cta5(), faq_schema(FAQ_GROUPS[3]['items']), BS)

# ================= SERVICE DETAIL (serviceleft.html) =================
DETAIL={
 'llc-formation':dict(img='founder-laptop-1',alt='Founder starting a Florida LLC online',
   p1='Diler Services prepares and files Articles of Organization with the State of Florida. LLC formation is $89 plus the $125 Florida state fee, passed through at cost.',
   p2='Diler Services submits within 1 business day of receiving complete information, or refunds the $89 service fee. The state fee is not refundable once filed.',
   h2='Everything Required to Open an LLC',p3='Add EIN filing for $95 and registered agent service for $13.99 per month or $169 per year. The Formation Bundle covers LLC formation, the state fee and EIN filing for $299 total. If the state rejects the business name, Diler Services refiles at no additional service fee.',
   ap=[('Send Your Information','Tell us your business name, owners or managers, and mailing address.'),('Filing With the State','Diler Services submits within 1 business day of receiving complete information.')],
   checks=['Free name refile','Service fee guarantee','State fee at cost','Email support','Articles of Organization prepared','State confirmation delivered'],faq=FAQ_GROUPS[0]['items']+[FAQ_GROUPS[3]['items'][0],FAQ_GROUPS[3]['items'][3]]),
}
GEN_FAQ={'ein-filing':[FAQ_GROUPS[2]['items'][0],FAQ_GROUPS[2]['items'][1]],'registered-agent':FAQ_GROUPS[1]['items'],'formation-bundle':[FAQ_GROUPS[3]['items'][0],FAQ_GROUPS[2]['items'][1]],
 'annual-report':[FAQ_GROUPS[2]['items'][2],FAQ_GROUPS[2]['items'][3]],'dba':[FAQ_GROUPS[3]['items'][1]],'amendment':[FAQ_GROUPS[3]['items'][1]],'reinstatement':[FAQ_GROUPS[2]['items'][3],FAQ_GROUPS[3]['items'][1]]}
GEN_IMG={'ein-filing':'signing-documents-1','registered-agent':'mailbox-1','formation-bundle':'consultation-1','annual-report':'signing-documents-2','dba':'founder-workshop-4','amendment':'office-bright-2','reinstatement':'opening-mail-2'}
def detail_page(s):
    k,n,price,note,pts,ic,href=s
    d=DETAIL.get(k) or dict(img=GEN_IMG[k],alt=n,p1=f'{n}: {price}, {note}.',p2='Diler Services prepares and submits the filing, and the client receives the confirmation by email.',
        h2=f'What {n} Includes',p3='Legal and tax questions are referred to a licensed attorney or CPA.',ap=[(pts[0],pts[1]+'.'),(pts[2],f'{price} {note}.')],checks=pts+['Flat service fee','Email support'],faq=GEN_FAQ[k])
    approach=''.join(f'''<div class="col-lg-6"><div class="approach-area margin-t32"><div class="approach-img"><img src="/assets/images/icons/{['stragig1.svg','approach1.svg'][i]}" alt="" class="approahimages ts" width="40" height="40"></div>
<div class="approach-text"><h3 class="font-lora font-20 weight-600 color-29 margin-b ts">{t}</h3><p class="fontks font-16 lineh-26 weight-500 color-30 ts">{x}</p></div></div></div>''' for i,(t,x) in enumerate(d['ap']))
    cols=[d['checks'][i::3] for i in range(3)]
    chk=''.join('<div class="col-lg-4">'+''.join(f'<div class="checkservice-area"><p class="font-ks font-16 lineh-20 weight-600 color-29">{CHECK}{c}</p></div>' for c in col)+'</div>' for col in cols)
    main=f'''<div class="serviceauthior-area">{img(d['img'],d['alt'],cls='ds-cover ds-detail-img',lazy=False)}
<h1 class="font-lora font-40 lineh-50 weight-600 color-29 margin-b20 margin-t28">{n}</h1>
<p class="ds-detail-price">{price} <span>{note}</span></p><p class="ds-detail-buy"><a href="/order/?service={k}#order" class="ds-buy">Buy now</a></p>
<p class="font-ks font-16 lineh-26 weight-500 color-30 margin-b20">{d['p1']}</p><p class="font-ks font-16 lineh-26 weight-500 color-30">{d['p2']}</p>
<div class="border30"></div><h2 class="font-lora font-40 lineh-50 weight-600 color-29 margin-b20">{d['h2']}</h2><p class="font-ks font-16 lineh-26 weight-500 color-30">{d['p3']}</p>
<div class="row">{approach}</div><div class="border30"></div>
<h2 class="font-lora font-40 lineh-50 weight-600 color-29 margin-b20 margin-t28">Included With {n}</h2><div class="row">{chk}</div>
<p class="font-ks font-16 lineh-26 weight-500 color-30">{DISC}</p>{b6('/order/?service='+k+'#order','Buy now','margin-t32')}</div>'''
    others=[o for o in SERVICES if o[0]!=k][:4]
    more=''.join(f'''<div class="col-lg-6 col-md-6 ds-cardcol" data-aos="fade-up" data-aos-duration="{900+150*i}"><div class="service3-boxarea margin-b30 bgservice2 ds-s3card"><div class="row align-items-center"><div class="col-6"><div class="service3-text2">
<a href="{o[6]}"><h3 class="font-lora font-22 lineh-28 color-29 weight-600 margin-b">{o[1]}</h3></a><p class="font-ks font-16 lineh-26 weight-500 color-30">{o[2]} {o[3]}.</p>
<div class="ds-card-actions"><a href="/order/?service={o[0]}#order" class="ds-buy">Order now</a><a href="{o[6]}" class="font-ks font-16 lineh-16 color-29 weight-700 laearnmore2">Details {AR}</a></div></div></div>
<div class="col-6"><div class="service3-imag1">{img(GEN_IMG.get(o[0],'founder-laptop-1'),o[1],cls='ds-cover ds-s3')}</div></div></div></div></div>''' for i,o in enumerate(others))
    body=breadcrumb(n,f'<a href="/services/" class="color">Services</a><span><i class="fa-solid fa-angle-right"></i></span> {n}',h1=False)+f'''<div class="serviceleft-section-area section-padding5"><div class="container"><div class="row">
<div class="col-lg-4 order-2 order-lg-1" data-aos="fade-right" data-aos-duration="1000">{services_sidebar(k)}</div><div class="col-lg-8 order-1 order-lg-2">{main}</div></div></div></div>
<div class="serviceleftblog-section-area section-padding8"><div class="container"><div class="row"><div class="col-lg-6 m-auto"><div class="sericeleft text-center margin-b60"><h2 class="font-lora font-40 lineh-50 weight-600 color-29">View Our More Services</h2></div></div></div><div class="row">{more}</div></div></div>'''+faq_two_col(d['faq'],'Frequently Asked Questions','d','h2','otherbg')+cta5()
    path=href
    page(path,f'{n} | Diler Services',f'{n}: {price} {note}. Diler Services prepares and files Florida business filings for owners nationwide.',body,faq_schema(d['faq']),BS)
for s in SERVICES: detail_page(s)

# ================= FAQ =================
faqs_body=breadcrumb('Frequently Asked Questions','FAQs')
for gi,g in enumerate(FAQ_GROUPS):
    faqs_body+=faq_two_col(g['items'],g['title'],f'g{gi}','h2','otherbg' if gi%2 else '')
page('/faqs/','Frequently Asked Questions | Diler Services','Answers about Florida LLC formation, registered agent service, EIN filing, annual reports, pricing and refunds.',faqs_body+cta5(),faq_schema(allfaq),BS)

# ================= BLOG LIST (blog2.html) =================
def blog_row():
    g0=GUIDES[0]
    side=''.join(f'''<div class="blog-auhtor2-text {'margin-b30' if i==0 else ''}" data-aos="zoom-in" data-aos-duration="{1100+200*i}"><div class="blog2-ahtuor2 blog2inner"><div class="blog-date-list margin-b"><img src="/assets/images/icons/daterane.png" alt="" width="20" height="20"><span class="font-16 lineh-16 font-ks weight-500 color-17">October 20, 2026 &middot; {g[1]}</span></div>
<a href="/blog/{g[0]}/"><h2 class="font-20 font-lora color-17 lineh-28 weight-600 margin-b14">{g[2]}</h2></a><p class="font-16 font-ks lineh-26 weight-500 color-17 margin-b24">{g[3]}</p>
<a href="/blog/{g[0]}/" class="font-16 font-ks weight-700 color-17 lineh-26 d-inline-block learn-more">Read the {g[5]} {ARROW}</a></div></div>''' for i,g in enumerate(GUIDES[1:]))
    return f'''<div class="cloginner-3-sevtion-area section-padding5"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="zoom-out" data-aos-duration="1000"><div class="blog2-author-area"><div class="blog2-images">{img(g0[4],'Founder working on a laptop',cls='ds-cover ds-blog-big',lazy=False)}</div>
<div class="blog-auhtor2-text blog2-author-poition"><div class="blog2-ahtuor2 blog-2ahthor bloinner2"><div class="blog-date-list margin-b"><img src="/assets/images/icons/daterange1.png" alt="" width="20" height="20"><span class="font-16 lineh-16 font-ks weight-600 color">October 20, 2026 &middot; {g0[1]}</span></div>
<a href="/blog/{g0[0]}/"><h2 class="font-20 font-lora color lineh-28 weight-600 margin-b">{g0[2]}</h2></a><p class="font-16 font-ks lineh-26 weight-400 color">{g0[3]}</p>
<a href="/blog/{g0[0]}/" class="font-16 font-ks weight-700 color lineh-26 margin-t24 d-inline-block learn-more learn-more1">Read the {g0[5]} {ARROW}</a></div></div></div></div>
<div class="col-lg-6">{side}</div></div></div></div>'''
page('/blog/','Florida Business Formation Guides | Diler Services','Clear, verified explanations of Florida filing requirements, prepared by Diler Services for business owners nationwide.',
 breadcrumb('Florida Business Formation Guides','Guides',sub='Clear, verified explanations of Florida filing requirements, prepared by Diler Services for business owners nationwide.')+blog_row()+cta5())

# ================= BLOG DETAIL (blogleft.html) =================
def styl(c):
    c=c.replace('<h2>','<h2 class="font-lora font-32 lineh-42 weight-600 color-29 margin-b20 margin-t32">').replace('<h3>','<h3 class="font-lora font-24 lineh-32 weight-600 color-29 margin-b14 margin-t24">')
    c=c.replace('<p>','<p class="font-ks font-16 weight-500 lineh-26 color-30 margin-b20">')
    return c
for gi,(slug,cat,title,desc,im,short) in enumerate(GUIDES):
    t,c=article(f'blog/{slug}/index.html')
    c=re.sub(r'^.*?October 20, 2026\s*(</p>)?','',c,count=1,flags=re.S) if 'October 20, 2026' in c[:600] else c
    c=re.sub(r'^\s*(Guides\s*/\s*[^<]*)','',c)
    others=[g for g in GUIDES if g[0]!=slug]
    cats=''.join(f'<div class="singlepalnning-area margin-b20 {"ds-on" if g[0]==slug else ""}"><a href="/blog/{g[0]}/" class="font-18 font-ks lineh-18 weight-600 color-29 ts">{g[1]}</a><span><i class="fa-solid fa-angle-right ts"></i></span></div>' for g in GUIDES)
    recent=''.join(f'''<div class="recentblog-text margin-b20"><div class="recent-images">{img(g[4],g[2],cls='ds-cover ds-recent',w=640)}</div><div class="recentblogsall"><div class="blog-date-list margin-b12"><img src="/assets/images/icons/daterane.png" alt="" width="20" height="20"><span class="font-16 lineh-16 font-ks weight-600 color-29">October 20, 2026</span></div>
<h3 class="font-16 lineh-24 weight-600 color-29 font-ks"><a href="/blog/{g[0]}/" class="color-29 ts">{g[2]}</a></h3></div></div>''' for g in others)
    side=f'''<div class="serviceour-area"><h2 class="font-lora font-24 lineh-24 weight-600 color-29 margin-b24">Guide Categories</h2>{cats}</div>
<div class="recenrblos-area"><h2 class="font-24 lineh-24 weight-600 color-29 font-lora margin-b24">Recent Guides</h2>{recent}</div>{email_help()}'''
    mainc=f'''<div class="blogleftinner3-area">{img(im,title,cls='w-100 innerimg ds-cover ds-detail-img',lazy=False)}
<div class="afteralex-area"><div class="alex"><img src="/assets/images/icons/daterane.png" alt="" width="20" height="20"><span class="font-16 lineh-16 font-ks weight-500 color-29">October 20, 2026</span></div>
<div class="alex"><img src="/assets/images/icons/tag1.png" alt="" width="20" height="20"><span class="font-ks font-16 lineh-24 weight-600 color-29">{cat}</span></div>
<div class="alex alex1"><span class="font-ks font-16 lineh-24 weight-600 color-29">Diler Services LLC</span></div></div>
<h1 class="font-lora font-40 lineh-50 weight-600 color-29 margin-b20">{title}</h1><div class="ds-article">{styl(c)}</div>
<div class="peragraph-pera peragraeabg"><p class="font-16 font-ks lineh-26 weight-500 color">{DISC} This guide is general information. Questions about a specific situation should go to a licensed attorney or CPA.</p></div>
{b6(CTA,'Start your LLC','margin-t32')}</div>'''
    more=''.join(f'''<div class="col-lg-6 col-md-6" data-aos="fade-up" data-aos-duration="{900+200*i}"><div class="blog-auhtor2-text"><div class="blog2-ahtuor2 blog2inner"><div class="blog-date-list margin-b"><img src="/assets/images/icons/daterane.png" alt="" width="20" height="20"><span class="font-16 lineh-16 font-ks weight-500 color-17">October 20, 2026 &middot; {g[1]}</span></div>
<a href="/blog/{g[0]}/"><h3 class="font-20 font-lora color-17 lineh-28 weight-600 margin-b14">{g[2]}</h3></a><p class="font-16 font-ks lineh-26 weight-500 color-17 margin-b24">{g[3]}</p><a href="/blog/{g[0]}/" class="font-16 font-ks weight-700 color-17 lineh-26 d-inline-block learn-more">Read the {g[5]} {ARROW}</a></div></div></div>''' for i,g in enumerate(others))
    body=breadcrumb('Florida Business Formation Guides',f'<a href="/blog/" class="color">Guides</a><span><i class="fa-solid fa-angle-right"></i></span> {cat}',h1=False)+f'''<div class="blogleft-section-area section-padding5"><div class="container"><div class="row">
<div class="col-lg-4 order-2 order-lg-1" data-aos="fade-right" data-aos-duration="1000">{side}</div><div class="col-lg-8 order-1 order-lg-2">{mainc}</div></div></div></div>
<div class="serviceleftblog-section-area section-padding8"><div class="container"><div class="row"><div class="col-lg-6 m-auto"><div class="sericeleft text-center margin-b60"><h2 class="font-lora font-40 lineh-50 weight-600 color-29">Read Our More Guides</h2></div></div></div><div class="row">{more}</div></div></div>'''+cta5()
    art='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"datePublished":"2026-10-20","author":{"@type":"Organization","name":"Diler Services LLC"},"publisher":{"@type":"Organization","name":"Diler Services LLC"},"description":desc})+'</script>'
    page(f'/blog/{slug}/',f'{title} | Diler Services',desc,body,art)

# ================= LEGAL (blogleft main column, no sidebar) =================
for slug,title,desc in [('privacy-policy','Privacy Policy','How Diler Services LLC collects, uses and protects information provided through dilerservices.com.'),
                        ('terms-of-service','Terms of Service','Terms governing the use of dilerservices.com and the services provided by Diler Services LLC.'),
                        ('refund-policy','Refund Policy','The Diler Services 1-business-day submission guarantee, state fee policy and free name refile.')]:
    t,c=article(f'{slug}/index.html')
    c=re.sub(r'^\s*'+re.escape(title)+r'\s*','',c)
    body=breadcrumb(title,h1=False)+f'<div class="blogleft-section-area section-padding5"><div class="container"><div class="row"><div class="col-lg-9 m-auto"><div class="blogleftinner3-area"><h1 class="font-lora font-40 lineh-50 weight-600 color-29 margin-b20">{title}</h1><div class="ds-article">{styl(c)}</div></div></div></div></div></div>'+cta5()
    page(f'/{slug}/',f'{title} | Diler Services',desc,body)

# ================= CONTACT (contact1.html) =================
opts=''.join(f'<option value="{o}">{o}</option>' for o in SERVICE_OPTS)
contact1=f'''<div class="cotactinner-section-area section-padding5"><div class="container"><div class="row align-items-center">
<div class="col-lg-6" data-aos="fade-right" data-aos-duration="1000"><div class="contcat5-textarea5">{span3('Contact Us')}
<h2 class="font-lora font-48 lineh-56 weight-600 color-29 margin-b20 clienth2">Order or Request Information</h2>
<p class="font-ks font-16 weight-500 lineh-26 color-30">Describe the service required. Diler Services responds to every inquiry by email.</p>
<div class="phone7-textarea margin-t32 contactinnerbg"><div class="phone7-icon"><img src="/assets/images/icons/email7.png" alt="" width="24" height="24"></div><div class="phone7-text"><p class="font-16 lineh-16 weight-500 font-ks color-30 margin-b">Send a message</p><a href="mailto:{EMAIL}" class="font-lora font-24 weight-700 lineh-24 color-29 ds-break">{EMAIL}</a></div></div>
<div class="phone7-textarea margin-t contactinnerbg"><div class="phone7-icon"><img src="/assets/images/icons/check1.png" alt="" width="24" height="24"></div><div class="phone7-text"><p class="font-16 lineh-16 weight-500 font-ks color-30 margin-b">Ready to order?</p><a href="{CTA}" class="font-lora font-24 weight-700 lineh-24 color-29">Start your LLC online</a></div></div>
</div></div>
<div class="col-lg-6" data-aos="fade-left" data-aos-duration="1000"><div class="contact5-main-section"><div class="contact-main-text"><h2 class="font-lora font-24 lineh-24 weight-600 color">Send Us a Message</h2><p class="font-ks font-16 lineh-26 weight-500 color margin-t">Diler Services will reply by email.</p></div>
<form class="contac5-input5area diler-form" method="POST" action="https://api.web3forms.com/submit"><input type="hidden" name="access_key" value="{KEY}"><input type="hidden" name="subject" value="New website inquiry: Diler Services"><input type="hidden" name="from_name" value="Diler Services Website"><input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off">
<div class="row"><div class="col-lg-6"><div class="input-5area margin-t32"><label class="visually-hidden" for="c-name">Full name</label><input id="c-name" type="text" name="Name" placeholder="Full name *" required autocomplete="name"></div></div>
<div class="col-lg-6"><div class="input-5area margin-t32"><label class="visually-hidden" for="c-email">Email</label><input id="c-email" type="email" name="Email" placeholder="Email address *" required autocomplete="email"></div></div>
<div class="col-lg-12"><div class="input-5area margin-t"><label class="visually-hidden" for="c-biz">Business name</label><input id="c-biz" type="text" name="Business name" placeholder="Business name" autocomplete="organization"></div></div>
<div class="col-lg-12"><div class="input-5area margin-t"><label class="visually-hidden" for="c-svc">Service</label><select id="c-svc" name="Service" class="ds-native ds-dark-select" required>{opts}</select></div></div>
<div class="col-lg-12"><div class="input-5area margin-t"><label class="visually-hidden" for="c-msg">Message</label><textarea id="c-msg" name="Message" rows="6" placeholder="Message *" required></textarea></div>
<div class="contact5-btn5"><button class="font-ks font-16 lineh-16 weight-700 color margin-t32 contcat5" type="submit">Submit Request {AR}</button></div><div class="dzFormMsg" role="status"></div>
<p class="font-14 color margin-t">{DISC}</p></div></div></form></div></div>
</div></div></div>'''
page('/contact/','Contact Diler Services | Florida LLC Formation','Request Florida LLC formation, EIN filing or registered agent service. Diler Services responds to every inquiry by email.',
 breadcrumb('Contact Us')+contact1+faq_two_col(FAQ_GROUPS[4]['items']+FAQ_GROUPS[0]['items'][1:4],'Frequently Asked Questions','k')+cta5(), faq_schema(FAQ_GROUPS[4]['items']+FAQ_GROUPS[0]['items'][1:4]), BS)

# ================= ORDER (contact5 layout, full purchase flow) =================
# Prices in cents. state: int = known Florida state fee passed through at cost, None = at cost, confirmed before filing.
PRODUCTS={
 'llc-formation':dict(name='LLC Formation',fee=8900,state=12500,note='$89 service fee plus the $125 Florida state fee at cost'),
 'formation-bundle':dict(name='Formation Bundle (LLC and EIN)',fee=17400,state=12500,note='$174 service fee plus the $125 state fee: $299 total'),
 'ein-filing':dict(name='EIN Filing',fee=9500,state=0,note='$95 flat service fee'),
 'annual-report':dict(name='Annual Report',fee=9900,state=None,note='$99 service fee plus the state fee at cost'),
 'annual-report-late':dict(name='Annual Report (filed late)',fee=14900,state=None,note='$149 service fee plus the state fee at cost'),
 'dba':dict(name='DBA (Fictitious Name)',fee=12900,state=None,note='$129 service fee plus the state fee at cost'),
 'amendment':dict(name='Amendment',fee=9900,state=None,note='$99 service fee plus the state fee at cost'),
 'reinstatement':dict(name='Reinstatement',fee=29900,state=None,note='$299 service fee plus the state fees at cost'),
 'registered-agent-only':dict(name='Registered agent only',fee=0,state=0,note='Choose a monthly or yearly plan below'),
 'ein-addon':dict(name='EIN Filing',fee=9500,state=0,note='$95 flat service fee',pay_key='ein-filing'),
 'registered-agent-monthly':dict(name='Registered Agent (monthly)',fee=1399,state=0,note='$13.99 per month',renew='month'),
 'registered-agent-yearly':dict(name='Registered Agent (yearly)',fee=16900,state=0,note='$169 per year',renew='year'),
}
BASE_ORDER=['llc-formation','formation-bundle','ein-filing','annual-report','annual-report-late','dba','amendment','reinstatement','registered-agent-only']
def _radio(name,k,checked=False,extra=''):
    P=PRODUCTS[k]
    return f'<label class="ds-radio"><input type="radio" name="{name}" value="{k}" {"checked" if checked else ""} {extra}><span><b>{P["name"]}</b><small>{P["note"]}</small></span></label>'
base_html=''.join(f'<div class="col-md-6 ds-cardcol">{_radio("product",k,i==0)}</div>' for i,k in enumerate(BASE_ORDER))
ra_html=''.join(f'<div class="col-md-4 ds-cardcol">{x}</div>' for x in [
 '<label class="ds-radio"><input type="radio" name="ra" value="" checked><span><b>No registered agent</b><small>I have my own Florida registered agent</small></span></label>',
 _radio('ra','registered-agent-monthly'),_radio('ra','registered-agent-yearly')])
ein_html=f'<label class="ds-radio ds-ein-addon"><input type="checkbox" name="ein" value="ein-addon"><span><b>Add EIN Filing</b><small>$95 flat service fee</small></span></label>'
types=''.join(f'<option value="{t}">{t}</option>' for t in ["","New Florida LLC","Existing Florida LLC","Fictitious name (DBA)","Other"]).replace('<option value=""></option>','<option value="">Select one</option>')
def inp(id,label,name,typ='text',req=False,extra=''):
    return f'<div class="input-5area margin-t"><label for="{id}">{label}{" *" if req else " (optional)"}</label><input id="{id}" type="{typ}" name="{name}" {"required" if req else ""} {extra}></div>'
order_js='<script src="/assets/js/payment-links.js" defer></script><script>window.DS_PRODUCTS='+json.dumps(PRODUCTS)+';window.DS_EMAIL="'+EMAIL+'";</script><script src="/assets/js/order.js" defer></script>'
STEPS_OL='<ol class="ds-steps" aria-label="Order steps">'+''.join(f'<li class="ds-step" data-step-ind="{i+1}"><span>{i+1}</span>{t}</li>' for i,t in enumerate(['Service','Details','Review','Payment']))+'</ol>'
order_body=breadcrumb('Order Online in Four Steps','Order',sub='Choose a service and any add-ons, enter your details, review and accept the terms, then pay. Filings are submitted within 1 business day of complete information.')+f'''<div class="cotactinner-section-area section-padding5" id="order"><div class="container"><div class="row">
<div class="col-lg-7"><div class="contact5-main-section ds-order-box">{STEPS_OL}
<form class="ds-order" autocomplete="off" method="POST" action="https://api.web3forms.com/submit" novalidate>
<input type="hidden" name="access_key" value="{KEY}"><input type="hidden" name="subject" value="New order: Diler Services" data-subject><input type="hidden" name="from_name" value="Diler Services Website">
<input type="hidden" name="Order reference" data-f="ref"><input type="hidden" name="Order items" data-f="items"><input type="hidden" name="Service fees" data-f="fees"><input type="hidden" name="State fees" data-f="state"><input type="hidden" name="Total due today" data-f="total"><input type="hidden" name="Payment status" data-f="pay">
<input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off">
<fieldset data-step="1"><legend class="font-lora font-24 weight-600 color margin-b24">1. Choose a service</legend><div class="row g-3">{base_html}</div>
<p class="font-lora font-20 weight-600 color margin-t32 margin-b">Add-ons</p><div class="ds-ein-wrap">{ein_html}</div>
<p class="ds-tip" data-bundle-tip hidden>LLC formation plus EIN filing ordered separately is $309. The Formation Bundle covers both for $299. <button type="button" class="ds-linkbtn" data-to-bundle>Switch to the bundle</button></p>
<p class="font-lora font-20 weight-600 color margin-t32 margin-b">Registered agent service</p><div class="row g-3">{ra_html}</div>
<p class="ds-ra-req" data-ra-req hidden>Choose a monthly or yearly registered agent plan.</p></fieldset>
<fieldset data-step="2" hidden><legend class="font-lora font-24 weight-600 color margin-b24">2. Your details</legend>
<p class="font-16 color margin-b">Business</p>
{inp('o-biz','Business name','Business name',req=True,extra='autocomplete="organization" placeholder="Example Ventures LLC"')}
{inp('o-alt','Alternate business name','Alternate name',extra='placeholder="Second choice, in case the first is unavailable"')}
<div class="input-5area margin-t"><label for="o-type">Order type *</label><select id="o-type" required name="Business type" class="ds-native ds-dark-select">{types}</select></div>
<p class="font-16 color margin-b margin-t32">Contact</p>
{inp('o-name','Full name','Name',req=True,extra='autocomplete="name"')}
{inp('o-email','Email','Email','email',req=True,extra='autocomplete="email" placeholder="you@yourbusiness.com"')}
{inp('o-tel','Phone','Phone','tel',extra='autocomplete="tel"')}
<div class="input-5area margin-t"><label for="o-addr">Mailing address *</label><textarea id="o-addr" name="Mailing address" rows="3" required autocomplete="street-address"></textarea></div>
<div class="input-5area margin-t"><label for="o-notes">Notes (optional)</label><textarea id="o-notes" name="Message" rows="3" placeholder="Managers or members, existing document number, or anything else we should know"></textarea></div></fieldset>
<fieldset data-step="3" hidden><legend class="font-lora font-24 weight-600 color margin-b24">3. Review and accept</legend><dl class="ds-review" data-review></dl>
<div class="ds-consents">
<label class="ds-check"><input type="checkbox" name="Agreed to Terms of Service" value="Yes" required><span>I agree to the <a href="/terms-of-service/" target="_blank" rel="noopener">Terms of Service</a>.</span></label>
<label class="ds-check"><input type="checkbox" name="Agreed to Refund Policy" value="Yes" required><span>I have read and accept the <a href="/refund-policy/" target="_blank" rel="noopener">Refund Policy</a>.</span></label>
<label class="ds-check"><input type="checkbox" name="Acknowledged not a law firm" value="Yes" required><span>I understand that {DISC}</span></label>
</div></fieldset>
<fieldset data-step="4" hidden><legend class="font-lora font-24 weight-600 color margin-b24">4. Payment</legend>
<div class="ds-total"><span>Total due today</span><span data-total>$214</span></div><p class="font-14 color margin-t" data-total-note></p>
<div class="ds-paynote" data-paynote-link hidden><p>You will be sent to our secure checkout to pay by card. Your order details are recorded first.</p></div>
<div class="ds-paynote" data-paynote-manual hidden><p><b>Online card payment is being set up.</b> Submit your order now and we'll email you a secure payment link within 1 business day. No payment is taken on this page.</p></div>
</fieldset>
<div class="dzFormMsg margin-t" role="status" aria-live="polite"></div>
<div class="ds-order-nav"><button type="button" data-back class="ds-btn-outline" hidden>Back</button><span class="font-14 color ms-auto" data-running>Total due today: $214</span>
<button type="button" data-next class="contcat5 font-ks font-16 weight-700 color">Continue {AR}</button><button type="submit" data-submit class="contcat5 font-ks font-16 weight-700 color" hidden>Submit order {AR}</button></div>
</form></div></div>
<div class="col-lg-5"><aside class="ds-summary" aria-label="Order summary"><h2 class="font-lora font-24 weight-600 color-29 margin-b20">Order summary</h2>
<table class="ds-sum-table"><thead><tr><th scope="col">Item</th><th scope="col">Our fee</th><th scope="col">State fee</th></tr></thead><tbody data-sum-rows></tbody>
<tfoot><tr><th scope="row">Subtotals</th><td data-sum-fees>$89</td><td data-sum-state>$125</td></tr><tr class="ds-sum-total"><th scope="row" colspan="2">Total due today</th><td data-sum-total>$214</td></tr></tfoot></table>
<p class="ds-sum-note" data-sum-note></p>
<p class="ds-sum-note">State fees are paid to the State of Florida at cost, with no markup. Our service fees are refundable under the <a href="/refund-policy/">Refund Policy</a>.</p>
<div class="phone7-textarea margin-t contactinnerbg"><div class="phone7-icon"><img src="/assets/images/icons/email7.png" alt="" width="24" height="24"></div><div class="phone7-text"><p class="font-16 lineh-16 weight-500 font-ks color-30 margin-b">Questions first?</p><a href="mailto:{EMAIL}" class="font-lora font-20 weight-700 lineh-24 color-29 ds-break">{EMAIL}</a></div></div>
<p class="ds-sum-note margin-t">{DISC}</p></aside></div>
</div></div></div>'''+faq_two_col([FAQ_GROUPS[0]['items'][4],FAQ_GROUPS[3]['items'][0],FAQ_GROUPS[3]['items'][2],FAQ_GROUPS[1]['items'][3]],'Before You Order','o')
page('/order/','Order | Diler Services','Order Florida LLC formation, EIN filing, registered agent service and compliance filings online. Flat service fees with state fees at cost.', order_body, '', order_js+BS)

# ================= 404 =================
page('/404.html','Page Not Found | Diler Services','Page not found.', breadcrumb('Page Not Found','404',h1=False)+f'''<div class="servicev1-section-area section-padding5"><div class="container"><div class="row"><div class="col-lg-7 m-auto text-center" data-aos="fade-up" data-aos-duration="900">
<p class="ds-404 font-lora weight-700">404</p><h1 class="font-lora font-40 lineh-50 weight-600 color-29 margin-b20">This page could not be found</h1><p class="font-ks font-16 color-30">The page may have moved. These links can help.</p>
<div class="ds-404-links">{b6('/','Back to home','margin-t32')} {b6('/services/','View services','margin-t32')} {b6('/contact/','Contact Diler Services','margin-t32')}</div></div></div></div></div>''')
print('inner built')
