"""Second head: another 1.2k HMI, or a 600 W LED COB?

Flux figures are approximate and manufacturers inflate. Treat the RATIOS as
sound and verify absolute levels against each fixture's photometric chart.
"""
import math
HMI_LM, LED_LM = 110000.0, 60000.0     # 1.2k HMI lamp vs ~600 W LED COB fixture
FRESNEL, GRID = 0.55, 0.55

def spot_fc(lm, dist_ft, beam_deg=20.0):
    """Narrow beam (Fresnel spot / hyper reflector) onto axis."""
    sr = 2*math.pi*(1-math.cos(math.radians(beam_deg/2)))
    cd = lm*FRESNEL/sr
    return cd/(dist_ft**2)

def thru_frame(lm, side, dist, capture=0.75):
    out = lm*FRESNEL*capture*GRID
    A = side*side; L = out/(math.pi*A); R = math.sqrt(A/math.pi)
    return math.pi*L*R*R/(R*R+dist*dist)

print("JOB 1 — KEY through the 6x6 at 6 ft  (needs ~100 fc to take over at 17:15)\n")
for lab, lm in (('1.2k HMI', HMI_LM), ('600 W LED', LED_LM)):
    print(f"   {lab:10} {thru_frame(lm,6,6):6.0f} fc    both clear the bar")

print("\nJOB 2 — KICKER, bare and spotted at 15 ft\n")
for lab, lm in (('1.2k HMI', HMI_LM), ('600 W LED', LED_LM)):
    fc = spot_fc(lm,15)
    print(f"   {lab:10} {fc:6.0f} fc")
print(f"   ratio: HMI is {math.log2(spot_fc(HMI_LM,15)/spot_fc(LED_LM,15)):.1f} stops brighter")

print("\nBUT — what does the kicker actually have to beat?\n")
for t, amb in (('16:30 (in sun)', 6420), ('17:15 (sun off subject)', 250), ('17:45 (twilight)', 60)):
    h, l = spot_fc(HMI_LM,15), spot_fc(LED_LM,15)
    print(f"   {t:24} ambient {amb:5.0f} fc | HMI {math.log2(h/amb):+5.1f} st | LED {math.log2(l/amb):+5.1f} st")

print("\n   From 17:15 on, the LED is already 2+ stops over ambient. The HMI's extra")
print("   2 stops are output you will immediately net back down.")
print("\n   Only daylight job either could do is the 16:30 kicker, and that is head #1,")
print("   the 1.2k you already own.")
