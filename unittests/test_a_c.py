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
    checking_pathlike_filename_variants,
    TEST_FILE_DIR,
    KERNEL_DIR
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


def test_axisar():
    axis = np.array([0.0, 0.0, 1.0])
    outmatrix = cs.axisar(axis, cs.halfpi())
    expected = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    npt.assert_array_almost_equal(expected, outmatrix, decimal=6)


def test_axisar_2():
    pi = np.pi
    npt.assert_almost_equal(cs.axisar([0, 0, 1], 0.), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    npt.assert_almost_equal(cs.axisar([0, 0, 1], pi), [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])

    npt.assert_almost_equal(cs.axisar_vector([0, 0, 1], [0., pi]), [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                                                    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]]])


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
    
    
def test_bodc2n_bodn2c_bodc2s_bods2c():
    INTMAX = cs.intmax()
    #### bodc2n, bodn2c, bodc2s, bods2c
    cs.boddef('BIG!', -INTMAX)
    
    assert cs.bodc2n.flag(699) == ['SATURN', True]
    assert cs.bodc2n_error(699) == 'SATURN'
    assert cs.bodc2n.flag(INTMAX)[1] == False
    with pytest.raises(Exception):
        cs.bodc2n_error(INTMAX)
    
    assert cs.bodn2c.flag('SATuRN ') == [699, True]
    assert cs.bodn2c_error('SATURN') == 699
    assert cs.bodn2c.flag('foobar')[1] == False
    with pytest.raises(Exception):
        cs.bodn2c_error('foobar')
    
    assert cs.bodc2s(699) == 'SATURN'
    assert cs.bodc2s(INTMAX) == str(INTMAX)
    
    assert cs.bods2c.flag('SATuRN ') == [699, True]
    assert cs.bods2c_error('SATURN') == 699
    assert cs.bods2c.flag('foobar')[1] == False
    with pytest.raises(Exception):
        cs.bods2c_error('foobar')
    assert cs.bods2c_error('  699 ') == 699
    assert cs.bods2c_error(str(INTMAX)) == INTMAX
    
    npt.assert_almost_equal(cs.bltfrm(1).as_array(), range(1, 22), 0)
    
    #  self.assertAllEqual(kplfrm(1), range(1,22), 0)
    cs.boddef('BIG!', INTMAX)
    
    assert cs.bodc2n.flag(INTMAX) == ['BIG!', True]
    assert cs.bodc2n_error(INTMAX) == 'BIG!'
    
    assert cs.bodn2c.flag('BiG! ') == [INTMAX, True]
    assert cs.bodn2c_error('BIG!') == INTMAX
    
    assert cs.bodc2s(INTMAX) == 'BIG!'
    assert cs.bods2c.flag('BiG! ') == [INTMAX, True]
    assert cs.bods2c_error('BIG!') == INTMAX


def test_bodc2s():
    assert cs.bodc2s(399) == "EARTH"
    assert cs.bodc2s(0) == "SOLAR SYSTEM BARYCENTER"


def test_boddef():
    cs.boddef("Jebediah", 117)
    assert cs.bodc2n(117) == "Jebediah"


def test_bodfnd():
    cs.furnsh(CoreKernels.testMetaKernel)
    assert cs.bodfnd(599, "RADII")
    
    
def test_bodfnd_2():
    cs.furnsh(CoreKernels.testMetaKernel)
    INTMIN = cs.intmin()
    assert cs.bodfnd(699, 'RADII')
    assert not cs.bodfnd(699, 'RADIIxxx')
    assert not cs.bodfnd(INTMIN, 'RADII')


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
    
    
def test_bodvar_2():
    cs.furnsh(CoreKernels.testMetaKernel)
    assert cs.bodvar(699, 'RADII')[0] == 60268.
    assert cs.bodvar(699, 'RADII')[1] == 60268.
    assert cs.bodvar(699, 'RADII')[2] == 54364.
    with pytest.raises(KeyError):
        cs.bodvar(699, 'RADIIxxx')


def test_bodvcd():
    cs.furnsh(CoreKernels.testMetaKernel)
    dim, values = 3, cs.bodvcd(399, "RADII")
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
    
    
def test_bodvcd_2():
    cs.furnsh(CoreKernels.testMetaKernel)
    assert cs.bodvcd(699, 'RADII')[0] == 60268.
    assert cs.bodvcd(699, 'RADII')[1] == 60268.
    assert cs.bodvcd(699, 'RADII')[2] == 54364.
    with pytest.raises(KeyError):
        cs.bodvcd(699, 'RADIIxxx')


