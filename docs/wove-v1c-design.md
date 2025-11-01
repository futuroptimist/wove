# Wove v1c Mechanical Crochet System Design

## Vision and Goals
- Deliver an open-source, mechanically actuated crochet device that hobbyists can build with
  consumer-grade 3D printers and widely available hardware.
- Provide a modular platform that evolves into the knitting-focused v1k variant while sharing
  control electronics, firmware foundations, and community documentation.
- Optimize for reproducibility, safety, and maintainability so contributors can iterate on
  specific subsystems without destabilizing the whole machine.

## System Overview
The v1c system combines a 3D-printed frame, modular motion assemblies, yarn-management features,
open firmware, and desktop control tools. A single-board microcontroller drives NEMA 17 steppers
and hobby servos to reproduce the hand motions required for crochet stitches. Optional sensors for
limit detection and yarn tension improve repeatability while remaining optional for early builds.

Key modules include:
- **Hook Actuation Gantry** – X/Y motion with interchangeable Z-axis carriage supporting a rotary or
  oscillating crochet hook end-effector.
- **Yarn Feed and Tensioner** – Spring-loaded tension post and guide ring combination that maintains
  constant feed resistance without damaging yarn.
- **Workpiece Support Bed** – Removable plate with magnetic anchors to hold fabric while enabling
  easy removal between runs. The Three.js viewer now pulses those anchor pucks so technicians can
  rehearse plate swaps before loading yarn, with a sequential glow sweeping across each puck to
  illustrate the recommended swap order.
- **Electronics Bay** – Enclosed mount for controller, stepper drivers, wiring harness, and cooling.
- **Safety Interlocks** – Mechanical end stops, emergency stop button, and firmware-based motion
  limits.

## Mechanical Subsystem
### Hook Motion Assembly
- **Axes**: CoreXY belt layout for fast X/Y travel using two GT2 belts and idler pulleys. Optional
  linear rail upgrade path; default uses 8 mm smooth rods with LM8UU bearings to minimize cost.
- **Hook Carriage**: Modular interface accepting either a rotary hook drive (geared stepper) or a
  cam-based oscillation module (MG90S metal gear servo). 20 mm fan mount supports passive cooling
  of the actuator. The Three.js viewer now renders the fan mount and blades so teams can spot the
  cooling hardware during walkthroughs.
- **Z Motion**: Leadscrew-driven lift (T8x2) moved by a compact stepper to set hook penetration
  depth. Anti-backlash nut and printed flexures reduce play. The Three.js viewer now spotlights
  the Z-axis leadscrew, anti-backlash nut, and flexures beside the hook carriage so contributors
  can rehearse how the lift assembly suppresses wobble before printing hardware.

(yarn-handling)=
### Yarn Handling {#yarn-handling}
- **Tension Post**: Dual-post design with printed spring clip for quick yarn swaps. Replaceable
  felt pads prevent abrasion.
- **Guide Path**: PTFE tube segments route yarn from spool to hook while allowing low-friction
  motion. Optional filament sensor monitors breaks for advanced builds.

The Three.js viewer mirrors this assembly with glowing felt pads and a translucent PTFE tube so
builders can visualize how yarn leaves the spool, touches the hall sensor, and reaches the hook
before printing hardware. Animated amber pulses now chase through the tube to illustrate feed
direction while the planner preview runs, and a trio of glowing beads—offset with staggered
speeds—follows the same path during yarn feed events so the motion reads clearly from the plaza
overview before fading once the feed cycle pauses.
The supply spool now spins in the hologram whenever yarn is extruding so teams can watch fiber
unwind from the source while the tube pulses, then glides to a stop when feed events pause so idle
segments stay calm.

#### Tension Profiles and Bench Tests

Phase 3 of the documentation roadmap now ships an initial catalog of yarn tension profiles. The
`wove.tension` module records bench tests for lace through super bulky weights, including target
pull force, recommended feed rate, and the measured variation during a 60-second feed trial. Use
the helpers to look up a tested profile or estimate tension for in-between yarns:

