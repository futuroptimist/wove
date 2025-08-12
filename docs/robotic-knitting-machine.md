# Robotic Knitting Machine Overview

The long-term goal of this project is to develop a DIY robotic system that automates knitting. Components are modeled in OpenSCAD and live in the `cad/` directory.

## Planned Modules
- **Needle adapter** – holds a standard needle with adjustable clearance and connects to a
  stepper-driven carriage.
- **Stepper mount** – secures a motor for precise control.
- **Carriage** – moves the working yarn and needles and includes a center hole for mounting hardware.
- **Spacer** – maintains consistent gaps between components and now includes an
  optional chamfer for smoother stacking.
- **Calibration cube** – simple 20 mm block with a center hole for printer
  calibration and bridging tests.
- **Washer** – flat ring for spacing hardware components with an optional chamfer for smoother edges.
- **Yarn guide** – directs yarn through the system and helps maintain tension.
- **Tension post** – vertical pin with a base to anchor yarn tension.
- **End cap** – covers rod ends to prevent snagging and now includes an optional
  chamfer for smoother edges.
- **Alignment pin** – 5 mm cylinder for aligning stacked components.

Generated G-code or custom instructions will drive these parts to knit automatically.
