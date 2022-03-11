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
    from setuptools import Command, setup, Extension
    from setuptools.command.build_py import build_py
except:
    from distutils.core import Command, setup, Extension
    from distutils.core import setup, Extension, build_py

import numpy
from glob import glob
import subprocess
import sys

PYTHON2 = sys.version_info[0] < 3

class GenerateCommand(Command):
    description = 'Create generated files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not PYTHON2:
            print("Recreating the vectorize macros")
            from swig.make_vectorize import create_vectorize_header_file
            create_vectorize_header_file("swig/vectorize.i")
            print("Rerunning swig")
            command = "swig -python -outdir cspyce/. -o swig/cspyce0_wrap.c swig/cspyce0.i".split(' ')
            subprocess.check_call(command)
            command = "swig -python -outdir cspyce/. -o swig/typemap_samples_wrap.c swig/typemap_samples.i".split(' ')
            subprocess.check_call(command)
        else:
            command = "echo Cannot rebuild files in Python2".split(' ')
            subprocess.check_call(command)

cspice_module = Extension(
    'cspyce.cspice',
    sources=glob("cspice/src/cspice/*.c"),
    include_dirs=['cspice/include'],
    extra_compile_args=['-Wno-incompatible-pointer-types', '-Wno-parentheses', 
               '-Wno-implicit-int', "-Wno-shift-op-parentheses",
               '-Wno-logical-op-parentheses', '-Wno-sign-compare',
               '-Wno-pointer-to-int-cast', '-Wno-strict-prototypes'],
)

cspyce0_module = Extension(
    'cspyce._cspyce0',
    sources=['swig/cspyce0_wrap.c'],
    include_dirs=['cspice/include', numpy.get_include()],
    extra_compile_args=['-Wno-incompatible-pointer-types'],
    libraries=['cspice'],
    library_dirs=['build/'],
)

typemap_samples_module = Extension(
    'cspyce._typemap_samples',
    sources=['swig/typemap_samples_wrap.c'],
    include_dirs=['cspice/include', numpy.get_include()],
    extra_compile_args=['-Wno-incompatible-pointer-types'],
)

setup (name = 'cspyce',
       version = '2.0.0',
       author  = "Mark Showalter/PDS Ring-Moon Systems Node",
       description = "Low-level SWIG interface to the CSPICE library",
       ext_modules = [cspyce0_module, typemap_samples_module, cspice_module],
       # libraries=[lib_cspice],
       packages=["cspyce"],
       install_requires=['numpy'],
       cmdclass={
           'generate': GenerateCommand,
       },
)

