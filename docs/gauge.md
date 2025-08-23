# Gauge utilities

The `wove.gauge` module provides helpers for calculating stitch and row gauge,
converting measurements between inches, centimeters, yards, and meters, and
estimating the number of stitches needed for a given width. Use
`stitches_for_inches` or `stitches_for_cm` to calculate how many stitches a
project requires, or `inches_for_stitches` and `cm_for_stitches` to determine
width from a stitch count. Use `inches_for_rows` and `cm_for_rows` to convert a
row count back to height.

Values ending in `.5` are rounded up when using `stitches_for_inches`,
`stitches_for_cm`, `rows_for_inches`, or `rows_for_cm`.

To calculate gauge:

1. Knit a swatch at least 4 in (10 cm) square.
2. Block the swatch and lay it flat to relax the stitches.
3. Measure in the middle of the swatch and count stitches across and rows down.
4. Pass those counts and measurements to the helper functions shown below.
5. Use `stitches_for_inches` or `stitches_for_cm` to estimate your cast-on, or
   `inches_for_stitches`/`cm_for_stitches` to check a pattern's finished size.

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
    inches_for_rows,
    cm_for_rows,
    inches_for_stitches,
    cm_for_stitches,
    rows_for_inches,
    rows_for_cm,
    yards_to_inches,
    inches_to_yards,
    yards_to_meters,
    meters_to_yards,
)

stitches_per_inch(20, 4)   # 5.0 stitches per inch
rows_per_inch(30, 4)       # 7.5 rows per inch
stitches_per_cm(20, 10)    # 2.0 stitches per cm
rows_per_cm(30, 10)        # 3.0 rows per cm
per_cm_to_per_inch(2.0)    # 5.08
per_inch_to_per_cm(5.08)   # ~2.0 per cm
rows_for_inches(7.5, 4)      # 30 rows
rows_for_cm(3.0, 10)         # 30 rows
inches_for_rows(30, 7.5)     # 4.0 inches for 30 rows
cm_for_rows(30, 3.0)         # 10.0 cm for 30 rows
stitches_for_inches(5.0, 7)   # 35 stitches for 7 in width
stitches_for_cm(2.0, 10)      # 20 stitches for 10 cm width
inches_for_stitches(35, 5.0)  # 7.0 inches for 35 stitches
cm_for_stitches(20, 2.0)      # 10.0 cm for 20 stitches
yards_to_inches(1.0)         # 36.0 inches
inches_to_yards(36.0)        # ~1.0 yard
yards_to_meters(1.0)         # 0.9144 meters
meters_to_yards(0.9144)      # ~1.0 yard
```

Each function checks that its inputs are positive and raises `ValueError`
when an invalid value is supplied.
