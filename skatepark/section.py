"""Section through the band, looking along the camera axis. Camera is behind
the page; the sun comes from camera LEFT, so left = frame side, right = far
side of the band. Both axes share one scale so the sun angle reads true."""
import math, sun as SUN, cairosvg

S      = 18.0            # px per foot, SAME on both axes
DMAX, YMAX = 36.0, 26.0
PW, PH = DMAX*S, YMAX*S
L, h, W, GAP = 20.0, 7.0, 20.0, 4.4
PANELS = [(14.0, '2 PM'), (16.0, '4 PM')]
CW, CH = 1560, 840

def panel(ox, oy, hour, label):
    el = SUN.solar(*SUN.DATE, hour)[1]
    t  = math.tan(math.radians(el))
    B  = GAP*t; T = B + L
    d0, d1 = B/t, (T-h)/t                 # fully-shaded span for a person h tall
    X = lambda d: ox + d*S
    Y = lambda y: oy + PH - y*S
    o = []
    o.append(f'<text x="{ox}" y="{oy-34}" class="h1">{label} &#183; SUN {el:.1f}&#176;</text>')
    o.append(f'<text x="{ox}" y="{oy-13}" class="h2">TOP RAIL {T:.0f} FT &#183; BOTTOM RAIL {B:.0f} FT</text>')

    # shaded wedge
    pts = [(0,B),(0,T)]
    if T/t <= DMAX: pts += [(T/t,0)]
    else:           pts += [(DMAX, T-DMAX*t),(DMAX,0)]
    pts += [(d0,0)]
    o.append('<polygon class="shade" points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a,b in pts) + '"/>')

    # sun rays off each rail
    for y0 in (T, B):
        dx = min(DMAX, y0/t)
        o.append(f'<line class="ray" x1="{X(0):.1f}" y1="{Y(y0):.1f}" x2="{X(dx):.1f}" y2="{Y(max(0,y0-dx*t)):.1f}"/>')
    # parallel sun rays above the wedge, to show the angle
    for c in (6, 13, 20):
        d_top = c; y_top = YMAX
        d_end = min(DMAX, d_top + y_top/t)
        y_end = y_top - (d_end - d_top)*t
        o.append(f'<line class="ray2" x1="{X(d_top):.1f}" y1="{Y(y_top):.1f}" '
                 f'x2="{X(d_end):.1f}" y2="{Y(y_end):.1f}"/>')
    # ground
    o.append(f'<line class="ground" x1="{ox}" y1="{Y(0):.1f}" x2="{ox+PW}" y2="{Y(0):.1f}"/>')
    for i in range(0, int(DMAX)*2):
        gx = ox + i*S/2
        o.append(f'<line class="hatch" x1="{gx:.1f}" y1="{Y(0):.1f}" x2="{gx-7:.1f}" y2="{Y(0)+10:.1f}"/>')
    # the frame
    o.append(f'<rect class="frame" x="{X(0)-5:.1f}" y="{Y(T):.1f}" width="10" height="{(T-B)*S:.1f}"/>')
    o.append(f'<line class="stand" x1="{X(0):.1f}" y1="{Y(B):.1f}" x2="{X(0):.1f}" y2="{Y(0):.1f}"/>')
    o.append(f'<text x="{X(0)-20:.1f}" y="{Y((B+T)/2):.1f}" class="lbl" text-anchor="end" '
             f'transform="rotate(-90 {X(0)-20:.1f} {Y((B+T)/2):.1f})">20 x 20 DIFFUSION</text>')
    # the two performers
    for d, who in ((GAP, 'NEAR'), (GAP+W, 'FAR')):
        lit = not (d0 - 1e-6 <= d <= d1 + 1e-6)
        cls = 'sunlit' if lit else 'shaded'
        bw = 1.5*S
        o.append(f'<rect class="{cls}" x="{X(d)-bw/2:.1f}" y="{Y(5.6):.1f}" width="{bw:.1f}" height="{5.6*S:.1f}" rx="6"/>')
        o.append(f'<circle class="{cls}" cx="{X(d):.1f}" cy="{Y(6.3):.1f}" r="{0.7*S:.1f}"/>')
        tag = 'IN SUN' if lit else 'SHADED'
        o.append(f'<text x="{X(d):.1f}" y="{Y(0)+28:.1f}" class="lbl" text-anchor="middle">{who}</text>')
        o.append(f'<text x="{X(d):.1f}" y="{Y(0)+45:.1f}" class="{"warn" if lit else "lbl"}" '
                 f'text-anchor="middle">{tag}</text>')
    # shade-height line at the far player
    top_far = T - (GAP+W)*t
    if top_far > 0:
        o.append(f'<line class="dim" x1="{X(GAP+W)-28:.1f}" y1="{Y(top_far):.1f}" '
                 f'x2="{X(GAP+W)+28:.1f}" y2="{Y(top_far):.1f}"/>')
        o.append(f'<text x="{X(GAP+W)+34:.1f}" y="{Y(top_far)+5:.1f}" class="lbl">SHADE TOP {top_far:.1f} FT</text>')
    # stripe bracket
    by = Y(0) + 78
    o.append(f'<line class="dim" x1="{X(d0):.1f}" y1="{by}" x2="{X(min(d1,DMAX)):.1f}" y2="{by}"/>')
    for dd in (d0, min(d1, DMAX)):
        o.append(f'<line class="dim" x1="{X(dd):.1f}" y1="{by-7}" x2="{X(dd):.1f}" y2="{by+7}"/>')
    o.append(f'<text x="{X((d0+min(d1,DMAX))/2):.1f}" y="{by+20:.1f}" class="lbl" text-anchor="middle">'
             f'SHADE STRIPE {d1-d0:.1f} FT</text>')
    # band bracket
    by2 = by + 50
    o.append(f'<line class="dim2" x1="{X(GAP):.1f}" y1="{by2}" x2="{X(GAP+W):.1f}" y2="{by2}"/>')
    for dd in (GAP, GAP+W):
        o.append(f'<line class="dim2" x1="{X(dd):.1f}" y1="{by2-7}" x2="{X(dd):.1f}" y2="{by2+7}"/>')
    verdict = f'BAND 20 FT &#8212; {min(max(0,min(d1,GAP+W)-max(d0,GAP)),W):.1f} FT COVERED'
    o.append(f'<text x="{X(GAP+W/2):.1f}" y="{by2+21:.1f}" class="{"warn" if d1 < GAP+W else "lbl"}" '
             f'text-anchor="middle">{verdict}</text>')
    return "\n  ".join(o)

body = "\n  ".join(panel(70 + i*(PW+100), 150, hr, lb) for i, (hr, lb) in enumerate(PANELS))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">
<style>
 text {{ font-family:'Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif; fill:#000 }}
 .h1 {{ font-size:21px; font-weight:700; letter-spacing:3px }}
 .h2 {{ font-size:12.5px; letter-spacing:1.6px }}
 .lbl{{ font-size:12.5px; letter-spacing:1.3px }}
 .warn{{ font-size:12.5px; letter-spacing:1.3px; font-weight:700 }}
 .ttl{{ font-size:25px; font-weight:700; letter-spacing:4.5px }}
 .sub{{ font-size:13px; letter-spacing:1.8px }}
 .shade {{ fill:#000; fill-opacity:0.10; stroke:none }}
 .ray   {{ stroke:#000; stroke-width:1.9; stroke-dasharray:9 6 }}
 .ray2  {{ stroke:#000; stroke-width:0.9; stroke-dasharray:4 7; stroke-opacity:0.55 }}
 .ground{{ stroke:#000; stroke-width:2.6 }}
 .hatch {{ stroke:#000; stroke-width:1 }}
 .frame {{ fill:#fff; stroke:#000; stroke-width:2.6 }}
 .stand {{ stroke:#000; stroke-width:1.6; stroke-dasharray:5 5 }}
 .shaded{{ fill:#fff; stroke:#000; stroke-width:2.2 }}
 .sunlit{{ fill:#000; stroke:#000; stroke-width:2.2 }}
 .dim   {{ stroke:#000; stroke-width:1.6 }}
 .dim2  {{ stroke:#000; stroke-width:1.6; stroke-dasharray:7 5 }}
</style>
<rect width="{CW}" height="{CH}" fill="#fff"/>
<text x="70" y="46" class="ttl">WHY THE 20 x 20 RUNS OUT</text>
<text x="70" y="70" class="sub">SECTION LOOKING ALONG THE CAMERA AXIS &#183; SUN FROM CAMERA LEFT &#183; 26 OCT 2026 &#183; BOTH AXES TO SCALE</text>
{body}
<text x="70" y="{CH-20}" class="sub">STRIPE WIDTH = (FRAME HEIGHT &#8722; PERFORMER HEIGHT) &#247; TAN(SUN ALTITUDE). RAIL HEIGHT SLIDES THE STRIPE, IT NEVER WIDENS IT.</text>
</svg>'''
open('section.svg','w').write(svg)
cairosvg.svg2png(url='section.svg', write_to='section.png', output_width=2400, output_height=int(2400*CH/CW))
print('ok')
