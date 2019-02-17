"""Update the shared GDEF definition feature file.

We want our own because Glyphs has the habit of propagating anchors on
_everything_, even symbols that happen to contain components of latin
glyphs with anchors.
"""

from pathlib import Path

import defcon
import ufo2ft.filters

import glyphsLib.builder.constants


# Lifted from glyphsLib and adapted to only recognize Letters as bases.
def _build_gdef(ufo):
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

    * https://github.com/googlei18n/glyphsLib/issues/85
    * https://github.com/googlei18n/glyphsLib/pull/100#issuecomment-275430289
    """
    from glyphsLib import glyphdata

    bases, ligatures, marks, carets = set(), set(), set(), {}
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
        glyphinfo = glyphdata.get_glyph(glyph.name)
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
        return None

    def fmt(g):
        if g:
            glyph_names = " ".join(sorted(g, key=ufo.glyphOrder.index))
            return f"[{glyph_names}]"
        return ""

    lines = [
        "table GDEF {",
        "  # automatic",
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

    return "\n".join(lines)


if __name__ == "__main__":
    main_source_path = Path(__file__).parent.parent / "src" / "Cantarell-Regular.ufo"
    main_source = defcon.Font(main_source_path)

    pre_filter, _ = ufo2ft.filters.loadFilters(main_source)
    for pf in pre_filter:
        pf(font=main_source)

    gdef_table = _build_gdef(main_source)

    with open(Path(__file__).parent.parent / "src" / "gdef.fea", "w") as fp:
        print(gdef_table, file=fp)
