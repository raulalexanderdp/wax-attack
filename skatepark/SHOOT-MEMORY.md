# CORRE FORREST! — Vega Baja Skate Park — Shoot Handoff

**Self-contained briefing. Paste or attach this into a new chat and it has everything
it needs — no re-deriving.**

Shoot date **26 October 2026**. DP: Raúl Alexander Marrero. 1-ton grip truck.
Scout was set for 16 Oct with Director, DP, Gaffer, Key Grip, Cam Op, 1st AD, Video Assist.
Last doc revision: Lighting Plan Rev 4, Plate Rev 6.

---

## 1. The location

Vega Baja Skate Park, Puerto Rico — **18.445°N, 66.388°W**, AST (UTC−4), no DST.

- **Concrete pad: 202.8 ft × 81.0 ft.** Measured off the Google Maps scale bar
  (50 ft and 20 m bars agree to 0.2%) and corroborated by the slab's 2.4:1 aspect.
- **Our overhead plate is NOT north-up.** Page-up on the plate = **true bearing 332° (NNW)**.
  The pad's long axis runs **62° (ENE)**, bowl at the south-west end. Measured two ways
  (rotation template match +28.0° at correlation 0.995; minAreaRect 330.5°), agreeing to 1.5°.
  **Everything direction-dependent flows from this.** The cameras look NNW, not N.
- Features west→east: bowl · long flat rail (E–W) · box / manny pad · triangular ledge ·
  roofed shelter.
- **Fixed obstacles that constrain staging:** the long flat rail sits at y = 70.5 ft and the
  box at y = 65–70 ft. The band therefore works the clear strip between the rail and the
  south edge of the pad — about **9 ft deep**. That strip, not preference, is why the drums
  are only 5 ft upstage.

Coordinate system used throughout: origin at the pad's north-west corner, **+x along the pad
(bearing 62°), +y across it**, all in feet.

## 2. Sun — 26 Oct 2026

Computed with the NOAA solar-position algorithm. **Verified against an outside source:
sunset 5:56 pm at 256.92° vs this model's 17:56 at 256.915° — 0.005° apart.**

**Sunrise 06:23 at bearing 102.93° · solar noon 12:09 at 59.0° due south · sunset 17:56 at 256.92°.**

Because the cameras look 332°, **the sun is camera LEFT all afternoon and the key direction
never flips between the two sets** — they will cut together as one day.

| Time | Altitude | Azimuth | Rel. to Cam A | Level |
|---|---|---|---|---|
| 14:30 | 43.5° | 230.7° | −101° | 8,735 fc |
| 15:00 | 37.7° | 236.7° | −95° | — |
| 15:30 | 31.6° | 241.6° | −90° (true side) | 7,965 fc |
| 16:30 | 18.7° | 249.1° | −83° | 6,420 fc |
| 17:00 | 12.0° | 252.1° | −80° | 4,988 fc |
| 17:30 | 5.3° | 254.8° | −77° | 2,565 fc |

Light falls only **0.44 stops from 14:30 to 16:30**, then −0.81 by 17:00 and −1.77 by 17:30.
Most of the loss is in the last twenty minutes.

**Avoid 10:00–12:30** — sun within 25° of straight behind Cam A at 46–59°, flat frontal,
and caps black out eyes. Neither set is scheduled there.

**UNVERIFIED:** trees west and north-west will block the sun before 17:56. The real out-time
for Set 2 is unknown and was a scout item.

## 3. Schedule

- **Set 1 — Corre Forrest!, four-piece band — 14:30–15:30**
- **Set 2 — singer + DJ duo — 16:30–17:30**
- 15–20 minute set change between.

**Standing recommendation, not yet accepted: swap the sets.** The band is the wide subject
and needs the low sun; the duo is narrow and doesn't. As scheduled it is inverted.
Cost of swapping: the band loads out at dusk. AD's call.

## 4. Cameras

All three sit south of the pad on one line, **28 ft south of the concrete**, looking 332°.

| | Lens | Covers | Position (ft) | Throw |
|---|---|---|---|---|
| **A** | 35 mm | Band wide, centre | 137.75, 109.0 | 35 ft |
| **B** | 70–200 mm | Close / vocals | 152.5, 109.0 | 37 ft |
| **C** | 70–200 mm | Close / instruments | 121.0, 109.0 | 42 ft |

Cam A, the box and the long E–W rail all share **x = 137.75 ft**.

**Cam A's throw is derived, not eyeballed:** 35 mm on full frame is a 54.4° horizontal field,
so covering the band needs 35 ft. **On Super 35 the same framing needs ~48 ft, which is into
the road — confirm the camera format.**

**Working stop — ISO 800, 1/50 (180° at 24p):**
14:30 ND2.1 → f/6.3 · 16:30 ND1.8 → f/8 · 17:00 ND1.5 → f/10 · 17:30 ND0.9 → f/14, then pull ND and open.
**6–8 stops of IRND required or the shoot does not happen** — at 8,735 fc you are otherwise at f/75.

## 5. Band layout (Layout 2, compressed)

**14 ft wide maximum.** This is the number everything downstream assumes.

| | x, y (ft) | Facing |
|---|---|---|
| GTR | 133.25, 77.8 | 14° in |
| VOX | 137.75, 77.4 | square |
| BASS | 142.25, 77.8 | 14° in |
| DRUMS | 137.75, 72.6 | square, 5.2 ft upstage |

Player centres span 9.0 ft; ~13.5 ft with bodies and instruments. **4.5 ft per player across
the front — tight for guitarists with pedalboards, and UNCONFIRMED against the real backline.**
Duo footprint assumed ~12 ft, also unconfirmed.

