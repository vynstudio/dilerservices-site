"""Builds the Diler Services proposal on the Vikinglab Consultore template with Brand Kit v3 (Folio).

Run from the repository root:  python3 v3/_build/build.py
Writes v3/*.html (English) and v3/es/*.html (Spanish). Content lives in content.json, en.json and es.json
beside this script; page chrome reuses the Consultore markup and classes.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
REPO = os.path.dirname(OUT)

C = json.load(open(os.path.join(HERE, 'content.json'), encoding='utf-8'))
T = {l: json.load(open(os.path.join(HERE, f'{l}.json'), encoding='utf-8')) for l in ('en', 'es')}
SERVICES = C['services']
EMAIL = 'info@dilerservices.com'
FORM_KEY = 'e2f8f8d8-34b9-425d-ad45-cba50184ec8e'  # Web3Forms public access key (same as the live site)
SITE = 'https://dilerservices.com'

e = html.escape


def L(lang, d):
    return d[lang] if isinstance(d, dict) else d


# Extra strings this build needs that the shared dictionaries do not carry.
X = {
    'en': {
        'home_title': 'Florida LLC Formation and Registered Agent',
        'services_more': 'Read more', 'all_services': 'All services', 'contact_us': 'Contact us',
        'facts': [('1', 'Business day to submit'), ('$89', 'Formation service fee'), ('$125', 'Florida state fee at cost'), ('8', 'Filing services')],
        'about_eyebrow': 'About us', 'about_title': 'Paperwork, <span>handled.</span>',
        'about_text': 'Diler Services forms Florida companies and keeps them in good standing. Our clients are first-time founders, Hispanic and immigrant entrepreneurs, contractors, real estate investors and out-of-state owners who need a Florida registered agent.',
        'about_checks': ['Plain, published prices', 'Filed within 1 business day', 'English and Spanish', 'State fees at cost'],
        'about_cta': 'More about us',
        'steps_text': 'Plain language, clear timelines and one point of contact. We explain each step so nothing is a surprise.',
        'pricing_note': 'State fees are paid to the State of Florida at cost, with no markup.',
        'other_services': 'Other services', 'other_services_text': 'Every other filing has one published fee, plus the state fee at cost.',
        'contact_title': 'Questions? <span>Ask us</span> in English or Spanish.',
        'contact_text': 'Tell us what you need. We reply by email within 1 business day.',
        'cta_title': 'Ready to start your Florida LLC?', 'cta_text': 'Submitted within 1 business day of complete information.',
        'detail_side_services': 'Our services', 'detail_side_contact': 'Contact', 'detail_includes': "What's included",
        'detail_faq': 'Questions about', 'home': 'Home', 'order_service': 'Choose a service', 'order_ra': 'Registered agent',
        'order_ra_none': 'I have my own Florida registered agent', 'order_ra_month': '$13.99 per month', 'order_ra_year': '$169 per year',
        'order_ein': 'Add EIN filing ($95)', 'order_details': 'Your details', 'order_item': 'Item',
        'reply_hours': 'We reply within 1 business day', 'not_found': 'Page not found', 'not_found_text': 'The page you are looking for has moved or does not exist.',
        'back_home': 'Back to home', 'legal_note': 'This text is a draft pending attorney review.',
        'menu': 'Menu', 'switch': 'Español', 'values_eyebrow': 'Why Diler Services',
        'values_title': 'Calm, precise and <span>bilingual.</span>',
    },
    'es': {
        'home_title': 'Formación de LLC en Florida y agente registrado',
        'services_more': 'Ver más', 'all_services': 'Todos los servicios', 'contact_us': 'Contáctenos',
        'facts': [('1', 'Día hábil para presentar'), ('$89', 'Tarifa de formación'), ('$125', 'Tarifa estatal al costo'), ('8', 'Servicios de trámites')],
        'about_eyebrow': 'Nosotros', 'about_title': 'Sus trámites, <span>resueltos.</span>',
        'about_text': 'Diler Services forma empresas en Florida y las mantiene al día. Atendemos a quienes abren su primer negocio, emprendedores hispanos e inmigrantes, contratistas, inversionistas de bienes raíces y dueños de otros estados que necesitan un agente registrado en Florida.',
        'about_checks': ['Precios claros y publicados', 'Presentado en 1 día hábil', 'Español e inglés', 'Tarifas estatales al costo'],
        'about_cta': 'Conozca más',
        'steps_text': 'Lenguaje claro, plazos claros y un solo punto de contacto. Le explicamos cada paso para que nada le sorprenda.',
        'pricing_note': 'Las tarifas estatales se pagan al Estado de Florida al costo, sin recargo.',
        'other_services': 'Otros servicios', 'other_services_text': 'Cada trámite tiene una tarifa publicada, más la tarifa estatal al costo.',
        'contact_title': '¿Preguntas? <span>Escríbanos</span> en español o en inglés.',
        'contact_text': 'Cuéntenos qué necesita. Respondemos por correo dentro de 1 día hábil.',
        'cta_title': '¿Listo para abrir su LLC en Florida?', 'cta_text': 'Presentada dentro de 1 día hábil de recibir la información completa.',
        'detail_side_services': 'Nuestros servicios', 'detail_side_contact': 'Contacto', 'detail_includes': 'Qué incluye',
        'detail_faq': 'Preguntas sobre', 'home': 'Inicio', 'order_service': 'Elija un servicio', 'order_ra': 'Agente registrado',
        'order_ra_none': 'Ya tengo un agente registrado en Florida', 'order_ra_month': '$13.99 al mes', 'order_ra_year': '$169 al año',
        'order_ein': 'Agregar EIN ($95)', 'order_details': 'Sus datos', 'order_item': 'Concepto',
        'reply_hours': 'Respondemos dentro de 1 día hábil', 'not_found': 'Página no encontrada', 'not_found_text': 'La página que busca cambió de lugar o no existe.',
        'back_home': 'Volver al inicio', 'legal_note': 'Este texto es un borrador pendiente de revisión legal. La versión en español está en preparación.',
        'menu': 'Menú', 'switch': 'English', 'values_eyebrow': 'Por qué Diler Services',
        'values_title': 'Tranquilos, precisos y <span>bilingües.</span>',
    },
}

PAGES = {
    'home': 'index.html', 'services': 'services.html', 'pricing': 'pricing.html', 'howItWorks': 'how-it-works.html',
    'about': 'about.html', 'faq': 'faq.html', 'contact': 'contact.html', 'order': 'order.html',
    'privacy': 'privacy.html', 'terms': 'terms.html', 'refundPolicy': 'refund-policy.html',
}


def svc_file(slug):
    return f'service-{slug}.html'


def rel(lang):
    return '' if lang == 'en' else '../'


def other_lang(lang):
    return 'es' if lang == 'en' else 'en'


def switch_href(lang, fname):
    return f'es/{fname}' if lang == 'en' else f'../{fname}'


def icon(name, white=False, cls='', size=40):
    p = '{R}' + f'assets/img/ds-icons/{name}{"-white" if white else ""}.svg'
    return f'<img src="{p}" alt="" width="{size}" height="{size}" class="{cls}">'


# ---------------------------------------------------------------- chrome
def head(lang, title, desc, fname):
    t = T[lang]
    full = f'{title} | Diler Services' if 'Diler' not in title else title
    alt_en = f'{SITE}/{fname}'
    alt_es = f'{SITE}/es/{fname}'
    return f'''<!DOCTYPE html>
<html lang="{lang}" class="ds-v3">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{{R}}assets/brand/og-{lang}.png">
<meta property="og:type" content="website">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="es" href="{alt_es}">
<link rel="alternate" hreflang="x-default" href="{alt_en}">
<link rel="icon" href="{{R}}assets/brand/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{{R}}assets/brand/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{{R}}assets/brand/apple-touch-icon-180.png">
<link rel="stylesheet" href="{{R}}assets/css/plugins/bootstrap.min.css">
<link rel="stylesheet" href="{{R}}assets/css/plugins/swiper.bundle.css">
<link rel="stylesheet" href="{{R}}assets/css/plugins/fontawesome.css">
<link rel="stylesheet" href="{{R}}assets/css/plugins/mobile-menu.css">
<link rel="stylesheet" href="{{R}}assets/css/plugins/owl.carousel.min.css">
<link rel="stylesheet" href="{{R}}assets/css/plugins/aos.css">
<link rel="stylesheet" href="{{R}}assets/css/plugins/nice-select.css">
<link rel="stylesheet" href="{{R}}assets/css/typography.css">
<link rel="stylesheet" href="{{R}}assets/css/comon.css">
<link rel="stylesheet" href="{{R}}assets/css/animation.css">
<link rel="stylesheet" href="{{R}}assets/css/master.css">
<link rel="stylesheet" href="{{R}}assets/css/diler-v3.css">
<script src="{{R}}assets/js/plugins/jquery-3-6-0.min.js"></script>
</head>
<body>
<a class="ds-skip" href="#main">{e(t["nav"]["skipToContent"])}</a>
<div class="paginacontainer"><div class="progress-wrap"><svg class="progress-circle svg-content" width="100%" height="100%" viewBox="-1 -1 102 102"><path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98"/></svg></div></div>
'''


def nav_items(lang):
    t = T[lang]['nav']
    return [('services', t['services']), ('pricing', t['pricing']), ('howItWorks', t['howItWorks']), ('about', t['about']), ('faq', t['faq']), ('contact', t['contact'])]


def header(lang, active, fname):
    t = T[lang]
    x = X[lang]
    lis = []
    for key, label in nav_items(lang):
        cls = ' class="ds-active"' if key == active else ''
        if key == 'services':
            sub = ''.join(f'<li><a href="{svc_file(s["slug"])}">{e(L(lang, s["name"]))}</a></li>' for s in SERVICES)
            lis.append(f'<li><a href="{PAGES[key]}"{cls}>{e(label)} <i class="fa-solid fa-angle-down"></i></a><ul>{sub}</ul></li>')
        else:
            lis.append(f'<li><a href="{PAGES[key]}"{cls}>{e(label)}</a></li>')
    lis.append(f'<li><a class="ds-lang" href="{switch_href(lang, fname)}" hreflang="{other_lang(lang)}" lang="{other_lang(lang)}">{other_lang(lang).upper()}</a></li>')
    mob = []
    for key, label in nav_items(lang):
        if key == 'services':
            sub = ''.join(f'<li><a href="{svc_file(s["slug"])}">{e(L(lang, s["name"]))}</a></li>' for s in SERVICES)
            mob.append(f'<li><a href="{PAGES[key]}">{e(label)}</a><ul class="sub-menu">{sub}</ul></li>')
        else:
            mob.append(f'<li><a href="{PAGES[key]}">{e(label)}</a></li>')
    mob.append(f'<li><a href="{switch_href(lang, fname)}" hreflang="{other_lang(lang)}">{e(x["switch"])}</a></li>')
    logo = '<img src="{R}assets/brand/DS-horizontal_full.svg" alt="Diler Services" width="182" height="48" class="ds-logo">'
    return f'''<header>
<div class="header-area-home1 d-none d-lg-block"><div class="container"><div class="row"><div class="col-12"><div class="header-elements">
<div class="site-logo"><a href="index.html" aria-label="Diler Services">{logo}</a></div>
<div class="main-menu-ex"><ul>{''.join(lis)}</ul></div>
<div class="cta-btn d-none d-lg-block btn-after button action-btn home1-header-btn"><a href="{PAGES['order']}">{e(t['nav']['cta'])}</a></div>
</div></div></div></div></div>
</header>
<div class="mobile-header mobile-header-4 d-block d-lg-none"><div class="container-fluid"><div class="col-12"><div class="mobile-header-elements">
<div class="mobile-logo"><a href="index.html" aria-label="Diler Services">{logo}</a></div>
<div class="mobile-nav-icon" role="button" tabindex="0" aria-label="{e(x['menu'])}"><i class="fa-solid fa-bars"></i></div>
</div></div></div></div>
<div class="mobile-sidebar">
<div class="menu-close" role="button" tabindex="0" aria-label="{e(t['nav']['closeMenu'])}"><i class="fa-solid fa-xmark"></i></div>
<div class="mobile-nav"><ul class="mobile-nav-list">{''.join(mob)}</ul>
<div class="ds-mobile-cta"><a class="ds-btn" href="{PAGES['order']}">{e(t['common']['startLlc'])}</a></div>
</div></div>
'''


def footer(lang):
    t = T[lang]
    f = t['footer']
    svc = ''.join(f'<li><a href="{svc_file(s["slug"])}">{e(L(lang, s["name"]))}</a></li>' for s in SERVICES[:6])
    company = ''.join(f'<li><a href="{PAGES[k]}">{e(lbl)}</a></li>' for k, lbl in [('about', t['nav']['about']), ('howItWorks', t['nav']['howItWorks']), ('pricing', t['nav']['pricing']), ('faq', t['nav']['faq']), ('contact', t['nav']['contact'])])
    legal = ''.join(f'<li><a href="{PAGES[k]}">{e(lbl)}</a></li>' for k, lbl in [('privacy', f['privacy']), ('terms', f['terms']), ('refundPolicy', f['refund'])])
    tr = f'<p>{e(f["disclaimerTranslation"])}</p>' if f['disclaimerTranslation'] else ''
    return f'''<div class="footer sec-padding"><div class="container"><div class="row">
<div class="col-lg-4 col-md-12"><div class="footer-hadding">
<a href="index.html"><img src="{{R}}assets/brand/DS-horizontal_reversed.svg" alt="Diler Services" width="182" height="48" class="ds-logo"></a>
<p>{e(t['site']['tagline'])}</p>
</div></div>
<div class="col-lg-3 col-md-4"><div class="footer-menu"><h4>{e(f['servicesHeading'])}</h4><ul>{svc}</ul></div></div>
<div class="col-lg-2 col-md-4"><div class="footer-menu"><h4>{e(f['companyHeading'])}</h4><ul>{company}</ul></div></div>
<div class="col-lg-3 col-md-4"><div class="footer-menu"><h4>{e(f['contactHeading'])}</h4>
<div class="foter-contact"><div class="footer-contact-icon">{icon('mail', True, size=20)}</div><div class="footer-contact-p"><a href="mailto:{EMAIL}"><p>{EMAIL}</p></a></div></div>
<div class="foter-contact"><div class="footer-contact-icon">{icon('languages', True, size=20)}</div><div class="footer-contact-p"><p>{e(f['languages'])}</p></div></div>
<h4 class="ds-legal-h">{e(f['legalHeading'])}</h4><ul>{legal}</ul>
</div></div>
</div></div></div>
<div class="fonter-end"><div class="container"><div class="row"><div class="col-md-12"><div class="footer-end-p ds-footer-end">
<div><p class="ds-disclaimer">{e(f['disclaimer'])}</p>{tr}</div>
<p>&copy; 2026 Diler Services LLC. {e(f['rights'])}</p>
</div></div></div></div></div>
<script src="{{R}}assets/js/plugins/bootstrap.min.js"></script>
<script src="{{R}}assets/js/plugins/swiper.bundle.js"></script>
<script>window.ModalVideo=window.ModalVideo||function(){{}};window.AOS=window.AOS||{{init:function(){{}},refresh:function(){{}}}};if(window.jQuery&&!jQuery.fn.countUp){{jQuery.fn.countUp=function(){{return this;}};}}</script>
<script src="{{R}}assets/js/plugins/mobile-menu.js"></script>
<script src="{{R}}assets/js/plugins/jquery.nice-select.js"></script>
<script src="{{R}}assets/js/plugins/owl.carousel.min.js"></script>
<script src="{{R}}assets/js/main.js"></script>
<script src="{{R}}assets/js/diler-v3.js"></script>
</body>
</html>
'''


def inner_hero(lang, title, lead=''):
    x = X[lang]
    sub = f'<p class="ds-hero-lead">{e(lead)}</p>' if lead else ''
    return f'''<div class="inner-page-hero-area _relative"><div class="container"><div class="row"><div class="col-lg-8 m-auto text-center">
<div class="hadding hadding-sec"><h1>{e(title)}</h1>{sub}<h6><a href="index.html">{e(x['home'])}</a> &rsaquo; {e(title)}</h6></div>
</div></div></div>{folio_svg('ds-inner-folio')}</div>
'''


def folio_svg(cls):
    return f'''<svg class="{cls}" viewBox="0 0 600 600" fill="none" aria-hidden="true" focusable="false"><path d="M240 60h40a240 240 0 0 1 0 480h-40z" fill="#E4EDFD"/><path d="M180 100h40a200 200 0 0 1 0 400h-40z" fill="#EFF4FE"/><path d="M120 140h40a160 160 0 0 1 0 320h-40z" fill="#E4EDFD"/><rect x="60" y="292" width="480" height="16" fill="#ffffff"/></svg>'''


def btn(href, label, kind=1):
    return f'<div class="header-btn-{kind} button btn-after home1-button"><a href="{href}">{e(label)}</a></div>'


# ---------------------------------------------------------------- sections
def hero(lang):
    t = T[lang]['home']
    c = T[lang]['common']
    status = ''.join(f'<li><span class="ds-dot{" ds-dot-sand" if i == 3 else ""}"></span>{e(s)}</li>' for i, s in enumerate(t['status']))
    return f'''<div class="hero-area ds-hero"><div class="container"><div class="row align-items-center">
<div class="col-md-12 col-lg-6" data-aos="fade-right" data-aos-duration="800"><div class="main-hadding hadding-p">
<span class="span ds-eyebrow">{e(t['eyebrow'])}</span>
<h1>{e(t['h1a'])}<br><span>{e(t['h1b'])}</span></h1>
<p>{e(t['lead'])}</p>
<div class="home1-header-button">{btn(PAGES['order'], c['startLlc'], 1)}{btn(PAGES['contact'], c['talkToUs'], 2)}</div>
</div></div>
<div class="col-md-12 col-lg-6"><div class="ds-hero-visual" data-aos="fade-left" data-aos-duration="800">
{folio_svg('ds-hero-folio')}
<div class="ds-status-card"><p class="ds-card-label">{e(t['statusLabel'])}</p><p class="ds-card-title">{e(t['statusName'])}</p><ul>{status}</ul></div>
<div class="ds-filed-card"><p>{e(t['filedWithin'])}</p><strong>{e(t['filedValue'])}</strong><small>{e(t['filedNote'])}</small></div>
</div></div>
</div></div></div>
'''


def facts(lang):
    cols = ''
    for i, (num, label) in enumerate(X[lang]['facts']):
        ic = ['clock', 'badge-check', 'building-2', 'file-text'][i]
        cols += f'''<div class="col-lg-3 col-md-6 text-center" data-aos="fade-up" data-aos-duration="{800 + 200 * i}"><div class="box-before"><div class="fact-box">
<div class="fact-icon">{icon(ic)}</div><h1>{e(num)}</h1><p>{e(label)}</p></div></div></div>'''
    return f'<div class="our-fact sec-padding _relative"><div class="container"><div class="row">{cols}</div></div></div>\n'


def about_block(lang, photo='consultation-1'):
    x = X[lang]
    checks = x['about_checks']
    col = lambda items: ''.join(f'<div class="chek-list"><p>{icon("check", size=20)} {e(i)}</p></div><div class="space20"></div>' for i in items)
    return f'''<div class="about sec-padding"><div class="container"><div class="row align-items-center">
<div class="col-md-6" data-aos="fade-right" data-aos-duration="800"><div class="about-img img-border"><img src="{{R}}assets/photos/{photo}.webp" alt="" width="1200" height="800" loading="lazy"></div></div>
<div class="col-md-6 space-sm-30" data-aos="fade-left" data-aos-duration="800"><div class="about-haddings">
<div class="hadding hadding-p"><span class="span">{e(x['about_eyebrow'])}</span><h1>{x['about_title']}</h1><p>{e(x['about_text'])}</p></div>
<div class="check-list-all"><div class="row"><div class="col-md-6">{col(checks[:2])}</div><div class="col-md-6">{col(checks[2:])}</div></div></div>
{btn(PAGES['about'], x['about_cta'], 1)}
</div></div></div></div></div>
'''


def service_card(lang, s, i):
    x = X[lang]
    return f'''<div class="col-md-6 col-lg-3" data-aos="fade-up" data-aos-duration="{700 + 100 * (i % 4)}"><div class="box-after ds-card-h"><div class="service-box hadding hadding-p">
{icon(s['icon'])}<div class="space20"></div><h2><a href="{svc_file(s['slug'])}">{e(L(lang, s['name']))}</a></h2>
<p class="ds-price">{e(s['price'])} <span>{e(L(lang, s['priceNote']))}</span></p>
<p>{e(L(lang, s['summary']))}</p><div class="space20"></div>
<div class="read-more-btn"><a href="{svc_file(s['slug'])}">{e(x['services_more'])} <i class="fa-solid fa-arrow-right"></i></a></div>
</div></div></div>'''


def services_block(lang, with_head=True):
    t = T[lang]['home']
    headblock = f'''<div class="row"><div class="col-lg-7 m-auto text-center" data-aos="fade-down" data-aos-duration="800"><div class="hadding hadding-p">
<span class="span">{e(t['servicesEyebrow'])}</span><h1>{e(t['servicesTitle'])}</h1><p>{e(t['servicesLead'])}</p></div></div></div><div class="space20"></div>''' if with_head else ''
    cards = ''.join(service_card(lang, s, i) for i, s in enumerate(SERVICES))
    return f'<div class="service sec-padding"><div class="container">{headblock}<div class="row">{cards}</div></div></div>\n'


def steps_block(lang, photo='mailbox-1'):
    t = T[lang]['home']
    items = ''
    for i, st in enumerate(C['steps'][lang]):
        items += f'''<div class="work-item" data-aos="fade-right" data-aos-duration="{900 + 150 * i}"><div><div class="work-icon ds-step-num">{i + 1:02d}</div></div>
<div class="hadding hadding-p"><h2>{e(st['title'])}</h2><p>{e(st['text'])}</p></div></div>'''
    return f'''<div class="works sec-padding"><div class="container"><div class="row align-items-center">
<div class="col-md-12 col-lg-6"><div class="how-in-work-sec">
<div class="hadding hadding-p" data-aos="fade-right" data-aos-duration="800"><span class="span">{e(t['stepsEyebrow'])}</span><h1>{e(t['stepsTitle'])}</h1><p>{e(X[lang]['steps_text'])}</p></div>
<div class="space20"></div><div class="works-items">{items}</div></div></div>
<div class="col-md-12 col-lg-6" data-aos="fade-left" data-aos-duration="800"><div class="works-img space-sm-50 img-border"><img src="{{R}}assets/photos/{photo}.webp" alt="" width="1200" height="800" loading="lazy"></div></div>
</div></div></div>
'''


def values_block(lang):
    x = X[lang]
    cols = ''.join(f'''<div class="col-md-6 col-lg-3" data-aos="fade-up" data-aos-duration="{800 + 150 * i}"><div class="ds-value">{icon(v['icon'])}<h3>{e(v['title'])}</h3><p>{e(v['text'])}</p></div></div>''' for i, v in enumerate(C['values'][lang]))
    return f'''<div class="ds-values sec-padding"><div class="container"><div class="row"><div class="col-lg-7 m-auto text-center"><div class="hadding hadding-p">
<span class="span">{e(x['values_eyebrow'])}</span><h1>{x['values_title']}</h1></div></div></div><div class="space30"></div><div class="row">{cols}</div></div></div>
'''


def pricing_block(lang, with_head=True, with_others=False):
    t = T[lang]
    x = X[lang]
    boxes = ''
    for i, slug in enumerate(C['featuredPlans']):
        s = next(v for v in SERVICES if v['slug'] == slug)
        feat = ' ds-featured' if slug == 'formation-bundle' else ''
        lis = ''.join(f'<li>{icon("check", size=20)} {e(p)}</li>' for p in s['detail']['includes'][lang][:5])
        boxes += f'''<div class="col-md-6 col-lg-4" data-aos="fade-up" data-aos-duration="{800 + 200 * i}"><div class="price-box box-after{feat}"><div class="hadding hadding-p single-price">
<h2>{e(L(lang, s['name']))}</h2><p>{e(L(lang, s['summary']))}</p><div class="space20"></div>
<h2 class="ds-plan-price">{e(s['price'])}</h2><p>{e(L(lang, s['priceNote']))}</p><div class="space20"></div>
<div class="price-button btn-after-price"><div class="button price-btn text-center"><a href="{PAGES['order']}?service={slug}">{e(t['common']['orderNow'])}</a></div></div>
<div class="space30"></div><div class="price-list"><ul>{lis}</ul></div>
</div></div></div>'''
    headblock = f'''<div class="row"><div class="col-lg-7 m-auto text-center" data-aos="fade-up" data-aos-duration="800"><div class="hadding hadding-p">
<span class="span">{e(t['home']['plansEyebrow'])}</span><h1>{e(t['home']['plansTitle'])}</h1><p>{e(x['pricing_note'])}</p></div></div></div><div class="space30"></div>''' if with_head else ''
    others = ''
    if with_others:
        rows = ''.join(f'<tr><th scope="row"><a href="{svc_file(s["slug"])}">{e(L(lang, s["name"]))}</a></th><td>{e(s["price"])}</td><td>{e(L(lang, s["priceNote"]))}</td></tr>' for s in SERVICES if s['slug'] not in C['featuredPlans'])
        others = f'''<div class="space60"></div><div class="row"><div class="col-lg-9 m-auto"><div class="hadding hadding-p text-center"><h2 class="ds-h2">{e(x['other_services'])}</h2><p>{e(x['other_services_text'])}</p></div>
<div class="ds-table-wrap"><table class="ds-table"><tbody>{rows}</tbody></table></div></div></div>'''
    return f'<div class="pricing-plan sec-padding"><div class="container">{headblock}<div class="row">{boxes}</div>{others}</div></div>\n'


def faq_block(lang, items, title, uid='f', half=True):
    def acc(sub, k):
        out = ''
        for j, it in enumerate(sub):
            n = f'{uid}{k}{j}'
            first = j == 0
            out += f'''<div class="accordion-item"><h2 class="accordion-header{' active-header' if first else ''}" id="h-{n}">
<button class="accordion-button{' accordion-button-active' if first else ' collapsed'}" type="button" data-bs-toggle="collapse" data-bs-target="#c-{n}" aria-expanded="{'true' if first else 'false'}" aria-controls="c-{n}">{e(it['q'])}</button></h2>
<div id="c-{n}" class="accordion-collapse collapse{' show' if first else ''}" aria-labelledby="h-{n}" data-bs-parent="#acc-{uid}{k}"><div class="accordion-body">{e(it['a'])}</div></div></div>'''
        return f'<div class="accordion" id="acc-{uid}{k}">{out}</div>'
    if half and len(items) > 1:
        mid = (len(items) + 1) // 2
        body = f'<div class="row"><div class="col-md-6">{acc(items[:mid], "a")}</div><div class="col-md-6">{acc(items[mid:], "b")}</div></div>'
    else:
        body = f'<div class="row"><div class="col-lg-9 m-auto">{acc(items, "a")}</div></div>'
    return f'''<div class="faq-pricing-plan sec-padding ds-faq"><div class="container"><div class="row"><div class="col-md-12 text-center"><div class="hadding hadding-p"><h1>{title}</h1></div></div></div>
<div class="space30"></div>{body}</div></div>
'''


def contact_form(lang, subject='Website question'):
    f = T[lang]['form']
    opts = ''.join(f'<option value="{e(L("en", s["name"]))}">{e(L(lang, s["name"]))}</option>' for s in SERVICES)
    return f'''<form class="ds-form" method="POST" action="https://api.web3forms.com/submit">
<input type="hidden" name="access_key" value="{FORM_KEY}"><input type="hidden" name="subject" value="{e(subject)}"><input type="hidden" name="Language" value="{lang}">
<input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off">
<div class="contact-form"><div class="contact-from-input">
<label class="visually-hidden" for="cf-name-{subject[:4]}">{e(f['name'])}</label><input id="cf-name-{subject[:4]}" type="text" name="Name" placeholder="{e(f['name'])} *" required autocomplete="name">
<label class="visually-hidden" for="cf-email-{subject[:4]}">{e(f['email'])}</label><input id="cf-email-{subject[:4]}" type="email" name="Email" placeholder="{e(f['email'])} *" required autocomplete="email">
</div><div class="contact-from-input">
<label class="visually-hidden" for="cf-biz-{subject[:4]}">{e(f['business'])}</label><input id="cf-biz-{subject[:4]}" type="text" name="Business" placeholder="{e(f['business'])}" autocomplete="organization">
<label class="visually-hidden" for="cf-svc-{subject[:4]}">{e(f['service'])}</label><select id="cf-svc-{subject[:4]}" name="Service" class="ds-native"><option value="">{e(f['service'])}</option>{opts}</select>
</div><div class="contact-from-input"><label class="visually-hidden" for="cf-msg-{subject[:4]}">{e(f['message'])}</label><textarea id="cf-msg-{subject[:4]}" name="Message" rows="4" placeholder="{e(f['message'])} *" required></textarea></div>
<div class="space20"></div><div class="button btn-after contact-form-btn"><button type="submit" data-sending="{e(f['sending'])}">{e(f['send'])}</button></div>
<p class="ds-form-msg" role="status" data-ok="{e(f['sent'])}" data-err="{e(f['error'])}"></p>
</div></form>'''


def contact_block(lang, photo='founder-laptop-2'):
    x = X[lang]
    return f'''<div class="contact sec-padding"><div class="container"><div class="row align-items-center">
<div class="col-md-6" data-aos="fade-right" data-aos-duration="800"><div class="contact-img img-border"><img src="{{R}}assets/photos/{photo}.webp" alt="" width="1200" height="800" loading="lazy"></div></div>
<div class="col-md-6 space-sm-30" data-aos="fade-left" data-aos-duration="800"><div class="hadding hadding-p"><span class="span">{e(x['contact_us'])}</span><h1>{x['contact_title']}</h1><p>{e(x['contact_text'])}</p></div>
<div class="space30"></div>{contact_form(lang)}</div>
</div></div></div>
'''


def cta_band(lang):
    t = T[lang]
    x = X[lang]
    return f'''<div class="subsraibe sec-padding ds-cta"><div class="container"><div class="row align-items-center">
<div class="col-lg-7"><div class="subsraibe-hadding"><h1>{e(x['cta_title'])}</h1><p>{e(x['cta_text'])}</p></div></div>
<div class="col-lg-5"><div class="ds-cta-btns space-sm-30">{btn(PAGES['order'], t['common']['startLlc'], 1)}{btn(PAGES['contact'], t['common']['talkToUs'], 2)}</div></div>
</div></div></div>
'''


# ---------------------------------------------------------------- pages
def page(lang, fname, title, desc, body, active=None):
    r = rel(lang)
    out = head(lang, title, desc, fname) + header(lang, active, fname) + '<main id="main">' + body + '</main>' + footer(lang)
    out = out.replace('{R}', r)
    # No scroll-animation dependency: content is always visible.
    out = re.sub(r'\s+data-aos(-[a-z]+)?="[^"]*"', '', out)
    d = OUT if lang == 'en' else os.path.join(OUT, 'es')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, fname), 'w', encoding='utf-8').write(out)


def all_faq(lang):
    return [i for g in C['faq'][lang] for i in g['items']]


def faq_by_id(lang, ids):
    a = {i['id']: i for i in all_faq(lang)}
    return [a[i] for i in ids if i in a]


def legal_html(path):
    s = open(os.path.join(REPO, path), encoding='utf-8').read()
    i = s.find('<div class="ds-article">')
    if i < 0:
        return ''
    depth, j = 0, i
    for m in re.finditer(r'<(/?)div\b[^>]*>', s[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            j = i + m.end()
            break
    body = s[i:j]
    body = re.sub(r'\sclass="[^"]*"', '', body)
    body = body.replace('info@toromovers.com', EMAIL)
    body = re.sub(r'href="/([a-z-]+)/"', lambda m: f'href="{ {"privacy-policy": "privacy.html", "terms-of-service": "terms.html", "refund-policy": "refund-policy.html", "contact": "contact.html", "order": "order.html"}.get(m.group(1), "index.html") }"', body)
    return body


def order_block(lang):
    t = T[lang]
    f = t['form']
    x = X[lang]
    radios = ''
    for i, s in enumerate(SERVICES):
        if s['slug'] == 'registered-agent':
            continue
        fee = {'llc-formation': 89, 'formation-bundle': 174, 'ein-filing': 95, 'annual-report': 99, 'dba': 129, 'amendment': 99, 'reinstatement': 299}[s['slug']]
        state = {'llc-formation': 125, 'formation-bundle': 125}.get(s['slug'], '')
        radios += f'''<label class="ds-radio"><input type="radio" name="Service" value="{e(L('en', s['name']))}" data-slug="{s['slug']}" data-fee="{fee}" data-state="{state}" data-label="{e(L(lang, s['name']))}"{' checked' if i == 0 else ''}>
<span><b>{e(L(lang, s['name']))}</b><small>{e(s['price'])} {e(L(lang, s['priceNote']))}</small></span></label>'''
    ra = f'''<label class="ds-radio"><input type="radio" name="Registered agent" value="None" data-fee="0" data-label="" checked><span><b>{e(x['order_ra_none'])}</b></span></label>
<label class="ds-radio"><input type="radio" name="Registered agent" value="Monthly" data-fee="13.99" data-label="{e(x['order_ra'])} ({e(x['order_ra_month'])})"><span><b>{e(x['order_ra'])}</b><small>{e(x['order_ra_month'])}</small></span></label>
<label class="ds-radio"><input type="radio" name="Registered agent" value="Yearly" data-fee="169" data-label="{e(x['order_ra'])} ({e(x['order_ra_year'])})"><span><b>{e(x['order_ra'])}</b><small>{e(x['order_ra_year'])}</small></span></label>'''
    return f'''<div class="contact-page-contact sec-padding ds-order"><div class="container"><div class="row">
<div class="col-lg-7"><form class="ds-form ds-order-form" method="POST" action="https://api.web3forms.com/submit">
<input type="hidden" name="access_key" value="{FORM_KEY}"><input type="hidden" name="subject" value="New order from the website"><input type="hidden" name="Language" value="{lang}">
<input type="hidden" name="Total due today" data-f="total"><input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off">
<fieldset><legend class="ds-legend">1. {e(x['order_service'])}</legend><div class="ds-radio-grid">{radios}</div>
<label class="ds-check"><input type="checkbox" name="Add EIN filing" value="Yes" data-fee="95" data-ein> <span>{e(x['order_ein'])}</span></label></fieldset>
<fieldset><legend class="ds-legend">2. {e(x['order_ra'])}</legend><div class="ds-radio-grid ds-radio-grid-3">{ra}</div></fieldset>
<fieldset><legend class="ds-legend">3. {e(x['order_details'])}</legend><div class="contact-form">
<div class="contact-from-input"><label class="visually-hidden" for="o-name">{e(f['name'])}</label><input id="o-name" type="text" name="Name" placeholder="{e(f['name'])} *" required autocomplete="name">
<label class="visually-hidden" for="o-email">{e(f['email'])}</label><input id="o-email" type="email" name="Email" placeholder="{e(f['email'])} *" required autocomplete="email"></div>
<div class="contact-from-input"><label class="visually-hidden" for="o-notes">{e(f['orderNotes'])}</label><textarea id="o-notes" name="Details" rows="4" placeholder="{e(f['orderNotes'])}"></textarea></div>
<label class="ds-check"><input type="checkbox" name="Accepted terms" value="Yes" required> <span>{e(f['consent'])} <a href="{PAGES['terms']}">{e(t['footer']['terms'])}</a> · <a href="{PAGES['refundPolicy']}">{e(t['footer']['refund'])}</a></span></label>
<p class="ds-paynote">{e(f['payNote'])}</p>
<div class="button btn-after contact-form-btn"><button type="submit" data-sending="{e(f['sending'])}">{e(f['orderSend'])}</button></div>
<p class="ds-form-msg" role="status" data-ok="{e(f['orderSent'])}" data-err="{e(f['error'])}"></p>
</div></fieldset></form></div>
<div class="col-lg-5"><aside class="ds-summary" aria-live="polite"><h2>{e(f['summary'])}</h2>
<table class="ds-sum"><thead><tr><th>{e(x['order_item'])}</th><th>{e(f['ourFee'])}</th><th>{e(f['stateFeeCol'])}</th></tr></thead><tbody data-f="rows"></tbody>
<tfoot><tr><th>{e(f['total'])}</th><td colspan="2" data-f="sum"></td></tr></tfoot></table>
<p class="ds-sum-note">{e(t['common']['stateFee'])}</p>
<p class="ds-sum-note" data-at-cost="{e(f['atCost'])}"></p>
<div class="ds-sum-mail">{icon('mail', size=24)}<a href="mailto:{EMAIL}">{EMAIL}</a></div>
</aside></div>
</div></div></div>
'''


def detail_block(lang, s):
    t = T[lang]
    x = X[lang]
    side = ''.join(f'<li><a href="{svc_file(o["slug"])}"{" class=ds-active" if o["slug"] == s["slug"] else ""}>{e(L(lang, o["name"]))} <i class="fa-solid fa-angle-right"></i></a></li>' for o in SERVICES)
    inc = ''.join(f'<li>{icon("check", size=20)} {e(p)}</li>' for p in s['detail']['includes'][lang])
    photo = {'registered-agent': 'mailbox-1', 'reinstatement': 'opening-mail-2', 'annual-report': 'signing-documents-2', 'ein-filing': 'founder-laptop-1', 'formation-bundle': 'consultation-1', 'llc-formation': 'founder-laptop-2', 'dba': 'office-plants-1', 'amendment': 'consultation-2'}[s['slug']]
    return f'''<div class="service-details sec-padding"><div class="container"><div class="row">
<div class="col-lg-4 order-2 order-lg-1">
<div class="details-box"><div class="hadding details-hadding"><h2>{e(x['detail_side_services'])}</h2></div><div class="service-details-list"><ul>{side}</ul></div></div>
<div class="details-box"><div class="hadding details-hadding"><h2>{e(x['detail_side_contact'])}</h2></div>
<div class="contact-details-1"><div class="contact-details-icon">{icon('mail', size=24)}</div><div class="contact-details-p hadding-p"><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>{e(x['reply_hours'])}</p></div></div></div>
</div>
<div class="col-lg-8 order-1 order-lg-2"><div class="ds-detail">
<div class="img-border ds-detail-img"><img src="{{R}}assets/photos/{photo}.webp" alt="" width="1200" height="800"></div>
<div class="hadding hadding-p"><h1>{e(L(lang, s['name']))}</h1><p class="ds-detail-price">{e(s['price'])} <span>{e(L(lang, s['priceNote']))}</span></p>
<p>{e(L(lang, s['detail']['lead']))}</p><p>{e(L(lang, s['detail']['second']))}</p></div>
<div class="ds-detail-cta">{btn(PAGES['order'] + '?service=' + (s['slug'] if s['slug'] != 'registered-agent' else 'registered-agent'), t['common']['orderNow'], 1)}</div>
<div class="hadding hadding-p"><h2 class="ds-h2">{e(x['detail_includes'])}</h2></div><div class="price-list ds-includes"><ul>{inc}</ul></div>
</div></div>
</div></div></div>
'''


def build(lang):
    t = T[lang]
    x = X[lang]
    p = t['pages']
    page(lang, 'index.html', x['home_title'], t['site']['description'],
         hero(lang) + facts(lang) + about_block(lang) + services_block(lang) + steps_block(lang) + pricing_block(lang)
         + faq_block(lang, faq_by_id(lang, ['llc-outside', 'llc-time', 'ra-what', 'price-refund', 'about-law', 'price-name']), t['home']['faqTitle'], 'h')
         + contact_block(lang) + cta_band(lang), 'home')
    page(lang, 'services.html', p['services']['title'], p['services']['lead'], inner_hero(lang, p['services']['title'], p['services']['lead']) + services_block(lang, False) + pricing_block(lang) + cta_band(lang), 'services')
    page(lang, 'pricing.html', p['pricing']['title'], p['pricing']['lead'], inner_hero(lang, p['pricing']['title'], p['pricing']['lead']) + pricing_block(lang, False, True)
         + faq_block(lang, C['faq'][lang][3]['items'], C['faq'][lang][3]['title'], 'p') + cta_band(lang), 'pricing')
    page(lang, 'how-it-works.html', p['howItWorks']['title'], p['howItWorks']['lead'], inner_hero(lang, p['howItWorks']['title'], p['howItWorks']['lead']) + steps_block(lang, 'opening-mail-2')
         + faq_block(lang, faq_by_id(lang, ['llc-info', 'llc-time', 'llc-included', 'ein-when']), t['common']['questions'], 'w') + cta_band(lang), 'howItWorks')
    ab = t['about']
    about_cols = ''.join(f'<div class="col-md-6" data-aos="fade-up" data-aos-duration="{800 + 150 * i}"><div class="ds-about-col"><h3>{e(ab[k + "Title"])}</h3><p>{e(ab[k + "Text"])}</p></div></div>' for i, k in enumerate(['who', 'what', 'approach', 'commit']))
    page(lang, 'about.html', p['about']['title'], p['about']['lead'], inner_hero(lang, p['about']['title'], p['about']['lead']) + about_block(lang, 'consultation-2')
         + f'<div class="ds-about-grid sec-padding"><div class="container"><div class="row">{about_cols}</div></div></div>' + values_block(lang) + cta_band(lang), 'about')
    faqs = ''.join(faq_block(lang, g['items'], g['title'], f'q{i}') for i, g in enumerate(C['faq'][lang]))
    page(lang, 'faq.html', p['faq']['title'], p['faq']['lead'], inner_hero(lang, p['faq']['title'], p['faq']['lead']) + faqs + cta_band(lang), 'faq')
    page(lang, 'contact.html', p['contact']['title'], p['contact']['lead'], inner_hero(lang, p['contact']['title'], p['contact']['lead']) + contact_block(lang, 'consultation-1'), 'contact')
    page(lang, 'order.html', p['order']['title'], p['order']['lead'], inner_hero(lang, p['order']['title'], p['order']['lead']) + order_block(lang))
    for s in SERVICES:
        name = L(lang, s['name'])
        page(lang, svc_file(s['slug']), name, L(lang, s['summary']), inner_hero(lang, name) + detail_block(lang, s)
             + faq_block(lang, faq_by_id(lang, s['faq']), f"{x['detail_faq']} {name}", 'd', True) + cta_band(lang), 'services')
    for key, src in [('privacy', 'privacy-policy/index.html'), ('terms', 'terms-of-service/index.html'), ('refundPolicy', 'refund-policy/index.html')]:
        title = p[key]['title']
        page(lang, PAGES[key], title, title, inner_hero(lang, title) + f'<div class="sec-padding"><div class="container"><div class="row"><div class="col-lg-8 m-auto"><p class="ds-legal-note">{e(x["legal_note"])}</p><div class="ds-prose">{legal_html(src)}</div></div></div></div></div>')
    page(lang, '404.html', x['not_found'], x['not_found_text'], f'''<div class="error-page-hero-area ds-404"><div class="container"><div class="row"><div class="col-lg-7 m-auto text-center"><div class="hadding hadding-p">
<p class="ds-404-num">404</p><h1>{e(x['not_found'])}</h1><p>{e(x['not_found_text'])}</p><div class="space30"></div><div class="ds-cta-btns justify-content-center">{btn('index.html', x['back_home'], 1)}</div></div></div></div></div></div>''')


if __name__ == '__main__':
    for lang in ('en', 'es'):
        build(lang)
    print('built', len([f for f in os.listdir(OUT) if f.endswith('.html')]), 'EN pages and', len([f for f in os.listdir(os.path.join(OUT, 'es')) if f.endswith('.html')]), 'ES pages')
