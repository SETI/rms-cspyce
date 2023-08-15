################################################################################
# Unit tests for all the supported spyce functions that do not involve kernels.
################################################################################

import numpy as np
import numbers
import cspyce as s

pi = np.pi


def assert_all_equal(arg1, arg2, tol=1.e-15):
    if type(arg1) == list:
        assert type(arg2) == list
        assert len(arg1) == len(arg2)
        for (item1, item2) in zip(arg1, arg2):
            assert_all_equal(item1, item2)

    elif isinstance(arg1, np.ndarray):
        arg1 = np.array(arg1)
        arg2 = np.array(arg2)
        assert arg1.shape == arg2.shape
        arg1 = arg1.flatten()
        arg2 = arg2.flatten()
        for (x1, x2) in zip(arg1, arg2):
            if isinstance(x1, numbers.Real):
                assert abs(x1 - x2) <= tol
            else:
                assert x1 == x2

    elif isinstance(arg1, numbers.Real):
        assert abs(arg1 - arg2) <= tol

    else:
        assert arg1 == arg2


def test_constants():
    assert s.pi() == pi
    assert s.halfpi() == pi / 2
    assert s.twopi() == pi * 2
    assert s.intmin() == -2 ** 31
    assert s.intmax() == 2 ** 31 - 1
    assert s.dpmin() == -1.7976931348623157e+308
    assert s.dpmax() == 1.7976931348623157e+308

    assert s.b1900() == 2415020.31352
    assert s.b1950() == 2433282.42345905
    assert s.clight() == 299792.458

    assert s.dpr() == 180./pi
    assert s.rpd() == 1./s.dpr()

    assert s.j1900() == 2415020.0
    assert s.j1950() == 2433282.5
    assert s.j2000() == 2451545.0
    assert s.j2100() == 2488070.0
    assert s.jyear() == 31557600.0
    assert s.tyear() == 31556925.9747
    assert s.spd() == 86400.0


def test_axisar():
    assert_all_equal(s.axisar([0,0,1],0.), [[ 1,0,0],[0, 1,0],[0,0,1]])
    assert_all_equal(s.axisar([0,0,1],pi), [[-1,0,0],[0,-1,0],[0,0,1]])

    assert_all_equal(s.axisar_vector([0,0,1],[0.,pi]), [[[ 1,0,0],[0, 1,0],[0,0,1]],
                                                           [[-1,0,0],[0,-1,0],[0,0,1]]])


def test_cvg2el_el2cvg():
    ellipse = s.cgv2el([0,0,0], [1,0,0], [0,1,0])
    assert_all_equal(ellipse, [0, 0, 0, 1, 0, 0, 0, 1, 0])

    assert_all_equal(s.el2cgv(ellipse), [[0,0,0],[1,0,0],[0,1,0]])

    ellipse = s.cgv2el_vector([0,0,0], [[1,0,0],[2,0,0]], [0,1,0])
    assert_all_equal(ellipse, [[0, 0, 0, 1, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 2, 0, 0, 0, 1, 0]])

    assert_all_equal(s.el2cgv_vector(ellipse), [[[0,0,0],[0,0,0]],
                                                   [[1,0,0],[2,0,0]],
                                                   [[0,1,0],[0,1,0]]])


def test_conics():
    elem1 = [1.,0.,0.,0.,0.,0.,0.,1.]
    elem4 = [4.,0.,0.,0.,0.,0.,0.,1.]
    state10 = s.conics(elem1, 0.)
    state11 = s.conics(elem1, pi)
    state40 = s.conics(elem4, 0.)
    state48 = s.conics(elem4, 8*pi)

    assert_all_equal(state10, [ 1,0,0,0, 1  ,0.])
    assert_all_equal(state11, [-1,0,0,0,-1  ,0.])
    assert_all_equal(state40, [ 4,0,0,0, 0.5,0.])
    assert_all_equal(state48, [-4,0,0,0,-0.5,0.])

    test1 = s.conics_vector(elem1, [0., pi, 2*pi])
    assert_all_equal(test1, [[ 1,0,0,0, 1,0.],
                                [-1,0,0,0,-1,0.],
                                [ 1,0,0,0, 1,0.]])

    test1 = s.conics_vector([elem1, elem1, elem4, elem4], [0., pi, 0, 8*pi])
    assert_all_equal(test1, [[ 1,0,0,0, 1,  0.],
                                [-1,0,0,0,-1,  0.],
                                [ 4,0,0,0, 0.5,0.],
                                [-4,0,0,0,-0.5,0.]])


def test_convrt():
    assert_all_equal(s.convrt( 1., 'inches', 'feet'), 1/12.)
    assert_all_equal(s.convrt(12., 'inches', 'feet'), 1.)
    assert_all_equal(s.convrt_vector([1.,12.], 'inches', 'feet'), [1/12.,1.])


def test_cyllat_cylrec_cylsph_radrec_reclat_reccyl_etc():
    assert_all_equal(s.cyllat(1, 0, 0), [1, 0, 0])
    assert_all_equal(s.cylrec(1, 0, 0), [1, 0, 0])
    assert_all_equal(s.cylsph(1, 0, 0), [1, pi/2, 0])
    assert_all_equal(s.radrec(1, 0, 0), [1, 0, 0])

    assert_all_equal(s.reclat([1, 0, 0]), [1, 0, 0])
    assert_all_equal(s.reccyl([1, 0, 0]), [1, 0, 0])
    assert_all_equal(s.recsph([1, 0, 0]), [1, pi/2, 0])
    assert_all_equal(s.recrad([1, 0, 0]), [1, 0, 0])

    assert_all_equal(s.sphlat(1, 0, 0), [1, 0, pi/2])
    assert_all_equal(s.sphcyl(1, 0, 0), [0, 0, 1])
    assert_all_equal(s.sphrec(1, 0, 0), [0, 0, 1])

    assert_all_equal(s.latcyl(1, 0, 0), [1, 0, 0])
    assert_all_equal(s.latrec(1, 0, 0), [1, 0, 0])
    assert_all_equal(s.latsph(1., 0., 0.), [1, pi/2, 0])

    assert_all_equal(s.cyllat_vector([1, 2, 3, 4], 0, 0), [[1, 2, 3, 4],
                                                              [0, 0, 0, 0],
                                                              [0, 0, 0, 0]])
    assert_all_equal(s.cylrec_vector([1, 2, 3, 4], 0, 0), [[1, 0, 0],
                                                              [2, 0, 0],
                                                              [3, 0, 0],
                                                              [4, 0, 0]])
    assert_all_equal(s.cylsph_vector(0, 0, [1, 2, 3, 4]), [[1, 2, 3, 4],
                                                              [0, 0, 0, 0],
                                                              [0, 0, 0, 0]])

    assert_all_equal(s.reclat_vector(5 * [[1, 0, 0]]), [5 * [1], 5 * [0], 5 * [0]])
    assert_all_equal(s.reccyl_vector(5 * [[1, 0, 0]]), [5 * [1], 5 * [0], 5 * [0]])
    assert_all_equal(s.recsph_vector(5 * [[1, 0, 0]]),
                        [5 * [1], 5 * [pi/2], 5 * [0]])
    assert_all_equal(s.recrad_vector(5 * [[1, 0, 0]]), [5 * [1], 5 * [0], 5 * [0]])
    assert_all_equal(s.sphlat_vector([1, 1], 0, 0), [[1, 1], [0, 0], 2 * [pi/2]])
    assert_all_equal(s.sphcyl_vector([1, 1], 0, 0), [[0, 0], [0, 0], [1, 1]])
    assert_all_equal(s.sphrec_vector([1, 1], 0, 0), 2 * [[0, 0, 1]])
    assert_all_equal(s.latcyl_vector(1., 0., [0, 0]), [[1, 1], [0, 0], [0, 0]])
    assert_all_equal(s.latrec_vector(1., [0, 0], 0), 2 * [[1, 0, 0]])
    assert_all_equal(s.latsph_vector([1, 2], 0., 0.),
                        [[1, 2], 2 * [pi/2], [0, 0]])


