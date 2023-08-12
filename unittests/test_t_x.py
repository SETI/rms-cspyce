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
    cleanup_cassini_kernels,
    cleanup_extra_kernels,
    TEST_FILE_DIR,
    checking_pathlike_filename_variants
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


# Test changed: furnsh() only works on one kernel at a time.
def test_tangpt():
    cs.reset()
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(CoreKernels.pck)
    cs.furnsh(CoreKernels.spk)
    cs.furnsh(CassiniKernels.satSpk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    cs.furnsh(ExtraKernels.earthStnSpk)
    locus = "TANGENT POINT"
    sc = "CASSINI"
    target = "SATURN"
    obsrvr = "DSS-14"
    fixref = "IAU_SATURN"
    rayfrm = "J2000"
    et = cs.str2et("2013-FEB-13 11:21:20.213872 (TDB)")
    raydir, raylt = cs.spkpos(sc, et, rayfrm, "NONE", obsrvr)
    tanpt, alt, range, srfpt, trgepc, srfvec = cs.tangpt(
        "ELLIPSOID", target, et, fixref, "NONE", locus, obsrvr, rayfrm, raydir
    )
    npt.assert_array_almost_equal(
        tanpt, [-113646.428171, 213634.489363, -222709.965702], decimal=5
    )
    assert alt == pytest.approx(271285.892825)
    assert range == pytest.approx(1425243487.098913)
    npt.assert_array_almost_equal(
        srfpt, [-21455.320586, 40332.076698, -35458.506180], decimal=5
    )
    assert trgepc == pytest.approx(414026480.213872)


# Test changed to check length of subarray of points
def test_termpt():
    cs.reset()
    cs.furnsh(CoreKernels.spk)
    cs.furnsh(ExtraKernels.marsSpk)
    cs.furnsh(CoreKernels.pck)
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(ExtraKernels.phobosDsk)
    # set the time
    et = cs.str2et("1972 AUG 11 00:00:00")
    # call limpt
    npts, points, epochs, tangts = cs.termpt(
        "UMBRAL/TANGENT/DSK/UNPRIORITIZED",
        "SUN",
        "Phobos",
        et,
        "IAU_PHOBOS",
        "CN+S",
        "CENTER",
        "MARS",
        [0.0, 0.0, 1.0],
        cs.twopi() / 3.0,
        3,
        1.0e-4,
        1.0e-7,
        10000,
    )
    assert points is not None
    assert len(points[0]) == 3


# Test changed: does not need a lenout parameter
def test_timdef():
    LSK = os.path.join(TEST_FILE_DIR, CoreKernels.lsk)
    cs.furnsh(LSK)
    # Calendar - default is Gregorian
    value = cs.timdef("GET", "CALENDAR", "GREGORIAN")
    assert value == "GREGORIAN" or "JULIAN" or "MIXED"
    # System - ensure it changes the str2et results
    assert "UTC" == cs.timdef("GET", "SYSTEM", "UTC")
    # Approximately 64.184
    saveET = cs.str2et("2000-01-01T12:00:00")
    # Change to TDB system
    assert "TDB" == cs.timdef("SET", "SYSTEM", "TDB")
    assert 0.0 == cs.str2et("2000-01-01T12:00:00")
    # Change back to UTC system
    assert "UTC" == cs.timdef("SET", "SYSTEM", "UTC")
    assert saveET == cs.str2et("2000-01-01T12:00:00")
    # Cleanup


# Test changed: tpictr() only has one returned value
def test_timout():
    sample = "Thu Oct 1 11:11:11 PDT 1111"
    cs.furnsh(CoreKernels.testMetaKernel)
    pic = cs.tpictr(sample)
    et = 188745364.0
    out = cs.timout(et, pic)
    assert out == "Sat Dec 24 18:14:59 PDT 2005"


def test_tipbod():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Jan 1 2005")
    tipm = cs.tipbod("J2000", 699, et)
    assert tipm is not None


def test_tisbod():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Jan 1 2005")
    tsipm = cs.tisbod("J2000", 699, et)
    assert tsipm is not None


def test_tkfram():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassFk)
    rotation, nextFrame = cs.tkfram(-82001)
    expected = np.array(
        [
            [6.12323400e-17, 0.00000000e00, -1.00000000e00],
            [0.00000000e00, 1.00000000e00, -0.00000000e00],
            [1.00000000e00, 0.00000000e00, 6.12323400e-17],
        ]
    ).T
    npt.assert_array_almost_equal(rotation, expected)
    assert nextFrame == -82000


