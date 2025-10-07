# Robotic Knitting Machine Overview

The long-term goal of this project is to develop a DIY robotic system that automates knitting.
Components are modeled in [OpenSCAD](https://openscad.org) and live in the `cad/` directory.
Open any `.scad` file in OpenSCAD, press **F6** to render, then export the part as an STL for
printing.

## Planned Modules
- **Needle adapter** – holds a standard needle with adjustable clearance and connects to a
  stepper-driven carriage.
- **Stepper mount** – secures a motor for precise control with adjustable screw spacing
  (set `hole_spacing`, defaulting to 31 mm for NEMA17).
- **Carriage** – moves the working yarn and needles and includes a center hole for mounting
  hardware.
- **Mounting bracket** – simple L-shaped bracket for test assemblies.
- **Spacer** – maintains consistent gaps between components and now includes an
  optional chamfer for smoother stacking.
- **Calibration cube** – simple 20 mm block with a center hole for printer
  calibration and bridging tests.
- **Washer** – flat ring for spacing hardware components with an optional chamfer for
  smoother edges.
- **Yarn guide** – directs yarn through the system and helps maintain tension.
- **Tension post** – vertical pin with a base to anchor yarn tension.
  Switch `STANDOFF_MODE` between ``heatset`` (cutouts for inserts) and ``printed``
  (solid posts) before exporting.
- **End cap** – covers rod ends to prevent snagging and now includes an optional
  chamfer for smoother edges.
- **Alignment pin** – 5 mm cylinder for aligning stacked components with an optional
  chamfer for easier insertion.
- **Hook** – L-shaped hook for hanging lightweight accessories.

## Exporting models

Use `./scripts/build_stl.sh <file.scad>` to convert any module in `cad/` to a matching STL.
The wrapper delegates to `python -m wove.build_stl <file.scad>` so both commands behave identically.
Run the script without arguments to update every model while skipping up-to-date outputs.
Store the exported models alongside their sources to keep hardware and code in sync.

Generated G-code or custom instructions will drive these parts to knit automatically.
