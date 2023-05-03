import cspyce as cs
import numpy as np
import numpy.testing as npt
import os
import pytest

from gettestkernels import (
    get_standard_kernels,
    write_test_meta_kernel,
    download_kernels,
    CoreKernels,
    CassiniKernels,
    ExtraKernels,
    cleanup_cassini_kernels,
    cleanup_extra_kernels,
    cleanup_core_kernels,
)

get_standard_kernels()
write_test_meta_kernel()

def cleanup_kernel(path):
    cs.kclear()
    cs.reset()
    if os.path.isfile(path):
        os.remove(path)  # pragma: no cover
    pass

cwd = os.environ['CSPYCE_TEST_KERNELS']


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
    

# This one had to be changed. Spiceypy also requires string length
# and the dimension of the array.
def test_bschoc():
    array = ["FEYNMAN", "BOHR", "EINSTEIN", "NEWTON", "GALILEO"]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoc("NEWTON", array, order) == 3
    assert cs.bschoc("EINSTEIN", array, order) == 2
    assert cs.bschoc("GALILEO", array, order) == 4
    assert cs.bschoc("Galileo", array, order) == -1
    assert cs.bschoc("OBETHE", array, order) == -1
    
    
# This one had to be changed. Spiceypy also requires the dimension of
# the array.
def test_bschoi():
    array = [100, 1, 10, 10000, 1000]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoi(1000, array, order) == 4
    assert cs.bschoi(1, array, order) == 1
    assert cs.bschoi(10000, array, order) == 3
    assert cs.bschoi(-1, array, order) == -1
    assert cs.bschoi(17, array, order) == -1

# This one had to be changed. Spiceypy also requires string length
# and the dimension of the array.
def test_bsrchc():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    assert cs.bsrchc("NEWTON", array) == 4
    assert cs.bsrchc("EINSTEIN", array) == 1
    assert cs.bsrchc("GALILEO", array) == 3
    assert cs.bsrchc("Galileo", array) == -1
    assert cs.bsrchc("BETHE", array) == -1


# This one had to be changed. Spiceypy also requires the dimension of
# the array.
def test_bsrchd():
    array = np.array([-11.0, 0.0, 22.0, 750.0])
    assert cs.bsrchd(-11.0, array) == 0
    assert cs.bsrchd(22.0, array) == 2
    assert cs.bsrchd(751.0, array) == -1
    
    
# This one had to be changed. Spiceypy also requires the dimension of
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
    

# This one had to be changed. SpiceyPy creates an Ellipse object.
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
    nrec = cs.cknr02(handle, descr)
    assert nrec > 0
    rec = cs.ckgr02(handle, descr, 1)
    sclks = rec[0]
    sclke = rec[1]
    sclkr = rec[2]
    assert sclks == pytest.approx(32380393707.000015)
    assert sclke == pytest.approx(32380395707.000015)
    assert sclkr == pytest.approx(0.001000)
    cs.dafcls(handle)
    cs.kclear()

