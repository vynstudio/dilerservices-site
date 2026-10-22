# Template and licensed assets

The home page is original markup and CSS. It follows the section rhythm of a licensed Envato template, recolored and rewritten for Diler Services. Nothing on the public page credits these sources.

## Structural base

**Landinger** (Tailwind CSS Laravel landing page), Envato Elements, licensed to Diler Services.

- Source file in the delivery archive: `Landinger-Laravel_v1.0`
- Used for structure only: sticky navigation, split dark hero, asymmetric feature bento, numbered steps, FAQ, multi-column footer.
- Not used: Laravel, Tailwind build, stock copy, stock imagery, pricing blocks, review widgets, app-store ratings, or motion libraries.
- License: Envato Elements commercial license, licensed to Diler Services. This is not an MIT grant. The template is adapted for this project and is not redistributed as a template.

Landinger replaced an earlier MIT candidate, [shadcn-landing-page](https://github.com/leoMirandaa/shadcn-landing-page) by Leopoldo Miranda (MIT). That kit allows commercial use, but Landinger’s SaaS section system is the closer fit and is the base this page adapts.

## Layout reference only

**Toxci** (SaaS and AI startup Tailwind template), Envato Elements, licensed to Diler Services.

- Borrowed ideas: product-window frames, dense service lists, and a compact language switch.
- Recolored away from the template’s purple. No Toxci stylesheet, script, or image is shipped.
- License: Envato Elements, licensed to Diler Services.

## Icons

**Business Finance Line**, 50 SVG icons, Envato Elements, licensed to Diler Services.

- Files: `v5/assets/icons/`
- Used inline on the home page with `fill="currentColor"` so they take black, white, or gold from the section.
- A few of the supplied SVGs included an extra dollar-mark path drawn over the symbol. Those paths were removed so the icons read as the business symbols themselves.
- No icon credit on the page.

## Type

**Rafory Grotesk** (Rafory Regular), Envato Elements, commercial license, licensed to Diler Services.

- Self-hosted: `v5/assets/fonts/Rafory.woff2`
- Used for headlines and the wordmark. Evaluated against Inter at display size: the geometric forms and tighter rhythm read as a custom brand face, which is what the headlines need. It ships as a single Regular weight, so size and tracking carry the hierarchy.
- Inter (SIL Open Font License) is self-hosted for body copy and the product UI, where a neutral text face stays readable. Files: `v5/assets/fonts/inter-400.woff2`, `inter-500.woff2`, `inter-600.woff2`.

## Photographs

Licensed Envato photographs supplied for this project, in `v5/assets/img/photo-01.jpg` through `photo-10.jpg`. No photo credit on the page.

## Logo

Original geometric D monogram, drawn for this version:

- `v5/assets/brand/mark.svg` (currentColor)
- `v5/assets/brand/mark-black.svg`
- `v5/assets/brand/mark-white.svg`
- `v5/assets/brand/mark-gold.svg`
- `v5/favicon.svg`

The wordmark “Diler Services” is set in Rafory Grotesk next to the mark. On black the wordmark is white and the mark is gold. On white the wordmark is black and the mark is gold.

## Scope of this version

Home page, navigation, and footer only (`v5/index.html`). Services, service detail, pricing, about, contact, legal pages, the Spanish mirror, and Stripe checkout are not built yet. Nav links are in-page anchors. The Spanish control is present and points at `#es` until `/es/` exists. `BOOK_CALL_URL` and `START_LLC_URL` live in `v5/assets/js/nav.js`.
