# CAD module overview

The `cad/` directory contains parametric OpenSCAD sources for the prototype knitting hardware.
Each module ships with a matching STL in `stl/` and can be regenerated when parameters change.
Use `scripts/build_stl.sh` for a quick render or `scripts/openscad_render.sh` to select the
standoff mode.

```bash
# Render the spacer with default parameters
./scripts/build_stl.sh cad/spacer.scad

# Render the tension post with printed standoffs
STANDOFF_MODE=printed ./scripts/openscad_render.sh cad/tension_post.scad
```

## Modules

- `alignment_pin`: Alignment pin with an optional chamfer for easier stacking.
- `calibration_cube`: 20 mm cube with a center hole for printer tuning.
- `carriage`: Carriage body that carries yarn guides or tools during experiments.
- `end_cap`: Cap that covers rod ends; match `inner_diameter` to your hardware.
- `hook`: L-shaped hook for hanging lightweight tools or yarn.
- `mounting_bracket`: L-bracket for attaching assemblies to a base surface.
- `needle_adapter`: Sleeve that grips a knitting needle.
  Raise `clearance` if insertion feels tight.
- `spacer`: Cylindrical spacer with an optional chamfer.
  Ensure `height >= 2 * chamfer` before rendering.
- `stepper_mount`: Plate that positions a stepper motor with editable hole spacing.
- `tension_post`: Upright post that manages yarn tension and pairs with the yarn guide.
- `washer`: Flat washer with optional chamfers for smoother edges.
- `yarn_guide`: Routes yarn through the carriage.
  Adjust the loop to match the yarn weight.

Open any `.scad` file in the OpenSCAD GUI to preview geometry or tweak parameters. After editing,
rebuild the STL so downstream assemblies stay accurate.
