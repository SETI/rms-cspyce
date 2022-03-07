#!/usr/bin/env python

import numpy
import sysconfig

from setuptools import setup, Extension


typemap_samples_module = Extension(
    'cspyce._typemap_samples',
    sources=['cspyce/swig/typemap_samples.i'],
    include_dirs=['cspyce/cspice/include',
                  sysconfig.get_config_var('INCLUDEPY'),
                  numpy.get_include()],
    swig_opts=["-outdir", "cspyce/"],
    extra_compile_args=['-Wno-incompatible-pointer-types'],
    library_dirs=['cspyce/cspice/lib'],
    libraries=['cspice'],
)

setup(name='typemap_test',
      version='1.0',
      author="Frank Yellin",
      description="Sample code for testing templates",
      ext_modules=[typemap_samples_module],
      py_modules=["cspyce/typemap_test",
                  "cspyce/typemap_samples",
                  "cspyce/_typemap_samples"],
)
