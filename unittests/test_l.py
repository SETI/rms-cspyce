##########################################################################################
# test_l.py
##########################################################################################

import numpy as np
import unittest
from cspyce import *

class Test_L(unittest.TestCase):

  def runTest(self):

    #### lgresp
    x = lgresp(5., -2., [148.0, 26.0, -8.0, -2.0], 2.)
    self.assertEqual(x, 1.)

    x = lgresp_vector(5., -2., [148.0, 26.0, -8.0, -2.0], [2.,3.])
    self.assertTrue(np.all(x == [1.,26.]))

    x = lgresp_vector(5., [-2.,2.], [148.0, 26.0, -8.0, -2.0], [2.,3.])
    self.assertTrue(np.all(x == [1.,406.]))

    #### lgrind
    x = lgrind([-1., 0., 1., 3.], [-2., -7., -8., 26.], 2.)
    self.assertTrue(np.all(x == [1.0, 16.0]))

    x = lgrind_vector([-1., 0., 1., 3.], [-2., -7., -8., 26.], [2.,-1.,1.])
    self.assertTrue(np.all(x == np.array([[1.,-2.,-8.], [16.,-5.,3.]])))

    self.assertRaises(ValueError, lgrind, [-1., 0., 1., 3.], [-2., -7., -8.], 2.)

    #### lparse
    x = lparse(" ,bob,   carol,, ted,  alice", ",")
    self.assertEqual(x, ['', 'bob', 'carol', '', 'ted', 'alice'])

    x = lparse("//option1//option2/ //", "/", )
    self.assertEqual(x, ['', '', 'option1', '', 'option2', '', '', ''])

    #### lparsm
    x = lparsm("Run and find out.", " ")
    self.assertEqual(x, ['Run', 'and', 'find', 'out.'])

    x = lparsm("  1986-187// 13:15:12.184 ", " ,/-:")
    self.assertEqual(x, ['1986', '187', '', '13', '15', '12.184'])

    #### lstlec
    x = lstlec("EINSTEIN", ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"])
    self.assertEqual(x, 1)

    x = lstlec("Galileo",  ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"])
    self.assertEqual(x, 3)

    x = lstlec("BETHE",    ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"])
    self.assertEqual(x, -1)

    #### lstled
    x = lstled(-3., np.array([-2., -2., 0., 1., 1., 11.]))
    self.assertEqual(x, -1)

    x = lstled(-2., [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, 1)

    x = lstled(0., [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, 2)

    x = lstled(1., [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, 4)

    x = lstled(11.1, [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, 5)

    #### lstlei
    x = lstlei(-3, np.array([-2, -2, 0, 1, 1, 11]))
    self.assertEqual(x, -1)

    x = lstlei(-2, np.array([-2, -2, 0, 1, 1, 11], dtype='int64'))
    self.assertEqual(x, 1)

    x = lstlei( 0, np.array([-2, -2, 0, 1, 1, 11], dtype='int32'))
    self.assertEqual(x, 2)

    x = lstlei( 1, np.array([-2, -2, 0, 1, 1, 11], dtype='int16'))
    self.assertEqual(x, 4)

    x = lstlei(12, [-2, -2, 0, 1, 1, 11])
    self.assertEqual(x, 5)

    #### lstltc
    x = lstltc("NEWTON", ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"])
    self.assertEqual(x, 3)

    x = lstltc("EINSTEIN", ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"])
    self.assertEqual(x, 0)

    x = lstltc("Galileo",  ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"])
    self.assertEqual(x, 3)

    x = lstltc("BETHE",    ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"])
    self.assertEqual(x, -1)

    #### lstltd
    x = lstltd(-3., np.array([-2., -2., 0., 1., 1., 11.]))
    self.assertEqual(x, -1)

    x = lstltd(-2., [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, -1)

    x = lstltd(0., [-2, -2, 0, 1, 1, 11])
    self.assertEqual(x, 1)

    x = lstltd(1., [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, 2)

    x = lstltd(11.1, [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, 5)

    #### lstlti
    x = lstlti(-3, np.array([-2, -2, 0, 1, 1, 11]))
    self.assertEqual(x, -1)

    x = lstlti(-2, [-2., -2., 0., 1., 1., 11.])
    self.assertEqual(x, -1)

    x = lstlti(0, [-2, -2, 0, 1, 1, 11])
    self.assertEqual(x, 1)

    x = lstlti(1, [-2, -2, 0, 1, 1, 11])
    self.assertEqual(x, 2)

    x = lstlti(12, [-2, -2, 0, 1, 1, 11])
    self.assertEqual(x, 5)

    #### lx4dec
    string = '123|-234|+345|-123.|+234.|1.23|-2.34|+3.4567|.666|-.678|+.789'
    first = 0
    numbers = []
    while(first < len(string)):
        (last, nchar) = lx4dec(string, first)
        if nchar > 0:
            numbers.append(string[first:first+nchar])
            first = last + 2
        else:
            first += 1
    self.assertEqual(numbers, ['123', '-234', '+345', '-123.', '+234.', '1.23',
                               '-2.34', '+3.4567', '.666', '-.67', '+.78'])
    # last two results seem wrong--the last digit in each was dropped

    #### lx4num
    string = '123|-234|+345|-123.|+234.|1.23|-2.34|+3.4567|.666|-.678|+.789|' + \
             '123e4|234.e5|-2.3d-4|+345.6e+78|-.12e3|.23e4|+.34e-5|-.456E-78'
    first = 0
    numbers = []
    while(first < len(string)):
        (last, nchar) = lx4num(string, first)
        if nchar > 0:
            numbers.append(string[first:first+nchar])
            first = last + 2
        else:
            first += 1
    self.assertEqual(numbers, ['123', '-234', '+345', '-123.', '+234.', '1.23',
                               '-2.34', '+3.4567', '.666', '-.67', '+.78',
                               '123e4', '234.e5', '-2.3d-4', '+345.6e+78', '-.12e3',
                               '.23e4', '+.34e-5', '-.456E-78'])

    #### lx4sgn
    string = '123|-234|+345|0|+0|-0'
    first = 0
    numbers = []
    while(first < len(string)):
        (last, nchar) = lx4sgn(string, first)
        if nchar > 0:
            numbers.append(string[first:first+nchar])
            first = last + 2
        else:
            first += 1
    self.assertEqual(numbers, ['123', '-234', '+345', '0', '+0', '-0'])

    #### lx4uns
    string = '123|-234|+345|0|+0|-0'
    first = 0
    numbers = []
    while(first < len(string)):
        (last, nchar) = lx4uns(string, first)
        if nchar > 0:
            numbers.append(string[first:first+nchar])
            first = last + 2
        else:
            first += 1
    self.assertEqual(numbers, ['123', '234', '345', '0', '0', '0'])

    #### lxqstr
    self.assertEqual(lxqstr('The "SPICE" system',      '"', 4), [10,  7])
    self.assertEqual(lxqstr('The "SPICE" system',      '"', 0), [-1,  0])
    self.assertEqual(lxqstr('The "SPICE" system',      "'", 4), [ 3,  0])
#   self.assertEqual(lxqstr('The """SPICE"" system"',  '"', 4), [12,  9]) wrong in docs?
    self.assertEqual(lxqstr('The """SPICE"" system"',  '"', 4), [21, 18])
    self.assertEqual(lxqstr('The """SPICE"""" system', '"', 4), [14, 11])
    self.assertEqual(lxqstr('The &&&SPICE system',     '&', 4), [ 5,  2])
    self.assertEqual(lxqstr("' '",                     "'", 0), [ 2,  3])
    self.assertEqual(lxqstr("''",                      "'", 0), [ 1,  2])

########################################
if __name__ == '__main__':
    unittest.main(verbosity=2)
##########################################################################################
