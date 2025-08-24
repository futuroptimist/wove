/* mounting_bracket.scad
 * Simple L-shaped bracket for test assemblies.
 */
module mounting_bracket(thickness=3, length=20, height=10, width=20) {
    difference() {
        union() {
            cube([length, width, thickness]);
            translate([0, 0, thickness]) cube([thickness, width, height]);
        }
        translate([length/2, width/2, 0])
            cylinder(h=thickness, d=3, center=false);
    }
}

mounting_bracket();
