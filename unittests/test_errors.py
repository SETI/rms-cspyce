################################################################################
# test_errors.py: Unit tests for error handling.
################################################################################

import cspyce as s
import pytest


def test_erract_errdev_errprt():
    assert s.erract() == 'EXCEPTION'
    assert s.erract('GET') == 'EXCEPTION'
    assert s.erract('GET', 'ignored') == 'EXCEPTION'
    assert s.erract('SET', 'IGNORE') == 'RETURN'
    assert s.erract() == 'EXCEPTION'   # always map return to one of these
    assert s.erract('set', 'RETURN') == 'RETURN'
    assert s.erract() == 'EXCEPTION'
    assert s.erract('RUNTIME') == 'RUNTIME'
    assert s.erract() == 'RUNTIME'
    assert s.erract('set', 'RETURN') == 'RETURN'
    assert s.erract() == 'RUNTIME'     # always map return to one of these
    s.erract('set', '  exception')
    assert s.erract() == 'EXCEPTION'

    assert s.errdev() == 'NULL'
    assert s.errdev('GET') == 'NULL'
    assert s.errdev('GET', 'ignored') == 'NULL'
    assert s.errdev('SET', 'foo.txt') == 'foo.txt'
    assert s.errdev('bar.txt') == 'bar.txt'
    assert s.errdev() == 'bar.txt'
    assert s.errdev('SET', 'SCREEN') == 'SCREEN'
    assert s.errdev() == 'SCREEN'

    assert s.errdev('SET', 'NULL') == 'NULL'
    assert s.errdev() == 'NULL'

    default = 'SHORT, LONG, EXPLAIN, TRACEBACK, DEFAULT'
    assert s.errprt() == default
    assert s.errprt('GET') == default
    assert s.errprt('GET', 'ignore') == default
    assert s.errprt('SET', 'NONE') == 'NONE'
    assert s.errprt('get') == ''
    assert s.errprt('SET', 'SHORT, TRACEBACK') == 'SHORT, TRACEBACK'
    assert s.errprt() == 'SHORT, TRACEBACK'
    assert s.errprt('LONG') == 'LONG'
    assert s.errprt() == 'SHORT, LONG, TRACEBACK'
    assert s.errprt('SET', 'NONE') == 'NONE'
    assert s.errprt(default) == default
    assert s.errprt() == default

    #### chkin, chkout, trcdep, trcnam, qcktrc, sigerr with Python exceptions

    s.erract('set', 'exception')
    assert s.erract() == 'EXCEPTION'
    s.erract('SET', ' ExcEptIon  ')
    assert s.erract() == 'EXCEPTION'
    s.errdev('set', 'screen')
    assert s.errdev() == 'SCREEN'

    s.chkin('zero')
    s.chkin('one')
    s.chkin('two')
    print(s.qcktrc())
    assert s.trcdep() == 3
    assert s.trcnam(0) == 'zero'
    assert s.trcnam(1) == 'one'
    assert s.trcnam(2) == 'two'
    assert s.qcktrc() == 'zero --> one --> two'

    print()
    print('*** One RuntimeError message should appear below')
    print('*** SPICE(INVALIDARRAYSHAPE) --')
    print('*** Traceback: zero --> one --> two --> vadd')
    s.erract('RUNTIME')
    with pytest.raises(RuntimeError):
        s.vadd([1,2,3], [4,5,6,7])

    print()
    print('*** One ValueError message should appear below')
    print('*** SPICE(INVALIDARRAYSHAPE) --')
    print('*** Traceback: zero --> one --> two --> vadd')
    s.erract('EXCEPTION')
    with pytest.raises(ValueError):
        s.vadd([1,2,3], [4,5,6,7])

    assert s.trcdep() == 3
    assert s.trcnam(2) == 'two'
    assert s.getmsg('short') == 'SPICE(INVALIDARRAYSHAPE)'

    s.errdev('set', 'null')
    try:
        s.vadd([1,2,3], [4,5,6,7])
    except ValueError as error:
        e = error

    assert str(e) == s.getmsg('short') + ' -- vadd -- ' + s.getmsg('long')

    s.errdev('set', 'screen')
    print()
    print('*** One error message should appear below')
    print('*** Error test -- \\n\\nThis is an error test')
    print('*** Traceback: zero --> one --> two')
    s.setmsg('This is an error test')
    with pytest.raises(RuntimeError):
        s.sigerr("Error test")

    assert s.trcdep() == 2
    s.errdev('set', 'null')

    with pytest.raises(RuntimeError):
        s.sigerr("Error test")
    assert s.getmsg('short') == 'Error test'
    assert not s.failed()
    assert s.trcdep() == 1
    assert s.qcktrc() == 'zero'

    s.reset()

    assert s.getmsg('short') == ''
    assert s.trcdep() == 1
    assert s.qcktrc() == 'zero'

    with pytest.raises(RuntimeError):
        s.sigerr("222")
    assert s.getmsg('short') == '222'
    assert not s.failed()
    assert s.trcdep() == 0
    assert s.qcktrc() == ''

    with pytest.raises(RuntimeError):
        s.sigerr("333")
    assert s.getmsg('short') == '333'
    assert not s.failed()
    assert s.trcdep() == 0
    assert s.qcktrc() == ''

    s.reset()

    assert s.getmsg('short') == ''

    with pytest.raises(KeyError):
        s.bodn2c('abc')
    assert s.getmsg('short') == 'SPICE(BODYNAMENOTFOUND)'
    assert s.getmsg('long') == 'body name "abc" not found in kernel pool'
    assert not s.failed()

    #### chkin, chkout, trcdep, trcnam, sigerr with erract="EXCEPTION"

    s.erract('set', 'exception')
    assert s.erract() == 'EXCEPTION'
    s.errdev('set', 'screen')
    s.chkin('zero')
    s.chkin('one')
    s.chkin('two')
    assert s.trcdep() == 3
    assert s.trcnam(0) == 'zero'
    assert s.trcnam(1) == 'one'
    assert s.trcnam(2) == 'two'
    assert s.qcktrc() == 'zero --> one --> two'

    print()
    print('*** One error message should appear below')
    print('*** SPICE(INVALIDARRAYSHAPE) --')
    print('*** Traceback: zero --> one --> two --> vadd')
    try:
        _ = s.vadd([1,2,3], [4,5,6,7])
    except ValueError as e:
        print(e)

    assert s.trcdep() == 3
    assert s.trcnam(2) == 'two'
    assert s.getmsg('short') == 'SPICE(INVALIDARRAYSHAPE)'
    assert s.qcktrc() == 'zero --> one --> two'

    s.reset()

    assert s.trcdep() == 3
    assert s.trcnam(2) == 'two'
    assert s.getmsg('short') == ''
    assert not s.failed()
    assert s.qcktrc() == 'zero --> one --> two'

    print()
    print('*** One error message should appear below')
    print('*** Error test -- \\n\\nThis is an error test')
    print('*** Traceback: zero --> one --> two')

    s.setmsg('This is an error test')
    try:
        s.sigerr("Error test")
    except RuntimeError as e:
        print(e)

    assert s.trcdep() == 2
    assert s.trcnam(1) == 'one'
    assert s.getmsg('short') == 'Error test'
    assert s.getmsg('long') == 'This is an error test'
    assert s.qcktrc() == 'zero --> one'

    s.reset()

    assert s.trcdep() == 2
    assert s.trcnam(1) == 'one'
    assert s.getmsg('short') == ''
    assert s.getmsg('long') == ''
    assert not s.failed()
    assert s.qcktrc() == 'zero --> one'

    s.errdev('set', 'null')
    try:
        s.sigerr("Error test")
    except RuntimeError as e:
        pass

    assert s.trcdep() == 1
    assert s.getmsg('short') == 'Error test'
    assert s.getmsg('long') == ''
    assert s.qcktrc() == 'zero'

    s.reset()

    assert s.trcdep() == 1
    assert s.getmsg('short') == ''
    assert not s.failed()
    assert s.qcktrc() == 'zero'

    try:
        s.sigerr("222")
    except RuntimeError as e:
        pass

    assert s.trcdep() == 0
    assert s.getmsg('short') == '222'
    assert s.getmsg('long') == ''
    assert s.qcktrc() == ''

    s.reset()

    assert s.trcdep() == 0
    assert s.getmsg('short') == ''
    assert s.qcktrc() == ''

    try:
        s.sigerr("333")
    except RuntimeError as e:
        pass

    assert s.trcdep() == 0
    assert s.getmsg('short') == '333'
    assert s.getmsg('long') == ''
    assert s.qcktrc() == ''

    s.reset()

    assert s.trcdep() == 0
    assert s.getmsg('short') == ''
    assert s.qcktrc() == ''

    #### setmsg, errdp, errint, errch

    s.erract('set', 'exception')

    with pytest.raises(RuntimeError):
        s.sigerr('Short')
    assert not s.failed()

    try:
        s.sigerr('Short')
    except RuntimeError as e:
        error = e

    assert str(error) == 'Short -- '

    s.setmsg('Long')
    try:
        s.sigerr('Short')
    except RuntimeError as e:
        error = e

    assert str(error) == 'Short -- Long'

    s.setmsg('Long pi=#; four=#; foo="#"')
    assert s.getmsg('LONG') == 'Long pi=#; four=#; foo="#"'
    s.errdp('#', 3.14159)
    s.errint('#', 4)
    s.errch('#', 'FOO')
    msg = s.getmsg('LONG')
    assert msg == 'Long pi=3.1415900000000E+00; four=4; foo="FOO"'

    s.chkin('foo')
    s.chkin('bar')
    assert s.trcdep() == 2
    assert s.trcnam(1) == 'bar'

    try:
        s.sigerr('Short')
    except RuntimeError as e:
        error = e

    assert str(error) == 'Short -- bar -- ' + msg
    assert s.getmsg('short') == 'Short'
    assert s.getmsg('long') == msg
    assert s.trcdep() == 1
    assert s.trcnam(0) == 'foo'

    s.reset()

    assert s.getmsg('short') == ''
    assert s.getmsg('long') == ''
    assert s.trcdep() == 1
    assert s.trcnam(0) == 'foo'

    s.chkout('foo')

    assert s.trcdep() == 0
