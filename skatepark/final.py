#!/usr/bin/env python3
"""Vega Baja Skate Park - 16:9 black & white overhead layout sheet. Units: feet."""
import math, geom as G, sun as SUN

W, H = 1920, 1080
MARGIN_X, TOP = 290, 150
S = (W - 2*MARGIN_X) / G.PAD_L            # canvas px per foot
PARK_H = G.PAD_D * S
TX = f"translate({MARGIN_X},{TOP}) scale({S:.5f})"

CAM_SCALE, BAND_SCALE = 0.5, 0.5
LENS_OFFSET = 46 * CAM_SCALE              # icon origin -> front of lens, canvas px

def w(px): return round(px / S, 4)
def f(v):  return round(v, 3)
def cx(x): return MARGIN_X + x * S
def cy(y): return TOP + y * S

# ----------------------------------------------------------------- park layer
def rect(x, y, ww, hh, cls, sw):
    return f'<rect class="{cls}" x="{f(x)}" y="{f(y)}" width="{f(ww)}" height="{f(hh)}" stroke-width="{w(sw)}"/>'

def draw(o):
    x, y, ww, hh, kind = o[:5]
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
        lo, hi = (x, x+ww) if G.WEDGE_HIGH_END == 'east' else (x+ww, x)
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
    return "\n      ".join(o)

# ------------------------------------------------------------------- the key
def keyed_items():
    return sorted([(o[6], o[5], o[7]) for o in G.OBJECTS if o[6]] + list(G.EXTRA_KEYS))

def disc(x_px, y_px, text, r=9.5, cls='key'):
    return (f'<circle class="{cls}" cx="{x_px:.1f}" cy="{y_px:.1f}" r="{r}"/>'
            f'<text x="{x_px:.1f}" y="{y_px + r*0.46:.1f}" class="keynum" text-anchor="middle">{text}</text>')

def key_markers():
    return "\n    ".join(disc(cx(p[0]), cy(p[1]), n) for n, _l, p in keyed_items() if p)

def keylegend(x, y, step=23):
    o = [f'<g transform="translate({x},{y})">', '<text x="0" y="0" class="sub">KEY</text>']
    for i, (n, label, _p) in enumerate(keyed_items()):
        py = 28 + i*step
        o.append(disc(9, py - 4.5, n, 9.0))
        o.append(f'<text x="26" y="{py}" class="legend">{label}</text>')
    o.append('</g>')
    return "\n    ".join(o)

# ---------------------------------------------------------------------- icons
def _ico(body, k):
    return re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{float(m.group(1))*k:.2f}"', body)
import re

CAM_BODY = '''
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
    <rect x="-12" y="40" width="24" height="8" rx="1.5"/>'''

PERSON_BODY = '''
    <ellipse cx="0" cy="0" rx="30" ry="12" stroke-width="2.8"/>
    <ellipse cx="-21" cy="0" rx="2.6" ry="6" stroke-width="2"/>
    <ellipse cx="21" cy="0" rx="2.6" ry="6" stroke-width="2"/>
    <circle cx="0" cy="-2" r="16" fill="#000" stroke-width="2.4"/>
    <path d="M -15.2,3 A 16,16 0 0 0 15.2,3 Z" fill="#fff" stroke-width="2.4"/>
    <path d="M -5.5,12.5 L 0,19 L 5.5,12.5 Z" fill="#000" stroke-width="2"/>'''

# Stroke widths are pre-multiplied so the icons keep their weight once scaled.
ICONS = (f'<g id="cam" stroke-width="{2.4/CAM_SCALE:.2f}">{_ico(CAM_BODY, 1/CAM_SCALE)}</g>'
         f'<g id="person" stroke-width="{2.4/BAND_SCALE:.2f}">{_ico(PERSON_BODY, 1/BAND_SCALE)}</g>')

def cone(x, y, rot, fov, length):
    h = math.radians(fov/2); a = math.radians(rot)
    ax, ay = cx(x) + math.sin(a)*LENS_OFFSET, cy(y) - math.cos(a)*LENS_OFFSET
    reach = length*S - LENS_OFFSET
    p = [(ax + math.sin(a + s*h)*reach, ay - math.cos(a + s*h)*reach) for s in (-1, 1)]
    return f'<path class="cone" d="M {ax:.1f},{ay:.1f} L {p[0][0]:.1f},{p[0][1]:.1f} L {p[1][0]:.1f},{p[1][1]:.1f} Z"/>'

