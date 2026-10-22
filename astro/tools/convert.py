"""One-off converter: turns the generated Finclix EN home (finclix/index.html) into Astro section
components, and exports copy (content.py) to src/data/content.json. Run from astro/."""
import json, re, sys, os, shutil, copy
sys.path.insert(0, "../finclix-build")
os.chdir("../finclix-build"); import content as C0; import build as B; os.chdir("../astro")
from bs4 import BeautifulSoup, NavigableString, Comment

LANGS = ["en", "es", "pt"]
# ---------- content.json ----------
data = {}
for i, L in enumerate(LANGS):
    d = {k: v[i] for k, v in C0.C.items()}
    d["faqs"] = [list(x) for x in d["faqs"]]
    if L == "en":
        d["faqs"] += [list(x) for x in B.EN_EXTRA_FAQ]
        d["title"], d["desc"] = B.EN_TITLE, B.EN_DESC
    def plan(p):
        o = {"name": p["name"], "fee": p["fee"], "rec": p["rec"], "summary": p["summary"][i], "sdet": p["sdet"][i], "inc": p["inc"][i]}
        if p.get("state"): o["state"] = p["state"]
        if p.get("monthly"): o["monthly"] = p["monthly"][i]
        return o
    d["llc"] = [plan(p) for p in C0.LLC]; d["yearly"] = [plan(p) for p in C0.YEARLY]
    data[L] = d
os.makedirs("src/data", exist_ok=True)
json.dump({"email": C0.EMAIL, **data}, open("src/data/content.json", "w"), ensure_ascii=False, indent=1)
en = data["en"]

src = BeautifulSoup(open("../finclix/index.html").read(), "html.parser")
schema = [json.loads(x.string) for x in src.select('script[type="application/ld+json"]')]
json.dump(schema, open("src/data/schema-en.json", "w"), ensure_ascii=False, indent=1)

# flatten copy for text substitution
flat = {}
def addf(path, v):
    if isinstance(v, str): flat.setdefault(re.sub(r"\s+", " ", v.replace("<br>", "<br/>")).strip(), path)
    elif isinstance(v, list):
        for j, x in enumerate(v): addf(f"{path}[{j}]", x)
    elif isinstance(v, dict):
        for k, x in v.items(): addf(f"{path}.{k}", x)
for k, v in en.items(): addf("t." + k, v)