Band rider needs: 2 guitar amps, bass amp (backline), drums, 4 wedges, X32 rack, 4× PSM300,
16-ch splitter, Focusrite 18i20, Roland pad.

## 6. Lighting plan (Rev 4)

**One rig per set. It does not move while they play.** All Set 2 rigging happens during the
15–20 min set change.

### Set 1 · Band · 14:30–15:30
| | | | |
|---|---|---|---|
| **KEY** | The sun | Camera left, hard, 90° side | 8,700 fc |
| **FILL** | 12×12 bounce | Camera right, ~20 ft off-axis, in full sun, **angled to favour the far side** | 1,500 fc |
| **EYE** | The bare concrete | **Do not carpet under the band** | 1,050 fc |

Second pass: walk the 12×12 in to 10–12 ft. +1 stop, softer, more even. Two grips, five minutes.

### Set 2 · Duo · 16:30–17:30
| | | | |
|---|---|---|---|
| **KEY** | The sun | Camera left, raking, falls 1.3 st across the hour | 6,400 fc |
| **FILL** | 12×12 bounce | Camera right, 12 ft — same frame, relocated | 1,350 fc |
| **KICKER** | 1.2k HMI bare, spotted | Camera right-rear. On at 16:30, stays on | 3,550 fc |
| **STANDBY** | 600 W LED COB + 6×6 ¼ grid | Camera left on the sun's departing azimuth. **Built and dark from 16:30** | 105 fc |

Crossover ~17:10 between songs: standby head on · 12×12 out · dial the LED warm. Two minutes.

## 7. Decisions already made — do not relitigate

1. **No 20×20 diffusion.** At 14:30 a four-hi-roller rig covers 13.2 ft; the band needs 13.5.
   Short by inches. 400 sq ft of sail in October trades for one hour of coverage. The geometry
   only closes with a 24.6 ft top rail raked 30° — a condor, not a grip stand.
2. **Governing equation:** `tan(sun altitude) ≤ (frame height − performer height) ÷ band width`.
   The distance needed to keep a frame out of shot **cancels out** — it only sets rail height.
3. **A 1.2k HMI cannot key against daylight** — 5.7 stops under the 2:30 sun. Bounce is the
   answer. Hard silver is the only "unit" that competes (1.3 stops under) because it re-aims
   the sun rather than fighting it.
4. **One 12×12 beats two 8×8s** for Set 1 fill — costs 0.2 stop of evenness across the band,
   saves a unit and a move. Keep two 8×8s as the wind fallback only.
5. **Second head = 600 W LED COB (bicolor/RGB), not another HMI.** It dims across a falling-
   ambient set, runs silent next to a live PA, strikes instantly, tracks the sun warm without
   gel, and halves that line on the generator. The LED's lower output does not matter — from
   17:15 it is already 2.6 stops over ambient.
6. **Do not carpet under the band.** Bare pad returns ~1,050 fc of uplight into faces, three
   stops under key; that is what opens the cap-brim shadow and it covers all four players.
   Carpet drops it to 150 fc. Carpet only where a hot spot reads in the background.
7. **No overhead on the band.** A 6×6 covers one person, not four, and cannot live in the wide.

## 8. Power — unresolved, highest risk

| Load | W | Paper A |
|---|---|---|
| 1.2k HMI + ballast | 1,400 | 14 |
| 600 W LED COB | 700 | 7 |
| Band audio — **ESTIMATE** | 2,500 | 25 |
| Village, monitors, chargers | 500 | 5 |
| **Total** | **5,100** | **51** |

- **10–12 kW tow plant**, sized for HMI strike surge (~2×), not the running load.
  Never run a plant continuously under 20% of capacity.
- **Keep the HMI off the audio supply.** Ballast noise into a PA is not fixable in post.
  Separate putt-putt for sound, or separate legs minimum, and sound gets the say.
- **Nobody has confirmed where power comes from.** This is the single biggest open item.

## 9. Open items

1. **Power source** — genny or park service? (highest risk)
2. **Western treeline** — real out-time for Set 2
3. Band footprint ≤ 14 ft with the real backline?
4. Duo footprint ≤ 12 ft?
5. Running order — swap or not?
6. Second head in budget?
7. **Camera format — FF or Super 35?** Changes Cam A's throw from 35 to 48 ft
8. 6–8 stops of IRND confirmed on the truck?
9. Wind at the band position at both set times
10. Is there 35 ft of clear, level ground south of the pad for Cam A?

## 10. Caveats

- **All light levels are order-of-magnitude**, derived from luminous flux and inverse square,
  not from spec sheets. Meter on the day and trust the meter over any of this.
- Band and duo footprints are assumptions until staked on site.
- **No heights are surveyed anywhere in the park.** The plate answers where things are, not
  what a camera can see over them.
- Nine of the park's traced elements have measured footprints but unconfirmed types; only
  the bowl, rail, box, triangular ledge and shelter are keyed on the plate.

## 11. Files

Repo `raulalexanderdp/wax-attack`, branch `claude/skate-park-overhead-graphic-remyi2`,
directory `skatepark/`.

- `scout/CORRE_FORREST_Tech_Scout_Brief_16OCT2026.pdf` — 4-page handout: scout brief,
  lighting plan, grip & gaffer package, plate
- `vega-baja-skatepark-overhead*.svg|png` — the plate, 5 variants (main, layout2, clean,
  alpha, grid), 1920×1080 SVG and 3840×2160 PNG
- Scripts: `sun.py` (solar position) · `geom.py` / `final.py` (plate) · `diffusion.py`,
  `stripe.py`, `raked.py`, `feasibility.py` (frame geometry) · `lightlevels.py`,
  `coverage.py`, `plan_levels.py`, `staticrig.py`, `bouncecompare.py`, `secondhead.py`
  (lighting maths) · `verify.py` (registration check)
