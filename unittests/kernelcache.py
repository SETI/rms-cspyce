import os
import platform
import pytest
import requests
import sys
import tempfile
import urllib3
import warnings

try:
    cwd = os.environ['CSPYCE_TEST_KERNELS']
except KeyError:
    cwd = "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
    
server = 'https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/'

warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)


def get_kernel_name_from_url(url: str) -> str:
    return url.split("/")[-1]


def get_path_from_url(url: str) -> str:
    return os.path.join(cwd, get_kernel_name_from_url(url))


class CassiniKernels(object):
    cassPck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cpck05Mar2004.tpc"
    cassPck_md5 = "8c16afc3bd886326e852b54bd71cc751"
# =============================================================================
#     satSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/130220AP_SE_13043_13073.bsp"
#     satSpk_md5 = "056c65b8a8064f2958aa097db40160b2"
#     cassTourSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/130212AP_SK_13043_13058.bsp"
#     cassTourSpk_md5 = "41210b787e06c1b8bce7ded3d0b930ab"
# =============================================================================
    cassFk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cas_v40.tf"
    cassFk_md5 = "99f1f5a1900afc536354306419dc119b"
    cassCk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/13056_13057ra.bc"
    cassCk_md5 = "d3acb29fd931b66e34120feb26f7efb7"
    cassSclk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cas00167.tsc"
    cassSclk_md5 = "a30faec21039ba589d3c88db6b5fb536"
    cassIk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cas_iss_v10.ti"
    cassIk_md5 = "101419660e4fe5856d30eb624da61a3f"
    cassPck = get_path_from_url(cassPck_url)
# =============================================================================
#     satSpk = get_path_from_url(satSpk_url)
#     cassTourSpk = get_path_from_url(cassTourSpk_url)
# =============================================================================
    cassFk = get_path_from_url(cassFk_url)
    cassCk = get_path_from_url(cassCk_url)
    cassSclk = get_path_from_url(cassSclk_url)
    cassIk = get_path_from_url(cassIk_url)
    
    
class CoreKernels(object):
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
    testMetaKernel = os.path.join(cwd, "exampleKernels.txt")    
    
    
class ExtraKernels(object):
    voyagerSclk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/vg200022.tsc"
    voyagerSclk_md5 = "4bcaf22788efbd86707c4b3c4d63c0c3"
    earthTopoTf_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/earth_topo_050714.tf"
    earthTopoTf_md5 = "fbde06c5abc5da969db984bb4ce5e6e0"
    earthStnSpk_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/earthstns_itrf93_050714.bsp"
    earthStnSpk_md5 = "a37d8d5e3023f0df7ead0e6b40d6a5b6"
    earthHighPerPck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/earth_031228_231229_predict.bpc"
    earthHighPerPck_md5 = "affa1da5adeee5ea4b0d7da54e4b69d7"
# =============================================================================
#     phobosDsk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/phobos_lores.bds"
#     phobosDsk_md5 = "68261460433bfc67b9e57bb57f79c5c9"
#     marsSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/mar022-1.bsp"
#     marsSpk_md5 = "d8d742db3f9502571fb5a5f8c55e8e62"
#     mroFk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/mro_v15.tf"
#     mroFk_md5 = "a938c271be63e0e5aa2ec86db89af109"
#     geophysical_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/geophysical.ker"
#     geophysical_md5 = "9a565ded819a9f0c6423b46f04e000db"
#     mro2007sub_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/mro_psp4_ssd_mro95a_sub.bsp"
#     mro2007sub_md5 = "8ed34eb77b21ac611f4680806677edfb"
#     spk430sub_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/de430sub.bsp"
#     spk430sub_md5 = "0b49545fa316f9053f5cfbcce155becc"
# =============================================================================
    vexboomck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/VEX_BOOM_V01.BC"
    vexboomck_md5 = "2f4dba65649246d72836fb3b53823c3d"
    v02swuck_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/vo2_swu_ck2.bc"
    v02swuck_md5 = "f59ef0556dfc63b55465e152f2d6f5a4"
    cklpfkrn_url = "https://pds-rings.seti.org/testrunner_support/cspyce-unit-test-kernels/cklpfkernel.bc"
    voyagerSclk = get_path_from_url(voyagerSclk_url)
    earthTopoTf = get_path_from_url(earthTopoTf_url)
    earthStnSpk = get_path_from_url(earthStnSpk_url)
    earthHighPerPck = get_path_from_url(earthHighPerPck_url)
    cklpfkrn = get_path_from_url(cklpfkrn_url)
