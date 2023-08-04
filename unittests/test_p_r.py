import subprocess
import sys
import textwrap
from pathlib import Path

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
    TEST_FILE_DIR,
    checking_pathlike_filename_variants
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
    
    
def test_pckopn_pckw02_pckcls():
    pck = os.path.join(TEST_FILE_DIR, "test_pck.pck")
    cleanup_kernel(pck)
    handle = cs.pckopn(pck, "Test PCK file", 5000)
    cs.pckw02(
        handle, 301, "j2000", 0.0, 3.0, "segid", 1.0, 3, 1, [1.0, 2.0, 3.0], 0.0
    )
    cs.pckcls(handle)
    cleanup_kernel(pck)
    

def test_pckcov():
    ids = cs.SpiceCell(typeno=2, size=1000)
    cover = cs.SpiceCell(typeno=1, size=2000)
    ids = cs.pckfrm(ExtraKernels.earthHighPerPck)
    cover = cs.pckcov(ExtraKernels.earthHighPerPck, ids[0])
    result = [x for x in cover]
    expected = [94305664.18380372, 757080064.1838132]
    npt.assert_array_almost_equal(result, expected)
    
    
def test_pckfrm():
    ids = cs.SpiceCell(typeno=2, size=1000)
    ids = cs.pckfrm(ExtraKernels.earthHighPerPck)
    assert ids[0] == 3000
    
    
def test_pcklof():
    handle = cs.pcklof(ExtraKernels.earthHighPerPck)
    assert handle != -1
    cs.pckuof(handle)
    
    
def test_pckuof():
    handle = cs.pcklof(ExtraKernels.earthHighPerPck)
    assert handle != -1
    cs.pckuof(handle)
    
    
def test_pcpool():
    import string

    data = tuple([j + str(i) for i, j in enumerate(list(string.ascii_lowercase))])
    cs.pcpool("pcpool_test", data)
    cvals = cs.gcpool("pcpool_test", 0)
    assert data == cvals
    
    
def test_pdpool():
    data = np.arange(0.0, 10.0)
    cs.pdpool("pdpool_array", data)
    dvals = cs.gdpool("pdpool_array", 0)
    npt.assert_array_almost_equal(data, dvals)
    
    
def test_pgrrec():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("MARS", "RADII")
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    rectan = cs.pgrrec("Mars", 90.0 * cs.rpd(), 45 * cs.rpd(), 300, re, f)
    expected = [1.604650025e-13, -2.620678915e3, 2.592408909e3]
    npt.assert_array_almost_equal(rectan, expected)
    
    
def test_phaseq():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {
        "=": [
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
        ],
        "<": [
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.468279091,
        ],
        ">": [
            0.940714974,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
        ],
        "LOCMIN": [0.086121423, 0.086121423, 0.079899769, 0.079899769],
        "ABSMIN": [0.079899769, 0.079899769],
        "LOCMAX": [3.055062862, 3.055062862, 3.074603891, 3.074603891],
        "ABSMAX": [3.074603891, 3.074603891],
    }
    cs.furnsh(CoreKernels.testMetaKernel)
    et0 = cs.str2et("2006 DEC 01")
    et1 = cs.str2et("2007 JAN 31")
    cnfine = cs.SpiceCell(typeno=1, size=2)
    cnfine = cs.wninsd(et0, et1, cnfine)
    result = cs.SpiceCell(typeno=1, size=10000)
    for relation in relate:
        result = cs.gfpa(
            "Moon",
            "Sun",
            "LT+S",
            "Earth",
            relation,
            0.57598845,
            0.0,
            cs.spd(),
            5000,
            cnfine
        )
        count = int(len(result) / 2)
        if count > 0:
            temp_results = []
            arr = np.arange(0, (len(result)), 1)
            subarrays = [arr[i:i+2] for i in range(0, len(result), 2)]
            for i in subarrays:
                x = i[0]
                y = i[1]
                start, stop = result[x], result[y]
                startPhase = cs.phaseq(start, "moon", "sun", "earth", "lt+s")
                stopPhase = cs.phaseq(stop, "moon", "sun", "earth", "lt+s")
                temp_results.append(startPhase)
                temp_results.append(stopPhase)
            npt.assert_array_almost_equal(temp_results, expected.get(relation))
            
            
