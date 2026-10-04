#!/usr/bin/env python3
"""Vega Baja Skate Park - 16:9 black & white overhead layout base."""
import geom as G

W, H = 1920, 1080
MARGIN_X, TOP = 190, 215
S = (W - 2*MARGIN_X) / G.PAD_L            # canvas px per metre
PARK_H = G.PAD_D * S
TX = f"translate({MARGIN_X},{TOP}) scale({S:.5f})"

def w(px):                                 # stroke authored in final px
    return round(px / S, 4)
def f(v):
    return round(v, 4)

# ------------------------------------------------------------------ bowl path

# -------------------------------------------------------------- object drawing
def rect(x, y, ww, hh, cls, sw):
    return f'<rect class="{cls}" x="{f(x)}" y="{f(y)}" width="{f(ww)}" height="{f(hh)}" stroke-width="{w(sw)}"/>'

def draw(o):
    x, y, ww, hh, kind, _ = o
    g = []
    if kind == 'rail':
        # centreline bar with end posts - reads as a rail, not a wall
        if ww >= hh:
            cy = y + hh/2
            g.append(f'<line class="rail" x1="{f(x)}" y1="{f(cy)}" x2="{f(x+ww)}" y2="{f(cy)}" stroke-width="{w(4.0)}"/>')
            for px in (x, x+ww):
                g.append(f'<line class="obj" x1="{f(px)}" y1="{f(cy-0.35)}" x2="{f(px)}" y2="{f(cy+0.35)}" stroke-width="{w(2.6)}"/>')
        else:
            cx = x + ww/2
            g.append(f'<line class="rail" x1="{f(cx)}" y1="{f(y)}" x2="{f(cx)}" y2="{f(y+hh)}" stroke-width="{w(4.0)}"/>')
            for py in (y, y+hh):
                g.append(f'<line class="obj" x1="{f(cx-0.35)}" y1="{f(py)}" x2="{f(cx+0.35)}" y2="{f(py)}" stroke-width="{w(2.6)}"/>')
    elif kind == 'bank':
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
        # top-of-transition line along the high (north) edge + fall ticks
        g.append(f'<line class="thin" x1="{f(x)}" y1="{f(y+0.55)}" x2="{f(x+ww)}" y2="{f(y+0.55)}" stroke-width="{w(2.0)}"/>')
    elif kind == 'wedge':
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
        cy = y + hh/2
        g.append(f'<line class="thin" x1="{f(x)}" y1="{f(cy)}" x2="{f(x+ww)}" y2="{f(cy)}" stroke-width="{w(2.0)}"/>')
        hi = x + ww if G.WEDGE_HIGH_END == 'east' else x
        lo = x if G.WEDGE_HIGH_END == 'east' else x + ww
        g.append(f'<line class="thin" x1="{f(lo)}" y1="{f(y)}" x2="{f(lo + (hi-lo)*0.22)}" y2="{f(cy)}" stroke-width="{w(2.0)}"/>')
        g.append(f'<line class="thin" x1="{f(lo)}" y1="{f(y+hh)}" x2="{f(lo + (hi-lo)*0.22)}" y2="{f(cy)}" stroke-width="{w(2.0)}"/>')
    elif kind == 'shelter':
        g.append(rect(x, y, ww, hh, 'shelter', 3.2))
        g.append(f'<line class="thin" x1="{f(x)}" y1="{f(y)}" x2="{f(x+ww)}" y2="{f(y+hh)}" stroke-width="{w(1.4)}"/>')
        g.append(f'<line class="thin" x1="{f(x+ww)}" y1="{f(y)}" x2="{f(x)}" y2="{f(y+hh)}" stroke-width="{w(1.4)}"/>')
    elif kind == 'slab':
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
        i = 0.35
        if ww > 2*i and hh > 2*i:
            g.append(rect(x+i, y+i, ww-2*i, hh-2*i, 'thin', 1.4))
    else:                                            # ledge / box
        g.append(rect(x, y, ww, hh, 'obj', 3.0))
    return "\n      ".join(g)

def park():
    o = [f'<path class="pad" d="{G.PAD}" stroke-width="{w(4.5)}"/>',
         f'<path class="coping" d="{G.BOWL_COPING}" stroke-width="{w(3.4)}"/>',
         f'<path class="floor"  d="{G.BOWL_FLOOR}" stroke-width="{w(2.4)}"/>']
    for (a, b), (c, d) in G.JOINT:
        o.append(f'<line class="joint" x1="{f(a)}" y1="{f(b)}" x2="{f(c)}" y2="{f(d)}" stroke-width="{w(2.0)}"/>')
    for ob in G.OBJECTS:
        o.append(draw(ob))
    cx, cy, r = G.DRAIN
    o.append(f'<circle class="obj" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" stroke-width="{w(2.2)}"/>')
    x, y, ww, hh = G.OFFPAD
    o.append(f'<rect class="offpad" x="{f(x)}" y="{f(y)}" width="{f(ww)}" height="{f(hh)}" stroke-width="{w(2.6)}"/>')
    return "\n      ".join(o)

