################################################################################

import sys
import numpy as np
import numbers
import platform
import unittest

from cspyce import *
PATH_ = os.path.split(__file__)[0] + '/../unittest_support/'

class Test_cspyce1_kernels(unittest.TestCase):

  @staticmethod
  def furnish_kernels():
    furnsh(PATH_ + 'naif0012.tls')
    furnsh(PATH_ + 'pck00010.tpc')
    furnsh(PATH_ + 'de432s.bsp')
    furnsh(PATH_ + 'sat164.bsp')
    furnsh(PATH_ + 'earth_000101_180317_171224.bpc')

    furnsh(PATH_ + 'cas_v40.tf')
    furnsh(PATH_ + 'cas00171.tsc')
    furnsh(PATH_ + '17257_17262ra.bc')
    furnsh(PATH_ + '171106R_SCPSE_17224_17258.bsp')
    furnsh(PATH_ + 'cas_iss_v10.ti')

  @staticmethod
  def unload_kernels():
    unload(PATH_ + 'naif0012.tls')
    unload(PATH_ + 'pck00010.tpc')
    unload(PATH_ + 'de432s.bsp')
    unload(PATH_ + 'sat164.bsp')
    unload(PATH_ + 'earth_000101_180317_171224.bpc')

    unload(PATH_ + 'cas_v40.tf')
    unload(PATH_ + 'cas00171.tsc')
    unload(PATH_ + '17257_17262ra.bc')
    unload(PATH_ + '171106R_SCPSE_17224_17258.bsp')
    unload(PATH_ + 'cas_iss_v10.ti')

  def assertAllEqual(self, arg1, arg2, tol=1.e-15, frac=False):
    if isinstance(arg1, list):
        self.assertEqual(type(arg2), list)
        self.assertEqual(len(arg1), len(arg2))
        for (item1,item2) in zip(arg1,arg2):
            self.assertAllEqual(item1, item2, tol, frac)

    elif isinstance(arg1, np.ndarray):
        arg1 = np.array(arg1)
        arg2 = np.array(arg2)
        self.assertEqual(arg1.shape, arg2.shape)
        arg1 = arg1.flatten()
        arg2 = arg2.flatten()
        for (x1,x2) in zip(arg1,arg2):
            if isinstance(x1,numbers.Real):
                if frac:
                    self.assertTrue(abs(x1 - x2) <= tol * abs(x1 + x2)/2.)
                else:
                    self.assertTrue(abs(x1 - x2) <= tol)
            else:
                self.assertEqual(x1, x2, tol)

    elif isinstance(arg1, numbers.Real):
        if frac:
            self.assertTrue(abs(arg1 - arg2) <= tol * abs(arg1 + arg2)/2.)
        else:
            self.assertTrue(abs(arg1 - arg2) <= tol)

    else:
        self.assertEqual(arg1, arg2)

  def assertAllClose(self, arg1, arg2, tol=1.e-8):
        return self.assertAllEqual(arg1, arg2, tol, frac=True)

  def tearDown(self):
    # Be sure the kernel pool is completely empty upon exit
    for k in range(ktotal()-1, -1, -1):
        unload(kdata(k)[0])

  def runTest(self):

    INTMAX = intmax()
    INTMIN = intmin()

    # Time inside Cassini kernels
    CASSINI_ET = 17.65 * 365.25 * 86400.

    # Times inside sat164.bsp
    Y2005 = 5 * 365.25 * 86400.
    Y2006 = 6 * 365.25 * 86400.
    Y2007 = 7 * 365.25 * 86400.

    #### Not tested: dafbfs, dafcls, dafgda, dafgn, dafgs, daffna, dafopr, dafus
    #### Not tested: stcf01, stcg01, stcl01, stcl01

    ### furnsh
    self.furnish_kernels()

    #### pool functions

    # This test adapted from pipool_c.html
    pipool('FRAME_MYTOPO',            [1500000])
    pcpool('FRAME_1500000_NAME',      ['MYTOPO'])
    pipool('FRAME_1500000_CLASS',     [4])
    pipool('FRAME_1500000_CLASS_ID',  [1500000])
    pipool('FRAME_1500000_CENTER',    [300000])
    pcpool('OBJECT_300000_FRAME',     ['MYTOPO'])
    pcpool('TKFRAME_MYTOPO_RELATIVE', ['J2000'])
    pcpool('TKFRAME_MYTOPO_SPEC',     ['ANGLES'])
    pcpool('TKFRAME_MYTOPO_UNITS',    ['DEGREES'])
    pipool('TKFRAME_MYTOPO_AXES',     [3,2,3])
    pdpool('TKFRAME_MYTOPO_ANGLES',   [22.2, 0., -22.2])
    et = 0.

    rmat = pxform('J2000', 'MYTOPO', et)
    self.assertAllEqual(rmat, [[1,0,0],[0,1,0],[0,0,1]])

    et = 10.*365.*86400.
    rmat = pxform('J2000', 'MYTOPO', et)
    self.assertAllEqual(rmat, [[1,0,0],[0,1,0],[0,0,1]])

    pcpool('CTEST', ['LARRY', 'MOE', 'CURLY'])
    pipool('ITEST', [3141,186,282])
    pdpool('DTEST', [3.1415,186.282,.0175])

