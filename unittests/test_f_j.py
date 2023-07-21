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
    assert data == list(cvals)


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
        kernelFile.write(
            "INS-999004_BORESIGHT            = (  0.0,  1.0,  0.0 )\n")
        kernelFile.write(
            "INS-999004_FOV_BOUNDARY_CORNERS = (  0.0,  0.8,  0.5,\n")
        kernelFile.write(
            "                                     0.4,  0.8, -0.2,\n")
        kernelFile.write(
            "                                    -0.4,  0.8, -0.2 )\n")
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
        kernelFile.write(
            "INS-999004_BORESIGHT            = (  0.0,  1.0,  0.0 )\n")
        kernelFile.write(
            "INS-999004_FOV_BOUNDARY_CORNERS = (  0.0,  0.8,  0.5,\n")
        kernelFile.write(
            "                                     0.4,  0.8, -0.2,\n")
        kernelFile.write(
            "                                    -0.4,  0.8, -0.2)\n")
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
def test_getmsg():
    cs.sigerr("test error")
    message = cs.getmsg("SHORT", 200)
    assert message == "test error"
    cs.reset()


def test_gfdist():
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2007 JAN 01 00:00:00 TDB")
    et1 = cs.str2et("2007 APR 01 00:00:00 TDB")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=1000)
    result = cs.gfdist(
        "moon", "none", "earth", ">", 400000, 0.0, cs.spd(), 1000, cnfine)
    count = int(len(result) / 2)
    assert count == 4
    temp_results = []
    arr = np.arange(0, (len(result)), 1)
    subarrays = [arr[i:i+2] for i in range(0, len(result), 2)]
    for i in subarrays:
        x = i[0]
        y = i[1]
        left, right = result[x], result[y]
        timstr_left = cs.timout(
            left, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
        )
        timstr_right = cs.timout(
            right, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
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


def test_gfevnt():
    cs.furnsh(CoreKernels.testMetaKernel)
    #
    et_start = cs.str2et("2001 jan 01 00:00:00.000")
    et_end = cs.str2et("2001 dec 31 00:00:00.000")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et_start, et_end, cnfine)
    result = cs.SpiceCell(typeno=1, size=1000)
    qpnams = ["TARGET", "OBSERVER", "ABCORR"]
    qcpars = ["MOON  ", "EARTH   ", "LT+S  "]
    # Set the step size to 1/1000 day and convert to seconds
    step = 0.001 * cs.spd()
    # setup callbacks
    qdpars = np.zeros(10, dtype=float)
    qipars = np.zeros(10, dtype=np.int32)
    qlpars = np.zeros(10, dtype=np.int32)
    # call gfevnt
    result = cs.gfevnt(
        step,
        "DISTANCE",
        qpnams,
        qcpars,
        qdpars,
        qipars,
        qlpars,
        "LOCMAX",
        0.0,
        1.0e-6,
        0.0,
        True,
        10000,
        cnfine
    )

    # Verify the expected results
    assert len(result) == 26
    sTimout = "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
    assert cs.timout(result[0], sTimout) == "2001-JAN-24 19:22:01.418715 (TDB)"
    assert cs.timout(result[1], sTimout) == "2001-JAN-24 19:22:01.418715 (TDB)"
    assert cs.timout(result[2], sTimout) == "2001-FEB-20 21:52:07.900872 (TDB)"
    assert cs.timout(result[3], sTimout) == "2001-FEB-20 21:52:07.900872 (TDB)"


