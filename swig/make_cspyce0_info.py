################################################################################
# make_cspyce_info.py
#
# Usage:
#   python3 swig/make_cspyce_info.py
#
# This program writes the file cspyce/cspyce0_info.py containing dictionary
# information needed for mananging cspyce signatures and docstrings. It reads
# the files matching swig/cspyce0*.i as input and extracts the dictionary info
# from the comments of those files. It should be run from the root directory of
# the cspyce repo.
################################################################################
import collections
import os
import re
import textwrap

# Conversion from declared types in C to Python types
from pathlib import Path

TYPE_INFO = {
    'SpiceChar'         : 'string',
    'SpiceInt'          : 'int',
    'SpiceDouble'       : 'float',
    'SpiceBoolean'      : 'bool',
    'ConstSpiceChar'    : 'string',
    'ConstSpiceInt'     : 'int',
    'ConstSpiceDouble'  : 'float',
    'ConstSpiceBoolean' : 'bool',
    'void'              : 'string',
    'const void'        : 'string',
    'char'              : 'string',
    'const char'        : 'string',
    'double'            : 'float',
    'int'               : 'int',
}

# How to interpret a typemap in an extern declaration
MAP_INFO = {
    'OUT_BOOLEAN' : ('O', 'SpiceBoolean'),
    'OUTPUT'      : ('O', ''),
    'IN_STRING'   : ('I', 'SpiceChar'),
    'CONST_STRING': ('I', 'ConstSpiceChar'),
    'IN_ARRAY1'   : ('I', ''),
}

# Argument names that always refer to body codes or body names
BODY_ARGNAMES = {
    "back",
    "bodids",
    "bodstr",
    "body",
    "bodyid",
    "bodynm",
    "cent",
    "center",
    "cname",
    "front",
    "illmn",
    "ilusrc",
    "obs",
    "observer",
    "obsrvr",
    "sc",
    "source",
    "targ",
    "targ1",
    "targ2",
    "target",
}

# Argument names that always refer to frame codes or frame names
FRAME_ARGNAMES = {
    "bframe",
    "dref",
    "fframe",
    "fixref",
    "frame1",
    "frame2",
    "frcode",
    "frname",
    "fromfr",
    "obsref",
    "outref",
    "ref",
    "rframe",
    "tframe",
    "tofr",
}

# Argument names that always refer to surface codes or surface names
SURFACE_ARGNAMES = {'srfstr'}

# Argument names that always refer to time
TIME_ARGNAMES = {
    "cover",
    "epoch",
    "epochs",
    "et",
    "et0",
    "et1",
    "etfrom",
    "etobs",
    "etto",
    "trgepc",
    "windows",
}

# Regular expressions used below
PROCEDURE = re.compile(r'\*? *-Procedure +(\w{2,6})(_c|_) +\(.*', re.I)
ABSTRACT  = re.compile(r'\*? ?-Abstract', re.I)
FUNC_DEF  = re.compile(r'\*? *(void|Spice\w+' +
                       r'|SpiceChar) *\*? *\w+ *\(.*')
ARG_DEF   = re.compile(r' *\*? *(const|) *(\w+) *(\*+|) *(\w+) *(\[.*\]|) *')
VAR_DESC  = re.compile(r'\* (\w+) +(I-O|I|O|R|) .*')
APPLY1    = re.compile(r'%apply +\((.*?)\).*')
APPLY2    = re.compile(r'(?: *|%apply +\(.*\)) *\{\(?(.*?)\)?\};?')
RENAME    = re.compile(r'%rename *\((\w+)\).*')


def process_one_dot_i_file(filename, out):
    """Process one ".i" file and return a list of strings defining the content. """

    with open(filename) as f:
        records = [rec.rstrip() for rec in f]

    length = len(records)
    # get index of first PROCEDURE record
    index = next(i for i, record in enumerate(records) if PROCEDURE.fullmatch(record))

    while index < length:
        # index of next PROCEDURE record, or else end of file
        next_index = next((i for i in range(index + 1, len(records))
                           if PROCEDURE.fullmatch(records[i])), len(records))
        this_batch = collections.deque(records[index:next_index])
        handle_one_function(out, this_batch)
        index = next_index

    out.write('#########################################\n')



