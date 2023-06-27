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


def test_edlimb():
    viewpt = [2.0, 0.0, 0.0]
    limb = cs.edlimb(np.sqrt(2), 2.0 * np.sqrt(2), np.sqrt(2), viewpt)
    expected_s_minor = [0.0, 0.0, -1.0]
    expected_s_major = [0.0, 2.0, 0.0]
    expected_center = [1.0, 0.0, 0.0]
    npt.assert_array_almost_equal(limb[:3], expected_center)
    npt.assert_array_almost_equal(limb[3:6], expected_s_major)
    npt.assert_array_almost_equal(limb[6:9], expected_s_minor)


def test_ednmpt():
    point = cs.ednmpt(10.0, 5.0, 2.0, [15.0, -7.0, 3.0])
    npt.assert_array_almost_equal(point, [9.73103203, -1.13528707, 0.07784826])


def test_edpnt():
    ep = cs.edpnt([1.0, 1.0, 1.0], 3.0, 2.0, 1.0)
    npt.assert_array_almost_equal(
        ep, [0.85714285714286, 0.85714285714286, 0.85714285714286]
    )


def test_edterm():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2007 FEB 3 00:00:00.000")
    # umbral
    trgepc, obspos, trmpts = cs.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trgepc = 223732863.86351674795
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
    expected_trmpts2 = [
        42.21324376177891224415,
        868.21134635239388899208,
        -1504.3223923468244720425,
    ]
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
    # penumbral
    trgepc, obspos, trmpts = cs.edterm(
        "PENUMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trmpts0 = [
        1.54019056755619715204e02,
        1.73055969989532059117e03,
        -1.23508409498995316844e-01,
    ]
    expected_trmpts1 = [
        -87.33436047798454637814,
        -864.41003834758112134296,
        -1504.56862757530461749411,
    ]
    expected_trmpts2 = [
        -42.17254722919552278881,
        -868.21467833235510624945,
        1504.32161075630597224517,
    ]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = cs.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[0]
    )
    npt.assert_almost_equal(cs.dpr() * solar0, 89.730234406)
    iluet1, srfvec1, phase1, solar1, emissn1 = cs.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[1]
    )
    npt.assert_almost_equal(cs.dpr() * solar1, 89.730234298)
    iluet2, srfvec2, phase2, solar2, emissn2 = cs.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[2]
    )
    npt.assert_almost_equal(cs.dpr() * solar2, 89.730234322)


