# Vega Baja Skate Park — overhead layout base

Black-and-white overhead plate for production layouts. 16:9, white background,
black linework, wide margins for callouts and text. **All units are feet.**

## Files

| File | Contents |
|---|---|
| `vega-baja-skatepark-overhead` | Park + Cam A/B/C + legend, scale, north |
| `vega-baja-skatepark-overhead-layout2` | The above + band in Layout 2 / semi-circle |
| `vega-baja-skatepark-overhead-clean` | Park artwork only |
| `vega-baja-skatepark-overhead-alpha` | Park artwork only, transparent background |
| `vega-baja-skatepark-overhead-grid` | Main plate + 20 ft grid |

Each exists as `.svg` (1920×1080 user units, scales losslessly — Illustrator,
Affinity) and `.png` (3840×2160 — Resolve, Premiere, AE).

Drawing area is inset 290 px left/right, 140 top. The bottom ~400 px carries the
camera row, the band key and the scale bar.

## Scale — confirmed

**Pad is 202.8 ft × 81.0 ft.** 1 ft = 6.608 px on the 1920×1080 canvas.

Derived, not assumed: the Google Maps scale bar gives 10.15 px/m in that
screenshot (the 50 ft bar at 155 px and the 20 m bar at 203 px agree to 0.2%),
and that frame matches the trace frame at 0.4950 by template correlation 0.984,
so the trace frame is 6.250 px/ft. Everything was measured there, converted,
and rounded to 0.5 ft. North is up.

## Cameras

All three sit south of the pad, shooting north, on one line 28 ft south of the
pad's south edge.

| | Lens | Covers | Position (ft) | Throw |
|---|---|---|---|---|
| **A** | 35 mm | Band wide, centre | 137.75, 109.0 | 35 ft |
| **B** | 70–200 mm | Close / vocals | 152.5, 109.0 | 37 ft |
| **C** | 70–200 mm | Close / instruments | 121.0, 109.0 | 42 ft |

**Cam A is centred on the box and the long rail** — all three share x = 137.75 ft.

Cam A's distance is not arbitrary: 35 mm on full frame is a 54.4° horizontal
field, so covering the ~36 ft band width needs 35 ft of throw. That puts Cam A
about 28 ft south of the concrete, out on the apron. If you shoot Super 35 the
same framing needs ~48 ft, which is into the road — worth checking before the
day.

B sits right of A and C left of A, both cross-shooting. **C's position is my
call** — you specified B's side but not C's; left of A gives cross coverage of
the drums and the right-hand players. Say the word if you want it elsewhere.

FOV cones are drawn at each lens's wide end on full frame (35 mm → 54.4°,
70 mm → 28.8°).

## Band — Layout 2

Indicative, not surveyed: a shallow semi-circle on the pad south of the long
rail, keyed 1–4. Move freely; the icons are a symbol in the SVG `<defs>`.

## Element schedule

Origin at the north-west corner of the pad bounding box, +x east, +y south.
No two objects overlap — `final.py` asserts it at build.

| Element | x, y | size |
|---|---|---|
| North bank + deck | 105.0, 1.5 | 31.0 × 7.5 |
| Long ledge, N–S | 100.0, 24.5 | 5.0 × 33.0 |
| Flat rail, N–S | 117.5, 28.0 | 3.0 × 30.5 |
| Raised platform | 131.0, 39.5 | 15.5 × 18.0 |
| Triangular ledge | 131.0, 58.0 | 15.5 × 4.0 |
| Box / manny pad | 127.0, 65.0 | 21.5 × 5.0 |
| Long flat rail, E–W | 123.75, 70.5 | 28.0 |
| Edge, E–W | 149.5, 27.0 | 14.5 × 2.5 |
| Upright, N-E | 156.5, 16.5 | 4.0 × 10.5 |
| Long ledge, east | 164.0, 28.5 | 6.5 × 27.0 |
| East bars (×2) | 160.5 / 166.5, 56.5 | 3.5 / 4.0 × 18.0 |
| East pad | 171.5, 59.0 | 8.0 × 11.5 |
| North-east slab | 184.5, 17.0 | 17.0 × 10.5 |
| Roofed shelter | 174.0, 36.0 | 21.5 × 19.0 |
| Bowl, coping | — | 46.8 × 33.0 overall |

## Registration

`_trace-verification.png` renders the plan back into the satellite frame over
the source image.

**One deliberate departure:** the long E–W rail is now centred on the box, per
your note. It therefore no longer sits on the dark band I originally traced it
from, about 22 ft further west. Either that band is a seam or shadow rather than
the rail, or the rail has moved since the imagery. Everything else still
registers.

## Still uncertain

- Obstacle **heights and transitions** are invisible from overhead and are not
  drawn. If you want them, a numbered key is the way, not plan linework.
- The wedge's high end is set east, read off the yellow "?" cap in your photo.
- The dashed rectangle south-west of the plaza is a separate reddish object on
  dirt, off the concrete. Still unidentified.
- The north-east corner sits under the map label in the source and is interpolated.
- Not drawn: fencing, lighting, trees, parking, the road along the south edge.

## Regenerating

```sh
pip install opencv-python-headless numpy pillow cairosvg
python3 final.py <output-dir>     # build all five variants
python3 verify.py                 # registration check against the satellite
```

- `geom.py` — plan geometry, cameras and band positions, all in feet
- `final.py` — canvas layout, icons, drawing conventions, export, assertions
- `verify.py` — registration check