def test_gffove():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.satSpk)
    # Cassini ISS NAC observed Enceladus on 2013-FEB-25 from ~11:00 to ~12:00
    # Split confinement window, from continuous CK coverage, into two pieces
    et_start = cs.str2et("2013-FEB-25 10:00:00.000")
    et_end = cs.str2et("2013-FEB-25 11:45:00.000")
    step = 1.0
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et_start, et_end, cnfine)
    result = cs.SpiceCell(typeno=1, size=1000)

    # call gffove
    result = cs.gffove(
        "CASSINI_ISS_NAC",
        "ELLIPSOID",
        [0.0, 0.0, 0.0],
        "ENCELADUS",
        "IAU_ENCELADUS",
        "LT+S",
        "CASSINI",
        1.0e-6,
        step,
        True,
        cnfine
    )
    # Verify the expected results
    assert len(result) == 2
    sTimout = "YYYY-MON-DD HR:MN:SC UTC ::RND"
    assert cs.timout(result[0], sTimout) == "2013-FEB-25 10:42:33 UTC"
    assert cs.timout(result[1], sTimout) == "2013-FEB-25 11:45:00 UTC"
    # Cleanup


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
    cnfine = cs.SpiceCell(typeno=1, size=2000)
    cs.wninsd(startET, endET, cnfine)
    wnsolr = cs.SpiceCell(typeno=1, size=2000)
    # Find windows where solar incidence angle at MER-1 position is < 60deg
    wnsolr = cs.gfilum(
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
        cnfine
    )
    # Create result window for emission angle GF check
    result = cs.SpiceCell(typeno=1, size=2000)
    # Find windows, within solar incidence angle windows found above (wnsolar),
    # where emission angle from MER-1 position to Phobos is < 20deg
    result = cs.gfilum(
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
        wnsolr
    )
    # Ensure there were some results
    assert len(result) > 0
    startEpoch = cs.timout(result[0], "YYYY MON DD HR:MN:SC.###### UTC")
    endEpoch = cs.timout(result[-1], "YYYY MON DD HR:MN:SC.###### UTC")
    # Check times of results
    assert startEpoch.startswith("1971 OCT 02")
    assert endEpoch.startswith("1971 NOV 29")


def test_gfocce():
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2001 DEC 01 00:00:00 TDB")
    et1 = cs.str2et("2002 JAN 01 00:00:00 TDB")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=1000)
    step = 20.0
    # call gfocce
    result = cs.gfocce(
        "Any",
        "moon",
        "ellipsoid",
        "iau_moon",
        "sun",
        "ellipsoid",
        "iau_sun",
        "lt",
        "earth",
        1.0e-6,
        step,
        True,
        cnfine
    )
    count = len(result) / 2
    assert count == 1


def test_gfoclt():
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2001 DEC 01 00:00:00 TDB")
    et1 = cs.str2et("2002 JAN 01 00:00:00 TDB")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=1000)
    result = cs.gfoclt(
        "any",
        "moon",
        "ellipsoid",
        "iau_moon",
        "sun",
        "ellipsoid",
        "iau_sun",
        "lt",
        "earth",
        180.0,
        cnfine,
    )
    count = len(result) / 2
    assert count == 1
    start, end = result[0], result[1]
    start_time = cs.timout(
        start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
    )
    end_time = cs.timout(
        end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
    assert start_time == "2001-DEC-14 20:10:14.203347 (TDB)"
    assert end_time == "2001-DEC-14 21:35:50.328804 (TDB)"


def test_gfpa():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {
        "=": [
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-07 14:07:55.480",
            "2006-DEC-07 14:07:55.480",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-30 11:41:32.568",
            "2007-JAN-30 11:41:32.568",
        ],
        "<": [
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-07 14:07:55.480",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-30 11:41:32.568",
            "2007-JAN-31 00:00:00.000",
        ],
        ">": [
            "2006-DEC-01 00:00:00.000",
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-07 14:07:55.480",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-30 11:41:32.568",
        ],
        "LOCMIN": [
            "2006-DEC-05 00:16:50.327",
            "2006-DEC-05 00:16:50.327",
            "2007-JAN-03 14:18:31.987",
            "2007-JAN-03 14:18:31.987",
        ],
        "ABSMIN": ["2007-JAN-03 14:18:31.987", "2007-JAN-03 14:18:31.987"],
        "LOCMAX": [
            "2006-DEC-20 14:09:10.402",
            "2006-DEC-20 14:09:10.402",
            "2007-JAN-19 04:27:54.610",
            "2007-JAN-19 04:27:54.610",
        ],
        "ABSMAX": ["2007-JAN-19 04:27:54.610", "2007-JAN-19 04:27:54.610"],
    }
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2006 DEC 01")
    et1 = cs.str2et("2007 JAN 31")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=2000)
    for relation in relate:
        cs.gfpa(
            "Moon",
            "Sun",
            "LT+S",
            "Earth",
            relation,
            0.57598845,
            0.0,
            cs.spd(),
            5000,
            cnfine
        )
        count = len(result) / 2
        if count > 0:
            temp_results = []
            arr = np.arange(0, (len(result)), 1)
            subarrays = [arr[i:i+2] for i in range(0, len(result), 2)]
            for i in subarrays:
                x = i[0]
                y = i[1]
                left, right = result[x], result[y]
                timstr_left = cs.timout(left, "YYYY-MON-DD HR:MN:SC.###")
                timstr_right = cs.timout(right, "YYYY-MON-DD HR:MN:SC.###")
                temp_results.append(timstr_left)
                temp_results.append(timstr_right)
            assert temp_results == expected.get(relation)


