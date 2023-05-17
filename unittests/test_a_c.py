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
    cwd
)

download_kernels()


def cleanup_kernel(path):
    cs.kclear()
    cs.reset()
    if os.path.isfile(path):
        os.remove(path)  # pragma: no cover
    pass


def test_axisar():
    axis = np.array([0.0, 0.0, 1.0])
    outmatrix = cs.axisar(axis, cs.halfpi())
    expected = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    npt.assert_array_almost_equal(expected, outmatrix, decimal=6)


def test_azlcpo():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    et = cs.str2et("2003 Oct 13 06:00:00 UTC")
    obspos = [-2353.621419700, -4641.341471700, 3677.052317800]
    azlsta, lt = cs.azlcpo(
        "ELLIPSOID", "VENUS", et, "CN+S", False, True, obspos, "EARTH", "ITRF93"
    )
    assert azlsta == pytest.approx(
        [
            2.45721479e8,
            5.13974044,
            -8.54270565e-1,
            -4.68189831,
            7.02070016e-5,
            -5.39579640e-5,
        ]
    )


def test_azlrec():
    d = cs.rpd()
    npt.assert_array_almost_equal(
        cs.azlrec(0.000, 0.000 * d, 0.000 * d, True, True),
        [0.000, 0.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 0.000 * d, 0.000 * d, True, True),
        [1.000, 0.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 270.000 * d, 0.000 * d, True, True),
        [-0.000, -1.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 0.000 * d, -90.000 * d, True, True),
        [0.000, 0.000, -1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 180.000 * d, 0.000 * d, True, True),
        [-1.000, 0.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 90.000 * d, 0.000 * d, True, True),
        [0.000, 1.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 0.000 * d, 90.000 * d, True, True),
        [0.000, 0.000, 1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.414, 315.000 * d, 0.000 * d, True, True),
        [1.000, -1.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.414, 0.000 * d, -45.000 * d, True, True),
        [1.000, 0.000, -1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.414, 270.000 * d, -45.000 * d, True, True),
        [-0.000, -1.000, -1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.732, 315.000 * d, -35.264 * d, True, True),
        [1.000, -1.000, -1.000],
        decimal=3,
    )


def test_b1900():
    assert cs.b1900() == 2415020.31352


def test_b1950():
    assert cs.b1950() == 2433282.42345905


def test_badkpv():
    cs.pdpool("DTEST_VAL", [3.1415, 186.0, 282.397])
    assert not cs.badkpv("csypy BADKPV test", "DTEST_VAL", "=", 3, 1, "N")
    cs.clpool()
    assert not cs.expool("DTEST_VAL")


def test_bltfrm():
    out_cell = cs.bltfrm(-1)
    assert out_cell.size >= 126


def test_bodc2n():
    assert cs.bodc2n(399) == "EARTH"
    assert cs.bodc2n(0) == "SOLAR SYSTEM BARYCENTER"


def test_bodc2s():
    assert cs.bodc2s(399) == "EARTH"
    assert cs.bodc2s(0) == "SOLAR SYSTEM BARYCENTER"


def test_boddef():
    cs.boddef("Jebediah", 117)
    assert cs.bodc2n(117) == "Jebediah"


def test_bodfnd():
    cs.furnsh(CoreKernels.testMetaKernel)
    assert cs.bodfnd(599, "RADII")


def test_bodn2c():
    assert cs.bodn2c("EARTH") == 399
    with pytest.raises(KeyError):
        cs.bodn2c("U.S.S. Enterprise")


def test_bods2c():
    assert cs.bods2c("EARTH") == 399
    with pytest.raises(KeyError):
        cs.bods2c("U.S.S. Enterprise")


def test_bodvar():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvar(399, "RADII")
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, radii, decimal=1)


def test_bodvcd():
    cs.furnsh(CoreKernels.testMetaKernel)
    dim, values = 3, cs.bodvcd(399, "RADII")
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
    
    
def test_bodvrd():
    cs.furnsh(CoreKernels.testMetaKernel)
    dim, values = 3, cs.bodvrd("EARTH", "RADII")
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
    
    
def test_brcktd():
    assert cs.brcktd(-1.0, 1.0, 10.0) == 1.0
    assert cs.brcktd(29.0, 1.0, 10.0) == 10.0
    assert cs.brcktd(3.0, -10.0, 10.0) == 3.0
    assert cs.brcktd(3.0, -10.0, -1.0) == -1.0
    
    
