import { checkoutConfig, quote } from "../../v5/checkout-config.mjs";

export default async (req) => {
  if (req.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Send a product id." }, 400);
  }

  const priced = quote(body.product);
  if (!priced) return json({ error: "Unknown product." }, 400);

  const returnUrl = typeof body.returnUrl === "string" ? body.returnUrl : "";
  if (!/^https?:\/\/[^/\s]+\/(?:v5\/)?(?:es\/|pt\/)?checkout\/return\.html\?session_id=\{CHECKOUT_SESSION_ID\}$/.test(returnUrl)) {
    return json({ error: "Return URL is not allowed." }, 400);
  }

  const key = typeof Netlify !== "undefined" ? Netlify.env.get("STRIPE_SECRET_KEY") || "" : "";
  if (!key.startsWith("sk_test_") || key.includes("REPLACE") || key.startsWith("sk_live_")) {
    return json({ error: "A Stripe test secret key is required." }, 503);
  }

  const ids = [priced.priceId, priced.statePriceId].filter(Boolean);
  if (ids.some((priceId) => !priceId.startsWith("price_") || priceId.includes("REPLACE"))) {
    return json({ error: "Price IDs are still placeholders." }, 503);
  }

  const params = new URLSearchParams();
  params.set("mode", "payment");
  params.set("ui_mode", "embedded");
  params.set("return_url", returnUrl);
  let index = 0;
  params.set(`line_items[${index}][price]`, priced.priceId);
  params.set(`line_items[${index}][quantity]`, "1");
  index += 1;
  if (priced.statePriceId) {
    params.set(`line_items[${index}][price]`, priced.statePriceId);
    params.set(`line_items[${index}][quantity]`, "1");
    index += 1;
  }
  params.set(`line_items[${index}][quantity]`, "1");
  params.set(`line_items[${index}][price_data][currency]`, "usd");
  params.set(`line_items[${index}][price_data][unit_amount]`, String(priced.feeCents));
  params.set(`line_items[${index}][price_data][product_data][name]`, "Card processing fee");

  const stripe = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: params,
  });
  const session = await stripe.json();
  if (!stripe.ok) {
    return json({ error: "Stripe did not open a test checkout." }, 502);
  }
  return json({ clientSecret: session.client_secret });
};

export const config = {
  path: "/api/checkout",
  method: "POST",
};

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "content-type": "application/json" },
  });
}