# ------------------------------------------------------------------ furniture
def scalebar(x, y):
    seg = 10 * S
    o = [f'<g transform="translate({x:.1f},{y:.1f})">',
         f'<rect x="0" y="0" width="{seg:.1f}" height="11" fill="#000"/>',
         f'<rect x="{seg:.1f}" y="0" width="{seg:.1f}" height="11" fill="none" stroke="#000" stroke-width="2"/>',
         f'<rect x="{2*seg:.1f}" y="0" width="{seg:.1f}" height="11" fill="#000"/>']
    for i in range(4):
        o.append(f'<text x="{i*seg:.1f}" y="-12" class="tick" text-anchor="middle">{i*10}</text>')
    o.append(f'<text x="{3*seg+30:.1f}" y="-12" class="tick">METRES</text>')
    o.append(f'<text x="0" y="32" class="note">PAD {G.PAD_L:.1f} m &#215; {G.PAD_D:.1f} m &#183; SCALE FROM GOOGLE MAPS BAR</text>')
    o.append('</g>')
    return "\n    ".join(o)

def northarrow(x, y):
    return (f'<g transform="translate({x},{y})">'
            f'<path d="M 0,-40 L 13,24 L 0,13 L -13,24 Z" fill="#000"/>'
            f'<text x="0" y="50" class="tick" text-anchor="middle">N</text></g>')

def camera(x, y):
    """Main camera position + look direction: south of the pad, facing north."""
    return (f'<g transform="translate({x:.1f},{y:.1f})">'
            f'<circle cx="0" cy="0" r="9" fill="#000"/>'
            f'<path d="M -26,34 L 0,2 L 26,34" fill="none" stroke="#000" stroke-width="2.6"/>'
            f'<text x="0" y="56" class="tick" text-anchor="middle">CAM A</text></g>')

def grid_layer():
    step = 5 * S
    o = ['<g class="grid">']
    x = MARGIN_X
    while x <= W - MARGIN_X + 0.5:
        o.append(f'<line x1="{x:.2f}" y1="{TOP-30:.1f}" x2="{x:.2f}" y2="{TOP+PARK_H+30:.1f}"/>'); x += step
    y = TOP
    while y <= TOP + PARK_H + 0.5:
        o.append(f'<line x1="{MARGIN_X}" y1="{y:.2f}" x2="{W-MARGIN_X}" y2="{y:.2f}"/>'); y += step
    o.append('</g>')
    return "\n    ".join(o)

CSS = f"""
    text {{ font-family:'Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif; fill:#000 }}
    .pad,.coping,.floor,.thin,.joint,.obj,.rail,.step,.shelter,.offpad {{
      fill:#fff; stroke:#000; stroke-linejoin:round; stroke-linecap:round }}
    .thin,.joint,.floor,.coping,.rail {{ fill:none }}
    .joint  {{ stroke-dasharray:{w(14)} {w(9)} }}
    .shelter{{ fill:url(#hatch) }}
    .offpad {{ fill:none; stroke-dasharray:{w(11)} {w(8)} }}
    .title {{ font-size:26px; letter-spacing:4.5px; font-weight:700 }}
    .sub   {{ font-size:15px; letter-spacing:2.6px }}
    .tick  {{ font-size:15px; letter-spacing:1.6px }}
    .note  {{ font-size:12.5px; letter-spacing:1.4px }}
    .grid line {{ stroke:#000; stroke-width:0.6; opacity:0.22 }}
"""
DEFS = """
  <defs>
    <pattern id="hatch" patternUnits="userSpaceOnUse" width="0.42" height="0.42" patternTransform="rotate(45)">
      <rect width="0.42" height="0.42" fill="#fff"/>
      <line x1="0" y1="0" x2="0" y2="0.42" stroke="#000" stroke-width="0.09"/>
    </pattern>
  </defs>
"""

def svg(transparent=False, annotate=True, grid=False, cam=True):
    bg = '' if transparent else f'<rect width="{W}" height="{H}" fill="#fff"/>'
    anno = ''
    if annotate:
        anno = f'''
    <text x="{MARGIN_X}" y="132" class="title">VEGA BAJA SKATE PARK</text>
    <text x="{MARGIN_X}" y="160" class="sub">OVERHEAD LAYOUT BASE &#183; NORTH UP</text>
    {scalebar(MARGIN_X, 936)}
    {northarrow(W-MARGIN_X, 930)}'''
    camg = camera(MARGIN_X + 41.0*S, TOP + PARK_H + 46) if cam else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>Vega Baja Skate Park - overhead layout base</title>
  <style>{CSS}</style>{DEFS}
  {bg}
  {grid_layer() if grid else ''}
  <g id="park" transform="{TX}">
      {park()}
  </g>
  {camg}{anno}
</svg>
'''

if __name__ == "__main__":
    import sys, os, cairosvg, itertools
    for a, b in itertools.combinations(G.OBJECTS, 2):
        ox = min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0])
        oy = min(a[1]+a[3], b[1]+b[3]) - max(a[1], b[1])
        assert not (ox > 1e-9 and oy > 1e-9), f'overlap: {a[5]} / {b[5]}'
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    jobs = [('vega-baja-skatepark-overhead.svg',       dict()),
            ('vega-baja-skatepark-overhead-clean.svg', dict(annotate=False, cam=False)),
            ('vega-baja-skatepark-overhead-alpha.svg', dict(annotate=False, cam=False, transparent=True)),
            ('vega-baja-skatepark-overhead-grid.svg',  dict(grid=True))]
    for name, kw in jobs:
        p = os.path.join(out, name)
        open(p, 'w').write(svg(**kw))
        cairosvg.svg2png(url=p, write_to=p.replace('.svg', '.png'),
                         output_width=3840, output_height=2160,
                         background_color=None if kw.get('transparent') else '#ffffff')
        print('wrote', name)
    print(f'{S:.3f} canvas px per metre; pad {G.PAD_L} x {G.PAD_D} m; no overlaps')
