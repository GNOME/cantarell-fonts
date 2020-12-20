import argparse
from pathlib import Path

import ufoLib2

parser = argparse.ArgumentParser()
parser.add_argument("glyph_list", type=Path)
parser.add_argument("source", type=ufoLib2.Font.open)
parser.add_argument("target", type=ufoLib2.Font.open)
args = parser.parse_args()

glyph_list = {x.strip() for x in args.glyph_list.read_text().split("\n") if x}
source_ufo = args.source
target_ufo = args.target
target_ufo_glyph_order = target_ufo.lib["public.glyphOrder"]
target_ufo_glyph_order_set = set(target_ufo_glyph_order)

for source_glyph in source_ufo:
    if source_glyph.name not in glyph_list:
        continue

    target_ufo[source_glyph.name] = source_glyph
    if source_glyph.name not in target_ufo_glyph_order_set:
        target_ufo_glyph_order.append(source_glyph.name)

target_ufo.save()
