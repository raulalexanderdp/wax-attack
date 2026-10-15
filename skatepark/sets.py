import math, sun as SUN
L, h = 20.0, 7.0

def stripe(el): return (L - h)/math.tan(math.radians(el))
def airmass(el):
    return 1.0/(math.sin(math.radians(el)) + 0.50572*(el + 6.07995)**-1.6364)
def dni(el):                      # direct normal irradiance, kW/m^2 (Meinel)
    return 1.353 * 0.7**(airmass(el)**0.678) if el > 0 else 0.0

SETS = [('SET 1  band, 4 members', 14.5, 15.5, 20.0),
        ('SET 2  singer + DJ',     16.5, 17.5, 12.0)]

for name, t0, t1, W in SETS:
    print(f"\n{name}   {SUN.hm(t0)}-{SUN.hm(t1)}   subject {W:.0f} ft wide")
    print(f"  {'time':>6} {'alt':>6} {'az':>7} {'rel':>7} {'stripe':>8} {'20x20?':>7} "
          f"{'frame ht needed':>16} {'rel light':>10}")
    ref = dni(SUN.solar(*SUN.DATE, t0)[1])
    for k in range(5):
        hh = t0 + k*(t1-t0)/4
        az, el, _, _ = SUN.solar(*SUN.DATE, hh)
        rel = SUN.rel_to_camera(az); s = stripe(el)
        need = h + W*math.tan(math.radians(el))
        stops = math.log2(dni(el)/ref) if dni(el) > 0 else float('-inf')
        print(f"  {SUN.hm(hh):>6} {el:5.1f}d {az:6.1f}d {rel:+6.1f}d {s:7.1f}' "
              f"{'YES' if s >= W else 'no':>7} {need:13.1f} ft {stops:+9.2f} st")

print("\n\nWHAT IF THE TWO SETS SWAPPED?\n")
for name, t0, t1, W in [('band (20 ft) in the LATE slot', 16.5, 17.5, 20.0),
                        ('duo  (12 ft) in the EARLY slot', 14.5, 15.5, 12.0)]:
    print(f"{name}:")
    for k in range(3):
        hh = t0 + k*(t1-t0)/2
        el = SUN.solar(*SUN.DATE, hh)[1]; s = stripe(el)
        print(f"   {SUN.hm(hh)}  sun {el:4.1f}d  stripe {s:5.1f}' vs {W:.0f}' needed  -> "
              f"{'WORKS' if s >= W else 'short by %.1f ft' % (W-s)}")
    print()

print("Light level through the afternoon (direct normal, relative to 14:30):")
ref = dni(SUN.solar(*SUN.DATE, 14.5)[1])
for hh in (14.5, 15.5, 16.5, 17.0, 17.5, 17.75):
    el = SUN.solar(*SUN.DATE, hh)[1]
    print(f"   {SUN.hm(hh)}  sun {el:4.1f}d  air mass {airmass(el):4.2f}  "
          f"{math.log2(dni(el)/ref):+5.2f} stops")
print(f"\n   sunset {SUN.hm(SUN._event(*SUN.DATE, False)[0])}")
