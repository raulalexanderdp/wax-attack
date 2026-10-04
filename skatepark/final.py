#!/usr/bin/env python3
"""Build the Vega Baja Skate Park overhead layout background (16:9, B/W)."""
import geom as G

# ---------------------------------------------------------------- scale setup
# Park footprint in source-satellite pixels
U0, U1 = 25, 1292          # west .. east
V0, V1 = 76, 582           # north .. south
PAD_LEN_M = 60.0           # ASSUMED overall length of the concrete pad, metres.
                           # Change this one number to re-scale the scale bar.

W, H = 1920, 1080
MARGIN_X = 190
DRAW_W = W - 2*MARGIN_X
S = DRAW_W / (U1 - U0)                 # px per source px
PARK_H = (V1 - V0) * S
TOP = 215                              # park top edge on canvas
TX = f"translate({MARGIN_X},{TOP}) scale({S:.5f}) translate({-U0},{-V0})"

M_PER_SRCPX = PAD_LEN_M / (U1 - U0)
PX_PER_M = S / M_PER_SRCPX             # canvas px per metre

def w(px):      # stroke width authored in final px, emitted in source-px space
    return round(px / S, 3)

# ------------------------------------------------------------------- geometry
def park():
    o = []
    o.append(f'<path class="pad"    d="{G.PAD}"         stroke-width="{w(4.5)}"/>')
    o.append(f'<path class="coping" d="{G.BOWL_COPING}" stroke-width="{w(3.4)}"/>')
    o.append(f'<path class="floor"  d="{G.BOWL_FLOOR}"  stroke-width="{w(2.4)}"/>')
    for (a, b), (c, d) in G.JOINTS:
        o.append(f'<line class="joint" x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke-width="{w(2.0)}"/>')
    x, y, ww, hh = G.DARKBOX
    o.append(f'<rect class="dark" x="{x}" y="{y}" width="{ww}" height="{hh}" stroke-width="{w(3.0)}"/>')
    for rx in G.DARK_RIBS:
        o.append(f'<line class="thin" x1="{rx}" y1="{y}" x2="{rx}" y2="{y+hh}" stroke-width="{w(2.0)}"/>')
    for x, y, ww, hh, k in G.BOXES:
        cls = 'bank' if k == 'bank' else 'obj'
        o.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{ww}" height="{hh}" '
                 f'rx="2" stroke-width="{w(3.0)}"/>')
    for x, y, ww, hh in G.STEPS:
        o.append(f'<rect class="step" x="{x}" y="{y}" width="{ww}" height="{hh}" stroke-width="{w(2.4)}"/>')
    cx, cy, r = G.DRAIN
    o.append(f'<circle class="obj" cx="{cx}" cy="{cy}" r="{r}" stroke-width="{w(2.2)}"/>')
    x, y, ww, hh = G.OFFPAD
    o.append(f'<rect class="offpad" x="{x}" y="{y}" width="{ww}" height="{hh}" stroke-width="{w(2.6)}"/>')
    return "\n      ".join(o)

# ------------------------------------------------------------------ furniture
def scalebar(x, y):
    """10 m increments, 30 m total."""
    seg = 10 * PX_PER_M
    o = [f'<g class="anno" transform="translate({x:.1f},{y:.1f})">']
    o.append(f'<rect x="0" y="0" width="{seg:.1f}" height="11" fill="#000"/>')
    o.append(f'<rect x="{seg:.1f}" y="0" width="{seg:.1f}" height="11" fill="none" stroke="#000" stroke-width="2"/>')
    o.append(f'<rect x="{2*seg:.1f}" y="0" width="{seg:.1f}" height="11" fill="#000"/>')
    for i in range(4):
        o.append(f'<text x="{i*seg:.1f}" y="-12" class="tick" text-anchor="middle">{i*10}</text>')
    o.append(f'<text x="{3*seg+30:.1f}" y="-12" class="tick">METRES</text>')
    o.append(f'<text x="0" y="32" class="note">SCALE ASSUMED — PAD = {PAD_LEN_M:.0f} m OVERALL. CONFIRM ON SITE.</text>')
    o.append('</g>')
    return "\n    ".join(o)

