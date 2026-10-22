"""Build the trilingual Diler Services site from the Finclix home-1 template.
Markup, classes, SVG icons and animation hooks are kept from the template; only text,
links and photos are swapped. Run: python3 finclix-build/build.py"""
import copy, os, re, sys
from bs4 import BeautifulSoup, NavigableString
sys.path.insert(0, os.path.dirname(__file__))
from content import C, LLC, YEARLY, EMAIL

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(os.path.dirname(__file__), "template-index.html")
OUT = os.path.join(ROOT, "finclix")
LANGS = ["en", "es", "pt"]
PREFIX = {"en": "/", "es": "/es/", "pt": "/pt/"}

MARK = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="40" height="40" aria-hidden="true">'
        '<path fill="{c}" fill-rule="evenodd" d="M6.5 4.5h9.2c6.7 0 11.3 4.6 11.3 11.5s-4.6 11.5-11.3 11.5H6.5v-23zm3.4 3.3v16.4h5.6c4.7 0 7.9-3.2 7.9-8.2s-3.2-8.2-7.9-8.2H9.9z"/></svg>')

def logo(dark):
    c = "#ffffff" if dark else "#144443"
    cls = "diler-logo on-dark" if dark else "diler-logo"
    return f'<span class="{cls}">{MARK.format(c=c)}<span class="diler-word"><strong>Diler</strong><em>Services</em></span></span>'

def frag(html):
    return BeautifulSoup(html, "html.parser")

def set_html(el, html):
    el.clear()
    for n in list(frag(html).contents):
        el.append(n)

def text_only(el, txt):
    """Replace the bare text nodes of el, keep child elements (icons) in place."""
    done = False
    for n in list(el.contents):
        if isinstance(n, NavigableString) and n.strip():
            if not done:
                n.replace_with(" " + txt + " "); done = True
            else:
                n.extract()
    if not done:
        el.append(txt)

