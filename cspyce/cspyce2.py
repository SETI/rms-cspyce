################################################################################
# cspyce/cspyce2.py
#
# This module re-declares every cspyce1 function explicitly, with its list of
# argument names as used by CSPICE. The practical effect is that functions in
# cspyce2 module can be called in a fully Python-like way, the rightmost inputs
# in any order and identified by their names.
#
# Used internally by cspyce; not intended for direct import.
################################################################################

import cspyce.cspyce1 as cspyce1
import keyword

def populate_cspyce2():
    snippets = []
    for name, func in sorted(cspyce1.__dict__.items()):
        if callable(func) and hasattr(func, 'ARGNAMES'):
            argnames = [(x + "_" if keyword.iskeyword(x) else x) for x in func.ARGNAMES]
            arglist = ", ".join(argnames)
            code = f"def {name}({arglist}):\n    return cspyce1.{name}({arglist})\n\n"
            snippets.append(code)
    code = "".join(snippets)

    exec(code, globals(), globals())


# This function makes cspyce2 look the same as cspyce1. It ensures that every
# location in the global dictionary and every function's internal link point to
# a new function of the same name.

def relink_all(new_dict, old_dict):
    old_funcs = {name: defn for name, defn in old_dict.items()
                 if callable(defn) and hasattr(defn, 'SIGNATURE') }
    for name, defn in old_funcs.items():
        assert defn.__name__ == name

    for (name, old_func) in old_funcs.items():
        new_func = new_dict[name]

        # Copy function properties
        new_func.__doc__ = old_func.__doc__
        new_func.__defaults__ = old_func.__defaults__

        # Copy attributes
        old_vars, new_vars = vars(old_func), vars(new_func)
        for (key, value) in old_vars.items():
            assert old_func.__dict__ is vars(old_func)
            if not callable(value):
                new_vars[key] = value
            else:
                # If it's a function, locate a new one with the same name
                new_vars[key] = new_dict[value.__name__]


populate_cspyce2()
relink_all(globals(), cspyce1.__dict__)

################################################################################
