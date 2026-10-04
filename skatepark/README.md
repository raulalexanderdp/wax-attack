# Vega Baja Skate Park — overhead layout sheet

**CORRE FORREST! · shoot 26 Oct 2026 · Rev 3**

Black-and-white overhead sheet for production layouts. 16:9, white ground,
black linework, wide margins. **All units are feet.**

## Files

| File | Contents |
|---|---|
| `vega-baja-skatepark-overhead` | Park + numbered key + Cam A/B/C + sun dial + title block |
| `vega-baja-skatepark-overhead-layout2` | The above + band in Layout 2 / semi-circle |
| `vega-baja-skatepark-overhead-clean` | Park artwork only, no key or annotation |
| `vega-baja-skatepark-overhead-alpha` | Park artwork only, transparent background |
| `vega-baja-skatepark-overhead-grid` | Full sheet + 20 ft grid |

Each is `.svg` (1920×1080, scales losslessly) and `.png` (3840×2160). The SVG is
split into named groups — `park`, `keys`, `band`, `cameras`, `annotation` — so
you can toggle them in Illustrator instead of asking for another variant.

## Scale

**Pad is 202.8 ft × 81.0 ft.** 1 ft = 6.608 px on the 1920×1080 canvas.

Measured, not assumed: the Google Maps scale bar gives 10.15 px/m (the 50 ft and
20 m bars agree to 0.2%), and that frame matches the trace frame at 0.4950 by
template correlation 0.984, so the trace frame is 6.250 px/ft. North is up.

## Sun — 26 October 2026, Vega Baja (18.445°N 66.388°W, AST)

Computed with the NOAA solar-position algorithm (`sun.py`), not traced off a
screenshot. Puerto Rico has no DST.

**Sunrise 06:23 · solar noon 12:09 at 59.0° due south · sunset 17:56.**
Declination −12.60°.

| Time | Azimuth | Altitude | Relative to Cam A (facing north) |
|---|---|---|---|
| 07:00 | 106° ESE | 8° | camera left, low |
| 09:00 | 120° ESE | 34° | camera left |
| 10:30 | 140° SE | 50° | swings behind camera |
| 12:09 | 180° S | 59° | **directly behind camera, high** |
| 14:00 | 223° SW | 49° | behind camera |
| 15:30 | 242° WSW | 32° | camera right |
| 16:00 | 246° WSW | 25° | camera right, raking |
| 17:00 | 252° WSW | 12° | camera right, very low |

**The band faces south and Cam A shoots north, so the sun is behind the camera
for most of the middle of the day.** From roughly 10:30 to 14:00 it sits behind
Cam A at 50–59° altitude: flat frontal light straight down onto the players.
Everyone in the reference photo is wearing a cap, and at that altitude a brim
puts the eyes in black shadow. Avoid that window for anything on faces.

**Best window is about 15:30–17:00**, sun in the WSW at 32° down to 12°. That
rakes across the band from camera right, models faces, and lights the north bank
behind them instead of leaving it flat.

One thing to check on a scout: there are large trees west and north-west of the
plaza. At 12–25° altitude they will throw long shadows east across the
performance area, which could eat the back half of that window. I can't measure
tree height from imagery.

**Your screenshot is rotated 180°** (north is down, east is left) relative to
this sheet. I didn't trace angles off it, but it does independently agree with
the computed values — the sunrise arrows point WNW, matching azimuth 103.5°.

## Cameras

All three sit south of the pad on one line, 28 ft south of the concrete, facing
north. Icons are at half the previous size.

| | Lens | Covers | Position (ft) | Throw |
|---|---|---|---|---|
| **A** | 35 mm | Band wide, centre | 137.75, 109.0 | 35 ft |
| **B** | 70–200 mm | Close / vocals | 152.5, 109.0 | 37 ft |
| **C** | 70–200 mm | Close / instruments | 121.0, 109.0 | 42 ft |

