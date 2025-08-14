# Gauge utilities

The `wove.gauge` module provides helpers for calculating stitch and row gauge and
converting measurements between inches and centimeters.

To calculate gauge:

1. Knit a swatch at least 4 in (10 cm) square.
2. Measure a section of the swatch and count the stitches across and rows down.
3. Pass those counts and measurements to the helper functions shown below.

```python
from wove import (
    stitches_per_inch,
    rows_per_inch,
    per_cm_to_per_inch,
)

stitches_per_inch(20, 4)  # 5.0 stitches per inch
rows_per_inch(30, 4)      # 7.5 rows per inch
per_cm_to_per_inch(2.0)   # 5.08
```

Each function checks that its inputs are positive and raises `ValueError`
when an invalid value is supplied.