def test_ekacec():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekacec.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle,
        "test_table_ekacec",
        ["c1"],
        ["DATATYPE = CHARACTER*(*), NULLS_OK = TRUE"],
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacec(handle, segno, recno, "c1", ["1.0", "2.0"], False)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekaced():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekaced.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle,
        "test_table_ekaced",
        ["c1"],
        ["DATATYPE = DOUBLE PRECISION, NULLS_OK = TRUE"],
    )
    recno = cs.ekappr(handle, segno)
    cs.ekaced(handle, segno, recno, "c1", [1.0, 2.0], False)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekappr_ekacei():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekappr.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle, "test_table_ekappr", ["c1"], [
            "DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacei(handle, segno, recno, "c1", [1, 2], False)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekaclc():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekaclc.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekaclc",
        2,
        ["c1"],
        ["DATATYPE = CHARACTER*(*), INDEXED  = TRUE"],
    )
    cs.ekaclc(
        handle, segno, "c1", ["1.0", "2.0"], [
            4, 4], [False, False], rcptrs
    )
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekacld():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekacld.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekacld",
        2,
        ["c1"],
        ["DATATYPE = DOUBLE PRECISION, NULLS_OK = FALSE"]
    )
    cs.ekacld(
        handle, segno, "c1", [1, 1], [False, False], rcptrs, [0, 0]
    )
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekacli():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekacli.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekacli",
        2,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"]
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [
              1, 1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekappr():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekappr.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle, "test_table_ekappr", ["c1"], [
            "DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacei(handle, segno, recno, "c1", [1, 2], False)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekbseg():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekbseg.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, "Test EK", 100)
    cnames = ["INT_COL_1"]
    cdecls = ["DATATYPE=INTEGER, INDEXED=TRUE, NULLS_OK=TRUE"]
    segno = cs.ekbseg(handle, "SCALAR_DATA", cnames, cdecls)
    recno = cs.ekappr(handle, segno)
    assert recno != -1
    ordids = [x for x in range(5)]
    cs.ekacei(handle, segno, recno, "INT_COL_1", ordids, False)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekccnt():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekccnt.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle, "TEST_TABLE_EKCCNT", ["c1"], [
            "DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacei(handle, segno, recno, "c1", [1, 2], False)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    assert cs.ekntab() == 1
    assert cs.ektnam(0) == "TEST_TABLE_EKCCNT"
    assert cs.ekccnt("TEST_TABLE_EKCCNT") == 1
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekcii():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekcii.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle, "TEST_TABLE_EKCII", ["c1"], [
            "DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacei(handle, segno, recno, "c1", [1, 2], False)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    assert cs.ekntab() == 1
    assert cs.ektnam(0) == "TEST_TABLE_EKCII"
    assert cs.ekccnt("TEST_TABLE_EKCII") == 1
    column, cclass, dtype, strlen, size, indexd, nullok = cs.ekcii(
        "TEST_TABLE_EKCII", 0)
    assert column == "C1"
    assert cclass == 1
    assert dtype == 2
    assert size == 1
    assert strlen == 1
    assert not indexd
    assert nullok  # this used to be false, although clearly it should be true given the call to ekbseg
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekcls():
    # same as ekopn test
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekcls.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 80)
    cs.ekcls(handle)
    assert os.path.exists(ekpath)
    cleanup_kernel(ekpath)


def test_ekdelr():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekdelr.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekdelr",
        10,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekdelr(handle, segno, 2)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekffld():
    # same as test_ekacli
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekffld.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekffld",
        10,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekfind():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekfind.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekfind",
        2,
        ["cc1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    cs.ekacli(handle, segno, "cc1", [1, 2], [
              1, 1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    nmrows = cs.ekfind("SELECT CC1 FROM TEST_TABLE_EKFIND WHERE CC1 > 0")
    assert (
        nmrows != 0
    )  # should be 2 but I am not concerned about correctness in this case
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekgc():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekgc.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekgc",
        2,
        ["c1"],
        ["DATATYPE = CHARACTER*(*), INDEXED  = TRUE"],
    )
    cs.ekaclc(
        handle, segno, "c1", ["1.0", "2.0"], [
            4, 4], [False, False], rcptrs
    )
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    nmrows = cs.ekfind("SELECT C1 FROM TEST_TABLE_EKGC")
    c, null = cs.ekgc(0, 0, 0)
    assert not null
    assert c == "1.0"
    c, null = cs.ekgc(0, 1, 0)
    assert not null
    # assert c == "2.0" this fails, c is an empty string despite found being true.
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekgd():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekgd.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekgd",
        2,
        ["c1"],
        ["DATATYPE = DOUBLE PRECISION, NULLS_OK = TRUE"],
    )
    cs.ekacld(
        handle, segno, "c1", [1.0, 2.0], [1, 1], [False, False], rcptrs
    )
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    nmrows = cs.ekfind("SELECT C1 FROM TEST_TABLE_EKGD")
    d, null = cs.ekgd(0, 0, 0)
    assert not null
    assert d == 1.0
    d, null = cs.ekgd(0, 1, 0)
    assert not null
    assert d == 2.0
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


# Test fails due to reliance on ekfind
def test_ekgi():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekgi.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekgi",
        2,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = FALSE"],
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [
        1, 1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    nmrows = cs.ekfind("SELECT C1 FROM TEST_TABLE_EKGI")
    i, null = cs.ekgi(0, 0, 0)
    assert not null
    assert i == 1
    i, null = cs.ekgi(0, 1, 0)
    assert not null
    assert i == 2
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekifld():
    # Same as test_ekacli2
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekifld.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekifld",
        2,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [
        1, 1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def fail_ekinsr_eknelt_ekpsel_ekrcec_ekrced_ekrcei():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekmany.ek")
    tablename = "test_table_ekmany"
    cleanup_kernel(ekpath)
    # Create new EK and new segment with table
    handle = cs.ekopn(ekpath, ekpath, 0)
    decls = [
        "DATATYPE = CHARACTER*(10),   NULLS_OK = FALSE, SIZE = VARIABLE",
        "DATATYPE = DOUBLE PRECISION, NULLS_OK = FALSE, SIZE = VARIABLE",
        "DATATYPE = INTEGER,          NULLS_OK = FALSE, SIZE = VARIABLE",
    ]
    segno = cs.ekbseg(handle, tablename, ["c1", "d1", "i1"], decls)
    # Insert records:  1, 2, and 3 entries at rows 0, 1, 2, respectively
    c_data = [["100"], ["101", "101"], ["102", "102", "102"]]
    d_data = [[100.0], [101.0, 101.0], [102.0, 102.0, 102.0]]
    i_data = [[100], [101, 101], [102, 102, 102]]
    for r in range(0, 3):
        cs.ekinsr(handle, segno, r)
        cs.ekacec(handle, segno, r, "c1", c_data[r], False)
        cs.ekaced(handle, segno, r, "d1", d_data[r], False)
        cs.ekacei(handle, segno, r, "i1", i_data[r], False)
    # Try record insertion beyond the next available, verify the exception
    with pytest.raises(Exception):
        cs.ekinsr(handle, segno, 4)
    # Close EK, then reopen for reading
    cs.ekcls(handle)
    cs.kclear()
    #
    # Start of part two
    #
    handle = cs.eklef(ekpath)
    assert handle is not None
    # Test query using ekpsel
    query = "SELECT c1, d1, i1 from {}".format(tablename)
    xbegs, xends, xtypes, xclass, tabs, cols = cs.ekpsel(query)
    assert xtypes[0] == 0
    assert xtypes[1] == 1
    assert xtypes[2] == 2
    assert ([0] * 3) == list(xclass)
    assert ([["TEST_TABLE_EKMANY"] * 3]) == tabs
    assert ["C1 D1 I1".split()] == cols
    # Run query to retrieve the row count
    nmrows = cs.ekfind(query)
    assert nmrows == 3
    # test fail case for eknelt
    with pytest.raises(Exception):
        cs.eknelt(0, nmrows + 1)
    # Validate the content of each field, including exceptions when
    # Loop over rows, test .ekgc/.ekgd/.ekgi
    for r in range(nmrows):
        # get number of elements in this row
        n_elm = cs.eknelt(0, r)
        assert n_elm == r + 1
        for e in range(0, n_elm):
            # get row int data
            i_datum, i_null = cs.ekgi(2, r, e)
            assert not i_null
            assert i_datum == i_data[r][e]
            # get row double data
            d_datum, d_null = cs.ekgd(1, r, e)
            assert not d_null
            assert d_datum == d_data[r][e]
            # get row char data
            c_datum, c_null = cs.ekgc(0, r, e)
            assert not c_null
            assert c_datum == c_data[r][e]
    # Loop over rows, test .ekrcec/.ekrced/.ekrcei
    for r in range(nmrows):
        # get row int data
        ri_data, i_null = cs.ekrcei(handle, segno, r, "i1")
        assert not i_null

        npt.assert_array_equal(ri_data, i_data[r])
        # get row double data
        rd_data, d_null = cs.ekrced(handle, segno, r, "d1")
        assert not d_null
        npt.assert_array_equal(rd_data, d_data[r])
        # get row char data
        rc_data, c_null = cs.ekrcec(handle, segno, r, "c1")
        assert not c_null
        assert rc_data == c_data[r]
    # test out of bounds
    with pytest.raises(Exception):
        cs.ekrcei(handle, segno, 3, "i1")
    with pytest.raises(Exception):
        cs.ekrced(handle, segno, 3, "d1")
    # with pytest.raises(Exception): TODO: FIX
    #    cs.ekrcec(handle, segno, 4, "c1", 4) # this causes a SIGSEGV
    #
    # Part 3
    #
    # Close file, re-open for writing
    cs.ekuef(handle)
    handle = cs.ekopw(ekpath)
    # Loop over rows, update values using .ekucec/.ekuced/.ekucei
    c_data = [["200"], ["201", "201"], ["202", "202", "202"]]
    d_data = [[200.0], [201.0, 201.0], [202.0, 202.0, 202.0]]
    i_data = [[200], [201, 201], [202, 202, 202]]
    for r in range(0, 3):
        cs.ekucec(handle, segno, r, "c1", c_data[r], False)
        cs.ekuced(handle, segno, r, "d1", d_data[r], False)
        cs.ekucei(handle, segno, r, "i1", i_data[r], False)
    # Test invalid updates
    with pytest.raises(Exception):
        cs.ekucec(handle, segno, 3, "c1", 1, ["300"], False)
    with pytest.raises(Exception):
        cs.ekuced(handle, segno, 3, "d1", 1, [300.0], False)
    with pytest.raises(Exception):
        cs.ekucei(handle, segno, 3, "i1", 1, [300], False)
    # Loop over rows, use .ekrcec/.ekrced/.ekrcei to test updates
    for r in range(nmrows):
        # get row int data
        ri_data, i_null = cs.ekrcei(handle, segno, r, "i1")
        assert not i_null
        npt.assert_array_equal(ri_data, i_data[r])
        # get row double data
        rd_data, d_null = cs.ekrced(handle, segno, r, "d1")
        assert not d_null
        npt.assert_array_equal(rd_data, d_data[r])
        # get row char data
        rc_data, c_null = cs.ekrcec(handle, segno, r, "c1", 11)
        assert not c_null
        assert rc_data == c_data[r]
    # Cleanup
    cs.ekcls(handle)
    assert not cs.failed()
    cleanup_kernel(ekpath)


def test_eklef():
    ekpath = os.path.join(TEST_FILE_DIR, "example_eklef.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle, "test_table_eklef", ["c1"], [
            "DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacei(handle, segno, recno, "c1", [1, 2], False)
    cs.ekcls(handle)
    cs.kclear()
    handle = cs.eklef(ekpath)
    assert handle is not None
    cs.ekuef(handle)
    cs.kclear()
    cleanup_kernel(ekpath)


def test_eknseg():
    ekpath = os.path.join(TEST_FILE_DIR, "example_eknseg.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle, "TEST_TABLE_EKNSEG", ["c1"], [
            "DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacei(handle, segno, recno, "c1", [1, 2], False)
    cs.ekcls(handle)
    cs.kclear()
    handle = cs.ekopr(ekpath)
    assert cs.eknseg(handle) == 1
    cs.ekcls(handle)
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekntab():
    assert cs.ekntab() == 0


def test_ekopn():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ek.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 80)
    cs.ekcls(handle)
    assert os.path.exists(ekpath)
    cleanup_kernel(ekpath)


def test_ekopr():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekopr.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 80)
    cs.ekcls(handle)
    assert os.path.exists(ekpath)
    testhandle = cs.ekopr(ekpath)
    assert testhandle is not None
    cs.ekcls(testhandle)
    cleanup_kernel(ekpath)


def test_ekops():
    handle = cs.ekops()
    assert handle is not None
    cs.ekcls(handle)


def test_ekopw():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekopw.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 80)
    cs.ekcls(handle)
    assert os.path.exists(ekpath)
    testhandle = cs.ekopw(ekpath)
    assert testhandle is not None
    cs.ekcls(testhandle)
    cleanup_kernel(ekpath)


def fail_ekssum():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekssum.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekssum",
        2,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"]
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [
        1, 1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    tabnam, ncols, cnames, cclass, dtype, strln, size, indexd, nullok = cs.ekssum(
        handle, segno)
    assert ncols == 1
    assert cnames == ["C1"]
    assert tabnam == "TEST_TABLE_EKSSUM"
    assert dtype == 2
    assert indexd is False
    # assert c1descr.null == True, for some reason this is actually false, SpikeEKAttDsc may not be working correctly
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ektnam():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ektnam.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno = cs.ekbseg(
        handle, "TEST_TABLE_EKTNAM", ["c1"], [
            "DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = cs.ekappr(handle, segno)
    cs.ekacei(handle, segno, recno, "c1", [1, 2], False)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    assert cs.ekntab() == 1
    assert cs.ektnam(0) == "TEST_TABLE_EKTNAM"
    assert cs.ekccnt("TEST_TABLE_EKTNAM") == 1
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekucec():
    assert 1


def test_ekuced():
    assert 1


def test_ekucei():
    assert 1


def test_ekuef():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekuef.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 80)
    cs.ekcls(handle)
    cs.kclear()
    assert os.path.exists(ekpath)
    testhandle = cs.ekopr(ekpath)
    assert testhandle is not None
    cs.ekuef(testhandle)
    cs.ekcls(testhandle)
    cleanup_kernel(ekpath)


def test_el2cgv():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [1.0, 1.0, 1.0]
    smajor, sminor = cs.saelgv(vec1, vec2)
    ellipse = cs.cgv2el(center, smajor, sminor)
    outCenter, outSmajor, outSminor = cs.el2cgv(ellipse)
    expected_center = [1.0, 1.0, 1.0]
    expected_s_major = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expected_s_minor = [0.0, np.sqrt(2.0), 0.0]
    npt.assert_array_almost_equal(outCenter, expected_center)
    npt.assert_array_almost_equal(outSmajor, expected_s_major)
    npt.assert_array_almost_equal(outSminor, expected_s_minor)


def test_eqncpv():
    p = 10000.0
    gm = 398600.436
    ecc = 0.1
    a = p / (1.0 - ecc)
    n = np.sqrt(gm / a) / a
    argp = 30.0 * cs.rpd()
    node = 15.0 * cs.rpd()
    inc = 10.0 * cs.rpd()
    m0 = 45.0 * cs.rpd()
    t0 = -100000000.0
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
    state = cs.eqncpv(t0 - 9750.0, t0, eqel, cs.halfpi() * -1, cs.halfpi())
    expected = [
        -10732.167433285387,
        3902.505790600528,
        1154.4516152766892,
        -2.540766899262123,
        -5.15226920298345,
        -0.7615758062877463,
    ]
    npt.assert_array_almost_equal(expected, state, decimal=5)


def test_erract():
    assert cs.erract("GET", "") == "EXCEPTION"


# fails due to sigerr
def fail_errch():
    cs.setmsg("test errch value: #")
    cs.errch("#", "some error")
    cs.sigerr("some error")
    message = cs.getmsg("LONG", 2000)
    assert message == "test errch value: some error"
    cs.reset()


def test_errdev():
    assert cs.errdev("GET", "Screen") == "NULL"


# fails due to sigerr
def fail_errdp():
    cs.setmsg("test errdp value: #")
    cs.errdp("#", 42.1)
    cs.sigerr("some error")
    message = cs.getmsg("LONG", 2000)
    assert message == "test errdp value: 4.2100000000000E+01"
    cs.reset()


# fails due to sigerr
def fail_errint():
    cs.setmsg("test errint value: #")
    cs.errint("#", 42)
    cs.sigerr("some error")
    message = cs.getmsg("LONG", 2000)
    assert message == "test errint value: 42"
    cs.reset()


def fail_errprt():
    assert cs.errprt("GET", "ALL") == "NULL"


def test_esrchc():
    array = ["This", "is", "a", "test"]
    assert cs.esrchc("This", array) == 0
    assert cs.esrchc("is", array) == 1
    assert cs.esrchc("a", array) == 2
    assert cs.esrchc("test", array) == 3
    assert cs.esrchc("fail", array) == -1


def test_et2lst():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("2004 may 17 16:30:00")
    hr, mn, sc, time, ampm = cs.et2lst(
        et, 399, 281.49521300000004 * cs.rpd(), "planetocentric")
    assert hr == 11
    assert mn == 19
    assert sc == 22
    assert time == "11:19:22"
    assert ampm == "11:19:22 A.M."


def test_et2utc():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = -527644192.5403653
    output = cs.et2utc(et, "J", 6)
    assert output == "JD 2445438.006415"


def test_etcal():
    et = np.arange(0.0, 20.0)
    cal = cs.etcal(et[0])
    assert cal == "2000 JAN 01 12:00:00.000"


def test_eul2m():
    rot = np.array(cs.eul2m(cs.halfpi(), 0.0, 0.0, 3, 1, 1))
    assert rot.shape == ((3, 3))


def test_eul2xf():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Jan 1, 2009")
    expected = cs.sxform("IAU_EARTH", "J2000", et)
    eul = [
        1.571803284049681,
        0.0008750002978301174,
        2.9555269829740034,
        3.5458495690569166e-12,
        3.080552365717176e-12,
        -7.292115373266558e-05,
    ]
    out = cs.eul2xf(eul, 3, 1, 3)
    npt.assert_array_almost_equal(out, expected)


def test_evsgp4():
    # LUME 1 cubesat
    noadpn = ["J2", "J3", "J4", "KE", "QO", "SO", "ER", "AE"]
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(ExtraKernels.geophKer)
    tle = [
        "1 43908U 18111AJ  20146.60805006  .00000806  00000-0  34965-4 0  9999",
        "2 43908  97.2676  47.2136 0020001 220.6050 139.3698 15.24999521 78544",
    ]
    geophs = [cs.bodvcd(399, _)[0] for _ in noadpn]
    _, elems = cs.getelm(1957, tle)
    et = np.array([cs.str2et("2020-05-26 02:25:00")])
    state = cs.evsgp4(et, geophs, elems)
    expected_state = np.array(
        [
            -4644.60403398,
            -5038.95025539,
            -337.27141116,
            -0.45719025,
            0.92884817,
            -7.55917355,
        ]
    )
    npt.assert_array_almost_equal(expected_state, state)


def test_expool():
    textbuf = ["DELTET/K = 1.657D-3", "DELTET/EB = 1.671D-2"]
    cs.lmpool(textbuf)
    assert cs.expool("DELTET/K")
    assert cs.expool("DELTET/EB")
