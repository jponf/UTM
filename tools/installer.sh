#!/usr/bin/env sh
#
# Author: Josep Pon Farreny
#
# Creates a bundled executable for linux/osx using pyinstaller
#

uname_str=`uname`
arch_str=`uname -m`

if [ "${uname_str}" = "Linux" ]; then
    platform="linux"
elif [ "${uname_str}" = "FreeBSD" ]; then
    platform="bsd"
elif [ "${uname_str}" = "Darwin" ]; then
    platform="mac"
else
    platform="unknown"
fi

pymain=../utm/__main__.py
outname=utm-${platform}-${arch_str}
specdir=installer
distdir=${specdir}/dist
workdir=${specdir}/build


# Add data separator is ; in windows
pyinstaller --log-level=INFO \
    --onefile             \
    --name "${outname}"   \
    --specpath=${specdir} \
    --distpath=${distdir} \
    --workpath=${workdir} \
    --hidden-import="utm.resources" \
    --add-data "../../utm/resources/icon.png:utm/resources" \
    --i ../graphics/icon.ico \
    ${pymain}