def northarrow(x, y):
    return f'''<g class="anno" transform="translate({x},{y})">
      <path d="M 0,-40 L 13,24 L 0,13 L -13,24 Z" fill="#000"/>
      <text x="0" y="50" class="tick" text-anchor="middle">N</text>
    </g>'''

CSS = f"""
    text {{ font-family:'Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif; fill:#000 }}
    .pad,.coping,.floor,.thin,.joint,.obj,.bank,.step,.dark,.offpad {{
      fill:#fff; stroke:#000; stroke-linejoin:round; stroke-linecap:round }}
    .thin,.step,.floor,.coping {{ fill:none }}
    .joint {{ fill:none; stroke:#000; stroke-width:2; stroke-dasharray:{w(14)} {w(9)} }}
    .pad  {{ fill:#fff }}
    .bank {{ fill:url(#hatch) }}
    .dark {{ fill:url(#hatch) }}
    .offpad {{ fill:none; stroke-dasharray:{w(11)} {w(8)} }}
    .title {{ font-size:26px; letter-spacing:4.5px; font-weight:700 }}
    .sub   {{ font-size:15px; letter-spacing:2.6px; fill:#000 }}
    .tick  {{ font-size:15px; letter-spacing:1.6px }}
    .note  {{ font-size:12.5px; letter-spacing:1.4px }}
    .grid line {{ stroke:#000; stroke-width:0.6; opacity:0.22 }}
"""

DEFS = """
  <defs>
    <pattern id="hatch" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)">
      <rect width="10" height="10" fill="#fff"/>
      <line x1="0" y1="0" x2="0" y2="10" stroke="#000" stroke-width="2.2"/>
    </pattern>
  </defs>
"""

def grid_layer():
    """5 m grid across the drawing area, in canvas coords."""
    step = 5 * PX_PER_M
    o = ['<g class="grid">']
    x = MARGIN_X
    while x <= W - MARGIN_X + 0.5:
        o.append(f'<line x1="{x:.2f}" y1="{TOP-30:.1f}" x2="{x:.2f}" y2="{TOP+PARK_H+30:.1f}"/>')
        x += step
    y = TOP
    while y <= TOP + PARK_H + 0.5:
        o.append(f'<line x1="{MARGIN_X}" y1="{y:.2f}" x2="{W-MARGIN_X}" y2="{y:.2f}"/>')
        y += step
    o.append('</g>')
    return "\n    ".join(o)


def svg(transparent=False, annotate=True, grid=False):
    bg = '' if transparent else f'<rect width="{W}" height="{H}" fill="#fff"/>'
    anno = ''
    if annotate:
        anno = f'''
    <text x="{MARGIN_X}" y="132" class="title">VEGA BAJA SKATE PARK</text>
    <text x="{MARGIN_X}" y="160" class="sub">OVERHEAD LAYOUT BASE &#183; NORTH UP</text>
    {scalebar(MARGIN_X, 936)}
    {northarrow(W-MARGIN_X, 930)}'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}">
  <title>Vega Baja Skate Park - overhead layout plate</title>
  <style>{CSS}</style>{DEFS}
  {bg}
  {grid_layer() if grid else ''}
  <g id="park" transform="{TX}">
      {park()}
  </g>{anno}
</svg>
'''

if __name__ == "__main__":
    import sys, cairosvg, os
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    jobs = [
        ('vega-baja-skatepark-overhead.svg',            dict(transparent=False, annotate=True)),
        ('vega-baja-skatepark-overhead-clean.svg',      dict(transparent=False, annotate=False)),
        ('vega-baja-skatepark-overhead-alpha.svg',      dict(transparent=True,  annotate=False)),
        ('vega-baja-skatepark-overhead-grid.svg',       dict(transparent=False, annotate=True, grid=True)),
    ]
    for name, kw in jobs:
        p = os.path.join(out, name)
        open(p, 'w').write(svg(**kw))
        png = p.replace('.svg', '.png')
        cairosvg.svg2png(url=p, write_to=png, output_width=3840, output_height=2160,
                         background_color=None if kw.get('transparent') else '#ffffff')
        print('wrote', p, '+', png)
    print(f'scale: {PX_PER_M:.2f} canvas px per metre (at {PAD_LEN_M} m pad length)')
