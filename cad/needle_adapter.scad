// Adapter for holding a knitting needle
// clearance: extra space added to the needle diameter for easier insertion
module needle_adapter(needle_diameter=3, length=40, clearance=0.2) {
    difference() {
        cylinder(d=needle_diameter + 2, h=length);
        cylinder(d=needle_diameter + clearance, h=length);
    }
}

needle_adapter();
