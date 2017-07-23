# Cantarell

This file provides detailed information on the Cantarell font software. This
information should be distributed along with the Cantarell fonts and any
derivative works.

## Font Information

The Cantarell typeface family is a contemporary Humanist sans serif, and is
used by the GNOME project for its user interface. 

Cantarell was originally designed by Dave Crossland as part of his coursework
for the MA Typeface Design program at the Department of Typography in the
University of Reading, England. [1] 

After the GNOME project adopted the typeface in November 2010, minor
modifications and slight expansions were made to it over the years. Pooja
Saxena initially worked on the typeface as a participant of the GNOME outreach
program and later developed her own Devanagari typeface Cambay, which included
a redesigned latin version of Cantarell. It was backported to the GNOME branch
of Cantarell by Nikolaus Waxweiler, who also performed other janitorial tasks
on it.

The overall quality of the design was however far from good, given that the
regular and bold face were worked on seperately and without consistency and had
low quality outlines, and the oblique variants were simply slanted uprights
without much correction. The GNOME design team also requested lighter weights.
Up to this point, the work on Cantarell was mainly done with libre tools such
as FontForge. 

Given the decaying state of FontForge (arcane user interface, heaps of quirky
and buggy behavior) and the very early development status of alternatives such
as TruFont, Nikolaus Waxweiler started redrawing Cantarell in the proprietary
and Mac-only Glyphs.app.

Taking inspiration from Source Sans Pro, the redesign was a thin and a black
master, with all other weights inbetween interpolated. Using proprietary
plugins like SpeedPunk and RMX Tools resulted in much higher quality outlines.
The open-source HT Letterspacer plugin made good and consistent spacing almost
trivial. The original character of Cantarell was however ironed out in the
process, for better or worse.

There was one victim of the redesign: participation. As the design process
continues, the master file is in the proprietary, but documented .glyphs
format, which no open-source design application can read. This is because the
widely supported UFO format has a limited feature set. See below.

[1]: http://www.typedesign.reading.ac.uk

## Developer information
                                  
The master file is `src/Cantarell.glyphs`. To contribute, you need to either:
1) Use the proprietary and Mac-only Glyphs.app.
2) Generate UFOs from it by using `fontmake -g src/Cantarell.glyphs -o ufo`.
You can then open the masters in `master_ufo` with any design app that supports
it. Send the contribution to Nikolaus Waxweiler somehow so he can consider it
using 1).

## Acknowledgements

Here is a list of major contributors; all contributors are listed in the GNOME
Git repository changelogs.

If you make major modifications be sure to add your name (N), email (E),
web-address (W) and description (D). This list is sorted by last name in
alphabetical order.

N: Dave Crossland
E: <dave@understandinglimited.com>
W: http://understandingfonts.com/who/dave-crossland/
D: Designer, original Latin glyphs.

N: Valek Filippov
E: <frob@gnome.org>
W: https://plus.google.com/108983215764171548842/about
D: Designer, original Cyrillic glyphs.

N: Erik Hartenian
E: <infinality@infinality.net>
W: -
D: Connoisseur of fine font renderding.

N: Pooja Saxena
E: <anexasajoop@gmail.com>
W: http://www.poojasaxena.in
D: Designer, new glyphs and many improvements to weight and metric balance.

N: Jakub Steiner
E: <jimmac@gmail.com>
W: http://jimmac.musichall.cz
D: Designer, many improvements and GNOME standards engineering.

N: Nikolaus Waxweiler
E: <madigens@gmail.com>
W: -
D: Designer, general clean up and increased language coverage, later on complete redesign.
