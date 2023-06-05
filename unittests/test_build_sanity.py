import os
import re
from pathlib import Path

import pytest
import inspect

import cspyce.cspyce1 as cspyce1
import cspyce.cspyce2 as cspyce2

"""
This file contains tests of the build process
"""

def test_sane_argnames_and_signatures():
    """
    For every function in cspyce1, it has the ARGNAMES attribute iff it has the SIGNATURE
    attribute.  The ARGNAMES attribute, the SIGNATURE attribute, and the actual length
    of the function's parameters must be identical.
    """

    # This function finds as many errors as it can, rather than reporting them one by one.
    errors = []
    for name, func in vars(cspyce1).items():
        if callable(func):
            argnames = getattr(func, 'ARGNAMES', None)
            signature = getattr(func, 'SIGNATURE', None)

            if argnames is None and signature is None:
                # We're not interested
                continue

            if argnames is None or signature is None:
                if argnames is None:
                    errors.append(f"cs1.{name}.ARGNAMES is missing")
                else:
                    errors.append(f"cs1.{name}.SIGNATURE is missing")
                continue

            # Both argnames and signature are non-NULL
            parameters = inspect.signature(func).parameters

            if len(argnames) != len(parameters):
                error = f"cs1.{name}.ARGNAMES has length {len(argnames)} but " \
                        f"actually takes {len(parameters)} arguments."
                errors.append(error)

            if len(argnames) != len(signature):
                errors.append(f'cs1.{name}.ARGNAMES has length {len(argnames)}; '
                              f'cs1.{name}.SIGNATURE has length {len(signature)}.')

    if errors:
        error_message = "These functions may have bad Typemaps:\n" + "\n".join(errors)
        pytest.fail(error_message)


def test_cspyce2_default_arguments():
    # Test that every function in cspyce2 has a corresponding function in cspyce1, and
    # that the default arguments match.
    for name, func in vars(cspyce2).items():
        if callable(func) and hasattr(func, 'ARGNAMES'):
            old_func = vars(cspyce1).get(name)
            assert old_func is not None, f"{name} not defined in cspyce1"
            assert func.__defaults__ == old_func.__defaults__, f"{name} has unexpected defaults"


@pytest.mark.parametrize("filename", ["cspyce0_wrap.c", "typemap_samples_wrap.c"])
def test_no_SWIG_ConvertPtr(filename):
    # At this point, we have successfully removed all occurrences of
    #      res<digits> = SWIG_ConvertPtr(......)
    # from the generated swig code. This code is generally caused either because
    # swig is generating "wrap" code for a function that it shouldn't be, or because
    # there is a problem with a function's template. We should take a look if this
    # ever reappears.
    root_dir = Path(os.path.realpath(__file__)).parent.parent
    swig_file_path = root_dir / "swig" / filename
    if not swig_file_path.exists():
        return

    bad_lines = []
    regexp = re.compile(r"\s+res\d+ = SWIG_ConvertPtr\(")
    with open(swig_file_path, "r") as file:
        for lineno, line in enumerate(file, start=1):
            if regexp.search(line):
                bad_lines.append(lineno)
    if bad_lines:
        lines = ", ".join(map(str, bad_lines))
        message = f"Probably a bad template. Call to SWIG_ConvertPtr found on " \
                  f"line{'s' if len(lines) > 1 else ''} {lines} of {filename}."
        pytest.fail(message)



