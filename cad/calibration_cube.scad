// Calibration cube: 20 mm test block with optional center hole
module calibration_cube(size=20, hole_diameter=5) {
    difference() {
        cube([size, size, size], center=true);
        cylinder(h=size + 2, d=hole_diameter, center=true);
    }
}

calibration_cube();