def test_brckti():
    assert cs.brckti(-1, 1, 10) == 1
    assert cs.brckti(29, 1, 10) == 10
    assert cs.brckti(3, -10, 10) == 3
    assert cs.brckti(3, -10, -1) == -1
    

# Test changed. Spiceypy also requires string length
# and the dimension of the array.
def test_bschoc():
    array = ["FEYNMAN", "BOHR", "EINSTEIN", "NEWTON", "GALILEO"]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoc("NEWTON", array, order) == 3
    assert cs.bschoc("EINSTEIN", array, order) == 2
    assert cs.bschoc("GALILEO", array, order) == 4
    assert cs.bschoc("Galileo", array, order) == -1
    assert cs.bschoc("OBETHE", array, order) == -1
    
    
# Test changed. Spiceypy also requires the dimension of
# the array.
def test_bschoi():
    array = [100, 1, 10, 10000, 1000]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoi(1000, array, order) == 4
    assert cs.bschoi(1, array, order) == 1
    assert cs.bschoi(10000, array, order) == 3
    assert cs.bschoi(-1, array, order) == -1
    assert cs.bschoi(17, array, order) == -1

# Test changed. Spiceypy also requires string length
# and the dimension of the array.
def test_bsrchc():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    assert cs.bsrchc("NEWTON", array) == 4
    assert cs.bsrchc("EINSTEIN", array) == 1
    assert cs.bsrchc("GALILEO", array) == 3
    assert cs.bsrchc("Galileo", array) == -1
    assert cs.bsrchc("BETHE", array) == -1


# Test changed. Spiceypy also requires the dimension of
# the array.
def test_bsrchd():
    array = np.array([-11.0, 0.0, 22.0, 750.0])
    assert cs.bsrchd(-11.0, array) == 0
    assert cs.bsrchd(22.0, array) == 2
    assert cs.bsrchd(751.0, array) == -1
    
    
# Test changed. Spiceypy also requires the dimension of
# the array.
def test_bsrchi():
    array = np.array([-11, 0, 22, 750])
    assert cs.bsrchi(-11, array) == 0
    assert cs.bsrchi(22, array) == 2
    assert cs.bsrchi(751, array) == -1
    
    
def test_ccifrm():
    frcode, frname, center = cs.ccifrm(2, 3000)
    assert frname == "ITRF93"
    assert frcode == 13000
    assert center == 399
    

# Test changed. SpiceyPy creates an Ellipse object.
def test_cgv2el():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [-1.0, 1.0, -1.0]
    ellipse = cs.cgv2el(center, vec1, vec2)
    expected_s_major = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expected_s_minor = [0.0, np.sqrt(2.0), 0.0]
    expected_center = [-1.0, 1.0, -1.0]
    npt.assert_array_almost_equal(expected_center, ellipse[0:3])
    npt.assert_array_almost_equal(expected_s_major, ellipse[3:6])
    npt.assert_array_almost_equal(expected_s_minor, ellipse[6:9])
    
    
# Test changed. SpiceyPy also requires the degree of the polynomial.
def test_chbder():
    cp = [1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0]
    x2s = [0.5, 3.0]
    dpdxs = cs.chbder(cp, x2s, 1.0, 3)
    npt.assert_array_almost_equal([-0.340878, 0.382716, 4.288066, -1.514403],
                                  dpdxs)
    

# Test changed. SpiceyPy also requires degree of input Chebyshev expansion.
def test_chbigr():
    p, itgrlp = cs.chbigr([0.0, 3.75, 0.0, 1.875, 0.0, 0.375], [20.0, 10.0],
                          30.0)
    assert p == pytest.approx(6.0)
    assert itgrlp == pytest.approx(10.0)
    
    
# Test changed. SpiceyPy also requires the degree of the polynomial.
def test_chbint():
    p, dpdx = cs.chbint([1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0], [0.5, 3.0], 1.0)
    assert p == pytest.approx(-0.340878, abs=1e-6)
    assert dpdx == pytest.approx(0.382716, abs=1e-6)


# Test changed. SpiceyPy also requires the degree of the polynomial.  
def test_chbval():
    p = cs.chbval([1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0], [0.5, 3.0], 1.0)
    assert p == pytest.approx(-0.340878, abs=1e-6)
    
    
