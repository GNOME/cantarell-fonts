dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.53)

AC_INIT([cantarell-fonts], [0.0.24],
        [http://bugzilla.gnome.org/enter_bug.cgi?product=cantarell-fonts])

AM_INIT_AUTOMAKE([1.9 tar-ustar foreign dist-bzip2 no-dist-gzip])

AC_ARG_ENABLE(source-rebuild,
	    AS_HELP_STRING([--enable-source-rebuild], [Rebuild from source using fontforge]),,
	    enable_source_rebuild=no)
AM_CONDITIONAL(SOURCE_REBUILD, test x$enable_source_rebuild != xno)

PKG_PROG_PKG_CONFIG([0.19])
AC_PROG_SED

# Workaround to make aclocal get the right flags
AC_SUBST(ACLOCAL_AMFLAGS, "\${ACLOCAL_FLAGS}")

AC_ARG_WITH([configdir],
            [AC_HELP_STRING([--with-configdir=DIR],
            [Use DIR to store fontconfig configuration files [default=DATADIR/fontconfig/conf.avail]])],
            [configdir="$withval"],
            [configdir=yes])

case "$configdir" in
no|yes)
    configdir='${datadir}'/fontconfig/conf.avail
    ;;
*)
    ;;
esac

CONFIGDIR=${configdir}
AC_SUBST(CONFIGDIR)

AC_ARG_WITH([fontdir],
            [AC_HELP_STRING([--with-fontdir=DIR],
            [Use DIR to store font files [default=DATADIR/fonts/cantarell]])],
            [fontdir="$withval"],
            [fontdir=yes])

case "$fontdir" in
no|yes)
    fontdir='${datadir}'/fonts/cantarell
    ;;
*)
    ;;
esac

FONTDIR=${fontdir}
AC_SUBST(FONTDIR)

AC_CONFIG_FILES([
Makefile
fontconfig/Makefile
src/Makefile
otf/Makefile
scripts/Makefile
])

AC_OUTPUT

echo "
    $PACKAGE $VERSION
    ===============

    rebuild via fontforge: ${enable_source_rebuild}
"
