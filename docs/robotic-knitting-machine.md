# Robotic Knitting Machine Design Specification

This document captures the current architecture and operating assumptions for Wove's DIY robotic
knitting platform. It complements the `cad/` OpenSCAD models and firmware experiments by
surfacing the mechanical decisions, firmware dependencies, and simplification opportunities that
shape the build.

## Scope and goals

The system aims to automate flat-bed knitting with easily sourced components and hobby-grade 3D
printers. The minimum viable platform should:

- Drive at least one knitting needle along X/Y with repeatable ±0.25 mm positioning.
- Maintain yarn tension suitable for fingering-to-worsted weight yarn without manual intervention.
- Use off-the-shelf stepper motors (NEMA17 class) and common M3/M5 fasteners.
- Remain printable on 200 mm × 200 mm × 200 mm build volumes using PLA or PETG.

Assume builders have access to a four-axis controller (e.g., Klipper, GRBL, or Duet) capable of at
least 1/16 microstepping and end-stop monitoring.

## Operating assumptions and constraints

- **Coordinate system:** Right-handed, origin at the home position of the carriage, Z axis positive
  upward. Firmware expects homing switches on X and Y.
- **Needle form factor:** Standard 2.0–2.5 mm circular knitting needles trimmed to 120 mm usable
  length. The adapter allows ±0.5 mm radial adjustment.
- **Frame spacing:** Module spacing is designed around 20 mm aluminum extrusion or 8 mm linear rod.
- **Fasteners:** Default to M3 × 8 mm machine screws with heat-set inserts where possible; models
  also accommodate printed standoffs when inserts are unavailable.
- **Print orientation:** Parts are modeled assuming layers run perpendicular to primary loads to
  avoid delamination under yarn tension and carriage acceleration.

These constraints should be reviewed when targeting alternative materials, print profiles, or yarn
weights.

## System architecture

### Motion platform

- Linear motion is delivered via a stepper-driven carriage that rides along a primary X rail. A
  secondary rail or idler can be added for stabilization when the payload exceeds 200 g.
- Homing is performed with mechanical end stops wired to the controller. Add print-in-place flag
  pockets in the carriage to mount micro-switches without secondary brackets.
- Cable routing should reserve a 12 mm-wide channel for PTFE tubing and wiring harnesses, kept clear
  of the needle sweep envelope.

### Yarn handling stack

- Yarn enters through a tension post, passes the yarn guide, then feeds into the needle adapter.
- Adjustable spacers control the vertical separation between guide features to prevent snags when
  using multiple yarn weights.
- The tension subsystem remains passive. For active feedback, leave space for a future load cell in
  the base plate (30 mm × 15 mm × 5 mm).

### Control electronics interface

- A removable electronics mounting bracket seats a NEMA17 stepper and breakout board. Keep 20 mm of
  clearance behind the motor to route cables and fit 2-pin JST connectors.
- Firmware expects per-axis limit switch inputs and optional servo control for a yarn cutter. Route
  signal wiring through the carriage spine to reduce external harnessing.

## Module responsibilities and key parameters

- **Needle adapter**
  - Purpose: clamps the knitting needle and presents it to the yarn path.
  - Key parameters: adjustable clamp gap (`needle_clearance` 2.5–3.5 mm), grub screw pocket for an
    M3 set screw.
  - Interfaces: slides into the carriage via a 10 mm dovetail and accepts tension from the yarn
    guide.
- **Stepper mount**
  - Purpose: locates a NEMA17 motor and couples it to the carriage belt or lead screw.
  - Key parameters: `hole_spacing` defaults to 31 mm; optional 5 mm registration lip to align with
    extrusion.
  - Interfaces: bolts to the carriage plate with four M3 screws; motor shaft couples to a GT2 pulley
    or lead screw coupler.
- **Carriage**
  - Purpose: carries the needle adapter and optional sensors.
  - Key parameters: central boss sized for 608 bearings; `belt_width` parameter supports 6–9 mm
    belts.
  - Interfaces: mates with linear rail blocks and belt clamp; includes cavities for micro-switches.