def handle_one_function(out, records):
    # The first item on the list must be a PROCEDURE
    match = PROCEDURE.fullmatch(records.popleft())
    func = match.group(1).lower()

    abstract = []
    cnames = []
    types = {}
    stars = {}
    dims = {}
    defs = {}
    inouts = {}
    hidden_names = set()
    postscript = []
    defaults = {}
    replaced_types = {}
    python_args = []
    argno = 0
    url = f'https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/{func}_c.html'

    inout = ''
    prevname = ''
    return_name = ''

    try:
        # Read all records up to and include the ABSTRACT record
        while True:
            record = records.popleft()
            if ABSTRACT.fullmatch(record):
                break

        # The next line should just be a comment:
        if records.popleft().lstrip('* '):
            raise ValueError('Error in abstract0', record)

        # The abstract includes everything up until the FUNC_DEF record
        while True:
            record = records.popleft()
            match = FUNC_DEF.fullmatch(record)
            if match:
                break
            abstract.append(record.lstrip('* '))
        while abstract and abstract[-1] == '':
            abstract.pop()

        # record contains the FUNC_DEF record.
        # Handle this record, and continue reading records until we get a blank comment
        ctype = match.group(1)
        while True:
            record = records.popleft().lstrip('* ')
            if not record:
                break
            match = ARG_DEF.fullmatch(record.rstrip(' ,)'))
            if not match:
                if '(*' in record:     # C func as argument
                    continue
                else:
                    raise ValueError('Bad C declaration: ' + record)

            (const, argtype, star, name, dim) = match.groups()
            argtype = (const + ' ' + argtype).lstrip()
            dim = dim.replace(' ', '')

            cnames.append(name)
            types[name] = argtype
            stars[name] = star
            dims[name] = dim

        # Skip until we see '----'
        while True:
            record = records.popleft()
            if '----------' in record:
                break

        # Read the argument descriptions.  This section continues until we read
        # a line that starts with '*******'
        while True:
            record = records.popleft()
            if record.startswith('*******'):
                break
            parts = record.lstrip('* ').split()
            if parts[0].startswith('SPICE_'):   # ignore parameters
                continue
            elif 'P' in parts[:2]:
                inout = 'P'             # save for multiline description
            elif len(parts) > 1 and parts[1] in ('I', 'O', 'I-O', 'R'):
                name = parts[0]
                prevname = name         # save for multiline description
                inout = parts[1]
                inouts[name] = inout
                defs[name] = ' '.join(parts[2:])
                if parts[1] == 'R':
                    return_name = name
                    types[name] = ctype
                    stars[name] = ''
                    dims[name] = ''
            elif inout != 'P':
                defs[prevname] += ' ' + ' '.join(parts)

        # Skip to the rename section
        while True:
            record = records.popleft()
            if record.startswith('%rename'):
                break

        # Handle the rename records
        func2 = RENAME.match(record).group(1)
        if func != func2:
            if func + '_' == func2:  # e.g., return -> return_
                func = func2
            else:
                raise ValueError('%rename value does not match '
                                 f'function name: {func2} {func}')

        # Skip to the first %apply record
        while True:
            record = records.popleft()
            if record.startswith('%apply'):
                break

        # Handle the first %apply record, which will be the return statement
        if func not in record:
            raise ValueError('Error in apply0, missing declaration', record)
        elif '(' + ctype + ' ' not in record:
            raise ValueError('Error in body0, type mismatch', record)

        # Handle all the remaining %apply records.  They end with a blank line
        while True:
            record = records.popleft()
            if record == '':
                break
            assert 'RETURN_' not in record     # already handled above
            match = APPLY1.fullmatch(record)   # match %apply (...) ...?
            if match:
                subrec = match.group(1)
                this_inout = ''
                this_main_arg = -1
                for k, argdef in enumerate(subrec.split(',')):
                    if 'INOUT_' in argdef:
                        this_inout = 'I-O'
                        this_main_arg = k
                    elif 'IN_' in argdef:
                        this_inout = 'I'
                        this_main_arg = k
                    elif 'OUT' in argdef:
                        this_inout = 'O'
                        this_main_arg = k
                    elif 'CONST' in argdef:
                        this_inout = 'I'
                        this_main_arg = k

                assert this_main_arg >= 0, record

            match = APPLY2.fullmatch(record)   # match ... {...};
            if match:
                if not record[-1] == ';':
                    raise ValueError('Missing semicolon: ' + record)
                subrec = match.group(1)
                for k, argdef in enumerate(subrec.split(',')):
                    match = ARG_DEF.fullmatch(argdef)
                    (const, argtype, star, name, dim) = match.groups()
                    argtype = (const + ' ' + argtype).lstrip()
                    dim = dim.replace(' ', '')

                    if name in types:
                        validate_type_change(argtype, types[name],
                                             name, func)
                    types[name] = argtype

                    if (name not in dims
                        or (dim and not dims[name])
                        or (not star and stars[name])):
                            dims[name] = dim
                            stars[name] = star

                    if k == this_main_arg:
                        inouts[name] = this_inout
                    else:
                        inouts[name] = '?'
                        hidden_names.add(name)

        # Immediately after the %apply and blank line, we have the body.  Look for
        # a line containing 'inline' or 'extern'.  If the former, the actual
        # declaration starts on the next line
        while True:
            record = records.popleft()
            if 'inline' in record:
                record = records.popleft()
                break
            elif 'extern' in record:
                break

        if 'void)' in record:
            pass
        elif not record.endswith('('):
            raise ValueError('Move first argument to new line: ' + record.lstrip())
        else:
            while True:
                record = records.popleft().strip()
                if record in (');', '{'):
                    break
                argdefs = record.rstrip(',) ').split(',')
                for argdef in argdefs:
                    match = ARG_DEF.fullmatch(argdef.rstrip(' ,)'))
                    if not match:
                        raise ValueError(f"Bad match on record {argdef}")
                    (const, argtype, star, name, dim) = match.groups()
                    argtype = (const + ' ' + argtype).lstrip()
                    dim = dim.replace(' ', '')

                    if name.isupper():      # if this is a typemap, not a name
                        (inout, argtype2) = MAP_INFO[name]
                        name = cnames[argno]    # use name from original C
                                                # declaration
                        assert inouts[name] == inout
                        if argtype2:
                            assert types[name] == argtype2
                    else:
                        if name in types:
                            validate_type_change(argtype, types[name],
                                                 name, func)
                        types[name] = argtype
                        if (name not in dims
                            or (dim and not dims[name])
                            or (not star and stars[name])):
                                dims[name] = dim
                                stars[name] = star

                    if name in hidden_names:
                        pass
                    elif name in types:
                        python_args.append(name)
                    else:
                        raise ValueError('Unrecognized arg: ' + record)

                    if name in cnames:
                        argno = cnames.index(name) + 1

        for record in records:
            if record.startswith('//CSPYCE'):
                (key, _, record) = record.partition(':')
                record = record.lstrip()
                if key == '//CSPYCE_PS':
                    postscript.append(record)
                elif key == '//CSPYCE_DEFAULT':
                    (name, _, value) = record.partition(':')
                    defaults[name] = eval(value)
                elif key == '//CSPYCE_TYPE':
                    (name, _, value) = record.partition(':')
                    replaced_types[name] = value
                elif key == '//CSPYCE_URL':
                    url = record
                else:
                    raise ValueError('Invalid comment: ' + key + ':' + record)

    except IndexError:
        raise ValueError("Queue seems to have ended early!")

    # Preserve the return name, if any
    if return_name and return_name not in python_args:
        python_args.append(return_name)

    #### Save new records...

    out.write('#########################################\n')

    # CSPYCE_ARGNAMES
    argnames = [name for name in python_args if inouts[name] in ('I', 'I-O')]
    quoted_argnames = [f'"{name}"' for name in argnames]
    out.write(f'CSPYCE_ARGNAMES["{func}"] = [{", ".join(quoted_argnames)}]\n')

    # CSPYCE_RETNAMES
    outnames = [name for name in python_args if inouts[name] in ('O', 'I-O', 'R')]
    quoted_outnames = [f'"{name}"' for name in outnames]
    out.write(f'CSPYCE_RETNAMES["{func}"] = [{", ".join(quoted_outnames)}]\n')

    # CSPYCE_ABSTRACT
    out.write(f'CSPYCE_ABSTRACT["{func}"] = """\n')
    abstract = '\n'.join(abstract)
    paragraphs = abstract.split('\n\n')
    for k,paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        paragraph = ' '.join(paragraph.split())
        paragraph = textwrap.wrap(paragraph, 72, break_on_hyphens=False)
        for line in paragraph:
            out.write(line + '\n')
        if k < len(paragraphs) - 1:
            out.write('\n')
    out.write('"""\n')

    # CSPYCE_DEFINITIONS
    out.write(f'CSPYCE_DEFINITIONS["{func}"] = {{\n')
    for name in python_args:
        argtype = TYPE_INFO.get(types[name], types[name])


        dim = dims[name]
        star = stars[name]

        if name in replaced_types:
            (argtype, bracket, xdim) = replaced_types[name].partition('[')
            if bracket:
                dim = '[' + xdim
                star = ''
        elif name in BODY_ARGNAMES:
            if argtype == 'int':
                argtype = 'body_code'
            elif argtype == 'string':
                argtype = 'body_name'
        elif name in FRAME_ARGNAMES:
            if argtype == 'int':
                argtype = 'frame_code'
            elif argtype == 'string':
                argtype = 'frame_name'
        elif name in TIME_ARGNAMES and argtype == 'float':
            argtype = 'time'
        elif name in SURFACE_ARGNAMES:
            if argtype == 'int':
                argtype = 'surface_code'
            elif argtype == 'string':
                argtype = 'surface_name'

        if argtype == 'string' or argtype.endswith('_name'):
            dim = dim.rpartition('[')[0]    # strip dimensioned string len
        elif inouts[name] == 'I':
            if star:
                dim = '[]'

        dim = dim.replace('NPLANE',   '4')
        dim = dim.replace('NELLIPSE', '9')
        if '][' in dim:
            dim = dim.replace('[]', '[*]')
            parts = dim.split('][')
            if len(parts[0]) > 2:
                parts[0] = '[*'
            if len(parts[1]) > 2:
                parts[1] = '*]'
            dim = ','.join(parts)
        elif dim == '[]':
            dim = '[*]'
        elif len(dim) > 3:
            dim = '[*]'


        if name not in defs:
            raise ValueError(f'Missing definition: {func} {name}')
        defn = defs[name].replace('"','\\"')
        defn = ' '.join(defn.strip().split())
        new_rec = f'{name!a:<8}: ("{argtype}{dim}", "{defn}"),\n'
        out.write(new_rec)
    out.write('}\n')

    # CSPYCE_PS
    if postscript:
        postscripts = ' '.join(p.strip() for p in postscript)
        out.write(f'CSPYCE_PS["{func}"] = {postscripts!a}\n')

    # CSPYCE_URL
    out.write(f'CSPYCE_URL["{func}"] = "{url}"\n')

    # CSPYCE_DEFAULTS
    if defaults:
        defaults = [repr(defaults[name]).replace("'", '"') for name in argnames]
        out.write(f'CSPYCE_DEFAULTS["{func}"] = [{", ".join(defaults)}]\n')


