#!/usr/bin/env fontforge

if ($version < "20080330")
    Error("Your version of FontForge is too old - 20080330 or newer is required");
endif

SetPref("FoundryName", "Cantarell")
SetPref("TTFFoundry", "Cantarell")

i = 1
while (i < $argc)
    Open($argv[i], 1)
    SelectAll()
    Simplify()
    AddExtrema()
    RoundToInt()
    CorrectDirection()
    ClearHints()
    AutoHint()
    Generate($fontname + ".otf")
    #generate oblique
    Skew(8)
    Simplify()
    AddExtrema()
    RoundToInt()
    CorrectDirection()
    ClearHints()
    AutoHint()
    Generate($fontname + "-Oblique.otf")
    Close()
    i++
endloop
