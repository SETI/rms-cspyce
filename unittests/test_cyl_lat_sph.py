##########################################################################################
# test_cyl_lat_sph.py: conversions between rec, cyl, lat, and sph coordinates
##########################################################################################

import numpy as np
import pytest
from cspyce import *
from pathlib import Path

DPR = dpr()
TWOPI = twopi()

@pytest.fixture(autouse=True)
def load_kernel():
    kernels = Path(__file__).parent.parent / 'unittest_support/'
    furnsh(kernels / 'de421.bsp')
    furnsh(kernels / 'naif0012.tls')
    yield
    unload(kernels / 'de421.bsp')
    unload(kernels / 'naif0012.tls')


def test_all():

    et = str2et( "2017 Mar 20")
    et1d = np.array([et, et+10, et+20, et+30])

    #### spkpos
    (pos, lt) = spkpos("Moon", et, "J2000", "NONE", "Earth")
    assert round(abs(pos[0]--55658.44323296262), 9) == 0
    assert round(abs(pos[1]--379226.3293147546), 9) == 0
    assert round(abs(pos[2]--126505.93063865259), 9) == 0

    #### spkpos_vector
    (pos1d, lt1d) = spkpos_vector("Moon", et1d, "J2000", "NONE", "Earth")
    pos1d_ = np.array([[-55658.44323296, -379226.32931475, -126505.93063865],
                       [-55648.84010563, -379227.28937824, -126506.68034533],
                       [-55639.23694455, -379228.24920749, -126507.42997386],
                       [-55629.63374972, -379229.2088025 , -126508.17952426]])
    lt1d_ = np.array([1.3463525460835728, 1.346351921934707, 1.346351297728633,
                    1.3463506734653514])

    for index, value in np.ndenumerate(pos1d):
        assert round(abs(value-pos1d_[index]), 7) == 0

    for index, value in np.ndenumerate(lt1d):
        assert round(abs(value-lt1d_[index]), 14) == 0

    #### reclat
    (latrad1, latlon1, latlat1) = reclat(pos)
    assert round(abs(latrad1-403626.33912495256), 9) == 0
    assert round(abs(latlon1 * DPR--98.34959788856911), 13) == 0
    assert round(abs(latlat1 * DPR--18.265660770458155), 13) == 0

    #### latrec
    latpos = latrec(latrad1, latlon1, latlat1)
    assert round(abs(latpos[0]-pos[0]), 9) == 0
    assert round(abs(latpos[1]-pos[1]), 9) == 0
    assert round(abs(latpos[2]-pos[2]), 9) == 0

    #### reclat_vector, latrec_vector
    (lat1dx, lat1dy, lat1dz) = reclat_vector(pos1d)
    latpos1d = latrec_vector(lat1dx, lat1dy, lat1dz)
    maxdiff = np.max(np.abs(latpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### reccyl
    (cylrad1, cyllon1, cylz1) = reccyl(pos)
    assert round(abs(cylrad1-383289.01777726377), 9) == 0
    assert round(abs(cyllon1 * DPR- (-98.34959788856911 + 360)), 13) == 0
    assert round(abs(cylz1--126505.9306386526), 9) == 0

    #### cylrec
    cylpos = cylrec(cylrad1, cyllon1, cylz1)
    assert round(abs(latpos[0]-pos[0]), 9) == 0
    assert round(abs(latpos[1]-pos[1]), 9) == 0
    assert round(abs(latpos[2]-pos[2]), 9) == 0

    #### reccyl_vector, cylrec_vector
    (cyl1dx, cyl1dy, cyl1dz) = reccyl_vector(pos1d)
    cylpos1d = cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    maxdiff = np.max(np.abs(cylpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### latcyl
    (cylrad2, cyllon2, cylz2) = latcyl(latrad1, latlon1, latlat1)
    assert round(abs(cylrad2-cylrad1), 9) == 0
    assert round(abs(cyllon2 % TWOPI-cyllon1 % TWOPI), 15) == 0
    assert round(abs(cylz2-cylz1), 9) == 0

    #### cyllat
    (latrad2, latlon2, latlat2) = cyllat(cylrad2, cyllon2, cylz2)
    assert round(abs(latrad2-latrad1), 9) == 0
    assert round(abs(latlon2 % TWOPI-latlon1 % TWOPI), 15) == 0
    assert round(abs(latlat2 % TWOPI-latlat1 % TWOPI), 15) == 0

    #### latcyl_vector, cyllat_vector
    (cyl1dx, cyl1dy, cyl1dz) = latcyl_vector(lat1dx, lat1dy, lat1dz)
    cylpos1d = cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    maxdiff = np.max(np.abs(cylpos1d - pos1d))
    assert maxdiff < 1.e-9

    (lat1dx, lat1dy, lat1dz) = cyllat_vector(cyl1dx, cyl1dy, cyl1dz)
    latpos1d = latrec_vector(lat1dx, lat1dy, lat1dz)
    maxdiff = np.max(np.abs(latpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### recsph
    (sphrad1, sphlat1, sphlon1) = recsph(pos)
    assert round(abs(sphrad1-403626.33912495256), 9) == 0
    assert round(abs(sphlat1 * DPR-108.26566077045815), 15) == 0
    assert round(abs(sphlon1 * DPR--98.34959788856911), 15) == 0

    #### sphrec
    sphpos = sphrec(sphrad1, sphlat1, sphlon1)
    assert round(abs(sphpos[0]-pos[0]), 9) == 0
    assert round(abs(sphpos[1]-pos[1]), 9) == 0
    assert round(abs(sphpos[2]-pos[2]), 9) == 0

    #### recsph_vector, sphrec_vector
    (sph1dx, sph1dy, sph1dz) = recsph_vector(pos1d)
    sphpos1d = sphrec_vector(sph1dx, sph1dy, sph1dz)
    maxdiff = np.max(np.abs(sphpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### latsph
    (sphrad2, sphlat2, sphlon2) = latsph(latrad1, latlon1, latlat1)
    assert round(abs(sphrad2-sphrad1), 9) == 0
    assert round(abs(sphlat2 % TWOPI-sphlat1 % TWOPI), 15) == 0
    assert round(abs(sphlon2 % TWOPI-sphlon1 % TWOPI), 15) == 0

    #### sphlat
    (latrad3, latlon3, latlat3) = sphlat(sphrad2, sphlat2, sphlon2)
    assert round(abs(latrad2-latrad1), 9) == 0
    assert round(abs(latlon2 % TWOPI-latlon1 % TWOPI), 15) == 0
    assert round(abs(latlat2 % TWOPI-latlat1 % TWOPI), 15) == 0

    #### latsph_vector, sphlat_vector
    (sph1dx, sph1dy, sph1dz) = latsph_vector(lat1dx, lat1dy, lat1dz)
    sphpos1d = sphrec_vector(sph1dx, sph1dy, sph1dz)
    maxdiff = np.max(np.abs(sphpos1d - pos1d))
    assert maxdiff < 1.e-9

    (lat1dx, lat1dy, lat1dz) = sphlat_vector(sph1dx, sph1dy, sph1dz)
    latpos1d = latrec_vector(lat1dx, lat1dy, lat1dz)
    maxdiff = np.max(np.abs(latpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### cylsph
    (sphrad3, sphlat3, sphlon3) = cylsph(cylrad1, cyllon1, cylz1)
    assert round(abs(sphrad3-sphrad1), 9) == 0
    assert round(abs(sphlat3 % TWOPI-sphlat1 % TWOPI), 15) == 0
    assert round(abs(sphlon3 % TWOPI-sphlon1 % TWOPI), 15) == 0

    #### sphcyl
    (cylrad3, cyllon3, cylz3) = sphcyl(sphrad3, sphlat3, sphlon3)
    assert round(abs(cylrad3-cylrad1), 9) == 0
    assert round(abs(cyllon3 % TWOPI-cyllon1 % TWOPI), 15) == 0
    assert round(abs(cylz3-cylz1), 9) == 0

    #### cylsph_vector, sphcyl_vector
    (sph1dx, sph1dy, sph1dz) = cylsph_vector(cyl1dx, cyl1dy, cyl1dz)
    sphpos1d = sphrec_vector(sph1dx, sph1dy, sph1dz)
    maxdiff = np.max(np.abs(sphpos1d - pos1d))
    assert maxdiff < 1.e-9

    (cyl1dx, cyl1dy, cyl1dz) = sphcyl_vector(sph1dx, sph1dy, sph1dz)
    cylpos1d = cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    maxdiff = np.max(np.abs(cylpos1d - pos1d))
    assert maxdiff < 1.e-9
