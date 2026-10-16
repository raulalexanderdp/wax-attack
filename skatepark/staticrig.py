"""One rig per set that never moves. Cameras move, light stays."""
import math, sun as SUN
EFF=110.0
def sun_fc(h):
    el=SUN.solar(*SUN.DATE,h)[1]
    am=1.0/(math.sin(math.radians(el))+0.50572*(el+6.07995)**-1.6364)
    return el, 1.353*0.7**(am**0.678)*1000*EFF/10.764
def bounce(side,dist,src,rho=0.87):
    A=side*side; R=math.sqrt(A/math.pi); L=src*rho/math.pi
    return math.pi*L*R*R/(R*R+dist*dist)

el,S1=sun_fc(14.5)
print(f"14:30 sun {el:.1f} deg, {S1:.0f} fc\n")

# The concrete pad as a free, always-on uplight
for albedo,surf in ((0.35,'bare concrete'),(0.05,'carpet / duvetyne')):
    Eh = S1*math.sin(math.radians(el))          # horizontal illuminance on the pad
    up = albedo*Eh/2                            # onto a vertical surface standing on it
    print(f"  {surf:22} uplight onto a face: {up:6.0f} fc   "
          f"{-math.log2(S1/up):+.1f} st vs key")
print("\n  => the pad is already a 1,000 fc eye light covering the WHOLE band, for free,")
print("     and it cannot be in shot because it IS the shot. Carpet it and you lose that.\n")

print("8x8 ULTRABOUNCE — same frame, just moved closer between passes\n")
for d in (14,12,10,8,6):
    fc=bounce(8,d,S1)
    print(f"  @ {d:2d} ft  {fc:6.0f} fc   {-math.log2(S1/fc):+.1f} st vs key")
print(f"\n  12 ft -> 8 ft is +{math.log2(bounce(8,8,S1)/bounce(8,12,S1)):.1f} stop. That is the whole")
print("  'second pass' move: no new gear, no rebuild, just walk it in.\n")

print("SET 2 — what the rig has to ride\n")
for h in (16.5,17.0,17.5):
    e,f=sun_fc(h)
    print(f"  {SUN.hm(h)}  sun {e:4.1f} deg  {f:5.0f} fc   12x12 @12ft fill {bounce(12,12,f):5.0f} fc")
print(f"\n  Sun falls {math.log2(sun_fc(16.5)[1]/sun_fc(17.5)[1]):.1f} stops across the hour.")
print("  Pre-rig the crossover during the 15-20 min set change. Then it is a switch, not a build.")