def test_bodvrd():
    cs.furnsh(CoreKernels.testMetaKernel)
    dim, values = 3, cs.bodvrd("EARTH", "RADII")
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
    
    
def test_bodvrd_2():
    cs.furnsh(CoreKernels.testMetaKernel)
    assert cs.bodvrd('SATURN', 'RADII')[0] == 60268.
    assert cs.bodvrd('SATURN', 'RADII')[1] == 60268.
    assert cs.bodvrd('SATURN', 'RADII')[2] == 54364.
    with pytest.raises(KeyError):
        cs.bodvrd('SATURN', 'RADIIxxx')


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


def test_bschoc():
    array = ["FEYNMAN", "BOHR", "EINSTEIN", "NEWTON", "GALILEO"]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoc("NEWTON", array, order) == 3
    assert cs.bschoc("EINSTEIN", array, order) == 2
    assert cs.bschoc("GALILEO", array, order) == 4
    assert cs.bschoc("Galileo", array, order) == -1
    assert cs.bschoc("OBETHE", array, order) == -1


def test_bschoi():
    array = [100, 1, 10, 10000, 1000]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoi(1000, array, order) == 4
    assert cs.bschoi(1, array, order) == 1
    assert cs.bschoi(10000, array, order) == 3
    assert cs.bschoi(-1, array, order) == -1
    assert cs.bschoi(17, array, order) == -1


def test_bsrchc():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    assert cs.bsrchc("NEWTON", array) == 4
    assert cs.bsrchc("EINSTEIN", array) == 1
    assert cs.bsrchc("GALILEO", array) == 3
    assert cs.bsrchc("Galileo", array) == -1
    assert cs.bsrchc("BETHE", array) == -1


def test_bsrchd():
    array = np.array([-11.0, 0.0, 22.0, 750.0])
    assert cs.bsrchd(-11.0, array) == 0
    assert cs.bsrchd(22.0, array) == 2
    assert cs.bsrchd(751.0, array) == -1


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
    
    
def test_ccifrm_2():
    INTMIN = cs.intmin()
    assert cs.cidfrm.flag(INTMIN)[2] == False
    assert cs.ccifrm.flag(2, 699) == [10016, 'IAU_SATURN', 699, True]
    assert cs.ccifrm_error(2, 699) == [10016, 'IAU_SATURN', 699]
    assert cs.ccifrm.flag(2, INTMIN)[3] == False
    with pytest.raises(ValueError):
        cs.ccifrm_error(INTMIN, INTMIN)


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


def test_chbder():
    cp = [1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0]
    x2s = [0.5, 3.0]
    dpdxs = cs.chbder(cp, x2s, 1.0, 3)
    npt.assert_array_almost_equal([-0.340878, 0.382716, 4.288066, -1.514403],
                                  dpdxs)


def test_chbigr():
    p, itgrlp = cs.chbigr([0.0, 3.75, 0.0, 1.875, 0.0, 0.375], [20.0, 10.0],
                          30.0)
    assert p == pytest.approx(6.0)
    assert itgrlp == pytest.approx(10.0)


def test_chbint():
    p, dpdx = cs.chbint([1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0], [0.5, 3.0], 1.0)
    assert p == pytest.approx(-0.340878, abs=1e-6)
    assert dpdx == pytest.approx(0.382716, abs=1e-6)


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


def test_cidfrm_2():
    INTMIN = cs.intmin()
    assert cs.cidfrm.flag(699) == [10016, 'IAU_SATURN', True]
    assert cs.cidfrm_error(699) == [10016, 'IAU_SATURN']
    assert cs.cidfrm.flag(INTMIN)[2] == False
    with pytest.raises(KeyError):
        cs.cidfrm_error(INTMIN)


def test_ckcls():
    # Spice crashes if ckcls detects nothing written to ck1
    ck1 = os.path.join(TEST_FILE_DIR, "ckopenkernel.bc")
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
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )
    cs.ckcls(handle)
    cs.kclear()
    assert os.path.exists(ck1)
    cleanup_kernel(ck1)
    assert not os.path.exists(ck1)


