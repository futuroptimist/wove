#!/usr/bin/env bash
# Render a single OpenSCAD file to STL.
# Usage: scripts/openscad_render.sh path/to/file.scad
# Set STANDOFF_MODE=printed for alternate mode.

set -euo pipefail

mode="${STANDOFF_MODE:-heatset}"
scad="$1"
out_dir="stl"
base="$(basename "$scad" .scad)"
out="$out_dir/${base}_${mode}.stl"

mkdir -p "$out_dir"
echo "[INFO] Rendering $scad in $mode mode -> $out"
openscad -o "$out" -D STANDOFF_MODE=\"$mode\" "$scad"