def test_gfposc():
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2007 JAN 01")
    et1 = cs.str2et("2008 JAN 01")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=1000)
    result = cs.gfposc(
        "sun",
        "iau_earth",
        "none",
        "earth",
        "latitudinal",
        "latitude",
        "absmax",
        0.0,
        0.0,
        90.0 * cs.spd(),
        1000,
        cnfine
    )
    count = len(result) / 2
    assert count == 1
    start, end = result[0], result[1]
    start_time = cs.timout(
        start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
    )
    end_time = cs.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
    assert start_time == end_time
    assert start_time == "2007-JUN-21 17:54:13.201561 (TDB)"


def test_gfrfov():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.satSpk)
    # Changed ABCORR to NONE from S for this test, so we do not need SSB
    # begin test
    inst = "CASSINI_ISS_WAC"
    # Cassini ISS NAC observed Enceladus on 2013-FEB-25 from ~11:00 to ~12:00
    # Split confinement window, from continuous CK coverage, into two pieces
    et_start1 = cs.str2et("2013-FEB-25 07:20:00.000")
    et_end1 = cs.str2et("2013-FEB-25 11:45:00.000")  # \
    et_start2 = cs.str2et("2013-FEB-25 11:55:00.000")  # _>synthetic 10min gap
    et_end2 = cs.str2et("2013-FEB-26 14:25:00.000")
    cnfine = cs.SpiceCell(typeno=1, size=4)
    cnfine = cs.wninsd(et_start1, et_end1, cnfine)
    cnfine = cs.wninsd(et_start2, et_end2, cnfine)
    # The ray direction vector is from Cassini toward Enceladus during the gap
    et_nom = cs.str2et("2013-FEB-25 11:50:00.000")  # \
    raydir, lt = cs.spkpos("Enceladus", et_nom, "J2000", "NONE", "Cassini")
    result = cs.SpiceCell(typeno=1, size=2000)
    result = cs.gfrfov(inst, raydir, "J2000", "NONE", "Cassini", 10.0, cnfine)
    # Verify the expected results
    assert len(result) == 4
    sTimout = "YYYY-MON-DD HR:MN:SC UTC ::RND"
    assert cs.timout(result[0], sTimout) == "2013-FEB-25 11:26:46 UTC"
    assert cs.timout(result[1], sTimout) == "2013-FEB-25 11:45:00 UTC"
    assert cs.timout(result[2], sTimout) == "2013-FEB-25 11:55:00 UTC"
    assert cs.timout(result[3], sTimout) == "2013-FEB-25 12:05:33 UTC"


