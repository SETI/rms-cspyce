################################################################################
# cspyce/cspyce1.py
#
# This module provides several enhancements over the low-level cspyce0 interface
# to the CSPICE library. See cspyce/__init__.py for a full explanation.
#
# Used internally by cspyce; not intended for direct import.
################################################################################
import numpy as np
import textwrap
from contextlib import contextmanager

from cspyce import cspyce0
from cspyce.cspyce0 import *

from cspyce.cspyce1_info import \
    CSPYCE_SIGNATURES, CSPYCE_ARGNAMES, CSPYCE_DEFAULTS, \
    CSPYCE_RETURNS, CSPYCE_RETNAMES, CSPYCE_DEFINITIONS, \
    CSPYCE_ABSTRACT, CSPYCE_PS, CSPYCE_URL

# Global variables used below
import __main__
INTERACTIVE = not hasattr(__main__, '__file__')

################################################################################
# GET/SET handling
################################################################################

## Helpers

def _deleting_final_return_value(function):
    name = function.__name__
    return_names = CSPYCE_RETNAMES[name][-1:]
    del CSPYCE_RETURNS[name][-1:]
    del CSPYCE_RETNAMES[name][-1:]
    for return_name in return_names:
        del CSPYCE_DEFINITIONS[name][return_name]
    return function

def _removing_final_arguments(function):
    name = function.__name__
    old_function = vars(cspyce0)[name]
    count = old_function.__code__.co_argcount - function.__code__.co_argcount
    if count > 0:
        del CSPYCE_SIGNATURES[name][-count:]
        del CSPYCE_ARGNAMES[name][-count:]
        defaults = CSPYCE_DEFAULTS.get(name)
        if defaults:
            if len(defaults) <= count:
                del CSPYCE_DEFAULTS[name]
            else:
                CSPYCE_DEFAULTS[name] = CSPYCE_DEFAULTS[name][:count]
    return function

@contextmanager
def chkin_and_chkout(name):
    cspyce0.chkin(name)
    try:
        yield
    finally:
        cspyce0.chkout(name)


def erract(op='', action=''):
    """Allow special argument handling:
        erract()            -> erract('GET', '')
        erract('GET')       -> erract('GET', '')
        erract('EXCEPTION') -> erract('SET', 'EXCEPTION')
    Also override 'ABORT' and 'DEFAULT' options in interactive mode.
    """

    op = op.upper().strip()
    if not op:
        op = 'GET'

    if op == 'GET':
        return cspyce0.erract('GET', '')

    if op != 'SET' and not action:  # single input value, assume 'SET'
        cspyce0.erract('SET', op)
        return op

    action = action.upper().strip()
    if op == 'SET' and INTERACTIVE and action in ('ABORT', 'DEFAULT'):
        print(f'ERROR action "{action}" is disabled in interactive mode; using "RETURN"')
        cspyce0.erract('SET', 'RETURN')
        return 'RETURN'

    return cspyce0.erract(op, action)

def errdev(op='', action=''):
    """Allow special argument handling:
        errdev()            -> errdev('GET', '')
        errdev('GET')       -> errdev('GET', '')
        errdev('SCREEN')    -> errdev('SET', 'SCREEN')
    """

    if not op:
        return cspyce0.errdev('GET', '')

    op_upper = op.upper()
    if op_upper == 'GET':
        return cspyce0.errdev('GET', '')

    if op_upper != 'SET' and not action:  # single input value, assume 'SET'
        cspyce0.errdev('SET', op)
        return op

    return cspyce0.errdev(op, action)

def errprt(op='', list_=''):
    """Allow special argument handling:
        errprt()            -> errprt('GET', '')
        errprt('GET')       -> errprt('GET', '')
        errprt('LONG')      -> errprt('SET', 'LONG')
    """

    op = op.upper().strip()
    if not op:
        op = 'GET'

    if op == 'GET':
        return cspyce0.errprt('GET', '')

    if op != 'SET' and not list_:  # single input value, assume 'SET'
        cspyce0.errprt('SET', op)
        return op

    list_ = list_.upper().strip()
    return cspyce0.errprt(op, list_)

################################################################################
# Define _error versions of functions that raise error conditions rather than
# return status flags.
#
# The code is written to work regardless of the type of error handling in use.
################################################################################

#### defined in cspyce0.i

def bodc2n_error(code):
    (name, found) = cspyce0.bodc2n(code)
    if not found:
        with chkin_and_chkout('bodc2n_error'):
            setmsg(f'body code {code} not found in kernel pool')
            sigerr('SPICE(BODYIDNOTFOUND)')

    return name

def bodn2c_error(name):
    (code, found) = cspyce0.bodn2c(name)
    if not found:
        with chkin_and_chkout('bodn2c_error'):
            setmsg(f'body name "{name}" not found in kernel pool')
            sigerr('SPICE(BODYNAMENOTFOUND)')

    return code

def bods2c_error(name):
    (code, found) = cspyce0.bods2c(name)
    if not found:
        with chkin_and_chkout('bods2c_error'):
            setmsg(f'body name "{name}" not found in kernel pool')
            sigerr('SPICE(BODYNAMENOTFOUND)')

    return code