def build(lang):
    i = LANGS.index(lang)
    t = lambda k: C[k][i]
    P = PREFIX[lang]
    s = BeautifulSoup(open(TPL, encoding="utf-8").read(), "html.parser")

    # head
    s.html["lang"] = lang
    s.title.string = t("title")
    head = s.head
    for l in head.find_all("link"):
        l["href"] = "/" + l["href"]
    head.append(frag(f'<meta name="description" content="{t("desc")}">'))
    for L in LANGS:
        head.append(frag(f'<link rel="alternate" hreflang="{L}" href="https://dilerservices.com{PREFIX[L]}">'))
    head.append(frag('<link href="/css/diler.css" rel="stylesheet">'))
    head.append(frag('<meta name="robots" content="noindex">'))
    for sc in s.find_all("script"):
        sc["src"] = "/" + sc["src"]

    # preloader letters -> DILER
    txt = s.select_one(".txt-loading"); txt.clear()
    for ch in "DILER":
        txt.append(frag(f'<span data-text-preloader="{ch}" class="letters-loading">{ch}</span>'))
    s.select_one(".animation-preloader p").string = t("loading")

    # drop sections with staff names, invented reviews, and blog posts
    for sel in [".team-section", ".testimonial-section", ".news-secton"]:
        s.select_one(sel).decompose()

    # ---------- header ----------
    hdr = s.select_one("header.main-header")
    for a in hdr.select(".logo a, .nav-logo a"):
        a["href"] = P; a["aria-label"] = "Diler Services"
    set_html(hdr.select_one(".header-lower .logo a"), logo(False))
    set_html(hdr.select_one(".sticky-header .logo a"), logo(False))
    set_html(hdr.select_one(".mobile-menu .nav-logo a"), logo(True))
    nav = hdr.select_one(".header-lower .navigation")
    items = [(t("nav_home"), P, True), (t("nav_services"), P + "#services", False),
             (t("nav_pricing"), P + "#pricing", False), (t("nav_faq"), P + "#faq", False),
             (t("nav_contact"), P + "#contact", False)]
    set_html(nav, "".join(f'<li{" class=\"current\"" if cur else ""}><a href="{h}">{n}</a></li>' for n, h, cur in items))
    def switch(cls):
        return (f'<div class="{cls}" aria-label="{t("lang_label")}">' + "".join(
            f'<a href="{PREFIX[L]}" hreflang="{L}" lang="{L}"{" class=\"active\" aria-current=\"true\"" if L == lang else ""}>{L.upper()}</a>'
            for L in LANGS) + "</div>")
    hc = hdr.select_one(".header-contact")
    set_html(hc, switch("social-icon lang-switch") +
             f'<a href="mailto:{EMAIL}" class="info-btn"><i class="icon fa fa-envelope"></i> {EMAIL}</a>')
    btn = hdr.select_one(".outer-box > a.theme-btn")
    btn["href"] = P + "#pricing"; btn.string = t("cta_start")
    # compact switcher visible on mobile, next to the menu toggler
    hdr.select_one(".outer-box .mobile-nav-toggler").insert_before(frag(switch("lang-switch lang-switch-mobile")))
    cl = hdr.select_one(".contact-list-one")
    set_html(cl, f'<li><div class="contact-info-box"><span class="icon lnr-icon-envelope1"></span>'
                 f'<span class="title">{t("send_email")}</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>'
                 f'<li><div class="contact-info-box"><span class="icon fa fa-globe"></span>'
                 f'<span class="title">{t("lang_label")}</span>{switch("lang-switch lang-switch-menu")}</div></li>')
    hdr.select_one(".mobile-menu .social-links").decompose()

    # ---------- hero ----------
    h = s.select_one(".hero-section")
    img = h.select_one(".hero-image > img"); img["src"] = "/images/home-1/hero/hero-01.jpg"; img["alt"] = ""
    text_only(h.select_one(".hero-content h6"), t("hero_kicker"))
    h.select_one(".hero-content h1").string = t("hero_h1")
    h.select_one(".hero-content p").string = t("hero_p")
    a = h.select_one(".hero-button a"); a["href"] = P + "#pricing"; text_only(a, t("hero_btn"))

    # ---------- business solution ----------
    b = s.select_one(".business-solution-section")
    b.select_one("h2").string = t("bs_h2")
    ci = b.select_one(".client-image")
    set_html(ci, '<span class="lang-chip">EN</span><span class="lang-chip">ES</span><span class="lang-chip">PT</span>')
    b.select_one(".feature-left-content-1 h4").string = t("bs_lang_title")
    set_html(b.select_one(".star"), f'<span>{t("bs_lang_sub")}</span>')
    b.select_one(".feature-business-solution-items-1 h3").string = t("bs1_h")
    b.select_one(".feature-business-solution-items-1 p").string = t("bs1_p")
    b.select_one(".feature-business-solution-items-2 h3").string = t("bs2_h")
    b.select_one(".feature-business-solution-items-2 p").string = t("bs2_p")

    # ---------- about ----------
    ab = s.select_one(".about-section")
    ab["id"] = "about"
    im = ab.select_one(".about-image-1 img"); im["src"] = "/images/home-1/about/about-image.jpg"
    text_only(ab.select_one("h6.sub-title"), t("ab_sub"))
    ab.select_one(".sec-title h2").string = t("ab_h2")
    ab.select_one(".icon-items p").string = t("ab_icon_p")
    ab.select_one("p.about-text").string = t("ab_text")
    for li, k in zip(ab.select(".about-list li"), ["ab_l1", "ab_l2", "ab_l3", "ab_l4"]):
        text_only(li, t(k))
    set_html(ab.select_one(".counter-box .count-box h2"), '<span class="count-text" data-speed="1500" data-stop="3">0</span>')
    ab.select_one(".counter-bottom p").string = t("ab_count_lbl")

    # ---------- counters (all true numbers) ----------
    for box, (pre, n, suf, k) in zip(s.select(".counter-section .counter-box-1"),
        [("$", 99, "", "c1"), ("$", 125, "", "c2"), ("$", 129, "", "c3"), ("", 1, "", "c4")]):
        set_html(box.select_one("h2"), f'{pre}<span class="count-text" data-speed="2000" data-stop="{n}">0</span>{suf}')
        box.select_one("p").string = t(k)

    # ---------- services ----------
    sv = s.select_one(".service-section")
    sv["id"] = "services"; sv["style"] = "background-color:#144443;"
    text_only(sv.select_one("h6.sub-title"), t("sv_sub"))
    sv.select_one(".sec-title h2").string = t("sv_h2")
    set_html(sv.select_one(".section-counter-content h3"), '<span class="count-text" data-speed="1500" data-stop="3">0</span>')
    sv.select_one(".section-counter-content h6").string = t("sv_count_lbl")
    for card, n in zip(sv.select(".service-card-items"), range(1, 5)):
        a = card.select_one("h3 a"); a.string = t(f"sv{n}_h"); a["href"] = P + "#pricing"
        card.select_one(".content p").string = t(f"sv{n}_p")
        card.select_one("a.link-btn")["href"] = P + "#pricing"
        card.select_one("a.link-btn")["aria-label"] = t(f"sv{n}_h")

    # ---------- how it works (template case-study slider) ----------
    pj = s.select_one(".project-section")
    text_only(pj.select_one("h6.sub-title"), t("hw_sub"))
    set_html(pj.select_one(".sec-title h2"), t("hw_h2"))
    for k, card in enumerate(pj.select(".project-card-items"), 1):
        for im in card.select(".project-image img"): im["alt"] = ""
        a = card.select_one(".content h3 a"); a.string = t(f"hw{k}_h"); a["href"] = P + "#contact"
        card.select_one(".content p").string = t(f"hw{k}_p")
        card.select_one("a.icon")["href"] = P + "#contact"; card.select_one("a.icon")["aria-label"] = t(f"hw{k}_h")

    # ---------- marquee ----------
    words = t("mq")
    for g in s.select(".marquee-group"):
        texts = [d for d in g.select(".text") if not d.find("img")]
        for d, w in zip(texts, words): d.string = w
        if len(words) > len(texts):
            last = texts[-1]
            for w in words[len(texts):]:
                sep = copy.copy(g.select(".text img")[0].parent)
                nd = copy.copy(last); nd.string = w
                last.insert_after(sep); sep.insert_after(nd); last = nd

    # ---------- why choose ----------
    wc = s.select_one(".why-choose-section")
    set_html(wc.select_one(".icon-box-items h3"), t("wc_badge"))
    text_only(wc.select_one("h6.sub-title"), t("wc_sub"))
    wc.select_one(".sec-title h2").string = t("wc_h2")
    ids = ["fees", "language", "direct", "reminders"]
    for k, (a, pane) in enumerate(zip(wc.select("ul.nav a"), wc.select(".tab-pane"))):
        a["href"] = "#" + ids[k]; a.string = t("wc_tabs")[k]; pane["id"] = ids[k]
        pane.select_one(".why-choose-list h3").string = t("wc_h3")[k]
        pane.select_one(".why-choose-list p").string = t("wc_p")[k]
        for li, x in zip(pane.select(".why-list li"), t("wc_list")[k]): text_only(li, x)
        pane.select_one(".choose-us-progressbar").decompose()  # no invented percentages

    # ---------- pricing ----------
    pr = s.select_one(".pricing-section")
    pr["id"] = "pricing"
    text_only(pr.select_one("h6.sub-title"), t("pr_sub"))
    set_html(pr.select_one(".sec-title h2"), t("pr_h2"))
    tabs = pr.select("ul.nav a")
    tabs[0]["href"] = "#llc"; tabs[0].string = t("pr_tab1")
    tabs[1]["href"] = "#yearly"; tabs[1].string = t("pr_tab2")
    panes = pr.select(".tab-pane")
    panes[0]["id"] = "llc"; panes[1]["id"] = "yearly"
    for pane, plans, yearly in [(panes[0], LLC, False), (panes[1], YEARLY, True)]:
        boxes = pane.select(".pricing-box-items")
        for box, p in zip(boxes, plans):
            box.select_one(".pricing-header h3").string = p["name"]
            box.select_one(".pricing-header > span").string = p["summary"][i]
            tag = box.select_one(".gt-price-tag")
            if tag: tag.string = t("recommended")
            ul = box.select_one("ul.pricing-list")
            proto = ul.select_one("li")
            has_icon = proto.find("div", class_="icon") is not None
            icon = str(proto.find("div", class_="icon")) if has_icon else ""
            fee_line = (f'<li class="fee-line"><span class="fee-amt">{p["fee"]}</span> <span class="fee-lbl">{t("svc_fee")}{" " + t("per_year") if yearly else ""}</span></li>')
            if yearly:
                state_line = f'<li class="fee-line state-line"><span class="fee-detail">{p["sdet"][i]}</span></li>'
            else:
                state_line = (f'<li class="fee-line state-line"><span class="fee-amt small">+ {p["state"]}</span> <span class="fee-lbl">{t("state_fee")}</span>'
                              f'<span class="fee-detail">{p["sdet"][i]}</span></li>')
            set_html(ul, fee_line + state_line + "".join(f"<li>{icon}{x}</li>" for x in p["inc"][i]))
            a = box.select_one(".pricing-button a"); a["href"] = P + "#contact"
            a.string = f'{t("choose")} {p["name"]}'
    note = frag(f'<p class="pricing-note wow fadeInUp">{t("pr_note")}</p>')
    pr.select_one(".tab-content").insert_after(note)

    # ---------- contact (Netlify form) ----------
    ct = s.select_one(".contact-section")
    ct["id"] = "contact"
    text_only(ct.select_one("h6.sub-title"), t("ct_sub"))
    ct.select_one(".sec-title h2").string = t("ct_h2")
    f = ct.select_one("form")
    f.attrs = {"name": "contact", "method": "POST", "action": P + "thanks/", "data-netlify": "true",
               "netlify-honeypot": "bot-field", "class": ["form-box", "wow", "fadeInUp"], "data-wow-delay": ".3s"}
    rows = f.select(".form-clt")
    set_html(rows[0], f'<input type="text" name="name" id="name" placeholder="{t("f_name")}" aria-label="{t("f_name")}" required autocomplete="name">')
    set_html(rows[1], f'<input type="email" name="email" id="email" placeholder="{t("f_email")}" aria-label="{t("f_email")}" required autocomplete="email">')
    set_html(rows[2], f'<input type="text" name="business" id="business" placeholder="{t("f_biz")}" aria-label="{t("f_biz")}">')
    set_html(rows[3], f'<textarea name="message" id="message" placeholder="{t("f_msg")}" aria-label="{t("f_msg")}"></textarea>')
    set_html(rows[4], f'<button class="theme-btn btn-style-one w-100" type="submit">{t("f_btn")}</button>')
    f.insert(0, frag(f'<input type="hidden" name="form-name" value="contact"><input type="hidden" name="language" value="{lang}">'
                     '<p hidden><label>Do not fill this out <input name="bot-field"></label></p>'))
    ct.select_one(".contact-image-1 > img")["alt"] = ""
    ct.select_one(".contact-info-box h2").string = t("ct_box_h")
    lis = ct.select(".contact-info-box .contact-list li")
    # first item (phone) becomes languages; second stays email
    lis[0].select_one(".icon img")["src"] = "/images/home-1/contact/email.svg"
    set_html(lis[0].select_one(".content"), f'<h3>{t("ct_mail")}</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>')
    set_html(lis[1].select_one(".icon"), '<i class="fa fa-globe" style="color:#144443;font-size:22px"></i>')
    set_html(lis[1].select_one(".content"), f'<h3>{t("ct_lang")}</h3><p>{t("ct_lang_v")}</p>')

    # ---------- faq ----------
    fq = s.select_one(".faq-section")
    fq["id"] = "faq"
    text_only(fq.select_one("h6.sub-title"), t("fq_sub"))
    fq.select_one(".sec-title h2").string = t("fq_h2")
    fq.select_one(".faq-image > img")["alt"] = ""
    fq.select_one(".faq-image .shape-2").decompose()  # template badge shows invented review counts
    box = fq.select_one("ul.accordion-box")
    blocks = box.select("li.accordion")
    faqs = t("faqs")
    while len(blocks) < len(faqs):
        nb = copy.copy(blocks[-1]); blocks[-1].insert_after(nb); blocks.append(nb)
    for blk, (q, ans) in zip(blocks, faqs):
        text_only(blk.select_one(".acc-btn"), q)
        blk.select_one(".acc-content .text").string = ans

    # ---------- cta ----------
    cta = s.select_one(".cta-contact-section")
    cta.select_one(".cta-contact-wrapper")["style"] = "background-color:#144443;"
    cta.select_one("h3").string = t("cta_h3")
    a = cta.select_one("a.theme-btn"); a["href"] = P + "#contact"; a.string = t("cta_btn")

    # ---------- footer ----------
    ft = s.select_one("footer")
    set_html(ft.select_one(".footer-newsletter-left h3"), t("ft_news_h3"))
    fform = ft.select_one(".footer-newsletter-wrapper form")
    arrow = fform.select_one("button.arrow-icon")
    newa = frag(f'<a href="mailto:{EMAIL}" class="footer-mail wow fadeInUp" data-wow-delay=".5s">'
                f'<span class="form-clt"><span class="footer-mail-text">{EMAIL}</span></span></a>')
    a2 = newa.a
    arrow.name = "span"; arrow.attrs = {"class": ["arrow-icon"]}
    a2.select_one(".form-clt").append(arrow)
    fform.replace_with(newa)
    fl = ft.select_one(".footer-logo"); fl["href"] = P; set_html(fl, logo(True))
    ft.select_one(".footer-content p").string = t("ft_about")
    ft.select_one(".footer-content .social-icon").replace_with(frag(switch("social-icon lang-switch")))
    cols = ft.select(".footer-widget-items")
    cols[1].select_one("h3").string = t("ft_company")
    set_html(cols[1].select_one("ul"), "".join(f'<li><a href="{h}">{n}</a></li>' for n, h, _ in items))
    cols[2].select_one("h3").string = t("ft_services")
    set_html(cols[2].select_one("ul"), "".join(f'<li><a href="{P}#pricing">{x}</a></li>' for x in t("mq")[:4]))
    cols[3].select_one("h3").string = t("ft_contact")
    cl = cols[3].select_one("ul.contact-list")
    em = cl.select("li")[1]
    em.select_one("a")["href"] = f"mailto:{EMAIL}"; em.select_one("a").string = EMAIL
    set_html(cl, str(em))
    ft.select_one(".footer-bottom p").string = t("ft_copy")

    # absolute asset paths everywhere
    for tag in s.find_all(["img"]):
        if not tag["src"].startswith(("/", "http")): tag["src"] = "/" + tag["src"]
        if tag.get("alt") in ("img", None): tag["alt"] = ""
    out = str(s)
    out = re.sub(r"url\(\s*'?(images/)", lambda m: "url('/" + m.group(1) if "'" in m.group(0) else "url(/" + m.group(1), out)
    return out