def test_pi():
    assert cs.pi() == np.pi
    
    
def test_pipool():
    data = np.arange(0, 10)
    cs.pipool("pipool_array", data)
    ivals = cs.gipool("pipool_array", 0)
    npt.assert_array_almost_equal(data, ivals)
    

def test_pjelpl():
    center = [1.0, 1.0, 1.0]
    vec1 = [2.0, 0.0, 0.0]
    vec2 = [0.0, 1.0, 1.0]
    normal = [0.0, 0.0, 1.0]
    plane = cs.nvc2pl(normal, 0.0)
    elin = cs.cgv2el(center, vec1, vec2)
    ellipse = cs.pjelpl(elin, plane)
    expected_s_major = [2.0, 0.0, 0.0]
    expected_s_minor = [0.0, 1.0, 0.0]
    expected_center = [1.0, 1.0, 0.0]
    npt.assert_array_almost_equal(expected_center, ellipse[0:3])
    npt.assert_array_almost_equal(expected_s_major, ellipse[3:6])
    npt.assert_array_almost_equal(expected_s_minor, ellipse[6:9])
    
    
def test_pl2nvc():
    normal = [-1.0, 5.0, -3.5]
    point = [9.0, -0.65, -12.0]
    plane = cs.nvp2pl(normal, point)
    normal, constant = cs.pl2nvc(plane)
    expected_normal = [-0.16169042, 0.80845208, -0.56591646]
    npt.assert_almost_equal(constant, 4.8102899, decimal=6)
    npt.assert_array_almost_equal(expected_normal, normal, decimal=6)
    
    
def test_pl2nvp():
    plane_norm = [2.44, -5.0 / 3.0, 11.0 / 9.0]
    const = 3.141592654
    plane = cs.nvc2pl(plane_norm, const)
    norm_vec, point = cs.pl2nvp(plane)
    expected_point = [0.74966576, -0.51206678, 0.37551564]
    npt.assert_array_almost_equal(expected_point, point)
    
    
def test_pl2psv():
    normal = [-1.0, 5.0, -3.5]
    point = [9.0, -0.65, -12.0]
    plane = cs.nvp2pl(normal, point)
    point, span1, span2 = cs.pl2psv(plane)
    npt.assert_almost_equal(cs.vdot(point, span1), 0)
    npt.assert_almost_equal(cs.vdot(point, span2), 0)
    npt.assert_almost_equal(cs.vdot(span1, span2), 0)
    
    
def test_pltar():
    vrtces = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    plates = [[1, 4, 3], [1, 2, 4], [1, 3, 2], [2, 3, 4]]
    assert cs.pltar(vrtces, plates) == pytest.approx(2.3660254037844)
    
    
def test_pltexp():
    iverts = [
        [np.sqrt(3.0) / 2.0, -0.5, 7.0],
        [0.0, 1.0, 7.0],
        [-np.sqrt(3.0) / 2.0, -0.5, 7.0],
    ]
    overts = cs.pltexp(iverts, 1.0)
    expected = [
        [1.732050807569, -1.0, 7.0],
        [0.0, 2.0, 7.0],
        [-1.732050807569, -1.0, 7.0],
    ]
    npt.assert_array_almost_equal(expected, overts)
    
    
def test_pltnp():
    point = [2.0, 2.0, 2.0]
    v1 = [1.0, 0.0, 0.0]
    v2 = [0.0, 1.0, 0.0]
    v3 = [0.0, 0.0, 1.0]
    near, distance = cs.pltnp(point, v1, v2, v3)
    npt.assert_array_almost_equal([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], near)
    assert distance == pytest.approx(2.8867513)
    
    