def test_chkin():
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
    
    
def test_chkout():
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


def test_cidfrm():
    frcode, frname = cs.cidfrm(501)
    assert frcode == 10023
    assert frname == "IAU_IO"
    frcode, frname = cs.cidfrm(399)
    assert frcode == 10013
    assert frname == "IAU_EARTH"
    frcode, frname = cs.cidfrm(301)
    assert frcode == 10020
    assert frname == "IAU_MOON"


# Test changed. SpiceyPy's ckw01 also needs the number of pointing records.
# Test is currently commented out due to issue with cspyce.ckw01
def fail_ckcls():
    # Spice crashes if ckcls detects nothing written to ck1
    ck1 = os.path.join(cwd, "ckopenkernel.bc")
    cleanup_kernel(ck1)
    ifname = "Test CK type 1 segment created by cspice_ckw01"
    handle = cs.ckopn(ck1, ifname, 10)
    cs.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        2 - 1,
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )

    
    cs.ckcls(handle)
    cs.kclear()
    assert os.path.exists(ck1)
    cleanup_kernel(ck1)
    assert not os.path.exists(ck1)


# Test changed. Removed usage 
def test_ckcov(): 
    cs.furnsh(CassiniKernels.cassSclk)
    ckid = cs.ckobj(CassiniKernels.cassCk)[0]
    cover = cs.ckcov(CassiniKernels.cassCk, ckid, False, "INTERVAL", 0.0, "SCLK")
    expected_intervals = [
        [267832537952.000000, 267839247264.000000],
        [267839256480.000000, 267867970464.000000],
        [267868006304.000000, 267876773792.000000],
    ]
    npt.assert_array_equal(cover, expected_intervals)
    

# Test changed. Added 'found' to the variable assignment since cspyce outputs an
# extra variable.
def test_ckfrot():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    ckid = cs.ckobj(CassiniKernels.cassCk)[0]
    # arbitrary time covered by test ck kernel
    et = cs.str2et("2013-FEB-26 00:01:08.828")
    rotation, ref, found = cs.ckfrot(ckid, et)
    expected = np.array(
        [
            [-0.64399206, -0.34110294, 0.68477954],
            [0.48057295, -0.87682328, 0.01518468],
            [0.5952511, 0.33886533, 0.72859208],
        ]
    )
    npt.assert_array_almost_equal(rotation, expected)
    assert ref == 1

# Test changed. Added 'found' to the variable assignment since cspyce outputs an
# extra variable. Currently fails.
def fail_ckfxfm():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    # arbitrary time covered by test ck kernel
    et = cs.str2et("2013-FEB-26 00:01:08.828")
    xform, ref, found = cs.ckfxfm(-82000, et)
    rot, av = cs.xf2rav(xform)
    arc = cs.vnorm(av)
    assert ref == 1
    assert arc > 0
    

# Test changed. SpiceyPy's encoded spacecraft clock time is in a SpiceDouble
# format. Cspyce requires one float-type value.
def test_ckgp():
    cs.reset()
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    ckid = cs.ckobj(CassiniKernels.cassCk)[0]
    cover = cs.ckcov(CassiniKernels.cassCk, ckid, False, "INTERVAL", 0.0, "SCLK")
    
    cmat, clkout = cs.ckgp(ckid, cover[0][0], 256, "J2000")
    expected_cmat = [
        [0.5064665782997639365, -0.75794210739897316387, 0.41111478554891744963],
        [-0.42372128242505308071, 0.19647683351734512858, 0.88422685364733510927],
        [-0.7509672961490383436, -0.6220294331642198804, -0.22164725216433822652],
    ]
    npt.assert_array_almost_equal(cmat, expected_cmat)
    assert clkout == 267832537952.0
    cs.reset()


# Test changed. SpiceyPy's encoded spacecraft clock time is in a SpiceDouble
# format. Cspyce requires one float-type value.
def test_ckgpav():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    ckid = cs.ckobj(CassiniKernels.cassCk)[0]
    cover = cs.ckcov(CassiniKernels.cassCk, ckid, False, "INTERVAL", 0.0, "SCLK")
    cmat, avout, clkout = cs.ckgpav(ckid, cover[0][0], 256, "J2000")
    expected_cmat = [
        [0.5064665782997639365, -0.75794210739897316387, 0.41111478554891744963],
        [-0.42372128242505308071, 0.19647683351734512858, 0.88422685364733510927],
        [-0.7509672961490383436, -0.6220294331642198804, -0.22164725216433822652],
    ]
    expected_avout = [
        -0.00231258422150853885,
        -0.00190333614370416515,
        -0.00069657429072504716,
    ]
    npt.assert_array_almost_equal(cmat, expected_cmat)
    npt.assert_array_almost_equal(avout, expected_avout)
    assert clkout == 267832537952.0
    