@checking_pathlike_filename_variants("path_type_variant")
def test_ckcov(path_type_variant):
    cs.furnsh(CassiniKernels.cassSclk)
    ckid = cs.ckobj(path_type_variant(CassiniKernels.cassCk))[0]
    cover = cs.ckcov(path_type_variant(CassiniKernels.cassCk),
                     ckid, False, "INTERVAL", 0.0, "SCLK")
    expected_intervals = [
        [267832537952.000000, 267839247264.000000],
        [267839256480.000000, 267867970464.000000],
        [267868006304.000000, 267876773792.000000],
    ]
    npt.assert_array_equal(cover.as_intervals(), expected_intervals)
    
    
def test_ckcov_2():
    cassCk = os.path.join(KERNEL_DIR,'13056_13057ra.bc' )
    values = cs.ckcov(cassCk, -82000, False, 'INTERVAL', 1., 'SCLK')
    npt.assert_allclose(values.as_intervals(),
                           [[2.67832538e+11, 2.67839247e+11],
                            [2.67839256e+11, 2.67867970e+11],
                            [2.67868006e+11, 2.67876774e+11]])
    
    values = cs.ckcov.flag(cassCk, 1, False, 'INTERVAL', 1., 'SCLK')
    assert values.card == 0
    
    with pytest.raises(KeyError):
        cs.ckcov_error(cassCk, 1, False, 'INTERVAL', 1., 'SCLK')
    
    #### pckcov, pckfrm
    with pytest.raises(IOError):
        pck = os.path.join(KERNEL_DIR,'pck00010.tpc' )
        cs.pckcov(pck, 10016)
    
    predict = os.path.join(KERNEL_DIR, 'earth_031228_231229_predict.bpc')
    frames = cs.pckfrm(predict)
    limits = [9.430566e+07, 7.570801e+08]
    npt.assert_allclose(cs.pckcov(predict, 3000).as_array(),
                        limits)


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


def test_ckfxfm():
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


def test_ckgp():
    cs.reset()
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    ckid = cs.ckobj(CassiniKernels.cassCk)[0]
    cover = cs.ckcov(CassiniKernels.cassCk, ckid,
                     False, "INTERVAL", 0.0, "SCLK")

    cmat, clkout = cs.ckgp(ckid, cover[0], 256, "J2000")
    expected_cmat = [
        [0.5064665782997639365, -0.75794210739897316387, 0.41111478554891744963],
        [-0.42372128242505308071, 0.19647683351734512858, 0.88422685364733510927],
        [-0.7509672961490383436, -0.6220294331642198804, -0.22164725216433822652],
    ]
    npt.assert_array_almost_equal(cmat, expected_cmat)
    assert clkout == 267832537952.0
    cs.reset()


def test_ckgp_ckgpav():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    ckid = cs.ckobj(CassiniKernels.cassCk)[0]
    cover = cs.ckcov(CassiniKernels.cassCk, ckid,
                     False, "INTERVAL", 0.0, "SCLK")
    
    (array1a, sclk1, found1) = cs.ckgp.flag(ckid, cover[0], 1., 'J2000')
    (array2a, array2b, sclk2, found2) = cs.ckgpav.flag(ckid, cover[0], 1., 'J2000')
    
    assert found1
    assert found2
    
    (array1a, sclk1,) = cs.ckgp(ckid, cover[0], 1., 'J2000')
    (array2a, array2b, sclk2) = cs.ckgpav(ckid, cover[0], 1., 'J2000')
    
    assert abs(sclk1 - sclk1) <= 1.
    assert sclk1 == sclk2
    npt.assert_array_equal(array1a, array2a, 0.)
    
    result2a = np.array([[ 0.506467, -0.757942,  0.411115],
                         [-0.423721,  0.196477,  0.884227],
                         [-0.750967, -0.622029, -0.221647]])
    
    result2b = np.array([-0.00231258, -0.00190334, -0.000696574])
    
    npt.assert_array_almost_equal(array2a, result2a)
    npt.assert_array_almost_equal(array2b, result2b)
    
    # sclk is 0.
    assert not cs.ckgp.flag(-82000, 0., 1., 'J2000')[-1]
    assert not cs.ckgpav.flag(-82000, 0., 1., 'J2000')[-1]
    
    with pytest.raises(IOError):
        cs.ckgp_error(-82000, 0., 1., 'J2000')
    with pytest.raises(IOError):
        cs.ckgpav_error(-82000, 0., 1., 'J2000')
    
    # sclk is 0.
    assert not cs.ckgp.flag(-82000, 0., 1., 'J2000')[-1]
    assert not cs.ckgpav.flag(-82000, 0., 1., 'J2000')[-1]
    
    with pytest.raises(IOError):
        cs.ckgp_error(-82000, 0., 1., 'J2000')
    with pytest.raises(IOError):
        cs.ckgpav_error(-82000, 0., 1., 'J2000')
    
    sclk = cover[0] + 100. * np.arange(10)
    (array1ax, sclk1x) = cs.ckgp_vector(-82000, sclk, 1., 'J2000')
    (array2ax, array2bx, sclk2x) = cs.ckgpav_vector(-82000, sclk, 1., 'J2000')
    
    assert array1ax.shape == (10, 3, 3)
    assert array2ax.shape == (10, 3, 3)
    assert array2bx.shape == (10, 3)
    npt.assert_array_equal(array1ax[0], array1a, 0)
    npt.assert_array_equal(array2ax[0], array2a, 0)
    npt.assert_array_equal(array2bx[0], array2b, 0)
    
    sclk = sclk + 100. * np.arange(10)
    (array1ax, sclk1x, found1x) = cs.ckgp_vector.flag(-82000, sclk, 1., 'J2000')
    (array2ax, array2bx, sclk2x, found2x) = cs.ckgpav_vector.flag(-82000, sclk, 1., 'J2000')
    
    assert array1ax.shape == (10, 3, 3)
    assert array2ax.shape == (10, 3, 3)
    assert array2bx.shape == (10, 3)
    npt.assert_array_equal(array1ax[0], array1a, 0)
    npt.assert_array_equal(array2ax[0], array2a, 0)
    npt.assert_array_equal(array2bx[0], array2b, 0)
    assert np.all(found1x)
    assert np.all(found2x)
    cs.reset()


