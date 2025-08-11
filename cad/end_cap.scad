// End cap with optional chamfer to smooth edges
// chamfer: size of edge bevel; ensure height >= 2*chamfer
module end_cap(outer_diameter=20, inner_diameter=10, height=5, chamfer=1) {
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

end_cap();
