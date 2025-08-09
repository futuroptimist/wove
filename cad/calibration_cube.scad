// Calibration cube: customizable test block for printer calibration
// size: edge length of cube in millimeters
module calibration_cube(size=20) {
    cube([size, size, size]);
}

calibration_cube();
