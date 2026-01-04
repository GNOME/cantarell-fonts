import argparse
import logging
import sys
from pathlib import Path

from glyphConstruction import (
    GlyphBuilderError,
    GlyphConstructionBuilder,
    ParseGlyphConstructionListFromString,
)
from ufoLib2 import Font

parser = argparse.ArgumentParser()
parser.add_argument("constructions_file", type=Path)
parser.add_argument("ufos", type=Font.open, nargs="+")
parser.add_argument("--overwrite", action="store_true")
parsed_args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

constructions_file: Path = parsed_args.constructions_file
ufos: list[Font] = parsed_args.ufos
overwrite: bool = parsed_args.overwrite

try:
    constructions = ParseGlyphConstructionListFromString(constructions_file.read_text())
except GlyphBuilderError:
    logging.exception("Cannot parse file '%s'", constructions_file)
    sys.exit(1)

for font in ufos:
    for construction_string in constructions:
        try:
            construction = GlyphConstructionBuilder(construction_string, font)
        except GlyphBuilderError:
            logging.exception("Cannot construct '%s'", construction_string)
            sys.exit(1)

        if construction.name is None or not construction.name.strip():
            continue
        if construction.name in font and not overwrite:
            continue

        if construction.name in font:
            glyph = font[construction.name]
        else:
            glyph = font.newGlyph(construction.name)
        glyph.clear()

        glyph.width = construction.width
        if construction.unicodes:
            glyph.unicodes = construction.unicodes
        glyph.note = construction.note
        construction.draw(glyph.getPen())
        if construction.markColor:
            glyph.lib["public.markColor"] = str(tuple(construction.markColor))

        logging.info("Built '%s' in font '%s'", construction_string, font.path)

    font.save()
