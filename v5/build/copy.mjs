import { agent, agreement, annual, bundle, ein } from "./catalog.mjs";

function esc(value) {
  return String(value).replace(/[&<>"]/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]));
}

export const ui = {
  en: {
    locale: "en_US",
    langName: { en: "English", es: "Español", pt: "Português" },
    skip: "Skip to content",
    homeLabel: "Diler Services home",
    primary: "Primary",
    choose: "Choose language",
    open: "Open menu",
    language: "Language",
    home: "Home",
    services: "Services",
    pricing: "Pricing",
    about: "About",
    contact: "Contact",
    start: "Start an LLC",
    privacy: "Privacy",
    terms: "Terms",
    refund: "Refund Policy",
    navigate: "Navigate",
    policies: "Policies",
    disclaimer: "Diler Services is not a law firm and does not provide legal advice. We answer in English, Spanish, and Portuguese.",
    languages: "English, Spanish, and Portuguese",
    rights: "© 2026 Diler Services. All rights reserved.",
    ourFee: "Our fee",
    stateFee: "Florida state fee",
    cardFee: "Card processing fee",
    pending: "Stripe test checkout is wired. Add a pk_test key and Price IDs in checkout-config.mjs to load the payment form. No live charge is set up.",
    payTitle: "Pay our fee",
    payLede: "The card processing fee is 3.5% of our fee and any Florida state fee, on its own line. This checkout is test mode only.",
    checkout: "Continue to checkout",
    send: "Send",
    name: "Name",
    email: "Email",
    topic: "What do you need?",
    message: "Message",
    book: "Book a call",
  },
  es: {
    locale: "es_ES",
    langName: { en: "English", es: "Español", pt: "Português" },
    skip: "Saltar al contenido",
    homeLabel: "Inicio de Diler Services",
    primary: "Principal",
    choose: "Elegir idioma",
    open: "Abrir menú",
    language: "Idioma",
    home: "Inicio",
    services: "Servicios",
    pricing: "Precios",
    about: "Nosotros",
    contact: "Contacto",
    start: "Formar una LLC",
    privacy: "Privacidad",
    terms: "Términos",
    refund: "Reembolsos",
    navigate: "Navegar",
    policies: "Políticas",
    disclaimer: "Diler Services no es un bufete de abogados y no da asesoría legal. Respondemos en inglés, español y portugués.",
    languages: "Inglés, español y portugués",
    rights: "© 2026 Diler Services. Todos los derechos reservados.",
    ourFee: "Nuestro cargo",
    stateFee: "Tasa del estado de Florida",
    cardFee: "Cargo por procesamiento de tarjeta",
    pending: "El pago de prueba de Stripe está conectado. Agregue una clave pk_test y los Price IDs en checkout-config.mjs para cargar el formulario. No hay ningún cobro real.",
    payTitle: "Pague nuestro cargo",
    payLede: "El cargo de la tarjeta es el 3.5% de nuestro cargo y de la tasa de Florida, en su propia línea. Este pago está solo en modo de prueba.",
    checkout: "Seguir al pago",
    send: "Enviar",
    name: "Nombre",
    email: "Correo",
    topic: "¿Qué necesita?",
    message: "Mensaje",
    book: "Agendar una llamada",
  },
  pt: {
    locale: "pt_BR",
    langName: { en: "English", es: "Español", pt: "Português" },
    skip: "Pular para o conteúdo",
    homeLabel: "Início da Diler Services",
    primary: "Principal",
    choose: "Escolher idioma",
    open: "Abrir menu",
    language: "Idioma",
    home: "Início",
    services: "Serviços",
    pricing: "Preços",
    about: "Sobre",
    contact: "Contato",
    start: "Formar uma LLC",
    privacy: "Privacidade",
    terms: "Termos",
    refund: "Reembolso",
    navigate: "Navegar",
    policies: "Políticas",
    disclaimer: "A Diler Services não é um escritório de advocacia e não oferece aconselhamento jurídico. Respondemos em inglês, espanhol e português.",
    languages: "Inglês, espanhol e português",
    rights: "© 2026 Diler Services. Todos os direitos reservados.",
    ourFee: "Nossa taxa",
    stateFee: "Taxa do estado da Flórida",
    cardFee: "Taxa de processamento do cartão",
    pending: "O checkout de teste da Stripe está ligado. Adicione uma chave pk_test e os Price IDs em checkout-config.mjs para carregar o formulário. Nenhum pagamento real está ativo.",
    payTitle: "Pague nossa taxa",
    payLede: "A taxa do cartão é 3,5% da nossa taxa e de qualquer taxa da Flórida, em uma linha própria. Este checkout fica só em modo de teste.",
    checkout: "Seguir para o pagamento",
    send: "Enviar",
    name: "Nome",
    email: "E-mail",
    topic: "Do que você precisa?",
    message: "Mensagem",
    book: "Marcar uma ligação",
  },
};

const refund = {
  en: "If the state rejects your filing and we can't fix it, we refund our fee.",
  es: "Si el estado rechaza su presentación y no podemos corregirla, le devolvemos nuestro cargo.",
  pt: "Se o estado recusar o seu registro e não pudermos corrigir, devolvemos a nossa taxa.",
};

const prompt = {
  en: "We file promptly once your details are complete. We don't name a day or a week. Florida sets the pace after that.",
  es: "Presentamos el trámite en cuanto sus datos están completos. No prometemos un día ni una semana. Florida marca el ritmo después.",
  pt: "Protocolamos assim que seus dados estão completos. Não prometemos um dia nem uma semana. A Flórida define o ritmo depois disso.",
};

function steps(items) {
  return `<div class="steps">${items.map((item, i) => `<article><b>0${i + 1}</b><h3>${esc(item.h)}</h3><p>${esc(item.p)}</p></article>`).join("")}</div>`;
}

function points(items) {
  return `<ul class="points">${items.map((item) => `<li><span class="ico" aria-hidden="true"></span><div><strong>${esc(item.h)}</strong>${esc(item.p)}</div></li>`).join("")}</ul>`;
}

function faq(items) {
  return `<div class="faq">${items.map((item, i) => `<details${i === 0 ? " open" : ""}><summary>${esc(item.q)}</summary><p>${esc(item.a)}</p></details>`).join("")}</div>`;
}

function pay(lang, t, product, options) {
  const ret = `${lang === "en" ? "" : `/${lang}`}/checkout/return.html`;
  const picks = options
    ? `<div class="choice">${options.map((item) => `<button type="button" class="btn btn-line" data-pick="${item.id}">${esc(item.label)}</button>`).join("")}</div>`
    : "";
  const slots = (options || [{ id: product }]).map((item) => `<div data-product="${item.id}"></div>`).join("");
  return `<section class="section section-warm tight" id="checkout" data-checkout="${product}" data-return-path="${ret}" data-our-fee="${esc(t.ourFee)}" data-state-fee="${esc(t.stateFee)}" data-card-fee="${esc(t.cardFee)}" data-pending="${esc(t.pending)}">
    <div class="wrap split">
      <div class="copy">
        <h2>${esc(t.payTitle)}</h2>
        <p class="lede">${esc(t.payLede)}</p>
        ${picks}
      </div>
      ${slots}
    </div>
  </section>`;
}

function pack(file, nav, checkout, data) {
  const out = { file, nav, checkout: Boolean(checkout) };
  for (const lang of ["en", "es", "pt"]) {
    const copy = data[lang];
    out[lang] = {
      title: copy.title,
      description: copy.description,
      faqs: copy.faqs || null,
      main(langRoot, t, code) {
        return data.kind === "service"
          ? serviceMain({ ...copy, product: data.product, options: copy.options }, code, t, langRoot)
          : data.render(copy, langRoot, t, code);
      },
    };
  }
  return out;
}

const services = [
  {
    file: "services/llc.html",
    product: "llc",
    en: {
      title: "Form a Florida LLC | Diler Services",
      description: "Form a Florida LLC with a local Lake Wales shop. Our fee is $89. Florida's state fee is $125. Test-mode checkout, no live charge.",
      kicker: "Florida LLC",
      h1: "Form a Florida LLC.",
      lede: "You tell us about the business. We prepare the paperwork and file it with the State of Florida.",
      price: "Our fee is $89. Florida's state fee is $125.",
      how: "How the filing goes",
      faqTitle: "Questions on a Florida LLC",
      steps: [
        { h: "Tell us about the business", p: "Name, address, and who is involved. A short set is enough to start." },
        { h: "We prepare and file", p: "We review every detail, then file the articles with Florida." },
        { h: "You get the record", p: "You can follow Filed, Approved, and the documents that come back." },
      ],
      faqs: [
        { q: "How do I form a Florida LLC?", a: "Share the business name, the address, and who is involved. We prepare the articles and file them with the State of Florida." },
        { q: "What does the $89 cover?", a: "It is our fee to prepare and file the Florida LLC. Florida's state fee is $125, listed on its own." },
        { q: "What if Florida rejects the filing?", a: refund.en },
      ],
    },
    es: {
      title: "Formar una LLC en Florida | Diler Services",
      description: "Forme una LLC en Florida con un taller local en Lake Wales. Nuestro cargo es $89. La tasa de Florida es $125. Pago solo en modo de prueba.",
      kicker: "LLC en Florida",
      h1: "Forme una LLC en Florida.",
      lede: "Usted nos cuenta del negocio. Nosotros preparamos los papeles y los presentamos ante el estado de Florida.",
      price: "Nuestro cargo es $89. La tasa del estado de Florida es $125.",
      how: "Cómo sigue el trámite",
      faqTitle: "Preguntas sobre una LLC en Florida",
      steps: [
        { h: "Cuéntenos del negocio", p: "Nombre, dirección y quiénes participan. Con poco se puede empezar." },
        { h: "Preparamos y presentamos", p: "Revisamos cada dato y presentamos los artículos en Florida." },
        { h: "Usted recibe el registro", p: "Puede seguir Presentado, Aprobado y los documentos que regresan." },
      ],
      faqs: [
        { q: "¿Cómo formo una LLC en Florida?", a: "Comparta el nombre del negocio, la dirección y quiénes participan. Preparamos los artículos y los presentamos ante el estado de Florida." },
        { q: "¿Qué cubre el cargo de $89?", a: "Es nuestro cargo por preparar y presentar la LLC en Florida. La tasa del estado es $125 y va en su propia línea." },
        { q: "¿Qué pasa si Florida rechaza la presentación?", a: refund.es },
      ],
    },
    pt: {
      title: "Formar uma LLC na Flórida | Diler Services",
      description: "Forme uma LLC na Flórida com uma casa local em Lake Wales. Nossa taxa é $89. A taxa da Flórida é $125. Pagamento só em modo de teste.",
      kicker: "LLC na Flórida",
      h1: "Forme uma LLC na Flórida.",
      lede: "Você nos conta do negócio. Nós preparamos os papéis e protocolamos no estado da Flórida.",
      price: "Nossa taxa é $89. A taxa do estado da Flórida é $125.",
      how: "Como o registro anda",
      faqTitle: "Perguntas sobre uma LLC na Flórida",
      steps: [
        { h: "Conte do negócio", p: "Nome, endereço e quem participa. Pouca informação já basta para começar." },
        { h: "Preparamos e protocolamos", p: "Revisamos cada detalhe e protocolamos o contrato na Flórida." },
        { h: "Você recebe o registro", p: "Dá para acompanhar Protocolado, Aprovado e os documentos que voltam." },
      ],
      faqs: [
        { q: "Como eu formo uma LLC na Flórida?", a: "Passe o nome do negócio, o endereço e quem participa. Preparamos os documentos e protocolamos no estado da Flórida." },
        { q: "O que a taxa de $89 cobre?", a: "É a nossa taxa para preparar e protocolar a LLC na Flórida. A taxa do estado é $125, em uma linha própria." },
        { q: "E se a Flórida recusar o registro?", a: refund.pt },
      ],
    },
  },
  {
    file: "services/corporation.html",
    product: "corp",
    en: {
      title: "Form a Florida Corporation | Diler Services",
      description: "Form a Florida corporation when you plan to bring on investors or issue stock. Our fee is $89. Florida's state fee is $70.",
      kicker: "Florida corporation",
      h1: "Form a Florida corporation.",
      lede: "Planning to bring on investors or issue stock? We form the corporation and file it with Florida, with the same care we give every LLC.",
      price: "Our fee is $89. Florida's state fee is $70.",
      how: "How the filing goes",
      faqTitle: "Questions on a Florida corporation",
      steps: [
        { h: "Tell us the plan", p: "Company name, address, and who will hold the stock." },
        { h: "We file with Florida", p: "We review the details and file the corporation with the state." },
        { h: "You get the record", p: "The approved documents come back to one place." },
      ],
      faqs: [
        { q: "When is a Florida corporation the right fit?", a: "When you expect investors or want to issue stock. We file it with the same care we give a Florida LLC." },
        { q: "What are the fees?", a: "Our fee is $89. Florida charges a $70 state fee." },
        { q: "What if Florida rejects the filing?", a: refund.en },
      ],
    },
    es: {
      title: "Formar una corporación en Florida | Diler Services",
      description: "Forme una corporación en Florida si va a recibir inversionistas o emitir acciones. Nuestro cargo es $89. La tasa de Florida es $70.",
      kicker: "Corporación en Florida",
      h1: "Forme una corporación en Florida.",
      lede: "¿Piensa recibir inversionistas o emitir acciones? Formamos la corporación y la presentamos en Florida, con el mismo cuidado que damos a cada LLC.",
      price: "Nuestro cargo es $89. La tasa del estado de Florida es $70.",
      how: "Cómo sigue el trámite",
      faqTitle: "Preguntas sobre una corporación en Florida",
      steps: [
        { h: "Cuéntenos el plan", p: "Nombre, dirección y quién tendrá las acciones." },
        { h: "Presentamos en Florida", p: "Revisamos los datos y presentamos la corporación ante el estado." },
        { h: "Usted recibe el registro", p: "Los documentos aprobados vuelven a un solo lugar." },
      ],
      faqs: [
        { q: "¿Cuándo conviene una corporación en Florida?", a: "Cuando espera inversionistas o quiere emitir acciones. La presentamos con el mismo cuidado que una LLC." },
        { q: "¿Cuáles son los cargos?", a: "Nuestro cargo es $89. Florida cobra una tasa estatal de $70." },
        { q: "¿Qué pasa si Florida rechaza la presentación?", a: refund.es },
      ],
    },
    pt: {
      title: "Formar uma corporação na Flórida | Diler Services",
      description: "Forme uma corporação na Flórida para receber investidores ou emitir ações. Nossa taxa é $89. A taxa da Flórida é $70.",
      kicker: "Corporação na Flórida",
      h1: "Forme uma corporação na Flórida.",
      lede: "Vai receber investidores ou emitir ações? Formamos a corporação e protocolamos na Flórida, com o mesmo cuidado de cada LLC.",
      price: "Nossa taxa é $89. A taxa do estado da Flórida é $70.",
      how: "Como o registro anda",
      faqTitle: "Perguntas sobre uma corporação na Flórida",
      steps: [
        { h: "Conte o plano", p: "Nome, endereço e quem vai deter as ações." },
        { h: "Protocolamos na Flórida", p: "Revisamos os dados e protocolamos a corporação no estado." },
        { h: "Você recebe o registro", p: "Os documentos aprovados voltam para um só lugar." },
      ],
      faqs: [
        { q: "Quando uma corporação na Flórida faz sentido?", a: "Quando você espera investidores ou quer emitir ações. Protocolamos com o mesmo cuidado de uma LLC." },
        { q: "Quais são as taxas?", a: "Nossa taxa é $89. A Flórida cobra uma taxa estadual de $70." },
        { q: "E se a Flórida recusar o registro?", a: refund.pt },
      ],
    },
  },
  agent, ein, annual, agreement, bundle,
];

function finishService(item) {
  return {
    file: item.file,
    nav: "services",
    checkout: true,
    en: wrapService(item.en, item.product, item.en.options),
    es: wrapService(item.es, item.product, item.es.options),
    pt: wrapService(item.pt, item.product, item.pt.options),
  };
}

function wrapService(copy, product, options) {
  return {
    title: copy.title,
    description: copy.description,
    faqs: copy.faqs,
    main(langRoot, t, lang) {
      return serviceMain({ ...copy, product, options }, lang, t, langRoot);
    },
  };
}

function serviceMain(copy, lang, t, root) {
  return `<section class="section section-warm page-hero">
    <div class="wrap">
      <p class="crumb"><a href="${root}services/index.html">${esc(t.services)}</a></p>
      <p class="kicker">${esc(copy.kicker)}</p>
      <h1>${esc(copy.h1)}</h1>
      <p class="lede">${esc(copy.lede)}</p>
      <p class="fee">${esc(copy.price)}</p>
      <div class="actions"><a class="btn btn-gold" href="#checkout">${esc(t.checkout)}</a></div>
    </div>
  </section>
  <section class="section section-light tight">
    <div class="wrap">
      <h2>${esc(copy.how)}</h2>
      ${steps(copy.steps)}
    </div>
  </section>
  ${pay(lang, t, copy.product, copy.options)}
  <section class="section section-light tight">
    <div class="wrap">
      <h2>${esc(copy.faqTitle)}</h2>
      ${faq(copy.faqs)}
    </div>
  </section>`;
}

function rates(langRoot, items) {
  return `<div class="rate-list">${items.map(([href, h, p, fee]) => `<a class="rate" href="${langRoot}${href}"><span><strong>${esc(h)}</strong><small>${esc(p)}</small></span><em>${esc(fee)}</em></a>`).join("")}</div>`;
}

function legal(copy) {
  return `<section class="section section-warm page-hero"><div class="wrap prose">
    <p class="draft">${esc(copy.draft)}</p>
    <h1>${esc(copy.h1)}</h1>
    <p class="lede">${esc(copy.lede)}</p>
    ${copy.blocks.map((block) => `<h2>${esc(block.h)}</h2>${block.p.map((p) => `<p>${esc(p)}</p>`).join("")}`).join("")}
  </div></section>`;
}

function simple(file, nav, fields, noindex = false) {
  const out = { file, nav, checkout: false, noindex };
  for (const lang of ["en", "es", "pt"]) {
    out[lang] = {
      title: fields[lang].title,
      description: fields[lang].description,
      faqs: fields[lang].faqs || null,
      main: fields[lang].main,
    };
  }
  return out;
}

const draft = {
  en: "Draft for attorney review. Diler Services is not a law firm and does not provide legal advice.",
  es: "Borrador para revisión de un abogado. Diler Services no es un bufete y no da asesoría legal.",
  pt: "Rascunho para revisão de um advogado. A Diler Services não é um escritório de advocacia e não oferece aconselhamento jurídico.",
};

export const pages = [
  ...services.map(finishService),
  simple("services/index.html", "services", {
    en: {
      title: "Florida LLC Services | Diler Services",
      description: "Form a Florida LLC, keep a Florida registered agent, request an EIN, file the Florida annual report, or put an operating agreement in place.",
      main: (root) => `<section class="section section-warm page-hero"><div class="wrap"><h1>Everything your business needs to get started.</h1><p class="lede">Form a Florida LLC, keep a registered agent, request an EIN for your LLC, file the Florida annual report, or put a Florida LLC operating agreement in place.</p></div></section>
      <section class="section section-light tight"><div class="wrap"><div class="solve-grid">
        ${[
          ["llc.html", "Florida LLC", "Form a Florida LLC without the guesswork.", "$89 + $125 state fee"],
          ["corporation.html", "Florida corporation", "For investors or stock, filed with the same care.", "$89 + $70 state fee"],
          ["registered-agent.html", "Florida registered agent", "Official mail at our Florida address, not your home.", "$13.99/mo or $169/yr"],
          ["ein.html", "EIN for LLC", "We request your EIN for you, so you can open a bank account and file taxes.", "$95"],
          ["annual-report.html", "Florida annual report", "A reminder, then the filing, between January 1 and May 1.", "$99 + $138.75 state fee"],
          ["operating-agreement.html", "Florida LLC operating agreement", "Custom, for a company with more than one member.", "$149"],
          ["bundle.html", "Bundle", "Florida LLC, EIN, and the operating agreement.", "$299 + $125 state fee"],
        ].map(([href, h, p, fee]) => `<a class="card" href="${root}services/${href}"><h3>${esc(h)}</h3><p>${esc(p)}</p><span class="fee">${esc(fee)}</span></a>`).join("")}
      </div></div></section>`,
    },
    es: {
      title: "Servicios de LLC en Florida | Diler Services",
      description: "Forme una LLC en Florida, tenga un agente registrado, solicite el EIN, presente el informe anual o deje listo el acuerdo operativo.",
      main: (root) => `<section class="section section-warm page-hero"><div class="wrap"><h1>Todo lo que su negocio necesita para empezar.</h1><p class="lede">Forme una LLC en Florida, tenga un agente registrado, solicite el EIN, presente el informe anual o deje listo un acuerdo operativo.</p></div></section>
      <section class="section section-light tight"><div class="wrap"><div class="solve-grid">
        ${[
          ["llc.html", "LLC en Florida", "Forme una LLC en Florida sin adivinar el trámite.", "$89 + $125 del estado"],
          ["corporation.html", "Corporación en Florida", "Para inversionistas o acciones, con el mismo cuidado.", "$89 + $70 del estado"],
          ["registered-agent.html", "Agente registrado en Florida", "Correo oficial en nuestra dirección, no en su casa.", "$13.99/mes o $169/año"],
          ["ein.html", "EIN para LLC", "Solicitamos su EIN para que abra un banco y declare impuestos.", "$95"],
          ["annual-report.html", "Informe anual de Florida", "Un aviso y luego la presentación, del 1 de enero al 1 de mayo.", "$99 + $138.75 del estado"],
          ["operating-agreement.html", "Acuerdo operativo de LLC", "A la medida, para más de un miembro.", "$149"],
          ["bundle.html", "Paquete", "LLC en Florida, EIN y el acuerdo operativo.", "$299 + $125 del estado"],
        ].map(([href, h, p, fee]) => `<a class="card" href="${root}services/${href}"><h3>${esc(h)}</h3><p>${esc(p)}</p><span class="fee">${esc(fee)}</span></a>`).join("")}
      </div></div></section>`,
    },
    pt: {
      title: "Serviços de LLC na Flórida | Diler Services",
      description: "Forme uma LLC na Flórida, tenha um agente registrado, peça o EIN, protocole o relatório anual ou deixe pronto o contrato social.",
      main: (root) => `<section class="section section-warm page-hero"><div class="wrap"><h1>Tudo o que o seu negócio precisa para começar.</h1><p class="lede">Forme uma LLC na Flórida, tenha um agente registrado, peça o EIN, protocole o relatório anual ou deixe pronto um contrato social.</p></div></section>
      <section class="section section-light tight"><div class="wrap"><div class="solve-grid">
        ${[
          ["llc.html", "LLC na Flórida", "Forme uma LLC na Flórida sem adivinhar o caminho.", "$89 + $125 do estado"],
          ["corporation.html", "Corporação na Flórida", "Para investidores ou ações, com o mesmo cuidado.", "$89 + $70 do estado"],
          ["registered-agent.html", "Agente registrado na Flórida", "Correspondência oficial no nosso endereço, não na sua casa.", "$13.99/mês ou $169/ano"],
          ["ein.html", "EIN para LLC", "Pedimos o seu EIN para você abrir um banco e declarar impostos.", "$95"],
          ["annual-report.html", "Relatório anual da Flórida", "Um aviso e o protocolo, de 1º de janeiro a 1º de maio.", "$99 + $138.75 do estado"],
          ["operating-agreement.html", "Contrato social de LLC", "Sob medida, para mais de um sócio.", "$149"],
          ["bundle.html", "Pacote", "LLC na Flórida, EIN e o contrato social.", "$299 + $125 do estado"],
        ].map(([href, h, p, fee]) => `<a class="card" href="${root}services/${href}"><h3>${esc(h)}</h3><p>${esc(p)}</p><span class="fee">${esc(fee)}</span></a>`).join("")}
      </div></div></section>`,
    },
  }),
  simple("pricing.html", "pricing", {
    en: {
      title: "Florida LLC Pricing | Diler Services",
      description: "Quiet fees for a Florida LLC, corporation, registered agent, EIN, annual report, and operating agreement. State fees are listed beside ours.",
      main: (root) => `<section class="section section-warm page-hero"><div class="wrap"><h1>Clear fees.</h1><p class="lede">Our fee is listed here. Florida's state fee sits beside it when the state charges one. A 3.5% card processing fee is added at checkout, on its own line.</p></div></section>
      <section class="section section-light tight"><div class="wrap"><h2>A package</h2>${rates(root, [["services/bundle.html", "Bundle", "Florida LLC, EIN, and a custom operating agreement.", "$299 + $125 state fee"]])}<h2 class="stack-title">A la carte</h2>${rates(root, [
        ["services/llc.html", "Florida LLC", "Form a Florida LLC.", "$89 + $125"],
        ["services/corporation.html", "Florida corporation", "File a Florida corporation.", "$89 + $70"],
        ["services/registered-agent.html", "Florida registered agent", "A month, or a year.", "$13.99 or $169"],
        ["services/ein.html", "EIN for LLC", "We request the EIN for you.", "$95"],
        ["services/annual-report.html", "Florida annual report", "Reminder and filing for an LLC.", "$99 + $138.75"],
        ["services/operating-agreement.html", "Florida LLC operating agreement", "Custom, multi-member.", "$149"],
      ])}</div></section>`,
    },
    es: {
      title: "Precios de LLC en Florida | Diler Services",
      description: "Cargos claros para una LLC en Florida, corporación, agente registrado, EIN, informe anual y acuerdo operativo.",
      main: (root) => `<section class="section section-warm page-hero"><div class="wrap"><h1>Cargos claros.</h1><p class="lede">Nuestro cargo está en la lista. La tasa de Florida va al lado cuando el estado cobra una. El 3.5% de la tarjeta se suma en el pago, en su propia línea.</p></div></section>
      <section class="section section-light tight"><div class="wrap"><h2>Un paquete</h2>${rates(root, [["services/bundle.html", "Paquete", "LLC en Florida, EIN y un acuerdo operativo a la medida.", "$299 + $125 del estado"]])}<h2 class="stack-title">Por separado</h2>${rates(root, [
        ["services/llc.html", "LLC en Florida", "Forme una LLC en Florida.", "$89 + $125"],
        ["services/corporation.html", "Corporación en Florida", "Presente una corporación en Florida.", "$89 + $70"],
        ["services/registered-agent.html", "Agente registrado en Florida", "Un mes, o un año.", "$13.99 o $169"],
        ["services/ein.html", "EIN para LLC", "Solicitamos el EIN por usted.", "$95"],
        ["services/annual-report.html", "Informe anual de Florida", "Aviso y presentación para una LLC.", "$99 + $138.75"],
        ["services/operating-agreement.html", "Acuerdo operativo de LLC", "A la medida, varios miembros.", "$149"],
      ])}</div></section>`,
    },
    pt: {
      title: "Preços de LLC na Flórida | Diler Services",
      description: "Taxas claras para uma LLC na Flórida, corporação, agente registrado, EIN, relatório anual e contrato social.",
      main: (root) => `<section class="section section-warm page-hero"><div class="wrap"><h1>Taxas claras.</h1><p class="lede">Nossa taxa está na lista. A taxa da Flórida fica ao lado quando o estado cobra uma. Os 3,5% do cartão entram no pagamento, numa linha própria.</p></div></section>
      <section class="section section-light tight"><div class="wrap"><h2>Um pacote</h2>${rates(root, [["services/bundle.html", "Pacote", "LLC na Flórida, EIN e um contrato social sob medida.", "$299 + $125 do estado"]])}<h2 class="stack-title">Avulso</h2>${rates(root, [
        ["services/llc.html", "LLC na Flórida", "Forme uma LLC na Flórida.", "$89 + $125"],
        ["services/corporation.html", "Corporação na Flórida", "Protocole uma corporação na Flórida.", "$89 + $70"],
        ["services/registered-agent.html", "Agente registrado na Flórida", "Um mês, ou um ano.", "$13.99 ou $169"],
        ["services/ein.html", "EIN para LLC", "Pedimos o EIN para você.", "$95"],
        ["services/annual-report.html", "Relatório anual da Flórida", "Aviso e protocolo para uma LLC.", "$99 + $138.75"],
        ["services/operating-agreement.html", "Contrato social de LLC", "Sob medida, vários sócios.", "$149"],
      ])}</div></section>`,
    },
  }),
  aboutPage(),
  contactPage(),
  thanksPage(),
  returnPage(),
  privacyPage(),
  termsPage(),
  refundPage(),
];

function aboutPage() {
  const body = {
    en: {
      title: "About Diler Services | Lake Wales, FL",
      description: "A local Lake Wales shop that forms Florida companies, keeps the record, and answers in English, Spanish, and Portuguese.",
      h1: "A local shop in Lake Wales.",
      lede: "We help you form a Florida company and keep the record straight after that. You talk to real people.",
      how: "How we work",
      howLede: "You share the company. We prepare the Florida filing. The documents, the dates, and the mail stay where you can see them.",
      steps: [
        { h: "Tell us about your business", p: "Your business name, your address, and who's involved." },
        { h: "We check and file", p: "We review every detail. Then we file with the State of Florida. If something needs fixing, we fix it." },
        { h: "You're in business", p: "You get your approved documents. Then we help you stay in good standing, year after year." },
      ],
      trust: "Why you can trust the filing",
      fastH: "Filed when you are ready",
      langsH: "English, Spanish, and Portuguese",
      langsP: "Real people answer in your language.",
      faqs: [
        { q: "What if the state rejects the filing?", a: "If the state rejects your filing and we can't fix it, we refund our fee." },
        { q: "How soon is the filing sent?", a: "We file promptly once your details are complete. We don't name a day or a week. Florida sets the pace after that." },
        { q: "Is Diler Services a law firm?", a: "No. Diler Services is not a law firm and does not provide legal advice." },
      ],
    },
    es: {
      title: "Sobre Diler Services | Lake Wales, FL",
      description: "Un taller local en Lake Wales que forma empresas en Florida, guarda el registro y responde en inglés, español y portugués.",
      h1: "Un taller local en Lake Wales.",
      lede: "Le ayudamos a formar una empresa en Florida y a dejar el registro en orden después. Habla con personas de verdad.",
      how: "Cómo trabajamos",
      howLede: "Usted comparte la empresa. Nosotros preparamos la presentación en Florida. Los documentos, las fechas y el correo quedan a la vista.",
      steps: [
        { h: "Cuéntenos de su negocio", p: "El nombre, la dirección y quiénes participan." },
        { h: "Revisamos y presentamos", p: "Revisamos cada dato. Luego presentamos ante el estado de Florida. Si algo hay que corregir, lo corregimos." },
        { h: "Ya está en el negocio", p: "Recibe los documentos aprobados. Después le ayudamos a seguir al día, año tras año." },
      ],
      trust: "Por qué puede confiar en el trámite",
      fastH: "Se presenta cuando usted está listo",
      langsH: "Inglés, español y portugués",
      langsP: "Personas de verdad responden en su idioma.",
      faqs: [
        { q: "¿Qué pasa si el estado rechaza la presentación?", a: "Si el estado rechaza su presentación y no podemos corregirla, le devolvemos nuestro cargo." },
        { q: "¿Cuándo se envía?", a: "Presentamos en cuanto sus datos están completos. No prometemos un día ni una semana. Florida marca el ritmo después." },
        { q: "¿Diler Services es un bufete?", a: "No. Diler Services no es un bufete de abogados y no da asesoría legal." },
      ],
    },
    pt: {
      title: "Sobre a Diler Services | Lake Wales, FL",
      description: "Uma casa local em Lake Wales que forma empresas na Flórida, guarda o registro e responde em inglês, espanhol e português.",
      h1: "Uma casa local em Lake Wales.",
      lede: "Ajudamos você a formar uma empresa na Flórida e a deixar o registro em ordem depois. Você fala com pessoas de verdade.",
      how: "Como trabalhamos",
      howLede: "Você conta da empresa. Nós preparamos o protocolo na Flórida. Os documentos, as datas e a correspondência ficam à vista.",
      steps: [
        { h: "Conte do seu negócio", p: "O nome, o endereço e quem participa." },
        { h: "Revisamos e protocolamos", p: "Revisamos cada detalhe. Depois protocolamos no estado da Flórida. Se algo precisa de ajuste, a gente ajusta." },
        { h: "Você está no negócio", p: "Recebe os documentos aprovados. Depois ajudamos a manter tudo em dia, ano após ano." },
      ],
      trust: "Por que confiar no registro",
      fastH: "Protocolado quando você está pronto",
      langsH: "Inglês, espanhol e português",
      langsP: "Pessoas de verdade respondem no seu idioma.",
      faqs: [
        { q: "E se o estado recusar o registro?", a: "Se o estado recusar o seu registro e não pudermos corrigir, devolvemos a nossa taxa." },
        { q: "Quando o registro é enviado?", a: "Protocolamos assim que seus dados estão completos. Não prometemos um dia nem uma semana. A Flórida define o ritmo depois disso." },
        { q: "A Diler Services é um escritório de advocacia?", a: "Não. A Diler Services não é um escritório de advocacia e não oferece aconselhamento jurídico." },
      ],
    },
  };
  return simple("about.html", "about", Object.fromEntries(Object.entries(body).map(([lang, copy]) => [lang, {
    title: copy.title,
    description: copy.description,
    faqs: copy.faqs,
    main: (root, t, lang) => `<section class="section section-warm page-hero"><div class="wrap"><p class="kicker">Lake Wales, FL</p><h1>${esc(copy.h1)}</h1><p class="lede">${esc(copy.lede)}</p></div></section>
      <section class="section section-light tight"><div class="wrap"><h2>${esc(copy.how)}</h2><p class="lede">${esc(copy.howLede)}</p>${steps(copy.steps)}</div></section>
      <section class="section section-warm tight"><div class="wrap"><h2>${esc(copy.trust)}</h2><p class="guarantee">${esc(copy.faqs[0].a)}</p><div class="trust-grid"><article><h3>${esc(copy.fastH)}</h3><p>${esc(copy.faqs[1].a)}</p></article><article><h3>${esc(copy.langsH)}</h3><p>${esc(copy.langsP)}</p></article></div></div></section>
      <section class="section section-light tight"><div class="wrap"><h2>${esc({ en: "Questions", es: "Preguntas", pt: "Perguntas" }[lang])}</h2>${faq(copy.faqs)}</div></section>`,
  }])));
}

function contactPage() {
  const topics = {
    en: ["Florida LLC", "Florida corporation", "Florida registered agent", "EIN for LLC", "Florida annual report", "Florida LLC operating agreement", "Bundle", "Something else"],
    es: ["LLC en Florida", "Corporación en Florida", "Agente registrado en Florida", "EIN para LLC", "Informe anual de Florida", "Acuerdo operativo", "Paquete", "Otra cosa"],
    pt: ["LLC na Flórida", "Corporação na Flórida", "Agente registrado na Flórida", "EIN para LLC", "Relatório anual da Flórida", "Contrato social", "Pacote", "Outra coisa"],
  };
  const copy = {
    en: { title: "Contact Diler Services | Lake Wales, FL", description: "Write to info@dilerservices.com or book a call. A short note is enough.", h1: "Write to us.", lede: "Tell us what you need. We read every note at info@dilerservices.com.", note: "Prefer to talk it through? Use Book a call when the calendar is connected, or send the note and we will find a time." },
    es: { title: "Contacto | Diler Services", description: "Escriba a info@dilerservices.com o agende una llamada. Con una nota breve basta.", h1: "Escríbanos.", lede: "Cuéntenos qué necesita. Leemos cada nota en info@dilerservices.com.", note: "¿Prefiere hablarlo? Use Agendar una llamada cuando el calendario esté conectado, o envíe la nota y buscamos un momento." },
    pt: { title: "Contato | Diler Services", description: "Escreva para info@dilerservices.com ou marque uma ligação. Um recado curto já basta.", h1: "Escreva para nós.", lede: "Conte o que você precisa. Lemos cada recado em info@dilerservices.com.", note: "Prefere conversar? Use Marcar uma ligação quando o calendário estiver ligado, ou envie o recado e achamos um horário." },
  };
  return simple("contact.html", "contact", Object.fromEntries(["en", "es", "pt"].map((lang) => [lang, {
    ...copy[lang],
    main: (root, t) => `<section class="section section-warm page-hero"><div class="wrap"><h1>${esc(copy[lang].h1)}</h1><p class="lede">${esc(copy[lang].lede)}</p>
      <form class="form" name="contact" method="POST" action="thanks.html" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="contact">
        <input type="hidden" name="language" value="${lang}">
        <p class="hp"><label>Leave blank <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <label class="field"><span>${esc(t.name)}</span><input name="name" required autocomplete="name"></label>
        <label class="field"><span>${esc(t.email)}</span><input type="email" name="email" required autocomplete="email"></label>
        <label class="field"><span>${esc(t.topic)}</span><select name="topic">${topics[lang].map((item) => `<option>${esc(item)}</option>`).join("")}</select></label>
        <label class="field"><span>${esc(t.message)}</span><textarea name="message" required></textarea></label>
        <div class="actions"><button class="btn btn-gold" type="submit">${esc(t.send)}</button><a class="btn btn-line" id="book" href="#book" data-book-call>${esc(t.book)}</a></div>
      </form>
      <p class="quiet">${esc(copy[lang].note)}</p>
    </div></section>`,
  }])));
}

function thanksPage() {
  const copy = {
    en: { title: "Message received | Diler Services", description: "We have your note and will reply at the email you gave us.", h1: "We have your note.", lede: "We will reply from info@dilerservices.com." },
    es: { title: "Mensaje recibido | Diler Services", description: "Tenemos su nota y responderemos al correo que nos dejó.", h1: "Tenemos su nota.", lede: "Responderemos desde info@dilerservices.com." },
    pt: { title: "Recado recebido | Diler Services", description: "Recebemos seu recado e vamos responder no e-mail que você deixou.", h1: "Recebemos seu recado.", lede: "Vamos responder de info@dilerservices.com." },
  };
  return simple("thanks.html", "contact", Object.fromEntries(["en", "es", "pt"].map((lang) => [lang, {
    ...copy[lang],
    main: () => `<section class="section section-warm page-hero"><div class="wrap"><h1>${esc(copy[lang].h1)}</h1><p class="lede">${esc(copy[lang].lede)}</p></div></section>`,
  }])), true);
}

function returnPage() {
  const copy = {
    en: { title: "Checkout return | Diler Services", description: "Test checkout return. No live charge was made from this page.", h1: "You're back.", lede: "If this was a test payment, Stripe has the receipt. No live charge is set up on this site." },
    es: { title: "Regreso del pago | Diler Services", description: "Regreso del pago de prueba. Esta página no hace un cobro real.", h1: "Ya volvió.", lede: "Si fue un pago de prueba, Stripe tiene el recibo. En este sitio no hay un cobro real." },
    pt: { title: "Retorno do pagamento | Diler Services", description: "Retorno do pagamento de teste. Esta página não faz uma cobrança real.", h1: "Você voltou.", lede: "Se foi um pagamento de teste, a Stripe tem o recibo. Neste site não há cobrança real." },
  };
  return simple("checkout/return.html", "services", Object.fromEntries(["en", "es", "pt"].map((lang) => [lang, {
    ...copy[lang],
    main: (root) => `<section class="section section-warm page-hero"><div class="wrap"><h1>${esc(copy[lang].h1)}</h1><p class="lede">${esc(copy[lang].lede)}</p><div class="actions"><a class="btn btn-gold" href="${root}services/llc.html">${esc(ui[lang].start)}</a></div></div></section>`,
  }])), true);
}

function policy(file, nav, blocks) {
  return simple(file, nav, Object.fromEntries(["en", "es", "pt"].map((lang) => [lang, {
    title: blocks[lang].title,
    description: blocks[lang].description,
    main: () => legal(blocks[lang]),
  }])));
}

function privacyPage() {
  return policy("privacy.html", "", {
    en: { title: "Privacy Draft | Diler Services", description: "Draft privacy notice for attorney review. Diler Services is not a law firm.", draft: draft.en, h1: "Privacy", lede: "This page is a draft. An attorney still needs to review it before it is final.", blocks: [
      { h: "What you send us", p: ["The contact form asks for your name, email, and a message. Checkout details are handled by Stripe in test mode until a live account is connected.", "We use that information to answer you and to prepare the Florida filing you asked for."] },
      { h: "What we don't do", p: ["We don't sell your information. We don't ask for a phone number on this site."] },
      { h: "Where we are", p: ["Diler Services, Lake Wales, FL. Questions go to info@dilerservices.com."] },
    ] },
    es: { title: "Borrador de privacidad | Diler Services", description: "Borrador de privacidad para revisión de un abogado. Diler Services no es un bufete.", draft: draft.es, h1: "Privacidad", lede: "Esta página es un borrador. Un abogado todavía debe revisarla antes de que sea final.", blocks: [
      { h: "Lo que nos envía", p: ["El formulario pide su nombre, correo y un mensaje. Los datos del pago los maneja Stripe en modo de prueba hasta que se conecte una cuenta real.", "Usamos esa información para responderle y para preparar el trámite de Florida que pidió."] },
      { h: "Lo que no hacemos", p: ["No vendemos su información. En este sitio no pedimos un número de teléfono."] },
      { h: "Dónde estamos", p: ["Diler Services, Lake Wales, FL. Las preguntas van a info@dilerservices.com."] },
    ] },
    pt: { title: "Rascunho de privacidade | Diler Services", description: "Rascunho de privacidade para revisão de um advogado. A Diler Services não é um escritório de advocacia.", draft: draft.pt, h1: "Privacidade", lede: "Esta página é um rascunho. Um advogado ainda precisa revisá-la antes de ficar final.", blocks: [
      { h: "O que você nos envia", p: ["O formulário pede seu nome, e-mail e uma mensagem. Os dados do pagamento ficam com a Stripe em modo de teste até uma conta real ser ligada.", "Usamos essa informação para responder e para preparar o registro da Flórida que você pediu."] },
      { h: "O que não fazemos", p: ["Não vendemos suas informações. Neste site não pedimos telefone."] },
      { h: "Onde estamos", p: ["Diler Services, Lake Wales, FL. As perguntas vão para info@dilerservices.com."] },
    ] },
  });
}

function termsPage() {
  return policy("terms.html", "", {
    en: { title: "Terms Draft | Diler Services", description: "Draft terms for attorney review. Diler Services is not a law firm and does not give legal advice.", draft: draft.en, h1: "Terms", lede: "This page is a draft. An attorney still needs to review it before it is final.", blocks: [
      { h: "Not a law firm", p: ["Diler Services is not a law firm and does not provide legal advice. We prepare and file Florida paperwork from the details you give us."] },
      { h: "Your details", p: ["You confirm that the name, address, and ownership you send are accurate. We file from what you provide."] },
      { h: "Fees", p: ["Our fee and Florida's state fee are listed separately. A 3.5% card processing fee is added at checkout on its own line. Checkout on this site is test mode only until live keys are added."] },
    ] },
    es: { title: "Borrador de términos | Diler Services", description: "Borrador de términos para revisión de un abogado. Diler Services no es un bufete.", draft: draft.es, h1: "Términos", lede: "Esta página es un borrador. Un abogado todavía debe revisarla antes de que sea final.", blocks: [
      { h: "No somos un bufete", p: ["Diler Services no es un bufete de abogados y no da asesoría legal. Preparamos y presentamos papeles de Florida con los datos que usted nos da."] },
      { h: "Sus datos", p: ["Usted confirma que el nombre, la dirección y los dueños que envía son correctos. Presentamos a partir de lo que usted entrega."] },
      { h: "Cargos", p: ["Nuestro cargo y la tasa de Florida van por separado. El 3.5% de la tarjeta se suma en el pago, en su propia línea. El pago de este sitio está solo en modo de prueba."] },
    ] },
    pt: { title: "Rascunho de termos | Diler Services", description: "Rascunho de termos para revisão de um advogado. A Diler Services não é um escritório de advocacia.", draft: draft.pt, h1: "Termos", lede: "Esta página é um rascunho. Um advogado ainda precisa revisá-la antes de ficar final.", blocks: [
      { h: "Não somos um escritório de advocacia", p: ["A Diler Services não é um escritório de advocacia e não oferece aconselhamento jurídico. Preparamos e protocolamos papéis da Flórida com os dados que você nos passa."] },
      { h: "Seus dados", p: ["Você confirma que o nome, o endereço e os donos que envia estão certos. Protocolamos a partir do que você entrega."] },
      { h: "Taxas", p: ["Nossa taxa e a taxa da Flórida ficam separadas. Os 3,5% do cartão entram no pagamento, numa linha própria. O pagamento deste site está só em modo de teste."] },
    ] },
  });
}

function refundPage() {
  return policy("refund.html", "", {
    en: { title: "Refund Draft | Diler Services", description: "Draft refund policy for attorney review. If the state rejects your filing and we can't fix it, we refund our fee.", draft: draft.en, h1: "Refunds", lede: "If the state rejects your filing and we can't fix it, we refund our fee.", blocks: [
      { h: "Our fee", p: ["If the state rejects your filing and we can't fix it, we refund our fee. Write to info@dilerservices.com and we will look at the filing with you."] },
      { h: "Florida's fee", p: ["Florida's state fee is charged by the state. This draft does not promise a refund of that fee. An attorney should confirm the final wording."] },
      { h: "The card line", p: ["The 3.5% card processing fee is its own line at checkout. This draft leaves the treatment of that line for attorney review."] },
    ] },
    es: { title: "Borrador de reembolsos | Diler Services", description: "Borrador de reembolsos para revisión de un abogado. Si el estado rechaza su presentación y no podemos corregirla, le devolvemos nuestro cargo.", draft: draft.es, h1: "Reembolsos", lede: "Si el estado rechaza su presentación y no podemos corregirla, le devolvemos nuestro cargo.", blocks: [
      { h: "Nuestro cargo", p: ["Si el estado rechaza su presentación y no podemos corregirla, le devolvemos nuestro cargo. Escriba a info@dilerservices.com y revisamos el trámite con usted."] },
      { h: "La tasa de Florida", p: ["La tasa del estado la cobra Florida. Este borrador no promete devolver esa tasa. Un abogado debe confirmar el texto final."] },
      { h: "La línea de la tarjeta", p: ["El 3.5% de la tarjeta es una línea propia en el pago. Este borrador deja el trato de esa línea para la revisión del abogado."] },
    ] },
    pt: { title: "Rascunho de reembolso | Diler Services", description: "Rascunho de reembolso para revisão de um advogado. Se o estado recusar o seu registro e não pudermos corrigir, devolvemos a nossa taxa.", draft: draft.pt, h1: "Reembolsos", lede: "Se o estado recusar o seu registro e não pudermos corrigir, devolvemos a nossa taxa.", blocks: [
      { h: "Nossa taxa", p: ["Se o estado recusar o seu registro e não pudermos corrigir, devolvemos a nossa taxa. Escreva para info@dilerservices.com e olhamos o registro com você."] },
      { h: "A taxa da Flórida", p: ["A taxa do estado é cobrada pela Flórida. Este rascunho não promete devolver essa taxa. Um advogado deve confirmar o texto final."] },
      { h: "A linha do cartão", p: ["Os 3,5% do cartão são uma linha própria no pagamento. Este rascunho deixa o tratamento dessa linha para a revisão do advogado."] },
    ] },
  });
}
