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
    epoch, elems = cs.getelm(1950, tle)
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
    shape, frame, bsight, bounds = cs.getfov(-999004)
    assert shape == "POLYGON"
    assert frame == "SC999_INST004"
    npt.assert_array_almost_equal(bsight, [0.0, 1.0, 0.0])
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
    shape, frame, bsight, bounds = cs.getfvn("SC999_INST004")
    assert shape == "POLYGON"
    assert frame == "SC999_INST004"
    npt.assert_array_almost_equal(bsight, [0.0, 1.0, 0.0])
    expected = np.array([[0.0, 0.8, 0.5], [0.4, 0.8, -0.2], [-0.4, 0.8, -0.2]])
    npt.assert_array_almost_equal(expected, bounds)
    cleanup_kernel(kernel)
    
  
# Fails due to known issue
def fail_getmsg():
    cs.sigerr("test error")
    message = cs.getmsg("SHORT", 200)
    assert message == "test error"
    cs.reset()
    
    
def test_gfdist():
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2007 JAN 01 00:00:00 TDB")
    et1 = cs.str2et("2007 APR 01 00:00:00 TDB")
    cnfine = cs.cell_double(2)
    cs.wninsd(et0, et1, cnfine)
    result = cs.cell_double(1000)
    cs.gfdist(
        "moon", "none", "earth", ">", 400000, 0.0, cs.spd(), 1000, cnfine, result
    )
    count = cs.wncard(result)
    assert count == 4
    temp_results = []
    for i in range(0, count):
        left, right = cs.wnfetd(result, i)
        timstr_left = cs.timout(
            left, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
        )
        timstr_right = cs.timout(
            right, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
        )
        temp_results.append(timstr_left)
        temp_results.append(timstr_right)
    expected = [
        "2007-JAN-08 00:11:07.661897 (TDB)",
        "2007-JAN-13 06:37:47.937762 (TDB)",
        "2007-FEB-04 07:02:35.320555 (TDB)",
        "2007-FEB-10 09:31:01.829206 (TDB)",
        "2007-MAR-03 00:20:25.228066 (TDB)",
        "2007-MAR-10 14:04:38.482902 (TDB)",
        "2007-MAR-29 22:53:58.186230 (TDB)",
        "2007-APR-01 00:00:00.000000 (TDB)",
    ]
    assert temp_results == expected
    
    