# Replacements for other random SPICE types
TYPES_REPLACED = {
    'SpiceCK05Subtype'  : ('ConstSpiceChar',),
    'SpiceDLADescr'     : ('SpiceInt',),
    'ConstSpiceDLADescr': ('ConstSpiceInt',),
    'SpiceDSKDescr'     : ('SpiceDouble',),
    'SpiceEKDataType'   : ('SpiceInt',),
    'SpiceEKExprClass'  : ('SpiceInt',),
    'SpiceSPK18Subtype' : ('ConstSpiceChar',),
    'SpiceEllipse'      : ('SpiceDouble',),
    'SpicePlane'        : ('SpiceDouble',),
    'ConstSpiceEllipse' : ('ConstSpiceDouble',),
    'ConstSpicePlane'   : ('ConstSpiceDouble',),
    'SpiceCell'         : ('SpiceInt', 'SpiceDouble', 'ConstSpiceDouble'),
}


def validate_type_change(newtype, oldtype, name, func):
    if newtype == oldtype:
        return

    if oldtype in TYPES_REPLACED and newtype in TYPES_REPLACED[oldtype]:
        return

    if oldtype == 'const void' and newtype[:5].lower() == 'const':
        return

    if oldtype == 'void' and newtype[:5].lower() != 'const':
        return

    raise ValueError(f'Incompatible types for {name} in {func}: ' +
                     f'{oldtype}, {newtype}')

