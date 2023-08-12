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



def test_saelgv():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    expected_s_major = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expected_s_minor = [0.0, np.sqrt(2.0), 0.0]
    smajor, sminor = cs.saelgv(vec1, vec2)
    npt.assert_array_almost_equal(smajor, expected_s_major)
    npt.assert_array_almost_equal(sminor, expected_s_minor)
    
    
def test_scdecd():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    timein = cs.scencd(-32, "2/20538:39:768")
    sclkch = cs.scdecd(-32, timein)
    assert sclkch == "2/20538:39:768"
    
    
def test_sce2c():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    et = cs.str2et("1979 JUL 05 21:50:21.23379")
    sclkdp = cs.sce2c(-32, et)
    npt.assert_almost_equal(sclkdp, 985327949.9999709, decimal=6)


def test_sce2s():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    et = cs.str2et("1979 JUL 05 21:50:21.23379")
    sclkch = cs.sce2s(-32, et)
    assert sclkch == "2/20538:39:768"


def test_sce2t():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    et = cs.str2et("1979 JUL 05 21:50:21.23379")
    sclkdp = cs.sce2t(-32, et)
    npt.assert_almost_equal(sclkdp, 985327950.000000)
    
    
def test_scencd():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    sclkch = cs.scdecd(-32, 985327950.0)
    sclkdp = cs.scencd(-32, sclkch)
    npt.assert_almost_equal(sclkdp, 985327950.0)
    assert sclkch == "2/20538:39:768"
    

def test_scfmt():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    pstart, pstop = cs.scpart(-32)
    start = cs.scfmt(-32, pstart[0])
    stop = cs.scfmt(-32, pstop[0])
    assert start == "00011:00:001"
    assert stop == "04011:21:784"
    
    
def test_scpart():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    pstart, pstop = cs.scpart(-32)
    assert pstart is not None
    assert pstop is not None
    
    
def test_scs2e():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    et = cs.scs2e(-32, "2/20538:39:768")
    npt.assert_almost_equal(et, -646668528.58222842)
    utc = cs.et2utc(et, "C", 3)
    assert utc == "1979 JUL 05 21:50:21.234"
    
    
def test_sct2e():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    et = cs.sct2e(-32, 985327965.0)
    utc = cs.et2utc(et, "C", 3)
    assert utc == "1979 JUL 05 21:50:22.134"
    
    
def test_sctiks():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.voyagerSclk)
    ticks = cs.sctiks(-32, "20656:14:768")
    assert ticks == 991499967.00000000
    

# Fails due to sigerr
def fail_setmsg():
    cs.setmsg("test setmsg")
    cs.sigerr("some error")
    message = cs.getmsg("LONG", 2000)
    assert message == "test setmsg"
    cs.reset()
    
    
def test_shellc():
    array = ["FEYNMAN", "NEWTON", "EINSTEIN", "GALILEO", "EUCLID", "Galileo"]
    expected = ["EINSTEIN", "EUCLID", "FEYNMAN", "GALILEO", "Galileo", "NEWTON"]
    assert list(cs.shellc(array)) == expected
    
    
def test_shelld():
    array = [99.0, 33.0, 55.0, 44.0, -77.0, 66.0]
    expected = [-77.0, 33.0, 44.0, 55.0, 66.0, 99.0]
    npt.assert_array_almost_equal(cs.shelld(array), expected)


def test_shelli():
    array = [99, 33, 55, 44, -77, 66]
    expected = [-77, 33, 44, 55, 66, 99]
    npt.assert_array_almost_equal(cs.shelli(array), expected)
    
    
def fail_sigerr():
    cs.sigerr("test error")
    message = cs.getmsg("SHORT", 200)
    assert message == "test error"
    cs.reset()
    
    
def test_sincpt():
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
    # start test
    et = cs.str2et("2013 FEB 25 11:50:00 UTC")
    camid = cs.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, bounds = cs.getfov(camid)
    # run sincpt on boresight vector
    spoint, trgepc, obspos, found = cs.sincpt(
        "Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", frame, bsight
    )
    npt.assert_almost_equal(trgepc, 415065064.9055491)
    expected_spoint = [
        -143.56046004007180272311,
        202.90045955888857065474,
        -27.99454300594213052022,
    ]
    expected_obspos = [
        -329794.62202281970530748367,
        -557628.89673861570190638304,
        217721.3870436516881454736,
    ]
    npt.assert_array_almost_equal(spoint, expected_spoint, 5)
    npt.assert_array_almost_equal(obspos, expected_obspos, 5)
    
    
def test_spd():
    assert cs.spd() == 86400.0
    
    
def test_sphcyl():
    a = np.array(cs.sphcyl(1.4142, np.deg2rad(180.0), np.deg2rad(45.0)))
    b = [0.0, np.deg2rad(45.0), -np.sqrt(2)]
    np.testing.assert_almost_equal(a, b, decimal=4)
    
    
# Needs issue
def test_sphlat():
    result = np.array(cs.sphlat(1.0, cs.pi(), cs.halfpi()))
    expected = np.array([1.0, cs.halfpi(), -cs.halfpi()])
    npt.assert_array_almost_equal(result, expected)
    
    
def test_sphrec():
    expected1 = np.array([0.0, 0.0, 0.0])
    expected2 = np.array([1.0, 0.0, 0.0])
    expected3 = np.array([0.0, 0.0, -1.0])
    npt.assert_array_almost_equal(cs.sphrec(0.0, 0.0, 0.0), expected1)
    npt.assert_array_almost_equal(cs.sphrec(1.0, 90.0 * cs.rpd(), 0.0), expected2)
    npt.assert_array_almost_equal(
        cs.sphrec(1.0, 180.0 * cs.rpd(), 0.0), expected3
    )
    
    
