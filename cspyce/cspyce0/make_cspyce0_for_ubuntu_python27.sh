#!/bin/sh
#
# Create cspyce0.py and _cspyce0.so for Ubuntu Linux and Python 2.7
#
# This script depends on the python-dev and swig packages:
#    apt-get install python-dev
#    apt-get install swig
#
# You must also have an appropriate 64-bit version of Python installed.
#
# For Linux 64-bit, download the CSPICE toolkit from:
#    http://naif.jpl.nasa.gov/naif/toolkit_C_PC_Linux_GCC_64bit.html
# and uncompress and untar it in this directory. This will create a new
# subdirectory pds-tools/cspyce/cspyce0/cspice.
#
# Alternatively, type
#   ln -s [cspice_path] cspice
# where "[cspice_path]" is replaced by the path to your existing cspice
# directory.
#
# Execute this shell script: ./make_cspyce0_for_ubuntu_python27.sh
#
# To test the installation, the following should display the CSPICE
# toolkit version string:
#
#    $ python
#    >>> import cspyce
#    >>> cspyce.tkvrsn("toolkit")
#
# *** NOTE ***
# Adjust the following variables to point at your Python directories:

PYTHON_INCLUDE=/home/rfrench/anaconda2/include/python2.7
PYTHON_LIB=/home/rfrench/anaconda2/lib
PYTHON_PKGS=/home/rfrench/anacodna2/lib/python2.7/site-packages

rm -f cspyce0_wrap.c cspyce0_wrap.o

swig -python cspyce0.i

/usr/bin/gcc -c `python-config --cflags` -fPIC cspyce0_wrap.c -I$PYTHON_INCLUDE \
    -I$PYTHON_PKGS/numpy/core/include -Icspice/src/cspice
# This returns many warnings but should not report any errors

# Use this version to limit Python exceptions to RuntimeErrors.
# gcc -c `python-config --cflags` cspyce0_wrap.c -I$PYTHON_INCLUDE \
#     -I$PYTHON_PKGS/numpy/core/include -Icspice/src/cspice \
#     -D RUNTIME_ERRORS_ONLY

rm -f _cspyce0.so

ld -lpython2.7 -lm -shared -L$PYTHON_LIB \
    -o _cspyce0.so cspyce0_wrap.o cspice/lib/cspice.a -lm

rm -f cspyce0_wrap.c cspyce0_wrap.o
