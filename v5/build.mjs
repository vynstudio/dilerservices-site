import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { homeCopy } from "./build/home-copy.mjs";
import { pages, ui } from "./build/copy.mjs";

const v5 = path.dirname(fileURLToPath(import.meta.url));
const site = "https://dilerservices.com";
const langs = ["en", "es", "pt"];

function esc(value) {
  return String(value).replace(/[&<>"]/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]));
}

function prefixes(lang, rel) {
  const depth = rel.split("/").length - 1;
  return {
    asset: "../".repeat(lang === "en" ? depth : depth + 1),
    langRoot: "../".repeat(depth),
  };
}

function canonical(lang, rel) {
  if (rel === "index.html") return lang === "en" ? `${site}/` : `${site}/${lang}/`;
  const clean = rel.endsWith("/index.html") ? rel.slice(0, -11) : rel.replace(/\.html$/, "");
  return `${site}${lang === "en" ? "" : `/${lang}`}/${clean}`;
}

function langHref(fromLang, rel, toLang) {
  const from = fromLang === "en" ? rel : `${fromLang}/${rel}`;
  const to = toLang === "en" ? rel : `${toLang}/${rel}`;
  let href = path.posix.relative(path.posix.dirname(from), to);
  if (!href.startsWith(".")) href = `./${href}`;
  return href;
}

function absFor(lang, rel) {
  return canonical(lang, rel);
}

function shell(lang, rel, page, main) {
  const t = ui[lang];
  const { asset, langRoot } = prefixes(lang, rel);
  const url = canonical(lang, rel);
  const alternates = langs.map((code) => `<link rel="alternate" hreflang="${code}" href="${absFor(code, rel)}">`).join("");
  const nav = [
    ["home", `${langRoot}index.html`, t.home],
    ["services", `${langRoot}services/index.html`, t.services],
    ["pricing", `${langRoot}pricing.html`, t.pricing],
    ["about", `${langRoot}about.html`, t.about],
    ["contact", `${langRoot}contact.html`, t.contact],
  ];
  const link = ([key, href, label]) => `<a href="${href}"${page.nav === key ? ' aria-current="page"' : ""}>${esc(label)}</a>`;
  const langsMenu = (role) => langs.map((code) => {
    const checked = code === lang ? "true" : "false";
    return `<li role="none"><a role="menuitemradio" aria-checked="${checked}" href="${langHref(lang, rel, code)}" lang="${code}" hreflang="${code}">${t.langName[code]}</a></li>`;
  }).join("");
  const logo = `<a class="logo" href="${langRoot}index.html" aria-label="${esc(t.homeLabel)}"><span class="logo-mark"><img src="${asset}assets/brand/mark.svg" alt="" width="26" height="26"></span><span class="logo-word">Diler <span>Services</span></span></a>`;
  const checkout = page.checkout ? `<script type="module" src="${asset}assets/js/checkout.js"></script>` : "";
  const robots = page.noindex ? `<meta name="robots" content="noindex">` : "";
  return `<!DOCTYPE html>
<html lang="${lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(page.title)}</title>
<meta name="description" content="${esc(page.description)}">
${robots}
<meta name="theme-color" content="#f7f4ee">
<link rel="canonical" href="${url}">
<link rel="alternate" hreflang="en" href="${absFor("en", rel)}">
<link rel="alternate" hreflang="es" href="${absFor("es", rel)}">
<link rel="alternate" hreflang="pt" href="${absFor("pt", rel)}">
<link rel="alternate" hreflang="x-default" href="${absFor("en", rel)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Diler Services">
<meta property="og:locale" content="${t.locale}">
<meta property="og:title" content="${esc(page.title)}">
<meta property="og:description" content="${esc(page.description)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${site}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(page.title)}">
<meta name="twitter:description" content="${esc(page.description)}">
<meta name="twitter:image" content="${site}/assets/img/og.jpg">
<link rel="icon" href="${asset}assets/brand/mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="${asset}assets/brand/apple-touch-icon.png">
<link rel="preload" href="${asset}assets/fonts/Rafory.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="${asset}assets/css/site.css">
${page.schema || ""}
</head>
<body id="top">
<a class="skip" href="#content">${esc(t.skip)}</a>
<header class="site-header">
  <div class="wrap header-bar">
    ${logo}
    <nav class="nav-desk" aria-label="${esc(t.primary)}">${nav.map(link).join("")}</nav>
    <div class="nav-tools">
      <div class="lang-menu" data-lang>
        <button class="lang-btn" type="button" data-lang-toggle aria-expanded="false" aria-haspopup="menu" aria-controls="lang-menu-desk" aria-label="${esc(t.choose)}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18"></path><path d="M12 3c2.6 2.7 3.9 5.8 3.9 9s-1.3 6.3-3.9 9c-2.6-2.7-3.9-5.8-3.9-9s1.3-6.3 3.9-9z"></path></svg>
        </button>
        <ul class="lang-list" id="lang-menu-desk" data-lang-list role="menu" hidden>${langsMenu()}</ul>
      </div>
      <a class="btn btn-gold" href="${langRoot}services/llc.html" data-start-llc>${esc(t.start)}</a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="nav-panel" aria-label="${esc(t.open)}"><span></span></button>
    </div>
  </div>
</header>
<div class="nav-panel" id="nav-panel" data-nav-panel hidden>
  ${nav.map(link).join("\n  ")}
  <ul class="lang-list" role="menu" aria-label="${esc(t.language)}">${langsMenu()}</ul>
  <a class="btn btn-gold" href="${langRoot}services/llc.html" data-start-llc>${esc(t.start)}</a>
</div>
<noscript><nav class="noscript-nav wrap" aria-label="${esc(t.primary)}">${nav.map(link).join("")}<a href="${langRoot}services/llc.html">${esc(t.start)}</a>${langs.map((code) => `<a href="${langHref(lang, rel, code)}" lang="${code}" hreflang="${code}">${t.langName[code]}</a>`).join("")}</nav></noscript>
<main id="content">
${main}
</main>
<footer class="footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        ${logo}
        <p class="disclaimer">${esc(t.disclaimer)}</p>
      </div>
      <div>
        <h2>${esc(t.navigate)}</h2>
        <ul>${nav.map(([key, href, label]) => `<li>${link([key, href, label])}</li>`).join("")}</ul>
      </div>
      <div>
        <h2>${esc(t.policies)}</h2>
        <ul>
          <li><a href="${langRoot}privacy.html">${esc(t.privacy)}</a></li>
          <li><a href="${langRoot}terms.html">${esc(t.terms)}</a></li>
          <li><a href="${langRoot}refund.html">${esc(t.refund)}</a></li>
        </ul>
      </div>
      <div>
        <h2>${esc(t.contact)}</h2>
        <ul>
          <li><a href="mailto:info@dilerservices.com">info@dilerservices.com</a></li>
          <li>Lake Wales, FL</li>
          <li>${esc(t.languages)}</li>
        </ul>
      </div>
    </div>
    <div class="legal-bar">
      <span>${esc(t.rights)}</span>
      <span>
        <a href="${langRoot}privacy.html">${esc(t.privacy)}</a>
        <a href="${langRoot}terms.html">${esc(t.terms)}</a>
        <a href="${langRoot}refund.html">${esc(t.refund)}</a>
      </span>
    </div>
  </div>
</footer>
<script src="${asset}assets/js/nav.js" defer data-root="${langRoot}"></script>
${checkout}
</body>
</html>
`;
}

function faqSchema(items) {
  return `<script type="application/ld+json">${JSON.stringify({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: items.map((item) => ({
      "@type": "Question",
      name: item.q,
      acceptedAnswer: { "@type": "Answer", text: item.a },
    })),
  })}</script>`;
}

function write(file, html) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, html);
}

