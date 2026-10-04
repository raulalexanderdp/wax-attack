"""Vega Baja Skate Park - plan geometry.

Project : CORRE FORREST! - Vega Baja Skate Park
Shoot   : 26 October 2026


Authored in FEET, origin at the north-west corner of the concrete pad bounding
box, +x east, +y south.

Scale is fixed, not assumed: the Google Maps scale bar in the reference
screenshot gives 10.15 px/m there (the 50 ft and 20 m bars agree to 0.2%), and
that frame matches the trace frame at 0.4950 by template correlation 0.984, so
the trace frame is 20.505 px/m = 6.250 px/ft. Everything below was measured in
that frame, converted, and rounded to 0.5 ft.
"""

PAD_L = 202.8        # overall pad length, east-west   (measured)
PAD_D = 81.0         # overall pad depth,  north-south (measured)

# ---------------------------------------------------------------- pad outline
PAD = """M 0.0,22.1
 C 0.0,15.6 1.3,10.7 3.6,8.5
 C 7.2,4.3 15.1,2.0 25.4,1.6
 L 134.5,1.6
 L 146.0,6.6 L 155.8,15.6
 L 202.6,14.8 L 202.6,28.7 L 196.0,29.5 L 196.0,36.1
 L 173.9,36.1 L 173.9,55.8
 L 183.7,59.1 L 183.7,67.3 L 179.6,71.4 L 179.6,79.6
 L 102.5,80.4 L 100.9,68.9
 L 93.5,68.9 L 93.5,57.4 L 100.9,57.4
 L 100.9,39.4
 L 32.8,43.5
 C 21.3,46.3 10.7,44.3 4.6,39.7
 C 1.3,36.1 0.0,29.2 0.0,22.1 Z"""

# ----------------------------------------------------------------------- bowl
BOWL_COPING = """M 13.9,5.7
 L 49.2,5.7 A 3.3,3.3 0 0 1 52.5,9.0
 L 52.5,30.3 A 3.3,3.3 0 0 1 49.2,33.6
 L 27.9,33.6
 C 26.2,37.1 23.0,38.7 18.9,38.7
 C 13.5,38.7 7.7,35.3 6.1,30.2
 L 5.7,27.9 L 5.7,13.9
 A 8.2,8.2 0 0 1 13.9,5.7 Z"""

BOWL_FLOOR = """M 18.4,10.7
 L 44.3,10.7 A 3.3,3.3 0 0 1 47.6,13.9
 L 47.6,25.4 A 3.3,3.3 0 0 1 44.3,28.7
 L 27.2,28.7
 C 25.8,31.8 22.8,33.8 19.0,33.8
 C 14.6,33.8 12.0,30.7 10.8,26.6
 L 10.7,18.4
 A 7.7,7.7 0 0 1 18.4,10.7 Z"""

# -------------------------------------------------------------------- objects
# kind: ledge | rail | bank | box | wedge | slab | shelter
BOX_X, BOX_W = 127.0, 21.5                 # the box the rail must centre on
BOX_CX = BOX_X + BOX_W/2                   # 137.75 ft - rail and Cam A share this
RAIL_W = 28.0

# x, y, w, h, kind, label, key number, key marker (ft), confirmed-on-the-ground
OBJECTS = [
    (105.0,  1.5, 31.0,  7.5, 'bank',   'NORTH BANK + DECK',    5, (120.5, 13.0), True),
    (100.0, 24.5,  5.0, 33.0, 'ledge',  'LONG LEDGE, N-S',      3, ( 95.0, 30.0), False),
    (117.5, 28.0,  3.0, 30.5, 'rail',   'FLAT RAIL, N-S',       6, (112.5, 32.0), False),
    (131.0, 39.5, 15.5, 18.0, 'slab',   'RAISED PLATFORM',      9, (138.8, 48.5), False),
    (131.0, 58.0, 15.5,  4.0, 'wedge',  'TRIANGULAR LEDGE',    10, (126.5, 60.0), True),
    (BOX_X, 65.0, BOX_W, 5.0, 'box',    'BOX / MANNY PAD',      8, (122.0, 62.0), True),
    (BOX_CX - RAIL_W/2, 70.5, RAIL_W, 0.5, 'rail',
                                        'LONG FLAT RAIL, E-W',  7, (117.0, 70.8), True),
    (149.5, 27.0, 14.5,  2.5, 'ledge',  'EDGE, E-W',           11, (156.8, 32.5), False),
    (156.5, 16.5,  4.0, 10.5, 'ledge',  'UPRIGHT',             12, (151.5, 19.5), False),
    (164.0, 28.5,  6.5, 27.0, 'ledge',  'LONG LEDGE, EAST',    14, (167.3, 24.5), False),
    (160.5, 56.5,  3.5, 18.0, 'ledge',  'EAST BARS',           13, (157.0, 62.0), False),
    (166.5, 56.5,  4.0, 18.0, 'ledge',  '',                     0, None,          False),
    (171.5, 59.0,  8.0, 11.5, 'slab',   'EAST PAD',            15, (175.5, 75.0), False),
    (184.5, 17.0, 17.0, 10.5, 'slab',   'NORTH-EAST SLAB',     17, (193.0, 31.0), False),
    (174.0, 36.0, 21.5, 19.0, 'shelter','ROOFED SHELTER',      16, (184.8, 45.5), True),
]

# Keyed items that are not plain rectangles
EXTRA_KEYS = [
    (1,  'BOWL',            (29.0, 19.5), True),
    (2,  'OFF-PAD OBJECT',  (67.3, 65.0), False),
    (4,  'DRAIN',           ( 97.0, 62.5), True),
]

DRAIN  = (104.0, 62.5, 1.25)
JOINT  = [((61.5, 2.0), (61.5, 40.5))]
OFFPAD = (46.0, 69.0, 42.5, 6.5)
WEDGE_HIGH_END = 'east'

# ------------------------------------------------------------------- staging
# Band, "Layout 2 / semi-circle". Indicative - not surveyed.
BAND_NAME = 'CORRE FORREST!'
BAND = [
    (122.0, 75.5,  18, 'GTR',       1),
    (135.5, 76.5,   0, 'VOX / GTR', 0),
    (144.0, 74.5,  -8, 'DRUMS',     1),
    (153.0, 75.5, -18, 'BASS',      0),
]
PERF_AREA = (114.0, 71.8, 46.0, 8.2)

# Cameras: x, y, label, lens, horizontal FOV at the wide end (full frame),
# target point, and which side the label sits.
CAM_Y = 109.0
CAMERAS = [
    (BOX_CX,        CAM_Y, 'A', '35 MM',     54.4, (BOX_CX, 74.0), 'BAND WIDE / CENTRE'),
    (BOX_CX + 14.75, CAM_Y, 'B', '70-200 MM', 28.8, (135.5, 76.5), 'CLOSE / VOCALS'),
    (BOX_CX - 16.75, CAM_Y, 'C', '70-200 MM', 28.8, (144.0, 74.5), 'CLOSE / INSTRUMENTS'),
]

# --------------------------------------------------------------------- sheet
PROJECT   = 'VEGA BAJA SKATE PARK'
SUBTITLE  = 'OVERHEAD LAYOUT BASE \u00b7 NORTH UP'
SHOOT     = '26 OCT 2026'
REV       = 'REV 3 \u00b7 04 OCT 2026'
SITE      = '18.445\u00b0N 66.388\u00b0W \u00b7 AST (UTC-4)'