def test_ckgpav():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassCk)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    ckid = cs.ckobj(CassiniKernels.cassCk)[0]
    cover = cs.ckcov(CassiniKernels.cassCk, ckid,
                     False, "INTERVAL", 0.0, "SCLK")
    cmat, avout, clkout = cs.ckgpav(ckid, cover[0], 256, "J2000")
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


@checking_pathlike_filename_variants("path_type_variant")
def test_cklpf(path_type_variant):
    cs.reset()
    cklpf = os.path.join(TEST_FILE_DIR, "cklpfkernel.bc")
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
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )
    cs.ckcls(handle)
    cs.kclear()
    handle = cs.cklpf(path_type_variant(cklpf))
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


@checking_pathlike_filename_variants("path_type_variant")
def test_ckobj(path_type_variant):
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    ids = cs.ckobj(path_type_variant(CassiniKernels.cassCk))
    assert len(ids) == 1
    
    
def test_ckobj_2():
    assert cs.ckobj(os.path.join(KERNEL_DIR, '13056_13057ra.bc')).as_array() == [-82000]


@checking_pathlike_filename_variants("path_type_variant")
def test_ckopn(path_type_variant):
    # cs crashes if ckcls detects nothing written to ck1
    ck1 = os.path.join(TEST_FILE_DIR, "ckopenkernel.bc")
    cleanup_kernel(ck1)
    ifname = "Test CK type 1 segment created by ccs_ckw01"
    handle = cs.ckopn(path_type_variant(ck1), ifname, 10)
    cs.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )

    cs.ckcls(handle)
    cs.kclear()
    assert os.path.exists(ck1)
    cleanup_kernel(ck1)
    assert not os.path.exists(ck1)


def test_ckupf():
    cs.reset()
    handle = cs.cklpf(CassiniKernels.cassCk)
    cs.ckupf(handle)
    cs.ckcls(handle)
    cs.reset()


def test_ckw01():
    ck1 = os.path.join(TEST_FILE_DIR, "type1.bc")
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
    for i in range(1, MAXREC):
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


def test_ckw02():
    ck2 = os.path.join(TEST_FILE_DIR, "type2.bc")
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
    for i in range(1, MAXREC):
        theta = i * RATE * SPACING_SECS * 1.0
        work_mat = cs.rotmat(work_mat, theta, 3)
        work_quat = cs.m2q(work_mat)
        quats[i] = work_quat
        av[i] = [0.0, 0.0, RATE]
    # begtime = sclkdp[0]
    # endtime = sclkdp[-1]
    begtime, endtime = starts[0], stops[-1]
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


def test_ckw03():
    ck3 = os.path.join(TEST_FILE_DIR, "type3.bc")
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
    for i in range(1, MAXREC):
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


# Test changed: subtyp variable chaged from int to string
def test_ckw05():
    cs.kclear()
    ck5 = os.path.join(TEST_FILE_DIR, "type5.bc")
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
        "C05TP0",
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
        "C05TP1",
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
        "C05TP2",
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
        "C05TP3",
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