# =============================================================================
# def fail_gfevnt():
#     cs.furnsh(CoreKernels.testMetaKernel)
#     #
#     et_start = cs.str2et("2001 jan 01 00:00:00.000")
#     et_end = cs.str2et("2001 dec 31 00:00:00.000")
#     cnfine = cs.cell_double(2)
#     cs.wninsd(et_start, et_end, cnfine)
#     result = cs.cell_double(1000)
#     qpnams = ["TARGET", "OBSERVER", "ABCORR"]
#     qcpars = ["MOON  ", "EARTH   ", "LT+S  "]
#     # Set the step size to 1/1000 day and convert to seconds
#     cs.gfsstp(0.001 * cs.spd())
#     # setup callbacks
#     udstep = spiceypy.utils.callbacks.SpiceUDSTEP(spice.gfstep)
#     udrefn = spiceypy.utils.callbacks.SpiceUDREFN(spice.gfrefn)
#     udrepi = spiceypy.utils.callbacks.SpiceUDREPI(spice.gfrepi)
#     udrepu = spiceypy.utils.callbacks.SpiceUDREPU(spice.gfrepu)
#     udrepf = spiceypy.utils.callbacks.SpiceUDREPF(spice.gfrepf)
#     udbail = spiceypy.utils.callbacks.SpiceUDBAIL(spice.gfbail)
#     qdpars = np.zeros(10, dtype=float)
#     qipars = np.zeros(10, dtype=np.int32)
#     qlpars = np.zeros(10, dtype=np.int32)
#     # call gfevnt
#     cs.gfevnt(
#         udstep,
#         udrefn,
#         "DISTANCE",
#         3,
#         81,
#         qpnams,
#         qcpars,
#         qdpars,
#         qipars,
#         qlpars,
#         "LOCMAX",
#         0,
#         1.0e-6,
#         0,
#         True,
#         udrepi,
#         udrepu,
#         udrepf,
#         10000,
#         True,
#         udbail,
#         cnfine,
#         result,
#     )
# 
#     # Verify the expected results
#     assert len(result) == 26
#     sTimout = "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
#     assert cs.timout(result[0], sTimout) == "2001-JAN-24 19:22:01.418715 (TDB)"
#     assert cs.timout(result[1], sTimout) == "2001-JAN-24 19:22:01.418715 (TDB)"
#     assert cs.timout(result[2], sTimout) == "2001-FEB-20 21:52:07.900872 (TDB)"
#     assert cs.timout(result[3], sTimout) == "2001-FEB-20 21:52:07.900872 (TDB)"
#     # Cleanup
#     if cs.gfbail():
#         cs.gfclrh()  # pragma: no cover
#     cs.gfsstp(0.5)
# =============================================================================
    
    
# =============================================================================
# def fail_gffove():
#     cs.furnsh(CoreKernels.testMetaKernel)
#     cs.furnsh(CassiniKernels.cassCk)
#     cs.furnsh(CassiniKernels.cassFk)
#     cs.furnsh(CassiniKernels.cassIk)
#     cs.furnsh(CassiniKernels.cassPck)
#     cs.furnsh(CassiniKernels.cassSclk)
#     cs.furnsh(CassiniKernels.cassTourSpk)
#     cs.furnsh(CassiniKernels.satSpk)
#     # Cassini ISS NAC observed Enceladus on 2013-FEB-25 from ~11:00 to ~12:00
#     # Split confinement window, from continuous CK coverage, into two pieces
#     et_start = cs.str2et("2013-FEB-25 10:00:00.000")
#     et_end = cs.str2et("2013-FEB-25 11:45:00.000")
#     cnfine = cs.cell_double(2)
#     cs.wninsd(et_start, et_end, cnfine)
#     result = cs.cell_double(1000)
#     # call gffove
#     udstep = spiceypy.utils.callbacks.SpiceUDSTEP(spice.gfstep)
#     udrefn = spiceypy.utils.callbacks.SpiceUDREFN(spice.gfrefn)
#     udrepi = spiceypy.utils.callbacks.SpiceUDREPI(spice.gfrepi)
#     udrepu = spiceypy.utils.callbacks.SpiceUDREPU(spice.gfrepu)
#     udrepf = spiceypy.utils.callbacks.SpiceUDREPF(spice.gfrepf)
#     udbail = spiceypy.utils.callbacks.SpiceUDBAIL(spice.gfbail)
#     cs.gfsstp(1.0)
#     cs.gffove(
#         "CASSINI_ISS_NAC",
#         "ELLIPSOID",
#         [0.0, 0.0, 0.0],
#         "ENCELADUS",
#         "IAU_ENCELADUS",
#         "LT+S",
#         "CASSINI",
#         1.0e-6,
#         udstep,
#         udrefn,
#         True,
#         udrepi,
#         udrepu,
#         udrepf,
#         True,
#         udbail,
#         cnfine,
#         result,
#     )
#     # Verify the expected results
#     assert len(result) == 2
#     sTimout = "YYYY-MON-DD HR:MN:SC UTC ::RND"
#     assert cs.timout(result[0], sTimout) == "2013-FEB-25 10:42:33 UTC"
#     assert cs.timout(result[1], sTimout) == "2013-FEB-25 11:45:00 UTC"
#     # Cleanup
#     if cs.gfbail():
#         cs.gfclrh()  # pragma: no cover
#     cs.gfsstp(0.5)
# =============================================================================
    
    
def test_gfilum():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.marsSpk)  # to get Phobos ephemeris
    # Hard-code the future position of MER-1
    # pos, lt = cs.spkpos("MER-1", cs.str2et("2006 OCT 02 00:00:00 UTC"), "iau_mars", "CN+S", "Mars")
    pos = [
        3376.17890941875839416753,
        -325.55203839445334779157,
        -121.47422900638389364758,
    ]
    # Two-month Viking orbiter window for Phobos;
    # - marsSPK runs from [1971 OCT 01] to [1972 OCT 01]
    startET = cs.str2et("1971 OCT 02 00:00:00 UTC")
    endET = cs.str2et("1971 NOV 30 12:00:00 UTC")
    # Create confining and result windows for incidence angle GF check
    cnfine = cs.cell_double(2000)
    cs.wninsd(startET, endET, cnfine)
    wnsolr = cs.cell_double(2000)
    # Find windows where solar incidence angle at MER-1 position is < 60deg
    cs.gfilum(
        "Ellipsoid",
        "INCIDENCE",
        "Mars",
        "Sun",
        "iau_mars",
        "CN+S",
        "PHOBOS",
        pos,
        "<",
        60.0 * cs.rpd(),
        0.0,
        21600.0,
        1000,
        cnfine,
        wnsolr,
    )
    # Create result window for emission angle GF check
    result = cs.cell_double(2000)
    # Find windows, within solar incidence angle windows found above (wnsolar),
    # where emission angle from MER-1 position to Phobos is < 20deg
    cs.gfilum(
        "Ellipsoid",
        "EMISSION",
        "Mars",
        "Sun",
        "iau_mars",
        "CN+S",
        "PHOBOS",
        pos,
        "<",
        20.0 * cs.rpd(),
        0.0,
        900.0,
        1000,
        wnsolr,
        result,
    )
    # Ensure there were some results
    assert cs.wncard(result) > 0
    startEpoch = cs.timout(result[0], "YYYY MON DD HR:MN:SC.###### UTC")
    endEpoch = cs.timout(result[-1], "YYYY MON DD HR:MN:SC.###### UTC")
    # Check times of results
    assert startEpoch.startswith("1971 OCT 02")
    assert endEpoch.startswith("1971 NOV 29")
    
    