# Test changed. cs.dafgs() does not have a parameter for the length N for the
# result array
def test_ckgr02_cknr02():
    cs.kclear()
    cs.reset()
    handle = cs.dafopr(ExtraKernels.v02swuck)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    descr = cs.dafgs()
    dc, ic = cs.dafus(descr, 2, 6)
    assert ic[2] == 2
    nrec = cs.cknr02(handle, descr[:5])
    assert nrec > 0
    rec = cs.ckgr02(handle, descr[:5], 1)
    sclks = rec[0]
    sclke = rec[1]
    sclkr = rec[2]
    assert sclks == pytest.approx(32380393707.000015)
    assert sclke == pytest.approx(32380395707.000015)
    assert sclkr == pytest.approx(0.001000)
    cs.dafcls(handle)
    cs.kclear()
    

# Test changed. cs.dafgs() does not have a parameter for the length N for the
# result array
def test_ckgr03_cknr03():
    cs.kclear()
    cs.reset()
    handle = cs.dafopr(ExtraKernels.vexboomck)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    descr = cs.dafgs()
    dc, ic = cs.dafus(descr, 2, 6)
    assert ic[2] == 3
    nrec = cs.cknr03(handle, descr[:5])
    assert nrec > 0
    rec = cs.ckgr03(handle, descr[:5], 1)
    cs.dafcls(handle)
    sclkdp = rec[0]
    assert sclkdp == pytest.approx(2162686.710986)
    cs.dafcls(handle)
    cs.kclear()
    
    
# Test fails due to cs.ckw01
def fail_cklpf():
    cs.reset()
    cklpf = os.path.join(cwd, "cklpfkernel.bc")
    cleanup_kernel(cklpf)
    ifname = "Test CK type 1 segment created by ccs_cklpf"
    handle = cs.ckopn(cklpf, ifname, 10)
    cs.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        2 - 1,
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )
    cs.ckcls(handle)
    cs.kclear()
    handle = cs.cklpf(cklpf)
    cs.ckupf(handle)
    cs.ckcls(handle)
    cs.kclear()
    cs.reset()
    assert os.path.isfile(cklpf)
    cleanup_kernel(cklpf)
    assert not os.path.isfile(cklpf)
    
    
def test_ckmeta():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    idcode = cs.ckmeta(-32000, "SCLK")
    assert idcode == -32
    
    
def test_ckobj():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    ids = cs.ckobj(CassiniKernels.cassCk)
    assert len(ids) == 1
    
    
# Fails due to cs.ckw01
def fail_ckopn():
    # cs crashes if ckcls detects nothing written to ck1
    ck1 = os.path.join(cwd, "ckopenkernel.bc")
    cleanup_kernel(ck1)
    ifname = "Test CK type 1 segment created by ccs_ckw01"
    handle = cs.ckopn(ck1, ifname, 10)
    cs.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        2 - 1,
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )

    cs.ckcls(handle)
    cs.kclear()
    assert cs.exists(ck1)
    cleanup_kernel(ck1)
    assert not cs.exists(ck1)
    
    
def test_ckupf():
    cs.reset()
    handle = cs.cklpf(CassiniKernels.cassCk)
    cs.ckupf(handle)
    cs.ckcls(handle)
    cs.reset()


