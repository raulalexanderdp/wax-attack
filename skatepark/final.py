#!/usr/bin/env python3
"""Vega Baja Skate Park - 16:9 black & white overhead layout base. Units: feet."""
import math, geom as G

W, H = 1920, 1080
MARGIN_X, TOP = 290, 140
S = (W - 2*MARGIN_X) / G.PAD_L          # canvas px per foot
PARK_H = G.PAD_D * S
TX = f"translate({MARGIN_X},{TOP}) scale({S:.5f})"

def w(px):  return round(px / S, 4)     # stroke authored in final px
def f(v):   return round(v, 3)
def cx(x):  return MARGIN_X + x * S     # feet -> canvas px
def cy(y):  return TOP + y * S

# ----------------------------------------------------------------- park layer
def rect(x, y, ww, hh, cls, sw):
    return f'<rect class="{cls}" x="{f(x)}" y="{f(y)}" width="{f(ww)}" height="{f(hh)}" stroke-width="{w(sw)}"/>'

def draw(o):
    x, y, ww, hh, kind, _ = o
    g = []
    if kind == 'rail':
        if ww >= hh:
            m = y + hh/2
            g.append(f'<line class="rail" x1="{f(x)}" y1="{f(m)}" x2="{f(x+ww)}" y2="{f(m)}" stroke-width="{w(4.0)}"/>')
            for p in (x, x+ww):
                g.append(f'<line class="obj" x1="{f(p)}" y1="{f(m-1.2)}" x2="{f(p)}" y2="{f(m+1.2)}" stroke-width="{w(2.6)}"/>')
        else:
            m = x + ww/2
            g.append(f'<line class="rail" x1="{f(m)}" y1="{f(y)}" x2="{f(m)}" y2="{f(y+hh)}" stroke-width="{w(4.0)}"/>')
            for p in (y, y+hh):
                g.append(f'<line class="obj" x1="{f(m-1.2)}" y1="{f(p)}" x2="{f(m+1.2)}" y2="{f(p)}" stroke-width="{w(2.6)}"/>')
    elif kind == 'bank':
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
        g.append(f'<line class="thin" x1="{f(x)}" y1="{f(y+1.8)}" x2="{f(x+ww)}" y2="{f(y+1.8)}" stroke-width="{w(2.0)}"/>')
    elif kind == 'wedge':
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
        m = y + hh/2
        g.append(f'<line class="thin" x1="{f(x)}" y1="{f(m)}" x2="{f(x+ww)}" y2="{f(m)}" stroke-width="{w(2.0)}"/>')
        lo = x if G.WEDGE_HIGH_END == 'east' else x + ww
        hi = x + ww if G.WEDGE_HIGH_END == 'east' else x
        k = lo + (hi - lo)*0.22
        g.append(f'<line class="thin" x1="{f(lo)}" y1="{f(y)}" x2="{f(k)}" y2="{f(m)}" stroke-width="{w(2.0)}"/>')
        g.append(f'<line class="thin" x1="{f(lo)}" y1="{f(y+hh)}" x2="{f(k)}" y2="{f(m)}" stroke-width="{w(2.0)}"/>')
    elif kind == 'shelter':
        g.append(rect(x, y, ww, hh, 'shelter', 3.2))
    elif kind == 'slab':
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
        i = 1.15
        if ww > 2*i and hh > 2*i:
            g.append(rect(x+i, y+i, ww-2*i, hh-2*i, 'thin', 1.4))
    else:
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
    return "\n      ".join(g)

def park():
    o = [f'<path class="pad" d="{G.PAD}" stroke-width="{w(4.5)}"/>',
         f'<path class="coping" d="{G.BOWL_COPING}" stroke-width="{w(3.4)}"/>',
         f'<path class="floor"  d="{G.BOWL_FLOOR}"  stroke-width="{w(2.4)}"/>']
    for (a, b), (c, d) in G.JOINT:
        o.append(f'<line class="joint" x1="{f(a)}" y1="{f(b)}" x2="{f(c)}" y2="{f(d)}" stroke-width="{w(2.0)}"/>')
    for ob in G.OBJECTS:
        o.append(draw(ob))
    a, b, r = G.DRAIN
    o.append(f'<circle class="obj" cx="{f(a)}" cy="{f(b)}" r="{f(r)}" stroke-width="{w(2.2)}"/>')
    x, y, ww, hh = G.OFFPAD
    o.append(f'<rect class="offpad" x="{f(x)}" y="{f(y)}" width="{f(ww)}" height="{f(hh)}" stroke-width="{w(2.6)}"/>')
    return "\n      ".join(o)

