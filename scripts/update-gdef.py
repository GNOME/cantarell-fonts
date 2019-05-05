"""Update the GDEF definition in the feature file.

We want our own because Glyphs has the habit of propagating anchors on
_everything_, even symbols that happen to contain components of latin
glyphs with anchors.
"""

from pathlib import Path
from typing import Any, Dict, List

import ufoLib2
import glyphsLib.builder.constants
import glyphsLib.glyphdata
import ufo2ft.filters


# Lifted from glyphsLib and adapted to only recognize Letters as bases and not
# insert a "# automatic".
def _build_gdef(ufo) -> List[str]:
    """Build a GDEF table statement (GlyphClassDef and LigatureCaretByPos).

    Building GlyphClassDef requires anchor propagation or user care to work as
    expected, as Glyphs.app also looks at anchors for classification:

    * Base: any glyph that has an attaching anchor (such as "top"; "_top" does
      not count) and is neither classified as Ligature nor Mark using the
      definitions below;
    * Ligature: if subCategory is "Ligature" and the glyph has at least one
      attaching anchor;
    * Mark: if category is "Mark" and subCategory is either "Nonspacing" or
      "Spacing Combining";
    * Compound: never assigned by Glyphs.app.

    See:

    * https://github.com/googlefonts/glyphsLib/issues/85
    * https://github.com/googlefonts/glyphsLib/pull/100#issuecomment-275430289
    """
    bases, ligatures, marks = set(), set(), set()
    carets: Dict[str, Any] = {}  # glyph names to anchor objects
    category_key = glyphsLib.builder.constants.GLYPHLIB_PREFIX + "category"
    subCategory_key = glyphsLib.builder.constants.GLYPHLIB_PREFIX + "subCategory"

    for glyph in ufo:
        has_attaching_anchor = False
        for anchor in glyph.anchors:
            name = anchor.name
            if name and not name.startswith("_"):
                has_attaching_anchor = True
            if name and name.startswith("caret_") and "x" in anchor:
                carets.setdefault(glyph.name, []).append(round(anchor["x"]))

        # First check glyph.lib for category/subCategory overrides. Otherwise,
        # use global values from GlyphData.
        glyphinfo = glyphsLib.glyphdata.get_glyph(glyph.name)
        category = glyph.lib.get(category_key) or glyphinfo.category
        subCategory = glyph.lib.get(subCategory_key) or glyphinfo.subCategory

        if subCategory == "Ligature" and has_attaching_anchor:
            ligatures.add(glyph.name)
        elif category == "Mark" and (
            subCategory == "Nonspacing" or subCategory == "Spacing Combining"
        ):
            marks.add(glyph.name)
        elif category == "Letter" and has_attaching_anchor:
            bases.add(glyph.name)

    if not any((bases, ligatures, marks, carets)):
        return []

    def fmt(g):
        if g:
            glyph_names = " ".join(sorted(g, key=ufo.glyphOrder.index))
            return f"[{glyph_names}]"
        return ""

    lines = [
        "table GDEF {",
        "  GlyphClassDef",
        f"    {fmt(bases)}, # Base",
        f"    {fmt(ligatures)}, # Liga",
        f"    {fmt(marks)}, # Mark",
        "    ;",
    ]
    for glyph, caretPos in sorted(carets.items()):
        caretPos_joined = " ".join(sorted(caretPos))
        lines.append(f"  LigatureCaretByPos {glyph} {caretPos_joined};")
    lines.append("} GDEF;")

    return lines


# Anchors have to be propagated before we can construct the GDEF table.
if __name__ == "__main__":
    source_directory = Path(__file__).parent.parent / "src"

    # The list of glyph names for anchor propagation is stored in the main UFO
    # (main == whatever has info=1 set in the Designspace).
    main_source_path = source_directory / "Cantarell-Regular.ufo"
    main_source = ufoLib2.Font.open(main_source_path)
    pre_filter, _ = ufo2ft.filters.loadFilters(main_source)
    for pf in pre_filter:
        pf(font=main_source)  # Run propagation filters on main UFO

    # Generate GDEF definition string from processed, in-memory UFO
    gdef_table_lines = [f"{l}\n" for l in _build_gdef(main_source)]

    # Update features.fea in all UFOs.
    for feature_file in source_directory.glob("*.ufo/features.fea"):
        with open(feature_file) as fp:
            file_contents = fp.readlines()
        gdef_start = file_contents.index("table GDEF {\n")
        gdef_end = file_contents.index("} GDEF;\n") + 1
        file_contents[gdef_start:gdef_end] = gdef_table_lines
        with open(feature_file, "w+") as fp:
            fp.write("".join(file_contents))
