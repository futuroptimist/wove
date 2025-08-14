// Simple rectangular mounting bracket with two holes
// edge_offset: distance from each hole center to the bracket edge
module mounting_bracket(length=40, width=20, thickness=4, hole_d=5, edge_offset=10) {
    difference() {
        cube([length, width, thickness]);
        translate([edge_offset, width/2, 0])
            cylinder(d=hole_d, h=thickness + 1);
        translate([length - edge_offset, width/2, 0])
            cylinder(d=hole_d, h=thickness + 1);
    }
}

mounting_bracket();