def thanks(lang, home_html):
    i = LANGS.index(lang); P = PREFIX[lang]
    s = BeautifulSoup(home_html, "html.parser")
    wrapper = s.select_one(".page-wrapper")
    keep = {"header", "footer"}
    for el in list(wrapper.find_all(["section", "div"], recursive=False)):
        if el.name == "section" or "marquee-section" in (el.get("class") or []):
            el.decompose()
    sec = frag(f'<section class="section-padding" style="padding:160px 0 120px"><div class="auto-container text-center">'
               f'<div class="sec-title text-center mb-0"><h2>{C["pg_thanks_h1"][i]}</h2></div>'
               f'<p style="margin:20px 0 30px">{C["thanks_p"][i]}</p>'
               f'<a href="{P}" class="theme-btn btn-style-one">{C["back_home"][i]}</a></div></section>')
    s.select_one("header").insert_after(sec)
    s.title.string = C["pg_thanks_h1"][i] + " | Diler Services"
    return str(s)

for L in LANGS:
    d = OUT + PREFIX[L]
    os.makedirs(d + "thanks", exist_ok=True)
    html = build(L)
    open(d + "index.html", "w", encoding="utf-8").write(html)
    open(d + "thanks/index.html", "w", encoding="utf-8").write(thanks(L, html))
print("built", OUT)
