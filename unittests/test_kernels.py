################################################################################

import numpy as np
import numpy.testing as npt
import numbers
import platform
from pathlib import Path

from cspyce import *
import pytest

PATH_ = Path(os.path.realpath(__file__)).parent.parent / "unittest_support"

def furnish_kernels():
    furnsh(PATH_ / 'naif0012.tls')
    furnsh(PATH_ / 'pck00010.tpc')
    furnsh(PATH_ / 'de432s.bsp')
    furnsh(PATH_ / 'sat164.bsp')
    furnsh(PATH_ / 'earth_000101_180317_171224.bpc')

    furnsh(PATH_ / 'cas_v40.tf')
    furnsh(PATH_ / 'cas00171.tsc')
    furnsh(PATH_ / '17257_17262ra.bc')
    furnsh(PATH_ / '171106R_SCPSE_17224_17258.bsp')
    furnsh(PATH_ / 'cas_iss_v10.ti')


def unload_kernels():
    unload(PATH_ / 'naif0012.tls')
    unload(PATH_ / 'pck00010.tpc')
    unload(PATH_ / 'de432s.bsp')
    unload(PATH_ / 'sat164.bsp')
    unload(PATH_ / 'earth_000101_180317_171224.bpc')

    unload(PATH_ / 'cas_v40.tf')
    unload(PATH_ / 'cas00171.tsc')
    unload(PATH_ / '17257_17262ra.bc')
    unload(PATH_ / '171106R_SCPSE_17224_17258.bsp')
    unload(PATH_ / 'cas_iss_v10.ti')


@pytest.fixture(autouse=True)
def kernels():
    furnish_kernels()
    yield
    unload_kernels()

@pytest.fixture
def CASSINI_ET():
    return 17.65 * 365.25 * 86400.

@pytest.fixture
def CASSINI_ET2(CASSINI_ET):
    return CASSINI_ET + 86400

@pytest.fixture
def eps():
    if platform.machine() == 'arm64':
        # TODO(fy,rf,mrs): This code gives slightly different results on MacOS Arm64.
        # This lowering of expectations needs to be investigated. Is it Mac only?
        eps = 1e-5
    else:
        eps = 5e-8
    return eps


