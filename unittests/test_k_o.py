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


def test_kclear():
    cs.kclear()
    assert cs.ktotal("ALL") == 0


def test_kdata():
    cs.furnsh(CoreKernels.testMetaKernel)
    file, ftype, source, handle = cs.kdata(0, "META")
    assert ftype == "META"


def test_kinfo():
    cs.furnsh(CoreKernels.testMetaKernel)
    filetype, source, handle = cs.kinfo(CoreKernels.testMetaKernel)
    assert filetype == "META"


def test_kplfrm():
    cs.furnsh(CoreKernels.testMetaKernel)
    cell = cs.kplfrm(-1)
    assert cell.size > 100


def test_ktotal():
    # same as unload test
    cs.furnsh(CoreKernels.testMetaKernel)
    # 4 kernels + the meta kernel = 5
    assert cs.ktotal("ALL") == 5
    cs.unload(CoreKernels.testMetaKernel)
    assert cs.ktotal("ALL") == 0


def test_kxtrct():
    # Tests from examples at this URL:  https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/ccs/kxtrct_c.html#Examples
    i = 0
    while i < 500:
        i += 1
        assert [" TO 1 January 1987", True, "1 October 1984 12:00:00"] == cs.kxtrct(
            "FROM",
            "from to beginning ending".upper().split(),
            "FROM 1 October 1984 12:00:00 TO 1 January 1987"
        )
        assert ["FROM 1 October 1984 12:00:00", True, "1 January 1987"] == cs.kxtrct(
            "TO",
            "from to beginning ending".upper().split(),
            "FROM 1 October 1984 12:00:00 TO 1 January 1987"
        )
        assert [" PHONE: 354-4321", True, "4800 OAK GROVE DRIVE"] == cs.kxtrct(
            "ADDRESS:",
            "address: phone: name:".upper().split(),
            "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ",
        )
        assert ["ADDRESS: 4800 OAK GROVE DRIVE", True, "354-4321"] == cs.kxtrct(
            "PHONE:",
            "address: phone: name:".upper().split(),
            "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 "
        )
# =============================================================================
#         with pytest.raises(Exception):
#             cs.kxtrct(
#                 "NAME:",
#                 "address: phone: name:".upper().split(),
#                 "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 "
#             )
# =============================================================================


