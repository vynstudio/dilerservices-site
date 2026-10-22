/* Test mode only. Replace the publishable key and Price IDs.
   Do not put a secret key or a live key in this file.
   Stripe Price amounts must match the cents below. The card fee is 3.5% of our fee plus any Florida state fee. */

export const checkoutConfig = {
  publishableKey: "pk_test_REPLACE_ME",
  processingFeeRate: 0.035,
  products: {
    llc: {
      priceId: "price_REPLACE_llc",
      statePriceId: "price_REPLACE_llc_state",
      serviceCents: 8900,
      stateFeeCents: 12500,
    },
    corp: {
      priceId: "price_REPLACE_corp",
      statePriceId: "price_REPLACE_corp_state",
      serviceCents: 8900,
      stateFeeCents: 7000,
    },
    ra_month: {
      priceId: "price_REPLACE_ra_month",
      serviceCents: 1399,
      stateFeeCents: 0,
    },
    ra_year: {
      priceId: "price_REPLACE_ra_year",
      serviceCents: 16900,
      stateFeeCents: 0,
    },
    ein: {
      priceId: "price_REPLACE_ein",
      serviceCents: 9500,
      stateFeeCents: 0,
    },
    annual: {
      priceId: "price_REPLACE_annual",
      statePriceId: "price_REPLACE_annual_state",
      serviceCents: 9900,
      stateFeeCents: 13875,
    },
    oa: {
      priceId: "price_REPLACE_oa",
      serviceCents: 14900,
      stateFeeCents: 0,
    },
    bundle: {
      priceId: "price_REPLACE_bundle",
      statePriceId: "price_REPLACE_bundle_state",
      serviceCents: 29900,
      stateFeeCents: 12500,
    },
  },
};

export function quote(id) {
  const product = checkoutConfig.products[id];
  if (!product) return null;
  const subtotal = product.serviceCents + (product.stateFeeCents || 0);
  const feeCents = Math.round(subtotal * checkoutConfig.processingFeeRate);
  return { ...product, subtotal, feeCents, totalCents: subtotal + feeCents };
}

export function checkoutReady(id) {
  const product = checkoutConfig.products[id];
  if (!product) return false;
  const key = checkoutConfig.publishableKey;
  const ids = [product.priceId, product.statePriceId].filter(Boolean);
  if (!key.startsWith("pk_test_") || key.includes("REPLACE")) return false;
  return ids.every((priceId) => priceId.startsWith("price_") && !priceId.includes("REPLACE"));
}
