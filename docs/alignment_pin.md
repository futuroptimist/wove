# Alignment pin

Simple cylindrical pin used to align parts during assembly.

The OpenSCAD source `cad/alignment_pin.scad` supports two render modes:

- **heatset** (default): adds a slight taper to aid installation with heat-set inserts.
- **printed**: renders a straight pin for direct 3D printing.

Render the models with:

```
bash scripts/openscad_render.sh cad/alignment_pin.scad
STANDOFF_MODE=printed bash scripts/openscad_render.sh cad/alignment_pin.scad
```

The STL files are generated in `stl/` but are not committed to the repository.
