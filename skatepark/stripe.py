import math, sun as SUN
L, h, W, g = 20.0, 7.0, 20.0, 4.4      # frame height, performer, band width, gap to band
print("A frame makes a SHADE STRIPE on the ground. Its width is what matters.\n")
print(f"{'time':>6} {'alt':>6} {'tan':>6} {'rail B':>7} {'rail T':>7} "
      f"{'ground reach':>13} {'stripe start':>13} {'stripe end':>11} {'stripe':>8} {'band covered':>13}")
for hh in (14, 15, 15.5, 16, 17):
    el = SUN.solar(*SUN.DATE, hh)[1]; t = math.tan(math.radians(el))
    B = g*t; T = B + L                  # bottom rail set so sun just grazes the near player's feet
    reach = T/t                         # where the top rail's ray hits the ground
    d0, d1 = B/t, (T-h)/t               # fully-shaded span for a person h tall
    cov = max(0.0, min(d1, g+W) - max(d0, g))
    print(f"{SUN.hm(hh):>6} {el:5.1f}d {t:6.3f} {B:6.1f}' {T:6.1f}' {reach:12.1f}' "
          f"{d0:12.1f}' {d1:10.1f}' {d1-d0:7.1f}' {cov:7.1f}' of {W:.0f}")
print(f"\nstripe width is always (L - h)/tan(alt) = ({L:.0f} - {h:.0f})/tan(alt). "
      f"Rail height slides it, never widens it.")
print(f"\nAt 14:00 the band needs {W:.0f} ft of stripe and gets "
      f"{(L-h)/math.tan(math.radians(SUN.solar(*SUN.DATE,14)[1])):.1f} ft.")
print("\nRaising the whole rig does not help -- it slides the stripe outward:")
el = SUN.solar(*SUN.DATE, 14)[1]; t = math.tan(math.radians(el))
for B in (0, 5, 10, 20):
    T = B + L
    print(f"   bottom rail {B:2.0f}' -> top {T:2.0f}' : ground reach {T/t:5.1f}', "
          f"fully shaded from {B/t:5.1f}' to {(T-h)/t:5.1f}'  (stripe {(L-h)/t:.1f}')")
