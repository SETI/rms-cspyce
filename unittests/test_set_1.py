#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:49:21 2023

@author: emiliesimpson
"""
import pytest
import os
import cspyce as cs
import numpy as np
import numpy.testing as npt

from gettestkernels import (
    get_standard_kernels,
    write_test_meta_kernel,
    download_kernels,
    CoreKernels,
    CassiniKernels,
    ExtraKernels,
    cleanup_cassini_kernels,
    cleanup_extra_kernels,
    cleanup_core_kernels,
    cwd,
)


get_standard_kernels()
write_test_meta_kernel()

cwd = os.environ['CSPYCE_TEST_KERNELS']


# =============================================================================
# def setup():
#     cs.furnsh(os.path.join(KERNELS_, 'de430.bsp'))
#     cs.furnsh(os.path.join(KERNELS_, 'naif0011.tls'))
#     cs.furnsh(os.path.join(KERNELS_, 'pck00010.tpc'))
#     cs.furnsh(os.path.join(KERNELS_, 'earth_720101_070426.bpc'))
#     cs.furnsh(os.path.join(KERNELS_, 'earthstns_itrf93_050714.bsp'))
#     cs.furnsh(os.path.join(KERNELS_, 'earth_topo_050714.tf'))
#     cs.furnsh(os.path.join(KERNELS_, 'pck00008.tpc'))
# 
# 
# setup()
# 
# =============================================================================
# =============================================================================
# def clear_kernel_pool_and_reset():
#     cs.kclear()
#     cs.reset()
#     # yield for test
#     yield
#     # clear kernel pool again
#     cs.kclear()
#     cs.reset()
# 
# 
# def cleanup_kernel(path):
#     cs.kclear()
#     cs.reset()
# =============================================================================
# =============================================================================
#     if cs.exists(path):
#         os.remove(path)  # pragma: no cover
#     pass
# =============================================================================

def test_axisar():
    axis = np.array([0.0, 0.0, 1.0])
    outmatrix = cs.axisar(axis, cs.halfpi())
    expected = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    npt.assert_array_almost_equal(expected, outmatrix, decimal=6)


def test_azlcpo():
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(ExtraKernels.earthTopoTf)
    cs.furnsh(ExtraKernels.earthStnSpk)
    cs.furnsh(ExtraKernels.earthHighPerPck)
    et = cs.str2et("2003 Oct 13 06:00:00 UTC")
    obspos = [-2353.621419700, -4641.341471700, 3677.052317800]
    azlsta, lt = cs.azlcpo(
        "ELLIPSOID", "VENUS", et, "CN+S", False, True, obspos, "EARTH", "ITRF93"
    )
    assert azlsta == pytest.approx(
        [
            2.45721479e8,
            5.13974044,
            -8.54270565e-1,
            -4.68189831,
            7.02070016e-5,
            -5.39579640e-5,
        ]
    )


def test_azlrec():
    d = cs.rpd()
    npt.assert_array_almost_equal(
        cs.azlrec(0.000, 0.000 * d, 0.000 * d, True, True),
        [0.000, 0.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 0.000 * d, 0.000 * d, True, True),
        [1.000, 0.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 270.000 * d, 0.000 * d, True, True),
        [-0.000, -1.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 0.000 * d, -90.000 * d, True, True),
        [0.000, 0.000, -1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 180.000 * d, 0.000 * d, True, True),
        [-1.000, 0.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 90.000 * d, 0.000 * d, True, True),
        [0.000, 1.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.000, 0.000 * d, 90.000 * d, True, True),
        [0.000, 0.000, 1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.414, 315.000 * d, 0.000 * d, True, True),
        [1.000, -1.000, 0.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.414, 0.000 * d, -45.000 * d, True, True),
        [1.000, 0.000, -1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.414, 270.000 * d, -45.000 * d, True, True),
        [-0.000, -1.000, -1.000],
        decimal=3,
    )
    npt.assert_array_almost_equal(
        cs.azlrec(1.732, 315.000 * d, -35.264 * d, True, True),
        [1.000, -1.000, -1.000],
        decimal=3,
    )


def test_b1900():
    assert cs.b1900() == 2415020.31352


def test_b1950():
    assert cs.b1950() == 2433282.42345905


def test_badkpv():
    cs.pdpool("DTEST_VAL", [3.1415, 186.0, 282.397])
    assert not cs.badkpv("csypy BADKPV test", "DTEST_VAL", "=", 3, 1, "N")
    cs.clpool()
    assert not cs.expool("DTEST_VAL")


def test_bltfrm():
    out_cell = cs.bltfrm(-1)
    assert out_cell.size >= 126


def test_bodc2n():
    assert cs.bodc2n(399) == "EARTH"
    assert cs.bodc2n(0) == "SOLAR SYSTEM BARYCENTER"


def test_bodc2s():
    assert cs.bodc2s(399) == "EARTH"
    assert cs.bodc2s(0) == "SOLAR SYSTEM BARYCENTER"


def test_boddef():
    cs.boddef("Jebediah", 117)
    assert cs.bodc2n(117) == "Jebediah"


def test_bodfnd():
    cs.furnsh(CoreKernels.testMetaKernel)
    assert cs.bodfnd(599, "RADII")


def test_bodn2c():
    assert cs.bodn2c("EARTH") == 399
    with pytest.raises(KeyError):
        cs.bodn2c("U.S.S. Enterprise")


def test_bods2c():
    assert cs.bods2c("EARTH") == 399
    with pytest.raises(KeyError):
        cs.bods2c("U.S.S. Enterprise")


def test_bodvar():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvar(399, "RADII")
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, radii, decimal=1)