def cameras():
    o = []
    for x, y, tag, lens, fov, (tx, ty), _role in G.CAMERAS:
        dx, dy = tx - x, ty - y
        rot = math.degrees(math.atan2(dx, -dy))
        o.append(cone(x, y, rot, fov, math.hypot(dx, dy)))
        o.append(f'<g class="icon" transform="translate({cx(x):.1f},{cy(y):.1f}) rotate({rot:.1f}) '
                 f'scale({CAM_SCALE})"><use href="#cam"/></g>')
        o.append(f'<text x="{cx(x):.1f}" y="{cy(y)+42:.1f}" class="camtag" text-anchor="middle">CAM {tag}</text>')
        o.append(f'<text x="{cx(x):.1f}" y="{cy(y)+60:.1f}" class="camlens" text-anchor="middle">{lens}</text>')
    return "\n    ".join(o)

def band():
    x, y, ww, hh = G.PERF_AREA
    base = cy(y + hh) + 16
    o = [f'<rect class="perf" x="{cx(x):.1f}" y="{cy(y):.1f}" width="{ww*S:.1f}" height="{hh*S:.1f}"/>']
    for bx, by, rot, label, row in G.BAND:
        o.append(f'<g class="icon" transform="translate({cx(bx):.1f},{cy(by):.1f}) rotate({rot}) '
                 f'scale({BAND_SCALE})"><use href="#person"/></g>')
        o.append(f'<text x="{cx(bx):.1f}" y="{base + row*16:.1f}" class="bandtag" text-anchor="middle">{label}</text>')
    return "\n    ".join(o)

# -------------------------------------------------------------- sun / compass
def sundial(ox, oy, r=76):
    y_, mo, d = SUN.DATE
    rise, noon = SUN._event(y_, mo, d, True)
    sett, _ = SUN._event(y_, mo, d, False)
    def pt(az, rad):                       # true bearing -> page position
        a = math.radians(az - G.UP_BEARING)
        return ox + math.sin(a)*rad, oy - math.cos(a)*rad
    az_r = SUN.solar(y_, mo, d, rise + 0.05)[0]
    az_s = SUN.solar(y_, mo, d, sett - 0.05)[0]
    o = [f'<g transform="translate(0,0)">',
         f'<circle class="dial" cx="{ox}" cy="{oy}" r="{r}"/>']
    for az in range(0, 360, 15):
        a, b = pt(az, r); c, e = pt(az, r - (9 if az % 90 == 0 else 5))
        o.append(f'<line class="dialtick" x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{e:.1f}"/>')
    # sun's track across the sky, sunrise bearing to sunset bearing
    a0, b0 = pt(az_r, r); a1, b1 = pt(az_s, r)
    o.append(f'<path class="sunarc" d="M {a0:.1f},{b0:.1f} A {r},{r} 0 0 1 {a1:.1f},{b1:.1f}"/>')
    for hh in (8, 10, 12, 14, 16):
        az, el, _, _ = SUN.solar(y_, mo, d, hh)
        a, b = pt(az, r); c, e = pt(az, r + 9); tx_, ty_ = pt(az, r + 25)
        o.append(f'<line class="dialtick" x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{e:.1f}"/>')
        o.append(f'<text x="{tx_:.1f}" y="{ty_+4:.1f}" class="dialnum" text-anchor="middle">{hh:02d}</text>')
    # light direction at the recommended hour: from the sun's bearing in to centre
    az, el, _, _ = SUN.solar(y_, mo, d, 16.0)
    a, b = pt(az, r - 6); c, e = pt(az, 20)
    o.append(f'<line class="sunray" x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{e:.1f}"/>')
    o.append(f'<polygon class="sunhead" points="{c:.1f},{e:.1f} '
             f'{c + math.sin(math.radians(az+150))*13:.1f},{e - math.cos(math.radians(az+150))*13:.1f} '
             f'{c + math.sin(math.radians(az-150))*13:.1f},{e - math.cos(math.radians(az-150))*13:.1f}"/>')
    tip = pt(0, r + 20); mid = pt(0, r + 3)
    na = math.radians(-G.UP_BEARING); px_, py_ = math.cos(na), math.sin(na)
    o.append(f'<path class="narrow" d="M {tip[0]:.1f},{tip[1]:.1f} '
             f'L {mid[0]+px_*8:.1f},{mid[1]+py_*8:.1f} L {mid[0]-px_*8:.1f},{mid[1]-py_*8:.1f} Z"/>')
    lab = pt(0, r + 36)
    o.append(f'<text x="{lab[0]:.1f}" y="{lab[1]+5:.1f}" class="tick" text-anchor="middle">N</text>')
    o.append('</g>')
    return "\n    ".join(o), rise, noon, sett