def test_clpool():
    cs.pdpool("TEST_VAR", [-666.0])
    value = cs.gdpool("TEST_VAR", 0)
    assert len(value) == 1
    assert value[0] == -666.0
    cs.clpool()
    with pytest.raises(KeyError):
        cs.gdpool("TEST_VAR", 0)
        
        
def test_clpool_dlpool():
#### clpool, ldpool
    cs.furnsh(CoreKernels.pck)
    assert cs.bodfnd(599, 'RADII')
    assert cs.bodfnd(699, 'RADII')
    cs.clpool()
    assert not cs.bodfnd(699, 'RADII')
    cs.ldpool(CoreKernels.pck)
    assert cs.bodfnd(699, 'RADII')


def test_cmprss():
    strings = ["ABC...DE.F...", "...........", ".. ..AB....CD"]
    assert cs.cmprss(".", 2, strings[0]) == "ABC..DE.F.."
    assert cs.cmprss(".", 3, strings[1]) == "..."
    assert cs.cmprss(".", 1, strings[2]) == ". .AB.CD"
    assert cs.cmprss(".", 3, strings[1]) == "..."
    assert cs.cmprss(".", 1, strings[2]) == ". .AB.CD"
    assert cs.cmprss(
        " ", 0, " Embe dde d -sp   a c  es   ") == "Embedded-spaces"


def test_cnmfrm():
    ioFrcode, ioFrname = cs.cnmfrm("IO")
    assert ioFrcode == 10023
    assert ioFrname == "IAU_IO"


def test_cnmfrm_2():
    assert cs.cnmfrm('SATURN') == [10016, 'IAU_SATURN']
    assert cs.cnmfrm.flag('SATURN')[-1]
    assert not cs.cnmfrm.flag('foo')[-1]
    with pytest.raises(KeyError):
        cs.cnmfrm_error('foo')


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


def test_conics_2():
    pi = np.pi
    elem1 = [1., 0., 0., 0., 0., 0., 0., 1.]
    elem4 = [4., 0., 0., 0., 0., 0., 0., 1.]
    state10 = cs.conics(elem1, 0.)
    state11 = cs.conics(elem1, pi)
    state40 = cs.conics(elem4, 0.)
    state48 = cs.conics(elem4, 8*pi)

    npt.assert_almost_equal(state10, [1, 0, 0, 0, 1, 0.])
    npt.assert_almost_equal(state11, [-1, 0, 0, 0, -1, 0.])
    npt.assert_almost_equal(state40, [4, 0, 0, 0, 0.5, 0.])
    npt.assert_almost_equal(state48, [-4, 0, 0, 0, -0.5, 0.])

    test1 = cs.conics_vector(elem1, [0., pi, 2*pi])
    npt.assert_almost_equal(test1, [[1, 0, 0, 0, 1, 0.],
                                    [-1, 0, 0, 0, -1, 0.],
                                    [1, 0, 0, 0, 1, 0.]])

    test1 = cs.conics_vector([elem1, elem1, elem4, elem4], [0., pi, 0, 8*pi])
    npt.assert_almost_equal(test1, [[1, 0, 0, 0, 1,  0.],
                                    [-1, 0, 0, 0, -1,  0.],
                                    [4, 0, 0, 0, 0.5, 0.],
                                    [-4, 0, 0, 0, -0.5, 0.]])


def test_convrt():
    assert cs.convrt(300.0, "statute_miles", "km") == 482.80320
    npt.assert_almost_equal(
        cs.convrt(1.0, "parsecs", "lightyears"), 3.2615638, decimal=6
    )

    npt.assert_almost_equal(
        cs.convrt(1, "AU", "km"), 149597870.7, decimal=0
    )


def test_convrt_2():
    npt.assert_almost_equal(cs.convrt(1., 'inches', 'feet'), 1/12.)
    npt.assert_almost_equal(cs.convrt(12., 'inches', 'feet'), 1.)
    npt.assert_almost_equal(cs.convrt_vector([1., 12.], 'inches', 'feet'), [1/12., 1.])


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