def test_tkvrsn():
    version = cs.tkvrsn("toolkit")
    assert version == "CSPICE_N0067"


def fail_tparch():
    cs.tparch("NO")
    cs.tparch("YES")
    a, e = cs.tparse("FEB 34, 1993")
    assert "The day of the month specified for the month of February was 3.40E+01." in e
    cs.tparch("NO")
    a, e = cs.tparse("FEB 34, 1993")
    assert (
        "The day of the month specified for the month of February was 3.40E+01."
        not in e
    )


def test_tparse():
    actual_one = cs.tparse("1996-12-18T12:28:28")
    assert actual_one == -95815892.0
    actual_two = cs.tparse("1 DEC 1997 12:28:29.192")
    assert actual_two == -65748690.808
    actual_three = cs.tparse("1997-162::12:18:28.827")
    assert actual_three == -80696491.173


def test_tpictr():
    testString = "10:23 P.M. PDT January 3, 1993"
    pictur = cs.tpictr(testString)
    assert pictur == "AP:MN AMPM PDT Month DD, YYYY ::UTC-7"


def test_trace():
    matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    assert cs.trace(matrix) == 3.0


def test_trcdep():
    cs.reset()
    assert cs.trcdep() == 0
    cs.chkin("test")
    assert cs.trcdep() == 1
    cs.chkin("trcdep")
    assert cs.trcdep() == 2
    cs.chkout("trcdep")
    assert cs.trcdep() == 1
    cs.chkout("test")
    assert cs.trcdep() == 0
    cs.reset()


def test_trcnam():
    cs.reset()
    assert cs.trcdep() == 0
    cs.chkin("test")
    assert cs.trcdep() == 1
    assert cs.trcnam(0) == "test"
    cs.chkin("trcnam")
    assert cs.trcdep() == 2
    assert cs.trcnam(1) == "trcnam"
    cs.chkout("trcnam")
    assert cs.trcdep() == 1
    cs.chkout("test")
    assert cs.trcdep() == 0
    cs.reset()


def test_trgsep():
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(CoreKernels.pck)
    cs.furnsh(CoreKernels.spk)
    cs.furnsh(ExtraKernels.mro2007sub)
    et = cs.str2et("2007-JAN-11 11:21:20.213872 (TDB)")
    frame = ["IAU_MOON", "IAU_EARTH"]
    targ = ["MOON", "EARTH"]
    shape = ["POINT", "SPHERE"]
    pointsep = cs.trgsep(
        et, targ[0], shape[0], frame[0], targ[1], shape[0], frame[1], "SUN", "LT+S"
    )
    sphersep = cs.trgsep(
        et, targ[0], shape[1], frame[0], targ[1], shape[1], frame[1], "SUN", "LT+S"
    )
    assert cs.dpr() * pointsep == pytest.approx(0.15729276)
    assert cs.dpr() * sphersep == pytest.approx(0.15413221)


