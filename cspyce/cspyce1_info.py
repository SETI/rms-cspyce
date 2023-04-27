################################################################################
# cspyce/cspyce1_info.py
#
# A dictionary of docstrings and call signatures, keyed by the name of the
# CSPICE function name.
#
# This function reads the associated cspyce0 dictionaries and updates them for
# the cspyce1 "_error" versions.
#
# Used internally by cspyce; not intended for direct import.
################################################################################

from cspyce.cspyce0_info import \
    CSPYCE_SIGNATURES, CSPYCE_ARGNAMES, CSPYCE_DEFAULTS, \
    CSPYCE_RETURNS, CSPYCE_RETNAMES, CSPYCE_DEFINITIONS, \
    CSPYCE_ABSTRACT, CSPYCE_PS, CSPYCE_URL

ERROR_INFO = [      # (function name, return value to remove if any, postscript text for docstring)

# Functions defined in cspyce0.i
    ('bodc2n', 'found' , 'Raise KeyError(BODYIDNOTFOUND) if name could not be translated.'),
    ('bodn2c', 'found' , 'Raise KeyError(BODYNAMENOTFOUND) if name could not be translated.'),
    ('bods2c', 'found' , 'Raise KeyError(BODYNAMENOTFOUND) if name could not be translated.'),
    ('ccifrm', 'found' , 'Raise ValueError(INVALIDFRAMEDEF) if frame is not found.'),
    ('cidfrm', 'found' , 'Raise KeyError(BODYIDNOTFOUND) if the requested frame information is unavailable.'),
    ('ckcov' , ''      , 'Raise KeyError(BODYIDNOTFOUND) if the body code is not found in the C kernel.'),
    ('ckgp'  , 'found' , 'Raise IOError(CKINSUFFDATA) if the requested pointing is unavailable.'),
    ('ckgpav', 'found' , 'Raise IOError(CKINSUFFDATA) if the requested pointing is unavailable.'),
    ('cnmfrm', 'found' , 'Raise KeyError(BODYNAMENOTFOUND) if the requested frame information is unavailable.'),
    ('dtpool', 'found' , 'Raise KeyError(VARIABLENOTFOUND) if the requested variable is not in the kernel pool.'),
    ('frinfo', 'found' , 'Raise KeyError(FRAMEIDNOTFOUND) if the requested frame is not found.'),
    ('frmnam', ''      , 'Raise KeyError(FRAMEIDNOTFOUND) if the requested frame is not found.'),
    ('gcpool', 'found' , 'Raise KeyError(VARIABLENOTFOUND) if the variable is not in the pool; ' +
                         'TypeError(WRONGDATATYPE) if it has the wrong type; ' +
                         'IndexError(INDEXOUTOFRANGE) if the start index is out of range.'),
    ('gdpool', 'found' , 'Raise KeyError(VARIABLENOTFOUND) if the variable is not in the pool; ' +
                         'TypeError(WRONGDATATYPE) if it has the wrong type; ' +
                         'IndexError(INDEXOUTOFRANGE) if the start index is out of range.'),
    ('gipool', 'found' , 'Raise KeyError(VARIABLENOTFOUND) if the variable is not in the pool; ' +
                         'TypeError(WRONGDATATYPE) if it has the wrong type; ' +
                         'IndexError(INDEXOUTOFRANGE) if the start index is out of range.'),
    ('gnpool', 'found' , 'Raise KeyError(VARIABLENOTFOUND) if the variable is not in the pool; ' +
                         'TypeError(WRONGDATATYPE) if it has the wrong type; ' +
                         'IndexError(INDEXOUTOFRANGE) if the start index is out of range.'),
    ('invert', ''      , 'Raise ValueError(SINGULARMATRIX) if the matrix is singular.'),
    ('namfrm', ''      , 'Raise KeyError(FRAMENAMENOTFOUND) if the frame name is not recognized.'),
    ('pckcov', ''      , 'Raise KeyError(FRAMEIDNOTFOUND) if the frame is not found.'),
    ('spkcov', ''      , 'Raise KeyError(BODYIDNOTFOUND) if the body is not found.'),
    ('srfc2s', ''      , 'Raise KeyError(NOTRANSLATION) if surface not found.'),
    ('srfcss', 'isname', 'Raise KeyError(NOTRANSLATION) if surface not found.'),
    ('srfs2c', 'found' , 'Raise KeyError(NOTRANSLATION) if surface not found.'),
    ('srfscc', 'found' , 'Raise KeyError(NOTRANSLATION) if surface not found.'),
    ('stpool', 'found' , 'Raise KeyError(VARIABLENOTFOUND) if the variable is not in the pool; ' +
                         'TypeError(WRONGDATATYPE) if it has the wrong type; ' +
                         'IndexError(INDEXOUTOFRANGE) if the start index is out of range.'),
    ('tparse', 'errmsg', 'Raise ValueError(INVALIDTIMESTRING) if the sample string is invalid.'),
    ('tpictr', 'errmsg', 'Raise ValueError(INVALIDTIMESTRING) if the sample string is invalid.'),

# Functions defined in cspyce0_part2.i
    ('ckfrot',  'found', 'Raise IOError(CKINSUFFDATA) if the requested information is unavailable.'),
    ('ckfxfm',  'found', 'Raise IOError(CKINSUFFDATA) if the requested information is unavailable.'),
    ('dafgsr',  'found', 'Raise IOError(DAFFRNOTFOUND) if the file read failed.'),
    ('dlabbs',  'found', 'Raise IOError(DASFILEREADFAILED) if the file read failed.'),
    ('dlabfs',  'found', 'Raise IOError(DASFILEREADFAILED) if the file read failed.'),
    ('dlafns',  'found', 'Raise IOError(DASFILEREADFAILED) if the file read failed.'),
    ('dlafps',  'found', 'Raise IOError(DASFILEREADFAILED) if the file read failed.'),
#     ('dnearp',  'found', 'Raise ValueError(DEGENERATESURFACE) if the point is degenerate.'),  removed, not really an error condition
    ('dskx02',  'found', 'Raise ValueError(NOINTERCEPT) if the intercept does not exist.'),
    ('dskxsi',  'found', 'Raise ValueError(NOINTERCEPT) if the intercept does not exist.'),
    ('ekfind', ('error',
              'errmsg'), 'Raise ValueError(INVALIDVALUE) if the query is invalid.'),
    ('ekgc'  ,  'found', 'Raise IndexError(INDEXOUTOFRANGE) if the column is not present in the row.'),
    ('ekgd'  ,  'found', 'Raise IndexError(INDEXOUTOFRANGE) if the column is not present in the row.'),
    ('ekgi'  ,  'found', 'Raise IndexError(INDEXOUTOFRANGE) if the column is not present in the row.'),
    ('ekpsel', ('error',
              'errmsg'), 'Raise ValueError(INVALIDVALUE) if the query is invalid.'),
    ('hx2dp' , ('error',
              'errmsg'), 'Raise ValueError(INVALIDVALUE) if the hex string is invalid.'),
    ('kdata' ,  'found', 'Raise IOError(FILENOTFOUND) if the specified file could be located.'),
    ('kinfo' ,  'found', 'Raise IOError(FILENOTFOUND) if the specified file could be located.'),
    ('spksfs',  'found', 'Raise IOError(SPKINSUFFDATA) if the requested information is unavailable.'),
    ('szpool',  'found', 'Raise KeyError(KERNELVARNOTFOUND) if the parameter name is not recognized.'),
    ('tkfram',  'found', 'Raise KeyError(FRAMEIDNOTFOUND) if the frame transformation could not be found.'),
]

