"""
The MIT License (MIT)

Copyright (c) [2015-2022] [Andrew Annex]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Sources for this file are mostly from DaRasch, spiceminer/getcspice.py,
with edits by me as needed for python2/3 compatibility
https://github.com/DaRasch/spiceminer/blob/master/getcspice.py

The MIT License (MIT)

Copyright (c) 2013 Philipp Rasch

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

The MIT License (MIT)

Copyright (c) 2017 ODC Space

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

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


DISTRIBUTIONS = {
    # system   arch        distribution name           extension
    # -------- ----------  -------------------------   ---------
    ("Darwin", "x86_64"): ("MacIntel_OSX_AppleC_64bit", "tar.Z"),
    ("Darwin", "arm64"): ("MacM1_OSX_clang_64bit", "tar.Z"),
    ("cygwin", "x86_64"): ("PC_Cygwin_GCC_64bit", "tar.Z"),
    ("FreeBSD", "x86_64"): ("PC_Linux_GCC_64bit", "tar.Z"),
    ("Linux", "x86_64"): ("PC_Linux_GCC_64bit", "tar.Z"),
    ("Windows", "x86_64"): ("PC_Windows_VisualC_64bit", "zip"),
    # This is just so I can test it in a docker image on my Mac
    ("Linux", "aarch64"): ("PC_Linux_GCC_64bit", "tar.Z"),

}


# versions
SPICE_VERSION = "N0067"


class GetCspice(object):
    def __init__(self):
        self.host_OS = platform.system()
        architecture = platform.machine()
        self.architecture = "x86_64" if architecture == "AMD64" else architecture
        # Get platform is Unix-like OS or not
        self.is_unix = self.host_OS in ("Linux", "Darwin", "FreeBSD")
        # Get current working directory
        self.root_dir = str(Path(os.path.realpath(__file__)).parent)

        self.target_directory = os.path.join(
            self.root_dir, "cspice", self.host_OS + "-" + self.architecture)

    def download(self):
        if Path(os.path.join(self.target_directory, "src")).is_dir() and \
           Path(os.path.join(self.target_directory, "include")).is_dir():
            return self.target_directory
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
            distribution, extension = self._distribution_info()
        except KeyError:
            print("SpiceyPy currently does not support your system.")
            return

        cspice = "cspice.{}".format(extension)
        url = ("https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_{0}/C/{1}/packages/{2}"
               .format(SPICE_VERSION, distribution, cspice))

        # Download the file
        print("Downloading CSPICE for {0}...".format(distribution))
        target_file = os.path.join(destination, cspice)
        attempts = 10  # Let's try a maximum of attempts for getting SPICE
        while attempts:
            try:
                if extension == "zip":
                    subprocess.check_call(["curl", url, "-o", target_file])  # -s = silent
                    with ZipFile(target_file, "r") as archive:
                        archive.extractall(destination)
                else:
                    target_file = target_file[:-2]
                    subprocess.check_call("curl {} | gzip -d > {}".format(url, target_file), shell=True)
                    with TarFile.open(target_file, "r") as archive:
                        archive.extractall(destination)
                os.unlink(target_file)
                break
            except (RuntimeError, subprocess.CalledProcessError) as error:
                if attempts == 0:
                    raise error
                attempts -= 1
                print("Download failed with URLError: {0}, trying again after "
                      "15 seconds!".format(error))
                time.sleep(15)
        print("Download done.")

    def _distribution_info(self):
        assert sys.maxsize > 2 ** 32, "Machine must support 64bit"
        system = self.host_OS
        system = "cygwin" if "CYGWIN" in system else system
        print("SYSTEM:        ", system)
        print("ARCHITECTURE:  ", self.architecture)
        return DISTRIBUTIONS[(system, self.architecture)]


if __name__ == "__main__":
    GetCspice().download()