def ccifrm_error(frclss, clssid):
    (frcode, frname, center, found) = cspyce0.ccifrm(frclss, clssid)
    if not found:
        with chkin_and_chkout('ccifrm_error'):
            setmsg(f'unrecognized frame description: class {frclss}; class id {clssid}')
            sigerr('SPICE(INVALIDFRAMEDEF)')

    return [frcode, frname, center]

def cidfrm_error(code):
    (frcode, name, found) = cspyce0.cidfrm(code)
    if not found:
        with chkin_and_chkout('cidfrm_error'):
            setmsg(f'body code {code} not found in kernel pool')
            sigerr('SPICE(BODYIDNOTFOUND)')

    return [frcode, name]

def ckcov_error(ck, idcode, needav, level, tol, timsys):
    coverage = cspyce0.ckcov(ck, idcode, needav, level, tol, timsys)
    if coverage.card == 0:
        with chkin_and_chkout('ckcov_error'):
            setmsg(f'body code {idcode} not found in C kernel file {ck}')
            sigerr('SPICE(BODYIDNOTFOUND)')

    return coverage

def ckgp_error(inst, sclkdp, tol, ref):
    (cmat, clkout, found) = cspyce0.ckgp(inst, sclkdp, tol, ref)
    if not found:
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        with chkin_and_chkout('ckgp_error'):
            setmsg(f'insufficient C kernel data to evaluate instrument/spacecraft '
                   f'{inst}{namestr} at spacecraft clock time {sclkdp} '
                   f'with tolerance {tol}')
            sigerr('SPICE(CKINSUFFDATA)')

    return [cmat, clkout]

def ckgpav_error(inst, sclkdp, tol, ref):
    (cmat, av, clkout, found) = cspyce0.ckgpav(inst, sclkdp, tol, ref)
    if not found:
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        with chkin_and_chkout('ckgpav_error'):
            setmsg(f'insufficient C kernel data to evaluate '
                   f'instrument/spacecraft {inst}{namestr} '
                   f'at spacecraft clock time {sclkdp} with tolerance {tol}')
            sigerr('SPICE(CKINSUFFDATA)')

    return [cmat, av, clkout]

def cnmfrm_error(cname):
    (frcode, frname, found) = cspyce0.cnmfrm(cname)
    if not found:
        with chkin_and_chkout('cnmfrm_error'):
            setmsg(f'body name "{cname}" not found in kernel pool')
            sigerr('SPICE(BODYNAMENOTFOUND)')

    return [frcode, frname]

def dtpool_error(name):
    (found, n, vtype) = cspyce0.dtpool(name)
    if not found:
        with chkin_and_chkout('dtpool_error'):
            setmsg(f'pool variable "{name}" not found')
            sigerr('SPICE(VARIABLENOTFOUND)')

    return [n, vtype]

def frinfo_error(frcode):
    (cent, frclss, clssid, found) = cspyce0.frinfo(frcode)
    if not found:
        with chkin_and_chkout('frinfo_error'):
            setmsg(f'frame code {frcode} not found in kernel pool')
            sigerr('SPICE(FRAMEIDNOTFOUND)')

    return [cent, frclss, clssid]

def frmnam1_error(frcode):  # change of name; frmnam_error is defined below
    frname = cspyce0.frmnam(frcode)
    if frname == '':
        with chkin_and_chkout('frmnam_error'):
            setmsg(f'frame code {frcode} not found')
            sigerr('SPICE(FRAMEIDNOTFOUND)')

    return frname

def gcpool_error(name, start=0):
    with chkin_and_chkout('gcpool_error'):
        (cvals, found) = cspyce0.gcpool(name, start)
        if not found:
            ok, _, _ = cspyce0.dtpool(name)
            if not ok:
                setmsg(f'pool variable "{name}" not found')
                sigerr('SPICE(VARIABLENOTFOUND)')
            return []

        _, count, nctype = cspyce0.dtpool(name)
        if nctype != 'C':
            setmsg(f'string information not available; '
                   f'kernel pool variable "{name}" has numeric values')
            sigerr('SPICE(WRONGDATATYPE)')
            return []

        if start > count:
            setmsg(f'kernel pool has only {count} values for variable "{name}";'
                   f'start index value {start} is too large')
            sigerr('SPICE(INDEXOUTOFRANGE)')
            return []

    return cvals

def gdpool_error(name, start=0):
    with chkin_and_chkout("gdpool_error"):
        (values, found) = cspyce0.gdpool(name, start)
        if not found:
            (ok, count, nctype) = cspyce0.dtpool(name)
            if not ok:
                setmsg(f'pool variable "{name}" not found')
                sigerr('SPICE(VARIABLENOTFOUND)')
                return []

        (ok, count, nctype) = cspyce0.dtpool(name)
        if nctype != 'N':
            setmsg(f'numeric values are not available; '
                   f'kernel pool variable "{name}" has string values')
            sigerr('SPICE(WRONGDATATYPE)')
            return []

        if start > count:
            setmsg(f'kernel pool has only {count} values for variable "{name}"; '
                   f'start index value {start} is too large')
            sigerr('SPICE(INDEXOUTOFRANGE)')
            return []

    return values