const written = [];
for (const lang of langs) {
  for (const page of pages) {
    const rel = page.file;
    const copy = page[lang];
    const html = shell(lang, rel, {
      title: copy.title,
      description: copy.description,
      nav: page.nav,
      checkout: page.checkout || false,
      noindex: page.noindex || false,
      schema: copy.faqs ? faqSchema(copy.faqs) : "",
    }, copy.main(prefixes(lang, rel).langRoot, ui[lang], lang));
    const dest = path.join(lang === "en" ? v5 : path.join(v5, lang), rel);
    write(dest, html);
    if (!page.noindex) written.push(canonical(lang, rel));
  }
}

function localizeHome(lang) {
  let html = fs.readFileSync(path.join(v5, "index.html"), "utf8");
  html = html.replace("<html lang=\"en\">", `<html lang="${lang}">`);
  html = html.replaceAll('="assets/', '="../assets/');
  html = html.replaceAll('href="./" lang="en"', 'href="__EN__" lang="en"');
  html = html.replaceAll('href="es/"', 'href="__ES__"');
  html = html.replaceAll('href="pt/"', 'href="__PT__"');
  html = html.replaceAll('href="#top"', 'href="./"');
  const map = lang === "es"
    ? { __EN__: "../", __ES__: "./", __PT__: "../pt/" }
    : { __EN__: "../", __ES__: "../es/", __PT__: "./" };
  for (const [token, href] of Object.entries(map)) html = html.replaceAll(`href="${token}"`, `href="${href}"`);
  html = html.replaceAll('aria-checked="true"', 'aria-checked="false"');
  html = html.replaceAll('aria-checked="false" href="./"', 'aria-checked="true" href="./"');
  html = html.replace('content="en_US"', `content="${ui[lang].locale}"`);
  html = html.replace('rel="canonical" href="https://dilerservices.com/"', `rel="canonical" href="${canonical(lang, "index.html")}"`);
  html = html.replace('property="og:url" content="https://dilerservices.com/"', `property="og:url" content="${canonical(lang, "index.html")}"`);
  const entries = Object.entries(homeCopy[lang]).sort((a, b) => b[0].length - a[0].length);
  for (const [from, to] of entries) html = html.split(from).join(to);
  write(path.join(v5, lang, "index.html"), html);
  written.push(canonical(lang, "index.html"));
}

localizeHome("es");
localizeHome("pt");
written.unshift(`${site}/`);

const urls = [...new Set(written)].sort();
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((loc) => `  <url><loc>${loc}</loc><lastmod>2026-10-22</lastmod></url>`).join("\n")}
</urlset>
`;
fs.writeFileSync(path.join(v5, "sitemap.xml"), sitemap);
console.log(`Wrote ${urls.length} URLs`);
