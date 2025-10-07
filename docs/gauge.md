# Gauge utilities

The `wove.gauge` module provides helpers for calculating stitch and row gauge,
including direct helpers for inches, centimeters, yards, and meters. It also
converts measurements between these units and estimates the number of stitches
or rows needed for a given dimension. Use
`stitches_for_inches`, `stitches_for_cm`, `stitches_for_yards`, or
`stitches_for_meters` to calculate how many stitches a project requires. Use
`inches_for_stitches`, `cm_for_stitches`, `yards_for_stitches`, or
`meters_for_stitches` to determine width from a stitch count. Use
`rows_for_inches`, `rows_for_cm`, `rows_for_yards`, or `rows_for_meters` to find
the row count for a desired height, or `inches_for_rows`, `cm_for_rows`,
`yards_for_rows`, and `meters_for_rows` to convert a row count back to height.

Direct helpers such as `meters_to_cm`, `cm_to_meters`, `meters_to_inches`, and
`inches_to_meters` keep metric conversions straightforward without chaining
multiple functions. Gauge conversion helpers (`per_inch_to_per_cm`,
`per_cm_to_per_inch`, `per_inch_to_per_yard`, `per_yard_to_per_inch`,
`per_inch_to_per_meter`, `per_meter_to_per_inch`, `per_cm_to_per_meter`,
`per_meter_to_per_cm`, `per_cm_to_per_yard`, `per_yard_to_per_cm`,
`per_yard_to_per_meter`, and `per_meter_to_per_yard`) translate stitches- or
rows-per-unit values across inches, centimeters, yards, and meters.

Values ending in `.5` are rounded up when using `stitches_for_inches`,
`stitches_for_cm`, `stitches_for_yards`, `stitches_for_meters`,
`rows_for_inches`, `rows_for_cm`, `rows_for_yards`, or `rows_for_meters`.
Use `width_difference_for_stitches` or `height_difference_for_rows` to
quantify how an off-gauge swatch will change a project's finished size.

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
    per_cm_to_per_meter,
    per_cm_to_per_yard,
    per_inch_to_per_meter,
    per_inch_to_per_yard,
    per_meter_to_per_cm,
    per_meter_to_per_inch,
    per_meter_to_per_yard,
    stitches_per_yard,
    rows_per_yard,
    stitches_per_meter,
    rows_per_meter,
    stitches_for_inches,
    stitches_for_cm,
    stitches_for_yards,
    stitches_for_meters,
    inches_for_rows,
    cm_for_rows,
    yards_for_rows,
    meters_for_rows,
    inches_for_stitches,
    cm_for_stitches,
    yards_for_stitches,
    meters_for_stitches,
    height_difference_for_rows,
    rows_for_inches,
    rows_for_cm,
    rows_for_yards,
    rows_for_meters,
    inches_to_cm,
    cm_to_inches,
    meters_to_cm,
    cm_to_meters,
    yards_to_inches,
    inches_to_yards,
    yards_to_cm,
    cm_to_yards,
    yards_to_meters,
    meters_to_yards,
    meters_to_inches,
    inches_to_meters,
    per_yard_to_per_cm,
    per_yard_to_per_inch,
    per_yard_to_per_meter,
    width_difference_for_stitches,
)

stitches_per_inch(20, 4)   # 5.0 stitches per inch
rows_per_inch(30, 4)       # 7.5 rows per inch
stitches_per_cm(20, 10)    # 2.0 stitches per cm
rows_per_cm(30, 10)        # 3.0 rows per cm
stitches_per_yard(450, 5)  # 90.0 stitches per yard
rows_per_yard(800, 10)     # 80.0 rows per yard
stitches_per_meter(300, 3) # 100.0 stitches per meter
rows_per_meter(250, 2.5)   # 100.0 rows per meter
per_cm_to_per_inch(2.0)    # 5.08
per_inch_to_per_cm(5.08)   # ~2.0 per cm
per_inch_to_per_yard(5.0)      # 180.0 per yard
per_yard_to_per_inch(180.0)    # 5.0 per inch
per_inch_to_per_meter(5.0)     # ~196.85 per meter
per_meter_to_per_inch(196.8503937)  # ~5.0 per inch
per_cm_to_per_meter(2.0)       # 200.0 per meter
per_meter_to_per_cm(200.0)     # 2.0 per cm
per_cm_to_per_yard(2.0)        # ~182.88 per yard
per_yard_to_per_cm(182.88)     # ~2.0 per cm
per_yard_to_per_meter(180.0)   # ~196.85 per meter
per_meter_to_per_yard(196.8503937)  # ~180.0 per yard
rows_for_inches(7.5, 4)      # 30 rows
rows_for_cm(3.0, 10)         # 30 rows
rows_for_yards(270, 0.1)     # 27 rows
rows_for_meters(100, 0.25)   # 25 rows
inches_for_rows(30, 7.5)     # 4.0 inches for 30 rows
cm_for_rows(30, 3.0)         # 10.0 cm for 30 rows
yards_for_rows(36, 120)      # 0.3 yards for 36 rows
meters_for_rows(400, 400)    # 1.0 meter for 400 rows
width_difference_for_stitches(180, 20, 22)  # ~-0.82 units (narrower fabric)
height_difference_for_rows(220, 30, 28)     # ~0.52 units (taller fabric)
stitches_for_inches(5.0, 7)   # 35 stitches for 7 in width
stitches_for_cm(2.0, 10)      # 20 stitches for 10 cm width
stitches_for_yards(180, 0.25) # 45 stitches for 0.25 yards
stitches_for_meters(120, 0.3) # 36 stitches for 0.3 meters
inches_for_stitches(35, 5.0)  # 7.0 inches for 35 stitches
cm_for_stitches(20, 2.0)      # 10.0 cm for 20 stitches
yards_for_stitches(90, 360)   # 0.25 yards for 90 stitches
meters_for_stitches(200, 200) # 1.0 meter for 200 stitches
inches_to_cm(1.0)            # 2.54 cm
cm_to_inches(2.54)          # 1.0 inch
meters_to_cm(1.5)           # 150.0 cm
cm_to_meters(123)           # 1.23 meters
yards_to_inches(1.0)         # 36.0 inches
inches_to_yards(36.0)        # ~1.0 yard
yards_to_cm(1.0)             # 91.44 cm
cm_to_yards(91.44)           # ~1.0 yard
yards_to_meters(1.0)         # 0.9144 meters
meters_to_yards(0.9144)      # ~1.0 yard
meters_to_inches(1.0)        # ~39.37 inches
inches_to_meters(39.37007874)  # ~1.0 meter
```

Each function checks that its inputs are positive and raises `ValueError`
when an invalid value is supplied.
