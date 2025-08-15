# Gauge utilities

The `wove.gauge` module provides helpers for calculating stitch and row gauge and
converting measurements between inches and centimeters.

To calculate gauge:

1. Knit a swatch at least 4 in (10 cm) square.
2. Block the swatch and lay it flat to relax the stitches.
3. Measure in the middle of the swatch and count stitches across and rows down.
4. Pass those counts and measurements to the helper functions shown below.

```python
from wove import (
    stitches_per_inch,
    rows_per_inch,
    stitches_per_cm,
    rows_per_cm,
    per_cm_to_per_inch,
    per_inch_to_per_cm,
)

stitches_per_inch(20, 4)   # 5.0 stitches per inch
rows_per_inch(30, 4)       # 7.5 rows per inch
stitches_per_cm(20, 10)    # 2.0 stitches per cm
rows_per_cm(30, 10)        # 3.0 rows per cm
per_cm_to_per_inch(2.0)    # 5.08
per_inch_to_per_cm(5.08)   # ~2.0 per cm
```

Each function checks that its inputs are positive and raises `ValueError`
when an invalid value is supplied.
