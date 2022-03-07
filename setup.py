#!/usr/bin/env python

# We prefer setuptools, but will use distutils if setuptools isn't available
try:
    from setuptools import setup, Extension
    from setuptools.command.build_py import build_py
except:
    from distutils.core import setup, Extension
    from distutils.core import setup, Extension, build_py

import numpy
import sysconfig
from glob import glob

cspyce0_module = Extension(
    'cspyce._cspyce0',
    sources=['cspyce/swig/cspyce0.i'],
    include_dirs=['cspyce/cspice/include',
                  sysconfig.get_config_var('INCLUDEPY'),
                  numpy.get_include()],
    swig_opts=["-outdir", "cspyce/."],
    extra_compile_args=['-Wno-incompatible-pointer-types'],
    library_dirs=['cspyce/cspice/lib'],
    libraries=['cspice'],
)

setup (name = 'cspyce',
       version = '2.0',
       author  = "Mark Showalter/PDS Ring-Moon Systems Node",
       description = "Low-level SWIG interface to the CSPICE library",
       ext_modules = [cspyce0_module],
       packages=["cspyce"],
       data_files=[("cspyce/swig", glob("cspyce/swig/*.i"))],
       install_requires=['numpy']
       )

