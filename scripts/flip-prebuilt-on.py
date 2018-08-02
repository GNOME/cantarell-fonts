"""Elaborate sed script to flip useprebuilt=True by default as I don't know
how to "" things in .gitlab-ci.yml."""

import argparse
import fileinput

parser = argparse.ArgumentParser()
parser.add_argument(
    "meson_options_txt", type=str, help="The meson_options.txt file to change"
)
args = parser.parse_args()

text_to_search = "'useprebuilt', type : 'boolean', value : false"
replacement_text = "'useprebuilt', type : 'boolean', value : true"

with fileinput.FileInput(args.meson_options_txt, inplace=True, backup=".bak") as file:
    for line in file:
        print(line.replace(text_to_search, replacement_text), end="")
