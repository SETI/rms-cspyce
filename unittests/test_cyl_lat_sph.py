##########################################################################################
# test_cyl_lat_sph.py: conversions between rec, cyl, lat, and sph coordinates
##########################################################################################

import numpy as np
import pytest
from pytest import approx
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
    assert pos == pytest.approx([-55658.44323296262, -379226.3293147546, -126505.93063865259], abs=1e-9)

    #### spkpos_vector
    (pos1d, lt1d) = spkpos_vector("Moon", et1d, "J2000", "NONE", "Earth")
    pos1d_ = np.array([[-55658.44323296, -379226.32931475, -126505.93063865],
                       [-55648.84010563, -379227.28937824, -126506.68034533],
                       [-55639.23694455, -379228.24920749, -126507.42997386],
                       [-55629.63374972, -379229.2088025 , -126508.17952426]])
    lt1d_ = np.array([1.3463525460835728, 1.346351921934707, 1.346351297728633,
                    1.3463506734653514])

    for index, value in np.ndenumerate(pos1d):
        assert value == approx(pos1d_[index], abs=1e-7)

    for index, value in np.ndenumerate(lt1d):
        assert value == approx(lt1d_[index], abs=1e-14)

    #### reclat
    (latrad1, latlon1, latlat1) = reclat(pos)
    assert latrad1 == approx(403626.33912495256, abs=1e-9)
    assert latlon1 * DPR == approx(-98.34959788856911, abs=1e-13)
    assert latlat1 * DPR == approx(-18.265660770458155, abs=1e-13)

    #### latrec
    latpos = latrec(latrad1, latlon1, latlat1)
    assert latpos == approx(pos, abs=1e-9)

    #### reclat_vector, latrec_vector
    (lat1dx, lat1dy, lat1dz) = reclat_vector(pos1d)
    latpos1d = latrec_vector(lat1dx, lat1dy, lat1dz)
    maxdiff = np.max(np.abs(latpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### reccyl
    (cylrad1, cyllon1, cylz1) = reccyl(pos)
    assert cylrad1 == approx(383289.01777726377, abs=1e-9)
    assert cyllon1 * DPR == approx((-98.34959788856911 + 360), abs=1e-13)
    assert cylz1 == approx(-126505.9306386526, abs=1e-9)

    #### cylrec
    cylpos = cylrec(cylrad1, cyllon1, cylz1)
    assert cylpos == approx(pos, abs=1e-9)

    #### reccyl_vector, cylrec_vector
    (cyl1dx, cyl1dy, cyl1dz) = reccyl_vector(pos1d)
    cylpos1d = cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    maxdiff = np.max(np.abs(cylpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### latcyl
    (cylrad2, cyllon2, cylz2) = latcyl(latrad1, latlon1, latlat1)
    assert cylrad2 == approx(cylrad1, abs=1e-9)
    assert ((cyllon2 - cyllon1 + TWOPI) % TWOPI) == approx(0, 1e-15)
    assert cylz2 == approx(cylz1, 1e-9)

    #### cyllat
    (latrad2, latlon2, latlat2) = cyllat(cylrad2, cyllon2, cylz2)
    assert latrad2 == approx(latrad1, abs=1e-9)
    assert (latlon2 - latlon1 + TWOPI) % TWOPI == approx(0, abs=1e-15)
    assert (latlat2 - latlat1 + TWOPI) % TWOPI == approx(0, abs=1e-15)

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
    assert sphrad1 == approx(403626.33912495256, abs=1e-9)
    assert sphlat1 * DPR == approx(108.26566077045815, abs=1e-15)
    assert sphlon1 * DPR == approx(-98.34959788856911, abs=1e-15)

    #### sphrec
    sphpos = sphrec(sphrad1, sphlat1, sphlon1)
    assert sphpos == approx(pos, abs=1e-9)

    #### recsph_vector, sphrec_vector
    (sph1dx, sph1dy, sph1dz) = recsph_vector(pos1d)
    sphpos1d = sphrec_vector(sph1dx, sph1dy, sph1dz)
    maxdiff = np.max(np.abs(sphpos1d - pos1d))
    assert maxdiff < 1.e-9

    #### latsph
    (sphrad2, sphlat2, sphlon2) = latsph(latrad1, latlon1, latlat1)
    assert sphrad2 == approx(sphrad1, abs=1e-9)
    assert (sphlat2 - sphlat1 + TWOPI) % TWOPI == approx(0, abs=1e-15)
    assert (sphlon2 - sphlon1 + TWOPI) % TWOPI == approx(0, abs=1e-15)

    #### sphlat
    (latrad3, latlon3, latlat3) = sphlat(sphrad2, sphlat2, sphlon2)
    assert latrad3 == approx(latrad1, abs=1e-9)
    assert (latlat3 - latlat1 + TWOPI) % TWOPI == approx(0, abs=1e-15)
    assert (latlon3 - latlon1 + TWOPI) % TWOPI == approx(0, abs=1e-15)

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
    assert sphrad3 == approx(sphrad1, abs=1e-9)
    assert (sphlat3 - sphlat1 + TWOPI) % TWOPI == approx(0, abs=1e-15)
    assert (sphlon3 - sphlon1 + TWOPI) % TWOPI == approx(0, abs=1e-15)

    #### sphcyl
    (cylrad3, cyllon3, cylz3) = sphcyl(sphrad3, sphlat3, sphlon3)
    assert cylrad3 == approx(cylrad1, abs=1e-9)
    assert (cyllon3 - cyllon1 + TWOPI) % TWOPI == approx(0, abs=1e-15)
    assert cylz3 == approx(cylz1, abs=1e-9)

    #### cylsph_vector, sphcyl_vector
    (sph1dx, sph1dy, sph1dz) = cylsph_vector(cyl1dx, cyl1dy, cyl1dz)
    sphpos1d = sphrec_vector(sph1dx, sph1dy, sph1dz)
    maxdiff = np.max(np.abs(sphpos1d - pos1d))
    assert maxdiff < 1.e-9

    (cyl1dx, cyl1dy, cyl1dz) = sphcyl_vector(sph1dx, sph1dy, sph1dz)
    cylpos1d = cylrec_vector(cyl1dx, cyl1dy, cyl1dz)
    maxdiff = np.max(np.abs(cylpos1d - pos1d))
    assert maxdiff < 1.e-9
