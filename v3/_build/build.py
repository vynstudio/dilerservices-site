"""Builds the Diler Services proposal as a literal clone of the Vikinglab Consultore template.

Each output page starts from the template's own HTML (Home 1 for the home page, and the template's
about, service, service-details, pricing-plan, faq, contact, checkout and error pages). Sections,
layout, image placements, decorative shapes, AOS animations, sliders, counters, icons and spacing are
kept as shipped. Only three things change: the copy (Diler Services content plus the Semrush SEO copy),
the colours (Brand Kit v3, applied to the template's own CSS and art by assets.py) and the logo (Folio).

Run from the repository root:  python3 v3/_build/build.py
Needs beautifulsoup4, numpy, Pillow and fontTools (set DS_PYLIB to a folder holding fontTools if it is
not installed).
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bs4 import BeautifulSoup  # noqa: E402

import assets as A  # noqa: E402
from seo import ALT, BRAND, META, SERVICE_META, SERVICE_SECTIONS  # noqa: E402
from site_copy import COPY, EMAIL, PLAN_MATRIX, SERVICE_BLOCK2, SERVICE_ICON, SERVICE_PHOTOS  # noqa: E402

V3 = os.path.dirname(HERE)
REPO = os.path.dirname(V3)
TPL = os.path.join(HERE, 'template')
CONTENT = json.load(open(os.path.join(HERE, 'content.json'), encoding='utf-8'))
SERVICES = CONTENT['services']
SITE = 'https://dilerservices.com'
FORM_KEY = 'e2f8f8d8-34b9-425d-ad45-cba50184ec8e'  # Web3Forms public access key (same as the live site)
e = html.escape
PAGES = ['index', 'about', 'services', 'how-it-works', 'pricing', 'faq', 'contact', 'order', 'privacy', 'terms', 'refund-policy', '404']


def L(lang, d):
    return d[lang] if isinstance(d, dict) else d


def svc_file(slug):
    return f'service-{slug}.html'


def svc(slug):
    return next(s for s in SERVICES if s['slug'] == slug)


def faq_items(lang):
    return {i['id']: i for g in CONTENT['faq'][lang] for i in g['items']}


def alt(lang, name):
    return ALT[lang][name]


# ---------------------------------------------------------------- soup helpers
def frag(markup):
    return BeautifulSoup(markup, 'html.parser')


def q(root, css):
    el = root.select_one(css)
    assert el is not None, css
    return el


def qa(root, css, n=None):
    els = root.select(css)
    assert n is None or len(els) == n, (css, len(els), n)
    return els


def inner(el, markup):
    el.clear()
    for c in list(frag(markup).contents):
        el.append(c)


def text(el, s):
    el.clear()
    el.append(s)


def set_img(el, src, alt_text='', w=None, h=None):
    el['src'] = src
    el['alt'] = alt_text
    if w:
        el['width'], el['height'] = str(w), str(h)


def photo(el, name, w, h, alt_text):
    # cropped to the placeholder's exact size; no width/height attributes, as in the template markup
    set_img(el, A.crop(name, w, h), alt_text)


def retag(el, tag, cls):
    """Turn a template heading into another element and keep its look (see the .ds-h* twins in assets.py)."""
    el.name = tag
    el['class'] = (el.get('class') or []) + [cls]


def heading(sec, span=None, h=None, p=None, idx=0):
    """Fill the template's heading block: span.span eyebrow, highlighted title and lead paragraph."""
    box = qa(sec, '.hadding')[idx]
    if span is not None and box.select_one('span.span'):
        text(q(box, 'span.span'), span)
    if h is not None:
        inner(q(box, 'h1'), h)
    if p is not None:
        ps = box.find_all('p', recursive=False)
        if ps:
            inner(ps[0], p)
    return box


# ---------------------------------------------------------------- chrome
def nav_lists(lang):
    c = COPY[lang]
    services = [(svc_file(s['slug']), L(lang, s['name'])) for s in SERVICES]
    guides = [('how-it-works.html', c['nav_how']), (svc_file('llc-formation'), c['guide_llc']),
              (svc_file('registered-agent'), c['guide_ra']), (svc_file('ein-filing'), c['guide_ein'])]
    company = [('pricing.html', c['nav_pricing']), ('faq.html', c['nav_faq']), ('contact.html', c['nav_contact']), ('order.html', c['nav_order'])]
    return services, guides, company


def other_href(lang, fname):
    return f'es/{fname}' if lang == 'en' else f'../{fname}'


def lis(items):
    return ''.join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in items)


def header_html(lang, fname):
    c = COPY[lang]
    services, guides, company = nav_lists(lang)
    other = 'es' if lang == 'en' else 'en'
    logo = '<img src="assets/brand/DS-horizontal_full.svg" alt="Diler Services" width="174" height="46">'
    nav_label = 'Main navigation' if lang == 'en' else 'Navegación principal'
    return f'''<!--=====HEADER START=======-->
  <header>
    <div class="header-area-home1 d-none d-lg-block">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <div class="header-elements">
              <div class="site-logo">
                <a href="index.html">{logo}</a>
              </div>
              <nav class="main-menu-ex" aria-label="{nav_label}">
                <ul>
                  <li><a href="index.html">{e(c['nav_home'])}</a></li>
                  <li><a href="about.html">{e(c['nav_about'])}</a></li>
                  <li><a href="services.html">{e(c['nav_services'])} <i class="fa-solid fa-angle-down"></i></a>
                    <ul>{lis(services)}</ul>
                  </li>
                  <li><a href="how-it-works.html">{e(c['nav_guides'])} <i class="fa-solid fa-angle-down"></i></a>
                    <ul>{lis(guides)}</ul>
                  </li>
                  <li class="dropdown-menu-parrent"><a href="pricing.html">{e(c['nav_company'])} <i class="fa-solid fa-angle-down"></i></a>
                    <ul>{lis(company)}</ul>
                  </li>
                  <li><a href="{other_href(lang, fname)}" hreflang="{other}" lang="{other}" title="{e(c['switch_lang'])}">{c['lang_other']}</a></li>
                  <li class="d-lg-none d-block"><a href="mailto:{EMAIL}"><img src="assets/img/icons/footer-icon-3.svg" alt="">{EMAIL}</a></li>
                </ul>
              </nav>
              <div class="cta-btn d-none d-lg-block btn-after button action-btn home1-header-btn">
                <a href="mailto:{EMAIL}"> <img src="assets/img/icons/footer-icon-3.svg" alt="">{EMAIL}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  <!--=====HEADER END=======-->

  <!--=====Mobile header start=======-->
  <div class="mobile-header mobile-header-4 d-block d-lg-none ">
    <div class="container-fluid">
      <div class="col-12">
        <div class="mobile-header-elements">
          <div class="mobile-logo">
            <a href="index.html">{logo}</a>
          </div>
          <div class="mobile-nav-icon" role="button" tabindex="0" aria-label="{e(c['menu'])}">
            <i class="fa-solid fa-bars"></i>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="mobile-sidebar">
    <div class="menu-close" role="button" tabindex="0" aria-label="{e(c['close'])}">
      <i class="fa-solid fa-xmark"></i>
    </div>
    <nav class="mobile-nav" aria-label="{nav_label}">
      <ul class="mobile-nav-list">
        <li><a href="index.html">{e(c['nav_home'])}</a></li>
        <li><a href="about.html">{e(c['nav_about'])}</a></li>
        <li><a href="services.html">{e(c['nav_services'])}</a>
          <ul class="sub-menu">{lis(services)}</ul>
        </li>
        <li><a href="how-it-works.html">{e(c['nav_guides'])}</a>
          <ul class="sub-menu">{lis(guides)}</ul>
        </li>
        <li><a href="pricing.html">{e(c['nav_company'])}</a>
          <ul class="sub-menu">{lis(company)}</ul>
        </li>
        <li><a href="{other_href(lang, fname)}" hreflang="{other}" lang="{other}">{e(c['lang_other_name'])}</a></li>
        <li><a href="mailto:{EMAIL}"> <img src="assets/img/icons/footer-icon-3.svg" alt="">{EMAIL}</a></li>
      </ul>
    </nav>
  </div>
  </header>
  <!--=====Mobile header end=======-->'''


