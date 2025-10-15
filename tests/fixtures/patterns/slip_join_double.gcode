G21 ; use millimeters
G90 ; absolute positioning
G92 X0.00 Y0.00 Z4.00 E0 ; zero axes
G1 Z-1.00 F600 ; slip stitch 1 of 2: plunge
G1 E0.30 F300 ; slip stitch 1 of 2: feed yarn
G1 Z4.00 F600 ; slip stitch 1 of 2: raise
G0 X3.50 Y0.00 F1200 ; slip stitch 1 of 2: advance
G1 Z-1.00 F600 ; slip stitch 2 of 2: plunge
G1 E0.60 F300 ; slip stitch 2 of 2: feed yarn
G1 Z4.00 F600 ; slip stitch 2 of 2: raise
G0 X7.00 Y0.00 F1200 ; slip stitch 2 of 2: advance
G1 Z-1.50 F600 ; chain stitch 1 of 1: plunge
G1 E1.10 F300 ; chain stitch 1 of 1: feed yarn
G1 Z4.00 F600 ; chain stitch 1 of 1: raise
G0 X12.00 Y0.00 F1200 ; chain stitch 1 of 1: advance
G0 X0.00 Y5.50 F1200 ; turn to next row
G1 Z-2.50 F600 ; double stitch 1 of 2: plunge
G1 E1.80 F300 ; double stitch 1 of 2: feed yarn
G1 Z4.00 F600 ; double stitch 1 of 2: raise
G0 X5.50 Y5.50 F1200 ; double stitch 1 of 2: advance
G1 Z-2.50 F600 ; double stitch 2 of 2: plunge
G1 E2.50 F300 ; double stitch 2 of 2: feed yarn
G1 Z4.00 F600 ; double stitch 2 of 2: raise
G0 X11.00 Y5.50 F1200 ; double stitch 2 of 2: advance
