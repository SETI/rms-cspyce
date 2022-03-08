#!/usr/bin/env python

# If a binary distribution exists for your OS and Python, congratulations.  You should
# be able to simply install swig.
#
#
# If you are doing a build from sources, you must also have have swig and a copy of
# the cspice toolkit.
#
# [I need appropriate instructions here on how to get cspice.a and install it. so that
#    <this top level directory>/cspice/lib/libcspice.a
#    <this top level directory>/cspice/include/
# contains the library and and the include files]
#
# Execute the following:
#     python setup.py build_ext --inplace
#
# To test the installation, the following should display the CSPICE
# toolkit version string:
#
#    $ python
#    >>> import cspyce
#    >>> cspyce.tkvrsn("toolkit")
#


# We prefer setuptools, but will use distutils if setuptools isn't available
try:
    from setuptools import setup, Extension
    from setuptools.command.build_py import build_py
except:
    from distutils.core import setup, Extension
    from distutils.core import setup, Extension, build_py

import numpy
from glob import glob

sources = (['cspyce/swig/cspyce0.i'] + glob("cspice/src/cspice/*.c"))

cspyce0_module = Extension(
    'cspyce._cspyce0',
    sources=sources,
    include_dirs=['cspice/include',
                  numpy.get_include()],
    swig_opts=["-outdir", "cspyce/."],
    extra_compile_args=['-Wno-incompatible-pointer-types'],
)

setup (name = 'cspyce',
       version = '2.0.1',
       author  = "Mark Showalter/PDS Ring-Moon Systems Node",
       description = "Low-level SWIG interface to the CSPICE library",
       ext_modules = [cspyce0_module],
       packages=["cspyce"],
       install_requires=['numpy'],
       data_files = [("cspyce/swig", glob("cspyce/swig/*.i")),
                     ("cspice/include/", glob("cspice/include/*.h")),
                    ],

)

