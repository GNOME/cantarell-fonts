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
    name = source_glyph.name
    if name not in glyph_list:
        continue

    target_ufo[name] = source_glyph
    if name not in target_ufo_glyph_order_set:
        target_ufo_glyph_order.append(name)

    source_ps_names = source_ufo.lib["public.postscriptNames"]
    target_ps_names = target_ufo.lib["public.postscriptNames"]
    if name in source_ps_names:
        target_ps_names[name] = source_ps_names[name]

target_ufo.save()