def test_pltnrm():
    v1 = [np.sqrt(3.0) / 2.0, -0.5, 0.0]
    v2 = [0.0, 1.0, 0.0]
    v3 = [-np.sqrt(3.0) / 2.0, -0.5, 0.0]
    npt.assert_array_almost_equal([0.0, 0.0, 2.59807621135], cs.pltnrm(v1, v2, v3))
    
    
def test_pltvol():
    vrtces = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    plates = [[1, 4, 3], [1, 2, 4], [1, 3, 2], [2, 3, 4]]
    assert cs.pltvol(vrtces, plates) == pytest.approx(1.0 / 6.0)
    
    
def test_polyds():
    result = cs.polyds([1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0], 3, 1)
    npt.assert_array_almost_equal([6.0, 10.0, 23.0, 78.0], result)
    
    
def test_pos():
    string = "AN ANT AND AN ELEPHANT        "
    assert cs.pos(string, "AN", 0) == 0
    assert cs.pos(string, "AN", 2) == 3
    assert cs.pos(string, "AN", 5) == 7
    assert cs.pos(string, "AN", 9) == 11
    assert cs.pos(string, "AN", 13) == 19
    assert cs.pos(string, "AN", 21) == -1
    assert cs.pos(string, "AN", -6) == 0
    assert cs.pos(string, "AN", -1) == 0
    assert cs.pos(string, "AN", 30) == -1
    assert cs.pos(string, "AN", 43) == -1
    assert cs.pos(string, "AN", 0) == 0
    assert cs.pos(string, " AN", 0) == 2
    assert cs.pos(string, " AN ", 0) == 10
    assert cs.pos(string, " AN  ", 0) == -1


def test_posr():
    string = "AN ANT AND AN ELEPHANT        "
    assert cs.posr(string, "AN", 29) == 19
    assert cs.posr(string, "AN", 18) == 11
    assert cs.posr(string, "AN", 10) == 7
    assert cs.posr(string, "AN", 6) == 3
    assert cs.posr(string, "AN", 2) == 0
    assert cs.posr(string, "AN", -6) == -1
    assert cs.posr(string, "AN", -1) == -1
    assert cs.posr(string, "AN", 30) == 19
    assert cs.posr(string, "AN", 43) == 19
    assert cs.posr(string, " AN", 29) == 10
    assert cs.posr(string, " AN ", 29) == 10
    assert cs.posr(string, " AN ", 9) == -1
    assert cs.posr(string, " AN  ", 29) == -1


def test_prompt(tmp_path):
    prompt = 'PROMPT: '
    user_input = "My User Input"
    path = Path(__file__).parent.parent  # root directory
    script_file = tmp_path / "script.py"
    script = f"""
        import sys
        sys.path.insert(0, "{path}")  # Make sure we get the correct cspyce
        import cspyce as cs
        text = cs.prompt("{prompt}")
        print(text, end='', file=sys.stderr)
    """
    with open(script_file, "w") as file:
        file.write(textwrap.dedent(script))

    result = subprocess.run([sys.executable, script_file],
                            input=user_input + "\n", text=True,
                            capture_output=True)
    assert result.stderr == user_input  # Contains the prompt
    assert result.stdout == prompt



def test_prop2b():
    mu = 398600.45
    r = 1.0e8
    speed = np.sqrt(mu / r)
    t = cs.pi() * (r / speed)
    pvinit = np.array(
        [
            0.0,
            r / np.sqrt(2.0),
            r / np.sqrt(2.0),
            0.0,
            -speed / np.sqrt(2.0),
            speed / np.sqrt(2.0),
        ]
    )
    state = np.array(cs.prop2b(mu, pvinit, t))
    npt.assert_array_almost_equal(state, -1.0 * pvinit, decimal=6)
    
    
def test_prsdp():
    assert cs.prsdp("-1. 000") == -1.0
    

def test_prsint():
    assert cs.prsint("PI") == 3
    
    