```python
from wove import (
    estimate_profile_for_force,
    estimate_profile_for_wpi,
    estimate_tension_for_force,
    estimate_tension_for_wpi,
    find_tension_profile_for_wpi,
    find_tension_profile_for_force,
    match_tension_profile_for_wpi,
    get_tension_profile,
)

# Retrieve a documented profile (case-insensitive lookup)
worsted = get_tension_profile("Worsted")
print(worsted.target_force_grams)  # -> 65.0 grams of pull force

# Interpolate for a yarn that falls between fingering and sport weights
target_force = estimate_tension_for_wpi(17.5)
print(round(target_force, 1))  # -> 42.1 grams (approx)

# Inspect interpolated feed-rate guidance and bounding weights
profile = estimate_profile_for_wpi(17.5)
print(profile.feed_rate_mm_s, profile.heavier_weight, profile.lighter_weight)
print(profile.trial_duration_seconds)  # -> 60.0-second trial window

# Identify the documented profile that spans a measured wraps-per-inch value
matched = find_tension_profile_for_wpi(18.0)
print(matched.weight if matched else "no catalog match")

wpi_match = match_tension_profile_for_wpi(24.0)
print(wpi_match.profile.weight, round(wpi_match.difference_wpi, 1))

# Map a measured pull force back to the catalog and inspect the difference
force_match = find_tension_profile_for_force(68.0)
print(force_match.profile.weight, force_match.difference_grams)

# Interpolate feed rate and variation guidance directly from a measured pull force
force_profile = estimate_profile_for_force(68.0)
print(round(force_profile.feed_rate_mm_s, 1))  # -> 34.0 mm/s (approx)
print(force_profile.heavier_weight, force_profile.lighter_weight)

# Clamp a measured pull force to the catalog bounds when only the tension target is needed
target_force = estimate_tension_for_force(110.0)
print(target_force)  # -> 95.0 grams (clamped to the heaviest profile)
```

Profiles are sorted from lightest to heaviest yarns so the automation stack can feed the data into
future calibration scripts. Each entry captures the wraps-per-inch range, the 60-second trial
duration, and highlights how evenly the passive tensioner maintained feed force during testing.
Use `match_tension_profile_for_wpi` to locate the nearest catalog entry when a measurement falls
between documented ranges; the helper reports the absolute wraps-per-inch difference so calibration
tools can surface how far a swatch deviates from the recorded data.

`estimate_profile_for_wpi` returns interpolated values along with the heavier and lighter catalog
weights that bound the requested wraps-per-inch. Use those labels to surface which tested yarns the
estimate derived from during calibration reports. Call `estimate_profile_for_force` when bench
measurements start from pull force instead of wraps-per-inch; it returns the same metadata while
preserving the measured tension target.

Hall-effect sensors mounted on the tension arm can feed real-time readings back into the same
catalog. Calibrate the sensor with a handful of measured loads, then translate new readings into
grams and match them to the documented yarn weights:

```
from wove import (
    CalibrationPoint,
    HallSensorCalibration,
    estimate_tension_for_sensor_reading,
    match_tension_profile_for_sensor_reading,
    estimate_profile_for_sensor_reading,
    estimate_sensor_reading_for_tension,
)

calibration = HallSensorCalibration.from_pairs(
    [
        (102.0, 20.0),
        (168.5, 55.0),
        (220.0, 85.0),
    ]
)

reading_grams = estimate_tension_for_sensor_reading(185.0, calibration)
force_match = match_tension_profile_for_sensor_reading(185.0, calibration)
interpolated = estimate_profile_for_sensor_reading(185.0, calibration)
target_reading = estimate_sensor_reading_for_tension(65.0, calibration)

print(round(reading_grams, 1))  # -> 61.3 grams (interpolated)
print(force_match.profile.weight, round(force_match.difference_grams, 1))
print(round(interpolated.feed_rate_mm_s, 1))  # -> 33.5 mm/s (approx)
print(interpolated.heavier_weight, interpolated.lighter_weight)
print(round(target_reading, 1))  # -> 185.7 (approx)
```

