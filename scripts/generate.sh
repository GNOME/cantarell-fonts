#!/usr/bin/env fontforge

if ($version < "20080330")
    Error("Your version of FontForge is too old - 20080330 or newer is required");
endif

SetPref("FoundryName", "Cantarell")
SetPref("TTFFoundry", "Cantarell")

i = 1
while (i < $argc)
    Open($argv[i])

    if (Validate(1))
      Error($argv[i] + " did not pass validation. Tolerate no technical flaws in the source! Run 'Validate' in FontForge to see and fix what's wrong. The generated files might not validate completely due to the way FontForge scripting seems to work..")
    endif

    SelectGlyphsBoth()
    UnlinkReference()
    RemoveOverlap()
    AddExtrema()
    Simplify(1 | 8 | 16 | 32 | 64 | 128, 1)

    SelectAll()
    ClearHints()
    AutoHint()
    RoundToInt()
    Generate($fontname + ".otf")

    i++
endloop
