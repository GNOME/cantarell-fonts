#!/bin/sh
# Run this to generate all the initial makefiles, etc.

srcdir=`dirname $0`
test -z "$srcdir" && srcdir=.

PKG_NAME="cantarell-fonts"
REQUIRED_AUTOMAKE_VERSION=1.9
REQUIRED_PKG_CONFIG_VERSION=0.19.0

(test -f $srcdir/configure.ac \
  && test -d $srcdir/src) || {
    echo -n "**Error**: Directory "\`$srcdir\'" does not look like the"
    echo " top-level $PKG_NAME directory"
    exit 1
}

which gnome-autogen.sh || {
    echo "You need to install gnome-common from the GNOME CVS"
    exit 1
}

(cd $srcdir && autoreconf --force --install) || exit 1

if test x$NOCONFIGURE = x; then
    . gnome-autogen.sh
else
    echo Skipping configure process.
fi