def test_gfrr():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {
        "=": [
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-19 22:04:54.905",
            "2007-JAN-19 22:04:54.905",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-17 11:10:46.547",
            "2007-FEB-17 11:10:46.547",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-18 09:59:05.966",
            "2007-MAR-18 09:59:05.966",
        ],
        "<": [
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-19 22:04:54.905",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-17 11:10:46.547",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-18 09:59:05.966",
        ],
        ">": [
            "2007-JAN-01 00:00:00.000",
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-19 22:04:54.905",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-17 11:10:46.547",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-18 09:59:05.966",
            "2007-APR-01 00:00:00.000",
        ],
        "LOCMIN": [
            "2007-JAN-11 07:03:59.001",
            "2007-JAN-11 07:03:59.001",
            "2007-FEB-10 06:26:15.451",
            "2007-FEB-10 06:26:15.451",
            "2007-MAR-12 03:28:36.414",
            "2007-MAR-12 03:28:36.414",
        ],
        "ABSMIN": ["2007-JAN-11 07:03:59.001", "2007-JAN-11 07:03:59.001"],
        "LOCMAX": [
            "2007-JAN-26 02:27:33.772",
            "2007-JAN-26 02:27:33.772",
            "2007-FEB-24 09:35:07.822",
            "2007-FEB-24 09:35:07.822",
            "2007-MAR-25 17:26:56.158",
            "2007-MAR-25 17:26:56.158",
        ],
        "ABSMAX": ["2007-MAR-25 17:26:56.158", "2007-MAR-25 17:26:56.158"],
    }
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2007 JAN 01")
    et1 = cs.str2et("2007 APR 01")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cs.wninsd(et0, et1, cnfine)
    for relation in relate:
        result = cs.SpiceCell(typeno=1, size=2000)
        cs.gfrr(
            "moon",
            "none",
            "sun",
            relation,
            0.3365,
            0.0,
            cs.spd(),
            2000,
            cnfine
        )
        count = len(result) / 2
        if count > 0:
            temp_results = []
            arr = np.arange(0, (len(result)), 1)
            subarrays = [arr[i:i+2] for i in range(0, len(result), 2)]
            for i in subarrays:
                x = i[0]
                y = i[1]
                left, right = result[x], result[y]
                timstr_left = cs.timout(left, "YYYY-MON-DD HR:MN:SC.###")
                timstr_right = cs.timout(right, "YYYY-MON-DD HR:MN:SC.###")
                temp_results.append(timstr_left)
                temp_results.append(timstr_right)
            assert temp_results == expected.get(relation)


