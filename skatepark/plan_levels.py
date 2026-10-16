"""Levels and working stops for the lighting plan. Decisions, not options."""
import math, sun as SUN
EFF=110.0
def sun_fc(h):
    el=SUN.solar(*SUN.DATE,h)[1]
    am=1.0/(math.sin(math.radians(el))+0.50572*(el+6.07995)**-1.6364)
    return el, 1.353*0.7**(am**0.678)*1000*EFF/10.764
def bounce(side,dist,src,rho=0.87):
    A=side*side; R=math.sqrt(A/math.pi); L=src*rho/math.pi
    return math.pi*L*R*R/(R*R+dist*dist)
def stop(E, iso=800, t=1/50):           # f-number for a given incident level
    return math.sqrt(E*0.64*(iso/800)*(t*50))
print("WORKING STOP  (ISO 800, 1/50 = 180 deg at 24p)\n")
for h,nd in ((14.5,7),(15.5,7),(16.5,6),(17.0,5),(17.5,3)):
    el,fc=sun_fc(h); fc_nd=fc/(2**nd)
    print(f"  {SUN.hm(h)}  sun {el:4.1f}d  {fc:6.0f} fc  with ND{nd} -> {fc_nd:5.0f} fc  = f/{stop(fc_nd):.1f}")
print("\nSET 1 LEVELS (14:30 sun = %.0f fc)\n" % sun_fc(14.5)[1])
S1=sun_fc(14.5)[1]
for lab,v in (('8x8 ultrabounce @ 10 ft  [1B key]',bounce(8,10,S1)),
              ('8x8 ultrabounce @ 12 ft  [1A fill]',bounce(8,12,S1)),
              ('4x4 ultrabounce @  5 ft  [1A eye]',bounce(4,5,S1)),
              ('4x4 ultrabounce @  8 ft  [1B fill]',bounce(4,8,S1)),
              ('4x4 hard silver @ 15 ft  [1B back / 1C key]',S1*0.9*0.45)):
    print(f"  {lab:46} {v:6.0f} fc   -{math.log2(S1/v):.1f} st")
print("\nSET 2 LEVELS\n")
for h in (16.5,17.0,17.5):
    el,fc=sun_fc(h)
    print(f"  {SUN.hm(h)} sun {fc:5.0f} fc | 12x12 bounce @12ft {bounce(12,12,fc):5.0f} fc "
          f"| 1.2k bare spot @15ft ~3550 fc | 1.2k thru 6x6 @8ft ~105 fc")
print("\n  Ambient once the sun is off the subject, late day: ~100-300 fc.")
print("  => 1.2k thru 6x6 at 105 fc becomes the key from about 17:15.")
