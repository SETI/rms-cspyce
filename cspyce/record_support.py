import numpy as np

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
        ('stop',   np.double)])
}


def create_record(name):
    """ Creates a new empty record whose descriptor has the indicated name. """
    descriptor = DESCRIPTORS.get(name)
    if not descriptor:
        return None
    array = np.rec.array(None, dtype=descriptor, shape=1)
    return array[0]


def as_record(name, record):
    """
    Attempts to convert the record into a record whose descriptor has the indicated name.

    If the record argument is okay, then it is returned unchanged.  Otherwise we use
    np.rec.array to try and convert it.
    """
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

##########################
#
# It is simpler to callback from C to Python if everything is grouped as methods in a
# single class.  Methods can be called by giving the method name as a C string.
#
##########################


class _SwigSupport:
    @staticmethod
    def create_record(name: str, _size=0):
        return create_record(name)

    @staticmethod
    def as_record(name: str, record):
        return as_record(name, record)

    @staticmethod
    def debug(*args):
        print(args)
