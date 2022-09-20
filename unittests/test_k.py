##########################################################################################
# test_k.py
##########################################################################################

import numpy as np
import unittest
from cspyce import *

class Test_K(unittest.TestCase):

  def runTest(self):
    x = kxtrct("TO", ["FROM", "TO", "BEGINNING", "ENDING"],
               "FROM 1 October 1984 12:00:00 TO 1 January 1987")
    self.assertEqual(x, ["FROM 1 October 1984 12:00:00", True, "1 January 1987"])

    x = kxtrct("FROM", ["FROM", "TO", "BEGINNING", "ENDING"],
           "FROM 1 October 1984 12:00:00 TO 1 January 1987")
    self.assertEqual(x, [" TO 1 January 1987", True, "1 October 1984 12:00:00"])

    x = kxtrct("ADDRESS:", ["ADDRESS:", "PHONE:", "NAME:"],
           "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ")
    self.assertEqual(x, [" PHONE: 354-4321", True, "4800 OAK GROVE DRIVE"])

    x = kxtrct("NAME:", ["ADDRESS:", "PHONE:", "NAME:"],
           "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ")
    self.assertEqual(x, ["ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321", False, ""])

########################################
if __name__ == '__main__':
    unittest.main(verbosity=2)
##########################################################################################
