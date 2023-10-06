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