"""NOAA solar position. Vega Baja Skate Park, PR. No DST in Puerto Rico."""
import math

LAT, LON, TZ = 18.4450, -66.3880, -4.0      # AST year-round
DATE = (2026, 10, 26)

def _jday(y, m, d):
    if m <= 2: y, m = y-1, m+12
    a = y//100; b = 2 - a + a//4
    return int(365.25*(y+4716)) + int(30.6001*(m+1)) + d + b - 1524.5

def solar(y, mo, d, hour):
    jd = _jday(y, mo, d) + (hour - TZ)/24.0
    t = (jd - 2451545.0)/36525.0
    L0 = (280.46646 + t*(36000.76983 + t*0.0003032)) % 360
    M  = 357.52911 + t*(35999.05029 - 0.0001537*t)
    e  = 0.016708634 - t*(0.000042037 + 0.0000001267*t)
    Mr = math.radians(M)
    C  = (math.sin(Mr)*(1.914602 - t*(0.004817 + 0.000014*t))
          + math.sin(2*Mr)*(0.019993 - 0.000101*t) + math.sin(3*Mr)*0.000289)
    true_long = L0 + C
    omega = 125.04 - 1934.136*t
    app_long = true_long - 0.00569 - 0.00478*math.sin(math.radians(omega))
    seconds = 21.448 - t*(46.8150 + t*(0.00059 - t*0.001813))
    e0 = 23.0 + (26.0 + seconds/60.0)/60.0
    ec = e0 + 0.00256*math.cos(math.radians(omega))
    decl = math.degrees(math.asin(math.sin(math.radians(ec))*math.sin(math.radians(app_long))))
    vy = math.tan(math.radians(ec/2))**2
    L0r = math.radians(L0)
    eot = 4*math.degrees(vy*math.sin(2*L0r) - 2*e*math.sin(Mr) + 4*e*vy*math.sin(Mr)*math.cos(2*L0r)
                         - 0.5*vy*vy*math.sin(4*L0r) - 1.25*e*e*math.sin(2*Mr))
    tst = (hour*60 + eot + 4*LON - 60*TZ) % 1440
    ha = tst/4 - 180 if tst/4 < 180 else tst/4 - 180
    ha = (tst/4) - 180
    lr, dr, hr = math.radians(LAT), math.radians(decl), math.radians(ha)
    cz = math.sin(lr)*math.sin(dr) + math.cos(lr)*math.cos(dr)*math.cos(hr)
    cz = max(-1, min(1, cz))
    zen = math.degrees(math.acos(cz))
    el = 90 - zen
    # refraction
    if el > -0.575:
        te = math.tan(math.radians(el))
        if el > 5:    r = 58.1/te - 0.07/te**3 + 0.000086/te**5
        elif el > -0.575: r = 1735 + el*(-518.2 + el*(103.4 + el*(-12.79 + el*0.711)))
        else: r = -20.772/te
        el += r/3600.0
    den = math.cos(lr)*math.sin(math.radians(zen))
    if abs(den) < 1e-9: az = 180.0
    else:
        ca = (math.sin(lr)*math.cos(math.radians(zen)) - math.sin(dr))/den
        ca = max(-1, min(1, ca))
        az = math.degrees(math.acos(ca))
        az = (az + 180) % 360 if ha > 0 else (540 - az) % 360
    return az, el, eot, decl

def _event(y, mo, d, rising):
    jd = _jday(y, mo, d)
    t = (jd - 2451545.0)/36525.0
    _, _, eot, decl = solar(y, mo, d, 12.0)
    lr, dr = math.radians(LAT), math.radians(decl)
    c = math.cos(math.radians(90.833))/(math.cos(lr)*math.cos(dr)) - math.tan(lr)*math.tan(dr)
    ha = math.degrees(math.acos(max(-1, min(1, c))))
    noon = (720 - 4*LON - eot)/60 + TZ
    return noon - ha/15 if rising else noon + ha/15, noon

CAM_BEARING = 332.0        # the plan's page-up bearing; cameras look up the page

def rel_to_camera(az, look=CAM_BEARING):
    """Signed angle from the camera's look direction. 0 = straight into the
    lens (back light), +/-180 = straight behind the camera (flat frontal light
    on the band), + = camera right, - = camera left."""
    return ((az - look + 180) % 360) - 180

def hm(h):
    h = h % 24
    return f"{int(h):02d}:{int(round((h-int(h))*60)):02d}"

if __name__ == "__main__":
    y, mo, d = DATE
    rise, noon = _event(y, mo, d, True)
    sett, _ = _event(y, mo, d, False)
    print(f"Vega Baja  {LAT}N {abs(LON)}W   26 OCT 2026  (AST, UTC{TZ:+.0f})")
    print(f"  sunrise {hm(rise)}   solar noon {hm(noon)}   sunset {hm(sett)}")
    az, el, _, decl = solar(y, mo, d, noon)
    print(f"  declination {decl:+.2f} deg ; noon altitude {el:.1f} deg at azimuth {az:.1f}")
    print()
    azr = solar(y, mo, d, rise)[0]; azs = solar(y, mo, d, sett)[0]
    print(f"  sunrise bearing {azr:.2f} ; sunset bearing {azs:.2f}")
    print()
    print(f"  Cam A looks at {CAM_BEARING:.0f} deg (page up).")
    print("  time    azimuth  altitude     rel   reading")
    for h in [x/2 for x in range(12, 37)]:
        az, el, _, _ = solar(y, mo, d, h)
        if el < -0.5: continue
        r = rel_to_camera(az)
        if   abs(r) > 150: side = 'straight behind camera, flat frontal'
        elif abs(r) > 110: side = 'behind-' + ('right' if r > 0 else 'left')
        elif abs(r) >  70: side = 'camera ' + ('RIGHT' if r > 0 else 'LEFT') + ', side'
        else:              side = 'front-' + ('right' if r > 0 else 'left') + ', back light'
        print(f"  {hm(h)}   {az:6.1f}   {el:6.1f}  {r:+7.1f}   {side}")
