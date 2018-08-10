Cantarell
=========

This file provides detailed information on the Cantarell font software. This information should be distributed along with the Cantarell fonts and any derivative works.

Build instructions
------------------

```
python3 -m venv venv
. venv/bin/activate  # Unixoids...
venv/Scripts/activate  # ...or on Windows cmd.exe or PowerShell

pip3 install meson ninja  # Unless already present on system.
pip3 install fontmake psautohint "glyphslib>=3.0.3"

meson build
ninja -C build install
```

Contributing
------------

The master file is `src/Cantarell.glyphs`. To contribute, you need to:

-	Use the proprietary and Mac-only Glyphs.app...
-	...or generate UFOs from it by using `fontmake -g src/Cantarell.glyphs -o ufo`. You can then open the masters in `master_ufo` with any design app that supports it. Send the contribution to Nikolaus Waxweiler somehow so he can consider it.
-	...or wait for glyphsLib 2.3.0 to be released, which will finally contain code to roundtrip between Glyphs files and UFOs, at which point I'll switch over and you'll be able to use any UFO editor you'd like. Rejoice!

History
-------

The Cantarell typeface family is a contemporary Humanist sans serif, and is used by the GNOME project for its user interface.

Cantarell was originally designed by Dave Crossland as part of his coursework for the MA Typeface Design program at the [Department of Typography in the University of Reading, England](http://www.typedesign.reading.ac.uk).

After the GNOME project adopted the typeface in November 2010, minor modifications and slight expansions were made to it over the years. Pooja Saxena initially worked on the typeface as a participant of the GNOME outreach program and later developed her own Devanagari typeface Cambay, which included a redesigned latin version of Cantarell. It was backported to the GNOME branch of Cantarell by Nikolaus Waxweiler, who also performed other janitorial tasks on it.

The overall quality of the design was however far from good, given that the regular and bold face were worked on seperately and without consistency and had low quality outlines, and the oblique variants were simply slanted uprights without much correction. The GNOME design team also requested lighter weights. Up to this point, the work on Cantarell was mainly done with libre tools such as FontForge.

Given the decaying state of FontForge (arcane user interface, heaps of quirky and buggy behavior) and the very early development status of alternatives such as TruFont, Nikolaus Waxweiler started redrawing Cantarell in the proprietary and Mac-only Glyphs.app under mentorship from Jacques Le Bailly ("Baron von Fonthausen"). Later, Alexei Vanyashin and Eben Sorkin reviewed the design.

Acknowledgements
----------------

Here is a list of major contributors; all contributors are listed in the GNOME Git repository changelogs. Please add yourself if you make major changes. This list is sorted by last name in alphabetical order.

| Name               | Email                         | Web Address                                         | Description                                                                             |
| ------------------ | ----------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Dave Crossland     | dave@understandinglimited.com | http://understandingfonts.com/who/dave-crossland/   | Designer, original Latin glyphs.                                                        |
| Valek Filippov     | frob@gnome.org                | https://plus.google.com/108983215764171548842/about | Designer, original Cyrillic glyphs.                                                     |
| Erik Hartenian     | infinality@infinality.net     | \-                                                  | Connoisseur of fine font renderding.                                                    |
| Pooja Saxena       | anexasajoop@gmail.com         | http://www.poojasaxena.in                           | Designer, new glyphs and many improvements to weight and metric balance.                |
| Jakub Steiner      | jimmac@gmail.com              | http://jimmac.musichall.cz                          | Designer, many improvements and GNOME standards engineering.                            |
| Nikolaus Waxweiler | madigens@gmail.com            | \-                                                  | Designer, general clean up and increased language coverage, later on complete redesign. |