def test_cvg2el_el2cvg():
    ellipse = cs.cgv2el([0, 0, 0], [1, 0, 0], [0, 1, 0])
    npt.assert_almost_equal(ellipse, [0, 0, 0, 1, 0, 0, 0, 1, 0])

    npt.assert_almost_equal(cs.el2cgv(ellipse), [[0, 0, 0], [1, 0, 0], [0, 1, 0]])

    ellipse = cs.cgv2el_vector([0, 0, 0], [[1, 0, 0], [2, 0, 0]], [0, 1, 0])
    npt.assert_almost_equal(ellipse, [[0, 0, 0, 1, 0, 0, 0, 1, 0],
                                      [0, 0, 0, 2, 0, 0, 0, 1, 0]])

    npt.assert_almost_equal(cs.el2cgv_vector(ellipse), [[[0, 0, 0], [0, 0, 0]],
                                                        [[1, 0, 0], [2, 0, 0]],
                                                        [[0, 1, 0], [0, 1, 0]]])


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


def test_cylsph():
    a = np.array(cs.cylsph(1.0, np.deg2rad(180.0), 1.0))
    b = np.array([1.4142, np.deg2rad(45.0), np.deg2rad(180.0)])
    np.testing.assert_almost_equal(b, a, decimal=4)


def test_cyllat_cylrec_cylsph_radrec_reclat_reccyl_etc():
    pi = np.pi
    npt.assert_almost_equal(cs.cyllat(1, 0, 0), [1, 0, 0])
    npt.assert_almost_equal(cs.cylrec(1, 0, 0), [1, 0, 0])
    npt.assert_almost_equal(cs.cylsph(1, 0, 0), [1, pi/2, 0])
    npt.assert_almost_equal(cs.radrec(1, 0, 0), [1, 0, 0])

    npt.assert_almost_equal(cs.reclat([1, 0, 0]), [1, 0, 0])
    npt.assert_almost_equal(cs.reccyl([1, 0, 0]), [1, 0, 0])
    npt.assert_almost_equal(cs.recsph([1, 0, 0]), [1, pi/2, 0])
    npt.assert_almost_equal(cs.recrad([1, 0, 0]), [1, 0, 0])

    npt.assert_almost_equal(cs.sphlat(1, 0, 0), [1, 0, pi/2])
    npt.assert_almost_equal(cs.sphcyl(1, 0, 0), [0, 0, 1])
    npt.assert_almost_equal(cs.sphrec(1, 0, 0), [0, 0, 1])

    npt.assert_almost_equal(cs.latcyl(1, 0, 0), [1, 0, 0])
    npt.assert_almost_equal(cs.latrec(1, 0, 0), [1, 0, 0])
    npt.assert_almost_equal(cs.latsph(1., 0., 0.), [1, pi/2, 0])

    npt.assert_almost_equal(cs.cyllat_vector([1, 2, 3, 4], 0, 0), [[1, 2, 3, 4],
                                                                   [0, 0, 0, 0],
                                                                   [0, 0, 0, 0]])
    npt.assert_almost_equal(cs.cylrec_vector([1, 2, 3, 4], 0, 0), [[1, 0, 0],
                                                                   [2, 0, 0],
                                                                   [3, 0, 0],
                                                                   [4, 0, 0]])
    npt.assert_almost_equal(cs.cylsph_vector(0, 0, [1, 2, 3, 4]), [[1, 2, 3, 4],
                                                                   [0, 0, 0, 0],
                                                                   [0, 0, 0, 0]])

    npt.assert_almost_equal(cs.reclat_vector(
        5 * [[1, 0, 0]]), [5 * [1], 5 * [0], 5 * [0]])
    npt.assert_almost_equal(cs.reccyl_vector(
        5 * [[1, 0, 0]]), [5 * [1], 5 * [0], 5 * [0]])
    npt.assert_almost_equal(cs.recsph_vector(5 * [[1, 0, 0]]),
                            [5 * [1], 5 * [pi/2], 5 * [0]])
    npt.assert_almost_equal(cs.recrad_vector(
        5 * [[1, 0, 0]]), [5 * [1], 5 * [0], 5 * [0]])
    npt.assert_almost_equal(cs.sphlat_vector([1, 1], 0, 0), [[1, 1], [0, 0], 2 * [pi/2]])
    npt.assert_almost_equal(cs.sphcyl_vector([1, 1], 0, 0), [[0, 0], [0, 0], [1, 1]])
    npt.assert_almost_equal(cs.sphrec_vector([1, 1], 0, 0), 2 * [[0, 0, 1]])
    npt.assert_almost_equal(cs.latcyl_vector(1., 0., [0, 0]), [[1, 1], [0, 0], [0, 0]])
    npt.assert_almost_equal(cs.latrec_vector(1., [0, 0], 0), 2 * [[1, 0, 0]])
    npt.assert_almost_equal(cs.latsph_vector([1, 2], 0., 0.),
                            [[1, 2], 2 * [pi/2], [0, 0]])