def gipool_error(name, start=0):
    with chkin_and_chkout('gipool_error'):
        (ivals, found) = cspyce0.gipool(name, start)
        if not found:
            (ok, count, nctype) = cspyce0.dtpool(name)
            if not ok:
                setmsg(f'fpool variable "{name}" not found')
                sigerr('SPICE(VARIABLENOTFOUND)')
                return []

        (ok, count, nctype) = cspyce0.dtpool(name)
        if nctype != 'N':
            setmsg(f'numeric values are not available; '
                   f'kernel pool variable "{name}" has string values')
            sigerr('SPICE(WRONGDATATYPE)')
            return []

        if start > count:
            setmsg(f'kernel pool has only {count} values for variable "{name}"; '
                   f'start index value {start} is too large')
            sigerr('SPICE(INDEXOUTOFRANGE)')
            return []

    return ivals

def gnpool_error(name, start=0):
    with chkin_and_chkout('gnpool_error'):
        (kvars, found) = cspyce0.gnpool(name, 0)
        if not found:
            setmsg(f'no kernel pool variables found matching template "{name}"')
            sigerr('SPICE(VARIABLENOTFOUND)')
            return []

        if start > len(kvars):
            setmsg(f'kernel pool has only {len(kvars)} variables matching template "{name}"; '
                   f'start index value {start} is too large')
            sigerr('SPICE(INDEXOUTOFRANGE)')
            return []

    return kvars[start:]

def namfrm1_error(frname):  # change of name; namfrm_error is defined below
    frcode = cspyce0.namfrm(frname)
    if frcode == 0:
        with chkin_and_chkout('namfrm_error'):
            setmsg(f'frame name "{frname}" not found in kernel pool')
            sigerr('SPICE(FRAMENAMENOTFOUND)')

    return frcode

def pckcov_error(pck, code):
    coverage = cspyce0.pckcov(pck, code)
    if coverage.card == 0:
        with chkin_and_chkout('pckcov_error'):
            setmsg(f'frame code {code} not found in binary PC kernel file {pck}')
            sigerr('SPICE(FRAMEIDNOTFOUND)')

    return coverage

def spkcov_error(spk, code):
    coverage = cspyce0.spkcov(spk, code)
    if coverage.card == 0:
        with chkin_and_chkout('spkcov_error'):
            setmsg(f'body code {code} not found in SP kernel file {spk}')
            sigerr('SPICE(BODYIDNOTFOUND)')

    return coverage

def srfc2s_error(code, bodyid):
    (srfstr, isname) = cspyce0.srfc2s(code, bodyid)
    if not isname:
        with chkin_and_chkout('srfc2s_error'):
            setmsg(f'surface for {code}/{bodyid} not found')
            sigerr('SPICE(NOTRANSLATION)')

    return srfstr

def srfcss_error(code, bodstr):
    (srfstr, isname) = cspyce0.srfcss(code, bodstr)
    if not isname:
        with chkin_and_chkout('srfcss_error'):
            setmsg(f'surface for {code}/"{bodstr}" not found')
            sigerr('SPICE(NOTRANSLATION)')

    return srfstr

def srfs2c_error(srfstr, bodstr):
    (code, found) = cspyce0.srfs2c(srfstr, bodstr)
    if not found:
        with chkin_and_chkout('srfs2c_error'):
            setmsg(f'surface for "{srfstr}"/"{bodstr}" not found')
            sigerr('SPICE(NOTRANSLATION)')

    return code

def srfscc_error(srfstr, bodyid):
    (code, found) = cspyce0.srfscc(srfstr, bodyid)
    if not found:
        with chkin_and_chkout('srfscc_error'):
            setmsg(f'"{srfstr}"/{bodyid} not found')
            sigerr('SPICE(NOTRANSLATION)')

    return code

def stpool_error(item, nth, contin):
    with chkin_and_chkout("stpool_error"):
        (string, found) = cspyce0.stpool(item, nth, contin)
        if not found:
            (ok, count, nctype) = cspyce0.dtpool(name)
            if not ok:
                setmsg(f'pool variable "{name}" not found')
                sigerr('SPICE(VARIABLENOTFOUND)')
                return ''

            if nth != 0:
                (_, ok) = cspyce0.stpool(item, 0, contin)
                if ok:
                    setmsg(f'index too large; '
                           f'kernel pool has fewer than {nth} '
                           f'strings matching name "{item}" '
                           f'and continuation "{contin}"')
                    sigerr('SPICE(INDEXOUTOFRANGE)')
                    return ''

        (ok, count, nctype) = cspyce0.dtpool(item)
        if nctype != 'C':
            setmsg(f'string values are not available; '
                   f'kernel pool variable "{item}" has numeric values')
            sigerr('SPICE(WRONGDATATYPE)')
            return ''

    return string

def tparse_error(string):
    (sp2000, msg) = cspyce0.tparse(string)
    if msg:
        with chkin_and_chkout('tparse_error'):
            setmsg(msg)
            sigerr('SPICE(INVALIDTIMESTRING)')

    return sp2000

