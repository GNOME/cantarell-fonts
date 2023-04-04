Cantarell
=========

This file provides detailed information on the Cantarell font software. This information should be distributed along with the Cantarell fonts and any derivative works. The latest release is available at the [Cantarell website](https://cantarell.gnome.org).

Build instructions
------------------

```
python3 -m venv venv
. venv/bin/activate  # Unixoids...
venv/Scripts/activate  # ...or on Windows cmd.exe or PowerShell

pip3 install meson ninja  # Unless already present on system.
pip3 install -r requirements.txt

meson build
ninja -C build install
```

By default, only the variable font is built. You can toggle either with the `buildstatics` and `buildvf` Meson option.

Contributing
------------

Cantarell consists of three masters: Thin (Cantarell-Light.ufo), Regular (Cantarell-Regular.ufo) and Extra Bold (Cantarell-Bold.ufo). The file that ties them together and defines where the masters and instances stand is Cantarell.designspace.

If you want to contribute, you should be familiar with font design applications. You will also unfortunately have to learn about the innards of the UFO format as you go, to know what is changing... FontForge, TruFont and RoboFont can open the UFO v3 masters directly, Glyphs is tied to UFO v2 at the time of this writing.

To use Glyphs, do:

```
# (activate the venv from above if you haven't done so)

pip3 install -r requirements-dev.txt
ufo2glyphs src/Cantarell.designspace
```

Edit the .glyphs file and round-trip back:

```
glyphs2ufo src/Cantarell.glyphs
```

Note that this will result in noise that will have to be trimmed... Send a MR and we'll sort it out togeher.

History
-------

The Cantarell typeface family is a contemporary Humanist sans serif, and is used by the GNOME project for its user interface.

Cantarell was originally designed by Dave Crossland as part of his coursework for the MA Typeface Design program at the [Department of Typography in the University of Reading, England](https://www.reading.ac.uk/typography/).

After the GNOME project adopted the typeface in November 2010, minor modifications and slight expansions were made to it over the years. Pooja Saxena initially worked on the typeface as a participant of the GNOME outreach program and later developed her own Devanagari typeface Cambay, which included a redesigned latin version of Cantarell. It was backported to the GNOME branch of Cantarell by Nikolaus Waxweiler, who also performed other janitorial tasks on it.

The overall quality of the design was however far from good, given that the regular and bold face were worked on separately and without consistency and had low quality outlines, and the oblique variants were simply slanted uprights without much correction. The GNOME design team also requested lighter weights. Up to this point, the work on Cantarell was mainly done with libre tools such as FontForge.

Given the decaying state of FontForge (arcane user interface, heaps of quirky and buggy behavior) and the very early development status of alternatives such as TruFont, Nikolaus Waxweiler started redrawing Cantarell in the proprietary and Mac-only Glyphs.app under mentorship from Jacques Le Bailly ("Baron von Fonthausen"). Later, Alexei Vanyashin and Eben Sorkin reviewed the design.

Acknowledgements
----------------

Here is a list of major contributors; all contributors are listed in the GNOME Git repository changelogs. Please add yourself if you make major changes. This list is sorted by last name in alphabetical order.

| Name               | Email                         | Web Address                                         | Description                                                                             |
| ------------------ | ----------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Dave Crossland     | dave@understandinglimited.com | http://understandingfonts.com/who/dave-crossland/   | Designer, original Latin glyphs.                                                        |
| Florian Fecher     | florian.fecher@grautesk.de    | https://www.twitter.com/grautesk                    | Designer, original Greek glyphs.                                                        |
| Valek Filippov     | frob@gnome.org                | https://plus.google.com/108983215764171548842/about | Designer, original Cyrillic glyphs.                                                     |
| Erik Hartenian     | infinality@infinality.net     | \-                                                  | Connoisseur of fine font renderding.                                                    |
| Jacques Le Bailly  | fonthausen@baronvonfonthausen.com  | https://baronvonfonthausen.com                 | Mentor for the Latin set                                                                |
| Pooja Saxena       | anexasajoop@gmail.com         | http://www.poojasaxena.in                           | Designer, new glyphs and many improvements to weight and metric balance.                |
| Eben Sorkin        | http://sorkintype.com/contact.html | http://sorkintype.com/                         | Mentor for the Latin set                                                                |
| Jakub Steiner      | jimmac@gmail.com              | http://jimmac.musichall.cz                          | Designer, many improvements and GNOME standards engineering.                            |
| Emilios Theofanous | \-                            | https://twitter.com/emilios__                       | GSoC 2018 mentor for the Greek set                                                      |
| Alexei Vanyashin   | hello@110design.ru            | http://www.110design.ru/                            | Mentor for the Cyrillic set                                                             |
| Irene Vlachou      | \-                            | https://twitter.com/irene_vlachou                   | GSoC 2018 mentor for the Greek set                                                      |
| Nikolaus Waxweiler | madigens@gmail.com            | \-                                                  | Designer, general clean up and increased language coverage, later on complete redesign. |
| Alexios Zavras     | \-                            | \-                                                  | GSoC 2018 mentor for the Greek set                                                      |