def rel_to_camera(az):
    """Signed angle from the camera's look direction; + is camera right,
    +/-180 is straight behind the camera (flat frontal light on the band)."""
    return ((az - G.CAM_BEARING + 180) % 360) - 180

def sunnotes(x, y, rise, noon, sett):
    el_noon = SUN.solar(*SUN.DATE, noon)[1]
    az16, el16 = SUN.solar(*SUN.DATE, 16.0)[:2]
    flat = max((h/4 for h in range(4*6, 4*18)),
               key=lambda h: (abs(rel_to_camera(SUN.solar(*SUN.DATE, h)[0])), ))
    lines = [f'SUN &#183; {G.SHOOT}',
             f'HOURS AST &#183; RISE {SUN.hm(rise)} &#183; SET {SUN.hm(sett)}',
             f'NOON {SUN.hm(noon)} &#183; {el_noon:.0f}&#176; DUE SOUTH',
             f'{SUN.hm(flat)} SUN BEHIND CAM A &#8212; FLATTEST',
             f'16:00 &#183; {az16:.0f}&#176; WSW AT {el16:.0f}&#176;',
             'BEST 15:30-17:00,',
             'RAKING FROM CAMERA LEFT']
    o = [f'<g transform="translate({x},{y})">']
    for i, t in enumerate(lines):
        cls = 'sub' if i == 0 else 'note'
        o.append(f'<text x="0" y="{i*17 + (0 if i == 0 else 7)}" class="{cls}">{t}</text>')
    o.append('</g>')
    return "\n    ".join(o)

# ------------------------------------------------------------------ furniture
def titleblock(x, y, show_band=False):
    extra = (f'<text x="0" y="90" class="note">BAND LAYOUT 2 / SEMI-CIRCLE &#183; INDICATIVE, NOT SURVEYED</text>'
             if show_band else '')
    return "\n    ".join([f'<g transform="translate({x},{y})">',
        f'<text x="0" y="0"  class="title">{G.PROJECT}</text>',
        f'<text x="0" y="26" class="sub">{G.SUBTITLE}</text>',
        f'<text x="0" y="50" class="sub">{G.BAND_NAME} &#183; SHOOT {G.SHOOT}</text>',
        f'<text x="0" y="70" class="note">{G.REV}</text>', extra, '</g>'])

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