def test_psv2pl():
    epoch = "Jan 1 2005"
    frame = "ECLIPJ2000"
    cs.furnsh(CoreKernels.testMetaKernel)
    et = cs.str2et(epoch)
    state, ltime = cs.spkezr("EARTH", et, frame, "NONE", "Solar System Barycenter")
    es_plane = cs.psv2pl(state[0:3], state[0:3], state[3:6])
    es_norm, es_const = cs.pl2nvc(es_plane)
    mstate, mltime = cs.spkezr("MOON", et, frame, "NONE", "EARTH BARYCENTER")
    em_plane = cs.psv2pl(mstate[0:3], mstate[0:3], mstate[3:6])
    em_norm, em_const = cs.pl2nvc(em_plane)
    npt.assert_almost_equal(
        cs.vsep(es_norm, em_norm) * cs.dpr(), 5.0424941, decimal=6
    )
    
    
def test_pxform():
    cs.furnsh(CoreKernels.testMetaKernel)
    lon = 118.25 * cs.rpd()
    lat = 34.05 * cs.rpd()
    alt = 0.0
    utc = "January 1, 2005"
    et = cs.str2et(utc)
    abc = cs.bodvrd("EARTH", "RADII")
    equatr = abc[0]
    polar = abc[2]
    f = (equatr - polar) / equatr
    epos = cs.georec(lon, lat, alt, equatr, f)
    rotate = np.array(cs.pxform("IAU_EARTH", "J2000", et))
    jstate = np.dot(epos, rotate)
    expected = np.array([5042.1309421, 1603.52962986, 3549.82398086])
    npt.assert_array_almost_equal(jstate, expected, decimal=4)
    

def test_pxfrm2():
    # load kernels
    cs.furnsh(CoreKernels.testMetaKernel)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.cassFk)
    cs.furnsh(CassiniKernels.cassPck)
    cs.furnsh(CassiniKernels.cassIk)
    cs.furnsh(CassiniKernels.cassSclk)
    cs.furnsh(CassiniKernels.satSpk)
    cs.furnsh(CassiniKernels.cassTourSpk)
    cs.furnsh(CassiniKernels.cassCk)
    # start of test
    etrec = cs.str2et("2013 FEB 25 11:50:00 UTC")
    camid = cs.bodn2c("CASSINI_ISS_NAC")
    shape, obsref, bsight, bounds = cs.getfov(camid)
    # run sincpt on boresight vector
    spoint, etemit, srfvec, found = cs.sincpt(
        "Ellipsoid",
        "Enceladus",
        etrec,
        "IAU_ENCELADUS",
        "CN+S",
        "CASSINI",
        obsref,
        bsight,
    )
    rotate = cs.pxfrm2(obsref, "IAU_ENCELADUS", etrec, etemit)
    # get radii
    radii = cs.bodvrd("Enceladus", "RADII")
    # find position of center with respect to MGS
    pcassmr = cs.vsub(spoint, srfvec)
    # rotate into IAU_MARS
    bndvec = cs.mxv(rotate, cs.vlcom(0.9999, bsight, 0.0001, bounds[1]))
    # get surface point
    spoint = cs.surfpt(pcassmr, bndvec, radii[0], radii[1], radii[2])
    radius, lon, lat = cs.reclat(spoint[0])
    lon *= cs.dpr()
    lat *= cs.dpr()
    # test output
    npt.assert_almost_equal(radius, 250.14507342586242, decimal=5)
    npt.assert_almost_equal(lon, 125.42089677611104, decimal=5)
    npt.assert_almost_equal(lat, -6.3718522103931585, decimal=5)
    
    
def test_q2m():
    mout = cs.q2m(np.array([0.5, 0.4, 0.3, 0.1]))
    expected = np.array(
        [
            [0.607843137254902, 0.27450980392156854, 0.7450980392156862],
            [0.6666666666666666, 0.33333333333333326, -0.6666666666666666],
            [-0.43137254901960775, 0.9019607843137255, 0.019607843137254832],
        ]
    )
    assert np.array_equal(expected, mout)
    
    
def test_qcktrc():
    cs.reset()
    cs.chkin("test")
    cs.chkin("qcktrc")
    trace = cs.qcktrc()
    assert trace == "test --> qcktrc"
    cs.chkout("qcktrc")
    cs.chkout("test")
    cs.reset()
    
    