def test_constants():
    pi = np.pi
    assert cs.pi() == pi
    assert cs.halfpi() == pi / 2
    assert cs.twopi() == pi * 2
    assert cs.intmin() == -2 ** 31
    assert cs.intmax() == 2 ** 31 - 1
    assert cs.dpmin() == -1.7976931348623157e+308
    assert cs.dpmax() == 1.7976931348623157e+308

    assert cs.b1900() == 2415020.31352
    assert cs.b1950() == 2433282.42345905
    assert cs.clight() == 299792.458

    assert cs.dpr() == 180./pi
    assert cs.rpd() == 1./cs.dpr()

    assert cs.j1900() == 2415020.0
    assert cs.j1950() == 2433282.5
    assert cs.j2000() == 2451545.0
    assert cs.j2100() == 2488070.0
    assert cs.jyear() == 31557600.0
    assert cs.tyear() == 31556925.9747
    assert cs.spd() == 86400.0
    
    



def test_all():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.spk432)
    def assert_longitudes_equal(angle1, angle2, *, abs=1e-15):
        # Two equal longitudes may differ by 2π.  We have to shift the % operation
        # away from 0 so that -ε does become 2π-ε
        delta = ((angle2 - angle1 + PI) % TWOPI) - PI
        assert delta == pytest.approx(0, abs=abs)
    
    DPR = 180 / np.pi
    PI = np.pi
    TWOPI = 2 * np.pi
    
    et = cs.str2et( "2017 Mar 20")
    et1d = np.array([et, et+10, et+20, et+30])

    #### spkpos
    (pos, lt) = cs.spkpos("Moon", et, "J2000", "NONE", "Earth")
    npt.assert_allclose(pos, [-55658.44323296262, -379226.3293147546, -126505.93063865259])

    #### spkpos_vector
    (pos1d, lt1d) = cs.spkpos_vector("Moon", et1d, "J2000", "NONE", "Earth")
    pos1d_expected = np.array([[-55658.44323296, -379226.32931475, -126505.93063865],
                               [-55648.84010563, -379227.28937824, -126506.68034533],
                               [-55639.23694455, -379228.24920749, -126507.42997386],
                               [-55629.63374972, -379229.2088025 , -126508.17952426]])
    lt1d_expected = np.array([1.3463525460835728, 1.346351921934707, 1.346351297728633,
                              1.3463506734653514])

    npt.assert_allclose(pos1d_expected, pos1d)
    npt.assert_allclose(lt1d_expected, lt1d)

    #### cs.reclat
    (latrad1, latlon1, latlat1) = cs.reclat(pos)
    npt.assert_allclose(403626.33912495256, latrad1)
    npt.assert_allclose(-98.34959788856911, latlon1 * DPR)
    npt.assert_allclose(-18.265660770458155, latlat1 * DPR)

    #### latrec
    latpos = cs.latrec(latrad1, latlon1, latlat1)
    assert latpos == pytest.approx(pos, abs=1e-9)

    #### cs.reclat_vector, cs.latrec_vector
    (lat1dx, lat1dy, lat1dz) = cs.reclat_vector(pos1d)
    latpos1d = cs.latrec_vector(lat1dx, lat1dy, lat1dz)
    assert latpos1d == pytest.approx(pos1d, abs=1e-9)

    #### cs.reccyl
    (cylrad1, cyllon1, cylz1) = cs.reccyl(pos)
    npt.assert_allclose(383289.01777726377, cylrad1)
    npt.assert_allclose((-98.34959788856911 + 360), cyllon1 * DPR)
    npt.assert_allclose(-126505.9306386526, cylz1)

    #### cylrec
    cylpos = cs.cylrec(cylrad1, cyllon1, cylz1)
    assert cylpos == pytest.approx(pos, abs=1e-9)

    #### cs.reccyl_vector, cylrec_vector
    (cyl1dx, cyl1dy, cyl1dz) = cs.reccyl_vector(pos1d)
    cylpos1d = cs.cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    assert cylpos1d == pytest.approx(pos1d, abs=1e-9)

    #### latcyl
    (cylrad2, cyllon2, cylz2) = cs.latcyl(latrad1, latlon1, latlat1)
    assert cylrad2 == pytest.approx(cylrad1, abs=1e-9)
    assert_longitudes_equal(cyllon2, cyllon1)
    assert cylz2 == pytest.approx(cylz1, 1e-9)

    #### cyllat
    (latrad2, latlon2, latlat2) = cs.cyllat(cylrad2, cyllon2, cylz2)
    assert latrad2 == pytest.approx(latrad1, abs=1e-9)
    assert_longitudes_equal(latlon2, latlon1)
    assert latlat2 == pytest.approx(latlat1, abs=1e-15)

    #### latcyl_vector, cyllat_vector
    (cyl1dx, cyl1dy, cyl1dz) = cs.latcyl_vector(lat1dx, lat1dy, lat1dz)
    cylpos1d = cs.cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    assert cylpos1d == pytest.approx(pos1d, abs=1e-9)

    (lat1dx, lat1dy, lat1dz) = cs.cyllat_vector(cyl1dx, cyl1dy, cyl1dz)
    latpos1d = cs.latrec_vector(lat1dx, lat1dy, lat1dz)
    assert latpos1d == pytest.approx(pos1d, abs=1e-9)

    #### recsph
    (sphrad1, sphlat1, sphlon1) = cs.recsph(pos)
    assert sphrad1 == pytest.approx(403626.33912495256, abs=1e-3)
    assert sphlat1 * DPR == pytest.approx(108.26566077045815, abs=1e-6)
    assert sphlon1 * DPR == pytest.approx(-98.34959788856911, abs=1e-6)

    #### sphrec
    sphpos = cs.sphrec(sphrad1, sphlat1, sphlon1)
    assert sphpos == pytest.approx(pos, abs=1e-9)

    #### recsph_vector, sphrec_vector
    (sph1dx, sph1dy, sph1dz) = cs.recsph_vector(pos1d)
    sphpos1d = cs.sphrec_vector(sph1dx, sph1dy, sph1dz)
    assert sphpos1d == pytest.approx(pos1d, abs=1e-9)

    #### latsph
    (sphrad2, sphlat2, sphlon2) = cs.latsph(latrad1, latlon1, latlat1)
    assert sphrad2 == pytest.approx(sphrad1, abs=1e-9)
    assert_longitudes_equal(sphlat2, sphlat1)
    assert sphlon2 == pytest.approx(sphlon1, abs=1e-15)

    #### sphlat
    (latrad3, latlon3, latlat3) = cs.sphlat(sphrad2, sphlat2, sphlon2)
    assert latrad3 == pytest.approx(latrad1, abs=1e-9)
    assert_longitudes_equal(latlon3, latlon1)
    assert latlat3 == pytest.approx(latlat1, abs=1e-15)

    #### latsph_vector, sphlat_vector
    (sph1dx, sph1dy, sph1dz) = cs.latsph_vector(lat1dx, lat1dy, lat1dz)
    sphpos1d = cs.sphrec_vector(sph1dx, sph1dy, sph1dz)
    assert sphpos1d == pytest.approx(pos1d, abs=1e-9)

    (lat1dx, lat1dy, lat1dz) = cs.sphlat_vector(sph1dx, sph1dy, sph1dz)
    latpos1d = cs.latrec_vector(lat1dx, lat1dy, lat1dz)
    assert latpos1d == pytest.approx(pos1d, abs=1e-9)

    #### cylsph
    (sphrad3, sphlat3, sphlon3) = cs.cylsph(cylrad1, cyllon1, cylz1)
    assert sphrad3 == pytest.approx(sphrad1, abs=1e-9)
    assert sphlat3 == pytest.approx(sphlat1, abs=1e-15)
    assert_longitudes_equal(sphlon3, sphlon1)

    #### sphcyl
    (cylrad3, cyllon3, cylz3) = cs.sphcyl(sphrad3, sphlat3, sphlon3)
    assert cylrad3 == pytest.approx(cylrad1, abs=1e-9)
    assert_longitudes_equal(cyllon3, cyllon1)
    assert cylz3 == pytest.approx(cylz1, abs=1e-9)

    #### cylsph_vector, sphcyl_vector
    (sph1dx, sph1dy, sph1dz) = cs.cylsph_vector(cyl1dx, cyl1dy, cyl1dz)
    sphpos1d = cs.sphrec_vector(sph1dx, sph1dy, sph1dz)
    assert sphpos1d == pytest.approx(pos1d, abs=1e-9)

    (cyl1dx, cyl1dy, cyl1dz) = cs.sphcyl_vector(sph1dx, sph1dy, sph1dz)
    cylpos1d = cs.cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    assert cylpos1d == pytest.approx(pos1d, abs=1e-9)

