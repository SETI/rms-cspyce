################################################################################
# cspyce/array_suppport.py
# Used internally by cspyce; not intended for direct import.
################################################################################

from __future__ import print_function

import numpy as np
import sys
import inspect

import cspyce
import cspyce.cspyce1 as cspyce1
from cspyce.alias_support import alias_version

PYTHON2 = sys.version_info[0] < 3

# This isn't how we want to handle a ragged array
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

################################################################################
# cspyce array function wrapper
################################################################################

ARRAY_NOTE = """
This version supports array inputs in place of any floating-point inputs. Array
shapes are broadcasted following NumPy rules. This function vectorizes the call
so that any iteration is performed inside C code and is therefore faster than
Python iteration.
"""

def _array_name(name):
    return name.replace('_vector', '_array')

def _arrayize_arglist(arglist):
    arrayized = []
    for arg in arglist:
        arrayized.append(arg.replace('[_', '[...'))

    return arrayized

def array_version(func):
    """Wrapper function to apply NumPy broadcasting rules to the vectorized
    inputs of any cspyce function.
    """

    if hasattr(func, 'array'):
        return func.array

    # Handle vector-free functions quickly
    if '_vector' not in func.__name__ and func.vector is func:
        func.array = func
        return func

    # Apply vector in front of alias option, via recursion
    # Note: repair alias links after all the array functions are defined
    if '_alias' in func.__name__:
        noalias_array_func = array_version(func.noalias)
        alias_array_func = alias_version(noalias_array_func)

        alias_array_func.array = alias_array_func
        func.array = alias_array_func
        return alias_array_func

    # Handle scalar versions of vector functions via recursion
    if '_vector' not in func.__name__:
        array_func = array_version(func.vector)
        func.array = array_func
        return func

    # At this point, we always have the vectorized version of the function, and
    # the array version has not yet been constructed.

    # Identify the names and locations of arguments that can be vectorized;

    # INPUT_ITEMS is a dictionary indicating the required shape of each
    # floating-point input. It is keyed by both the name and index of the input
    # argument. If the length along a particular axis is unspecified (indicated
    # by "*" in the signature), the value in the tuple is zero.

    # RETURN_ITEMS is a list containing the shapes of the returned items, in
    # order.

    if not hasattr(func, 'INPUT_ITEMS'):
        input_items = {}
        for k, sig in enumerate(func.SIGNATURE):
            parts = sig.split('[')
            if parts[0] in ('int', 'bool', 'string', 'body_name', 'body_code',
                            'frame_name', 'frame_code'):
                continue

            if len(parts) == 1:
                shape = ()
            else:
                dims = (parts[1][:-1].replace('_,', '')
                                     .replace('_', '')
                                     .replace('*', '0'))
                if dims:
                    shape = tuple([int(d) for d in dims.split(',')])
                else:
                    shape = ()

            input_items[k] = shape
            input_items[func.ARGNAMES[k]] = shape

        func.INPUT_ITEMS = input_items

        return_items = []
        for sig in func.RETURNS:
            parts = sig.split('[')
            if len(parts) == 1:
                shape = ()
            else:
                dims = (parts[1][:-1].replace('_,', '')
                                     .replace('_', '')
                                     .replace('*', '0'))
                if dims:
                    shape = tuple([int(d) for d in dims.split(',')])
                else:
                    shape = ()

            return_items.append(shape)

        func.RETURN_ITEMS = return_items

    if not func.INPUT_ITEMS:
        func.array = func.vector
        return func

    def wrapper(*args, **keywords):
        return _exec_with_broadcasting(func, *args, **keywords)

    # Copy type info but not function version links
    for (key, value) in func.__dict__.items():
        if not callable(value):
            wrapper.__dict__[key] = value

    # After copy, revise SIGNATURE, RETURNS, and NOTES
    wrapper.SIGNATURE = _arrayize_arglist(func.SIGNATURE)
    wrapper.RETURNS   = _arrayize_arglist(func.RETURNS)
    wrapper.NOTES     = [ARRAY_NOTE] + wrapper.NOTES[1:] # replace vector note

    # Save key attributes of the wrapper function before returning
    cspyce.assign_docstring(wrapper)
    wrapper.__name__ = _array_name(func.__name__)
    if PYTHON2:
        wrapper.func_defaults = func.func_defaults
    else:
        wrapper.__defaults__ = func.__defaults__
        wrapper.__signature__ = inspect.signature(func)

    # Insert mutual links
    wrapper.array  = wrapper
    wrapper.vector = func
    wrapper.scalar = func.scalar
    func.array = wrapper

    return wrapper