def tpictr_error(string):
    (pictur, ok, msg) = cspyce0.tpictr(string)
    if not ok:
        with chkin_and_chkout('tpictr_error'):
            setmsg(msg)
            sigerr('SPICE(INVALIDTIMESTRING)')

    return pictur

#### defined in cspyce0_part2.i

def ckfrot_error(inst, et):
    (rotate, ref, found) = cspyce0.ckfrot(inst, et)
    if not found:
        with chkin_and_chkout('ckfrot_error'):
            setmsg(f'Orientation data not found for instrument {inst} at time {et}')
            sigerr('SPICE(CKINSUFFDATA)')

    return [rotate, ref]

def ckfxfm_error(inst, et):
    (rotate, ref, found) = cspyce0.ckfxfm(inst, et)
    if not found:
        with chkin_and_chkout('ckfxfm_error'):
            setmsg(f'Orientation data not found for instrument {inst} at time {et}')
            sigerr('SPICE(CKINSUFFDATA)')

    return [rotate, ref]

def dafgsr_error(handle, recno, begin, end):
    (data, found) = cspyce0.dafgsr(handle, recno, begin, end)
    if not found:
        with chkin_and_chkout('dafgsr_error'):
            setmsg(f'DAF summary content not available for handle {handle}, '
                   f'record {recno}, words {begin}-{end}')
            sigerr('SPICE(DAFFRNOTFOUND)')

    return data

def dlabbs_error(handle):
    (dlabbs, found) = cspyce0.dlabbs(handle)
    if not found:
        with chkin_and_chkout('dlabbs_error'):
            setmsg(f'DLA segment not found for handle {handle}')
            sigerr('SPICE(DASFILEREADFAILED)')

    return dlabbs

def dlabfs_error(handle):
    (dladsc, found) = cspyce0.dlabfs(handle)
    if not found:
        with chkin_and_chkout('dlabfs_error'):
            setmsg(f'DLA segment not found for handle {handle}')
            sigerr('SPICE(DASFILEREADFAILED)')

    return dladsc

def dlafns_error(handle, dladsc):
    (nxtdsc, found) = cspyce0.dlafns(handle, dladsc)
    if not found:
        with chkin_and_chkout('dlafns_error'):
            setmsg(f'DLA segment not found for handle {handle}')
            sigerr('SPICE(DASFILEREADFAILED)')

    return nxtdsc

def dlafps_error(handle, dladsc):
    (prvdsc, found) = cspyce0.dlafps(handle, dladsc)
    if not found:
        with chkin_and_chkout('dlafps_error'):
            setmsg(f'DLA segment not found for handle {handle}')
            sigerr('SPICE(DASFILEREADFAILED)')

    return prvdsc

def dskx02_error(handle, dladsc, vertex, raydir):
    (plid, xpt, found) = cspyce0.dskx02(handle, dladsc, vertex, raydir)
    if not found:
        with chkin_and_chkout('dskx02_error'):
            setmsg('Intercept plate ID not found')
            sigerr('SPICE(NOINTERCEPT)')

    return [plid, xpt]

def dskxsi_error(pri, target, srflst, et, fixref, vertex, raydir):
    (xpt, handle, dladsc, dskdsc, dc, ic, found) = cspyce0.dskxsi(pri, target,
                                                                  srflst, et, fixref,
                                                                  vertex, raydir)
    if not found:
        with chkin_and_chkout('dskxsi_error'):
            setmsg('Intercept plate ID not found')
            sigerr('SPICE(NOINTERCEPT)')

    return [xpt, handle, dladsc, dskdsc, dc, ic]

def ekfind_error(query):
    (nmrows, error, errmsg) = cspyce0.ekfind(query)
    if error:
        with chkin_and_chkout('ekfind_error'):
            setmsg(errmsg)
            sigerr('SPICE(INVALIDVALUE)')

    return nmrows

def ekgc_error(selidx, row, elment):
    (cdata, null, found) = cspyce0.ekgc(selidx, row, elment)
    if not found:
        with chkin_and_chkout('ekgc_error'):
            setmsg(f'EK item not found: column index {selidx}, '
                   f'row {row}, element {elment}')
            sigerr('SPICE(INDEXOUTOFRANGE)')

    return [cdata, null]

def ekgd_error(selidx, row, elment):
    (ddata, null, found) = cspyce0.ekgd(selidx, row, elment)
    if not found:
        with chkin_and_chkout('ekgd_error'):
            setmsg(f'EK item not found: column index {selidx}, '
                   f'row {row}, element {elment}')
            sigerr('SPICE(INDEXOUTOFRANGE)')

    return [ddata, null]

def ekgi_error(selidx, row, elment):
    (idata, null, found) = cspyce0.ekgi(selidx, row, elment)
    if not found:
        with chkin_and_chkout('ekgi_error'):
            setmsg(f'EK item not found: column index {selidx}, '
                   f'row {row}, element {elment}')
            sigerr('SPICE(INDEXOUTOFRANGE)')

    return [idata, null]

def ekpsel_error(query):
    (xbegs, xends, xtypes, xclass, tabs, cols, error, errmsg) = cspyce0.ekpsel(query)
    if error:
        with chkin_and_chkout('ekpsel_error'):
            setmsg(errmsg)
            sigerr('SPICE(INVALIDVALUE)')

    return [xbegs, xends, xtypes, xclass, tabs, cols]

