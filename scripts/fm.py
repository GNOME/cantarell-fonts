#!/bin/env python3
#
# This wrapper works around the Meson build system's fixed expectations about
# where files must show up. Also, autohint the binaries while we're at it.
#
# XXX: Parallelize build process. Currently tricky because launching fontmake
# multiple times with the -i parameter set to an instance name will generate the
# master UFOs multiple times, overwriting each other and crashing. One could
# maybe generate the master UFOs and then interpolate concurrently from them,
# but fontmaking from UFOs may result in differences in the binary output due
# to... the way fontmake etc. works. Maybe wait until using UFOs and Designspace
# files exclusively.

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

subprocess.run(
    [
        args.fontmake,
        "-m",
        source,
        "-i",
        r"^((?!Interpolated).)*$",  # Generate all instances except the ones for testing.
        "-o",
        "otf",
        "--verbose",
        "WARNING",
        "--expand-features-to-instances",
        "--output-dir",
        args.output_dir,
    ]
)

otfs = output_dir.glob("*.otf")

subprocess.run([args.psautohint, *[str(otf) for otf in otfs]])
