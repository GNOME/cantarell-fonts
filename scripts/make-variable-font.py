#!/bin/env python3

# Note: To parallelize this, the cubic to quadratic filter could be run on all sources
# sequentially and the resulting single-layer UFOs written to disk, then compiling the
# masters could be done in parallel and finally, merging into a variable font happens
# sequentially.

import argparse
from pathlib import Path

import fontTools.designspaceLib
import fontTools.varLib
import statmake.classes
import statmake.lib
import ufo2ft
import ufoLib2

parser = argparse.ArgumentParser()
parser.add_argument(
    "designspace_path", type=Path, help="The path to the Designspace file."
)
parser.add_argument(
    "stylespace_path", type=Path, help="The path to the Stylespace file."
)
parser.add_argument("output_path", type=Path, help="The variable TTF output path.")
args = parser.parse_args()

designspace_path = args.designspace_path.resolve()
stylespace_path = args.stylespace_path.resolve()
output_path = args.output_path.resolve()


# 1. Load Designspace and filter out instances that are marked as non-exportable.
designspace = fontTools.designspaceLib.DesignSpaceDocument.fromfile(designspace_path)
designspace.loadSourceFonts(ufoLib2.Font.open)

designspace.instances = [
    s for s in designspace.instances if s.lib.get("com.schriftgestaltung.export", True)
]

# 2. Compile variable TTF from the masters.
varfont = ufo2ft.compileVariableTTF(designspace, inplace=True)

# 3. Generate STAT table.
stylespace = statmake.classes.Stylespace.from_file(stylespace_path)
statmake.lib.apply_stylespace_to_variable_font(stylespace, varfont, {})


varfont.save(output_path)