def hx2dp_error(string):
    (number, error, errmsg) = cspyce0.hx2dp(string)
    if error:
        with chkin_and_chkout('hx2dp_error'):
            setmsg(errmsg)
            sigerr('SPICE(INVALIDVALUE)')

    return number

def kdata_error(which, kind):
    (file, filtype, srcfil, handle, found) = cspyce0.kdata(which, kind)
    if not found:
        with chkin_and_chkout('kdata_error'):
            count = cspyce0.ktotal(kind)
            if which >= count:
                setmsg(f'index out of range: {which}/{count}, {kind}')
                sigerr('SPICE(INVALIDINDEX)')
            else:
                setmsg(f'kernel not found: {which}, {kind}')
                sigerr('SPICE(FILENOTFOUND)')

    return [file, filtype, srcfil, handle]

def kinfo_error(file):
    (filtyp, srcfil, handle, found) = cspyce0.kinfo(file)
    if not found:
        with chkin_and_chkout('kinfo_error'):
            setmsg(f'kernel file not found: {file}')
            sigerr('SPICE(FILENOTFOUND)')

    return [filtyp, srcfil, handle]

def spksfs_error(body, et,):
    (handle, descr, ident, found) = cspyce0.spksfs(body, et)
    if not found:
        with chkin_and_chkout('spksfs_error'):
            setmsg(f'SPK segment not found for body "{body}", time {et}')
            sigerr('SPICE(SPKINSUFFDATA)')

    return [handle, descr, ident]

def szpool_error(name):
    (n, found) = cspyce0.szpool(name)
    if not found:
        with chkin_and_chkout('szpool_error'):
            setmsg(f'kernel pool size limit "{name}" not found')
            sigerr('SPICE(KERNELVARNOTFOUND)')

    return n

def tkfram_error(frcode):
    (rot, frame, found) = cspyce0.tkfram(frcode)
    if not found:
        with chkin_and_chkout('tkfram_error'):
            setmsg(f'rotation matrix for frame {frcode} not found')
            sigerr('SPICE(FRAMEIDNOTFOUND)')

    return [rot, frame]

#### These functions are both vectorized and have _error versions

def ckgp_vector_error(inst, sclkdp, tol, ref):
    (cmat, clkout, found) = cspyce0.ckgp_vector(inst, sclkdp, tol, ref)
    if not np.all(found):
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        sclkdp_min = np.min(sclkdp)
        sclkdp_max = np.max(sclkdp)
        if sclkdp_min == sclkdp_max:
            clockstr = str(sclkdp)
        else:
            clockstr = '%s to %s' % (sclkdp_min, sclkdp_max)

        with chkin_and_chkout('ckgp_vector_error'):
            setmsg(f'insufficient C kernel data to evaluate '
                   f'instrument/spacecraft {inst}{namestr} ' 
                   f'at spacecraft clock times {clockstr} '
                   f'with tolerance {np.min(tol)}')
            sigerr('SPICE(CKINSUFFDATA)')

    return [cmat, clkout]

def ckgpav_vector_error(inst, sclkdp, tol, ref):
    (cmat, av, clkout, found) = cspyce0.ckgpav_vector(inst, sclkdp, tol, ref)
    if not np.all(found):
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        sclkdp_min = np.min(sclkdp)
        sclkdp_max = np.max(sclkdp)
        if sclkdp_min == sclkdp_max:
            clockstr = str(sclkdp)
        else:
            clockstr = '%s to %s' % (sclkdp_min, sclkdp_max)

        with chkin_and_chkout('ckgpav_vector_error'):
            setmsg(f'insufficient C kernel data to evaluate '
                   f'instrument/spacecraft {inst}{namestr} ' 
                   f'at spacecraft clock times {clockstr} '
                   f'with tolerance {np.min(tol)}')
            sigerr('SPICE(CKINSUFFDATA)')

    return [cmat, av, clkout]

def invert_error(m1):
    inverse = cspyce0.invert(m1)
    if np.all(inverse == 0.):
        with chkin_and_chkout('invert_error'):
            setmsg('singular matrix encountered; inverse failed')
            sigerr('SPICE(SINGULARMATRIX)')

    return inverse

def invert_vector_error(m1):
    inverses = cspyce0.invert_vector(m1)
    tests = np.all(inverses == 0., (-2, -1))
    if np.any(tests):
        with chkin_and_chkout('invert_error'):
            setmsg('singular matrix encountered; inverse failed')
            sigerr('SPICE(SINGULARMATRIX)')

    return inverses

################################################################################
# This is the one function that takes an array of strings as input. This fix
# allows it to work in a sensible way if a single input string is provided.
################################################################################

def pcpool(name, cvals):
    if isinstance(cvals, str):
        cspyce0.pcpool(name, [cvals])
    else:
        cspyce0.pcpool(name, cvals)

################################################################################
# These wrappers on the comment readers dafec and dasec ensure that the entire
# comment field is read. They eliminate the "done" return value.
################################################################################

