#!/usr/bin/env python

import numpy
import sysconfig
import sys

from setuptools import setup, Extension

if (sys.version_info > (3, 0)):
    swig_opts = ['-DPYTHON3']
else:
    swig_opts = []


typemap_samples_module = Extension(
    '_typemap_samples0',
    sources=['typemap_samples.i'],
    swig_opts=swig_opts,
    include_dirs=['cspice/src/cspice',
                  sysconfig.get_config_var('INCLUDEPY'),
                  numpy.get_include()],
    extra_compile_args=['-Wno-incompatible-pointer-types'],
    library_dirs=['cspice/lib'],
    libraries=['cspice'],
)

setup (name = 'typemap_samples',
       version = '1.0',
       author  = "Frank Yellin",
       description = "Sample code for testing templates",
       ext_modules = [typemap_samples_module],
       py_modules = ["code_samples"],
       )