HEADER = """\
################################################################################
# cspyce/cspyce0_info.py
#
# A dictionary of docstrings and call signatures, keyed by the name of the
# CSPICE function name.
#
# This file is automatically generated by program make_cspyce_info.py. Do not
# modify. To regenerate:
#     python make_cspyce0_info.py
################################################################################

CSPYCE_ARGNAMES    = {}
CSPYCE_RETNAMES    = {}
CSPYCE_ABSTRACT    = {}
CSPYCE_DEFINITIONS = {}
CSPYCE_URL         = {}
CSPYCE_PS          = {}
CSPYCE_DEFAULTS    = {}

"""

FOOTER = """
# Derive the CSPYCE_SIGNATURES, CSPYCE_RETURNS, and CSPYCE_DEFAULTS structures
CSPYCE_SIGNATURES = {}
CSPYCE_RETURNS = {}
for (func, def_dict) in CSPYCE_DEFINITIONS.items():
    CSPYCE_SIGNATURES[func] = [def_dict[name][0]
                               for name in CSPYCE_ARGNAMES[func]]
    CSPYCE_RETURNS[func] = [def_dict[name][0]
                            for name in CSPYCE_RETNAMES[func]]

################################################################################
"""

def make_cspice0_info(outfile=None, filepaths=None):
    root_dir = Path(os.path.realpath(__file__)).parent.parent

    if filepaths is None:
        filepaths = [x.absolute() for x in root_dir.joinpath('swig').glob('cspyce0*.i')]
    if outfile is None:
        outfile = root_dir.joinpath('cspyce/cspyce0_info.py').absolute()

    with open(outfile, 'w', encoding='latin-1') as f:
        f.write(HEADER)
        for filepath in filepaths:
            process_one_dot_i_file(filepath.absolute(), f)
        f.write(FOOTER)


if __name__ == '__main__':
    make_cspice0_info()