# ---------------------------------------------------------------------- icons
# Both symbols are drawn in canvas pixels so they stay legible at any park
# scale, and both point along -y (north) at rotation 0.
CAM_ICON = '''
  <g id="cam">
    <rect x="-17" y="-47" width="34" height="13" rx="2"/>
    <line x1="-17" y1="-41.5" x2="17" y2="-41.5" stroke-width="2"/>
    <rect x="-15" y="-34" width="30" height="14" rx="1.5"/>
    <g stroke-width="1.8">
      <line x1="-11" y1="-33" x2="-11" y2="-21"/><line x1="-7.3" y1="-33" x2="-7.3" y2="-21"/>
      <line x1="-3.6" y1="-33" x2="-3.6" y2="-21"/><line x1="0" y1="-33" x2="0" y2="-21"/>
      <line x1="3.6" y1="-33" x2="3.6" y2="-21"/><line x1="7.3" y1="-33" x2="7.3" y2="-21"/>
      <line x1="11" y1="-33" x2="11" y2="-21"/>
    </g>
    <rect x="-13" y="-20" width="26" height="6" rx="1.5"/>
    <rect x="-23" y="-14" width="46" height="45" rx="4" stroke-width="3"/>
    <rect x="23" y="-4" width="9" height="23" rx="2"/>
    <path d="M -23,-8 L -40,-8" stroke-width="2.4"/>
    <rect x="-29" y="-11.5" width="7" height="7" rx="1"/>
    <path d="M -40,-14.5 L -56,-17 L -53.5,-3 L -40,-4 Z"/>
    <rect x="-9" y="3" width="15" height="21" rx="2"/>
    <line x1="-6" y1="19" x2="0" y2="19" stroke-width="2"/>
    <rect x="-15" y="31" width="30" height="9" rx="1.5"/>
    <rect x="-12" y="40" width="24" height="8" rx="1.5"/>
  </g>'''

# Person: filled cap, white face chord, nose point. Faces +y (south) at rot 0,
# so a band facing the camera needs no rotation.
PERSON_ICON = '''
  <g id="person">
    <ellipse cx="0" cy="0" rx="30" ry="12" stroke-width="2.8"/>
    <ellipse cx="-21" cy="0" rx="2.6" ry="6" stroke-width="2"/>
    <ellipse cx="21" cy="0" rx="2.6" ry="6" stroke-width="2"/>
    <circle cx="0" cy="-2" r="16" fill="#000" stroke-width="2.4"/>
    <path d="M -15.2,3 A 16,16 0 0 0 15.2,3 Z" fill="#fff" stroke-width="2.4"/>
    <path d="M -5.5,12.5 L 0,19 L 5.5,12.5 Z" fill="#000" stroke-width="2"/>
  </g>'''

LENS_OFFSET = 46          # canvas px from icon origin to the front of the lens

def cone(x, y, rot, fov, length):
    """FOV wedge, apex at the lens front, in canvas px."""
    h = math.radians(fov/2); a = math.radians(rot)
    ax = cx(x) + math.sin(a)*LENS_OFFSET
    ay = cy(y) - math.cos(a)*LENS_OFFSET
    reach = length*S - LENS_OFFSET
    pts = [(ax + math.sin(a + s*h)*reach, ay - math.cos(a + s*h)*reach) for s in (-1, 1)]
    return (f'<path class="cone" d="M {ax:.1f},{ay:.1f} L {pts[0][0]:.1f},{pts[0][1]:.1f} '
            f'L {pts[1][0]:.1f},{pts[1][1]:.1f} Z"/>')

def cameras():
    o = []
    for x, y, tag, lens, fov, (tx, ty), _role in G.CAMERAS:
        dx, dy = tx - x, ty - y
        rot = math.degrees(math.atan2(dx, -dy))
        o.append(cone(x, y, rot, fov, math.hypot(dx, dy)))
        o.append(f'<g class="icon" transform="translate({cx(x):.1f},{cy(y):.1f}) rotate({rot:.1f})">'
                 f'<use href="#cam"/></g>')
        o.append(f'<text x="{cx(x):.1f}" y="{cy(y)+72:.1f}" class="camtag" text-anchor="middle">CAM {tag}</text>')
        o.append(f'<text x="{cx(x):.1f}" y="{cy(y)+92:.1f}" class="camlens" text-anchor="middle">{lens}</text>')
    return "\n    ".join(o)

BAND_ICON_SCALE = 0.5

