from pathlib import Path

from glyphsLib.glyphdata import get_glyph
from ufoLib2 import Font

SRC_DIR = Path(__file__).parent.parent / "src"

for source_path in SRC_DIR.glob("*.ufo"):
    ufo = Font.open(source_path)

    ps_names = {}
    for name in ufo.keys():
        glyph_info = get_glyph(name)
        if name != glyph_info.production_name:
            ps_names[name] = glyph_info.production_name

    ufo.lib["public.postscriptNames"] = ps_names

    ufo.save()
