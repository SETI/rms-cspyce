"""
cspyce/__init__.py

CSPYCE OVERVIEW

cspyce is a Python module that provides an interface to the CSPICE library. It
implements the most widely-used functions of CSPICE in a Python-like way. It
also supports numerous enhancements, including support for Python exceptions,
array inputs, and aliases.

This version of the library has been built for the CSPICE toolkit v. 67.

cspyce contains Python interfaces to all CSPICE functions likely to be useful
to a Python programmer. Excluded are deprecated functions and various low-level
functions supporting character strings, cells, sets, file I/O, and also all
low-level "geometry finder" functions that can only be implemented in C. It
also includes vectorized versions (with suffix "_vector") for nearly every
function that receives floating-point input and does not perform I/O.

ADDED FEATURES

DOCSTRINGS
- All cspyce functions have informative docstrings, so typing
      help(function)
  provides useful information. However, the call signature appearing in the
  first line of the help text is still defined by cspyce0 and may not make
  sense to the reader. This issue is fixed by module cspyce2.

DEFAULTS
- Many cspyce functions take sensible default values if input arguments are
  omitted.
  - In gcpool, gdpool, gipool, and gnpool, start values default to 1.
  - The functions that take "SET" or "GET" as their first argument (erract,
    errdev, errprt, and timdef) have simplified calling options, which are
    summarized in their docstrings.

RUNTIME ERROR HANDLING

In the CSPICE error handling mechanism, the programmer must check the value
of function failed() regularly to determine if an error has occurred. However,
Python's exception handling mechanism obviates the need for this approach. In
cspyce1, all CSPICE errors raise Python exceptions.

In CSPICE, the programmer can control how C errors are handled using the
function erract(). Options include "IGNORE", "REPORT", "ABORT", "DEFAULT",
and "RETURN", In cspyce1, the "IGNORE" and "REPORT" options are disabled,
because they can leave behind corrupted memory. In interactive Python, the
"ABORT" and "DEFAULT" options are also disabled, because aborting an
interactive session would be pointless. The "ABORT" and "DEFAULT" options are
still available, though not recommended, when running programs
non-interactively.

The cspyce1 module supports two additional error actions, which are variants
on "RETURN". These are "EXCEPTION" and "RUNTIME". The only difference between
them is that "RUNTIME" consistently raises RuntimeError exceptions, whereas
"EXCEPTION" tailors the type of the exception to the situation.

HANDLING OF ERROR FLAGS

Many CSPICE functions bypass the library's own error handling mechanism;
instead they return a status flag, sometimes called "found" or "ok", or else
an empty response might indicate failure. The cspyce module provides
alternative options for these functions.

Within cspyce1, functions that return error flags have an alternative
implementation with a suffix of "_error", which uses cspyce1's Python
exception handling instead. For example, bodn2c(name) is the function that
returns two values given the name of a body, its body ID and a True/False flag
indicating whether the name was recognized. bodn2c_error() instead just
returns a single value, the body ID. However, it raises a Python exception
(KeyError or RuntimeError, depending on the erract setting) if the name is not
recognized.

The cspyce1 module provides several ways to control which version of the
function to use:

- The function use_flags() takes a function name or list of names and
  designates the original version of each function as the default. If the
  input argument is missing, _flag versions are selected universally.  With
  this option, for example, a call to cspyce.bodn2c() will actually call
  cspyce1.bodn2c_flag().

- The function use_errors() takes a function name or list of names and
  designates the _error version of each function as the default. If the input
  argument is missing, _error versions are selected universally. With this
  option, for example, a call to cspyce1.bodn2c() will actually call
  cspyce1.bodn2c_error() instead.

You can also choose between the "flag" and "error" versions of a function
using cspyce function attributes, as discussed below.

FUNCTION ATTRIBUTES

Like any other Python class, functions can have attributes. These are used to
simplify the choices of function options in cspyce1. Every cspyce1 function
has these attributes:

  error   = the version of this function that raises exceptions intead of
            returning flags.
  flag    = the version that returns flags instead of raising exceptions.
  vector  = the vectorized version of this function.
  scalar  = the un-vectorized version of this function.

If a particular option is not relevant to a function, the attribute still
exists, and instead simply returns the function itself. This makes it trivial
to choose a particular combination of features for a particular function call.
For example:
  ckgpav.vector()         same as ckgpav_vector()
  ckgpav.vector.flag()    same as ckgpav_vector()
  ckgpav.vector.error()   same as ckgpav_vector_error()
  ckgpav.error.scalar()   same as ckgpav_error()
  ckgpav.flag()           same as ckgpav()
  bodn2c.vector()         same as bodn2c()
  bodn2c.flag()           same as bodn2c()
"""

import inspect
import os

try:
    from _version import __version__
except ImportError as err:
    __version__ = 'Version unspecified'

# We allow the import of cspyce2 to fail because, during development, there are
# times when cspyce2.py might be invalid. If that happens, we still want to be
# able to work inside the cspyce directory tree. Without allowing this
# exception, it could become impossible to work on and test cspyce functions
# inside this directory tree. This should never occur during a normal run.

try:
    from .cspyce2 import *
except ImportError as err:
    if os.getenv("CSPICE_DEVELOPMENT"):
        print("Package cspyce2 not found.  Error ignored.")
    else:
        print("Set environment variable 'CSPICE_DEVELOPMENT' to '1' to ignore this error")
        raise err

# A set of keywords listing options set globally across the cspyce functions
GLOBAL_STATUS = set()

################################################################################
# Define functions to select between error and flag versions of functions
################################################################################

