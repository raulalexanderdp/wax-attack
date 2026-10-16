"""Why a 6x6 works on a long lens when a 20x20 fails on the wide.

Two separate questions:
  1. Does an overhead frame clear the top of frame on a tight lens?
  2. What do the day-exterior sources actually deliver, relative to the sun?
"""
import math, sun as SUN
SENSOR_W, SENSOR_H = 36.0, 24.0
CAM_H = 5.0

def frame_at(fl, dist):
    return dist*SENSOR_W/fl, dist*SENSOR_H/fl

print("1. OVERHEAD CLEARANCE  (camera at 5 ft, subject 6 ft tall)\n")
print(f"  {'lens':>6} {'dist':>6} {'frame w':>8} {'frame h':>8} {'top of frame':>13}   6x6 flown at 9 ft?")
for fl, dist in ((35,35),(50,35),(85,40),(135,40),(200,45)):
    w,h = frame_at(fl, dist); top = CAM_H + h/2
    print(f"  {fl:4d}mm {dist:5.0f}' {w:7.1f}' {h:7.1f}' {top:12.1f}'   "
          f"{'CLEARS' if 9.0 > top else 'IN SHOT'}")

print("\n2. OVERHEAD OFFSET  (frame must sit up-sun by height/tan(alt))\n")
for h in (14.5, 15.5, 16.5):
    el = SUN.solar(*SUN.DATE, h)[1]; t = math.tan(math.radians(el))
    print(f"  {SUN.hm(h)}  sun {el:4.1f} deg   6x6 at 9 ft sits {9/t:5.1f} ft up-sun; "
          f"shadow is 6 ft across - covers one person, not four")

print("\n3. WHAT EACH SOURCE DELIVERS vs THE 14:30 SUN (8,735 fc)\n")
SUN_FC = 8735.0
def lambertian(side, dist, rho=0.87):
    A = side*side; R = math.sqrt(A/math.pi)
    L = SUN_FC*rho/math.pi
    return math.pi*L*R*R/(R*R + dist*dist)
rows = [('4x4 ultrabounce @ 10 ft', lambertian(4,10)),
        ('4x4 ultrabounce @  5 ft', lambertian(4,5)),
        ('8x8 ultrabounce @ 10 ft', lambertian(8,10)),
        ('8x8 ultrabounce @ 15 ft', lambertian(8,15)),
        ('12x12 ultrabounce @ 12 ft', lambertian(12,12)),
        ('4x4 HARD SILVER @ 15 ft (near-specular, ~0.9)', SUN_FC*0.9*0.45),
        ('1.2k HMI thru 6x6 @ 6 ft', 167.0)]
for lab, fc in rows:
    print(f"  {lab:46} {fc:7.0f} fc   {math.log2(SUN_FC/fc):4.1f} stops under sun")

print("\n  Open sky ambient under a solid (subject cut out of the sun): roughly 800-1,500 fc.")
print("  => once the sun is CUT, an 8x8 or 12x12 bounce becomes the dominant key.")
print("     That is the whole trick: subtract first, then your small sources matter.")
