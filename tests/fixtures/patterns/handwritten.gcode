G21 ; use millimeters
G90 ; absolute positioning
G92 X0.00 Y0.00 Z4.00 E0 ; zero axes
G1 Z-1.50 F600 ; chain stitch 1 of 3: plunge
G1 E0.50 F300 ; chain stitch 1 of 3: feed yarn
G1 Z4.00 F600 ; chain stitch 1 of 3: raise
G0 X5.00 Y0.00 F1200 ; chain stitch 1 of 3: advance
G1 Z-1.50 F600 ; chain stitch 2 of 3: plunge
G1 E1.00 F300 ; chain stitch 2 of 3: feed yarn
G1 Z4.00 F600 ; chain stitch 2 of 3: raise
G0 X10.00 Y0.00 F1200 ; chain stitch 2 of 3: advance
G1 Z-1.50 F600 ; chain stitch 3 of 3: plunge
G1 E1.50 F300 ; chain stitch 3 of 3: feed yarn
G1 Z4.00 F600 ; chain stitch 3 of 3: raise
G0 X15.00 Y0.00 F1200 ; chain stitch 3 of 3: advance
G4 P250 ; pause for 0.250 s
G0 X15.00 Y8.00 F1200 ; reposition
G0 X0.00 Y14.50 F1200 ; turn to next row
G1 Z-2.00 F600 ; single stitch 1 of 2: plunge
G1 E2.10 F300 ; single stitch 1 of 2: feed yarn
G1 Z4.00 F600 ; single stitch 1 of 2: raise
G0 X4.50 Y14.50 F1200 ; single stitch 1 of 2: advance
G1 Z-2.00 F600 ; single stitch 2 of 2: plunge
G1 E2.70 F300 ; single stitch 2 of 2: feed yarn
G1 Z4.00 F600 ; single stitch 2 of 2: raise
G0 X9.00 Y14.50 F1200 ; single stitch 2 of 2: advance
