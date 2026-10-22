"""Brand Kit v3 asset pass for the Consultore clone.

Reads the untouched template files in _build/template/ and writes v3/assets/:
  * CSS: every template colour swapped for its Brand Kit v3 role (background, text, border),
    Catamaran swapped for Inter. Layout, spacing, animation and component rules are untouched.
  * Images: background textures, hero circle, arrow, icon badges and sparkle marks are recoloured
    pixel by pixel (hue shift that keeps grain, shading and alpha), never removed.
  * SVG icons: template colours swapped; tax lettering inside the icon art is redrawn as our own
    lettering (LLC, EIN, FL...) in Inter Bold outlines so it renders the same everywhere.
  * Photos: crop() cuts our photos to the exact size of each template placeholder.
Run:  python3 v3/_build/assets.py   (build.py calls it first)
"""
import colorsys
import os
import re
import shutil
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
SRC = os.path.join(HERE, 'template', 'assets')
OUT = os.path.join(V3, 'assets')
PYLIB = os.environ.get('DS_PYLIB')  # optional extra path that holds fontTools
if PYLIB:
    sys.path.insert(0, PYLIB)

# ---------------------------------------------------------------- Brand Kit v3
DARK, DENIM, BLUE, SAND = '#1E2B40', '#395278', '#346BB5', '#7A6650'
LIGHT, LINE, MUTED, TEXT = '#F3F5F7', '#D5DAE1', '#646B6C', '#1F2430'
SKY = '#DCE7F6'      # light blue tint (replaces light lilac surfaces)
SKY2 = '#EEF3FA'     # lightest blue tint
SANDT = '#ECE4D8'    # light sand tint (replaces yellow highlight marks)
ICON_FILL = '#A9C4EA'  # icon accent fill (replaces the yellow fill inside icon art)

# template colour -> (background, text, border)
CSS_MAP = {
    '#0e1124': (DARK, TEXT, DARK), '#0b0a23': (DARK, TEXT, DARK), '#10002b': (DARK, TEXT, DARK),
    '#161540': (DARK, TEXT, DARK), '#131731': (DARK, TEXT, DARK), '#14213d': (DARK, TEXT, DARK),
    '#142329': (DARK, TEXT, DARK), '#06063f': (DARK, TEXT, DARK), '#1c1414': (DARK, TEXT, DARK),
    '#03256c': (DENIM, DENIM, DENIM), '#2a0072': (DENIM, DENIM, DENIM), '#133a8a': (DENIM, DENIM, DENIM),
    '#9667e0': (DENIM, DENIM, DENIM),
    '#d4aeff': (BLUE, BLUE, BLUE),
    '#fede65': (SANDT, SAND, SAND), '#ffe456': (SANDT, SAND, SAND),
    '#ff3e55': (BLUE, BLUE, BLUE), '#00bf71': (BLUE, BLUE, BLUE), '#fc0c0c': (BLUE, BLUE, BLUE),
    '#03a600': (BLUE, BLUE, BLUE), '#f23936': (BLUE, BLUE, BLUE), '#ff2424': (BLUE, BLUE, BLUE),
    '#eb6300': (BLUE, BLUE, BLUE), '#ff00c7': (BLUE, BLUE, BLUE), '#ff9c00': (SAND, SAND, SAND),
    '#fca311': (SAND, SAND, SAND), '#ffba00': (SAND, SAND, SAND),
    '#f3f3f3': (LIGHT, TEXT, LINE), '#f3f4fa': (LIGHT, TEXT, LINE), '#f4f4f4': (LIGHT, TEXT, LINE),
    '#dfc8f8': ('#C3D5EE', DENIM, '#C3D5EE'), '#f0e8f8': (SKY2, DENIM, SKY2), '#efe1ff': (SKY2, DENIM, SKY2),
    '#f3ecff': (SKY2, DENIM, SKY2), '#83bcff': (SKY, DENIM, SKY), '#a9d6ff': (SKY, DENIM, SKY),
    '#eaf8ff': (SKY2, DENIM, SKY2), '#f4f8ff': (SKY2, DENIM, SKY2), '#eff1ff': (SKY2, DENIM, SKY2),
    '#656565': (MUTED, MUTED, LINE), '#47494e': ('#47494E', '#4A5160', LINE),
}
RGBA_MAP = {
    (212, 174, 255): (52, 107, 181),   # lilac -> blue (alpha kept)
    (14, 17, 36): (31, 36, 48),        # template ink -> brand text
    (16, 0, 43): (30, 43, 64),
    (242, 57, 54): (52, 107, 181),
    (226, 132, 132): (52, 107, 181),
}
# Where the template uses lilac as a surface behind dark content (tiles, hover cards), use the light
# tint instead of solid blue so dark text and icon outlines keep their contrast.
LILAC_AS_TINT = ['.fact-icon', '.work-icon', '.work-item:hover', '.price-box:hover', '.about-choose-box:hover',
                 '.service-details-list ul li:hover', '.preview-counter:hover', '.preview-icon', '.details-tag',
                 '.shop-box-hover-icons', 'li.active-size', '.team-page-box-hover', 'li.li', '.number',
                 'hadding span.span', 'testimonial-page', '.main-menu-ex li li a:hover::after']
