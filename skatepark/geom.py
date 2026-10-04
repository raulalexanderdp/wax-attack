"""Vega Baja Skate Park - plan geometry.

Authored in METRES, origin at the north-west corner of the concrete pad
bounding box, +x east, +y south.

Scale is fixed, not assumed: the Google Maps scale bar in the reference
screenshot gives 10.15 px/m there, and that frame matches the trace frame at
0.4950 (template correlation 0.984), so the trace frame is 20.505 px/m.
Everything below was measured in that frame, converted, and rounded to 0.25 m.
"""

PX_PER_M_TRACE = 20.505
U0, V0 = 25, 76                      # trace-frame origin of the metre grid

PAD_L = 61.8                         # overall pad length, east-west  (measured)
PAD_D = 24.7                         # overall pad depth, north-south (measured)

def m(u, v):                         # trace px -> metres, for re-deriving
    return ((u - U0) / PX_PER_M_TRACE, (v - V0) / PX_PER_M_TRACE)

# ---------------------------------------------------------------- pad outline
# North edge straightened to y = 0.5 (measured 0.20-0.68 across its length).
PAD = """M 0.00,6.75
 C 0.00,4.75 0.40,3.25 1.10,2.60
 C 2.20,1.30 4.60,0.60 7.75,0.50
 L 41.00,0.50
 L 44.50,2.00 L 47.50,4.75
 L 61.75,4.50 L 61.75,8.75 L 59.75,9.00 L 59.75,11.00
 L 53.00,11.00 L 53.00,17.00
 L 56.00,18.00 L 56.00,20.50 L 54.75,21.75 L 54.75,24.25
 L 31.25,24.50 L 30.75,21.00
 L 28.50,21.00 L 28.50,17.50 L 30.75,17.50
 L 30.75,12.00
 L 10.00,13.25
 C 6.50,14.10 3.25,13.50 1.40,12.10
 C 0.40,11.00 0.00,8.90 0.00,6.75 Z"""

# ----------------------------------------------------------------------- bowl
# Regularised kidney: straight parallel top/bottom edges, equal east corner
# radii, one clean deep-end lobe at the south-west. Floor is a constant 1.5 m
# inset, i.e. a uniform transition the whole way round.
BOWL_COPING = """M 4.25,1.75
 L 15.00,1.75 A 1.00,1.00 0 0 1 16.00,2.75
 L 16.00,9.25 A 1.00,1.00 0 0 1 15.00,10.25
 L 8.50,10.25
 C 8.00,11.30 7.00,11.80 5.75,11.80
 C 4.10,11.80 2.35,10.75 1.85,9.20
 L 1.75,8.50 L 1.75,4.25
 A 2.50,2.50 0 0 1 4.25,1.75 Z"""

BOWL_FLOOR = """M 5.60,3.25
 L 13.50,3.25 A 1.00,1.00 0 0 1 14.50,4.25
 L 14.50,7.75 A 1.00,1.00 0 0 1 13.50,8.75
 L 8.30,8.75
 C 7.85,9.70 6.95,10.30 5.80,10.30
 C 4.45,10.30 3.65,9.35 3.30,8.10
 L 3.25,5.60
 A 2.35,2.35 0 0 1 5.60,3.25 Z"""

# -------------------------------------------------------------------- objects
# kind: ledge | rail | bank | box | wedge | steps | slab | shelter
# (x, y, w, h, kind, label)
OBJECTS = [
    (32.00,  0.50,  9.50, 2.25, 'bank',   'north bank + deck'),
    (30.50,  7.50,  1.50,10.00, 'ledge',  'long ledge, N-S'),
    (35.75,  8.50,  1.00, 9.25, 'rail',   'flat rail, N-S'),
    (40.00, 12.00,  4.75, 5.50, 'slab',   'raised platform'),
    (40.00, 17.75,  4.75, 1.25, 'wedge',  'triangular ledge'),
    (38.75, 19.75,  6.50, 1.50, 'box',    'box / manny pad'),
    (31.25, 21.50,  8.50, 0.15, 'rail',   'long flat rail, E-W'),
    (45.50,  8.25,  4.50, 0.75, 'ledge',  'edge, E-W'),
    (47.75,  5.00,  1.25, 3.25, 'ledge',  'upright, N-E'),
    (50.00,  8.75,  2.00, 8.25, 'ledge',  'long ledge, east'),
    (49.00, 17.25,  1.00, 5.50, 'ledge',  'east bar'),
    (50.75, 17.25,  1.25, 5.50, 'ledge',  'east bar'),
    (52.25, 18.00,  2.50, 3.50, 'slab',   'east pad'),
    (56.25,  5.25,  5.25, 3.25, 'slab',   'north-east slab'),
    (53.00, 11.00,  6.50, 5.75, 'shelter','roofed shelter'),
]

DRAIN = (31.75, 19.00, 0.40)
JOINT = [((18.75, 0.60), (18.75, 12.35))]      # grade change, bowl deck / flat
OFFPAD = (14.00, 21.00, 13.00, 2.00)           # separate object, off the slab
WEDGE_HIGH_END = 'east'                        # from the ground photos
