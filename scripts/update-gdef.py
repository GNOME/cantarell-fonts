"""Update the GDEF definition in the feature file.

We want our own because Glyphs has the habit of propagating anchors on
_everything_, even symbols that happen to contain components of latin
glyphs with anchors.
"""

from pathlib import Path
from typing import Dict, Optional

import glyphsLib.builder.constants
import glyphsLib.glyphdata
import ufo2ft.filters
import ufoLib2


def opentype_categories(ufo: ufoLib2.Font) -> Dict[str, str]:
    """Returns a public.openTypeCategories dictionary.

    Building it requires anchor propagation or user care to work as
    expected, as Glyphs.app also looks at anchors for classification:

    * base: any glyph that has an attaching anchor (such as "top"; "_top" does
      not count) and is neither classified as Ligature nor Mark using the
      definitions below;
    * ligature: if subCategory is "Ligature" and the glyph has at least one
      attaching anchor;
    * mark: if category is "Mark" and subCategory is either "Nonspacing" or
      "Spacing Combining";
    * composite: never assigned by Glyphs.app.

    See:

    * https://github.com/googlefonts/glyphsLib/issues/85
    * https://github.com/googlefonts/glyphsLib/pull/100#issuecomment-275430289
    """

    # Drop glyphs that don't exist in font anymore.
    existing: Dict[str, str] = ufo.lib.get("public.openTypeCategories", {})
    categories: Dict[str, str] = {k: v for k, v in existing.items() if k in ufo}

    category_key = glyphsLib.builder.constants.GLYPHLIB_PREFIX + "category"
    subcategory_key = glyphsLib.builder.constants.GLYPHLIB_PREFIX + "subCategory"

    for glyph in ufo:
        assert glyph.name is not None
        has_attaching_anchor = False
        for anchor in glyph.anchors:
            name = anchor.name
            if not name:
                continue
            if not name.startswith("_"):
                has_attaching_anchor = True

        # First check glyph.lib for category/subCategory overrides. Otherwise,
        # use global values from GlyphData.
        glyphinfo = glyphsLib.glyphdata.get_glyph(glyph.name)
        category: Optional[str] = glyph.lib.get(category_key, glyphinfo.category)
        subcategory: Optional[str] = glyph.lib.get(
            subcategory_key, glyphinfo.subCategory
        )

        if subcategory == "Ligature" and has_attaching_anchor:
            categories[glyph.name] = "ligature"
        elif category == "Mark" and (
            subcategory == "Nonspacing" or subcategory == "Spacing Combining"
        ):
            categories[glyph.name] = "mark"
        elif category == "Letter" and has_attaching_anchor:
            categories[glyph.name] = "base"

    return categories


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

    ot_categories = opentype_categories(main_source)

    for ufo_path in source_directory.glob("*.ufo"):
        ufo = ufoLib2.Font.open(ufo_path)
        if ot_categories:
            ufo.lib["public.openTypeCategories"] = ot_categories
        else:
            ufo.lib.pop("public.openTypeCategories", None)
        ufo.save()
