import cspyce as cs
import numpy as np
import numpy.testing as npt
import os
import pytest

from gettestkernels import (
    CoreKernels,
    CassiniKernels,
    ExtraKernels,
    download_kernels,
    cleanup_core_kernels,
    TEST_FILE_DIR
)


@pytest.fixture(autouse=True)
def clear_kernel_pool_and_reset():
    cs.kclear()
    cs.reset()
    # yield for test
    yield
    # clear kernel pool again
    cs.kclear()
    cs.reset()


def cleanup_kernel(path):
    cs.kclear()
    cs.reset()
    if os.path.isfile(path):
        os.remove(path)  # pragma: no cover
    pass


def setup_module(module):
    download_kernels()
    

def test_failed():
    assert not cs.failed()
    
    
def test_fovray():
    # load kernels
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.satSpk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.cassCk)
    # core of test
    camid = cs.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, bounds = cs.getfov(camid)
    et = cs.str2et("2013 FEB 25 11:50:00 UTC")
    visible = cs.fovray(
        "CASSINI_ISS_NAC", [0.0, 0.0, 1.0], frame, "S", "CASSINI", et
    )
    assert visible is True
    

def test_fovtrg():
    # load kernels
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.satSpk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.cassCk)
    # core of test
    et = cs.str2et("2013 FEB 25 11:50:00 UTC")
    visible = cs.fovtrg(
        "CASSINI_ISS_NAC",
        "Enceladus",
        "Ellipsoid",
        "IAU_ENCELADUS",
        "LT+S",
        "CASSINI",
        et,
    )
    assert visible is True
    
    
def test_frame():
    vec = [23.0, -3.0, 18.0]
    x, y, z = cs.frame(vec)
    expected_x = [0.78338311, -0.10218041, 0.61308243]
    expected_y = [0.61630826, 0.0000000, -0.78750500]
    expected_z = [0.080467580, 0.99476588, 0.062974628]
    npt.assert_array_almost_equal(expected_x, x)
    npt.assert_array_almost_equal(expected_y, y)
    npt.assert_array_almost_equal(expected_z, z)
    
    
def test_frinfo():
    assert cs.frinfo(13000) == [399, 2, 3000]
    

# INSERT FRMCHG FUNCTION HERE


def test_frmnam():
    assert cs.frmnam(13000) == "ITRF93"
    assert cs.frmnam(13000) == "ITRF93"
    
    
def test_furnsh():
    cs.furnsh(CoreKernels.testMetaKernel)
    # 4 kernels + the meta kernel = 5
    assert cs.ktotal("ALL") == 5
    
    
def test_gcpool():
    # same as pcpool test
    import string

    data = [j + str(i) for i, j in enumerate(list(string.ascii_lowercase))]
    cs.pcpool("pcpool_test", data)
    cvals = cs.gcpool("pcpool_test")
    assert data == cvals
    
    
def test_gdpool():
    # same as pdpool test
    data = np.arange(0.0, 10.0)
    cs.pdpool("pdpool_array", data)
    dvals = cs.gdpool("pdpool_array")
    npt.assert_array_almost_equal(data, dvals)
    
    
def test_georec():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("EARTH", "RADII")
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * cs.rpd()
    lat = 32.0 * cs.rpd()
    alt = 0.0
    output = cs.georec(lon, lat, alt, radii[0], flat)
    expected = [-2541.74621567, 4780.329376, 3360.4312092]
    npt.assert_array_almost_equal(expected, output)
    
    
def test_getelm():
    tle = [
        "1 18123U 87 53  A 87324.61041692 -.00000023  00000-0 -75103-5 0 00675",
        "2 18123  98.8296 152.0074 0014950 168.7820 191.3688 14.12912554 21686",
    ]
    cs.furnsh(CoreKernels.testMetaKernel)
    epoch, elems = cs.getelm(1950, 75, tle)
    expected_elems = [
        -6.969196665949579e-13,
        0.0,
        -7.510300000000001e-06,
        1.724901918428988,
        2.653029617396028,
        0.001495,
        2.9458016181010693,
        3.3400156455905243,
        0.06164994027515544,
        -382310404.79526937,
    ]
    expected_epoch = -382310404.79526937
    npt.assert_array_almost_equal(expected_elems, elems)
    npt.assert_almost_equal(epoch, expected_epoch)