def camlegend(x, y):
    o = [f'<g transform="translate({x},{y})">', '<text x="0" y="0" class="sub">CAMERAS</text>']
    for i, (_x, _y, tag, lens, _fov, _t, role) in enumerate(G.CAMERAS):
        yy = 26 + i*21
        o.append(f'<text x="0"   y="{yy}" class="legend" font-weight="700">{tag}</text>')
        o.append(f'<text x="22"  y="{yy}" class="legend">{lens}</text>')
        o.append(f'<text x="128" y="{yy}" class="legend">{role}</text>')
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
    .icon    {{ fill:#fff; stroke:#000; stroke-linejoin:round; stroke-linecap:round }}
    .cone    {{ fill:#000; fill-opacity:0.045; stroke:#000; stroke-width:1.0; stroke-opacity:0.55; stroke-dasharray:8 7 }}
    .perf    {{ fill:none; stroke:#000; stroke-width:1.6; stroke-dasharray:9 7 }}
    .key     {{ fill:#000; stroke:#fff; stroke-width:1.6 }}
    .keynum  {{ font-size:11.5px; font-weight:700; fill:#fff; letter-spacing:0 }}
    .dial    {{ fill:#fff; stroke:#000; stroke-width:1.8 }}
    .dialtick{{ stroke:#000; stroke-width:1.4 }}
    .sunarc  {{ fill:none; stroke:#000; stroke-width:5; stroke-linecap:round }}
    .sunray  {{ stroke:#000; stroke-width:3 }}
    .sunhead,.narrow {{ fill:#000 }}
    .dialnum {{ font-size:12px; letter-spacing:0.6px }}
    .title   {{ font-size:26px; letter-spacing:4.5px; font-weight:700 }}
    .sub     {{ font-size:15px; letter-spacing:2.6px }}
    .tick    {{ font-size:15px; letter-spacing:1.6px }}
    .note    {{ font-size:12.5px; letter-spacing:1.4px }}
    .legend  {{ font-size:14px; letter-spacing:1.4px }}
    .camtag  {{ font-size:15px; letter-spacing:2.4px; font-weight:700 }}
    .camlens {{ font-size:12.5px; letter-spacing:1.6px }}
    .bandtag {{ font-size:11.5px; letter-spacing:1.2px }}
    .grid line {{ stroke:#000; stroke-width:0.6; opacity:0.22 }}
"""
DEFS = f"""
  <defs>
    <pattern id="hatch" patternUnits="userSpaceOnUse" width="2.0" height="2.0" patternTransform="rotate(45)">
      <rect width="2.0" height="2.0" fill="#fff"/>
      <line x1="0" y1="0" x2="0" y2="2.0" stroke="#000" stroke-width="0.42"/>
    </pattern>{ICONS}
  </defs>"""

def svg(transparent=False, annotate=True, grid=False, cams=True, show_band=False, keys=True):
    bg = '' if transparent else f'<rect width="{W}" height="{H}" fill="#fff"/>'
    anno = ''
    if annotate:
        dial, rise, noon, sett = sundial(1505, 762, 70)
        anno = f'''
  <g id="annotation">
    {titleblock(MARGIN_X, 58, show_band)}
    {camlegend(W-MARGIN_X-300, 58)}
    {keylegend(MARGIN_X, 742)}
    {scalebar(MARGIN_X, 962)}
    {dial}
    {sunnotes(1362, 902, rise, noon, sett)}
  </g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>{G.PROJECT} - overhead layout, {G.BAND_NAME}, {G.SHOOT}</title>
  <style>{CSS}</style>{DEFS}
  {bg}
  {grid_layer() if grid else ''}
  <g id="park" transform="{TX}">
      {park()}
  </g>
  <g id="keys">{key_markers() if keys else ''}</g>
  <g id="band">{band() if show_band else ''}</g>
  <g id="cameras">{cameras() if cams else ''}</g>{anno}
</svg>
'''

if __name__ == "__main__":
    import sys, os, cairosvg, itertools
    for a, b in itertools.combinations(G.OBJECTS, 2):
        ox = min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0])
        oy = min(a[1]+a[3], b[1]+b[3]) - max(a[1], b[1])
        assert not (ox > 1e-9 and oy > 1e-9), f'overlap: {a[5]} / {b[5]}'
    rail = next(o for o in G.OBJECTS if o[5].startswith('LONG FLAT RAIL'))
    assert abs((rail[0]+rail[2]/2) - G.BOX_CX) < 1e-9
    assert abs(G.CAMERAS[0][0] - G.BOX_CX) < 1e-9
    nums = sorted(n for n, *_ in keyed_items())
    assert nums == list(range(1, len(nums)+1)), nums
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    jobs = [('vega-baja-skatepark-overhead.svg',         dict()),
            ('vega-baja-skatepark-overhead-layout2.svg', dict(show_band=True)),
            ('vega-baja-skatepark-overhead-clean.svg',   dict(annotate=False, cams=False, keys=False)),
            ('vega-baja-skatepark-overhead-alpha.svg',   dict(annotate=False, cams=False, keys=False, transparent=True)),
            ('vega-baja-skatepark-overhead-grid.svg',    dict(grid=True))]
    for name, kw in jobs:
        p = os.path.join(out, name)
        open(p, 'w').write(svg(**kw))
        cairosvg.svg2png(url=p, write_to=p.replace('.svg', '.png'),
                         output_width=3840, output_height=2160,
                         background_color=None if kw.get('transparent') else '#ffffff')
        print('wrote', name)
    print(f'{S:.4f} px/ft; {len(nums)} keyed items; rail/box/camA at {G.BOX_CX} ft')
