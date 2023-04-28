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


def test_bodvcd():
    cs.furnsh(CoreKernels.testMetaKernel)
    dim, values = 3, cs.bodvcd(399, "RADII")
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
    
    
def test_bodvrd():
    cs.furnsh(CoreKernels.testMetaKernel)
    dim, values = 3, cs.bodvrd("EARTH", "RADII")
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
    
    
def test_brcktd():
    assert cs.brcktd(-1.0, 1.0, 10.0) == 1.0
    assert cs.brcktd(29.0, 1.0, 10.0) == 10.0
    assert cs.brcktd(3.0, -10.0, 10.0) == 3.0
    assert cs.brcktd(3.0, -10.0, -1.0) == -1.0
    
    
def test_brckti():
    assert cs.brckti(-1, 1, 10) == 1
    assert cs.brckti(29, 1, 10) == 10
    assert cs.brckti(3, -10, 10) == 3
    assert cs.brckti(3, -10, -1) == -1
    

# This one had to be changed. Alex's version also requires string length
# and the dimension of the array.
def test_bschoc():
    array = ["FEYNMAN", "BOHR", "EINSTEIN", "NEWTON", "GALILEO"]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoc("NEWTON", array, order) == 3
    assert cs.bschoc("EINSTEIN", array, order) == 2
    assert cs.bschoc("GALILEO", array, order) == 4
    assert cs.bschoc("Galileo", array, order) == -1
    assert cs.bschoc("OBETHE", array, order) == -1
    
    
# This one had to be changed. Alex's version also requires the dimension of
# the array.
def test_bschoi():
    array = [100, 1, 10, 10000, 1000]
    order = [1, 2, 0, 4, 3]
    assert cs.bschoi(1000, array, order) == 4
    assert cs.bschoi(1, array, order) == 1
    assert cs.bschoi(10000, array, order) == 3
    assert cs.bschoi(-1, array, order) == -1
    assert cs.bschoi(17, array, order) == -1

# This one had to be changed. Alex's version also requires string length
# and the dimension of the array.
def test_bsrchc():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    assert cs.bsrchc("NEWTON", array) == 4
    assert cs.bsrchc("EINSTEIN", array) == 1
    assert cs.bsrchc("GALILEO", array) == 3
    assert cs.bsrchc("Galileo", array) == -1
    assert cs.bsrchc("BETHE", array) == -1


# This one had to be changed. Alex's version also requires the dimension of
# the array.
def test_bsrchd():
    array = np.array([-11.0, 0.0, 22.0, 750.0])
    assert cs.bsrchd(-11.0, array) == 0
    assert cs.bsrchd(22.0, array) == 2
    assert cs.bsrchd(751.0, array) == -1
    
    
# This one had to be changed. Alex's version also requires the dimension of
# the array.
def test_bsrchi():
    array = np.array([-11, 0, 22, 750])
    assert cs.bsrchi(-11, array) == 0
    assert cs.bsrchi(22, array) == 2
    assert cs.bsrchi(751, array) == -1
    
    
def test_ccifrm():
    frcode, frname, center = cs.ccifrm(2, 3000)
    assert frname == "ITRF93"
    assert frcode == 13000
    assert center == 399
    
    
def test_cgv2el():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [-1.0, 1.0, -1.0]
    ellipse = cs.cgv2el(center, vec1, vec2)
    expected_s_major = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expected_s_minor = [0.0, np.sqrt(2.0), 0.0]
    expected_center = [-1.0, 1.0, -1.0]
    npt.assert_array_almost_equal(expected_center, ellipse[0:3])
    npt.assert_array_almost_equal(expected_s_major, ellipse[3:6])
    npt.assert_array_almost_equal(expected_s_minor, ellipse[6:9])
    






