// Vertical post with base for maintaining yarn tension
// Switch between heat-set inserts and printed standoffs by setting STANDOFF_MODE.
mode = is_undef(STANDOFF_MODE) ? "heatset" : STANDOFF_MODE;

module standoff_positions(offset=4, count=3) {
    for (i = [0 : count - 1]) {
        angle = 360 / count * i;
        rotate([0, 0, angle]) translate([offset, 0, 0]) children();
    }
}

// post_diameter: diameter of the upright post
// post_height: height of the post
// base_diameter: diameter of the base disk
// base_height: thickness of the base
// standoff_diameter: diameter for inserts or printed standoffs
// standoff_height: height of printed standoffs above the base
// standoff_offset: distance of standoffs from the center
// standoff_count: number of standoffs arranged radially
module tension_post(
    post_diameter=5,
    post_height=20,
    base_diameter=10,
    base_height=3,
    standoff_diameter=3,
    standoff_height=4,
    standoff_offset=4,
    standoff_count=3
) {
    module base_body() {
        cylinder(d=base_diameter, h=base_height);
    }

    module heatset_cutouts() {
        standoff_positions(standoff_offset, standoff_count)
            cylinder(d=standoff_diameter, h=base_height);
    }

    module printed_standoffs() {
        standoff_positions(standoff_offset, standoff_count)
            translate([0, 0, base_height])
            cylinder(d=standoff_diameter, h=standoff_height);
    }

    union() {
        if (mode == "printed") {
            union() {
                base_body();
                printed_standoffs();
            }
        } else {
            difference() {
                base_body();
                heatset_cutouts();
            }
        }

        translate([0, 0, base_height])
            cylinder(d=post_diameter, h=post_height);
    }
}

tension_post();