@_deleting_final_return_value
def dafec(handle):
    records = []
    while True:
        (buffer, done) = cspyce0.dafec(handle)
        records += buffer
        if done:
            return records

@_deleting_final_return_value
def dasec(handle):
    records = []
    while True:
        (buffer, done) = cspyce0.dasec(handle)
        records += buffer
        if done:
            return records

################################################################################
# These functions need to be passed a fixed-size array that's based on the value of
# other arguments.  It is simpler to create those arrays in Python and pass them.
################################################################################

def dasadc(handle, n, bpos, epos, data):
    array = _create_das_char_array(data, epos)
    cspyce0.dasadc(handle, n, bpos, epos, array.itemsize, array)

del CSPYCE_SIGNATURES['dasadc'][4]
del CSPYCE_ARGNAMES['dasadc'][4]

def dasudc(handle, first, last, bpos, epos, data):
    array = _create_das_char_array(data, epos)
    cspyce0.dasudc(handle, first, last, bpos, epos, array.itemsize, array)

del CSPYCE_SIGNATURES['dasudc'][5]
del CSPYCE_ARGNAMES['dasudc'][5]

def dasrdc(handle, first, last, bpos, epos, data=None):
    char_count = last - first + 1
    record_size = epos - bpos + 1
    records = (char_count + (record_size - 1)) // record_size
    if data is None:
        array =  np.zeros(records, dtype=np.dtype(('S', epos + 1)))
    else:
        array = _create_das_char_array(data, epos)
        if len(array) < records:
            raise ValueError("Array not long enough")
    result = cspyce0.dasrdc(handle, first, last, bpos, epos, array.itemsize, array)
    return [item.decode() for item in result]

del CSPYCE_SIGNATURES['dasrdc'][5]
del CSPYCE_ARGNAMES['dasrdc'][5]

def _create_das_char_array(data, epos):
    byte_data = [string.encode('utf-8') for string in data]
    itemsize = max(epos + 1, max(len(x) for x in byte_data))
    return np.array(byte_data, dtype=np.dtype(('S', itemsize)))

################################################################################
# For technical reasons, prompt() returns its result twice.  It's simpler to just
# fix it here rather than to create a special typemap just for it.
################################################################################

def prompt(input):
    result = cspyce0.prompt(input)
    return result[0]

################################################################################
# When a function returns a value and a "found" flag, and the flag is False,
# the unused return values contain random values. We change these to something
# sensible.
################################################################################

def bodn2c(name):
    (code, found) = cspyce0.bodn2c(name)
    return [code if found else 0, found]

def bods2c(name):
    (code, found) = cspyce0.bods2c(name)
    return [code if found else 0, found]

def ccifrm(frclss, clssid):
    (frcode, frname, center, found) = cspyce0.ccifrm(frclss, clssid)
    return [frcode if found else 0, frname, center if found else 0, found]

def cnmfrm(cname):
    (frcode, frname, found) = cspyce0.cnmfrm(cname)
    return [frcode if found else 0, frname if found else '', found]

def frinfo(frcode):
    (cent, frclss, clssid, found) = cspyce0.frinfo(frcode)
    return [cent if found else 0,
            frclss if found else 0,
            clssid if found else 0, found]

def srfs2c(srfstr, bodstr):
    (code, found) = cspyce0.srfs2c(srfstr, bodstr)
    return [code if found else 0, found]

def tparse(string):
    (sp2000, msg) = cspyce0.tparse(string)
    return [0. if msg else sp2000, msg]

def ckfrot(inst, et):
    (rotate, ref, found) = cspyce0.ckfrot(inst, et)
    return [rotate if found else np.diag(3*[1.]), ref if found else 0, found]

def ckfxfm(inst, et):
    (rotate, ref, found) = cspyce0.ckfxfm(inst, et)
    return [rotate if found else np.diag(6*[1.]), ref if found else 0, found]

def hx2dp(string):
    (number, error, errmsg) = cspyce0.hx2dp(string)
    return [0. if error else number, error, errmsg]

################################################################################
# Handle "GET"/"SET" inputs to timdef().
################################################################################

def timdef(action='', item='', value=''):

    action = action.upper().strip()
    if action not in ('GET', 'SET'):
        if item == '':
            item = action
            action = 'GET'
        else:
            value = item
            item = action
            action = 'SET'

    return cspyce0.timdef(action, item, value)

################################################################################
# Prepare for the possible use of aliases
################################################################################

FRAME_CODE_OVERRIDES = {}
FRAME_NAME_OVERRIDES = {}

def _name_as_key(name):
    """Uppercase, stripped, no repeated interior whitespace."""

    name = name.upper().strip()
    while '  ' in name:
        name = name.replace('  ', ' ')

    return name

def frmnam(frcode):
    return FRAME_NAME_OVERRIDES.get(frcode, cspyce0.frmnam(frcode))

def frmnam_error(frcode):
    return FRAME_NAME_OVERRIDES.get(frcode, frmnam1_error(frcode))

def namfrm(frname):
    return FRAME_CODE_OVERRIDES.get(_name_as_key(frname), cspyce0.namfrm(frname))

def namfrm_error(frname):
    return FRAME_CODE_OVERRIDES.get(_name_as_key(frname), namfrm1_error(frname))