# Where the yellow is a solid offset block (the 6px "shadow" behind buttons and cards) use Sand itself.
YELLOW_AS_SAND = ['::after', ':hover']
YELLOW_KEEP_TINT = ['span::before', '.fact-box:hover', '.shop-page-hadding', 'color-selactor', '.chack2']

HEX = re.compile(r'#[0-9a-fA-F]{3,8}\b')
# Heading twins: every rule for h1/h4/h6 also styles .ds-h1/.ds-h4/.ds-h6, so section titles can be
# real <h2> elements (one <h1> per page) and keep the template's exact look.
HTAG = re.compile(r'(?<![\w.#-])h([146])(?![\w-])')


def _norm(h):
    h = h.lower()
    if len(h) == 4:
        h = '#' + ''.join(c * 2 for c in h[1:])
    return h


def _swap_hex(m, kind, sel):
    raw = m.group(0)
    h = _norm(raw)
    alpha = ''
    if len(h) == 9:
        h, alpha = h[:7], h[7:]
    if h not in CSS_MAP:
        return raw
    bg, tx, bd = CSS_MAP[h]
    new = {'bg': bg, 'text': tx, 'border': bd}.get(kind, bd)
    if h == '#d4aeff' and kind == 'bg' and any(k in sel for k in LILAC_AS_TINT):
        new = SKY
    if h in ('#fede65', '#ffe456') and kind == 'bg':
        if any(k in sel for k in YELLOW_KEEP_TINT):
            new = SANDT
        elif any(k in sel for k in YELLOW_AS_SAND):
            new = SAND
    return new + alpha


def _swap_rgba(m):
    parts = [p.strip() for p in m.group(1).split(',')]
    try:
        rgb = tuple(int(float(p)) for p in parts[:3])
    except ValueError:
        return m.group(0)
    if rgb in RGBA_MAP:
        r, g, b = RGBA_MAP[rgb]
        rest = ', '.join(parts[3:])
        return f'rgba({r}, {g}, {b}{", " + rest if rest else ""})' if rest else f'rgb({r}, {g}, {b})'
    return m.group(0)


def recolor_css(text):
    text = text.replace('@import url("https://fonts.googleapis.com/css2?family=Catamaran:wght@100;200;300;400;500;600;700;800;900&display=swap");', '')
    text = re.sub(r'"?Catamaran"?', '"Inter"', text)
    text = re.sub(r'"DM Serif Display"', '"Inter"', text)

    def rule(m):
        sel, body = m.group(1), m.group(2)
        sl = sel.strip().lower()

        def decl(d):
            prop = d.group(1).strip().lower()
            val = d.group(2)
            kind = 'bg' if 'background' in prop else 'text' if prop in ('color', 'fill', 'caret-color', '-webkit-text-fill-color') else 'border'
            val = HEX.sub(lambda x: _swap_hex(x, kind, sl), val)
            val = re.sub(r'rgba?\(([^)]*)\)', _swap_rgba, val)
            return f'{d.group(1)}:{val}'
        body = re.sub(r'([a-zA-Z-]+)\s*:([^;{}]*)', decl, body)
        if not sel.strip().startswith('@'):
            parts = [x for x in sel.split(',')]
            extra = [HTAG.sub(lambda t: '.ds-h' + t.group(1), x) for x in parts if HTAG.search(x)]
            if extra:
                sel = sel.rstrip() + ',' + ','.join(extra) + ' '
        return f'{sel}{{{body}}}'
    return re.sub(r'([^{}]+)\{([^{}]*)\}', rule, text)


