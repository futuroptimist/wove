// Simple cylindrical spacer for hardware prototypes
module spacer(outer_diameter=10, inner_diameter=5, height=5) {
    difference() {
        cylinder(d=outer_diameter, h=height);
        cylinder(d=inner_diameter, h=height);
    }
}

spacer();