def test_tsetyr():
    # Expand 2-digit year to full year, typically 4-digit

    def tmp_getyr4(iy2):
        return int(cs.etcal(cs.tparse("3/3/{:02}".format(iy2))).split()[0])

    # Find current lower bound on the 100 year interval of expansion,
    # so it can be restored on exit
    tsetyr_lowerbound = tmp_getyr4(0)
    for iy2_test in range(100):
        tmp_lowerbound = tmp_getyr4(iy2_test)
        if tmp_lowerbound < tsetyr_lowerbound:
            tsetyr_lowerbound = tmp_lowerbound
            break
    # Run first case with a year not ending in 00
    tsetyr_y2 = tsetyr_lowerbound % 100
    tsetyr_y4 = tsetyr_lowerbound + 200 + ((tsetyr_y2 == 0) and 50 or 0)
    cs.tsetyr(tsetyr_y4)
    assert tmp_getyr4(tsetyr_y4 % 100) == tsetyr_y4
    assert tmp_getyr4((tsetyr_y4 - 1) % 100) == (tsetyr_y4 + 99)
    # Run second case with a year ending in 00
    tsetyr_y4 -= tsetyr_y4 % 100
    cs.tsetyr(tsetyr_y4)
    assert tmp_getyr4(tsetyr_y4 % 100) == tsetyr_y4
    assert tmp_getyr4((tsetyr_y4 - 1) % 100) == (tsetyr_y4 + 99)
    # Cleanup:  reset lowerbound to what it was when this routine started
    tsetyr_y4 = tsetyr_lowerbound
    cs.tsetyr(tsetyr_y4)
    assert tmp_getyr4(tsetyr_y4 % 100) == tsetyr_y4
    assert tmp_getyr4((tsetyr_y4 - 1) % 100) == (tsetyr_y4 + 99)
    assert not cs.failed()
    cs.reset()


def test_twopi():
    assert cs.twopi() == np.pi * 2


def test_twovec():
    axdef = [1.0, 0.0, 0.0]
    plndef = [0.0, -1.0, 0.0]
    expected = [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]
    npt.assert_array_almost_equal(cs.twovec(axdef, 1, plndef, 2), expected)


def test_twovxf():
    RAJ2K = 90.3991968556
    DECJ2K = -52.6956610556
    PMRA = 19.93e-3
    PMDEC = 23.24e-3
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(ExtraKernels.mro2007sub)
    cs.furnsh(ExtraKernels.spk430sub)
    # need bsp and mro bsp
    et = cs.str2et("2007 SEP 30 00:00:00 TDB")
    rpmra = cs.convrt(PMRA, "ARCSECONDS", "RADIANS")
    rpmdec = cs.convrt(PMDEC, "ARCSECONDS", "RADIANS")
    ra = RAJ2K * cs.rpd() + rpmra * et / cs.jyear()
    dec = DECJ2K * cs.rpd() + rpmdec * et / cs.jyear()
    pcano = cs.radrec(1.0, ra, dec)
    state, lt = cs.spkezr("MRO", et, "J2000", "NONE", "SSB")
    stcano = cs.stelab(pcano, state[3:])
    stcano = np.array([*stcano, 0.0, 0.0, 0.0])
    stsun, lt = cs.spkezr("SUN", et, "J2000", "CN+S", "MRO")
    xfisc = cs.twovxf(stsun, 3, stcano, 1)
    state, lt = cs.spkezr("EARTH", et, "J2000", "CN+S", "MRO")
    sterth = cs.mxvg(xfisc, state)
    expected = np.array(
        [-16659764.322, 97343706.915, 106745539.738, 2.691, -10.345, -7.877]
    )
    npt.assert_array_almost_equal(np.around(sterth, 3), expected)


def test_tyear():
    assert cs.tyear() == 31556925.9747


def test_ucrss():
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = np.array([6.0, 1.0, 6.0])
    expected = np.cross(vec1, vec2) / np.linalg.norm(np.cross(vec1, vec2))
    outvec = cs.ucrss(vec1, vec2)
    npt.assert_array_almost_equal(expected, outvec)


def test_unitim():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Dec 19 2003")
    converted_et = cs.unitim(et, "ET", "JED")
    npt.assert_almost_equal(converted_et, 2452992.5007428653)