def test_latcyl():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * cs.rpd(), 0.0])
    expected3 = np.array([1.0, 180.0 * cs.rpd(), 0.0])
    npt.assert_array_almost_equal(
        expected1, cs.latcyl(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(
        expected2, cs.latcyl(1.0, 90.0 * cs.rpd(), 0.0), decimal=7
    )
    npt.assert_array_almost_equal(
        expected3, cs.latcyl(1.0, 180.0 * cs.rpd(), 0.0), decimal=7
    )


def test_latrec():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([0.0, 1.0, 0.0])
    expected3 = np.array([-1.0, 0.0, 0.0])
    npt.assert_array_almost_equal(
        expected1, cs.latrec(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(
        expected2, cs.latrec(1.0, 90.0 * cs.rpd(), 0.0), decimal=7
    )
    npt.assert_array_almost_equal(
        expected3, cs.latrec(1.0, 180.0 * cs.rpd(), 0.0), decimal=7
    )


def test_latsph():
    expected1 = np.array([1.0, 90.0 * cs.rpd(), 0.0])
    expected2 = np.array([1.0, 90.0 * cs.rpd(), 90.0 * cs.rpd()])
    expected3 = np.array([1.0, 90.0 * cs.rpd(), 180.0 * cs.rpd()])
    npt.assert_array_almost_equal(
        expected1, cs.latsph(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(
        expected2, cs.latsph(1.0, 90.0 * cs.rpd(), 0.0), decimal=7
    )
    npt.assert_array_almost_equal(
        expected3, cs.latsph(1.0, 180.0 * cs.rpd(), 0.0), decimal=7
    )


def test_latsrf():
    cs.furnsh(ExtraKernels.phobosDsk)
    srfpts = cs.latsrf(
        "DSK/UNPRIORITIZED", "phobos", 0.0, "iau_phobos", [
            [0.0, 45.0], [60.0, 45.0]]
    )
    radii = [cs.recrad(x)[0] for x in srfpts]
    assert radii[0] > 9.77
    assert radii[1] > 9.51


def test_ldpool():
    ldpool_names = [
        "DELTET/DELTA_T_A",
        "DELTET/K",
        "DELTET/EB",
        "DELTET/M",
        "DELTET/DELTA_AT",
    ]
    ldpool_lens = [1, 1, 1, 2, 46]
    textbuf = [
        "DELTET/DELTA_T_A = 32.184",
        "DELTET/K = 1.657D-3",
        "DELTET/EB  = 1.671D-2",
        "DELTET/M = ( 6.239996 1.99096871D-7 )",
        "DELTET/DELTA_AT = ( 10, @1972-JAN-1",
        "                     11, @1972-JUL-1",
        "                     12, @1973-JAN-1",
        "                     13, @1974-JAN-1",
        "                     14, @1975-JAN-1",
        "                     15, @1976-JAN-1",
        "                     16, @1977-JAN-1",
        "                     17, @1978-JAN-1",
        "                     18, @1979-JAN-1",
        "                     19, @1980-JAN-1",
        "                     20, @1981-JUL-1",
        "                     21, @1982-JUL-1",
        "                     22, @1983-JUL-1",
        "                     23, @1985-JUL-1",
        "                     24, @1988-JAN-1",
        "                     25, @1990-JAN-1",
        "                     26, @1991-JAN-1",
        "                     27, @1992-JUL-1",
        "                     28, @1993-JUL-1",
        "                     29, @1994-JUL-1",
        "                     30, @1996-JAN-1",
        "                     31, @1997-JUL-1",
        "                     32, @1999-JAN-1 )",
    ]
    kernel = os.path.join(TEST_FILE_DIR, "ldpool_test.tls")
    cleanup_kernel(kernel)
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        for line in textbuf:
            kernelFile.write(line + "\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    cs.ldpool(kernel)
    for var, expectLen in zip(ldpool_names, ldpool_lens):
        n, vartype = cs.dtpool(var)
        assert expectLen == n
        assert vartype == "N"
    cleanup_kernel(kernel)


def test_lgresp():
    yvals = [-2.0, -8.0, 26.0, 148.0]
    a = cs.lgresp(-1.0, 2.0, yvals, 2.0)
    assert a == pytest.approx(1.0)


def test_lgrind():
    p, dp = cs.lgrind([-1.0, 0.0, 1.0, 3.0], [-2.0, -7.0, -8.0, 26.0], 2.0)
    assert p == pytest.approx(1.0)
    assert dp == pytest.approx(16.0)


def test_lgrint():
    xvals = [-1.0, 0.0, 1.0, 3.0]
    yvals = [-2.0, -7.0, -8.0, 26.0]
    a = cs.lgrint(xvals, yvals, 2.0)
    assert a == pytest.approx(1.0)


def test_limbpt():
    cs.furnsh(CoreKernels.spk)
    cs.furnsh(ExtraKernels.marsSpk)
    cs.furnsh(CoreKernels.pck)
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(ExtraKernels.phobosDsk)
    # set the time
    et = cs.str2et("1972 AUG 11 00:00:00")
    # call limpt
    npts, points, epochs, tangts = cs.limbpt(
        "TANGENT/DSK/UNPRIORITIZED",
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


def test_lmpool():
    lmpool_names = [
        "DELTET/DELTA_T_A",
        "DELTET/K",
        "DELTET/EB",
        "DELTET/M",
        "DELTET/DELTA_AT",
    ]
    lmpool_lens = [1, 1, 1, 2, 46]
    textbuf = [
        "DELTET/DELTA_T_A = 32.184",
        "DELTET/K = 1.657D-3",
        "DELTET/EB  = 1.671D-2",
        "DELTET/M = ( 6.239996 1.99096871D-7 )",
        "DELTET/DELTA_AT = ( 10, @1972-JAN-1",
        "                     11, @1972-JUL-1",
        "                     12, @1973-JAN-1",
        "                     13, @1974-JAN-1",
        "                     14, @1975-JAN-1",
        "                     15, @1976-JAN-1",
        "                     16, @1977-JAN-1",
        "                     17, @1978-JAN-1",
        "                     18, @1979-JAN-1",
        "                     19, @1980-JAN-1",
        "                     20, @1981-JUL-1",
        "                     21, @1982-JUL-1",
        "                     22, @1983-JUL-1",
        "                     23, @1985-JUL-1",
        "                     24, @1988-JAN-1",
        "                     25, @1990-JAN-1",
        "                     26, @1991-JAN-1",
        "                     27, @1992-JUL-1",
        "                     28, @1993-JUL-1",
        "                     29, @1994-JUL-1",
        "                     30, @1996-JAN-1",
        "                     31, @1997-JUL-1",
        "                     32, @1999-JAN-1 )",
    ]
    cs.lmpool(textbuf)
    for var, expectLen in zip(lmpool_names, lmpool_lens):
        n, vartype = cs.dtpool(var)
        assert expectLen == n
        assert vartype == "N"


def test_lparse():
    stringtest = "one two three four"
    items = cs.lparse(stringtest, " ")
    assert items == ("one", "two", "three", "four")


def test_lparsm():
    stringtest = "  A number of words   separated   by spaces   "
    # Test with nmax (20) not equal to lenout (23), to ensure that
    # their purposes have not been switched within cs.lparsm()
    items = cs.lparsm(stringtest, " ")
    assert items == ("A", "number", "of", "words", "separated", "by", "spaces")
    # Test without lenout
    items = cs.lparsm(stringtest, " ")
    assert items == ("A", "number", "of", "words", "separated", "by", "spaces")


def test_lspcn():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("21 march 2005")
    lon = cs.dpr() * cs.lspcn("EARTH", et, "NONE")
    npt.assert_almost_equal(lon, 0.48153755894179384)


def test_lstlec():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    assert cs.lstlec("NEWTON", array) == 4
    assert cs.lstlec("EINSTEIN", array) == 1
    assert cs.lstlec("GALILEO", array) == 3
    assert cs.lstlec("Galileo", array) == 3
    assert cs.lstlec("BETHE", array) == -1


def test_lstled():
    array = [-2.0, -2.0, 0.0, 1.0, 1.0, 11.0]
    assert cs.lstled(-3.0, array) == -1
    assert cs.lstled(-2.0, array) == 1
    assert cs.lstled(0.0, array) == 2
    assert cs.lstled(1.0, array) == 4
    assert cs.lstled(11.1, array) == 5


def test_lstlei():
    array = [-2, -2, 0, 1, 1, 11]
    assert cs.lstlei(-3, array) == -1
    assert cs.lstlei(-2, array) == 1
    assert cs.lstlei(0, array) == 2
    assert cs.lstlei(1, array) == 4
    assert cs.lstlei(12, array) == 5


def test_lstltc():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    assert cs.lstltc("NEWTON", array) == 3
    assert cs.lstltc("EINSTEIN", array) == 0
    assert cs.lstltc("GALILEO", array) == 2
    assert cs.lstltc("Galileo", array) == 3
    assert cs.lstltc("BETHE", array) == -1


def test_lstltd():
    array = [-2.0, -2.0, 0.0, 1.0, 1.0, 11.0]
    assert cs.lstltd(-3.0, array) == -1
    assert cs.lstltd(-2.0, array) == -1
    assert cs.lstltd(0.0, array) == 1
    assert cs.lstltd(1.0, array) == 2
    assert cs.lstltd(11.1, array) == 5


def test_lstlti():
    array = [-2, -2, 0, 1, 1, 11]
    assert cs.lstlti(-3, array) == -1
    assert cs.lstlti(-2, array) == -1
    assert cs.lstlti(0, array) == 1
    assert cs.lstlti(1, array) == 2
    assert cs.lstlti(12, array) == 5


def test_ltime():
    cs.furnsh(CoreKernels.testMetaKernel)
    OBS = 399
    TARGET = 5
    TIME_STR = "July 4, 2004"
    et = cs.str2et(TIME_STR)
    arrive, ltime = cs.ltime(et, OBS, "->", TARGET)
    arrive_utc = cs.et2utc(arrive, "C", 3)
    npt.assert_almost_equal(ltime, 2918.71705, decimal=4)
    assert arrive_utc == "2004 JUL 04 00:48:38.717"
    receive, rtime = cs.ltime(et, OBS, "<-", TARGET)
    receive_utc = cs.et2utc(receive, "C", 3)
    npt.assert_almost_equal(rtime, 2918.75247, decimal=4)
    assert receive_utc == "2004 JUL 03 23:11:21.248"


def test_lx4dec():
    assert cs.lx4dec("1%2%3", 0) == [0, 1]
    assert cs.lx4dec("1%2%3", 1) == [0, 0]
    assert cs.lx4dec("1%2%3", 2) == [2, 1]


def test_lx4num():
    assert cs.lx4num("1%2%3", 0) == [0, 1]
    assert cs.lx4num("1%2%3", 1) == [0, 0]
    assert cs.lx4num("1%2%3", 2) == [2, 1]
    assert cs.lx4num("1%2e1%3", 2) == [4, 3]


def test_lx4sgn():
    assert cs.lx4sgn("1%2%3", 0) == [0, 1]
    assert cs.lx4sgn("1%2%3", 1) == [0, 0]
    assert cs.lx4sgn("1%2%3", 2) == [2, 1]


def test_lx4uns():
    # not a very good test
    assert cs.lx4uns("test 10 end", 4) == [3, 0]


def test_lxqstr():
    assert cs.lxqstr('The "SPICE" system', '"', 4) == [10, 7]
    assert cs.lxqstr('The "SPICE" system', '"', 4) == [10, 7]
    assert cs.lxqstr('The "SPICE" system', '"', 0) == [-1, 0]
    assert cs.lxqstr('The "SPICE" system', "'", 4) == [3, 0]
    assert cs.lxqstr('The """SPICE"""" system', '"', 4) == [14, 11]
    assert cs.lxqstr("The &&&SPICE system", "&", 4) == [5, 2]
    assert cs.lxqstr("' '", "'", 0) == [2, 3]
    assert cs.lxqstr("''", "'", 0) == [1, 2]


def test_m2eul():
    ticam = [
        [0.49127379678135830, 0.50872620321864170, 0.70699908539882417],
        [-0.50872620321864193, -0.49127379678135802, 0.70699908539882428],
        [0.70699908539882406, -0.70699908539882439, 0.01745240643728360],
    ]
    kappa, ang2, ang1 = cs.m2eul(ticam, 3, 1, 3)
    alpha = ang1 + 1.5 * cs.pi()
    delta = cs.halfpi() - ang2
    expected = [315.000000, 1.000000, 45.000000]
    result = [cs.dpr() * alpha, cs.dpr() * delta, cs.dpr() * kappa]
    npt.assert_array_almost_equal(expected, result)


def test_m2q():
    r = cs.rotate(cs.halfpi(), 3)
    q = cs.m2q(r)
    expected = [np.sqrt(2) / 2.0, 0.0, 0.0, -np.sqrt(2) / 2.0]
    np.testing.assert_array_almost_equal(expected, q, decimal=6)


def test_matchi():
    string = "  ABCDEFGHIJKLMNOPQRSTUVWXYZ  "
    wstr = "*"
    wchr = "%"
    assert cs.matchi(string, "*A*", wstr, wchr)
    assert cs.matchi(string, "A%D*", wstr, wchr) is False
    assert cs.matchi(string, "A%C*", wstr, wchr)
    assert cs.matchi(string, "%A*", wstr, wchr) is False
    assert cs.matchi(string, "%%CD*Z", wstr, wchr)
    assert cs.matchi(string, "%%CD", wstr, wchr) is False
    assert cs.matchi(string, "A*MN*Y*Z", wstr, wchr)
    assert cs.matchi(string, "A*MN*Y*%Z", wstr, wchr) is False
    assert cs.matchi(string, "*BCD*Z*", wstr, wchr)
    assert cs.matchi(string, "*bdc*z*", wstr, wchr) is False
    assert cs.matchi(string, " *bcD*Z*", wstr, wchr)


def test_matchw():
    string = "  ABCDEFGHIJKLMNOPQRSTUVWXYZ  "
    wstr = "*"
    wchr = "%"
    assert cs.matchw(string, "*A*", wstr, wchr)
    assert cs.matchw(string, "A%D*", wstr, wchr) is False
    assert cs.matchw(string, "A%C*", wstr, wchr)
    assert cs.matchw(string, "%A*", wstr, wchr) is False
    assert cs.matchw(string, "%%CD*Z", wstr, wchr)
    assert cs.matchw(string, "%%CD", wstr, wchr) is False
    assert cs.matchw(string, "A*MN*Y*Z", wstr, wchr)
    assert cs.matchw(string, "A*MN*Y*%Z", wstr, wchr) is False
    assert cs.matchw(string, "*BCD*Z*", wstr, wchr)
    assert cs.matchw(string, "*bdc*z*", wstr, wchr) is False
    assert cs.matchw(string, " *BCD*Z*", wstr, wchr)


def test_mequ():
    m1 = np.identity(3)
    mout = cs.mequ(m1)
    assert np.array_equal(m1, mout)


def test_mequg():
    m1 = np.identity(2)
    mout = cs.mequg(m1)
    assert np.array_equal(m1, mout)


def test_mtxm():
    m1 = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    m2 = np.array([[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    mout = cs.mtxm(m1, m2)
    expected = np.array([[-3.0, 5.0, 7.0], [-3.0, 7.0, 8.0], [-3.0, 9.0, 9.0]])
    assert np.array_equal(mout, expected)


def test_mtxmg():
    m1 = np.array([[1.0, 2.0, 3.0, 0.0], [1.0, 1.0, 1.0, 1.0]])
    m2 = np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0]])
    mout = cs.mtxmg(m1, m2)
    expected = np.array(
        [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0], [0.0, 0.0, 0.0]]
    )
    assert np.array_equal(mout, expected)


def test_mtxv():
    m1 = np.array([[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    vin = np.array([5.0, 10.0, 15.0])
    mout = cs.mtxv(m1, vin)
    expected = np.array([-5.0, 15.0, 15.0])
    assert np.array_equal(mout, expected)


def test_mtxvg():
    m1 = np.array([[1.0, 2.0], [1.0, 3.0], [1.0, 4.0]])
    v2 = np.array([1.0, 2.0, 3.0])
    mout = cs.mtxvg(m1, v2)
    expected = np.array([6.0, 20.0])
    assert np.array_equal(mout, expected)


def test_mxm():
    m1 = [[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    m2 = [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, -1.0, 1.0]]
    mout = np.array(cs.mxm(m1, m2))
    m1 = np.array(m1)
    m2 = np.array(m2)
    mout2 = np.dot(m1, m2)
    assert np.array_equal(mout, mout2)


def test_mxmg():
    m1 = [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    m2 = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]]
    mout = np.array(cs.mxmg(m1, m2))
    m1 = np.array(m1)
    m2 = np.array(m2)
    mout2 = np.dot(m1, m2)
    assert np.array_equal(mout, mout2)


def test_mxmt():
    m1 = [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    mout = cs.mxmt(m1, m1)
    assert np.array_equal(mout, np.identity(3))


def test_mxmtg():
    m1 = np.array([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]])
    m2 = np.array([[1.0, 2.0, 0.0], [2.0, 1.0, 2.0],
                  [1.0, 2.0, 0.0], [2.0, 1.0, 2.0]])
    mout = cs.mxmtg(m1, m2)
    expected = np.array([[5.0, 10.0, 5.0, 10.0], [7.0, 10.0, 7.0, 10.0]])
    assert np.array_equal(mout, expected)


def test_mxv():
    m1 = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    vin = np.array([1.0, 2.0, 3.0])
    mout = cs.mxv(m1, vin)
    expected = np.array([2.0, -1.0, 3.0])
    assert np.array_equal(mout, expected)


def test_mxvg():
    m1 = np.array([[1.0, 1.0, 1.0], [2.0, 3.0, 4.0]])
    v2 = np.array([1.0, 2.0, 3.0])
    mout = cs.mxvg(m1, v2)
    expected = np.array([6.0, 20.0])
    assert np.array_equal(mout, expected)


def test_namfrm():
    assert cs.namfrm("J2000") == 1


def test_ncpos():
    string = "BOB, JOHN, TED, AND MARTIN    "
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert cs.ncpos(string, chars, 0) == 3
    assert cs.ncpos(string, chars, 4) == 4
    assert cs.ncpos(string, chars, 5) == 9
    assert cs.ncpos(string, chars, 10) == 10
    assert cs.ncpos(string, chars, 11) == 14
    assert cs.ncpos(string, chars, 15) == 15
    assert cs.ncpos(string, chars, 16) == 19
    assert cs.ncpos(string, chars, 20) == 26
    assert cs.ncpos(string, chars, 27) == 27
    assert cs.ncpos(string, chars, 28) == 28
    assert cs.ncpos(string, chars, 29) == 29
    assert cs.ncpos(string, chars, -12) == 3
    assert cs.ncpos(string, chars, -1) == 3
    assert cs.ncpos(string, chars, 30) == -1
    assert cs.ncpos(string, chars, 122) == -1


def test_ncposr():
    string = "BOB, JOHN, TED, AND MARTIN...."
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert cs.ncposr(string, chars, 29) == 29
    assert cs.ncposr(string, chars, 28) == 28
    assert cs.ncposr(string, chars, 27) == 27
    assert cs.ncposr(string, chars, 26) == 26
    assert cs.ncposr(string, chars, 25) == 19
    assert cs.ncposr(string, chars, 18) == 15
    assert cs.ncposr(string, chars, 14) == 14
    assert cs.ncposr(string, chars, 13) == 10
    assert cs.ncposr(string, chars, 9) == 9
    assert cs.ncposr(string, chars, 8) == 4
    assert cs.ncposr(string, chars, 3) == 3
    assert cs.ncposr(string, chars, 2) == -1
    assert cs.ncposr(string, chars, -1) == -1
    assert cs.ncposr(string, chars, -5) == -1
    assert cs.ncposr(string, chars, 30) == 29
    assert cs.ncposr(string, chars, 122) == 29


def test_nearpt():
    a, b, c = 1.0, 2.0, 3.0
    point = [3.5, 0.0, 0.0]
    pnear, alt = cs.nearpt(point, a, b, c)
    expected_pnear = [1.0, 0.0, 0.0]
    expected_alt = 2.5
    npt.assert_almost_equal(alt, expected_alt)
    npt.assert_array_almost_equal(pnear, expected_pnear)


def test_npedln():
    linept = [1.0e6, 2.0e6, 3.0e6]
    a, b, c = 7.0e5, 7.0e5, 6.0e5
    linedr = [-4.472091234e-1, -8.944182469e-1, -4.472091234e-3]
    pnear, dist = cs.npedln(a, b, c, linept, linedr)
    expected_pnear = [-1633.3111, -3266.6222, 599991.83]
    expected_dist = 2389967.9
    npt.assert_almost_equal(dist, expected_dist, decimal=1)
    npt.assert_array_almost_equal(expected_pnear, pnear, decimal=2)


def test_npelpt():
    center = [1.0, 2.0, 3.0]
    smajor = [3.0, 0.0, 0.0]
    sminor = [0.0, 2.0, 0.0]
    point = [-4.0, 2.0, 1.0]
    expected_pnear = [-2.0, 2.0, 3.0]
    expected_dist = 2.8284271
    ellipse = cs.cgv2el(center, smajor, sminor)
    pnear, dist = cs.npelpt(point, ellipse)
    npt.assert_almost_equal(dist, expected_dist)
    npt.assert_array_almost_equal(expected_pnear, pnear)


def test_nplnpt():
    linept = [1.0, 2.0, 3.0]
    linedr = [0.0, 1.0, 1.0]
    point = [-6.0, 9.0, 10.0]
    pnear, dist = cs.nplnpt(linept, linedr, point)
    expected_pnear = [1.0, 9.0, 10.0]
    expected_dist = 7.0
    assert dist == expected_dist
    npt.assert_array_almost_equal(expected_pnear, pnear)


# Test changed
def test_nvc2pl():
    normal = [1.0, 1.0, 1.0]
    constant = 23.0
    expected_constant = 13.279056
    expected_normal = [0.57735027, 0.57735027, 0.57735027]
    plane = cs.nvc2pl(normal, constant)
    npt.assert_array_almost_equal(plane[0:3], expected_normal)
    npt.assert_almost_equal(plane[-1], expected_constant, decimal=6)


def test_nvp2pl():
    normal = [1.0, 1.0, 1.0]
    point = [1.0, 4.0, 9.0]
    expected_constant = 8.0829038
    expected_normal = [0.57735027, 0.57735027, 0.57735027]
    plane = cs.nvp2pl(normal, point)
    npt.assert_array_almost_equal(plane[0:3], expected_normal)
    npt.assert_almost_equal(plane[-1], expected_constant, decimal=6)


def test_occult():
    # load kernels
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    cs.furnsh(ExtraKernels.earthTopoTf)
    # start test
    # Mercury transited the Sun w.r.t. Earth-based observer ca. 2006-11-08 for about 5h
    # cf. https://science.nasa.gov/science-news/science-at-nasa/2006/20oct_transitofmercury
    # Mercury was occulted by the sun about six months later
    et_sun_transited_by_mercury = cs.str2et("2006-11-08T22:00")
    occult_code_one = cs.occult(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et_sun_transited_by_mercury,
    )
    # Mercury is in front of the Sun as seen by observer (DSS-13)
    assert occult_code_one == 2  # cs_OCCULT_ANNLR2
    et_sun_mercury_both_visible = cs.str2et("2006-11-09T02:00")
    occult_code_two = cs.occult(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et_sun_mercury_both_visible,
    )
    # Both Mercury and the Sun are visible to observer (DSS-13)
    assert occult_code_two == 0  # cs_OCCULT_NOOCC
    et_sun_totally_occulted_mercury = cs.str2et("2007-05-03T05:00")
    occult_code_three = cs.occult(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et_sun_totally_occulted_mercury,
    )
    # The Sun is in front of Mercury as seen by observer (DSS-13)
    assert occult_code_three == -3  # cs_OCCULT_TOTAL1
    # cleanup


def test_orderc():
    inarray = ["a", "abc", "ab"]
    expected_order = [0, 2, 1]
    order = cs.orderc(inarray)
    npt.assert_array_almost_equal(expected_order, order)
    # Using ndim
    order = cs.orderc(inarray)
    npt.assert_array_almost_equal(expected_order, order)


def test_orderd():
    inarray = [0.0, 2.0, 1.0]
    expected_order = [0, 2, 1]
    order = cs.orderd(inarray)
    npt.assert_array_almost_equal(expected_order, order)
    # Using ndim
    order = cs.orderd(inarray)
    npt.assert_array_almost_equal(expected_order, order)


def test_orderi():
    inarray = [0, 2, 1]
    expected_order = [0, 2, 1]
    order = cs.orderi(inarray)
    npt.assert_array_almost_equal(expected_order, order)
    # Using ndim
    order = cs.orderi(inarray)
    npt.assert_array_almost_equal(expected_order, order)


def test_oscelt():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Dec 25, 2007")
    state, ltime = cs.spkezr("Moon", et, "J2000", "LT+S", "EARTH")
    mass_earth = cs.bodvrd("EARTH", "GM")
    elts = cs.oscelt(state, et, mass_earth[0])
    expected = [
        3.65914105273643566761e05,
        4.23931145731340453494e05,
        4.87177926278510253777e-01,
        6.18584206992959551030e00,
        1.88544634402406319218e00,
        1.86769787246217056236e04,
        2.51812865183709204197e08,
        1.00000000000000000000e00,
    ]
    npt.assert_array_almost_equal(elts, expected, decimal=4)


def test_oscltx():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Dec 25, 2007")
    state, ltime = cs.spkezr("Moon", et, "J2000", "LT+S", "EARTH")
    mass_earth = cs.bodvrd("EARTH", "GM")
    elts = cs.oscltx(state, et, mass_earth[0])
    expected = [
        3.65914105273643566761e05,
        4.23931145731340453494e05,
        4.87177926278510253777e-01,
        6.18584206992959551030e00,
        1.88544634402406319218e00,
        1.86769787246217056236e04,
        2.51812865183709204197e08,
        1.00000000000000000000e00,
        4.40283687897870881778e-02,
        -8.63147169311087925081e-01,
        0.00000000000000000000e00,
    ]
    npt.assert_array_almost_equal(elts, expected, decimal=4)


# =============================================================================
# nextwd
# nthwd
# ==============================================================