def test_gfsep():
    cs.furnsh(CoreKernels.testMetaKernel)
    expected = [
        "2007-JAN-03 14:20:24.628017 (TDB)",
        "2007-FEB-02 06:16:24.111794 (TDB)",
        "2007-MAR-03 23:22:42.005064 (TDB)",
        "2007-APR-02 16:49:16.145506 (TDB)",
        "2007-MAY-02 09:41:43.840096 (TDB)",
        "2007-JUN-01 01:03:44.537483 (TDB)",
        "2007-JUN-30 14:15:26.586223 (TDB)",
        "2007-JUL-30 01:14:49.010797 (TDB)",
        "2007-AUG-28 10:39:01.398087 (TDB)",
        "2007-SEP-26 19:25:51.519413 (TDB)",
        "2007-OCT-26 04:30:56.635336 (TDB)",
        "2007-NOV-24 14:31:04.341632 (TDB)",
        "2007-DEC-24 01:40:12.245932 (TDB)",
    ]
    et0 = cs.str2et("2007 JAN 01")
    et1 = cs.str2et("2008 JAN 01")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=2000)
    result = cs.gfsep(
        "MOON",
        "SPHERE",
        "NULL",
        "SUN",
        "SPHERE",
        "NULL",
        "NONE",
        "EARTH",
        "LOCMAX",
        0.0,
        0.0,
        6.0 * cs.spd(),
        1000,
        cnfine
    )
    count = len(result) / 2
    assert count == 13
    temp_results = []
    arr = np.arange(0, (len(result)), 1)
    subarrays = [arr[i:i+2] for i in range(0, len(result), 2)]
    for i in subarrays:
        x = i[0]
        y = i[1]
        start, end = result[x], result[y]
        assert start == end
        temp_results.append(
            cs.timout(start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
        )
    assert temp_results == expected


def test_gfsntc():
    kernel = os.path.join(TEST_FILE_DIR, "gfnstc_test.tf")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("FRAME_SEM                     =  10100000\n")
        kernelFile.write("FRAME_10100000_NAME           = 'SEM'\n")
        kernelFile.write("FRAME_10100000_CLASS          =  5\n")
        kernelFile.write("FRAME_10100000_CLASS_ID       =  10100000\n")
        kernelFile.write("FRAME_10100000_CENTER         =  10\n")
        kernelFile.write("FRAME_10100000_RELATIVE       = 'J2000'\n")
        kernelFile.write("FRAME_10100000_DEF_STYLE      = 'PARAMETERIZED'\n")
        kernelFile.write("FRAME_10100000_FAMILY         = 'TWO-VECTOR'\n")
        kernelFile.write("FRAME_10100000_PRI_AXIS       = 'X'\n")
        kernelFile.write(
            "FRAME_10100000_PRI_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'\n")
        kernelFile.write("FRAME_10100000_PRI_OBSERVER   = 'SUN'\n")
        kernelFile.write("FRAME_10100000_PRI_TARGET     = 'EARTH'\n")
        kernelFile.write("FRAME_10100000_PRI_ABCORR     = 'NONE'\n")
        kernelFile.write("FRAME_10100000_SEC_AXIS       = 'Y'\n")
        kernelFile.write(
            "FRAME_10100000_SEC_VECTOR_DEF = 'OBSERVER_TARGET_VELOCITY'\n")
        kernelFile.write("FRAME_10100000_SEC_OBSERVER   = 'SUN'\n")
        kernelFile.write("FRAME_10100000_SEC_TARGET     = 'EARTH'\n")
        kernelFile.write("FRAME_10100000_SEC_ABCORR     = 'NONE'\n")
        kernelFile.write("FRAME_10100000_SEC_FRAME      = 'J2000'\n")
        kernelFile.close()
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(kernel)
    et0 = cs.str2et("2007 JAN 01")
    et1 = cs.str2et("2008 JAN 01")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=2000)
    result = cs.gfsntc(
        "EARTH",
        "IAU_EARTH",
        "Ellipsoid",
        "NONE",
        "SUN",
        "SEM",
        [1.0, 0.0, 0.0],
        "LATITUDINAL",
        "LATITUDE",
        "=",
        0.0,
        0.0,
        90.0 * cs.spd(),
        1000,
        cnfine
    )
    count = len(result) / 2
    assert count > 0
    beg, end = result[0], result[1]
    begstr = cs.timout(
        beg, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
    endstr = cs.timout(
        end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
    assert begstr == "2007-MAR-21 00:01:25.527303 (TDB)"
    assert endstr == "2007-MAR-21 00:01:25.527303 (TDB)"
    beg, end = result[2], result[3]
    begstr = cs.timout(
        beg, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
    endstr = cs.timout(
        end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
    assert begstr == "2007-SEP-23 09:46:39.606982 (TDB)"
    assert endstr == "2007-SEP-23 09:46:39.606982 (TDB)"
    cleanup_kernel(kernel)


def test_gfstol():
    cs.gfstol(1.0e-16)
    cs.gfstol(1.0e-6)


def test_gfsubc():
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2007 JAN 01")
    et1 = cs.str2et("2008 JAN 01")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=2000)
    result = cs.gfsubc(
        "earth",
        "iau_earth",
        "Near point: ellipsoid",
        "none",
        "sun",
        "geodetic",
        "latitude",
        ">",
        16.0 * cs.rpd(),
        0.0,
        cs.spd() * 90.0,
        1000,
        cnfine
    )
    count = len(result) / 2
    assert count > 0
    start, end = result[0], result[1]
    start_time = cs.timout(
        start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
    )
    end_time = cs.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND")
    assert start_time == "2007-MAY-04 17:08:56.724320 (TDB)"
    assert end_time == "2007-AUG-09 01:51:29.307830 (TDB)"


def test_gftfov():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.satSpk)
    # Changed ABCORR to LT from LT+S for this test, so we do not need SSB
    # begin test
    # Cassini ISS NAC observed Enceladus on 2013-FEB-25 from ~11:00 to ~12:00
    # Split confinement window, from continuous CK coverage, into two pieces
    et_start1 = cs.str2et("2013-FEB-25 07:20:00.000")
    et_end1 = cs.str2et("2013-FEB-25 11:45:00.000")  # \
    et_start2 = cs.str2et("2013-FEB-25 11:55:00.000")  # _>synthetic 10min gap
    et_end2 = cs.str2et("2013-FEB-26 14:25:00.000")
    cnfine = cs.SpiceCell(typeno=1, size=4)
    cnfine = cs.wninsd(et_start1, et_end1, cnfine)
    cnfine = cs.wninsd(et_start2, et_end2, cnfine)
    # Subtract off the position of the spacecraft relative to the solar system barycenter the result is the ray's direction vector.
    result = cs.gftfov(
        "CASSINI_ISS_NAC",
        "ENCELADUS",
        "ELLIPSOID",
        "IAU_ENCELADUS",
        "LT",
        "CASSINI",
        10.0,
        cnfine
    )
    # Verify the expected results
    assert len(result) == 4
    sTimout = "YYYY-MON-DD HR:MN:SC UTC ::RND"
    assert cs.timout(result[0], sTimout) == "2013-FEB-25 10:42:33 UTC"
    assert cs.timout(result[1], sTimout) == "2013-FEB-25 11:45:00 UTC"
    assert cs.timout(result[2], sTimout) == "2013-FEB-25 11:55:00 UTC"
    assert cs.timout(result[3], sTimout) == "2013-FEB-25 12:04:30 UTC"
# =============================================================================
# frmchg
# =============================================================================


def test_gipool():
    # same as pipool test
    data = np.arange(0, 10)
    cs.pipool("pipool_array", data)
    ivals = cs.gipool("pipool_array", 0)
    npt.assert_array_almost_equal(data, ivals)


def test_gnpool():
    cs.furnsh(CoreKernels.testMetaKernel)
    var = "BODY599*"
    index = 0
    expected = [
        "BODY599_POLE_DEC",
        "BODY599_LONG_AXIS",
        "BODY599_PM",
        "BODY599_RADII",
        "BODY599_POLE_RA",
        "BODY599_GM",
        "BODY599_NUT_PREC_PM",
        "BODY599_NUT_PREC_DEC",
        "BODY599_NUT_PREC_RA",
    ]
    kervar = cs.gnpool(var, index)
    assert set(expected) == set(kervar)


def test_halfpi():
    assert cs.halfpi() == np.pi / 2


def test_hrmesp():
    yvals = [6.0, 3.0, 8.0, 11.0, 2210.0, 5115.0, 78180.0, 109395.0]
    answer, deriv = cs.hrmesp(-1.0, 2.0, yvals, 2.0)
    assert answer == pytest.approx(141.0)
    assert deriv == pytest.approx(456.0)


def test_hrmint():
    xvals = [-1.0, 0.0, 3.0, 5.0]
    yvals = [[6.0, 3.0], [5.0, 0.0], [2210.0, 5115.0], [78180.0, 109395.0]]
    answer, deriv = cs.hrmint(xvals, yvals, 2.0)
    assert answer == pytest.approx(141.0)
    assert deriv == pytest.approx(456.0)


# Fails due to error andling
def fail_hx2dp():
    assert cs.hx2dp("1^1") == 1.0
    assert cs.hx2dp("7F5EB^5") == 521707.0
    assert cs.hx2dp("+1B^+2") == 27.0
    # Bad value
    badReturn = "ERROR: Illegal character 'Z' encountered."
    assert cs.hx2dp("1Z^+2")[: len(badReturn)] == badReturn


def test_ident():
    ident = cs.ident()
    expected = np.identity(3)
    npt.assert_array_almost_equal(ident, expected)


def test_illum():
    # Nearly the same as first half of test_edterm
    # possibly not smart to pick a terminator point for test.
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2007 FEB 3 00:00:00.000")
    trgepc, obspos, trmpts = cs.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trmpts0 = [
        -1.53978381936825627463e02,
        -1.73056331949840728157e03,
        1.22893325627419600088e-01,
    ]
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    phase, solar, emissn = cs.illum("MOON", et, "LT+S", "EARTH", trmpts[0])
    npt.assert_almost_equal(cs.dpr() * phase, 9.206597597007834)
    npt.assert_almost_equal(cs.dpr() * solar, 90.26976568986987)
    npt.assert_almost_equal(cs.dpr() * emissn, 99.27359835825851)


# Test changed. Added 'found' variable, got rid of 'n' result
def test_illumf():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.satSpk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.cassCk)
    et = cs.str2et("2013 FEB 25 11:50:00 UTC")
    # start of test
    camid = cs.bodn2c("CASSINI_ISS_NAC")
    shape, obsref, bsight, bounds = cs.getfov(camid)
    # run sincpt on boresight vector
    spoint, etemit, srfvec, found = cs.sincpt(
        "Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", obsref, bsight
    )
    trgepc2, srfvec2, phase, incid, emissn, visibl, lit = cs.illumf(
        "Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint
    )
    phase = phase * cs.dpr()
    incid = incid * cs.dpr()
    emissn = emissn * cs.dpr()
    assert phase == pytest.approx(161.82854377660345)
    assert incid == pytest.approx(134.92108561449996)
    assert emissn == pytest.approx(63.23618556218115)
    assert not lit  # Incidence angle is greater than 90deg
    assert visibl  # Emission angle is less than 90deg


def test_illumg():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.satSpk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.cassCk)
    et = cs.str2et("2013 FEB 25 11:50:00 UTC")
    spoint, trgepc, srfvec = cs.subpnt(
        "Near Point/Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "Earth"
    )
    trgepc2, srfvec2, phase, incid, emissn = cs.illumg(
        "Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint
    )
    phase = phase * cs.dpr()
    incid = incid * cs.dpr()
    emissn = emissn * cs.dpr()
    assert phase == pytest.approx(161.859925246638)
    assert incid == pytest.approx(18.47670084384343)
    assert emissn == pytest.approx(143.6546170649875)


