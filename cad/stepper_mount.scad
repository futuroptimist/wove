// Mount for NEMA17 stepper motor
module stepper_mount(width=42, depth=42, height=10) {
    difference() {
        cube([width, depth, height]);
        translate([width/2, depth/2, 0])
            cylinder(d=22, h=height);
    }
}

stepper_mount();