################################################################################
# Assign support information about each function:
#   ABSTRACT    = a brief description of what the function does, formatted
#                 and wrapped at 72-column width. It should start and end with
#                 a newline.
#   SIGNATURE   = a list indicating the type of each argument
#   ARGNAMES    = a list of names of the input arguments
#   RETURNS     = a list indicating the type of each return value
#   RETNAMES    = a list of names of the return values
#   URL         = a URL for more information
#   PS          = an optional, final note.
#   DEFINITIONS = a dictionary describing each input and return values.
#   NOTES       = a list of one or more note strings, each formatted and
#                 wrapped at 72-column width. It should start and end with a
#                 newline.
#
# Note that the docstring and defaults will be constructed from this
# information.
################################################################################

def assign_docstring(func, note=""):
    """Assign a docstring to a cspyce function.

    An optional additional note string can provide version information. It must
    be pre-formatted, wrapped at 72 columns, and begin and end with a newline.
    """

    doclist = [func.ABSTRACT, '\n']

    if func.URL:
        doclist += [func.URL, '\n']

    if note:
        # We need to copy the note list so as not to affect other versions using
        # the same note list.
        func.NOTES = list(func.NOTES) + [note]

    doclist += func.NOTES

    lname = 0
    names = []
    for name in func.ARGNAMES + func.RETNAMES:
        lname = max(lname, len(name))
        names.append(name)

    ltype = 0
    types = []
    for arg_type in func.SIGNATURE + func.RETURNS:
        arg_type = (arg_type.replace('time', 'float')
                            .replace('rotmat', 'float')
                            .replace('body_code', 'int')
                            .replace('body_name', 'string')
                            .replace('frame_code', 'int')
                            .replace('frame_name', 'string'))
        ltype = max(ltype, len(arg_type))
        types.append(arg_type)

    indent = 2 + ltype + 1 + lname + 3
    ldefs = 72 - indent
    tabstr = indent * ' '

    inputs = len(func.ARGNAMES)
    doclist += ['\nInputs:']
    if inputs == 0:
        doclist += [' none\n']
    else:
        doclist += ['\n']

    for (name, arg_type) in zip(names[:inputs], types[:inputs]):
        desc = textwrap.wrap(func.DEFINITIONS[name][1], ldefs)
        doclist += ['  ', arg_type, (ltype - len(arg_type))*' ', ' ']
        doclist += [name, (lname - len(name))*' ', ' = ']
        doclist += [desc[0], '\n']
        for k in range(1, len(desc)):
            doclist += [tabstr, desc[k], '\n']

    doclist += ['\nReturns:']
    if len(func.RETNAMES) == 0:
        doclist += [' none\n']
    else:
        doclist += ['\n']

    for (name, arg_type) in zip(names[inputs:], types[inputs:]):
        desc = textwrap.wrap(func.DEFINITIONS[name][1], ldefs)
        doclist += ['  ', arg_type, (ltype - len(arg_type))*' ', ' ']
        doclist += [name, (lname - len(name))*' ', ' = ']
        doclist += [desc[0], '\n']
        for k in range(1, len(desc)):
            doclist += [tabstr, desc[k], '\n']

    if func.PS:
        ps = textwrap.wrap('Note: ' + func.PS)
        doclist += ['\n', '\n'.join(ps)]

    doclist += ['\n']

    func.__doc__ = ''.join(doclist)

# Non-vector functions
for name in CSPYCE_SIGNATURES:
    func = globals()[name]
    func.ABSTRACT  = CSPYCE_ABSTRACT[name]
    func.SIGNATURE = CSPYCE_SIGNATURES[name]
    func.ARGNAMES  = CSPYCE_ARGNAMES[name]
    func.RETURNS   = CSPYCE_RETURNS[name]
    func.RETNAMES  = CSPYCE_RETNAMES[name]
    func.PS        = CSPYCE_PS.get(name, '')
    func.URL       = CSPYCE_URL.get(name, '')
    func.NOTES     = []
    func.DEFINITIONS = CSPYCE_DEFINITIONS[name]

    if name in CSPYCE_DEFAULTS:
        func.__defaults__ = tuple(CSPYCE_DEFAULTS[name])

    assign_docstring(func)

# This is a set of every unique cspyce function's basename (before any suffix)
CSPYCE_BASENAMES = {n for n in CSPYCE_ABSTRACT.keys()
                    if not n.endswith('_error')}

################################################################################
# Assign docstrings, signatures, etc. to the _vector functions
################################################################################

