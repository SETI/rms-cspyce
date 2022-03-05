################################################################################
# cspyce/make_cspyce2.py
#
# This program automatically generates the contents of file spice2.py. It fills
# in the names of the input parameters so that cspyce functions can be called
# using keyword inputs in addition to inputs that follow a strictly defined
# order. It also ensures that docstrings and function attributes are carried
# forward to the cspyce2 module.
################################################################################

from __future__ import print_function

HEADER = """
################################################################################
# cspyce/cspyce2.py
################################################################################
# module cspyce.cspyce2
#
# This module re-declares every cspyce1 function explicitly, with its list of
# argument names as used by CSPICE. The practical effect is that functions in
# cspyce2 module can be called in a fully Python-like way, the rightmost inputs
# in any order and identified by their names.
#
# NOTE: This file is generated automatically using program make_cspyce2.py:
#   python make_cspyce2.py > cspyce2.py
#
################################################################################

import sys
PYTHON2 = sys.version_info[0] < 3

# This function makes cspyce2 look the same as cspyce1. It ensures that every
# location in the global dictionary and every function's internal link point
# a new function of the same name.

CSPYCE_FUNCTION_LOOKUP = {}

def relink_all(new_dict, old_dict):

    # Assign a new function to the dictionary at the same location as every
    # cspyce function found in the old dictionary

    dict_names = {}     # maps each function name to its dictionary locations
    old_funcs = {}      # maps each function name to its old function
    for (dict_name, old_func) in old_dict.items():
        if not callable(old_func):
            continue
        if 'SIGNATURE' not in old_func.__dict__:
            continue

        func_name = old_func.__name__
        old_funcs[func_name] = old_func

        if func_name not in dict_names:
            dict_names[func_name] = []

        dict_names[func_name].append(dict_name)

    for (name, keys) in dict_names.items():
        func = new_dict[name]
        for key in keys:
            new_dict[key] = func
            CSPYCE_FUNCTION_LOOKUP[func.__name__] = func

    # Make sure each cspyce function has the same properties and attributes as
    # the one in the old dictionary

    for (name, old_func) in old_funcs.items():
        func = new_dict[name]

        # Copy function properties
        func.__doc__ = old_func.__doc__

        if PYTHON2:
            func.func_defaults = old_func.func_defaults
        else:
            func.__defaults__ = old_func.__defaults__

        # Copy attributes
        for (key, value) in old_func.__dict__.items():
            if not callable(value):
                func.__dict__[key] = value
            else:
                # If it's a function, locate a new one with the same name
                func.__dict__[key] = new_dict[value.__name__]


import cspyce.cspyce1 as cspyce1
from cspyce.cspyce1 import *
"""

import cspyce.cspyce1 as cspyce1

def generate_cspyce2():
    # Get a list by name of every define cspyce function
    arglists = {}  # keyed by name, returns argument name lists
    for (key, func) in cspyce1.__dict__.items():
        if type(func).__name__ != 'function': continue
        if not hasattr(func, 'ARGNAMES'): continue
        arglists[func.__name__] = func.ARGNAMES

    ########################################
    # Start writing
    ########################################

    print(HEADER.lstrip())


    for key in sorted(arglists.keys()):
        argstr = ', '.join(arglists[key])

        print('def %s(%s):' % (key, argstr))
        print('  return cspyce1.%s(%s)' % (key, argstr))
        print()

    print('# Upon execution, re-connect all the lost attibutes and broken links...')
    print()

    print('relink_all(globals(), cspyce1.__dict__)')

    print()
    print(80*'#')

if __name__ == '__main__':
    generate_cspyce2()
