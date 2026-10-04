# Vega Baja Skate Park — overhead layout base

Black-and-white overhead plate for production layouts. 16:9, white background,
black linework, generous margins on all four sides for callouts, pins and text.

## Files

| File | Use |
|---|---|
| `vega-baja-skatepark-overhead.svg/.png` | Main plate — title, scale bar, north arrow |
| `vega-baja-skatepark-overhead-clean.svg/.png` | Artwork only, no title/scale/north |
| `vega-baja-skatepark-overhead-alpha.svg/.png` | Transparent background, for compositing |
| `vega-baja-skatepark-overhead-grid.svg/.png` | Main plate + 5 m grid |

PNGs are 3840×2160. SVGs are 1920×1080 user units and scale losslessly —
use the SVG in Illustrator/Affinity, the PNG in Resolve/Premiere/AE.

Drawing area is inset 190 px left/right, 215 px top and 250 px bottom
(at 1920×1080), so there is clear room on every side.

## Scale — NOT YET CONFIRMED

The scale bar assumes the concrete pad is **60 m end to end**. That number is an
estimate from the satellite proportions; nothing in the source image fixes it.

To lock it: measure any one known dimension on site (easiest is the overall
length of the pad, or the long axis of the bowl) and change `PAD_LEN_M` in
`final.py`, then re-run. Everything else rescales from that one constant.

At the current assumption: 1 m = 25.67 px on the 1920×1080 canvas.

## Orientation

North is up, inherited from the Google Maps screenshot. Confirm before relying
on it for sun position or shot direction.

## What is drawn, and how certain it is

Traced from a ~1570 px satellite screenshot, so feature edges are good to
roughly ±1–2 m at the assumed scale. `_trace-verification.png` shows the
linework overlaid on the source so you can judge the fit yourself.

**High confidence** — measured off brightness profiles at the edges:
- Overall concrete footprint, including the west bowl deck, the central plaza
  and the eastern arm
- The bowl: coping outline and flat bottom
- The hatched block on the east side (a distinctly dark surface — shade
  structure, roof or dark-surfaced ramp; type unknown)
- The dashed rectangle south-west of the plaza: a separate reddish object
  sitting on dirt, off the concrete. Included because it occupies space, but
  what it is is unknown
- Step/stair bands in the south of the plaza
- The small square pad with a drain, west of the plaza

**Lower confidence** — readable as masses but the obstacle *type* is not
resolvable at this image resolution:
- Individual ledges, rails, banks and boxes in the plaza are drawn as outlines
  at their observed footprint. Heights, transitions and whether something is a
  ledge vs a rail vs a bank cannot be told from overhead
- Anything under the "Vega Baja Skate Park" map label (upper right) is partly
  obscured; the north-east edge there is interpolated

**Not drawn:** fencing, lighting, trees, parking, the road along the south
edge, and any feature below satellite resolution.

A site photo set or a ground measurement would upgrade the plaza obstacles
from "mass in the right place" to "correct feature."

## Regenerating

```sh
pip install opencv-python-headless numpy pillow cairosvg
python3 final.py <output-dir>
```

- `geom.py` — all plan geometry, in source-satellite pixel coordinates
- `final.py` — canvas layout, styling, scale bar, export
- `build.py` — renders the linework over the source satellite for verification
