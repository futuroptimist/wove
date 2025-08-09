// Simple yarn guide ring with slot for threading
module yarn_guide(radius=10, thickness=2, slot_width=4) {
    difference() {
        cylinder(h=5, r=radius + thickness);
        cylinder(h=5, r=radius);
        translate([radius, -slot_width/2, -1])
            cube([radius + thickness, slot_width, 7]);
    }
}

yarn_guide();
