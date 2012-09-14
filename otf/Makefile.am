
fontdir = $(FONTDIR)
font_DATA = \
	Cantarell-Regular.otf		\
	Cantarell-Bold.otf

%.otf: $(top_srcdir)/src/%.sfd
	/usr/bin/env fontforge -script $(top_srcdir)/scripts/generate.sh "$^"

EXTRA_DIST = $(font_DATA)

-include $(top_srcdir)/git.mk