def test_ilumin():
    # Same as first half of test_edterm
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2007 FEB 3 00:00:00.000")
    trgepc, obspos, trmpts = cs.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trgepc = 223732863.86351672
    expected_obspos = [
        394721.1024056578753516078,
        27265.11780063395417528227,
        -19069.08478859506431035697,
    ]
    expected_trmpts0 = [
        -1.53978381936825627463e02,
        -1.73056331949840728157e03,
        1.22893325627419600088e-01,
    ]
    expected_trmpts1 = [
        87.37506200891714058798,
        864.40670594653545322217,
        1504.56817899807947469526,
    ]
    expected_trmpts2 = [42.213243378688254,
                        868.21134651980412, -1504.3223922609538]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = cs.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[0]
    )
    npt.assert_almost_equal(cs.dpr() * solar0, 90.269765819)
    iluet1, srfvec1, phase1, solar1, emissn1 = cs.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[1]
    )
    npt.assert_almost_equal(cs.dpr() * solar1, 90.269765706)
    iluet2, srfvec2, phase2, solar2, emissn2 = cs.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[2]
    )
    npt.assert_almost_equal(cs.dpr() * solar2, 90.269765730)


# Test changed
def test_inedpl():
    cs.furnsh(CoreKernels.testMetaKernel)
    TIME = "Oct 31 2002, 12:55:00 PST"
    FRAME = "J2000"
    CORR = "LT+S"
    et = cs.str2et(TIME)
    state, ltime = cs.spkezr("EARTH", et, FRAME, CORR, "SUN")
    pos = state[0:3]
    radii = cs.bodvrd("EARTH", "RADII")
    pos = [pos[0] / radii[0] ** 2.0, pos[1] /
           radii[1] ** 2.0, pos[2] / radii[2] ** 2.0]
    plane = cs.nvc2pl(pos, 1.0)
    term = cs.inedpl(radii[0], radii[1], radii[2], plane)
    expected_center = [0.21512031, 0.15544527, 0.067391641]
    expected_s_major = [
        -3.73561164720596843836e03,
        5.16970328302375583007e03,
        1.35988201424391742850e-11,
    ]
    expected_s_minor = [
        -1276.33357469839393161237,
        -922.27470443423590040766,
        6159.97371233560443215538,
    ]
    center = term[0][0:3]
    semi_major = term[0][3:6]
    semi_minor = term[0][6:9]
    npt.assert_array_almost_equal(center, expected_center)
    npt.assert_array_almost_equal(semi_major, expected_s_major, decimal=5)
    npt.assert_array_almost_equal(semi_minor, expected_s_minor, decimal=5)
    npt.assert_almost_equal(cs.vnorm(semi_major), 6378.1365, decimal=2)
    npt.assert_almost_equal(cs.vnorm(semi_minor), 6358.0558, decimal=2)