def _getarg(indx, args, keywords):
    if isinstance(indx, int):
        return args[indx]
    else:
        return keywords[indx]

def _setarg(indx, value, args, keywords):
    if isinstance(indx, int):
        args[indx] = value
    else:
        keywords[indx] = value

def _exec_with_broadcasting(func, *args, **keywords):
    """Main function to broadcast together the shapes of the input arguments
    and return results with the broadcasted shape, given the vectorized form of
    a function.
    """

    args = list(args)   # args must be mutable

    # Identify arguments needing broadcasting, convert to arrays
    array_args = []     # list of tuples (index or key of arg, array, rank)
    shapes = []
    for indx in list(range(len(args))) + list(keywords.keys()):

        item = func.INPUT_ITEMS.get(indx, None)
        if not item:
            continue

        rank = len(item)

        # Get argument
        arg = _getarg(indx, args, keywords)

        # Convert to floating-point array
        error = False
        try:
            arg = np.asfarray(arg)
        except ValueError:
            error = True

        if error or arg.dtype == np.dtype('O'): # indicates a ragged array shape
            name = indx if isinstance(indx,str) else func.ARGNAMES[indx]
            cspyce1.chkin(func.array.__name__)
            cspyce1.setmsg('Ragged input array for "%s": ' % name)
            cspyce1.sigerr('SPICE(INVALIDARRAYSHAPE)')
            cspyce1.chkout(func.array.__name__)
            return None

        # Extract leading shape of each array
        if rank == 0:
            shape = arg.shape
            invalid_shape = False
        elif rank > len(arg.shape):
            shape = ()
            invalid_shape = True
        else:
            shape = arg.shape[:-rank]
            arg_item = arg.shape[-rank:]
            invalid_shape = any([d1 != 0 and d1 != d2
                                 for (d1,d2) in zip(arg_item, item)])

        if invalid_shape:
            name = indx if isinstance(indx,str) else func.ARGNAMES[indx]
            required_shape = str(item).replace('0','*').replace(',)',')')
            cspyce1.chkin(func.array.__name__)
            cspyce1.setmsg('Invalid array shape %s ' % str(arg.shape) +
                           'for input "%s" ' % name +
                           'in module %s: ' % func.__name__ +
                           '(...,%s is required' % required_shape[1:])
            cspyce1.sigerr('SPICE(INVALIDARRAYSHAPE)')
            cspyce1.chkout(func.array.__name__)
            return None

        # Unit-sized items never need broadcasting
        if all([d == 1 for d in shape]):
            continue

        shapes.append(shape)
        array_args.append((indx, arg, rank))

    # Call function now if iteration is not needed
    if not array_args:
        return func.scalar.__call__(*args, **keywords)

    # Determine the broadcasted shape
    try:
        broadcasted_shape = np.broadcast_shapes(*shapes)
    except ValueError:
        cspyce1.chkin(func.array.__name__)
        cspyce1.setmsg('Incompatible shapes for broadcasting: ' +
                       str(shapes)[1:-1])
        cspyce1.sigerr('SPICE(ARRAYSHAPEMISMATCH)')
        cspyce1.chkout(func.array.__name__)
        return None

    # Broadcast each array and prepare for vectorization
    for (indx, arg, rank) in array_args:

        # Determine required shape
        if rank:
            item = arg.shape[-rank:]
            required_shape = broadcasted_shape + item
        else:
            item = ()
            required_shape = broadcasted_shape

        # Leading axes are handled by iteration through the vector and can be
        # ignored
        required_shape = required_shape[-len(arg.shape):]

        # Leading unit axes can also be ignored
        arg_shape = arg.shape
        for d in arg_shape:
            if d == 1:
                required_shape = required_shape[1:]
                arg_shape = arg_shape[1:]
                arg = arg.reshape(arg.shape)
            else:
                break

        # Broadcast and copy if necessary
        if arg_shape == required_shape:
            arg = np.ascontiguousarray(arg)
        else:
            arg = np.broadcast_to(arg, required_shape).copy()

        # Flatten the leading axes
        arg = arg.reshape((-1,) + item)

        # Restore into the function arguments
        _setarg(indx, arg, args, keywords)

    # Execute the function
    cspyce1.chkin(func.array.__name__)
    results = func.__call__(*args, **keywords)

    if cspyce1.failed():
        cspyce1.chkout(func.array.__name__)
        return None

    # Reshape the results
    multiple_results = isinstance(results, list)
    if not multiple_results:
        results = [results]

    for indx,result in enumerate(results):
        rank = len(func.RETURN_ITEMS[indx])
        if rank:
            result = result.reshape(broadcasted_shape + result.shape[-rank:])
        else:
            result = result.reshape(broadcasted_shape)

        results[indx] = result

    # Return results
    cspyce1.chkout(func.array.__name__)

    if multiple_results:
        return results
    else:
        return results[0]

