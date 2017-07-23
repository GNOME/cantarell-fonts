#!/bin/env python3
#
# This wrapper works around fontmake's limitation (at the time of this writing)
# of not being able to specify the output directory for the generated font
# binaries. The Meson build system's custom target function expects those files
# to be on the same level in the build directory as the concerned meson.build
# file for the install command to work properly. Also, autohint the binaries
# while we're at it.

import os, argparse, subprocess

parser = argparse.ArgumentParser()
parser.add_argument("fontmake", type=str, help="The path to fontmake.")
parser.add_argument("psautohint", type=str, help="The path to psautohint.")
parser.add_argument("font_source", help="The path to the font source.")
args = parser.parse_args()

fontname = os.path.basename(args.font_source).split(".")[0]
print(os.path.join("master_otf", fontname + ".otf"))

if args.font_source.endswith(".ufo"):
    fontmake_cmd_switch = "-u"
elif args.font_source.endswith(".glyphs"):
    fontmake_cmd_switch = "-g"
else:
    raise(ValueError, "This script currently only handles UFO and Glyphs sources.")

subprocess.run([args.fontmake, fontmake_cmd_switch, args.font_source, "-o", "otf"])

font_original_path = os.path.join(os.getcwd(), "master_otf", fontname + ".otf")
font_new_path = os.path.join(os.getcwd(), fontname + ".otf")

os.rename(font_original_path, font_new_path)

subprocess.run([args.psautohint, font_new_path])
