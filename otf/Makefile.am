
fontdir = $(FONTDIR)
font_DATA = \
	Cantarell-Regular.otf		\
	Cantarell-Oblique.otf		\
	Cantarell-Bold.otf \
	Cantarell-Bold-Oblique.otf

if SOURCE_REBUILD
%.otf: $(top_srcdir)/src/%.sfdir
	/usr/bin/env fontforge -script $(top_srcdir)/scripts/generate.sh "$^"
endif

EXTRA_DIST = $(font_DATA)

-include $(top_srcdir)/git.mk
