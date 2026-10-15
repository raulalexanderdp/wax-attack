"""Can a 20x20 diffusion frame, kept out of a 35mm wide, cover the band?

Plan geometry: camera looks up the page (332 deg true). In the afternoon the sun
sits 86-109 deg to camera LEFT, i.e. close to a pure 90 deg side light, so the
sun's rays run essentially across frame, left to right.

Vertical frame, bottom rail at B, top rail at T = B + L.
A point at lateral distance d from the frame, height y, is shaded iff
    B <= y + d*tan(theta) <= T
Full-body shade on a performer of height h at distance d needs
    T >= h + d*tan(theta)      (sun over the top rail)
    B <= d*tan(theta)          (sun under the bottom rail)

Across a band of width W, worst case is the FAR performer for the top rail and
the NEAR performer for the bottom. Setting B to its best value, g*tan(theta),
the gap g to keep the frame out of shot cancels completely:

    L >= h + W*tan(theta)      =>   tan(theta) <= (L - h) / W

The out-of-frame distance decides only how high you rig the bottom rail.
"""
import math, sun as SUN

L   = 20.0          # frame height, ft
H_FF, V_FF = 36.0, 24.0          # full-frame sensor, mm
FL  = 35.0          # Cam A lens, mm
CAM_H = 5.0         # lens height, ft

def hfov(fl=FL): return 2*math.degrees(math.atan(H_FF/2/fl))
def vfov(fl=FL): return 2*math.degrees(math.atan(V_FF/2/fl))

def max_altitude(W, h, L=L):
    t = (L - h) / W
    return math.degrees(math.atan(t)) if t > 0 else 0.0

def frame_height_needed(theta, W, h):
    return h + W*math.tan(math.radians(theta))

def time_at_altitude(target, lo=12.0, hi=18.0):
    """Afternoon crossing of a given solar altitude."""
    for _ in range(60):
        mid = (lo+hi)/2
        if SUN.solar(*SUN.DATE, mid)[1] > target: lo = mid
        else: hi = mid
    return (lo+hi)/2

print(f"Cam A: {FL:.0f} mm full frame -> {hfov():.1f} deg horizontal, {vfov():.1f} deg vertical\n")

for W, tag in ((20.0, 'band 20 ft wide (your figure)'), (31.0, 'band 31 ft (as drawn in layout2)')):
    for h in (7.0, 9.0):
        th = max_altitude(W, h)
        t  = time_at_altitude(th)
        note = 'head + hat' if h == 7 else 'head + 2 ft working margin'
        print(f"{tag}, clear to {h:.0f} ft ({note}):")
        print(f"   20 ft frame works only at sun <= {th:4.1f} deg  ->  from {SUN.hm(t)} onward")
    print()

print("What a 20 ft frame actually delivers, hour by hour:\n")
print(f"{'time':>6} {'alt':>6} {'rel':>7} {'frame ht needed':>16} {'20x20':>7} {'shade top at far player':>24}")
for hh in [13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17]:
    az, el, _, _ = SUN.solar(*SUN.DATE, hh)
    rel = SUN.rel_to_camera(az)
    need = frame_height_needed(el, 20.0, 7.0)
    # shade height at the far performer, 20 ft across the band from the near one
    top = L - 20.0*math.tan(math.radians(el))
    ok = 'YES' if need <= L else 'no'
    print(f"{SUN.hm(hh):>6} {el:5.1f}d {rel:+6.1f}d {need:13.1f} ft {ok:>7} {top:19.1f} ft")

print("\nRaked frame (tilted perpendicular to the sun, the best possible case):")
print("   L/cos(theta) >= h + W*tan(theta)")
for th in (40, 45, 50, 51.4, 55):
    lhs = L/math.cos(math.radians(th)); rhs = 7 + 20*math.tan(math.radians(th))
    print(f"   {th:4.1f} deg: reach {lhs:5.1f} ft vs need {rhs:5.1f} ft  {'ok' if lhs>=rhs else 'FAILS'}")

print("\nBut the rake puts it in shot. At 14:00 (sun 48.7 deg), optimal rake = 48.7 deg:")
th = 48.7; Dc = 28.0
g = Dc*math.tan(math.radians(hfov()/2)) - 10.0
B = g*math.tan(math.radians(th))
x_top = L*math.sin(math.radians(th)); y_top = B + L*math.cos(math.radians(th))
top_of_frame = CAM_H + Dc*math.tan(math.radians(vfov()/2))
print(f"   camera {Dc:.0f} ft out, frustum half-width {Dc*math.tan(math.radians(hfov()/2)):.1f} ft, gap to band edge {g:.1f} ft")
print(f"   top rail leans {x_top:.1f} ft toward the band -> {x_top-g:.1f} ft INSIDE the frustum")
print(f"   panel spans {B:.1f} ft to {y_top:.1f} ft; top of frame at that depth is {top_of_frame:.1f} ft")
print(f"   => the panel is in shot between {B:.1f} and {top_of_frame:.1f} ft")

print("\nFalloff across the band from a single 20x20 side source")
print("(Lambertian disc of equal area, R = 11.3 ft; real grid cloth is more forward-throwing, so take this as the pessimistic bound):")
R = math.sqrt(400/math.pi)
for d in (5, 10, 15, 25):
    E = R*R/(R*R + d*d)
    print(f"   {d:2d} ft from the frame: relative level {E:.3f}")
near = R*R/(R*R+25); far = R*R/(R*R+625)
print(f"   near player to far player: {near/far:.1f}x = {math.log2(near/far):.1f} stops")
