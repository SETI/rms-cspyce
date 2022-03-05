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
import sys

if (sys.version_info > (3, 0)):
    swig_opts = ['-DPYTHON3']
else:
    swig_opts = []


class GenerateVectorize(build_py):
    def run(self):
        import make_vectorize
        print("Generating vectorize.i")
        make_vectorize.create_vectorize_header_file('cspyce0.i', 'vectorize.i')


cspyce0_module = Extension(
    '_cspyce0',
    sources=['cspyce0.i'],
    swig_opts=swig_opts,
    include_dirs=['cspice/src/cspice',
                  sysconfig.get_config_var('INCLUDEPY'),
                  numpy.get_include()],
    extra_compile_args=['-Wno-incompatible-pointer-types'],
    library_dirs=['cspice/lib'],
    libraries=['cspice'],
)

setup (name = 'cspyce0',
       version = '2.0',
       author  = "Mark Showalter/PDS Ring-Moon Systems Node",
       description = "Low-level SWIG interface to the CSPICE library",
       ext_modules = [cspyce0_module],
       py_modules = ["cspyce0"],
       cmdclass={
           'build_py': GenerateVectorize,
       },
)

