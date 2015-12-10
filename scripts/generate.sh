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
    weight=GetTTFName(0x409,2)
    if($weight=="Regular") 
      SetTTFName(0x409,2,"Oblique")
      SetFontNames("Cantarell-Oblique", "", "Cantarell Oblique", "","","")
    else
      SetTTFName(0x409,2,"Bold-Oblique")
      SetFontNames("Cantarell-Bold-Oblique", "", "Cantarell Bold Oblique", "","","")
    endif
    UnlinkReference() #workaround for shifting diacritics
    Skew(8)
    Simplify()
    AddExtrema()
    RoundToInt()
    CorrectDirection()
    ClearHints()
    AutoHint()
    Generate($fontname + ".otf")
    Close()
    i++
endloop
