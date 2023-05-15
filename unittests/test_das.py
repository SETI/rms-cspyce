import unittest
import cspyce as cs
import numpy as np
import numpy.testing as npt

class DasTestCase(unittest.TestCase):
    def test_read_write_integers(self):
        handle = cs.dasops()
        # Add ten elements
        cs.dasadi(handle, [10, 20, 30, 40, 50])
        cs.dasadi(handle, [100, 200, 300, 400, 500])

        # Reading the 5th and 6th gives us 50, 100 in a 32-bit int array
        result = cs.dasrdi(handle, 5, 6)
        self.assertEqual(np.int32, result.dtype)
        self.assertEqual([50, 100], list(result))

        # Modify two of the elements, and then read them.
        cs.dasudi(handle, 2, 3, [-1, -2])
        result = cs.dasrdi(handle, 1, 5)
        self.assertEqual( [10, -1, -2, 40, 50], list(result))

    def test_read_write_floats(self):
        handle = cs.dasops()
        # Add ten elements. These will be upgraded to doubls
        cs.dasadd(handle, [10, 20, 30, 40, 50])
        cs.dasadd(handle, [100, 200, 300, 400, 500])

        # Reading the 5th and 6th gives us 50.0 and 100.0
        result = cs.dasrdd(handle, 5, 6)
        self.assertEqual(result.dtype, np.double)
        self.assertEqual([50.0, 100.0], list(result))

        # Modify two of the lements, and then read them.
        cs.dasudd(handle, 2, 3, [-1, -2])
        result = cs.dasrdd(handle, 1, 5)
        self.assertEqual([10.0, -1.0, -2.0, 40.0, 50.0], list(result))

    def test_read_write_char(self):
        handle = cs.dasops()
        # Make the characters be bcdefghijkBCDEFGHIJK by taking 1:11 of each string
        cs.dasadc(handle, 20, 1, 10, ['abcdefghijklmnop', 'ABCDEFGHIJKLMNOP'])

        result = cs.dasrdc(handle, 1, 20, 0, 19)
        self.assertEqual(['bcdefghijkBCDEFGHIJK'], result)

        # Read the same result as two groups of 10
        result = cs.dasrdc(handle, 1, 20, 0, 9)
        self.assertEqual(['bcdefghijk', 'BCDEFGHIJK'], result)

        # Read the same result as three groups of 7
        result = cs.dasrdc(handle, 1, 20, 0, 6)
        self.assertEqual(['bcdefgh', 'ijkBCDE', 'FGHIJK'], result)

        # Offset the results by 1, and chop one character off the end of the saved results
        result = cs.dasrdc(handle, 2, 19, 1, 7)
        self.assertEqual(['\x00cdefghi', '\x00jkBCDEF', '\x00GHIJ'], result)

        # replace characters 1 and 2 with ??
        cs.dasudc(handle, 1, 2, 0, 2, ['?????'])
        result = cs.dasrdc(handle, 1, 5, 0, 4)
        self.assertEqual(['??def'], result)

if __name__ == '__main__':
    unittest.main(verbosity=2)

"""
    handle = cs.dasops()

    # handle = cs.dasonw("/tmp/test.foo", "test", "/tmp/test.foo", 0);
    cs.dasadi(handle, [10, 20, 30, 40, 50])
    cs.dasudi(handle, 4, 4, [200])

    cs.dasadd(handle, [10, 20, 30, 40, 50])
    cs.dasudd(handle, 4, 4, [200])

    cs.dasadc(handle, 40, 0, 19, ["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    # cs.dasadc(handle, 40, 0, 39, ["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV"])

    print(cs.dasrdc(handle, 1, 40, 0, 39))
    print(cs.dasrdc(handle, 1, 40, 0, 19))


def test_double():
    handle = cs.dasops()
    cs.dasadd(handle, [10, 20, 30, 40, 50])
    cs.dasudd(handle, 4, 4, [200])
    print(cs.dasrdd(handle, 1, 5))

def test_int():
    handle = cs.dasops()
    cs.dasadi(handle, [10, 20, 30, 40, 50])
    cs.dasudi(handle, 4, 4, [200])
    print(cs.dasrdi(handle, 1, 5))
"""
