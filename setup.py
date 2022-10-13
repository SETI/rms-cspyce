#!/usr/bin/env python

# If you are installing this code via "pip install pds-cspyce", then you should
# never see this file.  pip automatically determines whether you need a binary
# distribution or source distribution, and automatically builds it as needed for
# your machine.
#
# If you are doing a build from sources, please read README-developers.md in this
# directory.


# We prefer setuptools, but will use distutils if setuptools isn't available
import os
from glob import glob
import subprocess
import sys

from setuptools.command.build_ext import build_ext

from get_spice import GetCspice

try:
    from setuptools import Command, setup, Extension
    from setuptools.command.build_py import build_py
except ImportError:
    from distutils.core import Command, setup, Extension
    from distutils.core import setup, Extension, build_py

try:
    import numpy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy


import subprocess
import sys
import platform

PYTHON2 = sys.version_info[0] < 3
IS_LINUX = platform.system() == 'Linux'
IS_MACOS = platform.system() == 'Darwin'
IS_WINDOWS = platform.system() == 'Windows'
assert IS_LINUX or IS_MACOS or IS_WINDOWS


class GenerateCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not PYTHON2:
            from swig.make_vectorize import create_vectorize_header_file
            from swig.make_cspyce0_info import make_cspice0_info
            create_vectorize_header_file("swig/vectorize.i")
            make_cspice0_info("cspyce/cspyce0_info.py")
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
# smaller libraries with a maximum of 250 files apiece.

cspice_directory = GetCspice().download()

def get_c_libraries():
    files = sorted(glob(os.path.join(cspice_directory, "src", "*.c")))
    splits = 1 if IS_LINUX else 1 + (len(files) // 250)
    compiler_flags = ['-DKR_headers', '-DMSDOS', '/nowarn'] if IS_WINDOWS else ['-w']
    cspice_libraries = [
        ("cspice_" + str(i + 1), {
            "sources": files[i::splits],
            "include_dirs": [os.path.join(cspice_directory, "include")],
            "cflags": compiler_flags
        })
        for i in range(splits)]
    return cspice_libraries


def get_extensions():
    cspyce_cflags = ['/nowarn', '/DSWIG_PYTHON_CAST_MODE'] if IS_WINDOWS \
        else ['-Wno-incompatible-pointer-types', '-DSWIG_PYTHON_CAST_MODE']
    include_dirs = [os.path.join(cspice_directory, "include"), numpy.get_include()]

    cspyce0_module = Extension(
        'cspyce._cspyce0',
        sources=['swig/cspyce0_wrap.c'],
        include_dirs=include_dirs,
        extra_compile_args=cspyce_cflags)

    typemap_samples_module = Extension(
        'cspyce._typemap_samples',
        sources=['swig/typemap_samples_wrap.c'],
        include_dirs=include_dirs,
        extra_compile_args=cspyce_cflags,
    )
    return [cspyce0_module, typemap_samples_module]


class MyBuildExt(build_ext):
    def initialize_options(self):
        build_ext.initialize_options(self)


def do_setup():
    try:
        directory = os.path.dirname(os.path.abspath(__file__))
        prerelease_version_file = os.path.join(directory, "prerelease_version.txt")
        with open(prerelease_version_file, "r")  as f:
            prerelease_version = f.read().strip()
            if prerelease_version == 'release':
                prerelease_version = ''
    except IOError:
        prerelease_version = ''
    setup(
        name='cspyce',
        version='2.0.5' + prerelease_version,
        author="Mark Showalter/PDS Ring-Moon Systems Node",
        description="Low-level SWIG interface to the CSPICE library",
        ext_modules=get_extensions(),
        libraries=get_c_libraries(),
        packages=["cspyce"],
        install_requires=['numpy'],
        cmdclass={
            'build_ext': MyBuildExt,
            'generate': GenerateCommand,
        }
    )

do_setup()

