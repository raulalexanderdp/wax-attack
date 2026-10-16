"""Can the 1.2k compete with the sun? Order-of-magnitude, from first principles.

Fixture photometrics go stale and get inflated, so this reasons from luminous
flux and the inverse-square law rather than a remembered spec sheet. Check the
final numbers against the actual head's photometric chart before committing.
"""
import math, sun as SUN

EFFICACY   = 110.0     # lm/W, direct solar beam
HMI_LM     = 110000.0  # 1.2k HMI lamp flux, ~90-100 lm/W
FRESNEL_EF = 0.55      # fixture optical efficiency
GRID_QTR   = 0.55      # 1/4 grid transmission

def sun_fc(h):
    el = SUN.solar(*SUN.DATE, h)[1]
    if el <= 0: return el, 0.0
    am = 1.0/(math.sin(math.radians(el)) + 0.50572*(el+6.07995)**-1.6364)
    return el, 1.353*0.7**(am**0.678) * 1000 * EFFICACY / 10.764   # kW/m2 -> fc

def frame_fc(side_ft, lamp_dist, subj_dist, capture):
    """A diffusion frame lit from behind, treated as a Lambertian emitter."""
    lm = HMI_LM * FRESNEL_EF * capture * GRID_QTR
    area = side_ft**2
    L = lm/(math.pi*area)                      # cd/ft^2
    R = math.sqrt(area/math.pi)
    return math.pi * L * R*R/(R*R + subj_dist**2)

print("SUN AS A KEY (on a surface square to it)\n")
for h in (14.5, 15.5, 16.5, 17.0, 17.5):
    el, fc = sun_fc(h)
    print(f"   {SUN.hm(h)}  sun {el:4.1f} deg   {fc:7.0f} fc")

print("\n1.2k HMI THROUGH DIFFUSION\n")
rigs = [('12x12 @ 10 ft from subject, lamp 8 ft back', 12, 8, 10, 0.85),
        (' 6x6  @ 10 ft from subject, lamp 6 ft back',  6, 6, 10, 0.75),
        (' 6x6  @  8 ft from subject, lamp 6 ft back',  6, 6,  8, 0.75),
        (' 6x6  @  6 ft from subject, lamp 6 ft back',  6, 6,  6, 0.75)]
out = {}
for lab, s, ld, sd, cap in rigs:
    fc = frame_fc(s, ld, sd, cap); out[lab] = fc
    print(f"   {lab}   {fc:6.0f} fc")

print("\nSTOPS UNDER THE SUN\n")
best = max(out.values())
for h in (14.5, 16.5, 17.5):
    el, sfc = sun_fc(h)
    print(f"   vs {SUN.hm(h)} sun ({sfc:5.0f} fc): best rig is {math.log2(sfc/best):4.1f} stops under")

print("\n   Open shade / sun off the subject, late day: roughly 100-300 fc.")
print(f"   The 6x6 at 6 ft delivers {out[' 6x6  @  6 ft from subject, lamp 6 ft back']:.0f} fc.")
print("   => the 1.2k is not a daylight key. It is the key for AFTER the sun leaves.")

print("\n\nPOWER, PAPER AMPS AT 120 V (W/100)\n")
loads = [('1.2k HMI + ballast', 1400, 1), ('second head (1.2k or 600 W LED)', 1400, 1),
         ('band audio - ESTIMATE, CONFIRM', 2500, 1), ('village, monitors, chargers', 500, 1)]
tot_w = 0; tot_a = 0
for lab, w, n in loads:
    a = w*n/100; tot_w += w*n; tot_a += a
    print(f"   {lab:34} {w*n:5d} W   {a:5.1f} A")
print(f"   {'TOTAL':34} {tot_w:5d} W   {tot_a:5.1f} A")
print(f"\n   Plant: {tot_w/1000:.1f} kW running. HMI strike surges to ~2x, so size up:")
print(f"   10-12 kW tow plant. Never run a plant continuously under 20% of capacity.")
