##########################################################################################
# test_k.py
##########################################################################################

from cspyce import *


def test_kxtrct():
    x = kxtrct("TO", ["FROM", "TO", "BEGINNING", "ENDING"],
               "FROM 1 October 1984 12:00:00 TO 1 January 1987")
    assert x == ["FROM 1 October 1984 12:00:00", True, "1 January 1987"]

    x = kxtrct("FROM", ["FROM", "TO", "BEGINNING", "ENDING"],
               "FROM 1 October 1984 12:00:00 TO 1 January 1987")
    assert x == [" TO 1 January 1987", True, "1 October 1984 12:00:00"]

    x = kxtrct("ADDRESS:", ["ADDRESS:", "PHONE:", "NAME:"],
               "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ")
    assert x == [" PHONE: 354-4321", True, "4800 OAK GROVE DRIVE"]

    x = kxtrct("NAME:", ["ADDRESS:", "PHONE:", "NAME:"],
               "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ")
    assert x == ["ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321", False, ""]