# Rules the colour swap alone cannot express: text that sat on lilac now sits on blue, so it turns white.
CSS_FIXES = '''
/* ---- Brand Kit v3: text on the new blue buttons, and the self-hosted Inter face ---- */
@font-face{font-family:"Inter";src:url(../fonts/inter/inter-latin-wght-normal.woff2) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Inter";src:url(../fonts/inter/inter-latin-ext-wght-normal.woff2) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
.home1-button a,.home1-button button,.price-btn a,.contact-form-btn button,.cart-input-btn button,.cart-input-btn2 button,.home1-button a:hover,.home1-button button:hover,.price-btn a:hover,.contact-form-btn button:hover{color:#fff!important}
'''


# ---------------------------------------------------------------- images
def _hsv_arrays(rgb):
    r, g, b = [rgb[..., i] / 255.0 for i in range(3)]
    mx = np.max(rgb / 255.0, axis=-1)
    mn = np.min(rgb / 255.0, axis=-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rm = m & (mx == r)
    gm = m & (mx == g) & ~rm
    bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    h = h * 60.0
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
    return h, s, mx


def _rgb_from_hsv(h, s, v):
    h = (h % 360) / 60.0
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.zeros(h.shape + (3,))
    for k, (a, b_, c) in enumerate([(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]):
        sel = i == k
        out[..., 0][sel], out[..., 1][sel], out[..., 2][sel] = a[sel], b_[sel], c[sel]
    return np.clip(out * 255.0, 0, 255)


def _hex_hsv(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360, s, v


BLUE_H, BLUE_S, BLUE_V = _hex_hsv(BLUE)
DARK_H, DARK_S, _ = _hex_hsv(DARK)
SAND_H, _, _ = _hex_hsv(SAND)


def recolor_image(src, dst, solid_yellow=None):
    im = Image.open(src)
    mode = im.mode
    im = im.convert('RGBA')
    a = np.asarray(im).astype(float)
    rgb, alpha = a[..., :3], a[..., 3]
    h, s, v = _hsv_arrays(rgb)
    purple = (h >= 240) & (h <= 335) & (s > 0.03)
    yellow = (h >= 32) & (h <= 70) & (s > 0.22)
    green = (h >= 110) & (h <= 175) & (s > 0.3)
    red = ((h <= 15) | (h >= 340)) & (s > 0.4) & (v > 0.35)
    ink = (v < 0.32) & ~purple
    nh, ns, nv = h.copy(), s.copy(), v.copy()
    nh[purple] = BLUE_H
    ns[purple] = np.clip(s[purple] * 1.05, 0, 1)
    if solid_yellow:
        yh, ys, yv = _hex_hsv(solid_yellow)
        nh[yellow], ns[yellow], nv[yellow] = yh, ys, np.clip(v[yellow] * yv, 0, 1)
    else:
        nh[yellow], ns[yellow], nv[yellow] = SAND_H, 0.30, np.clip(v[yellow] * 0.90, 0, 1)
    for msk in (green, red):
        nh[msk], ns[msk], nv[msk] = BLUE_H, BLUE_S, BLUE_V
    nh[ink], ns[ink] = DARK_H, np.maximum(s[ink], DARK_S * 0.9)
    out = _rgb_from_hsv(nh, ns, nv)
    res = np.dstack([out, alpha]).astype(np.uint8)
    img = Image.fromarray(res, 'RGBA')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if dst.lower().endswith(('.jpg', '.jpeg')):
        img.convert('RGB').save(dst, quality=88, optimize=True)
    else:
        img.save(dst, optimize=True)


# Template art that is recoloured (placeholders are replaced with photos in build.py instead).
ART = ['header-bg.jpg', 'header-img-3.png', 'header-img-4.png', 'header-img-5.png', 'header-img-6.png',
       'header-inner-bg.png', 'service-bg.png', 'pricing-plan-bg.png', 'testimonial-bg.png', 'subsraibe-bg.png',
       'fact-bg.png', 'about-page-do-bg.png', 'error-bg.png', 'error-img.png', 'features.png',
       'hadding-after-1.png', 'hadding-after-2.png']
ART_SOLID = {'header-img-1.png': BLUE}   # the big hero circle becomes a solid brand-blue disc

def reletter_png(path, box, lines, ink=DARK):
    """Clear the drawn lettering inside box (x0, y0, x1, y1) and draw our lines in Inter Bold."""
    from PIL import ImageDraw, ImageFont
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im).astype(int)
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1, :3]
    light = reg[reg.sum(-1) > 450]
    fill = tuple(int(v) for v in np.median(light, axis=0)) if len(light) else (236, 228, 216)
    k = 8
    big = im.resize((im.width * k, im.height * k), Image.LANCZOS)
    d = ImageDraw.Draw(big)
    d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=fill + (255,))
    font_path = os.path.join(HERE, 'vendor', 'Inter-Bold.otf')
    lh = (y1 - y0) * k / len(lines)
    for i, line in enumerate(lines):
        size = int(lh * 0.95)
        while True:
            fnt = ImageFont.truetype(font_path, size)
            bb = d.textbbox((0, 0), line, font=fnt)
            if bb[2] - bb[0] <= (x1 - x0) * k * 0.98 or size < 8:
                break
            size -= 2
        cx = (x0 + x1) * k / 2
        cy = y0 * k + lh * (i + 0.5)
        d.text((cx, cy), line, font=fnt, fill=ink, anchor='mm')
    big.resize(im.size, Image.LANCZOS).save(path, optimize=True)


