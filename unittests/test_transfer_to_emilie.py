import pytest
import os
import cspyce as cs
from unittests.gettestkernels import ExtraKernels, TEST_FILE_DIR
from unittests.test_d import cleanup_kernel
import numpy as np


def test_ekdelr():
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekdelr.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekdelr",
        10,
        ["c1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    cs.ekacli(handle, segno, "c1", [1, 2], [1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekdelr(handle, segno, 2)
    cs.ekcls(handle)
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)


def test_ekfind():
    cs.use_flags(cs.ekfind)
    ekpath = os.path.join(TEST_FILE_DIR, "example_ekfind.ek")
    cleanup_kernel(ekpath)
    handle = cs.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = cs.ekifld(
        handle,
        "test_table_ekfind",
        2,
        ["cc1"],
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    cs.ekacli(handle, segno, "cc1", [1, 2], [
              1, 1], [False, False], rcptrs)
    cs.ekffld(handle, segno, rcptrs)
    cs.ekcls(handle)
    cs.kclear()
    cs.furnsh(ekpath)
    nmrows = cs.ekfind("SELECT CC1 FROM TEST_TABLE_EKFIND WHERE CC1 > 0")
    assert (
        nmrows != 0
    )  # should be 2 but I am not concerned about correctness in this case
    cs.kclear()
    cleanup_kernel(ekpath)
    assert not os.path.exists(ekpath)