- **Mounting bracket**
  - Purpose: anchors modules to extrusion or bench-top jigs during prototyping.
  - Key parameters: 90° angle with slots sized for M5 T-nuts.
  - Interfaces: connects to extrusion uprights and receives the spacer stack.
- **Spacer / washer set**
  - Purpose: maintains consistent module spacing.
  - Key parameters: shared profile with a `thickness` parameter and optional chamfer toggled by
    `add_chamfer`.
  - Interfaces: stacks between carriage plates or brackets to center modules.
- **Calibration cube**
  - Purpose: validates printer accuracy and clearance for hardware.
  - Key parameters: 20 mm cube with 5 mm through-hole; optional embossed axis labels.
  - Interfaces: used as a print check before fabricating load-bearing parts.
- **Yarn guide**
  - Purpose: directs yarn and isolates abrasion points.
  - Key parameters: replaceable PTFE liner channel (`liner_diameter` 3 mm).
  - Interfaces: mounts on the spacer stack and keys into the tension post.
- **Tension post**
  - Purpose: sets yarn wrap angle and overall tension.
  - Key parameters: `STANDOFF_MODE` toggles between heat-set inserts and printed standoffs.
  - Interfaces: fastens to the mounting bracket and shares the spacer stack footprint.
- **End cap / alignment pin**
  - Purpose: protects exposed rods and keeps stacked components square.
  - Key parameters: 5 mm pin diameter with optional chamfer.
  - Interfaces: press-fits into 5 mm bores on spacers or rods.
- **Accessory hook**
  - Purpose: provides parking for lightweight tools.
  - Key parameters: 15 mm offset from mount center; supports loads up to 200 g.
  - Interfaces: clips onto extrusion or the spacer stack.

## Manufacturing and assembly guidance

- Use `./scripts/build_stl.sh <file.scad>` or `python -m wove.build_stl <file.scad>` to regenerate
  STLs; both commands skip up-to-date outputs to accelerate iteration.
- Group print jobs by required nozzle size to minimize tool changes. Spacer and washer sets can be
  printed together using 0.2 mm layer heights; structural parts benefit from 0.28 mm layers for
  speed.
- Standardize on heat-set inserts when available; switch to the `printed` standoff mode for rapid
  prototyping or when inserts are out of stock.
- Label printed parts (e.g., with embossed axis letters) during slicing to reduce assembly errors.

## Simplification opportunities

- **Spacer/washer consolidation:** The spacer and washer share geometry—prefer the spacer model and
  vary `thickness` to eliminate redundant inventory.
- **Integrated yarn guide and tension post:** When only a single yarn path is needed, print the yarn
  guide with the tension post by enabling the `integrated_post` parameter (to be added) and remove
  two fasteners from the stack.
- **Stepper mount datum tabs:** Print datum tabs directly on the mount rather than using alignment
  pins when the frame is square; this removes two separate pins per axis.
- **Electronics sled:** Replace individual brackets with a single electronics sled that slides into
  2020 extrusion, reducing assembly time and cable strain.

Document deviations from these simplifications when testing multi-yarn or multi-axis variants so the
trade-offs remain visible to firmware and tooling contributors.

## Firmware alignment

- Firmware should expose a JSON or YAML profile describing microstepping, steps-per-mm, and travel
  limits for each axis so pattern planners can consume the data directly.
- Home-before-run is required; the pattern CLI can block execution if limit switch states are
  unknown.
- Maintain a shared definition of carriage payload mass for acceleration planning (target ≤250 g).

Use [`wove.pattern_cli`](pattern-cli.md) to translate stitch descriptions into motion commands while
the firmware matures. The CLI illustrates how textual patterns map to coordinated gantry moves and
highlights when hardware changes require planner updates.

## Risks, open questions, and follow-up

- Validate whether PETG provides sufficient stiffness for the tension subsystem or if CF-Nylon is
  required for higher-tension yarns.
- Investigate limit switch mounting that avoids exposed fasteners near the yarn path.
- Prototype the integrated yarn guide/tension post option and record torque measurements to ensure
  no loss of yarn control.
- Define electrical connector standards (e.g., JST-XH vs. MicroFit) to simplify wiring harnesses.

Capture findings in the corresponding module READMEs or CAD comments so future contributors inherit
the rationale behind changes.
