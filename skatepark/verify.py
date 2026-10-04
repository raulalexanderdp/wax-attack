"""Render the plan back into the satellite frame to confirm registration.
Trace frame is 20.505 px/m = 6.2500 px/ft, pad origin at (25, 76) px."""
import geom as G, final as F, cairosvg
from PIL import Image
PX_PER_FT, U0, V0 = 6.2500, 25, 76
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1567" height="642" viewBox="0 0 1567 642">
<style>{F.CSS}
 .pad,.coping,.floor,.thin,.joint,.obj,.rail,.shelter,.offpad{{stroke:#ff1744;fill:none}}
</style>
<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="2.0" height="2.0" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="2.0" stroke="#ff1744" stroke-width="0.42"/></pattern></defs>
<g transform="translate({U0},{V0}) scale({PX_PER_FT})">{F.park()}</g></svg>'''
open('verify.svg','w').write(svg)
cairosvg.svg2png(url='verify.svg', write_to='verify.png', output_width=1567, output_height=642)
b = Image.open('/root/.claude/uploads/67a85adb-e901-5ab7-ad58-b6a573ad9b24/46e85240-image.jpg').convert('RGBA')
Image.alpha_composite(b, Image.open('verify.png').convert('RGBA')).convert('RGB').save('verify_overlay.png')
print('ok')
