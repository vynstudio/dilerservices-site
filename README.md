# dilerservices.com

Static site for Diler Services LLC: Florida LLC formation and registered agent service, in English and Spanish.
Built on the VikingLab "Consult" template (licensed to dilerservices.com) with the Meridian v2 brand identity applied.

## Preview locally

    python3 -m http.server 4322

Then open http://localhost:4322/

All links and asset paths are relative, so the site also works from a subfolder such as GitHub Pages
(https://vynstudio.github.io/dilerservices-site/). `.nojekyll` tells Pages to serve the files as they are.

## Brand

The Meridian v2 identity (October 2026) is applied as an overlay so the template build and the `_gen/` pipeline stay intact:

- `assets/css/diler-meridian.css`: colours, type and components. The first part is generated from the purged template CSS
  by `_skin/make_meridian.py` (every template colour remapped to the Meridian palette, every font to Vengeance);
  the second part, after the `hand rules` comment, is `_skin/meridian_hand.css`.
- `assets/fonts/vengeance/`: Vengeance Regular, Medium, Bold and Oblique (woff) from the licensed web font kit.
- `assets/brand/`: the logo suite (horizontal, mark, stacked; full colour and reversed) and favicons from the kit.
  Logos are the supplied artwork; the CSS never retypes the wordmark.
- Every page carries `class="ds-meridian"` on `<html>` and links the stylesheet before `</head>`.

Palette: Dark `#1E2B40`, Denim `#395278`, Secondary Blue `#346BB5`, Sand `#7A6650`, Light `#F3F5F7`,
Text `#1F2430`, Muted `#646B6C`, Sky tints `#E4EDFD` and `#EFF4FE`.

To regenerate the stylesheet after a template rebuild:

    python3 _skin/make_meridian.py . assets/css/diler-meridian.css _skin/meridian_hand.css

Diler Services LLC is not a law firm and does not give legal or tax advice.
