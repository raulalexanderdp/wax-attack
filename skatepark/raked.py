import math, sun as SUN
H_PERF, CAM_H = 7.0, 5.0
TAN_H, TAN_V = math.tan(math.radians(27.21)), math.tan(math.radians(18.93))
STAND_CLEAR = 1.0        # ft the frame base sits outside the frustum edge (optimistic)

def works(th, W, fill, phi, L):
    """fill = fraction of frame width the band occupies."""
    t = math.tan(math.radians(th))
    Dc = (W/2/fill)/TAN_H
    X_edge, Y_top = -TAN_H*Dc, CAM_H + TAN_V*Dc
    X0 = X_edge - STAND_CLEAR
    sp, cp = math.sin(math.radians(phi)), math.cos(math.radians(phi))
    x_top = X0 + L*sp
    if x_top <= X_edge: B = 0.0
    else:
        s = (X_edge - X0)/(L*sp) if phi > 0 else 0.0
        B = max(0.0, Y_top - s*L*cp)
    T_eff = B + L*cp + L*sp*t
    d0, d1 = B/t, (T_eff - H_PERF)/t
    d_near, d_far = (-W/2) - X0, (W/2) - X0
    return (d0 <= d_near + 1e-6 and d1 >= d_far - 1e-6), B, B + L*cp, Dc

def max_width(th, fill, L, phis=range(0, 56, 2)):
    best = (0.0, None, None, None)
    for W10 in range(10, 400):
        W = W10/10
        for phi in phis:
            ok, B, top, Dc = works(th, W, fill, phi, L)
            if ok and W > best[0]: best = (W, phi, B, top)
    return best

print("MAX BAND WIDTH A 20x20 CAN COVER ON A WIDE, 26 OCT 2026")
print("(frame raked and lifted as far as it needs to go, still out of shot)\n")
print(f"  {'time':>6} {'sun':>6}   {'band fills 70%':>22}   {'band fills 85%':>22}")
for hh in (14.5, 15.0, 15.5, 16.0, 16.5, 17.0):
    el = SUN.solar(*SUN.DATE, hh)[1]
    row = f"  {SUN.hm(hh):>6} {el:5.1f}d  "
    for fill in (0.70, 0.85):
        W, phi, B, top = max_width(el, fill, 20.0)
        row += f"  {W:5.1f} ft (rake {phi:2.0f}d, rail {B:4.1f}-{top:4.1f} ft)" if W else "   --- "
    print(row)

print("\n\nSAME, FOR A 12x12 - far safer in wind, far easier to fly high\n")
print(f"  {'time':>6} {'sun':>6}   {'band fills 70%':>22}   {'band fills 85%':>22}")
for hh in (14.5, 15.0, 15.5, 16.0):
    el = SUN.solar(*SUN.DATE, hh)[1]
    row = f"  {SUN.hm(hh):>6} {el:5.1f}d  "
    for fill in (0.70, 0.85):
        W, phi, B, top = max_width(el, fill, 12.0)
        row += f"  {W:5.1f} ft (rake {phi:2.0f}d, rail {B:4.1f}-{top:4.1f} ft)" if W else "   --- "
    print(row)

print("\n\nWHEN DOES A FULL 20 FT BAND BECOME COVERABLE BY THE 20x20?")
for fill in (0.70, 0.85):
    lo, hi = 14.0, 18.0
    for _ in range(50):
        mid = (lo+hi)/2
        el = SUN.solar(*SUN.DATE, mid)[1]
        if any(works(el, 20.0, fill, p, 20.0)[0] for p in range(0, 56, 2)): hi = mid
        else: lo = mid
    el = SUN.solar(*SUN.DATE, hi)[1]
    print(f"   band filling {fill*100:.0f}% of frame width:  from {SUN.hm(hi)} (sun {el:.1f} deg)")

print("\n\nWHY THE LIFT BITES: 14:30, 20 ft band, filling 70%, raked 30 deg")
el = SUN.solar(*SUN.DATE, 14.5)[1]; t = math.tan(math.radians(el))
W, fill, phi, L = 20.0, 0.70, 30.0, 20.0
Dc = (W/2/fill)/TAN_H; X_edge = -TAN_H*Dc; Y_top = CAM_H + TAN_V*Dc; X0 = X_edge - 1
sp, cp = math.sin(math.radians(phi)), math.cos(math.radians(phi))
s = (X_edge - X0)/(L*sp); B = Y_top - s*L*cp
d_near = (-W/2) - X0
print(f"   camera {Dc:.1f} ft out, frame edge at {X_edge:.1f} ft off-axis, top of frame {Y_top:.1f} ft")
print(f"   base sits at {X0:.1f} ft off-axis; leaning in, it crosses into shot after {s*L:.1f} ft of panel")
print(f"   so the bottom rail must be at {B:.1f} ft to keep that crossing above frame")
print(f"   sun then passes under the rail for the first {B/t:.1f} ft of run")
print(f"   but the nearest performer is only {d_near:.1f} ft from the base")
print(f"   -> near player lit from the ground to {B - d_near*t:.1f} ft. Fully in sun.")