# This doesn't work, but calls to expool below work fine.
#     self.assertTrue(expool('CTEST'))
    self.assertTrue(expool('ITEST'))
    self.assertTrue(expool('DTEST'))
    self.assertFalse(expool('DTESTxxx'))

    self.assertEqual(dtpool('CTEST'), [3, 'C'])
    self.assertEqual(dtpool('ITEST'), [3, 'N'])
    self.assertEqual(dtpool('DTEST'), [3, 'N'])
    self.assertRaises(KeyError, dtpool, 'DTESTxxx')

    self.assertEqual(dtpool.flag('CTEST'), [True, 3, 'C'])
    self.assertEqual(dtpool.flag('ITEST'), [True, 3, 'N'])
    self.assertEqual(dtpool.flag('DTEST'), [True, 3, 'N'])
    self.assertEqual(dtpool.flag('DTESTxxx')[0], False)

    self.assertEqual(list(gipool('ITEST')), [3141,186,282])
    self.assertEqual(list(gdpool('DTEST')), [3.1415,186.282,.0175])
    self.assertEqual(gcpool('CTEST'), ['LARRY', 'MOE', 'CURLY'])

    self.assertEqual(list(gipool('ITEST',1)), [186,282])
    self.assertEqual(list(gdpool('DTEST',1)), [186.282,.0175])
    self.assertEqual(gcpool('CTEST',1), ['MOE', 'CURLY'])

    self.assertRaises(KeyError, gipool, 'ITESTxxx')
    self.assertRaises(KeyError, gdpool, 'DTESTxxx')
    self.assertRaises(KeyError, gcpool, 'CTESTxxx')

    self.assertEqual(len(gipool.flag('ITEST')), 2)
    self.assertEqual(len(gdpool.flag('DTEST')), 2)
    self.assertEqual(len(gcpool.flag('CTEST')), 2)

    self.assertTrue(gipool.flag('ITEST')[-1])
    self.assertTrue(gdpool.flag('DTEST')[-1])
    self.assertTrue(gcpool.flag('CTEST')[-1])
    self.assertFalse(gcpool.flag('CTESTxxx')[-1])

    #### clpool, ldpool
    self.assertTrue(bodfnd(599, 'RADII'))
    self.assertTrue(bodfnd(699, 'RADII'))
    clpool()
    self.assertFalse(bodfnd(699, 'RADII'))
    ldpool(PATH_ + 'pck00010.tpc')
    self.assertTrue(bodfnd(699, 'RADII'))
    self.unload_kernels()
    self.furnish_kernels()

    #### expool, dtpool
    self.assertTrue(expool('BODY699_RADII'))
    self.assertFalse(expool('BODY699_RADIIxxx'))
    self.assertEqual(dtpool_error('BODY699_RADII'), [3, 'N'])
    self.assertEqual(dtpool.flag('BODY699_RADII'), [True, 3, 'N'])
    self.assertEqual(dtpool.flag('BODY699_RADIIxxx')[0], False)
    self.assertRaises(KeyError, dtpool_error, 'BODY699_RADIIxxx')

    #### gnpool
    self.assertEqual(set(gnpool('BODY699*RA*')), set(['BODY699_POLE_RA',
                                                        'BODY699_RADII']))
    self.assertRaises(KeyError, gnpool, 'BODY699*RAxxx*')

    self.assertEqual(set(gnpool.flag('BODY699*RA*')[0]),
                                    set(['BODY699_POLE_RA', 'BODY699_RADII']))
    self.assertTrue(gnpool.flag('BODY699*RA*')[1])
    self.assertFalse(gnpool.flag('BODY699*RAxxx*')[1])

    SPK_FILES = ['this_is_the_full_path_specification_*',
                 'of_a_file_with_a_long_name'           ,
                 'this_is_the_full_path_specification_*',
                 'of_a_second_file_with_a_very_long_*'  ,
                 'name']
    pcpool('SPK_FILES', SPK_FILES)

    self.assertEqual(stpool('SPK_FILES', 0, '*'), SPK_FILES[0][:-1] + SPK_FILES[1])
    self.assertEqual(stpool('SPK_FILES', 1, '*'), SPK_FILES[2][:-1] + SPK_FILES[3][:-1] + SPK_FILES[4])
    self.assertRaises(KeyError, stpool, 'SPK_FILES', 2, '*')

    self.assertEqual(stpool.flag('SPK_FILES', 0, '*'), [SPK_FILES[0][:-1] + SPK_FILES[1], True])
    self.assertEqual(stpool.flag('SPK_FILES', 1, '*'), [SPK_FILES[2][:-1] + SPK_FILES[3][:-1] + SPK_FILES[4], True])
    self.assertFalse(stpool.flag('SPK_FILES', 2, '*')[1])

    #### bodc2n, bodn2c, bodc2s, bods2c
    self.assertEqual(bodc2n.flag(699), ['SATURN',True])
    self.assertEqual(bodc2n_error(699), 'SATURN')
    self.assertEqual(bodc2n.flag(INTMAX)[1], False)
    self.assertRaises(Exception, bodc2n_error, INTMAX)

    self.assertEqual(bodn2c.flag('SATuRN '), [699, True])
    self.assertEqual(bodn2c_error('SATURN'), 699)
    self.assertEqual(bodn2c.flag('foobar')[1], False)
    self.assertRaises(Exception, bodn2c_error, 'foobar')

    self.assertEqual(bodc2s(699), 'SATURN')
    self.assertEqual(bodc2s(INTMAX), str(INTMAX))

    self.assertEqual(bods2c.flag('SATuRN '), [699, True])
    self.assertEqual(bods2c_error('SATURN'), 699)
    self.assertEqual(bods2c.flag('foobar')[1], False)
    self.assertRaises(Exception, bods2c_error, 'foobar')
    self.assertEqual(bods2c_error('  699 '), 699)
    self.assertEqual(bods2c_error(str(INTMAX)), INTMAX)

    self.assertAllEqual(bltfrm(1), range(1,22), 0)