ICONS = {
 "plus": '<path d="M12 5v14M5 12h14"/>', "times": '<path d="M6 6l12 12M18 6L6 18"/>',
 "angle-up": '<path d="M6 15l6-6 6 6"/>', "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>', "bars": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "envelope": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>',
}
def icon_svg(name, keep):
    return (f'<svg class="{" ".join(keep + ["ico"])}" viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

ANIM = re.compile(r"^(wow|fadeIn\w*|bounceIn\w*|slideIn\w*|zoomIn\w*|img-custom-anim-\w+|float-bob-\w|bounce-\w)$")
imports = {}
def asset_var(path):
    v = "img_" + re.sub(r"\W", "_", path.split("/images/")[-1].rsplit(".", 1)[0])
    imports[v] = path
    return v

REMOVE = [  # decorative clutter
 ".preloader", ".scroll-to-top", ".sticky-header", ".marquee-section", ".cta-contact-section",
 ".about-section .star-shape", ".about-section .arrow-shape-1", ".about-section .arrow-shape-2", ".about-section .butterfly-shape",
 ".faq-section .shape-1", ".contact-section .contact-shape", ".contact-section .contact-info-box .ellipse-bg",
 ".project-section .shape-1", ".project-section .shape-2", ".project-section .arrow-shape",
 ".business-solution-section .spiral-shape",
]

def clean(el):
    for sel in REMOVE:
        for x in el.select(sel): x.decompose()
    for c in el.find_all(string=lambda x: isinstance(x, Comment)): c.extract()
    # duplicate hover images
    for box in el.select(".business-image, .project-image"):
        imgs = box.find_all("img", recursive=False)
        for x in imgs[1:]: x.decompose()
    for box in el.select(".pricing-header .title-icon"):
        imgs = box.find_all("img")
        for x in imgs[1:]: x.decompose()
    for t in el.find_all(True):
        cls = t.get("class")
        if cls:
            anim = any(ANIM.match(c) for c in cls if c not in ("float-bob-y", "float-bob-x") ) or "wow" in cls
            new = [c for c in cls if not ANIM.match(c)]
            if "wow" in cls: new.append("reveal")
            if new: t["class"] = new
            else: del t["class"]
        for a in list(t.attrs):
            if a.startswith("data-wow") or a in ("data-speed",): del t[a]
        if t.name == "a" and t.get("data-bs-toggle"):
            t["data-tab"] = t["href"]; del t["data-bs-toggle"]
    for c in el.select(".count-text"):
        c.string = c["data-stop"]; del c["data-stop"]
    for i in el.select("i[class*=fa], span[class*=lnr-icon], div.icon.fa"):
        cls = i.get("class", [])
        name = next((re.sub(r"^(fa-|lnr-icon-)", "", c) for c in cls if c.startswith(("fa-", "lnr-icon-")) and c not in ("fa-regular",)), None)
        name = {"envelope1": "envelope"}.get(name, name)
        keep = [c for c in cls if not c.startswith(("fa", "lnr"))]
        new = BeautifulSoup(icon_svg(name, keep), "html.parser").svg
        if i.name == "div":  # accordion icon keeps its box
            i.attrs = {"class": keep}; i.clear(); i.append(BeautifulSoup(icon_svg(name, []), "html.parser").svg)
        else:
            i.replace_with(new)
    return el

def to_astro(el):
    """serialize to Astro markup: copy -> {t.x}, images -> <Picture>, svg attr case fixed."""
    # html copy with <br>
    for t in el.find_all(True):
        inner = re.sub(r"\s+", " ", t.decode_contents()).strip()
        if "<br/>" in inner and inner in flat:
            t.clear(); t.append(NavigableString(f"@@HTML{flat[inner]}@@"))
    for s in el.find_all(string=True):
        txt = re.sub(r"\s+", " ", s).strip()
        if not txt or s.parent.name in ("style", "script"): continue
        if txt in flat:
            s.replace_with(s.replace(s.strip(), "@@" + flat[txt] + "@@") if s.strip() == txt else "@@" + flat[txt] + "@@")
    for img in el.find_all("img"):
        p = img["src"]
        if p.endswith(".svg"):
            continue
        v = asset_var(p)
        attrs = " ".join(f'{k}="{" ".join(x) if isinstance(x, list) else x}"' for k, x in img.attrs.items() if k not in ("src",))
        img.replace_with(NavigableString(f"@@PIC{v}|{attrs}@@"))
    for a in el.find_all(attrs={"placeholder": True}):
        ph = re.sub(r"\s+", " ", a["placeholder"]).strip()
        if ph in flat: a["placeholder"] = f"@@ATTR{flat[ph]}@@"
    for a in el.find_all(attrs={"aria-label": True}):
        ph = a["aria-label"].strip()
        if ph in flat: a["aria-label"] = f"@@ATTR{flat[ph]}@@"
    out = str(el)
    out = re.sub(r'"@@ATTR(.+?)@@"', r"{\1}", out)
    out = re.sub(r"@@HTML(.+?)@@", r"<Fragment set:html={\1} />", out)
    def pic(m):
        v, attrs = m.group(1), m.group(2)
        lazy = "" if "hero-image" in attrs else ' loading="lazy"'
        return f'<Picture src={{{v}}} formats={{["avif","webp"]}} {attrs}{lazy} />'
    out = re.sub(r"@@PIC(\w+)\|(.*?)@@", pic, out)
    out = re.sub(r"@@(t\.[\w\.\[\]]+)@@", r"{\1}", out)
    for a in ("viewbox", "lineargradient", "gradientunits", "stop-color", "clippath", "clip-path"):
        pass
    out = out.replace("viewbox=", "viewBox=").replace("<lineargradient", "<linearGradient").replace("</lineargradient>", "</linearGradient>")
    out = out.replace("gradientunits=", "gradientUnits=").replace("<clippath", "<clipPath").replace("</clippath>", "</clipPath>")
    out = out.replace("<radialgradient", "<radialGradient").replace("</radialgradient>", "</radialGradient>")
    return out

SECTIONS = {"hero-section": "Hero", "business-solution-section": "BusinessSolution", "about-section": "About",
            "counter-section": "Counters", "service-section": "Services", "project-section": "HowItWorks",
            "why-choose-section": "WhyChoose", "contact-section": "Contact"}
os.makedirs("src/components", exist_ok=True)
pw = src.select_one(".page-wrapper")
for el in pw.find_all(recursive=False):
    cls = el.get("class", [])[0]
    if cls not in SECTIONS: continue
    imports.clear()
    body = to_astro(clean(copy.copy(el)))
    imp = "\n".join(f"import {v} from '../assets{p.split('/images')[1] if p.startswith('/images') else p}';" for v, p in imports.items())
    fm = ("---\nimport { Picture } from 'astro:assets';\n" if imports else "---\n") + imp + "\nconst { t } = Astro.props;\n---\n"
    open(f"src/components/{SECTIONS[cls]}.astro", "w").write(fm + body + "\n")
    left = sorted(set(re.sub(r"\s+", " ", x).strip() for x in BeautifulSoup(body, "html.parser").find_all(string=True)
                      if re.sub(r"\s+", " ", x).strip() and not re.search(r"\{t\.|^\{|set:html", x)))
    print(SECTIONS[cls], "unmapped text:", left[:30])

# raw cleaned header/footer/pricing/faq for hand-written components (reference only)
os.makedirs("tools/ref", exist_ok=True)
for sel, n in ((".main-header", "header"), ("footer", "footer"), (".pricing-section", "pricing"), (".faq-section", "faq")):
    open(f"tools/ref/{n}.html", "w").write(clean(copy.copy(src.select_one(sel))).prettify())
