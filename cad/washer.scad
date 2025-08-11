// Flat washer for general spacing
// outer_diameter: overall diameter
// inner_diameter: hole diameter
// thickness: washer height
module washer(outer_diameter=20, inner_diameter=10, thickness=2) {
    difference() {
        // outer disc
        cylinder(d=outer_diameter, h=thickness);
        // inner hole
        cylinder(d=inner_diameter, h=thickness);
    }
}

washer();
