################################################################################
# test_errors.py: Unit tests for error handling.
################################################################################

from __future__ import print_function

import sys
import numpy as np
import numbers
import cspyce as s
import unittest

class Test_cspyce_errors(unittest.TestCase):

  def runTest(self):

    #### erract, errdev, errprt I/O

    self.assertEqual(s.erract(), 'EXCEPTION')
    self.assertEqual(s.erract('GET'), 'EXCEPTION')
    self.assertEqual(s.erract('GET', 'ignored'), 'EXCEPTION')
    self.assertEqual(s.erract('SET', 'IGNORE'), 'RETURN')
    self.assertEqual(s.erract(), 'EXCEPTION')   # always map return to one of these
    self.assertEqual(s.erract('set', 'RETURN'), 'RETURN')
    self.assertEqual(s.erract(), 'EXCEPTION')
    self.assertEqual(s.erract('RUNTIME'), 'RUNTIME')
    self.assertEqual(s.erract(), 'RUNTIME')
    self.assertEqual(s.erract('set', 'RETURN'), 'RETURN')
    self.assertEqual(s.erract(), 'RUNTIME')     # always map return to one of these
    s.erract('set', '  exception')
    self.assertEqual(s.erract(), 'EXCEPTION')

    self.assertEqual(s.errdev(), 'NULL')
    self.assertEqual(s.errdev('GET'), 'NULL')
    self.assertEqual(s.errdev('GET', 'ignored'), 'NULL')
    self.assertEqual(s.errdev('SET', 'foo.txt'), 'foo.txt')
    self.assertEqual(s.errdev('bar.txt'), 'bar.txt')
    self.assertEqual(s.errdev(), 'bar.txt')
    self.assertEqual(s.errdev('SET', 'SCREEN'), 'SCREEN')
    self.assertEqual(s.errdev(), 'SCREEN')

    self.assertEqual(s.errdev('SET', 'NULL'), 'NULL')
    self.assertEqual(s.errdev(), 'NULL')

    default = 'SHORT, LONG, EXPLAIN, TRACEBACK, DEFAULT'
    self.assertEqual(s.errprt(), default)
    self.assertEqual(s.errprt('GET'), default)
    self.assertEqual(s.errprt('GET', 'ignore'), default)
    self.assertEqual(s.errprt('SET', 'NONE'), 'NONE')
    self.assertEqual(s.errprt('get'), '')
    self.assertEqual(s.errprt('SET', 'SHORT, TRACEBACK'), 'SHORT, TRACEBACK')
    self.assertEqual(s.errprt(), 'SHORT, TRACEBACK')
    self.assertEqual(s.errprt('LONG'), 'LONG')
    self.assertEqual(s.errprt(), 'SHORT, LONG, TRACEBACK')
    self.assertEqual(s.errprt('SET', 'NONE'), 'NONE')
    self.assertEqual(s.errprt(default), default)
    self.assertEqual(s.errprt(), default)

    #### chkin, chkout, trcdep, trcnam, qcktrc, sigerr with Python exceptions

    s.erract('set', 'exception')
    self.assertEqual(s.erract(), 'EXCEPTION')
    s.erract('SET', ' ExcEptIon  ')
    self.assertEqual(s.erract(), 'EXCEPTION')
    s.errdev('set', 'screen')
    self.assertEqual(s.errdev(), 'SCREEN')

    s.chkin('zero')
    s.chkin('one')
    s.chkin('two')
    print(s.qcktrc())
    self.assertEqual(s.trcdep(), 3)
    self.assertEqual(s.trcnam(0), 'zero')
    self.assertEqual(s.trcnam(1), 'one')
    self.assertEqual(s.trcnam(2), 'two')
    self.assertEqual(s.qcktrc(), 'zero --> one --> two')

    print()
    print('*** One RuntimeError message should appear below')
    print('*** SPICE(INVALIDARRAYSHAPE) --')
    print('*** Traceback: zero --> one --> two --> vadd')
    s.erract('RUNTIME')
    self.assertRaises(RuntimeError, s.vadd, [1,2,3], [4,5,6,7])

    print()
    print('*** One ValueError message should appear below')
    print('*** SPICE(INVALIDARRAYSHAPE) --')
    print('*** Traceback: zero --> one --> two --> vadd')
    s.erract('EXCEPTION')
    self.assertRaises(ValueError, s.vadd, [1,2,3], [4,5,6,7])

    self.assertEqual(s.trcdep(), 3)
    self.assertEqual(s.trcnam(2), 'two')
    self.assertEqual(s.getmsg('short'), 'SPICE(INVALIDARRAYSHAPE)')

    s.errdev('set', 'null')
    try:
        s.vadd([1,2,3], [4,5,6,7])
    except ValueError as error:
        e = error

    self.assertEqual(str(e), s.getmsg('short') + ' -- vadd -- ' + s.getmsg('long'))

    s.errdev('set', 'screen')
    print()
    print('*** One error message should appear below')
    print('*** Error test -- \\n\\nThis is an error test')
    print('*** Traceback: zero --> one --> two')
    s.setmsg('This is an error test')
    self.assertRaises(RuntimeError, s.sigerr, "Error test")

    self.assertEqual(s.trcdep(), 2)
    s.errdev('set', 'null')

    self.assertRaises(RuntimeError, s.sigerr, "Error test")
    self.assertEqual(s.getmsg('short'), 'Error test')
    self.assertFalse(s.failed())
    self.assertEqual(s.trcdep(), 1)
    self.assertEqual(s.qcktrc(), 'zero')

    s.reset()

    self.assertEqual(s.getmsg('short'), '')
    self.assertEqual(s.trcdep(), 1)
    self.assertEqual(s.qcktrc(), 'zero')

    self.assertRaises(RuntimeError, s.sigerr, "222")
    self.assertEqual(s.getmsg('short'), '222')
    self.assertFalse(s.failed())
    self.assertEqual(s.trcdep(), 0)
    self.assertEqual(s.qcktrc(), '')

    self.assertRaises(RuntimeError, s.sigerr, "333")
    self.assertEqual(s.getmsg('short'), '333')
    self.assertFalse(s.failed())
    self.assertEqual(s.trcdep(), 0)
    self.assertEqual(s.qcktrc(), '')

    s.reset()

    self.assertEqual(s.getmsg('short'), '')

    self.assertRaises(KeyError, s.bodn2c, 'abc')
    self.assertEqual(s.getmsg('short'), 'SPICE(BODYNAMENOTFOUND)')
    self.assertEqual(s.getmsg('long'),
                     'body name "abc" not found in kernel pool')
    self.assertFalse(s.failed())

    #### chkin, chkout, trcdep, trcnam, sigerr with erract="EXCEPTION"

    s.erract('set', 'exception')
    self.assertEqual(s.erract(), 'EXCEPTION')
    s.errdev('set', 'screen')
    s.chkin('zero')
    s.chkin('one')
    s.chkin('two')
    self.assertEqual(s.trcdep(), 3)
    self.assertEqual(s.trcnam(0), 'zero')
    self.assertEqual(s.trcnam(1), 'one')
    self.assertEqual(s.trcnam(2), 'two')
    self.assertEqual(s.qcktrc(), 'zero --> one --> two')

    print()
    print('*** One error message should appear below')
    print('*** SPICE(INVALIDARRAYSHAPE) --')
    print('*** Traceback: zero --> one --> two --> vadd')
    try:
        _ = s.vadd([1,2,3], [4,5,6,7])
    except ValueError as e:
        print(e)

    self.assertEqual(s.trcdep(), 3)
    self.assertEqual(s.trcnam(2), 'two')
    self.assertEqual(s.getmsg('short'), 'SPICE(INVALIDARRAYSHAPE)')
    self.assertEqual(s.qcktrc(), 'zero --> one --> two')

    s.reset()

    self.assertEqual(s.trcdep(), 3)
    self.assertEqual(s.trcnam(2), 'two')
    self.assertEqual(s.getmsg('short'), '')
    self.assertFalse(s.failed())
    self.assertEqual(s.qcktrc(), 'zero --> one --> two')

    print()
    print('*** One error message should appear below')
    print('*** Error test -- \\n\\nThis is an error test')
    print('*** Traceback: zero --> one --> two')

    s.setmsg('This is an error test')
    try:
        s.sigerr("Error test")
    except RuntimeError as e:
        print(e)

    self.assertEqual(s.trcdep(), 2)
    self.assertEqual(s.trcnam(1), 'one')
    self.assertEqual(s.getmsg('short'), 'Error test')
    self.assertEqual(s.getmsg('long'), 'This is an error test')
    self.assertEqual(s.qcktrc(), 'zero --> one')

    s.reset()

    self.assertEqual(s.trcdep(), 2)
    self.assertEqual(s.trcnam(1), 'one')
    self.assertEqual(s.getmsg('short'), '')
    self.assertEqual(s.getmsg('long'), '')
    self.assertFalse(s.failed())
    self.assertEqual(s.qcktrc(), 'zero --> one')

    s.errdev('set', 'null')
    try:
        s.sigerr("Error test")
    except RuntimeError as e:
        pass

    self.assertEqual(s.trcdep(), 1)
    self.assertEqual(s.getmsg('short'), 'Error test')
    self.assertEqual(s.getmsg('long'), '')
    self.assertEqual(s.qcktrc(), 'zero')

    s.reset()

    self.assertEqual(s.trcdep(), 1)
    self.assertEqual(s.getmsg('short'), '')
    self.assertFalse(s.failed())
    self.assertEqual(s.qcktrc(), 'zero')

    try:
        s.sigerr("222")
    except RuntimeError as e:
        pass

    self.assertEqual(s.trcdep(), 0)
    self.assertEqual(s.getmsg('short'), '222')
    self.assertEqual(s.getmsg('long'), '')
    self.assertEqual(s.qcktrc(), '')

    s.reset()

    self.assertEqual(s.trcdep(), 0)
    self.assertEqual(s.getmsg('short'), '')
    self.assertEqual(s.qcktrc(), '')

    try:
        s.sigerr("333")
    except RuntimeError as e:
        pass

    self.assertEqual(s.trcdep(), 0)
    self.assertEqual(s.getmsg('short'), '333')
    self.assertEqual(s.getmsg('long'), '')
    self.assertEqual(s.qcktrc(), '')

    s.reset()

    self.assertEqual(s.trcdep(), 0)
    self.assertEqual(s.getmsg('short'), '')
    self.assertEqual(s.qcktrc(), '')

    #### setmsg, errdp, errint, errch

    s.erract('set', 'exception')

    self.assertRaises(RuntimeError, s.sigerr, 'Short')
    self.assertFalse(s.failed())

    try:
        s.sigerr('Short')
    except RuntimeError as e:
        error = e

    self.assertEqual(str(error), 'Short -- ')

    s.setmsg('Long')
    try:
        s.sigerr('Short')
    except RuntimeError as e:
        error = e

    self.assertEqual(str(error), 'Short -- Long')

    s.setmsg('Long pi=#; four=#; foo="#"')
    self.assertEqual(s.getmsg('LONG'), 'Long pi=#; four=#; foo="#"')
    s.errdp('#', 3.14159)
    s.errint('#', 4)
    s.errch('#', 'FOO')
    msg = s.getmsg('LONG')
    self.assertEqual(msg, 'Long pi=3.1415900000000E+00; four=4; foo="FOO"')

    s.chkin('foo')
    s.chkin('bar')
    self.assertEqual(s.trcdep(), 2)
    self.assertEqual(s.trcnam(1), 'bar')

    try:
        s.sigerr('Short')
    except RuntimeError as e:
        error = e

    self.assertEqual(str(error), 'Short -- bar -- ' + msg)
    self.assertEqual(s.getmsg('short'), 'Short')
    self.assertEqual(s.getmsg('long'), msg)
    self.assertEqual(s.trcdep(), 1)
    self.assertEqual(s.trcnam(0), 'foo')

    s.reset()

    self.assertEqual(s.getmsg('short'), '')
    self.assertEqual(s.getmsg('long'), '')
    self.assertEqual(s.trcdep(), 1)
    self.assertEqual(s.trcnam(0), 'foo')

    s.chkout('foo')

    self.assertEqual(s.trcdep(), 0)

################################################################################

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