# Test changed: cspyce can't load lists of kernels in this format
def test_unload():
    cs.furnsh(CoreKernels.testMetaKernel)
    # 4 kernels + the meta kernel = 5
    assert cs.ktotal("ALL") == 5
    # Make list of FURNSHed non-meta-kernels
    kernel_list = []
    for iKernel in range(cs.ktotal("ALL")):
        filnam, filtyp, srcnam, handle = cs.kdata(
            iKernel, "ALL")
        if filtyp != "META":
            kernel_list.append(filnam)
    assert len(kernel_list) > 0
    # Unload all kernels
    cs.unload(CoreKernels.testMetaKernel)
    assert cs.ktotal("ALL") == 0
    # Test passing the [list of kernels] as an argument to cs.unload
    for kernel in kernel_list:
        cs.furnsh(kernel)
    assert cs.ktotal("ALL") == len(kernel_list)
    for kernel in kernel_list[1:]:
        cs.unload(kernel)
    assert cs.ktotal("ALL") == 1
    for kernel in kernel_list[:1]:
        cs.unload(kernel)
    assert cs.ktotal("ALL") == 0


def test_unorm():
    v1 = np.array([5.0, 12.0, 0.0])
    expected_vout = np.array([5.0 / 13.0, 12.0 / 13.0, 0.0])
    expected_vmag = 13.0
    vout, vmag = cs.unorm(v1)
    assert vmag == expected_vmag
    assert np.array_equal(expected_vout, vout)


def test_unormg():
    v1 = np.array([5.0, 12.0])
    expected_vout = np.array([5.0 / 13.0, 12.0 / 13.0])
    expected_vmag = 13.0
    vout, vmag = cs.unormg(v1)
    assert vmag == expected_vmag
    assert np.array_equal(expected_vout, vout)


def test_utc2et():
    cs.furnsh(CoreKernels.testMetaKernel)
    utcstr = "December 1, 2004 15:04:11"
    output = cs.utc2et(utcstr)
    assert output == 155185515.1831043
    # icy utc2et example gives 1.5518552e+08 as output


def test_vadd():
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    npt.assert_array_almost_equal(cs.vadd(v1, v2), [5.0, 7.0, 9.0])


def test_vaddg():
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    npt.assert_array_almost_equal(cs.vaddg(v1, v2), [5.0, 7.0, 9.0])


def test_vcrss():
    v1 = np.array([0.0, 1.0, 0.0])
    v2 = np.array([1.0, 0.0, 0.0])
    vout = cs.vcrss(v1, v2)
    expected = np.array([0.0, 0.0, -1.0])
    assert np.array_equal(vout, expected)


def test_vdist():
    v1 = np.array([2.0, 3.0, 0.0])
    v2 = np.array([5.0, 7.0, 12.0])
    assert cs.vdist(v1, v2) == 13.0


def test_vdistg():
    v1 = np.array([2.0, 3.0])
    v2 = np.array([5.0, 7.0])
    assert cs.vdistg(v1, v2) == 5.0


def test_vdot():
    v1 = np.array([1.0, 0.0, -2.0])
    v2 = np.array([2.0, 1.0, -1.0])
    assert cs.vdot(v1, v2) == 4.0


def test_vdotg():
    v1 = np.array([1.0, 0.0])
    v2 = np.array([2.0, 1.0])
    assert cs.vdotg(v1, v2) == 2


def test_vequ():
    v1 = np.ones(3)
    assert np.array_equal(v1, cs.vequ(v1))


def test_vequg():
    v1 = np.ones(4)
    assert np.array_equal(v1, cs.vequg(v1))


def test_vhat():
    v1 = np.array([5.0, 12.0, 0.0])
    expected = np.array([5 / 13.0, 12 / 13.0, 0.0])
    vout = cs.vhat(v1)
    assert np.array_equal(vout, expected)


def test_vhatg():
    v1 = np.array([5.0, 12.0, 0.0, 0.0])
    expected = np.array([5 / 13.0, 12 / 13.0, 0.0, 0.0])
    vout = cs.vhatg(v1)
    assert np.array_equal(vout, expected)


def test_vlcom():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [2.0, 2.0, 2.0]
    outvec = cs.vlcom(1.0, vec1, 1.0, vec2)
    expected = [3.0, 3.0, 3.0]
    npt.assert_array_almost_equal(outvec, expected)