def band():
    x, y, ww, hh = G.PERF_AREA
    o = [f'<rect class="perf" x="{cx(x):.1f}" y="{cy(y):.1f}" width="{ww*S:.1f}" height="{hh*S:.1f}"/>']
    for i, (bx, by, rot, _label) in enumerate(G.BAND, 1):
        o.append(f'<g class="icon" transform="translate({cx(bx):.1f},{cy(by):.1f}) rotate({rot}) '
                 f'scale({BAND_ICON_SCALE})"><use href="#person"/></g>')
        o.append(f'<circle class="key" cx="{cx(bx)-19:.1f}" cy="{cy(by)-17:.1f}" r="10"/>')
        o.append(f'<text x="{cx(bx)-19:.1f}" y="{cy(by)-12.5:.1f}" class="keynum" text-anchor="middle">{i}</text>')
    return "\n    ".join(o)

def bandlegend(x, y):
    o = [f'<g transform="translate({x},{y})">',
         '<text x="0" y="0" class="sub">BAND &#183; LAYOUT 2 / SEMI-CIRCLE</text>']
    for i, (_bx, _by, _r, label) in enumerate(G.BAND, 1):
        yy = 26 + (i-1)*21
        o.append(f'<circle class="key" cx="7" cy="{yy-5}" r="10"/>')
        o.append(f'<text x="7" y="{yy-0.5}" class="keynum" text-anchor="middle">{i}</text>')
        o.append(f'<text x="28" y="{yy}" class="legend">{label}</text>')
    o.append('</g>')
    return "\n    ".join(o)

# ------------------------------------------------------------------ furniture
def scalebar(x, y):
    seg = 25 * S
    o = [f'<g transform="translate({x:.1f},{y:.1f})">',
         f'<rect x="0" y="0" width="{seg:.1f}" height="11" fill="#000"/>',
         f'<rect x="{seg:.1f}" y="0" width="{seg:.1f}" height="11" fill="none" stroke="#000" stroke-width="2"/>',
         f'<rect x="{2*seg:.1f}" y="0" width="{seg:.1f}" height="11" fill="#000"/>']
    for i in range(4):
        o.append(f'<text x="{i*seg:.1f}" y="-12" class="tick" text-anchor="middle">{i*25}</text>')
    o.append(f'<text x="{3*seg+28:.1f}" y="-12" class="tick">FEET</text>')
    o.append(f'<text x="0" y="31" class="note">PAD {G.PAD_L:.1f} ft &#215; {G.PAD_D:.1f} ft &#183; SCALE FROM GOOGLE MAPS BAR</text>')
    o.append('</g>')
    return "\n    ".join(o)

def northarrow(x, y):
    return (f'<g transform="translate({x},{y})"><path d="M 0,-38 L 12,22 L 0,12 L -12,22 Z" fill="#000"/>'
            f'<text x="0" y="46" class="tick" text-anchor="middle">N</text></g>')

def camlegend(x, y):
    o = [f'<g transform="translate({x},{y})">',
         '<text x="0" y="0" class="sub">CAMERAS</text>']
    for i, (_x, _y, tag, lens, _fov, _t, role) in enumerate(G.CAMERAS):
        yy = 26 + i*21
        o.append(f'<text x="0"   y="{yy}" class="legend" font-weight="700">{tag}</text>')
        o.append(f'<text x="22"  y="{yy}" class="legend">{lens}</text>')
        o.append(f'<text x="128" y="{yy}" class="legend">{role}</text>')
    o.append(f'<text x="0" y="{26+len(G.CAMERAS)*21+16}" class="note">CONES AT THE WIDE END, FULL FRAME</text>')
    o.append('</g>')
    return "\n    ".join(o)

def grid_layer():
    step = 20 * S
    o = ['<g class="grid">']
    x = MARGIN_X
    while x <= W - MARGIN_X + 0.5:
        o.append(f'<line x1="{x:.2f}" y1="{TOP-24:.1f}" x2="{x:.2f}" y2="{TOP+PARK_H+24:.1f}"/>'); x += step
    y = TOP
    while y <= TOP + PARK_H + 0.5:
        o.append(f'<line x1="{MARGIN_X}" y1="{y:.2f}" x2="{W-MARGIN_X}" y2="{y:.2f}"/>'); y += step
    o.append('</g>')
    return "\n    ".join(o)

