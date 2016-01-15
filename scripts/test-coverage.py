#!/usr/bin/env python3
#
# Test Unicode coverage of a given font file against a list with Unicode
# points, currently the Adobe Latin and Cyrillic precomposed glyphs lists.
#
# https://adobe-type-tools.github.io/adobe-latin-charsets/
# https://adobe-type-tools.github.io/adobe-cyrillic-charsets/

import os
import argparse
from fontTools.ttLib import TTFont
from urllib.request import urlopen

parser = argparse.ArgumentParser()
parser.add_argument("fonts", nargs='+',
                    help="One or more font files (.otf/.ttf) you want to test for coverage.")
args = parser.parse_args()

charset_list = [
"https://adobe-type-tools.github.io/adobe-latin-charsets/adobe-latin-4-precomposed.txt",
"https://adobe-type-tools.github.io/adobe-cyrillic-charsets/adobe-cyrillic-2.txt"
]

for charset in charset_list:
  charset_table = {}

  # Parse charset file into charset_table.
  with urlopen(charset) as c:
    # Split table manually and slice off header.
    raw_table = c.read().decode().split("\n")[1:]

    # We care only about the first column with the hex code and the third
    # column with the plain English description of that code point. The first
    # column must be converted from e.g. a string of a hex "20AE" to an int
    # 8366.
    for raw_line in raw_table:
      if raw_line: # Skip empty lines.
        sliced_line = raw_line.split("\t")
        charset_table[int(sliced_line[0], 16)] = sliced_line[3] # { 8366: "TUGRIK SIGN", ... }

  charset_set = frozenset(charset_table.keys())

  # Now compare each given font against this charset.
  for font_file in args.fonts:
    font = TTFont(font_file)

    # Font can contain multiple cmaps that map unicode code points (U+0020) to
    # glyph names ("space"), we want the code points from all Unicode cmaps and
    # flatten them into a (unique) set.
    codepoints = [[y[0] for y in x.cmap.items()] 
                  for x in font['cmap'].tables if x.isUnicode()]
    codepoints_set = frozenset([item for sublist in codepoints
                               for item in sublist])
    missing_codepoints = charset_set.difference(codepoints_set)

    if missing_codepoints:
      font_filename = os.path.basename(font_file)
      charset_filename = charset.rpartition("/")[-1]
      print("\n" + font_filename + " is missing from " + charset_filename + ":")
      
      for m in missing_codepoints:
        print("U+" + format(m, "04X") + " " + charset_table[m])

    font.close()
