# Knitting Basics

This guide introduces the fundamentals of hand knitting with two standard needles.

## Materials
- A pair of straight knitting needles sized for your yarn
- Worsted-weight yarn

## First Steps
1. **Cast on** a row of stitches.
2. Practice the **knit stitch** to create a simple fabric.
3. Learn the **purl stitch** to add texture.
4. **Bind off** to finish your piece.

## Measuring Gauge

Knit a small swatch (at least 4 in / 10 cm square), block it, then measure
the stitches across and rows down in the center. Use the
[gauge utilities](gauge.md) to convert between units or estimate how many
stitches you need for a project.

Continue experimenting with gauge and patterns as you grow more comfortable.

```python
from wove import (
    cm_to_inches,
    inches_to_cm,
    per_cm_to_per_inch,
    per_inch_to_per_cm,
    rows_per_cm,
    rows_per_inch,
    stitches_per_cm,
    stitches_per_inch,
)

stitches_per_inch(20, 4)  # 5.0 stitches per inch
rows_per_inch(30, 4)  # 7.5 rows per inch
stitches_per_cm(20, 10)  # 2.0 stitches per cm
rows_per_cm(30, 10)  # 3.0 rows per cm
per_inch_to_per_cm(5.08)  # ~2.0 per cm
per_cm_to_per_inch(2.0)  # ~5.08 per inch
inches_to_cm(1)  # 2.54 cm
cm_to_inches(2.54)  # 1.0 in
```

All gauge helpers require positive stitch and row counts and positive measurements.
Passing non-positive values raises ``ValueError``. Unit conversion helpers accept
non-negative values and raise ``ValueError`` for negatives.
