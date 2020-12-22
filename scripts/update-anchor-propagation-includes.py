"""Update the glyph name list for anchor propagation in all masters.

We rely on Glyphs-style anchor propagation to get mark-to-base and mark-
to-mark anchoring for composites. Contrary to Glyphs behavior, we want
to keep propagation to non-ligature letters and combining marks.
Propagation to ligatures like "fi" and compatibility digraphs is
broken/incomplete in ufo2ft 2.7.0 and probably makes little sense
anyway.

Propagation only makes sense for composites, but we include outline
glyphs in the list because it's faster to go through glyphOrder than the
glyph objects.
"""

from pathlib import Path

import fontTools.unicodedata
import glyphsLib.glyphdata
import ufoLib2

main_source_path = Path(__file__).parent.parent / "src" / "Cantarell-Regular.ufo"
main_source = ufoLib2.Font.open(main_source_path)
letters_and_marks = []
for glyph_name in main_source.glyphOrder:
    if not main_source[glyph_name].components:
        continue  # We only care about composites.

    if glyph_name.startswith("_"):
        continue

    info = glyphsLib.glyphdata.get_glyph(glyph_name)

    if info.category not in ("Letter", "Mark"):
        continue

    if (info.category, info.subCategory) == ("Letter", "Ligature"):
        continue

    if info.unicode:
        decomposition = fontTools.unicodedata.decomposition(
            chr(int(info.unicode, base=16))
        )
        if decomposition.startswith("<compat>"):
            continue

    letters_and_marks.append(glyph_name)

propagate_anchors_filter = next(
    f
    for f in main_source.lib["com.github.googlei18n.ufo2ft.filters"]
    if f["name"] == "propagateAnchors"
)
propagate_anchors_filter["include"] = sorted(letters_and_marks)

main_source.save()

# Mirror the ufo2ft filters to the other sources so that building them independently
# before merging them into a variable font produces identical results.
for other_source_path in (Path(__file__).parent.parent / "src").glob("*.ufo"):
    if other_source_path == main_source_path:
        continue

    other_source = ufoLib2.Font.open(other_source_path)
    other_source.lib["com.github.googlei18n.ufo2ft.filters"] = main_source.lib[
        "com.github.googlei18n.ufo2ft.filters"
    ]
    other_source.save()