# ---------------------------------------------------------------- SVG icons
SVG_MAP = {'#0e1124': DARK, '#06063f': DARK, '#0b0a23': DARK, '#fede65': ICON_FILL, '#ffe456': ICON_FILL,
           '#c41a1a': '#8A919C', '#00bf71': BLUE, '#ff3e55': BLUE, '#03256c': DENIM, '#d4aeff': SKY}

# Lettering to redraw inside the icon art: icon -> labels, one per detected letter row (top to bottom).
RELETTER = {
    'service-icon-1.svg': ['LLC', '+EIN'],   # formation bundle
    'service-icon-2.svg': ['EDIT'],          # amendments
    'service-icon-3.svg': ['FEE'],
    'service-icon-4.svg': ['LLC'],           # LLC formation
    'service-icon-5.svg': ['FL'],            # registered agent shield
    'service-icon-6.svg': ['MAY'],           # annual report (due by May 1)
    'service-icon-8.svg': ['DBA'],           # fictitious name
    'service-icon-9.svg': ['FL'],
    'works-icon-1.svg': ['EIN'],             # EIN filing
    'works-icon-3.svg': ['INFO'],            # step 1: send your information
    'about-vision-icon-1.svg': ['HELP'],
    'about-choose-icon-2.svg': ['FL'],
    'about-choose-icon-3.svg': ['LLC', 'FL'],
    'about-choose-icon-4.svg': ['EIN'],
    'fact-icon-1.svg': ['FEE'],
}


