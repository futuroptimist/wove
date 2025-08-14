// Alignment pin for assembly positioning
// Parameters: diameter, height, and optional taper
$fn = 100;
mode = is_undef(STANDOFF_MODE) ? "heatset" : STANDOFF_MODE;

module alignment_pin(d=5, h=20, tip=1) {
    if (mode == "printed") {
        cylinder(d = d, h = h);
    } else {
        // heatset mode: taper to ease insertion
        cylinder(h = h, d1 = d, d2 = d - tip);
    }
}

alignment_pin();
