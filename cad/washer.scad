// Flat washer for general spacing
// outer_diameter: overall diameter
// inner_diameter: hole diameter
// thickness: washer height
// chamfer: size of edge bevel; ensure thickness >= 2*chamfer
module washer(outer_diameter=20, inner_diameter=10, thickness=2, chamfer=0) {
    difference() {
        union() {
            // main body
            translate([0, 0, chamfer])
                cylinder(d=outer_diameter - 2 * chamfer, h=thickness - 2 * chamfer);
            if (chamfer > 0) {
                // bottom chamfer
                cylinder(d1=outer_diameter - 2 * chamfer, d2=outer_diameter, h=chamfer);
                // top chamfer
                translate([0, 0, thickness - chamfer])
                    cylinder(d1=outer_diameter, d2=outer_diameter - 2 * chamfer, h=chamfer);
            }
        }
        // inner hole
        cylinder(d=inner_diameter, h=thickness);
    }
}

washer();
