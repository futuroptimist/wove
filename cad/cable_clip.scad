$fn=64;
module cable_clip(radius=5, thickness=2, width=5) {
  difference() {
    // outer ring
    translate([0,0,0])
      rotate([90,0,0])
      cylinder(h=width, r=radius+thickness, center=true);
    // inner cutout
    translate([0,0,0])
      rotate([90,0,0])
      cylinder(h=width+2, r=radius, center=true);
    // opening slot
    translate([radius,0,0])
      cube([radius*2, radius*2, width*2], center=true);
  }
}

cable_clip();
