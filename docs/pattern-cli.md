# Pattern translation CLI

`wove.pattern_cli` turns a compact crochet stitch description into a
G-code-like motion sequence that you can stream to firmware or inspection tools.
The translator focuses on early-stage prototyping rather than production-grade
path planning, but it demonstrates how a text pattern becomes coordinated motion.

## Supported commands

The domain-specific language (DSL) accepts one command per line. Lines that are
empty or start with `#` are ignored.

| Command | Description |
| --- | --- |
| `CHAIN <count>` | Emit chain stitches spaced evenly along the X axis. |
| `SINGLE <count>` | Emit single crochet stitches with a deeper plunge and additional yarn feed. |
| `DOUBLE <count>` | Emit double crochet stitches with a taller pull-up motion. |
| `MOVE <x> <y>` | Lift safely, then travel to absolute `(x, y)` coordinates in millimeters. |
| `TURN [height]` | Reset X=0, advance Y to next row, optionally override default 6 mm height. |
| `PAUSE <seconds>` | Insert a `G4` dwell for the specified number of seconds. |

Values must be positive. Invalid commands or parameters raise `ValueError` and
stop translation so mistakes surface early.

## Example

Save the following pattern as `pattern.txt`:

```text
# form a base chain, reposition, and add a single crochet
CHAIN 3
PAUSE 0.4
MOVE 18 5
TURN 7
SINGLE 1
```

Translate it into G-code-like output:

```bash
python -m wove.pattern_cli pattern.txt
```

The CLI prints commented commands:

```text
G21 ; use millimeters
G90 ; absolute positioning
G92 X0.00 Y0.00 Z4.00 E0 ; zero axes
G1 Z-1.50 F600 ; chain stitch 1 of 3: plunge
G1 E0.50 F300 ; chain stitch 1 of 3: feed yarn
G1 Z4.00 F600 ; chain stitch 1 of 3: raise
G0 X5.00 Y0.00 F1200 ; chain stitch 1 of 3: advance
...
G4 P400 ; pause for 0.400 s
G0 X18.00 Y5.00 F1200 ; reposition
G0 X0.00 Y12.00 F1200 ; turn to next row
G1 Z-2.00 F600 ; single stitch 1 of 1: plunge
G1 E2.10 F300 ; single stitch 1 of 1: feed yarn
G1 Z4.00 F600 ; single stitch 1 of 1: raise
G0 X4.50 Y12.00 F1200 ; single stitch 1 of 1: advance
```

Use `--format json` to inspect a structured representation for downstream
pipelines:

```bash
python -m wove.pattern_cli --text "CHAIN 1\nDOUBLE 1" --format json
```

## Importing SVG polylines

Provide an SVG file containing a `polyline` or `polygon` element to trace its vertices as travel
moves. The CLI emits `MOVE` commands for each vertex after applying optional scaling and offsets:

```bash
python -m wove.pattern_cli --svg sketch.svg --svg-scale 1.5 --svg-offset-x 10 --svg-offset-y 5
```

This limited importer focuses on quick mechanical experiments, so it ignores curves and other path
commands. Clean up artwork so only the desired polyline or polygon remains before converting it.
