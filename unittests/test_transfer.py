import pytest
import os
import cspyce as cs
from unittests.gettestkernels import ExtraKernels, TEST_FILE_DIR
from unittests.test_d import cleanup_kernel
import numpy as np

"""
This file contains tests of the build process
"""
@pytest.mark.skip
def test_dskw02_dskrb2_dskmi2():
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
    cs_DSK02_MAXVRT = 16000002 // 256  # divide to lower memory usage
    cs_DSK02_MAXPLT = 2 * (cs_DSK02_MAXVRT - 2)
    cs_DSK02_MAXVXP = cs_DSK02_MAXPLT // 2
    cs_DSK02_MAXCEL = 60000000 // 256  # divide to lower memory usage
    cs_DSK02_MXNVLS = cs_DSK02_MAXCEL + (cs_DSK02_MAXVXP // 2)
    cs_DSK02_MAXCGR = 100000 // 256  # divide to lower memory usage
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
        vrtces, plates, finscl, corscl, worksz, voxpsz, voxlsz, False, spaisz)

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

import cspyce
import numpy.testing as npt
from gettestkernels import ExtraKernels

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

if __name__ == '__main__':
    # test_dskw02_dskrb2_dskmi2()
    test_dskv02()
