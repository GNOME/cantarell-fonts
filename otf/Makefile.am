
fontdir = $(FONTDIR)
font_DATA = \
	Cantarell-Regular.otf	   \
	Cantarell-Oblique.otf	   \
	Cantarell-Bold.otf         \
	Cantarell-BoldOblique.otf

if SOURCE_REBUILD
$(filter-out %Oblique.otf,$(font_DATA)): %.otf: $(top_srcdir)/src/%.sfdir
	/usr/bin/env fontforge -script $(top_srcdir)/scripts/generate.sh "$^"

$(filter %Oblique.otf,$(font_DATA)): %.otf: ;
endif

EXTRA_DIST = $(font_DATA)

-include $(top_srcdir)/git.mk
