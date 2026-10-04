# Vega Baja Skate Park — overhead layout sheet

**CORRE FORREST! · shoot 26 Oct 2026 · Rev 4**

Black-and-white overhead sheet for production layouts. 16:9, white ground,
black linework. All units are feet.

## Files

| File | Contents |
|---|---|
| `vega-baja-skatepark-overhead` | Park + key + Cam A/B/C + sun dial + title block |
| `vega-baja-skatepark-overhead-layout2` | The above + band in Layout 2 / semi-circle |
| `vega-baja-skatepark-overhead-clean` | Park artwork only |
| `vega-baja-skatepark-overhead-alpha` | Park artwork only, transparent background |
| `vega-baja-skatepark-overhead-grid` | Full sheet + 20 ft grid |

Each is `.svg` (1920×1080) and `.png` (3840×2160). The SVG is split into named
groups — `park`, `keys`, `band`, `cameras`, `annotation` — for toggling in
Illustrator.

## Orientation — corrected in Rev 4

**Page up is true bearing 332° (NNW), not north.** The pad's long axis runs at
62° (ENE), bowl at the south-west end.

Measured two ways, both from your north-up Google Maps capture:

1. Rotating the trace frame to match it peaks at **+28.0°** with correlation
   **0.995** (`orient.py`).
2. `minAreaRect` on the isolated slab gives 330.5°.

They agree within 1.5°. A PCA fit gave 340° but is biased by the park's uneven
mass distribution — discarded.

Independent check: that rectangle came out 2.40–2.48 : 1, against the plan's
202.8 × 81.0 ft = 2.504 : 1. The pad dimensions hold.

The plan is still drawn with the pad horizontal, because that is what fits a
16:9 page. The dial carries true north, rotated 28° clockwise off page up.

**Everything that depends on direction changed with it.** Cam A looks up the
page, so it looks at 332°, not 0°.

## Sun — 26 October 2026, Vega Baja (18.445°N 66.388°W, AST)

NOAA solar position (`sun.py`). No DST in Puerto Rico.

**Sunrise 06:23 · solar noon 12:09 at 59.0° due south · sunset 17:56.**

`rel` below is the angle from Cam A's look direction: 0° is straight into the
lens (back light), ±180° is straight behind the camera (flat frontal light on
the band), + is camera right, − is camera left.

| Time | Azimuth | Altitude | rel | Reading |
|---|---|---|---|---|
| 07:00 | 106° | 8° | +134° | behind-right, low |
| 09:00 | 120° | 34° | +148° | behind-right |
| 10:00 | 132° | 46° | +160° | effectively flat frontal |
| 11:00 | 150° | 55° | +178° | **straight behind camera — flattest** |
| 12:00 | 176° | 59° | −157° | flat frontal, very high |
| 13:00 | 203° | 57° | −129° | behind-left |
| 14:00 | 223° | 49° | −109° | camera left |
| 15:30 | 242° | 32° | −90° | **camera left, true 90° side light** |
| 16:00 | 246° | 25° | −86° | camera left, raking |
| 17:00 | 252° | 12° | −80° | camera left, edging to 3/4 back |

**Correction to Rev 3.** Rev 3 said the afternoon rakes from camera *right* and
that the flat moment was solar noon. Both were wrong — they assumed page up was
north. With the real 332° bearing, the afternoon rakes from **camera left**, and
the flattest moment is **about 11:00**, not 12:09.

**Avoid roughly 10:00–12:30.** The sun is within 25° of straight behind Cam A at
46–59° altitude. Flat frontal light from high up; everyone is in caps and the
brims will black out eyes.

**Best 15:30–17:00.** Sun WSW, 32° down to 12°, within a few degrees of true
side light from camera left. 15:30 is a clean 90° side; by 17:00 it has edged
8–10° forward of the camera plane, so it starts giving rim down the band's
right side. That is the most flattering part of the window.

Still to check on a scout: large trees west and north-west will throw long
shadows across the performance area at 12–25° altitude, which could eat the back
of that window. Not measurable from imagery.

## Cameras

All three sit 28 ft south-east of the pad edge on one line, looking up the page
(bearing 332°).

| | Lens | Covers | Position (ft) | Throw |
|---|---|---|---|---|
| **A** | 35 mm | Band wide, centre | 137.75, 109.0 | 35 ft |
| **B** | 70–200 mm | Close / vocals | 152.5, 109.0 | 37 ft |
| **C** | 70–200 mm | Close / instruments | 121.0, 109.0 | 42 ft |

Cam A, the box and the long E–W rail share x = 137.75 ft; the build asserts it.
Cam A's 35 ft throw is derived — 35 mm on full frame is a 54.4° horizontal
field, so covering the ~36 ft band width needs 35 ft. On Super 35 the same
framing needs ~48 ft, which is into the road.

FOV cones are drawn at each lens's wide end on full frame. C's side is an
assumption; you specified B's only.

## Key

Cut to the five things that matter for the shoot:

1 Bowl · 2 Long flat rail, E–W · 3 Box / manny pad · 4 Triangular ledge ·
5 Roofed shelter

Everything else is drawn plain and unlabelled. Removed from the drawing
entirely in Rev 4: off-pad object, drain, north bank + deck, flat rail N–S,
raised platform.

No heights are surveyed.

## Element schedule

Origin at the north-west corner of the pad bounding box, +x along the pad
(bearing 62°), +y across it. No two objects overlap — `final.py` asserts it.

| # | Element | x, y | size |
|---|---|---|---|
| 1 | Bowl, coping | — | 46.8 × 33.0 overall |
| 2 | Long flat rail, E–W | 123.75, 70.5 | 28.0 |
| 3 | Box / manny pad | 127.0, 65.0 | 21.5 × 5.0 |
| 4 | Triangular ledge | 131.0, 58.0 | 15.5 × 4.0 |
| 5 | Roofed shelter | 174.0, 36.0 | 21.5 × 19.0 |
| — | Long ledge | 100.0, 24.5 | 5.0 × 33.0 |
| — | Edge | 149.5, 27.0 | 14.5 × 2.5 |
| — | Upright | 156.5, 16.5 | 4.0 × 10.5 |
| — | Long ledge, east | 164.0, 28.5 | 6.5 × 27.0 |
| — | East bars (×2) | 160.5 / 166.5, 56.5 | 3.5 / 4.0 × 18.0 |
| — | East pad | 171.5, 59.0 | 8.0 × 11.5 |
| — | North-east slab | 184.5, 17.0 | 17.0 × 10.5 |

## Scale

Pad is 202.8 ft × 81.0 ft; 1 ft = 6.608 px on the 1920×1080 canvas. From the
Google Maps scale bar (50 ft and 20 m bars agree to 0.2%), carried into the
trace frame at 6.250 px/ft by template correlation 0.984.

## Registration

`_trace-verification.png` renders the plan back into the satellite frame over
the source image. One deliberate departure: the long E–W rail is centred on the
box per your note, about 22 ft along the pad from the band it was traced from.

## Regenerating

```sh
pip install opencv-python-headless numpy pillow cairosvg
python3 final.py <output-dir>   # build all five variants
python3 sun.py                  # solar table
python3 orient.py               # re-measure page-up bearing
python3 verify.py               # registration check
```

- `geom.py` — geometry, key, cameras, band, orientation, sheet metadata (feet)
- `final.py` — canvas layout, icons, conventions, export, assertions
- `sun.py` — NOAA solar position · `orient.py` — bearing measurement
- `verify.py` — registration check