def _letter_rows(svg_text):
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.svgLib.path import parse_path
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg_text).group(1).split()]
    W, H = vb[2], vb[3]
    paths = list(re.finditer(r'<path\b[^>]*?\bd="([^"]+)"[^>]*?/?>', svg_text))
    els = []
    for i, m in enumerate(paths):
        tag = m.group(0)
        fill = (re.search(r'fill="([^"]+)"', tag) or [None, ''])[1].lower()
        p = BoundsPen(None)
        parse_path(m.group(1), p)
        if p.bounds:
            els.append((i, fill, p.bounds, m))
    cand = [e for e in els if e[1] not in ('#fede65', 'white', '#fff', 'none', '') and (e[2][2] - e[2][0]) < 0.2 * W
            and 0.07 * H < (e[2][3] - e[2][1]) < 0.3 * H and 0.8 < (e[2][3] - e[2][1]) / max(e[2][2] - e[2][0], .01) < 3.2]
    groups = []
    for c in sorted(cand, key=lambda c: (round(c[2][1]), c[2][0])):
        for g in groups:
            b0 = g[0][2]
            if abs(c[2][1] - b0[1]) < 0.6 and abs((c[2][3] - c[2][1]) - (b0[3] - b0[1])) < 0.6:
                g.append(c)
                break
        else:
            groups.append([c])
    rows = []
    for g in groups:
        if len(g) < 2:
            continue
        xs = sorted(g, key=lambda c: c[2][0])
        hgt = xs[0][2][3] - xs[0][2][1]
        if max(xs[k + 1][2][0] - xs[k][2][2] for k in range(len(xs) - 1)) > 1.2 * hgt:
            continue
        box = (min(c[2][0] for c in g), min(c[2][1] for c in g), max(c[2][2] for c in g), max(c[2][3] for c in g))
        rows.append((box, [c[3] for c in g], g[0][1]))
    rows.sort(key=lambda r: r[0][1])
    return rows


_FONT = {}


def _text_path(label, box, color):
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    if 'f' not in _FONT:
        _FONT['f'] = TTFont(os.path.join(HERE, 'vendor', 'Inter-Bold.otf'))
    f = _FONT['f']
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    cap = f['OS/2'].sCapHeight or 0.727 * f['head'].unitsPerEm
    names = [cmap[ord(ch)] for ch in label]
    adv = sum(f['hmtx'][n][0] for n in names)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    scale = min(h / cap, (w * 1.08) / adv)
    tw, th = adv * scale, cap * scale
    ox = x0 + (w - tw) / 2
    base = y0 + (h + th) / 2
    pen = SVGPathPen(gs)
    x = 0
    for n in names:
        tp = TransformPen(pen, (scale, 0, 0, -scale, ox + x * scale, base))
        gs[n].draw(tp)
        x += f['hmtx'][n][0]
    return f'<path d="{pen.getCommands()}" fill="{color}"/>'


def recolor_svg(text, name):
    labels = RELETTER.get(name)
    if labels:
        rows = _letter_rows(text)
        drop = []
        add = []
        for (box, ms, fill), label in zip(rows, labels):
            drop += ms
            add.append(_text_path(label, box, fill or '#0e1124'))
        for m in sorted(drop, key=lambda m: -m.start()):
            text = text[:m.start()] + text[m.end():]
        text = text.replace('</svg>', ''.join(add) + '</svg>')
    for k, v in SVG_MAP.items():
        text = re.sub(re.escape(k), v, text, flags=re.I)
    return text


# ---------------------------------------------------------------- photos
PHOTOS = os.path.join(OUT, 'photos')
FOCUS = {'consultation-1': (0.62, 0.42), 'consultation-2': (0.62, 0.45), 'founder-laptop-1': (0.66, 0.42),
         'founder-laptop-2': (0.72, 0.42), 'mailbox-1': (0.36, 0.45), 'office-plants-1': (0.62, 0.62),
         'opening-mail-2': (0.45, 0.48), 'signing-documents-2': (0.5, 0.5)}


def crop(photo, w, h):
    """Cut a photo to a template placeholder's exact size; returns the asset path relative to v3/."""
    rel = f'assets/img/ds/{photo}-{w}x{h}.webp'
    dst = os.path.join(V3, rel)
    if not os.path.exists(dst):
        im = Image.open(os.path.join(PHOTOS, photo + '.webp')).convert('RGB')
        W, H = im.size
        r = w / h
        cw, ch = (W, W / r) if W / H < r else (H * r, H)
        fx, fy = FOCUS.get(photo, (0.5, 0.5))
        left = min(max(fx * W - cw / 2, 0), W - cw)
        top = min(max(fy * H - ch / 2, 0), H - ch)
        im = im.crop((round(left), round(top), round(left + cw), round(top + ch))).resize((w, h), Image.LANCZOS)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        im.save(dst, quality=84, method=6)
    return rel


def logo_tile(size, dst_rel):
    """The Folio icon on white, sized for the template's round testimonial avatar."""
    dst = os.path.join(V3, dst_rel)
    if not os.path.exists(dst):
        shutil.copy(os.path.join(OUT, 'brand', 'DS-icon_full.svg'), dst)
    return dst_rel


