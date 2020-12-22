from pathlib import Path

import ufoLib2


source_directory = Path(__file__).parent.parent / "src"
for ufo_path in source_directory.glob("*.ufo"):
    ufo = ufoLib2.Font.open(ufo_path)

    layer_names = [l.name for l in ufo.layers]
    for name in layer_names:
        if name != "public.default":
            del ufo.layers[name]

    ufo.layers.defaultLayer.lib = {
        k: v for k, v in ufo.layers.defaultLayer.lib.items() if k.startswith("public.")
    }

    for glyph in ufo:
        glyph.lib = {
            k: v
            for k, v in glyph.lib.items()
            if (
                k.startswith("public.")
                or k.startswith("com.schriftgestaltung.Glyphs.")
                or k == "com.schriftgestaltung.componentsAlignment"
            )
            and k != "public.markColor"
        }

    ufo.lib = {
        k: v
        for k, v in ufo.lib.items()
        if k.startswith("public.")
        or k.startswith("com.github.googlei18n.ufo2ft.")
        or (
            k
            in {
                "com.schriftgestaltung.appVersion",
                "com.schriftgestaltung.fontMasterID",
                "com.schriftgestaltung.customParameter.GSFont.disablesLastChange",
                "com.schriftgestaltung.customParameter.GSFontMaster.paramArea",
                "com.schriftgestaltung.customParameter.GSFontMaster.paramDepth",
                "com.schriftgestaltung.customParameter.GSFontMaster.paramOver",
            }
        )
    }

    ufo.save()
