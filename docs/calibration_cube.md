# Calibration Cube

The `cad/calibration_cube.scad` module generates a parametric calibration block for 3D printer tuning.
Adjust the `size` parameter to change the cube's edge length (default 20 mm):

```scad
calibration_cube(size=25);
```

Use the OpenSCAD render script to export STL files for both heatset and printed standoff modes.