CSS = f"""
    text {{ font-family:'Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif; fill:#000 }}
    .pad,.coping,.floor,.thin,.joint,.obj,.rail,.shelter,.offpad {{
      fill:#fff; stroke:#000; stroke-linejoin:round; stroke-linecap:round }}
    .thin,.joint,.floor,.coping,.rail {{ fill:none }}
    .joint   {{ stroke-dasharray:{w(14)} {w(9)} }}
    .shelter {{ fill:url(#hatch) }}
    .offpad  {{ fill:none; stroke-dasharray:{w(11)} {w(8)} }}
    .icon    {{ fill:#fff; stroke:#000; stroke-width:2.4; stroke-linejoin:round; stroke-linecap:round }}
    .cone    {{ fill:#000; fill-opacity:0.045; stroke:#000; stroke-width:1.0; stroke-opacity:0.55; stroke-dasharray:8 7 }}
    .perf    {{ fill:none; stroke:#000; stroke-width:1.6; stroke-dasharray:9 7 }}
    .title   {{ font-size:26px; letter-spacing:4.5px; font-weight:700 }}
    .sub     {{ font-size:15px; letter-spacing:2.6px }}
    .tick    {{ font-size:15px; letter-spacing:1.6px }}
    .note    {{ font-size:12.5px; letter-spacing:1.4px }}
    .legend  {{ font-size:14px; letter-spacing:1.4px }}
    .camtag  {{ font-size:16px; letter-spacing:2.4px; font-weight:700 }}
    .camlens {{ font-size:13px; letter-spacing:1.6px }}
    .key     {{ fill:#000; stroke:none }}
    .keynum  {{ font-size:13px; font-weight:700; fill:#fff; letter-spacing:0 }}
    .grid line {{ stroke:#000; stroke-width:0.6; opacity:0.22 }}
"""
DEFS = f"""
  <defs>
    <pattern id="hatch" patternUnits="userSpaceOnUse" width="2.0" height="2.0" patternTransform="rotate(45)">
      <rect width="2.0" height="2.0" fill="#fff"/>
      <line x1="0" y1="0" x2="0" y2="2.0" stroke="#000" stroke-width="0.42"/>
    </pattern>{CAM_ICON}{PERSON_ICON}
  </defs>"""

def svg(transparent=False, annotate=True, grid=False, cams=True, show_band=False):
    bg = '' if transparent else f'<rect width="{W}" height="{H}" fill="#fff"/>'
    anno = ''
    if annotate:
        anno = f'''
    <text x="{MARGIN_X}" y="86" class="title">VEGA BAJA SKATE PARK</text>
    <text x="{MARGIN_X}" y="112" class="sub">OVERHEAD LAYOUT BASE &#183; NORTH UP</text>
    {camlegend(W-MARGIN_X-300, 86)}
    {bandlegend(MARGIN_X, 790) if show_band else ''}
    {scalebar(MARGIN_X, 1032)}
    {northarrow(W-MARGIN_X, 1010)}'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>Vega Baja Skate Park - overhead layout base</title>
  <style>{CSS}</style>{DEFS}
  {bg}
  {grid_layer() if grid else ''}
  <g id="park" transform="{TX}">
      {park()}
  </g>
  {band() if show_band else ''}
  {cameras() if cams else ''}{anno}
</svg>
'''

if __name__ == "__main__":
    import sys, os, cairosvg, itertools
    for a, b in itertools.combinations(G.OBJECTS, 2):
        ox = min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0])
        oy = min(a[1]+a[3], b[1]+b[3]) - max(a[1], b[1])
        assert not (ox > 1e-9 and oy > 1e-9), f'overlap: {a[5]} / {b[5]}'
    rail = next(o for o in G.OBJECTS if o[5].startswith('long flat rail'))
    assert abs((rail[0]+rail[2]/2) - G.BOX_CX) < 1e-9
    assert abs(G.CAMERAS[0][0] - G.BOX_CX) < 1e-9
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    jobs = [('vega-baja-skatepark-overhead.svg',         dict()),
            ('vega-baja-skatepark-overhead-layout2.svg', dict(show_band=True)),
            ('vega-baja-skatepark-overhead-clean.svg',   dict(annotate=False, cams=False)),
            ('vega-baja-skatepark-overhead-alpha.svg',   dict(annotate=False, cams=False, transparent=True)),
            ('vega-baja-skatepark-overhead-grid.svg',    dict(grid=True))]
    for name, kw in jobs:
        p = os.path.join(out, name)
        open(p, 'w').write(svg(**kw))
        cairosvg.svg2png(url=p, write_to=p.replace('.svg', '.png'),
                         output_width=3840, output_height=2160,
                         background_color=None if kw.get('transparent') else '#ffffff')
        print('wrote', name)
    print(f'{S:.4f} px/ft; pad {G.PAD_L} x {G.PAD_D} ft; rail/box/camA centred at {G.BOX_CX} ft')
