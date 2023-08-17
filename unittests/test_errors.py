################################################################################
# test_errors.py: Unit tests for error handling.
################################################################################

import cspyce as s
import pytest


def cleanup_errors():
    length = s.trcdep()
    for index in reversed(range(length)):
        module = s.trcnam(index)
        s.chkout(module)
    s.reset()
    s.erract('SET', 'EXCEPTION')
    s.errdev('SET', 'NULL')


@pytest.fixture(autouse=True)
def cleanup():
    cleanup_errors()
    yield
    cleanup_errors()


def test_erract_set_and_get():
    cleanup_errors()
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

    s.erract('set', 'exception')
    assert s.erract() == 'EXCEPTION'


def test_errdev_set_and_get():
    assert s.errdev('GET') == 'NULL'
    assert s.errdev('GET', 'ignored') == 'NULL'
    assert s.errdev('SET', 'foo.txt') == 'foo.txt'
    assert s.errdev('bar.txt') == 'bar.txt'
    assert s.errdev() == 'bar.txt'
    assert s.errdev('SET', 'SCREEN') == 'SCREEN'
    assert s.errdev() == 'SCREEN'
    assert s.errdev('SET', 'NULL') == 'NULL'
    assert s.errdev() == 'NULL'
    assert s.errdev() == 'NULL'

    s.errdev('set', 'screen')
    assert s.errdev() == 'SCREEN'


def test_errprt_set_and_get():
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


def test_chkin_quicktrace():
    s.chkin('zero')
    s.chkin('one')
    s.chkin('two')
    assert s.trcdep() == 3
    assert s.trcnam(0) == 'zero'
    assert s.trcnam(1) == 'one'
    assert s.trcnam(2) == 'two'
    assert s.qcktrc() == 'zero --> one --> two'

    s.erract('RUNTIME')
    try:
        s.vadd([1, 2, 3], [4, 5, 6, 7])
    except RuntimeError as e:
        exception = e
        # TODO(fy): We should be seeing zero --> one --> two --> vadd
        # somewhere in the traceback, but we're not.

    assert s.trcdep() == 3
    assert s.trcnam(2) == 'two'
    assert s.getmsg('short') == 'SPICE(INVALIDARRAYSHAPE)'
    assert str(exception) == s.getmsg('short') + ' -- vadd -- ' + s.getmsg('long')


def test_external_errors():
    with pytest.raises(KeyError):
        s.bodn2c('abc')
    assert s.getmsg('short') == 'SPICE(BODYNAMENOTFOUND)'
    assert s.getmsg('long') == 'body name "abc" not found in kernel pool'
    assert not s.failed()


def test_Setting_msg_and_error():
    s.setmsg('Long')
    try:
        s.sigerr('Short')
    except RuntimeError as e:
        error = e
    assert str(error) == 'Short -- sigerr -- Long'


def test_set_msg():
    s.setmsg('Long pi=#; four=#; foo="#"')
    assert s.getmsg('LONG') == 'Long pi=#; four=#; foo="#"'
    s.errdp('#', 3.14159)
    s.errint('#', 4)
    s.errch('#', 'FOO')
    msg = s.getmsg('LONG')
    assert msg == 'Long pi=3.1415900000000E+00; four=4; foo="FOO"'


def fail_output_to_screen(capfd):
    # This test seems to run fine when run singly, but fails when run as part of a
    # larger pytest.  Somehow the ability to catch what is written to stdout is
    # different.  Need to investigate.
    s.errdev('set', 'screen')
    s.chkin('Name1')
    s.chkout('Name2')
    out, _err = capfd.readouterr()
    assert "Caller is Name2" in out
    assert "popped name is Name1" in out


def test_no_output_to_screen(capfd):
    s.errdev('set', 'NULL')
    s.chkin('Name1')
    s.chkout('Name2')
    out, err = capfd.readouterr()
    assert not out
    assert not err
