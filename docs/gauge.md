# Gauge utilities

The `wove.gauge` module provides helpers for calculating stitch and row gauge,
converting measurements between inches and centimeters, and estimating the
number of stitches needed for a given width.

To calculate gauge:

1. Knit a swatch at least 4 in (10 cm) square.
2. Measure a section of the swatch and count the stitches across and rows down.
3. Pass those counts and measurements to the helper functions shown below.

```python
from wove import (
    per_cm_to_per_inch,
    rows_per_inch,
    stitches_for_cm,
    stitches_for_inches,
    stitches_per_inch,
)

stitches_per_inch(20, 4)     # 5.0 stitches per inch
rows_per_inch(30, 4)         # 7.5 rows per inch
per_cm_to_per_inch(2.0)      # 5.08
stitches_for_inches(5.0, 4)  # 20 stitches
stitches_for_cm(2.0, 10)     # 20 stitches
```

Each function checks that its inputs are positive and raises `ValueError`
when an invalid value is supplied.