# =============================================================================
#     phobosDsk = get_path_from_url(phobosDsk_url)
#     marsSpk = get_path_from_url(marsSpk_url)
#     mroFk = get_path_from_url(mroFk_url)
#     geophKer = get_path_from_url(geophysical_url)
#     mro2007sub = get_path_from_url(mro2007sub_url)
#     spk430sub = get_path_from_url(spk430sub_url)
# =============================================================================
    vexboomck = get_path_from_url(vexboomck_url)
    v02swuck = get_path_from_url(v02swuck_url)    
    
def cleanup_file(path):
    if os.path.exists(path):
        os.remove(path)
    pass
    

def get_kernel(url):
    kernel_name = get_kernel_name_from_url(url)
    kernel_file = os.path.join(server, kernel_name)
    # does not download if files are present, which allows us to potentially cache kernels
    if not os.path.isfile(kernel_file):
        current_kernel = requests.get(url, verify=False)
        with open(os.path.join(cwd, kernel_name), "wb") as kernel:
            kernel.write(current_kernel.content)
            
def get_cassini_test_kernels():
    get_kernel(CassiniKernels.cassPck_url)
    get_kernel(CassiniKernels.cassFk_url)
    get_kernel(CassiniKernels.cassCk_url)
    get_kernel(CassiniKernels.cassSclk_url)
    get_kernel(CassiniKernels.cassIk_url)
    
    
def get_standard_kernels() -> None:
    print("\tChecking for kernels...\n", flush=True)
    get_kernel(CoreKernels.pck_url)
    get_kernel(CoreKernels.spk_url)
    get_kernel(CoreKernels.gm_pck_url)
    get_kernel(CoreKernels.lsk_url)
    
    
def get_extra_test_kernels() -> None:
    # these are test kernels not included in the standard meta kernel
    get_kernel(ExtraKernels.voyagerSclk_url)
    get_kernel(ExtraKernels.earthTopoTf_url)
    get_kernel(ExtraKernels.earthStnSpk_url)
    get_kernel(ExtraKernels.earthHighPerPck_url)
    get_kernel(ExtraKernels.vexboomck_url)
    get_kernel(ExtraKernels.v02swuck_url)
    get_kernel(ExtraKernels.cklpfkrn_url)


def cleanup_core_kernels() -> None:
    cleanup_file(CoreKernels.pck)
    cleanup_file(CoreKernels.spk)
    cleanup_file(CoreKernels.gm_pck)
    cleanup_file(CoreKernels.lsk)


def write_test_meta_kernel() -> None:
    # Update the paths!
    with open(os.path.join(cwd, "exampleKernels.txt"), "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("KERNELS_TO_LOAD = (\n")
        for kernel in CoreKernels.standardKernelList:
            lines = ["'"+kernel[i:i+75] for i in range(0, len(kernel), 75)]
            kernelFile.write("+'\n".join(lines) + "'\n")
        kernelFile.write(")\n")
        kernelFile.write("\\begintext")
    print("\nDone writing test meta kernel.", flush=True)
    
    
def download_kernels():
    get_standard_kernels()  # Download the kernels listed in kernelList and kernelURLlist
    get_cassini_test_kernels()  # Download Cassini kernels
    get_extra_test_kernels()  # Download any extra test kernels we need
    write_test_meta_kernel()  # Create the meta kernel file for tests
