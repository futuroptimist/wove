// Mount for NEMA17 stepper motor with configurable mounting holes
// width/depth/height: dimensions of the rectangular plate
// motor_hole_diameter: diameter of the central motor opening
// hole_spacing: center-to-center distance between mounting holes
// hole_diameter: diameter of the screw mounting holes
module stepper_mount(
    width=60,
    depth=60,
    height=6,
    motor_hole_diameter=22,
    hole_spacing=31,
    hole_diameter=3.5
) {
    difference() {
        cube([width, depth, height]);
        // Central hole for the motor shaft and boss
        translate([width/2, depth/2, 0])
            cylinder(d=motor_hole_diameter, h=height);
        // Corner mounting holes positioned symmetrically around the center
        for (x_sign = [-1, 1]) {
            for (y_sign = [-1, 1]) {
                translate([
                    width/2 + x_sign * hole_spacing / 2,
                    depth/2 + y_sign * hole_spacing / 2,
                    0
                ])
                    cylinder(d=hole_diameter, h=height);
            }
        }
    }
}

stepper_mount();
