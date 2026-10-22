import { checkoutConfig, quote, checkoutReady } from "../../checkout-config.mjs";

const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });

function lines(copy, priced) {
  const rows = [`<div class="pay-line"><span>${copy.ourFee}</span><span>${money.format(priced.serviceCents / 100)}</span></div>`];
  if (priced.stateFeeCents) {
    rows.push(`<div class="pay-line"><span>${copy.stateFee}</span><span>${money.format(priced.stateFeeCents / 100)}</span></div>`);
  }
  rows.push(`<div class="pay-line"><span>${copy.cardFee}</span><span>${money.format(priced.feeCents / 100)}</span></div>`);
  return rows.join("");
}

function placeholder(copy, priced) {
  return `<div class="pay-box">${lines(copy, priced)}<p class="quiet">${copy.pending}</p></div>`;
}

async function mount(slot, productId, copy, returnUrl) {
  const priced = quote(productId);
  if (!priced) return;
  if (!checkoutReady(productId)) {
    slot.innerHTML = placeholder(copy, priced);
    return;
  }
  slot.innerHTML = `<div class="pay-box">${lines(copy, priced)}<div class="checkout-slot"></div></div>`;
  const response = await fetch("/api/checkout", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ product: productId, returnUrl }),
  });
  if (!response.ok) {
    slot.querySelector(".checkout-slot").innerHTML = `<p class="quiet">${copy.pending}</p>`;
    return;
  }
  const { clientSecret } = await response.json();
  if (!window.Stripe) {
    await new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://js.stripe.com/v3/";
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }
  const stripe = window.Stripe(checkoutConfig.publishableKey);
  const checkout = await stripe.initEmbeddedCheckout({ clientSecret });
  checkout.mount(slot.querySelector(".checkout-slot"));
}

const root = document.querySelector("[data-checkout]");
if (root) {
  const copy = {
    ourFee: root.getAttribute("data-our-fee"),
    stateFee: root.getAttribute("data-state-fee"),
    cardFee: root.getAttribute("data-card-fee"),
    pending: root.getAttribute("data-pending"),
  };
  const returnUrl = `${location.origin}${root.getAttribute("data-return-path")}?session_id={CHECKOUT_SESSION_ID}`;
  const slots = [...root.querySelectorAll("[data-product]")];
  const picks = [...root.querySelectorAll("[data-pick]")];

  function show(id) {
    slots.forEach((slot) => {
      const on = slot.getAttribute("data-product") === id;
      slot.hidden = !on;
      if (on && !slot.dataset.ready) {
        slot.dataset.ready = "1";
        mount(slot, id, copy, returnUrl).catch(() => {
          slot.innerHTML = placeholder(copy, quote(id));
        });
      }
    });
    picks.forEach((button) => {
      button.setAttribute("aria-pressed", button.getAttribute("data-pick") === id ? "true" : "false");
    });
  }

  picks.forEach((button) => {
    button.addEventListener("click", () => show(button.getAttribute("data-pick")));
  });
  show(root.getAttribute("data-checkout"));
}
