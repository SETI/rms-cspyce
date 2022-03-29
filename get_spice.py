################################################################################
# get_spice.py
################################################################################
#
# This module is responsible for downloading the cspice source files based on whatever
# hardware and software it is currently running on.
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
# This file owes a big debt to Andrew Annex and his file:
#      https://github.com/AndrewAnnex/SpiceyPy/blob/main/get_spice.py
# His version is much more ambitious than this and also compiles the files into a
# shared library.
################################################################################


from __future__ import absolute_import, with_statement

import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from tarfile import TarFile
from zipfile import ZipFile

try:
    from pathlib import Path
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pathlib"])
    from pathlib import Path


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
        # Get directory that this file is in.
        self.root_dir = str(Path(os.path.realpath(__file__)).parent)
        # Get directory into which we want to put all our files
        self.target_directory = os.path.join(
            self.root_dir, "cspice", self.host_OS + "-" + self.architecture)

    def download(self):
        if Path(os.path.join(self.target_directory, "src")).is_dir() and \
           Path(os.path.join(self.target_directory, "include")).is_dir():
            return self.target_directory
        # Note.  Once we toss 2.7 support, this can be rewritten as "with ...."
        tmpdir = tempfile.mkdtemp()
        try:
            self.download_cspice(destination=tmpdir)
            shutil.copytree(os.path.join(tmpdir, "cspice", "src", "cspice"),
                            os.path.join(self.target_directory, "src"))
            shutil.copytree(os.path.join(tmpdir, "cspice", "include"),
                            os.path.join(self.target_directory, "include"))
        finally:
            shutil.rmtree(tmpdir)
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
                    subprocess.check_call("curl {} | gzip -d > {}".format(url, target_file), shell=True)
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


if __name__ == "__main__":
    GetCspice().download()