def test_qderiv():
    delta = 1.0e-3
    f0 = [(2.0 - delta) ** 2.0]
    f2 = [(2.0 + delta) ** 2.0]
    dfdt = cs.qderiv(f0, f2, delta)
    assert 4 - dfdt[0] < 1e-12
    
    
def test_qdq2av():
    angle = [-20.0 * cs.rpd(), 50.0 * cs.rpd(), -60.0 * cs.rpd()]
    m = cs.eul2m(angle[2], angle[1], angle[0], 3, 1, 3)
    q = cs.m2q(m)
    expav = [1.0, 2.0, 3.0]
    qav = [0.0, 1.0, 2.0, 3.0]
    dq = cs.qxq(q, qav)
    dq = [-0.5 * x for x in dq]
    av = cs.qdq2av(q, dq)
    npt.assert_array_almost_equal(av, expav)
    
    
def test_qxq():
    qID = [1.0, 0.0, 0.0, 0.0]
    nqID = [-1.0, 0.0, 0.0, 0.0]
    qI = [0.0, 1.0, 0.0, 0.0]
    qJ = [0.0, 0.0, 1.0, 0.0]
    qK = [0.0, 0.0, 0.0, 1.0]
    npt.assert_array_almost_equal(cs.qxq(qI, qJ), qK)
    npt.assert_array_almost_equal(cs.qxq(qJ, qK), qI)
    npt.assert_array_almost_equal(cs.qxq(qK, qI), qJ)
    npt.assert_array_almost_equal(cs.qxq(qI, qI), nqID)
    npt.assert_array_almost_equal(cs.qxq(qJ, qJ), nqID)
    npt.assert_array_almost_equal(cs.qxq(qK, qK), nqID)
    npt.assert_array_almost_equal(cs.qxq(qID, qI), qI)
    npt.assert_array_almost_equal(cs.qxq(qI, qID), qI)
    
    
def test_radrec():
    npt.assert_array_almost_equal([1.0, 0.0, 0.0], cs.radrec(1.0, 0.0, 0.0))
    npt.assert_array_almost_equal(
        [0.0, 1.0, 0.0], cs.radrec(1.0, 90.0 * cs.rpd(), 0.0)
    )
    npt.assert_array_almost_equal(
        [0.0, 0.0, 1.0], cs.radrec(1.0, 0.0, 90.0 * cs.rpd())
    )
    
    
def test_rav2xf():
    e = [1.0, 0.0, 0.0]
    rz = [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    assert cs.rav2xf(rz, e) is not None
    
    
def test_raxisa():
    axis = [1.0, 2.0, 3.0]
    angle = 0.1 * cs.twopi()
    rotate_matrix = cs.axisar(axis, angle)
    axout, angout = cs.raxisa(rotate_matrix)
    expected_angout = [0.26726124, 0.53452248, 0.80178373]
    npt.assert_approx_equal(angout, 0.62831853, significant=7)
    npt.assert_array_almost_equal(axout, expected_angout)
    
    
def test_recazl():
    d = cs.dpr()
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 0.0, 0.0], False, False), [0.000, 0.0, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 0.0, 0.0], False, False), [1.000, 0.0, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 1.0, 0.0], False, False), [1.000, 270.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 0.0, 1.0], False, False), [1.000, 0.0, -90.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([-1.0, 0.0, 0.0], False, False), [1.000, 180.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, -1.0, 0.0], False, False), [1.000, 90.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 0.0, -1.0], False, False), [1.000, 0.0, 90.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 1.0, 0.0], False, False), [1.414, 315.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 0.0, 1.0], False, False), [1.414, 0.0, -45.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 1.0, 1.0], False, False), [1.414, 270.0 / d, -45.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 1.0, 1.0], False, False), [1.732, 315.0 / d, -35.264 / d], 3
    )

    npt.assert_array_almost_equal(
        cs.recazl([0.0, 0.0, 0.0], True, True), [0.000, 0.0, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 0.0, 0.0], True, True), [1.000, 0.0, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 1.0, 0.0], True, True), [1.000, 90.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 0.0, 1.0], True, True), [1.000, 0.0, 90.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([-1.0, 0.0, 0.0], True, True), [1.000, 180.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, -1.0, 0.0], True, True), [1.000, 270.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 0.0, -1.0], True, True), [1.000, 0.0, -90.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 1.0, 0.0], True, True), [1.414, 45.0 / d, 0.000], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 0.0, 1.0], True, True), [1.414, 0.0, 45.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([0.0, 1.0, 1.0], True, True), [1.414, 90.0 / d, 45.000 / d], 3
    )
    npt.assert_array_almost_equal(
        cs.recazl([1.0, 1.0, 1.0], True, True), [1.732, 45.0 / d, 35.264 / d], 3
    )
    
    
