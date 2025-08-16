# Gauge utilities

The `wove.gauge` module provides helpers for calculating stitch and row gauge,
converting measurements between inches and centimeters, and estimating the
number of stitches needed for a given width. Use `stitches_for_inches` or
`stitches_for_cm` to calculate how many stitches a project requires.

To calculate gauge:

1. Knit a swatch at least 4 in (10 cm) square.
2. Block the swatch and lay it flat to relax the stitches.
3. Measure in the middle of the swatch and count stitches across and rows down.
4. Pass those counts and measurements to the helper functions shown below.
5. Use `stitches_for_inches` or `stitches_for_cm` to estimate your cast-on.

```python
from wove import (
    stitches_per_inch,
    rows_per_inch,
    stitches_per_cm,
    rows_per_cm,
    per_cm_to_per_inch,
    per_inch_to_per_cm,
    stitches_for_inches,
    stitches_for_cm,
    rows_for_inches,
    rows_for_cm,
)

stitches_per_inch(20, 4)   # 5.0 stitches per inch
rows_per_inch(30, 4)       # 7.5 rows per inch
stitches_per_cm(20, 10)    # 2.0 stitches per cm
rows_per_cm(30, 10)        # 3.0 rows per cm
per_cm_to_per_inch(2.0)    # 5.08
per_inch_to_per_cm(5.08)   # ~2.0 per cm
rows_for_inches(7.5, 4)      # 30 rows
rows_for_cm(3.0, 10)         # 30 rows
stitches_for_inches(5.0, 7)   # 35 stitches for 7 in width
stitches_for_cm(2.0, 10)      # 20 stitches for 10 cm width
```

Each function checks that its inputs are positive and raises `ValueError`
when an invalid value is supplied.
