##########################
#
# It is simpler to callback from C to Python if everything is grouped as methods in a
# single class.  Methods can be called using a simple C-string rather than a PyObject*.
#
# The location of this class is known by the function initialize_swig_callback() in
# cspyce_typemaps.i.
#
##########################
import os
from typing import Union


class _SwigPythonCallback:
    @staticmethod
    def create_record(name: str):
        from cspyce import record_support as rs
        return rs.create_record(name)

    @staticmethod
    def as_record(name: str, record):
        from cspyce import record_support as rs
        return rs.as_record(name, record)

    @staticmethod
    def create_spice_cell(typeno: int):
        from cspyce import SpiceCell as sc
        return sc.create_spice_cell(typeno)

    @staticmethod
    def as_spice_cell(typeno: int, record):
        from cspyce import SpiceCell as sc
        return sc.as_spice_cell(typeno, record)

    @staticmethod
    def convert_filename_to_byte_string(file: Union[str, bytes, os.PathLike]) -> bytes:
        return os.fsencode(file)

    @staticmethod
    def debug(*args):
        """
        Useful for debugging or setting a breakpoint in Spice code.

        Typically called with
           PyObject *result = PyObject_CallMethod(SWIG_SUPPORT_CLASS, "debug", format, args...);
           Py_XDECREF(result);
        Format and args might be something like:
           ...., "issO", 23, "message1", "message2", pyArray
        where "i" indicates an integer, "s" a c-string, and O a Python object.
        See Py_BuildValue for complete format details.
        """
        print(args)

