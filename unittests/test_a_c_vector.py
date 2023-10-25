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


def test_axisar_vector():
    axis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    outmatrix = cs.axisar_vector(axis, cs.halfpi())
    expected = np.array([[[ 1.0,  0.0,  0.0],
                          [ 0.0,  0.0, -1.0],
                          [ 0.0,  1.0,  0.0]],
    
                         [[ 0.0,  0.0,  1.0],
                          [ 0.0,  1.0,  0.0],
                          [-1.0,  0.0,  0.0]],
                        
                         [[ 0.0, -1.0,  0.0],
                          [ 1.0,  0.0,  0.0],
                          [ 0.0,  0.0,  1.0]]])
    npt.assert_array_almost_equal(expected, outmatrix, decimal=6)
    
    
def test_azlcpo_vector():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    et = cs.str2et("2003 Oct 13 06:00:00 UTC")
    obspos = [[-2353.621419700, -4641.341471700, 3677.052317800],
              [-2345.621419700, -4661.341471700, 3047.052317800],
              [-2313.621419700, -4621.341471700, 3337.052317800]
              ]
    azlsta, lt = cs.azlcpo_vector(
        "ELLIPSOID", "VENUS", et, "CN+S", False, True, obspos, "EARTH", "ITRF93"
    )
    npt.assert_allclose([[ 2.45721479e+08,  5.13974044e+00, -8.54270565e-01, -4.68189831e+00,
                           7.02070016e-05, -5.39579640e-05],
                         [ 2.45721364e+08,  5.04677647e+00, -8.88969162e-01, -4.68224541e+00,
                           6.20530885e-05, -5.92304583e-05],
                         [ 2.45721394e+08,  5.09964300e+00, -8.74738668e-01, -4.68498412e+00,
                           6.70444532e-05, -5.64760542e-05]],
                        azlsta)
    
    
def test_azlrec_vector():
    d = cs.rpd()
    npt.assert_array_almost_equal(
        cs.azlrec_vector([0.000, 0.000, 0.000], 0.000 * d, 0.000 * d, True, True),
        [[0.000, 0.000, 0.000],
         [0.000, 0.000, 0.000],
         [0.000, 0.000, 0.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.000, 1.000, 1.000], 0.000 * d, 0.000 * d, True, True),
        [[1.000, 0.000, 0.000],
         [1.000, 0.000, 0.000],
         [1.000, 0.000, 0.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.000, 1.000, 1.000], 270.000 * d, 0.000 * d, True, True),
        [[-0.000, -1.000, 0.000],
         [-0.000, -1.000, 0.000],
         [-0.000, -1.000, 0.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.000, 1.000, 1.000], 0.000 * d, -90.000 * d, True, True),
        [[0.000, 0.000, -1.000],
         [0.000, 0.000, -1.000],
         [0.000, 0.000, -1.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.000, 1.000, 1.000], 180.000 * d, 0.000 * d, True, True),
        [[-1.000, 0.000, 0.000],
         [-1.000, 0.000, 0.000],
         [-1.000, 0.000, 0.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.000, 1.000, 1.000], 90.000 * d, 0.000 * d, True, True),
        [[0.000, 1.000, 0.000],
         [0.000, 1.000, 0.000],
         [0.000, 1.000, 0.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.000, 1.000, 1.000], 0.000 * d, 90.000 * d, True, True),
        [[0.000, 0.000, 1.000],
         [0.000, 0.000, 1.000],
         [0.000, 0.000, 1.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.414, 1.414, 1.414], 315.000 * d, 0.000 * d, True, True),
        [[1.000, -1.000, 0.000],
         [1.000, -1.000, 0.000],
         [1.000, -1.000, 0.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.414, 1.414, 1.414], 0.000 * d, -45.000 * d, True, True),
        [[1.000, 0.000, -1.000],
         [1.000, 0.000, -1.000],
         [1.000, 0.000, -1.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.414, 1.414, 1.414], 270.000 * d, -45.000 * d, True, True),
        [[-0.000, -1.000, -1.000],
         [-0.000, -1.000, -1.000],
         [-0.000, -1.000, -1.000]],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec_vector([1.732, 1.732, 1.732], 315.000 * d, -35.264 * d, True, True),
        [[1.000, -1.000, -1.000],
         [1.000, -1.000, -1.000],
         [1.000, -1.000, -1.000]],
        decimal=3,
    )
    
    
def test_brcktd_vector():
    npt.assert_equal(cs.brcktd_vector([29.0, 12.0, 2.0], [1.0, 15.0, 0.0], [30.0, 17.0, 5.0]), [29.0, 15.0, 2.0])
    npt.assert_equal(cs.brcktd_vector([3.0, 4.0, 5.0], [-10.0, 0.0, 10.0], [10.0, 5.0, 20.0]), [3.0, 4.0, 10.0])
    npt.assert_equal(cs.brcktd_vector([3.0, 1.0, -1.0], [-10.0, 0.0, -2.0], [-1.0, 2.0, 1.0]), [-1.0, 1.0, -1.0])
    
    
def test_bsrchd_vector():
    array = np.array([-11.0, 0.0, 22.0, 750.0])
    npt.assert_equal(cs.bsrchd_vector([-11.0, 0.0], array), [0, 1])
    npt.assert_equal(cs.bsrchd_vector([22.0, -11.0], array), [2, 0])
    npt.assert_equal(cs.bsrchd_vector([751.0, 22.0, 0.0, -11.0], array), [-1, 2, 1, 0])
    
    
def test_cgv2el_vector():
    vec1 = [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
    vec2 = [[1.0, 1.0, 1.0], [-1.0, -1.0, -1.0], [1.0, 1.0, 1.0]]
    center = [[-1.0, -1.0, -1.0], [1.0, 1.0, 1.0], [-1.0, -1.0, -1.0]]
    ellipse = cs.cgv2el_vector(center, vec1, vec2)
    expected_s_major = [[np.sqrt(2.0), np.sqrt(2.0), np.sqrt(2.0)],
                        [-np.sqrt(2.0), -np.sqrt(2.0), -np.sqrt(2.0)],
                        [np.sqrt(2.0), np.sqrt(2.0), np.sqrt(2.0)]]
    expected_s_minor = [[0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0]]
    expected_center = [[-1.0, -1.0, -1.0],
                       [1.0, 1.0, 1.0],
                       [-1.0, -1.0, -1.0]]
    npt.assert_array_almost_equal(expected_center, ellipse[:3, :3])
    npt.assert_array_almost_equal(expected_s_major, ellipse[:3, 3:6])
    npt.assert_array_almost_equal(expected_s_minor, ellipse[:3, 6:9])
    

chbder  
chbigr
chbint
chbval
conics
convrt
cyllat
cylrec
cylsph