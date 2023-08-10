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
    
    
def fail_termpt():
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
    assert len(points) == 3
    

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
    
    
def fail_tkfram():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassFk)
    rotation, nextFrame = cs.tkfram(-82001)
    expected = np.array(
        [
            [6.12323400e-17, 0.00000000e00, -1.00000000e00],
            [0.00000000e00, 1.00000000e00, -0.00000000e00],
            [1.00000000e00, 0.00000000e00, 6.12323400e-17],
        ]
    )
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
# =============================================================================
# tparch
# tparse
# tpictr
# trace
# trcdep
# trcnam
# trcoff
# trgsep
# tsetyr
# twopi
# twovec
# twovxf
# tyear
# ucrss
# unitim
# unload
# unorm
# unormg
# utc2et
# vadd
# vaddg
# vcrss
# vdist
# vdistg
# vdot
# vdotg
# vequ
# vequg
# vhat
# vhatg
# vlcom
# vlcom3
# vlcomg
# vminug
# vminus
# vnorm
# vnormg
# vpack
# vperp
# vprjp
# vprjpi
# vproj
# vprojg
# vrel
# vrelg
# vrotv
# vscl
# vsclg
# vsep
# vsepg
# vsub
# vsubg
# vtmv
# vtmvg
# vupack
# vzero
# vzerog
# wncomd
# wncond
# wndifd
# wnelmd
# wnexpd
# wnextd
# wnfild
# wnfltd
# wnincd
# wninsd
# wnintd
# wnreld
# wnsumd
# wnunid
# xf2eul
# xf2rav
# xfmsta
# xpose
# xpose6
# xposeg
# =============================================================================
