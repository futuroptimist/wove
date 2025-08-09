// Simple cylindrical spacer for hardware prototypes
// chamfer: size of edge bevel; ensure height >= 2*chamfer
module spacer(outer_diameter=10, inner_diameter=5, height=5, chamfer=1) {
    difference() {
        union() {
            // main body
            translate([0, 0, chamfer])
                cylinder(d=outer_diameter - 2 * chamfer, h=height - 2 * chamfer);
            // bottom chamfer
            cylinder(d1=outer_diameter - 2 * chamfer, d2=outer_diameter, h=chamfer);
            // top chamfer
            translate([0, 0, height - chamfer])
                cylinder(d1=outer_diameter, d2=outer_diameter - 2 * chamfer, h=chamfer);
        }
        // inner hole
        cylinder(d=inner_diameter, h=height);
    }
}

spacer();
