#!/bin/env python3
#
# This wrapper works around fontmake's limitation (at the time of this writing)
# of not being able to specify the output directory for the generated font
# binaries. The Meson build system's custom target function has fixed
# expectations about where files must show up. Also, autohint the binaries
# while we're at it.

from pathlib import Path
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("fontmake", type=str, help="The path to fontmake.")
parser.add_argument("psautohint", type=str, help="The path to psautohint.")
parser.add_argument("font_source", help="The path to the font source.")
parser.add_argument("output_dir", help="The full target output path.")
args = parser.parse_args()

source = Path(args.font_source).resolve()
output_dir = Path(args.output_dir)

subprocess.run([
    args.fontmake, "-g", source, "-i", "-o", "otf", "--verbose",
    "WARNING"
], cwd=output_dir)

for otf in (output_dir / "instance_otf").glob("*.otf"):
    subprocess.run([args.psautohint, "-qq", str(otf)])
    output_dir.mkdir(exist_ok=True)
    otf.rename(output_dir / otf.name)