#     self.assertAllEqual(kplfrm(1), range(1,22), 0)

    #### boddef
    boddef('BIG!', INTMAX)

    self.assertEqual(bodc2n.flag(INTMAX), ['BIG!', True])
    self.assertEqual(bodc2n_error(INTMAX), 'BIG!')

    self.assertEqual(bodn2c.flag('BiG! '), [INTMAX, True])
    self.assertEqual(bodn2c_error('BIG!'), INTMAX)

    self.assertEqual(bodc2s(INTMAX), 'BIG!')
    self.assertEqual(bods2c.flag('BiG! '), [INTMAX, True])
    self.assertEqual(bods2c_error('BIG!'), INTMAX)

    #### bodfnd
    self.assertTrue(bodfnd(699, 'RADII'))
    self.assertFalse(bodfnd(699, 'RADIIxxx'))
    self.assertFalse(bodfnd(INTMIN, 'RADII'))

    #### bodvcd
    self.assertEqual(bodvcd(699, 'RADII')[0], 60268.)
    self.assertEqual(bodvcd(699, 'RADII')[1], 60268.)
    self.assertEqual(bodvcd(699, 'RADII')[2], 54364.)
    self.assertRaises(KeyError, bodvcd, 699, 'RADIIxxx')

    #### bodvrd
    self.assertEqual(bodvrd('SATURN', 'RADII')[0], 60268.)
    self.assertEqual(bodvrd('SATURN', 'RADII')[1], 60268.)
    self.assertEqual(bodvrd('SATURN', 'RADII')[2], 54364.)
    self.assertRaises(KeyError, bodvrd, 'SATURN', 'RADIIxxx')

    #### bodvrd
    self.assertEqual(bodvar(699, 'RADII')[0], 60268.)
    self.assertEqual(bodvar(699, 'RADII')[1], 60268.)
    self.assertEqual(bodvar(699, 'RADII')[2], 54364.)
    self.assertRaises(KeyError, bodvar, 699, 'RADIIxxx')

    # cidfrm
    self.assertEqual(cidfrm.flag(699), [10016, 'IAU_SATURN', True])
    self.assertEqual(cidfrm_error(699), [10016, 'IAU_SATURN'])
    self.assertEqual(cidfrm.flag(INTMIN)[2], False)
    self.assertRaises(KeyError, cidfrm_error, INTMIN)

    # ccifrm
    self.assertEqual(cidfrm.flag(INTMIN)[2], False)
    self.assertEqual(ccifrm.flag(2,699), [10016, 'IAU_SATURN',699,  True])
    self.assertEqual(ccifrm_error(2,699), [10016, 'IAU_SATURN', 699])
    self.assertEqual(ccifrm.flag(2,INTMIN)[3], False)
    self.assertRaises(ValueError, ccifrm_error, INTMIN, INTMIN)

    #### ckcov
    values = ckcov(PATH_ + '17257_17262ra.bc', -82000, False, 'INTERVAL', 1., 'SCLK')
    self.assertEqual(values[0,0], 304593554335.0)
    self.assertEqual(values[0,1], 304610188193.0)
    self.assertEqual(values[1,0], 304610195359.0)
    self.assertEqual(values[1,1], 304622337377.0)
    self.assertEqual(values[2,0], 304622354271.0)
    self.assertEqual(values[2,1], 304625376609.0)

    values = ckcov.flag(PATH_ + '17257_17262ra.bc', 1, False, 'INTERVAL', 1.,
                          'SCLK')
    self.assertEqual(values.shape, (0,2))

    self.assertRaises(KeyError, ckcov_error, PATH_ + '17257_17262ra.bc', 1,
                                               False, 'INTERVAL', 1., 'SCLK')

    #### pckcov, pckfrm
    self.assertRaises(IOError, pckcov, PATH_ + 'pck00010.tpc', 10016)

    frames = pckfrm(PATH_ + 'earth_000101_180317_171224.bpc')

    limits = [-4.31358161e+04, 5.74516869e+08]
    self.assertAllClose(pckcov(PATH_ + 'earth_000101_180317_171224.bpc', 3000),
                            [limits])

    #### ckgp and ckgpav
    sclk = 304593554335.
    (array1a, sclk1,          found1) = ckgp.flag(  -82000, sclk, 1., 'J2000')
    (array2a, array2b, sclk2, found2) = ckgpav.flag(-82000, sclk, 1., 'J2000')

    self.assertTrue(found1)
    self.assertTrue(found2)

    (array1a, sclk1,        ) = ckgp(  -82000, sclk, 1., 'J2000')
    (array2a, array2b, sclk2) = ckgpav(-82000, sclk, 1., 'J2000')

    self.assertTrue(abs(sclk1 - sclk1) <= 1.)
    self.assertEqual(sclk1, sclk2)
    self.assertAllEqual(array1a, array2a, 0.)

    result2a = np.array([[-0.099802  , -0.37245036, -0.92267019],
                         [-0.03169184, -0.92563955,  0.37707699],
                         [-0.99450248,  0.06687415,  0.08057704]])

    result2b = np.array([3.46254953e-05, 5.05354838e-06, -1.12043171e-05])

    self.assertAllEqual(array2a, result2a, 5.e-9)
    self.assertAllEqual(array2b, result2b, 4.e-14)

    # sclk is 0.
    self.assertFalse(ckgp.flag(  -82000, 0., 1., 'J2000')[-1])
    self.assertFalse(ckgpav.flag(-82000, 0., 1., 'J2000')[-1])

    self.assertRaises(IOError, ckgp_error,   -82000, 0., 1., 'J2000')
    self.assertRaises(IOError, ckgpav_error, -82000, 0., 1., 'J2000')

    # sclk is 0.
    self.assertFalse(ckgp.flag(  -82000, 0., 1., 'J2000')[-1])
    self.assertFalse(ckgpav.flag(-82000, 0., 1., 'J2000')[-1])

    self.assertRaises(IOError, ckgp_error,   -82000, 0., 1., 'J2000')
    self.assertRaises(IOError, ckgpav_error, -82000, 0., 1., 'J2000')

    #### ckgp_vector and ckgpav_vector
    sclk = sclk + 100. * np.arange(10)
    (array1ax,           sclk1x) = ckgp_vector(  -82000, sclk, 1., 'J2000')
    (array2ax, array2bx, sclk2x) = ckgpav_vector(-82000, sclk, 1., 'J2000')

    self.assertEqual(array1ax.shape, (10,3,3))
    self.assertEqual(array2ax.shape, (10,3,3))
    self.assertEqual(array2bx.shape, (10,3))
    self.assertAllEqual(array1ax[0], array1a, 0)
    self.assertAllEqual(array2ax[0], array2a, 0)
    self.assertAllEqual(array2bx[0], array2b, 0)

    sclk = sclk + 100. * np.arange(10)
    (array1ax,           sclk1x, found1x) = ckgp_vector.flag(  -82000, sclk, 1., 'J2000')
    (array2ax, array2bx, sclk2x, found2x) = ckgpav_vector.flag(-82000, sclk, 1., 'J2000')

    self.assertEqual(array1ax.shape, (10,3,3))
    self.assertEqual(array2ax.shape, (10,3,3))
    self.assertEqual(array2bx.shape, (10,3))
    self.assertAllEqual(array1ax[0], array1a, 0)
    self.assertAllEqual(array2ax[0], array2a, 0)
    self.assertAllEqual(array2bx[0], array2b, 0)
    self.assertTrue(np.all(found1x))
    self.assertTrue(np.all(found2x))

    #### ckobj
    self.assertEqual(ckobj(PATH_ + '17257_17262ra.bc'), [-82000])

    #### cnmfrm
    self.assertEqual(cnmfrm('SATURN'), [10016, 'IAU_SATURN'])
    self.assertTrue( cnmfrm.flag('SATURN')[-1])
    self.assertFalse(cnmfrm.flag('foo')[-1])
    self.assertRaises(KeyError, cnmfrm_error, 'foo')

    #### dpgrdr, drdpgr
    self.assertAllEqual(dpgrdr('saturn',1.,0.,0.,1.,0.), [[0,-1,0],
                                                            [0,0,1],
                                                            [1,0,0]])
    self.assertAllEqual(drdpgr('saturn',1.,0.,0.,1.,0.),
                                        [[-0.84147098, 0., 0.54030231],
                                         [-0.54030231, 0.,-0.84147098],
                                         [ 0.        , 1., 0.        ]], 5e-9)
    self.assertEqual(dpgrdr_vector('saturn',1.,0.,[1,2,3,4],1.,0.).shape, (4,3,3))
    self.assertEqual(drdpgr_vector('saturn',1.,0.,0.,1.,[0.1,0.02,0.03,0.04]).shape, (4,3,3))

    #### deltet
    d = deltet(0., 'UTC')
    self.assertAllEqual(d - 64.1839272847, 0., 4.e-11)
    self.assertAllEqual(deltet_vector(np.arange(10), 'UTC'), 10*[d], 4.e-9)

    # edterm
    results = edterm('UMBRAL', 'SUN', 'EARTH', 0., 'IAU_EARTH', 'LT+S',
                       'MOON', 100)
    self.assertEqual(len(results), 3)
    self.assertEqual(np.shape(results[0]), ())
    self.assertEqual(results[1].shape, (3,))
    self.assertEqual(results[2].shape, (100,3))

    # et2lst
    self.assertEqual(et2lst(0., 399, 0., 'PLANETOCENTRIC'),
                     [11, 55, 27, '11:55:27', '11:55:27'])
    self.assertEqual(et2lst(0., 399, 43200., 'PLANETOCENTRIC'),
                     [23, 46, 9, '23:46:09', '11:46:09'])

    # et2utc, utc2et, str2et, etcal
    utc = '2000-01-01T11:58:55.816'
    self.assertEqual(et2utc(0., 'ISOC', 3), utc)
    self.assertTrue(abs(utc2et(utc)) < 0.5e-3)
    self.assertTrue(abs(str2et(utc)) < 0.5e-3)
    self.assertEqual(etcal(0.), '2000 JAN 01 12:00:00.000')

    # frmnam, namfrm, frinfo
    self.assertEqual(frmnam(10016), 'IAU_SATURN')
    self.assertEqual(frmnam.flag(10016), 'IAU_SATURN')
    self.assertEqual(frmnam.flag(INTMAX), '')
    self.assertRaises(KeyError, frmnam_error, INTMAX)

    self.assertEqual(namfrm('IAU_SATURN'), 10016)
    self.assertEqual(namfrm.flag('IAU_SATURN'), 10016)
    self.assertEqual(namfrm.flag('xxxxx'), 0)
    self.assertRaises(KeyError, namfrm_error, 'xxxxx')

    self.assertEqual(frinfo(10016), [699, 2, 699])
    self.assertEqual(frinfo.flag(10016), [699, 2, 699, True])
    self.assertFalse(frinfo.flag(INTMAX)[-1])
    self.assertRaises(KeyError, frinfo, INTMAX)

    # frmchg, sxform, pxform, xf2rav, pxfrm2, refchg
    sat0a = frmchg(1, 10016, 0.)
    sat1a = frmchg(1, 10016, 86400.)
    sat0b = sxform('IAU_SATURN', 'J2000', 0.)
    sat1b = sxform('IAU_SATURN', 'J2000', 86400.)
    sat0c = pxform('IAU_SATURN', 'J2000', 0.)
    sat1c = pxform('IAU_SATURN', 'J2000', 86400.)
    sat0d = pxfrm2('IAU_SATURN', 'J2000', 0., 0.)
    sat1d = pxfrm2('IAU_SATURN', 'J2000', 86400., 86400.)
    sat0e = refchg(1, 10016, 0.)
    sat1e = refchg(1, 10016, 86400.)

    self.assertAllEqual(sat0a[:3,:3], sat0b[:3,:3], 0)
    self.assertAllEqual(sat0a[:3,:3], sat0c, 0)
    self.assertAllEqual(sat0a[:3,:3], sat0d, 0)
    self.assertAllEqual(sat0a[:3,:3], sat0e, 0)
    self.assertAllEqual(sat0a[:3,:3], sat0a[3:,3:], 0)  # frmchg not rotating

    self.assertAllEqual(sat1a[:3,:3], sat1b[:3,:3], 0)
    self.assertAllEqual(sat1a[:3,:3], sat1c, 0)
    self.assertAllEqual(sat1a[:3,:3], sat1d, 0)
    self.assertAllEqual(sat1a[:3,:3], sat1e, 0)
    self.assertAllEqual(sat1a[:3,:3], sat1a[3:,3:], 0)

    (mat0a, vec0a) = xf2rav(sat0a)
    (mat1a, vec1a) = xf2rav(sat1a)
    (mat0b, vec0b) = xf2rav(sat0b)
    (mat1b, vec1b) = xf2rav(sat1b)

    self.assertAllEqual(sat0a[:3,:3], mat0a, 0)
    self.assertAllEqual(sat1a[:3,:3], mat1a, 0)
    self.assertAllEqual(sat0b[:3,:3], mat0b, 0)
    self.assertAllEqual(sat1b[:3,:3], mat1b, 0)

    self.assertAllEqual(vec0a, 3*[0.], 0.)
    self.assertAllEqual(vec1a, 3*[0.], 0.)

    self.assertAllEqual(vec0b, vec1b, 1.e-13)

    sat01a = frmchg_vector(1, 10016, [0.,86400.])
    sat01b = sxform_vector('IAU_SATURN', 'J2000', [0.,86400.])
    sat01c = pxform_vector('IAU_SATURN', 'J2000', [0.,86400.])
    sat01d = pxfrm2_vector('IAU_SATURN', 'J2000', [0.,86400.], [0.,86400.])
    sat01e = refchg_vector(1, 10016, [0.,86400.])

    self.assertAllEqual(sat01a, [sat0a,sat1a], 0)
    self.assertAllEqual(sat01b, [sat0b,sat1b], 0)
    self.assertAllEqual(sat01c, [sat0c,sat1c], 0)
    self.assertAllEqual(sat01d, [sat0d,sat1d], 0)
    self.assertAllEqual(sat01e, [sat0e,sat1e], 0)

    (mat01b, vec01b) = xf2rav_vector(sat01b)
    self.assertAllEqual(mat01b, [mat0b,mat1b], 0)
    self.assertAllEqual(vec01b, [vec0b,vec1b], 0)

    #### pgrrec, recpgr
    self.assertAllEqual(pgrrec('MIMAS',0,0,1,1,0.1), [2,0,0])
    self.assertAllEqual(recpgr('MIMAS',[2,0,0],1,0.1), [0,0,1])

    self.assertAllEqual(pgrrec_vector('MIMAS',[0,0],0,1,1,0.1), 2*[[2,0,0]])
    self.assertAllEqual(recpgr_vector('MIMAS',[2,0,0],[1,1],0.1), [[0,0],[0,0],[1,1]])

    #### lspcn
    self.assertAllEqual(lspcn('SATURN', Y2005, 'LT+S'), 5.23103124275, 1.e-11)
    self.assertAllEqual(lspcn('SATURN', Y2006, 'LT+S'), 5.46639556423, 1.e-11)
    self.assertAllEqual(lspcn_vector('SATURN', Y2006, 'LT+S'), 5.46639556423, 1.e-11)
    self.assertAllEqual(lspcn_vector('SATURN', [Y2005,Y2006], 'LT+S'),
                        [5.23103124275,5.46639556423], 1.e-11)

    #### latsrf (no vector version)
    mimas = bodn2c('MIMAS')
    (a,b,C) = bodvcd(mimas, 'RADII')
    lonlats = np.array([[0,0],[90,0],[180,0],[270,0],[0,-90],[0,90]]) * rpd()
    results5 = latsrf('ELLIPSOID', 'MIMAS', Y2005, 'IAU_MIMAS', lonlats)
    results6 = latsrf('ELLIPSOID', 'MIMAS', Y2006, 'IAU_MIMAS', lonlats)

    target = [[a,0,0],[0,b,0],[-a,0,0],[0,-b,0],[0,0,-C],[0,0,C]]
    self.assertAllEqual(results5, target, 4e-14)
    self.assertAllEqual(results6, target, 4e-14)

    #### ltime
    self.assertAllEqual(ltime(CASSINI_ET, -82, '->', 399),
                        [556996483.4720103, 4843.472010222729], 1.e-7)
    self.assertAllEqual(ltime(CASSINI_ET, -82, '<-', 399),
                        [556986797.4373786, 4842.562621312754], 1.e-7)
    self.assertAllEqual(ltime_vector(CASSINI_ET, -82, '<-', 399),
                        [556986797.4373786, 4842.562621312754], 1.e-7)
    self.assertAllEqual(ltime_vector(3*[CASSINI_ET], -82, '<-', 399),
                        [3*[556986797.4373786], 3*[4842.562621312754]], 1.e-7)

    #### spkcov, spkobj
    self.assertRaises(IOError, spkcov, 'foo.bsp', -82)

    spkpath = PATH_ + '171106R_SCPSE_17224_17258.bsp'
    self.assertRaises(KeyError, spkcov, spkpath, 401)

    limits = [5.55782400e+08, 5.58745200e+08]
    self.assertAllEqual(spkcov(spkpath, -82), [limits], 1.)
    self.assertAllEqual(spkcov(spkpath, 699), [limits], 1.)

    self.assertAllEqual(spkcov.flag(spkpath, 699), [limits], 1.)
    self.assertAllEqual(spkcov.flag(spkpath, 401), np.empty((0,2)))

    bodies = set([-82, 301, 399, 699] + list(range(1,11)) +
                                        list(range(601,613)) +
                                        list(range(615,618)))
    self.assertEqual(set(spkobj(PATH_ + '171106R_SCPSE_17224_17258.bsp')), bodies)

    #### illum, illumf, illumg, ilumin, phaseq
    trgepc = 556991636.744989
    srfvec = [-898913.54085495, -158678.38639218, -344986.06074434]
    phase  = 2.3355683234002207
    incdnc = 2.6877326371660395
    emissn = 0.39969284462247634
    visibl = True
    lit    = False

    CASSINI_ET2 = CASSINI_ET + 86400.
    trgepc2 = 557078039.2141582
    srfvec2 = [-197119.85363806,   61957.21359249,  113170.06834279]
    phase2  = 3.0776373659048852
    incdnc2 = 2.6248933305972493
    emissn2 = 0.5795501233580607
    visibl2 = True
    lit2    = False

    if platform.machine() == 'arm64':
        # TODO(fy,rf,mrs): This code gives slightly different results on MacOS Arm64.
        # This lowering of expectations needs to be investigated. Is it Mac only?
        eps = 1e-5
    else:
        eps = 5e-8

    self.assertAllEqual(illum('mimas', CASSINI_ET, 'lt+S', 'cassini',
                                [200,0,0]),
            [phase, incdnc, emissn], eps)
    self.assertAllEqual(illumf('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn, visibl, lit], eps)
    self.assertAllEqual(illumg('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)
    self.assertAllEqual(ilumin('ellipsoid', 'mimas', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)


    self.assertAllEqual(illum('mimas', CASSINI_ET2, 'lt+S', 'cassini',
                                [200,0,0]),
            [phase2, incdnc2, emissn2], eps)
    self.assertAllEqual(illumf('ellipsoid', 'mimas', 'sun', CASSINI_ET2,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc2, srfvec2, phase2, incdnc2, emissn2, visibl2, lit2], eps)
    self.assertAllEqual(illumg('ellipsoid', 'mimas', 'sun', CASSINI_ET2,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc2, srfvec2, phase2, incdnc2, emissn2], eps)
    self.assertAllEqual(ilumin('ellipsoid', 'mimas', CASSINI_ET2,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc2, srfvec2, phase2, incdnc2, emissn2], eps)


    self.assertAllEqual(illum_vector('mimas', CASSINI_ET, 'lt+S', 'cassini',
                                [200,0,0]),
            [phase, incdnc, emissn], eps)
    self.assertAllEqual(illumf_vector('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn, visibl, lit], eps)
    self.assertAllEqual(illumg_vector('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)
    self.assertAllEqual(ilumin_vector('ellipsoid', 'mimas', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)


    self.assertAllEqual(illum_vector('mimas', [CASSINI_ET], 'lt+S', 'cassini',
                                [200,0,0]),
            [[phase], [incdnc], [emissn]], eps)
    self.assertAllEqual(illumf_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc], [srfvec], [phase], [incdnc], [emissn], [visibl], [lit]], eps)
    self.assertAllEqual(illumg_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc], [srfvec], [phase], [incdnc], [emissn]], eps)
    self.assertAllEqual(ilumin_vector('ellipsoid', 'mimas', [CASSINI_ET],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc], [srfvec], [phase], [incdnc], [emissn]], eps)


    self.assertAllEqual(illum_vector('mimas', [CASSINI_ET, CASSINI_ET2], 'lt+S', 'cassini',
                                [200,0,0]),
            [[phase,phase2], [incdnc,incdnc2], [emissn,emissn2]], eps)
    self.assertAllEqual(illumf_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET, CASSINI_ET2],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc,trgepc2], [srfvec,srfvec2], [phase,phase2], [incdnc,incdnc2], [emissn,emissn2], [visibl,visibl2], [lit,lit2]], eps)
    self.assertAllEqual(illumg_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET, CASSINI_ET2],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc,trgepc2], [srfvec,srfvec2], [phase,phase2], [incdnc,incdnc2], [emissn,emissn2]], eps)
    self.assertAllEqual(ilumin_vector('ellipsoid', 'mimas', [CASSINI_ET, CASSINI_ET2],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc,trgepc2], [srfvec,srfvec2], [phase,phase2], [incdnc,incdnc2], [emissn,emissn2]], eps)

    #### phaseq
    phase  = 2.33564238748
    phase2 = 3.07809474673

    self.assertAllEqual(phaseq(CASSINI_ET, 'mimas', 'sun', 'cassini', 'lt+s'),
            phase, eps)
    self.assertAllEqual(phaseq(CASSINI_ET2, 'mimas', 'sun', 'cassini', 'lt+s'),
            phase2, eps)

    self.assertAllEqual(phaseq_vector(CASSINI_ET, 'mimas', 'sun', 'cassini', 'lt+s'),
            phase, eps)

    self.assertAllEqual(phaseq_vector([CASSINI_ET,CASSINI_ET2], 'mimas', 'sun', 'cassini', 'lt+s'),
            [phase,phase2], eps)

    #### sce2c, sce2s, sce2t, scdecd, sct2e, scencd, scs2e, sctiks, scfmt, scpart
    scdp  = 3.04176877635e+11
    scdp2 = 3.04198996178e+11
    sclk  = '1/1882414947.067'
    sclk2 = '1/1882501347.210'

    self.assertAllEqual(sce2c( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(sce2c( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(sce2s( -82, CASSINI_ET) , sclk )
    self.assertAllEqual(sce2s( -82, CASSINI_ET2), sclk2)
    self.assertAllEqual(sce2t( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(sce2t( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(scdecd(-82, scdp ), sclk )
    self.assertAllEqual(scdecd(-82, scdp2), sclk2)
    self.assertAllEqual(sct2e( -82, scdp ), CASSINI_ET , 1.)
    self.assertAllEqual(sct2e( -82, scdp2), CASSINI_ET2, 1.)
    self.assertAllEqual(scencd(-82, sclk ), scdp , 1.)
    self.assertAllEqual(scencd(-82, sclk2), scdp2, 1.)
    self.assertAllEqual(scs2e( -82, sclk ), CASSINI_ET , 1.)
    self.assertAllEqual(scs2e( -82, sclk2), CASSINI_ET2, 1.)

    self.assertAllEqual(sctiks(-82,"1.000"), 256.)
    self.assertAllEqual(sctiks(-82,"0.001"),   1.)

    self.assertAllEqual(scfmt(-82, scdp) , '1188190928.067')
    self.assertAllEqual(scfmt(-82, scdp2), '1188277328.210')

    parts = [[1.77721349e+11], [1.09951163e+12]]
    self.assertAllEqual(scpart(-82), parts, 30000.)

    self.assertAllEqual(sce2c_vector( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(sce2c_vector( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(sce2t_vector( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(sce2t_vector( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(sct2e_vector( -82, scdp ), CASSINI_ET , 1.)
    self.assertAllEqual(sct2e_vector( -82, scdp2), CASSINI_ET2, 1.)

    self.assertAllEqual(sce2c_vector( -82, [CASSINI_ET ]), [scdp ], 1.)
    self.assertAllEqual(sce2c_vector( -82, [CASSINI_ET2]), [scdp2], 1.)
    self.assertAllEqual(sce2t_vector( -82, [CASSINI_ET ]), [scdp ], 1.)
    self.assertAllEqual(sce2t_vector( -82, [CASSINI_ET2]), [scdp2], 1.)
    self.assertAllEqual(sct2e_vector( -82, [scdp ]), [CASSINI_ET ], 1.)
    self.assertAllEqual(sct2e_vector( -82, [scdp2]), [CASSINI_ET2], 1.)

    self.assertAllEqual(sce2c_vector( -82, [CASSINI_ET,CASSINI_ET2]), [scdp,scdp2], 1.)
    self.assertAllEqual(sce2t_vector( -82, [CASSINI_ET,CASSINI_ET2]), [scdp,scdp2], 1.)
    self.assertAllEqual(sct2e_vector( -82, [scdp,scdp2]), [CASSINI_ET,CASSINI_ET2], 1.)

    #### spkssb, spkacs, spkapo, spkez, spkezr, spkpos
    xssb  = [-9.35325266e+07, -1.38980049e+09, -5.69362184e+08, 1.00994262e+01,
             5.57457613e+00, -1.32361199e+00]
    xssb2 = [-9.28933887e+07, -1.38916427e+09, -5.69894015e+08, -8.14701094e-01,
             -1.90665286e+01, -8.26491731e+00]

    ssb  = spkssb(-82, CASSINI_ET,  'J2000')
    ssb2 = spkssb(-82, CASSINI_ET2, 'J2000')
    self.assertAllClose(spkssb(-82, CASSINI_ET,  'J2000'), xssb)
    self.assertAllClose(spkssb(-82, CASSINI_ET2, 'J2000'), xssb2)

    xstate  = [-5.80013005e+04,   8.94350415e+05,  -3.86487455e+05,
               -1.49765896e+01,  -5.10106017e+00,   1.77874639e+00]
    xstate2  = [2.09801346e+04,   2.11762463e+05,   1.01477978e+05,
               -3.43826105e+00,   1.42982547e+01,   8.91877142e+00]
    xlt  = 3.255625500957274
    xdlt = -1.4972390244438447e-05
    xlt2  = 0.7864001637489081
    xdlt2 = 5.4624503604634114e-05

    (state,  lt,  dlt)  = spkaps(601, CASSINI_ET,  'J2000', 'lt', ssb, [0,0,0])
    (state2, lt2, dlt2) = spkaps(601, CASSINI_ET2, 'J2000', 'lt', ssb2, [0,0,0])

    self.assertAllClose([state,  lt,  dlt] , [xstate,  xlt,  xdlt ])
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

    # spkapp gives an erroneous velocity
    temp  = spkapp(601, CASSINI_ET , 'J2000', ssb , 'lt')
    temp2 = spkapp(601, CASSINI_ET2, 'J2000', ssb2, 'lt')

    self.assertAllEqual(temp [0][:3], state [:3], 0)
    self.assertAllEqual(temp2[0][:3], state2[:3], 0)
    self.assertAllEqual(temp [1:], [lt ], 0)
    self.assertAllEqual(temp2[1:], [lt2], 0)
    self.assertAllEqual(temp [0][3:], state [3:], 3e-4)
    self.assertAllEqual(temp2[0][3:], state2[3:], 3e-4)

    # vector versions with scalar inputs
    self.assertAllEqual(spkaps_vector(601, CASSINI_ET, 'J2000', 'lt', ssb, [0,0,0]),
                    [state, lt, dlt], 0)
    self.assertAllEqual(spkaps_vector(601, CASSINI_ET2, 'J2000', 'lt', ssb2, [0,0,0]),
                    [state2, lt2, dlt2], 0)

    self.assertAllEqual(spkacs_vector(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state, lt, dlt], 0)
    self.assertAllEqual(spkacs_vector(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2, lt2, dlt2], 0)

    self.assertAllEqual(spkapo_vector(601, CASSINI_ET, 'J2000', ssb, 'lt'),
                    [state[:3], lt], 0)
    self.assertAllEqual(spkapo_vector(601, CASSINI_ET2, 'J2000', ssb2, 'lt'),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(spkez_vector(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state, lt], 0)
    self.assertAllEqual(spkez_vector(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2, lt2], 0)

    self.assertAllEqual(spkezp_vector(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state[:3], lt], 0)
    self.assertAllEqual(spkezp_vector(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(spkezr_vector('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                    [state, lt], 0)
    self.assertAllEqual(spkezr_vector('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                    [state2, lt2], 0)

    self.assertAllEqual(spkpos_vector('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                    [state[:3], lt], 0)
    self.assertAllEqual(spkpos_vector('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(spkltc_vector(601, CASSINI_ET, 'J2000', 'lt', ssb),
                    [state, lt, dlt], 0)
    self.assertAllEqual(spkltc_vector(601, CASSINI_ET2, 'J2000', 'lt', ssb2),
                    [state2, lt2, dlt2], 0)

    temp  = spkapp_vector(601, CASSINI_ET , 'J2000', ssb , 'lt')
    temp2 = spkapp_vector(601, CASSINI_ET2, 'J2000', ssb2, 'lt')

    self.assertAllEqual(temp [0][:3], state [:3], 0)
    self.assertAllEqual(temp2[0][:3], state2[:3], 0)
    self.assertAllEqual(temp [1:], [lt ], 0)
    self.assertAllEqual(temp2[1:], [lt2], 0)
    self.assertAllClose(temp [0][3:], state [3:], 3e-4)
    self.assertAllClose(temp2[0][3:], state2[3:], 3e-4)

    # vector versions with vector inputs
    self.assertAllEqual(spkaps_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', [ssb,ssb2], 2*[[0,0,0]]),
                    [[state,state2], [lt,lt2], [dlt,dlt2]], 0)
    self.assertAllEqual(spkacs_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', -82),
                    [[state,state2], [lt,lt2], [dlt,dlt2]], 0)
    self.assertAllEqual(spkapo_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', [ssb,ssb2], 'lt'),
                    [[state[:3],state2[:3]], [lt,lt2]], 0)
    self.assertAllEqual(spkez_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', -82),
                    [[state,state2], [lt,lt2]], 0)
    self.assertAllEqual(spkezp_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', -82),
                    [[state[:3],state2[:3]], [lt,lt2]], 0)
    self.assertAllEqual(spkezr_vector('mimas', [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', 'cassini'),
                    [[state,state2], [lt,lt2]], 0)
    self.assertAllEqual(spkpos_vector('mimas', [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', 'cassini'),
                    [[state[:3],state2[:3]], [lt,lt2]], 0)
    self.assertAllEqual(spkltc_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', [ssb,ssb2]),
                    [[state,state2], [lt,lt2], [dlt,dlt2]], 0)

    temp  = spkapp_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', [ssb,ssb2], 'lt')
    self.assertAllEqual(temp[0][:,:3], [state[:3],state2[:3]], 0)
    self.assertAllEqual(temp[1], [lt,lt2], 0)
    self.assertAllEqual(temp[0][:,3:], [state[3:],state2[3:]], 3e-4)

    #### spkez, spkgeo, spkgps
    xstate  = [ -5.80171789e+04,   8.94351951e+05,  -3.86485973e+05,
                -1.49767494e+01,  -5.10452110e+00,   1.77892184e+00]
    xstate2  = [2.09767900e+04,   2.11758713e+05,   1.01478492e+05,
                -3.43824167e+00,   1.42971900e+01,   8.91882636e+00]
    xlt  = 3.2556313860561055
    xlt2  = 0.7863886730607871

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

    #### srfc2s, srfcss, srfs2c, srfscc
    furnsh(PATH_ + 'phobos_surface.tm')    # Example from srfc2s_c.html
    self.assertEqual(srfc2s(1,401), 'PHOBOS GASKELL Q512')
    self.assertEqual(srfcss(1,'phobos'), 'PHOBOS GASKELL Q512')
    self.assertEqual(srfs2c('PHOBOS GASKELL Q512','phobos'), 1)
    self.assertEqual(srfscc('PHOBOS GASKELL Q512',401), 1)

    self.assertRaises(KeyError, srfc2s, 2, 401)
    self.assertRaises(KeyError, srfc2s, 1, 402)
    self.assertRaises(KeyError, srfcss, 2, 'phobos')
    self.assertRaises(KeyError, srfcss, 1, 'deimos')
    self.assertRaises(KeyError, srfs2c, 'whatever', 'phobos')
    self.assertRaises(KeyError, srfs2c, 'PHOBOS GASKELL Q512', 'deimos')
    self.assertRaises(KeyError, srfscc, 'whatever', 401)
    self.assertRaises(KeyError, srfscc, 'PHOBOS GASKELL Q512', 402)

    self.assertAllEqual(srfc2s.flag(1,401), ['PHOBOS GASKELL Q512',True])
    self.assertAllEqual(srfcss.flag(1,'phobos'), ['PHOBOS GASKELL Q512',True])
    self.assertAllEqual(srfs2c.flag('PHOBOS GASKELL Q512','phobos'), [1,True])
    self.assertAllEqual(srfscc.flag('PHOBOS GASKELL Q512',401), [1,True])

    self.assertFalse(srfc2s.flag(2, 401)[1])
    self.assertFalse(srfc2s.flag(1, 402)[1])
    self.assertFalse(srfcss.flag(2, 'phobos')[1])
    self.assertFalse(srfcss.flag(1, 'deimos')[1])
    self.assertFalse(srfs2c.flag('whatever', 'phobos')[1])
    self.assertFalse(srfs2c.flag('PHOBOS GASKELL Q512', 'deimos')[1])
    self.assertFalse(srfscc.flag('whatever', 401)[1])
    self.assertFalse(srfscc.flag('PHOBOS GASKELL Q512', 402)[1])

    #### timdef
    self.assertEqual(timdef('get', 'calendar'), 'GREGORIAN')
    self.assertEqual(timdef('get', 'system'), 'UTC')
    self.assertEqual(timdef('get', 'zone'), '')

    self.assertEqual(timdef('set', 'calendar', 'mixed '), 'mixed ')
    self.assertEqual(timdef('get', 'calendar'), 'MIXED')

    self.assertEqual(timdef('set', 'system', 'utC'), 'utC')
    self.assertEqual(timdef('get', 'system'), 'UTC')

    self.assertEqual(timdef('set', 'zone', 'PDT'), 'PDT')
    self.assertEqual(timdef('get', 'zone'), 'UTC-7')
    timdef('set', 'zone', 'UTC-0')

    #### tparse
    self.assertEqual(tparse('Tue Aug  6 11:10:57  1996'), -107398143.0)
    self.assertEqual(tparse('JANUary 1, 2000 12:00'), 0.)

    self.assertRaises(ValueError, tparse, 'Tue Aug  6 11:10:57  1996g')
    try:
        _ = tparse('Tue Aug  6 11:10:57  1996g')
    except ValueError as e:
        fullmsg = str(e)
        msg = fullmsg.split(' -- ')[2]

    self.assertEqual(tparse.flag('Tue Aug  6 11:10:57  1996'), [-107398143.0,''])
    self.assertEqual(tparse.flag('JANUary 1, 2000 12:00'), [0.,''])
    self.assertEqual(tparse.flag('Tue Aug  6 11:10:57  1996g')[1], msg)

    #### tpictr, timout
    time  = 'Tue Aug 06 11:10:57  1996'
    pictr = 'Wkd Mon DD HR:MN:SC  YYYY'
    secs  = -107398143.0
    self.assertEqual(tparse(time), secs)
    self.assertEqual(tpictr(time), pictr)
    self.assertEqual(timout(secs + deltet(secs, 'UTC'), pictr), time)

    time  = 'JANUARY 01, 2000 12:00'
    pictr = 'MONTH DD, YYYY HR:MN'
    secs  = 0.
    self.assertEqual(tparse(time), secs)
    self.assertEqual(tpictr(time), pictr)
    self.assertEqual(timout(secs + deltet(secs, 'UTC'), pictr), time)

    self.assertRaises(ValueError, tpictr, 'Tue Aug  6 11:10:57  1996g')
    try:
        _ = tpictr('Tue Aug  6 11:10:57  1996g')
    except ValueError as e:
        fullmsg = str(e)
        msg = fullmsg.split(' -- ')[2]

    self.assertAllEqual(tpictr.flag('Tue Aug  6 11:10:57  1996'), ['Wkd Mon  DD HR:MN:SC  YYYY', True, ''])
    self.assertAllEqual(tpictr.flag('JANUary 1, 2000 12:00'), ['MONTH DD, YYYY HR:MN', True, ''])
    self.assertAllEqual(tpictr.flag('Tue Aug  6 11:10:57  1996g')[1:], [False, msg])

    self.assertEqual(timout(0., 'xxx'), 'xxx')

    ### timdef
    self.assertEqual(timdef('get', 'zone'), 'UTC-0')
    self.assertEqual(timdef('zone'), 'UTC-0')
    self.assertEqual(timdef('zone', 'pdt'), 'pdt')
    timdef('zone', 'UTC-0')

    timdef('set', 'calendar', 'mixed')
    self.assertEqual(timdef('get', 'calendar', ''), 'MIXED')
    self.assertEqual(timdef('get', 'calendar'), 'MIXED')
    self.assertEqual(timdef('calendar', '', ''), 'MIXED')
    self.assertEqual(timdef('calendar', ''), 'MIXED')
    self.assertEqual(timdef('calendar'), 'MIXED')

    timdef('set', 'calendar', 'gregorian')
    self.assertEqual(timdef('calendar'), 'GREGORIAN')
    self.assertEqual(timdef('get', 'calendar'), 'GREGORIAN')

    try:
        timdef('set', 'system', 'tdb')
        self.assertEqual(timdef('system'), 'TDB')
        self.assertEqual(timdef('get', 'system'), 'TDB')
        timdef('system', 'utc')
        self.assertEqual(timdef('system'), 'UTC')
        self.assertEqual(timdef('get', 'system'), 'UTC')
    finally:
        timdef('set', 'system', 'utc')  # DO NOT LEAVE TIME SYSTEM OTHER THAN UTC!!!

    ### tsetyr
    tsetyr(2000)
    self.assertEqual(tparse('Dec 31, 99'), 3155630400.0)
    tsetyr(1950)
    self.assertEqual(tparse('Dec 31, 99'), -129600.0)

    ### unitim
    self.assertAllClose(unitim(0., 'TAI', 'TDB'), 32.183927274)
    self.assertAllClose(unitim(0., 'TAI', 'JED'), 2451545.00037)

################################################################################

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
