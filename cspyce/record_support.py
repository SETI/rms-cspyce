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

def get_new_record(name:str):
    descriptor = DESCRIPTORS.get(name)
    if not descriptor:
        return None
    array = np.rec.array(None, dtype=descriptor, shape=1)
    return array[0]


def verify_record(name, record):
    descriptor = DESCRIPTORS.get(name)
    if descriptor is not None and isinstance(record, np.record) and record.dtype == descriptor:
        return record.base
    try:
        record = np.rec.array(record, descriptor, 1)
        return record.base
    except ValueError:
        pass
    return None

##########################
#
# It is simpler to callback from C to Python if everything is grouped as methods in a
# single class.
#
##########################

class _SwigSupport:
    @staticmethod
    def get_new_record(name: str, _size=0):
        return get_new_record(name)

    @staticmethod
    def verify_record(name: str, record):
        return verify_record(name, record)

    @staticmethod
    def debug(*args):
        print(args)





