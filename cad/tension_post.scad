// Vertical post with base for maintaining yarn tension
// post_diameter: diameter of the upright post
// post_height: height of the post
// base_diameter: diameter of the base disk
// base_height: thickness of the base
module tension_post(post_diameter=5, post_height=20, base_diameter=10, base_height=3) {
    union() {
        // base disk
        cylinder(d=base_diameter, h=base_height);
        // vertical post
        translate([0, 0, base_height])
            cylinder(d=post_diameter, h=post_height);
    }
}

tension_post();
