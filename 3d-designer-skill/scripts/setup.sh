#!/usr/bin/env bash
# Installs the toolchain for 3d-designer-skill.  Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v openscad >/dev/null; then
  if command -v apt-get >/dev/null; then sudo apt-get update -q && sudo apt-get install -y -q openscad xvfb
  elif command -v brew >/dev/null; then brew install --cask openscad
  else echo "install OpenSCAD from https://openscad.org/downloads.html and re-run"; exit 1; fi
fi
python3 -m pip install -q -r requirements.txt
command -v xvfb-run >/dev/null || echo "note: xvfb-run not found; PNG renders need a display on Linux (apt install xvfb)"
openscad --version
python3 -m designer --help | head -3
echo "ok"