Clamp behavior defaults to the calibration bounds so noisy readings outside the measured range do
not generate unrealistic values. Pass ``clamp=False`` to surface out-of-range readings for
additional debugging, or to raise errors when routing data through
``estimate_profile_for_sensor_reading``. When driving the optional servo-based tension adjuster,
use ``estimate_sensor_reading_for_tension`` to determine the sensor reading that corresponds to a
target pull force before commanding the actuator.

The calibration bench inside the Tension Lab renders that automation path. The Three.js viewer now
parks a micro-servo tension adjuster beside the load-cell carriage with a glowing status light so
contributors can see how programmable feed loops interface with the spool rig before printing
hardware. The horn now sweeps through its pull stroke whenever the planner preview feeds yarn and
the status orb brightens in step, making the servo-driven tension cues obvious from the plaza
overview.

### Frame and Build Volume
- **Frame**: 20x20 mm aluminum extrusion perimeter with printed corner cubes and feet. Designed for
  250 mm × 250 mm working area; printable parts cap at 220 mm to fit standard beds. The
  Three.js assembly viewer mirrors this perimeter with the same corner cubes and leveling feet so
  teams can visualize the bench footprint before cutting extrusion to length.
- **Bed**: Magnetic stainless sheet bonded to a printed base with embedded M3 heat-set inserts for
  accessory mounting.

### Safety Features
- Full-travel physical end stops on X, Y, and Z with printable housings.
- Snap-on belt guards protect against accidental entanglement. The Three.js viewer now renders the
  clip-on covers hugging the CoreXY belts so build crews can rehearse clearances before printing
  hardware.
- Firmware-configurable soft limits and homing sequences prevent overtravel.
- The Three.js assembly viewer in `viewer/index.html` spotlights the emergency
  stop and glowing axis end stops so builders can rehearse the safety flow
  before powering the hardware. Pulsing halos now wrap each limit switch while
  soft indicator lights float above the housings, matching the planned homing
  path. Pedestals in the same scene outline adjacent
  roadmap work cells (calibration lab, material prep pod, and the v1k research
  rig) so contributors understand how the crochet platform integrates with the
  broader automation journey. A pulsing selection ring sweeps around the active
  cluster so teams can track the focus from above, while a rotating teal arc
  orbits the ring to reinforce which milestone is active. Clicking a pedestal
  now swings the camera toward that work cell so crews immediately focus on the
  selected milestone. The material prep pod pedestal now highlights the
  cone tree, staging bins, inspection scale, and traceability cards that feed
  yarn into the crochet cell. The Pattern Studio hologram loops a base chain
  row exported from `wove.pattern_cli --format planner`, previewing how planner
  payloads animate across the workspace before firmware executes them. The
  viewer streams that sample directly from
  `viewer/assets/base_chain_row.planner.json` so the hologram stays aligned with
  the repository's planner fixtures. A translucent bounds frame now wraps the
  hologram while the overlay lists the exported X/Y/Z/E ranges so operators can
  verify the motion envelope matches the CLI payload.
- Optional polycarbonate shield with hinged access door for production environments;
  the Three.js viewer renders the translucent enclosure so teams can rehearse
  safe access paths before printing hardware. Mint-highlighted floor markings
  now extend through the open doorway with alternating, pulsing footprints so
  operators can practice each step without clipping the gantry or tension
  hardware. Numbered step badges hover above each footprint so crews can rehearse
  the left/right cadence before approaching the enclosure.

## Electronics and Control
### Control Board
- Recommend the BigTreeTech SKR Mini E3 V3 or comparable 32-bit board with TMC2209 drivers for
  quiet, sensorless-homing-capable motion.
- Alternate path: RAMPS 1.4 + Arduino Mega for builders using legacy hardware (documented in v1c
  appendix).

### Motors and Actuators
- **X/Y**: Two NEMA 17 42 × 40 mm steppers, 1.5 A max current.
- **Z**: One compact NEMA 17 or NEMA 14 stepper with integrated lead screw coupler.
- **Hook**: High-speed NEMA 11 stepper (rotary) or MG90S servo (oscillation).
- **Tensioner**: Optional micro-servo for automated yarn feed adjustments.

