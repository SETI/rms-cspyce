import cspyce as cs
import numpy as np
import numpy.testing as npt
import os
import pytest

@pytest.fixture
def das_handle():
    handle = cs.dasops()
    yield handle
    cs.dascls(handle)

def test_read_write_integers(das_handle):
    # Add ten elements
    cs.dasadi(das_handle, [10, 20, 30, 40, 50])
    cs.dasadi(das_handle, [100, 200, 300, 400, 500])

    # Reading the 5th and 6th gives us 50, 100 in a 32-bit int array
    result = cs.dasrdi(das_handle, 5, 6)
    print(result)
    assert result.dtype == np.int32
    assert list(result) == [50, 100]

    # Modify two of the elements, and then read them.
    cs.dasudi(das_handle, 2, 3, [-1, -2])
    result = cs.dasrdi(das_handle, 1, 5)
    assert list(result) == [10, -1, -2, 40, 50]

def test_read_write_floats(das_handle):
    # Add ten elements. These will be upgraded to doubls
    cs.dasadd(das_handle, [10, 20, 30, 40, 50])
    cs.dasadd(das_handle, [100, 200, 300, 400, 500])

    # Reading the 5th and 6th gives us 50.0 and 100.0
    result = cs.dasrdd(das_handle, 5, 6)
    assert result.dtype == np.double
    assert list(result) == [50.0, 100.0]

    # Modify two of the elements, and then read them.
    cs.dasudd(das_handle, 2, 3, [-1, -2])
    result = cs.dasrdd(das_handle, 1, 5)
    assert list(result) == [10.0, -1.0, -2.0, 40.0, 50.0]

def test_read_write_char(das_handle):
    # Make the characters be bcdefghijkBCDEFGHIJK by taking 1:11 of each string
    cs.dasadc(das_handle, 20, 1, 10, ['abcdefghijklmnop', 'ABCDEFGHIJKLMNOP'])

    result = cs.dasrdc(das_handle, 1, 20, 0, 19)
    assert result == ['bcdefghijkBCDEFGHIJK']

    # Read the same result as two groups of 10
    result = cs.dasrdc(das_handle, 1, 20, 0, 9)
    assert result == ['bcdefghijk', 'BCDEFGHIJK']

    # Read the same result as three groups of 7
    result = cs.dasrdc(das_handle, 1, 20, 0, 6)
    assert result == ['bcdefgh', 'ijkBCDE', 'FGHIJK']

    # Offset the results by 1, and chop one character off the end of the saved results
    result = cs.dasrdc(das_handle, 2, 19, 1, 7)
    assert result == ['\x00cdefghi', '\x00jkBCDEF', '\x00GHIJ']

    # Same test as above, but we're overwriting a string
    result = cs.dasrdc(das_handle, 2, 19, 1, 7, ['123456789'] * 4)
    assert result == ['1cdefghi9', '1jkBCDEF9', '1GHIJ6789', '123456789']

    # replace characters 1 and 2 with ??
    cs.dasudc(das_handle, 1, 2, 0, 2, ['?????'])
    result = cs.dasrdc(das_handle, 1, 5, 0, 4)
    assert result == ['??def']

def test_read_works_with_file(tmp_path):
    # This test writes multiple times to an actual file, closes it,
    # then assures
    filename = str(tmp_path.joinpath("dasfile"))
    handle = cs.dasonw(filename, "temp", filename, 0)
    cs.dasadi(handle, [10, 20, 30, 40, 50])
    cs.dasadd(handle, [100, 200, 300])
    cs.dasadc(handle, 5, 0, 4, ["abcde"])
    cs.dasadi(handle, [60, 70, 80, 90, 100])
    cs.dasadd(handle, [400, 500, 600])
    cs.dasadc(handle, 5, 0, 4, ["fghij"])
    cs.dascls(handle)

    handle = cs.dasopr(filename)
    assert cs.daslla(handle) == [10, 6, 10]  # count of chars, doubles, ints
    assert list(cs.dasrdi(handle, 1, 10)) == [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    assert list(cs.dasrdd(handle, 1, 6)) == [100., 200., 300., 400., 500., 600.]
    assert cs.dasrdc(handle, 1, 10, 0, 9) == ['abcdefghij']
    cs.dascls(handle)