def test_vlcom3():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [2.0, 2.0, 2.0]
    vec3 = [3.0, 3.0, 3.0]
    outvec = cs.vlcom3(1.0, vec1, 1.0, vec2, 1.0, vec3)
    expected = [6.0, 6.0, 6.0]
    npt.assert_array_almost_equal(outvec, expected)


def test_vlcomg():
    vec1 = [1.0, 1.0]
    vec2 = [2.0, 2.0]
    outvec = cs.vlcomg(1.0, vec1, 1.0, vec2)
    expected = [3.0, 3.0]
    npt.assert_array_almost_equal(outvec, expected)


def test_vminug():
    v1 = np.array([1.0, -2.0, 4.0, 0.0])
    expected = np.array([-1.0, 2.0, -4.0, 0.0])
    assert np.array_equal(cs.vminug(v1), expected)


def test_vminus():
    v1 = np.array([1.0, -2.0, 0.0])
    expected = np.array([-1.0, 2.0, 0.0])
    assert np.array_equal(cs.vminus(v1), expected)


def test_vnorm():
    v1 = np.array([1.0e0, 2.0e0, 2.0e0])
    assert cs.vnorm(v1) == 3.0e0


def test_vnormg():
    v1 = np.array([3.0, 3.0, 3.0, 3.0])
    assert cs.vnormg(v1) == 6.0


def test_vpack():
    assert np.array_equal(cs.vpack(1.0, 1.0, 1.0), np.ones(3))


def test_vperp():
    v1 = np.array([6.0, 6.0, 6.0])
    v2 = np.array([2.0, 0.0, 0.0])
    expected = np.array([0.0, 6.0, 6.0])
    assert np.array_equal(cs.vperp(v1, v2), expected)


def test_vprjp():
    vec1 = [-5.0, 7.0, 2.2]
    norm = [0.0, 0.0, 1.0]
    orig = [0.0, 0.0, 0.0]
    plane = cs.nvp2pl(norm, orig)
    proj = cs.vprjp(vec1, plane)
    expected = [-5.0, 7.0, 0.0]
    npt.assert_array_almost_equal(proj, expected)


# Test changed. result is returned as a [Numpy Array, Boolean]
def test_vprjpi():
    norm1 = [0.0, 0.0, 1.0]
    norm2 = [1.0, 0.0, 1.0]
    con1 = 1.2
    con2 = 0.65
    plane1 = cs.nvc2pl(norm1, con1)
    plane2 = cs.nvc2pl(norm2, con2)
    vec = [1.0, 1.0, 0.0]
    result = cs.vprjpi(vec, plane1, plane2)
    expected = [1.0, 1.0, -0.35]
    npt.assert_array_almost_equal(result[0], expected)


def test_vproj():
    v1 = np.array([6.0, 6.0, 6.0])
    v2 = np.array([2.0, 0.0, 0.0])
    expected = np.array([6.0, 0.0, 0.0])
    vout = cs.vproj(v1, v2)
    assert np.array_equal(expected, vout)


def test_vprojg():
    v1 = np.array([6.0, 6.0, 6.0])
    v2 = np.array([2.0, 0.0, 0.0])
    expected = np.array([6.0, 0.0, 0.0])
    vout = cs.vprojg(v1, v2)
    assert np.array_equal(expected, vout)
    v1 = np.array([6.0, 6.0, 6.0, 0.0])
    v2 = np.array([2.0, 0.0, 0.0, 0.0])
    expected = np.array([6.0, 0.0, 0.0, 0.0])
    vout = cs.vprojg(v1, v2)
    assert np.array_equal(expected, vout)


def test_vrel():
    vec1 = [12.3, -4.32, 76.0]
    vec2 = [23.0423, -11.99, -0.10]
    npt.assert_almost_equal(cs.vrel(vec1, vec2), 1.0016370)


def test_vrelg():
    vec1 = [12.3, -4.32, 76.0, 1.87]
    vec2 = [23.0423, -11.99, -0.10, -99.1]
    npt.assert_almost_equal(cs.vrelg(vec1, vec2), 1.2408623)


