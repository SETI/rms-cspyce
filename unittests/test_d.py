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


def test_dafac():
    # Create new DAF using CKOPN
    dafpath = os.path.join(TEST_FILE_DIR, "ex_dafac.bc")
    cleanup_kernel(dafpath)
    # Open CK to get new DAF because DAFONW (Create DAF) is not available to CSPICE/spiceypy
    handle = cs.ckopn(dafpath, "TEST_ex_dafac", 140)
    assert handle is not None
    # Write some comments
    cmnts = ["a", "bc", "def", "ghij"]
    cs.dafac(handle, cmnts)
    # Use DAFCLS because CKCLS requires segments to be written before closing
    cs.dafcls(handle)
    assert not cs.failed()
    cs.kclear()
    cs.reset()
    # Ensure all those DAF comments now exist in the new DAF
    handle = cs.dafopr(dafpath)
    assert handle is not None
    # Get up to 20 comments ...
    cmntsOut = cs.dafec(handle)
    # ...  nOut will have actual number of comments
    assert len(cmntsOut) == 4
    assert cmntsOut[:4] == cmnts
    cs.dafcls(handle)
    assert not cs.failed()
    cs.kclear()
    cs.reset()
    # Once more ...
    handle = cs.dafopr(dafpath)
    assert handle is not None
    # ... to get fewer than the total number of comments
    cmntsOut = cs.dafec(handle)
    cs.dafcls(handle)
    assert not cs.failed()
    cs.reset()
    cleanup_kernel(dafpath)


def test_dafbbs():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbbs(handle)
    found = cs.daffpa()
    assert found
    cs.dafcls(handle)


def test_dafbfs():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    cs.dafcls(handle)


def test_dafcls():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    cs.dafcls(handle)


def test_dafcs():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbbs(handle)
    cs.dafcs(handle)
    found = cs.daffpa()
    assert found
    cs.dafcls(handle)


def test_dafdc():
    dafpath = os.path.join(TEST_FILE_DIR, "ex_dafdc.bc")
    cleanup_kernel(dafpath)
    # Open CK to get new DAF because DAFONW (Create DAF) is not available to CSPICE/spiceypy
    handle = cs.ckopn(dafpath, "TEST_ex_dafdc", 140)
    assert handle is not None
    # Write some comments
    cmnts = ["a", "bc", "def", "ghij"]
    cs.dafac(handle, cmnts)
    # Use DAFCLS because CKCLS requires segments to be written before closing
    cs.dafcls(handle)
    assert not cs.failed()
    cs.kclear()
    cs.reset()
    # Open the DAF for reading
    handle = cs.dafopr(dafpath)
    assert handle is not None
    cmntsOut = cs.dafec(handle)
    # Confirm that the number of comments is greater than zero
    cs.dafcls(handle)
    assert not cs.failed()
    cs.kclear()
    cs.reset()
    # Delete the comments
    handle = cs.dafopw(dafpath)
    assert handle is not None
    cs.dafdc(handle)
    cs.dafcls(handle)
    assert not cs.failed()
    cs.kclear()
    cs.reset()
    # Confirm there are no more comments
    handle = cs.dafopr(dafpath)
    assert handle is not None
    cmntsOut = cs.dafec(handle)
    assert len(cmntsOut) == 0
    cs.dafcls(handle)
    assert not cs.failed()
    cs.reset()
    cs.kclear()
    cleanup_kernel(dafpath)


def test_dafec():
    handle = cs.dafopr(CoreKernels.spk)
    buffer = cs.dafec(handle)
    assert buffer[:13] == [
        "; de405s.bsp LOG FILE",
        ";",
        "; Created 1997-12-19/18:07:31.00.",
        ";",
        "; BEGIN NIOSPK COMMANDS",
        "",
        "LEAPSECONDS_FILE    = /kernels/gen/lsk/naif0006.tls",
        "SPK_FILE            = de405s.bsp",
        "  SOURCE_NIO_FILE   = /usr2/nio/gen/de405.nio",
        "    BODIES          = 1 2 3 4 5 6 7 8 9 10 301 399 199 299 499",
        "    BEGIN_TIME      = CAL-ET 1997 JAN 01 00:01:02.183",
        "    END_TIME        = CAL-ET 2010 JAN 02 00:01:03.183",
        "",
    ]
    cs.dafcls(handle)


def test_daffna():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    cs.dafcls(handle)


def test_daffpa():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbbs(handle)
    found = cs.daffpa()
    assert found
    cs.dafcls(handle)


def test_dafgda():
    # not a very good test...
    handle = cs.dafopr(CoreKernels.spk)
    elements = cs.dafgda(handle, 20, 20)
    npt.assert_array_almost_equal(elements, [0.0])
    cs.dafcls(handle)