def test_getfat():
    arch, outtype = cs.getfat(CoreKernels.lsk)
    assert arch == "KPL"
    assert outtype == "LSK"
    # Add test for resulting string with length > 3.
    arch, outtype = cs.getfat(CassiniKernels.cassSclk)
    assert arch == "KPL"
    assert outtype == "SCLK"
    
    
def test_getfov():
    kernel = os.path.join(TEST_FILE_DIR, "getfov_test.ti")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("INS-999004_FOV_SHAPE            = 'POLYGON'\n")
        kernelFile.write("INS-999004_FOV_FRAME            = 'SC999_INST004'\n")
        kernelFile.write("INS-999004_BORESIGHT            = (  0.0,  1.0,  0.0 )\n")
        kernelFile.write("INS-999004_FOV_BOUNDARY_CORNERS = (  0.0,  0.8,  0.5,\n")
        kernelFile.write("                                     0.4,  0.8, -0.2,\n")
        kernelFile.write("                                    -0.4,  0.8, -0.2 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    cs.furnsh(kernel)
    shape, frame, bsight, n, bounds = cs.getfov(-999004, 4, 32, 32)
    assert shape == "POLYGON"
    assert frame == "SC999_INST004"
    npt.assert_array_almost_equal(bsight, [0.0, 1.0, 0.0])
    assert n == 3
    expected = np.array([[0.0, 0.8, 0.5], [0.4, 0.8, -0.2], [-0.4, 0.8, -0.2]])
    npt.assert_array_almost_equal(expected, bounds)
    cleanup_kernel(kernel)
    
    
def test_getfvn():
    kernel = os.path.join(TEST_FILE_DIR, "getfvn_test.ti")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("INS-999004_FOV_SHAPE            = 'POLYGON'\n")
        kernelFile.write("INS-999004_FOV_FRAME            = 'SC999_INST004'\n")
        kernelFile.write("INS-999004_BORESIGHT            = (  0.0,  1.0,  0.0 )\n")
        kernelFile.write("INS-999004_FOV_BOUNDARY_CORNERS = (  0.0,  0.8,  0.5,\n")
        kernelFile.write("                                     0.4,  0.8, -0.2,\n")
        kernelFile.write("                                    -0.4,  0.8, -0.2)\n")
        kernelFile.write("NAIF_BODY_CODE += ( -999004 )\n")
        kernelFile.write("NAIF_BODY_NAME += ( 'SC999_INST004' )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    cs.furnsh(kernel)
    shape, frame, bsight, n, bounds = cs.getfvn("SC999_INST004", 4, 32, 32)
    assert shape == "POLYGON"
    assert frame == "SC999_INST004"
    npt.assert_array_almost_equal(bsight, [0.0, 1.0, 0.0])
    assert n == 3
    expected = np.array([[0.0, 0.8, 0.5], [0.4, 0.8, -0.2], [-0.4, 0.8, -0.2]])
    npt.assert_array_almost_equal(expected, bounds)
    cleanup_kernel(kernel)
    
  
# Fails due to known issue
def fail_getmsg():
    cs.sigerr("test error")
    message = cs.getmsg("SHORT", 200)
    assert message == "test error"
    cs.reset()
# =============================================================================
# frmchg
# getmsg
# gfdist
# gfevnt
# gffove
# gfilum
# gfocce
# gfoclt
# gfpa
# gfposc
# gfrfov
# gfrr
# gfsep
# gfsntc
# gfstol
# gfsubc
# gftfov
# gipool
# gnpool
# halfpi
# hrmesp
# hrmint
# hx2dp
# ident
# illum
# illumf
# illumg
# ilumin
# inedpl
# inelpl
# inrypl
# intmax
# intmin
# invert
# invort
# invstm
# isordv
# isrchc
# isrchd
# isrchi
# isrot
# iswhsp
# j1900
# j1950
# j2000
# j2100
# jyear
# =============================================================================
