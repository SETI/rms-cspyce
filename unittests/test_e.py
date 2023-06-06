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
    npt.assert_array_almost_equal(limb.center, expected_center)
    npt.assert_array_almost_equal(limb.semi_major, expected_s_major)
    npt.assert_array_almost_equal(limb.semi_minor, expected_s_minor)


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

# =============================================================================
# edterm
# ekacec
# ekaced
# ekacei
# ekaclc
# ekacld
# ekacli
# ekappr
# ekbseg
# ekccnt
# ekcii
# ekcls
# ekdelr
# ekffld
# ekfind
# ekgc
# ekgd
# =============================================================================