def footer_html(lang, fname):
    c = COPY[lang]
    services, guides, company = nav_lists(lang)
    company_links = [('about.html', c['nav_about']), ('how-it-works.html', c['nav_how'])] + company
    legal = [('privacy.html', c['privacy']), ('terms.html', c['terms']), ('refund-policy.html', c['refund'])]
    other = 'es' if lang == 'en' else 'en'
    return f'''<!--=====footer-start=======-->
  <footer>
  <div class="footer sec-padding">
    <div class="container">
      <div class="row">
        <div class="col-md-3">
          <div class="footer-hadding">
            <a href="index.html"><img src="assets/brand/DS-horizontal_reversed.svg" alt="Diler Services" width="174" height="46"></a>
            <div class="space30"></div>
            <p>{e(c['footer_text'])}</p>
            <div class="space30"></div>
            <div class="footer-shere">
              <ul>
                <li><a href="mailto:{EMAIL}" aria-label="{e(c['email_us'])}"><i class="fa-solid fa-envelope"></i></a></li>
                <li><a href="{other_href(lang, fname)}" hreflang="{other}" aria-label="{e(c['switch_lang'])}"><i class="fa-solid fa-globe"></i></a></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-2">
          <div class="footer-menu">
            <h2 class="ds-h4">{e(c['footer_services'])}</h2>
            <ul>{lis(services[:6])}</ul>
          </div>
        </div>
        <div class="col-md-2">
          <div class="footer-menu">
            <h2 class="ds-h4">{e(c['footer_company'])}</h2>
            <ul>{lis(company_links[:6])}</ul>
          </div>
        </div>
        <div class="col-md-2">
          <div class="footer-menu">
            <h2 class="ds-h4">{e(c['footer_legal'])}</h2>
            <ul>{lis(legal)}</ul>
          </div>
        </div>
        <div class="col-md-3">
          <div class="footer-menu">
            <h2 class="ds-h4">{e(c['footer_contact'])}</h2>
            <div class="foter-contact">
              <div class="footer-contact-icon">
                <img src="assets/img/icons/footer-icon-1.svg" alt="">
              </div>
              <div class="footer-contact-p">
                <p>{c['footer_area']}</p>
              </div>
            </div>
            <div class="foter-contact">
              <div class="footer-contact-icon">
                <img src="assets/img/icons/footer-icon-3.svg" alt="">
              </div>
              <div class="footer-contact-p">
                <a href="mailto:{EMAIL}"><p>{EMAIL}</p></a>
              </div>
            </div>
            <div class="foter-contact">
              <div class="footer-contact-icon">
                <i class="fa-regular fa-clock ds-foot-clock"></i>
              </div>
              <div class="footer-contact-p">
                <p>{c['footer_reply']}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="fonter-end">
    <div class="contaier">
      <div class="row">
        <div class="col-md-12 text-center">
          <div class="footer-end-p">
            <a href="index.html">{e(c['copyright'])}</a>
            <p class="ds-disclaimer">{e(c['disclaimer'])}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  </footer>
  <!--=====footer-end=======-->'''


