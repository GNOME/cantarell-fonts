dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.53)

AC_INIT([cantarell-fonts], [0.0.6],
        [http://bugzilla.gnome.org/enter_bug.cgi?product=cantarell-fonts])

AM_INIT_AUTOMAKE([1.9 tar-ustar foreign dist-bzip2 no-dist-gzip])

PKG_PROG_PKG_CONFIG([0.19])
AC_PROG_SED

# Workaround to make aclocal get the right flags
AC_SUBST(ACLOCAL_AMFLAGS, "\${ACLOCAL_FLAGS}")

AC_CONFIG_FILES([
Makefile
fontconfig/Makefile
src/Makefile
otf/Makefile
])

AC_OUTPUT
