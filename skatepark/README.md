# Vega Baja Skate Park — overhead layout base

Black-and-white overhead plate for production layouts. 16:9, white background,
black linework, generous margins on all four sides for callouts, pins and text.

## Files

| File | Use |
|---|---|
| `vega-baja-skatepark-overhead.svg/.png` | Main plate — title, scale bar, north arrow, Cam A |
| `vega-baja-skatepark-overhead-clean.svg/.png` | Artwork only |
| `vega-baja-skatepark-overhead-alpha.svg/.png` | Transparent background, for compositing |
| `vega-baja-skatepark-overhead-grid.svg/.png` | Main plate + 5 m grid |

PNGs are 3840×2160. SVGs are 1920×1080 user units and scale losslessly —
SVG for Illustrator/Affinity, PNG for Resolve/Premiere/AE.

Drawing area is inset 190 px left/right, 215 top, 250 bottom at 1920×1080.

## Scale — confirmed

**Pad is 61.8 m × 24.7 m.** 1 m = 24.92 px on the 1920×1080 canvas.

Derived, not assumed:
1. The Google Maps scale bar gives 10.15 px/m in that screenshot — the 50 ft
   bar (155 px) and the 20 m bar (203 px) agree to within 0.2%.
2. That screenshot matches the trace frame at 0.4950 scale (template
   correlation 0.984), so the trace frame is 20.505 px/m.
3. Every dimension below was measured in the trace frame, converted, and
   rounded to 0.25 m.

North is up, inherited from the Google Maps screenshot.

## Element schedule

All sizes in metres, origin at the north-west corner of the pad bounding box,
+x east, +y south. No two objects overlap — `final.py` asserts this at build.

| Element | x, y | size |
|---|---|---|
| North bank + deck | 32.00, 0.50 | 9.50 × 2.25 |
| Long ledge, N–S | 30.50, 7.50 | 1.50 × 10.00 |
| Flat rail, N–S | 35.75, 8.50 | 1.00 × 9.25 |
| Raised platform | 40.00, 12.00 | 4.75 × 5.50 |
| Triangular ledge | 40.00, 17.75 | 4.75 × 1.25 |
| Box / manny pad | 38.75, 19.75 | 6.50 × 1.50 |
| Long flat rail, E–W | 31.25, 21.50 | 8.50 |
| Edge, E–W | 45.50, 8.25 | 4.50 × 0.75 |
| Upright, N-E | 47.75, 5.00 | 1.25 × 3.25 |
| Long ledge, east | 50.00, 8.75 | 2.00 × 8.25 |
| East bars (×2) | 49.00 / 50.75, 17.25 | 1.00 / 1.25 × 5.50 |
| East pad | 52.25, 18.00 | 2.50 × 3.50 |
| North-east slab | 56.25, 5.25 | 5.25 × 3.25 |
| Roofed shelter | 53.00, 11.00 | 6.50 × 5.75 |
| Bowl, coping | — | 14.25 × 10.05 overall |

## What the ground photos confirmed

- The dark rectangle on the east is the **green-roofed shelter**. Drawn hatched.
- The north edge of the plaza is a **bank/quarter-pipe run with a raised deck
  and railing**, not a flat box. Drawn with a transition line along its high edge.
- The centre group is a **long flat rail, a box, and a triangular (wedge) ledge** —
  the rail west and south of the box, the wedge north of it, matching the
  photos. Each is now one clean shape.
- Cam A is marked south of the pad at x ≈ 41 m, looking north up the centre.

## Cleanup applied in this pass

- Rebuilt in metres rather than screen pixels; every dimension rounded to 0.25 m
- Straightened the north pad edge (measured 0.20–0.68 m of wander) to y = 0.50
- Straightened the south edge of the west slab to a single line
- Regularised the bowl: parallel top/bottom edges, equal corner radii, one clean
  deep-end lobe, and a constant 1.5 m transition inset for the floor
- Collapsed each pair of parallel bands in the centre into the single object it
  actually is — the second band of each pair is that object's shadow
- Merged collinear fragments (two N–S ledge segments into one 10 m ledge; two
  north-band fragments into one bank)
- Removed all overlaps; the build fails if any are reintroduced
- Rails now draw as rails (centreline + end posts), banks as banks, the wedge
  with a ridge line, rather than everything being a plain box

Nothing was moved. `_trace-verification.png` shows the cleaned linework
rendered back into the satellite frame, over the source image.

## Still uncertain

- Obstacle **heights and transitions** are invisible from overhead and are not
  drawn. The wedge's high end is set east from photo 5; confirm.
- The dashed rectangle south-west of the plaza is a separate reddish object on
  dirt, off the concrete. Still unidentified.
- The north-east corner sits under the map label in the source and is interpolated.
- Not drawn: fencing, lighting, trees, parking, the road along the south edge.

## Regenerating

```sh
pip install opencv-python-headless numpy pillow cairosvg
python3 final.py <output-dir>     # build the four variants
python3 verify.py                 # re-render over the satellite to check registration
```

- `geom.py` — all plan geometry, in metres
- `final.py` — canvas layout, drawing conventions, export, overlap assertion
- `verify.py` — registration check against the source satellite