# arg_type -> (arg_type for input, arg_type for output)
VECTORIZED_ARGS = {
    'time'       : ('time[_]'      , 'time[_]'      ),
    'float'      : ('float[_]'     , 'float[_]'     ),
    'float[2]'   : ('float[_,2]'   , 'float[_,2]'   ),
    'float[3]'   : ('float[_,3]'   , 'float[_,3]'   ),
    'float[4]'   : ('float[_,4]'   , 'float[_,4]'   ),
    'float[6]'   : ('float[_,6]'   , 'float[_,6]'   ),
    'float[8]'   : ('float[_,8]'   , 'float[_,8]'   ),
    'float[9]'   : ('float[_,9]'   , 'float[_,9]'   ),
    'float[2,2]' : ('float[_,2,2]' , 'float[_,2,2]' ),
    'float[3,3]' : ('float[_,3,3]' , 'float[_,3,3]' ),
    'float[6,6]' : ('float[_,6,6]' , 'float[_,6,6]' ),
    'float[*]'   : ('float[_,*]'   , 'float[_,*]'   ),
    'float[*,*]' : ('float[_,*,*]' , 'float[_,*,*]' ),
    'rotmat[3,3]': ('rotmat[_,3,3]', 'rotmat[_,3,3]'),
    'rotmat[6,6]': ('rotmat[_,6,6]', 'rotmat[_,6,6]'),
    'int'        : ('int'          , 'int[_]'       ),
    'bool'       : ('bool'         , 'bool[_]'      ),
    'body_code'  : ('body_code'    , 'body_code[_]' ),  # not used (yet)
    'frame_code' : ('frame_code'   , 'frame_code[_]'),  # not used (yet)
    'body_name'  : ('body_name'    , 'body_name[_]' ),  # not used (yet)
    'frame_name' : ('frame_name'   , 'frame_name[_]'),  # not used (yet)
}

def _vectorize_signature(signature):
    """Convert a scalar signature to a vectorized signature."""
    return _vectorize_arglist(signature, 0)

def _vectorize_return(returns):
    """Convert a scalar return list to a vectorized return list."""
    return _vectorize_arglist(returns, 1)

def _vectorize_arglist(arglist, k):
    vectorized = []
    for arg in arglist:
        if arg in VECTORIZED_ARGS:
            vectorized.append(VECTORIZED_ARGS[arg][k])
        else:
            vectorized.append(arg)

    return vectorized

VECTOR_NOTE = """
In this vectorized version, any or all of the floating-point inputs can
have an extra leading dimension. The function will loop over this axis
and return arrays of the results. If no inputs have an extra dimension,
it returns results identical to the un-vectorized version.
"""

for basename in CSPYCE_BASENAMES:
    for suffix in ('', '_error'):
        vname = basename + '_vector' + suffix
        if vname not in globals():
            continue

        name = basename + suffix
        func = globals()[name]
        vfunc = globals()[vname]

        vfunc.ABSTRACT = func.ABSTRACT
        vfunc.SIGNATURE = _vectorize_signature(func.SIGNATURE)
        vfunc.ARGNAMES = func.ARGNAMES
        vfunc.RETURNS = _vectorize_signature(func.RETURNS)
        vfunc.RETNAMES = func.RETNAMES
        vfunc.PS        = func.PS
        vfunc.URL       = func.URL
        vfunc.DEFINITIONS = func.DEFINITIONS
        vfunc.NOTES     = func.NOTES

        assign_docstring(vfunc, VECTOR_NOTE)

################################################################################
# Register _flag, _error, _scalar, and _vector versions of every function.
################################################################################

# The only options are:
#   func == func_error == func_vector
#   func == func_error != func_vector
#   func == func_vector != func_error
#   func != func_vector != func_error != func_vector_error

for name in CSPYCE_BASENAMES:
    ename  = name + '_error'
    vname  = name + '_vector'
    vename = name + '_vector_error'

    # Get up to four versions of the function
    func   = globals()[name]
    efunc  = globals().get(ename, func)
    vfunc  = globals().get(vname, func)

    if vename in globals():
        vefunc = globals()[vename]
    elif vfunc is func:
        vefunc = efunc
    elif efunc is func:
        vefunc = vfunc
    else:
        vefunc = func

    # Define them globally. They may already be defined, in which case this is
    # a harmless operation
# DISABLED! It creates too many symbols for the global dictionary
#     globals()[ ename] =  efunc
#     globals()[ vname] =  vfunc
#     globals()[vename] = vefunc

    # Define the links between the different versions.
    func.flag   =  func
    func.error  = efunc
    func.vector = vfunc
    func.scalar =  func

    efunc.flag   =   func
    efunc.error  =  efunc
    efunc.vector = vefunc
    efunc.scalar =  efunc

    vfunc.flag   =  vfunc
    vfunc.error  = vefunc
    vfunc.vector =  vfunc
    vfunc.scalar =   func

    vefunc.flag   =  vfunc
    vefunc.error  = vefunc
    vefunc.vector = vefunc
    vefunc.scalar =  efunc

    # Define the alternative names for these functions
# DISABLED! It creates too many symbols for the global dictionary
#     fname  = name + '_flag'
#     sname  = name + '_scalar'
#     sfname = name + '_scalar_flag'
#     sename = name + '_scalar_error'
#     vfname = name + '_vector_flag'
#
#     globals()[ fname] =  func
#     globals()[ sname] =  func
#     globals()[sfname] =  func
#     globals()[sename] = efunc
#     globals()[vfname] = vfunc

# These are temporary variables used by cspyce1.py whose values happen to be
# functions with an ARGNAMES property.  We don't want cspyce2.py to think that
# these are actual functions it needs to know about.  So we remove them from the
# namespace.
del func, efunc, vfunc, vefunc

