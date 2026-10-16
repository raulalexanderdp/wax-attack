"""Is the 20x20 actually riggable at 14:30, or only riggable on paper?

The pure geometry says yes at up to 19.3 ft of band - but only with the frame
raked 30 deg, bottom rail at 7.3 ft and top rail at 24.6 ft, overhanging 10 ft
over the performers. Top corners at 24.6 ft is past any hi-roller (~19.5 ft),
so that answer is a condor, not a grip stand.

Constrain the top rail to 20 ft and the rake to 30 deg - a normal four-stand
hi-roller rig - and the honest number at 14:30 is 13.2 ft against the 13.5 ft
the compressed band needs. It clears 13.5 ft from about 14:50.
"""
import math, sys
sys.path.insert(0, __import__('os').path.dirname(__file__) or '.')
import sun as SUN
CAM_H = 5.0
TAN_H, TAN_V = math.tan(math.radians(27.21)), math.tan(math.radians(18.93))

def works(th, W, fill, phi, L, h_perf, stand_clear):
    t = math.tan(math.radians(th))
    Dc = (W/2/fill)/TAN_H
    X_edge, Y_top = -TAN_H*Dc, CAM_H + TAN_V*Dc
    X0 = X_edge - stand_clear
    sp, cp = math.sin(math.radians(phi)), math.cos(math.radians(phi))
    if X0 + L*sp <= X_edge: B = 0.0
    else:
        s = (X_edge - X0)/(L*sp) if phi > 0 else 0.0
        B = max(0.0, Y_top - s*L*cp)
    T_eff = B + L*cp + L*sp*t
    d0, d1 = B/t, (T_eff - h_perf)/t
    return d0 <= (-W/2 - X0) + 1e-6 and d1 >= (W/2 - X0) - 1e-6

def max_width(th, h_perf, stand_clear, L=20.0, fill=0.70):
    best = 0.0
    for W10 in range(10, 400):
        W = W10/10
        if any(works(th, W, fill, p, L, h_perf, stand_clear) for p in range(0, 40, 2)):
            best = W
    return best

th = SUN.solar(*SUN.DATE, 14.5)[1]
print(f"14:30, sun {th:.1f} deg.  Band needs 13.5 ft covered.\n")
print(f"  {'performer':>10} {'stand clearance':>16} {'max band width':>16}   margin")
for h_perf, hlab in ((7.0, '7 ft'), (8.0, '8 ft, guitar up')):
    for sc, slab in ((1.0, '1 ft (optimistic)'), (4.0, '4 ft (real legs)')):
        W = max_width(th, h_perf, sc)
        m = W - 13.5
        flag = 'OK' if m > 1.5 else ('razor thin' if m > 0 else 'FAILS')
        print(f"  {hlab:>10} {slab:>16} {W:13.1f} ft   {m:+5.1f} ft  {flag}")

print("\n\nWhen does the realistic case (8 ft performer, 4 ft legs) clear 13.5 ft?")
lo, hi = 14.0, 18.0
for _ in range(50):
    mid = (lo+hi)/2
    if max_width(SUN.solar(*SUN.DATE, mid)[1], 8.0, 4.0) >= 13.5: hi = mid
    else: lo = mid
print(f"   from {SUN.hm(hi)}  (sun {SUN.solar(*SUN.DATE, hi)[1]:.1f} deg)")
print(f"   set 1 ends at 15:30, so that is the last {(15.5-hi)*60:.0f} minutes of the set.")