Cam A, the box and the long E–W rail all share x = 137.75 ft; the build asserts
it. Cam A's 35 ft throw is derived, not placed by eye — 35 mm on full frame is a
54.4° horizontal field, so covering the ~36 ft band width needs 35 ft. On Super
35 the same framing needs ~48 ft, which is into the road. FOV cones are drawn at
each lens's wide end on full frame.

C's side is my assumption; you specified B's only.

## Key

Seventeen items, numbered west to east, marked on the plan and listed on the
sheet. Items marked **\*** have a measured footprint but an unconfirmed type —
I can place them but can't tell you what they are from overhead.

1 Bowl · 2 Off-pad object\* · 3 Long ledge N–S\* · 4 Drain · 5 North bank + deck ·
6 Flat rail N–S\* · 7 Long flat rail E–W · 8 Box / manny pad · 9 Raised platform\* ·
10 Triangular ledge · 11 Edge E–W\* · 12 Upright\* · 13 East bars\* ·
14 Long ledge east\* · 15 East pad\* · 16 Roofed shelter · 17 North-east slab\*

**No heights are surveyed.** Until they are, this sheet answers where things are,
not what a camera can see over them.

## Element schedule

Origin at the north-west corner of the pad bounding box, +x east, +y south.
No two objects overlap — `final.py` asserts it at build.

| # | Element | x, y | size |
|---|---|---|---|
| 5 | North bank + deck | 105.0, 1.5 | 31.0 × 7.5 |
| 3 | Long ledge, N–S | 100.0, 24.5 | 5.0 × 33.0 |
| 6 | Flat rail, N–S | 117.5, 28.0 | 3.0 × 30.5 |
| 9 | Raised platform | 131.0, 39.5 | 15.5 × 18.0 |
| 10 | Triangular ledge | 131.0, 58.0 | 15.5 × 4.0 |
| 8 | Box / manny pad | 127.0, 65.0 | 21.5 × 5.0 |
| 7 | Long flat rail, E–W | 123.75, 70.5 | 28.0 |
| 11 | Edge, E–W | 149.5, 27.0 | 14.5 × 2.5 |
| 12 | Upright | 156.5, 16.5 | 4.0 × 10.5 |
| 14 | Long ledge, east | 164.0, 28.5 | 6.5 × 27.0 |
| 13 | East bars (×2) | 160.5 / 166.5, 56.5 | 3.5 / 4.0 × 18.0 |
| 15 | East pad | 171.5, 59.0 | 8.0 × 11.5 |
| 17 | North-east slab | 184.5, 17.0 | 17.0 × 10.5 |
| 16 | Roofed shelter | 174.0, 36.0 | 21.5 × 19.0 |
| 1 | Bowl, coping | — | 46.8 × 33.0 overall |

## Registration

`_trace-verification.png` renders the plan back into the satellite frame over
the source image.

One deliberate departure: the long E–W rail is centred on the box per your note,
which puts it about 22 ft east of the dark band it was originally traced from.
Either that band is a seam or shadow, or the rail has moved since the imagery.

## Still open

- **Heights.** The one thing that would most improve this sheet.
- Nine of seventeen elements have an unconfirmed type.
- The wedge's high end is set east, read off the yellow "?" cap in your photo.
- The north-east corner is interpolated — it sits under the map label in the source.
- Not drawn: fencing, lighting, trees, parking, the road along the south edge.
- Band positions are indicative, not surveyed.

## Regenerating

```sh
pip install opencv-python-headless numpy pillow cairosvg
python3 final.py <output-dir>     # build all five variants
python3 sun.py                    # print the solar table
python3 verify.py                 # registration check against the satellite
```

- `geom.py` — plan geometry, key numbers, cameras, band, sheet metadata (feet)
- `final.py` — canvas layout, icons, drawing conventions, export, assertions
- `sun.py` — NOAA solar position for the site and date
- `verify.py` — registration check
