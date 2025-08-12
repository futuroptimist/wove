// Alignment pin to position stacked components
// diameter: overall pin diameter
// length: overall pin length
// chamfer: size of conical tip
module alignment_pin(diameter=5, length=20, chamfer=1) {
    union() {
        // main shaft
        translate([0, 0, chamfer])
            cylinder(d=diameter, h=length - chamfer);
        // tapered tip
        cylinder(d1=0, d2=diameter, h=chamfer);
    }
}

alignment_pin();