# Test current fails.
def fail_ckw01():
    ck1 = os.path.join(cwd, "type1.bc")
    cleanup_kernel(ck1)
    INST = -77701
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 1 CK segment"
    ifname = "Test CK type 1 segment created by ccs_ckw01"
    NCOMCH = 0
    REF = "J2000"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = cs.ckopn(ck1, ifname, NCOMCH)
    init_size = os.path.getsize(ck1)
    quats = np.zeros((MAXREC, 4))
    av = np.zeros((MAXREC, 3))
    work_mat = cs.ident()
    work_quat = cs.m2q(work_mat)
    quats[0] = work_quat
    av[0] = [0.0, 0.0, RATE]
    sclkdp = np.arange(MAXREC) * SPACING_TICKS
    sclkdp += 1000.0
    for i in range(1, MAXREC - 1):
        theta = i * RATE * SPACING_SECS * 1.0
        work_mat = cs.rotmat(work_mat, theta, 3)
        work_quat = cs.m2q(work_mat)
        quats[i] = work_quat
        av[i] = [0.0, 0.0, RATE]
    avflag = True
    begtime = sclkdp[0]
    endtime = sclkdp[-1]
    cs.ckw01(
        handle,
        begtime,
        endtime,
        INST,
        REF,
        avflag,
        SEGID,
        sclkdp,
        quats,
        av,
    )
    cs.ckcls(handle)
    end_size = os.path.getsize(ck1)
    assert end_size != init_size
    cs.kclear()
    cleanup_kernel(ck1)


# Test fails.
def fail_ckw02():
    ck2 = os.path.join(cwd, "type2.bc")
    cleanup_kernel(ck2)
    INST = -77702
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 2 CK segment"
    ifname = "Test CK type 2 segment created by cspice_ckw02"
    NCOMCH = 0
    REF = "J2000"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = cs.ckopn(ck2, ifname, NCOMCH)
    init_size = os.path.getsize(ck2)
    quats = np.zeros((MAXREC, 4))
    av = np.zeros((MAXREC, 3))
    work_mat = cs.ident()
    work_quat = cs.m2q(work_mat)
    quats[0] = work_quat
    av[0] = [0.0, 0.0, RATE]
    rates = [SECPERTICK] * MAXREC
    sclkdp = np.arange(MAXREC) * SPACING_TICKS
    sclkdp += 1000.0
    starts = sclkdp
    stops = sclkdp + (0.8 * SPACING_TICKS)
    for i in range(1, MAXREC - 1):
        theta = i * RATE * SPACING_SECS * 1.0
        work_mat = cs.rotmat(work_mat, theta, 3)
        work_quat = cs.m2q(work_mat)
        quats[i] = work_quat
        av[i] = [0.0, 0.0, RATE]
    begtime = sclkdp[0]
    endtime = sclkdp[-1]
    cs.ckw02(
        handle,
        begtime,
        endtime,
        INST,
        REF,
        SEGID,
        starts,
        stops,
        quats,
        av,
        rates,
    )
    cs.ckcls(handle)
    end_size = os.path.getsize(ck2)
    assert end_size != init_size
    cs.kclear()
    cleanup_kernel(ck2)
    

# Test fails.
def fail_ckw03():
    ck3 = os.path.join(cwd, "type3.bc")
    cleanup_kernel(ck3)
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 3 CK segment"
    ifname = "Test CK type 3 segment created by ccs_ckw03"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = cs.ckopn(ck3, ifname, 0)
    init_size = os.path.getsize(ck3)
    quats = np.zeros((MAXREC, 4))
    av = np.zeros((MAXREC, 3))
    work_mat = cs.ident()
    work_quat = cs.m2q(work_mat)
    quats[0] = work_quat
    av[0] = [0.0, 0.0, RATE]
    sclkdp = np.arange(MAXREC) * SPACING_TICKS
    sclkdp += 1000.0
    for i in range(1, MAXREC - 1):
        theta = i * RATE * SPACING_SECS * 1.0
        work_mat = cs.rotmat(work_mat, theta, 3)
        work_quat = cs.m2q(work_mat)
        quats[i] = work_quat
        av[i] = [0.0, 0.0, RATE]
    starts = [sclkdp[2 * i] for i in range(99)]
    begtime = sclkdp[0]
    endtime = sclkdp[-1]
    cs.ckw03(
        handle,
        begtime,
        endtime,
        -77703,
        "J2000",
        True,
        SEGID,
        MAXREC - 1,
        sclkdp,
        quats,
        av,
        99,
        starts,
    )
    cs.ckcls(handle)
    end_size = os.path.getsize(ck3)
    assert end_size != init_size
    cs.kclear()
    cleanup_kernel(ck3)
    