def test_vrotv():
    v = np.array([1.0, 2.0, 3.0])
    axis = np.array([0.0, 0.0, 1.0])
    theta = cs.halfpi()
    vout = cs.vrotv(v, axis, theta)
    expected = np.array([-2.0, 1.0, 3.0])
    np.testing.assert_almost_equal(vout, expected, decimal=7)


def test_vscl():
    v1 = np.array([1.0, -2.0, 0.0])
    expected = np.array([-1.0, 2.0, 0.0])
    assert np.array_equal(cs.vscl(-1.0, v1), expected)


def test_vsclg():
    v1 = np.array([1.0, 2.0, -3.0, 4.0])
    expected = np.zeros(4)
    assert np.array_equal(cs.vsclg(0.0, v1), expected)


def test_vsep():
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    assert cs.vsep(v1, v2) == np.pi / 2


def test_vsepg():
    v1 = np.array([3.0, 0.0])
    v2 = np.array([-5.0, 0.0])
    assert cs.vsepg(v1, v2) == np.pi


def test_vsub():
    v1 = np.array([1.0, 2.0, 3.0])
    v2 = np.array([4.0, 5.0, 6.0])
    expected = np.array([-3.0, -3.0, -3.0])
    assert np.array_equal(cs.vsub(v1, v2), expected)


def test_vsubg():
    v1 = np.array([1.0, 2.0, 3.0, 4.0])
    v2 = np.array([1.0, 1.0, 1.0, 1.0])
    expected = np.array([0.0, 1.0, 2.0, 3.0])
    assert np.array_equal(cs.vsubg(v1, v2), expected)


def test_vtmv():
    v1 = np.array([2.0, 4.0, 6.0])
    v2 = np.array([1.0, 1.0, 1.0])
    matrix = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    assert cs.vtmv(v1, matrix, v2) == 4.0


def test_vtmvg():
    v1 = np.array([1.0, 2.0, 3.0])
    v2 = np.array([1.0, 2.0])
    matrix = np.array([[2.0, 0.0], [1.0, 2.0], [1.0, 1.0]])
    assert cs.vtmvg(v1, matrix, v2) == 21.0


def test_vupack():
    v1 = np.array([1.0, 2.0, 3.0])
    expected = [1.0, 2.0, 3.0]
    assert cs.vupack(v1) == expected


def test_vzero():
    assert cs.vzero(np.zeros(3))


def test_vzerog():
    assert cs.vzerog(np.zeros(5))


def test_wncomd():
    window1 = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        cs.wninsd(d[0], d[1], window1)
    assert len(window1) / 2 == 3
    window2 = cs.wncomd(2.0, 20.0, window1)
    assert len(window2) / 2 == 2
    assert (window2[0], window2[1]) == (3.0, 7.0)
    assert (window2[2], window2[3]) == (11.0, 20.0)


def test_wncond():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 3
    window = cs.wncond(2.0, 1.0, window)
    assert len(window) / 2 == 2
    assert (window[0], window[1]) == (9.0, 10.0)
    assert (window[2], window[3]) == (25.0, 26.0)


def test_wndifd():
    window1 = cs.SpiceCell(typeno=1, size=8)
    window2 = cs.SpiceCell(typeno=1, size=8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[2.0, 6.0], [8.0, 10.0], [16.0, 18.0]]
    for d in darray1:
        window1 = cs.wninsd(d[0], d[1], window1)
    assert len(window1) / 2 == 3
    for d in darray2:
        window2 = cs.wninsd(d[0], d[1], window2)
    assert len(window2) / 2 == 3
    window3 = cs.wndifd(window1, window2)
    assert len(window3) / 2 == 4
    assert (window3[0],  window3[1]) == (1.0, 2.0)
    assert (window3[2],  window3[3]) == (7.0, 8.0)
    assert (window3[4],  window3[5]) == (10.0, 11.0)
    assert (window3[6],  window3[7]) == (23.0, 27.0)


# Test changed. wnelmd outputs [Boolean, SpiceCell]
def test_wnelmd():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 3
    array = [0.0, 1.0, 9.0, 13.0, 29.0]
    expected = [False, True, True, False, False]
    for a, exp in zip(array, expected):
        assert cs.wnelmd(a, window) == [exp, window]