def test_refchg():
    frame1 = 1
    frame2 = 2
    et = 123456789.0
    calculated = cs.refchg(frame1, frame2, et)
    expected = [[ 9.99925708e-01, -1.11789381e-02, -4.85900382e-03],
                [ 1.11789381e-02,  9.99937513e-01, -2.71625947e-05],
                [ 4.85900384e-03, -2.71579263e-05,  9.99988195e-01]]
    npt.assert_almost_equal(expected, calculated)

    
def test_reccyl():
    expected1 = np.array([0.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * cs.rpd(), 0.0])
    expected3 = np.array([1.0, 270.0 * cs.rpd(), 0.0])
    npt.assert_array_almost_equal(expected1, cs.reccyl([0.0, 0.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected2, cs.reccyl([0.0, 1.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected3, cs.reccyl([0.0, -1.0, 0.0]), decimal=7)
    
    
def test_recgeo():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("EARTH", "RADII")
    flat = (radii[0] - radii[2]) / radii[0]
    x = [-2541.748162, 4780.333036, 3360.428190]
    lon, lat, alt = cs.recgeo(x, radii[0], flat)
    actual = [lon * cs.dpr(), lat * cs.dpr(), alt]
    expected = [118.000000, 32.000000, 0.001915518]
    npt.assert_array_almost_equal(actual, expected, decimal=4)
    
    
def test_reclat():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * cs.rpd(), 0.0])
    expected3 = np.array([1.0, 180.0 * cs.rpd(), 0.0])
    npt.assert_array_almost_equal(expected1, cs.reclat([1.0, 0.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected2, cs.reclat([0.0, 1.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected3, cs.reclat([-1.0, 0.0, 0.0]), decimal=7)
    
    
def test_recpgr():
    cs.furnsh(CoreKernels.testMetaKernel)
    radii = cs.bodvrd("MARS", "RADII")
    flat = (radii[0] - radii[2]) / radii[0]
    x = [0.0, -2620.678914818178, 2592.408908856967]
    lon, lat, alt = cs.recpgr("MARS", x, radii[0], flat)
    actual = [lon * cs.dpr(), lat * cs.dpr(), alt]
    expected = [90.0, 45.0, 300.0]
    npt.assert_array_almost_equal(actual, expected, decimal=4)
    
    
def test_recrad():
    range1, ra1, dec1 = cs.recrad([1.0, 0.0, 0.0])
    range2, ra2, dec2 = cs.recrad([0.0, 1.0, 0.0])
    range3, ra3, dec3 = cs.recrad([0.0, 0.0, 1.0])
    npt.assert_array_almost_equal([1.0, 0.0, 0.0], [range1, ra1, dec1])
    npt.assert_array_almost_equal([1.0, 90 * cs.rpd(), 0.0], [range2, ra2, dec2])
    npt.assert_array_almost_equal([1.0, 0.0, 90 * cs.rpd()], [range3, ra3, dec3])


def test_recsph():
    v1 = np.array([-1.0, 0.0, 0.0])
    assert cs.recsph(v1) == [1.0, np.pi / 2, np.pi]
    

# Test changed: outputs tuple, not array
def test_reordc():
    array = ["one", "three", "two", "zero"]
    iorder = [3, 0, 2, 1]
    outarray = cs.reordc(iorder, array)
    assert outarray == ("zero", "one", "two", "three")
    
    
def test_reordd():
    array = [1.0, 3.0, 2.0]
    iorder = [0, 2, 1]
    outarray = cs.reordd(iorder, array)
    npt.assert_array_almost_equal(outarray, [1.0, 2.0, 3.0])


def test_reordi():
    array = [1, 3, 2]
    iorder = [0, 2, 1]
    outarray = cs.reordi(iorder, array)
    npt.assert_array_almost_equal(outarray, [1, 2, 3])
    
    
def test_reordl():
    array = [True, True, False]
    iorder = [0, 2, 1]
    outarray = cs.reordl(iorder, array)
    npt.assert_array_almost_equal(outarray, [True, False, True])
    
    
def test_repmc():
    stringtestone = "The truth is #"
    outstringone = cs.repmc(stringtestone, "#", "SPICE")
    assert outstringone == "The truth is SPICE"
    
    
def test_repmct():
    stringtestone = "The value is #"
    outstringone = cs.repmct(stringtestone, "#", 5, "U")
    outstringtwo = cs.repmct(stringtestone, "#", 5, "l")
    assert outstringone == "The value is FIVE"
    assert outstringtwo == "The value is five"
    
    
def test_repmd():
    stringtestone = "The value is #"
    outstringone = cs.repmd(stringtestone, "#", 5.0e11, 1)
    assert outstringone == "The value is 5.E+11"
    

def test_repmf():
    stringtestone = "The value is #"
    outstringone = cs.repmf(stringtestone, "#", 5.0e3, 5, "f")
    outstringtwo = cs.repmf(stringtestone, "#", -5.2e-9, 3, "e")
    assert outstringone == "The value is 5000.0"
    assert outstringtwo == "The value is -5.20E-09"


def test_repmi():
    stringtest = "The value is <opcode>"
    outstring = cs.repmi(stringtest, "<opcode>", 5)
    assert outstring == "The value is 5"
    
    
def test_repmot():
    stringtestone = "The value is #"
    outstringone = cs.repmot(stringtestone, "#", 5, "U")
    outstringtwo = cs.repmot(stringtestone, "#", 5, "l")
    assert outstringone == "The value is FIFTH"
    assert outstringtwo == "The value is fifth"
    

def test_reset():
    cs.reset()
    assert not cs.failed()
    
    
def test_return_():
    cs.reset()
    assert not cs.return_()
    cs.reset()
    
    
def test_rotate():
    mout = cs.rotate(cs.pi() / 4, 3)
    mExpected = [
        [np.sqrt(2) / 2.0, np.sqrt(2) / 2.0, 0.0],
        [-np.sqrt(2) / 2.0, np.sqrt(2) / 2.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    npt.assert_array_almost_equal(mout, mExpected)


def test_rotmat():
    ident = cs.ident()
    expected_r = [[0.0, 0.0, -1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]
    r_out = cs.rotmat(ident, cs.halfpi(), 2)
    npt.assert_array_almost_equal(r_out, expected_r)
    

def test_rotvec():
    vin = [np.sqrt(2), 0.0, 0.0]
    angle = cs.pi() / 4
    iaxis = 3
    v_expected = [1.0, -1.0, 0.0]
    vout = cs.rotvec(vin, angle, iaxis)
    npt.assert_array_almost_equal(vout, v_expected)
    
    
def test_rpd():
    assert cs.rpd() == np.arccos(-1.0) / 180.0
    
    
def test_rquad():
    # solve x^2 + 2x + 3 = 0
    root1, root2 = cs.rquad(1.0, 2.0, 3.0)
    expected_root_one = [-1.0, np.sqrt(2.0)]
    expected_root_two = [-1.0, -np.sqrt(2.0)]
    npt.assert_array_almost_equal(root1, expected_root_one)
    npt.assert_array_almost_equal(root2, expected_root_two)
# =============================================================================
# prompt
# =============================================================================
# repml
# =============================================================================