def use_errors(*funcs):
    """Switch the listed functions or names of functions to use the "error"
    version by default. If the list is empty, apply this operation to all cspyce
    functions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.add('ERRORS')
        GLOBAL_STATUS.discard('FLAGS')
    else:
        GLOBAL_STATUS.discard('ERRORS')
        GLOBAL_STATUS.discard('FLAGS')

    for name in _get_func_names(funcs):
        # <name>_flag must always point to the flag version
        # <name>_error must always point to the error version
        # Only function names that don't specify one of these are modified to
        # point to the error version.
        if 'error' not in name and 'flag' not in name:
            globals()[name] = globals()[name].error

def use_flags(*funcs):
    """Switch the listed functions or names of functions to use the "flag"
    version by default. If the list is empty, apply this operation to all cspyce
    functions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.discard('ERRORS')
        GLOBAL_STATUS.add('FLAGS')
    else:
        GLOBAL_STATUS.discard('ERRORS')
        GLOBAL_STATUS.discard('FLAGS')

    for name in _get_func_names(funcs):
        # <name>_flag must always point to the flag version
        # <name>_error must always point to the error version
        # Only function names that don't specify one of these are modified to
        # point to the flag version.
        if 'error' not in name and 'flag' not in name:
            globals()[name] = globals()[name].flag

################################################################################
# Define functions to select between vector and scalar versions of functions
################################################################################

def use_vectors(*funcs):
    """Switch the listed functions or names of functions to use the "vector"
    version by default. If the list is empty, apply this operation to all cspyce
    functions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.add('VECTORS')
        GLOBAL_STATUS.discard('SCALARS')
    else:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.discard('VECTORS')
        GLOBAL_STATUS.discard('SCALARS')

    for name in _get_func_names(funcs):
        # <name>_scalar must always point to the scalar version
        # <name>_vector must always point to the vector version
        # <name>_array must always point to the array version
        # Only function names that don't specify one of these are modified to
        # point to the vector version.
        if ('scalar' not in name and 'vector' not in name
                                 and 'array' not in name):
            globals()[name] = globals()[name].vector

def use_scalars(*funcs):
    """Switch the named functions, or else all relevant cspyce functions, to
    return flags instead of raising exceptions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.discard('VECTORS')
        GLOBAL_STATUS.add('SCALARS')
    else:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.discard('VECTORS')
        GLOBAL_STATUS.discard('SCALARS')

    for name in _get_func_names(funcs):
        # <name>_scalar must always point to the scalar version
        # <name>_vector must always point to the vector version
        # <name>_array must always point to the array version
        # Only function names that don't specify one of these are modified to
        # point to the scalar version.
        if ('scalar' not in name and 'vector' not in name
                                 and 'array' not in name):
            globals()[name] = globals()[name].scalar

def _get_func_names(funcs=(), source=None):
    """Convert a list of cspyce functions or names to a set of unique names,
    including all version suffixes.
    """

    source = source or globals()

    if funcs:
        validated = set()
        for func in funcs:
            # Convert names to funcs, assemble all versions
            validated |= set(get_all_versions(func, source).keys())
    else:
        validated = set(get_all_funcs(source).keys())

    return validated

################################################################################
# Functions to track down cspyce functions
################################################################################

def get_all_funcs(source=None, cspyce_dict=None):
    """Return a dictionary of all cspyce functions, keyed by their names.

    Inputs:
        source      the dictionary to search, which defaults to globals().
        cspyce_dict is used internally for recursion; it should not be
                    referenced in external calls.
    """

    source = source or globals()

    if cspyce_dict is None:
        cspyce_dict = {}

    # Add names from this source
    names = source.keys()
    for name in names:
        func = source[name]
        if not callable(func):
            continue
        if not hasattr(func, 'SIGNATURE'):
            continue

        # Stop if this function was already found; break infinite recursion
        if func.__name__ in cspyce_dict:
            continue

        # Add this function to the dictionary
        cspyce_dict[func.__name__] = func

        # Use the internal dictionary of this function as a recursive source
        _ = get_all_funcs(func.__dict__, cspyce_dict)

    return cspyce_dict

def get_all_versions(func, source=None):
    """Return a dictionary of all cspyce functions associated with this one,
    keyed by their names.

    Inputs:
        func        a cspyce function or the name of a cspyce function.
        source      the dictionary to search if func is specified by name;
                    default is globals().
    """

    func = validate_func(func, source)
    return get_all_funcs(func.__dict__)

def validate_func(func, source=None):
    """Return a cspyce function, given either its name or the function itself.
    Otherwise, raise an exception.

    Inputs:
        func        a cspyce function or the name of a cspyce function.
        source      the dictionary to search if func is specified by name;
                    default is globals().
    """

    if isinstance(func, str):
        full_name = func
        short_name = full_name.split('_')[0]
        source = source or globals()
        try:
            func = source[short_name]
        except KeyError:
            raise KeyError('Unrecognized function name "%s"' % full_name)

    if not callable(func):
        raise ValueError('Not a function: "%s"' % func.__name__)

    if not hasattr(func, 'SIGNATURE'):
        raise ValueError('Not a cspyce function: "%s"' % func.__name__)

    return func

################################################################################
# Add return annotations to all cspyce functions if this is Python 3
################################################################################

for func in get_all_funcs().values():
    retnames = func.RETNAMES
    if retnames:
        sig = inspect.signature(func)
        if len(func.RETNAMES) == 1:
            func.__signature__ = sig.replace(return_annotation=retnames[0])
        else:
            func.__signature__ = sig.replace(return_annotation=retnames)

################################################################################

# This is the default at initialization
use_errors()

################################################################################