class Test_cspyce1_kernels:
    def assertAllEqual(self, arg1, arg2, tol=1.e-15, frac=False):
        if isinstance(arg1, list):
            assert type(arg2) == list
            assert len(arg1) == len(arg2)
            for (item1, item2) in zip(arg1, arg2):
                self.assertAllEqual(item1, item2, tol, frac)

        elif isinstance(arg1, np.ndarray):
            arg1 = np.array(arg1)
            arg2 = np.array(arg2)
            assert arg1.shape == arg2.shape
            arg1 = arg1.flatten()
            arg2 = arg2.flatten()
            for (x1, x2) in zip(arg1, arg2):
                if isinstance(x1, numbers.Real):
                    if frac:
                        assert abs(x1 - x2) <= tol * abs(x1 + x2) / 2.
                    else:
                        assert abs(x1 - x2) <= tol
                else:
                    assert x1 == x2, tol

        elif isinstance(arg1, numbers.Real):
            if frac:
                assert abs(arg1 - arg2) <= tol * abs(arg1 + arg2) / 2.
            else:
                assert abs(arg1 - arg2) <= tol

        else:
            assert arg1 == arg2

    def assertAllClose(self, arg1, arg2, tol=1.e-8):
        return self.assertAllEqual(arg1, arg2, tol, frac=True)


    #### Not tested: dafbfs, dafcls, dafgda, dafgn, dafgs, daffna, dafopr, dafus
    #### Not tested: stcf01, stcg01, stcl01, stcl01

    def test_gipool(self):
        # This test adapted from pipool_c.html
        pipool('FRAME_MYTOPO', [1500000])
        pcpool('FRAME_1500000_NAME', ['MYTOPO'])
        pipool('FRAME_1500000_CLASS', [4])
        pipool('FRAME_1500000_CLASS_ID', [1500000])
        pipool('FRAME_1500000_CENTER', [300000])
        pcpool('OBJECT_300000_FRAME', ['MYTOPO'])
        pcpool('TKFRAME_MYTOPO_RELATIVE', ['J2000'])
        pcpool('TKFRAME_MYTOPO_SPEC', ['ANGLES'])
        pcpool('TKFRAME_MYTOPO_UNITS', ['DEGREES'])
        pipool('TKFRAME_MYTOPO_AXES', [3, 2, 3])
        pdpool('TKFRAME_MYTOPO_ANGLES', [22.2, 0., -22.2])
        et = 0.

        rmat = pxform('J2000', 'MYTOPO', et)
        self.assertAllEqual(rmat, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        et = 10. * 365. * 86400.
        rmat = pxform('J2000', 'MYTOPO', et)
        self.assertAllEqual(rmat, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        pcpool('CTEST', ['LARRY', 'MOE', 'CURLY'])
        pipool('ITEST', [3141, 186, 282])
        pdpool('DTEST', [3.1415, 186.282, .0175])

        # This doesn't work, but calls to expool below work fine.
        #     self.assertTrue(expool('CTEST'))
        assert expool('ITEST')
        assert expool('DTEST')
        assert not expool('DTESTxxx')

        assert dtpool('CTEST') == [3, 'C']
        assert dtpool('ITEST') == [3, 'N']
        assert dtpool('DTEST') == [3, 'N']
        with pytest.raises(KeyError):
            dtpool('DTESTxxx')

        assert dtpool.flag('CTEST') == [True, 3, 'C']
        assert dtpool.flag('ITEST') == [True, 3, 'N']
        assert dtpool.flag('DTEST') == [True, 3, 'N']
        assert dtpool.flag('DTESTxxx')[0] == False

        assert list(gipool('ITEST')) == [3141, 186, 282]
        assert list(gdpool('DTEST')) == [3.1415, 186.282, .0175]
        assert list(gcpool('CTEST')) == ['LARRY', 'MOE', 'CURLY']

        assert list(gipool('ITEST', 1)) == [186, 282]
        assert list(gdpool('DTEST', 1)) == [186.282, .0175]
        assert list(gcpool('CTEST', 1)) == ['MOE', 'CURLY']

        with pytest.raises(KeyError):
            gipool('ITESTxxx')
        with pytest.raises(KeyError):
            gdpool('DTESTxxx')
        with pytest.raises(KeyError):
            gcpool('CTESTxxx')

        assert len(gipool.flag('ITEST')) == 2
        assert len(gdpool.flag('DTEST')) == 2
        assert len(gcpool.flag('CTEST')) == 2

        assert gipool.flag('ITEST')[-1]
        assert gdpool.flag('DTEST')[-1]
        assert gcpool.flag('CTEST')[-1]
        assert not gcpool.flag('CTESTxxx')[-1]

    def test_clpool_dlpool(self):
        #### clpool, ldpool
        assert bodfnd(599, 'RADII')
        assert bodfnd(699, 'RADII')
        clpool()
        assert not bodfnd(699, 'RADII')
        ldpool(PATH_ / 'pck00010.tpc')
        assert bodfnd(699, 'RADII')

    def test_expool_dtpool(self):
        assert expool('BODY699_RADII')
        assert not expool('BODY699_RADIIxxx')
        assert dtpool_error('BODY699_RADII') == [3, 'N']
        assert dtpool.flag('BODY699_RADII') == [True, 3, 'N']
        assert dtpool.flag('BODY699_RADIIxxx')[0] == False
        with pytest.raises(KeyError):
            dtpool_error('BODY699_RADIIxxx')

    def test_gnpool(self):
        assert set(gnpool('BODY699*RA*')) == set(['BODY699_POLE_RA',
                                                          'BODY699_RADII'])
        with pytest.raises(KeyError):
            gnpool('BODY699*RAxxx*')

        assert set(gnpool.flag('BODY699*RA*')[0]) == \
                         set(['BODY699_POLE_RA', 'BODY699_RADII'])
        assert gnpool.flag('BODY699*RA*')[1]
        assert not gnpool.flag('BODY699*RAxxx*')[1]

    def test_stpool(self):
        SPK_FILES = ['this_is_the_full_path_specification_*',
                     'of_a_file_with_a_long_name',
                     'this_is_the_full_path_specification_*',
                     'of_a_second_file_with_a_very_long_*',
                     'name']
        pcpool('SPK_FILES', SPK_FILES)

        assert stpool('SPK_FILES', 0, '*') == SPK_FILES[0][:-1] + SPK_FILES[1]
        assert stpool('SPK_FILES', 1, '*') == \
                         SPK_FILES[2][:-1] + SPK_FILES[3][:-1] + SPK_FILES[4]
        with pytest.raises(KeyError):
            stpool('SPK_FILES', 2, '*')

        assert stpool.flag('SPK_FILES', 0, '*') == \
                         [SPK_FILES[0][:-1] + SPK_FILES[1], True]
        assert stpool.flag('SPK_FILES', 1, '*') == \
                         [SPK_FILES[2][:-1] + SPK_FILES[3][:-1] + SPK_FILES[4], True]
        assert not stpool.flag('SPK_FILES', 2, '*')[1]

    def test_bodc2n_bodn2c_bodc2s_bods2c(self):
        INTMAX = intmax()
        #### bodc2n, bodn2c, bodc2s, bods2c
        boddef('BIG!', -INTMAX)

        assert bodc2n.flag(699) == ['SATURN', True]
        assert bodc2n_error(699) == 'SATURN'
        assert bodc2n.flag(INTMAX)[1] == False
        with pytest.raises(Exception):
            bodc2n_error(INTMAX)

        assert bodn2c.flag('SATuRN ') == [699, True]
        assert bodn2c_error('SATURN') == 699
        assert bodn2c.flag('foobar')[1] == False
        with pytest.raises(Exception):
            bodn2c_error('foobar')

        assert bodc2s(699) == 'SATURN'
        assert bodc2s(INTMAX) == str(INTMAX)

        assert bods2c.flag('SATuRN ') == [699, True]
        assert bods2c_error('SATURN') == 699
        assert bods2c.flag('foobar')[1] == False
        with pytest.raises(Exception):
            bods2c_error('foobar')
        assert bods2c_error('  699 ') == 699
        assert bods2c_error(str(INTMAX)) == INTMAX

        self.assertAllEqual(bltfrm(1).as_array(), range(1, 22), 0)

        #  self.assertAllEqual(kplfrm(1), range(1,22), 0)
        boddef('BIG!', INTMAX)

        assert bodc2n.flag(INTMAX) == ['BIG!', True]
        assert bodc2n_error(INTMAX) == 'BIG!'

        assert bodn2c.flag('BiG! ') == [INTMAX, True]
        assert bodn2c_error('BIG!') == INTMAX

        assert bodc2s(INTMAX) == 'BIG!'
        assert bods2c.flag('BiG! ') == [INTMAX, True]
        assert bods2c_error('BIG!') == INTMAX

    def test_bodfnd(self):
        INTMIN = intmin()
        assert bodfnd(699, 'RADII')
        assert not bodfnd(699, 'RADIIxxx')
        assert not bodfnd(INTMIN, 'RADII')

    def test_bodvcd(self):
        assert bodvcd(699, 'RADII')[0] == 60268.
        assert bodvcd(699, 'RADII')[1] == 60268.
        assert bodvcd(699, 'RADII')[2] == 54364.
        with pytest.raises(KeyError):
            bodvcd(699, 'RADIIxxx')

    def test_bodvrd(self):
        assert bodvrd('SATURN', 'RADII')[0] == 60268.
        assert bodvrd('SATURN', 'RADII')[1] == 60268.
        assert bodvrd('SATURN', 'RADII')[2] == 54364.
        with pytest.raises(KeyError):
            bodvrd('SATURN', 'RADIIxxx')

    def test_bodvar(self):
        assert bodvar(699, 'RADII')[0] == 60268.
        assert bodvar(699, 'RADII')[1] == 60268.
        assert bodvar(699, 'RADII')[2] == 54364.
        with pytest.raises(KeyError):
            bodvar(699, 'RADIIxxx')

    def test_cidfrm(self):
        INTMIN = intmin()
        assert cidfrm.flag(699) == [10016, 'IAU_SATURN', True]
        assert cidfrm_error(699) == [10016, 'IAU_SATURN']
        assert cidfrm.flag(INTMIN)[2] == False
        with pytest.raises(KeyError):
            cidfrm_error(INTMIN)

    def test_ccifrm(self):
        INTMIN = intmin()
        assert cidfrm.flag(INTMIN)[2] == False
        assert ccifrm.flag(2, 699) == [10016, 'IAU_SATURN', 699, True]
        assert ccifrm_error(2, 699) == [10016, 'IAU_SATURN', 699]
        assert ccifrm.flag(2, INTMIN)[3] == False
        with pytest.raises(ValueError):
            ccifrm_error(INTMIN, INTMIN)

    def test_ckcov(self):
        values = ckcov(PATH_ / '17257_17262ra.bc', -82000, False, 'INTERVAL', 1., 'SCLK')
        npt.assert_array_equal(values.as_intervals(),
                               [[304593554335.0, 304610188193.0],
                                [304610195359.0, 304622337377.0],
                                [304622354271.0, 304625376609.0]])

        values = ckcov.flag(PATH_ / '17257_17262ra.bc', 1, False, 'INTERVAL', 1., 'SCLK')
        assert values.card == 0

        with pytest.raises(KeyError):
            ckcov_error(PATH_ / '17257_17262ra.bc', 1, False, 'INTERVAL', 1., 'SCLK')

        #### pckcov, pckfrm
        with pytest.raises(IOError):
            pckcov(PATH_ / 'pck00010.tpc', 10016)

        frames = pckfrm(PATH_ / 'earth_000101_180317_171224.bpc')
        limits = [-4.31358161e+04, 5.74516869e+08]
        self.assertAllClose(pckcov(PATH_ / 'earth_000101_180317_171224.bpc', 3000).as_array(),
                            limits)

    def test_ckgp_ckgpav(self):
        sclk = 304593554335.
        (array1a, sclk1, found1) = ckgp.flag(-82000, sclk, 1., 'J2000')
        (array2a, array2b, sclk2, found2) = ckgpav.flag(-82000, sclk, 1., 'J2000')

        assert found1
        assert found2

        (array1a, sclk1,) = ckgp(-82000, sclk, 1., 'J2000')
        (array2a, array2b, sclk2) = ckgpav(-82000, sclk, 1., 'J2000')

        assert abs(sclk1 - sclk1) <= 1.
        assert sclk1 == sclk2
        self.assertAllEqual(array1a, array2a, 0.)

        result2a = np.array([[-0.099802, -0.37245036, -0.92267019],
                             [-0.03169184, -0.92563955, 0.37707699],
                             [-0.99450248, 0.06687415, 0.08057704]])

        result2b = np.array([3.46254953e-05, 5.05354838e-06, -1.12043171e-05])

        self.assertAllEqual(array2a, result2a, 5.e-9)
        self.assertAllEqual(array2b, result2b, 4.e-14)

        # sclk is 0.
        assert not ckgp.flag(-82000, 0., 1., 'J2000')[-1]
        assert not ckgpav.flag(-82000, 0., 1., 'J2000')[-1]

        with pytest.raises(IOError):
            ckgp_error(-82000, 0., 1., 'J2000')
        with pytest.raises(IOError):
            ckgpav_error(-82000, 0., 1., 'J2000')

        # sclk is 0.
        assert not ckgp.flag(-82000, 0., 1., 'J2000')[-1]
        assert not ckgpav.flag(-82000, 0., 1., 'J2000')[-1]

        with pytest.raises(IOError):
            ckgp_error(-82000, 0., 1., 'J2000')
        with pytest.raises(IOError):
            ckgpav_error(-82000, 0., 1., 'J2000')

        sclk = sclk + 100. * np.arange(10)
        (array1ax, sclk1x) = ckgp_vector(-82000, sclk, 1., 'J2000')
        (array2ax, array2bx, sclk2x) = ckgpav_vector(-82000, sclk, 1., 'J2000')

        assert array1ax.shape == (10, 3, 3)
        assert array2ax.shape == (10, 3, 3)
        assert array2bx.shape == (10, 3)
        self.assertAllEqual(array1ax[0], array1a, 0)
        self.assertAllEqual(array2ax[0], array2a, 0)
        self.assertAllEqual(array2bx[0], array2b, 0)

        sclk = sclk + 100. * np.arange(10)
        (array1ax, sclk1x, found1x) = ckgp_vector.flag(-82000, sclk, 1., 'J2000')
        (array2ax, array2bx, sclk2x, found2x) = ckgpav_vector.flag(-82000, sclk, 1., 'J2000')

        assert array1ax.shape == (10, 3, 3)
        assert array2ax.shape == (10, 3, 3)
        assert array2bx.shape == (10, 3)
        self.assertAllEqual(array1ax[0], array1a, 0)
        self.assertAllEqual(array2ax[0], array2a, 0)
        self.assertAllEqual(array2bx[0], array2b, 0)
        assert np.all(found1x)
        assert np.all(found2x)

    def test_ckobj(self):
        assert ckobj(PATH_ / '17257_17262ra.bc').as_array() == [-82000]

    def test_cnmfrm(self):
        assert cnmfrm('SATURN') == [10016, 'IAU_SATURN']
        assert cnmfrm.flag('SATURN')[-1]
        assert not cnmfrm.flag('foo')[-1]
        with pytest.raises(KeyError):
            cnmfrm_error('foo')

    def test_dpgrdr_drdpgr(self):
        self.assertAllEqual(dpgrdr('saturn', 1., 0., 0., 1., 0.), [[0, -1, 0],
                                                                   [0, 0, 1],
                                                                   [1, 0, 0]])
        self.assertAllEqual(drdpgr('saturn', 1., 0., 0., 1., 0.),
                            [[-0.84147098, 0., 0.54030231],
                             [-0.54030231, 0., -0.84147098],
                             [0., 1., 0.]], 5e-9)
        assert dpgrdr_vector('saturn', 1., 0., [1, 2, 3, 4], 1., 0.).shape == \
                         (4, 3, 3)
        assert drdpgr_vector('saturn', 1., 0., 0., 1., [0.1, 0.02, 0.03, 0.04]).shape == (4, 3, 3)

    def test_delte_t(self):
        d = deltet(0., 'UTC')
        self.assertAllEqual(d - 64.1839272847, 0., 4.e-11)
        self.assertAllEqual(deltet_vector(np.arange(10), 'UTC'), 10 * [d], 4.e-9)

    def test_edterm(self):
        results = edterm('UMBRAL', 'SUN', 'EARTH', 0., 'IAU_EARTH', 'LT+S',
                         'MOON', 100)
        assert len(results) == 3
        assert np.shape(results[0]) == ()
        assert results[1].shape == (3,)
        assert results[2].shape == (100, 3)

    def test_et2lst(self):
        assert et2lst(0., 399, 0., 'PLANETOCENTRIC') == \
                         [11, 55, 27, '11:55:27', '11:55:27 A.M.']
        assert et2lst(0., 399, 43200., 'PLANETOCENTRIC') == \
                         [23, 46, 9, '23:46:09', '11:46:09 P.M.']

    def test_et2utc_utc2et_str2et_etcal(self):
        utc = '2000-01-01T11:58:55.816'
        assert et2utc(0., 'ISOC', 3) == utc
        assert abs(utc2et(utc)) < 0.5e-3
        assert abs(str2et(utc)) < 0.5e-3
        assert etcal(0.) == '2000 JAN 01 12:00:00.000'

    def test_frmnam_namfrm_frinfo(self):
        INTMAX = intmax()
        assert frmnam(10016) == 'IAU_SATURN'
        assert frmnam.flag(10016) == 'IAU_SATURN'
        assert frmnam.flag(INTMAX) == ''
        with pytest.raises(KeyError):
            frmnam_error(INTMAX)

        assert namfrm('IAU_SATURN') == 10016
        assert namfrm.flag('IAU_SATURN') == 10016
        assert namfrm.flag('xxxxx') == 0
        with pytest.raises(KeyError):
            namfrm_error('xxxxx')

        assert frinfo(10016) == [699, 2, 699]
        assert frinfo.flag(10016) == [699, 2, 699, True]
        assert not frinfo.flag(INTMAX)[-1]
        with pytest.raises(KeyError):
            frinfo(INTMAX)

    def test_frmchg_sxform_pxform_xf2rav_pxfrm2_refchg(self):
        sat0a = frmchg(10016, 1, 0.)
        sat1a = frmchg(10016, 1, 86400.)
        sat0b = sxform('IAU_SATURN', 'J2000', 0.)
        sat1b = sxform('IAU_SATURN', 'J2000', 86400.)
        sat0c = pxform('IAU_SATURN', 'J2000', 0.)
        sat1c = pxform('IAU_SATURN', 'J2000', 86400.)
        sat0d = pxfrm2('IAU_SATURN', 'J2000', 0., 0.)
        sat1d = pxfrm2('IAU_SATURN', 'J2000', 86400., 86400.)
        sat0e = refchg(10016, 1, 0.)
        sat1e = refchg(10016, 1, 86400.)

        self.assertAllEqual(sat0a[:3, :3], sat0b[:3, :3], 0)
        self.assertAllEqual(sat0a[:3, :3], sat0c, 0)
        self.assertAllEqual(sat0a[:3, :3], sat0d, 0)
        self.assertAllEqual(sat0a[:3, :3], sat0e, 0)
        self.assertAllEqual(sat0a[:3, :3], sat0a[3:, 3:], 0)  # true even for rotating frames

        self.assertAllEqual(sat1a[:3, :3], sat1b[:3, :3], 0)
        self.assertAllEqual(sat1a[:3, :3], sat1c, 0)
        self.assertAllEqual(sat1a[:3, :3], sat1d, 0)
        self.assertAllEqual(sat1a[:3, :3], sat1e, 0)
        self.assertAllEqual(sat1a[:3, :3], sat1a[3:, 3:], 0)  # true even for rotating frames

        (mat0a, vec0a) = xf2rav(sat0a)
        (mat1a, vec1a) = xf2rav(sat1a)
        (mat0b, vec0b) = xf2rav(sat0b)
        (mat1b, vec1b) = xf2rav(sat1b)

        self.assertAllEqual(sat0a[:3, :3], mat0a, 0)
        self.assertAllEqual(sat1a[:3, :3], mat1a, 0)
        self.assertAllEqual(sat0b[:3, :3], mat0b, 0)
        self.assertAllEqual(sat1b[:3, :3], mat1b, 0)

        # Make sure that non-rotating frames have the form we're expecting
        non_rotate = frmchg(1, 2, 0.)  # J2000 and B1950 are both fixed
        self.assertAllEqual(non_rotate[:3, :3], non_rotate[3:, 3:])
        assert not np.any(non_rotate[:3, 3:])  # top left and bottom right are zero
        assert not np.any(non_rotate[3:, :3])
        non_rotate_matrix, non_rotate_vec = xf2rav(non_rotate)
        self.assertAllEqual(non_rotate[:3, :3], non_rotate_matrix)
        self.assertAllEqual(non_rotate_vec, [0., 0., 0.])

        self.assertAllEqual(vec0b, vec1b, 1.e-13)

        sat01a = frmchg_vector(10016, 1, [0., 86400.])
        sat01b = sxform_vector('IAU_SATURN', 'J2000', [0., 86400.])
        sat01c = pxform_vector('IAU_SATURN', 'J2000', [0., 86400.])
        sat01d = pxfrm2_vector('IAU_SATURN', 'J2000', [0., 86400.], [0., 86400.])
        sat01e = refchg_vector(10016, 1, [0., 86400.])

        self.assertAllEqual(sat01a, [sat0a, sat1a], 0)
        self.assertAllEqual(sat01b, [sat0b, sat1b], 0)
        self.assertAllEqual(sat01c, [sat0c, sat1c], 0)
        self.assertAllEqual(sat01d, [sat0d, sat1d], 0)
        self.assertAllEqual(sat01e, [sat0e, sat1e], 0)

        (mat01b, vec01b) = xf2rav_vector(sat01b)
        self.assertAllEqual(mat01b, [mat0b, mat1b], 0)
        self.assertAllEqual(vec01b, [vec0b, vec1b], 0)

    def test_pgrrec_recpgr(self):
        #### pgrrec, recpgr
        self.assertAllEqual(pgrrec('MIMAS', 0, 0, 1, 1, 0.1), [2, 0, 0])
        self.assertAllEqual(recpgr('MIMAS', [2, 0, 0], 1, 0.1), [0, 0, 1])

        self.assertAllEqual(pgrrec_vector('MIMAS', [0, 0], 0, 1, 1, 0.1), 2 * [[2, 0, 0]])
        self.assertAllEqual(recpgr_vector('MIMAS', [2, 0, 0], [1, 1], 0.1),
                            [[0, 0], [0, 0], [1, 1]])

    def test_lspcn(self):
        Y2005 = 5 * 365.25 * 86400.
        Y2006 = 6 * 365.25 * 86400.
        self.assertAllEqual(lspcn('SATURN', Y2005, 'LT+S'), 5.23103124275, 1.e-11)
        self.assertAllEqual(lspcn('SATURN', Y2006, 'LT+S'), 5.46639556423, 1.e-11)
        self.assertAllEqual(lspcn_vector('SATURN', Y2006, 'LT+S'), 5.46639556423, 1.e-11)
        self.assertAllEqual(lspcn_vector('SATURN', [Y2005, Y2006], 'LT+S'),
                            [5.23103124275, 5.46639556423], 1.e-11)

    def test_latsrf(self):  # no vector version
        Y2005 = 5 * 365.25 * 86400.
        Y2006 = 6 * 365.25 * 86400.
        mimas = bodn2c('MIMAS')
        (a, b, C) = bodvcd(mimas, 'RADII')
        lonlats = np.array([[0, 0], [90, 0], [180, 0], [270, 0], [0, -90], [0, 90]]) * rpd()
        results5 = latsrf('ELLIPSOID', 'MIMAS', Y2005, 'IAU_MIMAS', lonlats)
        results6 = latsrf('ELLIPSOID', 'MIMAS', Y2006, 'IAU_MIMAS', lonlats)

        target = [[a, 0, 0], [0, b, 0], [-a, 0, 0], [0, -b, 0], [0, 0, -C], [0, 0, C]]
        self.assertAllEqual(results5, target, 4e-14)
        self.assertAllEqual(results6, target, 4e-14)

    def test_ltime(self, CASSINI_ET):
        self.assertAllEqual(ltime(CASSINI_ET, -82, '->', 399),
                            [556996483.4720103, 4843.472010222729], 1.e-7)
        self.assertAllEqual(ltime(CASSINI_ET, -82, '<-', 399),
                            [556986797.4373786, 4842.562621312754], 1.e-7)
        self.assertAllEqual(ltime_vector(CASSINI_ET, -82, '<-', 399),
                            [556986797.4373786, 4842.562621312754], 1.e-7)
        self.assertAllEqual(ltime_vector(3 * [CASSINI_ET], -82, '<-', 399),
                            [3 * [556986797.4373786], 3 * [4842.562621312754]], 1.e-7)

    def test_spkcov_spkobj(self):
        #### spkcov, spkobj
        with pytest.raises(IOError):
            spkcov('foo.bsp', -82)

        spkpath = PATH_ / '171106R_SCPSE_17224_17258.bsp'
        with pytest.raises(KeyError):
            spkcov(spkpath, 401)

        limits = [5.55782400e+08, 5.58745200e+08]
        self.assertAllEqual(spkcov(spkpath, -82).as_intervals(), [limits], 1.)
        self.assertAllEqual(spkcov(spkpath, 699).as_intervals(), [limits], 1.)

        self.assertAllEqual(spkcov.flag(spkpath, 699).as_intervals(), [limits], 1.)
        self.assertAllEqual(spkcov.flag(spkpath, 401).as_intervals(), np.empty((0, 2)))

        bodies = set([-82, 301, 399, 699] + list(range(1, 11)) +
                     list(range(601, 613)) +
                     list(range(615, 618)))
        temp = spkobj(PATH_ / '171106R_SCPSE_17224_17258.bsp')
        assert set(temp) == bodies

    def test_illum_illumf_illumg_ilumin_phaseg(self, CASSINI_ET, CASSINI_ET2, eps):
        trgepc = 556991636.744989
        srfvec = [-898913.54085495, -158678.38639218, -344986.06074434]
        phase = 2.3355683234002207
        incdnc = 2.6877326371660395
        emissn = 0.39969284462247634
        visibl = True
        lit = False

        trgepc2 = 557078039.2141582
        srfvec2 = [-197119.85363806, 61957.21359249, 113170.06834279]
        phase2 = 3.0776373659048852
        incdnc2 = 2.6248933305972493
        emissn2 = 0.5795501233580607
        visibl2 = True
        lit2 = False

        self.assertAllEqual(illum('mimas', CASSINI_ET, 'lt+S', 'cassini',
                                  [200, 0, 0]),
                            [phase, incdnc, emissn], eps)
        self.assertAllEqual(illumf('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                   'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc, srfvec, phase, incdnc, emissn, visibl, lit], eps)
        self.assertAllEqual(illumg('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                   'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc, srfvec, phase, incdnc, emissn], eps)
        self.assertAllEqual(ilumin('ellipsoid', 'mimas', CASSINI_ET,
                                   'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc, srfvec, phase, incdnc, emissn], eps)

        self.assertAllEqual(illum('mimas', CASSINI_ET2, 'lt+S', 'cassini',
                                  [200, 0, 0]),
                            [phase2, incdnc2, emissn2], eps)
        self.assertAllEqual(illumf('ellipsoid', 'mimas', 'sun', CASSINI_ET2,
                                   'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc2, srfvec2, phase2, incdnc2, emissn2, visibl2, lit2],
                            eps)
        self.assertAllEqual(illumg('ellipsoid', 'mimas', 'sun', CASSINI_ET2,
                                   'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc2, srfvec2, phase2, incdnc2, emissn2], eps)
        self.assertAllEqual(ilumin('ellipsoid', 'mimas', CASSINI_ET2,
                                   'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc2, srfvec2, phase2, incdnc2, emissn2], eps)

        self.assertAllEqual(illum_vector('mimas', CASSINI_ET, 'lt+S', 'cassini',
                                         [200, 0, 0]),
                            [phase, incdnc, emissn], eps)
        self.assertAllEqual(illumf_vector('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc, srfvec, phase, incdnc, emissn, visibl, lit], eps)
        self.assertAllEqual(illumg_vector('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc, srfvec, phase, incdnc, emissn], eps)
        self.assertAllEqual(ilumin_vector('ellipsoid', 'mimas', CASSINI_ET,
                                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [trgepc, srfvec, phase, incdnc, emissn], eps)

        self.assertAllEqual(illum_vector('mimas', [CASSINI_ET], 'lt+S', 'cassini',
                                         [200, 0, 0]),
                            [[phase], [incdnc], [emissn]], eps)
        self.assertAllEqual(illumf_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET],
                                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [[trgepc], [srfvec], [phase], [incdnc], [emissn], [visibl],
                             [lit]], eps)
        self.assertAllEqual(illumg_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET],
                                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [[trgepc], [srfvec], [phase], [incdnc], [emissn]], eps)
        self.assertAllEqual(ilumin_vector('ellipsoid', 'mimas', [CASSINI_ET],
                                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [[trgepc], [srfvec], [phase], [incdnc], [emissn]], eps)

        self.assertAllEqual(
            illum_vector('mimas', [CASSINI_ET, CASSINI_ET2], 'lt+S', 'cassini',
                         [200, 0, 0]),
            [[phase, phase2], [incdnc, incdnc2], [emissn, emissn2]], eps)
        self.assertAllEqual(
            illumf_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET, CASSINI_ET2],
                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
            [[trgepc, trgepc2], [srfvec, srfvec2], [phase, phase2], [incdnc, incdnc2],
             [emissn, emissn2], [visibl, visibl2], [lit, lit2]], eps)
        self.assertAllEqual(
            illumg_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET, CASSINI_ET2],
                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
            [[trgepc, trgepc2], [srfvec, srfvec2], [phase, phase2], [incdnc, incdnc2],
             [emissn, emissn2]], eps)
        self.assertAllEqual(ilumin_vector('ellipsoid', 'mimas', [CASSINI_ET, CASSINI_ET2],
                                          'iau_mimas', 'lt+s', 'cassini', [200, 0, 0]),
                            [[trgepc, trgepc2], [srfvec, srfvec2], [phase, phase2],
                             [incdnc, incdnc2], [emissn, emissn2]], eps)

    def test_phaseq(self, CASSINI_ET, CASSINI_ET2, eps):
        phase = 2.33564238748
        phase2 = 3.07809474673

        self.assertAllEqual(phaseq(CASSINI_ET, 'mimas', 'sun', 'cassini', 'lt+s'),
                            phase, eps)
        self.assertAllEqual(phaseq(CASSINI_ET2, 'mimas', 'sun', 'cassini', 'lt+s'),
                            phase2, eps)

        self.assertAllEqual(phaseq_vector(CASSINI_ET, 'mimas', 'sun', 'cassini', 'lt+s'),
                            phase, eps)

        self.assertAllEqual(
            phaseq_vector([CASSINI_ET, CASSINI_ET2], 'mimas', 'sun', 'cassini', 'lt+s'),
            [phase, phase2], eps)

    def test_sce2c_sce2s_sce2t_scdecd_sct2e_scencd_scs2e_sctiks_scfmt_scpart(self, CASSINI_ET, CASSINI_ET2):
        scdp = 3.04176877635e+11
        scdp2 = 3.04198996178e+11
        sclk = '1/1882414947.067'
        sclk2 = '1/1882501347.210'

        self.assertAllEqual(sce2c(-82, CASSINI_ET), scdp, 1.)
        self.assertAllEqual(sce2c(-82, CASSINI_ET2), scdp2, 1.)
        self.assertAllEqual(sce2s(-82, CASSINI_ET), sclk)
        self.assertAllEqual(sce2s(-82, CASSINI_ET2), sclk2)
        self.assertAllEqual(sce2t(-82, CASSINI_ET), scdp, 1.)
        self.assertAllEqual(sce2t(-82, CASSINI_ET2), scdp2, 1.)
        self.assertAllEqual(scdecd(-82, scdp), sclk)
        self.assertAllEqual(scdecd(-82, scdp2), sclk2)
        self.assertAllEqual(sct2e(-82, scdp), CASSINI_ET, 1.)
        self.assertAllEqual(sct2e(-82, scdp2), CASSINI_ET2, 1.)
        self.assertAllEqual(scencd(-82, sclk), scdp, 1.)
        self.assertAllEqual(scencd(-82, sclk2), scdp2, 1.)
        self.assertAllEqual(scs2e(-82, sclk), CASSINI_ET, 1.)
        self.assertAllEqual(scs2e(-82, sclk2), CASSINI_ET2, 1.)

        self.assertAllEqual(sctiks(-82, "1.000"), 256.)
        self.assertAllEqual(sctiks(-82, "0.001"), 1.)

        self.assertAllEqual(scfmt(-82, scdp), '1188190928.067')
        self.assertAllEqual(scfmt(-82, scdp2), '1188277328.210')

        parts = [[1.77721349e+11], [1.09951163e+12]]
        self.assertAllEqual(scpart(-82), parts, 30000.)

        self.assertAllEqual(sce2c_vector(-82, CASSINI_ET), scdp, 1.)
        self.assertAllEqual(sce2c_vector(-82, CASSINI_ET2), scdp2, 1.)
        self.assertAllEqual(sce2t_vector(-82, CASSINI_ET), scdp, 1.)
        self.assertAllEqual(sce2t_vector(-82, CASSINI_ET2), scdp2, 1.)
        self.assertAllEqual(sct2e_vector(-82, scdp), CASSINI_ET, 1.)
        self.assertAllEqual(sct2e_vector(-82, scdp2), CASSINI_ET2, 1.)

        self.assertAllEqual(sce2c_vector(-82, [CASSINI_ET]), [scdp], 1.)
        self.assertAllEqual(sce2c_vector(-82, [CASSINI_ET2]), [scdp2], 1.)
        self.assertAllEqual(sce2t_vector(-82, [CASSINI_ET]), [scdp], 1.)
        self.assertAllEqual(sce2t_vector(-82, [CASSINI_ET2]), [scdp2], 1.)
        self.assertAllEqual(sct2e_vector(-82, [scdp]), [CASSINI_ET], 1.)
        self.assertAllEqual(sct2e_vector(-82, [scdp2]), [CASSINI_ET2], 1.)

        self.assertAllEqual(sce2c_vector(-82, [CASSINI_ET, CASSINI_ET2]), [scdp, scdp2], 1.)
        self.assertAllEqual(sce2t_vector(-82, [CASSINI_ET, CASSINI_ET2]), [scdp, scdp2], 1.)
        self.assertAllEqual(sct2e_vector(-82, [scdp, scdp2]), [CASSINI_ET, CASSINI_ET2], 1.)

    def test_spkssb_spkacs_spkapo_spkez_spkezr_spkpos(self, CASSINI_ET, CASSINI_ET2):
        #### spkssb, spkacs, spkapo, spkez, spkezr, spkpos
        xssb = [-9.35325266e+07, -1.38980049e+09, -5.69362184e+08, 1.00994262e+01,
                5.57457613e+00, -1.32361199e+00]
        xssb2 = [-9.28933887e+07, -1.38916427e+09, -5.69894015e+08, -8.14701094e-01,
                 -1.90665286e+01, -8.26491731e+00]

        ssb = spkssb(-82, CASSINI_ET, 'J2000')
        ssb2 = spkssb(-82, CASSINI_ET2, 'J2000')
        self.assertAllClose(spkssb(-82, CASSINI_ET, 'J2000'), xssb)
        self.assertAllClose(spkssb(-82, CASSINI_ET2, 'J2000'), xssb2)

        xstate = [-5.80013005e+04, 8.94350415e+05, -3.86487455e+05,
                  -1.49765896e+01, -5.10106017e+00, 1.77874639e+00]
        xstate2 = [2.09801346e+04, 2.11762463e+05, 1.01477978e+05,
                   -3.43826105e+00, 1.42982547e+01, 8.91877142e+00]
        xlt = 3.255625500957274
        xdlt = -1.4972390244438447e-05
        xlt2 = 0.7864001637489081
        xdlt2 = 5.4624503604634114e-05

        (state, lt, dlt) = spkaps(601, CASSINI_ET, 'J2000', 'lt', ssb, [0, 0, 0])
        (state2, lt2, dlt2) = spkaps(601, CASSINI_ET2, 'J2000', 'lt', ssb2, [0, 0, 0])

        self.assertAllClose([state, lt, dlt], [xstate, xlt, xdlt])
        self.assertAllClose([state2, lt2, dlt2], [xstate2, xlt2, xdlt2])

        self.assertAllEqual(spkacs(601, CASSINI_ET, 'J2000', 'lt', -82),
                            [state, lt, dlt], 0)
        self.assertAllEqual(spkacs(601, CASSINI_ET2, 'J2000', 'lt', -82),
                            [state2, lt2, dlt2], 0)

        self.assertAllEqual(spkapo(601, CASSINI_ET, 'J2000', ssb, 'lt'),
                            [state[:3], lt], 0)
        self.assertAllEqual(spkapo(601, CASSINI_ET2, 'J2000', ssb2, 'lt'),
                            [state2[:3], lt2], 0)

        self.assertAllEqual(spkez(601, CASSINI_ET, 'J2000', 'lt', -82),
                            [state, lt], 0)
        self.assertAllEqual(spkez(601, CASSINI_ET2, 'J2000', 'lt', -82),
                            [state2, lt2], 0)

        self.assertAllEqual(spkezp(601, CASSINI_ET, 'J2000', 'lt', -82),
                            [state[:3], lt], 0)
        self.assertAllEqual(spkezp(601, CASSINI_ET2, 'J2000', 'lt', -82),
                            [state2[:3], lt2], 0)

        self.assertAllEqual(spkezr('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                            [state, lt], 0)
        self.assertAllEqual(spkezr('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                            [state2, lt2], 0)

        self.assertAllEqual(spkpos('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                            [state[:3], lt], 0)
        self.assertAllEqual(spkpos('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                            [state2[:3], lt2], 0)

        self.assertAllEqual(spkltc(601, CASSINI_ET, 'J2000', 'lt', ssb),
                            [state, lt, dlt], 0)
        self.assertAllEqual(spkltc(601, CASSINI_ET2, 'J2000', 'lt', ssb2),
                            [state2, lt2, dlt2], 0)

    def test_spkez_spkgeo_spkgps(self, CASSINI_ET, CASSINI_ET2):
        xstate = [-5.80171789e+04, 8.94351951e+05, -3.86485973e+05,
                  -1.49767494e+01, -5.10452110e+00, 1.77892184e+00]
        xstate2 = [2.09767900e+04, 2.11758713e+05, 1.01478492e+05,
                   -3.43824167e+00, 1.42971900e+01, 8.91882636e+00]
        xlt = 3.2556313860561055
        xlt2 = 0.7863886730607871

        (state, lt) = spkez(601, CASSINI_ET, 'J2000', 'none', -82)
        (state2, lt2) = spkez(601, CASSINI_ET2, 'J2000', 'none', -82)

        self.assertAllClose(spkez(601, CASSINI_ET, 'J2000', 'none', -82),
                            [xstate, xlt])
        self.assertAllClose(spkez(601, CASSINI_ET2, 'J2000', 'none', -82),
                            [xstate2, xlt2])

        self.assertAllEqual(spkgeo(601, CASSINI_ET, 'J2000', -82),
                            [state, lt], 0)
        self.assertAllEqual(spkgeo(601, CASSINI_ET2, 'J2000', -82),
                            [state2, lt2], 0)

        self.assertAllEqual(spkgps(601, CASSINI_ET, 'J2000', -82),
                            [state[:3], lt], 0)
        self.assertAllEqual(spkgps(601, CASSINI_ET2, 'J2000', -82),
                            [state2[:3], lt2], 0)

    def test_srfc2s_srfcss_srfs2c_srfscc(self):
        furnsh(PATH_ / 'phobos_surface.tm')  # Example from srfc2s_c.html
        assert srfc2s(1, 401) == 'PHOBOS GASKELL Q512'
        assert srfcss(1, 'phobos') == 'PHOBOS GASKELL Q512'
        assert srfs2c('PHOBOS GASKELL Q512', 'phobos') == 1
        assert srfscc('PHOBOS GASKELL Q512', 401) == 1

        with pytest.raises(KeyError):
            srfc2s(2, 401)
        with pytest.raises(KeyError):
            srfc2s(1, 402)
        with pytest.raises(KeyError):
            srfcss(2, 'phobos')
        with pytest.raises(KeyError):
            srfcss(1, 'deimos')
        with pytest.raises(KeyError):
            srfs2c('whatever', 'phobos')
        with pytest.raises(KeyError):
            srfs2c('PHOBOS GASKELL Q512', 'deimos')
        with pytest.raises(KeyError):
            srfscc('whatever', 401)
        with pytest.raises(KeyError):
            srfscc('PHOBOS GASKELL Q512', 402)

        self.assertAllEqual(srfc2s.flag(1, 401), ['PHOBOS GASKELL Q512', True])
        self.assertAllEqual(srfcss.flag(1, 'phobos'), ['PHOBOS GASKELL Q512', True])
        self.assertAllEqual(srfs2c.flag('PHOBOS GASKELL Q512', 'phobos'), [1, True])
        self.assertAllEqual(srfscc.flag('PHOBOS GASKELL Q512', 401), [1, True])

        assert not srfc2s.flag(2, 401)[1]
        assert not srfc2s.flag(1, 402)[1]
        assert not srfcss.flag(2, 'phobos')[1]
        assert not srfcss.flag(1, 'deimos')[1]
        assert not srfs2c.flag('whatever', 'phobos')[1]
        assert not srfs2c.flag('PHOBOS GASKELL Q512', 'deimos')[1]
        assert not srfscc.flag('whatever', 401)[1]
        assert not srfscc.flag('PHOBOS GASKELL Q512', 402)[1]

    def test_timdef(self):
        assert timdef('get', 'calendar') == 'GREGORIAN'
        assert timdef('get', 'system') == 'UTC'
        assert timdef('get', 'zone') == ''

        assert timdef('set', 'calendar', 'mixed ') == 'mixed '
        assert timdef('get', 'calendar') == 'MIXED'

        assert timdef('set', 'system', 'utC') == 'utC'
        assert timdef('get', 'system') == 'UTC'

        assert timdef('set', 'zone', 'PDT') == 'PDT'
        assert timdef('get', 'zone') == 'UTC-7'
        timdef('set', 'zone', 'UTC-0')

    def test_tparse(self):
        assert tparse('Tue Aug  6 11:10:57  1996') == -107398143.0
        assert tparse('JANUary 1, 2000 12:00') == 0.

        with pytest.raises(ValueError):
            tparse('Tue Aug  6 11:10:57  1996g')
        try:
            tparse('Tue Aug  6 11:10:57  1996g')
        except ValueError as e:
            fullmsg = str(e)
            msg = fullmsg.split(' -- ')[2]

        assert tparse.flag('Tue Aug  6 11:10:57  1996') == [-107398143.0, '']
        assert tparse.flag('JANUary 1, 2000 12:00') == [0., '']
        assert tparse.flag('Tue Aug  6 11:10:57  1996g')[1] == msg

    def test_tpictr_timout(self):
        time = 'Tue Aug 06 11:10:57  1996'
        pictr = 'Wkd Mon DD HR:MN:SC  YYYY'
        secs = -107398143.0
        assert tparse(time) == secs
        assert tpictr(time) == pictr
        assert timout(secs + deltet(secs, 'UTC'), pictr) == time

        time = 'JANUARY 01, 2000 12:00'
        pictr = 'MONTH DD, YYYY HR:MN'
        secs = 0.
        assert tparse(time) == secs
        assert tpictr(time) == pictr
        assert timout(secs + deltet(secs, 'UTC'), pictr) == time

        with pytest.raises(ValueError):
            tpictr('Tue Aug  6 11:10:57  1996g')
        try:
            tpictr('Tue Aug  6 11:10:57  1996g')
        except ValueError as e:
            fullmsg = str(e)
            msg = fullmsg.split(' -- ')[2]

        self.assertAllEqual(tpictr.flag('Tue Aug  6 11:10:57  1996'),
                            ['Wkd Mon  DD HR:MN:SC  YYYY', True, ''])
        self.assertAllEqual(tpictr.flag('JANUary 1, 2000 12:00'),
                            ['MONTH DD, YYYY HR:MN', True, ''])
        self.assertAllEqual(tpictr.flag('Tue Aug  6 11:10:57  1996g')[1:], [False, msg])

        assert timout(0., 'xxx') == 'xxx'

    def test_timdef(self):
        timdef('zone', 'UTC-0')
        assert timdef('get', 'zone') == 'UTC-0'
        assert timdef('zone') == 'UTC-0'
        assert timdef('zone', 'pdt') == 'pdt'
        timdef('zone', 'UTC-0')

        timdef('set', 'calendar', 'mixed')
        assert timdef('get', 'calendar', '') == 'MIXED'
        assert timdef('get', 'calendar') == 'MIXED'
        assert timdef('calendar', '', '') == 'MIXED'
        assert timdef('calendar', '') == 'MIXED'
        assert timdef('calendar') == 'MIXED'

        timdef('set', 'calendar', 'gregorian')
        assert timdef('calendar') == 'GREGORIAN'
        assert timdef('get', 'calendar') == 'GREGORIAN'

        try:
            timdef('set', 'system', 'tdb')
            assert timdef('system') == 'TDB'
            assert timdef('get', 'system') == 'TDB'
            timdef('system', 'utc')
            assert timdef('system') == 'UTC'
            assert timdef('get', 'system') == 'UTC'
        finally:
            timdef('set', 'system', 'utc')  # DO NOT LEAVE TIME SYSTEM OTHER THAN UTC!!!

    def test_tsetyr(self):
        tsetyr(2000)
        assert tparse('Dec 31, 99') == 3155630400.0
        tsetyr(1950)
        assert tparse('Dec 31, 99') == -129600.0

    def test_unitim(self):
        self.assertAllClose(unitim(0., 'TAI', 'TDB'), 32.183927274)
        self.assertAllClose(unitim(0., 'TAI', 'JED'), 2451545.00037)