def test_spk14a():
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [
        150.0,
        50.0,
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        250.0,
        50.0,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        350.0,
        50.0,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        450.0,
        50.0,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    spk14 = os.path.join(TEST_FILE_DIR, "test14.bsp")
    cleanup_kernel(spk14)
    handle = cs.spkopn(spk14, "Type 14 SPK internal file name.", 1024)
    init_size = os.path.getsize(spk14)
    cs.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    cs.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    cs.spk14e(handle)
    cs.spkcls(handle)
    end_size = os.path.getsize(spk14)
    assert end_size != init_size
    cleanup_kernel(spk14)
    
    
def test_spk14b():
    # Same as test_spk14a
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [
        150.0,
        50.0,
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        250.0,
        50.0,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        350.0,
        50.0,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        450.0,
        50.0,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    spk14 = os.path.join(TEST_FILE_DIR, "test14.bsp")
    cleanup_kernel(spk14)
    handle = cs.spkopn(spk14, "Type 14 SPK internal file name.", 1024)
    init_size = os.path.getsize(spk14)
    cs.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    cs.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    cs.spk14e(handle)
    cs.spkcls(handle)
    end_size = os.path.getsize(spk14)
    assert end_size != init_size
    cleanup_kernel(spk14)
    
    
def test_spk14e():
    # Same as test_spk14a
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [
        150.0,
        50.0,
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        250.0,
        50.0,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        350.0,
        50.0,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        450.0,
        50.0,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    spk14 = os.path.join(TEST_FILE_DIR, "test14.bsp")
    cleanup_kernel(spk14)
    handle = cs.spkopn(spk14, "Type 14 SPK internal file name.", 1024)
    init_size = os.path.getsize(spk14)
    cs.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    cs.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    cs.spk14e(handle)
    cs.spkcls(handle)
    end_size = os.path.getsize(spk14)
    assert end_size != init_size
    cleanup_kernel(spk14)
    
    
def test_spkacs():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2000 JAN 1 12:00:00 TDB")
    state, lt, dlt = cs.spkacs(301, et, "J2000", "lt+s", 399)
    expected_state = [
        -2.91584616594972088933e05,
        -2.66693402359092258848e05,
        -7.60956475582799030235e04,
        6.43439144942984264652e-01,
        -6.66065882529007446955e-01,
        -3.01310065348405708985e-01,
    ]
    expected_lt = 1.3423106103603615
    expected_dlt = 1.073169085424106e-07
    npt.assert_almost_equal(expected_lt, lt)
    npt.assert_almost_equal(expected_dlt, dlt)
    npt.assert_array_almost_equal(state, expected_state)
    
    
def test_spkapo():
    MARS = 499
    MOON = 301
    EPOCH = "Jan 1 2004 5:00 PM"
    REF = "J2000"
    ABCORR = "LT+S"
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et(EPOCH)
    state = cs.spkssb(MOON, et, REF)
    pos_vec, ltime = cs.spkapo(MARS, et, REF, state, ABCORR)
    expected_pos = [
        1.64534472413454592228e08,
        2.51219951337271928787e07,
        1.11454124484200235456e07,
    ]
    npt.assert_array_almost_equal(pos_vec, expected_pos, decimal=5)


def test_spkapp():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Jan 1 2004 5:00 PM")
    state = cs.spkssb(301, et, "J2000")
    state_vec, ltime = cs.spkapp(499, et, "J2000", state, "LT+S")
    expected_vec = [
        1.64534472413454592228e08,
        2.51219951337271928787e07,
        1.11454124484200235456e07,
        1.23119770045260814584e01,
        1.98884005139675998919e01,
        9.40678685353050170193e00,
    ]
    npt.assert_array_almost_equal(state_vec, expected_vec, decimal=6)
    

def test_spkaps():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2000 JAN 1 12:00:00 TDB")
    stobs = cs.spkssb(399, et, "J2000")
    state0 = np.array(cs.spkssb(399, et - 1, "J2000"))
    state2 = np.array(cs.spkssb(399, et + 1, "J2000"))
    # qderiv proc
    acc = cs.vlcomg(0.5 / 1.0, state0 + 3, -0.5 / 1.0, state2 + 3)
    acc = [acc[0], acc[1], acc[2]]
    state, lt, dlt = cs.spkaps(301, et, "j2000", "lt+s", stobs, acc)
    expected_lt = 1.3423106103603615
    expected_dlt = 1.073169085424106e-07
    expected_state = [
        -2.91584616594972088933e05,
        -2.66693402359092258848e05,
        -7.60956475582799030235e04,
        1.59912685775666059129e01,
        -1.64471169612870582455e01,
        -3.80333369259831766129e00,
    ]
    npt.assert_almost_equal(expected_lt, lt)
    npt.assert_almost_equal(expected_dlt, dlt)
    npt.assert_array_almost_equal(state, expected_state, decimal=5)
    
    
def test_spkcls():
    # Same as test_spkw02
    spk2 = os.path.join(TEST_FILE_DIR, "test2.bsp")
    cleanup_kernel(spk2)
    handle = cs.spkopn(spk2, "Type 2 SPK internal file name.", 4)
    init_size = os.path.getsize(spk2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
    ]
    segid = "SPK type 2 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    cs.spkw02(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs02,
        discrete_epochs[0],
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk2)
    assert end_size != init_size
    cleanup_kernel(spk2)
    
    
def test_spkcov():

    ids = cs.spkobj(CoreKernels.spk)
    temp_obj = ids[0]

    # Checks for defaults
    cover = cs.spkcov(CoreKernels.spk, temp_obj)
    result = [x for x in cover]
    expected = [-94651137.81606464, 315662463.18395346]
    npt.assert_array_almost_equal(result, expected)

    # Checks for old way, where if cover is pre-set, it should remain set
    cover = cs.SpiceCell(typeno=1, size=2000)
    cover = cs.spkcov(CoreKernels.spk, temp_obj)
    result = [x for x in cover]
    expected = [-94651137.81606464, 315662463.18395346]
    npt.assert_array_almost_equal(result, expected)
    
    
def test_spkcpo():
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2003 Oct 13 06:00:00")
    obspos = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439]
    state, lt = cs.spkcpo(
        "SUN", et, "DSS-14_TOPO", "OBSERVER", "CN+S", obspos, "EARTH", "ITRF93"
    )
    expected_lt = 497.93167787805714
    expected_state = [
        6.25122733012810498476e07,
        5.89674929926417097449e07,
        -1.22059095879866167903e08,
        2.47597313358008614159e03,
        -9.87026711803482794494e03,
        -3.49990805659246507275e03,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkcpt():
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(CoreKernels.testMetaKernel)
    obstime = cs.str2et("2003 Oct 13 06:00:00")
    trgpos = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439]
    state, lt = cs.spkcpt(
        trgpos, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    expected_lt = 497.9321928250503
    expected_state = [
        -3.41263006568005401641e06,
        -1.47916331564148992300e08,
        1.98124035009580813348e07,
        -1.07582448117249587085e04,
        2.50028331500427839273e02,
        1.11355285621842696742e01,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)
    
    
def test_spkcvo():
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(CoreKernels.testMetaKernel)
    obstime = cs.str2et("2003 Oct 13 06:00:00")
    obstate = [
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ]
    state, lt = cs.spkcvo(
        "SUN",
        obstime,
        "DSS-14_TOPO",
        "OBSERVER",
        "CN+S",
        obstate,
        0.0,
        "EARTH",
        "ITRF93",
    )
    expected_lt = 497.93167787798325
    expected_state = [
        6.25122733012975975871e07,
        5.89674929925705492496e07,
        -1.22059095879864960909e08,
        2.47597313358015026097e03,
        -9.87026711803497346409e03,
        -3.49990805659256830040e03,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)
    
    
def test_spkcvt():
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(CoreKernels.testMetaKernel)
    obstime = cs.str2et("2003 Oct 13 06:00:00")
    trgstate = [
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ]
    state, lt = cs.spkcvt(
        trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    expected_lt = 497.932192824968
    expected_state = [
        -3.41263006574816117063e06,
        -1.47916331564124494791e08,
        1.98124035009435638785e07,
        -1.07582448117247804475e04,
        2.50028331500423831812e02,
        1.11355285621839659171e01,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)
    
    
def test_spkez():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("July 4, 2003 11:00 AM PST")
    state, lt = cs.spkez(499, et, "J2000", "LT+S", 399)
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
    
    
def test_spkezp():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("July 4, 2003 11:00 AM PST")
    pos, lt = cs.spkezp(499, et, "J2000", "LT+S", 399)
    expected_lt = 269.6898813661505
    expected_pos = [
        73822235.31053550541400909424,
        -27127918.99847228080034255981,
        -18741306.30148987472057342529,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    
    
def test_spkezr():
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
    
    
def test_spkgeo():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("July 4, 2003 11:00 AM PST")
    state, lt = cs.spkgeo(499, et, "J2000", 399)
    expected_lt = 269.70264751151603
    expected_state = [
        7.38262164145559966564e07,
        -2.71280305524311661720e07,
        -1.87419738849752545357e07,
        -6.80950358877040429206e00,
        7.51381423681132254444e00,
        3.00129002640705921934e00,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    
    
def test_spkgps():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("July 4, 2003 11:00 AM PST")
    pos, lt = cs.spkgps(499, et, "J2000", 399)
    expected_lt = 269.70264751151603
    expected_pos = [
        73826216.41455599665641784668,
        -27128030.55243116617202758789,
        -18741973.88497525453567504883,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    
    
def test_spklef():
    handle = cs.spklef(CoreKernels.spk)
    assert handle != -1
    cs.spkuef(handle)
    
    
def test_spkltc():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2000 JAN 1 12:00:00 TDB")
    stobs = cs.spkssb(399, et, "j2000")
    state, lt, dlt = cs.spkltc(301, et, "j2000", "lt", stobs)
    expectedOneWayLt = 1.342310610325
    expected_lt = 1.07316909e-07
    expected_state = [
        -2.91569268313527107239e05,
        -2.66709183005481958389e05,
        -7.60991494675353169441e04,
        6.43530600728670520994e-01,
        -6.66081825882520739412e-01,
        -3.01322833716675120286e-01,
    ]
    npt.assert_almost_equal(lt, expectedOneWayLt)
    npt.assert_almost_equal(dlt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=5)
    
    
def test_spkobj():
    # Same as test_spkcov
    cover = cs.SpiceCell(typeno=1, size=2000)
    ids = cs.spkobj(CoreKernels.spk)
    temp_obj = ids[0]
    cover = cs.spkcov(CoreKernels.spk, temp_obj)
    result = [x for x in cover]
    expected = [-94651137.81606464, 315662463.18395346]
    npt.assert_array_almost_equal(result, expected)
    
    
def test_spkopa():
    SPKOPA = os.path.join(TEST_FILE_DIR, "testspkopa.bsp")
    cleanup_kernel(SPKOPA)
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2002 APR 27 00:00:00.000 TDB")
    # load subset from kernels
    handle, descr, ident = cs.spksfs(5, et)
    body, center, frame, otype, first, last, begin, end = cs.spkuds(descr)
    # create empty spk kernel
    handle_test = cs.spkopn(SPKOPA, "Test Kernel for spkopa unit test.", 4)
    # created empty spk kernel, write to it
    cs.spksub(handle, descr, ident, first, last, handle_test)
    # close kernel
    cs.spkcls(handle_test)
    # open the file to append to it
    handle_spkopa = cs.spkopa(SPKOPA)
    et2 = cs.str2et("2003 APR 27 00:00:00.000 TDB")
    handle, descr, ident = cs.spksfs(5, et2)
    body, center, frame, otype, first, last, begin, end = cs.spkuds(descr)
    cs.spksub(handle, descr, ident, first, last, handle_spkopa)
    cs.spkcls(handle_spkopa)
    # clean up
    cleanup_kernel(SPKOPA)
    
    
def test_spkopn():
    # Same as test_spkw02
    spk2 = os.path.join(TEST_FILE_DIR, "test2.bsp")
    cleanup_kernel(spk2)
    handle = cs.spkopn(spk2, "Type 2 SPK internal file name.", 4)
    init_size = os.path.getsize(spk2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
    ]
    segid = "SPK type 2 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    cs.spkw02(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs02,
        discrete_epochs[0],
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk2)
    assert end_size != init_size
    cleanup_kernel(spk2)
    
    
def test_spkpds():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = cs.spksfs(5, et)
    body, center, frame, otype, first, last, begin, end = cs.spkuds(descr)
    outframe = cs.frmnam(frame)
    spkpds_output = cs.spkpds(body, center, outframe, otype, first, last)
    npt.assert_almost_equal(spkpds_output, descr)
    
    
def test_spkpos():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("July 4, 2003 11:00 AM PST")
    pos, lt = cs.spkpos("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898813661505
    expected_pos = [
        73822235.31053550541400909424,
        -27127918.99847228080034255981,
        -18741306.30148987472057342529,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    
    
def test_spkpvn():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = cs.spksfs(5, et)
    refid, state, center = cs.spkpvn(handle, descr, et)
    expected_state = [
        -2.70063336478468656540e08,
        6.69404818553274393082e08,
        2.93505043081457614899e08,
        -1.24191493217698472051e01,
        -3.70147572019018955558e00,
        -1.28422514561611489370e00,
    ]
    npt.assert_array_almost_equal(state, expected_state)
    
    
def test_spksfs():
    cs.furnsh(CoreKernels.testMetaKernel)
    idcode = cs.bodn2c("PLUTO BARYCENTER")
    et = cs.str2et("2001 FEB 18 UTC")
    handle, descr, ident = cs.spksfs(idcode, et)
    assert ident == "DE-405"
    
    
def test_spkssb():
    cs.furnsh(CoreKernels.testMetaKernel)
    targ1 = 499
    epoch = "July 4, 2003 11:00 AM PST"
    frame = "J2000"
    targ2 = 399
    et = cs.str2et(epoch)
    state1 = cs.spkssb(targ1, et, frame)
    state2 = cs.spkssb(targ2, et, frame)
    dist = cs.vdist(state1[0:3], state2[0:3])
    npt.assert_approx_equal(dist, 80854820.0, significant=7)
    
    
def test_spksub():
    SPKSUB = os.path.join(TEST_FILE_DIR, "testspksub.bsp")
    cleanup_kernel(SPKSUB)
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2002 APR 27 00:00:00.000 TDB")
    # load subset from kernels
    handle, descr, ident = cs.spksfs(5, et)
    body, center, frame, otype, first, last, begin, end = cs.spkuds(descr)
    # create empty spk kernel
    handle_test = cs.spkopn(SPKSUB, "Test Kernel for spksub unit test.", 4)
    # created empty spk kernel, write to it
    cs.spksub(handle, descr, ident, first, last, handle_test)
    # close kernel
    cs.spkcls(handle_test)
    cleanup_kernel(SPKSUB)
    
    
def test_spkuds():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = cs.spksfs(5, et)
    body, center, frame, otype, first, last, begin, end = cs.spkuds(descr)
    assert body == 5
    assert begin == 54073
    assert end == 57950
    assert otype == 2
    

def test_spkuef():
    handle = cs.spklef(CoreKernels.spk)
    assert handle != -1
    cs.spkuef(handle)
    
    
def test_spkw02():
    spk2 = os.path.join(TEST_FILE_DIR, "test2.bsp")
    cleanup_kernel(spk2)
    handle = cs.spkopn(spk2, "Type 2 SPK internal file name.", 4)
    init_size = os.path.getsize(spk2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
    ]
    segid = "SPK type 2 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    cs.spkw02(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs02,
        discrete_epochs[0],
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk2)
    assert end_size != init_size
    cleanup_kernel(spk2)
    
    
def test_spkw03():
    spk3 = os.path.join(TEST_FILE_DIR, "test3.bsp")
    cleanup_kernel(spk3)
    handle = cs.spkopn(spk3, "Type 3 SPK internal file name.", 4)
    init_size = os.path.getsize(spk3)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs03 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    segid = "SPK type 3 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    cs.spkw03(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs03,
        discrete_epochs[0],
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk3)
    assert end_size != init_size
    cleanup_kernel(spk3)
    
 
def test_spkw05():
    spk5 = os.path.join(TEST_FILE_DIR, "test5.bsp")
    cleanup_kernel(spk5)
    handle = cs.spkopn(spk5, "Type 5 SPK internal file name.", 4)
    init_size = os.path.getsize(spk5)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    
    # Convert the list of lists to a 1-dimensional NumPy array
    discrete_states = np.array([
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ])
    
    segid = "SPK type 5 test segment"
    cs.spkw05(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        132712440023.310,
        9,
        discrete_states.flatten(),  # Flatten the 2-dimensional array into a 1-dimensional array
        discrete_epochs,
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk5)
    assert end_size != init_size
    cleanup_kernel(spk5)
    

def test_spkw08():
    spk8 = os.path.join(TEST_FILE_DIR, "test8.bsp")
    cleanup_kernel(spk8)
    handle = cs.spkopn(spk8, "Type 8 SPK internal file name.", 4)
    init_size = os.path.getsize(spk8)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = np.array([
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ])
    segid = "SPK type 8 test segment"
    step = discrete_epochs[1] - discrete_epochs[0]
    cs.spkw08(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states.flatten(),
        discrete_epochs[0],
        step,
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk8)
    assert end_size != init_size
    cleanup_kernel(spk8)
    
    
def test_spkw09():
    spk9 = os.path.join(TEST_FILE_DIR, "test9.bsp")
    cleanup_kernel(spk9)
    handle = cs.spkopn(spk9, "Type 9 SPK internal file name.", 4)
    init_size = os.path.getsize(spk9)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = np.array([
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ])
    segid = "SPK type 9 test segment"
    cs.spkw09(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states.flatten(),
        discrete_epochs,
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk9)
    assert end_size != init_size
    cleanup_kernel(spk9)
    
    
def test_spkw10():
    spk10 = os.path.join(TEST_FILE_DIR, "test10.bsp")
    tle = [
        "1 18123U 87 53  A 87324.61041692 -.00000023  00000-0 -75103-5 0 00675",
        "2 18123  98.8296 152.0074 0014950 168.7820 191.3688 14.12912554 21686",
        "1 18123U 87 53  A 87326.73487726  .00000045  00000-0  28709-4 0 00684",
        "2 18123  98.8335 154.1103 0015643 163.5445 196.6235 14.12912902 21988",
        "1 18123U 87 53  A 87331.40868801  .00000104  00000-0  60183-4 0 00690",
        "2 18123  98.8311 158.7160 0015481 149.9848 210.2220 14.12914624 22644",
        "1 18123U 87 53  A 87334.24129978  .00000086  00000-0  51111-4 0 00702",
        "2 18123  98.8296 161.5054 0015372 142.4159 217.8089 14.12914879 23045",
        "1 18123U 87 53  A 87336.93227900 -.00000107  00000-0 -52860-4 0 00713",
        "2 18123  98.8317 164.1627 0014570 135.9191 224.2321 14.12910572 23425",
        "1 18123U 87 53  A 87337.28635487  .00000173  00000-0  10226-3 0 00726",
        "2 18123  98.8284 164.5113 0015289 133.5979 226.6438 14.12916140 23475",
        "1 18123U 87 53  A 87339.05673569  .00000079  00000-0  47069-4 0 00738",
        "2 18123  98.8288 166.2585 0015281 127.9985 232.2567 14.12916010 24908",
        "1 18123U 87 53  A 87345.43010859  .00000022  00000-0  16481-4 0 00758",
        "2 18123  98.8241 172.5226 0015362 109.1515 251.1323 14.12915487 24626",
        "1 18123U 87 53  A 87349.04167543  .00000042  00000-0  27370-4 0 00764",
        "2 18123  98.8301 176.1010 0015565 100.0881 260.2047 14.12916361 25138",
    ]
    epoch_x = []
    elems_x = []
    cs.furnsh(CoreKernels.testMetaKernel)
    for i in range(0, 18, 2):
        lines = [tle[i], tle[i + 1]]
        epoch, elems = cs.getelm(1950, lines)
        epoch_x.append(epoch)
        elems_x.extend(elems)
    first = epoch_x[0] - 0.5 * cs.spd()
    last = epoch_x[-1] + 0.5 * cs.spd()
    consts = [
        1.082616e-3,
        -2.538813e-6,
        -1.65597e-6,
        7.43669161e-2,
        120.0,
        78.0,
        6378.135,
        1.0,
    ]
    cleanup_kernel(spk10)
    handle = cs.spkopn(spk10, "Type 10 SPK internal file name.", 100)
    init_size = os.path.getsize(spk10)
    cs.spkw10(
        handle,
        -118123,
        399,
        "J2000",
        first,
        last,
        "DMSP F8",
        consts,
        9,
        elems_x,
        epoch_x,
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk10)
    assert end_size != init_size
    cleanup_kernel(spk10)


def test_spkw12():
    spk12 = os.path.join(TEST_FILE_DIR, "test12.bsp")
    cleanup_kernel(spk12)
    handle = cs.spkopn(spk12, "Type 12 SPK internal file name.", 4)
    init_size = os.path.getsize(spk12)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = np.array([
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ])
    segid = "SPK type 12 test segment"
    step = discrete_epochs[1] - discrete_epochs[0]
    cs.spkw12(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states.flatten(),
        discrete_epochs[0],
        step,
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk12)
    assert end_size != init_size
    cleanup_kernel(spk12)
    
    
def test_spkw13():
    spk13 = os.path.join(TEST_FILE_DIR, "test13.bsp")
    cleanup_kernel(spk13)
    handle = cs.spkopn(spk13, "Type 13 SPK internal file name.", 4)
    init_size = os.path.getsize(spk13)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = np.array([
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ])
    segid = "SPK type 13 test segment"
    cs.spkw13(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states.flatten(),
        discrete_epochs,
    )
    cs.spkcls(handle)
    end_size = os.path.getsize(spk13)
    assert end_size != init_size
    cleanup_kernel(spk13)
    
    
def test_spkw15():
    discrete_epochs = [100.0, 900.0]
    #
    spk15 = os.path.join(TEST_FILE_DIR, "test15.bsp")
    cleanup_kernel(spk15)
    # create the test kernel
    handle = cs.spkopn(spk15, "Type 13 SPK internal file name.", 4)
    init_size = os.path.getsize(spk15)
    # load kernels
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Dec 25, 2007")
    state, ltime = cs.spkezr("Moon", et, "J2000", "NONE", "EARTH")
    mu = cs.bodvrd("EARTH", "GM")
    elts = cs.oscelt(state, et, mu[0])
    # From these collect the eccentricity and semi-latus
    ecc = elts[1]
    p = elts[0] * (1.0 + ecc)
    # Next get the trajectory pole vector and the periapsis vector.
    state = state[0:3]
    tp = cs.ucrss(state, state + 4)
    pa = cs.vhat(state)
    # Enable both J2 corrections.
    j2flg = 0.0
    # other constants, as I don't need real values
    pv = [1.0, 2.0, 3.0]
    gm = 398600.436
    j2 = 1.0
    radius = 6000.0
    # now call spkw15
    cs.spkw15(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        "Test SPKW15",
        et,
        tp,
        pa,
        p,
        ecc,
        j2flg,
        pv,
        gm,
        j2,
        radius,
    )
    # close the kernel
    cs.spkcls(handle)
    end_size = os.path.getsize(spk15)
    # cleanup
    assert end_size != init_size
    cleanup_kernel(spk15)
    #
    
    
def test_spkw17():
    discrete_epochs = [100.0, 900.0]
    #
    spk17 = os.path.join(TEST_FILE_DIR, "test17.bsp")
    cleanup_kernel(spk17)
    # create the test kernel
    handle = cs.spkopn(spk17, "Type 17 SPK internal file name.", 4)
    init_size = os.path.getsize(spk17)
    # load kernels
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Dec 25, 2007")
    # make the eqel vector and the rapol and decpol floats
    p = 10000.0
    gm = 398600.436
    ecc = 0.1
    a = p / (1.0 - ecc)
    n = np.sqrt(gm / a) / a
    argp = 30.0 * cs.rpd()
    node = 15.0 * cs.rpd()
    inc = 10.0 * cs.rpd()
    m0 = 45.0 * cs.rpd()
    eqel = [
        a,
        ecc * np.sin(argp + node),
        ecc * np.cos(argp + node),
        m0 + argp + node,
        np.tan(inc / 2.0) * np.sin(node),
        np.tan(inc / 2.0) * np.cos(node),
        0.0,
        n,
        0.0,
    ]
    rapol = cs.halfpi() * -1
    decpol = cs.halfpi()
    # now call spkw17
    cs.spkw17(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        "Test SPKW17",
        et,
        eqel,
        rapol,
        decpol,
    )
    # close the kernel
    cs.spkcls(handle)
    end_size = os.path.getsize(spk17)
    # cleanup
    assert end_size != init_size
    cleanup_kernel(spk17)
    
    
def test_spkw18():
    #
    spk18 = os.path.join(TEST_FILE_DIR, "test18.bsp")
    cleanup_kernel(spk18)
    # make a new kernel
    handle = cs.spkopn(spk18, "Type 18 SPK internal file name.", 4)
    init_size = os.path.getsize(spk18)
    # test data
    body = 3
    center = 10
    ref = "J2000"
    epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    states = np.array([
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    ])
    # test spkw18 with S18TP0
    cs.spkw18(
        handle,
        "S18TP0",
        body,
        center,
        ref,
        epochs[0],
        epochs[-1],
        "SPK type 18 test segment",
        3,
        9,
        states.flatten(),
        epochs,
    )
    # close the kernel
    cs.spkcls(handle)
    end_size = os.path.getsize(spk18)
    assert end_size != init_size
    # test reading data
    handle = cs.spklef(spk18)
    state, lt = cs.spkgeo(body, epochs[0], ref, center)
    npt.assert_array_equal(state, [101.0, 201.0, 301.0, 1.0, 1.0, 1.0])
    state, lt = cs.spkgeo(body, epochs[1], ref, center)
    npt.assert_array_equal(state, [102.0, 202.0, 302.0, 1.0, 1.0, 1.0])
    cs.spkcls(handle)
    # cleanup
    cleanup_kernel(spk18)


def test_spkw20():
    #
    spk20 = os.path.join(TEST_FILE_DIR, "test20.bsp")
    cleanup_kernel(spk20)
    # create the test kernel
    handle = cs.spkopn(spk20, "Type 20 SPK internal file name.", 4)
    init_size = os.path.getsize(spk20)
    # now call spkw20, giving fake data from f_spk20.c from tcs
    intlen = 5.0
    n = 100
    polydg = 1
    cdata = np.arange(1.0, 198000.0)  #
    dscale = 1.0
    tscale = 1.0
    initjd = 2451545.0
    initfr = 0.25
    first = (initjd - cs.j2000() + initfr) * cs.spd()
    last = ((initjd - cs.j2000()) + initfr + n * intlen) * cs.spd()
    cs.spkw20(
        handle,
        301,
        3,
        "J2000",
        first,
        last,
        "Test SPKW20",
        intlen,
        n,
        polydg,
        cdata,
        dscale,
        tscale,
        initjd,
        initfr,
    )
    # close the kernel
    cs.spkcls(handle)
    end_size = os.path.getsize(spk20)
    # cleanup
    assert end_size != init_size
    cleanup_kernel(spk20)
    
    
def test_srfc2s():
    kernel = os.path.join(TEST_FILE_DIR, "srfc2s_ex1.tm")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    cs.furnsh(kernel)
    assert cs.srfc2s(1, 499) == "MGS MOLA  64 pixel/deg"
    assert cs.srfc2s(1, 401) == "PHOBOS GASKELL Q512"
    assert cs.srfc2s(2, 499) == "MGS MOLA 128 pixel/deg"
    with pytest.raises(KeyError):
        cs.srfc2s(1, -1)
    cs.reset()
    cleanup_kernel(kernel)
    
    
def test_srfcss():
    kernel = os.path.join(TEST_FILE_DIR, "srfcss_ex1.tm")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    cs.furnsh(kernel)
    assert cs.srfcss(1, "MARS") == "MGS MOLA  64 pixel/deg"
    assert cs.srfcss(1, "PHOBOS") == "PHOBOS GASKELL Q512"
    assert cs.srfcss(2, "499") == "MGS MOLA 128 pixel/deg"
    with pytest.raises(KeyError):
        cs.srfcss(1, "ZZZ")
    cs.reset()
    cleanup_kernel(kernel)
    
    
def test_srfnrm():
    cs.furnsh(CoreKernels.pck)
    cs.furnsh(ExtraKernels.phobosDsk)
    srfpts = cs.latsrf(
        "DSK/UNPRIORITIZED", "phobos", 0.0, "iau_phobos", [[0.0, 45.0], [60.0, 45.0]]
    )
    normals = cs.srfnrm("DSK/UNPRIORITIZED", "phobos", 0.0, "iau_phobos", srfpts)
    srf_rad = np.array([cs.recrad(x) for x in srfpts])
    nrm_rad = np.array([cs.recrad(x) for x in normals])
    assert np.any(np.not_equal(srf_rad, nrm_rad))
    
    
def test_srfrec():
    cs.furnsh(CoreKernels.testMetaKernel)
    x = cs.srfrec(399, 100.0 * cs.rpd(), 35.0 * cs.rpd())
    expected = [-906.24919474, 5139.59458217, 3654.29989637]
    npt.assert_array_almost_equal(x, expected)
    
    
def test_srfs2c():
    kernel = os.path.join(TEST_FILE_DIR, "srfs2c_ex1.tm")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    cs.furnsh(kernel)
    assert cs.srfs2c("MGS MOLA  64 pixel/deg", "MARS") == 1
    assert cs.srfs2c("PHOBOS GASKELL Q512", "PHOBOS") == 1
    assert cs.srfs2c("MGS MOLA 128 pixel/deg", "MARS") == 2
    assert cs.srfs2c("MGS MOLA  64 pixel/deg", "499") == 1
    assert cs.srfs2c("1", "PHOBOS") == 1
    assert cs.srfs2c("2", "499") == 2
    with pytest.raises(KeyError):
        cs.srfs2c("ZZZ", "MARS")
    cs.reset()
    cleanup_kernel(kernel)
    
    
def test_srfscc():
    kernel = os.path.join(TEST_FILE_DIR, "srfscc_ex1.tm")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    cs.furnsh(kernel)
    assert cs.srfscc("MGS MOLA  64 pixel/deg", 499) == 1
    assert cs.srfscc("PHOBOS GASKELL Q512", 401) == 1
    assert cs.srfscc("MGS MOLA 128 pixel/deg", 499) == 2
    assert cs.srfscc("1", 401) == 1
    assert cs.srfscc("2", 499) == 2
    with pytest.raises(KeyError):
        cs.srfscc("ZZZ", 499)
    cs.reset()
    cleanup_kernel(kernel)
    

def test_srfxpt():
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
    # start test
    et = cs.str2et("2013 FEB 25 11:50:00 UTC")
    camid = cs.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, bounds = cs.getfov(camid)
    # run srfxpt on boresight vector
    spoint, dist, trgepc, obspos, found = cs.srfxpt(
        "Ellipsoid", "Enceladus", et, "LT+S", "CASSINI", frame, bsight
    )
    npt.assert_almost_equal(dist, 683459.6415073496)
    npt.assert_almost_equal(trgepc, 415065064.9055491)
    expected_spoint = [
        -143.56046006834264971985,
        202.9004595420923067195,
        -27.99454299292458969717,
    ]
    expected_obspos = [
        329627.25001832831185311079,
        557847.97086489037610590458,
        -217744.02422016291529871523,
    ]
    npt.assert_array_almost_equal(spoint, expected_spoint)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    

def test_stelab():
    IDOBS = 399
    IDTARG = 301
    UTC = "July 4 2004"
    FRAME = "J2000"
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et(UTC)
    sobs = cs.spkssb(IDOBS, et, FRAME)
    starg, ltime = cs.spkapp(IDTARG, et, FRAME, sobs, "LT")
    expected_starg = [
        2.01738718005936592817e05,
        -2.60893145259797573090e05,
        -1.47722589585214853287e05,
        9.24727104822839152121e-01,
        5.32379608845730878386e-01,
        2.17669748758417824774e-01,
    ]
    npt.assert_array_almost_equal(starg, expected_starg)
    cortarg = cs.stelab(starg[0:3], starg[3:6])
    expected_cortarg = [
        201739.80378842627396807075,
        -260892.46619604207808151841,
        -147722.30606629714020527899,
    ]
    npt.assert_array_almost_equal(expected_cortarg, cortarg)
    
    
def test_stlabx():
    IDOBS = 399
    IDTARG = 301
    UTC = "July 4 2004"
    FRAME = "J2000"
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et(UTC)
    sobs = cs.spkssb(IDOBS, et, FRAME)
    pos, ltime = cs.spkapo(IDTARG, et, FRAME, sobs, "XLT")
    # note the values below won't match due to the different kernels used
    expected_pos = [201809.933536, -260878.049826, -147716.077987]
    npt.assert_array_almost_equal(pos, expected_pos, 1)
    pcorr = cs.stlabx(pos, sobs[3:6])
    expected_pcorr = [201782.730972, -260894.375627, -147724.405897]
    npt.assert_array_almost_equal(pcorr, expected_pcorr, 1)
    

def test_stpool():
    kernel = os.path.join(TEST_FILE_DIR, "stpool_t.ker")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("SPK_FILES = ( 'this_is_the_full_path_specification_*',\n")
        kernelFile.write("              'of_a_file_with_a_long_name',\n")
        kernelFile.write("              'this_is_the_full_path_specification_*',\n")
        kernelFile.write("              'of_a_second_file_name' )\n")
        kernelFile.close()
    cs.furnsh(kernel)
    string= cs.stpool("SPK_FILES", 0, "*")
    assert string == "this_is_the_full_path_specification_of_a_file_with_a_long_name"
    string = cs.stpool("SPK_FILES", 1, "*")
    assert string == "this_is_the_full_path_specification_of_a_second_file_name"
    cleanup_kernel(kernel)
    
    
def test_str2et():
    cs.furnsh(CoreKernels.testMetaKernel)
    date = "Thu Mar 20 12:53:29 PST 1997"
    et = cs.str2et(date)
    npt.assert_almost_equal(et, -87836728.81438904)
    
    
def test_subpnt():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2008 aug 11 00:00:00")
    radii = cs.bodvrd("MARS", "RADII")
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    methods = ["Intercept:  ellipsoid", "Near point: ellipsoid"]
    expecteds = [
        [
            349199089.604657,
            349199089.64135259,
            0.0,
            199.30230503198658,
            199.30230503198658,
            26.262401237213588,
            25.99493675077423,
            160.69769496801342,
            160.69769496801342,
            25.994934171245205,
            25.994934171245202,
        ],
        [
            349199089.6046486,
            349199089.60464859,
            0.0,
            199.30230503240247,
            199.30230503240247,
            25.99493675092049,
            25.99493675092049,
            160.69769496759753,
            160.69769496759753,
            25.729407227461937,
            25.994934171391463,
        ],
    ]
    for expected, method in zip(expecteds, methods):
        spoint, trgepc, srfvec = cs.subpnt(
            method, "Mars", et, "IAU_MARS", "LT+S", "Earth"
        )
        odist = np.linalg.norm(srfvec)
        npt.assert_almost_equal(odist, expected[1], decimal=5)
        spglon, spglat, spgalt = cs.recpgr("mars", spoint, re, f)
        npt.assert_almost_equal(spgalt, expected[2], decimal=5)
        npt.assert_almost_equal(spglon * cs.dpr(), expected[3], decimal=5)
        npt.assert_almost_equal(spglat * cs.dpr(), expected[5], decimal=5)
        spcrad, spclon, spclat = cs.reclat(spoint)
        npt.assert_almost_equal(spclon * cs.dpr(), expected[7], decimal=5)
        npt.assert_almost_equal(spclat * cs.dpr(), expected[9], decimal=5)
        obspos = np.subtract(spoint, srfvec)
        opglon, opglat, opgalt = cs.recpgr("mars", obspos, re, f)
        npt.assert_almost_equal(opgalt, expected[0], decimal=5)
        npt.assert_almost_equal(opglon * cs.dpr(), expected[4], decimal=5)
        npt.assert_almost_equal(opglat * cs.dpr(), expected[6], decimal=5)
        opcrad, opclon, opclat = cs.reclat(obspos)
        npt.assert_almost_equal(opclon * cs.dpr(), expected[8], decimal=5)
        npt.assert_almost_equal(opclat * cs.dpr(), expected[10], decimal=5)


def test_subpt():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("JAN 1, 2006")
    point1, alt1 = np.array(
        cs.subpt("near point", "earth", et, "lt+s", "moon"), dtype=object
    )
    point2, alt2 = np.array(
        cs.subpt("intercept", "earth", et, "lt+s", "moon"), dtype=object
    )
    dist = np.linalg.norm(np.subtract(point1, point2))
    sep = cs.vsep(point1, point2) * cs.dpr()
    npt.assert_almost_equal(dist, 16.705476097706171)
    npt.assert_almost_equal(sep, 0.15016657506598063)
    
    
def test_subslr():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2008 aug 11 00:00:00")
    radii = cs.bodvrd("MARS", "RADII")
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    methods = ["Intercept:  ellipsoid", "Near point: ellipsoid"]
    expecteds = [
        [
            0.0,
            175.8106755102322,
            23.668550281477703,
            -175.81067551023222,
            23.420819936106213,
            175.810721536362,
            23.42082337182491,
            -175.810721536362,
            23.42081994605096,
        ],
        [
            0.0,
            175.8106754100492,
            23.420823361866685,
            -175.81067551023222,
            23.175085577910583,
            175.81072152220804,
            23.420823371828,
            -175.81072152220804,
            23.420819946054046,
        ],
    ]
    for expected, method in zip(expecteds, methods):
        spoint, trgepc, srfvec = cs.subslr(
            method, "Mars", et, "IAU_MARS", "LT+S", "Earth"
        )
        spglon, spglat, spgalt = cs.recpgr("mars", spoint, re, f)
        npt.assert_almost_equal(spgalt, expected[0], decimal=5)
        npt.assert_almost_equal(spglon * cs.dpr(), expected[1], decimal=5)
        npt.assert_almost_equal(spglat * cs.dpr(), expected[2], decimal=5)
        spcrad, spclon, spclat = cs.reclat(spoint)
        npt.assert_almost_equal(spclon * cs.dpr(), expected[3], decimal=5)
        npt.assert_almost_equal(spclat * cs.dpr(), expected[4], decimal=5)
        sunpos, sunlt = cs.spkpos("sun", trgepc, "iau_mars", "lt+s", "mars")
        supgln, supglt, supgal = cs.recpgr("mars", sunpos, re, f)
        npt.assert_almost_equal(supgln * cs.dpr(), expected[5], decimal=5)
        npt.assert_almost_equal(supglt * cs.dpr(), expected[6], decimal=5)
        supcrd, supcln, supclt = cs.reclat(sunpos)
        npt.assert_almost_equal(supcln * cs.dpr(), expected[7], decimal=5)
        npt.assert_almost_equal(supclt * cs.dpr(), expected[8], decimal=5)
        
        
def test_subsol():
    cs.furnsh(CoreKernels.testMetaKernel)
    point = cs.subsol("near point", "earth", 0.0, "lt+s", "mars")
    npt.assert_array_almost_equal(
        point, [5850.44947427, 509.68837118, -2480.24722673], decimal=4
    )
    intercept = cs.subsol("intercept", "earth", 0.0, "lt+s", "mars")
    npt.assert_array_almost_equal(
        intercept, [5844.4362338, 509.16450054, -2494.39569089], decimal=4
    )
    
    
def test_sumad():
    assert cs.sumad([1.0, 2.0, 3.0]) == 6.0
    
    
def test_sumai():
    assert cs.sumai([1, 2, 3]) == 6
    
    
def test_surfnm():
    point = [0.0, 0.0, 3.0]
    npt.assert_array_almost_equal(cs.surfnm(1.0, 2.0, 3.0, point),
                                  [0.0, 0.0, 1.0])
    

def test_surfpt():
    position = [2.0, 0.0, 0.0]
    u = [-1.0, 0.0, 0.0]
    point = cs.surfpt(position, u, 1.0, 2.0, 3.0)
    npt.assert_array_almost_equal(point[0], [1.0, 0.0, 0.0])
    

def test_surfpv():
    stvrtx = [2.0, 0.0, 0.0, 0.0, 0.0, 3.0]
    stdir = [-1.0, 0.0, 0.0, 0.0, 0.0, 4.0]
    stx = cs.surfpv(stvrtx, stdir, 1.0, 2.0, 3.0)
    expected = [1.0, 0.0, 0.0, 0.0, 0.0, 7.0]
    npt.assert_array_almost_equal(expected, stx[0])
    
    
def test_swpool():
    # add TEST_VAR_SWPOOL
    cs.pdpool("TEST_VAR_SWPOOL", [-666.0])
    # establish check for TEST_VAR_SWPOOL
    cs.swpool("TEST_SWPOOL", ["TEST_VAR_SWPOOL"])
    # update TEST_VAR_SWPOOL
    cs.pdpool("TEST_VAR_SWPOOL", [555.0])
    # check for updated variable
    updated = cs.cvpool("TEST_SWPOOL")
    value = cs.gdpool("TEST_VAR_SWPOOL", 0)
    assert len(value) == 1
    assert value[0] == 555.0
    cs.clpool()
    assert updated is True
    
    
def test_sxform():
    cs.furnsh(CoreKernels.testMetaKernel)
    lon = 118.25 * cs.rpd()
    lat = 34.05 * cs.rpd()
    alt = 0.0
    utc = "January 1, 1990"
    et = cs.str2et(utc)
    abc = cs.bodvrd("EARTH", "RADII")
    equatr = abc[0]
    polar = abc[2]
    f = (equatr - polar) / equatr
    estate = cs.georec(lon, lat, alt, equatr, f)
    estate = np.append(estate, [0.0, 0.0, 0.0])
    xform = np.array(cs.sxform("IAU_EARTH", "J2000", et))
    jstate = np.dot(xform, estate)
    expected = np.array(
        [
            -4131.45969,
            -3308.36805,
            3547.02462,
            0.241249619,
            -0.301019201,
            0.000234215666,
        ]
    )
    npt.assert_array_almost_equal(jstate, expected, decimal=4)


def test_szpool():
    assert cs.szpool("MAXVAR") == 26003
    assert cs.szpool("MAXLEN") == 32
    assert cs.szpool("MAXVAL") == 400000
    assert cs.szpool("MXNOTE") == 130015
    assert cs.szpool("MAXAGT") == 1000
    assert cs.szpool("MAXCHR") == 80
    assert cs.szpool("MAXLIN") == 15000
# =============================================================================
# =============================================================================
# # stcf01
# =============================================================================
# =============================================================================
# # stcg01
# =============================================================================
# =============================================================================
# # stcl01
# =============================================================================
# =============================================================================