### Sensors and Switches
- Mechanical limit switches on each axis (Omron D2F or similar).
- Optional hall-effect sensor for yarn tension measurement via flexible arm deflection.
- The Three.js assembly viewer now spotlights the hall-effect sensor beside the yarn path so
  builders can rehearse how feedback hardware integrates before printing the mount.
- Thermistor channel reserved for future heated bed accessory; the Three.js viewer now illuminates
  the conduit so wiring routes stay obvious before the heater upgrade ships.
- A tinted electronics bay beneath the work bed now reveals the SKR Mini controller
  stack, cooling fan, and cable harness routing so operators can plan airflow and wiring
  alongside the rest of the assembly.
- Emergency stop wired in series with board power.

### Power and Wiring
- 24 V, 10 A supply for steppers; onboard 5 V regulator powers sensors and servos.
- JST-XH harnesses for modular axis replacement; printed cable chains keep wiring tidy.
- Provide wiring schematics and harness length tables for standard build sizes.

### Firmware and Software
- Base firmware forked from Klipper for flexible motion control and macro scripting.
- Default config files define axis scaling, stepper currents, and safety limits.
- Companion Python CLI handles pattern translation from custom stitch descriptions to
  G-code-like motion sequences. Initial DSL support is complete, and a lightweight SVG polyline
  importer converts sketches into travel moves for rapid prototyping.
- Browser-based planner integration has started: the Pattern Studio hologram in
  the Three.js viewer replays a base chain row exported via
  `wove.pattern_cli --format planner`, showcasing how planner payloads map to
  motion without parsing raw G-code while leaving room for deeper
  interactivity. The overlay's Pattern Studio panel now streams the active
  planner comment and timeline progress so operators can read the motion step as
  the hologram animates. A Planner Defaults list now surfaces the safe Z height,
  fabric plane, row spacing, and feed-rate settings embedded in the planner
  export so operators can reconcile the viewer preview with CLI configuration
  before a dry run. A Yarn Flow monitor in the overlay mirrors the glowing PTFE
  tube, flipping between feed-active and idle states so the hologram, spool
  animation, and status text stay synchronized. The same panel now reports how
  much yarn the preview has fed versus the planned total and highlights the
  remaining feed pulses so crews can pace dry runs without guessing when the
  next extrusion event lands. A companion Machine Profile
  panel lists the
  microstepping, steps-per-millimeter, and travel bounds from planner exports so
  technicians can confirm the browser preview mirrors the configured gantry
  before committing motion to hardware. The Homing Guard overlay highlights the
  `require_home` setting and recorded `home_state`, switching to green when the
  export captured a verified homing cycle and calling attention to plans that
  need a fresh homing run. The same panel now streams live `X`, `Y`, `Z`, and
  yarn-feed coordinates so contributors can note the precise motion snapshot as
  the hologram advances.

## Bill of Materials (Initial Release)
| Subsystem | Component | Qty | Notes |
|-----------|-----------|-----|-------|
| Frame | 20×20 mm aluminum extrusion, 300 mm | 6 | Pre-cut lengths |
| Frame | M5 × 10 mm button head screws | 24 | For extrusion joints |
| Motion | NEMA 17 stepper (1.5 A) | 3 | X, Y, Z axes |
| Motion | GT2 6 mm belt (loop) | 2 | 1.5 m each |
| Motion | 20-tooth GT2 pulley | 4 | For CoreXY layout |
| Motion | T8x2 lead screw, 250 mm | 1 | Z axis |
| Motion | LM8UU bearings | 8 | Linear motion |
| Hook | NEMA 11 stepper | 1 | Rotary hook option |
| Hook | MG90S servo | 1 | Oscillation option |
| Electronics | SKR Mini E3 V3 | 1 | Primary controller |
| Electronics | 24 V 10 A PSU | 1 | Meanwell LRS-200-24 or similar |
| Electronics | Emergency stop switch | 1 | Panel mount |
| Electronics | JST-XH connector kit | 1 | 2-, 3-, 4-pin assortments |
| Safety | Limit switch kit | 3 | Omron-style |
| Materials | PTFE tubing, 4 mm OD | 1 m | Yarn guide |
| Materials | Felt pads | 4 | Tensioner |

