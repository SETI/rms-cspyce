import os

import cspyce as cs
from unittests.gettestkernels import download_kernels

"""
Nothing to see here for now
"""

import cspyce as cs
import os

from gettestkernels import TEST_FILE_DIR


def cleanup_kernel(path):
    cs.kclear()
    cs.reset()
    if os.path.isfile(path):
        os.remove(path)  # pragma: no cover
    pass

def test_ekssum():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekssum.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekssum",
        2,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"]
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [
        1, 1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)

    tabnam, nrows, ncols, cnames, cclass, dtype, strln, size, indexd, nullok = cs.ekssum(
        handle, segno)
    assert ncols == 1
    assert nrows == 2
    assert cnames == ["C1"]
    assert tabnam == "TEST_TABLE_EKSSUM"
    assert dtype[0] == 2
    assert bool(indexd[0]) is False  # We currently return an int.
    assert bool(nullok[0]) is True  # Ditto
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)