def test_dafgh():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbbs(handle)
    cs.dafcs(handle)
    searchHandle = cs.dafgh()
    assert searchHandle == handle
    cs.dafcls(handle)


def test_dafgn():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    out = cs.dafgs()
    npt.assert_array_almost_equal(
        out[:2], [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    outname = cs.dafgn()
    assert outname == "DE-405"
    cs.dafcls(handle)


# Fails
def test_dafgs():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    out = cs.dafgs()
    npt.assert_array_almost_equal(
        out[:2], [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    cs.dafcls(handle)


# Fails due to dafgsr()
def test_dafgsr():
    cs.reset()
    # Open DAF
    # N.B. The SPK used must use the LTL-IEEE double byte-ordering and format
    # This should be de405s.bsp from the test kernel set
    handle = cs.dafopr(CoreKernels.spk)
    # get ND, NI (N.B. for SPKs, ND=2 and NI=6),
    # and first, last and free record numbers
    nd, ni, ifname, fward, bward, free = cs.dafrfr(handle)
    assert nd == 2 and ni == 6
    # Calculate Single Summary size
    ss = nd + ((ni + 1) >> 1)
    # Loop over Summary records
    while fward > 0:
        iRecno = fward
        # Get first three words at summary record (DAF record iRecno)
        # * drec(1) NEXT forward pointer to next summary record
        # * drec(2) PREV backward pointer (not used here)
        # * drec(3) NSUM Number of single summaries in this DAF record
        fward, bward, nSS = drec = map(int, cs.dafgsr(handle, iRecno, 1, 3))
        # There is only one summary record in de405s.bsp
        assert iRecno == 7 and fward == 0 and bward == 0 and nSS == 15
        # Set index to first word of first summary
        firstWord = 4
        # Set DAF record before daf421.bsp next summary record's first record (641)
        lastIEndWord = 1024
        for iSS in range(1, nSS + 1):
            # Get packed summary
            drec = cs.dafgsr(handle, iRecno, firstWord, firstWord + ss - 1)
            # Unpack summary
            dc, ic = cs.dafus(drec, nd, ni)
            iBody, iCenter, iFrame, iSPKtype, iStartWord, iEndWord = ic
            # SPK de405s.bsp ephemerides run from [1997 JAN 01 00:01:02.183 (TDB)] to [2010 JAN 02 00:01:03.183 (TDB)]
            npt.assert_array_almost_equal(
                dc, [-9.46511378160646408796e07, 3.15662463183953464031e08]
            )
            # Solar System body barycenters (IDs 1-10) centers are the Solar System Barycenter (ID=0)
            # All other bodies' centers (e.g. 301; Moon) are their systems barycenter (e.g. 3 Earth-Moon Barycenter)
            assert (iBody // 100) == iCenter
            # All de405s.bsp ephemerides are in the J2000 frame (ID 1), use Type 2 SPK records,
            # and start after the last record for the previous ephemeris
            assert iFrame == 1 and iSPKtype == 2 and (
                lastIEndWord + 1) == iStartWord
            # Set up for next pa through loop
            firstWord += ss
            lastIEndWord = iEndWord
        # There is only one summary record in de405s.bsp
        assert fward == 0
    # Cleanup
    cs.dafcls(handle)
    cs.reset()


def test_dafhsf():
    handle = cs.dafopr(CoreKernels.spk)
    nd, ni = cs.dafhsf(handle)
    cs.dafcls(handle)
    assert nd > 0
    assert ni > 0


def test_dafopr():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    cs.dafcls(handle)
    cs.kclear()


def test_dafopw():
    handle = cs.dafopw(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    cs.dafcls(handle)


def test_dafrfr():
    handle = cs.dafopr(CoreKernels.spk)
    nd, ni, ifname, fward, bward, free = cs.dafrfr(handle)
    cs.dafcls(handle)
    assert nd == 2
    assert ni == 6
    assert ifname == ""
    assert fward == 7
    assert bward == 7


def _dafps_dafrs():
    dafpath = os.path.join(TEST_FILE_DIR, "ckopenkernel_dafps.bc")
    cleanup_kernel(dafpath)
    ifname = "Test CK type 1 segment created by ccs_ckw01"
    handle = cs.ckopn(dafpath, ifname, 10)
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
    # reload
    handle = cs.dafopw(dafpath)
    assert handle is not None
    # begin forward search
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    out = cs.dafgs()
    dc, ic = cs.dafus(out, 2, 6)
    # change the id code and repack
    ic[0] = -1999
    ic[1] = -2999
    summ = cs.dafps(dc, ic)
    cs.dafrs(summ)
    # finished.
    cs.dafcls(handle)
    cs.kclear()
    # reload the kernel and verify the ic's got updated
    handle = cs.dafopr(dafpath)
    assert handle is not None
    # begin forward search
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    out = cs.dafgs(n=124)
    dc, ic = cs.dafus(out, 2, 6)
    assert ic[0] == -1999
    assert ic[1] == -2999
    # cleanup
    cs.dafcls(handle)
    cs.kclear()
    cleanup_kernel(dafpath)


def test_dafus():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    out = cs.dafgs()
    dc, ic = cs.dafus(out, 2, 6)
    cs.dafcls(handle)
    npt.assert_array_almost_equal(
        dc, [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    npt.assert_array_almost_equal(ic, [1, 0, 1, 2, 1025, 27164])


def test_dasac_dasopr_dasec_dasdc_dashfn_dasrfr_dashfs_dasllc():
    daspath = os.path.join(TEST_FILE_DIR, "ex_dasac.das")
    cleanup_kernel(daspath)
    handle = cs.dasonw(daspath, "TEST", "ex_dasac", 140)
    assert handle is not None
    # write some comments
    cs.dasac(handle, ["spice", "naif", "python"])
    cs.dascls(handle)
    cs.kclear()
    cs.reset()
    # we wrote to the test kernel, now load it in read mode
    handle = cs.dasopr(daspath)
    assert handle is not None
    # check that dashfn points to the correct path
    assert cs.dashfn(handle) == daspath
    # extract out the comment, say we only want 3 things out
    comments = cs.dasec(handle)
    assert set(comments) == {"spice", "naif", "python"} & set(comments)
    # close the das file
    cs.dascls(handle)
    ###############################################
    # now test dasrfr
    handle = cs.dasopr(daspath)
    assert handle is not None
    idword, ifname, nresvr, nresvc, ncomr, ncomc = cs.dasrfr(handle)
    assert idword is not None
    assert idword == "DAS/TEST"
    assert ifname == "ex_dasac"
    assert nresvr == 0
    assert nresvc == 0
    assert ncomr == 140
    assert ncomc == 18
    # close the das file
    cs.dascls(handle)
    # test dashfs
    handle = cs.dasopr(daspath)
    nresvr, nresvc, ncomr, ncomc, free, lastla, lastrc, lastwd = cs.dashfs(
        handle)
    assert nresvr == 0
    assert nresvc == 0
    assert ncomr == 140
    assert ncomc == 18
    cs.dasllc(handle)
    ###############################################
    # now reload the kernel and delete the commnets
    handle = cs.dasopw(daspath)
    assert handle is not None
    # delete the comments
    cs.dasdc(handle)
    # close the das file
    cs.dascls(handle)
    # open again for reading
    handle = cs.dasopr(daspath)
    assert handle is not None
    # extract out the comments, hopefully nothing
    comments = cs.dasec(handle)
    assert len(comments) == 0
    # close it again
    cs.dascls(handle)
    # done, so clean up
    cs.kclear()
    cleanup_kernel(daspath)


def test_dasadc():
    h = cs.dasops()
    cs.dasadc(h, 4, 0, 4, ["SPUD"])
    nc, _, _ = cs.daslla(h)
    assert nc == 4
    cs.dascls(h)


def test_dasadd():
    h = cs.dasops()
    data = np.linspace(0.0, 1.0, num=10)
    cs.dasadd(h, data)
    _, nd, _ = cs.daslla(h)
    assert nd == 10
    cs.dascls(h)


def test_dasadi():
    h = cs.dasops()
    data = np.arange(0, 10, dtype=int)
    cs.dasadi(h, data)
    _, _, ni = cs.daslla(h)
    assert ni == 10
    cs.dascls(h)


def test_dasopw_dascls_dasopr():
    daspath = os.path.join(TEST_FILE_DIR, "ex_das.das")
    cleanup_kernel(daspath)
    handle = cs.dasonw(daspath, "TEST", daspath, 0)
    assert handle is not None
    cs.dascls(handle)
    handle = cs.dasopw(daspath)
    assert handle is not None
    cs.dascls(handle)
    handle = cs.dasopr(daspath)
    cs.dascls(handle)
    assert handle is not None
    cs.kclear()
    cleanup_kernel(daspath)


def test_daslla():
    h = cs.dasops()
    data = np.arange(4, 12, dtype=int)
    cs.dasadi(h, data)
    x, y, ni = cs.daslla(h)
    assert x == 0, y == 0
    assert ni == 8


def test_dasonw():
    daspath = os.path.join(TEST_FILE_DIR, "ex_dasac.das")
    cleanup_kernel(daspath)
    handle = cs.dasonw(daspath, "TEST", "ex_dasac", 140)
    assert handle is not None
    cs.dascls(handle)


def test_dasops():
    h = cs.dasops()
    assert h is not None
    cs.dascls(h)


# Unit test cannot be written without dasadc()
def test_dasrdc():
    pass


def test_dasudd_dasrdd():
    daspath = os.path.join(TEST_FILE_DIR, "ex_dasudd.das")
    cleanup_kernel(daspath)
    handle = cs.dasonw(daspath, "TEST", "ex_dasudd", 140)
    cs.dasadd(handle, np.zeros(200, dtype=float))
    data = np.arange(200, dtype=float)
    cs.dasudd(handle, 1, 200, data)
    cs.dascls(handle)
    # load and ensure data was written
    handle = cs.dasopr(daspath)
    rdata = cs.dasrdd(handle, 1, 200)
    assert rdata == pytest.approx(data)
    cs.dascls(handle)
    cleanup_kernel(daspath)


# Fails due to unknown reason
def test_dasudi_dasrdi():
    daspath = os.path.join(TEST_FILE_DIR, "ex_dasudi.das")
    cleanup_kernel(daspath)
    handle = cs.dasonw(daspath, "TEST", "ex_dasudi", 140)
    cs.dasadi(handle, np.zeros(200, dtype=int))
    data = np.arange(200, dtype=int)
    cs.dasudi(handle, 1, 200, data)
    cs.dascls(handle)
    # load and ensure data was written
    handle = cs.dasopr(daspath)
    rdata = cs.dasrdi(handle, 1, 200)
    assert rdata == pytest.approx(data)
    cs.dascls(handle)
    cleanup_kernel(daspath)


def test_dp2hx():
    assert cs.dp2hx(2.0e-9) == "89705F4136B4A8^-7"
    assert cs.dp2hx(1.0) == "1^1"
    assert cs.dp2hx(-1.0) == "-1^1"
    assert cs.dp2hx(1024.0) == "4^3"

# Fails due to bytearray reliance.


def test_dasudc():
    pass


def test_dazldr_drdazl():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    et = cs.str2et("2003 Oct 13 06:00:00 UTC")
    state, lt = cs.spkezr("VENUS", et, "DSS-14_TOPO", "CN+S", "DSS-14")
    r, az, el = cs.recazl(state[0:3], False, True)
    jacobi = cs.dazldr(state[0], state[1], state[2], False, True)
    azlvel = cs.mxv(jacobi, state[3:])
    jacobi = cs.drdazl(r, az, el, False, True)
    drectn = cs.mxv(jacobi, azlvel)
    npt.assert_array_almost_equal(
        drectn,
        [
            6166.04150307,
            -13797.77164550,
            -8704.32385654,
        ],
        decimal=3,
    )


def test_dcyldr():
    output = cs.dcyldr(1.0, 0.0, 0.0)
    expected = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_deltet():
    cs.furnsh(CoreKernels.testMetaKernel)
    UTC_1997 = "Jan 1 1997"
    UTC_2004 = "Jan 1 2004"
    et_1997 = cs.str2et(UTC_1997)
    et_2004 = cs.str2et(UTC_2004)
    delt_1997 = cs.deltet(et_1997, "ET")
    delt_2004 = cs.deltet(et_2004, "ET")
    npt.assert_almost_equal(delt_1997, 62.1839353, decimal=6)
    npt.assert_almost_equal(delt_2004, 64.1839116, decimal=6)


def test_det():
    m1 = np.array([[5.0, -2.0, 1.0], [0.0, 3.0, -1.0], [2.0, 0.0, 7.0]])
    expected = 103
    assert cs.det(m1) == expected


def test_dgeodr():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("EARTH", "RADII")
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * cs.rpd()
    lat = 32.0 * cs.rpd()
    alt = 0.0
    rec = cs.latrec(lon, lat, alt)
    output = cs.dgeodr(rec[0], rec[1], rec[2], radii[0], flat)
    expected = [
        [-0.25730624850202866, 0.41177607401581356, 0.0],
        [-0.019818463887750683, -0.012383950685377182, 0.0011247386599188864],
        [0.040768073853231314, 0.02547471988726025, 0.9988438330394612],
    ]
    npt.assert_array_almost_equal(output, expected)


def test_diags2():
    mat = [[1.0, 4.0], [4.0, -5.0]]
    diag, rot = cs.diags2(mat)
    expected_diag = [[3.0, 0.0], [0.0, -7.0]]
    expected_rot = [[0.89442719, -0.44721360], [0.44721360, 0.89442719]]
    npt.assert_array_almost_equal(diag, expected_diag)
    npt.assert_array_almost_equal(rot, expected_rot)


def test_dlabbs_dlafps():
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    current = cs.dlabbs(handle)
    assert current is not None
    assert current[5] == 1300
    with pytest.raises(Exception):
        prev = cs.dlafps(handle, current)
    cs.dascls(handle)


def test_dlabfs_dlafns():
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    current = cs.dlabfs(handle)
    assert current is not None
    assert current[5] == 1300
    with pytest.raises(Exception):
        next = cs.dlafns(handle, current)
    cs.dascls(handle)


def fail_dlafns():
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    cs.use_flags(cs.dlafns)
    current = cs.dlabfs(handle)
    output = cs.dlafns(handle, current)
    assert output[1] is False


def test_dlaopn_dlabns_dlaens_daswbr():
    path = os.path.join(TEST_FILE_DIR, "dlaopn_dlabns_dlaens_daswbr.dla")
    cleanup_kernel(path)
    handle = cs.dlaopn(path, "DLA", "Example DLA file for testing", 0)
    cs.dlabns(handle)  # start segm
    datai = np.arange(100, dtype=int)
    datad = np.arange(100.0, dtype=float)
    cs.dasadi(handle, datai)
    cs.dasadd(handle, datad)
    cs.dlaens(handle)  # end the segment
    cs.daswbr(handle)
    cs.dasllc(handle)
    # now read the file to check data
    handle = cs.dasopr(path)
    dladsc = cs.dlabfs(handle)
    assert dladsc[3] == 100
    cs.dascls(handle)
    # now clean up
    cleanup_kernel(path)


def test_dlatdr():
    output = cs.dlatdr(1.0, 0.0, 0.0)
    expected = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_dnearp():
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(CoreKernels.pck)
    cs.furnsh(CoreKernels.spk)
    cs.furnsh(ExtraKernels.mro2007sub)
    cs.furnsh(ExtraKernels.marsSpk)
    cs.furnsh(ExtraKernels.spk430sub)
    et = cs.str2et("2007 SEP 30 00:00:00 TDB")
    radii = cs.bodvrd("MARS", "RADII")
    state, lt = cs.spkezr("MRO", et, "IAU_MARS", "NONE", "MARS")
    dnear, dalt, found = cs.dnearp(state, radii[0], radii[1], radii[2])
    shift = (dalt[1] / cs.clight()) * 20.0  # 20mhz
    assert shift == pytest.approx(-0.0000005500991159)
    assert cs.vnorm(dnear[3:]) == pytest.approx(3.214001, abs=1e-6)


def test_dpgrdr():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("MARS", "RADII")
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    output = cs.dpgrdr("Mars", 90.0 * cs.rpd(), 45 * cs.rpd(), 300, re, f)
    expected = [
        [0.25464790894703276, -0.5092958178940655, -0.0],
        [-0.002629849831988239, -0.0013149249159941194, 1.5182979166821334e-05],
        [0.004618598844358383, 0.0023092994221791917, 0.9999866677515724],
    ]
    npt.assert_array_almost_equal(output, expected)


def test_dpmax():
    assert cs.dpmax() >= 1.0e37


def test_dpmin():
    assert cs.dpmin() <= -1.0e37


def test_dpr():
    assert cs.dpr() == 180.0 / np.arccos(-1.0)


def test_drdcyl():
    output = cs.drdcyl(1.0, np.deg2rad(180.0), 1.0)
    expected = [[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_drdgeo():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("EARTH", "RADII")
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * cs.rpd()
    lat = 32.0 * cs.rpd()
    alt = 0.0
    output = cs.drdgeo(lon, lat, alt, radii[0], flat)
    expected = [
        [-4780.329375996193, 1580.5982261675397, -0.3981344650201568],
        [-2541.7462156656084, -2972.6729150327574, 0.7487820251299121],
        [0.0, 5387.9427815962445, 0.5299192642332049],
    ]
    npt.assert_array_almost_equal(output, expected)


def test_drdlat():
    output = cs.drdlat(1.0, 90.0 * cs.rpd(), 0.0)
    expected = [[0.0, -1.0, -0.0], [1.0, 0.0, -0.0], [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_drdpgr():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("MARS", "RADII")
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    output = cs.drdpgr("Mars", 90.0 * cs.rpd(), 45 * cs.rpd(), 300, re, f)
    expected = [
        [-2620.6789148181783, 0.0, 0.0],
        [0.0, 2606.460468253308, -0.7071067811865476],
        [-0.0, 2606.460468253308, 0.7071067811865475],
    ]
    npt.assert_array_almost_equal(output, expected)


def test_drdsph():
    output = cs.drdsph(1.0, np.pi / 2, np.pi)
    expected = [[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]]
    npt.assert_array_almost_equal(output, expected)


def test_dskopn_dskcls():
    dskpath = os.path.join(TEST_FILE_DIR, "TEST.dsk")
    cleanup_kernel(dskpath)
    handle = cs.dskopn(dskpath, "TEST.DSK/NAIF/NJB/20-OCT-2006/14:37:00", 0)
    assert handle is not None
    cs.dskcls(handle, False)
    cs.kclear()
    cleanup_kernel(dskpath)


def test_dskb02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # test dskb02
    (
        nv,
        nump,
        nvxtot,
        vtxbds,
        voxsiz,
        voxori,
        vgrext,
        cgscal,
        vtxnpl,
        voxnpt,
        voxnpl,
    ) = cs.dskb02(handle, dladsc)
    # test results
    assert nv == 422
    assert nump == 840
    assert nvxtot == 8232
    assert cgscal == 7
    assert vtxnpl == 0
    assert voxnpt == 2744
    assert voxnpl == 3257
    assert voxsiz == pytest.approx(3.320691339664286)
    # cleanup
    cs.dascls(handle)


def test_dskd02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # Fetch the vertex
    values = cs.dskd02(handle, dladsc, 19, 0)
    assert len(values) > 0
    npt.assert_almost_equal(
        values[:3],
        [
            5.12656957900699912362e-16,
            -0.00000000000000000000e00,
            -8.37260000000000026432e00,
        ],
    )
    cs.dascls(handle)


def test_dskgd():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = cs.dskgd(handle, dladsc)
    assert dskdsc.surfce == 401
    assert dskdsc.center == 401
    assert dskdsc.dclass == 1
    assert dskdsc.dtype_ == 2
    assert dskdsc.frmcde == 10021
    assert dskdsc.corsys == 1
    npt.assert_almost_equal(dskdsc.corpar, np.zeros(10))
    assert dskdsc.co1min == pytest.approx(-3.141593)
    assert dskdsc.co1max == pytest.approx(3.141593)
    assert dskdsc.co2min == pytest.approx(-1.570796)
    assert dskdsc.co2max == pytest.approx(1.570796)
    assert dskdsc.co3min == pytest.approx(8.181895873588292)
    assert dskdsc.co3max == pytest.approx(13.89340000000111)
    assert dskdsc.start == pytest.approx(-1577879958.816059)
    assert dskdsc.stop == pytest.approx(1577880066.183913)
    # cleanup
    cs.dascls(handle)


def test_dskgtl_dskstl():
    cs_DSK_KEYXFR = 1
    assert cs.dskgtl(cs_DSK_KEYXFR) == pytest.approx(1.0e-10)
    cs.dskstl(cs_DSK_KEYXFR, 1.0e-8)
    assert cs.dskgtl(cs_DSK_KEYXFR) == pytest.approx(1.0e-8)
    cs.dskstl(cs_DSK_KEYXFR, 1.0e-10)
    assert cs.dskgtl(cs_DSK_KEYXFR) == pytest.approx(1.0e-10)


def test_dski02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # Find the number of plates in the model
    # cs_DSK02_KWNP == 2
    num_plates = cs.dski02(handle, dladsc, 2, 0, 3)
    assert len(num_plates) > 0
    cs.dascls(handle)


def fail_dskw02_dskrb2_dskmi2():
    dskpath = os.path.join(TEST_FILE_DIR, "TESTdskw02.dsk")
    cleanup_kernel(dskpath)
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # declare some variables
    finscl = 5.0
    corscl = 4
    center = 401
    surfid = 1
    dclass = 2
    frame = "IAU_PHOBOS"
    first = -50 * cs.jyear()
    last = 50 * cs.jyear()
    # stuff from csdsk.h
    cs_DSK02_MAXVRT = 16000002 // 128  # divide to lower memory usage
    cs_DSK02_MAXPLT = 2 * (cs_DSK02_MAXVRT - 2)
    cs_DSK02_MAXVXP = cs_DSK02_MAXPLT // 2
    cs_DSK02_MAXCEL = 60000000 // 128  # divide to lower memory usage
    cs_DSK02_MXNVLS = cs_DSK02_MAXCEL + (cs_DSK02_MAXVXP // 2)
    cs_DSK02_MAXCGR = 100000 // 128  # divide to lower memory usage
    cs_DSK02_IXIFIX = cs_DSK02_MAXCGR + 7
    cs_DSK02_MAXNPV = 3 * (cs_DSK02_MAXPLT // 2) + 1
    cs_DSK02_SPAISZ = (
        cs_DSK02_IXIFIX
        + cs_DSK02_MAXVXP
        + cs_DSK02_MXNVLS
        + cs_DSK02_MAXVRT
        + cs_DSK02_MAXNPV
    )
    worksz = cs_DSK02_MAXCEL
    voxpsz = cs_DSK02_MAXVXP
    voxlsz = cs_DSK02_MXNVLS
    spaisz = cs_DSK02_SPAISZ
    # get verts, number from dskb02 test
    vrtces = cs.dskv02(handle, dladsc, 1)
    # get plates, number from dskb02 test
    plates = cs.dskp02(handle, dladsc, 1)
    # close the input kernel
    cs.dskcls(handle, optmiz=True)
    cs.kclear()
    # open new dsk file
    handle = cs.dskopn(dskpath, "TESTdskw02.dsk/AA/29-SEP-2017", 0)
    # create spatial index
    spaixd, spaixi = cs.dskmi2(
        vrtces, plates, finscl, corscl, False)
    # do stuff
    corsys = 1
    mncor1 = -cs.pi()
    mxcor1 = cs.pi()
    mncor2 = -cs.pi() / 2
    mxcor2 = cs.pi() / 2
    # Compute plate model radius bounds.
    corpar = np.zeros(10)
    mncor3, mxcor3 = cs.dskrb2(vrtces, plates, corsys, corpar)
    # Write the segment to the file
    cs.dskw02(
        handle,
        center,
        surfid,
        dclass,
        frame,
        corsys,
        corpar,
        mncor1,
        mxcor1,
        mncor2,
        mxcor2,
        mncor3,
        mxcor3,
        first,
        last,
        vrtces,
        plates,
        spaixd,
        spaixi,
    )
    # Close the dsk file
    cs.dskcls(handle, optmiz=True)
    # cleanup
    cs.kclear()
    cleanup_kernel(dskpath)


def test_dskn02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get the normal vector for first plate
    normal = cs.dskn02(handle, dladsc, 1)
    npt.assert_almost_equal(
        normal,
        [0.20813166897151150203, 0.07187012861854354118, -0.97545676120650637309],
    )
    cs.dascls(handle)


def test_dskobj_dsksrf():
    cs.reset()
    bodyids = cs.dskobj(ExtraKernels.phobosDsk)
    assert 401 in bodyids
    srfids = cs.dsksrf(ExtraKernels.phobosDsk, 401)
    assert 401 in srfids
    cs.reset()


def test_dskp02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get the first plate
    plates = cs.dskp02(handle, dladsc, 1)
    npt.assert_almost_equal(plates[0], [1, 9, 2])
    npt.assert_almost_equal(plates[1], [1, 2, 3])
    cs.dascls(handle)


def test_dskv02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # read the vertices
    vrtces = cs.dskv02(handle, dladsc, 1)
    npt.assert_almost_equal(
        vrtces[0],
        [
            5.12656957900699912362e-16,
            -0.00000000000000000000e00,
            -8.37260000000000026432e00,
        ],
    )
    cs.dascls(handle)


def test_dskx02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = cs.dskgd(handle, dladsc)
    r = 2.0 * dskdsc.co3max
    # Produce a ray vertex
    vertex = cs.latrec(r, 0.0, 0.0)
    raydir = cs.vminus(vertex)
    plid, xpt = cs.dskx02(handle, dladsc, vertex, raydir)
    # test results
    assert plid == 421
    npt.assert_almost_equal(xpt, [12.36679999999999957083, 0.0, 0.0])
    # cleanup
    cs.dascls(handle)


def test_dskxsi():
    # load kernels
    cs.furnsh(ExtraKernels.phobosDsk)
    # get handle
    dsk1, filtyp, source, handle = cs.kdata(0, "DSK")
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = cs.dskgd(handle, dladsc)
    target = cs.bodc2n(dskdsc.center)
    fixref = cs.frmnam(dskdsc.frmcde)
    r = 1.0e10
    vertex = cs.latrec(r, 0.0, 0.0)
    raydir = cs.vminus(vertex)
    srflst = [dskdsc.surfce]
    # call dskxsi
    xpt, handle, dladsc2, dskdsc2, dc, ic = cs.dskxsi(
        False, target, srflst, 0.0, fixref, vertex, raydir
    )
    # check output
    assert handle is not None
    assert ic[0] == 420
    npt.assert_almost_equal(xpt, [12.36679999999999957083, 0.0, 0.0])


def test_dskxv():
    # load kernels
    cs.furnsh(ExtraKernels.phobosDsk)
    # get handle
    dsk1, filtyp, source, handle = cs.kdata(0, "DSK")
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = cs.dskgd(handle, dladsc)
    target = cs.bodc2n(dskdsc.center)
    fixref = cs.frmnam(dskdsc.frmcde)
    r = 1.0e10
    vertex = cs.latrec(r, 0.0, 0.0)
    raydir = cs.vminus(vertex)
    srflst = [dskdsc.surfce]
    # call dskxsi
    xpt, foundarray = cs.dskxv(
        False, target, srflst, 0.0, fixref, [vertex], [raydir]
    )
    # check output
    assert len(xpt) == 1
    assert len(foundarray) == 1
    assert foundarray[0]
    npt.assert_almost_equal(xpt[0], [12.36679999999999957083, 0.0, 0.0])


def test_dskxv_2():
    # load kernels
    cs.furnsh(ExtraKernels.phobosDsk)
    # get handle
    dsk1, filtyp, source, handle = cs.kdata(0, "DSK")
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = cs.dskgd(handle, dladsc)
    target = cs.bodc2n(dskdsc.center)
    fixref = cs.frmnam(dskdsc.frmcde)
    r = 1.0e10
    polmrg = 0.5
    latstp = 1.0
    lonstp = 2.0

    lon = -180.0
    lat = 90.0
    nlstep = 0
    nrays = 0
    verticies = []
    raydirs = []

    while lon <= 180.0:
        while nlstep <= 180.0:
            if lon == 180.0:
                lat = 90.0 - nlstep * latstp
            else:
                if nlstep == 0:
                    lat = 90.0 - polmrg
                elif nlstep == 180:
                    lat = -90.0 + polmrg
                else:
                    lat = 90.0 - nlstep * latstp
            vertex = cs.latrec(r, np.radians(lon), np.radians(lat))
            raydir = cs.vminus(vertex)
            verticies.append(vertex)
            raydirs.append(raydir)
            nrays += 1
            nlstep += 1
        lon += lonstp
        lat = 90.0
        nlstep = 0

    srflst = [dskdsc.surfce]
    # call dskxsi
    xpt, foundarray = cs.dskxv(
        False, target, srflst, 0.0, fixref, verticies, raydirs
    )
    # check output
    assert len(xpt) == 32761
    assert len(foundarray) == 32761
    assert foundarray.all()


def test_dskz02():
    # open the dsk file
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = cs.dlabfs(handle)
    # get vertex and plate counts
    nv, nplates = cs.dskz02(handle, dladsc)
    assert nv > 0
    assert nplates > 0
    cs.dascls(handle)


def test_dsphdr():
    output = cs.dsphdr(-1.0, 0.0, 0.0)
    expected = [[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]]
    npt.assert_array_almost_equal(output, expected)


def test_dtpool():
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


def test_ducrss():
    cs.furnsh(CoreKernels.testMetaKernel)
    z_earth = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    et = cs.str2et("Jan 1, 2009")
    trans = cs.sxform("IAU_EARTH", "J2000", et)
    z_j2000 = np.dot(np.array(trans), np.array(z_earth))
    state, ltime = cs.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    z_new = cs.ducrss(state, z_j2000)
    z_expected = [
        -0.9798625180326394,
        -0.1996715076226282,
        0.0008572038510904833,
        4.453114222872359e-08,
        -2.1853106962531453e-07,
        -3.6140021238340607e-11,
    ]
    npt.assert_array_almost_equal(z_new, z_expected)


def test_dvcrss():
    cs.furnsh(CoreKernels.testMetaKernel)
    z_earth = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    et = cs.str2et("Jan 1, 2009")
    trans = cs.sxform("IAU_EARTH", "J2000", et)
    z_j2000 = np.dot(np.array(trans), np.array(z_earth))
    state, ltime = cs.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    z = cs.dvcrss(state, z_j2000)
    expected = [
        -1.32672690582546606660e08,
        -2.70353812480484284461e07,
        1.16064793997540167766e05,
        5.12510726479525757782e00,
        -2.97732415336074147660e01,
        -4.10216496370272454969e-03,
    ]
    npt.assert_almost_equal(z, expected)


def test_dvdot():
    assert (
        cs.dvdot([1.0, 0.0, 1.0, 0.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0, 1.0, 0.0, 1.0])
        == 3.0
    )


def test_dvhat():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("Jan 1, 2009")
    state, ltime = cs.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    x_new = cs.dvhat(state)
    expected = [
        0.1834466376334262,
        -0.9019196633282948,
        -0.39100927360200305,
        2.0244976750658316e-07,
        3.4660106111045445e-08,
        1.5033141925267006e-08,
    ]
    npt.assert_array_almost_equal(expected, x_new)


def test_dvnorm():
    mag = np.array([-4.0, 4, 12])
    x = np.array([1.0, np.sqrt(2.0), np.sqrt(3.0)])
    s1 = np.array([x * 10.0 ** mag[0], x]).flatten()
    s2 = np.array([x * 10.0 ** mag[1], -x]).flatten()
    s3 = np.array([[0.0, 0.0, 0.0], x * 10 ** mag[2]]).flatten()
    npt.assert_approx_equal(cs.dvnorm(s1), 2.4494897)
    npt.assert_approx_equal(cs.dvnorm(s2), -2.4494897)
    npt.assert_approx_equal(cs.dvnorm(s3), 0.0)


def test_dvpool():
    cs.pdpool("DTEST_VAL", [3.1415, 186.0, 282.397])
    assert cs.expool("DTEST_VAL")
    cs.dvpool("DTEST_VAL")
    assert not cs.expool("DTEST_VAL")
    cs.clpool()


def test_dvsep():
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et("JAN 1 2009")
    state_e, eltime = cs.spkezr("EARTH", et, "J2000", "NONE", "SUN")
    state_m, mltime = cs.spkezr("MOON", et, "J2000", "NONE", "SUN")
    dsept = cs.dvsep(state_e, state_m)
    npt.assert_approx_equal(dsept, 3.8121194e-09)