################################################################################
# Define the alias function selector
################################################################################

SPYCE_DICT = cspyce.__dict__

def use_arrays(*funcs):
    """Switch the listed functions or names of functions to use the "array"
    version by default. This affects all versions of any given cspyce function.
    If the list is empty, apply this operation to all cspyce functions.
    """

    if funcs:
        cspyce.GLOBAL_STATUS.add('ARRAYS')
        cspyce.GLOBAL_STATUS.discard('VECTORS')
        cspyce.GLOBAL_STATUS.discard('SCALARS')
    else:
        cspyce.GLOBAL_STATUS.discard('ARRAYS')
        cspyce.GLOBAL_STATUS.discard('VECTORS')
        cspyce.GLOBAL_STATUS.discard('SCALARS')

    for name in cspyce._get_func_names(funcs, source=SPYCE_DICT):
        # <name>_scalar must always point to the scalar version
        # <name>_vector must always point to the vector version
        # <name>_array must always point to the array version
        # Only function names that don't specify one of these are modified to
        # point to the array version.
        if ('scalar' not in name and 'vector' not in name
                                 and 'array' not in name):
            SPYCE_DICT[name] = SPYCE_DICT[name].array

################################################################################
# Function to define array versions and links for all cspyce functions
################################################################################

def _define_all_array_versions():
    """Generate all missing array functions and set the "array" attributes for
    all cspyce functions.

    This routine can be run multiple times. At each run, it only creates
    whatever is missing.
    """

    # Define an _array function for each cspyce _vector function
    avpairs = []
    funcs = cspyce.get_all_funcs(SPYCE_DICT).values()

    # Do non-alias versions first; otherwise some .array attributes are broken
    for func in funcs:
        if 'alias' in func.__name__:
            continue

        afunc = array_version(func)
        if afunc is func:               # function could not use arrays
            continue

        aname = afunc.__name__
        SPYCE_DICT[aname] = afunc

        if '_vector' in func.__name__:
            avpairs.append((afunc, func))

    for func in funcs:
        if 'alias' not in func.__name__:
            continue

        afunc = array_version(func)
        if afunc is func:               # function could not use arrays
            continue

        aname = afunc.__name__
        SPYCE_DICT[aname] = afunc

        if '_vector' in func.__name__:
            avpairs.append((afunc, func))

    # At this point, every vector function has an array function counterpart.
    # Also, every function has an "array" attribute, which points to itself if
    # there is no array version. However, the new array functions still need
    # internal links to other associated versions.

    # Fill in missing version attributes for every array function
    for (afunc, func) in avpairs:
        _define_missing_versions_for_array(afunc, func)

def _define_missing_versions_for_array(afunc, vfunc):
    """Complete the missing version attributes for a given array function."""

    for (key, version) in vfunc.__dict__.items():
        if not callable(version):
            continue
        if key in ('vector', 'scalar', 'array'):
            afunc.__dict__[key] = version
        else:
            version_name = version.__name__.replace('_vector', '_array')
            afunc.__dict__[key] = SPYCE_DICT[version_name]

################################################################################
