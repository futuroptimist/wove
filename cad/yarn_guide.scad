// Yarn guide ring with optional integrated tension post
module yarn_guide(
    radius=10,
    thickness=2,
    slot_width=4,
    ring_height=5,
    integrated_post=false,
    post_diameter=5,
    post_height=20,
    base_diameter=14,
    base_height=4,
    post_offset=undef
) {
    outer_radius = radius + thickness;
    slot_height = ring_height + 2;
    offset = is_undef(post_offset)
        ? outer_radius + base_diameter / 2
        : post_offset;

    module ring() {
        difference() {
            cylinder(h=ring_height, r=outer_radius);
            cylinder(h=ring_height, r=radius);
            translate([radius, -slot_width / 2, -1])
                cube([outer_radius, slot_width, slot_height]);
        }
    }

    module integrated_post_body() {
        translate([offset, 0, 0]) {
            cylinder(h=base_height, d=base_diameter);
            translate([0, 0, base_height])
                cylinder(h=post_height, d=post_diameter);
        }
    }

    if (integrated_post) {
        union() {
            ring();
            integrated_post_body();
        }
    } else {
        ring();
    }
}

yarn_guide();
