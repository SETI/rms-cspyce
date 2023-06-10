import numpy as np

"""
This file supports the special records that are used for SpiceEllipse, SpacePlane,
SpiceDLADescr, and SpiceDSKDescr.

Ellipses and Planes are created as a subclass of nd.nparray.  They behave exactly like
numpy arrays, except that there field names can also be accessed directly.  So

      ellipse = ..... method that returns ellipse .....
      ellipse = ellipse + 1     # Looks like a numpy array
      print(ellipse.semiMajor)  # Looks like a numpy record
      
DLA and DSK descriptors are implemented only as numpy records.  
       
       dladescr = .... method that returns a SpiceDLADescr
       print(dladescr.isize)

"""

DESCRIPTORS = {
    'SpiceDLADescr': np.dtype([
        ("bwdptr", np.int32),
        ("fwdptr", np.int32),
        ("ibase", np.int32),
        ("isize", np.int32),
        ("dbase", np.int32),
        ("dsize", np.int32),
        ("cbase", np.int32),
        ("csize", np.int32),
    ]),

    'SpiceDSKDescr': np.dtype([
        ('surfce', np.int32),
        ('center', np.int32),
        ('dclass', np.int32),
        ('dtype_', np.int32),  # had to rename from dtype, which is taken.
        ('frmcde', np.int32),
        ('corsys', np.int32),
        ('corpar', np.double, 10),
        ('co1min', np.double),
        ('co1max', np.double),
        ('co2min', np.double),
        ('co2max', np.double),
        ('co3min', np.double),
        ('co3max', np.double),
        ('start',  np.double),
        ('stop',   np.double)]),
}


def create_record(name):
    """Creates a new zeroed record whose descriptor has the indicated name."""
    if name in ('SpiceEllipse', 'SpicePlane'):
        record_type = Ellipse if name == 'SpiceEllipse' else Plane
        return record_type()
    else:
        descriptor = DESCRIPTORS.get(name)
        if not descriptor:
            return None
        array = np.rec.array(None, dtype=descriptor, shape=1)
        array.fill(0)
        return array[0]


def as_record(name, record):
    """
    Attempts to convert the argument into a record whose descriptor has the indicated name.

    If the record argument is okay, then it is returned unchanged.  Otherwise we use
    np.rec.array to try and convert it.
    """
    if name in ('SpiceEllipse', 'SpicePlane'):
        record_type = Ellipse if name == 'SpiceEllipse' else Plane
        return record_type(record)
    else:
        descriptor = DESCRIPTORS.get(name)
        if (descriptor is not None and isinstance(record, np.record)
                and record.dtype == descriptor):
            return record
        try:
            record = np.rec.array(record, descriptor, 1)
            return record
        except ValueError:
            pass
        # Add more attempts to convert it into a record here.
        return None


class _HiddenDescriptor(np.ndarray):
    """
    The secret subclass of np.ndarray that allows Ellipse and Plane to both be
    numpy arrays and to have field access.
    """
    double_size = np.dtype(np.double).itemsize

    def __new__(cls, descriptor, input_array):
        if input_array is None:
            assert descriptor.itemsize % cls.double_size == 0
            input_array = np.zeros(descriptor.itemsize // cls.double_size,
                                   dtype=np.double)
        obj = np.asarray(input_array, dtype=np.double).view(cls)
        obj._descriptor = descriptor
        obj._as_record = np.rec.array(obj, dtype=obj._descriptor)[0]
        return obj
    
    def as_record(self):
        return self._as_record

    def __getattr__(self, item):
        if item in self._descriptor.names:
            return self._as_record[item]
        raise AttributeError


class Ellipse(_HiddenDescriptor):
    descriptor = np.dtype([
        ('center', np.double, 3),
        ('semiMajor', np.double, 3),
        ('semiMinor', np.double, 3),
    ])

    def __new__(cls, input_array=None):
        return super().__new__(cls, cls.descriptor, input_array)


class Plane(_HiddenDescriptor):
    descriptor = np.dtype([
        ('normal', np.double, 3),
        ('constant', np.double),
    ])

    def __new__(cls, input_array=None):
        return super().__new__(cls, cls.descriptor, input_array)


##########################
#
# It is simpler to callback from C to Python if everything is grouped as methods in a
# single class.  Methods can be called using a simple C-string rather than a PyObject*.
#
# The location of this class is known by the function initialize_swig_callback() in
# cspyce_typemaps.i.
#
##########################


class _SwigSupport:
    @staticmethod
    def create_record(name: str):
        return create_record(name)

    @staticmethod
    def as_record(name: str, record):
        return as_record(name, record)

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
