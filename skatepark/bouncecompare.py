"""One 12x12 vs two 8x8s across a 14 ft band. Evenness is the only real trade."""
import math, sun as SUN
EFF=110.0
el=SUN.solar(*SUN.DATE,14.5)[1]
am=1.0/(math.sin(math.radians(el))+0.50572*(el+6.07995)**-1.6364)
SUNFC=1.353*0.7**(am**0.678)*1000*EFF/10.764
AMBIENT=1500.0        # concrete uplight + open sky on the shadow side

def bounce(side,dist,rho=0.87):
    A=side*side; R=math.sqrt(A/math.pi); L=SUNFC*rho/math.pi
    return math.pi*L*R*R/(R*R+dist*dist)

# band spans +/-7 ft off-axis; 35mm frustum edge at 28 ft is 14.4 ft off-axis
EDGE=14.4
print(f"14:30 sun {SUNFC:.0f} fc.  Band 14 ft wide, frame edge at {EDGE} ft off-axis.\n")

print("ONE 12x12, centre at 20.4 ft off-axis (near edge on the frustum line)\n")
c=EDGE+6
n,f=bounce(12,c-7), bounce(12,c+7)
print(f"   near player {c-7:4.1f} ft away  {n:6.0f} fc")
print(f"   far  player {c+7:4.1f} ft away  {f:6.0f} fc")
print(f"   raw falloff across the band: {math.log2(n/f):.1f} stops")
print(f"   with {AMBIENT:.0f} fc ambient on the shadow side: "
      f"{math.log2((n+AMBIENT)/(f+AMBIENT)):.2f} stops  <- what the camera sees\n")

print("TWO 8x8, one per half, each centred 13 ft from its own group\n")
n2,f2=bounce(8,10), bounce(8,16)
print(f"   nearest player {n2:6.0f} fc / furthest {f2:6.0f} fc")
print(f"   raw falloff: {math.log2(n2/f2):.1f} stops")
print(f"   with ambient: {math.log2((n2+AMBIENT)/(f2+AMBIENT)):.2f} stops\n")

print("VERDICT")
print(f"   12x12 is ~{math.log2(n/n2):+.1f} stop brighter at the near side and one unit to move.")
print(f"   Cost is {math.log2((n+AMBIENT)/(f+AMBIENT)) - math.log2((n2+AMBIENT)/(f2+AMBIENT)):.2f}"
      f" stop more unevenness across the band - under a third of a stop. Take the 12x12.")
print("   Cheat it by angling the frame to favour the far side rather than squaring it to the band.")
