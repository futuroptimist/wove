// Alignment pin for assembly positioning
// Parameters: diameter, height, and optional chamfer
$fn = 100;
module alignment_pin(d=5, h=20, chamfer=0) {
    if (chamfer > 0 && chamfer < h) {
        // Main body minus chamfer height
        cylinder(d=d, h=h - chamfer);
        // Tapered chamfer at the top
        translate([0, 0, h - chamfer])
            cylinder(d1=d, d2=d - 2 * chamfer, h=chamfer);
    } else {
        cylinder(d=d, h=h);
    }
}

alignment_pin(chamfer=1);