(See appendices for full fastener counts and optional upgrades.)

## Manufacturing Plan
### 3D-Printed Parts
- Provide STL and SCAD sources for the frame joints, carriage, hook modules, belt guards, wire
  clips, and electronics mounts.
- Default print settings: 0.2 mm layer height, 40% infill, PETG or ABS for structural parts,
  flexible TPU for tensioner pads.
- Include print orientation diagrams to reduce support usage and post-processing.

### Purchased Hardware
- Source extrusions, bearings, and fasteners from vendors with global distribution (Misumi,
  OpenBuilds, Amazon). Provide alternates for EU and APAC builders.
- Document cost ranges and bundle suggestions for community group buys.

### Assembly Strategy
1. Assemble frame on a flat surface using printed corner jigs and square-check procedure.
2. Install linear motion hardware and belts; verify smooth travel before mounting steppers.
3. Assemble and mount hook carriage; route PTFE yarn guide.
4. Wire electronics bay, verify continuity, and route harnesses through cable chains.
5. Load firmware configuration, perform homing, and calibrate step/mm.
6. Run dry-run crochet pattern without yarn to confirm motion, then perform first sample stitch.

## Testing and Validation
- **Mechanical**: Measure backlash on each axis (<0.1 mm target) and run endurance loop for 1000
  cycles to validate belt tension.
- **Electronics**: Validate thermal performance under continuous duty; ensure drivers stay below
  70 °C with passive cooling.
- **Firmware**: Execute stitch test suites covering chain, single crochet, and slip stitch
  sequences. Capture log files for regression.
- **User Validation**: Conduct build-along with at least three community testers to collect
  assembly and documentation feedback.

## Documentation and Community Support
- Maintain annotated exploded diagrams in the `cad/` directory and printable bill of materials in
  `docs/`.
- Produce step-by-step build guides with photographs and QR codes linking to video walkthroughs.
- Encourage contributors to submit field reports detailing yarn types, hook sizes, and stitch
  recipes tested.
- License hardware under CERN-OHL-P and software under GPLv3 to ensure derivatives remain open.

## Roadmap
| Phase | Focus | Key Deliverables | Owner(s) |
|-------|-------|------------------|----------|
| 0. Discovery (Weeks 1-2) | Research & benchmarking | Comparative study of existing crochet machines, requirements doc | Core design team |
| 1. Motion Prototype (Weeks 3-6) | Mechanical validation | Printed frame mockup, CoreXY motion demo, hook carriage v0.1 | Mechanical subgroup |
| 2. Electronics Integration (Weeks 5-8) | Control system | Controller selection report, wiring harness draft, firmware baseline | Electronics subgroup |
| 3. Yarn Handling (Weeks 7-10) | Feed & tension | Adjustable tensioner prototype, yarn guide validation tests, published tension profiles | Materials subgroup |
| 4. Full Assembly Alpha (Weeks 9-12) | System bring-up | Assembly manual v0.5, dry-run stitch tests, BOM freeze | Cross-functional |
| 5. Beta Validation (Weeks 12-16) | User testing | Community build feedback, issue tracker triage, documentation polish | Community leads |
| 6. Release Candidate (Weeks 16-18) | Packaging | Final CAD/STL bundle, firmware v1.0 configs, sourcing guide, marketing launch plan | Release manager |

### Risk Mitigation
- Maintain weekly design reviews to track dependencies between mechanical and electronics teams.
- Keep alternative components listed for high-risk supply chain items (steppers, controller).
- Document lessons learned per phase to accelerate v1k planning.

### Materials Sourcing Checklist
- Confirm extrusions and fasteners availability before launching community builds.
- Validate that recommended PSUs meet safety certifications (UL, CE).
- Provide printing filament alternatives with temperature and mechanical ratings.
- Publish vendor-neutral BOM spreadsheet to encourage localized sourcing.

### Documentation Deliverables per Phase
- Phase 1: Capture mechanical sketches and calibration metrics in the repository.
- Phase 3: Add yarn-specific tension profiles and test results.
- Phase 5: Finalize assembly guide, troubleshooting FAQ, and firmware configuration templates.