def test_wnexpd():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 4
    window = cs.wnexpd(2.0, 1.0, window)
    assert len(window) / 2 == 3
    assert (window[0],  window[1]) == (-1.0, 4.0)
    assert (window[2],  window[3]) == (5.0, 12.0)
    assert (window[4],  window[5]) == (21.0, 30.0)


def test_wnextd():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 4
    window = cs.wnextd("L", window)
    assert len(window) / 2 == 4
    assert (window[0], window[1]) == (1.0, 1.0)
    assert (window[2], window[3]) == (7.0, 7.0)
    assert (window[4], window[5]) == (23.0, 23.0)
    assert (window[6], window[7]) == (29.0, 29.0)


def test_wnfild():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 4
    window = cs.wnfild(3.0, window)
    assert len(window) / 2 == 3
    assert (window[0], window[1]) == (1.0, 3.0)
    assert (window[2], window[3]) == (7.0, 11.0)
    assert (window[4], window[5]) == (23.0, 29.0)


def test_wnfltd():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 4
    window = cs.wnfltd(3.0, window)
    assert len(window) / 2 == 2
    assert (window[0], window[1]) == (7.0, 11.0)
    assert (window[2], window[3]) == (23.0, 27.0)


# Test changed. wnincd outputs [Boolean, SpiceCell]
def test_wnincd():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 3
    array = [[1.0, 3.0], [9.0, 10.0], [0.0, 2.0], [13.0, 15.0], [29.0, 30.0]]
    expected = [True, True, False, False, False]
    for a, exp in zip(array, expected):
        assert cs.wnincd(a[0], a[1], window) == [exp, window]