def test_inelpl():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("SATURN", "RADII")
    vertex = [100.0 * radii[0], 0.0, radii[0] * 100.0]
    limb = cs.edlimb(radii[0], radii[1], radii[2], vertex)
    normal = [0.0, 0.0, 1.0]
    point = [0.0, 0.0, 0.0]
    plane = cs.nvp2pl(normal, point)
    nxpts, xpt1, xpt2 = cs.inelpl(limb, plane)
    expectedXpt1 = [602.68000, 60264.9865, 0.0]
    expectedXpt2 = [602.68000, -60264.9865, 0.0]
    assert nxpts == 2.0
    npt.assert_array_almost_equal(expectedXpt1, xpt1, decimal=4)
    npt.assert_array_almost_equal(expectedXpt2, xpt2, decimal=4)


def test_inrypl():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("SATURN", "RADII")
    vertex = [3.0 * radii[0], 0.0, radii[2] * 0.5]
    dire = [0.0, np.cos(30.0 * cs.rpd()), -1.0 * np.sin(30.0 * cs.rpd())]
    normal = [0.0, 0.0, 1.0]
    point = [0.0, 0.0, 0.0]
    plane = cs.nvp2pl(normal, point)
    nxpts, xpt = cs.inrypl(vertex, dire, plane)
    expectedXpt = np.array([180804.0, 47080.6050513, 0.0])
    assert nxpts == 1
    np.testing.assert_almost_equal(np.array(xpt), expectedXpt, decimal=6)


