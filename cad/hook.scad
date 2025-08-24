// Simple L-shaped hook for mounting
// width: thickness of the hook
// depth: horizontal reach from the mount
// height: vertical height of the hook
module hook(width=5, depth=20, height=30) {
    union() {
        // vertical base
        cube([width, width, height]);
        // horizontal arm
        translate([0, width, 0])
            cube([width, depth - width, width]);
        // vertical tip to hold items
        translate([0, depth - width, width])
            cube([width, width, height - width]);
    }
}

hook();
