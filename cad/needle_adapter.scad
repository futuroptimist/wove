// Adapter for holding a knitting needle
module needle_adapter(needle_diameter=3, length=40) {
    difference() {
        cylinder(d=needle_diameter + 2, h=length);
        cylinder(d=needle_diameter, h=length);
    }
}

needle_adapter();