def test_intmax():
    assert cs.intmax() >= 2147483647 or cs.intmax() >= 32768


def test_intmin():
    assert cs.intmin() <= -2147483648 or cs.intmin() <= -32768


def test_invert():
    m1 = np.array([[0.0, -1.0, 0.0], [0.5, 0.0, 0.0], [0.0, 0.0, 1.0]])
    expected = np.array([[0.0, 2.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    mout = cs.invert(m1)
    assert np.array_equal(expected, mout)


def test_invort():
    # I think this is valid...
    m = cs.ident()
    mit = cs.invort(m)
    npt.assert_array_almost_equal(m, mit)


def test_invstm():
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2003 Oct 13 06:00:00")
    mat = cs.tisbod("J2000", 3000, et)
    invmat = cs.invstm(mat)
    state = [
        175625246.29100420,
        164189388.12540060,
        -62935198.26067264,
        11946.73372264,
        -12771.29732556,
        13.84902914,
    ]
    istate1 = cs.mxvg(invmat, state)
    xmat = cs.sxform("ITRF93", "J2000", et)
    istate2 = cs.mxvg(xmat, state)
    npt.assert_array_almost_equal(istate1, istate2)


def test_isordv():
    assert cs.isordv([0, 1])
    assert cs.isordv([0, 1, 2])
    assert cs.isordv([0, 1, 2, 3])
    assert cs.isordv([1, 1, 1]) is False


def test_isrchc():
    array = ["1", "0", "4", "2"]
    assert cs.isrchc("4", array) == 2
    assert cs.isrchc("2", array) == 3
    assert cs.isrchc("3", array) == -1


def test_isrchd():
    array = [1.0, 0.0, 4.0, 2.0]
    assert cs.isrchd(4.0, array) == 2
    assert cs.isrchd(2.0, array) == 3
    assert cs.isrchd(3.0, array) == -1


def test_isrchi():
    array = [1, 0, 4, 2]
    assert cs.isrchi(4, array) == 2
    assert cs.isrchi(2, array) == 3
    assert cs.isrchi(3, array) == -1


def test_isrot():
    assert cs.isrot(cs.ident(), 0.0001, 0.0001)


def test_iswhsp():
    assert cs.iswhsp("       ")
    assert cs.iswhsp("cs") is False


def test_j1900():
    assert cs.j1900() == 2415020.0


def test_j1950():
    assert cs.j1950() == 2433282.5


def test_j2000():
    assert cs.j2000() == 2451545.0


def test_j2100():
    assert cs.j2100() == 2488070.0


def test_jyear():
    assert cs.jyear() == 31557600.0
