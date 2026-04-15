#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"

echo "Building d4..."
cd "$ROOT_DIR/d4"
make
cp d4_bin "$ROOT_DIR/"

echo "Building ganak..."
cd "$ROOT_DIR/ganak-asp/scripts"
./build_norm.sh
cp ganak "$ROOT_DIR/"

echo "Building sharpsat-td..."
cd "$ROOT_DIR/sharpsat-td"
./setupdev.sh
cp bin/sharpSAT "$ROOT_DIR/"
cp bin/flow_cutter_pace17 "$ROOT_DIR/"

echo "Done. Copied binaries to:"
echo "  $ROOT_DIR/d4_bin"
echo "  $ROOT_DIR/ganak"
echo "  $ROOT_DIR/sharpSAT"
echo "  $ROOT_DIR/flow_cutter_pace17"