# Add a new set of dictionary entries for each "_error" function
for (func, name, message) in ERROR_INFO:
    key = func + '_error'
    CSPYCE_ARGNAMES[key] = CSPYCE_ARGNAMES[func]
    CSPYCE_ABSTRACT[key] = CSPYCE_ABSTRACT[func]
    CSPYCE_URL[key] = CSPYCE_URL[func]

    if func in CSPYCE_DEFAULTS:
        CSPYCE_DEFAULTS[key] = CSPYCE_DEFAULTS[func]

    if name:
        CSPYCE_RETNAMES[key] = list(CSPYCE_RETNAMES[func])
        CSPYCE_DEFINITIONS[key] = CSPYCE_DEFINITIONS[func].copy()
        if isinstance(name, str):
            name = (name,)
        for n in name:
            CSPYCE_RETNAMES[key].remove(n)
            del(CSPYCE_DEFINITIONS[key][n])
    else:
        CSPYCE_RETNAMES[key] = CSPYCE_RETNAMES[func]
        CSPYCE_DEFINITIONS[key] = CSPYCE_DEFINITIONS[func]

    if func in CSPYCE_PS:
        CSPYCE_PS[key] = CSPYCE_PS[func] + '\n\n' + message
    else:
        CSPYCE_PS[key] = message

    old_defs = CSPYCE_DEFINITIONS[func]
    CSPYCE_SIGNATURES[key] = [old_defs[n][0] for n in CSPYCE_ARGNAMES[key]]
    CSPYCE_RETURNS[key]    = [old_defs[n][0] for n in CSPYCE_RETNAMES[key]]

################################################################################
