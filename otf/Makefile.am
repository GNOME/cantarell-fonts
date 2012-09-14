
fontdir = $(FONTDIR)
font_DATA = \
	Cantarell-Regular.otf		\
	Cantarell-Bold.otf

if SOURCE_REBUILD
%.otf: $(top_srcdir)/src/%.sfd
	/usr/bin/env fontforge -script $(top_srcdir)/scripts/generate.sh "$^"
endif

EXTRA_DIST = $(font_DATA)

-include $(top_srcdir)/git.mk
