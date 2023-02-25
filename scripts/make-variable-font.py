#!/bin/env python3

# Note: To parallelize this, the cubic to quadratic filter could be run on all sources
# sequentially and the resulting single-layer UFOs written to disk, then compiling the
# masters could be done in parallel and finally, merging into a variable font happens
# sequentially.

import argparse
import os
import subprocess
from pathlib import Path

import cffsubr
import fontTools.designspaceLib
import fontTools.ttLib
import fontTools.varLib
import ufo2ft
import ufoLib2

parser = argparse.ArgumentParser()
parser.add_argument(
    "designspace_path", type=Path, help="The path to the Designspace file."
)
parser.add_argument(
    "stylespace_path", type=Path, help="The path to the Stylespace file."
)
parser.add_argument(
    "psautohint_path", type=Path, help="The path to the psautohint executable."
)
parser.add_argument("output_path", type=Path, help="The variable TTF output path.")
args = parser.parse_args()

designspace_path = args.designspace_path.resolve()
stylespace_path = args.stylespace_path.resolve()
output_path = args.output_path.resolve()
psautohint_path = args.psautohint_path.resolve()


# 1. Load Designspace and filter out instances that are marked as non-exportable.
designspace = fontTools.designspaceLib.DesignSpaceDocument.fromfile(designspace_path)
designspace.loadSourceFonts(ufoLib2.Font.open)

designspace.instances = [
    s for s in designspace.instances if s.lib.get("com.schriftgestaltung.export", True)
]

# 2. Compile variable OTF from the masters. Do not optimize, because we have to do
# it again after autohinting.
varfont = ufo2ft.compileVariableCFF2(
    designspace,
    inplace=True,
    useProductionNames=True,
    optimizeCFF=ufo2ft.CFFOptimization.NONE,
)

# 3. Save. External tools after this point.
varfont.save(output_path)

# 4. Autohint
subprocess.check_call([os.fspath(args.psautohint_path), os.fspath(output_path)])

# 5. Subroutinize (compress)
varfont = fontTools.ttLib.TTFont(output_path)
cffsubr.subroutinize(varfont).save(output_path)