def test_wninsd():
    window = cs.SpiceCell(typeno=1, size=8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    assert len(window) / 2 == 3
    assert [x for x in window] == [1.0, 3.0, 7.0, 11.0, 23.0, 27.0]


def test_wnintd():
    window1 = cs.SpiceCell(typeno=1, size=8)
    window2 = cs.SpiceCell(typeno=1, size=8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[2.0, 6.0], [8.0, 10.0], [16.0, 18.0]]
    for d in darray1:
        window1 = cs.wninsd(d[0], d[1], window1)
    assert len(window1) / 2 == 3
    for d in darray2:
        window2 = cs.wninsd(d[0], d[1], window2)
    assert len(window2) / 2 == 3
    window3 = cs.wnintd(window1, window2)
    assert len(window3) / 2 == 2
    assert (window3[0], window3[1]) == (2.0, 3.0)
    assert (window3[2], window3[3]) == (8.0, 10.0)


def test_wnreld():
    window1 = cs.SpiceCell(typeno=1, size=8)
    window2 = cs.SpiceCell(typeno=1, size=8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[1.0, 2.0], [9.0, 9.0], [24.0, 27.0]]
    for d in darray1:
        window1 = cs.wninsd(d[0], d[1], window1)
    assert len(window1) / 2 == 3
    for d in darray2:
        window2 = cs.wninsd(d[0], d[1], window2)
    assert len(window2) / 2 == 3
    ops = ["=", "<>", "<=", "<", ">=", ">"]
    expected = [False, True, False, False, True, True]
    for op, exp in zip(ops, expected):
        assert cs.wnreld(window1, op, window2) == exp


# Test changed. wnsumd also returns window SpiceCell
def test_wnsumd():
    window = cs.SpiceCell(typeno=1, size=12)
    darray = [
        [1.0, 3.0],
        [7.0, 11.0],
        [18.0, 18.0],
        [23.0, 27.0],
        [30.0, 69.0],
        [72.0, 80.0],
    ]
    for d in darray:
        window = cs.wninsd(d[0], d[1], window)
    window, meas, avg, stddev, shortest, longest = cs.wnsumd(window)
    assert meas == 57.0
    assert avg == 9.5
    assert np.around(stddev, decimals=6) == 13.413302
    assert shortest == 4
    assert longest == 8


def test_wnunid():
    window1 = cs.SpiceCell(typeno=1, size=8)
    window2 = cs.SpiceCell(typeno=1, size=8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[2.0, 6.0], [8.0, 10.0], [16.0, 18.0]]
    for d in darray1:
        window1 = cs.wninsd(d[0], d[1], window1)
    assert len(window1) / 2 == 3
    for d in darray2:
        window2 = cs.wninsd(d[0], d[1], window2)
    assert len(window2) / 2 == 3
    window3 = cs.wnunid(window1, window2)
    assert len(window3) / 2 == 4
    assert (window3[0], window3[1]) == (1.0, 6.0)
    assert (window3[2], window3[3]) == (7.0, 11.0)
    assert (window3[4], window3[5]) == (16.0, 18.0)
    assert (window3[6], window3[7]) == (23.0, 27.0)


def test_xf2eul():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Jan 1, 2009")
    m = cs.sxform("IAU_EARTH", "J2000", et)
    eulang, unique = cs.xf2eul(m, 3, 1, 3)
    assert unique
    expected = [
        1.571803284049681,
        0.0008750002978301174,
        2.9555269829740034,
        3.5458495690569166e-12,
        3.080552365717176e-12,
        -7.292115373266558e-05,
    ]
    npt.assert_array_almost_equal(expected, eulang)


def test_xf2rav():
    e = [1.0, 0.0, 0.0]
    rz = [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    xform = cs.rav2xf(rz, e)
    rz2, e2 = cs.xf2rav(xform)
    npt.assert_array_almost_equal(e, e2)
    npt.assert_array_almost_equal(rz, rz2)


def test_xfmsta():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("July 4, 2003 11:00 AM PST")
    state, lt = cs.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898813661505
    expected_state = [
        7.38222353105354905128e07,
        -2.71279189984722770751e07,
        -1.87413063014898747206e07,
        -6.80851334001380692484e00,
        7.51399612408221173609e00,
        3.00129849265935222391e00,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    state_lat = cs.xfmsta(state, "rectangular", "latitudinal", " ")
    expected_lat_state = [
        8.08509924324866235256e07,
        -3.52158255331780634112e-01,
        -2.33928262716770696272e-01,
        -9.43348972618204761886e00,
        5.98157681117165682860e-08,
        1.03575559016377728336e-08,
    ]
    npt.assert_array_almost_equal(state_lat, expected_lat_state)


def test_xpose():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    npt.assert_array_almost_equal(
        cs.xpose(m1), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    )
    npt.assert_array_almost_equal(
        cs.xpose(np.array(m1)), [[1.0, 0.0, 0.0],
                                 [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    )


def test_xpose6():
    m1 = [
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        [0.0, 7.0, 8.0, 9.0, 10.0, 11.0],
        [0.0, 0.0, 12.0, 13.0, 14.0, 15.0],
        [0.0, 0.0, 0.0, 16.0, 17.0, 18.0],
        [0.0, 0.0, 0.0, 0.0, 19.0, 20.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 21.0],
    ]
    mout_expected = np.array(m1).transpose().tolist()
    npt.assert_array_almost_equal(cs.xpose6(m1), mout_expected)


def test_xposeg():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    npt.assert_array_almost_equal(
        cs.xposeg(m1), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    )
    npt.assert_array_almost_equal(
        cs.xposeg(np.array(m1)),
        [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]],
    )
    m2 = np.random.rand(3, 4)
    npt.assert_array_almost_equal(cs.xposeg(m2), m2.T)


def test_teardown_trcoff():
    cs.reset()
    # Initialize stack trace with two values, and test
    cs.chkin("A")
    cs.chkin("B")
    assert 2 == cs.trcdep()
    assert "B" == cs.trcnam(1)
    assert "A" == cs.trcnam(0)
    # Turn off tracing and test
    cs.trcoff()
    assert 0 == cs.trcdep()
    assert "" == cs.qcktrc()
    # Ensure subsequent checkins are also ignored
    cs.chkin("C")
    assert 0 == cs.trcdep()
    # Cleanup
    cs.reset()
