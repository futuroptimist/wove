# Knitting Basics

This guide introduces the fundamentals of hand knitting with two
standard needles.

## Materials
- A pair of straight knitting needles sized for your yarn
- Worsted-weight yarn

## First Steps
1. **Cast on** a row of stitches.
2. Practice the **knit stitch** to create a simple fabric.
3. Learn the **purl stitch** to add texture.
4. **Bind off** to finish your piece.

## Gauge

Gauge keeps your project at the intended size; even small stitch differences
can grow into inches on larger pieces. Swatching ensures your fabric matches
the pattern's expectations.

1. Cast on enough stitches for a 4 in / 10 cm square in your pattern.
2. Knit until the swatch reaches 4 in / 10 cm tall.
3. Block the swatch, then measure stitches and rows in the center.

## Measuring Gauge

After knitting and blocking your swatch, count the stitches across and rows
down in the center. Use the [gauge utilities](gauge.md) to convert between
units or estimate how many stitches you need for a project.
`width_difference_for_stitches` and `height_difference_for_rows` show how far an
off-gauge swatch will push a project's width or height. Use
`stitch_adjustment_for_width` and `row_adjustment_for_height` to translate that
gap into concrete stitch or row adjustments so the finished piece stays on
size.

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
    width_difference_for_stitches,
    height_difference_for_rows,
    stitch_adjustment_for_width,
    row_adjustment_for_height,
)

stitches_per_inch(20, 4)  # 5.0 stitches per inch
rows_per_inch(30, 4)  # 7.5 rows per inch
stitches_per_cm(20, 10)  # 2.0 stitches per cm
rows_per_cm(30, 10)  # 3.0 rows per cm
per_inch_to_per_cm(5.08)  # ~2.0 per cm
per_cm_to_per_inch(2.0)  # ~5.08 per inch
inches_to_cm(1)  # 2.54 cm
cm_to_inches(2.54)  # 1.0 in
width_difference_for_stitches(180, 20, 22)  # ~-0.82 units (narrower fabric)
height_difference_for_rows(220, 30, 28)     # ~0.52 units (taller fabric)
stitch_adjustment_for_width(90, 4.5, 5.025)  # 11 extra stitches keep width
row_adjustment_for_height(120, 6.0, 6.5)     # 10 extra rows keep height
```

Translate gauge between yards and meters with helpers such as
`per_inch_to_per_yard`, `per_yard_to_per_inch`, `per_yard_to_per_meter`, and
`per_meter_to_per_yard` so a single swatch can inform patterns across units.

All gauge helpers require positive stitch and row counts and positive
measurements. Passing non-positive values raises ``ValueError``.
Unit conversion helpers accept non-negative values and raise
``ValueError`` for negatives.

For large projects measured in yards or meters, use
``stitches_for_yards``/``stitches_for_meters`` and
``rows_for_yards``/``rows_for_meters`` to scale your fabric without converting
back to inches or centimeters first.

## Where to go next

- Review the [Learning resources](learning-resources.md) guide for material
  science primers, fiber selection tips, and additional stitch tutorials.
- Read the {ref}`Wove v1c mechanical crochet system design's yarn handling section <yarn-handling>`
  for sensor calibration context and yarn tension workflow notes that bridge
  into automation experiments.
- Explore the [Pattern translation CLI](pattern-cli.md) once you are ready to
  convert swatches into motion; it shows how hand-driven practice feeds the
  browser planner and gantry tests.
