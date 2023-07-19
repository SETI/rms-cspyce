from typing import Optional
import numpy as np

PROTOTYPES = {name: np.rec.array(None, fields, 1)
              for name, fields in [
                  ('SpiceDLADescr', [
                      ("bwdptr", np.int32),
                      ("fwdptr", np.int32),
                      ("ibase", np.int32),
                      ("isize", np.int32),
                      ("dbase", np.int32),
                      ("dsize", np.int32),
                      ("cbase", np.int32),
                      ("csize", np.int32),
                  ]),

                  ('SpiceDSKDescr', [
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
                      ('stop',   np.double)])]
              }

def create_record(name: str) -> np.record:
    """Creates a new uninitialized record whose descriptor has the indicated name."""
    prototype = PROTOTYPES.get(name)
    assert prototype is not None
    return np.zeros_like(prototype)[0]


def as_record(name: str, record) -> Optional[np.record]:
    """
    Attempts to convert the record into a record whose descriptor has the indicated name.

    If the record argument is okay, then it is returned unchanged.  Otherwise we use
    np.rec.array to try and convert it.
    """
    prototype = PROTOTYPES.get(name)
    assert prototype is not None
    if isinstance(record, np.record) and record.dtype == prototype.dtype:
        return record
    try:
        result = np.rec.array(record, prototype.dtype, 1)
        return result[0]
    except ValueError:
        pass
    # Add more attempts to convert it into a record here.
    return None