def test_dcyldr_dgeodr_dlatdr_drdcyl_etc():
    assert_all_equal(s.dcyldr(1., 0., 0.), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert_all_equal(s.dgeodr(1., 0., 0., 1., 0.),
                        [[0, 1, 0], [0, 0, 1, ], [1, 0, 0]])
    assert_all_equal(s.dlatdr(1., 0., 0.), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert_all_equal(s.drdcyl(1., 0., 0.), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert_all_equal(s.drdgeo(1., 0., 0., 1., 0.),
                        [[-0.84147098, 0., 0.54030231],
                         [0.54030231, 0., 0.84147098],
                         [0., 1., 0.]], 5e-9)
    assert_all_equal(s.drdlat(1., 0., 0.), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert_all_equal(s.drdsph(1., 0., 0.), [[0, 1, 0], [0, 0, 0], [1, 0, 0]])
    assert_all_equal(s.dsphdr(1., 0., 0.), [[1, 0, 0], [0, 0, -1], [0, 1, 0]])

    assert s.dcyldr_vector([1, 2, 3, 4], 0., 0.).shape == (4, 3, 3)
    assert s.dgeodr_vector(1., 0., 0., [1, 2, 3, 4], 0.1).shape == (4, 3, 3)
    assert s.dlatdr_vector(1., [1, 2, 3, 4], 0.).shape == (4, 3, 3)
    assert s.drdcyl_vector(1., 0., [1, 2, 3, 4]).shape == (4, 3, 3)
    assert s.drdgeo_vector([1, 2, 3, 4], 0., 0., 1., 0.).shape == (4, 3, 3)
    assert s.drdlat_vector(1., 0., [1, 2, 3, 4]).shape == (4, 3, 3)
    assert s.drdsph_vector(1., 0., [1, 2, 3, 4]).shape == (4, 3, 3)
    assert s.dsphdr_vector([1, 2, 3, 4], 0., 0.).shape == (4, 3, 3)


def test_det():
    ident = np.array([[1,0,0],[0,1,0],[0,0,1]]).astype('float')
    assert s.det(ident) == 1.

    idents = np.arange(20).reshape((20, 1, 1)) * ident
    assert_all_equal(s.det_vector(idents), np.arange(20)**3)


def test_diags2():
    result1 = np.array([[0, 0], [0, 2]])
    result2 = np.array([[1, 1], [-1, 1]]) * np.sqrt(0.5)
    assert_all_equal(s.diags2([[1, 1], [1, 1]])[0], result1)
    assert_all_equal(s.diags2([[1, 1], [1, 1]])[1], result2)

    assert s.diags2_vector([[[1, 2], [2, 1]], [[3, 1], [1, 3]]])[0].shape, (2, 2, 2)
    assert s.diags2_vector([[[1, 2], [2, 1]], [[3, 1], [1, 3]]])[1].shape, (2, 2, 2)


def test_ducrss_dvcrss():
    assert_all_equal(s.ducrss([1, 0, 0, 1, 0, 0], [1, 1, 0, 1, 1, 0]),
                        [0, 0, 1, 0, 0, 0])
    assert_all_equal(s.dvcrss([1, 0, 0, 1, 0, 0], [1, 1, 0, 1, 1, 0]),
                        [0, 0, 1, 0, 0, 2])

    assert_all_equal(s.ducrss_vector(2 * [[1, 0, 0, 1, 0, 0]], [1, 1, 0, 1, 1, 0]),
                        2 * [[0, 0, 1, 0, 0, 0]])
    assert_all_equal(s.dvcrss_vector(2 * [[1, 0, 0, 1, 0, 0]], [1, 1, 0, 1, 1, 0]),
                        2 * [[0, 0, 1, 0, 0, 2]])
def test_dvdot():
    assert s.dvdot(6 * [1], 6 * [1]) == 6
    assert_all_equal(s.dvdot_vector(6 * [1], [6 * [1], 6 * [2]]), [6, 12])


def test_dvhat():
    assert_all_equal(s.dvhat(6 * [1]), (3 * [np.sqrt(1. / 3.)] + 3 * [0.]))
    assert_all_equal(s.dvhat_vector([6 * [1], 6 * [2]]),
                        2 * [3 * [np.sqrt(1. / 3.)] + 3 * [0.]])


def test_dvnorm():
    assert_all_equal(s.dvnorm(6 * [1]), np.sqrt(3.))
    assert_all_equal(s.dvnorm_vector([6 * [1], 6 * [2]]),
                        [np.sqrt(3.), np.sqrt(12.)])


def test_dvsep():
    assert s.dvsep([1, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1]) == -1
    assert s.dvsep_vector([[1, 0, 0, 0, 1, 0], [2, 0, 0, 0, 2, 0]],
                          [0, 1, 0, 0, 0, 1]).shape == (2,)


def test_edlim():
    results = s.edlimb(1., 2., 3., [4., 4., 4.])
    assert results.shape == ( 9,)

    results = s.edlimb_vector(1., 2., [3.,2.5,2.1,1.8], [4., 4., 4.])
    assert results.shape == (4,9)


def test_eqncpv():
    elem = (1.e5, 0.01, 0., 0., 0., 0.01, 0.1, 1., -0.1)
    state = s.eqncpv(0., 100., elem, 0., pi/2)
    assert np.all(np.abs(state) < 1.1e5)

    ra = np.arange(1000.)
    states = s.eqncpv_vector(0., 100., elem, ra, pi/2)
    for i in range(1000):
      assert np.all(np.abs(states[i]) < 1.1e5)


def test_eul2m_m2eul():
    mat1 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    assert_all_equal(s.eul2m(pi, pi/2, pi, 2, 3, 2), mat1)

    mat2 = [[0, 0, -1], [0, -1, 0], [-1, 0, 0]]
    assert_all_equal(s.eul2m(pi, pi, pi/2, 2, 3, 2), mat2)

    assert_all_equal(s.eul2m_vector(pi, [pi/2, pi], [pi, pi/2], 2, 3, 2),
                        [mat1, mat2])

    assert_all_equal(s.m2eul(mat1, 2, 3, 2), [pi, pi/2, pi])
    assert_all_equal(s.m2eul(mat2, 2, 3, 2), [0, pi, -pi/2])

    assert_all_equal(s.m2eul_vector([mat1, mat2], 2, 3, 2),
                        [[pi, 0], [pi/2, pi], [pi, -pi/2]])


def test_eul2xf_xf2eul():
    angles1 = np.array([pi, pi/2, pi, 1, 0, -1])
    mat1 = np.array([[0, 0, -1, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, -1], [2, 0, 0, 0, 1, 0], [0, -2, 0, 1, 0, 0]])

    assert np.max(np.abs(s.eul2xf(angles1, 1, 2, 3) - mat1)) < 3.e-16

    angles2 = np.array([pi, pi, pi, 1, -1, 0])
    mat2 = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                     [0, 0, -1, 1, 0, 0], [0, 0, 1, 0, 1, 0], [1, -1, 0, 0, 0, 1]])

    assert_all_equal(s.eul2xf(angles2, 1, 2, 3), mat2)

    angles = np.array([angles1, angles2])
    assert_all_equal(s.eul2xf_vector(angles, 1, 2, 3), [mat1, mat2])

    angles1 = [0, pi/2, 0, 0, 0, -2]
    assert_all_equal(s.xf2eul(mat1, 1, 2, 3), [angles1, False])

    angles2 = [0, 0, 0, 1, 1, 0]
    assert_all_equal(s.xf2eul(mat2, 1, 2, 3), [angles2, True])

    assert_all_equal(s.xf2eul_vector([mat1, mat2], 1, 2, 3),
                        [[angles1, angles2], [False, True]])


def test_frame():
    assert_all_equal(s.frame([1,0,0]), [[1,0,0],[0,0,-1],[0,1,0]])
    assert_all_equal(s.frame([0,1,0]), [[0,1,0],[0,0,1],[1,0,0]])


def test_ident():
    assert np.all(s.ident() == [[1,0,0],[0,1,0],[0,0,1]])


def test_georec_recgeo():
    assert_all_equal(s.georec(0,0,1,1,0.1), [2,0,0])
    assert_all_equal(s.recgeo([2,0,0],1,0.1), [0,0,1])

    assert_all_equal(s.georec_vector([0,0],0,1,1,0.1), 2*[[2,0,0]])

    assert_all_equal(s.recgeo_vector([2,0,0],[1,1],0.1), [[0,0],[0,0],[1,1]])


def test_repmc():
    assert s.repmc('pi = ##!', '##', '3.14159') == 'pi = 3.14159!'
    assert s.repmct('On one, two, #', '#', 3, 'L') == 'On one, two, three'
    assert s.repmd('pi = #!', '#', pi, 6) == 'pi = 3.14159E+00!'
    assert s.repmf('pi = #!', '#', pi, 6, 'F') == 'pi = 3.14159!'
    assert s.repmi('On 1, 2, #', '#', 3) == 'On 1, 2, 3'
    assert s.repmot('On # base', '#', 3, 'L') == 'On third base'


def test_q2m_m2q_qx1():
    assert_all_equal(s.q2m([1,0,0,0]), [[1,0,0],[0,1,0],[0,0,1]] ,0)
    assert_all_equal(s.m2q([[1,0,0],[0,1,0],[0,0,1]]), [1,0,0,0], 0)

    assert_all_equal(s.q2m_vector(2*[[1,0,0,0]]), 2*[[[1,0,0],[0,1,0],[0,0,1]]], 0)
    assert_all_equal(s.m2q_vector(3*[[[1,0,0],[0,1,0],[0,0,1]]]), 3*[[1,0,0,0]], 0)

    assert_all_equal(s.qxq([1,1,1,1],[1,0,0,0]), [1,1,1,1], 0)
    assert_all_equal(s.qxq_vector([1,1,1,1],2*[[1,0,0,0]]), 2*[4*[1]], 0)


def test_vequ_vequg():
    assert_all_equal(s.vequ([1,2,3]), [1,2,3], 0)
    assert_all_equal(s.vequ_vector([[1,2,3],[4,5,6]]), [[1,2,3],[4,5,6]], 0)

    assert_all_equal(s.vequg([1,2,3]), [1,2,3], 0)
    assert_all_equal(s.vequg([4,5,6,7]), [4,5,6,7], 0)
    assert_all_equal(s.vequg_vector([1,2,3]), [1,2,3], 0)  # drop one dim
    assert_all_equal(s.vequg_vector([[1,2,3]]), [[1,2,3]], 0)  # retain dim
    assert_all_equal(s.vequg_vector([[1,2,3],[4,5,6]]), [[1,2,3],[4,5,6]], 0)


def test_mequ_mequg():
    mat1 = np.arange(9).reshape(3,3)
    mat2 = mat1[::-1]
    assert_all_equal(s.mequ(mat1), mat1, 0)
    assert_all_equal(s.mequ_vector([mat1,mat2]), [mat1,mat2], 0)
    assert_all_equal(s.mequg(mat1), mat1, 0)
    assert_all_equal(s.mequg_vector([mat1,mat2]), [mat1,mat2], 0)


def test_mtxm_mtxmg():
    mat1 = np.arange(9).reshape(3,3)
    mat2 = mat1[::-1]
    mmat1 = np.array(mat1)
    mmat2 = np.array(mat2)
    prod = np.matmul(mmat1.T, mmat2)
    assert_all_equal(s.mtxm(mat1, mat2), prod, 0)
    assert_all_equal(s.mtxm_vector(2*[mat1],mat2), 2*[prod], 0)
    assert_all_equal(s.mtxmg(mat1, mat2), prod, 0)
    assert_all_equal(s.mtxmg_vector(2*[mat1],mat2), 2*[prod], 0)


def test_mxm_mxmg():
    mat1 = np.arange(9).reshape(3,3)
    mat2 = mat1[::-1]
    mmat1 = np.array(mat1)
    mmat2 = np.array(mat2)
    prod = np.matmul(mmat1, mmat2)
    assert_all_equal(s.mxm(mat1, mat2), prod, 0)
    assert_all_equal(s.mxm_vector(2*[mat1],mat2), 2*[prod], 0)
    assert_all_equal(s.mxmg(mat1, mat2), prod, 0)
    assert_all_equal(s.mxmg_vector(2*[mat1],mat2), 2*[prod], 0)


def test_mxmt_mxmtg():
    mat1 = np.arange(9).reshape(3,3)
    mat2 = mat1[::-1]
    mmat1 = np.array(mat1)
    mmat2 = np.array(mat2)
    prod = np.matmul(mmat1, mmat2.T)
    assert_all_equal(s.mxmt(mat1, mat2), prod, 0)
    assert_all_equal(s.mxmt_vector(2*[mat1],mat2), 2*[prod], 0)
    assert_all_equal(s.mxmtg(mat1, mat2), prod, 0)
    assert_all_equal(s.mxmtg_vector(2*[mat1],mat2), 2*[prod], 0)


def test_mtxv_mtxvg():
    mat1 = np.arange(9).reshape(3,3)
    vec = np.array([3,1,2])
    prod = np.dot(mat1.T,vec)
    assert_all_equal(s.mtxv(mat1, vec), prod, 0)
    assert_all_equal(s.mtxv_vector(2*[mat1],vec), 2*[prod], 0)
    assert_all_equal(s.mtxvg(mat1, vec), prod, 0)
    assert_all_equal(s.mtxvg_vector(2*[mat1],vec), 2*[prod], 0)


def test_mxv_mxvg():
    mat1 = np.arange(9).reshape(3,3)
    vec = np.array([3,1,2])
    prod = np.dot(mat1,vec)
    assert_all_equal(s.mxv(mat1, vec), prod, 0)
    assert_all_equal(s.mxv_vector(2*[mat1],vec), 2*[prod], 0)
    assert_all_equal(s.mxvg(mat1, vec), prod, 0)
    assert_all_equal(s.mxvg_vector(2*[mat1],vec), 2*[prod], 0)


def test_vtmv_vtmvg():
    mat1 = np.arange(9).reshape(3,3)
    vec = np.array([3, 1, 2])
    vecT = np.array([vec])
    prod = np.dot(np.dot(vecT,mat1),vec)[0]
    assert_all_equal(s.vtmv(vec, mat1, vec), prod, 0)
    assert_all_equal(s.vtmv_vector(vec, 2*[mat1], vec), 2*[prod], 0)
    assert_all_equal(s.vtmvg(vec, mat1, vec), prod, 0)
    assert_all_equal(s.vtmvg_vector(vec, 2*[mat1], vec), 2*[prod], 0)


def test_xpose_xpose6_xposeg():
    mat = np.arange(9).reshape(3,3)
    assert_all_equal(s.xpose(mat), np.swapaxes(mat,0,1), 0)

    mat = np.arange(18).reshape((2,3,3))
    assert_all_equal(s.xpose_vector(mat), np.swapaxes(mat,1,2), 0)

    mat = np.arange(36).reshape((6,6))
    assert_all_equal(s.xpose6(mat), np.swapaxes(mat,0,1), 0)

    mat = np.arange(72).reshape((2,6,6))
    assert_all_equal(s.xpose6_vector(mat), np.swapaxes(mat,1,2), 0)

    mat = np.arange(6).reshape((2,3))
    assert_all_equal(s.xposeg(mat), np.swapaxes(mat,0,1), 0)

    mat = np.arange(24).reshape((4,2,3))
    assert_all_equal(s.xposeg_vector(mat), np.swapaxes(mat,1,2), 0)


def test_tkvrsn():
    assert s.tkvrsn('toolkit') == 'CSPICE_N0067'
    assert s.tkvrsn() == 'CSPICE_N0067'


def test_unorm_unormg_vhat_vhatg_vnorm_vnormg():
    vec = np.array([1,2,3])
    vec2 = np.array([1,-3,2])
    mag = np.sqrt(np.sum(vec**2))
    unit = vec / mag

    assert_all_equal(s.unorm(vec), [unit,mag])
    assert_all_equal(s.unormg(vec), [unit,mag])
    assert_all_equal(s.unorm_vector([vec,vec2]), [[unit,vec2/mag], 2*[mag]])
    assert_all_equal(s.unormg_vector([vec,vec2]), [[unit,vec2/mag], 2*[mag]])

    assert_all_equal(s.vhat(vec), unit)
    assert_all_equal(s.vhatg(vec), unit)
    assert_all_equal(s.vhat_vector([vec,vec2]), [unit,vec2/mag])
    assert_all_equal(s.vhatg_vector([vec,vec2]), [unit,vec2/mag])

    assert_all_equal(s.vnorm(vec), mag)
    assert_all_equal(s.vnormg(vec), mag)
    assert_all_equal(s.vnorm_vector([vec,vec2]), [mag,mag])
    assert_all_equal(s.vnormg_vector([vec,vec2]), [mag,mag])


def test_vequ_vequg_vminus_vminusg_vadd_vaddg_etc():
    vec1 = np.array([1,2,3])
    vec2 = np.array([2,4,6])
    vec3 = np.array([3,1,3])

    assert_all_equal(s.vequ(vec1), vec1, 0)
    assert_all_equal(s.vequg(vec1), vec1, 0)
    assert_all_equal(s.vequ_vector([vec1,vec2]), [vec1,vec2], 0)
    assert_all_equal(s.vequg_vector([vec1,vec2]), [vec1,vec2], 0)

    assert_all_equal(s.vequ_vector(vec1), vec1, 0) # drop one dim

    assert_all_equal(s.vminus(vec1), -vec1, 0)
    assert_all_equal(s.vminug(vec1), -vec1, 0)
    assert_all_equal(s.vminus_vector([vec1,vec2]), [-vec1,-vec2], 0)
    assert_all_equal(s.vminug_vector([vec1,vec2]), [-vec1,-vec2], 0)

    assert_all_equal(s.vadd(vec1,vec2), vec1+vec2, 0)
    assert_all_equal(s.vaddg(vec1,vec2), vec1+vec2, 0)
    assert_all_equal(s.vadd_vector([vec1,vec3],vec2), [vec1+vec2,vec3+vec2], 0)
    assert_all_equal(s.vaddg_vector([vec1,vec3],vec2), [vec1+vec2,vec3+vec2], 0)

    assert_all_equal(s.vsub(vec1,vec2), vec1-vec2, 0)
    assert_all_equal(s.vsubg(vec1,vec2), vec1-vec2, 0)
    assert_all_equal(s.vsub_vector([vec1,vec3],vec2), [vec1-vec2,vec3-vec2], 0)
    assert_all_equal(s.vsubg_vector([vec1,vec3],vec2), [vec1-vec2,vec3-vec2], 0)

    assert_all_equal(s.vlcom(2,vec1,3,vec2), 2*vec1 + 3*vec2, 0)
    assert_all_equal(s.vlcomg(2,vec1,3,vec2), 2*vec1 + 3*vec2, 0)
    assert_all_equal(s.vlcom_vector(2,[vec1,vec3],3,vec2), [2*vec1+3*vec2,2*vec3+3*vec2], 0)
    assert_all_equal(s.vlcomg_vector(2,[vec1,vec3],3,vec2), [2*vec1+3*vec2,2*vec3+3*vec2], 0)
    assert_all_equal(s.vlcom_vector([1,2],vec1,3,vec2), [1*vec1+3*vec2,2*vec1+3*vec2], 0)
    assert_all_equal(s.vlcomg_vector([1,2],vec1,3,vec2), [1*vec1+3*vec2,2*vec1+3*vec2], 0)

    assert_all_equal(s.vlcom3(2,vec1,3,vec2,4,vec3), 2*vec1 + 3*vec2 + 4*vec3, 0)
    assert_all_equal(s.vlcom3_vector([1,2],vec1,3,vec2,4,vec3),
                    [1*vec1 + 3*vec2 + 4*vec3,2*vec1 + 3*vec2 + 4*vec3], 0)

    assert s.vzero([0,0,0])
    assert not s.vzero([0,0,1.e-99])
    assert s.vzerog([0,0,0,0])
    assert not s.vzerog([0,0,0,1.e-99])

    assert_all_equal(s.vzero_vector([[0,0,0],[0,0,1]]), [True,False])
    assert_all_equal(s.vzerog_vector([[0,0,0,0],[0,0,0,1]]), [True,False])

    assert_all_equal(s.vscl(2,vec1), 2*vec1, 0)
    assert_all_equal(s.vsclg(2,vec1), 2*vec1, 0)
    assert_all_equal(s.vscl_vector([2,3],[vec1,vec2]), [2*vec1, 3*vec2], 0)
    assert_all_equal(s.vsclg_vector([2,3],[vec1,vec2]), [2*vec1, 3*vec2], 0)


def test_vpack_vupack():
    assert_all_equal(s.vpack(1,2,3), [1,2,3], 0)
    assert_all_equal(s.vupack([2,3,4]), [2,3,4], 0)
    assert_all_equal(s.vpack_vector([0,1],2,3), [[0,2,3],[1,2,3]], 0)
    assert_all_equal(s.vupack_vector([[1,3,4],[2,3,4]]), [[1,2],[3,3],[4,4]], 0)

    assert_all_equal(s.vpack_vector(0,2,3), [0,2,3], 0)
    assert_all_equal(s.vpack_vector([0],2,3), [[0,2,3]], 0)


def test_vsep_vsepg():
    assert_all_equal(s.vsep([1,0,0],[0,2,0]), pi/2, 0)
    assert_all_equal(s.vsepg([1,0,0,0],[0,0,2,0]), pi/2, 0)

    assert_all_equal(s.vsep([1,0,0],[2,2,0]), pi/4, 0)
    assert_all_equal(s.vsepg([1,0,0,0],[2,0,2,0]), pi/4., 0)

    assert_all_equal(s.vsep_vector( [1,0,0],[[0,2,0],[2,2,0]]), [pi/2, pi/4], 0)
    assert_all_equal(s.vsepg_vector([1,0,0],[[0,2,0],[2,2,0]]), [pi/2, pi/4], 0)


def test_vdot_vdotg():
    vec = np.array([1,2,3])
    vec2 = np.array([2,4,6])
    vec3 = np.array([3,1,3])

    assert_all_equal(s.vdot(vec,vec2),  np.dot(vec,vec2), 0)
    assert_all_equal(s.vdotg(vec,vec2), np.dot(vec,vec2), 0)

    assert_all_equal(s.vdot_vector(vec,[vec2,vec3]),  [np.dot(vec,vec2),np.dot(vec,vec3)], 0)
    assert_all_equal(s.vdotg_vector(vec,[vec2,vec3]), [np.dot(vec,vec2),np.dot(vec,vec3)], 0)

    assert_all_equal(s.vdotg_vector(vec,vec2), np.dot(vec,vec2), 0)


def test_vcrss_ucrss():
    vec = np.array([1,2,3])
    vec2 = [2,4,7] #can't be parallel to vec
    vec3 = np.array([3,1,3])
    cross12 = np.cross(vec,vec2)
    cross13 = np.cross(vec,vec3)
    norm12 = np.sqrt(np.sum(cross12**2))
    norm13 = np.sqrt(np.sum(cross13**2))

    assert_all_equal(s.vcrss(vec,vec2), cross12, 0)
    assert_all_equal(s.ucrss(vec,vec2), cross12/norm12)

    assert_all_equal(s.vcrss_vector(vec,[vec2,vec3]), [cross12,cross13], 0)
    assert_all_equal(s.ucrss_vector(vec,[vec2,vec3]), [cross12/norm12,cross13/norm13])


def test_twovec():
    assert_all_equal(s.twovec([1,0,0],1,[0,1,0],2), [[1,0,0],[0,1,0],[0,0,1]], 0)
    assert_all_equal(s.twovec([1,0,0],1,[1,1,0],2), [[1,0,0],[0,1,0],[0,0,1]], 0)

    assert_all_equal(s.twovec_vector([1,0,0],1,[[0,1,0],[1,1,0]],2),
                2*[[[1,0,0],[0,1,0],[0,0,1]]], 0)


def test_vperp_vproj():
    assert_all_equal(s.vperp([1,2,3],[2,0,0]), [0,2,3], 0)
    assert_all_equal(s.vperp([1,2,3],[0,4,0]), [1,0,3], 0)
    assert_all_equal(s.vperp_vector([1,2,3],[[2,0,0],[0,4,0]]), [[0,2,3],[1,0,3]], 0)

    assert_all_equal(s.vproj([1,2,3],[2,0,0]), [1,0,0], 0)
    assert_all_equal(s.vproj([1,2,3],[0,4,0]), [0,2,0], 0)
    assert_all_equal(s.vproj_vector([1,2,3],[[2,0,0],[0,4,0]]), [[1,0,0],[0,2,0]], 0)


def test_vdist_vdistg():
    vec = np.array([1,2,3])
    vec2 = [2,4,7] #can't be parallel to vec
    vec3 = np.array([3,1,3])

    assert_all_equal(s.vdist( vec,vec2), s.vnorm( vec - vec2), 0)
    assert_all_equal(s.vdistg(vec,vec2), s.vnormg(vec - vec2), 0)
    assert_all_equal(s.vdist_vector(vec,[vec2,vec3]),
                    [s.vnorm(vec - vec2),s.vnorm(vec - vec3)], 0)
    assert_all_equal(s.vdistg_vector(vec,[vec2,vec3]),
                    [s.vnorm(vec - vec2),s.vnorm(vec - vec3)], 0)


def test_vprjp():
    assert_all_equal(s.vprjp([0,0,1],[1,1,1,1]), [0,0,1], 0)
    assert_all_equal(s.vprjp_vector(2*[[0,0,1]],[1,1,1,1]), 2*[[0,0,1]], 0)


def test_vprjpi():
    assert_all_equal(s.vprjpi([0,0,1], [1,1,1,1], [1,0,0,1]),
                                    [[1,1,2], True], 0)
    assert_all_equal(s.vprjpi_vector(2*[[0,0,1]], [1,1,1,1], 4*[[1,0,0,1]]),
                                    [4*[[1,1,2]], 4*[True]], 0)


def test_vrel_vrelg():
    assert_all_equal(s.vrel([1,0,0],[0,0,1]), np.sqrt(2), 0)
    assert_all_equal(s.vrel([2,0,0],[0,0,2]), np.sqrt(2), 0)
    assert_all_equal(s.vrel_vector([[1,0,0],[2,0,0]],
                                      [[0,1,0],[0,0,2]]), 2*[np.sqrt(2)], 0)

    assert_all_equal(s.vrelg([1,0,0],[0,0,1]), np.sqrt(2), 0)
    assert_all_equal(s.vrelg([2,0,0],[0,0,2]), np.sqrt(2), 0)
    assert_all_equal(s.vrelg_vector([[1,0,0],[2,0,0]],
                                       [[0,1,0],[0,0,2]]), 2*[np.sqrt(2)], 0)


def test_vrotv():
    assert_all_equal(s.vrotv([1,1,0],[0,0,1],pi),   [-1,-1,0])
    assert_all_equal(s.vrotv([1,1,0],[0,0,1],pi/2), [-1, 1,0])
    assert_all_equal(s.vrotv_vector([1,1,0],[0,0,1],[pi,pi/2]),
                                            [[-1,-1,0],[-1,1,0]])


def test_isrot():
    assert s.isrot([[1,0,0],[0,1,0],[0,0,1]],0,0)
    assert not s.isrot([[1,0,0],[0,1,0],[0,0,0.9999999999]],0,0)
    assert s.isrot([[1,0,0],[0,1,0],[0,0,0.9999999999]],0.00001,0)

    assert_all_equal(s.isrot_vector([[1,0,0],[0,1,0],[0,0,0.9999999999]],
                                       [0,0.00001],0), [False,True])

    assert_all_equal(s.isrot_vector([[1,0,0],[0,1,0],[0,0,1]],0,0), True)


def test_invert():
    ident = [[1,0,0],[0,1,0],[0,0,1]]
    assert_all_equal(s.invert(ident), ident, 0)

    mat = [[2,0,0],[0,0,-1],[0,1,0]]
    inv = s.invert(mat)
    assert_all_equal(np.dot(mat,inv), ident, 0)
    assert_all_equal(s.invert_vector([ident,mat]), [ident,inv], 0)


def test_invort():
    mat = (np.arange(9) - 4.).reshape(3,3)
    inv = np.array([[-0.19047619, -0.04761905,  0.0952381 ],
                    [-0.16666667,  0.        ,  0.16666667],
                    [-0.0952381 ,  0.04761905,  0.19047619]])

    assert_all_equal(s.invort(mat), inv, 1.e-7)
    assert_all_equal(s.invort_vector(3*[mat]), 3*[inv], 1.e-7)


def test_indedpl():
    assert_all_equal(s.inedpl(1.,1.,1.,[1,0,0,0]),
                        [[0,0,0,0,0,-1,0,1,0], True], 0)
    assert_all_equal(s.inedpl_vector(1.,1.,1.,[1,0,0,0]),
                        [[0,0,0,0,0,-1,0,1,0],True], 0)
    assert_all_equal(s.inedpl_vector([1.],1.,1.,[1,0,0,0]),
                        [[[0,0,0,0,0,-1,0,1,0]],[True]], 0)
    assert_all_equal(s.inedpl_vector(1.,1.,[1,1],[1,0,0,0]),
                        [2*[[0,0,0,0,0,-1,0,1,0]], 2*[True]], 0)


def test_inelpl():
    assert_all_equal(s.inelpl([0,0,0,1,0,0,0,1,0],[1,0,0,0]),
                        [2,[0,-1,0],[0,1,0]])
    assert_all_equal(s.inelpl_vector([0,0,0,1,0,0,0,1,0],[1,0,0,0]),
                        [2,[0,-1,0],[0,1,0]])
    assert_all_equal(s.inelpl_vector([0,0,0,1,0,0,0,1,0],[[1,0,0,0]]),
                        [[2],[[0,-1,0]],[[0,1,0]]])
    assert_all_equal(s.inelpl_vector(4*[[0,0,0,1,0,0,0,1,0]],2*[[1,0,0,0]]),
                        [4*[2],4*[[0,-1,0]],4*[[0,1,0]]])


def test_inrypl():
    assert_all_equal(s.inrypl([0,0,0],[1,0,0],[1,0,0,0]),
                        [1,[0,0,0]], 0)
    assert_all_equal(s.inrypl_vector([0,0,0],[1,0,0],[1,0,0,0]),
                        [1,[0,0,0]], 0)
    assert_all_equal(s.inrypl_vector([[0,0,0]],[1,0,0],[1,0,0,0]),
                        [[1],[[0,0,0]]], 0)
    assert_all_equal(s.inrypl_vector([0,0,0],[1,0,0],[[1,0,0,0],[2,0,0,0]]),
                        [2*[1],2*[[0,0,0]]], 0)


def test_nplnpt():
    assert_all_equal(s.nplnpt([0,0,0],[0,0,7],[0,1,1]),
                        [[0,0,1], 1], 0)
    assert_all_equal(s.nplnpt([0,0,0],[0,0,7],[2,0,2]),
                        [[0,0,2], 2], 0)
    assert_all_equal(s.nplnpt_vector([0,0,0],[0,0,7],[0,1,1]),
                        [[0,0,1], 1], 0)
    assert_all_equal(s.nplnpt_vector([0,0,0],[[0,0,7]],[0,1,1]),
                        [[[0,0,1]], [1]], 0)
    assert_all_equal(s.nplnpt_vector([0,0,0],[0,0,7],[[0,1,1],[2,0,2]]),
                        [[[0,0,1],[0,0,2]], [1,2]], 0)


def test_nvc2pl():
    assert_all_equal(s.nvc2pl([0,0,1],1), [0,0,1,1], 0)
    assert_all_equal(s.nvc2pl_vector([0,0,1],1), [0,0,1,1], 0)
    assert_all_equal(s.nvc2pl_vector([0,0,1],3*[1]),
                        3*[[0,0,1,1]], 0)


def test_nvp2pl():
    assert_all_equal(s.nvp2pl([0,0,7],[2,0,0]), [0,0,1,0], 0)
    assert_all_equal(s.nvp2pl_vector([0,0,7],[2,0,0]), [0,0,1,0], 0)
    assert_all_equal(s.nvp2pl_vector([0,0,7],9*[[2,0,0]]),
                        9*[[0,0,1,0]], 0)


def test_npedln():
    assert_all_equal(s.npedln(3,2,1,[6,0,0],[-1,0,0]), [[3,0,0],0])
    assert_all_equal(s.npedln(3,2,1,[6,0,6],[-1,0,0]), [[0,0,1],5])
    assert_all_equal(s.npedln_vector(3,2,1,[6,0,0],[-1,0,0]), [[3,0,0],0])
    assert_all_equal(s.npedln_vector(3,2,1,[[6,0,0],[6,0,6]],[-1,0,0]),
                        [[[3,0,0],[0,0,1]],[0,5]])


def test_npelpt():
    assert_all_equal(s.npelpt([5,0,4],[0,0,0,2,0,0,0,3,0]), [[2,0,0],5])
    assert_all_equal(s.npelpt([0,7,3],[0,0,0,2,0,0,0,3,0]), [[0,3,0],5])
    assert_all_equal(s.npelpt_vector([5,0,4],[0,0,0,2,0,0,0,3,0]),
                        [[2,0,0],5])
    assert_all_equal(s.npelpt_vector([[5,0,4],[0,7,3]],[0,0,0,2,0,0,0,3,0]),
                        [[[2,0,0],[0,3,0]],[5,5]])


def test_oscelt():
    assert_all_equal(s.oscelt([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1])
    assert_all_equal(s.oscelt([1,0,0,0,1,0], 0, 0.25),
                        [1,3,0,0,0,0,0,0.25])
    assert_all_equal(s.oscelt_vector([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1])
    assert_all_equal(s.oscelt_vector([1,0,0,0,1,0], 0, [1]),
                        [[1,0,0,0,0,0,0,1]])
    assert_all_equal(s.oscelt_vector([1,0,0,0,1,0], 0, [1,0.25]),
                        [[1,0,0,0,0,0,0,1],[1,3,0,0,0,0,0,0.25]])


def test_oscltx():
    assert_all_equal(s.oscltx([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1,0,1,2*pi,0,0,0,0,0,0,0,0,0])
    assert_all_equal(s.oscltx([1,0,0,0,1,0], 0, 0.25),
                        [1,3,0,0,0,0,0,0.25,0,-0.5,0,0,0,0,0,0,0,0,0,0])
    assert_all_equal(s.oscltx_vector([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1,0,1,2*pi,0,0,0,0,0,0,0,0,0])
    assert_all_equal(s.oscltx_vector([1,0,0,0,1,0], [0],[1]),
                        [[1,0,0,0,0,0,0,1,0,1,2*pi,0,0,0,0,0,0,0,0,0]])
    assert_all_equal(s.oscltx_vector([1,0,0,0,1,0], 0, [1,0.25]),
                        [[1,0,0,0,0,0,0,1,0,1,2*pi,0,0,0,0,0,0,0,0,0],
                         [1,3,0,0,0,0,0,0.25,0,-0.5,0,0,0,0,0,0,0,0,0,0]])


def test_pjelpj():
    assert_all_equal(s.pjelpl([0,0,0,2,0,0,0,3,0], [0,0,1,0]),
                        [0,0,0,0,3,0,2,0,0])
    assert_all_equal(s.pjelpl([0,0,0,2,0,0,0,4,0], [0,0,1,0]),
                        [0,0,0,0,4,0,2,0,0])
    assert_all_equal(s.pjelpl_vector([0,0,0,2,0,0,0,3,0], [0,0,1,0]),
                        [0,0,0,0,3,0,2,0,0])
    assert_all_equal(s.pjelpl_vector([0,0,0,2,0,0,0,3,0], [[0,0,1,0]]),
                        [[0,0,0,0,3,0,2,0,0]])
    assert_all_equal(s.pjelpl_vector([[0,0,0,2,0,0,0,3,0],
                                         [0,0,0,2,0,0,0,4,0]], [0,0,1,0]),
                        [[0,0,0,0,3,0,2,0,0],
                         [0,0,0,0,4,0,2,0,0]])


def test_pl2nvc():
    assert_all_equal(s.pl2nvc([0,0,1,0]), [[0,0,1],0])
    assert_all_equal(s.pl2nvc([0,0,0,1]), [[0,0,0],1])
    assert_all_equal(s.pl2nvc_vector([0,0,1,0]), [[0,0,1],0])
    assert_all_equal(s.pl2nvc_vector([[0,0,1,0]]), [[[0,0,1]],[0]])
    assert_all_equal(s.pl2nvc_vector([[0,0,1,0],[0,0,0,1]]),
                        [[[0,0,1],[0,0,0]],[0,1]])


def test_pl2nvp():
    assert_all_equal(s.pl2nvp([0,0,1,0]), [[0,0,1],[0,0,0]])
    assert_all_equal(s.pl2nvp([0,1,0,0]), [[0,1,0],[0,0,0]])
    assert_all_equal(s.pl2nvp_vector([0,0,1,0]), [[0,0,1],[0,0,0]])
    assert_all_equal(s.pl2nvp_vector([[0,0,1,0],[0,1,0,0]]),
                        [[[0,0,1],[0,1,0]],2*[[0,0,0]]])


def test_pl2psv():
    assert_all_equal(s.pl2psv([0,0,1,0]), [[0,0,0],[0,-1,0],[1,0,0]])
    assert_all_equal(s.pl2psv([0,1,0,0]), [[0,0,0],[0,0,1],[1,0,0]])
    assert_all_equal(s.pl2psv_vector([0,0,1,0]), [[0,0,0],[0,-1,0],[1,0,0]])
    assert_all_equal(s.pl2psv_vector([[0,0,1,0],[0,1,0,0]]),
                        [2*[[0,0,0]],[[0,-1,0],[0,0,1]],2*[[1,0,0]]])


def test_psv2pl():
    assert_all_equal(s.psv2pl([0,0,0],[2,0,0],[0,3,0]), [0,0,1,0])
    assert_all_equal(s.psv2pl([0,0,0],[2,0,0],[0,1,0]), [0,0,1,0])
    assert_all_equal(s.psv2pl_vector([0,0,0],[2,0,0],[0,3,0]), [0,0,1,0])
    assert_all_equal(s.psv2pl_vector([0,0,0],[2,0,0],[[0,3,0],[0,1,0]]),
                        2*[[0,0,1,0]])


def test_raxisa():
    #### raxisa
    assert_all_equal(s.raxisa([[0,1,0],[1,0,0],[0,0,-1]]),
                        [[-np.sqrt(0.5), -np.sqrt(0.5), 0.], pi])
    assert_all_equal(s.raxisa([[1,0,0],[0,0,1],[0,-1,0]]),
                        [[-1,0,0], pi/2])
    assert_all_equal(s.raxisa_vector([[0,1,0],[1,0,0],[0,0,-1]]),
                        [[-np.sqrt(0.5), -np.sqrt(0.5), 0.], pi])
    assert_all_equal(s.raxisa_vector([[[0,1,0],[1,0,0],[0,0,-1]],
                                         [[1,0,0],[0,0,1],[0,-1,0]]]),
                        [[[-np.sqrt(0.5),-np.sqrt(0.5),0],[-1,0,0]],
                         [pi,pi/2]])


def test_prop2b():
    assert_all_equal(s.prop2b(1,[1,0,0,0,1,0],pi/2), [0,1,0,-1,0,0])
    assert_all_equal(s.prop2b(1,[1,0,0,0,1,0],pi/4),
                        np.array([1,1,0,-1,1,0]) / np.sqrt(2))
    assert_all_equal(s.prop2b_vector(1,[1,0,0,0,1,0],pi/2), [0,1,0,-1,0,0])
    assert_all_equal(s.prop2b_vector(1,[1,0,0,0,1,0],[pi/2,pi/4]),
                        [[0,1,0,-1,0,0],np.array([1,1,0,-1,1,0]) / np.sqrt(2)])


def prop_nearpt():
    assert_all_equal(s.nearpt([3,0,0],2,3,1), [[2,0,0],1])
    assert_all_equal(s.nearpt([0,0,3],2,3,1), [[0,0,1],2])
    assert_all_equal(s.nearpt_vector([3,0,0],2,3,1), [[2,0,0],1])
    assert_all_equal(s.nearpt_vector([[3,0,0],[0,0,3]],2,3,1),
                        [[[2,0,0],[0,0,1]],[1,2]])


def test_qdq2av():
    assert_all_equal(s.qdq2av([1,0,0,0],[0,0,0,0]), [ 0,0,0])
    assert_all_equal(s.qdq2av([1,0,0,0],[0,1,0,0]), [-2,0,0])
    assert_all_equal(s.qdq2av_vector([1,0,0,0],[0,0,0,0]), [ 0,0,0])
    assert_all_equal(s.qdq2av_vector([1,0,0,0],[[0,0,0,0],[0,1,0,0]]),
                        [[0,0,0],[-2,0,0]])


def test_rav2xf():
    mat1 = [[0,1,0],[-1,0,0],[0,0,-1]]
    result1 = [[ 0, 1, 0, 0, 0, 0.],
               [-1, 0, 0, 0, 0, 0.],
               [ 0, 0,-1, 0, 0, 0.],
               [ 0, 0, 0, 0, 1, 0.],
               [ 0, 0, 0,-1, 0, 0.],
               [ 0, 0, 0, 0, 0,-1.]]
    result2 = [[ 0, 1, 0, 0, 0, 0.],
               [-1, 0, 0, 0, 0, 0.],
               [ 0, 0,-1, 0, 0, 0.],
               [ 0, 0, 1, 0, 1, 0.],
               [ 0, 0, 0,-1, 0, 0.],
               [ 0, 1, 0, 0, 0,-1.]]

    assert_all_equal(s.rav2xf(mat1,[0,0,0]), result1)
    assert_all_equal(s.rav2xf(mat1,[1,0,0]), result2)
    assert_all_equal(s.rav2xf_vector(mat1,[0,0,0]), result1)
    assert_all_equal(s.rav2xf_vector([mat1],[0,0,0]), [result1])
    assert_all_equal(s.rav2xf_vector(mat1,[[0,0,0],[1,0,0]]),
                                        [result1,result2])


def test_rotate():
    ident = [[1,0,0],[0,1,0],[0,0,1]]

    assert_all_equal(s.rotate(0,1), ident)
    assert_all_equal(s.rotate(pi,1), [[1,0,0],[0,-1,0],[0,0,-1]])
    assert_all_equal(s.rotate(pi/2,1), [[1,0,0],[0,0,1],[0,-1,0]])
    assert_all_equal(s.rotate_vector(0,1), ident)
    assert_all_equal(s.rotate_vector([0],1), [ident])
    assert_all_equal(s.rotate_vector(3*[0],1), 3*[ident])


def test_rotmat():
    ident = [[1,0,0],[0,1,0],[0,0,1]]
    assert_all_equal(s.rotmat(ident,0,1), ident)
    assert_all_equal(s.rotmat(ident,pi,1), [[1,0,0],[0,-1,0],[0,0,-1]])
    assert_all_equal(s.rotmat_vector(ident,0,1), ident)
    assert_all_equal(s.rotmat_vector(ident,[0],1), [ident])
    assert_all_equal(s.rotmat_vector(ident,[0,pi],1),
                                [ident, [[1,0,0],[0,-1,0],[0,0,-1]]])


def test_rotvec():
    assert_all_equal(s.rotvec([1,0,0],0,2), [1,0,0])
    assert_all_equal(s.rotvec([1,0,0],pi,2), [-1,0,0])
    assert_all_equal(s.rotvec_vector([1,0,0],pi,2), [-1,0,0])
    assert_all_equal(s.rotvec_vector([[1,0,0]],[pi],2), [[-1,0,0]])
    assert_all_equal(s.rotvec_vector([[1,0,0]],[pi,0],2), [[-1,0,0],[1,0,0]])


def test_rquad():
    assert_all_equal(s.rquad(1,0,-1), [[1,0],[-1,0]])
    assert_all_equal(s.rquad(1,0, 1), [[0,1],[0,-1]])
    assert_all_equal(s.rquad_vector(1,0,-1), [[1,0],[-1,0]])
    assert_all_equal(s.rquad_vector(1,0,[-1]), [[[1,0]],[[-1,0]]])
    assert_all_equal(s.rquad_vector(1,0,[-1,1]),
                            [[[1,0],[0,1]],[[-1,0],[0,-1]]])


def test_saelgv():
    assert_all_equal(s.saelgv([2,0,0],[0,3,0]), [[0,3,0],[2,0,0]])
    assert_all_equal(s.saelgv_vector([2,0,0],[0,3,0]), [[0,3,0],[2,0,0]])
    assert_all_equal(s.saelgv_vector([2,0,0],[[0,3,0]]),
                            [[[0,3,0]],[[2,0,0]]])
    assert_all_equal(s.saelgv_vector([2,0,0],[[0,3,0],[0,1,0]]),
                            [[[0,3,0],[2,0,0]],[[2,0,0],[0,1,0]]])


def test_stelab():
    cxx = s.clight() / 100.
    eps = 2.e-9
    assert_all_equal(s.stelab([1,0,0],[cxx,0,0]), [1,0,0])
    assert_all_equal(s.stelab([1,0,0],[0,cxx,0]), [0.99995, 0.01, 0], eps)
    assert_all_equal(s.stelab_vector([1,0,0],[cxx,0,0]), [1,0,0])
    assert_all_equal(s.stelab_vector([[1,0,0]],[cxx,0,0]), [[1,0,0]])
    assert_all_equal(s.stelab_vector([1,0,0],[[cxx,0,0],[0,cxx,0]]),
                            [[1,0,0],[0.99995,0.01,0]], eps)


def test_stlabx():
    cxx = s.clight() / 100.
    eps = 2.e-9
    assert_all_equal(s.stlabx([1,0,0],[cxx,0,0]), [1,0,0])
    assert_all_equal(s.stlabx([1,0,0],[0,cxx,0]), [0.99995,-0.01, 0], eps)
    assert_all_equal(s.stlabx_vector([1,0,0],[cxx,0,0]), [1,0,0])
    assert_all_equal(s.stlabx_vector([[1,0,0]],[cxx,0,0]), [[1,0,0]])
    assert_all_equal(s.stlabx_vector([1,0,0],[[cxx,0,0],[0,cxx,0]]),
                            [[1,0,0],[0.99995,-0.01,0]], eps)


def test_trace():
    ident = [[1,0,0],[0,1,0],[0,0,1]]
    assert_all_equal(s.trace(ident), 3.)
    assert_all_equal(s.trace(np.arange(9).reshape((3,3))), 12.)
    assert_all_equal(s.trace_vector(np.arange(9).reshape((3,3))), 12.)
    assert_all_equal(s.trace_vector(np.arange(9).reshape((1,3,3))), [12.])
    assert_all_equal(s.trace_vector(np.arange(36).reshape((4,3,3))),
                            [12,39,66,93.])


def test_pltarr_pltval_pltexp_pltnp():
    vertices = [[0,0,0],[0,0,1],[0,1,0],[1,0,0]]
    indices = [[1,2,3],[1,4,2],[1,3,4],[2,4,3]]

    assert_all_equal(s.pltar( vertices,indices), 1.5 + np.sqrt(3)/2.)
    assert_all_equal(s.pltvol(vertices,indices), 1/6.)

    assert_all_equal(s.pltexp([[0,0,0],[0,1,0],[1,0,0]], 0.),
                            [[0,0,0],[0,1,0],[1,0,0]])
    assert_all_equal(s.pltexp([[0,0,0],[0,1,0],[1,0,0]], 3.),
                            [[-1,-1,0],[-1,3,0],[3,-1,0]])

    assert_all_equal(s.pltnp([1,0,0],[0,0,0],[0,0,1],[0,1,0]),
                            [[0,0,0],1])
    assert_all_equal(s.pltnp([1,-1,0],[0,0,0],[0,0,1],[0,1,0]),
                            [[0,0,0],np.sqrt(2)])
    assert_all_equal(s.pltnp([1,1,1],[0,0,0],[0,0,1],[0,1,0]),
                            [[0,0.5,0.5],np.sqrt(1.5)])
