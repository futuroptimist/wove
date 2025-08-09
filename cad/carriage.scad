// Simple carriage that can slide along rails
// Now includes a central mounting hole
module carriage(width=60, depth=20, height=10, hole_diameter=5) {
    difference() {
        cube([width, depth, height]);
        // Central hole for attaching hardware
        translate([width/2, depth/2, 0])
            cylinder(d=hole_diameter, h=height);
    }
}

carriage();
