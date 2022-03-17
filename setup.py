#!/usr/bin/env python

# If you are installing this code via "pip install pds-cspyce", then you should
# never see this file.  pip automatically determines whether you need a binary
# distribution or source distribution, and automatically builds it as neede for
# your machine.
#
# If you are doing a build from sources, please read README.develoeprs.me in this
# directory.


# We prefer setuptools, but will use distutils if setuptools isn't available
import math

try:
    from setuptools import Command, setup, Extension
    from setuptools.command.build_py import build_py
except ImportError:
    from distutils.core import Command, setup, Extension
    from distutils.core import setup, Extension, build_py

import os
import subprocess
import sys
from glob import glob

import numpy

PYTHON2 = sys.version_info[0] < 3
IS_WINDOWS = os.name == 'nt'
IS_POSIX = os.name == 'posix'


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
            command = "swig -python -outdir cspyce/. " \
                      "-o swig/cspyce0_wrap.c swig/cspyce0.i".split(' ')
            subprocess.check_call(command)
            command = "swig -python -outdir cspyce/. " \
                      "-o swig/typemap_samples_wrap.c swig/typemap_samples.i".split(' ')
            subprocess.check_call(command)
        else:
            command = "echo Cannot rebuild files in Python2".split(' ')
            subprocess.check_call(command)


# Some linkers seem to have trouble with 2400 files.  So we break it up into
# smaller libraries with a maximum of 500 files apiece.

def get_c_libraries():
    files = sorted(glob("cspice/src/cspice/*.c"))
    splits = 1 if IS_POSIX else int(math.ceil(len(files) / 500))
    compiler_flags = ['-DKR_headers', '-DMSDOS', '/nowarn'] if IS_WINDOWS else ['-w']
    cspice_libraries = [
        ("cspice_" + str(i + 1), {
            "sources": files[i::splits],
            "include_dirs": ["cspice/include", ],
            "cflags": compiler_flags
        })
        for i in range(splits)]
    return cspice_libraries

if IS_WINDOWS:
    cspyce_cflags = ['/nowarn']
else:
    cspyce_cflags = ['-Wno-incompatible-pointer-types']


cspyce0_module = Extension(
    'cspyce._cspyce0',
    sources=['swig/cspyce0_wrap.c'],
    include_dirs=['cspice/include', numpy.get_include()],
    extra_compile_args=cspyce_cflags,
)

typemap_samples_module = Extension(
    'cspyce._typemap_samples',
    sources=['swig/typemap_samples_wrap.c'],
    include_dirs=['cspice/include', numpy.get_include()],
    extra_compile_args=cspyce_cflags,
)

setup(
    name='cspyce',
    version='2.0.0',
    author="Mark Showalter/PDS Ring-Moon Systems Node",
    description="Low-level SWIG interface to the CSPICE library",
    ext_modules=[cspyce0_module, typemap_samples_module],
    libraries=get_c_libraries(),
    packages=["cspyce"],
    install_requires=['numpy'],
    cmdclass={
        'generate': GenerateCommand,
    }
)
