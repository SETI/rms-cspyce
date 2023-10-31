import cspyce as cs
import numpy as np
import numpy.testing as npt
import os
import pytest

from gettestkernels import (
    CoreKernels,
    CassiniKernels,
    ExtraKernels,
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


def test_dazldr_drdazl_vector():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    et1 = cs.str2et("2003 Oct 13 06:00:00 UTC")
    et2 = cs.str2et("2004 Oct 13 06:00:00 UTC")
    state, lt = cs.spkezr_vector("VENUS", [et1, et2], "DSS-14_TOPO", "CN+S", "DSS-14")
    r1, az1, el1 = cs.recazl_vector(state[0, 0:3], False, True)
    r2, az2, el2 = cs.recazl_vector(state[1, 0:3], False, True)
    jacobi = cs.dazldr_vector([state[0, 0], state[1, 0]],
                              [state[0, 1], state[0, 1]],
                              [state[0, 2], state[1, 2]], False, True)
    azlvel1 = cs.mxv(jacobi[0], state[0, 3:])
    azlvel2 = cs.mxv(jacobi[1], state[1, 3:])
    jacobi = cs.drdazl_vector([r1, r2], [az1, az2], [el1, el2], False, True)
    drectn1 = cs.mxv(jacobi[0], azlvel1)
    drectn2 = cs.mxv(jacobi[1], azlvel2)
    npt.assert_array_almost_equal(
        drectn1,
        [
            6166.04150307,
            -13797.77164550,
            -8704.32385654,
        ],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        drectn2,
        [
            -9690.26617647,
            -1035.05117688,
            4856.47648959,
        ],
        decimal=3,
    )
    
    
def test_dcyldr_vector():
    output = cs.dcyldr_vector([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    expected = np.array([[[ 1.0,  0.0,  0.0],
                 [-0.0,  1.0,  0.0],
                 [ 0.0,  0.0,  1.0]],
            
                [[ 1.0,  0.0,  0.0],
                 [-0.0,  1.0,  0.0],
                 [ 0.0,  0.0,  1.0]],
            
                [[ 1.0,  0.0,  0.0],
                 [-0.0,  1.0,  0.0],
                 [ 0.0,  0.0,  1.0]]])
    npt.assert_array_almost_equal(output, expected)
    
    
def test_deltet_vector():
    cs.furnsh(CoreKernels.testMetaKernel)
    UTC_1997 = "Jan 1 1997"
    UTC_2004 = "Jan 1 2004"
    et_1997 = cs.str2et(UTC_1997)
    et_2004 = cs.str2et(UTC_2004)
    delt = cs.deltet_vector([et_1997, et_2004], "ET")
    npt.assert_almost_equal(delt[0], 62.1839353, decimal=6)
    npt.assert_almost_equal(delt[1], 64.1839116, decimal=6)
    
    
def test_det_vector():
    m1 = np.array([[5.0, -2.0, 1.0], [0.0, 3.0, -1.0], [2.0, 0.0, 7.0]])
    m2 = np.array([[3.0, 0.0, -1.0], [2.0, 3.0, 1.0], [2.0, 2.0, 9.0]])
    expected = np.array([103.0, 77.0])
    npt.assert_array_equal(cs.det_vector([m1, m2]), expected)
    
    
def test_dgeodr_vector():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("EARTH", "RADII")
    flat = (radii[0] - radii[2]) / radii[0]
    lon1 = 123.0 * cs.rpd()
    lat1 = 27.0 * cs.rpd()
    alt1 = 0.0
    lon2 = 118.0 * cs.rpd()
    lat2 = 32.0 * cs.rpd()
    alt2 = 0.0
    rec1 = cs.latrec(lon1, lat1, alt1)
    rec2 = cs.latrec(lon2, lat2, alt2)
    output = cs.dgeodr_vector([rec1[0], rec2[0]], [rec1[1], rec2[1]],
                              [rec1[2], rec2[2]], radii[0], flat)
    expected = [[[-0.21147756,  0.41504808,  0.        ],
      [-0.02082451, -0.01061062,  0.00117264],
      [ 0.0446482,   0.0227494,   0.99874371]],

     [[-0.25730625,  0.41177607,  0.        ],
      [-0.01981846, -0.01238395,  0.00112474],
      [ 0.04076807,  0.02547472,  0.99884383]]]
    npt.assert_array_almost_equal(output, expected)
    
    
def test_diags2_vector():
    mat1 = [[1.0, 4.0], [4.0, -5.0]]
    mat2 = [[1.0, 0.0], [0.0, -3.0]]
    mats = np.array([mat1, mat2])
    diag, rot = cs.diags2_vector(mats)
    expected_diag = np.array([[[3.0, 0.0], [0.0, -7.0]], [[1.0, 0.0], [0.0, -3.0]]])
    expected_rot = np.array([[[0.89442719, -0.44721360], [0.44721360, 0.89442719]],
                    [[1.0, 0.0], [0.0, 1.0]]])
    npt.assert_array_almost_equal(diag, expected_diag)
    npt.assert_array_almost_equal(rot, expected_rot)
    
    
def test_dlatdr_vector():
    output = cs.dlatdr_vector([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    expected = np.array([[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
                [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
                [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]])
    npt.assert_array_almost_equal(output, expected)
    
    
def test_dnearp_vector():
    cs.furnsh(CoreKernels.lsk)
    cs.furnsh(CoreKernels.pck)
    cs.furnsh(CoreKernels.spk)
    cs.furnsh(ExtraKernels.mro2007sub)
    cs.furnsh(ExtraKernels.marsSpk)
    cs.furnsh(ExtraKernels.spk430sub)
    et1 = cs.str2et("2007 SEP 30 00:00:00 TDB")
    et2 = cs.str2et("2007 OCT 01 00:00:00 TDB")
    radii = cs.bodvrd("MARS", "RADII")
    state, lt = cs.spkezr_vector("MRO", [et1, et2], "IAU_MARS", "NONE", "MARS")
    dnear, dalt, found = cs.dnearp_vector(state, radii[0], radii[1], radii[2])
    shift1 = (dalt[0, 1] / cs.clight()) * 20.0  # 20mhz
    shift2 = (dalt[1, 1] / cs.clight()) * 20.0  # 20mhz
    assert shift1 == pytest.approx(-0.0000005500991159)
    assert shift2 == pytest.approx(-0.0000025016857224)
    assert cs.vnorm(dnear[0, 3:]) == pytest.approx(3.214001, abs=1e-6)
    assert cs.vnorm(dnear[1, 3:]) == pytest.approx(3.166120, abs=1e-6)
    
    
def test_dpgrdr_vector():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("MARS", "RADII")
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    output = cs.dpgrdr_vector("Mars", [90.0 * cs.rpd(), 45 * cs.rpd()],
                       [45 * cs.rpd(), 45 * cs.rpd()], [300, 150], re, f)
    expected = np.array([
        [[0.25464790894703276, -0.5092958178940655, -0.0],
        [-0.002629849831988239, -0.0013149249159941194, 1.5182979166821334e-05],
        [0.004618598844358383, 0.0023092994221791917, 0.9999866677515724]],
        [[ 6.36619772e-01, -6.36619772e-01, 0.0],
         [-3.71960272e-03, -3.71960272e-03,  3.07354553e-05],
         [ 4.13148029e-03,  4.13148029e-03,  9.99982931e-01]]
    ])
    npt.assert_array_almost_equal(output, expected)
    
    
def test_drdcyl_vector():
    output = cs.drdcyl_vector([1.0, 0.5], [np.deg2rad(180.0), np.deg2rad(270.0)],
                              [1.0, 1.5])
    expected1 = np.array([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])
    expected2 = np.array([[0.0, 0.5, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    npt.assert_array_almost_equal(output[0], expected1)
    npt.assert_array_almost_equal(output[1], expected2)
    
    
def test_drdgeo_vector():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("EARTH", "RADII")
    flat = (radii[0] - radii[2]) / radii[0]
    lon1 = 118.0 * cs.rpd()
    lon2 = 105.0 * cs.rpd()
    lat1 = 32.0 * cs.rpd()
    lat2 = 35.0 * cs.rpd()
    alt = [0.0, 0.0]
    output = cs.drdgeo_vector([lon1, lon2], [lat1, lat2], alt, radii[0], flat)
    expected = [[[-4.78032938e+03,  1.58059823e+03, -3.98134465e-01],
                 [-2.54174622e+03, -2.97267292e+03,  7.48782025e-01],
                 [ 0.00000000e+00, 5.38794278e+03,  5.29919264e-01]],
                
                [[-5.05220405e+03,  9.43627408e+02, -2.12012150e-01],
                 [-1.35373400e+03, -3.52166543e+03,  7.91240115e-01],
                 [ 0.00000000e+00, 5.20687958e+03,  5.73576436e-01]]]
    npt.assert_array_almost_equal(output, expected, decimal = 1e-9)
    
    
def _test_drdlat_vector():
    output = cs.drdlat_vector([1.0, 1.0], [0.0, 0.0], [0.0, 0.0])
    expected = np.array([[[ 1.0, -0.0, -0.0],
                 [ 0.0,  1.0, -0.0],
                 [ 0.0,  0.0,  1.0]],
                
                [[ 1.0, -0.0, -0.0],
                 [ 0.0,  1.0, -0.0],
                 [ 0.0,  0.0,  1.0]]])
    npt.assert_almost_equal(output, expected)
    assert cs.drdlat_vector(1., 0., [1, 2, 3, 4]).shape == (4, 3, 3)
    
    
def test_drdpgr_vector():
    cs.furnsh(CoreKernels.testMetaKernel)
    npt.assert_almost_equal(cs.drdpgr_vector('saturn', 1., 0., 0., 1., 0.),
                        [[-0.84147098, 0., 0.54030231],
                         [-0.54030231, 0., -0.84147098],
                         [0., 1., 0.]])
    assert cs.drdpgr_vector('saturn', 1., 0., 0., 1., [0.1, 0.02, 0.03, 0.04]).shape == (4, 3, 3)
    
    
def test_drdsph_vector():
    output = cs.drdsph_vector([1.0, 1.5], np.pi / 2, np.pi)
    expected = np.array([[[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]],
                         [[-1.0, 0.0, 0.0], [0.0, 0.0, -1.5], [0.0, -1.5, 0.0]]])
    npt.assert_array_almost_equal(output, expected)
    
    
def test_dsphdr_vector():
    output = cs.dsphdr_vector([-1.0, -1.0], [0.0, 0.0], [0.0, 0.0])
    expected = [[[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]],
                [[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]]]
    npt.assert_almost_equal(output, expected)
# =============================================================================
# ducrss
# dvcrss
# dvdot
# dvhat
# dvnorm
# dvsep
# =============================================================================