# ---------------------------------------------------------------- run
def run():
    # fresh template copies (our brand, photos and Inter files are kept)
    for d in ('css', 'js', 'img'):
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)
    shutil.copytree(os.path.join(SRC, 'css'), os.path.join(OUT, 'css'))
    shutil.copytree(os.path.join(SRC, 'js'), os.path.join(OUT, 'js'))
    os.makedirs(os.path.join(OUT, 'fonts'), exist_ok=True)
    for f in os.listdir(os.path.join(SRC, 'fonts')):
        shutil.copy2(os.path.join(SRC, 'fonts', f), os.path.join(OUT, 'fonts', f))
    # vendored builds of the CDN scripts the template expects (AOS 2.3.4, Waypoints 4.0.1)
    os.makedirs(os.path.join(OUT, 'js', 'vendor'), exist_ok=True)
    for f in ('aos.js', 'jquery.waypoints.min.js'):
        shutil.copy2(os.path.join(HERE, 'vendor', f), os.path.join(OUT, 'js', 'vendor', f))
    shutil.copy2(os.path.join(HERE, 'vendor', 'aos.css'), os.path.join(OUT, 'css', 'plugins', 'aos.css'))
    os.remove(os.path.join(OUT, 'js', 'plugins', 'aos.js'))  # unbuilt ES-module source shipped by the template
    # count-up: ignore a second trigger while a count is running (the shipped plugin throws on it)
    cu = os.path.join(OUT, 'js', 'plugins', 'jquery.countup.js')
    s = open(cu, encoding='utf-8').read()
    s = s.replace("var counterUpper = function() {", "var counterUpper = function() {\n            if ($this.data('counterup-nums')) { return; }", 1)
    s = s.replace("$this.text($this.data('counterup-nums').shift());", "var q = $this.data('counterup-nums'); if (!q) { return; } $this.text(q.shift());")
    open(cu, 'w', encoding='utf-8').write(s)
    # CSS
    for root, _, files in os.walk(os.path.join(OUT, 'css')):
        for f in files:
            if f.endswith('.css') and f in ('master.css', 'comon.css', 'typography.css', 'animation.css'):
                p = os.path.join(root, f)
                t = recolor_css(open(p, encoding='utf-8').read())
                if f == 'master.css':
                    t += CSS_FIXES
                open(p, 'w', encoding='utf-8').write(t)
    # images
    src_img = os.path.join(SRC, 'img')
    for f in ART:
        recolor_image(os.path.join(src_img, 'image', f), os.path.join(OUT, 'img', 'image', f))
    for f, col in ART_SOLID.items():
        recolor_image(os.path.join(src_img, 'image', f), os.path.join(OUT, 'img', 'image', f), solid_yellow=col)
    reletter_png(os.path.join(OUT, 'img', 'image', 'header-img-6.png'), (30, 13, 59, 39), ['LLC', '+EIN'])
    for f in ('checkout-icon-1.png', 'checkout-icon-2.png', 'checkout-icon-3.png', 'checkout-icon-4.png'):
        shutil.copy2(os.path.join(src_img, 'image', f), os.path.join(OUT, 'img', 'image', f))
    for sub in ('icons', 'shapes'):
        os.makedirs(os.path.join(OUT, 'img', sub), exist_ok=True)
        for f in os.listdir(os.path.join(src_img, sub)):
            p = os.path.join(src_img, sub, f)
            if f.endswith('.svg'):
                open(os.path.join(OUT, 'img', sub, f), 'w', encoding='utf-8').write(recolor_svg(open(p, encoding='utf-8').read(), f))
            else:
                recolor_image(p, os.path.join(OUT, 'img', sub, f))
    os.makedirs(os.path.join(OUT, 'img', 'ds'), exist_ok=True)
    shutil.copy2(os.path.join(HERE, 'static', 'diler.css'), os.path.join(OUT, 'css', 'diler.css'))
    shutil.copy2(os.path.join(HERE, 'static', 'diler.js'), os.path.join(OUT, 'js', 'diler.js'))


if __name__ == '__main__':
    run()
    print('assets ok')
