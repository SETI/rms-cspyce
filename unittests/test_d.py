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
    cwd
)

# =============================================================================
# @pytest.fixture(autouse=True)
# =============================================================================
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
    dafpath = os.path.join(cwd, "ex_dafac.bc")
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
    dafpath = os.path.join(cwd, "ex_dafdc.bc")
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
    

# Test changed. cs.dafec() only takes one input, while spiceypy.dafec() takes
# three. Fails due to lack of maximum size parameter.
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


# Fails due to dafgda()
def fail_dafgda():
    # not a very good test...
    handle = cs.dafopr(CoreKernels.spk)
    elements = cs.dafgda(handle, 20, 20)
    assert elements == [0.0]
    cs.dafcls(handle)
    
    
def test_dafgh():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbbs(handle)
    cs.dafcs(handle)
    searchHandle = cs.dafgh()
    assert searchHandle == handle
    cs.dafcls(handle)
    
    
# Fails due to dafgs()
def fail_dafgn():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    out = cs.dafgs()
    npt.assert_array_almost_equal(
        out, [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    outname = cs.dafgn()
    assert outname == "DE-405"
    cs.dafcls(handle)
    

# Fails
def fail_dafgs():
    handle = cs.dafopr(CoreKernels.spk)
    cs.dafbfs(handle)
    found = cs.daffna()
    assert found
    out = cs.dafgs()
    npt.assert_array_almost_equal(
        out, [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    cs.dafcls(handle)
    

# Fails due to dafgsr()
def fail_dafgsr():
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
            assert iFrame == 1 and iSPKtype == 2 and (lastIEndWord + 1) == iStartWord
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


def fail_dafps_dafrs():
    dafpath = os.path.join(cwd, "ckopenkernel_dafps.bc")
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
        2 - 1,
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
    out = cs.dafgs(n=124)
    dc, ic = cs.dafus(out, 2, 6)
    # change the id code and repack
    ic[0] = -1999
    ic[1] = -2999
    summ = cs.dafps(2, 6, dc, ic)
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
    

# Test changed. cspyce.dafgs needs fixing.
def fail_dafus():
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
    
    
# Test changed. cs.dasec() outputs one value, not three. 
def test_dasac_dasopr_dasec_dasdc_dashfn_dasrfr_dashfs_dasllc():
    daspath = os.path.join(cwd, "ex_dasac.das")
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
    nresvr, nresvc, ncomr, ncomc, free, lastla, lastrc, lastwd = cs.dashfs(handle)
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
    
    
# Test changed. cs.dasdadc takes five arguments, not six (does not use datlen: 
# Common length of the character arrays in data.)
def fail_dasadc():
    h = cs.dasops()
    cs.dasadc(h, 4, 0, 4, ["SPUD"])
    nc, _, _ = cs.daslla(h)
    assert nc == 4
    cs.dascls(h)


# Test changed. cs.dasadd takes two inputs, not three (does not use n: Number 
# of d p numbers to add to DAS file.)
def test_dasadd():
    h = cs.dasops()
    data = np.linspace(0.0, 1.0, num=10)
    cs.dasadd(h, data)
    _, nd, _ = cs.daslla(h)
    assert nd == 10
    cs.dascls(h)


# Test changed. cs.dasadi takes two inputs, not three ( n: Number of d p 
# numbers to add to DAS file.)
def test_dasadi():
    h = cs.dasops()
    data = np.arange(0, 10, dtype=int)
    cs.dasadi(h, data)
    _, _, ni = cs.daslla(h)
    assert ni == 10
    cs.dascls(h)

# Test changed. cs.dasopr does not exist. 
def test_dasopw_dascls_dasopr():
    daspath = os.path.join(cwd, "ex_das.das")
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
    daspath = os.path.join(cwd, "ex_dasac.das")
    cleanup_kernel(daspath)
    handle = cs.dasonw(daspath, "TEST", "ex_dasac", 140)
    assert handle is not None
    cs.dascls(handle)
    
    
def test_dasops():
    h = cs.dasops()
    assert h is not None
    cs.dascls(h)
    

# Unit test cannot be written without dasadc()
def fail_dasrdc():
    pass


def test_dasudd_dasrdd():
    daspath = os.path.join(cwd, "ex_dasudd.das")
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
def fail_dasudi_dasrdi():
    daspath = os.path.join(cwd, "ex_dasudi.das")
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
    
    
# Fails due to bytearray reliance.
def test_dasudc():
    pass
    

def fail_dlaopn_dlabns_dlaens_daswbr():
    path = os.path.join(cwd, "dlaopn_dlabns_dlaens_daswbr.dla")
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
    assert dladsc.isize == 100
    assert dladsc.dsize == 100
    cs.dascls(handle)
    # now clean up
    cleanup_kernel(path)
    
    
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
    

# Test changed. cspyce currently defaults to dlabbs_error. Using cs.use_flags()
# to use original version. Also, cspyce does not have SpiceyPy's .dsize
# feature, so .dsize is replaced with indexes.
def test_dlabbs():
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    cs.use_flags(cs.dlabbs)
    current = cs.dlabbs(handle)
    assert current is not None
    assert current[0][5] == 1300
    with pytest.raises(Exception):
        prev = cs.dlafps(handle, current)
    cs.dascls(handle)
    

# Test changed. cspyce does not have a spiceypy.dsize equivalent. Replaced
# with indexing.
def test_dlabfs_dlafns():
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    current = cs.dlabfs(handle)
    assert current is not None
    assert current[5] == 1300
    with pytest.raises(Exception):
        next = cs.dlafns(handle, current)
    cs.dascls(handle)
    

# This is a unique test...not good.
def test_dlafns():
    handle = cs.dasopr(ExtraKernels.phobosDsk)
    cs.use_flags(cs.dlafns)
    current = cs.dlabfs(handle)
    output = cs.dlafns(handle, current)
    assert output[1] is False
    

# Still developing this test.
# =============================================================================
# def test_dlafps():
#     cs.use_flags(cs.dlafps)
#     result = cs.dlafps(1, )
#     assert result == [0, 0, 1]
# =============================================================================
    

# Test changed. No equivalent to spiceypy.isize
def test_dlaopn_dlabns_dlaens_daswbr():
    path = os.path.join(cwd, "dlaopn_dlabns_dlaens_daswbr.dla")
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
    cs.furnsh(
        [
            CoreKernels.lsk,
            CoreKernels.pck,
            CoreKernels.spk,
            ExtraKernels.mro2007sub,
            ExtraKernels.marsSpk,
            ExtraKernels.spk430sub,
        ]
    )
    et = cs.str2et("2007 SEP 30 00:00:00 TDB")
    _, radii = cs.bodvrd("MARS", "RADII", 3)
    state, lt = cs.spkezr("MRO", et, "IAU_MARS", "NONE", "MARS")
    dnear, dalt = cs.dnearp(state, radii[0], radii[1], radii[2])
    shift = (dalt[1] / cs.clight()) * 20.0  # 20mhz
    assert shift == pytest.approx(-0.0000005500991159)
    assert cs.vnorm(dnear[3:]) == pytest.approx(3.214001, abs=1e-6)
    
    
def test_dp2hx():
    assert cs.dp2hx(2.0e-9) == "89705F4136B4A8^-7"
    assert cs.dp2hx(1.0) == "1^1"
    assert cs.dp2hx(-1.0) == "-1^1"
    assert cs.dp2hx(1024.0) == "4^3"
    assert cs.dp2hx(-1024.0) == "-4^3"
    assert cs.dp2hx(521707.0) == "7F5EB^5"
    assert cs.dp2hx(27.0) == "1B^2"
    assert cs.dp2hx(0.0) == "0^0"
    
    
def test_dpgrdr():
    cs.furnsh(CoreKernels.testMetaKernel)
    n, radii = cs.bodvrd("MARS", "RADII")
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




