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
"""

import hashlib
import os
import sys
import tempfile
import time
from pathlib import Path
import pytest

import requests
from requests import RequestException


def _get_kernel_directory():
    try:
        return os.environ['CSPYCE_TEST_KERNELS']
    except KeyError:
        pass

    directory = Path(tempfile.gettempdir()) / "cspyce-test-kernels"
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory)


def _get_test_output_directory():
    directory = Path(tempfile.gettempdir()) / "cspyce-test-file-output"
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory)


KERNEL_DIR = _get_kernel_directory()
TEST_FILE_DIR = _get_test_output_directory()


def get_kernel_name_from_url(url: str) -> str:
    return url.split("/")[-1]


def get_path_from_url(url: str) -> str:
    return os.path.join(KERNEL_DIR, get_kernel_name_from_url(url))


def cleanup_file(path: str) -> None:
    # =============================================================================
    #     if os.path.exists(path):
    #         os.remove(path)
    # =============================================================================
    pass


class CassiniKernels:
    cassPck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cpck05Mar2004.tpc"
    cassPck_md5 = "8c16afc3bd886326e852b54bd71cc751"
    satSpk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/130220AP_SE_13043_13073.bsp"
    satSpk_md5 = "056c65b8a8064f2958aa097db40160b2"
    cassTourSpk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/130212AP_SK_13043_13058.bsp"
    cassTourSpk_md5 = "41210b787e06c1b8bce7ded3d0b930ab"
    cassFk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cas_v40.tf"
    cassFk_md5 = "99f1f5a1900afc536354306419dc119b"
    cassCk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/13056_13057ra.bc"
    cassCk_md5 = "d3acb29fd931b66e34120feb26f7efb7"
    cassSclk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cas00167.tsc"
    cassSclk_md5 = "a30faec21039ba589d3c88db6b5fb536"
    cassIk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cas_iss_v10.ti"
    cassIk_md5 = "101419660e4fe5856d30eb624da61a3f"
    cassPck = get_path_from_url(cassPck_url)
    satSpk = get_path_from_url(satSpk_url)
    cassTourSpk = get_path_from_url(cassTourSpk_url)
    cassFk = get_path_from_url(cassFk_url)
    cassCk = get_path_from_url(cassCk_url)
    cassSclk = get_path_from_url(cassSclk_url)
    cassIk = get_path_from_url(cassIk_url)


def cleanup_cassini_kernels() -> None:
    cleanup_file(CassiniKernels.cassPck)
    cleanup_file(CassiniKernels.satSpk)
    cleanup_file(CassiniKernels.cassTourSpk)
    cleanup_file(CassiniKernels.cassFk)
    cleanup_file(CassiniKernels.cassCk)
    cleanup_file(CassiniKernels.cassSclk)
    cleanup_file(CassiniKernels.cassIk)


class ExtraKernels:
    voyagerSclk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/vg200022.tsc"
    voyagerSclk_md5 = "4bcaf22788efbd86707c4b3c4d63c0c3"
    earthTopoTf_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/EARTH_TOPO_050714.TF"
    earthTopoTf_md5 = "0c152e057d753a4c550d31699662be4b"
    earthStnSpk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/earthstns_itrf93_050714.bsp"
    earthStnSpk_md5 = "a37d8d5e3023f0df7ead0e6b40d6a5b6"
    earthHighPerPck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/earth_031228_231229_predict.bpc"
    earthHighPerPck_md5 = "affa1da5adeee5ea4b0d7da54e4b69d7"
    phobosDsk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/phobos_lores.bds"
    phobosDsk_md5 = "68261460433bfc67b9e57bb57f79c5c9"
    marsSpk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/mar022-1.bsp"
    marsSpk_md5 = "d8d742db3f9502571fb5a5f8c55e8e62"
    mroFk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/mro_v15.tf"
    mroFk_md5 = "a938c271be63e0e5aa2ec86db89af109"
    geophysical_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/geophysical.ker"
    geophysical_md5 = "caff390a00897d09a1f9cdeae0028e3d"
    mro2007sub_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/mro_psp4_ssd_mro95a_sub.bsp"
    mro2007sub_md5 = "8ed34eb77b21ac611f4680806677edfb"
    spk430sub_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/de430sub.bsp"
    spk430sub_md5 = "0b49545fa316f9053f5cfbcce155becc"
    vexboomck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/VEX_BOOM_V01.BC"
    vexboomck_md5 = "2f4dba65649246d72836fb3b53823c3d"
    v02swuck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/vo2_swu_ck2.bc"
    v02swuck_md5 = "f59ef0556dfc63b55465e152f2d6f5a4"
    voyagerSclk = get_path_from_url(voyagerSclk_url)
    earthTopoTf = get_path_from_url(earthTopoTf_url)
    earthStnSpk = get_path_from_url(earthStnSpk_url)
    earthHighPerPck = get_path_from_url(earthHighPerPck_url)
    phobosDsk = get_path_from_url(phobosDsk_url)
    marsSpk = get_path_from_url(marsSpk_url)
    mroFk = get_path_from_url(mroFk_url)
    geophKer = get_path_from_url(geophysical_url)
    mro2007sub = get_path_from_url(mro2007sub_url)
    spk430sub = get_path_from_url(spk430sub_url)
    vexboomck = get_path_from_url(vexboomck_url)
    v02swuck = get_path_from_url(v02swuck_url)


def cleanup_extra_kernels() -> None:
    cleanup_file(ExtraKernels.voyagerSclk)
    cleanup_file(ExtraKernels.earthTopoTf)
    cleanup_file(ExtraKernels.earthStnSpk)
    cleanup_file(ExtraKernels.earthHighPerPck)
    cleanup_file(ExtraKernels.phobosDsk)
    cleanup_file(ExtraKernels.marsSpk)
    cleanup_file(ExtraKernels.mroFk)
    cleanup_file(ExtraKernels.geophKer)
    cleanup_file(ExtraKernels.mro2007sub)
    cleanup_file(ExtraKernels.spk430sub)
    cleanup_file(ExtraKernels.vexboomck)
    cleanup_file(ExtraKernels.v02swuck)


class CoreKernels:
    # note this gets updated
    currentLSK = "naif0012.tls"
    #
    pck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/pck00010.tpc"
    pck_md5 = "da153641f7346bd5b6a1226778e0d51b"
    spk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/de405s_{}endian.bsp".format(
        sys.byteorder
    )
    spk_bigendian_md5 = "b010eb485bd01da5b651c58a6c8f8e67"
    spk_littleendian_md5 = "b4bb31ce13a006a4b20c124ad58b933a"
    gm_pck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/gm_de431.tpc"
    gm_pck_md5 = "6445f12003d1effcb432ea2671a51f18"
    lsk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/{}".format(
        currentLSK
    )
    lsk_md5 = "25a2fff30b0dedb4d76c06727b1895b1"
    pck = get_path_from_url(pck_url)
    spk = get_path_from_url(spk_url)
    gm_pck = get_path_from_url(gm_pck_url)
    lsk = get_path_from_url(lsk_url)
    standardKernelList = [pck, spk, gm_pck, lsk]
    testMetaKernel = os.path.join(TEST_FILE_DIR, "exampleKernels.txt")


def cleanup_core_kernels() -> None:
    cleanup_file(CoreKernels.pck)
    cleanup_file(CoreKernels.spk)
    cleanup_file(CoreKernels.gm_pck)
    cleanup_file(CoreKernels.lsk)


def get_kernel(url: str, provided_hash: str = None):
    kernel_name = get_kernel_name_from_url(url)
    kernel_file = os.path.join(KERNEL_DIR, kernel_name)
    # does not download if files are present, which allows us to potentially cache kernels
    if not os.path.isfile(kernel_file):
        attempt_download(url, kernel_name, kernel_file,
                         5, provided_hash=provided_hash)


def attempt_download(
    url: str,
    kernel_name: str,
    target_file_name: str,
    num_attempts: int,
    provided_hash: str = None,
) -> None:
    current_attempt = 0
    while current_attempt < num_attempts:
        print("Attempting to Download kernel: {}".format(kernel_name), flush=True)
        hasher = None if provided_hash is None else hashlib.md5()
        temp_filename = target_file_name + ".download"
        try:
            with requests.get(url, timeout=10, stream=True) as request, \
                    open(temp_filename, "wb") as current_kernel:
                for data in request.iter_content(chunk_size=(1 << 16)):
                    current_kernel.write(data)
                    if hasher:
                        hasher.update(data)
            print("Downloaded kernel: {}".format(kernel_name), flush=True)
            # check file hash if provided, assumes md5
            if hasher:
                file_hash = hasher.hexdigest()
                if provided_hash != file_hash:
                    raise AssertionError(
                        f"File {kernel_name} appears corrupted. "
                        f"Expected md5: {provided_hash} but got {file_hash} instead"
                    )
            os.rename(temp_filename, target_file_name)
            break
        except RequestException as h:
            print(f"Some http error when downloading kernel {kernel_name}, error: ",
                  f"{h}, trying again after a bit.")
        except TimeoutError:
            print(f"Download of kernel: {kernel_name} timed out, "
                  f"trying again after a bit.")
        except AssertionError as ae:
            print(f"Download of kernel: {kernel_name} failed with AssertionError, ({ae}), "
                  f"trying again after a bit.")
        current_attempt += 1
        print("\t Attempting to Download kernel again...", flush=True)
        time.sleep(2 + current_attempt)
    if current_attempt >= num_attempts:
        raise Exception(f"Error Downloading kernel: {kernel_name}, "
                        f"check if kernel exists at url: {url}"
                        )


def get_standard_kernels() -> None:
    print("\tChecking for kernels...\n", flush=True)
    get_kernel(CoreKernels.pck_url, CoreKernels.pck_md5)
    get_kernel(
        CoreKernels.spk_url,
        CoreKernels.spk_bigendian_md5
        if sys.byteorder == "big"
        else CoreKernels.spk_littleendian_md5,
    )
    get_kernel(CoreKernels.gm_pck_url, CoreKernels.gm_pck_md5)
    get_kernel(CoreKernels.lsk_url, CoreKernels.lsk_md5)


def get_extra_test_kernels() -> None:
    # these are test kernels not included in the standard meta kernel
    get_kernel(ExtraKernels.voyagerSclk_url, ExtraKernels.voyagerSclk_md5)
    get_kernel(ExtraKernels.earthTopoTf_url, ExtraKernels.earthTopoTf_md5)
    get_kernel(ExtraKernels.earthStnSpk_url, ExtraKernels.earthStnSpk_md5)
    get_kernel(ExtraKernels.earthHighPerPck_url,
               ExtraKernels.earthHighPerPck_md5)
    get_kernel(ExtraKernels.phobosDsk_url, ExtraKernels.phobosDsk_md5)
    get_kernel(ExtraKernels.marsSpk_url, ExtraKernels.marsSpk_md5)
    get_kernel(ExtraKernels.mroFk_url, ExtraKernels.mroFk_md5)
    get_kernel(ExtraKernels.geophysical_url, ExtraKernels.geophysical_md5)
    get_kernel(ExtraKernels.mro2007sub_url, ExtraKernels.mro2007sub_md5)
    get_kernel(ExtraKernels.spk430sub_url, ExtraKernels.spk430sub_md5)
    get_kernel(ExtraKernels.vexboomck_url, ExtraKernels.vexboomck_md5)
    get_kernel(ExtraKernels.v02swuck_url, ExtraKernels.v02swuck_md5)


def get_cassini_test_kernels() -> None:
    get_kernel(CassiniKernels.cassPck_url, CassiniKernels.cassPck_md5)
    get_kernel(CassiniKernels.satSpk_url, CassiniKernels.satSpk_md5)
    get_kernel(CassiniKernels.cassTourSpk_url, CassiniKernels.cassTourSpk_md5)
    get_kernel(CassiniKernels.cassFk_url, CassiniKernels.cassFk_md5)
    get_kernel(CassiniKernels.cassCk_url, CassiniKernels.cassCk_md5)
    get_kernel(CassiniKernels.cassSclk_url, CassiniKernels.cassSclk_md5)
    get_kernel(CassiniKernels.cassIk_url, CassiniKernels.cassIk_md5)


def write_test_meta_kernel() -> None:
    # Update the paths!
    with open(os.path.join(TEST_FILE_DIR, "exampleKernels.txt"), "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("KERNELS_TO_LOAD = (\n")
        for kernel in CoreKernels.standardKernelList:
            filename = os.path.join(KERNEL_DIR, kernel)
            lines = ["'"+filename[i:i+75] for i in range(0, len(filename), 75)]
            kernelFile.write("+'\n".join(lines) + "'\n")
        kernelFile.write(")\n")
        kernelFile.write("\\begintext")
    print("\nDone writing test meta kernel.", flush=True)


def download_kernels() -> None:
    get_standard_kernels()  # Download the kernels listed in kernelList and kernelURLlist
    get_cassini_test_kernels()  # Download Cassini kernels
    get_extra_test_kernels()  # Download any extra test kernels we need
    write_test_meta_kernel()  # Create the meta kernel file for tests


_PATHLIKE_FILENAME_VARIANT_FUNCTIONS =  {
    'string':   lambda pathlike: os.fsdecode(pathlike),
    'bytes':    lambda pathlike: os.fsencode(pathlike),
    'filepath': lambda pathlike: pathlike if isinstance(pathlike, os.PathLike) else Path(pathlike),
}


def checking_pathlike_filename_variants(variable_name: str):
    """
    Adding this annotation to a test (and adding the variable itself as an argument to the
    test) will cause the test to be called three times.  Each time, the variable will be
    bound to a different function:
    1) A function that returns its filename argument as a string,
    2) A function that returns its filename argument as a byte string,
    3) A function that returns its filename argument as a Path.
    These are the three "path-like values" defined by Python
    """
    parameters = [pytest.param(value, id=key) for key, value in
                  _PATHLIKE_FILENAME_VARIANT_FUNCTIONS.items()]
    def outer(function):
        return pytest.mark.parametrize(variable_name, parameters)(function)
    return outer
