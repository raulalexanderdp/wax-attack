import geom as G

def shapes(sw=1.0):
    """SVG body in source-pixel coords. sw = stroke scale divisor."""
    def w(px): return round(px/sw, 2)
    o=[]
    o.append(f'<path class="pad" d="{G.PAD}" stroke-width="{w(4.2)}"/>')
    o.append(f'<path class="coping" d="{G.BOWL_COPING}" stroke-width="{w(3.4)}"/>')
    o.append(f'<path class="floor" d="{G.BOWL_FLOOR}" stroke-width="{w(2.2)}"/>')
    o.append(f'<path class="thin" d="{G.BANK_EDGE}" stroke-width="{w(2.2)}"/>')
    for (a,b),(c,d) in G.JOINTS:
        o.append(f'<line class="thin" x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke-width="{w(2.2)}"/>')
    x,y,ww,hh=G.DARKBOX
    o.append(f'<rect class="dark" x="{x}" y="{y}" width="{ww}" height="{hh}" stroke-width="{w(3.0)}"/>')
    for rx in G.DARK_RIBS:
        o.append(f'<line class="darkrib" x1="{rx}" y1="{y}" x2="{rx}" y2="{y+hh}" stroke-width="{w(2.0)}"/>')
    for x,y,ww,hh,k in G.BOXES:
        cls={'ledge':'obj','bank':'bank','slab':'obj'}[k]
        o.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{ww}" height="{hh}" stroke-width="{w(3.0)}"/>')
    for x,y,ww,hh in G.STEPS:
        o.append(f'<rect class="step" x="{x}" y="{y}" width="{ww}" height="{hh}" stroke-width="{w(2.4)}"/>')
    cx,cy,r=G.DRAIN
    o.append(f'<circle class="obj" cx="{cx}" cy="{cy}" r="{r}" stroke-width="{w(2.4)}"/>')
    x,y,ww,hh=G.OFFPAD
    o.append(f'<rect class="offpad" x="{x}" y="{y}" width="{ww}" height="{hh}" stroke-width="{w(2.6)}"/>')
    return "\n    ".join(o)

CSS = """
    .pad,.coping,.floor,.thin,.obj,.bank,.step,.dark,.darkrib,.offpad{fill:none;stroke:#000;
      stroke-linejoin:round;stroke-linecap:round}
    .pad{stroke:#000}
    .bank{fill:url(#hatch)}
    .dark{fill:url(#hatchD)}
    .offpad{stroke-dasharray:10 7}
    .step{fill:none}
"""
DEFS = """
  <defs>
    <pattern id="hatch" patternUnits="userSpaceOnUse" width="9" height="9" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="9" stroke="#000" stroke-width="1.6"/></pattern>
    <pattern id="hatchD" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="7" stroke="#000" stroke-width="2.6"/></pattern>
  </defs>
"""

def overlay_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1567" height="642" viewBox="0 0 1567 642">
  <style>{CSS}
    .pad,.coping,.floor,.thin,.obj,.bank,.step,.dark,.darkrib,.offpad{{stroke:#ff1744}}
  </style>{DEFS}
  <g>
    {shapes(1.0)}
  </g>
</svg>'''

if __name__=="__main__":
    open('overlay.svg','w').write(overlay_svg())
    import cairosvg
    cairosvg.svg2png(url='overlay.svg', write_to='overlay.png', output_width=1567, output_height=642)
    from PIL import Image
    base=Image.open('/root/.claude/uploads/67a85adb-e901-5ab7-ad58-b6a573ad9b24/46e85240-image.jpg').convert('RGBA')
    ov=Image.open('overlay.png').convert('RGBA')
    Image.alpha_composite(base,ov).convert('RGB').save('check.png')
    print('wrote check.png')