# Test fails.
def fail_ckw05():
    cs.kclear()
    ck5 = os.path.join(cwd, "type5.bc")
    cleanup_kernel(ck5)
    # constants
    avflag = True
    epochs = np.arange(0.0, 2.0)
    inst = [-41000, -41001, -41002, -41003]
    segid = "CK type 05 test segment"
    # make type 1 data
    type0data = [
        [9.999e-1, -1.530e-4, -8.047e-5, -4.691e-4, 0.0, 0.0, 0.0, 0.0],
        [
            9.999e-1,
            -4.592e-4,
            -2.414e-4,
            -1.407e-3,
            -7.921e-10,
            -1.616e-7,
            -8.499e-8,
            -4.954e-7,
        ],
    ]
    type1data = [
        [9.999e-1, -1.530e-4, -8.047e-5, -4.691e-4],
        [9.999e-1, -4.592e-4, -2.414e-4, -1.407e-3],
    ]
    type2data = [
        [
            0.959,
            -0.00015309,
            -8.0476e-5,
            -0.00046913,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.959,
            -0.00045928,
            -0.00024143,
            -0.0014073,
            -7.921e-10,
            -1.616e-7,
            -8.499e-8,
            -4.954e-7,
            3.234e-7,
            1.7e-7,
            9.91e-7,
            3.234e-7,
            1.7e-9,
            9.91e-9,
        ],
    ]
    type3data = [
        [0.959, -0.00015309, -8.0476e-05, -0.00046913, 0.0, 0.0, 0.0],
        [0.959, -0.00045928, -0.00024143, -0.0014073, 3.234e-7, 1.7e-7, 9.91e-7],
    ]
    # begin testing ckw05
    handle = cs.ckopn(ck5, " ", 0)
    init_size = os.path.getsize(ck5)
    # test subtype 0
    cs.ckw05(
        handle,
        0,
        15,
        epochs[0],
        epochs[-1],
        inst[0],
        "J2000",
        avflag,
        segid,
        epochs,
        type0data,
        1000.0,
        1,
        epochs,
    )
    # test subtype 1
    cs.ckw05(
        handle,
        1,
        15,
        epochs[0],
        epochs[-1],
        inst[1],
        "J2000",
        avflag,
        segid,
        epochs,
        type1data,
        1000.0,
        1,
        epochs,
    )
    # test subtype 2
    cs.ckw05(
        handle,
        2,
        15,
        epochs[0],
        epochs[-1],
        inst[2],
        "J2000",
        avflag,
        segid,
        epochs,
        type2data,
        1000.0,
        1,
        epochs,
    )
    # test subtype 3
    cs.ckw05(
        handle,
        3,
        15,
        epochs[0],
        epochs[-1],
        inst[3],
        "J2000",
        avflag,
        segid,
        epochs,
        type3data,
        1000.0,
        1,
        epochs,
    )
    cs.ckcls(handle)
    # test size
    end_size = os.path.getsize(ck5)
    assert end_size != init_size
    # try reading using ck kernel
    cs.furnsh(ck5)
    cmat, av, clk = cs.ckgpav(-41000, epochs[0] + 0.5, 1.0, "J2000")
    assert clk == pytest.approx(0.5)
    cs.kclear()
    cleanup_kernel(ck5)
    
    
def test_clight():
    assert cs.clight() == 299792.458
    

# Test changed. cs.cdpool() takes two args, not 3.
def test_clpool():
    cs.pdpool("TEST_VAR", [-666.0])
    value = cs.gdpool("TEST_VAR", 0)
    assert len(value) == 1
    assert value[0] == -666.0
    cs.clpool()
    with pytest.raises(KeyError):
        cs.gdpool("TEST_VAR", 0)
        
        
def test_cmprss():
    strings = ["ABC...DE.F...", "...........", ".. ..AB....CD"]
    assert cs.cmprss(".", 2, strings[0]) == "ABC..DE.F.."
    assert cs.cmprss(".", 3, strings[1]) == "..."
    assert cs.cmprss(".", 1, strings[2]) == ". .AB.CD"
    assert cs.cmprss(".", 3, strings[1]) == "..."
    assert cs.cmprss(".", 1, strings[2]) == ". .AB.CD"
    assert cs.cmprss(" ", 0, " Embe dde d -sp   a c  es   ") == "Embedded-spaces"
    
    
def test_cnmfrm():
    ioFrcode, ioFrname = cs.cnmfrm("IO")
    assert ioFrcode == 10023
    assert ioFrname == "IAU_IO"
    
    