def head_meta(lang, fname, title, desc, ld):
    assert len(title) < 60, (fname, lang, len(title), title)
    assert len(desc) < 155, (fname, lang, len(desc), desc)
    en_url = f'{SITE}/{fname}'.replace('/index.html', '/')
    es_url = f'{SITE}/es/{fname}'.replace('/index.html', '/')
    url = en_url if lang == 'en' else es_url
    ld_html = ''.join(f'\n  <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="es" href="{es_url}">
  <link rel="alternate" hreflang="x-default" href="{en_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/brand/og-{lang}.png">
  <meta property="og:locale" content="{'en_US' if lang == 'en' else 'es_US'}">{ld_html}'''


def load_template(name, lang, fname, title, desc, ld):
    s = open(os.path.join(TPL, name), encoding='utf-8').read()
    a = s.index('<!--=====HEADER START=======-->')
    b = s.index('<!--=====Mobile header end=======-->') + len('<!--=====Mobile header end=======-->')
    s = s[:a] + header_html(lang, fname) + s[b:]
    a = s.index('<!--=====footer-start=======-->')
    b = s.index('<!--=====footer-end=======-->') + len('<!--=====footer-end=======-->')
    s = s[:a] + footer_html(lang, fname) + s[b:]
    s = re.sub(r'<title>.*?</title>', lambda m_: head_meta(lang, fname, title, desc, ld), s, count=1, flags=re.S)
    s = s.replace('<link rel="shortcut icon" href="assets/img/logo/titel-logo.png">',
                  '<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">\n  <link rel="icon" href="assets/brand/favicon.ico" sizes="32x32">\n  <link rel="apple-touch-icon" href="assets/brand/apple-touch-icon-180.png">')
    s = s.replace('content="width=`device-width`, initial-scale=1.0"', 'content="width=device-width, initial-scale=1.0"')
    s = s.replace('<link rel="stylesheet" href="assets/css/master.css">', '<link rel="stylesheet" href="assets/css/master.css">\n  <link rel="stylesheet" href="assets/css/diler.css">')
    # self-hosted builds of the CDN scripts the template loads (AOS 2.3.4, Waypoints 4.0.1)
    s = s.replace('<script src="https://unpkg.com/aos@next/dist/aos.js"></script>', '<script src="assets/js/vendor/aos.js"></script>')
    s = s.replace('<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>', '')
    s = s.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/waypoints/4.0.1/jquery.waypoints.min.js"></script>', '<script src="assets/js/vendor/jquery.waypoints.min.js"></script>')
    s = re.sub(r'\s*<script src="https://cdn.jsdelivr.net/npm/@popperjs[^>]*></script>', '', s)
    s = s.replace('<script src="assets/js/main.js"></script>', '<script src="assets/js/main.js"></script>\n  <script src="assets/js/diler.js"></script>')
    soup = BeautifulSoup(s, 'html.parser')
    q(soup, 'html')['lang'] = lang
    q(soup, 'body').insert(0, frag(f'<a class="ds-skip" href="#main">{e(COPY[lang]["skip"])}</a>'))
    return soup


def finish(soup, lang, fname):
    """Wrap the content in <main>, keep one h1, prefix asset paths for Spanish pages and write the file."""
    hdr = q(soup, 'header')
    ftr = q(soup, 'footer')
    main = soup.new_tag('main', id='main')
    nodes = []
    n = hdr.next_sibling
    while n is not None and n is not ftr:
        nodes.append(n)
        n = n.next_sibling
    hdr.insert_after(main)
    for x in nodes:
        main.append(x.extract())
    for h in main.find_all('h1')[1:]:
        retag(h, 'h2', 'ds-h1')
    for h in main.find_all('h6'):
        retag(h, 'p', 'ds-h6')
    for h in main.find_all('h4'):
        retag(h, 'h3', 'ds-h4')
    out = str(soup)
    if lang == 'es':
        out = re.sub(r'(src|href)="assets/', r'\1="../assets/', out)
    d = V3 if lang == 'en' else os.path.join(V3, 'es')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, fname), 'w', encoding='utf-8').write(out)


# ---------------------------------------------------------------- forms
def web3_hidden(subject, lang):
    return (f'<input type="hidden" name="access_key" value="{FORM_KEY}"><input type="hidden" name="subject" value="{e(subject)}">'
            f'<input type="hidden" name="Language" value="{lang}"><input type="checkbox" name="botcheck" class="d-none" tabindex="-1" autocomplete="off" aria-hidden="true">')


def fill_contact_form(form, lang, uid):
    c = COPY[lang]
    form['action'], form['method'] = 'https://api.web3forms.com/submit', 'POST'
    form['class'] = (form.get('class') or []) + ['ds-form']
    form.insert(0, frag(web3_hidden('Website question', lang)))
    specs = [('Name', 'text', c['f_name'], 'name', True), ('Email', 'email', c['f_email'], 'email', True),
             ('Phone', 'tel', c['f_phone'], 'tel', False), ('Service', 'text', c['f_subject'], 'off', False)]
    for el, (name, typ, label, ac, req) in zip(qa(form, '.contact-from-input input', 4), specs):
        fid = f'{uid}-{name.lower()}'
        el['name'], el['type'], el['placeholder'], el['id'], el['autocomplete'] = name, typ, label + (' *' if req else ''), fid, ac
        if req:
            el['required'] = ''
        el.insert_before(frag(f'<label class="visually-hidden" for="{fid}">{e(label)}</label>'))
    ta = q(form, 'textarea')
    fid = f'{uid}-message'
    ta['name'], ta['id'], ta['placeholder'], ta['required'] = 'Message', fid, c['f_message'] + ' *', ''
    ta.insert_before(frag(f'<label class="visually-hidden" for="{fid}">{e(c["f_message"])}</label>'))
    btn = q(form, 'button')
    btn['type'], btn['data-sending'] = 'submit', c['f_sending']
    text(btn, c['f_send'])
    btn.parent.insert_after(frag(f'<p class="ds-form-msg" role="status" data-ok="{e(c["f_sent"])}" data-err="{e(c["f_error"])}"></p>'))


def fill_subscribe(soup, lang):
    c = COPY[lang]
    sec = soup.select_one('.subsraibe')
    if not sec:
        return
    text(q(sec, '.subsraibe-hadding h1'), c['sub_title'])
    text(q(sec, '.subsraibe-hadding p'), c['sub_text'])
    form = q(sec, 'form')
    form['action'], form['method'], form['class'] = 'https://api.web3forms.com/submit', 'POST', ['ds-form']
    form.insert(0, frag(web3_hidden('Question from the website (email only)', lang)))
    inp = q(form, 'input[name=email]')
    inp['type'], inp['name'], inp['placeholder'], inp['id'], inp['required'], inp['autocomplete'] = 'email', 'Email', c['sub_placeholder'], 'sub-email', '', 'email'
    inp.insert_before(frag(f'<label class="visually-hidden" for="sub-email">{e(c["sub_label"])}</label>'))
    btn = q(form, 'button')
    btn['type'], btn['data-sending'] = 'submit', c['f_sending']
    text(btn, c['sub_btn'])
    form.append(frag(f'<p class="ds-form-msg" role="status" data-ok="{e(c["sub_sent"])}" data-err="{e(c["f_error"])}"></p>'))


# ---------------------------------------------------------------- shared sections
def fill_inner_hero(soup, lang, h1, crumb):
    box = q(soup, '.inner-page-hero-area .hadding')
    text(q(box, 'h1'), h1)
    h6 = q(box, 'h6')
    h6.name = 'nav'
    h6['aria-label'] = 'Breadcrumb' if lang == 'en' else 'Ruta de navegación'
    h6['class'] = ['ds-h6']
    inner(h6, f'<a href="index.html">{e(COPY[lang]["home"])}</a> {COPY[lang]["crumb_sep"]} <span aria-current="page">{e(crumb)}</span>')


def service_card(box, lang, s):
    c = COPY[lang]
    name = e(L(lang, s['name']))
    set_img(q(box, 'img'), f'assets/img/icons/{SERVICE_ICON[s["slug"]]}', '')
    inner(q(box, 'h2'), f'<a href="{svc_file(s["slug"])}">{name}</a>')
    inner(q(box, 'p'), f'{e(L(lang, s["summary"]))} <b>{e(s["price"])}</b> {e(L(lang, s["priceNote"]))}.')
    a = q(box, '.read-more-btn a')
    a['href'] = svc_file(s['slug'])
    inner(a, f'{e(c["svc_more"])}<span class="visually-hidden"> {name}</span> <i class="fa-solid fa-arrow-right"></i>')


def fill_service_grid(sec, lang, slugs, other=False):
    c = COPY[lang]
    if other:
        inner(q(sec, '.hadding h1'), c['svc_other_h'])
    else:
        heading(sec, c['svc_span'], c['svc_h'])
    boxes = qa(sec, '.service-box', len(slugs))
    for box, slug in zip(boxes, slugs):
        if slug == 'help':
            set_img(q(box, 'img'), 'assets/img/icons/about-vision-icon-1.svg', '')
            inner(q(box, 'h2'), f'<a href="contact.html">{e(c["svc_help_name"])}</a>')
            text(q(box, 'p'), c['svc_help_text'])
            a = q(box, '.read-more-btn a')
            a['href'] = 'contact.html'
            inner(a, f'{e(c["nav_contact"])} <i class="fa-solid fa-arrow-right"></i>')
        else:
            service_card(box, lang, svc(slug))


def fill_facts(soup, lang):
    sec = soup.select_one('.our-fact')
    if not sec:
        return
    icons = ['fact-icon-3.svg', 'fact-icon-1.svg', 'fact-icon-2.svg', 'fact-icon-4.svg']
    for box, (pre, num, post, label), ic in zip(qa(sec, '.fact-box', 4), COPY[lang]['facts'], icons):
        set_img(q(box, '.fact-icon img'), f'assets/img/icons/{ic}', '')
        h = q(box, 'h1')
        inner(h, f'{e(pre)}<span class="counter-up">{num}</span>{e(post)}')
        retag(h, 'p', 'ds-h1')
        text(q(box, 'p:not(.ds-h1)'), label)


def fill_works(sec, lang, img_name='signing-documents-2'):
    c = COPY[lang]
    heading(sec, c['works_span'], c['works_h'], e(c['works_p']))
    icons = ['works-icon-3.svg', 'works-icon-2.svg', 'about-vision-icon-3.svg']
    for item, (t, p), ic in zip(qa(sec, '.work-item', 3), c['works'], icons):
        set_img(q(item, '.work-icon img'), f'assets/img/icons/{ic}', '')
        text(q(item, 'h2'), t)
        text(q(item, '.hadding p'), p)
    photo(q(sec, '.works-img img'), img_name, 600, 660, alt(lang, img_name))


def fill_pricing(sec, lang, h=None):
    c = COPY[lang]
    heading(sec, c['price_span'], h or c['price_h'], e(c['price_p']))
    text(q(sec, '.t-month'), c['toggle_month'])
    text(q(sec, '.t-year'), c['toggle_year'])
    q(sec, '#ce-toggle')['aria-label'] = f'{c["toggle_month"]} / {c["toggle_year"]}'
    for tab, key in (('#monthly', 'month'), ('#yearly', 'year')):
        for box, plan in zip(qa(q(sec, tab), '.single-price', 3), c['plans']):
            h2s = box.find_all('h2')
            ps = box.find_all('p', recursive=False)
            text(h2s[0], plan['name'])
            text(ps[0], plan['text'])
            text(h2s[1], plan[key][0])
            text(ps[1], plan[key][1])
            a = q(box, '.price-btn a')
            a['href'] = f'order.html?service={plan["slug"]}'
            inner(a, f'{e(c["plan_btn"])}<span class="visually-hidden"> {e(plan["name"])}</span>')
            for li, row, ok in zip(qa(box, '.price-list li', 8), c['plan_rows'], PLAN_MATRIX[plan['slug']]):
                icon = 'check.svg' if ok else 'check1.svg'
                a_ = ('Included' if lang == 'en' else 'Incluido') if ok else ('Not included' if lang == 'en' else 'No incluido')
                inner(li, f'<img src="assets/img/icons/{icon}" alt="{a_}:"> {e(row)}')


def fill_blog(sec, lang):
    c = COPY[lang]
    heading(sec, c['blog_span'], c['blog_h'])
    for box, (href, title, p), ph in zip(qa(sec, '.blog-box', 3), c['blog'], ['founder-laptop-2', 'mailbox-1', 'opening-mail-2']):
        photo(q(box, '.blog-img img'), ph, 370, 280, alt(lang, ph))
        inner(q(box, 'h2'), f'<a href="{href}">{title}</a>')
        text(q(box, '.box-hadding p'), p)
        a = q(box, '.read-more-btn a')
        a['href'] = href
        inner(a, f'{e(c["blog_more"])}<span class="visually-hidden">: {e(re.sub("<[^>]+>", "", title))}</span> <i class="fa-solid fa-arrow-right"></i>')


def fill_testimonial(sec, lang, img_name='consultation-2'):
    c = COPY[lang]
    heading(sec, c['testi_span'], c['testi_h'])
    for slide, (t, role, quote) in zip(qa(sec, '.testimonial-box', 3), c['testi']):
        im = q(slide, 'img')
        set_img(im, 'assets/brand/DS-icon_full.svg', '', 90, 90)
        im['class'] = ['ds-commit-logo']
        text(q(slide, 'h2'), t)
        text(q(slide, 'p'), role)
        text(q(slide, 'h6'), quote)
    photo(q(sec, '.testimonial-img img'), img_name, 498, 490, alt(lang, img_name))


def fill_contact(sec, lang, img_name, uid):
    c = COPY[lang]
    heading(sec, c['contact_span'], c['contact_h'], e(c['contact_p']))
    photo(q(sec, '.contact-img img'), img_name, 562, 634, alt(lang, img_name))
    fill_contact_form(q(sec, 'form'), lang, uid)


def faq_accordion(acc, items, uid):
    """Fill a template accordion with our questions, keeping its markup and Bootstrap wiring."""
    blocks = qa(acc, '.accordion-item', len(items))
    for k, (blk, it) in enumerate(zip(blocks, items)):
        hid, cid = f'{uid}-h{k}', f'{uid}-c{k}'
        q(blk, '.accordion-header')['id'] = hid
        b = q(blk, 'button')
        b['data-bs-target'], b['aria-controls'] = f'#{cid}', cid
        text(b, it['q'])
        col = q(blk, '.accordion-collapse')
        col['id'], col['aria-labelledby'] = cid, hid
        text(q(blk, '.accordion-body'), it['a'])


# ---------------------------------------------------------------- JSON-LD
def ld_org(lang):
    return {'@context': 'https://schema.org', '@type': 'ProfessionalService', 'name': 'Diler Services LLC', 'url': SITE + '/',
            'email': EMAIL, 'logo': SITE + '/assets/brand/DS-icon_full.svg', 'areaServed': {'@type': 'State', 'name': 'Florida'},
            'availableLanguage': ['English', 'Spanish'],
            'description': {'en': 'Florida LLC formation and registered agent service.', 'es': 'Formación de LLC en Florida y servicio de agente registrado.'}[lang]}


def ld_faq(items):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': i['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': i['a']}} for i in items]}


def ld_crumbs(lang, trail):
    base = SITE + ('/' if lang == 'en' else '/es/')
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': k + 1, 'name': n, 'item': base + ('' if f == 'index.html' else f)} for k, (n, f) in enumerate(trail)]}


def ld_service(lang, s):
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': L(lang, s['name']), 'description': L(lang, s['summary']),
            'provider': {'@type': 'ProfessionalService', 'name': 'Diler Services LLC', 'url': SITE + '/'},
            'areaServed': {'@type': 'State', 'name': 'Florida'},
            'offers': {'@type': 'Offer', 'price': re.sub(r'[^0-9.]', '', s['price']), 'priceCurrency': 'USD',
                       'description': f"{s['price']} {L(lang, s['priceNote'])}"}}


def crumbs(lang, *trail):
    return ld_crumbs(lang, [(COPY[lang]['home'], 'index.html')] + list(trail))


# ---------------------------------------------------------------- pages
def page_home(lang):
    c = COPY[lang]
    m = META[lang]['index.html']
    fq = faq_items(lang)
    soup = load_template('index1.html', lang, 'index.html', m['title'], m['desc'], [ld_org(lang)])
    hero = q(soup, '.hero-area')
    inner(q(hero, '.main-hadding h1'), c['hero_h1'])
    inner(q(hero, '.main-hadding p'), c['hero_p'])
    b1, b2 = qa(hero, '.home1-header-button a', 2)
    b1['href'], b2['href'] = 'order.html', 'services.html'
    text(b1, c['hero_btn1'])
    text(b2, c['hero_btn2'])
    photo(q(hero, '.home1-header-img-2 img'), 'founder-laptop-1', 572, 802, c['hero_alt'])
    about = q(soup, '.about')
    heading(about, c['about_span'], c['about_h'], c['about_p'])
    photo(q(about, '.about-img img'), 'consultation-1', 600, 627, alt(lang, 'consultation-1'))
    for p_, t in zip(qa(about, '.chek-list p', 4), c['about_checks']):
        inner(p_, f'<img src="assets/img/icons/check.svg" alt=""> {e(t)}')
    btn = q(about, '.home1-button button')
    btn.name = 'a'
    btn['href'] = 'about.html'
    text(btn, c['about_btn'])
    fill_facts(soup, lang)
    fill_service_grid(q(soup, '.service'), lang, ['llc-formation', 'formation-bundle', 'ein-filing', 'registered-agent', 'annual-report', 'dba'])
    fill_works(q(soup, '.works'), lang)
    fill_pricing(q(soup, '.pricing-plan'), lang)
    fill_blog(q(soup, '.blog'), lang)
    fill_testimonial(q(soup, '.testimonial'), lang)
    fill_contact(q(soup, '.contact'), lang, 'office-plants-1', 'hc')
    fill_subscribe(soup, lang)
    finish(soup, lang, 'index.html')


def page_about(lang):
    c = COPY[lang]
    m = META[lang]['about.html']
    soup = load_template('about.html', lang, 'about.html', m['title'], m['desc'], [ld_org(lang), crumbs(lang, (m['h1'], 'about.html'))])
    fill_inner_hero(soup, lang, m['h1'], m['crumb'])
    sec = q(soup, '.about-page-about-sec')
    box = heading(sec, c['ab_span'], c['ab_h'])
    ps = box.find_all('p', recursive=False)
    text(ps[0], c['ab_p1'])
    text(ps[1], c['ab_p2'])
    for p_, t in zip(qa(sec, '.chek-list p', 4), c['ab_checks']):
        inner(p_, f'<img src="assets/img/icons/check.svg" alt=""> {e(t)}')
    a = q(sec, '.home1-button a')
    a['href'] = 'services.html'
    text(a, c['ab_btn'])
    photo(q(sec, '.about-page-about-img1 img'), 'consultation-2', 608, 348, alt(lang, 'consultation-2'))
    photo(q(sec, '.about-page-img-2 img'), 'mailbox-1', 285, 285, alt(lang, 'mailbox-1'))
    photo(q(sec, '.about-page-img-3 img'), 'signing-documents-2', 285, 285, alt(lang, 'signing-documents-2'))
    wwd = q(soup, '.what-we-do')
    heading(wwd, c['wwd_span'], c['wwd_h'], e(c['wwd_p']))
    for box, (pre, num, post, label) in zip(qa(wwd, '.preview-counter', 4), c['wwd_counters']):
        h = q(box, 'h1')
        inner(h, f'{e(pre)}<span class="counter-up">{num}</span>{e(post)}')
        retag(h, 'p', 'ds-h1')
        text(q(box, 'p:not(.ds-h1)'), label)
    photo(q(wwd, '.about-page-img img'), 'founder-laptop-1', 600, 630, alt(lang, 'founder-laptop-1'))
    why = q(soup, '.about-choose')
    box = heading(why, c['why_span'], c['why_h'])
    ps = box.find_all('p', recursive=False)
    text(ps[0], c['why_p1'])
    text(ps[1], c['why_p2'])
    a = q(why, '.home1-button a')
    a['href'] = 'order.html'
    text(a, c['why_btn'])
    for b, (t, p, href), ic in zip(qa(why, '.about-choose-box', 4), c['why_boxes'], ['service-icon-4.svg', 'service-icon-5.svg', 'service-icon-1.svg', 'works-icon-1.svg']):
        set_img(q(b, 'img'), f'assets/img/icons/{ic}', '')
        inner(q(b, 'h4'), f'<a href="{href}">{e(t)}</a>')
        text(q(b, '.hadding p'), p)
    vis = q(soup, '.our-vision')
    heading(vis, c['vis_span'], c['vis_h'])
    for b, (t, p), ic in zip(qa(vis, '.about-vision-box', 4), c['vis'], ['about-vision-icon-1.svg', 'fact-icon-3.svg', 'about-vision-icon-3.svg', 'fact-icon-1.svg']):
        set_img(q(b, 'img'), f'assets/img/icons/{ic}', '')
        inner(q(b, 'h4'), f'<a href="how-it-works.html">{t}</a>')
        text(q(b, '.hadding p'), p)
    fill_contact(q(soup, '.contact'), lang, 'founder-laptop-2', 'ac')
    fill_subscribe(soup, lang)
    finish(soup, lang, 'about.html')


def page_services(lang):
    m = META[lang]['services.html']
    soup = load_template('service.html', lang, 'services.html', m['title'], m['desc'], [crumbs(lang, (m['h1'], 'services.html'))])
    fill_inner_hero(soup, lang, m['h1'], m['h1'])
    fill_service_grid(q(soup, '.service-page-service'), lang, [s['slug'] for s in SERVICES] + ['help'])
    fill_pricing(q(soup, '.pricing-plan'), lang)
    fill_testimonial(q(soup, '.testimonial'), lang, 'consultation-1')
    fill_contact(q(soup, '.contact'), lang, 'opening-mail-2', 'sc')
    fill_subscribe(soup, lang)
    finish(soup, lang, 'services.html')


def page_service(lang, s):
    c = COPY[lang]
    slug = s['slug']
    sm = SERVICE_META[lang][slug]
    fq = faq_items(lang)
    name = L(lang, s['name'])
    ids = (s['faq'] + [i for i in ['price-refund', 'llc-time', 'about-law', 'price-other', 'about-contact'] if i not in s['faq']])[:4]
    items = [fq[i] for i in ids]
    fname = svc_file(slug)
    soup = load_template('service-details.html', lang, fname, sm['title'], sm['desc'],
                         [ld_service(lang, s), ld_faq(items), crumbs(lang, (c['nav_services'], 'services.html'), (name, fname))])
    fill_inner_hero(soup, lang, sm['h1'], name)
    sd = q(soup, '.service-details')
    boxes = qa(sd, '.details-box', 4)
    # sidebar: search (submits to the FAQ page, which filters its questions)
    text(q(boxes[0], 'h2'), c['sd_search'])
    form = q(boxes[0], 'form')
    form['action'], form['method'], form['role'] = 'faq.html', 'get', 'search'
    inp = q(form, 'input')
    inp['name'], inp['placeholder'], inp['id'] = 'q', c['sd_search_ph'], 'sd-search'
    inp.insert_before(frag(f'<label class="visually-hidden" for="sd-search">{e(c["sd_search_ph"])}</label>'))
    b = q(form, 'button')
    b['type'], b['aria-label'] = 'submit', c['sd_search_btn']
    # sidebar: services
    text(q(boxes[1], 'h2'), c['sd_services'])
    inner(q(boxes[1], 'ul'), ''.join(
        f'<li><a href="{svc_file(o["slug"])}"' + (' aria-current="page"' if o['slug'] == slug else '') + f'>{e(L(lang, o["name"]))} <i class="fa-solid fa-angle-right"></i></a></li>'
        for o in SERVICES))
    # sidebar: contact (no street address or phone yet, so area, response time and email)
    text(q(boxes[2], 'h2'), c['sd_contact'])
    rows = qa(boxes[2], '.contact-details-p', 3)
    for p_, t in zip(rows[0].find_all('p'), c['sd_area']):
        text(p_, t)
    set_img(qa(boxes[2], '.contact-details-icon img', 3)[1], 'assets/img/icons/date.svg', '', 20, 20)
    for p_, t in zip(rows[1].find_all('p'), c['sd_hours']):
        text(p_, t)
    ps = rows[2].find_all('p')
    inner(ps[0], f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    ps[1].decompose()
    # sidebar: call to action
    text(q(boxes[3], 'h2'), c['sd_profile'])
    a = q(boxes[3], '.home1-button a')
    a['href'] = f'order.html?service={slug}'
    text(a, c['sd_profile_btn'])
    # main column
    main = q(sd, '.service-details-all')
    ph = SERVICE_PHOTOS[slug]
    for el, (nm, w, h) in zip(qa(main, '.service-details-img img', 5), [(ph[0], 720, 480), (ph[1], 720, 340), (ph[2], 345, 260), (ph[3], 345, 260), (ph[4], 320, 300)]):
        photo(el, nm, w, h, alt(lang, nm))
    b1, b2 = main.find_all('div', class_='hadding', recursive=False)[:2]
    text(q(b1, 'h2'), f'{name}: {s["price"]} {L(lang, s["priceNote"])}')
    p1, p2 = b1.find_all('p')
    text(p1, L(lang, s['detail']['lead']))
    text(p2, L(lang, s['detail']['second']))
    sections = SERVICE_SECTIONS[lang].get(slug)
    if sections:
        text(q(b2, 'h2'), sections[0][0])
        for p_ in b2.find_all('p'):
            p_.decompose()
        for x in list(frag(sections[0][1]).contents):
            b2.append(x)
        anchor = b2
        for h, body in sections[1:]:
            blk = frag(f'<div class="hadding hadding-p ds-more"><h2>{e(h)}</h2>{body}</div>').contents[0]
            anchor.insert_after(blk)
            anchor = blk
    else:
        h, ps2 = SERVICE_BLOCK2[lang][slug]
        text(q(b2, 'h2'), h)
        for p_, t in zip(b2.find_all('p'), ps2):
            text(p_, t)
    ben = qa(q(main, '.row.align-items-center'), '.col-md-6', 2)[1]
    text(q(ben, 'h2'), c['sd_benefit'])
    text(q(ben, 'p'), f'{name}: {s["price"]} {L(lang, s["priceNote"])}.')
    inner(q(ben, 'ul'), ''.join(f'<li><img src="assets/img/icons/check.svg" alt=""> {e(t)}</li>' for t in s['detail']['includes'][lang]))
    fill_service_grid(q(soup, '.service'), lang, [o['slug'] for o in SERVICES if o['slug'] != slug][:3], other=True)
    sf = q(soup, '.service-faq')
    inner(q(sf, '.hadding h1'), c['sd_faq_h'].replace('{name}', e(name)))
    photo(q(sf, '.service-details-img img'), ph[5], 570, 630, alt(lang, ph[5]))
    hb = qa(sf, '.hadding')[1]
    text(q(hb, 'h2'), c['sd_faq_sub'])
    text(q(hb, 'p'), c['sd_faq_p'])
    faq_accordion(q(sf, '.accordion'), items, f'sf-{slug}')
    fill_subscribe(soup, lang)
    finish(soup, lang, fname)


PRICING_FAQ = ['price-llc', 'price-other', 'price-refund', 'price-name', 'ra-price', 'ein-what', 'llc-included', 'llc-time']


def page_pricing(lang):
    c = COPY[lang]
    m = META[lang]['pricing.html']
    fq = faq_items(lang)
    items = [fq[i] for i in PRICING_FAQ]
    soup = load_template('pricing-plan.html', lang, 'pricing.html', m['title'], m['desc'], [ld_faq(items), crumbs(lang, (m['crumb'], 'pricing.html'))])
    fill_inner_hero(soup, lang, m['h1'], m['crumb'])
    fill_pricing(q(soup, '.pricing-plan2'), lang, {'en': 'Choose the plan that <span>fits your business</span>', 'es': 'Elija el plan que <span>se adapte a su empresa</span>'}[lang])
    fs = q(soup, '.faq-pricing-plan')
    inner(q(fs, '.hadding h1'), {'en': 'Pricing and <span>refund questions</span>', 'es': 'Preguntas sobre <span>precios y reembolsos</span>'}[lang])
    accs = qa(fs, '.accordion', 2)
    faq_accordion(accs[0], items[:4], 'pfa')
    faq_accordion(accs[1], items[4:], 'pfb')
    fill_subscribe(soup, lang)
    finish(soup, lang, 'pricing.html')


def page_faq(lang):
    c = COPY[lang]
    m = META[lang]['faq.html']
    fq = faq_items(lang)
    all_items = [fq[i] for blk in c['faq_blocks'] for i in blk[2]]
    soup = load_template('faq.html', lang, 'faq.html', m['title'], m['desc'], [ld_faq(all_items), crumbs(lang, (m['crumb'], 'faq.html'))])
    fill_inner_hero(soup, lang, m['h1'], m['crumb'])
    for k, (sec, (hl, rest, ids)) in enumerate(zip(qa(soup, '.faq-pricing-plan', 3), c['faq_blocks'])):
        sec['id'] = f'faq-{k + 1}'
        inner(q(sec, '.hadding h1'), f'<span>{e(hl)}</span>{e(rest)}')
        items = [fq[i] for i in ids]
        accs = qa(sec, '.accordion', 2)
        faq_accordion(accs[0], items[:4], f'fq{k}a')
        faq_accordion(accs[1], items[4:], f'fq{k}b')
    fill_subscribe(soup, lang)
    finish(soup, lang, 'faq.html')


def page_contact(lang):
    c = COPY[lang]
    m = META[lang]['contact.html']
    soup = load_template('contact.html', lang, 'contact.html', m['title'], m['desc'], [ld_org(lang), crumbs(lang, (m['h1'], 'contact.html'))])
    fill_inner_hero(soup, lang, m['h1'], m['h1'])
    for box, (t, lines), ic in zip(qa(soup, '.home4-contact-box', 3), c['cp_boxes'], ['home4-contact-iocn-1.svg', 'date.svg', 'home4-contact-iocn-3.svg']):
        set_img(q(box, '.contact-iocn img'), f'assets/img/icons/{ic}', '', 40, 40)
        h4 = q(box, 'h4')
        text(h4, t)
        retag(h4, 'h2', 'ds-h4')
        for x in box.find_all(['a', 'p']):
            x.decompose()
        for ln in lines:
            box.append(frag(f'<a href="mailto:{ln}">{ln}</a>' if '@' in ln else f'<p>{e(ln)}</p>'))
    form = q(soup, 'main form, form') if soup.select_one('main') else q(soup, '.contact-form').find_parent('form')
    sec = form.find_parent('div', class_='container')
    heading(sec, c['contact_span'], c['contact_h'], e(c['contact_p']))
    photo(q(sec, '.contact-img img'), 'consultation-1', 562, 634, alt(lang, 'consultation-1'))
    fill_contact_form(form, lang, 'cc')
    ifr = q(soup, '.contact-map iframe')
    ifr['src'], ifr['title'], ifr['loading'] = 'https://www.google.com/maps?q=Florida&z=6&output=embed', c['map_title'], 'lazy'
    fill_subscribe(soup, lang)
    finish(soup, lang, 'contact.html')


ORDER_FEES = {'llc-formation': (89, 125), 'formation-bundle': (174, 125), 'ein-filing': (95, 0), 'annual-report': (99, None),
              'dba': (129, None), 'amendment': (99, None), 'reinstatement': (299, None), 'registered-agent': (0, 0)}


def page_order(lang):
    c = COPY[lang]
    m = META[lang]['order.html']
    soup = load_template('checkout.html', lang, 'order.html', m['title'], m['desc'], [crumbs(lang, (m['crumb'], 'order.html'))])
    fill_inner_hero(soup, lang, m['h1'], m['crumb'])
    pg = q(soup, '.checkout-page')
    form = q(pg, '.col-md-7 form')
    form['action'], form['method'], form['class'], form['id'] = 'https://api.web3forms.com/submit', 'POST', ['ds-form', 'ds-order-form'], 'order-form'
    form.insert(0, frag(web3_hidden('New order from the website', lang) + '<input type="hidden" name="Total due today" data-f="total">'))
    text(q(pg, '.checkout-form .hadding h2'), c['o_details'])
    fields = qa(form, '.checkout-input')
    spec = {0: ('First name', 'text', c['o_first'], c['o_ph_first'], 'given-name', True),
            1: ('Email', 'email', c['o_email'], c['o_ph_email'], 'email', True),
            2: ('Company name', 'text', c['o_company'], c['o_ph_company'], 'organization', True),
            5: ('Last name', 'text', c['o_last'], c['o_ph_last'], 'family-name', True),
            6: ('Phone', 'tel', c['o_phone'], c['o_ph_phone'], 'tel', False),
            7: ('Mailing address', 'text', c['o_address'], c['o_ph_address'], 'street-address', True)}
    svc_opts = [(L('en', s['name']), f"{L(lang, s['name'])} ({s['price']})", s['slug']) for s in SERVICES if s['slug'] != 'registered-agent']
    svc_opts.append(('Registered Agent only', L(lang, svc('registered-agent')['name']), 'registered-agent'))
    selects = {3: ('Service', c['o_service']), 4: ('Registered agent', c['o_ra']), 8: ('Add EIN filing', c['o_ein']), 9: ('Preferred language', c['o_lang'])}
    for k, fld in enumerate(fields[:10]):
        lab = q(fld, 'p')
        fid = f'o-{k}'
        req = False
        if k in spec:
            name, typ, label, ph, ac, req = spec[k]
            inp = q(fld, 'input')
            inp['name'], inp['type'], inp['placeholder'], inp['id'], inp['autocomplete'] = name, typ, ph, fid, ac
            if req:
                inp['required'] = ''
        else:
            name, label = selects[k]
            sel = q(fld, 'select')
            sel['name'], sel['id'] = name, fid
            if k == 3:
                inner(sel, ''.join(f'<option value="{e(v)}" data-slug="{sl}" data-fee="{ORDER_FEES[sl][0]}" data-state="{"" if ORDER_FEES[sl][1] is None else ORDER_FEES[sl][1]}">{e(t)}</option>' for v, t, sl in svc_opts))
            elif k == 4:
                inner(sel, ''.join(f'<option value="{e(v)}" data-fee="{f}">{e(t)}</option>' for v, t, f in c['o_ra_opts']))
            elif k == 8:
                inner(sel, ''.join(f'<option value="{e(v)}" data-fee="{f}">{e(t)}</option>' for v, t, f in c['o_ein_opts']))
            else:
                inner(sel, ''.join(f'<option value="{e(v)}">{e(t)}</option>' for v, t in c['o_lang_opts']))
        lab.name = 'label'
        lab['for'] = fid
        text(lab, label + (' *' if req else ''))
    note = q(form, '.checkout-textarea')
    text(q(note, 'h2'), c['o_notes_h'])
    lab = q(note, 'p')
    lab.name, lab['for'] = 'label', 'o-notes'
    text(lab, c['o_notes'])
    ta = q(note, 'textarea')
    ta['name'], ta['id'], ta['placeholder'] = 'Details', 'o-notes', c['o_notes_ph']
    btn = q(form, 'button')
    btn['type'], btn['data-sending'] = 'submit', c['f_sending']
    text(btn, c['o_send'])
    btn.parent.insert_before(frag(f'<p class="ds-check"><input type="checkbox" id="o-consent" name="Accepted terms" value="Yes" required> <label for="o-consent">{c["o_consent"]}</label></p><p class="ds-paynote">{e(c["o_note"])}</p>'))
    btn.parent.insert_after(frag(f'<p class="ds-form-msg" role="status" data-ok="{e(c["o_sent"])}" data-err="{e(c["f_error"])}"></p>'))
    tax = q(pg, '.checkout-tax-area')
    text(q(tax, '.checkout-tax-hadding h2'), c['o_total_h'])
    tax['aria-live'], tax['data-at-cost'] = 'polite', c['o_at_cost']
    for pera, label, key in zip(qa(tax, '.checkout-pera', 4), c['o_rows'], ['fee', 'state', 'ra', 'sum']):
        cols = qa(pera, '.checkout-hadding-p p', 2)
        text(cols[0], label)
        text(cols[1], '—')
        cols[1]['data-f'] = key
    pay = q(tax, 'form')
    pay.name = 'fieldset'
    pay.attrs.pop('action', None)
    pay.insert(0, frag(f'<legend class="visually-hidden">{e(c["o_pay_legend"])}</legend>'))
    opts = qa(pay, '.checkout-input-selact')
    for blk, (label, checked) in zip(opts, c['o_pay']):
        inp = q(blk, 'input')
        inp['name'], inp['value'], inp['form'] = 'Next step', label, 'order-form'
        if checked:
            inp['checked'] = ''
        text(q(blk, 'label'), label)
    for extra in opts[2:]:  # the card-logo option: payment methods are not confirmed yet
        prev = extra.find_previous_sibling('div', class_='checkout-border')
        if prev:
            prev.decompose()
        extra.decompose()
    for b_ in pay.find_all('div', class_='button'):
        b_.decompose()
    fill_subscribe(soup, lang)
    finish(soup, lang, 'order.html')


def index1_block(start, end):
    s = open(os.path.join(TPL, 'index1.html'), encoding='utf-8').read()
    return s[s.index(start):s.index(end)]


def page_how(lang):
    """How it works: the template's inner hero with Home 1's How-it-works and fact sections."""
    m = META[lang]['how-it-works.html']
    soup = load_template('pricing-plan.html', lang, 'how-it-works.html', m['title'], m['desc'], [crumbs(lang, (m['h1'], 'how-it-works.html'))])
    fill_inner_hero(soup, lang, m['h1'], m['h1'])
    pp = q(soup, '.pricing-plan2')
    pp.insert_before(frag(index1_block('<!--=====How-it-works-start=======-->', '<!--=====How-it-works-end=======-->')))
    pp.insert_before(frag(index1_block('<!--=====fact-start=======-->', '<!--=====fact-end=======-->')))
    pp.decompose()
    q(soup, '.faq-pricing-plan').decompose()
    fill_works(q(soup, '.works'), lang, 'opening-mail-2')
    fill_facts(soup, lang)
    fill_subscribe(soup, lang)
    finish(soup, lang, 'how-it-works.html')


def legal_html(path):
    s = open(os.path.join(REPO, path), encoding='utf-8').read()
    i = s.find('<div class="ds-article">')
    if i < 0:
        return ''
    depth, j = 0, i
    for mm in re.finditer(r'<(/?)div\b[^>]*>', s[i:]):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            j = i + mm.end()
            break
    body = re.sub(r'\sclass="[^"]*"', '', s[i:j])
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, flags=re.S)
    body = body.replace('info@toromovers.com', EMAIL)
    links = {'privacy-policy': 'privacy.html', 'terms-of-service': 'terms.html', 'refund-policy': 'refund-policy.html', 'contact': 'contact.html', 'order': 'order.html'}
    return re.sub(r'href="/([a-z-]+)/"', lambda mm: f'href="{links.get(mm.group(1), "index.html")}"', body)


def page_legal(lang, fname, src, title_en, title_es):
    c = COPY[lang]
    title = title_en if lang == 'en' else title_es
    desc = {'en': f'{title} for Diler Services LLC, a Florida LLC formation and registered agent service. Draft pending attorney review.',
            'es': f'{title} de Diler Services LLC, servicio de formación de LLC y agente registrado en Florida. Borrador en revisión legal.'}[lang]
    soup = load_template('pricing-plan.html', lang, fname, title + BRAND, desc, [crumbs(lang, (title, fname))])
    fill_inner_hero(soup, lang, title, title)
    pp = q(soup, '.pricing-plan2')
    pp.insert_before(frag(f'<div class="service-details sec-padding"><div class="container"><div class="row"><div class="col-lg-8 m-auto"><div class="service-details-all"><div class="hadding hadding-p ds-legal"><p class="ds-legal-note">{e(c["legal_note"])}</p>{legal_html(src)}</div></div></div></div></div></div>'))
    pp.decompose()
    q(soup, '.faq-pricing-plan').decompose()
    fill_subscribe(soup, lang)
    finish(soup, lang, fname)


def page_404(lang):
    c = COPY[lang]
    soup = load_template('error.html', lang, '404.html', c['e_h1'] + BRAND, c['e_p'], [])
    box = q(soup, '.error-page-hero-area .hadding')
    set_img(q(box, 'img'), 'assets/img/image/error-img.png', '', 512, 512)
    h_a, h_b = qa(box, 'h1', 2)
    text(h_a, '404')
    retag(h_a, 'p', 'ds-h1')
    h_a.name = 'p'
    text(h_b, c['e_h1'])
    h_b.insert_after(frag(f'<p>{e(c["e_p"])}</p><div class="space30"></div><div class="header-btn-1 button btn-after home1-button d-inline-block"><a href="index.html">{e(c["e_btn"])}</a></div>'))
    finish(soup, lang, '404.html')


def build_all():
    A.run()
    for d in (V3, os.path.join(V3, 'es')):
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith('.html'):
                    os.remove(os.path.join(d, f))
    for lang in ('en', 'es'):
        page_home(lang)
        page_about(lang)
        page_services(lang)
        for s in SERVICES:
            page_service(lang, s)
        page_pricing(lang)
        page_how(lang)
        page_faq(lang)
        page_contact(lang)
        page_order(lang)
        page_legal(lang, 'privacy.html', 'privacy-policy/index.html', 'Privacy Policy', 'Política de privacidad')
        page_legal(lang, 'terms.html', 'terms-of-service/index.html', 'Terms of Service', 'Términos de servicio')
        page_legal(lang, 'refund-policy.html', 'refund-policy/index.html', 'Refund Policy', 'Política de reembolsos')
        page_404(lang)
    n_en = len([f for f in os.listdir(V3) if f.endswith('.html')])
    n_es = len([f for f in os.listdir(os.path.join(V3, 'es')) if f.endswith('.html')])
    print(f'built {n_en} EN and {n_es} ES pages')


if __name__ == '__main__':
    build_all()