# =============================================================================
# def fail_gfocce():
#     if cs.gfbail():
#         cs.gfclrh()  # pragma: no cover
#     cs.furnsh(CoreKernels.testMetaKernel)
#     et0 = cs.str2et("2001 DEC 01 00:00:00 TDB")
#     et1 = cs.str2et("2002 JAN 01 00:00:00 TDB")
#     cnfine = cs.cell_double(2)
#     cs.wninsd(et0, et1, cnfine)
#     result = cs.cell_double(1000)
#     cs.gfsstp(20.0)
#     udstep = spiceypy.utils.callbacks.SpiceUDSTEP(spice.gfstep)
#     udrefn = spiceypy.utils.callbacks.SpiceUDREFN(spice.gfrefn)
#     udrepi = spiceypy.utils.callbacks.SpiceUDREPI(spice.gfrepi)
#     udrepu = spiceypy.utils.callbacks.SpiceUDREPU(spice.gfrepu)
#     udrepf = spiceypy.utils.callbacks.SpiceUDREPF(spice.gfrepf)
#     udbail = spiceypy.utils.callbacks.SpiceUDBAIL(spice.gfbail)
#     # call gfocce
#     cs.gfocce(
#         "Any",
#         "moon",
#         "ellipsoid",
#         "iau_moon",
#         "sun",
#         "ellipsoid",
#         "iau_sun",
#         "lt",
#         "earth",
#         1.0e-6,
#         udstep,
#         udrefn,
#         True,
#         udrepi,
#         udrepu,
#         udrepf,
#         True,
#         udbail,
#         cnfine,
#         result,
#     )
#     if cs.gfbail():
#         cs.gfclrh()  # pragma: no cover
#     count = cs.wncard(result)
#     assert count == 1
# =============================================================================
    
    

# =============================================================================
# =============================================================================
# # frmchg
# =============================================================================
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
# =============================================================================
# =============================================================================
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