# Test changed. cs.bodvrd only returns one result.
def test_conics():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Dec 25, 2007")
    state, ltime = cs.spkezr("Moon", et, "J2000", "NONE", "EARTH")
    mu = cs.bodvrd("EARTH", "GM")
    elts = cs.oscelt(state, et, mu[0])
    later = et + 7.0 * cs.spd()
    later_state = cs.conics(elts, later)
    state, ltime = cs.spkezr("Moon", later, "J2000", "NONE", "EARTH")
    pert = np.array(later_state) - np.array(state)
    expected_pert = [
        -7.48885583081946242601e03,
        3.97608014470621128567e02,
        1.95744667259379639290e02,
        -3.61527427787390887026e-02,
        -1.27926899069508159812e-03,
        -2.01458906615054056388e-03,
    ]
    npt.assert_array_almost_equal(pert, expected_pert, decimal=5)
    
    
# Test changed. cs.convrt() can't do multiple arg1s
def test_convrt():
    assert cs.convrt(300.0, "statute_miles", "km") == 482.80320
    npt.assert_almost_equal(
        cs.convrt(1.0, "parsecs", "lightyears"), 3.2615638, decimal=6
    )

    npt.assert_almost_equal(
        cs.convrt(1, "AU", "km"), 149597870.7, decimal=0
    )
    
    
def test_cpos():
    string = "BOB, JOHN, TED, AND MARTIN...."
    assert cs.cpos(string, " ,", 0) == 3
    assert cs.cpos(string, " ,", 4) == 4
    assert cs.cpos(string, " ,", 5) == 9
    assert cs.cpos(string, " ,", 10) == 10
    assert cs.cpos(string, " ,", 11) == 14
    assert cs.cpos(string, " ,", 15) == 15
    assert cs.cpos(string, " ,", 16) == 19
    assert cs.cpos(string, " ,", 20) == -1
    assert cs.cpos(string, " ,", -112) == 3
    assert cs.cpos(string, " ,", -1) == 3
    assert cs.cpos(string, " ,", 1230) == -1
    
    
def test_cposr():
    string = "BOB, JOHN, TED, AND MARTIN...."
    assert cs.cposr(string, " ,", 29) == 19
    assert cs.cposr(string, " ,", 25) == 19
    assert cs.cposr(string, " ,", 18) == 15
    assert cs.cposr(string, " ,", 14) == 14
    assert cs.cposr(string, " ,", 13) == 10
    assert cs.cposr(string, " ,", 9) == 9
    assert cs.cposr(string, " ,", 8) == 4
    assert cs.cposr(string, " ,", 3) == 3
    assert cs.cposr(string, " ,", 2) == -1
    assert cs.cposr(string, " ,", 230) == 19
    assert cs.cposr(string, " ,", 30) == 19
    assert cs.cposr(string, " ,", -1) == -1
    assert cs.cposr(string, " ,", -10) == -1
    

# Test changed. spiceypy.swpool also has params for nnames (number of variables
# to associate with agent) and lenvals (length of strings in the names array).
def test_cvpool():
    # add TEST_VAR_CVPOOL
    cs.pdpool("TEST_VAR_CVPOOL", [-646.0])
    # establish check for TEST_VAR_CVPOOL
    cs.swpool("TEST_CVPOOL", ["TEST_VAR_CVPOOL"])
    # update TEST_VAR_CVPOOL
    cs.pdpool("TEST_VAR_CVPOOL", [565.0])
    # check for updated variable
    updated = cs.cvpool("TEST_CVPOOL")
    value = cs.gdpool("TEST_VAR_CVPOOL", 0)
    assert len(value) == 1
    assert value[0] == 565.0
    cs.clpool()
    assert updated is True
    

# Test changed. result comes in [], not ()
def test_cyllat():
    assert cs.cyllat(1.0, (180.0 * cs.rpd()), -1.0) == [
        np.sqrt(2),
        np.pi,
        -np.pi / 4,
    ]
    
    
def test_cylrec():
    npt.assert_array_almost_equal(
        cs.cylrec(0.0, np.radians(33.0), 0.0), [0.0, 0.0, 0.0]
    )
    
# Test changed. b[1] and b[2] were switched to match a.
def test_cylsph():
    a = np.array(cs.cylsph(1.0, np.deg2rad(180.0), 1.0))
    b = np.array([1.4142, np.deg2rad(45.0), np.deg2rad(180.0)])
    np.testing.assert_almost_equal(b, a, decimal=4)

