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
    
    SelectAll()
    CorrectDirection()

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

    # Using RoundToInt() above doesn't actually round everything to int. Ugh.
    # Workaround: open generated file and RoundToInt() there, then regenerate.
    # This can mess with the PS Private dictionary. Gah!
    #Open($fontname + ".otf")
    #SelectAll()
    #RoundToInt()
    #Generate($fontname + ".otf")
    #
    #Open($argv[i])

    ###
    # Generate synthetic oblique. Better than nothing.
    SetItalicAngle(-8)

    weight=GetTTFName(0x409,2)
    if ($weight == "Regular") 
      SetTTFName(0x409, 2, "Oblique")
      SetFontNames("Cantarell-Oblique", "", "Cantarell Oblique")
    else
      SetTTFName(0x409, 2, "BoldOblique")
      SetFontNames("Cantarell-BoldOblique", "", "Cantarell Bold Oblique")
    endif

    # XXX: Does not work from the script, only works when done through the GUI.
#    # To keep references, selectively unlink and remove overlap. First select
#    # glyphs constructed out of references and splines and turn them into
#    # splines-only. Also unlink diacritics and some misc. glyphs if they are
#    # constructed out of other diacritics (e.g. 2x dotaccent -> dieresis). Skew
#    # won't work correctly otherwise.
#    SelectGlyphsBoth()
#    SelectMore(0u02c6, 0u0331)
#    SelectMore(0u0022)
#    SelectMore(0u003a, 0u003b)
#    UnlinkReference()
#    RemoveOverlap()
#    Simplify(1 | 8 | 16 | 32 | 64 | 128)
#    RoundToInt()

    SelectAll()
    UnlinkReference()
    RemoveOverlap()
    Simplify(1 | 8 | 16 | 32 | 64 | 128, 1)
    RoundToInt()
    Skew(8)
    AddExtrema()
    Simplify(1 | 8 | 16 | 32 | 64 | 128, 1)
    RoundToInt()

    # Can't validate oblique'd font because RoundToInt doesn't seem to round
    # control handles to integers, causing missing extrema on a few glyphs that
    # disappear when manually rounding to int in the GUI.
    #if (Validate(1))
    #  Error("Oblique'd " + $argv[i] + " did not pass validation. Fix the script.")
    #endif

    # Deselect combining diacritics before tightening spacing of the oblique.
    # The tightening has been calculated according to Thomas Phinney's
    # presentation on "How to Space a font", H * (tan i) = left shift, where H
    # is 0.5 * average(cap height, x height) and i is the italic angle. I
    # halved the result because it looks better.
    SelectGlyphsSplines()
    SelectFewer(0u0300, 0u0331)
    Move(-20, 0)

    AutoHint()
    Generate($fontname + ".otf")
    Close()

    i++
endloop
