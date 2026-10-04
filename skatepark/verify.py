"""Render the metre-space plan back into the satellite frame to confirm registration."""
import geom as G, final as F, cairosvg
from PIL import Image
P = G.PX_PER_M_TRACE
body = F.park()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1567" height="642" viewBox="0 0 1567 642">
<style>{F.CSS}
 .pad,.coping,.floor,.thin,.joint,.obj,.rail,.shelter,.offpad{{stroke:#ff1744;fill:none}}
</style>
<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="0.42" height="0.42" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="0.42" stroke="#ff1744" stroke-width="0.09"/></pattern></defs>
<g transform="translate({G.U0},{G.V0}) scale({P})">{body}</g></svg>'''
open('verify.svg','w').write(svg)
cairosvg.svg2png(url='verify.svg', write_to='verify.png', output_width=1567, output_height=642)
b = Image.open('/root/.claude/uploads/67a85adb-e901-5ab7-ad58-b6a573ad9b24/46e85240-image.jpg').convert('RGBA')
Image.alpha_composite(b, Image.open('verify.png').convert('RGBA')).convert('RGB').save('verify_overlay.png')
print('ok')
