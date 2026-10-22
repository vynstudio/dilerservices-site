/*
  Diler Services payment links. This is the ONLY file to edit to turn on online card payment.

  Paste a Stripe Payment Link or Checkout URL between the quotes for each product.
  Leave a value empty ("") and the order is still recorded, and the client sees:
  "We'll email you a secure payment link within 1 business day."

  How the order page picks a link:
  1. If the cart matches a combination key below (items joined with "+", in this order:
     service, then EIN add-on, then registered agent), that link is used.
  2. Otherwise, if the cart has exactly one item, that item's link is used.
  3. Otherwise no link is used and the order is submitted for a payment link by email.
  Each link must charge the exact "Total due today" shown on the order page,
  including the Florida state fee where one is shown ($125 for LLC formation and the bundle).
  Products with a state fee "at cost" (annual report, DBA, amendment, reinstatement) are
  best left empty, so the state fee can be confirmed before the client is billed.
  The client's email and the order reference are appended to the link automatically
  (prefilled_email and client_reference_id), which Stripe Payment Links accept.
*/
window.DS_PAYMENT_LINKS = {
  "llc-formation": "",              // $214 = $89 fee + $125 state fee
  "formation-bundle": "",           // $299 = $174 fee + $125 state fee
  "ein-filing": "",                 // $95
  "annual-report": "",              // $99 + state fee at cost
  "annual-report-late": "",         // $149 + state fee at cost
  "dba": "",                        // $129 + state fee at cost
  "amendment": "",                  // $99 + state fee at cost
  "reinstatement": "",              // $299 + state fees at cost
  "registered-agent-monthly": "",   // $13.99 per month (subscription)
  "registered-agent-yearly": "",    // $169 per year (subscription)

  // Optional combinations (same total as the order page):
  "llc-formation+registered-agent-monthly": "",     // $227.99 today, then $13.99 per month
  "llc-formation+registered-agent-yearly": "",      // $383
  "llc-formation+ein-filing": "",                   // $309
  "llc-formation+ein-filing+registered-agent-monthly": "", // $322.99
  "llc-formation+ein-filing+registered-agent-yearly": "",  // $478
  "formation-bundle+registered-agent-monthly": "",  // $312.99
  "formation-bundle+registered-agent-yearly": ""    // $468
};
