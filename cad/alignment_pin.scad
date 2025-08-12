// Alignment pin for assembly positioning
// Parameters: diameter and height
$fn = 100;
module alignment_pin(d=5, h=20) {
    cylinder(d=d, h=h);
}

alignment_pin();
