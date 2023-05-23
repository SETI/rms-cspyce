#!/usr/bin/env python

# If you are installing this code via "pip install cspyce", then you should
# never see this file.  pip automatically determines whether you need a binary
# distribution or source distribution, and automatically builds it as needed for
# your machine.
#
# If you are doing a build from sources, please read README-developers.md in
# this directory.


from glob import glob
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from tarfile import TarFile
import tempfile
import time
from zipfile import ZipFile

from setuptools.command.build_ext import build_ext

from setuptools import Command, setup, Extension

try:
    import numpy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy


IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"
assert IS_LINUX or IS_MACOS or IS_WINDOWS


################################################################################
# The following code is responsible for downloading the CSPICE source files
# based on whatever hardware and software it is currently running on.
#
# The contents of the directories
#        <download>/cspice/src/cspice
#        <download>/include
# are put into the two directories
#        cspice/<os>-<arch>/src
#        cspice/<os>-<arch>/include
#
# This module should only be called by setup.py.
#
# This code owes a big debt to Dr. Andrew Annex and his file:
#      https://github.com/AndrewAnnex/SpiceyPy/blob/main/get_spice.py
# His version is much more ambitious than this and also compiles the files into
# a shared library.
################################################################################

CSPICE_DISTRIBUTIONS = {
    # system   arch        distribution name           extension
    # -------- ----------  -------------------------   ---------
    ("Darwin", "x86_64"): ("MacIntel_OSX_AppleC_64bit", "tar.Z"),
    ("Darwin", "arm64"): ("MacM1_OSX_clang_64bit", "tar.Z"),
    ("cygwin", "x86_64"): ("PC_Cygwin_GCC_64bit", "tar.Z"),
    ("FreeBSD", "x86_64"): ("PC_Linux_GCC_64bit", "tar.Z"),
    ("Linux", "x86_64"): ("PC_Linux_GCC_64bit", "tar.Z"),
    ("Windows", "x86_64"): ("PC_Windows_VisualC_64bit", "zip"),
    # This is just so I can easily test it in a docker image on my Mac
    ("Linux", "arm64"): ("PC_Linux_GCC_64bit", "tar.Z"),
}

ARCHITECTURE_TRANSLATOR = {"aarch64": "arm64", "AMD64": "x86_64"}

# versions
SPICE_VERSION = "N0067"


class GetCspice(object):
    def __init__(self):
        self.host_OS = platform.system()
        architecture = platform.machine()
        self.architecture = ARCHITECTURE_TRANSLATOR.get(architecture, architecture)

        # Check if platform is Unix-like OS or not
        self.is_unix = self.host_OS in ("Linux", "Darwin", "FreeBSD")
        # Get directory into which we want to put all our files
        self.target_directory = os.path.join(
            "cspice", self.host_OS + "-" + self.architecture)

    def download(self):
        if (Path(os.path.join(self.target_directory, "src")).is_dir() and
            Path(os.path.join(self.target_directory, "include")).is_dir()):
            return self.target_directory
        with tempfile.TemporaryDirectory() as tmpdir:
            self.download_cspice(destination=tmpdir)
            shutil.copytree(os.path.join(tmpdir, "cspice", "src", "cspice"),
                            os.path.join(self.target_directory, "src"))
            shutil.copytree(os.path.join(tmpdir, "cspice", "include"),
                            os.path.join(self.target_directory, "include"))
        return self.target_directory

    def download_cspice(self, destination):
        try:
            # Get the remote file path for the Python architecture that
            # executes the script.
            assert sys.maxsize > 2 ** 32, "Machine must support 64bit"
            system = self.host_OS
            system = "cygwin" if "CYGWIN" in system else system
            distribution, extension = CSPICE_DISTRIBUTIONS[(system, self.architecture)]
        except KeyError:
            raise RuntimeError("CSpice does not support your system")

        cspice_filename = "cspice.{}".format(extension)
        url = ("https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_{0}/C/{1}/packages/{2}"
               .format(SPICE_VERSION, distribution, cspice_filename))

        # Download the file
        target_file = os.path.join(destination, cspice_filename)
        attempts = 10  # Let's try a maximum of attempts for getting SPICE
        while attempts:
            try:
                if extension == "zip":
                    # TODO:
                    # Do we want --connect_timeout? This curl either seems to take
                    # 3s or several minutes, somewhat randomly.
                    subprocess.check_call(["curl", url, "-o", target_file])
                    with ZipFile(target_file, "r") as archive:
                        archive.extractall(destination)
                else:
                    target_file = target_file[:-2] # remove the .Z
                    subprocess.check_call("curl {} | gzip -d > {}".format(
                        url, target_file), shell=True)
                    with TarFile.open(target_file, "r") as archive:
                        archive.extractall(destination)
                os.unlink(target_file)
                break
            except (RuntimeError, subprocess.CalledProcessError) as error:
                attempts -= 1
                if attempts == 0:
                    raise error
                print("Download failed with URLError: {0}, trying again after "
                      "15 seconds!".format(error))
                time.sleep(15)


class GenerateCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from swig.make_vectorize import create_vectorize_header_file
        from swig.make_cspyce0_info import make_cspice0_info
        create_vectorize_header_file("swig/vectorize.i")
        make_cspice0_info("cspyce/cspyce0_info.py")
        command = "swig -python -outdir cspyce/. " \
                    "-o swig/cspyce0_wrap.c swig/cspyce0.i".split(" ")
        subprocess.check_call(command)
        command = "swig -python -outdir cspyce/. " \
                    "-o swig/typemap_samples_wrap.c swig/typemap_samples.i".split(" ")
        subprocess.check_call(command)


# Some linkers seem to have trouble with 2400 files, so we break it up into
# smaller libraries with a maximum of 250 files apiece.

cspice_directory = GetCspice().download()

def get_c_libraries():
    files = sorted(glob(os.path.join(cspice_directory, "src", "*.c")))
    splits = 1 if IS_LINUX else 1 + (len(files) // 250)
    compiler_flags = ["-DKR_headers", "-DMSDOS", "/nowarn"] if IS_WINDOWS else ["-w"]
    cspice_libraries = [
        ("cspice_" + str(i + 1), {
            "sources": files[i::splits],
            "include_dirs": [os.path.join(cspice_directory, "include")],
            "cflags": compiler_flags
        })
        for i in range(splits)]
    return cspice_libraries


def get_extensions():
    cspyce_cflags = ["/nowarn", "/DSWIG_PYTHON_CAST_MODE"] if IS_WINDOWS \
        else ["-Wno-incompatible-pointer-types", "-DSWIG_PYTHON_CAST_MODE"]
    include_dirs = [os.path.join(cspice_directory, "include"), numpy.get_include()]

    cspyce0_module = Extension(
        "cspyce._cspyce0",
        sources=["swig/cspyce0_wrap.c"],
        include_dirs=include_dirs,
        extra_compile_args=cspyce_cflags)

    typemap_samples_module = Extension(
        "cspyce._typemap_samples",
        sources=["swig/typemap_samples_wrap.c"],
        include_dirs=include_dirs,
        extra_compile_args=cspyce_cflags,
    )
    return [cspyce0_module, typemap_samples_module]


class MyBuildExt(build_ext):
    def initialize_options(self):
        build_ext.initialize_options(self)


def do_setup():
    setup(
        ext_modules=get_extensions(),
        libraries=get_c_libraries(),
        cmdclass={
            "build_ext": MyBuildExt,
            "generate": GenerateCommand,
        }
    )

do_setup()
